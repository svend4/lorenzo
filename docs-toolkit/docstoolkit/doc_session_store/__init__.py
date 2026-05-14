"""E334 DocSessionStore — user editing session tracking for documents.

Public API
----------
:class:`Session`        — a single editing session
:class:`SessionStats`   — aggregate statistics
:class:`DocSessionStore` — main interface for session management
"""

from .store import Session, SessionStats, DocSessionStore

__all__ = ["Session", "SessionStats", "DocSessionStore"]
