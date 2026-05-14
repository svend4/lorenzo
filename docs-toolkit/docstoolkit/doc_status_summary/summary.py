"""Aggregate status summary across documents.

Maintains a per-doc :class:`StatusSnapshot` (the latest known status for
each tracked document) and produces aggregate :class:`SummaryReport`
counts on demand.  Pure stdlib, thread-safe via a single ``threading.Lock``.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StatusSnapshot:
    """A document's status at a point in time."""

    doc_id: str
    status: str
    updated_at: float = 0.0


@dataclass
class SummaryReport:
    """Aggregate summary report computed across all tracked snapshots."""

    status_counts: dict = field(default_factory=dict)
    total: int = 0
    generated_at: float = 0.0


@dataclass
class SummaryStats:
    """Aggregate statistics about the summary state."""

    total_docs: int
    unique_statuses: int
    reports_generated: int


class DocStatusSummary:
    """Maintain per-doc status snapshots and produce aggregate reports.

    Storage is in-memory; all mutating and reading operations are
    serialised through an internal ``threading.Lock``.
    """

    def __init__(self) -> None:
        # doc_id -> StatusSnapshot
        self._snapshots: dict = {}
        self._reports_generated: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Core mutations
    # ------------------------------------------------------------------

    def update_status(
        self,
        doc_id: str,
        status: str,
        now: Optional[float] = None,
    ) -> StatusSnapshot:
        """Set or replace the status snapshot for *doc_id*.

        Parameters
        ----------
        doc_id:
            Unique identifier of the document.
        status:
            New status string.
        now:
            Timestamp to record; defaults to ``time.time()`` when ``None``.

        Returns
        -------
        StatusSnapshot
            The freshly stored snapshot.
        """
        ts = now if now is not None else time.time()
        snap = StatusSnapshot(doc_id=doc_id, status=status, updated_at=ts)
        with self._lock:
            self._snapshots[doc_id] = snap
        return snap

    def clear_doc(self, doc_id: str) -> bool:
        """Remove the snapshot for *doc_id*.

        Returns
        -------
        bool
            ``True`` if a snapshot existed and was removed; ``False`` otherwise.
        """
        with self._lock:
            if doc_id not in self._snapshots:
                return False
            del self._snapshots[doc_id]
            return True

    def clear_all(self) -> int:
        """Remove every snapshot.

        Returns
        -------
        int
            Number of snapshots that were removed.
        """
        with self._lock:
            count = len(self._snapshots)
            self._snapshots.clear()
            return count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_snapshot(self, doc_id: str) -> Optional[StatusSnapshot]:
        """Return the snapshot for *doc_id*, or ``None`` if unknown."""
        with self._lock:
            return self._snapshots.get(doc_id)

    def docs_with_status(self, status: str) -> list:
        """Return a sorted list of doc_ids currently in *status*."""
        with self._lock:
            return sorted(
                doc_id
                for doc_id, snap in self._snapshots.items()
                if snap.status == status
            )

    def summarize(self, now: Optional[float] = None) -> SummaryReport:
        """Produce a :class:`SummaryReport` from current snapshots.

        Increments the internal counter of reports generated.

        Parameters
        ----------
        now:
            Timestamp to record as ``generated_at``; defaults to ``time.time()``.
        """
        ts = now if now is not None else time.time()
        with self._lock:
            status_counts: dict = {}
            for snap in self._snapshots.values():
                status_counts[snap.status] = status_counts.get(snap.status, 0) + 1
            total = len(self._snapshots)
            self._reports_generated += 1
        return SummaryReport(
            status_counts=status_counts,
            total=total,
            generated_at=ts,
        )

    def top_statuses(self, limit: int = 10) -> list:
        """Return ``(status, count)`` pairs sorted by count desc, status asc.

        Parameters
        ----------
        limit:
            Maximum number of entries to return.  Non-positive values yield
            an empty list.
        """
        if limit <= 0:
            return []
        with self._lock:
            counts: dict = {}
            for snap in self._snapshots.values():
                counts[snap.status] = counts.get(snap.status, 0) + 1
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return ordered[:limit]

    def status_changed_since(self, timestamp: float) -> list:
        """Return snapshots updated strictly after *timestamp*.

        Results are sorted by ``updated_at`` ascending.
        """
        with self._lock:
            picked = [
                snap
                for snap in self._snapshots.values()
                if snap.updated_at > timestamp
            ]
        picked.sort(key=lambda s: s.updated_at)
        return picked

    def all_doc_ids(self) -> list:
        """Return a sorted list of every tracked doc_id."""
        with self._lock:
            return sorted(self._snapshots.keys())

    def all_statuses(self) -> list:
        """Return a sorted list of the unique status values currently in use."""
        with self._lock:
            return sorted({snap.status for snap in self._snapshots.values()})

    def stats(self) -> SummaryStats:
        """Return aggregate statistics about the summary state."""
        with self._lock:
            statuses = {snap.status for snap in self._snapshots.values()}
            return SummaryStats(
                total_docs=len(self._snapshots),
                unique_statuses=len(statuses),
                reports_generated=self._reports_generated,
            )
