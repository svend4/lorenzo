"""System snapshot: capture, store, diff, and restore corpus state."""
from docstoolkit.snapshot.capture import SnapshotCapture, CapturedState
from docstoolkit.snapshot.store import SnapshotStore, SnapshotMeta
from docstoolkit.snapshot.diff import SnapshotDiff, diff_snapshots

__all__ = [
    "SnapshotCapture", "CapturedState",
    "SnapshotStore", "SnapshotMeta",
    "SnapshotDiff", "diff_snapshots",
]
