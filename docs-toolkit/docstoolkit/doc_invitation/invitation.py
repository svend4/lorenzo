"""Invitation system implementation."""

from __future__ import annotations

import secrets
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class InviteStatus(str, Enum):
    """Lifecycle state of an invitation."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    REVOKED = "revoked"


class InviteRole(str, Enum):
    """Permitted collaboration role granted by an invitation."""

    VIEWER = "viewer"
    COMMENTER = "commenter"
    EDITOR = "editor"
    ADMIN = "admin"


@dataclass
class Invitation:
    """Server-side record of a document collaboration invitation."""

    invite_id: str
    doc_id: str
    invitee_email: str
    inviter_id: str
    role: InviteRole
    token: str
    status: InviteStatus = InviteStatus.PENDING
    created_at: float = 0.0
    expires_at: Optional[float] = None
    accepted_at: Optional[float] = None
    accepted_by_user_id: Optional[str] = None
    message: Optional[str] = None


@dataclass
class InviteStats:
    """Aggregate statistics across all invitations."""

    total: int = 0
    pending: int = 0
    accepted: int = 0
    declined: int = 0
    expired: int = 0
    revoked: int = 0

    @property
    def acceptance_rate(self) -> float:
        """Ratio of accepted invitations to total ever issued (0.0..1.0)."""
        if self.total == 0:
            return 0.0
        return self.accepted / self.total


class DocInvitation:
    """Manages the lifecycle of document collaboration invitations."""

    def __init__(self) -> None:
        self._invites: Dict[str, Invitation] = {}
        self._token_index: Dict[str, str] = {}
        self._counter: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ helpers
    def _new_invite_id(self) -> str:
        self._counter += 1
        return f"inv_{self._counter:08d}"

    @staticmethod
    def _is_expired(invite: Invitation, now: float) -> bool:
        return invite.expires_at is not None and invite.expires_at <= now

    # ------------------------------------------------------------------ create
    def create_invite(
        self,
        doc_id: str,
        invitee_email: str,
        inviter_id: str,
        role: InviteRole = InviteRole.VIEWER,
        expires_at: Optional[float] = None,
        message: Optional[str] = None,
        now: float = 0.0,
    ) -> Invitation:
        """Create a new PENDING invitation and return it."""
        with self._lock:
            invite_id = self._new_invite_id()
            token = secrets.token_urlsafe(32)
            invite = Invitation(
                invite_id=invite_id,
                doc_id=doc_id,
                invitee_email=invitee_email,
                inviter_id=inviter_id,
                role=role,
                token=token,
                status=InviteStatus.PENDING,
                created_at=now,
                expires_at=expires_at,
                accepted_at=None,
                accepted_by_user_id=None,
                message=message,
            )
            self._invites[invite_id] = invite
            self._token_index[token] = invite_id
            return invite

    # ------------------------------------------------------------------ accept
    def accept(
        self, token: str, user_id: str, now: float = 0.0
    ) -> Optional[Invitation]:
        """Mark a PENDING invitation as ACCEPTED. Returns None on failure."""
        with self._lock:
            invite_id = self._token_index.get(token)
            if invite_id is None:
                return None
            invite = self._invites.get(invite_id)
            if invite is None:
                return None
            if invite.status != InviteStatus.PENDING:
                return None
            if self._is_expired(invite, now):
                invite.status = InviteStatus.EXPIRED
                return None
            invite.status = InviteStatus.ACCEPTED
            invite.accepted_at = now
            invite.accepted_by_user_id = user_id
            return invite

    # ------------------------------------------------------------------ decline
    def decline(self, token: str, now: float = 0.0) -> Optional[Invitation]:
        """Decline a PENDING invitation by token. Returns None on failure."""
        with self._lock:
            invite_id = self._token_index.get(token)
            if invite_id is None:
                return None
            invite = self._invites.get(invite_id)
            if invite is None:
                return None
            if invite.status != InviteStatus.PENDING:
                return None
            if self._is_expired(invite, now):
                invite.status = InviteStatus.EXPIRED
                return None
            invite.status = InviteStatus.DECLINED
            return invite

    # ------------------------------------------------------------------ revoke
    def revoke(self, invite_id: str) -> bool:
        """Revoke a PENDING invitation. Returns True on success."""
        with self._lock:
            invite = self._invites.get(invite_id)
            if invite is None:
                return False
            if invite.status != InviteStatus.PENDING:
                return False
            invite.status = InviteStatus.REVOKED
            return True

    # ------------------------------------------------------------------ expire
    def expire_overdue(self, now: float = 0.0) -> int:
        """Mark all PENDING invites with expires_at <= now as EXPIRED."""
        count = 0
        with self._lock:
            for invite in self._invites.values():
                if (
                    invite.status == InviteStatus.PENDING
                    and invite.expires_at is not None
                    and invite.expires_at <= now
                ):
                    invite.status = InviteStatus.EXPIRED
                    count += 1
        return count

    # ------------------------------------------------------------------ lookups
    def get_invite(self, invite_id: str) -> Optional[Invitation]:
        with self._lock:
            return self._invites.get(invite_id)

    def get_by_token(self, token: str) -> Optional[Invitation]:
        with self._lock:
            invite_id = self._token_index.get(token)
            if invite_id is None:
                return None
            return self._invites.get(invite_id)

    def invites_for_doc(
        self, doc_id: str, status: Optional[InviteStatus] = None
    ) -> List[Invitation]:
        with self._lock:
            result = [i for i in self._invites.values() if i.doc_id == doc_id]
        if status is not None:
            result = [i for i in result if i.status == status]
        return result

    def invites_for_email(
        self, email: str, status: Optional[InviteStatus] = None
    ) -> List[Invitation]:
        with self._lock:
            result = [
                i for i in self._invites.values() if i.invitee_email == email
            ]
        if status is not None:
            result = [i for i in result if i.status == status]
        return result

    def invites_by_inviter(self, inviter_id: str) -> List[Invitation]:
        with self._lock:
            return [
                i for i in self._invites.values() if i.inviter_id == inviter_id
            ]

    def pending_invites(self, now: float = 0.0) -> List[Invitation]:
        """Return PENDING invites that are not yet expired."""
        with self._lock:
            return [
                i
                for i in self._invites.values()
                if i.status == InviteStatus.PENDING
                and not self._is_expired(i, now)
            ]

    # ------------------------------------------------------------------ mutate
    def resend(
        self,
        invite_id: str,
        new_expires_at: Optional[float] = None,
        now: float = 0.0,
    ) -> bool:
        """Extend the expiry of a PENDING invitation."""
        with self._lock:
            invite = self._invites.get(invite_id)
            if invite is None:
                return False
            if invite.status != InviteStatus.PENDING:
                return False
            invite.expires_at = new_expires_at
            return True

    def change_role(self, invite_id: str, new_role: InviteRole) -> bool:
        """Change the role of a PENDING invitation."""
        with self._lock:
            invite = self._invites.get(invite_id)
            if invite is None:
                return False
            if invite.status != InviteStatus.PENDING:
                return False
            invite.role = new_role
            return True

    # ------------------------------------------------------------------ stats
    def stats(self) -> InviteStats:
        s = InviteStats()
        with self._lock:
            for invite in self._invites.values():
                s.total += 1
                if invite.status == InviteStatus.PENDING:
                    s.pending += 1
                elif invite.status == InviteStatus.ACCEPTED:
                    s.accepted += 1
                elif invite.status == InviteStatus.DECLINED:
                    s.declined += 1
                elif invite.status == InviteStatus.EXPIRED:
                    s.expired += 1
                elif invite.status == InviteStatus.REVOKED:
                    s.revoked += 1
        return s

    @property
    def total_invites(self) -> int:
        with self._lock:
            return len(self._invites)

    def clear(self) -> None:
        with self._lock:
            self._invites.clear()
            self._token_index.clear()
            self._counter = 0
