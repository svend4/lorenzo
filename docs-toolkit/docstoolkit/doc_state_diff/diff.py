"""E418 DocStateDiff — diff document state snapshots field-by-field.

Thread-safe via ``threading.Lock``; stdlib only; dataclasses throughout.
"""
from __future__ import annotations

import copy
import threading
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class FieldChange:
    """A single field-level change between two state snapshots."""

    field_name: str
    change_type: str  # "added", "removed", "modified"
    old_value: object = None
    new_value: object = None


@dataclass
class StateDiffResult:
    """Full field-by-field diff between two document state snapshots."""

    doc_id: str
    from_version: str
    to_version: str
    changes: list[FieldChange] = field(default_factory=list)
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0


@dataclass
class DiffStats:
    """Aggregate statistics about all stored diffs."""

    total_diffs: int
    total_field_changes: int
    unique_docs: int


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------


class DocStateDiff:
    """Stores document state snapshots and computes field-by-field diffs.

    Each state is identified by ``(doc_id, version)``. Diffs are computed
    on demand and optionally cached by ``(doc_id, from_version, to_version)``.

    Thread-safe: all public operations are guarded by an internal lock.
    """

    def __init__(self) -> None:
        self._states: dict[tuple, dict] = {}
        self._diffs: dict[tuple, StateDiffResult] = {}
        self._lock = threading.Lock()

    # ----- state storage --------------------------------------------------

    def store_state(self, doc_id: str, version: str, state: dict) -> None:
        """Store a state snapshot. The state dict is deep-copied to prevent
        external mutation from affecting cached values."""
        with self._lock:
            self._states[(doc_id, version)] = copy.deepcopy(state)

    def get_state(self, doc_id: str, version: str) -> Optional[dict]:
        """Return a deep copy of the stored state, or ``None`` if absent."""
        with self._lock:
            st = self._states.get((doc_id, version))
            if st is None:
                return None
            return copy.deepcopy(st)

    def delete_state(self, doc_id: str, version: str) -> bool:
        """Delete a stored state. Returns ``True`` if it existed."""
        with self._lock:
            key = (doc_id, version)
            if key in self._states:
                del self._states[key]
                return True
            return False

    # ----- diff computation ----------------------------------------------

    def compute_diff(
        self,
        doc_id: str,
        from_version: str,
        to_version: str,
        cache: bool = True,
    ) -> Optional[StateDiffResult]:
        """Compute a field-by-field diff between two state snapshots.

        Returns ``None`` if either state is missing. The result is cached
        when ``cache=True``.
        """
        with self._lock:
            old = self._states.get((doc_id, from_version))
            new = self._states.get((doc_id, to_version))
            if old is None or new is None:
                return None

            changes: list[FieldChange] = []
            added = 0
            removed = 0
            modified = 0

            all_keys = set(old.keys()) | set(new.keys())
            for key in sorted(all_keys):
                in_old = key in old
                in_new = key in new
                if in_new and not in_old:
                    changes.append(
                        FieldChange(
                            field_name=key,
                            change_type="added",
                            old_value=None,
                            new_value=copy.deepcopy(new[key]),
                        )
                    )
                    added += 1
                elif in_old and not in_new:
                    changes.append(
                        FieldChange(
                            field_name=key,
                            change_type="removed",
                            old_value=copy.deepcopy(old[key]),
                            new_value=None,
                        )
                    )
                    removed += 1
                else:
                    if old[key] != new[key]:
                        changes.append(
                            FieldChange(
                                field_name=key,
                                change_type="modified",
                                old_value=copy.deepcopy(old[key]),
                                new_value=copy.deepcopy(new[key]),
                            )
                        )
                        modified += 1

            result = StateDiffResult(
                doc_id=doc_id,
                from_version=from_version,
                to_version=to_version,
                changes=changes,
                added_count=added,
                removed_count=removed,
                modified_count=modified,
            )
            if cache:
                self._diffs[(doc_id, from_version, to_version)] = result
            return result

    def get_cached(
        self,
        doc_id: str,
        from_version: str,
        to_version: str,
    ) -> Optional[StateDiffResult]:
        """Return cached diff or ``None`` if not cached."""
        with self._lock:
            return self._diffs.get((doc_id, from_version, to_version))

    def invalidate_cache(self, doc_id: Optional[str] = None) -> int:
        """Drop cached diffs.

        If ``doc_id`` is ``None``, clear all cached diffs. Otherwise drop
        only entries for the given document. Returns the number removed.
        """
        with self._lock:
            if doc_id is None:
                n = len(self._diffs)
                self._diffs.clear()
                return n
            to_drop = [k for k in self._diffs if k[0] == doc_id]
            for k in to_drop:
                del self._diffs[k]
            return len(to_drop)

    # ----- enumeration ----------------------------------------------------

    def versions_for(self, doc_id: str) -> list[str]:
        """Return all stored versions for ``doc_id`` sorted lexicographically."""
        with self._lock:
            return sorted(v for (d, v) in self._states if d == doc_id)

    def all_doc_ids(self) -> list[str]:
        """Return all known document ids sorted lexicographically."""
        with self._lock:
            return sorted({d for (d, _v) in self._states})

    # ----- patch / merge --------------------------------------------------

    def apply_diff(self, state: dict, diff: StateDiffResult) -> dict:
        """Apply ``diff`` to a deep copy of ``state`` and return the result.

        - ``added`` and ``modified`` entries set the new value.
        - ``removed`` entries delete the key (if present).
        """
        result = copy.deepcopy(state)
        for change in diff.changes:
            if change.change_type in ("added", "modified"):
                result[change.field_name] = copy.deepcopy(change.new_value)
            elif change.change_type == "removed":
                if change.field_name in result:
                    del result[change.field_name]
        return result

    def merge_states(
        self,
        state_a: dict,
        state_b: dict,
        prefer: str = "b",
    ) -> dict:
        """Merge two state dicts. ``prefer`` chooses the winner on conflicts.

        ``prefer="b"`` (default) — values from ``state_b`` win.
        ``prefer="a"`` — values from ``state_a`` win.
        """
        if prefer not in ("a", "b"):
            raise ValueError("prefer must be 'a' or 'b'")
        result: dict = {}
        if prefer == "b":
            for k, v in state_a.items():
                result[k] = copy.deepcopy(v)
            for k, v in state_b.items():
                result[k] = copy.deepcopy(v)
        else:
            for k, v in state_b.items():
                result[k] = copy.deepcopy(v)
            for k, v in state_a.items():
                result[k] = copy.deepcopy(v)
        return result

    # ----- bulk ops -------------------------------------------------------

    def clear_all(self) -> int:
        """Drop every stored state and cached diff. Returns number cleared."""
        with self._lock:
            n = len(self._states) + len(self._diffs)
            self._states.clear()
            self._diffs.clear()
            return n

    def stats(self) -> DiffStats:
        """Return aggregate statistics over cached diffs and stored states."""
        with self._lock:
            total_diffs = len(self._diffs)
            total_field_changes = sum(
                len(d.changes) for d in self._diffs.values()
            )
            unique_docs = len({d for (d, _v) in self._states})
            return DiffStats(
                total_diffs=total_diffs,
                total_field_changes=total_field_changes,
                unique_docs=unique_docs,
            )
