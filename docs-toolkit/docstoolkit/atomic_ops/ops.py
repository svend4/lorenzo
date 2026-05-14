"""SQLite-backed atomic operations store.

:class:`AtomicStore` provides a thread-safe key-value store with
strong atomic primitives: set, get, compare-and-swap (CAS),
get-and-set, atomic numeric increment/decrement, delete, exists
and version.

Values are JSON-serialised on the way into the database and
JSON-deserialised on the way out, so any JSON-compatible Python
value (``int``, ``float``, ``str``, ``bool``, ``None``, ``list``,
``dict``) can be stored.

Pure stdlib - no external dependencies.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class OpResult:
    """Result of an atomic operation.

    Attributes:
        success: ``True`` if the operation completed successfully.
        value: The value the key now holds after the operation
            (``None`` on failure or where not applicable).
        previous: The previous value of the key before the operation
            (``None`` if the key did not exist).
        error: Human-readable error message on failure (empty string
            otherwise).
    """
    success: bool
    value: Any = None
    previous: Any = None
    error: str = ""


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS atomic_kv (
    key     TEXT PRIMARY KEY,
    value   TEXT,
    version INTEGER DEFAULT 0
)
"""


# Sentinel used to detect "default not supplied" in get().
_MISSING = object()


def _encode(value: Any) -> str:
    """JSON-encode a value.  Falls back to ``repr`` for non-JSON values."""
    return json.dumps(value, ensure_ascii=False, sort_keys=False, default=repr)


def _decode(text: Optional[str]) -> Any:
    """JSON-decode a value, returning ``None`` for SQL ``NULL``."""
    if text is None:
        return None
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


class AtomicStore:
    """SQLite-backed atomic key-value store.

    The store is thread-safe: an internal :class:`threading.Lock`
    serialises writers, and SQLite's transactional semantics give
    each individual operation atomicity.

    Pass ``":memory:"`` (the default) for an in-memory database, or
    a filesystem path for on-disk persistence.

    For in-memory databases a single connection is kept alive for
    the life of the store (otherwise each connect would see an
    empty database).  For on-disk databases a fresh connection is
    used per call so the store can be safely shared across threads
    without ``check_same_thread`` complications.
    """

    def __init__(self, db_path: str = ":memory:"):
        self._db_path = db_path
        self._lock = threading.Lock()
        self._is_memory = db_path == ":memory:"
        if self._is_memory:
            self._mem_conn: Optional[sqlite3.Connection] = sqlite3.connect(
                db_path,
                check_same_thread=False,
                timeout=5.0,
                isolation_level=None,  # autocommit; we control transactions manually
            )
        else:
            self._mem_conn = None
        self._closed = False
        self._ensure_table()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        if self._closed:
            raise RuntimeError("AtomicStore is closed")
        if self._mem_conn is not None:
            return self._mem_conn
        conn = sqlite3.connect(self._db_path, timeout=5.0)
        try:
            conn.execute("PRAGMA journal_mode=WAL")
        except sqlite3.Error:
            pass
        return conn

    def _close_conn(self, conn: sqlite3.Connection) -> None:
        """Close a per-call connection (no-op for the shared in-memory one)."""
        if self._mem_conn is None:
            try:
                conn.close()
            except sqlite3.Error:
                pass

    def _ensure_table(self) -> None:
        with self._lock:
            conn = self._connect()
            try:
                conn.execute(_CREATE_TABLE)
                conn.commit()
            finally:
                self._close_conn(conn)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value stored at *key*, or *default* if missing."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self._lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT value FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    return default
                return _decode(row[0])
            finally:
                self._close_conn(conn)

    def set(self, key: str, value: Any) -> int:
        """Unconditionally set *key* to *value*; return the new version.

        Inserting a new key starts the version at 1.  Updating an existing
        key increments its version by 1.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        encoded = _encode(value)
        with self._lock:
            conn = self._connect()
            try:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT version FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    new_version = 1
                    conn.execute(
                        "INSERT INTO atomic_kv (key, value, version) "
                        "VALUES (?, ?, ?)",
                        (key, encoded, new_version),
                    )
                else:
                    new_version = int(row[0]) + 1
                    conn.execute(
                        "UPDATE atomic_kv SET value = ?, version = ? "
                        "WHERE key = ?",
                        (encoded, new_version, key),
                    )
                conn.commit()
                return new_version
            except Exception:
                try:
                    conn.rollback()
                except sqlite3.Error:
                    pass
                raise
            finally:
                self._close_conn(conn)

    def cas(self, key: str, expected: Any, new: Any) -> OpResult:
        """Compare-and-swap.

        Only update *key* to *new* if its current value equals *expected*.
        Returns an :class:`OpResult` with ``success=True`` on success and
        ``success=False`` on mismatch.  ``previous`` carries the value
        that was actually stored before the operation; ``value`` carries
        the value stored after a successful swap.

        If *key* does not exist:
          * if *expected* is ``None``, the key is created with *new* and
            the operation succeeds;
          * otherwise the operation fails with ``previous=None``.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        new_encoded = _encode(new)
        with self._lock:
            conn = self._connect()
            try:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT value, version FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    current_value: Any = None
                    current_version = 0
                    exists = False
                else:
                    current_value = _decode(row[0])
                    current_version = int(row[1])
                    exists = True

                if current_value == expected:
                    if exists:
                        new_version = current_version + 1
                        conn.execute(
                            "UPDATE atomic_kv SET value = ?, version = ? "
                            "WHERE key = ?",
                            (new_encoded, new_version, key),
                        )
                    else:
                        new_version = 1
                        conn.execute(
                            "INSERT INTO atomic_kv (key, value, version) "
                            "VALUES (?, ?, ?)",
                            (key, new_encoded, new_version),
                        )
                    conn.commit()
                    return OpResult(
                        success=True,
                        value=new,
                        previous=current_value,
                        error="",
                    )
                else:
                    conn.rollback()
                    return OpResult(
                        success=False,
                        value=None,
                        previous=current_value,
                        error="CAS mismatch: expected != current",
                    )
            except Exception as exc:
                try:
                    conn.rollback()
                except sqlite3.Error:
                    pass
                return OpResult(success=False, value=None, previous=None,
                                error=str(exc))
            finally:
                self._close_conn(conn)

    def increment(self, key: str, delta: int = 1) -> int:
        """Atomically add *delta* to *key* and return the new numeric value.

        If *key* does not exist it is created with value *delta*.  If
        *key* exists but its value is not numeric an exception is raised.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise TypeError("delta must be an int")
        with self._lock:
            conn = self._connect()
            try:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT value, version FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    new_value: int = int(delta)
                    new_version = 1
                    conn.execute(
                        "INSERT INTO atomic_kv (key, value, version) "
                        "VALUES (?, ?, ?)",
                        (key, _encode(new_value), new_version),
                    )
                else:
                    current = _decode(row[0])
                    if not isinstance(current, (int, float)) or isinstance(current, bool):
                        conn.rollback()
                        raise TypeError(
                            f"cannot increment non-numeric value for key {key!r}"
                        )
                    new_value = int(current) + int(delta)
                    new_version = int(row[1]) + 1
                    conn.execute(
                        "UPDATE atomic_kv SET value = ?, version = ? "
                        "WHERE key = ?",
                        (_encode(new_value), new_version, key),
                    )
                conn.commit()
                return new_value
            except Exception:
                try:
                    conn.rollback()
                except sqlite3.Error:
                    pass
                raise
            finally:
                self._close_conn(conn)

    def decrement(self, key: str, delta: int = 1) -> int:
        """Atomically subtract *delta* from *key* and return the new value."""
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise TypeError("delta must be an int")
        return self.increment(key, -int(delta))

    def getset(self, key: str, value: Any) -> Any:
        """Atomically set *key* to *value* and return its previous value.

        Returns ``None`` if the key did not exist.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        encoded = _encode(value)
        with self._lock:
            conn = self._connect()
            try:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT value, version FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    previous: Any = None
                    conn.execute(
                        "INSERT INTO atomic_kv (key, value, version) "
                        "VALUES (?, ?, ?)",
                        (key, encoded, 1),
                    )
                else:
                    previous = _decode(row[0])
                    new_version = int(row[1]) + 1
                    conn.execute(
                        "UPDATE atomic_kv SET value = ?, version = ? "
                        "WHERE key = ?",
                        (encoded, new_version, key),
                    )
                conn.commit()
                return previous
            except Exception:
                try:
                    conn.rollback()
                except sqlite3.Error:
                    pass
                raise
            finally:
                self._close_conn(conn)

    def delete(self, key: str) -> bool:
        """Delete *key*.  Returns True if the key existed."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self._lock:
            conn = self._connect()
            try:
                cur = conn.execute(
                    "DELETE FROM atomic_kv WHERE key = ?", (key,),
                )
                conn.commit()
                return cur.rowcount > 0
            finally:
                self._close_conn(conn)

    def exists(self, key: str) -> bool:
        """Return ``True`` if *key* is present in the store."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self._lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT 1 FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                return row is not None
            finally:
                self._close_conn(conn)

    def version(self, key: str) -> int:
        """Return the current version of *key*, or 0 if missing."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self._lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT version FROM atomic_kv WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    return 0
                return int(row[0])
            finally:
                self._close_conn(conn)

    def close(self) -> None:
        """Close the underlying SQLite connection (in-memory only)."""
        with self._lock:
            if self._mem_conn is not None:
                try:
                    self._mem_conn.close()
                except sqlite3.Error:
                    pass
                self._mem_conn = None
            self._closed = True
