"""DocDiffRecorder — record per-edit diffs with metadata.

Pure stdlib, thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# DiffRecord
# ---------------------------------------------------------------------------

@dataclass
class DiffRecord:
    """A single recorded diff."""
    record_id: int = 0
    doc_id: str = ""
    author: str = ""
    recorded_at: float = 0.0
    added_lines: int = 0
    removed_lines: int = 0
    summary: str = ""


# ---------------------------------------------------------------------------
# DiffRecorderStats
# ---------------------------------------------------------------------------

@dataclass
class DiffRecorderStats:
    """Aggregate statistics across all recorded diffs."""
    total_records: int = 0
    unique_docs: int = 0
    unique_authors: int = 0
    total_added: int = 0
    total_removed: int = 0


# ---------------------------------------------------------------------------
# DocDiffRecorder
# ---------------------------------------------------------------------------

class DocDiffRecorder:
    """Record per-edit diffs with metadata and provide query/index methods."""

    def __init__(self) -> None:
        self._records: list[DiffRecord] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_author: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_diff(
        self,
        doc_id: str,
        added_lines: int,
        removed_lines: int,
        author: str = "",
        summary: str = "",
        now: Optional[float] = None,
    ) -> DiffRecord:
        """Record a new diff and return its :class:`DiffRecord`."""
        if now is None:
            now = time.time()
        added = max(0, int(added_lines))
        removed = max(0, int(removed_lines))
        with self._lock:
            record = DiffRecord(
                record_id=self._next_id,
                doc_id=doc_id,
                author=author,
                recorded_at=float(now),
                added_lines=added,
                removed_lines=removed,
                summary=summary,
            )
            self._next_id += 1
            self._records.append(record)
            self._by_doc.setdefault(doc_id, []).append(record.record_id)
            self._by_author.setdefault(author, []).append(record.record_id)
            return record

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------

    def _record_by_id(self, record_id: int) -> Optional[DiffRecord]:
        # No lock required for read of immutable record by index; but use lock
        # to ensure consistent snapshot.
        if 1 <= record_id < self._next_id:
            idx = record_id - 1
            if 0 <= idx < len(self._records):
                rec = self._records[idx]
                if rec.record_id == record_id:
                    return rec
            # fallback linear search if records have been cleared
            for r in self._records:
                if r.record_id == record_id:
                    return r
        return None

    def get_record(self, record_id: int) -> Optional[DiffRecord]:
        """Return the record with the given id, or ``None``."""
        with self._lock:
            return self._record_by_id(record_id)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def records_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[DiffRecord]:
        """Records for a document, most recent first."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        records = [self._record_by_id(rid) for rid in ids]
        records = [r for r in records if r is not None]
        records.sort(key=lambda r: r.record_id, reverse=True)
        if limit is not None:
            records = records[:limit]
        return records

    def records_by_author(
        self, author: str, limit: Optional[int] = None
    ) -> list[DiffRecord]:
        """Records authored by ``author``, most recent first."""
        with self._lock:
            ids = list(self._by_author.get(author, []))
        records = [self._record_by_id(rid) for rid in ids]
        records = [r for r in records if r is not None]
        records.sort(key=lambda r: r.record_id, reverse=True)
        if limit is not None:
            records = records[:limit]
        return records

    def records_in_range(
        self, start_time: float, end_time: float
    ) -> list[DiffRecord]:
        """Records with ``start_time <= recorded_at <= end_time`` sorted asc."""
        with self._lock:
            snap = list(self._records)
        out = [
            r for r in snap
            if start_time <= r.recorded_at <= end_time
        ]
        out.sort(key=lambda r: r.recorded_at)
        return out

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    def total_lines_changed(self, doc_id: str) -> int:
        """Return total ``added + removed`` lines for ``doc_id``."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        total = 0
        for rid in ids:
            r = self._record_by_id(rid)
            if r is not None:
                total += r.added_lines + r.removed_lines
        return total

    def top_authors(self, limit: int = 10) -> list[tuple]:
        """Top authors by total lines changed.

        Returns ``(author, total_lines)`` tuples sorted desc by total, then by
        author asc. Empty author strings are excluded.
        """
        totals: dict[str, int] = {}
        with self._lock:
            snap = list(self._records)
        for r in snap:
            if not r.author:
                continue
            totals[r.author] = totals.get(r.author, 0) + r.added_lines + r.removed_lines
        items = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
        return items[:limit]

    def top_docs(self, limit: int = 10) -> list[tuple]:
        """Top docs by total lines changed, sorted desc by total then doc_id asc."""
        totals: dict[str, int] = {}
        with self._lock:
            snap = list(self._records)
        for r in snap:
            totals[r.doc_id] = totals.get(r.doc_id, 0) + r.added_lines + r.removed_lines
        items = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
        return items[:limit]

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def clear_doc(self, doc_id: str) -> int:
        """Remove all records for ``doc_id`` from indexes; return count removed."""
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            if not ids:
                return 0
            id_set = set(ids)
            # Remove from author indexes
            for author, author_ids in list(self._by_author.items()):
                new_list = [i for i in author_ids if i not in id_set]
                if new_list:
                    self._by_author[author] = new_list
                else:
                    del self._by_author[author]
            # Remove from records list
            self._records = [r for r in self._records if r.record_id not in id_set]
            return len(ids)

    def clear_all(self) -> int:
        """Clear everything; return number of records cleared."""
        with self._lock:
            count = len(self._records)
            self._records.clear()
            self._by_doc.clear()
            self._by_author.clear()
            return count

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> DiffRecorderStats:
        """Return aggregate :class:`DiffRecorderStats`."""
        with self._lock:
            snap = list(self._records)
        total_added = sum(r.added_lines for r in snap)
        total_removed = sum(r.removed_lines for r in snap)
        unique_docs = len({r.doc_id for r in snap})
        unique_authors = len({r.author for r in snap if r.author})
        return DiffRecorderStats(
            total_records=len(snap),
            unique_docs=unique_docs,
            unique_authors=unique_authors,
            total_added=total_added,
            total_removed=total_removed,
        )
