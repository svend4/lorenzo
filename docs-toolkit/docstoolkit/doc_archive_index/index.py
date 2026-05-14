"""E432 DocArchiveIndex — searchable index of archived documents.

Provides a thread-safe in-memory index over archive entries with lookups by
doc, tag, time range, user, and substring search over summaries. All
operations use a single ``threading.Lock``. No third-party dependencies.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class ArchiveEntry:
    """A single archive index entry."""

    archive_id: str
    doc_id: str
    archived_at: float = 0.0
    archived_by: str = ""
    tags: List[str] = field(default_factory=list)
    size_bytes: int = 0
    summary: str = ""


@dataclass
class ArchiveStats:
    """Aggregate statistics over all entries currently held."""

    total_archives: int
    unique_docs: int
    total_size_bytes: int
    unique_tags: int


# ---------------------------------------------------------------------------
# DocArchiveIndex
# ---------------------------------------------------------------------------


class DocArchiveIndex:
    """Thread-safe in-memory searchable index over archived documents.

    Entries are keyed by a UUID ``archive_id``. Secondary indexes by
    ``doc_id`` and ``tag`` allow efficient lookups.
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        # archive_id → ArchiveEntry
        self._archives: Dict[str, ArchiveEntry] = {}
        # doc_id → list of archive_ids (insertion order)
        self._by_doc: Dict[str, List[str]] = {}
        # tag → set of archive_ids
        self._by_tag: Dict[str, Set[str]] = {}

    # ------------------------------------------------------------------
    # Mutating operations
    # ------------------------------------------------------------------

    def add_entry(
        self,
        doc_id: str,
        archived_by: str = "",
        tags: Optional[List[str]] = None,
        size_bytes: int = 0,
        summary: str = "",
        now: Optional[float] = None,
    ) -> ArchiveEntry:
        """Add a new archive entry to the index.

        Parameters
        ----------
        doc_id:
            Identifier of the archived document.
        archived_by:
            Optional actor/user who triggered the archive.
        tags:
            Optional list of tags; stored lowercased and deduplicated while
            preserving first-seen order.
        size_bytes:
            Size of the archived content in bytes.
        summary:
            Short summary text used by :meth:`search_summary`.
        now:
            Timestamp for ``archived_at``; defaults to ``time.time()``.

        Returns
        -------
        ArchiveEntry
            The newly created entry.
        """
        archive_id = str(uuid.uuid4())
        archived_at = now if now is not None else time.time()

        # Lowercase tags, dedupe preserving order
        normalized_tags: List[str] = []
        seen: Set[str] = set()
        for tag in tags or []:
            t = tag.lower()
            if t not in seen:
                seen.add(t)
                normalized_tags.append(t)

        entry = ArchiveEntry(
            archive_id=archive_id,
            doc_id=doc_id,
            archived_at=archived_at,
            archived_by=archived_by,
            tags=normalized_tags,
            size_bytes=size_bytes,
            summary=summary,
        )
        with self._lock:
            self._archives[archive_id] = entry
            self._by_doc.setdefault(doc_id, []).append(archive_id)
            for t in normalized_tags:
                self._by_tag.setdefault(t, set()).add(archive_id)
        return entry

    def remove_entry(self, archive_id: str) -> bool:
        """Remove the entry with *archive_id*.

        Returns ``True`` if it existed and was removed, else ``False``.
        """
        with self._lock:
            entry = self._archives.pop(archive_id, None)
            if entry is None:
                return False
            ids = self._by_doc.get(entry.doc_id, [])
            try:
                ids.remove(archive_id)
            except ValueError:
                pass
            if not ids:
                self._by_doc.pop(entry.doc_id, None)
            for t in entry.tags:
                bucket = self._by_tag.get(t)
                if bucket is not None:
                    bucket.discard(archive_id)
                    if not bucket:
                        self._by_tag.pop(t, None)
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove all entries for *doc_id*.

        Returns
        -------
        int
            Number of entries removed.
        """
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            for aid in ids:
                entry = self._archives.pop(aid, None)
                if entry is None:
                    continue
                for t in entry.tags:
                    bucket = self._by_tag.get(t)
                    if bucket is not None:
                        bucket.discard(aid)
                        if not bucket:
                            self._by_tag.pop(t, None)
            return len(ids)

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_entry(self, archive_id: str) -> Optional[ArchiveEntry]:
        """Return the entry with *archive_id*, or ``None`` if missing."""
        with self._lock:
            return self._archives.get(archive_id)

    def entries_for_doc(self, doc_id: str) -> List[ArchiveEntry]:
        """Return entries for *doc_id*, sorted by ``archived_at`` descending."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            entries = [
                self._archives[aid] for aid in ids if aid in self._archives
            ]
        entries.sort(key=lambda e: e.archived_at, reverse=True)
        return entries

    def entries_with_tag(self, tag: str) -> List[ArchiveEntry]:
        """Return entries that carry *tag* (case-insensitive), newest first."""
        key = tag.lower()
        with self._lock:
            ids = list(self._by_tag.get(key, set()))
            entries = [
                self._archives[aid] for aid in ids if aid in self._archives
            ]
        entries.sort(key=lambda e: e.archived_at, reverse=True)
        return entries

    def entries_in_range(self, start: float, end: float) -> List[ArchiveEntry]:
        """Return entries with ``start <= archived_at <= end``, ascending."""
        with self._lock:
            entries = [
                e
                for e in self._archives.values()
                if start <= e.archived_at <= end
            ]
        entries.sort(key=lambda e: e.archived_at)
        return entries

    def entries_by_user(
        self,
        archived_by: str,
        limit: Optional[int] = None,
    ) -> List[ArchiveEntry]:
        """Return entries created by *archived_by*, most-recent first.

        Parameters
        ----------
        archived_by:
            Exact-match actor string.
        limit:
            If given, truncate the result to at most *limit* entries.
        """
        with self._lock:
            entries = [
                e
                for e in self._archives.values()
                if e.archived_by == archived_by
            ]
        entries.sort(key=lambda e: e.archived_at, reverse=True)
        if limit is not None:
            entries = entries[:limit]
        return entries

    def search_summary(self, query: str) -> List[ArchiveEntry]:
        """Return entries whose ``summary`` contains *query* (case-insensitive).

        Results are sorted by ``archived_at`` descending. An empty *query*
        matches every entry.
        """
        needle = query.lower()
        with self._lock:
            entries = [
                e
                for e in self._archives.values()
                if needle in e.summary.lower()
            ]
        entries.sort(key=lambda e: e.archived_at, reverse=True)
        return entries

    def total_size_for_doc(self, doc_id: str) -> int:
        """Return the sum of ``size_bytes`` over all entries for *doc_id*."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            return sum(
                self._archives[aid].size_bytes
                for aid in ids
                if aid in self._archives
            )

    def all_doc_ids(self) -> List[str]:
        """Return all doc IDs with at least one entry, sorted."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def all_tags(self) -> List[str]:
        """Return all known tags, sorted."""
        with self._lock:
            return sorted(self._by_tag.keys())

    def stats(self) -> ArchiveStats:
        """Return aggregate statistics over all entries currently held."""
        with self._lock:
            total_archives = len(self._archives)
            unique_docs = len(self._by_doc)
            total_size_bytes = sum(
                e.size_bytes for e in self._archives.values()
            )
            unique_tags = len(self._by_tag)
        return ArchiveStats(
            total_archives=total_archives,
            unique_docs=unique_docs,
            total_size_bytes=total_size_bytes,
            unique_tags=unique_tags,
        )
