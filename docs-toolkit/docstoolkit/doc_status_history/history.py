"""E399 DocStatusHistory — track status changes over time for documents.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.

Internally each :class:`DocStatusHistory` instance stores:

* ``_changes`` — a flat ordered list of every :class:`StatusChange` ever recorded,
* ``_by_doc`` — index ``doc_id -> [change_id, ...]`` for quick per-doc lookups,
* ``_current_status`` — the latest status per ``doc_id``,
* ``_next_id`` — monotonically increasing identifier counter starting at ``1``.

All public methods acquire ``self._lock`` so the class is safe to use from
multiple threads.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class StatusChange:
    """A single status change record."""

    change_id: int
    doc_id: str
    old_status: Optional[str]
    new_status: str
    changed_at: float = 0.0
    changed_by: str = ""
    note: str = ""


@dataclass
class StatusStats:
    """Aggregate statistics for a :class:`DocStatusHistory` instance."""

    total_changes: int
    unique_docs: int
    current_status_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocStatusHistory
# ---------------------------------------------------------------------------


class DocStatusHistory:
    """Main interface for recording and querying document status history."""

    def __init__(self) -> None:
        self._changes: List[StatusChange] = []
        self._by_doc: Dict[str, List[int]] = {}
        self._current_status: Dict[str, str] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_change(
        self,
        doc_id: str,
        new_status: str,
        changed_by: str = "",
        note: str = "",
        now: Optional[float] = None,
    ) -> StatusChange:
        """Record a status change for ``doc_id``.

        ``old_status`` is auto-detected from the latest recorded status,
        and ``_current_status`` is updated to ``new_status``.
        """

        ts = time.time() if now is None else now
        with self._lock:
            old_status = self._current_status.get(doc_id)
            change = StatusChange(
                change_id=self._next_id,
                doc_id=doc_id,
                old_status=old_status,
                new_status=new_status,
                changed_at=ts,
                changed_by=changed_by,
                note=note,
            )
            self._next_id += 1
            self._changes.append(change)
            self._by_doc.setdefault(doc_id, []).append(change.change_id)
            self._current_status[doc_id] = new_status
            return change

    # ------------------------------------------------------------------
    # Status queries
    # ------------------------------------------------------------------

    def current_status(self, doc_id: str) -> Optional[str]:
        """Return the latest known status for ``doc_id`` (or ``None``)."""

        with self._lock:
            return self._current_status.get(doc_id)

    def history_for(
        self, doc_id: str, limit: Optional[int] = None
    ) -> List[StatusChange]:
        """Return changes for ``doc_id``, most recent first.

        ``limit`` truncates the result to at most that many entries.
        """

        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            id_to_change = {c.change_id: c for c in self._changes}
            result = [id_to_change[i] for i in reversed(ids) if i in id_to_change]
            if limit is not None:
                result = result[:limit]
            return result

    def latest_change_for(self, doc_id: str) -> Optional[StatusChange]:
        """Return the most recent change for ``doc_id`` (or ``None``)."""

        with self._lock:
            ids = self._by_doc.get(doc_id)
            if not ids:
                return None
            target = ids[-1]
            for c in reversed(self._changes):
                if c.change_id == target:
                    return c
            return None

    def time_in_current_status(
        self, doc_id: str, now: Optional[float] = None
    ) -> Optional[float]:
        """Return seconds since the latest change for ``doc_id``.

        Returns ``None`` if the doc has no history.
        """

        ts = time.time() if now is None else now
        with self._lock:
            ids = self._by_doc.get(doc_id)
            if not ids:
                return None
            target = ids[-1]
            for c in reversed(self._changes):
                if c.change_id == target:
                    return ts - c.changed_at
            return None

    # ------------------------------------------------------------------
    # Transitions / lookups
    # ------------------------------------------------------------------

    def transitions(self, from_status: str, to_status: str) -> List[StatusChange]:
        """Return changes matching ``from_status -> to_status`` transition."""

        with self._lock:
            matches = [
                c
                for c in self._changes
                if c.old_status == from_status and c.new_status == to_status
            ]
        matches.sort(key=lambda c: c.changed_at)
        return matches

    def docs_in_status(self, status: str) -> List[str]:
        """Return sorted list of ``doc_id`` whose current status is ``status``."""

        with self._lock:
            return sorted(
                doc_id
                for doc_id, s in self._current_status.items()
                if s == status
            )

    def status_distribution(self) -> dict:
        """Return a copy of the current status -> doc count mapping."""

        with self._lock:
            counts: Dict[str, int] = {}
            for s in self._current_status.values():
                counts[s] = counts.get(s, 0) + 1
            return counts

    def changes_in_range(
        self,
        start_time: float,
        end_time: float,
        doc_id: Optional[str] = None,
    ) -> List[StatusChange]:
        """Return changes with ``start_time <= changed_at <= end_time``.

        Inclusive on both ends. Optional ``doc_id`` filter. Sorted ascending.
        """

        with self._lock:
            result = [
                c
                for c in self._changes
                if start_time <= c.changed_at <= end_time
                and (doc_id is None or c.doc_id == doc_id)
            ]
        result.sort(key=lambda c: c.changed_at)
        return result

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear_doc(self, doc_id: str) -> int:
        """Remove all history for ``doc_id``. Returns number of changes cleared."""

        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            if ids:
                ids_set = set(ids)
                self._changes = [c for c in self._changes if c.change_id not in ids_set]
            self._current_status.pop(doc_id, None)
            return len(ids)

    def all_doc_ids(self) -> List[str]:
        """Return sorted list of all known ``doc_id`` values."""

        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> StatusStats:
        """Return aggregate :class:`StatusStats`."""

        with self._lock:
            counts: Dict[str, int] = {}
            for s in self._current_status.values():
                counts[s] = counts.get(s, 0) + 1
            return StatusStats(
                total_changes=len(self._changes),
                unique_docs=len(self._by_doc),
                current_status_counts=counts,
            )
