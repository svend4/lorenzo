"""DocProgressLog implementation.

Incremental, thread-safe progress log for document operations. Pure stdlib.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProgressEntry:
    """A single progress data point."""

    entry_id: int
    operation_id: str
    doc_id: str
    percent: float
    message: str = ""
    recorded_at: float = 0.0


@dataclass
class ProgressSummary:
    """Summary for a specific operation."""

    operation_id: str
    doc_id: str
    current_percent: float
    entry_count: int
    started_at: float
    last_updated_at: float


@dataclass
class ProgressStats:
    """Aggregate statistics across the log."""

    total_entries: int
    unique_operations: int
    unique_docs: int


def _clamp_percent(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 100.0:
        return 100.0
    return float(value)


class DocProgressLog:
    """Thread-safe incremental progress log for document operations."""

    def __init__(self) -> None:
        self._entries: list[ProgressEntry] = []
        self._by_operation: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def log_progress(
        self,
        operation_id: str,
        doc_id: str,
        percent: float,
        message: str = "",
        now: Optional[float] = None,
    ) -> ProgressEntry:
        """Log a single progress data point. Percent is clamped to [0, 100]."""
        clamped = _clamp_percent(percent)
        ts = now if now is not None else time.time()
        with self._lock:
            entry = ProgressEntry(
                entry_id=self._next_id,
                operation_id=operation_id,
                doc_id=doc_id,
                percent=clamped,
                message=message,
                recorded_at=ts,
            )
            self._next_id += 1
            index = len(self._entries)
            self._entries.append(entry)
            self._by_operation.setdefault(operation_id, []).append(index)
            return entry

    def entries_for(
        self, operation_id: str, limit: Optional[int] = None
    ) -> list[ProgressEntry]:
        """Return entries for an operation, most recent first."""
        with self._lock:
            idxs = self._by_operation.get(operation_id, [])
            entries = [self._entries[i] for i in reversed(idxs)]
            if limit is not None:
                entries = entries[:limit]
            return entries

    def summary(self, operation_id: str) -> Optional[ProgressSummary]:
        """Return a summary for an operation, or None if no entries."""
        with self._lock:
            idxs = self._by_operation.get(operation_id, [])
            if not idxs:
                return None
            first = self._entries[idxs[0]]
            last = self._entries[idxs[-1]]
            return ProgressSummary(
                operation_id=operation_id,
                doc_id=last.doc_id,
                current_percent=last.percent,
                entry_count=len(idxs),
                started_at=first.recorded_at,
                last_updated_at=last.recorded_at,
            )

    def latest_for(self, operation_id: str) -> Optional[ProgressEntry]:
        """Return the most recent entry for an operation, or None."""
        with self._lock:
            idxs = self._by_operation.get(operation_id, [])
            if not idxs:
                return None
            return self._entries[idxs[-1]]

    def operations_for_doc(self, doc_id: str) -> list[str]:
        """Sorted unique operation_ids that touched the given doc."""
        with self._lock:
            seen: set[str] = set()
            for entry in self._entries:
                if entry.doc_id == doc_id:
                    seen.add(entry.operation_id)
            return sorted(seen)

    def entries_for_doc(self, doc_id: str) -> list[ProgressEntry]:
        """Return entries for a given doc, most recent first."""
        with self._lock:
            matched = [e for e in self._entries if e.doc_id == doc_id]
            matched.reverse()
            return matched

    def clear_operation(self, operation_id: str) -> int:
        """Remove an operation's entries from indexes. Returns count removed."""
        with self._lock:
            idxs = self._by_operation.pop(operation_id, None)
            if not idxs:
                return 0
            idx_set = set(idxs)
            # Keep entries for other operations in the global list. We rebuild
            # _entries and remap _by_operation indices so they stay consistent.
            new_entries: list[ProgressEntry] = []
            new_by_op: dict[str, list[int]] = {}
            for entry in self._entries:
                if entry.operation_id == operation_id:
                    continue
                new_index = len(new_entries)
                new_entries.append(entry)
                new_by_op.setdefault(entry.operation_id, []).append(new_index)
            removed = len(idx_set)
            self._entries = new_entries
            self._by_operation = new_by_op
            return removed

    def clear_all(self) -> int:
        """Clear all entries. Returns total count removed."""
        with self._lock:
            removed = len(self._entries)
            self._entries = []
            self._by_operation = {}
            return removed

    def all_operations(self) -> list[str]:
        """Sorted unique operation_ids known to the log."""
        with self._lock:
            return sorted(self._by_operation.keys())

    def stats(self) -> ProgressStats:
        """Aggregate statistics."""
        with self._lock:
            unique_docs = {e.doc_id for e in self._entries}
            return ProgressStats(
                total_entries=len(self._entries),
                unique_operations=len(self._by_operation),
                unique_docs=len(unique_docs),
            )
