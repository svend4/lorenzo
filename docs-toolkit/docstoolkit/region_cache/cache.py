"""Region-aware multi-tier cache (L1 in-memory, L2 SQLite).

Values must be JSON-serialisable (``str``, ``int``, ``float``, ``bool``,
``None``, ``list``, ``dict`` of these). Non-serialisable values raise
``TypeError`` at :meth:`RegionCache.set` time.

The cache organises entries by *region*. Each region keeps its own LRU
window; when the global L1 capacity is exceeded the least recently used
entry is automatically demoted to the persistent L2 (SQLite) tier.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class CacheTier(Enum):
    """Tier where an entry currently lives (or :attr:`MISS` if absent)."""

    L1 = "l1"
    L2 = "l2"
    MISS = "miss"


@dataclass
class CacheEntry:
    """A cached value plus bookkeeping metadata."""

    key: str
    value: Any
    tier: CacheTier
    region: str = "default"
    created_at: float = 0.0
    accessed_at: float = 0.0
    access_count: int = 0
    expires_at: Optional[float] = None


@dataclass
class RegionStats:
    """Per-region statistics snapshot."""

    region: str
    l1_size: int = 0
    l2_size: int = 0
    l1_hits: int = 0
    l2_hits: int = 0
    misses: int = 0

    @property
    def hit_rate(self) -> float:
        """Hit rate ``(l1_hits + l2_hits) / total_lookups``.

        Returns ``0.0`` when no lookups have been performed.
        """
        total = self.l1_hits + self.l2_hits + self.misses
        if total == 0:
            return 0.0
        return (self.l1_hits + self.l2_hits) / total


class RegionCache:
    """Two-tier region-aware cache with automatic LRU demotion.

    Parameters
    ----------
    l1_capacity:
        Maximum number of entries kept in the fast L1 dictionary across
        *all* regions. When exceeded, the least-recently-used entry is
        demoted to L2.
    db_path:
        SQLite database path. ``":memory:"`` keeps L2 in process memory.
    """

    _SCHEMA = """
        CREATE TABLE IF NOT EXISTS entries (
            region TEXT NOT NULL,
            key TEXT NOT NULL,
            value_json TEXT NOT NULL,
            created_at REAL NOT NULL,
            accessed_at REAL NOT NULL,
            access_count INTEGER NOT NULL,
            expires_at REAL,
            PRIMARY KEY (region, key)
        )
    """

    def __init__(self, l1_capacity: int = 100, db_path: str = ":memory:") -> None:
        if l1_capacity < 1:
            raise ValueError("l1_capacity must be >= 1")
        self.l1_capacity = l1_capacity
        self.db_path = db_path
        self._lock = threading.RLock()
        # OrderedDict acts as global LRU across regions, keyed by (region, key).
        self._l1: "OrderedDict[Tuple[str, str], CacheEntry]" = OrderedDict()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(self._SCHEMA)
        self._conn.commit()
        # Per-region stats counters.
        self._stats: Dict[str, RegionStats] = {}
        self._closed = False

    # ------------------------------------------------------------------ utils
    def _stats_for(self, region: str) -> RegionStats:
        s = self._stats.get(region)
        if s is None:
            s = RegionStats(region=region)
            self._stats[region] = s
        return s

    @staticmethod
    def _serialize(value: Any) -> str:
        try:
            return json.dumps(value)
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"RegionCache values must be JSON-serialisable: {exc}"
            ) from exc

    @staticmethod
    def _deserialize(blob: str) -> Any:
        return json.loads(blob)

    def _is_expired(self, entry: CacheEntry, now: float) -> bool:
        return entry.expires_at is not None and now > 0.0 and now >= entry.expires_at

    def _l2_count(self, region: Optional[str] = None) -> int:
        cur = self._conn.cursor()
        if region is None:
            cur.execute("SELECT COUNT(*) FROM entries")
        else:
            cur.execute("SELECT COUNT(*) FROM entries WHERE region = ?", (region,))
        return int(cur.fetchone()[0])

    def _l2_fetch(self, region: str, key: str) -> Optional[CacheEntry]:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT value_json, created_at, accessed_at, access_count, expires_at "
            "FROM entries WHERE region = ? AND key = ?",
            (region, key),
        )
        row = cur.fetchone()
        if row is None:
            return None
        value_json, created_at, accessed_at, access_count, expires_at = row
        return CacheEntry(
            key=key,
            value=self._deserialize(value_json),
            tier=CacheTier.L2,
            region=region,
            created_at=created_at,
            accessed_at=accessed_at,
            access_count=access_count,
            expires_at=expires_at,
        )

    def _l2_write(self, entry: CacheEntry) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO entries "
            "(region, key, value_json, created_at, accessed_at, access_count, expires_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                entry.region,
                entry.key,
                self._serialize(entry.value),
                entry.created_at,
                entry.accessed_at,
                entry.access_count,
                entry.expires_at,
            ),
        )
        self._conn.commit()

    def _l2_delete(self, region: str, key: str) -> bool:
        cur = self._conn.execute(
            "DELETE FROM entries WHERE region = ? AND key = ?", (region, key)
        )
        self._conn.commit()
        return cur.rowcount > 0

    def _evict_if_needed(self) -> None:
        """If L1 is over capacity, demote LRU entries to L2."""
        while len(self._l1) > self.l1_capacity:
            (region, key), entry = self._l1.popitem(last=False)
            entry.tier = CacheTier.L2
            self._l2_write(entry)

    # ------------------------------------------------------------------ API
    def set(
        self,
        key: str,
        value: Any,
        region: str = "default",
        expires_at: Optional[float] = None,
        now: float = 0.0,
    ) -> CacheEntry:
        """Insert or overwrite ``key`` in ``region``. Returns the entry."""
        # Validate value serialisability early.
        self._serialize(value)
        with self._lock:
            self._stats_for(region)
            entry = CacheEntry(
                key=key,
                value=value,
                tier=CacheTier.L1,
                region=region,
                created_at=now,
                accessed_at=now,
                access_count=0,
                expires_at=expires_at,
            )
            # Ensure no stale L2 copy lingers under the same composite key.
            self._l2_delete(region, key)
            # Place into L1 (or move to MRU position).
            cache_key = (region, key)
            if cache_key in self._l1:
                self._l1.move_to_end(cache_key, last=True)
            self._l1[cache_key] = entry
            self._evict_if_needed()
            return entry

    def get(
        self,
        key: str,
        region: str = "default",
        now: float = 0.0,
    ) -> Tuple[CacheTier, Any]:
        """Look up ``key`` in ``region``.

        Returns ``(CacheTier.L1|L2, value)`` on hit and
        ``(CacheTier.MISS, None)`` on miss. Expired entries are evicted
        and reported as MISS.
        """
        with self._lock:
            stats = self._stats_for(region)
            cache_key = (region, key)
            entry = self._l1.get(cache_key)
            if entry is not None:
                if self._is_expired(entry, now):
                    del self._l1[cache_key]
                    stats.misses += 1
                    return CacheTier.MISS, None
                entry.accessed_at = now
                entry.access_count += 1
                self._l1.move_to_end(cache_key, last=True)
                stats.l1_hits += 1
                return CacheTier.L1, entry.value

            # L2 lookup.
            entry = self._l2_fetch(region, key)
            if entry is None:
                stats.misses += 1
                return CacheTier.MISS, None
            if self._is_expired(entry, now):
                self._l2_delete(region, key)
                stats.misses += 1
                return CacheTier.MISS, None
            entry.accessed_at = now
            entry.access_count += 1
            # Persist updated bookkeeping in L2 (entry stays in L2 until
            # ``promote`` is called explicitly).
            self._l2_write(entry)
            stats.l2_hits += 1
            return CacheTier.L2, entry.value

    def delete(self, key: str, region: str = "default") -> bool:
        """Remove ``key`` from both tiers. Returns ``True`` if anything was removed."""
        with self._lock:
            cache_key = (region, key)
            removed = False
            if cache_key in self._l1:
                del self._l1[cache_key]
                removed = True
            if self._l2_delete(region, key):
                removed = True
            return removed

    def promote(self, key: str, region: str = "default") -> bool:
        """Move an L2 entry up to L1. Returns ``False`` if not in L2."""
        with self._lock:
            cache_key = (region, key)
            if cache_key in self._l1:
                # Already L1; treat as no-op success.
                self._l1.move_to_end(cache_key, last=True)
                return True
            entry = self._l2_fetch(region, key)
            if entry is None:
                return False
            self._l2_delete(region, key)
            entry.tier = CacheTier.L1
            self._l1[cache_key] = entry
            self._evict_if_needed()
            return True

    def demote(self, key: str, region: str = "default") -> bool:
        """Push an L1 entry down to L2. Returns ``False`` if not in L1."""
        with self._lock:
            cache_key = (region, key)
            entry = self._l1.pop(cache_key, None)
            if entry is None:
                return False
            entry.tier = CacheTier.L2
            self._l2_write(entry)
            return True

    def clear_region(self, region: str) -> int:
        """Drop every entry for ``region`` from both tiers; return removed count."""
        with self._lock:
            removed = 0
            keys = [k for k in self._l1 if k[0] == region]
            for k in keys:
                del self._l1[k]
                removed += 1
            cur = self._conn.execute(
                "DELETE FROM entries WHERE region = ?", (region,)
            )
            self._conn.commit()
            removed += cur.rowcount
            # Reset stats counters for this region but keep it registered.
            if region in self._stats:
                self._stats[region] = RegionStats(region=region)
            return removed

    def clear_all(self) -> int:
        """Drop every entry from both tiers; return removed count."""
        with self._lock:
            removed = len(self._l1)
            self._l1.clear()
            removed += self._l2_count()
            self._conn.execute("DELETE FROM entries")
            self._conn.commit()
            self._stats.clear()
            return removed

    def stats(self, region: Optional[str] = None) -> Dict[str, RegionStats]:
        """Return per-region stats snapshots.

        Pass ``region`` to get a single-region dict; otherwise all known
        regions (including those that appear only in L2) are returned.
        """
        with self._lock:
            if region is not None:
                snap = self._snapshot_stats(region)
                return {region: snap}
            regions = set(self._stats.keys())
            for (r, _) in self._l1.keys():
                regions.add(r)
            cur = self._conn.execute("SELECT DISTINCT region FROM entries")
            for (r,) in cur.fetchall():
                regions.add(r)
            return {r: self._snapshot_stats(r) for r in sorted(regions)}

    def _snapshot_stats(self, region: str) -> RegionStats:
        base = self._stats.get(region) or RegionStats(region=region)
        l1_size = sum(1 for k in self._l1 if k[0] == region)
        l2_size = self._l2_count(region)
        return RegionStats(
            region=region,
            l1_size=l1_size,
            l2_size=l2_size,
            l1_hits=base.l1_hits,
            l2_hits=base.l2_hits,
            misses=base.misses,
        )

    def regions(self) -> List[str]:
        """Return a sorted list of regions known to the cache."""
        with self._lock:
            seen = set(self._stats.keys())
            for (r, _) in self._l1.keys():
                seen.add(r)
            cur = self._conn.execute("SELECT DISTINCT region FROM entries")
            for (r,) in cur.fetchall():
                seen.add(r)
            return sorted(seen)

    def cleanup_expired(self, now: float = 0.0) -> int:
        """Remove every entry whose ``expires_at`` is in the past; return count."""
        with self._lock:
            removed = 0
            # L1 sweep.
            for cache_key in list(self._l1.keys()):
                entry = self._l1[cache_key]
                if self._is_expired(entry, now):
                    del self._l1[cache_key]
                    removed += 1
            # L2 sweep.
            cur = self._conn.execute(
                "DELETE FROM entries WHERE expires_at IS NOT NULL AND expires_at <= ?",
                (now,),
            )
            self._conn.commit()
            removed += cur.rowcount
            return removed

    def size(self, region: Optional[str] = None) -> int:
        """Total entries across both tiers (optionally filtered by region)."""
        with self._lock:
            if region is None:
                return len(self._l1) + self._l2_count()
            l1 = sum(1 for k in self._l1 if k[0] == region)
            return l1 + self._l2_count(region)

    def close(self) -> None:
        """Release the SQLite connection. Idempotent."""
        with self._lock:
            if self._closed:
                return
            self._conn.close()
            self._closed = True

    # Context-manager sugar.
    def __enter__(self) -> "RegionCache":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
