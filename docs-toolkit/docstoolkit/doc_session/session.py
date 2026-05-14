"""Doc session: user session management with activity tracking, timeouts, and roles."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4


class SessionStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: float
    last_activity: float
    expires_at: float
    status: SessionStatus = SessionStatus.ACTIVE
    data: dict = field(default_factory=dict)
    roles: set = field(default_factory=set)


@dataclass
class SessionStats:
    total: int
    active: int
    idle: int
    expired: int
    revoked: int
    unique_users: int


class DocSession:
    """User session manager.

    Provides session lifecycle management, activity tracking,
    role-based access tagging, and dynamic status computation.
    """

    def __init__(self, default_ttl: float = 3600, idle_after: float = 900):
        self.default_ttl = default_ttl
        self.idle_after = idle_after
        self._sessions: dict[str, Session] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _compute_status(self, sess: Session, now: float) -> SessionStatus:
        """Compute dynamic status. Does not modify stored status if REVOKED."""
        if sess.status == SessionStatus.REVOKED:
            return SessionStatus.REVOKED
        if now >= sess.expires_at:
            return SessionStatus.EXPIRED
        if now - sess.last_activity >= self.idle_after:
            return SessionStatus.IDLE
        return SessionStatus.ACTIVE

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------
    def create(
        self,
        user_id: str,
        ttl: float = None,
        roles: set = None,
        data: dict = None,
        now: float = 0.0,
    ) -> Session:
        """Create a new session for a user."""
        with self._lock:
            session_id = uuid4().hex
            effective_ttl = ttl if ttl is not None else self.default_ttl
            sess = Session(
                session_id=session_id,
                user_id=user_id,
                created_at=now,
                last_activity=now,
                expires_at=now + effective_ttl,
                status=SessionStatus.ACTIVE,
                data=dict(data) if data else {},
                roles=set(roles) if roles else set(),
            )
            self._sessions[session_id] = sess
            return sess

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------
    def get(self, session_id: str, now: float = 0.0) -> Optional[Session]:
        """Get session; update last_activity if currently ACTIVE/IDLE.

        Status is computed dynamically. Returns None if not found.
        """
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return None
            status = self._compute_status(sess, now)
            sess.status = status
            if status in (SessionStatus.ACTIVE, SessionStatus.IDLE):
                sess.last_activity = now
                # Recompute (may go from IDLE back to ACTIVE)
                sess.status = self._compute_status(sess, now)
            return sess

    def peek(self, session_id: str, now: float = 0.0) -> Optional[Session]:
        """Like get(), but does not update last_activity."""
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return None
            sess.status = self._compute_status(sess, now)
            return sess

    # ------------------------------------------------------------------
    # Activity / state changes
    # ------------------------------------------------------------------
    def touch(self, session_id: str, now: float = 0.0) -> bool:
        """Update last_activity for an existing, non-revoked, non-expired session."""
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            if sess.status == SessionStatus.REVOKED:
                return False
            if now >= sess.expires_at:
                sess.status = SessionStatus.EXPIRED
                return False
            sess.last_activity = now
            sess.status = self._compute_status(sess, now)
            return True

    def revoke(self, session_id: str, now: float = 0.0) -> bool:
        """Mark session as revoked."""
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            if sess.status == SessionStatus.REVOKED:
                return False
            sess.status = SessionStatus.REVOKED
            return True

    def revoke_user(self, user_id: str, now: float = 0.0) -> int:
        """Revoke all sessions for a user. Returns count of revoked."""
        with self._lock:
            count = 0
            for sess in self._sessions.values():
                if sess.user_id == user_id and sess.status != SessionStatus.REVOKED:
                    sess.status = SessionStatus.REVOKED
                    count += 1
            return count

    def extend(
        self, session_id: str, additional_ttl: float, now: float = 0.0
    ) -> bool:
        """Extend session expiration by additional_ttl. Only for non-revoked,
        non-expired sessions."""
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            if sess.status == SessionStatus.REVOKED:
                return False
            if now >= sess.expires_at:
                sess.status = SessionStatus.EXPIRED
                return False
            sess.expires_at += additional_ttl
            return True

    def update_data(self, session_id: str, updates: dict) -> bool:
        """Merge updates into session data dict."""
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            if sess.status == SessionStatus.REVOKED:
                return False
            sess.data.update(updates)
            return True

    # ------------------------------------------------------------------
    # Roles
    # ------------------------------------------------------------------
    def add_role(self, session_id: str, role: str) -> bool:
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            if sess.status == SessionStatus.REVOKED:
                return False
            sess.roles.add(role)
            return True

    def remove_role(self, session_id: str, role: str) -> bool:
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            if sess.status == SessionStatus.REVOKED:
                return False
            if role not in sess.roles:
                return False
            sess.roles.discard(role)
            return True

    def has_role(self, session_id: str, role: str) -> bool:
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                return False
            return role in sess.roles

    # ------------------------------------------------------------------
    # Listing / filtering
    # ------------------------------------------------------------------
    def sessions_for_user(self, user_id: str, now: float = 0.0) -> list:
        with self._lock:
            result = []
            for sess in self._sessions.values():
                if sess.user_id == user_id:
                    sess.status = self._compute_status(sess, now)
                    result.append(sess)
            return result

    def active_sessions(self, now: float = 0.0) -> list:
        with self._lock:
            result = []
            for sess in self._sessions.values():
                sess.status = self._compute_status(sess, now)
                if sess.status == SessionStatus.ACTIVE:
                    result.append(sess)
            return result

    def idle_sessions(self, now: float = 0.0) -> list:
        with self._lock:
            result = []
            for sess in self._sessions.values():
                sess.status = self._compute_status(sess, now)
                if sess.status == SessionStatus.IDLE:
                    result.append(sess)
            return result

    def expired_sessions(self, now: float = 0.0) -> list:
        with self._lock:
            result = []
            for sess in self._sessions.values():
                sess.status = self._compute_status(sess, now)
                if sess.status == SessionStatus.EXPIRED:
                    result.append(sess)
            return result

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------
    def cleanup_expired(self, now: float = 0.0) -> int:
        """Remove EXPIRED sessions from storage. Returns count removed."""
        with self._lock:
            to_remove = []
            for sid, sess in self._sessions.items():
                if sess.status == SessionStatus.REVOKED:
                    continue
                if now >= sess.expires_at:
                    to_remove.append(sid)
            for sid in to_remove:
                del self._sessions[sid]
            return len(to_remove)

    def stats(self, now: float = 0.0) -> SessionStats:
        with self._lock:
            total = len(self._sessions)
            active = idle = expired = revoked = 0
            users = set()
            for sess in self._sessions.values():
                sess.status = self._compute_status(sess, now)
                users.add(sess.user_id)
                if sess.status == SessionStatus.ACTIVE:
                    active += 1
                elif sess.status == SessionStatus.IDLE:
                    idle += 1
                elif sess.status == SessionStatus.EXPIRED:
                    expired += 1
                elif sess.status == SessionStatus.REVOKED:
                    revoked += 1
            return SessionStats(
                total=total,
                active=active,
                idle=idle,
                expired=expired,
                revoked=revoked,
                unique_users=len(users),
            )

    def session_count(self, now: float = 0.0) -> int:
        """Count of currently ACTIVE sessions."""
        with self._lock:
            count = 0
            for sess in self._sessions.values():
                sess.status = self._compute_status(sess, now)
                if sess.status == SessionStatus.ACTIVE:
                    count += 1
            return count

    @property
    def total_sessions(self) -> int:
        with self._lock:
            return len(self._sessions)

    def clear(self) -> None:
        with self._lock:
            self._sessions.clear()
