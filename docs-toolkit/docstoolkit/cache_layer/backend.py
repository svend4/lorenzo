"""Cache backend implementations: in-memory and SQLite-backed."""
from __future__ import annotations

import sqlite3
import threading
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Optional


class CacheBackend(ABC):
    """Abstract base class for cache backends."""

    @abstractmethod
    def get(self, key: str) -> Optional[bytes]:
        """Return cached bytes for *key*, or None if missing/expired."""

    @abstractmethod
    def set(self, key: str, value: bytes, ttl: Optional[float] = None) -> None:
        """Store *value* bytes under *key* with optional TTL (seconds)."""

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Remove *key*. Return True if the key existed."""

    @abstractmethod
    def clear(self) -> int:
        """Remove all entries. Return the number of entries deleted."""

    @abstractmethod
    def size(self) -> int:
        """Return the number of currently-stored (non-expired) entries."""


# ---------------------------------------------------------------------------
# MemoryBackend
# ---------------------------------------------------------------------------

class MemoryBackend(CacheBackend):
    """In-memory cache backend with per-entry TTL tracking.

    Entries are stored in an :class:`~collections.OrderedDict` so insertion
    order is preserved (useful for LRU eviction at a higher layer).

    Thread-safety: a :class:`threading.Lock` guards all mutations.
    """

    def __init__(self) -> None:
        # key -> (value_bytes, expiry_timestamp_or_None)
        self._store: OrderedDict[str, tuple[bytes, Optional[float]]] = OrderedDict()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_expired(self, expiry: Optional[float]) -> bool:
        """Return True when *expiry* is set and has passed."""
        if expiry is None:
            return False
        return time.monotonic() >= expiry

    # ------------------------------------------------------------------
    # CacheBackend interface
    # ------------------------------------------------------------------

    def get(self, key: str) -> Optional[bytes]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expiry = entry
            if self._is_expired(expiry):
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: bytes, ttl: Optional[float] = None) -> None:
        expiry = (time.monotonic() + ttl) if ttl is not None else None
        with self._lock:
            self._store[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def clear(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count

    def size(self) -> int:
        now = time.monotonic()
        with self._lock:
            return sum(
                1
                for _value, expiry in self._store.values()
                if expiry is None or now < expiry
            )


# ---------------------------------------------------------------------------
# SqliteBackend
# ---------------------------------------------------------------------------

class SqliteBackend(CacheBackend):
    """SQLite-backed cache backend.

    Parameters
    ----------
    path:
        File-system path for the SQLite database, or ``":memory:"`` (default)
        for a purely in-process store.

    TTL semantics
    -------------
    The expiry time is stored as a REAL (Unix epoch, ``time.time()``).
    Expired rows are evicted lazily on ``get`` access and eagerly during
    ``size()`` / ``clear()``.
    """

    _CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS cache (
            key      TEXT PRIMARY KEY,
            value    BLOB NOT NULL,
            expiry   REAL          -- NULL means never expires
        )
    """

    def __init__(self, path: str = ":memory:") -> None:
        self._path = path
        # check_same_thread=False + our own lock lets multiple Python threads
        # share the same connection safely.
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock:
            self._conn.execute(self._CREATE_TABLE)
            self._conn.commit()

    # ------------------------------------------------------------------
    # CacheBackend interface
    # ------------------------------------------------------------------

    def get(self, key: str) -> Optional[bytes]:
        now = time.time()
        with self._lock:
            row = self._conn.execute(
                "SELECT value, expiry FROM cache WHERE key = ?", (key,)
            ).fetchone()
            if row is None:
                return None
            value, expiry = row
            if expiry is not None and now >= expiry:
                self._conn.execute("DELETE FROM cache WHERE key = ?", (key,))
                self._conn.commit()
                return None
            return value

    def set(self, key: str, value: bytes, ttl: Optional[float] = None) -> None:
        expiry = (time.time() + ttl) if ttl is not None else None
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO cache (key, value, expiry) VALUES (?, ?, ?)",
                (key, value, expiry),
            )
            self._conn.commit()

    def delete(self, key: str) -> bool:
        with self._lock:
            cursor = self._conn.execute(
                "DELETE FROM cache WHERE key = ?", (key,)
            )
            self._conn.commit()
            return cursor.rowcount > 0

    def clear(self) -> int:
        with self._lock:
            cursor = self._conn.execute("DELETE FROM cache")
            self._conn.commit()
            return cursor.rowcount

    def size(self) -> int:
        now = time.time()
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) FROM cache WHERE expiry IS NULL OR expiry > ?",
                (now,),
            ).fetchone()
            return row[0] if row else 0

    # ------------------------------------------------------------------
    # Resource management
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass
