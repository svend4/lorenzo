"""Document edit history with undo/redo and snapshots.

Tracks edits per-document in two stacks (applied/undone), supports max history
limits, full-content snapshots with restore, and unified diffs across edits.
Thread-safe.
"""
from __future__ import annotations

import difflib
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EditType(Enum):
    """Type of document edit."""

    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"
    FORMAT = "format"
    RENAME = "rename"


@dataclass
class Edit:
    """A single recorded edit on a document."""

    edit_id: int
    doc_id: str
    edit_type: EditType
    before: str
    after: str
    timestamp: float
    author: Optional[str] = None
    description: Optional[str] = None


@dataclass
class DocSnapshot:
    """Full content snapshot of a document at a point in time."""

    snapshot_id: int
    doc_id: str
    content: str
    timestamp: float
    label: Optional[str] = None


@dataclass
class HistoryStats:
    """Aggregate statistics about recorded history."""

    total_edits: int
    total_snapshots: int
    edits_per_doc: dict = field(default_factory=dict)
    can_undo_count: int = 0


class DocHistory:
    """Undo/redo history manager for document edits."""

    def __init__(self, max_history: int = 100):
        if max_history <= 0:
            raise ValueError("max_history must be positive")
        self.max_history = max_history
        self._lock = threading.Lock()
        # doc_id -> {"applied": list[Edit], "undone": list[Edit]}
        self._docs: dict = {}
        self._snapshots: dict = {}  # snapshot_id -> DocSnapshot
        self._edit_counter = 0
        self._snapshot_counter = 0
        self._total_edits_recorded = 0

    # ------------------------------------------------------------------ utils
    def _doc_bucket(self, doc_id: str) -> dict:
        if doc_id not in self._docs:
            self._docs[doc_id] = {"applied": [], "undone": []}
        return self._docs[doc_id]

    # ------------------------------------------------------------------ record
    def record(
        self,
        doc_id: str,
        edit_type: EditType,
        before: str,
        after: str,
        author: Optional[str] = None,
        description: Optional[str] = None,
        now: float = 0.0,
    ) -> Edit:
        """Record a new edit, clearing the redo stack for that document."""
        with self._lock:
            self._edit_counter += 1
            self._total_edits_recorded += 1
            edit = Edit(
                edit_id=self._edit_counter,
                doc_id=doc_id,
                edit_type=edit_type,
                before=before,
                after=after,
                timestamp=now,
                author=author,
                description=description,
            )
            bucket = self._doc_bucket(doc_id)
            bucket["applied"].append(edit)
            bucket["undone"].clear()
            # Enforce max_history on applied stack: drop oldest
            while len(bucket["applied"]) > self.max_history:
                bucket["applied"].pop(0)
            return edit

    # ------------------------------------------------------------------ undo/redo
    def undo(self, doc_id: str) -> Optional[Edit]:
        """Undo the last applied edit on a doc. Returns the moved edit."""
        with self._lock:
            if doc_id not in self._docs:
                return None
            bucket = self._docs[doc_id]
            if not bucket["applied"]:
                return None
            edit = bucket["applied"].pop()
            bucket["undone"].append(edit)
            return edit

    def redo(self, doc_id: str) -> Optional[Edit]:
        """Redo the last undone edit on a doc. Returns the re-applied edit."""
        with self._lock:
            if doc_id not in self._docs:
                return None
            bucket = self._docs[doc_id]
            if not bucket["undone"]:
                return None
            edit = bucket["undone"].pop()
            bucket["applied"].append(edit)
            return edit

    def can_undo(self, doc_id: str) -> bool:
        with self._lock:
            return doc_id in self._docs and len(self._docs[doc_id]["applied"]) > 0

    def can_redo(self, doc_id: str) -> bool:
        with self._lock:
            return doc_id in self._docs and len(self._docs[doc_id]["undone"]) > 0

    # ------------------------------------------------------------------ inspect
    def history(self, doc_id: str, limit: Optional[int] = None) -> list:
        """Return applied edits newest-first."""
        with self._lock:
            if doc_id not in self._docs:
                return []
            applied = list(reversed(self._docs[doc_id]["applied"]))
            if limit is not None:
                applied = applied[:limit]
            return applied

    def current_content(self, doc_id: str) -> Optional[str]:
        """Return current content of doc: 'after' of last applied edit, or None."""
        with self._lock:
            if doc_id not in self._docs:
                return None
            applied = self._docs[doc_id]["applied"]
            if not applied:
                # No applied edits — fall back to 'before' of last undone, if any
                undone = self._docs[doc_id]["undone"]
                if undone:
                    return undone[-1].before
                return None
            return applied[-1].after

    # ------------------------------------------------------------------ snapshots
    def take_snapshot(
        self,
        doc_id: str,
        content: str,
        label: Optional[str] = None,
        now: float = 0.0,
    ) -> DocSnapshot:
        with self._lock:
            self._snapshot_counter += 1
            snap = DocSnapshot(
                snapshot_id=self._snapshot_counter,
                doc_id=doc_id,
                content=content,
                timestamp=now,
                label=label,
            )
            self._snapshots[snap.snapshot_id] = snap
            return snap

    def restore_snapshot(self, snapshot_id: int) -> Optional[str]:
        """Restore content from snapshot. Clears redo stack of that doc.

        Returns the snapshot content (so caller can apply it).
        """
        with self._lock:
            snap = self._snapshots.get(snapshot_id)
            if snap is None:
                return None
            bucket = self._doc_bucket(snap.doc_id)
            bucket["undone"].clear()
            return snap.content

    def list_snapshots(self, doc_id: str) -> list:
        with self._lock:
            return [
                s for s in self._snapshots.values() if s.doc_id == doc_id
            ]

    def delete_snapshot(self, snapshot_id: int) -> bool:
        with self._lock:
            if snapshot_id in self._snapshots:
                del self._snapshots[snapshot_id]
                return True
            return False

    # ------------------------------------------------------------------ diff
    def diff_edits(self, doc_id: str, from_edit: int, to_edit: int) -> str:
        """Unified diff between two edits' content states.

        Uses 'before' of from_edit and 'after' of to_edit (within the doc).
        Returns empty string if either edit_id not found in the doc's history.
        """
        with self._lock:
            if doc_id not in self._docs:
                return ""
            # Look in both applied + undone for that doc
            all_edits = (
                self._docs[doc_id]["applied"] + self._docs[doc_id]["undone"]
            )
            by_id = {e.edit_id: e for e in all_edits}
            a = by_id.get(from_edit)
            b = by_id.get(to_edit)
            if a is None or b is None:
                return ""
            left = a.before.splitlines(keepends=True)
            right = b.after.splitlines(keepends=True)
            diff = difflib.unified_diff(
                left,
                right,
                fromfile=f"edit-{from_edit}-before",
                tofile=f"edit-{to_edit}-after",
                lineterm="",
            )
            return "\n".join(diff)

    # ------------------------------------------------------------------ stats
    def stats(self) -> HistoryStats:
        with self._lock:
            edits_per_doc = {}
            can_undo_count = 0
            total_edits = 0
            for doc_id, bucket in self._docs.items():
                n = len(bucket["applied"])
                # count both applied + undone as known edits per doc
                count = n + len(bucket["undone"])
                edits_per_doc[doc_id] = count
                total_edits += count
                can_undo_count += n
            return HistoryStats(
                total_edits=total_edits,
                total_snapshots=len(self._snapshots),
                edits_per_doc=edits_per_doc,
                can_undo_count=can_undo_count,
            )

    # ------------------------------------------------------------------ clear
    def clear(self, doc_id: Optional[str] = None) -> int:
        """Clear history. If doc_id is None, clears all docs (not snapshots).

        Returns the number of edits cleared.
        """
        with self._lock:
            if doc_id is None:
                removed = 0
                for bucket in self._docs.values():
                    removed += len(bucket["applied"]) + len(bucket["undone"])
                self._docs.clear()
                return removed
            if doc_id not in self._docs:
                return 0
            bucket = self._docs[doc_id]
            removed = len(bucket["applied"]) + len(bucket["undone"])
            del self._docs[doc_id]
            return removed

    # ------------------------------------------------------------------ properties
    @property
    def total_edits(self) -> int:
        """Number of edits currently retained across all docs."""
        with self._lock:
            total = 0
            for bucket in self._docs.values():
                total += len(bucket["applied"]) + len(bucket["undone"])
            return total
