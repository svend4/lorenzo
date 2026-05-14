"""Distributed lock primitives — FileLock and SQLiteLock.

Both implementations share the same interface:
  acquire(owner) -> bool
  release(owner) -> bool
  is_locked()    -> bool
  owner()        -> str | None
  context manager (__enter__ / __exit__)

Lock state is stored as JSON in a file (FileLock) or a SQLite row (SQLiteLock).
Locks carry a TTL; expired locks can be stolen by a new acquirer.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


class LockError(Exception):
    """Raised when a lock cannot be acquired."""


@dataclass
class LockConfig:
    """Configuration shared by FileLock and SQLiteLock."""
    ttl: float = 30.0            # seconds before an un-released lock auto-expires
    retry_interval: float = 0.1  # seconds between retries
    max_retries: int = 0         # 0 = try once only (no retries)


# ---------------------------------------------------------------------------
# FileLock
# ---------------------------------------------------------------------------

class FileLock:
    """Filesystem-backed distributed lock.

    The lock state is stored in ``{lock_dir}/{name}.lock`` as JSON:
    ``{"owner": "<str>", "expires_at": <float>}``.

    Atomicity is achieved via a temp-file + ``os.replace`` rename.
    """

    def __init__(self, name: str, lock_dir: str, config: Optional[LockConfig] = None):
        self._name = name
        self._lock_dir = lock_dir
        self._config = config if config is not None else LockConfig()
        self._lock_path = os.path.join(lock_dir, f"{name}.lock")
        self._ctx_owner: Optional[str] = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_dir(self) -> None:
        os.makedirs(self._lock_dir, exist_ok=True)

    def _read(self) -> Optional[dict]:
        """Return the parsed lock record, or None if missing / corrupt."""
        try:
            with open(self._lock_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return None

    def _write(self, owner: str, expires_at: float) -> None:
        """Atomically write the lock file using a temp file + rename."""
        self._ensure_dir()
        fd, tmp = tempfile.mkstemp(dir=self._lock_dir, prefix=f".{self._name}_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump({"owner": owner, "expires_at": expires_at}, fh)
            os.replace(tmp, self._lock_path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def _delete(self) -> None:
        try:
            os.unlink(self._lock_path)
        except FileNotFoundError:
            pass

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def acquire(self, owner: Optional[str] = None) -> bool:
        """Try to acquire the lock.

        Returns True if the lock was acquired, False if it could not be
        acquired after ``max_retries`` retries.
        """
        if owner is None:
            owner = str(uuid.uuid4())

        attempts = self._config.max_retries + 1  # first try + retries
        for attempt in range(attempts):
            if attempt > 0:
                time.sleep(self._config.retry_interval)

            self._ensure_dir()
            record = self._read()
            now = time.time()

            if record is None:
                # No lock file — try to grab it.
                try:
                    self._write(owner, now + self._config.ttl)
                    # Verify we actually own it (best-effort; not full fencing).
                    check = self._read()
                    if check and check.get("owner") == owner:
                        return True
                except OSError:
                    continue
            elif record.get("expires_at", 0) <= now:
                # Lock exists but is expired — steal it.
                try:
                    self._write(owner, now + self._config.ttl)
                    check = self._read()
                    if check and check.get("owner") == owner:
                        return True
                except OSError:
                    continue
            # else: locked by someone else and not expired → retry or give up

        return False

    def release(self, owner: Optional[str] = None) -> bool:
        """Release the lock if it is currently held by *owner*.

        Returns True if the lock file was removed, False otherwise.
        """
        record = self._read()
        if record is None:
            return False
        if owner is not None and record.get("owner") != owner:
            return False
        self._delete()
        return True

    def is_locked(self) -> bool:
        """Return True if a valid (non-expired) lock exists."""
        record = self._read()
        if record is None:
            return False
        return record.get("expires_at", 0) > time.time()

    def owner(self) -> Optional[str]:
        """Return the current lock owner, or None if no valid lock exists."""
        record = self._read()
        if record is None:
            return None
        if record.get("expires_at", 0) <= time.time():
            return None
        return record.get("owner")

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "FileLock":
        self._ctx_owner = str(uuid.uuid4())
        if not self.acquire(self._ctx_owner):
            raise LockError(
                f"Could not acquire FileLock '{self._name}' "
                f"after {self._config.max_retries} retries"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._ctx_owner is not None:
            self.release(self._ctx_owner)
            self._ctx_owner = None
        return False  # do not suppress exceptions


# ---------------------------------------------------------------------------
# SQLiteLock
# ---------------------------------------------------------------------------

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS locks (
    name       TEXT PRIMARY KEY,
    owner      TEXT NOT NULL,
    expires_at REAL NOT NULL
)
"""


class SQLiteLock:
    """SQLite-backed distributed lock.

    The lock state is stored in a ``locks`` table inside *db_path*:
    ``(name TEXT PRIMARY KEY, owner TEXT, expires_at REAL)``.

    SQLite's serialised writes give us sufficient atomicity for
    single-host "distributed" coordination scenarios.
    """

    def __init__(self, name: str, db_path: str, config: Optional[LockConfig] = None):
        self._name = name
        self._db_path = db_path
        self._config = config if config is not None else LockConfig()
        self._ctx_owner: Optional[str] = None
        self._ensure_table()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _ensure_table(self) -> None:
        with self._connect() as conn:
            conn.execute(_CREATE_TABLE)
            conn.commit()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def acquire(self, owner: Optional[str] = None) -> bool:
        """Try to acquire the lock.

        Returns True if acquired, False if it could not be acquired after
        ``max_retries`` retries.
        """
        if owner is None:
            owner = str(uuid.uuid4())

        attempts = self._config.max_retries + 1
        for attempt in range(attempts):
            if attempt > 0:
                time.sleep(self._config.retry_interval)

            now = time.time()
            expires_at = now + self._config.ttl

            try:
                with self._connect() as conn:
                    # Fetch the current row (if any) to check expiry.
                    row = conn.execute(
                        "SELECT owner, expires_at FROM locks WHERE name = ?",
                        (self._name,),
                    ).fetchone()

                    if row is None:
                        # No row → insert
                        conn.execute(
                            "INSERT OR IGNORE INTO locks (name, owner, expires_at) "
                            "VALUES (?, ?, ?)",
                            (self._name, owner, expires_at),
                        )
                    elif row[1] <= now:
                        # Row exists but expired → overwrite
                        conn.execute(
                            "UPDATE locks SET owner = ?, expires_at = ? "
                            "WHERE name = ? AND expires_at <= ?",
                            (owner, expires_at, self._name, now),
                        )
                    else:
                        # Locked by someone else and not expired → next attempt
                        continue

                    conn.commit()

                    # Verify ownership
                    check = conn.execute(
                        "SELECT owner FROM locks WHERE name = ?",
                        (self._name,),
                    ).fetchone()
                    if check and check[0] == owner:
                        return True
            except sqlite3.Error:
                continue

        return False

    def release(self, owner: Optional[str] = None) -> bool:
        """Release the lock if it is currently held by *owner*.

        Returns True if the row was removed, False otherwise.
        """
        try:
            with self._connect() as conn:
                if owner is not None:
                    row = conn.execute(
                        "SELECT owner FROM locks WHERE name = ?",
                        (self._name,),
                    ).fetchone()
                    if row is None or row[0] != owner:
                        return False
                result = conn.execute(
                    "DELETE FROM locks WHERE name = ?" + (
                        " AND owner = ?" if owner is not None else ""
                    ),
                    (self._name, owner) if owner is not None else (self._name,),
                )
                conn.commit()
                return result.rowcount > 0
        except sqlite3.Error:
            return False

    def is_locked(self) -> bool:
        """Return True if a valid (non-expired) lock exists."""
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT expires_at FROM locks WHERE name = ?",
                    (self._name,),
                ).fetchone()
                if row is None:
                    return False
                return row[0] > time.time()
        except sqlite3.Error:
            return False

    def owner(self) -> Optional[str]:
        """Return the current lock owner, or None if no valid lock exists."""
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT owner, expires_at FROM locks WHERE name = ?",
                    (self._name,),
                ).fetchone()
                if row is None:
                    return None
                if row[1] <= time.time():
                    return None
                return row[0]
        except sqlite3.Error:
            return None

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "SQLiteLock":
        self._ctx_owner = str(uuid.uuid4())
        if not self.acquire(self._ctx_owner):
            raise LockError(
                f"Could not acquire SQLiteLock '{self._name}' "
                f"after {self._config.max_retries} retries"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._ctx_owner is not None:
            self.release(self._ctx_owner)
            self._ctx_owner = None
        return False  # do not suppress exceptions
