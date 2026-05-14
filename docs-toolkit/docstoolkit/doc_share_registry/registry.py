"""DocShareRegistry — share links and direct access grants for documents.

All state is kept in memory with a single :class:`threading.Lock` guarding
every mutation and read that touches internal dicts, so the registry is safe
to use from multiple threads without any external synchronisation.

UUID tokens are generated with :func:`uuid.uuid4` (stdlib only).
Timestamps are ``float`` Unix seconds; pass ``now`` in tests for determinism.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _now(now: Optional[float]) -> float:
    """Return *now* if provided, else :func:`time.time`."""
    if now is not None:
        return now
    return time.time()


# ---------------------------------------------------------------------------
# dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ShareLink:
    """A shareable link for a document.

    Parameters
    ----------
    link_id:
        Unique UUID token identifying this link.
    doc_id:
        The document this link points to.
    created_by:
        User id of the creator.
    created_at:
        Unix timestamp of creation (default 0.0, set by :class:`DocShareRegistry`).
    expires_at:
        Unix timestamp after which the link is no longer valid; ``None`` means
        the link never expires.
    access_level:
        One of ``"read"``, ``"comment"``, or ``"edit"``.
    use_count:
        Number of times the link has been successfully used.
    revoked:
        Whether the link has been explicitly revoked.
    """

    link_id: str
    doc_id: str
    created_by: str
    created_at: float = 0.0
    expires_at: Optional[float] = None
    access_level: str = "read"
    use_count: int = 0
    revoked: bool = False


@dataclass
class ShareGrant:
    """A direct share grant to a specific user.

    Parameters
    ----------
    grant_id:
        Unique UUID identifying this grant.
    doc_id:
        The document this grant covers.
    granted_to:
        User id receiving access.
    granted_by:
        User id of the granter.
    granted_at:
        Unix timestamp of grant creation (default 0.0, set by registry).
    access_level:
        One of ``"read"``, ``"comment"``, or ``"edit"``.
    revoked:
        Whether the grant has been explicitly revoked.
    """

    grant_id: str
    doc_id: str
    granted_to: str
    granted_by: str
    granted_at: float = 0.0
    access_level: str = "read"
    revoked: bool = False


@dataclass
class ShareStats:
    """Aggregate statistics for the registry.

    Parameters
    ----------
    total_links:
        Number of non-revoked share links.
    total_grants:
        Number of non-revoked share grants.
    unique_shared_docs:
        Number of distinct documents covered by at least one non-revoked link
        or grant.
    """

    total_links: int
    total_grants: int
    unique_shared_docs: int


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

class DocShareRegistry:
    """Thread-safe in-memory manager for document share links and grants.

    All public methods acquire ``_lock`` for the duration of their
    critical section, so concurrent callers will never observe partial
    state.

    Internal storage
    ----------------
    ``_links``      — ``link_id  → ShareLink``
    ``_grants``     — ``grant_id → ShareGrant``
    ``_doc_links``  — ``doc_id   → [link_id, ...]``
    ``_doc_grants`` — ``doc_id   → [grant_id, ...]``
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._links: dict[str, ShareLink] = {}
        self._grants: dict[str, ShareGrant] = {}
        self._doc_links: dict[str, list[str]] = {}
        self._doc_grants: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # share-link API
    # ------------------------------------------------------------------

    def create_link(
        self,
        doc_id: str,
        created_by: str,
        access_level: str = "read",
        expires_at: Optional[float] = None,
        now: Optional[float] = None,
    ) -> ShareLink:
        """Create and store a new share link; returns the new :class:`ShareLink`."""

        link = ShareLink(
            link_id=str(uuid.uuid4()),
            doc_id=doc_id,
            created_by=created_by,
            created_at=_now(now),
            expires_at=expires_at,
            access_level=access_level,
        )
        with self._lock:
            self._links[link.link_id] = link
            self._doc_links.setdefault(doc_id, []).append(link.link_id)
        return link

    def revoke_link(self, link_id: str) -> bool:
        """Mark a link as revoked.

        Returns
        -------
        bool
            ``True`` if the link was found and revoked; ``False`` if the
            link does not exist.
        """

        with self._lock:
            link = self._links.get(link_id)
            if link is None:
                return False
            link.revoked = True
            return True

    def get_link(self, link_id: str) -> Optional[ShareLink]:
        """Return the :class:`ShareLink` for *link_id*, or ``None``."""

        with self._lock:
            return self._links.get(link_id)

    def use_link(self, link_id: str, now: Optional[float] = None) -> bool:
        """Increment ``use_count`` if the link is currently valid.

        A link is valid when it is not revoked and not expired (comparing
        against *now*).

        Returns
        -------
        bool
            ``True`` if the use was counted; ``False`` otherwise.
        """

        ts = _now(now)
        with self._lock:
            link = self._links.get(link_id)
            if link is None:
                return False
            if link.revoked:
                return False
            if link.expires_at is not None and ts >= link.expires_at:
                return False
            link.use_count += 1
            return True

    def links_for_doc(
        self,
        doc_id: str,
        include_revoked: bool = False,
    ) -> list[ShareLink]:
        """Return share links for *doc_id*, sorted by ``created_at`` ascending.

        Parameters
        ----------
        include_revoked:
            When ``False`` (default) revoked links are omitted.
        """

        with self._lock:
            ids = self._doc_links.get(doc_id, [])
            links = [self._links[lid] for lid in ids if lid in self._links]
        if not include_revoked:
            links = [lnk for lnk in links if not lnk.revoked]
        links.sort(key=lambda lnk: lnk.created_at)
        return links

    # ------------------------------------------------------------------
    # grant API
    # ------------------------------------------------------------------

    def grant_access(
        self,
        doc_id: str,
        granted_to: str,
        granted_by: str,
        access_level: str = "read",
        now: Optional[float] = None,
    ) -> ShareGrant:
        """Create and store a new access grant; returns the :class:`ShareGrant`."""

        grant = ShareGrant(
            grant_id=str(uuid.uuid4()),
            doc_id=doc_id,
            granted_to=granted_to,
            granted_by=granted_by,
            granted_at=_now(now),
            access_level=access_level,
        )
        with self._lock:
            self._grants[grant.grant_id] = grant
            self._doc_grants.setdefault(doc_id, []).append(grant.grant_id)
        return grant

    def revoke_grant(self, grant_id: str) -> bool:
        """Mark a grant as revoked.

        Returns
        -------
        bool
            ``True`` if found and revoked; ``False`` if not found.
        """

        with self._lock:
            grant = self._grants.get(grant_id)
            if grant is None:
                return False
            grant.revoked = True
            return True

    def get_grant(self, grant_id: str) -> Optional[ShareGrant]:
        """Return the :class:`ShareGrant` for *grant_id*, or ``None``."""

        with self._lock:
            return self._grants.get(grant_id)

    def grants_for_doc(
        self,
        doc_id: str,
        include_revoked: bool = False,
    ) -> list[ShareGrant]:
        """Return grants for *doc_id*, sorted by ``granted_at`` ascending.

        Parameters
        ----------
        include_revoked:
            When ``False`` (default) revoked grants are omitted.
        """

        with self._lock:
            ids = self._doc_grants.get(doc_id, [])
            grants = [self._grants[gid] for gid in ids if gid in self._grants]
        if not include_revoked:
            grants = [g for g in grants if not g.revoked]
        grants.sort(key=lambda g: g.granted_at)
        return grants

    def grants_for_user(
        self,
        user_id: str,
        include_revoked: bool = False,
    ) -> list[ShareGrant]:
        """Return all grants for *user_id* across all documents.

        Sorted by ``granted_at`` ascending.

        Parameters
        ----------
        include_revoked:
            When ``False`` (default) revoked grants are omitted.
        """

        with self._lock:
            grants = [g for g in self._grants.values() if g.granted_to == user_id]
        if not include_revoked:
            grants = [g for g in grants if not g.revoked]
        grants.sort(key=lambda g: g.granted_at)
        return grants

    def has_access(self, user_id: str, doc_id: str) -> bool:
        """Return ``True`` if *user_id* has at least one non-revoked grant for *doc_id*."""

        with self._lock:
            ids = self._doc_grants.get(doc_id, [])
            for gid in ids:
                g = self._grants.get(gid)
                if g is not None and g.granted_to == user_id and not g.revoked:
                    return True
        return False

    # ------------------------------------------------------------------
    # aggregates
    # ------------------------------------------------------------------

    def stats(self) -> ShareStats:
        """Return aggregate :class:`ShareStats` for the current registry state."""

        with self._lock:
            active_links = [lnk for lnk in self._links.values() if not lnk.revoked]
            active_grants = [g for g in self._grants.values() if not g.revoked]

        shared_docs: set[str] = set()
        for lnk in active_links:
            shared_docs.add(lnk.doc_id)
        for g in active_grants:
            shared_docs.add(g.doc_id)

        return ShareStats(
            total_links=len(active_links),
            total_grants=len(active_grants),
            unique_shared_docs=len(shared_docs),
        )
