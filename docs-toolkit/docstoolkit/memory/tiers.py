"""Memory tiers: Working, Recall, Archival."""
import json
import math
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


# ── helpers ────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _gen_id(prefix: str = "") -> str:
    return (prefix + uuid.uuid4().hex[:16]) if prefix else uuid.uuid4().hex[:16]


def _token_overlap_score(query: str, text: str) -> float:
    """Simple TF-IDF-style token overlap score."""
    q_tokens = set(query.lower().split())
    if not q_tokens:
        return 0.0
    t_tokens = text.lower().split()
    if not t_tokens:
        return 0.0
    t_set = set(t_tokens)
    overlap = len(q_tokens & t_set)
    # Normalise by geometric mean of lengths
    score = overlap / math.sqrt(len(q_tokens) * len(t_set))
    return score


# ── Working Memory ─────────────────────────────────────────────────────────

@dataclass
class WorkingMemory:
    """In-context message window."""
    messages: list = field(default_factory=list)  # list[dict]: {role, content, ts}
    max_messages: int = 20

    def add(self, role: str, content: str) -> None:
        """Add message, evict oldest if over max_messages."""
        self.messages.append({"role": role, "content": content, "ts": _now_iso()})
        while len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    def to_context(self) -> str:
        """Render as single string for LLM context."""
        lines = []
        for m in self.messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

    def token_estimate(self) -> int:
        """Rough token count: total chars / 4."""
        total = sum(len(m.get("content", "")) for m in self.messages)
        return total // 4


# ── Recall Memory ──────────────────────────────────────────────────────────

@dataclass
class RecallItem:
    id: str
    content: str
    role: str               # "user" | "assistant"
    ts: str                 # ISO timestamp
    tags: list = field(default_factory=list)
    importance: float = 0.5


_RECALL_SCHEMA = """
CREATE TABLE IF NOT EXISTS recall_items (
    id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,
    role        TEXT NOT NULL,
    content     TEXT NOT NULL,
    ts          TEXT NOT NULL,
    tags        TEXT NOT NULL DEFAULT '[]',
    importance  REAL NOT NULL DEFAULT 0.5
);
CREATE INDEX IF NOT EXISTS idx_recall_user ON recall_items(user_id);
CREATE INDEX IF NOT EXISTS idx_recall_ts   ON recall_items(ts);
"""


class RecallMemory:
    """Full searchable history backed by SQLite."""

    def __init__(self, db_path: str = ":memory:", user_id: str = "default"):
        self._user_id = user_id
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_RECALL_SCHEMA)
        self._conn.commit()

    def store(self, item: RecallItem) -> str:
        """Persist item. Returns item.id."""
        self._conn.execute(
            "INSERT OR REPLACE INTO recall_items "
            "(id, user_id, role, content, ts, tags, importance) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (item.id, self._user_id, item.role, item.content,
             item.ts, json.dumps(item.tags, ensure_ascii=False), item.importance),
        )
        self._conn.commit()
        return item.id

    def search(self, query: str, top_k: int = 5) -> list:
        """TF-IDF token overlap search across stored items for this user."""
        rows = self._conn.execute(
            "SELECT * FROM recall_items WHERE user_id = ? ORDER BY ts DESC",
            (self._user_id,),
        ).fetchall()
        if not rows:
            return []
        scored = []
        for row in rows:
            score = _token_overlap_score(query, row["content"])
            scored.append((score, row))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [self._row_to_item(r) for _, r in scored[:top_k]]

    def get(self, item_id: str):
        """Return RecallItem or None."""
        row = self._conn.execute(
            "SELECT * FROM recall_items WHERE id = ? AND user_id = ?",
            (item_id, self._user_id),
        ).fetchone()
        return self._row_to_item(row) if row else None

    def list_recent(self, limit: int = 20) -> list:
        """Return most recent items first."""
        rows = self._conn.execute(
            "SELECT * FROM recall_items WHERE user_id = ? "
            "ORDER BY ts DESC LIMIT ?",
            (self._user_id, limit),
        ).fetchall()
        return [self._row_to_item(r) for r in rows]

    def count(self) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM recall_items WHERE user_id = ?",
            (self._user_id,),
        ).fetchone()
        return row["n"] if row else 0

    def _row_to_item(self, row) -> "RecallItem":
        return RecallItem(
            id=row["id"],
            content=row["content"],
            role=row["role"],
            ts=row["ts"],
            tags=json.loads(row["tags"] or "[]"),
            importance=row["importance"],
        )


# ── Archival Memory ─────────────────────────────────────────────────────────

@dataclass
class ArchivalFact:
    id: str
    text: str               # compressed fact / preference
    tags: list = field(default_factory=list)
    importance: float = 0.5
    source_ids: list = field(default_factory=list)  # recall item ids
    created_ts: str = ""


_ARCHIVAL_SCHEMA = """
CREATE TABLE IF NOT EXISTS archival_facts (
    id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,
    text        TEXT NOT NULL,
    tags        TEXT NOT NULL DEFAULT '[]',
    importance  REAL NOT NULL DEFAULT 0.5,
    source_ids  TEXT NOT NULL DEFAULT '[]',
    created_ts  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_arch_user ON archival_facts(user_id);
CREATE INDEX IF NOT EXISTS idx_arch_ts   ON archival_facts(created_ts);
"""


class ArchivalMemory:
    """Long-term compressed facts backed by SQLite."""

    def __init__(self, db_path: str = ":memory:", user_id: str = "default"):
        self._user_id = user_id
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_ARCHIVAL_SCHEMA)
        self._conn.commit()

    def archive(self, text: str, tags: list = None,
                importance: float = 0.5,
                source_ids: list = None) -> str:
        """Store fact. Returns fact_id."""
        fact_id = _gen_id("fact_")
        ts = _now_iso()
        self._conn.execute(
            "INSERT INTO archival_facts "
            "(id, user_id, text, tags, importance, source_ids, created_ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (fact_id, self._user_id, text,
             json.dumps(tags or [], ensure_ascii=False),
             importance,
             json.dumps(source_ids or [], ensure_ascii=False),
             ts),
        )
        self._conn.commit()
        return fact_id

    def search(self, query: str, top_k: int = 5) -> list:
        """Token overlap search."""
        rows = self._conn.execute(
            "SELECT * FROM archival_facts WHERE user_id = ? ORDER BY created_ts DESC",
            (self._user_id,),
        ).fetchall()
        if not rows:
            return []
        scored = []
        for row in rows:
            score = _token_overlap_score(query, row["text"])
            scored.append((score, row))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [self._row_to_fact(r) for _, r in scored[:top_k]]

    def get(self, fact_id: str):
        """Return ArchivalFact or None."""
        row = self._conn.execute(
            "SELECT * FROM archival_facts WHERE id = ? AND user_id = ?",
            (fact_id, self._user_id),
        ).fetchone()
        return self._row_to_fact(row) if row else None

    def forget(self, fact_id: str) -> bool:
        """Delete fact. Returns True if existed."""
        cursor = self._conn.execute(
            "DELETE FROM archival_facts WHERE id = ? AND user_id = ?",
            (fact_id, self._user_id),
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def list_by_tag(self, tag: str) -> list:
        """Return all facts that contain tag."""
        rows = self._conn.execute(
            "SELECT * FROM archival_facts WHERE user_id = ? ORDER BY created_ts DESC",
            (self._user_id,),
        ).fetchall()
        result = []
        for row in rows:
            tags = json.loads(row["tags"] or "[]")
            if tag in tags:
                result.append(self._row_to_fact(row))
        return result

    def count(self) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM archival_facts WHERE user_id = ?",
            (self._user_id,),
        ).fetchone()
        return row["n"] if row else 0

    def _row_to_fact(self, row) -> "ArchivalFact":
        return ArchivalFact(
            id=row["id"],
            text=row["text"],
            tags=json.loads(row["tags"] or "[]"),
            importance=row["importance"],
            source_ids=json.loads(row["source_ids"] or "[]"),
            created_ts=row["created_ts"],
        )
