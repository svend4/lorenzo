"""Cache entry types and status enumeration."""
import time
from dataclasses import dataclass, field
from enum import Enum


class CacheStatus(str, Enum):
    HIT = "hit"
    MISS = "miss"
    STALE = "stale"
    EXPIRED = "expired"


@dataclass
class CacheEntry:
    """A single cached response entry."""
    cache_key: str
    value: str
    created_ts: float
    ttl_seconds: float
    hit_count: int = 0
    last_accessed: float = 0.0

    def is_expired(self, now: float = None) -> bool:
        """Return True if the entry's TTL has elapsed."""
        if now is None:
            now = time.time()
        return (now - self.created_ts) >= self.ttl_seconds

    def is_stale(self, stale_after: float, now: float = None) -> bool:
        """Return True if age > stale_after but the entry is not yet expired."""
        if now is None:
            now = time.time()
        age = now - self.created_ts
        return age > stale_after and not self.is_expired(now)

    def touch(self, now: float = None) -> "CacheEntry":
        """Return a new entry with incremented hit_count and updated last_accessed."""
        if now is None:
            now = time.time()
        return CacheEntry(
            cache_key=self.cache_key,
            value=self.value,
            created_ts=self.created_ts,
            ttl_seconds=self.ttl_seconds,
            hit_count=self.hit_count + 1,
            last_accessed=now,
        )
