"""High-level SessionManager that wraps SessionStore."""

from __future__ import annotations

from docstoolkit.session_mgr.session import Session
from docstoolkit.session_mgr.store import SessionStore


class SessionManager:
    """Convenience façade over :class:`SessionStore`.

    If no *store* is provided, an in-memory SQLite store is created
    automatically.
    """

    def __init__(self, store: SessionStore = None) -> None:
        self._store = store if store is not None else SessionStore()

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def create_session(
        self,
        user_id: str,
        data: dict = None,
        ttl: float = None,
    ) -> Session:
        """Create a new session for *user_id*."""
        return self._store.create(user_id, data=data, ttl=ttl)

    def get_session(self, session_id: str) -> Session | None:
        """Return the session, or ``None`` if not found / expired."""
        return self._store.get(session_id)

    def refresh_session(self, session_id: str) -> bool:
        """Touch the session, updating last_accessed.

        Returns ``False`` if the session does not exist or is expired.
        """
        return self._store.touch(session_id)

    def destroy_session(self, session_id: str) -> bool:
        """Invalidate the session.

        Returns ``False`` if the session does not exist.
        """
        return self._store.invalidate(session_id)

    def user_sessions(self, user_id: str) -> list[Session]:
        """Return all active sessions for *user_id*."""
        return self._store.active_for_user(user_id)

    def cleanup(self) -> int:
        """Delete expired and invalidated sessions; return count removed."""
        return self._store.cleanup()
