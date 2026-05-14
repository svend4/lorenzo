"""Core implementation of the DocInvitationStore (E366).

Pure stdlib, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import time
import uuid
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Invitation:
    """A single invitation to access a document."""

    invitation_id: str
    doc_id: str
    invitee: str
    invited_by: str
    role: str = "viewer"
    created_at: float = 0.0
    expires_at: Optional[float] = None
    status: str = "pending"
    accepted_at: Optional[float] = None
    accepted_by: str = ""


@dataclass
class InvitationStats:
    """Aggregate statistics across all invitations."""

    total: int = 0
    pending: int = 0
    accepted: int = 0
    declined: int = 0
    expired: int = 0
    revoked: int = 0


class DocInvitationStore:
    """Manage invitations to access documents."""

    def __init__(self) -> None:
        self._invitations: dict[str, Invitation] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._by_invitee: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # --------------------------------------------------------------
    # Create
    # --------------------------------------------------------------
    def invite(
        self,
        doc_id: str,
        invitee: str,
        invited_by: str,
        role: str = "viewer",
        expires_at: Optional[float] = None,
        now: Optional[float] = None,
    ) -> Invitation:
        """Create a new pending invitation."""
        ts = now if now is not None else time.time()
        invitation_id = str(uuid.uuid4())
        inv = Invitation(
            invitation_id=invitation_id,
            doc_id=doc_id,
            invitee=invitee,
            invited_by=invited_by,
            role=role,
            created_at=ts,
            expires_at=expires_at,
            status="pending",
        )
        with self._lock:
            self._invitations[invitation_id] = inv
            self._by_doc.setdefault(doc_id, []).append(invitation_id)
            self._by_invitee.setdefault(invitee, []).append(invitation_id)
        return inv

    # --------------------------------------------------------------
    # State transitions
    # --------------------------------------------------------------
    def accept(
        self,
        invitation_id: str,
        accepted_by: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Accept a pending invitation."""
        ts = now if now is not None else time.time()
        with self._lock:
            inv = self._invitations.get(invitation_id)
            if inv is None or inv.status != "pending":
                return False
            inv.status = "accepted"
            inv.accepted_at = ts
            inv.accepted_by = accepted_by if accepted_by else inv.invitee
        return True

    def decline(self, invitation_id: str) -> bool:
        """Decline a pending invitation."""
        with self._lock:
            inv = self._invitations.get(invitation_id)
            if inv is None or inv.status != "pending":
                return False
            inv.status = "declined"
        return True

    def revoke(self, invitation_id: str) -> bool:
        """Revoke a pending or accepted invitation."""
        with self._lock:
            inv = self._invitations.get(invitation_id)
            if inv is None or inv.status not in ("pending", "accepted"):
                return False
            inv.status = "revoked"
        return True

    def expire_if_due(self, now: Optional[float] = None) -> int:
        """Expire any pending invitations whose expires_at < now."""
        ts = now if now is not None else time.time()
        count = 0
        with self._lock:
            for inv in self._invitations.values():
                if (
                    inv.status == "pending"
                    and inv.expires_at is not None
                    and inv.expires_at < ts
                ):
                    inv.status = "expired"
                    count += 1
        return count

    # --------------------------------------------------------------
    # Queries
    # --------------------------------------------------------------
    def get(self, invitation_id: str) -> Optional[Invitation]:
        """Look up an invitation by id."""
        with self._lock:
            return self._invitations.get(invitation_id)

    def invitations_for_doc(
        self, doc_id: str, status: Optional[str] = None
    ) -> list[Invitation]:
        """Return invitations attached to ``doc_id``, sorted by created_at."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            result = [self._invitations[i] for i in ids if i in self._invitations]
        if status is not None:
            result = [inv for inv in result if inv.status == status]
        result.sort(key=lambda inv: inv.created_at)
        return result

    def invitations_for_invitee(
        self, invitee: str, status: Optional[str] = None
    ) -> list[Invitation]:
        """Return invitations sent to ``invitee``, sorted by created_at."""
        with self._lock:
            ids = list(self._by_invitee.get(invitee, []))
            result = [self._invitations[i] for i in ids if i in self._invitations]
        if status is not None:
            result = [inv for inv in result if inv.status == status]
        result.sort(key=lambda inv: inv.created_at)
        return result

    def pending_for(self, doc_id: str) -> list[Invitation]:
        """Return only pending invitations for ``doc_id`` sorted by created_at."""
        return self.invitations_for_doc(doc_id, status="pending")

    # --------------------------------------------------------------
    # Mutation
    # --------------------------------------------------------------
    def delete(self, invitation_id: str) -> bool:
        """Fully remove an invitation from the store."""
        with self._lock:
            inv = self._invitations.pop(invitation_id, None)
            if inv is None:
                return False
            doc_ids = self._by_doc.get(inv.doc_id)
            if doc_ids and invitation_id in doc_ids:
                doc_ids.remove(invitation_id)
                if not doc_ids:
                    del self._by_doc[inv.doc_id]
            invitee_ids = self._by_invitee.get(inv.invitee)
            if invitee_ids and invitation_id in invitee_ids:
                invitee_ids.remove(invitation_id)
                if not invitee_ids:
                    del self._by_invitee[inv.invitee]
        return True

    # --------------------------------------------------------------
    # Stats
    # --------------------------------------------------------------
    def stats(self) -> InvitationStats:
        """Return aggregate stats over all invitations."""
        s = InvitationStats()
        with self._lock:
            for inv in self._invitations.values():
                s.total += 1
                if inv.status == "pending":
                    s.pending += 1
                elif inv.status == "accepted":
                    s.accepted += 1
                elif inv.status == "declined":
                    s.declined += 1
                elif inv.status == "expired":
                    s.expired += 1
                elif inv.status == "revoked":
                    s.revoked += 1
        return s
