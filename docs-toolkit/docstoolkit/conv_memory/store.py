"""ConversationStore — SQLite-backed persistence for conversation sessions."""
from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Optional

from docstoolkit.conv_memory.turn import ConversationTurn, Role


def _auto_session_id() -> str:
    return uuid.uuid4().hex[:8]


class ConversationStore:
    """Persist conversation sessions and turns in an SQLite database.

    Parameters
    ----------
    db_path:
        Path to the SQLite file, or ``":memory:"`` (default) for an
        in-process temporary database.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _create_schema(self) -> None:
        # Enable foreign-key enforcement (SQLite requires this per-connection)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS turns (
                turn_id    TEXT PRIMARY KEY,
                session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                role       TEXT NOT NULL,
                content    TEXT NOT NULL,
                ts         REAL NOT NULL,
                metadata   TEXT NOT NULL DEFAULT '{}'
            );

            CREATE INDEX IF NOT EXISTS idx_turns_session_ts
                ON turns (session_id, ts);
            """
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def new_session(self, session_id: Optional[str] = None) -> str:
        """Create a new session and return its ID.

        If *session_id* is not provided, a random 8-character hex string is
        generated automatically.
        """
        import time

        sid = session_id if session_id is not None else _auto_session_id()
        self._conn.execute(
            "INSERT INTO sessions (session_id, created_at) VALUES (?, ?)",
            (sid, time.time()),
        )
        self._conn.commit()
        return sid

    def get_session_ids(self) -> list[str]:
        """Return all session IDs, ordered by creation time."""
        rows = self._conn.execute(
            "SELECT session_id FROM sessions ORDER BY created_at"
        ).fetchall()
        return [r["session_id"] for r in rows]

    def delete_session(self, session_id: str) -> int:
        """Delete a session and all its turns.

        Returns the number of turns deleted.
        """
        count = self._conn.execute(
            "SELECT COUNT(*) FROM turns WHERE session_id = ?", (session_id,)
        ).fetchone()[0]
        self._conn.execute(
            "DELETE FROM sessions WHERE session_id = ?", (session_id,)
        )
        self._conn.commit()
        return count

    # ------------------------------------------------------------------
    # Turn management
    # ------------------------------------------------------------------

    def add_turn(self, session_id: str, turn: ConversationTurn) -> None:
        """Persist a ConversationTurn under the given session."""
        self._conn.execute(
            """
            INSERT INTO turns (turn_id, session_id, role, content, ts, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                turn.turn_id,
                session_id,
                turn.role.value,
                turn.content,
                turn.ts,
                json.dumps(turn.metadata),
            ),
        )
        self._conn.commit()

    def get_turns(
        self, session_id: str, limit: Optional[int] = None
    ) -> list[ConversationTurn]:
        """Return turns for *session_id* ordered by timestamp ascending.

        If *limit* is given, only the last *limit* turns are returned.
        """
        if limit is not None:
            rows = self._conn.execute(
                """
                SELECT * FROM (
                    SELECT turn_id, role, content, ts, metadata
                    FROM turns
                    WHERE session_id = ?
                    ORDER BY ts DESC
                    LIMIT ?
                ) ORDER BY ts ASC
                """,
                (session_id, limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                """
                SELECT turn_id, role, content, ts, metadata
                FROM turns
                WHERE session_id = ?
                ORDER BY ts ASC
                """,
                (session_id,),
            ).fetchall()

        return [
            ConversationTurn(
                turn_id=r["turn_id"],
                role=Role(r["role"]),
                content=r["content"],
                ts=r["ts"],
                metadata=json.loads(r["metadata"]),
            )
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return aggregate statistics for the store."""
        total_sessions = self._conn.execute(
            "SELECT COUNT(*) FROM sessions"
        ).fetchone()[0]
        total_turns = self._conn.execute(
            "SELECT COUNT(*) FROM turns"
        ).fetchone()[0]
        avg_turns = (
            total_turns / total_sessions if total_sessions > 0 else 0.0
        )
        return {
            "total_sessions": total_sessions,
            "total_turns": total_turns,
            "avg_turns_per_session": avg_turns,
        }

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
