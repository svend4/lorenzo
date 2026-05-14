"""E202 Document publishing manager.

Manages document publication lifecycle: drafts, scheduled releases, embargo
windows, and revocations. Uses only the Python standard library (``threading``,
``dataclasses``, ``enum``).

The manager keeps **one** active :class:`Publication` per ``doc_id`` (the most
recent one). All operations are thread-safe via an internal lock and accept a
deterministic ``now`` parameter (seconds since epoch).
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Enums and dataclasses
# ---------------------------------------------------------------------------


class PublishState(Enum):
    """Lifecycle states of a publication."""

    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    EMBARGOED = "embargoed"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class Publication:
    """A publication record for a single document."""

    pub_id: str
    doc_id: str
    state: PublishState
    scheduled_for: Optional[float] = None
    published_at: Optional[float] = None
    expires_at: Optional[float] = None
    revoked_at: Optional[float] = None
    revoked_by: Optional[str] = None
    author: Optional[str] = None
    embargo_until: Optional[float] = None


@dataclass
class PublishStats:
    """Aggregate publication statistics."""

    total: int
    by_state: Dict[str, int] = field(default_factory=dict)
    scheduled_count: int = 0
    published_count: int = 0


# Terminal states – cannot transition out of these (except by submitting a new draft).
_TERMINAL_STATES = {PublishState.REVOKED, PublishState.EXPIRED}


# ---------------------------------------------------------------------------
# DocPublish
# ---------------------------------------------------------------------------


class DocPublish:
    """In-memory thread-safe publication manager."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # doc_id -> Publication
        self._pubs: Dict[str, Publication] = {}
        # counter for total publications ever created
        self._total: int = 0

    # ------------------------------------------------------------------
    # Internal helpers (must be called with the lock held)
    # ------------------------------------------------------------------

    def _new_pub_id(self) -> str:
        return uuid.uuid4().hex

    def _effective_state(self, pub: Publication, now: float) -> PublishState:
        """Compute the dynamic state given ``now``.

        Does not mutate the publication. Useful for ``state_of`` and ``is_public``
        queries where we don't want to write through state until the caller
        invokes the appropriate release/expire method.
        """
        if pub.state in _TERMINAL_STATES:
            return pub.state
        # If revoked timestamp present, treat as REVOKED
        if pub.revoked_at is not None:
            return PublishState.REVOKED
        # Expiration takes priority over embargo
        if pub.state == PublishState.PUBLISHED and pub.expires_at is not None and pub.expires_at <= now:
            return PublishState.EXPIRED
        # SCHEDULED → PUBLISHED if time has come (and not under embargo)
        if pub.state == PublishState.SCHEDULED and pub.scheduled_for is not None and pub.scheduled_for <= now:
            if pub.embargo_until is None or pub.embargo_until <= now:
                return PublishState.PUBLISHED
            return PublishState.EMBARGOED
        # PUBLISHED but embargo still active
        if pub.state == PublishState.PUBLISHED and pub.embargo_until is not None and pub.embargo_until > now:
            return PublishState.EMBARGOED
        # EMBARGOED but embargo lifted
        if pub.state == PublishState.EMBARGOED and pub.embargo_until is not None and pub.embargo_until <= now:
            return PublishState.PUBLISHED
        return pub.state

    # ------------------------------------------------------------------
    # Submission / scheduling / immediate publication
    # ------------------------------------------------------------------

    def submit_draft(
        self,
        doc_id: str,
        author: Optional[str] = None,
        now: float = 0.0,
    ) -> Publication:
        """Create (or replace) a publication record in :pyattr:`PublishState.DRAFT`."""
        with self._lock:
            pub = Publication(
                pub_id=self._new_pub_id(),
                doc_id=doc_id,
                state=PublishState.DRAFT,
                author=author,
            )
            self._pubs[doc_id] = pub
            self._total += 1
            return pub

    def schedule(
        self,
        doc_id: str,
        scheduled_for: float,
        expires_at: Optional[float] = None,
        embargo_until: Optional[float] = None,
        now: float = 0.0,
    ) -> Optional[Publication]:
        """Schedule a draft for publication.

        If ``scheduled_for`` is in the past (or zero) and there's no active
        embargo, the publication immediately transitions to PUBLISHED. Otherwise
        it becomes SCHEDULED. Returns ``None`` if the document has no draft or
        is in a terminal state.
        """
        with self._lock:
            pub = self._pubs.get(doc_id)
            if pub is None:
                return None
            if pub.state in _TERMINAL_STATES:
                return None
            # only DRAFT may be scheduled
            if pub.state != PublishState.DRAFT:
                return None
            pub.scheduled_for = scheduled_for
            pub.expires_at = expires_at
            pub.embargo_until = embargo_until
            # Decide initial state
            if scheduled_for <= now:
                # past or now → publish immediately (respecting embargo)
                if embargo_until is not None and embargo_until > now:
                    pub.state = PublishState.EMBARGOED
                    pub.published_at = None
                else:
                    pub.state = PublishState.PUBLISHED
                    pub.published_at = now
            else:
                pub.state = PublishState.SCHEDULED
            return pub

    def publish_now(
        self,
        doc_id: str,
        expires_at: Optional[float] = None,
        now: float = 0.0,
    ) -> Optional[Publication]:
        """Immediately publish the document.

        Works from any non-terminal state. Returns ``None`` if the document is
        unknown or in a terminal state.
        """
        with self._lock:
            pub = self._pubs.get(doc_id)
            if pub is None:
                return None
            if pub.state in _TERMINAL_STATES:
                return None
            pub.state = PublishState.PUBLISHED
            pub.published_at = now
            if expires_at is not None:
                pub.expires_at = expires_at
            # publishing clears any pending embargo set during scheduling
            pub.embargo_until = None
            return pub

    # ------------------------------------------------------------------
    # Embargo / revocation
    # ------------------------------------------------------------------

    def embargo(self, doc_id: str, embargo_until: float) -> bool:
        """Place a currently-PUBLISHED document under embargo until the given time.

        Returns ``True`` on success, ``False`` if the publication is missing or
        not currently PUBLISHED.
        """
        with self._lock:
            pub = self._pubs.get(doc_id)
            if pub is None:
                return False
            if pub.state != PublishState.PUBLISHED:
                return False
            pub.state = PublishState.EMBARGOED
            pub.embargo_until = embargo_until
            return True

    def revoke(self, doc_id: str, revoked_by: str, now: float = 0.0) -> bool:
        """Revoke a publication (terminal). Returns ``False`` if already revoked."""
        with self._lock:
            pub = self._pubs.get(doc_id)
            if pub is None:
                return False
            if pub.state == PublishState.REVOKED:
                return False
            pub.state = PublishState.REVOKED
            pub.revoked_at = now
            pub.revoked_by = revoked_by
            return True

    # ------------------------------------------------------------------
    # Time-driven transitions
    # ------------------------------------------------------------------

    def release_for_publish(self, now: float = 0.0) -> List[Publication]:
        """Publish all SCHEDULED documents whose time has come.

        Documents whose embargo is still active are transitioned to EMBARGOED
        instead and **not** included in the returned list.
        """
        released: List[Publication] = []
        with self._lock:
            for pub in self._pubs.values():
                if pub.state != PublishState.SCHEDULED:
                    continue
                if pub.scheduled_for is None or pub.scheduled_for > now:
                    continue
                # time reached; check embargo
                if pub.embargo_until is not None and pub.embargo_until > now:
                    pub.state = PublishState.EMBARGOED
                    continue
                pub.state = PublishState.PUBLISHED
                pub.published_at = now
                released.append(pub)
        return released

    def expire_overdue(self, now: float = 0.0) -> int:
        """Expire any PUBLISHED documents whose ``expires_at`` has passed.

        Returns the number of newly expired documents.
        """
        count = 0
        with self._lock:
            for pub in self._pubs.values():
                if pub.state != PublishState.PUBLISHED:
                    continue
                if pub.expires_at is not None and pub.expires_at <= now:
                    pub.state = PublishState.EXPIRED
                    count += 1
        return count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get(self, doc_id: str) -> Optional[Publication]:
        """Return the publication record (or ``None``)."""
        with self._lock:
            return self._pubs.get(doc_id)

    def state_of(self, doc_id: str, now: float = 0.0) -> Optional[PublishState]:
        """Return the *effective* state of a publication at ``now``."""
        with self._lock:
            pub = self._pubs.get(doc_id)
            if pub is None:
                return None
            return self._effective_state(pub, now)

    def is_public(self, doc_id: str, now: float = 0.0) -> bool:
        """Return ``True`` iff the document is publicly visible at ``now``."""
        with self._lock:
            pub = self._pubs.get(doc_id)
            if pub is None:
                return False
            return self._effective_state(pub, now) == PublishState.PUBLISHED

    def published_docs(self, now: float = 0.0) -> List[Publication]:
        """Return publications whose effective state is PUBLISHED."""
        with self._lock:
            return [
                p for p in self._pubs.values()
                if self._effective_state(p, now) == PublishState.PUBLISHED
            ]

    def scheduled_docs(self) -> List[Publication]:
        """Return all publications currently in SCHEDULED state."""
        with self._lock:
            return [p for p in self._pubs.values() if p.state == PublishState.SCHEDULED]

    def embargoed_docs(self, now: float = 0.0) -> List[Publication]:
        """Return publications whose effective state is EMBARGOED."""
        with self._lock:
            return [
                p for p in self._pubs.values()
                if self._effective_state(p, now) == PublishState.EMBARGOED
            ]

    def revoked_docs(self) -> List[Publication]:
        """Return all revoked publications."""
        with self._lock:
            return [p for p in self._pubs.values() if p.state == PublishState.REVOKED]

    def next_scheduled(self, now: float = 0.0) -> Optional[Publication]:
        """Return the SCHEDULED publication with the earliest ``scheduled_for``.

        Publications already due (``scheduled_for <= now``) still count — they
        just haven't been released yet.
        """
        with self._lock:
            candidates = [
                p for p in self._pubs.values()
                if p.state == PublishState.SCHEDULED and p.scheduled_for is not None
            ]
            if not candidates:
                return None
            return min(candidates, key=lambda p: p.scheduled_for)

    def stats(self, now: float = 0.0) -> PublishStats:
        """Return aggregate statistics computed from effective states."""
        with self._lock:
            by_state: Dict[str, int] = {s.value: 0 for s in PublishState}
            scheduled_count = 0
            published_count = 0
            for pub in self._pubs.values():
                eff = self._effective_state(pub, now)
                by_state[eff.value] = by_state.get(eff.value, 0) + 1
                if eff == PublishState.SCHEDULED:
                    scheduled_count += 1
                elif eff == PublishState.PUBLISHED:
                    published_count += 1
            return PublishStats(
                total=len(self._pubs),
                by_state=by_state,
                scheduled_count=scheduled_count,
                published_count=published_count,
            )

    # ------------------------------------------------------------------
    # Bulk
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Forget all publications."""
        with self._lock:
            self._pubs.clear()
            self._total = 0

    @property
    def total_publications(self) -> int:
        """Total number of publications ever submitted (not the current count)."""
        with self._lock:
            return self._total
