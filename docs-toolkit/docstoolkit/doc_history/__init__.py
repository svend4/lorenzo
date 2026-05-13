"""Undo/redo-style history for document edits with snapshot management."""
from docstoolkit.doc_history.history import (
    DocHistory,
    Edit,
    EditType,
    DocSnapshot,
    HistoryStats,
)

__all__ = [
    "DocHistory",
    "Edit",
    "EditType",
    "DocSnapshot",
    "HistoryStats",
]
