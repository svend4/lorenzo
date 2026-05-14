"""Implementation of the E431 DocEventDedup module."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class DedupEntry:
    """A single deduplication record for a document event."""

    event_key: str
    first_seen_at: float
    last_seen_at: float
    hit_count: int = 1
    expires_at: Optional[float] = None


@dataclass
class DedupStats:
    """Aggregate statistics about the dedup store."""

    total_entries: int
    total_seen: int
    unique_events: int
    total_filtered: int


class DocEventDedup:
    """Deduplicate document events with optional TTL.

    The store keeps one :class:`DedupEntry` per ``event_key``. Each call to
    :meth:`record` either creates a new entry (returning ``is_new=True``) or
    updates an existing, non-expired entry (returning ``is_new=False`` and
    incrementing the duplicate counter).

    Thread-safety is provided by an internal :class:`threading.Lock`.
    """

    def __init__(self, default_ttl_seconds: Optional[float] = None) -> None:
        self._entries: dict[str, DedupEntry] = {}
        self._default_ttl: Optional[float] = default_ttl_seconds
        self._total_filtered: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else now

    @staticmethod
    def _is_expired(entry: DedupEntry, now: float) -> bool:
        return entry.expires_at is not None and entry.expires_at <= now

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def is_duplicate(self, event_key: str, now: Optional[float] = None) -> bool:
        """Return True if ``event_key`` exists and has not expired."""
        ts = self._now(now)
        with self._lock:
            entry = self._entries.get(event_key)
            if entry is None:
                return False
            if self._is_expired(entry, ts):
                return False
            return True

    def record(
        self,
        event_key: str,
        ttl_seconds: Optional[float] = None,
        now: Optional[float] = None,
    ) -> tuple:
        """Record an event occurrence.

        Returns a tuple ``(is_new, entry)``. If the key is unseen or its
        previous entry has expired, a fresh entry is created (``is_new=True``).
        Otherwise the existing entry's ``last_seen_at`` and ``hit_count`` are
        updated and ``_total_filtered`` is incremented (``is_new=False``).
        """
        ts = self._now(now)
        effective_ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        expires_at = ts + effective_ttl if effective_ttl is not None else None

        with self._lock:
            existing = self._entries.get(event_key)
            if existing is None or self._is_expired(existing, ts):
                entry = DedupEntry(
                    event_key=event_key,
                    first_seen_at=ts,
                    last_seen_at=ts,
                    hit_count=1,
                    expires_at=expires_at,
                )
                self._entries[event_key] = entry
                return True, entry

            existing.last_seen_at = ts
            existing.hit_count += 1
            self._total_filtered += 1
            return False, existing

    def get_entry(self, event_key: str) -> Optional[DedupEntry]:
        """Return the stored entry for ``event_key`` (or ``None``)."""
        with self._lock:
            return self._entries.get(event_key)

    def forget(self, event_key: str) -> bool:
        """Remove a single entry; return True if it existed."""
        with self._lock:
            return self._entries.pop(event_key, None) is not None

    def purge_expired(self, now: Optional[float] = None) -> int:
        """Drop every expired entry; return the number removed."""
        ts = self._now(now)
        with self._lock:
            expired_keys = [
                k for k, e in self._entries.items() if self._is_expired(e, ts)
            ]
            for k in expired_keys:
                del self._entries[k]
            return len(expired_keys)

    def set_default_ttl(self, ttl_seconds: Optional[float]) -> None:
        """Update the default TTL applied to future :meth:`record` calls."""
        with self._lock:
            self._default_ttl = ttl_seconds

    def clear(self) -> int:
        """Remove all entries; return the count cleared."""
        with self._lock:
            count = len(self._entries)
            self._entries.clear()
            return count

    def all_keys(self) -> list[str]:
        """Sorted list of currently-stored, non-expired keys."""
        ts = time.time()
        with self._lock:
            return sorted(
                k for k, e in self._entries.items() if not self._is_expired(e, ts)
            )

    def most_seen(self, limit: int = 10) -> list[DedupEntry]:
        """Top entries by ``hit_count`` (descending)."""
        if limit < 0:
            limit = 0
        with self._lock:
            entries = list(self._entries.values())
        entries.sort(key=lambda e: (-e.hit_count, e.event_key))
        return entries[:limit]

    def stats(self, now: Optional[float] = None) -> DedupStats:
        """Snapshot of aggregate counters."""
        ts = self._now(now)
        with self._lock:
            total_entries = len(self._entries)
            total_seen = sum(e.hit_count for e in self._entries.values())
            unique_events = sum(
                1 for e in self._entries.values() if not self._is_expired(e, ts)
            )
            return DedupStats(
                total_entries=total_entries,
                total_seen=total_seen,
                unique_events=unique_events,
                total_filtered=self._total_filtered,
            )
