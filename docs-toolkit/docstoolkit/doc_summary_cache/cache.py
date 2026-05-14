"""DocSummaryCache implementation — versioned, thread-safe summary cache."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SummaryEntry:
    """A single cached summary entry."""

    doc_id: str
    version: str
    summary: str
    cached_at: float = 0.0
    hit_count: int = 0
    length: int = 0


@dataclass
class CacheStats:
    """Aggregate statistics about the cache."""

    total_entries: int = 0
    unique_docs: int = 0
    total_hits: int = 0
    total_chars: int = 0


class DocSummaryCache:
    """Versioned cache for document summaries.

    Stores (doc_id, version) -> SummaryEntry mappings. Thread-safe via
    ``threading.Lock``.
    """

    def __init__(self) -> None:
        self._cache: dict[tuple, SummaryEntry] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ store

    def store(
        self,
        doc_id: str,
        version: str,
        summary: str,
        now: Optional[float] = None,
    ) -> SummaryEntry:
        """Create or replace a summary entry. Returns the stored entry."""
        ts = now if now is not None else time.time()
        with self._lock:
            entry = SummaryEntry(
                doc_id=doc_id,
                version=version,
                summary=summary,
                cached_at=ts,
                hit_count=0,
                length=len(summary),
            )
            self._cache[(doc_id, version)] = entry
            self._by_doc.setdefault(doc_id, set()).add(version)
            return entry

    # ------------------------------------------------------------------ get / peek

    def get(self, doc_id: str, version: str) -> Optional[str]:
        """Return cached summary text and increment hit_count, or None."""
        with self._lock:
            entry = self._cache.get((doc_id, version))
            if entry is None:
                return None
            entry.hit_count += 1
            return entry.summary

    def peek(self, doc_id: str, version: str) -> Optional[SummaryEntry]:
        """Return the entry without modifying hit_count."""
        with self._lock:
            return self._cache.get((doc_id, version))

    def exists(self, doc_id: str, version: str) -> bool:
        with self._lock:
            return (doc_id, version) in self._cache

    # ------------------------------------------------------------------ delete

    def delete(self, doc_id: str, version: str) -> bool:
        """Remove a specific (doc_id, version) entry. Returns True if removed."""
        with self._lock:
            key = (doc_id, version)
            if key not in self._cache:
                return False
            del self._cache[key]
            versions = self._by_doc.get(doc_id)
            if versions is not None:
                versions.discard(version)
                if not versions:
                    del self._by_doc[doc_id]
            return True

    def delete_doc(self, doc_id: str) -> int:
        """Remove all versions for a doc_id. Returns count removed."""
        with self._lock:
            versions = self._by_doc.pop(doc_id, set())
            count = 0
            for version in list(versions):
                if (doc_id, version) in self._cache:
                    del self._cache[(doc_id, version)]
                    count += 1
            return count

    # ------------------------------------------------------------------ queries

    def versions_for(self, doc_id: str) -> list[str]:
        """Return sorted list of versions cached for doc_id."""
        with self._lock:
            return sorted(self._by_doc.get(doc_id, set()))

    def latest_version_for(self, doc_id: str) -> Optional[str]:
        """Return version with the highest ``cached_at`` for doc_id."""
        with self._lock:
            versions = self._by_doc.get(doc_id)
            if not versions:
                return None
            best_version: Optional[str] = None
            best_ts = float("-inf")
            for version in versions:
                entry = self._cache.get((doc_id, version))
                if entry is None:
                    continue
                if entry.cached_at > best_ts:
                    best_ts = entry.cached_at
                    best_version = version
            return best_version

    def top_accessed(self, limit: int = 10) -> list[SummaryEntry]:
        """Return entries sorted by hit_count descending, up to ``limit``."""
        with self._lock:
            entries = list(self._cache.values())
        entries.sort(key=lambda e: e.hit_count, reverse=True)
        if limit < 0:
            limit = 0
        return entries[:limit]

    def total_size_for(self, doc_id: str) -> int:
        """Return sum of ``length`` across all versions for doc_id."""
        with self._lock:
            versions = self._by_doc.get(doc_id, set())
            total = 0
            for version in versions:
                entry = self._cache.get((doc_id, version))
                if entry is not None:
                    total += entry.length
            return total

    def clear(self) -> int:
        """Clear all entries. Returns count cleared."""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            self._by_doc.clear()
            return count

    def all_doc_ids(self) -> list[str]:
        """Return sorted list of all doc_ids with at least one cached version."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> CacheStats:
        """Aggregate statistics across the cache."""
        with self._lock:
            total_entries = len(self._cache)
            unique_docs = len(self._by_doc)
            total_hits = sum(e.hit_count for e in self._cache.values())
            total_chars = sum(e.length for e in self._cache.values())
            return CacheStats(
                total_entries=total_entries,
                unique_docs=unique_docs,
                total_hits=total_hits,
                total_chars=total_chars,
            )
