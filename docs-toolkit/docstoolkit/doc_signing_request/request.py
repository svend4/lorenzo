"""E349 DocSigningRequest implementation.

Pure stdlib, thread-safe via ``threading.Lock``, dataclasses throughout.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

_TERMINAL_STATUSES = {"completed", "expired", "cancelled"}


@dataclass
class SigningRequest:
    """A single signature request for a document."""

    request_id: str
    doc_id: str
    requested_by: str
    created_at: float = 0.0
    expires_at: Optional[float] = None
    status: str = "pending"
    message: str = ""


@dataclass
class Signer:
    """A person asked to sign a request."""

    signer_id: str
    request_id: str
    name: str
    email: str = ""
    order: int = 0
    signed_at: Optional[float] = None
    declined: bool = False


@dataclass
class SigningStats:
    """Aggregate statistics across the store."""

    total_requests: int
    pending: int
    in_progress: int
    completed: int
    expired: int
    cancelled: int
    total_signers: int
    total_signed: int


class DocSigningRequest:
    """Main interface for managing signature requests."""

    def __init__(self) -> None:
        self._requests: dict[str, SigningRequest] = {}
        self._signers: dict[str, list[Signer]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ creation

    def create_request(
        self,
        doc_id: str,
        requested_by: str,
        signers: list[tuple] = [],
        expires_at: Optional[float] = None,
        message: str = "",
        now: Optional[float] = None,
    ) -> SigningRequest:
        """Create a new signing request with optional initial signers.

        ``signers`` is a list of ``(name, email)`` tuples. Signer ``order`` is
        assigned based on the position in the list (0-indexed).
        """
        ts = time.time() if now is None else now
        request_id = uuid.uuid4().hex
        request = SigningRequest(
            request_id=request_id,
            doc_id=doc_id,
            requested_by=requested_by,
            created_at=ts,
            expires_at=expires_at,
            status="pending",
            message=message,
        )
        with self._lock:
            self._requests[request_id] = request
            signer_list: list[Signer] = []
            for idx, item in enumerate(signers):
                if isinstance(item, tuple):
                    name = item[0]
                    email = item[1] if len(item) > 1 else ""
                else:
                    name = str(item)
                    email = ""
                signer = Signer(
                    signer_id=uuid.uuid4().hex,
                    request_id=request_id,
                    name=name,
                    email=email,
                    order=idx,
                )
                signer_list.append(signer)
            self._signers[request_id] = signer_list
        return request

    def add_signer(
        self, request_id: str, name: str, email: str = ""
    ) -> Optional[Signer]:
        """Append a signer to an existing request, assigning the next order."""
        with self._lock:
            if request_id not in self._requests:
                return None
            existing = self._signers.setdefault(request_id, [])
            next_order = (max((s.order for s in existing), default=-1) + 1)
            signer = Signer(
                signer_id=uuid.uuid4().hex,
                request_id=request_id,
                name=name,
                email=email,
                order=next_order,
            )
            existing.append(signer)
            return signer

    # ------------------------------------------------------------------ actions

    def _find_signer_locked(self, signer_id: str) -> Optional[Signer]:
        for signers in self._signers.values():
            for s in signers:
                if s.signer_id == signer_id:
                    return s
        return None

    def sign(self, signer_id: str, now: Optional[float] = None) -> bool:
        """Record a signature; mark request completed when all signed."""
        ts = time.time() if now is None else now
        with self._lock:
            signer = self._find_signer_locked(signer_id)
            if signer is None:
                return False
            if signer.signed_at is not None:
                return False
            if signer.declined:
                return False
            signer.signed_at = ts
            request = self._requests.get(signer.request_id)
            if request is not None and request.status not in _TERMINAL_STATUSES:
                all_signers = self._signers.get(signer.request_id, [])
                active = [s for s in all_signers if not s.declined]
                if active and all(s.signed_at is not None for s in active):
                    request.status = "completed"
                else:
                    if request.status == "pending":
                        request.status = "in_progress"
            return True

    def decline(self, signer_id: str) -> bool:
        """Mark a signer as declined."""
        with self._lock:
            signer = self._find_signer_locked(signer_id)
            if signer is None:
                return False
            if signer.declined:
                return False
            signer.declined = True
            request = self._requests.get(signer.request_id)
            if request is not None and request.status == "pending":
                request.status = "in_progress"
            return True

    def cancel(self, request_id: str) -> bool:
        """Cancel a non-terminal request."""
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                return False
            if request.status in _TERMINAL_STATUSES:
                return False
            request.status = "cancelled"
            return True

    def expire_if_due(self, now: Optional[float] = None) -> int:
        """Expire all pending/in_progress requests whose ``expires_at`` < ``now``."""
        ts = time.time() if now is None else now
        count = 0
        with self._lock:
            for request in self._requests.values():
                if request.status not in ("pending", "in_progress"):
                    continue
                if request.expires_at is None:
                    continue
                if request.expires_at < ts:
                    request.status = "expired"
                    count += 1
        return count

    # ------------------------------------------------------------------ queries

    def get_request(self, request_id: str) -> Optional[SigningRequest]:
        with self._lock:
            return self._requests.get(request_id)

    def get_signer(self, signer_id: str) -> Optional[Signer]:
        with self._lock:
            return self._find_signer_locked(signer_id)

    def signers_of(self, request_id: str) -> list[Signer]:
        with self._lock:
            signers = list(self._signers.get(request_id, []))
        return sorted(signers, key=lambda s: s.order)

    def pending_signers(self, request_id: str) -> list[Signer]:
        with self._lock:
            signers = [
                s
                for s in self._signers.get(request_id, [])
                if s.signed_at is None and not s.declined
            ]
        return sorted(signers, key=lambda s: s.order)

    def requests_for_doc(self, doc_id: str) -> list[SigningRequest]:
        with self._lock:
            matched = [r for r in self._requests.values() if r.doc_id == doc_id]
        return sorted(matched, key=lambda r: r.created_at)

    def requests_by_status(self, status: str) -> list[SigningRequest]:
        with self._lock:
            matched = [r for r in self._requests.values() if r.status == status]
        return sorted(matched, key=lambda r: r.created_at)

    def stats(self) -> SigningStats:
        with self._lock:
            total_requests = len(self._requests)
            pending = sum(1 for r in self._requests.values() if r.status == "pending")
            in_progress = sum(
                1 for r in self._requests.values() if r.status == "in_progress"
            )
            completed = sum(
                1 for r in self._requests.values() if r.status == "completed"
            )
            expired = sum(1 for r in self._requests.values() if r.status == "expired")
            cancelled = sum(
                1 for r in self._requests.values() if r.status == "cancelled"
            )
            total_signers = sum(len(lst) for lst in self._signers.values())
            total_signed = sum(
                1
                for lst in self._signers.values()
                for s in lst
                if s.signed_at is not None
            )
        return SigningStats(
            total_requests=total_requests,
            pending=pending,
            in_progress=in_progress,
            completed=completed,
            expired=expired,
            cancelled=cancelled,
            total_signers=total_signers,
            total_signed=total_signed,
        )
