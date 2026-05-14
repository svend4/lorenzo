"""E322 DocDiffEngine — compute and store document diffs.

Public API
----------
:class:`DiffLine`     — a single diff line with operation
:class:`DiffResult`   — full diff between two versions
:class:`DiffStats`    — aggregate statistics
:class:`DocDiffEngine` — main interface for diff computation
"""

from .engine import DiffLine, DiffResult, DiffStats, DocDiffEngine

__all__ = ["DiffLine", "DiffResult", "DiffStats", "DocDiffEngine"]
