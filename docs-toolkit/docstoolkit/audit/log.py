import json
import sqlite3
from pathlib import Path
from docstoolkit.audit.event import AuditEvent, EventCategory

_SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_log (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    resource TEXT NOT NULL DEFAULT '',
    detail_json TEXT NOT NULL DEFAULT '{}',
    ts TEXT NOT NULL,
    prev_hash TEXT NOT NULL DEFAULT '',
    event_hash TEXT NOT NULL DEFAULT ''
);
"""


class AuditLog:
    """Append-only SQLite audit log with hash chaining."""

    def __init__(self, db_path=None):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()
        self._last_hash = self._load_last_hash()

    def _load_last_hash(self) -> str:
        """Load last event_hash from DB (supports reopening existing DB)."""
        row = self._conn.execute(
            "SELECT event_hash FROM audit_log ORDER BY seq DESC LIMIT 1"
        ).fetchone()
        return row["event_hash"] if row else ""

    def append(self, event: AuditEvent) -> None:
        """Append event; sets prev_hash and seals before insert."""
        event.prev_hash = self._last_hash
        event.seal()
        self._conn.execute(
            "INSERT INTO audit_log "
            "(event_id, category, action, actor, resource, detail_json, "
            " ts, prev_hash, event_hash) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event.event_id,
                event.category.value if isinstance(event.category, EventCategory) else event.category,
                event.action,
                event.actor,
                event.resource,
                json.dumps(event.detail),
                event.ts,
                event.prev_hash,
                event.event_hash,
            ),
        )
        self._conn.commit()
        self._last_hash = event.event_hash

    def get(self, event_id: str) -> AuditEvent | None:
        row = self._conn.execute(
            "SELECT * FROM audit_log WHERE event_id=?", (event_id,)
        ).fetchone()
        return self._row_to_event(row) if row else None

    def list_events(
        self,
        category: EventCategory | None = None,
        actor: str = "",
        limit: int = 100,
    ) -> list:
        """Return events ordered by seq ASC."""
        where = "1=1"
        params: list = []
        if category:
            where += " AND category=?"
            params.append(category.value)
        if actor:
            where += " AND actor=?"
            params.append(actor)
        params.append(limit)
        rows = self._conn.execute(
            f"SELECT * FROM audit_log WHERE {where} ORDER BY seq ASC LIMIT ?",
            params,
        ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]

    def last_hash(self) -> str:
        return self._last_hash

    def close(self):
        self._conn.close()

    def _row_to_event(self, row) -> AuditEvent:
        return AuditEvent(
            event_id=row["event_id"],
            category=EventCategory(row["category"]),
            action=row["action"],
            actor=row["actor"],
            resource=row["resource"],
            detail=json.loads(row["detail_json"] or "{}"),
            ts=row["ts"],
            prev_hash=row["prev_hash"],
            event_hash=row["event_hash"],
        )
