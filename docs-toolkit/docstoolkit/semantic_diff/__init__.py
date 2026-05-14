"""Semantic diff — sentence-, paragraph-, and word-level semantic diffing.

Pure stdlib. No external dependencies.

Public API
----------
DiffType        — enum of change categories
DiffChunk       — single diff unit with similarity score
SemanticDiffer  — low-level differ (sentences / paragraphs / words)
DiffStats       — aggregate statistics for a diff
DiffReport      — full report with chunks + stats + markdown rendering
DiffReporter    — high-level facade: report() and compare_sections()
"""
from docstoolkit.semantic_diff.diff import (
    DiffChunk,
    DiffType,
    SemanticDiffer,
)
from docstoolkit.semantic_diff.report import (
    DiffReport,
    DiffReporter,
    DiffStats,
)

__all__ = [
    "DiffChunk",
    "DiffType",
    "SemanticDiffer",
    "DiffReport",
    "DiffReporter",
    "DiffStats",
]
