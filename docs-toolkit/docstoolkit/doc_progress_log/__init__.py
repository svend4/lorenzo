"""E371 DocProgressLog — incremental progress log for document operations.

Public API
----------
:class:`ProgressEntry`    — a single progress data point
:class:`ProgressSummary`  — summary for a specific operation
:class:`ProgressStats`    — aggregate statistics
:class:`DocProgressLog`   — main interface for progress logging
"""

from .log import ProgressEntry, ProgressSummary, ProgressStats, DocProgressLog

__all__ = ["ProgressEntry", "ProgressSummary", "ProgressStats", "DocProgressLog"]
