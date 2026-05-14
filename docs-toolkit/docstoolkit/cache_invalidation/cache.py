"""Tag-based cache invalidation: in-memory cache with optional TTL and tag sets."""
from __future__ import annotations

import threading
import time as _time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class CacheEntry:
    """A single cache entry carrying a value, tags, creation timestamp, and TTL."""

    key: str
    value: Any
    tags: frozenset[str] = field(default_factory=frozenset)
    created_at: float = 0.0
    ttl: Optional[float] = None  # seconds; None = no expiry


# ---------------------------------------------------------------------------
# TaggedCache
# ---------------------------------------------------------------------------

class TaggedCache:
    """In-memory cache with tag-based invalidation and optional TTL.

    Parameters
    ----------
    now_fn:
        Callable that returns the current time as a float (seconds).
        Defaults to :func:`time.time`.  Inject a deterministic function
        for unit tests.

    Thread safety
    -------------
    All public methods acquire a single :class:`threading.Lock` for the
    duration of their operation, making the cache safe for concurrent use.

    Internal storage
    ----------------
    ``_store``: ``dict[str, CacheEntry]``
        Primary key → entry mapping.
    ``_tag_index``: ``dict[str, set[str]]``
        Tag → set of keys mapping for O(1) invalidation by tag.
    """

    def __init__(self, now_fn: Optional[Callable[[], float]] = None) -> None:
        self._now: Callable[[], float] = now_fn if now_fn is not None else _time.time
        self._store: dict[str, CacheEntry] = {}
        self._tag_index: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers (caller must hold _lock)
    # ------------------------------------------------------------------

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Return True if *entry* has a TTL and it has elapsed."""
        if entry.ttl is None:
            return False
        return self._now() > entry.created_at + entry.ttl

    def _remove_entry(self, key: str) -> None:
        """Remove *key* from _store and clean up _tag_index (caller holds lock)."""
        entry = self._store.pop(key, None)
        if entry is None:
            return
        for tag in entry.tags:
            keys_for_tag = self._tag_index.get(tag)
            if keys_for_tag is not None:
                keys_for_tag.discard(key)
                if not keys_for_tag:
                    del self._tag_index[tag]

    def _add_to_tag_index(self, key: str, tags: frozenset[str]) -> None:
        """Register *key* under each tag in *tags* (caller holds lock)."""
        for tag in tags:
            if tag not in self._tag_index:
                self._tag_index[tag] = set()
            self._tag_index[tag].add(key)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
        tags: Optional[set[str]] = None,
        ttl: Optional[float] = None,
    ) -> None:
        """Store *value* under *key* with optional *tags* and *ttl*.

        If *key* already exists it is fully replaced (old tags are removed
        from the tag index before new ones are registered).
        """
        frozen_tags: frozenset[str] = frozenset(tags) if tags else frozenset()
        entry = CacheEntry(
            key=key,
            value=value,
            tags=frozen_tags,
            created_at=self._now(),
            ttl=ttl,
        )
        with self._lock:
            # Clean up any existing entry for this key first.
            if key in self._store:
                self._remove_entry(key)
            self._store[key] = entry
            self._add_to_tag_index(key, frozen_tags)

    def get(self, key: str, default: Any = None) -> Any:
        """Return value for *key*, or *default* if missing or expired."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            if self._is_expired(entry):
                self._remove_entry(key)
                return default
            return entry.value

    def delete(self, key: str) -> bool:
        """Remove *key*. Returns ``True`` if it existed (even if expired)."""
        with self._lock:
            if key not in self._store:
                return False
            self._remove_entry(key)
            return True

    def invalidate_tag(self, tag: str) -> int:
        """Remove all entries tagged with *tag*. Returns count removed."""
        with self._lock:
            keys = list(self._tag_index.get(tag, set()))
            for key in keys:
                self._remove_entry(key)
            return len(keys)

    def invalidate_tags(self, tags: set[str]) -> int:
        """Remove all entries tagged with ANY of the given *tags*.

        Union semantics: an entry is removed if it carries at least one of
        the specified tags.  Returns total count of entries removed.
        """
        with self._lock:
            # Collect all unique keys across all requested tags.
            keys_to_remove: set[str] = set()
            for tag in tags:
                keys_to_remove.update(self._tag_index.get(tag, set()))
            for key in keys_to_remove:
                self._remove_entry(key)
            return len(keys_to_remove)

    def exists(self, key: str) -> bool:
        """Return ``True`` if *key* is present and not expired."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return False
            if self._is_expired(entry):
                self._remove_entry(key)
                return False
            return True

    def keys(self) -> list[str]:
        """Return all non-expired keys."""
        with self._lock:
            expired = [k for k, e in self._store.items() if self._is_expired(e)]
            for k in expired:
                self._remove_entry(k)
            return list(self._store.keys())

    def size(self) -> int:
        """Number of non-expired entries."""
        with self._lock:
            expired = [k for k, e in self._store.items() if self._is_expired(e)]
            for k in expired:
                self._remove_entry(k)
            return len(self._store)

    def clear(self) -> None:
        """Remove all entries."""
        with self._lock:
            self._store.clear()
            self._tag_index.clear()

    def get_entry(self, key: str) -> Optional[CacheEntry]:
        """Return full :class:`CacheEntry` or ``None`` if missing or expired."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if self._is_expired(entry):
                self._remove_entry(key)
                return None
            return entry

    def keys_for_tag(self, tag: str) -> list[str]:
        """Return non-expired keys that carry *tag*."""
        with self._lock:
            raw_keys = list(self._tag_index.get(tag, set()))
            result: list[str] = []
            for key in raw_keys:
                entry = self._store.get(key)
                if entry is None:
                    continue
                if self._is_expired(entry):
                    self._remove_entry(key)
                    continue
                result.append(key)
            return result

    def purge_expired(self) -> int:
        """Remove all expired entries. Returns count removed."""
        with self._lock:
            expired = [k for k, e in self._store.items() if self._is_expired(e)]
            for k in expired:
                self._remove_entry(k)
            return len(expired)
