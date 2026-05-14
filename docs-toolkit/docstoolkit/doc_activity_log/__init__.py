"""E304 DocActivityLog — append-only activity log for document operations.

Public API
----------
:class:`ActivityEntry`  — a single logged activity event
:class:`ActivityStats`  — aggregate statistics
:class:`DocActivityLog` — main interface for logging and querying activity
"""

from .log import ActivityEntry, ActivityStats, DocActivityLog

__all__ = ["ActivityEntry", "ActivityStats", "DocActivityLog"]
