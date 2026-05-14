"""E385 DocReviewAssignment — assign reviewers to documents.

Thread-safe, stdlib-only, dataclass-based reviewer assignment tracker.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass
from typing import Optional


_TERMINAL_STATUSES = ("completed", "declined")
_ACTIVE_STATUSES = ("assigned", "in_progress")
_ALL_STATUSES = ("assigned", "in_progress", "completed", "declined")


@dataclass
class ReviewAssignment:
    """A single review assignment."""

    assignment_id: str
    doc_id: str
    reviewer: str
    assigned_by: str
    assigned_at: float = 0.0
    due_date: Optional[float] = None
    status: str = "assigned"  # "assigned", "in_progress", "completed", "declined"
    completed_at: Optional[float] = None
    note: str = ""


@dataclass
class AssignmentStats:
    """Aggregate review assignment statistics."""

    total: int
    assigned: int
    in_progress: int
    completed: int
    declined: int
    overdue: int


class DocReviewAssignment:
    """In-memory, thread-safe document review assignment tracker."""

    def __init__(self) -> None:
        self._assignments: dict[str, ReviewAssignment] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._by_reviewer: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- assign
    def assign(
        self,
        doc_id: str,
        reviewer: str,
        assigned_by: str,
        due_date: Optional[float] = None,
        note: str = "",
        now: Optional[float] = None,
    ) -> ReviewAssignment:
        """Create a new review assignment.

        Returns the created ReviewAssignment.
        """
        if now is None:
            now = time.time()
        assignment = ReviewAssignment(
            assignment_id=uuid.uuid4().hex,
            doc_id=doc_id,
            reviewer=reviewer,
            assigned_by=assigned_by,
            assigned_at=now,
            due_date=due_date,
            status="assigned",
            completed_at=None,
            note=note,
        )
        with self._lock:
            self._assignments[assignment.assignment_id] = assignment
            self._by_doc.setdefault(doc_id, []).append(assignment.assignment_id)
            self._by_reviewer.setdefault(reviewer, []).append(assignment.assignment_id)
        return assignment

    # ---------------------------------------------------------------- start
    def start(self, assignment_id: str) -> bool:
        """Mark an assignment as in_progress. Only valid from 'assigned'.

        Returns True on success, False otherwise.
        """
        with self._lock:
            a = self._assignments.get(assignment_id)
            if a is None or a.status != "assigned":
                return False
            a.status = "in_progress"
            return True

    # ---------------------------------------------------------------- complete
    def complete(
        self,
        assignment_id: str,
        now: Optional[float] = None,
    ) -> bool:
        """Mark an assignment as completed. Valid from 'assigned' or 'in_progress'.

        Returns True on success, False otherwise.
        """
        if now is None:
            now = time.time()
        with self._lock:
            a = self._assignments.get(assignment_id)
            if a is None or a.status not in ("assigned", "in_progress"):
                return False
            a.status = "completed"
            a.completed_at = now
            return True

    # ---------------------------------------------------------------- decline
    def decline(self, assignment_id: str) -> bool:
        """Mark an assignment as declined. Valid from 'assigned' or 'in_progress'.

        Returns True on success, False otherwise.
        """
        with self._lock:
            a = self._assignments.get(assignment_id)
            if a is None or a.status not in ("assigned", "in_progress"):
                return False
            a.status = "declined"
            return True

    # ---------------------------------------------------------------- get
    def get(self, assignment_id: str) -> Optional[ReviewAssignment]:
        """Return the ReviewAssignment with the given id, or None."""
        with self._lock:
            return self._assignments.get(assignment_id)

    # ---------------------------------------------------------------- queries
    def assignments_for_doc(
        self,
        doc_id: str,
        status: Optional[str] = None,
    ) -> list[ReviewAssignment]:
        """Return all assignments for a doc, sorted by assigned_at.

        If status is provided, filter to that status.
        """
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            items = [self._assignments[i] for i in ids if i in self._assignments]
        if status is not None:
            items = [a for a in items if a.status == status]
        items.sort(key=lambda a: a.assigned_at)
        return items

    def assignments_for_reviewer(
        self,
        reviewer: str,
        status: Optional[str] = None,
    ) -> list[ReviewAssignment]:
        """Return all assignments for a reviewer, sorted by assigned_at.

        If status is provided, filter to that status.
        """
        with self._lock:
            ids = list(self._by_reviewer.get(reviewer, []))
            items = [self._assignments[i] for i in ids if i in self._assignments]
        if status is not None:
            items = [a for a in items if a.status == status]
        items.sort(key=lambda a: a.assigned_at)
        return items

    # ---------------------------------------------------------------- overdue
    def overdue(self, now: Optional[float] = None) -> list[ReviewAssignment]:
        """Return non-terminal assignments past their due_date.

        Sorted by due_date ascending.
        """
        if now is None:
            now = time.time()
        with self._lock:
            items = [
                a
                for a in self._assignments.values()
                if a.status in _ACTIVE_STATUSES
                and a.due_date is not None
                and a.due_date < now
            ]
        items.sort(key=lambda a: (a.due_date if a.due_date is not None else 0.0))
        return items

    # ---------------------------------------------------------------- delete
    def delete(self, assignment_id: str) -> bool:
        """Remove an assignment entirely. Returns True if it existed."""
        with self._lock:
            a = self._assignments.pop(assignment_id, None)
            if a is None:
                return False
            doc_ids = self._by_doc.get(a.doc_id)
            if doc_ids is not None:
                try:
                    doc_ids.remove(assignment_id)
                except ValueError:
                    pass
                if not doc_ids:
                    self._by_doc.pop(a.doc_id, None)
            rev_ids = self._by_reviewer.get(a.reviewer)
            if rev_ids is not None:
                try:
                    rev_ids.remove(assignment_id)
                except ValueError:
                    pass
                if not rev_ids:
                    self._by_reviewer.pop(a.reviewer, None)
            return True

    # ---------------------------------------------------------------- stats
    def stats(self, now: Optional[float] = None) -> AssignmentStats:
        """Return aggregate counts. Overdue counts active assignments past due_date."""
        if now is None:
            now = time.time()
        with self._lock:
            assigned = 0
            in_progress = 0
            completed = 0
            declined = 0
            overdue = 0
            for a in self._assignments.values():
                if a.status == "assigned":
                    assigned += 1
                elif a.status == "in_progress":
                    in_progress += 1
                elif a.status == "completed":
                    completed += 1
                elif a.status == "declined":
                    declined += 1
                if (
                    a.status in _ACTIVE_STATUSES
                    and a.due_date is not None
                    and a.due_date < now
                ):
                    overdue += 1
            total = len(self._assignments)
        return AssignmentStats(
            total=total,
            assigned=assigned,
            in_progress=in_progress,
            completed=completed,
            declined=declined,
            overdue=overdue,
        )
