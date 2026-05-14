"""E436 DocInviteLink — invite link generation and consumption.

Pure stdlib implementation, thread-safe via :class:`threading.Lock`.
Invite links carry an expiry, a max-use cap, and a revoked flag. The
:class:`DocInviteLink` class is the main interface; it owns an in-memory
catalogue of :class:`InviteLink` records indexed by ``link_id`` and by
``doc_id``.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class InviteLink:
    """A single invite link.

    Attributes
    ----------
    link_id:
        UUID token identifying this invite.
    doc_id:
        Identifier of the document this invite grants access to.
    created_by:
        Identifier of the user who created the invite.
    created_at:
        Unix timestamp at which the invite was created.
    expires_at:
        Unix timestamp at which the invite expires, or ``None`` for no expiry.
    max_uses:
        Maximum number of times the invite may be successfully used, or
        ``None`` for unlimited.
    use_count:
        Number of successful uses recorded so far.
    revoked:
        Whether the invite has been revoked.
    """

    link_id: str
    doc_id: str
    created_by: str
    created_at: float = 0.0
    expires_at: Optional[float] = None
    max_uses: Optional[int] = None
    use_count: int = 0
    revoked: bool = False

    def is_expired(self, now: float) -> bool:
        """Return ``True`` if the invite is past its ``expires_at`` timestamp."""
        return self.expires_at is not None and now >= self.expires_at

    def is_exhausted(self) -> bool:
        """Return ``True`` if ``use_count`` has reached ``max_uses``."""
        return self.max_uses is not None and self.use_count >= self.max_uses

    def is_valid(self, now: float) -> bool:
        """Return ``True`` if the invite is usable: not revoked, expired or exhausted."""
        if self.revoked:
            return False
        if self.is_expired(now):
            return False
        if self.is_exhausted():
            return False
        return True


@dataclass
class LinkStats:
    """Aggregate statistics across all known invite links."""

    total_links: int
    active_links: int
    revoked_count: int
    total_uses: int


# ---------------------------------------------------------------------------
# Main interface
# ---------------------------------------------------------------------------


class DocInviteLink:
    """Thread-safe registry for document invite links."""

    def __init__(self) -> None:
        self._links: Dict[str, InviteLink] = {}
        self._by_doc: Dict[str, List[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else now

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def create_link(
        self,
        doc_id: str,
        created_by: str,
        expires_at: Optional[float] = None,
        duration_seconds: Optional[float] = None,
        max_uses: Optional[int] = None,
        now: Optional[float] = None,
    ) -> InviteLink:
        """Create and register a new invite link.

        If ``duration_seconds`` is provided, it overrides ``expires_at`` and is
        computed relative to ``now``. ``max_uses``, when given, must be
        positive.
        """
        if max_uses is not None and max_uses <= 0:
            raise ValueError("max_uses must be positive when set")
        if duration_seconds is not None and duration_seconds < 0:
            raise ValueError("duration_seconds must be non-negative when set")

        ts = self._now(now)
        if duration_seconds is not None:
            expires_at = ts + duration_seconds

        link = InviteLink(
            link_id=uuid.uuid4().hex,
            doc_id=doc_id,
            created_by=created_by,
            created_at=ts,
            expires_at=expires_at,
            max_uses=max_uses,
            use_count=0,
            revoked=False,
        )
        with self._lock:
            self._links[link.link_id] = link
            self._by_doc.setdefault(doc_id, []).append(link.link_id)
        return link

    def use_link(self, link_id: str, now: Optional[float] = None) -> bool:
        """Consume one use of the invite. Return ``True`` on success."""
        ts = self._now(now)
        with self._lock:
            link = self._links.get(link_id)
            if link is None:
                return False
            if not link.is_valid(ts):
                return False
            link.use_count += 1
            return True

    def revoke(self, link_id: str) -> bool:
        """Mark an invite as revoked. Return ``True`` if a change was made."""
        with self._lock:
            link = self._links.get(link_id)
            if link is None or link.revoked:
                return False
            link.revoked = True
            return True

    def delete(self, link_id: str) -> bool:
        """Delete an invite from the registry. Return ``True`` if it existed."""
        with self._lock:
            link = self._links.pop(link_id, None)
            if link is None:
                return False
            ids = self._by_doc.get(link.doc_id)
            if ids is not None:
                try:
                    ids.remove(link_id)
                except ValueError:
                    pass
                if not ids:
                    self._by_doc.pop(link.doc_id, None)
            return True

    def revoke_all_for_doc(self, doc_id: str) -> int:
        """Revoke every non-revoked invite for ``doc_id``. Return count revoked."""
        revoked = 0
        with self._lock:
            for lid in self._by_doc.get(doc_id, []):
                link = self._links.get(lid)
                if link is not None and not link.revoked:
                    link.revoked = True
                    revoked += 1
        return revoked

    def purge_invalid(self, now: Optional[float] = None) -> int:
        """Delete every invalid invite (expired, exhausted or revoked).

        Returns the number of invites deleted.
        """
        ts = self._now(now)
        removed = 0
        with self._lock:
            doomed = [
                lid
                for lid, link in self._links.items()
                if link.revoked or link.is_expired(ts) or link.is_exhausted()
            ]
            for lid in doomed:
                link = self._links.pop(lid)
                ids = self._by_doc.get(link.doc_id)
                if ids is not None:
                    try:
                        ids.remove(lid)
                    except ValueError:
                        pass
                    if not ids:
                        self._by_doc.pop(link.doc_id, None)
                removed += 1
        return removed

    # ------------------------------------------------------------------
    # Read-only queries
    # ------------------------------------------------------------------

    def is_valid(self, link_id: str, now: Optional[float] = None) -> bool:
        """Return ``True`` if the invite exists and is currently usable."""
        ts = self._now(now)
        with self._lock:
            link = self._links.get(link_id)
            if link is None:
                return False
            return link.is_valid(ts)

    def get_link(self, link_id: str) -> Optional[InviteLink]:
        """Return the invite, or ``None`` if unknown."""
        with self._lock:
            return self._links.get(link_id)

    def links_for_doc(
        self,
        doc_id: str,
        include_invalid: bool = False,
        now: Optional[float] = None,
    ) -> List[InviteLink]:
        """Return invites for ``doc_id`` sorted by ``created_at`` descending."""
        ts = self._now(now)
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            result = [self._links[lid] for lid in ids if lid in self._links]
        if not include_invalid:
            result = [link for link in result if link.is_valid(ts)]
        result.sort(key=lambda l: l.created_at, reverse=True)
        return result

    def active_links(self, now: Optional[float] = None) -> List[InviteLink]:
        """Return every currently-valid invite, newest first."""
        ts = self._now(now)
        with self._lock:
            result = [link for link in self._links.values() if link.is_valid(ts)]
        result.sort(key=lambda l: l.created_at, reverse=True)
        return result

    def expired_links(self, now: Optional[float] = None) -> List[InviteLink]:
        """Return every invite that has passed its ``expires_at``."""
        ts = self._now(now)
        with self._lock:
            result = [link for link in self._links.values() if link.is_expired(ts)]
        result.sort(key=lambda l: l.created_at, reverse=True)
        return result

    def exhausted_links(self) -> List[InviteLink]:
        """Return every invite whose ``use_count`` has reached ``max_uses``."""
        with self._lock:
            result = [link for link in self._links.values() if link.is_exhausted()]
        result.sort(key=lambda l: l.created_at, reverse=True)
        return result

    def stats(self, now: Optional[float] = None) -> LinkStats:
        """Snapshot aggregate counts across the registry."""
        ts = self._now(now)
        with self._lock:
            total = len(self._links)
            active = sum(1 for link in self._links.values() if link.is_valid(ts))
            revoked = sum(1 for link in self._links.values() if link.revoked)
            uses = sum(link.use_count for link in self._links.values())
        return LinkStats(
            total_links=total,
            active_links=active,
            revoked_count=revoked,
            total_uses=uses,
        )
