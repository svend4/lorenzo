"""SQLite-backed GDPR-style consent manager."""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from typing import Callable, Optional

from docstoolkit.consent_manager.models import ConsentRecord, ConsentStatus


class ConsentManager:
    """Track user consent records for data processing purposes (GDPR-style).

    Features
    --------
    - Multiple consent purposes per user
    - Versioned consent with ``min_version`` checks
    - Withdrawal and full audit trail via ``granted_at`` / ``withdrawn_at``
    - SQLite-backed; uses WAL mode for file DBs
    - Thread-safe via ``threading.Lock``
    - Injectable ``now_fn`` for deterministic testing
    """

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS consent (
        user_id      TEXT NOT NULL,
        purpose      TEXT NOT NULL,
        status       TEXT NOT NULL,
        version      INTEGER DEFAULT 1,
        granted_at   REAL,
        withdrawn_at REAL,
        metadata     TEXT DEFAULT '{}',
        PRIMARY KEY (user_id, purpose)
    )
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        now_fn: Optional[Callable[[], float]] = None,
    ) -> None:
        self._db_path = db_path
        self._now = now_fn if now_fn is not None else time.time
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        if db_path != ":memory:":
            self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(self._CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> ConsentRecord:
        return ConsentRecord(
            user_id=row["user_id"],
            purpose=row["purpose"],
            status=ConsentStatus(row["status"]),
            version=row["version"],
            granted_at=row["granted_at"],
            withdrawn_at=row["withdrawn_at"],
            metadata=json.loads(row["metadata"] or "{}"),
        )

    def _fetchone(self, user_id: str, purpose: str) -> Optional[ConsentRecord]:
        row = self._conn.execute(
            "SELECT * FROM consent WHERE user_id = ? AND purpose = ?",
            (user_id, purpose),
        ).fetchone()
        return self._row_to_record(row) if row else None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def grant(
        self,
        user_id: str,
        purpose: str,
        version: int = 1,
        metadata: Optional[dict] = None,
    ) -> ConsentRecord:
        """Record consent granted.

        Overwrites any existing record for the same *(user_id, purpose)* pair.
        """
        now = self._now()
        meta_json = json.dumps(metadata or {})
        with self._lock:
            self._conn.execute(
                """
                INSERT OR REPLACE INTO consent
                    (user_id, purpose, status, version, granted_at, withdrawn_at, metadata)
                VALUES (?, ?, ?, ?, ?, NULL, ?)
                """,
                (user_id, purpose, ConsentStatus.GRANTED.value, version, now, meta_json),
            )
            self._conn.commit()
            record = self._fetchone(user_id, purpose)
        assert record is not None  # just inserted
        return record

    def withdraw(self, user_id: str, purpose: str) -> ConsentRecord:
        """Mark consent as withdrawn.

        Raises
        ------
        KeyError
            If no consent record exists for *(user_id, purpose)*.
        """
        with self._lock:
            existing = self._fetchone(user_id, purpose)
            if existing is None:
                raise KeyError(f"No consent record for user={user_id!r}, purpose={purpose!r}")
            now = self._now()
            self._conn.execute(
                """
                UPDATE consent
                   SET status = ?, withdrawn_at = ?
                 WHERE user_id = ? AND purpose = ?
                """,
                (ConsentStatus.WITHDRAWN.value, now, user_id, purpose),
            )
            self._conn.commit()
            record = self._fetchone(user_id, purpose)
        assert record is not None
        return record

    def has_consent(
        self,
        user_id: str,
        purpose: str,
        min_version: int = 1,
    ) -> bool:
        """Return ``True`` if the user has GRANTED consent at ``version >= min_version``."""
        with self._lock:
            record = self._fetchone(user_id, purpose)
        if record is None:
            return False
        return (
            record.status == ConsentStatus.GRANTED
            and record.version >= min_version
        )

    def get(self, user_id: str, purpose: str) -> Optional[ConsentRecord]:
        """Return the consent record, or ``None`` if not found."""
        with self._lock:
            return self._fetchone(user_id, purpose)

    def list_user(self, user_id: str) -> list[ConsentRecord]:
        """Return all consent records for *user_id*."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM consent WHERE user_id = ? ORDER BY purpose",
                (user_id,),
            ).fetchall()
        return [self._row_to_record(r) for r in rows]

    def list_purpose(self, purpose: str) -> list[ConsentRecord]:
        """Return all consent records for *purpose*."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM consent WHERE purpose = ? ORDER BY user_id",
                (purpose,),
            ).fetchall()
        return [self._row_to_record(r) for r in rows]

    def revoke_all(self, user_id: str) -> int:
        """Withdraw all GRANTED consents for *user_id*.

        Returns
        -------
        int
            Number of records changed.
        """
        now = self._now()
        with self._lock:
            cur = self._conn.execute(
                """
                UPDATE consent
                   SET status = ?, withdrawn_at = ?
                 WHERE user_id = ? AND status = ?
                """,
                (ConsentStatus.WITHDRAWN.value, now, user_id, ConsentStatus.GRANTED.value),
            )
            self._conn.commit()
        return cur.rowcount

    def granted_users(self, purpose: str, min_version: int = 1) -> list[str]:
        """Return ``user_id`` values with GRANTED consent for *purpose* at ``version >= min_version``."""
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT user_id FROM consent
                 WHERE purpose = ?
                   AND status  = ?
                   AND version >= ?
                 ORDER BY user_id
                """,
                (purpose, ConsentStatus.GRANTED.value, min_version),
            ).fetchall()
        return [r["user_id"] for r in rows]

    def delete(self, user_id: str, purpose: str) -> bool:
        """Permanently delete the record.

        Returns
        -------
        bool
            ``True`` if a record existed and was deleted, ``False`` otherwise.
        """
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM consent WHERE user_id = ? AND purpose = ?",
                (user_id, purpose),
            )
            self._conn.commit()
        return cur.rowcount > 0

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
