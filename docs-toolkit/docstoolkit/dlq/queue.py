import json
import sqlite3
from pathlib import Path
from docstoolkit.dlq.item import DeadLetterItem, FailureReason

_SCHEMA = """
CREATE TABLE IF NOT EXISTS dlq (
    job_id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    reason TEXT NOT NULL,
    error_message TEXT NOT NULL DEFAULT '',
    attempt_count INTEGER NOT NULL DEFAULT 1,
    first_failure_ts TEXT NOT NULL,
    last_failure_ts TEXT NOT NULL,
    resolved INTEGER NOT NULL DEFAULT 0,
    tags_json TEXT NOT NULL DEFAULT '[]'
);
"""

class DeadLetterQueue:
    """SQLite-backed dead letter queue."""

    def __init__(self, db_path: Path | str | None = None):
        if db_path is None:
            db_path = ":memory:"
        self._path = str(db_path)
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def push(self, item: DeadLetterItem) -> None:
        """Insert or replace item."""
        self._conn.execute(
            "INSERT OR REPLACE INTO dlq "
            "(job_id, payload, reason, error_message, attempt_count, "
            " first_failure_ts, last_failure_ts, resolved, tags_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (item.job_id, item.payload, item.reason.value, item.error_message,
             item.attempt_count, item.first_failure_ts, item.last_failure_ts,
             int(item.resolved), json.dumps(item.tags)),
        )
        self._conn.commit()

    def get(self, job_id: str) -> DeadLetterItem | None:
        """Fetch by job_id."""
        row = self._conn.execute(
            "SELECT * FROM dlq WHERE job_id = ?", (job_id,)
        ).fetchone()
        return self._row_to_item(row) if row else None

    def list_pending(self, limit: int = 50) -> list:
        """Return unresolved items, oldest first."""
        rows = self._conn.execute(
            "SELECT * FROM dlq WHERE resolved = 0 "
            "ORDER BY first_failure_ts ASC LIMIT ?", (limit,)
        ).fetchall()
        return [self._row_to_item(r) for r in rows]

    def resolve(self, job_id: str) -> bool:
        """Mark job as resolved. Returns True if found."""
        cur = self._conn.execute(
            "UPDATE dlq SET resolved = 1 WHERE job_id = ?", (job_id,)
        )
        self._conn.commit()
        return cur.rowcount > 0

    def increment_attempt(self, job_id: str) -> bool:
        """Increment attempt count and update last_failure_ts."""
        from datetime import datetime
        ts = datetime.now().isoformat(timespec='seconds')
        cur = self._conn.execute(
            "UPDATE dlq SET attempt_count = attempt_count + 1, last_failure_ts = ? "
            "WHERE job_id = ?", (ts, job_id)
        )
        self._conn.commit()
        return cur.rowcount > 0

    def stats(self) -> dict:
        """Return {total, pending, resolved} counts."""
        total = self._conn.execute("SELECT COUNT(*) FROM dlq").fetchone()[0]
        pending = self._conn.execute(
            "SELECT COUNT(*) FROM dlq WHERE resolved = 0"
        ).fetchone()[0]
        return {"total": total, "pending": pending, "resolved": total - pending}

    def purge_resolved(self) -> int:
        """Delete all resolved items. Returns count deleted."""
        cur = self._conn.execute("DELETE FROM dlq WHERE resolved = 1")
        self._conn.commit()
        return cur.rowcount

    def close(self) -> None:
        self._conn.close()

    def _row_to_item(self, row) -> DeadLetterItem:
        return DeadLetterItem(
            job_id=row["job_id"],
            payload=row["payload"],
            reason=FailureReason(row["reason"]),
            error_message=row["error_message"],
            attempt_count=row["attempt_count"],
            first_failure_ts=row["first_failure_ts"],
            last_failure_ts=row["last_failure_ts"],
            resolved=bool(row["resolved"]),
            tags=json.loads(row["tags_json"] or "[]"),
        )
