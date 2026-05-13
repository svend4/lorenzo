"""Session manager module for docs-toolkit.

Provides SQLite-backed session lifecycle management with TTL support.

Example usage::

    from docstoolkit.session_mgr import SessionManager

    mgr = SessionManager()
    session = mgr.create_session("alice", data={"role": "editor"}, ttl=1800)
    s = mgr.get_session(session.session_id)
    mgr.refresh_session(session.session_id)
    mgr.destroy_session(session.session_id)
"""

from docstoolkit.session_mgr.session import Session, SessionStatus
from docstoolkit.session_mgr.store import SessionStore
from docstoolkit.session_mgr.manager import SessionManager

__all__ = [
    "Session",
    "SessionStatus",
    "SessionStore",
    "SessionManager",
]
