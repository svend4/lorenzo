"""Implementation of :class:`DocCacheInvalidation` (E262)."""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class InvalidationStrategy(Enum):
    """Strategy used to invalidate cache entries."""

    TTL = "ttl"
    MANUAL = "manual"
    DEPENDENCY = "dependency"
    TAG = "tag"
    PATTERN = "pattern"


@dataclass
class CacheKey:
    """A single cache entry."""

    key: str
    doc_id: str
    value: Any
    created_at: float
    expires_at: Optional[float] = None
    tags: set[str] = field(default_factory=set)
    dependencies: set[str] = field(default_factory=set)


@dataclass
class InvalidationEvent:
    """Record of an invalidation action."""

    event_id: int
    strategy: InvalidationStrategy
    keys_invalidated: list[str]
    timestamp: float
    reason: Optional[str] = None


@dataclass
class CacheStats:
    """Aggregate cache statistics."""

    total_entries: int
    total_invalidations: int
    hit_count: int
    miss_count: int

    @property
    def hit_rate(self) -> float:
        total = self.hit_count + self.miss_count
        if total == 0:
            return 0.0
        return self.hit_count / total


class DocCacheInvalidation:
    """Thread-safe document cache with pattern-based invalidation."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: dict[str, CacheKey] = {}
        self._events: list[InvalidationEvent] = []
        self._next_event_id: int = 1
        self._hit_count: int = 0
        self._miss_count: int = 0
        # Secondary indexes
        self._by_doc: dict[str, set[str]] = {}
        self._by_tag: dict[str, set[str]] = {}
        self._by_dep: dict[str, set[str]] = {}

    # ------------------------------------------------------------------ helpers
    def _index_add(self, entry: CacheKey) -> None:
        self._by_doc.setdefault(entry.doc_id, set()).add(entry.key)
        for tag in entry.tags:
            self._by_tag.setdefault(tag, set()).add(entry.key)
        for dep in entry.dependencies:
            self._by_dep.setdefault(dep, set()).add(entry.key)

    def _index_remove(self, entry: CacheKey) -> None:
        bucket = self._by_doc.get(entry.doc_id)
        if bucket is not None:
            bucket.discard(entry.key)
            if not bucket:
                self._by_doc.pop(entry.doc_id, None)
        for tag in entry.tags:
            bucket = self._by_tag.get(tag)
            if bucket is not None:
                bucket.discard(entry.key)
                if not bucket:
                    self._by_tag.pop(tag, None)
        for dep in entry.dependencies:
            bucket = self._by_dep.get(dep)
            if bucket is not None:
                bucket.discard(entry.key)
                if not bucket:
                    self._by_dep.pop(dep, None)

    def _record_event(
        self,
        strategy: InvalidationStrategy,
        keys: list[str],
        timestamp: float,
        reason: Optional[str],
    ) -> InvalidationEvent:
        event = InvalidationEvent(
            event_id=self._next_event_id,
            strategy=strategy,
            keys_invalidated=list(keys),
            timestamp=timestamp,
            reason=reason,
        )
        self._next_event_id += 1
        self._events.append(event)
        return event

    def _invalidate_keys(
        self,
        keys: list[str],
        strategy: InvalidationStrategy,
        reason: Optional[str],
        now: float,
    ) -> int:
        removed: list[str] = []
        for key in keys:
            entry = self._entries.pop(key, None)
            if entry is None:
                continue
            self._index_remove(entry)
            removed.append(key)
        if removed:
            self._record_event(strategy, removed, now, reason)
        return len(removed)

    # --------------------------------------------------------------- basic ops
    def set(
        self,
        key: str,
        doc_id: str,
        value: Any,
        ttl: Optional[float] = None,
        tags: Optional[set[str]] = None,
        dependencies: Optional[set[str]] = None,
        now: float = 0.0,
    ) -> CacheKey:
        tag_set = set(tags) if tags else set()
        dep_set = set(dependencies) if dependencies else set()
        expires_at = now + ttl if ttl is not None else None
        entry = CacheKey(
            key=key,
            doc_id=doc_id,
            value=value,
            created_at=now,
            expires_at=expires_at,
            tags=tag_set,
            dependencies=dep_set,
        )
        with self._lock:
            existing = self._entries.get(key)
            if existing is not None:
                self._index_remove(existing)
            self._entries[key] = entry
            self._index_add(entry)
        return entry

    def get(self, key: str, now: float = 0.0) -> Any:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                self._miss_count += 1
                return None
            if entry.expires_at is not None and now >= entry.expires_at:
                # expire it
                self._index_remove(entry)
                self._entries.pop(key, None)
                self._record_event(
                    InvalidationStrategy.TTL, [key], now, "expired"
                )
                self._miss_count += 1
                return None
            self._hit_count += 1
            return entry.value

    def delete(self, key: str) -> bool:
        with self._lock:
            entry = self._entries.pop(key, None)
            if entry is None:
                return False
            self._index_remove(entry)
            self._record_event(
                InvalidationStrategy.MANUAL, [key], entry.created_at, "delete"
            )
            return True

    def has(self, key: str, now: float = 0.0) -> bool:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return False
            if entry.expires_at is not None and now >= entry.expires_at:
                return False
            return True

    # ------------------------------------------------------------- invalidation
    def invalidate_by_doc(
        self,
        doc_id: str,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        with self._lock:
            keys = list(self._by_doc.get(doc_id, set()))
            return self._invalidate_keys(
                keys, InvalidationStrategy.MANUAL, reason, now
            )

    def invalidate_by_tag(
        self,
        tag: str,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        with self._lock:
            keys = list(self._by_tag.get(tag, set()))
            return self._invalidate_keys(
                keys, InvalidationStrategy.TAG, reason, now
            )

    def invalidate_by_tags(
        self,
        tags: set[str],
        match_all: bool = False,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        with self._lock:
            if not tags:
                return 0
            sets = [self._by_tag.get(t, set()) for t in tags]
            if match_all:
                if any(not s for s in sets):
                    matched: set[str] = set()
                else:
                    matched = set(sets[0])
                    for s in sets[1:]:
                        matched &= s
            else:
                matched = set()
                for s in sets:
                    matched |= s
            keys = list(matched)
            return self._invalidate_keys(
                keys, InvalidationStrategy.TAG, reason, now
            )

    def invalidate_by_pattern(
        self,
        regex_pattern: str,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        compiled = re.compile(regex_pattern)
        with self._lock:
            keys = [k for k in self._entries.keys() if compiled.search(k)]
            return self._invalidate_keys(
                keys, InvalidationStrategy.PATTERN, reason, now
            )

    def invalidate_dependency(
        self,
        doc_id: str,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        with self._lock:
            keys = list(self._by_dep.get(doc_id, set()))
            return self._invalidate_keys(
                keys, InvalidationStrategy.DEPENDENCY, reason, now
            )

    def invalidate_all(
        self,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        with self._lock:
            keys = list(self._entries.keys())
            return self._invalidate_keys(
                keys, InvalidationStrategy.MANUAL, reason, now
            )

    def cleanup_expired(self, now: float = 0.0) -> int:
        with self._lock:
            keys = [
                k
                for k, e in self._entries.items()
                if e.expires_at is not None and now >= e.expires_at
            ]
            return self._invalidate_keys(
                keys, InvalidationStrategy.TTL, "expired", now
            )

    # ---------------------------------------------------------- introspection
    def add_dependency(self, key: str, doc_id: str) -> bool:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return False
            if doc_id in entry.dependencies:
                return False
            entry.dependencies.add(doc_id)
            self._by_dep.setdefault(doc_id, set()).add(key)
            return True

    def add_tag(self, key: str, tag: str) -> bool:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return False
            if tag in entry.tags:
                return False
            entry.tags.add(tag)
            self._by_tag.setdefault(tag, set()).add(key)
            return True

    def tags_for(self, key: str) -> set[str]:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return set()
            return set(entry.tags)

    def dependencies_of(self, key: str) -> set[str]:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return set()
            return set(entry.dependencies)

    def keys_with_tag(self, tag: str) -> list[str]:
        with self._lock:
            return sorted(self._by_tag.get(tag, set()))

    def keys_for_doc(self, doc_id: str) -> list[str]:
        with self._lock:
            return sorted(self._by_doc.get(doc_id, set()))

    def recent_invalidations(self, limit: int = 10) -> list[InvalidationEvent]:
        if limit <= 0:
            return []
        with self._lock:
            return list(self._events[-limit:])

    def stats(self) -> CacheStats:
        with self._lock:
            total_invalidated = sum(
                len(e.keys_invalidated) for e in self._events
            )
            return CacheStats(
                total_entries=len(self._entries),
                total_invalidations=total_invalidated,
                hit_count=self._hit_count,
                miss_count=self._miss_count,
            )

    @property
    def total_entries(self) -> int:
        with self._lock:
            return len(self._entries)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._events.clear()
            self._by_doc.clear()
            self._by_tag.clear()
            self._by_dep.clear()
            self._hit_count = 0
            self._miss_count = 0
            self._next_event_id = 1
