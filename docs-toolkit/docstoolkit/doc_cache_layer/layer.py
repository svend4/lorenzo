"""DocCacheLayer implementation — LRU+TTL cache.

Pure stdlib, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CacheEntry:
    """Single cache entry."""

    key: str
    value: object
    stored_at: float = 0.0
    expires_at: Optional[float] = None
    hit_count: int = 0


@dataclass
class CacheStats:
    """Aggregate cache statistics."""

    size: int
    capacity: int
    hit_count: int
    miss_count: int
    eviction_count: int
    expiry_count: int


class DocCacheLayer:
    """LRU+TTL cache for document data.

    Uses :class:`collections.OrderedDict` for LRU tracking. Entries are
    moved to the end on access. Optional per-entry TTL controls expiry.

    Thread-safe via an internal :class:`threading.Lock`.
    """

    def __init__(self, capacity: int = 128) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._capacity: int = capacity
        self._cache: "OrderedDict[str, CacheEntry]" = OrderedDict()
        self._hits: int = 0
        self._misses: int = 0
        self._evictions: int = 0
        self._expiries: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else now

    @staticmethod
    def _is_expired(entry: CacheEntry, now: float) -> bool:
        return entry.expires_at is not None and now >= entry.expires_at

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------
    def put(
        self,
        key: str,
        value: object,
        ttl_seconds: Optional[float] = None,
        now: Optional[float] = None,
    ) -> None:
        """Store entry. Updates value+expires_at if key already present.

        Evicts oldest entry if cache full (LRU semantics).
        """
        ts = self._now(now)
        expires_at: Optional[float]
        if ttl_seconds is None:
            expires_at = None
        else:
            expires_at = ts + ttl_seconds
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                entry.value = value
                entry.stored_at = ts
                entry.expires_at = expires_at
                self._cache.move_to_end(key)
                return
            if len(self._cache) >= self._capacity:
                self._cache.popitem(last=False)
                self._evictions += 1
            self._cache[key] = CacheEntry(
                key=key,
                value=value,
                stored_at=ts,
                expires_at=expires_at,
                hit_count=0,
            )

    def get(self, key: str, now: Optional[float] = None) -> Optional[object]:
        """Return value or None. Updates LRU + hit counters."""
        ts = self._now(now)
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None
            if self._is_expired(entry, ts):
                del self._cache[key]
                self._expiries += 1
                self._misses += 1
                return None
            entry.hit_count += 1
            self._hits += 1
            self._cache.move_to_end(key)
            return entry.value

    def peek(self, key: str, now: Optional[float] = None) -> Optional[object]:
        """Return value without updating LRU order or hit counters.

        Expired entries are still removed and counted as expiry.
        """
        ts = self._now(now)
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            if self._is_expired(entry, ts):
                del self._cache[key]
                self._expiries += 1
                return None
            return entry.value

    def delete(self, key: str) -> bool:
        """Remove entry. Return True if existed."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> int:
        """Remove all entries. Return count removed."""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    # ------------------------------------------------------------------
    # Read-only queries
    # ------------------------------------------------------------------
    def contains(self, key: str, now: Optional[float] = None) -> bool:
        """True if key present and not expired. Does not affect LRU/counters."""
        ts = self._now(now)
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return False
            if self._is_expired(entry, ts):
                return False
            return True

    def size(self) -> int:
        """Return count of non-expired entries (does not remove them)."""
        now = time.time()
        with self._lock:
            return sum(
                1 for e in self._cache.values() if not self._is_expired(e, now)
            )

    def purge_expired(self, now: Optional[float] = None) -> int:
        """Actively remove expired entries. Return count removed."""
        ts = self._now(now)
        with self._lock:
            expired_keys = [
                k for k, e in self._cache.items() if self._is_expired(e, ts)
            ]
            for k in expired_keys:
                del self._cache[k]
            self._expiries += len(expired_keys)
            return len(expired_keys)

    def keys(self) -> list[str]:
        """Sorted list of all keys (may include expired)."""
        with self._lock:
            return sorted(self._cache.keys())

    def stats(self) -> CacheStats:
        """Snapshot of current statistics."""
        with self._lock:
            return CacheStats(
                size=len(self._cache),
                capacity=self._capacity,
                hit_count=self._hits,
                miss_count=self._misses,
                eviction_count=self._evictions,
                expiry_count=self._expiries,
            )
