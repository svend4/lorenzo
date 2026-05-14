"""Field-by-field diff between two document dicts.

Supports nested dicts, lists (by index), type-change detection, and patch
application. Stdlib only.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ChangeKind(Enum):
    """Kind of change for a single field."""

    ADDED = "ADDED"
    REMOVED = "REMOVED"
    CHANGED = "CHANGED"
    UNCHANGED = "UNCHANGED"
    TYPE_CHANGED = "TYPE_CHANGED"


@dataclass
class FieldChange:
    """A single field-level change."""

    path: str  # dotted path, e.g. "metadata.author" or "tags[0]"
    kind: ChangeKind
    old_value: Any = None
    new_value: Any = None


@dataclass
class DiffSummary:
    """Aggregated summary of changes between two dicts."""

    total_changes: int = 0
    added_count: int = 0
    removed_count: int = 0
    changed_count: int = 0
    type_changed_count: int = 0
    unchanged_count: int = 0
    affected_paths: set[str] = field(default_factory=set)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _join(prefix: str, key: str) -> str:
    if not prefix:
        return key
    return f"{prefix}.{key}"


def _index_path(prefix: str, idx: int) -> str:
    return f"{prefix}[{idx}]"


def _parse_path(path: str) -> list[tuple[str, Any]]:
    """Parse a dotted path with optional list indices into segments.

    Returns list of tuples (kind, key) where kind is "key" or "index".
    """
    segments: list[tuple[str, Any]] = []
    if not path:
        return segments
    parts = path.split(".")
    for part in parts:
        # Could be "name" or "name[0]" or "name[0][1]"
        # Find first '['
        bracket = part.find("[")
        if bracket == -1:
            segments.append(("key", part))
        else:
            name = part[:bracket]
            if name:
                segments.append(("key", name))
            rest = part[bracket:]
            # Parse [i][j]...
            while rest:
                close = rest.find("]")
                if close == -1:
                    # malformed; treat rest as key
                    segments.append(("key", rest))
                    break
                idx_str = rest[1:close]
                try:
                    idx = int(idx_str)
                    segments.append(("index", idx))
                except ValueError:
                    segments.append(("key", idx_str))
                rest = rest[close + 1:]
    return segments


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class DocFieldDiff:
    """Computes field-by-field diff between two document dicts."""

    def __init__(self) -> None:  # pragma: no cover - trivial
        pass

    # ----- core diff -------------------------------------------------------

    def diff(
        self,
        old: dict,
        new: dict,
        include_unchanged: bool = False,
    ) -> list[FieldChange]:
        """Return list of field-level changes between old and new dicts."""
        changes = self.diff_value(old, new, path="")
        if not include_unchanged:
            changes = [c for c in changes if c.kind != ChangeKind.UNCHANGED]
        return changes

    def diff_value(
        self,
        old: Any,
        new: Any,
        path: str = "",
    ) -> list[FieldChange]:
        """Recursively diff two values at given path."""
        changes: list[FieldChange] = []

        # Both dicts: recurse by keys
        if isinstance(old, dict) and isinstance(new, dict):
            all_keys = list(old.keys())
            for k in new.keys():
                if k not in old:
                    all_keys.append(k)
            for key in all_keys:
                sub_path = _join(path, str(key))
                if key not in new:
                    changes.append(FieldChange(
                        path=sub_path,
                        kind=ChangeKind.REMOVED,
                        old_value=old[key],
                        new_value=None,
                    ))
                elif key not in old:
                    changes.append(FieldChange(
                        path=sub_path,
                        kind=ChangeKind.ADDED,
                        old_value=None,
                        new_value=new[key],
                    ))
                else:
                    changes.extend(self.diff_value(old[key], new[key], sub_path))
            return changes

        # Both lists: compare by index
        if isinstance(old, list) and isinstance(new, list):
            max_len = max(len(old), len(new))
            for i in range(max_len):
                sub_path = _index_path(path, i)
                if i >= len(new):
                    changes.append(FieldChange(
                        path=sub_path,
                        kind=ChangeKind.REMOVED,
                        old_value=old[i],
                        new_value=None,
                    ))
                elif i >= len(old):
                    changes.append(FieldChange(
                        path=sub_path,
                        kind=ChangeKind.ADDED,
                        old_value=None,
                        new_value=new[i],
                    ))
                else:
                    changes.extend(self.diff_value(old[i], new[i], sub_path))
            return changes

        # Type change: different concrete types (and not both dict/list)
        if type(old) is not type(new):
            changes.append(FieldChange(
                path=path,
                kind=ChangeKind.TYPE_CHANGED,
                old_value=old,
                new_value=new,
            ))
            return changes

        # Same primitive type
        if old == new:
            changes.append(FieldChange(
                path=path,
                kind=ChangeKind.UNCHANGED,
                old_value=old,
                new_value=new,
            ))
        else:
            changes.append(FieldChange(
                path=path,
                kind=ChangeKind.CHANGED,
                old_value=old,
                new_value=new,
            ))
        return changes

    # ----- queries ---------------------------------------------------------

    def is_equal(self, old: dict, new: dict, deep: bool = True) -> bool:
        """Check whether two dicts are equal.

        With deep=False, only top-level keys/values are compared (via ==).
        With deep=True, runs a full recursive diff and verifies no changes.
        """
        if not deep:
            return old == new
        changes = self.diff(old, new, include_unchanged=False)
        return len(changes) == 0

    def summary(self, old: dict, new: dict) -> DiffSummary:
        """Build aggregated summary of changes."""
        changes = self.diff(old, new, include_unchanged=True)
        s = DiffSummary()
        for c in changes:
            if c.kind == ChangeKind.ADDED:
                s.added_count += 1
                s.affected_paths.add(c.path)
            elif c.kind == ChangeKind.REMOVED:
                s.removed_count += 1
                s.affected_paths.add(c.path)
            elif c.kind == ChangeKind.CHANGED:
                s.changed_count += 1
                s.affected_paths.add(c.path)
            elif c.kind == ChangeKind.TYPE_CHANGED:
                s.type_changed_count += 1
                s.affected_paths.add(c.path)
            elif c.kind == ChangeKind.UNCHANGED:
                s.unchanged_count += 1
        s.total_changes = (
            s.added_count
            + s.removed_count
            + s.changed_count
            + s.type_changed_count
        )
        return s

    def added_fields(self, old: dict, new: dict) -> list[str]:
        return [c.path for c in self.diff(old, new) if c.kind == ChangeKind.ADDED]

    def removed_fields(self, old: dict, new: dict) -> list[str]:
        return [c.path for c in self.diff(old, new) if c.kind == ChangeKind.REMOVED]

    def changed_fields(self, old: dict, new: dict) -> list[str]:
        return [
            c.path
            for c in self.diff(old, new)
            if c.kind in (ChangeKind.CHANGED, ChangeKind.TYPE_CHANGED)
        ]

    def unchanged_fields(self, old: dict, new: dict) -> list[str]:
        return [
            c.path
            for c in self.diff(old, new, include_unchanged=True)
            if c.kind == ChangeKind.UNCHANGED
        ]

    # ----- path utilities --------------------------------------------------

    def get_value(self, data: dict, path: str, default: Any = None) -> Any:
        """Look up a value using a dotted path with optional [N] indices."""
        if not path:
            return data
        segments = _parse_path(path)
        cur: Any = data
        for kind, key in segments:
            if kind == "key":
                if isinstance(cur, dict) and key in cur:
                    cur = cur[key]
                else:
                    return default
            else:  # index
                if isinstance(cur, list) and 0 <= key < len(cur):
                    cur = cur[key]
                else:
                    return default
        return cur

    def set_value(self, data: dict, path: str, value: Any) -> bool:
        """Set a value at a dotted path. Returns True on success."""
        if not path:
            return False
        segments = _parse_path(path)
        if not segments:
            return False
        cur: Any = data
        for i, (kind, key) in enumerate(segments[:-1]):
            nxt_kind, nxt_key = segments[i + 1]
            if kind == "key":
                if not isinstance(cur, dict):
                    return False
                if key not in cur or not isinstance(cur[key], (dict, list)):
                    cur[key] = [] if nxt_kind == "index" else {}
                cur = cur[key]
            else:  # index
                if not isinstance(cur, list):
                    return False
                # Grow list as needed
                while len(cur) <= key:
                    cur.append(None)
                if not isinstance(cur[key], (dict, list)):
                    cur[key] = [] if nxt_kind == "index" else {}
                cur = cur[key]
        last_kind, last_key = segments[-1]
        if last_kind == "key":
            if not isinstance(cur, dict):
                return False
            cur[last_key] = value
            return True
        else:
            if not isinstance(cur, list):
                return False
            while len(cur) <= last_key:
                cur.append(None)
            cur[last_key] = value
            return True

    def _delete_value(self, data: dict, path: str) -> bool:
        """Delete a value at a dotted path. Returns True if removed."""
        if not path:
            return False
        segments = _parse_path(path)
        if not segments:
            return False
        cur: Any = data
        for kind, key in segments[:-1]:
            if kind == "key":
                if not isinstance(cur, dict) or key not in cur:
                    return False
                cur = cur[key]
            else:
                if not isinstance(cur, list) or not (0 <= key < len(cur)):
                    return False
                cur = cur[key]
        last_kind, last_key = segments[-1]
        if last_kind == "key":
            if isinstance(cur, dict) and last_key in cur:
                del cur[last_key]
                return True
            return False
        else:
            if isinstance(cur, list) and 0 <= last_key < len(cur):
                # Set to None rather than reindex; safer for ADDED/REMOVED
                # consistency. But to be useful, pop it.
                cur.pop(last_key)
                return True
            return False

    # ----- patch -----------------------------------------------------------

    def apply_patch(
        self,
        data: dict,
        changes: list[FieldChange],
    ) -> dict:
        """Apply a list of changes to a copy of data and return new dict.

        Handles ADDED (insert new value), REMOVED (delete), CHANGED and
        TYPE_CHANGED (replace value). UNCHANGED entries are skipped.

        Removals on list indices are processed last and in descending index
        order to keep earlier indices stable.
        """
        result = copy.deepcopy(data)

        adds_changes: list[FieldChange] = []
        replaces: list[FieldChange] = []
        removes: list[FieldChange] = []

        for c in changes:
            if c.kind == ChangeKind.ADDED:
                adds_changes.append(c)
            elif c.kind in (ChangeKind.CHANGED, ChangeKind.TYPE_CHANGED):
                replaces.append(c)
            elif c.kind == ChangeKind.REMOVED:
                removes.append(c)
            # UNCHANGED skipped

        # Apply replacements first (paths exist)
        for c in replaces:
            self.set_value(result, c.path, c.new_value)

        # Then additions (may create new keys / extend lists)
        for c in adds_changes:
            self.set_value(result, c.path, c.new_value)

        # Removals last; sort descending so list indices remain valid
        def _sort_key(ch: FieldChange) -> tuple:
            # Higher list indices first; otherwise reverse path order
            return (-len(ch.path), ch.path)

        removes.sort(key=_sort_key)
        # For list removals, ensure highest index removed first within same parent
        # A simple way: sort by path; reverse so deeper / higher indices first.
        removes.sort(key=lambda ch: ch.path, reverse=True)
        for c in removes:
            self._delete_value(result, c.path)

        return result

    # ----- path enumeration -----------------------------------------------

    def extract_paths(self, data: Any, prefix: str = "") -> list[str]:
        """Return all leaf paths in the data structure."""
        paths: list[str] = []
        if isinstance(data, dict):
            if not data:
                if prefix:
                    paths.append(prefix)
                return paths
            for k, v in data.items():
                sub = _join(prefix, str(k))
                if isinstance(v, (dict, list)) and v:
                    paths.extend(self.extract_paths(v, sub))
                else:
                    paths.append(sub)
        elif isinstance(data, list):
            if not data:
                if prefix:
                    paths.append(prefix)
                return paths
            for i, v in enumerate(data):
                sub = _index_path(prefix, i)
                if isinstance(v, (dict, list)) and v:
                    paths.extend(self.extract_paths(v, sub))
                else:
                    paths.append(sub)
        else:
            if prefix:
                paths.append(prefix)
        return paths

    # ----- compact ---------------------------------------------------------

    def compact(self, changes: list[FieldChange]) -> list[FieldChange]:
        """Remove UNCHANGED entries from a list of changes."""
        return [c for c in changes if c.kind != ChangeKind.UNCHANGED]
