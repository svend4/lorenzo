"""Doc merger — merge multiple documents intelligently.

Pure stdlib. No external dependencies.

Public API
----------
MergeStrategy   — enum of merge strategies
MergeConflict   — single conflict between document versions
MergeResult     — merged document with metadata
DocMerger       — high-level merging facade
"""
from docstoolkit.doc_merger.merger import (
    DocMerger,
    MergeConflict,
    MergeResult,
    MergeStrategy,
)

__all__ = [
    "DocMerger",
    "MergeConflict",
    "MergeResult",
    "MergeStrategy",
]
