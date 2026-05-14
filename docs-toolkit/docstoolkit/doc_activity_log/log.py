"""E304 DocActivityLog — append-only activity log for document operations.

Public API
----------
- ``ActivityEntry``  — a single logged activity event
- ``ActivityStats``  — aggregate statistics
- ``DocActivityLog`` — main interface for logging and querying activity
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ActivityEntry:
    """A single logged activity event."""

    entry_id: int
    doc_id: str
    action: str
    actor: str
    timestamp: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class ActivityStats:
    """Aggregate statistics over all logged activity."""

    total_entries: int
    unique_docs: int
    unique_actors: int
    action_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocActivityLog
# ---------------------------------------------------------------------------


class DocActivityLog:
    """Thread-safe append-only activity log for document operations.

    All entries are stored in memory.  The log is ordered by insertion time
    (auto-increment ``entry_id``).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: list[ActivityEntry] = []
        self._by_doc: dict[str, list[ActivityEntry]] = {}
        self._by_actor: dict[str, list[ActivityEntry]] = {}
        # O(1) lookup by entry_id
        self._by_id: dict[int, ActivityEntry] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def log(
        self,
        doc_id: str,
        action: str,
        actor: str,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> ActivityEntry:
        """Append a new activity entry and return it.

        Parameters
        ----------
        doc_id:
            Identifier of the document being acted upon.
        action:
            Name of the action, e.g. ``"created"``, ``"viewed"``,
            ``"edited"``, ``"deleted"``, ``"shared"``.
        actor:
            User or system principal performing the action.
        metadata:
            Optional mapping of additional context.  Defaults to ``{}``.
        now:
            Timestamp for the entry.  When ``None``, :func:`time.time` is used.
        """
        ts = time.time() if now is None else now
        meta = dict(metadata) if metadata else {}
        with self._lock:
            entry_id = self._next_id
            self._next_id += 1
            entry = ActivityEntry(
                entry_id=entry_id,
                doc_id=doc_id,
                action=action,
                actor=actor,
                timestamp=ts,
                metadata=meta,
            )
            self._entries.append(entry)
            self._by_doc.setdefault(doc_id, []).append(entry)
            self._by_actor.setdefault(actor, []).append(entry)
            self._by_id[entry_id] = entry
        return entry

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def entries_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[ActivityEntry]:
        """Return entries for *doc_id* in insertion order, optionally limited."""
        with self._lock:
            result = list(self._by_doc.get(doc_id, []))
        if limit is not None:
            result = result[:limit]
        return result

    def entries_by_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> list[ActivityEntry]:
        """Return entries logged by *actor* in insertion order, optionally limited."""
        with self._lock:
            result = list(self._by_actor.get(actor, []))
        if limit is not None:
            result = result[:limit]
        return result

    def entries_by_action(
        self, action: str, limit: Optional[int] = None
    ) -> list[ActivityEntry]:
        """Return entries whose action matches *action*, in insertion order.

        Performs a linear scan of the global entry list.
        """
        with self._lock:
            result = [e for e in self._entries if e.action == action]
        if limit is not None:
            result = result[:limit]
        return result

    def recent(self, limit: int = 10) -> list[ActivityEntry]:
        """Return the last *limit* entries across all docs (tail of global list)."""
        with self._lock:
            return list(self._entries[-limit:]) if limit > 0 else []

    def get_entry(self, entry_id: int) -> Optional[ActivityEntry]:
        """Return the entry with *entry_id*, or ``None`` if not found."""
        with self._lock:
            return self._by_id.get(entry_id)

    # ------------------------------------------------------------------
    # Enumeration helpers
    # ------------------------------------------------------------------

    def doc_ids(self) -> list[str]:
        """Return a sorted list of unique doc IDs that have at least one entry."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def actors(self) -> list[str]:
        """Return a sorted list of unique actors seen in the log."""
        with self._lock:
            return sorted(self._by_actor.keys())

    def actions(self) -> list[str]:
        """Return a sorted list of unique action types seen in the log."""
        with self._lock:
            seen: set[str] = {e.action for e in self._entries}
        return sorted(seen)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> ActivityStats:
        """Return aggregate statistics over all logged entries."""
        with self._lock:
            total = len(self._entries)
            unique_docs = len(self._by_doc)
            unique_actors = len(self._by_actor)
            action_counts: dict[str, int] = {}
            for entry in self._entries:
                action_counts[entry.action] = action_counts.get(entry.action, 0) + 1
        return ActivityStats(
            total_entries=total,
            unique_docs=unique_docs,
            unique_actors=unique_actors,
            action_counts=action_counts,
        )
