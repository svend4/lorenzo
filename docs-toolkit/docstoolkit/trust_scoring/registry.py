"""SQLite-backed TrustRegistry for persisting and querying TrustScore objects."""
from __future__ import annotations

import json
import sqlite3
from typing import Optional

from docstoolkit.trust_scoring.signals import SignalScore, TrustSignal
from docstoolkit.trust_scoring.scorer import TrustScore


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------

def _signals_to_json(signals: list[SignalScore]) -> str:
    data = [
        {
            "signal": s.signal.value,
            "raw_value": s.raw_value,
            "normalized": s.normalized,
            "weight": s.weight,
        }
        for s in signals
    ]
    return json.dumps(data)


def _json_to_signals(text: str) -> list[SignalScore]:
    data = json.loads(text)
    return [
        SignalScore(
            signal=TrustSignal(item["signal"]),
            raw_value=item["raw_value"],
            normalized=item["normalized"],
            weight=item["weight"],
        )
        for item in data
    ]


def _row_to_score(row: tuple) -> TrustScore:
    doc_id, overall, grade, signals_json = row
    return TrustScore(
        doc_id=doc_id,
        overall=overall,
        grade=grade,
        signals=_json_to_signals(signals_json),
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_DDL = """
CREATE TABLE IF NOT EXISTS trust_scores (
    doc_id   TEXT PRIMARY KEY,
    overall  REAL NOT NULL,
    grade    TEXT NOT NULL,
    signals  TEXT NOT NULL
);
"""


class TrustRegistry:
    """Persist and query TrustScore objects using SQLite."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(_DDL)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def save(self, score: TrustScore) -> None:
        """Insert or replace a TrustScore in the registry."""
        self._conn.execute(
            """
            INSERT OR REPLACE INTO trust_scores (doc_id, overall, grade, signals)
            VALUES (?, ?, ?, ?)
            """,
            (score.doc_id, score.overall, score.grade, _signals_to_json(score.signals)),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, doc_id: str) -> Optional[TrustScore]:
        """Return the TrustScore for *doc_id*, or None if not found."""
        cur = self._conn.execute(
            "SELECT doc_id, overall, grade, signals FROM trust_scores WHERE doc_id = ?",
            (doc_id,),
        )
        row = cur.fetchone()
        return _row_to_score(row) if row else None

    def top_trusted(self, n: int = 10) -> list[TrustScore]:
        """Return up to *n* scores sorted by overall descending."""
        cur = self._conn.execute(
            "SELECT doc_id, overall, grade, signals FROM trust_scores "
            "ORDER BY overall DESC LIMIT ?",
            (n,),
        )
        return [_row_to_score(row) for row in cur.fetchall()]

    def low_trust(self, n: int = 10, threshold: float = 0.4) -> list[TrustScore]:
        """Return up to *n* scores where overall < *threshold*, sorted asc."""
        cur = self._conn.execute(
            "SELECT doc_id, overall, grade, signals FROM trust_scores "
            "WHERE overall < ? ORDER BY overall ASC LIMIT ?",
            (threshold, n),
        )
        return [_row_to_score(row) for row in cur.fetchall()]

    def stats(self) -> dict:
        """Return aggregate statistics over all stored scores.

        Keys:
        - ``total``: number of documents
        - ``avg_score``: average overall score (float, 0 if empty)
        - ``grade_distribution``: dict mapping grade letter → count
        """
        cur = self._conn.execute(
            "SELECT COUNT(*), AVG(overall) FROM trust_scores"
        )
        total, avg = cur.fetchone()
        total = total or 0
        avg = avg or 0.0

        grade_cur = self._conn.execute(
            "SELECT grade, COUNT(*) FROM trust_scores GROUP BY grade"
        )
        grade_distribution: dict[str, int] = {
            row[0]: row[1] for row in grade_cur.fetchall()
        }

        return {
            "total": total,
            "avg_score": avg,
            "grade_distribution": grade_distribution,
        }

    # ------------------------------------------------------------------
    # Resource management
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        self._conn.close()

    def __enter__(self) -> "TrustRegistry":
        return self

    def __exit__(self, *args) -> None:
        self.close()
