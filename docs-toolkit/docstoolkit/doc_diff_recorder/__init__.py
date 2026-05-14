"""E390 DocDiffRecorder — record per-edit diffs with metadata.

Public API
----------
:class:`DiffRecord`       — a single recorded diff
:class:`DiffRecorderStats` — aggregate statistics
:class:`DocDiffRecorder`  — main interface for diff recording
"""

from .recorder import DiffRecord, DiffRecorderStats, DocDiffRecorder

__all__ = ["DiffRecord", "DiffRecorderStats", "DocDiffRecorder"]
