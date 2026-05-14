"""E332 DocChangeHistory — granular change history with diff entries.

Public API
----------
:class:`ChangeEntry`       — a single change record
:class:`ChangeHistoryStats` — aggregate statistics
:class:`DocChangeHistory`  — main interface for change history management
"""

from .history import ChangeEntry, ChangeHistoryStats, DocChangeHistory

__all__ = ["ChangeEntry", "ChangeHistoryStats", "DocChangeHistory"]
