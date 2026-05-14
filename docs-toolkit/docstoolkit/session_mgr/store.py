"""SQLite-backed SessionStore."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from docstoolkit.session_mgr.session import Session, SessionStatus


class SessionStore:
    """Persistent SQLite-backed session store.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an in-memory
        database (default).
    ttl_seconds:
        Default time-to-live in seconds applied when creating sessions.
        Pass ``0`` to disable expiry by default.
    """

    def __init__(
        self,
        db_path: str | Path = ":memory:",
        ttl_seconds: float = 3600.0,
    ) -> None:
        self._db_path = str(db_path)
        self._ttl_seconds = ttl_seconds
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_schema()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _create_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id    TEXT PRIMARY KEY,
                user_id       TEXT NOT NULL,
                created_at    REAL NOT NULL,
                last_accessed REAL NOT NULL,
                expires_at    REAL NOT NULL,
                data_json     TEXT NOT NULL DEFAULT '{}',
                status        TEXT NOT NULL DEFAULT 'active'
            )
            """
        )
        self._conn.commit()

    @staticmethod
    def _row_to_session(row: sqlite3.Row) -> Session:
        return Session(
            session_id=row["session_id"],
            user_id=row["user_id"],
            created_at=row["created_at"],
            last_accessed=row["last_accessed"],
            expires_at=row["expires_at"],
            data=json.loads(row["data_json"]),
            status=SessionStatus(row["status"]),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create(
        self,
        user_id: str,
        data: dict = None,
        ttl: float = None,
    ) -> Session:
        """Create and persist a new session.

        Parameters
        ----------
        user_id:
            Owner of the session.
        data:
            Initial session data dict.
        ttl:
            Time-to-live in seconds.  Overrides the store default.
            Pass ``0`` explicitly to create a non-expiring session.
        """
        now = time.time()

        # Determine effective TTL
        if ttl is None:
            effective_ttl = self._ttl_seconds
        else:
            effective_ttl = ttl

        expires_at = (now + effective_ttl) if effective_ttl > 0 else 0.0

        session = Session(
            user_id=user_id,
            created_at=now,
            last_accessed=now,
            expires_at=expires_at,
            data=data or {},
            status=SessionStatus.ACTIVE,
        )

        self._conn.execute(
            """
            INSERT INTO sessions
                (session_id, user_id, created_at, last_accessed, expires_at, data_json, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.session_id,
                session.user_id,
                session.created_at,
                session.last_accessed,
                session.expires_at,
                json.dumps(session.data),
                session.status.value,
            ),
        )
        self._conn.commit()
        return session

    def get(self, session_id: str) -> Session | None:
        """Return the session or ``None`` if not found or expired."""
        row = self._conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()

        if row is None:
            return None

        session = self._row_to_session(row)

        # Treat invalidated sessions as absent
        if session.status == SessionStatus.INVALIDATED:
            return None

        # Treat expired sessions as absent
        if session.is_expired():
            return None

        return session

    def touch(self, session_id: str, now: float = None) -> bool:
        """Update last_accessed for the session.

        Returns ``False`` if the session does not exist or is expired/invalidated.
        """
        session = self.get(session_id)
        if session is None:
            return False

        if now is None:
            now = time.time()

        self._conn.execute(
            "UPDATE sessions SET last_accessed = ? WHERE session_id = ?",
            (now, session_id),
        )
        self._conn.commit()
        return True

    def invalidate(self, session_id: str) -> bool:
        """Mark the session as INVALIDATED.

        Returns ``False`` if the session does not exist.
        """
        row = self._conn.execute(
            "SELECT session_id FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()

        if row is None:
            return False

        self._conn.execute(
            "UPDATE sessions SET status = ? WHERE session_id = ?",
            (SessionStatus.INVALIDATED.value, session_id),
        )
        self._conn.commit()
        return True

    def cleanup(self, now: float = None) -> int:
        """Delete expired and invalidated sessions.

        Returns the number of rows deleted.
        """
        if now is None:
            now = time.time()

        cursor = self._conn.execute(
            """
            DELETE FROM sessions
            WHERE status = ?
               OR (expires_at > 0 AND expires_at < ?)
            """,
            (SessionStatus.INVALIDATED.value, now),
        )
        self._conn.commit()
        return cursor.rowcount

    def active_for_user(self, user_id: str) -> list[Session]:
        """Return all non-expired, non-invalidated sessions for *user_id*."""
        now = time.time()
        rows = self._conn.execute(
            """
            SELECT * FROM sessions
            WHERE user_id = ?
              AND status = ?
              AND (expires_at = 0 OR expires_at > ?)
            """,
            (user_id, SessionStatus.ACTIVE.value, now),
        ).fetchall()
        return [self._row_to_session(r) for r in rows]

    def count_active(self) -> int:
        """Return count of all currently active (non-expired, non-invalidated) sessions."""
        now = time.time()
        row = self._conn.execute(
            """
            SELECT COUNT(*) FROM sessions
            WHERE status = ?
              AND (expires_at = 0 OR expires_at > ?)
            """,
            (SessionStatus.ACTIVE.value, now),
        ).fetchone()
        return row[0]

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
