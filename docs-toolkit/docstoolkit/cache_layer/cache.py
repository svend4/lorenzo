"""High-level CacheLayer combining a backend, a serializer, and a config."""
from __future__ import annotations

import random
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from docstoolkit.cache_layer.backend import CacheBackend, MemoryBackend
from docstoolkit.cache_layer.serializer import JsonSerializer, Serializer


# ---------------------------------------------------------------------------
# Configuration & statistics
# ---------------------------------------------------------------------------

@dataclass
class CacheConfig:
    """Configuration parameters for :class:`CacheLayer`."""

    default_ttl: float = 300.0
    """Default TTL (seconds) applied when ``ttl`` is not specified in calls."""

    max_size: int = 1000
    """Maximum number of entries before eviction is triggered."""

    eviction_policy: str = "lru"
    """Eviction policy: ``"lru"``, ``"ttl"``, or ``"random"``."""


@dataclass
class CacheStats:
    """Accumulates runtime statistics for a :class:`CacheLayer`."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0

    def hit_rate(self) -> float:
        """Return the fraction of lookups that were cache hits.

        Returns ``0.0`` when no lookups have been performed yet.
        """
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total


# ---------------------------------------------------------------------------
# CacheLayer
# ---------------------------------------------------------------------------

class CacheLayer:
    """High-level cache facade.

    Wraps a :class:`~docstoolkit.cache_layer.backend.CacheBackend` with:

    * Optional serialization via a :class:`~docstoolkit.cache_layer.serializer.Serializer`
    * Automatic TTL application from :class:`CacheConfig`
    * Size-bounded eviction (``max_size``)
    * Hit/miss statistics via :class:`CacheStats`

    Parameters
    ----------
    backend:
        Storage backend.  Defaults to a fresh :class:`MemoryBackend`.
    serializer:
        Value serializer.  Defaults to :class:`JsonSerializer`.
    config:
        Layer configuration.  Defaults to ``CacheConfig()``.
    """

    def __init__(
        self,
        backend: Optional[CacheBackend] = None,
        serializer: Optional[Serializer] = None,
        config: Optional[CacheConfig] = None,
    ) -> None:
        self._backend: CacheBackend = backend if backend is not None else MemoryBackend()
        self._serializer: Serializer = serializer if serializer is not None else JsonSerializer()
        self._config: CacheConfig = config if config is not None else CacheConfig()
        self._stats = CacheStats()
        self._lock = threading.Lock()
        # Track insertion order for LRU / TTL eviction (key → ttl_used).
        # We maintain this independently so we don't rely on backend iteration.
        self._order: "list[str]" = []  # ordered list of keys (oldest first)
        self._key_ttl: "dict[str, Optional[float]]" = {}  # key → ttl at insertion

    # ------------------------------------------------------------------
    # Eviction helpers
    # ------------------------------------------------------------------

    def _register_key(self, key: str, ttl: Optional[float]) -> None:
        """Register a new key for eviction bookkeeping (caller holds _lock)."""
        if key in self._key_ttl:
            self._order.remove(key)
        self._order.append(key)
        self._key_ttl[key] = ttl

    def _touch_key(self, key: str) -> None:
        """Move *key* to the end (most-recently-used) position (caller holds _lock)."""
        if key in self._key_ttl:
            self._order.remove(key)
            self._order.append(key)

    def _evict_if_needed(self) -> None:
        """Evict entries until ``backend.size() <= max_size`` (caller holds _lock)."""
        max_size = self._config.max_size
        while self._backend.size() > max_size and self._order:
            policy = self._config.eviction_policy
            if policy == "lru":
                victim = self._order[0]
            elif policy == "ttl":
                # Evict the entry with the smallest TTL value (expires soonest).
                # Fall back to LRU order when all TTLs are None.
                candidates_with_ttl = [
                    k for k in self._order if self._key_ttl.get(k) is not None
                ]
                if candidates_with_ttl:
                    victim = min(candidates_with_ttl, key=lambda k: self._key_ttl[k])  # type: ignore[arg-type]
                else:
                    victim = self._order[0]
            elif policy == "random":
                victim = random.choice(self._order)  # noqa: S311
            else:
                victim = self._order[0]

            self._backend.delete(victim)
            if victim in self._key_ttl:
                del self._key_ttl[victim]
            if victim in self._order:
                self._order.remove(victim)
            self._stats.evictions += 1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str) -> Optional[Any]:
        """Return the deserialized value for *key*, or ``None`` on miss/expiry."""
        raw = self._backend.get(key)
        if raw is None:
            with self._lock:
                self._stats.misses += 1
                # Key may have been evicted from backend; clean up bookkeeping.
                if key in self._key_ttl:
                    self._key_ttl.pop(key, None)
                    try:
                        self._order.remove(key)
                    except ValueError:
                        pass
            return None
        with self._lock:
            self._stats.hits += 1
            self._touch_key(key)
        return self._serializer.deserialize(raw)

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Serialize *value* and store it under *key*.

        Uses ``config.default_ttl`` when *ttl* is ``None``.
        Triggers eviction if the backend exceeds ``config.max_size``.
        """
        effective_ttl: Optional[float] = ttl if ttl is not None else self._config.default_ttl
        raw = self._serializer.serialize(value)
        with self._lock:
            self._backend.set(key, raw, effective_ttl)
            self._register_key(key, effective_ttl)
            self._evict_if_needed()

    def delete(self, key: str) -> bool:
        """Remove *key* from the cache. Returns ``True`` if it existed."""
        result = self._backend.delete(key)
        with self._lock:
            self._key_ttl.pop(key, None)
            try:
                self._order.remove(key)
            except ValueError:
                pass
        return result

    def clear(self) -> int:
        """Remove all entries. Returns the count of deleted entries."""
        count = self._backend.clear()
        with self._lock:
            self._order.clear()
            self._key_ttl.clear()
        return count

    def stats(self) -> CacheStats:
        """Return a snapshot of current statistics."""
        with self._lock:
            return CacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
            )

    def get_or_set(
        self,
        key: str,
        factory: Callable[[], Any],
        ttl: Optional[float] = None,
    ) -> Any:
        """Return cached value for *key*, computing it via *factory* on miss.

        The computed value is stored in the cache before being returned.
        """
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl=ttl)
        return value
