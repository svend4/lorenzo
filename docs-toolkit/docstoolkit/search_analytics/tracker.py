import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

@dataclass
class QueryRecord:
    query: str
    result_count: int
    latency_ms: float
    user_id: str = ""
    session_id: str = ""
    ts: str = ""
    clicked_doc_id: str = ""    # if user clicked a result

    def __post_init__(self):
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')

    def is_zero_result(self) -> bool:
        return self.result_count == 0


_SCHEMA = """
CREATE TABLE IF NOT EXISTS query_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    result_count INTEGER NOT NULL DEFAULT 0,
    latency_ms REAL NOT NULL DEFAULT 0,
    user_id TEXT NOT NULL DEFAULT '',
    session_id TEXT NOT NULL DEFAULT '',
    ts TEXT NOT NULL,
    clicked_doc_id TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_ts ON query_log(ts DESC);
CREATE INDEX IF NOT EXISTS idx_query ON query_log(query);
"""


class QueryTracker:
    """SQLite-backed query tracker."""

    def __init__(self, db_path=None):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def record(self, record: QueryRecord) -> None:
        self._conn.execute(
            "INSERT INTO query_log "
            "(query, result_count, latency_ms, user_id, session_id, ts, clicked_doc_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (record.query, record.result_count, record.latency_ms,
             record.user_id, record.session_id, record.ts, record.clicked_doc_id),
        )
        self._conn.commit()

    def total_queries(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM query_log").fetchone()[0]

    def zero_result_queries(self) -> list:
        """Return list of (query, count) pairs where result_count=0, ordered by count desc."""
        rows = self._conn.execute(
            "SELECT query, COUNT(*) as cnt FROM query_log "
            "WHERE result_count=0 GROUP BY query ORDER BY cnt DESC"
        ).fetchall()
        return [(r["query"], r["cnt"]) for r in rows]

    def top_queries(self, limit: int = 10) -> list:
        """Return list of (query, count) pairs, ordered by count desc."""
        rows = self._conn.execute(
            "SELECT query, COUNT(*) as cnt FROM query_log "
            "GROUP BY query ORDER BY cnt DESC LIMIT ?", (limit,)
        ).fetchall()
        return [(r["query"], r["cnt"]) for r in rows]

    def avg_latency_ms(self) -> float:
        """Average latency across all queries."""
        result = self._conn.execute(
            "SELECT AVG(latency_ms) FROM query_log"
        ).fetchone()[0]
        return result or 0.0

    def click_through_rate(self) -> float:
        """Fraction of queries where clicked_doc_id is non-empty."""
        total = self.total_queries()
        if total == 0:
            return 0.0
        clicked = self._conn.execute(
            "SELECT COUNT(*) FROM query_log WHERE clicked_doc_id != ''"
        ).fetchone()[0]
        return clicked / total

    def close(self):
        self._conn.close()
