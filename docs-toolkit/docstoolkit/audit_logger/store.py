"""SQLite-backed audit event store."""
import json
import sqlite3
from pathlib import Path
from typing import Optional

from docstoolkit.audit_logger.event import AuditAction, AuditEvent


class AuditStore:
    """Persist and query AuditEvents in a SQLite database."""

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS audit_log (
        event_id    TEXT PRIMARY KEY,
        action      TEXT NOT NULL,
        actor       TEXT NOT NULL,
        resource    TEXT NOT NULL,
        resource_id TEXT NOT NULL DEFAULT '',
        details     TEXT NOT NULL DEFAULT '{}',
        outcome     TEXT NOT NULL DEFAULT 'success',
        ts          REAL NOT NULL,
        ip_address  TEXT NOT NULL DEFAULT '',
        session_id  TEXT NOT NULL DEFAULT ''
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_log (actor)",
        "CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log (action)",
        "CREATE INDEX IF NOT EXISTS idx_audit_ts     ON audit_log (ts)",
    ]

    def __init__(self, db_path: "str | Path" = ":memory:") -> None:
        self._db_path = str(db_path)
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._setup()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        cur = self._conn.cursor()
        cur.execute(self._CREATE_TABLE)
        for stmt in self._CREATE_INDEXES:
            cur.execute(stmt)
        self._conn.commit()

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> AuditEvent:
        return AuditEvent(
            event_id=row["event_id"],
            action=AuditAction(row["action"]),
            actor=row["actor"],
            resource=row["resource"],
            resource_id=row["resource_id"],
            details=json.loads(row["details"]),
            outcome=row["outcome"],
            ts=row["ts"],
            ip_address=row["ip_address"],
            session_id=row["session_id"],
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record(self, event: AuditEvent) -> None:
        """Persist *event* to the store."""
        self._conn.execute(
            """
            INSERT OR REPLACE INTO audit_log
                (event_id, action, actor, resource, resource_id, details,
                 outcome, ts, ip_address, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.action.value,
                event.actor,
                event.resource,
                event.resource_id,
                json.dumps(event.details),
                event.outcome,
                event.ts,
                event.ip_address,
                event.session_id,
            ),
        )
        self._conn.commit()

    def get(self, event_id: str) -> Optional[AuditEvent]:
        """Return the event with *event_id*, or None if not found."""
        row = self._conn.execute(
            "SELECT * FROM audit_log WHERE event_id = ?", (event_id,)
        ).fetchone()
        return self._row_to_event(row) if row else None

    def query(
        self,
        actor: Optional[str] = None,
        action: Optional[AuditAction] = None,
        resource: Optional[str] = None,
        since: Optional[float] = None,
        until: Optional[float] = None,
        limit: int = 100,
    ) -> "list[AuditEvent]":
        """Return events matching ALL supplied filters, newest-first."""
        clauses: list[str] = []
        params: list = []

        if actor is not None:
            clauses.append("actor = ?")
            params.append(actor)
        if action is not None:
            clauses.append("action = ?")
            params.append(action.value)
        if resource is not None:
            clauses.append("resource = ?")
            params.append(resource)
        if since is not None:
            clauses.append("ts >= ?")
            params.append(since)
        if until is not None:
            clauses.append("ts <= ?")
            params.append(until)

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        params.append(limit)

        rows = self._conn.execute(
            f"SELECT * FROM audit_log {where} ORDER BY ts DESC LIMIT ?",
            params,
        ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def count(
        self,
        actor: Optional[str] = None,
        action: Optional[AuditAction] = None,
    ) -> int:
        """Count events, optionally filtered by actor and/or action."""
        clauses: list[str] = []
        params: list = []

        if actor is not None:
            clauses.append("actor = ?")
            params.append(actor)
        if action is not None:
            clauses.append("action = ?")
            params.append(action.value)

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        row = self._conn.execute(
            f"SELECT COUNT(*) FROM audit_log {where}", params
        ).fetchone()
        return row[0]

    def recent(self, n: int = 20) -> "list[AuditEvent]":
        """Return the *n* most recent events, newest-first."""
        rows = self._conn.execute(
            "SELECT * FROM audit_log ORDER BY ts DESC LIMIT ?", (n,)
        ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
