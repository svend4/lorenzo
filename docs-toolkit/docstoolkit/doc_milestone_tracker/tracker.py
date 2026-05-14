"""E367 DocMilestoneTracker — milestone tracking for document deliverables."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


_TERMINAL = {"completed", "missed", "cancelled"}
_ACTIVE = {"pending", "in_progress"}


@dataclass
class Milestone:
    """A single milestone tied to a document deliverable."""

    milestone_id: str
    doc_id: str
    name: str
    target_date: float
    status: str = "pending"
    description: str = ""
    completed_at: Optional[float] = None
    progress: float = 0.0


@dataclass
class MilestoneStats:
    """Aggregate statistics over a tracker's milestones."""

    total: int
    pending: int
    in_progress: int
    completed: int
    missed: int
    cancelled: int
    avg_progress: float


class DocMilestoneTracker:
    """Track milestones for documents.

    Thread-safe: all public mutating operations acquire an internal
    :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._milestones: dict[str, Milestone] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Creation                                                            #
    # ------------------------------------------------------------------ #
    def create_milestone(
        self,
        doc_id: str,
        name: str,
        target_date: float,
        description: str = "",
    ) -> Milestone:
        """Create a new milestone (status="pending")."""
        with self._lock:
            milestone_id = str(uuid.uuid4())
            m = Milestone(
                milestone_id=milestone_id,
                doc_id=doc_id,
                name=name,
                target_date=target_date,
                status="pending",
                description=description,
                completed_at=None,
                progress=0.0,
            )
            self._milestones[milestone_id] = m
            self._by_doc.setdefault(doc_id, []).append(milestone_id)
            return m

    # ------------------------------------------------------------------ #
    # State transitions                                                   #
    # ------------------------------------------------------------------ #
    def start(self, milestone_id: str) -> bool:
        """Transition pending → in_progress."""
        with self._lock:
            m = self._milestones.get(milestone_id)
            if m is None or m.status != "pending":
                return False
            m.status = "in_progress"
            return True

    def complete(
        self, milestone_id: str, now: Optional[float] = None
    ) -> bool:
        """Mark milestone as completed."""
        with self._lock:
            m = self._milestones.get(milestone_id)
            if m is None or m.status not in _ACTIVE:
                return False
            m.status = "completed"
            m.progress = 1.0
            m.completed_at = now if now is not None else time.time()
            return True

    def cancel(self, milestone_id: str) -> bool:
        """Cancel a pending or in_progress milestone."""
        with self._lock:
            m = self._milestones.get(milestone_id)
            if m is None or m.status not in _ACTIVE:
                return False
            m.status = "cancelled"
            return True

    def update_progress(self, milestone_id: str, progress: float) -> bool:
        """Set progress; clamp to [0,1]. Reject if in terminal state."""
        with self._lock:
            m = self._milestones.get(milestone_id)
            if m is None or m.status in _TERMINAL:
                return False
            if progress < 0.0:
                progress = 0.0
            elif progress > 1.0:
                progress = 1.0
            m.progress = progress
            return True

    def mark_missed(
        self,
        milestone_ids: Optional[list[str]] = None,
        now: Optional[float] = None,
    ) -> int:
        """Mark overdue active milestones as missed.

        If ``milestone_ids`` is None, scan all active milestones with
        ``target_date < now``. Otherwise only consider the supplied IDs.
        """
        if now is None:
            now = time.time()
        count = 0
        with self._lock:
            if milestone_ids is None:
                candidates = list(self._milestones.values())
            else:
                candidates = [
                    self._milestones[mid]
                    for mid in milestone_ids
                    if mid in self._milestones
                ]
            for m in candidates:
                if m.status in _ACTIVE and m.target_date < now:
                    m.status = "missed"
                    count += 1
        return count

    # ------------------------------------------------------------------ #
    # Read-only queries                                                   #
    # ------------------------------------------------------------------ #
    def get(self, milestone_id: str) -> Optional[Milestone]:
        """Return the milestone or None if not found."""
        with self._lock:
            return self._milestones.get(milestone_id)

    def milestones_for_doc(
        self, doc_id: str, status: Optional[str] = None
    ) -> list[Milestone]:
        """Return milestones for a document, sorted by target_date."""
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            ms = [self._milestones[i] for i in ids if i in self._milestones]
            if status is not None:
                ms = [m for m in ms if m.status == status]
            return sorted(ms, key=lambda m: m.target_date)

    def upcoming(
        self, within_seconds: float, now: Optional[float] = None
    ) -> list[Milestone]:
        """Active milestones with target_date in [now, now+within_seconds]."""
        if now is None:
            now = time.time()
        end = now + within_seconds
        with self._lock:
            ms = [
                m
                for m in self._milestones.values()
                if m.status in _ACTIVE and now <= m.target_date <= end
            ]
            return sorted(ms, key=lambda m: m.target_date)

    def overdue(self, now: Optional[float] = None) -> list[Milestone]:
        """Active milestones whose target_date is in the past."""
        if now is None:
            now = time.time()
        with self._lock:
            ms = [
                m
                for m in self._milestones.values()
                if m.status in _ACTIVE and m.target_date < now
            ]
            return sorted(ms, key=lambda m: m.target_date)

    def delete(self, milestone_id: str) -> bool:
        """Remove a milestone by id."""
        with self._lock:
            m = self._milestones.pop(milestone_id, None)
            if m is None:
                return False
            ids = self._by_doc.get(m.doc_id)
            if ids is not None:
                try:
                    ids.remove(milestone_id)
                except ValueError:
                    pass
                if not ids:
                    self._by_doc.pop(m.doc_id, None)
            return True

    def stats(self) -> MilestoneStats:
        """Compute aggregate statistics."""
        with self._lock:
            total = len(self._milestones)
            counts = {
                "pending": 0,
                "in_progress": 0,
                "completed": 0,
                "missed": 0,
                "cancelled": 0,
            }
            total_progress = 0.0
            for m in self._milestones.values():
                if m.status in counts:
                    counts[m.status] += 1
                total_progress += m.progress
            avg = (total_progress / total) if total > 0 else 0.0
            return MilestoneStats(
                total=total,
                pending=counts["pending"],
                in_progress=counts["in_progress"],
                completed=counts["completed"],
                missed=counts["missed"],
                cancelled=counts["cancelled"],
                avg_progress=avg,
            )
