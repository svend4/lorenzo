"""E360 DocDLQStore — dead letter queue for failed document operations.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class DLQEntry:
    """A single failed operation entry in the dead letter queue."""

    entry_id: int = 0
    doc_id: str = ""
    operation: str = ""
    payload: dict = field(default_factory=dict)
    error: str = ""
    failed_at: float = 0.0
    attempts: int = 1
    retried_at: Optional[float] = None
    resolved: bool = False


@dataclass
class DLQStats:
    """Aggregate statistics across all DLQ entries."""

    total_entries: int = 0
    unresolved_count: int = 0
    unique_docs: int = 0
    total_attempts: int = 0


class DocDLQStore:
    """Dead letter queue for failed document operations.

    Thread-safe in-memory store of :class:`DLQEntry` objects keyed by an
    auto-incrementing ``entry_id``. Each entry is also indexed by ``doc_id``
    for quick per-document lookups.
    """

    def __init__(self) -> None:
        self._entries: Dict[int, DLQEntry] = {}
        self._by_doc: Dict[str, List[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ writes

    def record_failure(
        self,
        doc_id: str,
        operation: str,
        error: str = "",
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DLQEntry:
        """Record a new failed operation; returns the created entry."""
        ts = time.time() if now is None else now
        with self._lock:
            entry_id = self._next_id
            self._next_id += 1
            entry = DLQEntry(
                entry_id=entry_id,
                doc_id=doc_id,
                operation=operation,
                payload=dict(payload) if payload else {},
                error=error,
                failed_at=ts,
                attempts=1,
                retried_at=None,
                resolved=False,
            )
            self._entries[entry_id] = entry
            self._by_doc.setdefault(doc_id, []).append(entry_id)
            return entry

    def increment_attempt(
        self,
        entry_id: int,
        error: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Increment attempt counter; return True if found and not resolved."""
        ts = time.time() if now is None else now
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry is None or entry.resolved:
                return False
            entry.attempts += 1
            entry.error = error
            entry.retried_at = ts
            return True

    def resolve(self, entry_id: int) -> bool:
        """Mark an entry as resolved; return True if found."""
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry is None:
                return False
            entry.resolved = True
            return True

    def unresolve(self, entry_id: int) -> bool:
        """Mark an entry as unresolved; return True if found."""
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry is None:
                return False
            entry.resolved = False
            return True

    def delete(self, entry_id: int) -> bool:
        """Fully remove an entry; return True if found."""
        with self._lock:
            entry = self._entries.pop(entry_id, None)
            if entry is None:
                return False
            ids = self._by_doc.get(entry.doc_id)
            if ids is not None:
                try:
                    ids.remove(entry_id)
                except ValueError:
                    pass
                if not ids:
                    self._by_doc.pop(entry.doc_id, None)
            return True

    # ------------------------------------------------------------------- reads

    def get(self, entry_id: int) -> Optional[DLQEntry]:
        """Return entry by id or ``None``."""
        with self._lock:
            return self._entries.get(entry_id)

    def entries_for_doc(
        self, doc_id: str, unresolved_only: bool = False
    ) -> List[DLQEntry]:
        """All entries for a document, sorted by ``failed_at`` descending."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, ()))
            result = [self._entries[i] for i in ids if i in self._entries]
        if unresolved_only:
            result = [e for e in result if not e.resolved]
        result.sort(key=lambda e: e.failed_at, reverse=True)
        return result

    def unresolved_entries(self) -> List[DLQEntry]:
        """All unresolved entries, sorted by ``failed_at`` descending."""
        with self._lock:
            result = [e for e in self._entries.values() if not e.resolved]
        result.sort(key=lambda e: e.failed_at, reverse=True)
        return result

    def oldest_unresolved(self, limit: int = 10) -> List[DLQEntry]:
        """Oldest unresolved entries first; bounded by ``limit``."""
        with self._lock:
            result = [e for e in self._entries.values() if not e.resolved]
        result.sort(key=lambda e: e.failed_at)
        if limit < 0:
            limit = 0
        return result[:limit]

    def most_failing_docs(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Documents with most entries; ``(doc_id, count)`` desc by count."""
        with self._lock:
            counts = {
                doc_id: len([i for i in ids if i in self._entries])
                for doc_id, ids in self._by_doc.items()
            }
        items = [(d, c) for d, c in counts.items() if c > 0]
        items.sort(key=lambda kv: (-kv[1], kv[0]))
        if limit < 0:
            limit = 0
        return items[:limit]

    # ----------------------------------------------------------------- bulk

    def resolve_all_for_doc(self, doc_id: str) -> int:
        """Resolve every entry for ``doc_id``; return count of newly resolved."""
        count = 0
        with self._lock:
            for i in self._by_doc.get(doc_id, ()):
                entry = self._entries.get(i)
                if entry is not None and not entry.resolved:
                    entry.resolved = True
                    count += 1
        return count

    def purge_resolved(self) -> int:
        """Delete all resolved entries; return count removed."""
        with self._lock:
            to_remove = [i for i, e in self._entries.items() if e.resolved]
            for i in to_remove:
                entry = self._entries.pop(i, None)
                if entry is None:
                    continue
                ids = self._by_doc.get(entry.doc_id)
                if ids is not None:
                    try:
                        ids.remove(i)
                    except ValueError:
                        pass
                    if not ids:
                        self._by_doc.pop(entry.doc_id, None)
            return len(to_remove)

    # ---------------------------------------------------------------- stats

    def stats(self) -> DLQStats:
        """Aggregate counters across all entries."""
        with self._lock:
            total = len(self._entries)
            unresolved = sum(1 for e in self._entries.values() if not e.resolved)
            unique_docs = sum(
                1
                for ids in self._by_doc.values()
                if any(i in self._entries for i in ids)
            )
            total_attempts = sum(e.attempts for e in self._entries.values())
        return DLQStats(
            total_entries=total,
            unresolved_count=unresolved,
            unique_docs=unique_docs,
            total_attempts=total_attempts,
        )
