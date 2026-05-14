"""SQLite-backed access log for recording and querying API/resource access events."""
import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Optional
from uuid import uuid4


@dataclass
class AccessEvent:
    """Represents a single access event."""

    event_id: str = field(default_factory=lambda: uuid4().hex[:12])
    timestamp: float = 0.0
    user_id: str = ""
    resource: str = ""
    action: str = ""
    status_code: int = 200
    duration_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class LogStats:
    """Aggregated statistics over a set of access events."""

    total_events: int = 0
    unique_users: int = 0
    unique_resources: int = 0
    error_count: int = 0          # status_code >= 400
    avg_duration_ms: float = 0.0
    by_action: dict = field(default_factory=dict)    # action → count
    by_status: dict = field(default_factory=dict)    # status_code → count


class AccessLog:
    """SQLite-backed access log.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an
        in-memory database (default).
    now_fn:
        Callable that returns the current time as a ``float`` (Unix
        timestamp).  Defaults to :func:`time.time`.  Inject a custom
        function in tests to control virtual time.
    """

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS access_log (
        event_id    TEXT PRIMARY KEY,
        timestamp   REAL,
        user_id     TEXT,
        resource    TEXT,
        action      TEXT,
        status_code INTEGER DEFAULT 200,
        duration_ms REAL    DEFAULT 0,
        metadata    TEXT    DEFAULT '{}'
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_al_user_id    ON access_log (user_id)",
        "CREATE INDEX IF NOT EXISTS idx_al_resource   ON access_log (resource)",
        "CREATE INDEX IF NOT EXISTS idx_al_action     ON access_log (action)",
        "CREATE INDEX IF NOT EXISTS idx_al_timestamp  ON access_log (timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_al_status     ON access_log (status_code)",
    ]

    def __init__(
        self,
        db_path: str = ":memory:",
        now_fn: Optional[Callable[[], float]] = None,
    ) -> None:
        self._db_path = db_path
        self._now_fn: Callable[[], float] = now_fn if now_fn is not None else time.time
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._setup()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL")
            cur.execute(self._CREATE_TABLE)
            for stmt in self._CREATE_INDEXES:
                cur.execute(stmt)
            self._conn.commit()

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> AccessEvent:
        return AccessEvent(
            event_id=row["event_id"],
            timestamp=row["timestamp"],
            user_id=row["user_id"],
            resource=row["resource"],
            action=row["action"],
            status_code=row["status_code"],
            duration_ms=row["duration_ms"],
            metadata=json.loads(row["metadata"]),
        )

    @staticmethod
    def _build_where(
        clauses: "list[str]",
        params: list,
        user_id: Optional[str] = None,
        resource: Optional[str] = None,
        action: Optional[str] = None,
        status_code: Optional[int] = None,
        since: Optional[float] = None,
        until: Optional[float] = None,
    ) -> str:
        if user_id is not None:
            clauses.append("user_id = ?")
            params.append(user_id)
        if resource is not None:
            clauses.append("resource = ?")
            params.append(resource)
        if action is not None:
            clauses.append("action = ?")
            params.append(action)
        if status_code is not None:
            clauses.append("status_code = ?")
            params.append(status_code)
        if since is not None:
            clauses.append("timestamp >= ?")
            params.append(since)
        if until is not None:
            clauses.append("timestamp <= ?")
            params.append(until)
        return ("WHERE " + " AND ".join(clauses)) if clauses else ""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record(
        self,
        user_id: str,
        resource: str,
        action: str,
        status_code: int = 200,
        duration_ms: float = 0.0,
        metadata: Optional[dict] = None,
    ) -> AccessEvent:
        """Record an access event and return it."""
        event = AccessEvent(
            timestamp=self._now_fn(),
            user_id=user_id,
            resource=resource,
            action=action,
            status_code=status_code,
            duration_ms=duration_ms,
            metadata=metadata if metadata is not None else {},
        )
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO access_log
                    (event_id, timestamp, user_id, resource, action,
                     status_code, duration_ms, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.timestamp,
                    event.user_id,
                    event.resource,
                    event.action,
                    event.status_code,
                    event.duration_ms,
                    json.dumps(event.metadata),
                ),
            )
            self._conn.commit()
        return event

    def query(
        self,
        user_id: Optional[str] = None,
        resource: Optional[str] = None,
        action: Optional[str] = None,
        status_code: Optional[int] = None,
        since: Optional[float] = None,
        until: Optional[float] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> "list[AccessEvent]":
        """Return events matching filters, ordered by timestamp DESC."""
        clauses: list[str] = []
        params: list = []
        where = self._build_where(
            clauses, params,
            user_id=user_id,
            resource=resource,
            action=action,
            status_code=status_code,
            since=since,
            until=until,
        )
        params.extend([limit, offset])
        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM access_log {where} "
                f"ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                params,
            ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def stats(
        self,
        user_id: Optional[str] = None,
        since: Optional[float] = None,
        until: Optional[float] = None,
    ) -> LogStats:
        """Return aggregated statistics, optionally filtered by user_id/time range."""
        clauses: list[str] = []
        params: list = []
        where = self._build_where(
            clauses, params,
            user_id=user_id,
            since=since,
            until=until,
        )

        with self._lock:
            # Scalar aggregates
            row = self._conn.execute(
                f"""
                SELECT
                    COUNT(*)                              AS total_events,
                    COUNT(DISTINCT user_id)               AS unique_users,
                    COUNT(DISTINCT resource)              AS unique_resources,
                    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END)
                                                          AS error_count,
                    AVG(duration_ms)                      AS avg_duration_ms
                FROM access_log {where}
                """,
                params,
            ).fetchone()

            # by_action breakdown
            action_rows = self._conn.execute(
                f"SELECT action, COUNT(*) AS cnt FROM access_log {where} "
                f"GROUP BY action",
                params,
            ).fetchall()

            # by_status breakdown
            status_rows = self._conn.execute(
                f"SELECT status_code, COUNT(*) AS cnt FROM access_log {where} "
                f"GROUP BY status_code",
                params,
            ).fetchall()

        total = row["total_events"] or 0
        return LogStats(
            total_events=total,
            unique_users=row["unique_users"] or 0,
            unique_resources=row["unique_resources"] or 0,
            error_count=row["error_count"] or 0,
            avg_duration_ms=row["avg_duration_ms"] or 0.0,
            by_action={r["action"]: r["cnt"] for r in action_rows},
            by_status={r["status_code"]: r["cnt"] for r in status_rows},
        )

    def get(self, event_id: str) -> Optional[AccessEvent]:
        """Return the event with *event_id*, or None if not found."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM access_log WHERE event_id = ?", (event_id,)
            ).fetchone()
        return self._row_to_event(row) if row else None

    def count(
        self,
        user_id: Optional[str] = None,
        resource: Optional[str] = None,
    ) -> int:
        """Return count of matching events."""
        clauses: list[str] = []
        params: list = []
        where = self._build_where(clauses, params, user_id=user_id, resource=resource)
        with self._lock:
            row = self._conn.execute(
                f"SELECT COUNT(*) FROM access_log {where}", params
            ).fetchone()
        return row[0]

    def delete_before(self, timestamp: float) -> int:
        """Delete events with timestamp < *timestamp*. Returns count deleted."""
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM access_log WHERE timestamp < ?", (timestamp,)
            )
            self._conn.commit()
            return cur.rowcount

    def close(self) -> None:
        """Close the underlying database connection."""
        with self._lock:
            self._conn.close()
