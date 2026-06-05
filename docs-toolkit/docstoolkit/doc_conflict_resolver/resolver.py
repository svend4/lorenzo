"""Conflict detection and resolution for document versions (E301).

Detects field-level conflicts between two versions of a document and
provides manual and automatic resolution strategies.
Stdlib-only, thread-safe via threading.Lock.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Conflict:
    """A detected conflict between two document versions."""

    conflict_id: str
    doc_id: str
    version_a: str
    version_b: str
    field: str
    value_a: str
    value_b: str
    detected_at: float = 0.0
    status: str = "open"  # "open", "resolved", "ignored"


@dataclass
class Resolution:
    """The result of resolving a conflict."""

    conflict_id: str
    doc_id: str
    chosen_version: str  # "a", "b", or "merged"
    resolved_value: str
    resolved_at: float = 0.0
    resolver: str = "manual"  # "manual", "auto_latest", "auto_merge"


@dataclass
class ResolverStats:
    """Aggregate statistics for tracked conflicts."""

    total_conflicts: int
    open_conflicts: int
    resolved_conflicts: int
    ignored_conflicts: int


class DocConflictResolver:
    """Thread-safe registry for detecting and resolving document conflicts."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._conflicts: dict[str, Conflict] = {}
        self._resolutions: dict[str, Resolution] = {}

    # --- detection ---

    def detect_conflict(
        self,
        doc_id: str,
        version_a: str,
        version_b: str,
        field: str,
        value_a: str,
        value_b: str,
        now: Optional[float] = None,
    ) -> Optional[Conflict]:
        """Detect a conflict between two versions of a document field.

        Returns None if value_a == value_b (no conflict).
        Otherwise creates, stores, and returns a new Conflict.
        """
        if value_a == value_b:
            return None
        conflict_id = str(uuid.uuid4())
        detected_at = now if now is not None else 0.0
        conflict = Conflict(
            conflict_id=conflict_id,
            doc_id=doc_id,
            version_a=version_a,
            version_b=version_b,
            field=field,
            value_a=value_a,
            value_b=value_b,
            detected_at=detected_at,
            status="open",
        )
        with self._lock:
            self._conflicts[conflict_id] = conflict
        return conflict

    # --- resolution ---

    def resolve(
        self,
        conflict_id: str,
        chosen_version: str,
        resolved_value: str,
        resolver: str = "manual",
        now: Optional[float] = None,
    ) -> Optional[Resolution]:
        """Mark a conflict as resolved and store the resolution.

        Returns None if the conflict_id is not found.
        """
        resolved_at = now if now is not None else 0.0
        with self._lock:
            conflict = self._conflicts.get(conflict_id)
            if conflict is None:
                return None
            conflict.status = "resolved"
            resolution = Resolution(
                conflict_id=conflict_id,
                doc_id=conflict.doc_id,
                chosen_version=chosen_version,
                resolved_value=resolved_value,
                resolved_at=resolved_at,
                resolver=resolver,
            )
            self._resolutions[conflict_id] = resolution
        return resolution

    def ignore_conflict(self, conflict_id: str) -> bool:
        """Set a conflict's status to 'ignored'. Returns True if found."""
        with self._lock:
            conflict = self._conflicts.get(conflict_id)
            if conflict is None:
                return False
            conflict.status = "ignored"
            return True

    # --- auto-resolution strategies ---

    def auto_resolve_latest(
        self,
        conflict_id: str,
        now: Optional[float] = None,
    ) -> Optional[Resolution]:
        """Auto-resolve by choosing version_b (assumed latest).

        Sets resolver='auto_latest' and resolved_value=conflict.value_b.
        Returns None if conflict not found.
        """
        with self._lock:
            conflict = self._conflicts.get(conflict_id)
            if conflict is None:
                return None
        return self.resolve(
            conflict_id=conflict_id,
            chosen_version="b",
            resolved_value=conflict.value_b,
            resolver="auto_latest",
            now=now,
        )

    def auto_resolve_merge(
        self,
        conflict_id: str,
        separator: str = " | ",
        now: Optional[float] = None,
    ) -> Optional[Resolution]:
        """Auto-resolve by merging both values with a separator.

        Sets resolved_value=value_a + separator + value_b,
        chosen_version='merged', resolver='auto_merge'.
        Returns None if conflict not found.
        """
        with self._lock:
            conflict = self._conflicts.get(conflict_id)
            if conflict is None:
                return None
        merged_value = conflict.value_a + separator + conflict.value_b
        return self.resolve(
            conflict_id=conflict_id,
            chosen_version="merged",
            resolved_value=merged_value,
            resolver="auto_merge",
            now=now,
        )

    # --- queries ---

    def get_conflict(self, conflict_id: str) -> Optional[Conflict]:
        """Return a conflict by id, or None."""
        with self._lock:
            return self._conflicts.get(conflict_id)

    def get_resolution(self, conflict_id: str) -> Optional[Resolution]:
        """Return a resolution by conflict_id, or None."""
        with self._lock:
            return self._resolutions.get(conflict_id)

    def conflicts_for_doc(self, doc_id: str) -> list[Conflict]:
        """All conflicts for a given document, sorted by detected_at."""
        with self._lock:
            results = [c for c in self._conflicts.values() if c.doc_id == doc_id]
        return sorted(results, key=lambda c: c.detected_at)

    def open_conflicts(self) -> list[Conflict]:
        """All conflicts with status 'open', sorted by detected_at."""
        with self._lock:
            results = [c for c in self._conflicts.values() if c.status == "open"]
        return sorted(results, key=lambda c: c.detected_at)

    def all_conflicts(self) -> list[Conflict]:
        """All conflicts sorted by detected_at."""
        with self._lock:
            results = list(self._conflicts.values())
        return sorted(results, key=lambda c: c.detected_at)

    def stats(self) -> ResolverStats:
        """Return aggregate statistics over all tracked conflicts."""
        with self._lock:
            conflicts = list(self._conflicts.values())
        total = len(conflicts)
        open_count = sum(1 for c in conflicts if c.status == "open")
        resolved_count = sum(1 for c in conflicts if c.status == "resolved")
        ignored_count = sum(1 for c in conflicts if c.status == "ignored")
        return ResolverStats(
            total_conflicts=total,
            open_conflicts=open_count,
            resolved_conflicts=resolved_count,
            ignored_conflicts=ignored_count,
        )
