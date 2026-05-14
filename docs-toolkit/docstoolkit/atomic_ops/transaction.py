"""Atomic transactions over :class:`AtomicStore`.

:class:`AtomicTransaction` is a context manager that wraps a group of
``get`` / ``set`` / ``cas`` / ``increment`` / ``decrement`` operations
in a single SQLite transaction.  On normal exit the transaction is
committed; if an exception escapes the ``with`` block the transaction
is rolled back, leaving the store unchanged.

Pure stdlib - no external dependencies.
"""
from __future__ import annotations

import sqlite3
import threading
from typing import Any, Optional

from docstoolkit.atomic_ops.ops import (
    AtomicStore,
    OpResult,
    _decode,
    _encode,
)


class TransactionError(Exception):
    """Raised when a transaction is misused (e.g. used outside its context)."""


class AtomicTransaction:
    """Context manager wrapping a group of operations in one SQLite tx.

    Usage::

        store = AtomicStore()
        with AtomicTransaction(store) as tx:
            tx.set("a", 1)
            tx.increment("a", 5)
        # changes are now committed; if the block raised, they would be
        # rolled back.

    The transaction acquires the store's internal lock for its entire
    lifetime so concurrent writers cannot interleave with it.  Reads
    and writes inside the ``with`` block go through a *private*
    connection so they participate in a single SQLite transaction.

    Operations on the transaction object outside of a ``with`` block
    (i.e. before ``__enter__`` or after ``__exit__``) raise
    :class:`TransactionError`.
    """

    def __init__(self, store: AtomicStore):
        if not isinstance(store, AtomicStore):
            raise TypeError("store must be an AtomicStore")
        self._store = store
        self._conn: Optional[sqlite3.Connection] = None
        self._active = False
        self._lock_held = False

    # ------------------------------------------------------------------
    # Context manager protocol
    # ------------------------------------------------------------------

    def __enter__(self) -> "AtomicTransaction":
        if self._active:
            raise TransactionError("transaction already active")
        # Acquire the store's lock first so concurrent operations serialise
        # against this transaction.
        self._store._lock.acquire()
        self._lock_held = True
        try:
            self._conn = self._store._connect()
            # Start an IMMEDIATE transaction so we have a write lock for
            # the whole block; this matches what AtomicStore methods do.
            self._conn.execute("BEGIN IMMEDIATE")
            self._active = True
            return self
        except Exception:
            # Roll back any partial state and release the lock.
            if self._conn is not None:
                try:
                    self._conn.rollback()
                except sqlite3.Error:
                    pass
                try:
                    self._store._close_conn(self._conn)
                except sqlite3.Error:
                    pass
                self._conn = None
            if self._lock_held:
                self._store._lock.release()
                self._lock_held = False
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._active or self._conn is None:
            # Should not happen, but defensively release the lock if held.
            if self._lock_held:
                try:
                    self._store._lock.release()
                finally:
                    self._lock_held = False
            return None
        try:
            if exc_type is None:
                try:
                    self._conn.commit()
                except Exception:
                    try:
                        self._conn.rollback()
                    except sqlite3.Error:
                        pass
                    raise
            else:
                try:
                    self._conn.rollback()
                except sqlite3.Error:
                    pass
        finally:
            try:
                self._store._close_conn(self._conn)
            except sqlite3.Error:
                pass
            self._conn = None
            self._active = False
            if self._lock_held:
                self._store._lock.release()
                self._lock_held = False
        return None

    # ------------------------------------------------------------------
    # Public operations (mirror AtomicStore but operate on the private conn)
    # ------------------------------------------------------------------

    def _require_active(self) -> sqlite3.Connection:
        if not self._active or self._conn is None:
            raise TransactionError(
                "transaction is not active; use inside a `with` block"
            )
        return self._conn

    def get(self, key: str, default: Any = None) -> Any:
        """Read a key inside the transaction."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        conn = self._require_active()
        row = conn.execute(
            "SELECT value FROM atomic_kv WHERE key = ?", (key,),
        ).fetchone()
        if row is None:
            return default
        return _decode(row[0])

    def set(self, key: str, value: Any) -> int:
        """Set a key inside the transaction.  Returns the new version."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        conn = self._require_active()
        encoded = _encode(value)
        row = conn.execute(
            "SELECT version FROM atomic_kv WHERE key = ?", (key,),
        ).fetchone()
        if row is None:
            new_version = 1
            conn.execute(
                "INSERT INTO atomic_kv (key, value, version) VALUES (?, ?, ?)",
                (key, encoded, new_version),
            )
        else:
            new_version = int(row[0]) + 1
            conn.execute(
                "UPDATE atomic_kv SET value = ?, version = ? WHERE key = ?",
                (encoded, new_version, key),
            )
        return new_version

    def cas(self, key: str, expected: Any, new: Any) -> OpResult:
        """Compare-and-swap inside the transaction."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        conn = self._require_active()
        new_encoded = _encode(new)
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
                    "UPDATE atomic_kv SET value = ?, version = ? WHERE key = ?",
                    (new_encoded, new_version, key),
                )
            else:
                conn.execute(
                    "INSERT INTO atomic_kv (key, value, version) "
                    "VALUES (?, ?, ?)",
                    (key, new_encoded, 1),
                )
            return OpResult(success=True, value=new, previous=current_value,
                            error="")
        return OpResult(success=False, value=None, previous=current_value,
                        error="CAS mismatch: expected != current")

    def increment(self, key: str, delta: int = 1) -> int:
        """Atomic numeric increment inside the transaction."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise TypeError("delta must be an int")
        conn = self._require_active()
        row = conn.execute(
            "SELECT value, version FROM atomic_kv WHERE key = ?", (key,),
        ).fetchone()
        if row is None:
            new_value = int(delta)
            conn.execute(
                "INSERT INTO atomic_kv (key, value, version) VALUES (?, ?, ?)",
                (key, _encode(new_value), 1),
            )
        else:
            current = _decode(row[0])
            if not isinstance(current, (int, float)) or isinstance(current, bool):
                raise TypeError(
                    f"cannot increment non-numeric value for key {key!r}"
                )
            new_value = int(current) + int(delta)
            new_version = int(row[1]) + 1
            conn.execute(
                "UPDATE atomic_kv SET value = ?, version = ? WHERE key = ?",
                (_encode(new_value), new_version, key),
            )
        return new_value

    def decrement(self, key: str, delta: int = 1) -> int:
        """Atomic numeric decrement inside the transaction."""
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise TypeError("delta must be an int")
        return self.increment(key, -int(delta))
