"""E418 DocStateDiff — diff document state snapshots field-by-field.

Public API
----------
:class:`FieldChange`     — a single field change
:class:`StateDiffResult` — full diff of two state dicts
:class:`DiffStats`       — aggregate statistics
:class:`DocStateDiff`    — main interface for state diff
"""

from .diff import FieldChange, StateDiffResult, DiffStats, DocStateDiff

__all__ = ["FieldChange", "StateDiffResult", "DiffStats", "DocStateDiff"]
