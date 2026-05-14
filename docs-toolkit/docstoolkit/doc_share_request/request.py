"""E406 DocShareRequest implementation.

Pure stdlib, thread-safe via ``threading.Lock``, dataclasses throughout.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ShareRequest:
    """A single share request for a document."""

    request_id: str
    doc_id: str
    requester: str
    target: str
    permissions: list[str] = field(default_factory=list)
    reason: str = ""
    created_at: float = 0.0
    status: str = "pending"
    decided_by: str = ""
    decided_at: Optional[float] = None
    decision_note: str = ""


@dataclass
class ShareRequestStats:
    """Aggregate statistics across the store."""

    total: int
    pending: int
    approved: int
    rejected: int
    cancelled: int
    expired: int


class DocShareRequest:
    """Main interface for managing share requests."""

    def __init__(self) -> None:
        self._requests: dict[str, ShareRequest] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ creation

    def request_share(
        self,
        doc_id: str,
        requester: str,
        target: str,
        permissions: list[str],
        reason: str = "",
        now: Optional[float] = None,
    ) -> ShareRequest:
        """Create a new share request in ``pending`` state."""
        ts = time.time() if now is None else now
        request_id = uuid.uuid4().hex
        request = ShareRequest(
            request_id=request_id,
            doc_id=doc_id,
            requester=requester,
            target=target,
            permissions=list(permissions),
            reason=reason,
            created_at=ts,
            status="pending",
        )
        with self._lock:
            self._requests[request_id] = request
        return request

    # ------------------------------------------------------------------ decisions

    def approve(
        self,
        request_id: str,
        decided_by: str,
        note: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Approve a pending request. Returns False if not pending or missing."""
        ts = time.time() if now is None else now
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                return False
            if request.status != "pending":
                return False
            request.status = "approved"
            request.decided_by = decided_by
            request.decided_at = ts
            request.decision_note = note
            return True

    def reject(
        self,
        request_id: str,
        decided_by: str,
        note: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Reject a pending request. Returns False if not pending or missing."""
        ts = time.time() if now is None else now
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                return False
            if request.status != "pending":
                return False
            request.status = "rejected"
            request.decided_by = decided_by
            request.decided_at = ts
            request.decision_note = note
            return True

    def cancel(self, request_id: str) -> bool:
        """Cancel a pending request. Returns False if not pending or missing."""
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                return False
            if request.status != "pending":
                return False
            request.status = "cancelled"
            return True

    def expire_old(
        self, max_age_seconds: float, now: Optional[float] = None
    ) -> int:
        """Set ``pending`` requests older than ``max_age_seconds`` to ``expired``.

        Returns the number of requests that were expired.
        """
        ts = time.time() if now is None else now
        count = 0
        with self._lock:
            for request in self._requests.values():
                if request.status != "pending":
                    continue
                if (ts - request.created_at) > max_age_seconds:
                    request.status = "expired"
                    count += 1
        return count

    def delete(self, request_id: str) -> bool:
        """Fully remove a request. Returns False if not found."""
        with self._lock:
            if request_id not in self._requests:
                return False
            del self._requests[request_id]
            return True

    # ------------------------------------------------------------------ queries

    def get(self, request_id: str) -> Optional[ShareRequest]:
        """Return the request by id, or ``None``."""
        with self._lock:
            return self._requests.get(request_id)

    def requests_for_doc(
        self, doc_id: str, status: Optional[str] = None
    ) -> list[ShareRequest]:
        """Return all requests for a given document, sorted by ``created_at``."""
        with self._lock:
            matched = [
                r for r in self._requests.values() if r.doc_id == doc_id
            ]
        if status is not None:
            matched = [r for r in matched if r.status == status]
        return sorted(matched, key=lambda r: r.created_at)

    def requests_by_requester(
        self, requester: str, status: Optional[str] = None
    ) -> list[ShareRequest]:
        """Return all requests by a given requester, sorted by ``created_at``."""
        with self._lock:
            matched = [
                r for r in self._requests.values() if r.requester == requester
            ]
        if status is not None:
            matched = [r for r in matched if r.status == status]
        return sorted(matched, key=lambda r: r.created_at)

    def requests_for_target(
        self, target: str, status: Optional[str] = None
    ) -> list[ShareRequest]:
        """Return all requests for a given target, sorted by ``created_at``."""
        with self._lock:
            matched = [
                r for r in self._requests.values() if r.target == target
            ]
        if status is not None:
            matched = [r for r in matched if r.status == status]
        return sorted(matched, key=lambda r: r.created_at)

    def pending_requests(self) -> list[ShareRequest]:
        """Return all pending requests, sorted by ``created_at``."""
        with self._lock:
            matched = [
                r for r in self._requests.values() if r.status == "pending"
            ]
        return sorted(matched, key=lambda r: r.created_at)

    def stats(self) -> ShareRequestStats:
        """Return aggregate statistics across all requests."""
        with self._lock:
            total = len(self._requests)
            pending = sum(
                1 for r in self._requests.values() if r.status == "pending"
            )
            approved = sum(
                1 for r in self._requests.values() if r.status == "approved"
            )
            rejected = sum(
                1 for r in self._requests.values() if r.status == "rejected"
            )
            cancelled = sum(
                1 for r in self._requests.values() if r.status == "cancelled"
            )
            expired = sum(
                1 for r in self._requests.values() if r.status == "expired"
            )
        return ShareRequestStats(
            total=total,
            pending=pending,
            approved=approved,
            rejected=rejected,
            cancelled=cancelled,
            expired=expired,
        )
