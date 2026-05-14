"""Doc session module (E232).

User session management with activity tracking, timeouts, and roles.

Usage:
    from docstoolkit.doc_session import DocSession, Session, SessionStatus, SessionStats

    mgr = DocSession(default_ttl=3600, idle_after=900)
    sess = mgr.create(user_id="alice", now=1000.0)
    mgr.add_role(sess.session_id, "admin")
    fetched = mgr.get(sess.session_id, now=1100.0)
"""
from docstoolkit.doc_session.session import (
    DocSession,
    Session,
    SessionStats,
    SessionStatus,
)

__all__ = [
    "DocSession",
    "Session",
    "SessionStats",
    "SessionStatus",
]
