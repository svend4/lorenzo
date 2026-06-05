"""doc_snapshot_manager — point-in-time document snapshots with diff and restore (E291)."""

from docstoolkit.doc_snapshot_manager.manager import (
    Snapshot,
    SnapshotDiff,
    SnapshotStats,
    DocSnapshotManager,
)

__all__ = [
    "Snapshot",
    "SnapshotDiff",
    "SnapshotStats",
    "DocSnapshotManager",
]
