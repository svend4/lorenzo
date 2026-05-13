"""Schema differ — recursive dict-based schema comparison.

Pure stdlib only: enum, dataclasses, copy.

Public API
----------
ChangeType   — enum of change categories
FieldChange  — single field-level change with path, old/new values and types
DiffResult   — collection of FieldChange objects with helper properties
SchemaDiffer — recursive differ with ignore_paths and treat_list_as_scalar options
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# ChangeType
# ---------------------------------------------------------------------------

class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"
    TYPE_CHANGED = "type_changed"


# ---------------------------------------------------------------------------
# FieldChange
# ---------------------------------------------------------------------------

@dataclass
class FieldChange:
    """Represents a single field-level change between two dicts."""

    path: str           # dot-notation path, e.g. "user.address.city"
    change_type: ChangeType
    old_value: Any = None
    new_value: Any = None
    old_type: str = ""
    new_type: str = ""

    def __repr__(self) -> str:
        return (
            f"FieldChange(path={self.path!r}, change_type={self.change_type!r}, "
            f"old_value={self.old_value!r}, new_value={self.new_value!r})"
        )


# ---------------------------------------------------------------------------
# DiffResult
# ---------------------------------------------------------------------------

@dataclass
class DiffResult:
    """Collection of FieldChange objects produced by SchemaDiffer.diff()."""

    changes: list[FieldChange] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def has_changes(self) -> bool:
        """Return True if there is at least one change."""
        return bool(self.changes)

    @property
    def added(self) -> list[FieldChange]:
        """Return only ADDED changes."""
        return [c for c in self.changes if c.change_type == ChangeType.ADDED]

    @property
    def removed(self) -> list[FieldChange]:
        """Return only REMOVED changes."""
        return [c for c in self.changes if c.change_type == ChangeType.REMOVED]

    @property
    def changed(self) -> list[FieldChange]:
        """Return only CHANGED changes."""
        return [c for c in self.changes if c.change_type == ChangeType.CHANGED]

    @property
    def type_changed(self) -> list[FieldChange]:
        """Return only TYPE_CHANGED changes."""
        return [c for c in self.changes if c.change_type == ChangeType.TYPE_CHANGED]

    # ------------------------------------------------------------------
    # summary
    # ------------------------------------------------------------------

    def summary(self) -> dict:
        """Return counts per change type plus total.

        Returns
        -------
        dict with keys: 'added', 'removed', 'changed', 'type_changed', 'total'
        """
        added = len(self.added)
        removed = len(self.removed)
        changed = len(self.changed)
        type_changed = len(self.type_changed)
        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "type_changed": type_changed,
            "total": added + removed + changed + type_changed,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _join_path(parent: str, key: str) -> str:
    """Join parent path and key using dot notation."""
    if parent:
        return f"{parent}.{key}"
    return key


def _type_name(value: Any) -> str:
    """Return the type name of value as a string."""
    return type(value).__name__


def _deep_set(target: dict, path: str, value: Any) -> None:
    """Set *value* at *path* (dot-notation) inside *target*, creating dicts as needed."""
    parts = path.split(".")
    cursor = target
    for part in parts[:-1]:
        if part not in cursor or not isinstance(cursor[part], dict):
            cursor[part] = {}
        cursor = cursor[part]
    cursor[parts[-1]] = value


def _deep_del(target: dict, path: str) -> None:
    """Delete the key at *path* (dot-notation) inside *target*.

    If intermediate keys are missing the operation is silently skipped.
    After deletion, intermediate dicts are NOT pruned.
    """
    parts = path.split(".")
    cursor = target
    for part in parts[:-1]:
        if not isinstance(cursor, dict) or part not in cursor:
            return
        cursor = cursor[part]
    if isinstance(cursor, dict):
        cursor.pop(parts[-1], None)


# ---------------------------------------------------------------------------
# SchemaDiffer
# ---------------------------------------------------------------------------

class SchemaDiffer:
    """Recursive dict schema differ.

    Parameters
    ----------
    ignore_paths:
        Set of dot-notation paths to skip entirely during comparison.
    treat_list_as_scalar:
        When True, lists are compared as opaque scalar values (equal or not).
        When False (default), lists are reported as CHANGED if they differ
        (no element-level diffing is performed).
    """

    def __init__(
        self,
        ignore_paths: set[str] | None = None,
        treat_list_as_scalar: bool = False,
    ) -> None:
        self._ignore_paths: set[str] = ignore_paths or set()
        self._treat_list_as_scalar = treat_list_as_scalar

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def diff(self, old: dict, new: dict) -> DiffResult:
        """Compare *old* and *new* dicts recursively.

        Returns a :class:`DiffResult` whose ``changes`` list contains one
        :class:`FieldChange` per field that was added, removed, changed, or
        had its type changed.

        Rules
        -----
        * Key in *new* but not *old*  → ADDED
        * Key in *old* but not *new*  → REMOVED
        * Both present, same type, both dicts → recurse
        * Both present, different type → TYPE_CHANGED
        * Both present, same type, not dict, value differs → CHANGED
        * Both present, same type, not dict, value equal → no change
        """
        result = DiffResult()
        self._recurse(old, new, parent_path="", result=result)
        return result

    def is_compatible(self, old: dict, new: dict) -> bool:
        """Return True if *new* is backward-compatible with *old*.

        Backward-compatible means no REMOVED fields and no TYPE_CHANGED
        fields.  ADDED and CHANGED fields are acceptable.
        """
        result = self.diff(old, new)
        return not result.removed and not result.type_changed

    def patch(self, base: dict, changes: DiffResult) -> dict:
        """Apply *changes* to *base* and return a new dict.

        * ADDED entries set the key in the result.
        * CHANGED entries overwrite the key in the result.
        * REMOVED entries delete the key from the result.
        * TYPE_CHANGED entries apply the new value.

        The original *base* dict is never modified.
        """
        result = copy.deepcopy(base)
        for change in changes.changes:
            if change.change_type in (
                ChangeType.ADDED,
                ChangeType.CHANGED,
                ChangeType.TYPE_CHANGED,
            ):
                _deep_set(result, change.path, change.new_value)
            elif change.change_type == ChangeType.REMOVED:
                _deep_del(result, change.path)
        return result

    # ------------------------------------------------------------------
    # Internal recursion
    # ------------------------------------------------------------------

    def _recurse(
        self,
        old: dict,
        new: dict,
        parent_path: str,
        result: DiffResult,
    ) -> None:
        """Recursive worker that populates *result.changes*."""
        all_keys = set(old) | set(new)

        for key in sorted(all_keys):  # sorted for deterministic output
            path = _join_path(parent_path, str(key))

            # Skip ignored paths
            if path in self._ignore_paths:
                continue

            in_old = key in old
            in_new = key in new

            if in_new and not in_old:
                # Key present only in new → ADDED
                result.changes.append(FieldChange(
                    path=path,
                    change_type=ChangeType.ADDED,
                    old_value=None,
                    new_value=new[key],
                ))

            elif in_old and not in_new:
                # Key present only in old → REMOVED
                result.changes.append(FieldChange(
                    path=path,
                    change_type=ChangeType.REMOVED,
                    old_value=old[key],
                    new_value=None,
                ))

            else:
                # Key present in both
                old_val = old[key]
                new_val = new[key]

                old_t = type(old_val)
                new_t = type(new_val)

                # Python treats bool as a subclass of int; we want to
                # distinguish them as different types.
                if old_t != new_t:
                    result.changes.append(FieldChange(
                        path=path,
                        change_type=ChangeType.TYPE_CHANGED,
                        old_value=old_val,
                        new_value=new_val,
                        old_type=_type_name(old_val),
                        new_type=_type_name(new_val),
                    ))

                elif isinstance(old_val, dict):
                    # Both are dicts → recurse
                    self._recurse(old_val, new_val, path, result)

                elif isinstance(old_val, list) and not self._treat_list_as_scalar:
                    # List comparison (no element-level diff, just equality)
                    if old_val != new_val:
                        result.changes.append(FieldChange(
                            path=path,
                            change_type=ChangeType.CHANGED,
                            old_value=old_val,
                            new_value=new_val,
                        ))

                else:
                    # Scalar (or list treated as scalar)
                    if old_val != new_val:
                        result.changes.append(FieldChange(
                            path=path,
                            change_type=ChangeType.CHANGED,
                            old_value=old_val,
                            new_value=new_val,
                        ))
