"""SQLite-backed distributed counter store.

CounterStore supports atomic increment/decrement, get/set/delete,
prefix-based listing/sum/reset, and is thread-safe via a Lock + SQLite WAL.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import sqlite3
import threading
import time
from dataclasses import dataclass
from typing import List, Optional


class CounterError(Exception):
    """Raised for counter store errors."""


@dataclass
class CounterValue:
    """A single counter value with metadata."""
    key: str
    value: int
    updated_at: float


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS counters (
    key        TEXT PRIMARY KEY,
    value      INTEGER NOT NULL,
    updated_at REAL    NOT NULL
)
"""


class CounterStore:
    """SQLite-backed counter store.

    Schema: ``counters(key TEXT PRIMARY KEY, value INTEGER, updated_at REAL)``.

    Thread-safe — an internal :class:`threading.Lock` serialises writes from
    multiple Python threads, and SQLite's WAL mode allows safe concurrent
    readers.  For ``":memory:"`` databases we keep a single connection alive
    so all callers see the same database; for on-disk databases we open a
    new connection per call which makes the store safe to share across
    threads without ``check_same_thread`` complications.
    """

    def __init__(self, db_path: str = ":memory:"):
        self._db_path = db_path
        self._lock = threading.Lock()
        # For :memory: databases a fresh connection has its own empty DB,
        # so we keep one shared connection alive for the lifetime of the
        # store.  We disable check_same_thread because the external Lock
        # provides the necessary serialisation.
        self._is_memory = db_path == ":memory:"
        if self._is_memory:
            self._mem_conn: Optional[sqlite3.Connection] = sqlite3.connect(
                db_path, check_same_thread=False, timeout=5.0,
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
            raise CounterError("CounterStore is closed")
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
            conn.close()

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

    def increment(self, key: str, delta: int = 1) -> int:
        """Atomically add *delta* to *key* and return the new value.

        If *key* does not exist it is created with value *delta*.
        """
        if not isinstance(key, str):
            raise CounterError("key must be a string")
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise CounterError("delta must be an int")

        with self._lock:
            conn = self._connect()
            try:
                now = time.time()
                # Upsert: insert if missing, otherwise add delta.
                conn.execute(
                    "INSERT INTO counters (key, value, updated_at) "
                    "VALUES (?, ?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET "
                    "    value = value + excluded.value, "
                    "    updated_at = excluded.updated_at",
                    (key, delta, now),
                )
                conn.commit()
                row = conn.execute(
                    "SELECT value FROM counters WHERE key = ?", (key,),
                ).fetchone()
                return int(row[0])
            finally:
                self._close_conn(conn)

    def decrement(self, key: str, delta: int = 1) -> int:
        """Atomically subtract *delta* from *key* and return the new value."""
        return self.increment(key, -delta)

    def get(self, key: str) -> int:
        """Return the value of *key*, or 0 if missing."""
        with self._lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT value FROM counters WHERE key = ?", (key,),
                ).fetchone()
                if row is None:
                    return 0
                return int(row[0])
            finally:
                self._close_conn(conn)

    def get_value(self, key: str) -> Optional[CounterValue]:
        """Return the full :class:`CounterValue` for *key*, or None if missing."""
        with self._lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT key, value, updated_at FROM counters WHERE key = ?",
                    (key,),
                ).fetchone()
                if row is None:
                    return None
                return CounterValue(key=row[0], value=int(row[1]),
                                    updated_at=float(row[2]))
            finally:
                self._close_conn(conn)

    def set(self, key: str, value: int) -> None:
        """Overwrite *key* with *value*, creating the row if missing."""
        if not isinstance(key, str):
            raise CounterError("key must be a string")
        if not isinstance(value, int) or isinstance(value, bool):
            raise CounterError("value must be an int")

        with self._lock:
            conn = self._connect()
            try:
                now = time.time()
                conn.execute(
                    "INSERT INTO counters (key, value, updated_at) "
                    "VALUES (?, ?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET "
                    "    value = excluded.value, "
                    "    updated_at = excluded.updated_at",
                    (key, value, now),
                )
                conn.commit()
            finally:
                self._close_conn(conn)

    def delete(self, key: str) -> bool:
        """Delete *key*.  Returns True if the row existed, False otherwise."""
        with self._lock:
            conn = self._connect()
            try:
                cur = conn.execute("DELETE FROM counters WHERE key = ?", (key,))
                conn.commit()
                return cur.rowcount > 0
            finally:
                self._close_conn(conn)

    def list_all(self, prefix: str = "") -> List[CounterValue]:
        """Return all :class:`CounterValue` rows whose key starts with
        *prefix*, sorted lexicographically by key.
        """
        with self._lock:
            conn = self._connect()
            try:
                if prefix:
                    pattern = prefix.replace("\\", "\\\\") \
                                    .replace("%", "\\%") \
                                    .replace("_", "\\_") + "%"
                    rows = conn.execute(
                        "SELECT key, value, updated_at FROM counters "
                        "WHERE key LIKE ? ESCAPE '\\' "
                        "ORDER BY key",
                        (pattern,),
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT key, value, updated_at FROM counters "
                        "ORDER BY key",
                    ).fetchall()
                return [
                    CounterValue(key=r[0], value=int(r[1]),
                                 updated_at=float(r[2]))
                    for r in rows
                ]
            finally:
                self._close_conn(conn)

    def total(self, prefix: str = "") -> int:
        """Return the sum of all values whose key starts with *prefix*."""
        with self._lock:
            conn = self._connect()
            try:
                if prefix:
                    pattern = prefix.replace("\\", "\\\\") \
                                    .replace("%", "\\%") \
                                    .replace("_", "\\_") + "%"
                    row = conn.execute(
                        "SELECT COALESCE(SUM(value), 0) FROM counters "
                        "WHERE key LIKE ? ESCAPE '\\'",
                        (pattern,),
                    ).fetchone()
                else:
                    row = conn.execute(
                        "SELECT COALESCE(SUM(value), 0) FROM counters"
                    ).fetchone()
                return int(row[0])
            finally:
                self._close_conn(conn)

    def count(self) -> int:
        """Return the number of counter rows."""
        with self._lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT COUNT(*) FROM counters"
                ).fetchone()
                return int(row[0])
            finally:
                self._close_conn(conn)

    def reset(self, prefix: str = "") -> int:
        """Delete all rows whose key starts with *prefix* (or all rows if
        *prefix* is empty).  Returns the number of rows deleted.
        """
        with self._lock:
            conn = self._connect()
            try:
                if prefix:
                    pattern = prefix.replace("\\", "\\\\") \
                                    .replace("%", "\\%") \
                                    .replace("_", "\\_") + "%"
                    cur = conn.execute(
                        "DELETE FROM counters WHERE key LIKE ? ESCAPE '\\'",
                        (pattern,),
                    )
                else:
                    cur = conn.execute("DELETE FROM counters")
                conn.commit()
                return cur.rowcount if cur.rowcount is not None else 0
            finally:
                self._close_conn(conn)

    def close(self) -> None:
        """Close the underlying connection (only meaningful for in-memory)."""
        with self._lock:
            if self._mem_conn is not None:
                try:
                    self._mem_conn.close()
                except sqlite3.Error:
                    pass
                self._mem_conn = None
            self._closed = True
