"""Read-receipt + reading-time tracking backed by SQLite.

All storage is in ``.docstoolkit/reads.sqlite``.
No external dependencies — stdlib only (sqlite3, math, re, datetime).
"""
from __future__ import annotations

import math
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# ReadStatus literals
# ---------------------------------------------------------------------------
ReadStatus = str   # "unread" | "read" | "skipped" | "saved"

UNREAD: ReadStatus = "unread"
READ: ReadStatus = "read"
SKIPPED: ReadStatus = "skipped"
SAVED: ReadStatus = "saved"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------
@dataclass
class ReadRecord:
    user: str
    doc_id: str
    status: str
    ts: str
    reading_time_sec: int = 0


# ---------------------------------------------------------------------------
# SQLite schema
# ---------------------------------------------------------------------------
_SCHEMA = """
CREATE TABLE IF NOT EXISTS reads (
    user              TEXT NOT NULL,
    doc_id            TEXT NOT NULL,
    status            TEXT NOT NULL,
    ts                TEXT NOT NULL,
    reading_time_sec  INT  NOT NULL DEFAULT 0,
    PRIMARY KEY (user, doc_id)
);
CREATE INDEX IF NOT EXISTS idx_reads_user ON reads(user);
CREATE INDEX IF NOT EXISTS idx_reads_status ON reads(user, status);
CREATE INDEX IF NOT EXISTS idx_reads_ts ON reads(ts);
"""


# ---------------------------------------------------------------------------
# ReadStore
# ---------------------------------------------------------------------------
class ReadStore:
    """Persistent store for read-receipts and reading-time data.

    Database is created at ``<db_path>`` (default ``.docstoolkit/reads.sqlite``
    relative to the current working directory).
    """

    def __init__(self, db_path: Path | None = None) -> None:
        if db_path is None:
            db_path = Path(".docstoolkit") / "reads.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------
    def mark(
        self,
        user: str,
        doc_id: str,
        status: str,
        reading_time_sec: int = 0,
    ) -> None:
        """Insert or replace a read record (upsert by primary key)."""
        ts = datetime.now().isoformat(timespec="seconds")
        self.conn.execute(
            """
            INSERT INTO reads (user, doc_id, status, ts, reading_time_sec)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user, doc_id) DO UPDATE SET
                status           = excluded.status,
                ts               = excluded.ts,
                reading_time_sec = excluded.reading_time_sec
            """,
            (user, doc_id, status, ts, reading_time_sec),
        )
        self.conn.commit()

    def get_status(self, user: str, doc_id: str) -> str:
        """Return the status string, or ``"unread"`` if no record exists."""
        row = self.conn.execute(
            "SELECT status FROM reads WHERE user = ? AND doc_id = ?",
            (user, doc_id),
        ).fetchone()
        return row["status"] if row else UNREAD

    def list_by_status(self, user: str, status: str) -> list[ReadRecord]:
        """Return all records for *user* with the given *status*."""
        rows = self.conn.execute(
            "SELECT * FROM reads WHERE user = ? AND status = ? ORDER BY ts DESC",
            (user, status),
        ).fetchall()
        return [_row_to_record(r) for r in rows]

    def reading_history(self, user: str, limit: int = 50) -> list[ReadRecord]:
        """Return the most recent *limit* records for *user*, newest first."""
        rows = self.conn.execute(
            "SELECT * FROM reads WHERE user = ? ORDER BY ts DESC LIMIT ?",
            (user, limit),
        ).fetchall()
        return [_row_to_record(r) for r in rows]

    def stats(self, user: str) -> dict[str, int]:
        """Return ``{status: count}`` breakdown for *user*."""
        rows = self.conn.execute(
            "SELECT status, COUNT(*) as cnt FROM reads WHERE user = ? GROUP BY status",
            (user,),
        ).fetchall()
        return {r["status"]: r["cnt"] for r in rows}


# ---------------------------------------------------------------------------
# estimate_reading_time
# ---------------------------------------------------------------------------
def estimate_reading_time(
    text: str,
    wpm_ru: int = 200,
    wpm_en: int = 250,
) -> int:
    """Estimate reading time in seconds.

    Detects RU ratio by counting Cyrillic characters vs total alphabetic.
    ``wpm = wpm_ru * ru_ratio + wpm_en * (1 - ru_ratio)``
    Returns ``ceil(word_count / wpm * 60)``.
    """
    cyrillic_chars = len(re.findall(r"[а-яёА-ЯЁ]", text))
    alpha_chars = len(re.findall(r"[a-zA-Zа-яёА-ЯЁ]", text))
    ru_ratio = (cyrillic_chars / alpha_chars) if alpha_chars > 0 else 0.0
    wpm = wpm_ru * ru_ratio + wpm_en * (1.0 - ru_ratio)

    words = text.split()
    word_count = len(words)
    if word_count == 0 or wpm == 0:
        return 0
    return math.ceil(word_count / wpm * 60)


# ---------------------------------------------------------------------------
# recommendations_for
# ---------------------------------------------------------------------------
def recommendations_for(
    user: str,
    store: ReadStore,
    citation_graph: dict[str, list[str]],
    top_k: int = 10,
) -> list[tuple[str, float, str]]:
    """Recommend unread docs based on the user's reading history + citation graph.

    *citation_graph* maps ``doc_id → [cited_doc_id, ...]``.

    Scoring: if the graph contains a ``pagerank`` key (``{doc_id: float}``),
    use that score; otherwise use uniform score of 1.0.

    Returns ``[(doc_id, score, reason), ...]`` sorted by score descending,
    deduplicated, at most *top_k* entries.
    """
    # Collect read doc_ids
    read_records = store.reading_history(user, limit=10_000)
    read_ids: set[str] = {r.doc_id for r in read_records if r.status == READ}

    # Optional PageRank lookup
    pagerank: dict[str, float] = {}
    if "pagerank" in citation_graph:
        raw_pr = citation_graph["pagerank"]
        if isinstance(raw_pr, dict):
            pagerank = {str(k): float(v) for k, v in raw_pr.items()}

    # Build candidates: doc cited by a read doc, not yet read
    candidates: dict[str, tuple[float, str]] = {}   # doc_id → (best_score, reason)

    for read_doc in read_ids:
        cited = citation_graph.get(read_doc, [])
        for cited_doc in cited:
            if isinstance(cited_doc, str) and cited_doc not in read_ids:
                score = pagerank.get(cited_doc, 1.0)
                reason = f"cited by {read_doc}"
                if cited_doc not in candidates or candidates[cited_doc][0] < score:
                    candidates[cited_doc] = (score, reason)

    sorted_candidates = sorted(
        candidates.items(), key=lambda kv: kv[1][0], reverse=True
    )
    return [
        (doc_id, score, reason)
        for doc_id, (score, reason) in sorted_candidates[:top_k]
    ]


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------
def _row_to_record(row: sqlite3.Row) -> ReadRecord:
    return ReadRecord(
        user=row["user"],
        doc_id=row["doc_id"],
        status=row["status"],
        ts=row["ts"],
        reading_time_sec=row["reading_time_sec"] or 0,
    )
