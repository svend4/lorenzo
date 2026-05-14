"""E312 DocReviewQueue — document review workflow queue.

Thread-safe, stdlib-only, dataclass-based review queue for document workflows.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ReviewItem:
    """A single document review request."""

    item_id: str
    doc_id: str
    requester: str
    submitted_at: float = 0.0
    priority: int = 0  # higher = more urgent
    status: str = "pending"  # "pending", "in_review", "approved", "rejected", "withdrawn"
    assigned_to: Optional[str] = None
    note: str = ""


@dataclass
class ReviewDecision:
    """The outcome of a review."""

    item_id: str
    doc_id: str
    reviewer: str
    decision: str  # "approved" or "rejected"
    decided_at: float = 0.0
    comment: str = ""


@dataclass
class QueueStats:
    """Aggregate queue statistics."""

    pending: int
    in_review: int
    approved: int
    rejected: int
    withdrawn: int
    total: int


class DocReviewQueue:
    """In-memory, thread-safe document review workflow queue."""

    def __init__(self) -> None:
        self._items: dict[str, ReviewItem] = {}
        self._decisions: dict[str, ReviewDecision] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- submit
    def submit(
        self,
        doc_id: str,
        requester: str,
        priority: int = 0,
        note: str = "",
        now: Optional[float] = None,
    ) -> ReviewItem:
        """Create a new review request and add it to the queue."""
        if now is None:
            now = time.time()
        item = ReviewItem(
            item_id=uuid.uuid4().hex,
            doc_id=doc_id,
            requester=requester,
            submitted_at=now,
            priority=priority,
            status="pending",
            note=note,
        )
        with self._lock:
            self._items[item.item_id] = item
            self._by_doc.setdefault(doc_id, []).append(item.item_id)
        return item

    # ---------------------------------------------------------------- assign
    def assign(self, item_id: str, reviewer: str) -> bool:
        """Assign a pending item to a reviewer, marking it in_review.

        Returns False if item not found or not in 'pending' status.
        """
        with self._lock:
            item = self._items.get(item_id)
            if item is None or item.status != "pending":
                return False
            item.assigned_to = reviewer
            item.status = "in_review"
            return True

    # ---------------------------------------------------------------- approve
    def approve(
        self,
        item_id: str,
        reviewer: str,
        comment: str = "",
        now: Optional[float] = None,
    ) -> Optional[ReviewDecision]:
        """Approve a review item.

        Sets status to 'approved' and creates a ReviewDecision.
        Returns None if item not found.
        """
        if now is None:
            now = time.time()
        with self._lock:
            item = self._items.get(item_id)
            if item is None:
                return None
            item.status = "approved"
            decision = ReviewDecision(
                item_id=item_id,
                doc_id=item.doc_id,
                reviewer=reviewer,
                decision="approved",
                decided_at=now,
                comment=comment,
            )
            self._decisions[item_id] = decision
            return decision

    # ---------------------------------------------------------------- reject
    def reject(
        self,
        item_id: str,
        reviewer: str,
        comment: str = "",
        now: Optional[float] = None,
    ) -> Optional[ReviewDecision]:
        """Reject a review item.

        Sets status to 'rejected' and creates a ReviewDecision.
        Returns None if item not found.
        """
        if now is None:
            now = time.time()
        with self._lock:
            item = self._items.get(item_id)
            if item is None:
                return None
            item.status = "rejected"
            decision = ReviewDecision(
                item_id=item_id,
                doc_id=item.doc_id,
                reviewer=reviewer,
                decision="rejected",
                decided_at=now,
                comment=comment,
            )
            self._decisions[item_id] = decision
            return decision

    # ---------------------------------------------------------------- withdraw
    def withdraw(self, item_id: str) -> bool:
        """Withdraw a pending or in_review item.

        Returns True if item was found and status was 'pending' or 'in_review'.
        """
        with self._lock:
            item = self._items.get(item_id)
            if item is None:
                return False
            if item.status not in ("pending", "in_review"):
                return False
            item.status = "withdrawn"
            return True

    # ---------------------------------------------------------------- lookups
    def get_item(self, item_id: str) -> Optional[ReviewItem]:
        """Return the ReviewItem with the given id, or None."""
        with self._lock:
            return self._items.get(item_id)

    def get_decision(self, item_id: str) -> Optional[ReviewDecision]:
        """Return the ReviewDecision for the given item_id, or None."""
        with self._lock:
            return self._decisions.get(item_id)

    # ---------------------------------------------------------------- queries
    def pending_items(self) -> list[ReviewItem]:
        """Return all pending items sorted by (-priority, submitted_at)."""
        with self._lock:
            items = [i for i in self._items.values() if i.status == "pending"]
        items.sort(key=lambda i: (-i.priority, i.submitted_at))
        return items

    def items_for_doc(self, doc_id: str) -> list[ReviewItem]:
        """Return all items for a given doc_id, sorted by submitted_at."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            items = [self._items[iid] for iid in ids if iid in self._items]
        items.sort(key=lambda i: i.submitted_at)
        return items

    def items_by_status(self, status: str) -> list[ReviewItem]:
        """Return all items with the given status, sorted by submitted_at."""
        with self._lock:
            items = [i for i in self._items.values() if i.status == status]
        items.sort(key=lambda i: i.submitted_at)
        return items

    # ---------------------------------------------------------------- stats
    def stats(self) -> QueueStats:
        """Return aggregate counts by status."""
        with self._lock:
            pending = 0
            in_review = 0
            approved = 0
            rejected = 0
            withdrawn = 0
            for item in self._items.values():
                if item.status == "pending":
                    pending += 1
                elif item.status == "in_review":
                    in_review += 1
                elif item.status == "approved":
                    approved += 1
                elif item.status == "rejected":
                    rejected += 1
                elif item.status == "withdrawn":
                    withdrawn += 1
            total = len(self._items)
        return QueueStats(
            pending=pending,
            in_review=in_review,
            approved=approved,
            rejected=rejected,
            withdrawn=withdrawn,
            total=total,
        )
