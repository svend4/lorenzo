"""Document share-link manager.

Each ``ShareLink`` carries an opaque URL-safe token (``secrets.token_urlsafe(32)``)
that callers embed into share URLs. The manager records every access attempt
in an audit list and supports password-protected, expiring, and use-limited
shares. Password hashing is ``sha256(password + secret)``; verification uses
``hmac.compare_digest`` to avoid timing side-channels.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ShareStatus(Enum):
    """Lifecycle state of a share link."""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    EXHAUSTED = "exhausted"


class PermissionLevel(Enum):
    """Permissions granted to a share-link consumer."""

    VIEW = "view"
    COMMENT = "comment"
    EDIT = "edit"


@dataclass
class ShareLink:
    """A single share record."""

    share_id: str
    doc_id: str
    token: str
    created_by: str
    created_at: float
    expires_at: Optional[float] = None
    max_uses: Optional[int] = None
    use_count: int = 0
    password_hash: Optional[str] = None
    permission: PermissionLevel = PermissionLevel.VIEW
    revoked: bool = False


@dataclass
class AccessRecord:
    """A single access attempt against a share link."""

    share_id: str
    accessed_at: float
    succeeded: bool
    reason: Optional[str] = None


@dataclass
class ShareStats:
    """Aggregate counters across the share store."""

    total_shares: int
    active: int
    expired: int
    revoked: int
    exhausted: int
    total_uses: int


def _resolve_now(now: float) -> float:
    """Return ``now`` if positive, else current wall-clock time.

    The 0.0 sentinel keeps tests deterministic while letting callers
    omit the argument in production.
    """

    if now and now > 0:
        return now
    return time.time()


class DocShare:
    """Thread-safe in-memory store of share links.

    A single ``secret`` is mixed into every password hash so that an
    attacker who lifts the in-memory database alone cannot precompute
    a rainbow table against well-known passwords.
    """

    def __init__(self, secret: str = "") -> None:
        self._secret = secret
        self._lock = threading.Lock()
        self._shares: dict[str, ShareLink] = {}
        self._by_token: dict[str, str] = {}
        self._history: list[AccessRecord] = []

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256((password + self._secret).encode("utf-8")).hexdigest()

    def _status_locked(self, share: ShareLink, now: float) -> ShareStatus:
        if share.revoked:
            return ShareStatus.REVOKED
        if share.expires_at is not None and now >= share.expires_at:
            return ShareStatus.EXPIRED
        if share.max_uses is not None and share.use_count >= share.max_uses:
            return ShareStatus.EXHAUSTED
        return ShareStatus.ACTIVE

    def _record(self, share_id: str, when: float, ok: bool, reason: Optional[str]) -> None:
        self._history.append(
            AccessRecord(
                share_id=share_id,
                accessed_at=when,
                succeeded=ok,
                reason=reason,
            )
        )

    # ------------------------------------------------------------------
    # mutation API
    # ------------------------------------------------------------------
    def create_share(
        self,
        doc_id: str,
        created_by: str,
        expires_at: Optional[float] = None,
        max_uses: Optional[int] = None,
        password: Optional[str] = None,
        permission: PermissionLevel = PermissionLevel.VIEW,
        now: float = 0.0,
    ) -> ShareLink:
        """Create a new share link and return its server-side record."""

        ts = _resolve_now(now)
        share_id = secrets.token_hex(16)
        token = secrets.token_urlsafe(32)
        password_hash = self._hash_password(password) if password else None
        link = ShareLink(
            share_id=share_id,
            doc_id=doc_id,
            token=token,
            created_by=created_by,
            created_at=ts,
            expires_at=expires_at,
            max_uses=max_uses,
            use_count=0,
            password_hash=password_hash,
            permission=permission,
            revoked=False,
        )
        with self._lock:
            self._shares[share_id] = link
            self._by_token[token] = share_id
        return link

    def revoke(self, share_id: str) -> bool:
        """Mark a share as revoked. Returns False if unknown or already revoked."""

        with self._lock:
            share = self._shares.get(share_id)
            if share is None or share.revoked:
                return False
            share.revoked = True
            return True

    def access(
        self,
        token: str,
        password: Optional[str] = None,
        now: float = 0.0,
    ) -> Optional[ShareLink]:
        """Attempt to access a share by token; returns the ShareLink on success.

        A failed attempt (unknown token, wrong password, expired, etc.) records
        an audit row but does not increment ``use_count``.
        """

        ts = _resolve_now(now)
        with self._lock:
            share_id = self._by_token.get(token)
            if share_id is None:
                # No id to attach the audit row to — log under empty share_id.
                self._record("", ts, False, "unknown_token")
                return None
            share = self._shares[share_id]
            status = self._status_locked(share, ts)
            if status is not ShareStatus.ACTIVE:
                self._record(share_id, ts, False, status.value)
                return None
            if share.password_hash is not None:
                if password is None:
                    self._record(share_id, ts, False, "password_required")
                    return None
                expected = share.password_hash
                actual = self._hash_password(password)
                if not hmac.compare_digest(expected, actual):
                    self._record(share_id, ts, False, "wrong_password")
                    return None
            share.use_count += 1
            self._record(share_id, ts, True, None)
            return share

    def verify_password(self, share_id: str, password: str) -> bool:
        """Check whether ``password`` matches the share's stored hash."""

        with self._lock:
            share = self._shares.get(share_id)
            if share is None or share.password_hash is None:
                return False
            actual = self._hash_password(password)
            return hmac.compare_digest(share.password_hash, actual)

    # ------------------------------------------------------------------
    # read-only API
    # ------------------------------------------------------------------
    def get_share(self, share_id: str) -> Optional[ShareLink]:
        with self._lock:
            return self._shares.get(share_id)

    def get_by_token(self, token: str) -> Optional[ShareLink]:
        with self._lock:
            share_id = self._by_token.get(token)
            if share_id is None:
                return None
            return self._shares.get(share_id)

    def status_of(self, share_id: str, now: float = 0.0) -> Optional[ShareStatus]:
        ts = _resolve_now(now)
        with self._lock:
            share = self._shares.get(share_id)
            if share is None:
                return None
            return self._status_locked(share, ts)

    def shares_for_doc(self, doc_id: str) -> list[ShareLink]:
        with self._lock:
            return [s for s in self._shares.values() if s.doc_id == doc_id]

    def shares_by_creator(self, creator: str) -> list[ShareLink]:
        with self._lock:
            return [s for s in self._shares.values() if s.created_by == creator]

    def access_history(self, share_id: Optional[str] = None) -> list[AccessRecord]:
        with self._lock:
            if share_id is None:
                return list(self._history)
            return [r for r in self._history if r.share_id == share_id]

    # ------------------------------------------------------------------
    # lifecycle helpers
    # ------------------------------------------------------------------
    def cleanup_expired(self, now: float = 0.0) -> int:
        """Remove expired and exhausted shares from the store.

        Returns the number of shares removed. Revoked shares are kept so
        ``status_of`` continues to report ``REVOKED`` for them.
        """

        ts = _resolve_now(now)
        removed = 0
        with self._lock:
            for share_id in list(self._shares.keys()):
                share = self._shares[share_id]
                status = self._status_locked(share, ts)
                if status in (ShareStatus.EXPIRED, ShareStatus.EXHAUSTED):
                    del self._shares[share_id]
                    self._by_token.pop(share.token, None)
                    removed += 1
        return removed

    def extend_expiry(
        self,
        share_id: str,
        additional_seconds: float,
        now: float = 0.0,
    ) -> bool:
        """Push the expiry of a share forward by ``additional_seconds``.

        If the share has no expiry yet, it gets one anchored at ``now``.
        Returns False if the share is unknown or revoked.
        """

        ts = _resolve_now(now)
        with self._lock:
            share = self._shares.get(share_id)
            if share is None or share.revoked:
                return False
            base = share.expires_at if share.expires_at is not None else ts
            share.expires_at = base + additional_seconds
            return True

    def change_permission(self, share_id: str, permission: PermissionLevel) -> bool:
        with self._lock:
            share = self._shares.get(share_id)
            if share is None:
                return False
            share.permission = permission
            return True

    # ------------------------------------------------------------------
    # aggregates
    # ------------------------------------------------------------------
    def stats(self, now: float = 0.0) -> ShareStats:
        ts = _resolve_now(now)
        active = expired = revoked = exhausted = total_uses = 0
        with self._lock:
            for share in self._shares.values():
                total_uses += share.use_count
                status = self._status_locked(share, ts)
                if status is ShareStatus.ACTIVE:
                    active += 1
                elif status is ShareStatus.EXPIRED:
                    expired += 1
                elif status is ShareStatus.REVOKED:
                    revoked += 1
                elif status is ShareStatus.EXHAUSTED:
                    exhausted += 1
            total = len(self._shares)
        return ShareStats(
            total_shares=total,
            active=active,
            expired=expired,
            revoked=revoked,
            exhausted=exhausted,
            total_uses=total_uses,
        )

    @property
    def total_shares(self) -> int:
        with self._lock:
            return len(self._shares)

    def clear(self) -> None:
        with self._lock:
            self._shares.clear()
            self._by_token.clear()
            self._history.clear()
