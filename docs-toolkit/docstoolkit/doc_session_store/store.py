"""E334 DocSessionStore — user editing session tracking implementation.

Tracks editing sessions per user/document, supports idle expiration,
concurrent editor detection, and aggregate statistics. Thread-safe.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Session:
    """A single editing session."""

    session_id: str
    user_id: str
    doc_id: str
    started_at: float = 0.0
    last_activity_at: float = 0.0
    ended_at: Optional[float] = None
    active: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class SessionStats:
    """Aggregate session statistics."""

    total_sessions: int
    active_sessions: int
    unique_users: int
    unique_docs: int


class DocSessionStore:
    """Thread-safe in-memory store of editing sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._by_user: dict[str, list[str]] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ utils
    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else float(now)

    # ----------------------------------------------------------------- start
    def start(
        self,
        user_id: str,
        doc_id: str,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> Session:
        """Create and register a new active session."""
        ts = self._now(now)
        session = Session(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            doc_id=doc_id,
            started_at=ts,
            last_activity_at=ts,
            ended_at=None,
            active=True,
            metadata=dict(metadata) if metadata else {},
        )
        with self._lock:
            self._sessions[session.session_id] = session
            self._by_user.setdefault(user_id, []).append(session.session_id)
            self._by_doc.setdefault(doc_id, []).append(session.session_id)
        return session

    # ----------------------------------------------------------------- touch
    def touch(self, session_id: str, now: Optional[float] = None) -> bool:
        """Update last_activity_at; return True if session exists and is active."""
        ts = self._now(now)
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None or not session.active:
                return False
            session.last_activity_at = ts
            return True

    # ------------------------------------------------------------------- end
    def end(self, session_id: str, now: Optional[float] = None) -> bool:
        """Mark session ended; return True if it was previously active."""
        ts = self._now(now)
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None or not session.active:
                return False
            session.active = False
            session.ended_at = ts
            return True

    # ------------------------------------------------------------------- get
    def get(self, session_id: str) -> Optional[Session]:
        with self._lock:
            return self._sessions.get(session_id)

    # ---------------------------------------------------------------- listing
    def _collect(self, ids: list[str], active_only: bool) -> list[Session]:
        result = []
        for sid in ids:
            s = self._sessions.get(sid)
            if s is None:
                continue
            if active_only and not s.active:
                continue
            result.append(s)
        result.sort(key=lambda s: s.started_at)
        return result

    def active_sessions_for_user(self, user_id: str) -> list[Session]:
        with self._lock:
            return self._collect(self._by_user.get(user_id, []), active_only=True)

    def active_sessions_for_doc(self, doc_id: str) -> list[Session]:
        with self._lock:
            return self._collect(self._by_doc.get(doc_id, []), active_only=True)

    def sessions_for_user(
        self, user_id: str, active_only: bool = False
    ) -> list[Session]:
        with self._lock:
            return self._collect(
                self._by_user.get(user_id, []), active_only=active_only
            )

    def sessions_for_doc(
        self, doc_id: str, active_only: bool = False
    ) -> list[Session]:
        with self._lock:
            return self._collect(
                self._by_doc.get(doc_id, []), active_only=active_only
            )

    # ---------------------------------------------------------- expire idle
    def expire_idle(
        self, timeout_seconds: float, now: Optional[float] = None
    ) -> int:
        """End active sessions idle longer than timeout. Return count expired."""
        ts = self._now(now)
        count = 0
        with self._lock:
            for session in self._sessions.values():
                if session.active and (ts - session.last_activity_at) > timeout_seconds:
                    session.active = False
                    session.ended_at = ts
                    count += 1
        return count

    # ----------------------------------------------------- concurrent editors
    def concurrent_editors(self, doc_id: str) -> list[str]:
        """Return sorted unique user IDs with active sessions on this doc."""
        with self._lock:
            users = set()
            for sid in self._by_doc.get(doc_id, []):
                s = self._sessions.get(sid)
                if s is not None and s.active:
                    users.add(s.user_id)
            return sorted(users)

    # --------------------------------------------------------- delete_session
    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            session = self._sessions.pop(session_id, None)
            if session is None:
                return False
            user_ids = self._by_user.get(session.user_id)
            if user_ids is not None:
                try:
                    user_ids.remove(session_id)
                except ValueError:
                    pass
                if not user_ids:
                    self._by_user.pop(session.user_id, None)
            doc_ids = self._by_doc.get(session.doc_id)
            if doc_ids is not None:
                try:
                    doc_ids.remove(session_id)
                except ValueError:
                    pass
                if not doc_ids:
                    self._by_doc.pop(session.doc_id, None)
            return True

    # ------------------------------------------------------------- clear_user
    def clear_user(self, user_id: str) -> int:
        """Delete all sessions for user; return count deleted."""
        with self._lock:
            session_ids = list(self._by_user.get(user_id, []))
        count = 0
        for sid in session_ids:
            if self.delete_session(sid):
                count += 1
        return count

    # ------------------------------------------------------------ all_doc_ids
    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return sorted({s.doc_id for s in self._sessions.values()})

    # ----------------------------------------------------------------- stats
    def stats(self) -> SessionStats:
        with self._lock:
            total = len(self._sessions)
            active = sum(1 for s in self._sessions.values() if s.active)
            users = {s.user_id for s in self._sessions.values()}
            docs = {s.doc_id for s in self._sessions.values()}
            return SessionStats(
                total_sessions=total,
                active_sessions=active,
                unique_users=len(users),
                unique_docs=len(docs),
            )
