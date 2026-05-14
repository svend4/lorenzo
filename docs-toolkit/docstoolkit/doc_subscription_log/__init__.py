"""E426 DocSubscriptionLog — append-only log of subscription lifecycle events.

Public API
----------
:class:`SubLogEntry`        — a single log entry
:class:`SubLogStats`        — aggregate statistics
:class:`DocSubscriptionLog` — main interface for subscription log
"""

from .log import SubLogEntry, SubLogStats, DocSubscriptionLog

__all__ = ["SubLogEntry", "SubLogStats", "DocSubscriptionLog"]
