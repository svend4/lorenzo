"""High-level ResponseCache with config, lookup results and eviction."""
import time
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.response_cache.entry import CacheEntry, CacheStatus
from docstoolkit.response_cache.store import ResponseCacheStore


@dataclass
class CacheConfig:
    """Configuration for ResponseCache."""
    ttl_seconds: float = 600.0
    stale_after: float = 300.0
    max_size: int = 1000


@dataclass
class CacheLookupResult:
    """Result returned by ResponseCache.get()."""
    status: CacheStatus
    value: Optional[str]
    cache_key: str
    age_seconds: float = 0.0


class ResponseCache:
    """Caching layer with HIT/STALE/EXPIRED/MISS semantics."""

    def __init__(self, config: CacheConfig = None, store: ResponseCacheStore = None):
        self._config = config or CacheConfig()
        self._store = store or ResponseCacheStore()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, cache_key: str, now: float = None) -> CacheLookupResult:
        """Look up cache_key and return a CacheLookupResult.

        Status rules:
        - MISS    — key not in store
        - EXPIRED — entry exists but TTL has elapsed; value is None
        - STALE   — entry exists, not expired, but age > stale_after; value returned
        - HIT     — entry exists and is fresh
        """
        if now is None:
            now = time.time()

        entry = self._store.get(cache_key)
        if entry is None:
            return CacheLookupResult(
                status=CacheStatus.MISS,
                value=None,
                cache_key=cache_key,
                age_seconds=0.0,
            )

        age = now - entry.created_ts

        if entry.is_expired(now):
            return CacheLookupResult(
                status=CacheStatus.EXPIRED,
                value=None,
                cache_key=cache_key,
                age_seconds=age,
            )

        # Entry is live — touch it to record the access.
        touched = entry.touch(now)
        self._store.set(touched)

        if entry.is_stale(self._config.stale_after, now):
            return CacheLookupResult(
                status=CacheStatus.STALE,
                value=touched.value,
                cache_key=cache_key,
                age_seconds=age,
            )

        return CacheLookupResult(
            status=CacheStatus.HIT,
            value=touched.value,
            cache_key=cache_key,
            age_seconds=age,
        )

    def set(
        self,
        cache_key: str,
        value: str,
        ttl_seconds: float = None,
        now: float = None,
    ) -> None:
        """Store value under cache_key with optional TTL override."""
        if now is None:
            now = time.time()
        ttl = ttl_seconds if ttl_seconds is not None else self._config.ttl_seconds
        entry = CacheEntry(
            cache_key=cache_key,
            value=value,
            created_ts=now,
            ttl_seconds=ttl,
            hit_count=0,
            last_accessed=now,
        )
        self._store.set(entry)

    def invalidate(self, cache_key: str) -> bool:
        """Remove cache_key from the store. Returns True if it existed."""
        return self._store.delete(cache_key)

    def evict(self, now: float = None) -> int:
        """Run expired eviction then LRU trim. Returns total rows removed."""
        if now is None:
            now = time.time()
        removed = self._store.evict_expired(now)
        removed += self._store.evict_lru(self._config.max_size)
        return removed

    def stats(self) -> dict:
        """Return store statistics."""
        return self._store.stats()
