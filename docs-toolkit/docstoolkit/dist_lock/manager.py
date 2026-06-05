"""Fencing-token manager for distributed locks.

Adds monotonically-increasing fencing tokens to SQLite-backed locks so that
write-backs from stale (network-partitioned) lock holders can be safely
rejected.

Pattern:
    1. ``acquire()`` returns a ``FencingToken`` with a globally-unique epoch.
    2. Caller passes the token to any guarded resource write.
    3. The guarded resource calls ``validate_write(token)`` before committing.
       Writes with a token whose epoch < the current max epoch are rejected.

This prevents the classic scenario where a slow / partitioned process holds a
lock that has since been acquired by another — its old token is invalidated as
soon as the new holder acquires with a higher epoch.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Optional


class FencingError(Exception):
    """Raised when a write is rejected because the fencing token is stale."""


@dataclass
class FencingToken:
    """Monotonically-increasing lease token issued on lock acquisition."""
    epoch: int          # global sequence, strictly increases with every acquire
    owner: str          # UUID of the lock holder
    lock_name: str      # which lock resource this token belongs to
    issued_at: float    # unix timestamp when the lock was acquired

    def is_fresh(self, current_epoch: int) -> bool:
        """Return True iff this token's epoch is still the current one."""
        return self.epoch == current_epoch

    def __repr__(self) -> str:
        return f"FencingToken(epoch={self.epoch}, owner={self.owner!r})"


_DDL = """
CREATE TABLE IF NOT EXISTS fenced_locks (
    name       TEXT    PRIMARY KEY,
    owner      TEXT    NOT NULL,
    expires_at REAL    NOT NULL,
    epoch      INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS fenced_write_log (
    resource   TEXT    NOT NULL,
    max_epoch  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (resource)
);
"""


class FencedLockManager:
    """SQLite-backed distributed lock with fencing-token support.

    Each ``acquire()`` returns a :class:`FencingToken` whose ``epoch`` is
    atomically incremented.  Callers *must* present the token when writing to
    any guarded resource via ``validate_write(resource, token)``; stale tokens
    raise :class:`FencingError`.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an in-process
        (non-shared) store.
    ttl:
        Lock TTL in seconds.  Expired locks can be stolen by a new caller.
    max_retries:
        Number of additional acquire attempts after the first (0 = try once).
    retry_interval:
        Seconds to wait between retry attempts.
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        ttl: float = 30.0,
        max_retries: int = 0,
        retry_interval: float = 0.1,
    ) -> None:
        self._db_path = db_path
        self._ttl = ttl
        self._max_retries = max_retries
        self._retry_interval = retry_interval
        self._mutex = threading.Lock()

        # Keep a single persistent connection so :memory: works correctly.
        # check_same_thread=False is safe because we guard with _mutex.
        self._conn = sqlite3.connect(db_path, check_same_thread=False, timeout=5.0)
        self._conn.row_factory = sqlite3.Row
        if db_path != ":memory:":
            self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_DDL)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        """Serialised access to the shared connection."""
        with self._mutex:
            try:
                yield self._conn
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise

    # ------------------------------------------------------------------
    # Acquire / release
    # ------------------------------------------------------------------

    def acquire(self, name: str, owner: Optional[str] = None) -> Optional[FencingToken]:
        """Try to acquire lock *name*.

        Returns a :class:`FencingToken` on success, ``None`` on failure (after
        all retries are exhausted).
        """
        if owner is None:
            owner = str(uuid.uuid4())

        attempts = self._max_retries + 1
        for attempt in range(attempts):
            if attempt > 0:
                time.sleep(self._retry_interval)

            now = time.time()
            expires_at = now + self._ttl

            try:
                with self._tx() as conn:
                    row = conn.execute(
                        "SELECT owner, expires_at, epoch FROM fenced_locks WHERE name = ?",
                        (name,),
                    ).fetchone()

                    if row is None:
                        conn.execute(
                            "INSERT OR IGNORE INTO fenced_locks "
                            "(name, owner, expires_at, epoch) VALUES (?, ?, ?, 1)",
                            (name, owner, expires_at),
                        )
                    elif row["expires_at"] <= now:
                        new_epoch = row["epoch"] + 1
                        conn.execute(
                            "UPDATE fenced_locks SET owner=?, expires_at=?, epoch=? "
                            "WHERE name=? AND expires_at<=?",
                            (owner, expires_at, new_epoch, name, now),
                        )
                    else:
                        continue  # held by someone else, retry

                    # Read back to confirm ownership
                    check = conn.execute(
                        "SELECT owner, epoch FROM fenced_locks WHERE name = ?",
                        (name,),
                    ).fetchone()
                    if check and check["owner"] == owner:
                        return FencingToken(
                            epoch=check["epoch"],
                            owner=owner,
                            lock_name=name,
                            issued_at=now,
                        )
            except sqlite3.Error:
                continue

        return None

    def release(self, name: str, owner: str) -> bool:
        """Release lock *name* if currently held by *owner*.

        Returns True if the lock was released.
        """
        try:
            with self._tx() as conn:
                row = conn.execute(
                    "SELECT owner FROM fenced_locks WHERE name = ?", (name,)
                ).fetchone()
                if row is None or row["owner"] != owner:
                    return False
                cur = conn.execute(
                    "DELETE FROM fenced_locks WHERE name = ? AND owner = ?",
                    (name, owner),
                )
                return cur.rowcount > 0
        except sqlite3.Error:
            return False

    def current_epoch(self, name: str) -> Optional[int]:
        """Return the current epoch for lock *name*, or None if not held."""
        with self._mutex:
            row = self._conn.execute(
                "SELECT epoch, expires_at FROM fenced_locks WHERE name = ?", (name,)
            ).fetchone()
            if row is None:
                return None
            if row["expires_at"] <= time.time():
                return None
            return row["epoch"]

    def is_locked(self, name: str) -> bool:
        """Return True if lock *name* is currently held (non-expired)."""
        return self.current_epoch(name) is not None

    # ------------------------------------------------------------------
    # Fencing validation
    # ------------------------------------------------------------------

    def validate_write(self, resource: str, token: FencingToken) -> None:
        """Assert that *token* is still the authoritative token for *resource*.

        Raises :class:`FencingError` if the token's epoch is less than the
        highest epoch seen for this resource.  Advances the max_epoch record
        on success so future stale tokens are caught.
        """
        try:
            with self._tx() as conn:
                row = conn.execute(
                    "SELECT max_epoch FROM fenced_write_log WHERE resource = ?",
                    (resource,),
                ).fetchone()
                max_epoch = row["max_epoch"] if row else 0

                if token.epoch < max_epoch:
                    raise FencingError(
                        f"Stale token: epoch {token.epoch} < current max {max_epoch} "
                        f"for resource {resource!r}. "
                        f"Lock was re-acquired while this holder was paused."
                    )

                if row is None:
                    conn.execute(
                        "INSERT INTO fenced_write_log (resource, max_epoch) VALUES (?, ?)",
                        (resource, token.epoch),
                    )
                else:
                    conn.execute(
                        "UPDATE fenced_write_log SET max_epoch = ? WHERE resource = ?",
                        (token.epoch, resource),
                    )
        except FencingError:
            raise
        except sqlite3.Error as exc:
            raise FencingError(f"DB error during fencing check: {exc}") from exc

    def close(self) -> None:
        """Close the underlying database connection."""
        with self._mutex:
            self._conn.close()

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def lock(self, name: str) -> "_FencedLockCtx":
        """Context manager that acquires and releases lock *name*.

        Usage::

            with manager.lock("my-resource") as token:
                manager.validate_write("doc-42", token)
                # … write here …
        """
        return _FencedLockCtx(self, name)


class _FencedLockCtx:
    """Context manager returned by :meth:`FencedLockManager.lock`."""

    def __init__(self, manager: FencedLockManager, name: str) -> None:
        self._manager = manager
        self._name = name
        self._owner = str(uuid.uuid4())
        self._token: Optional[FencingToken] = None

    def __enter__(self) -> FencingToken:
        token = self._manager.acquire(self._name, owner=self._owner)
        if token is None:
            raise FencingError(
                f"Could not acquire fenced lock '{self._name}' "
                f"after {self._manager._max_retries} retries"
            )
        self._token = token
        return token

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._manager.release(self._name, self._owner)
        return False
