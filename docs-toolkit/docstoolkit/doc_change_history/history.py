"""E332 DocChangeHistory — granular change history with diff entries.

Public API
----------
- ``ChangeEntry``        — a single change record
- ``ChangeHistoryStats`` — aggregate statistics
- ``DocChangeHistory``   — main interface for change history management
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ChangeEntry:
    """A single change record describing one field mutation on a document."""

    change_id: int
    doc_id: str
    field: str
    old_value: str
    new_value: str
    changed_at: float = 0.0
    changed_by: str = ""
    comment: str = ""


@dataclass
class ChangeHistoryStats:
    """Aggregate statistics over the recorded change history."""

    total_changes: int
    unique_docs: int
    unique_users: int
    unique_fields: int


# ---------------------------------------------------------------------------
# DocChangeHistory
# ---------------------------------------------------------------------------


class DocChangeHistory:
    """Thread-safe granular change history for documents.

    Each :meth:`record` call appends a :class:`ChangeEntry` describing a
    single field mutation.  Entries are indexed by document and by user for
    fast lookup.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._changes: list[ChangeEntry] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_user: dict[str, list[int]] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def record(
        self,
        doc_id: str,
        field: str,
        old_value: str,
        new_value: str,
        changed_by: str = "",
        comment: str = "",
        now: Optional[float] = None,
    ) -> ChangeEntry:
        """Record a single change and return the resulting :class:`ChangeEntry`."""
        ts = time.time() if now is None else now
        with self._lock:
            change_id = self._next_id
            self._next_id += 1
            entry = ChangeEntry(
                change_id=change_id,
                doc_id=doc_id,
                field=field,
                old_value=old_value,
                new_value=new_value,
                changed_at=ts,
                changed_by=changed_by,
                comment=comment,
            )
            self._changes.append(entry)
            self._by_doc.setdefault(doc_id, []).append(change_id)
            if changed_by:
                self._by_user.setdefault(changed_by, []).append(change_id)
        return entry

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _entry_by_id(self, change_id: int) -> Optional[ChangeEntry]:
        # change_ids are 1-based and contiguous; index = change_id - 1.
        idx = change_id - 1
        if 0 <= idx < len(self._changes):
            entry = self._changes[idx]
            if entry.change_id == change_id:
                return entry
        # Fallback: linear scan (should not happen with the invariant above).
        for entry in self._changes:
            if entry.change_id == change_id:
                return entry
        return None

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_change(self, change_id: int) -> Optional[ChangeEntry]:
        """Return the change with *change_id*, or ``None`` if not found."""
        with self._lock:
            return self._entry_by_id(change_id)

    def changes_for_doc(
        self,
        doc_id: str,
        field: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[ChangeEntry]:
        """Return changes for *doc_id*, sorted by ``changed_at``.

        Optionally filter by *field* and limit the number of returned entries.
        """
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            entries = [self._changes[i - 1] for i in ids]
        if field is not None:
            entries = [e for e in entries if e.field == field]
        entries.sort(key=lambda e: e.changed_at)
        if limit is not None:
            entries = entries[:limit]
        return entries

    def changes_by_user(
        self, user_id: str, limit: Optional[int] = None
    ) -> list[ChangeEntry]:
        """Return changes performed by *user_id*, sorted by ``changed_at``."""
        with self._lock:
            ids = list(self._by_user.get(user_id, []))
            entries = [self._changes[i - 1] for i in ids]
        entries.sort(key=lambda e: e.changed_at)
        if limit is not None:
            entries = entries[:limit]
        return entries

    def changes_in_range(
        self,
        start: float,
        end: float,
        doc_id: Optional[str] = None,
    ) -> list[ChangeEntry]:
        """Return changes with ``start <= changed_at <= end``.

        Optionally restrict to a single *doc_id*.  Result is sorted by
        ``changed_at``.
        """
        with self._lock:
            if doc_id is not None:
                ids = list(self._by_doc.get(doc_id, []))
                source = [self._changes[i - 1] for i in ids]
            else:
                source = list(self._changes)
        entries = [e for e in source if start <= e.changed_at <= end]
        entries.sort(key=lambda e: e.changed_at)
        return entries

    def latest_for(self, doc_id: str, field: str) -> Optional[ChangeEntry]:
        """Return the most recent change for *doc_id*+*field*, or ``None``."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            entries = [self._changes[i - 1] for i in ids if self._changes[i - 1].field == field]
        if not entries:
            return None
        entries.sort(key=lambda e: e.changed_at)
        return entries[-1]

    def revert_value(self, doc_id: str, field: str) -> Optional[str]:
        """Return the ``old_value`` of the most recent change for *doc_id*+*field*.

        Returns ``None`` if no such change has been recorded.
        """
        latest = self.latest_for(doc_id, field)
        return latest.old_value if latest is not None else None

    def count_changes_for(
        self, doc_id: str, field: Optional[str] = None
    ) -> int:
        """Return the number of changes recorded for *doc_id*.

        When *field* is provided, only count changes matching that field.
        """
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            if field is None:
                return len(ids)
            return sum(1 for i in ids if self._changes[i - 1].field == field)

    def purge_doc(self, doc_id: str) -> int:
        """Remove all change references for *doc_id* from the indexes.

        The global list of changes is preserved.  Returns the number of
        change entries removed from the per-document and per-user indexes.
        """
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            if not ids:
                return 0
            id_set = set(ids)
            # Remove from per-user indexes.
            empty_users: list[str] = []
            for user, user_ids in self._by_user.items():
                filtered = [i for i in user_ids if i not in id_set]
                if filtered:
                    self._by_user[user] = filtered
                else:
                    empty_users.append(user)
            for user in empty_users:
                del self._by_user[user]
            return len(ids)

    # ------------------------------------------------------------------
    # Enumeration / stats
    # ------------------------------------------------------------------

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of doc IDs with at least one indexed change."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> ChangeHistoryStats:
        """Return aggregate statistics over recorded changes."""
        with self._lock:
            total = len(self._changes)
            unique_docs = len(self._by_doc)
            unique_users = len(self._by_user)
            unique_fields = len({e.field for e in self._changes})
        return ChangeHistoryStats(
            total_changes=total,
            unique_docs=unique_docs,
            unique_users=unique_users,
            unique_fields=unique_fields,
        )
