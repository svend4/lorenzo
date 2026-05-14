"""E399 DocStatusHistory — track status changes over time for documents.

Public API
----------
:class:`StatusChange`     — a single status change record
:class:`StatusStats`      — aggregate statistics
:class:`DocStatusHistory` — main interface for status history
"""

from .history import StatusChange, StatusStats, DocStatusHistory

__all__ = ["StatusChange", "StatusStats", "DocStatusHistory"]
