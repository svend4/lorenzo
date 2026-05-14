"""E416 DocRecentActivity — track and query recent document activities.

In-memory, thread-safe ring buffer of activity events keyed by ``doc_id``,
``actor`` and ``kind``.  Newest items are appended at the end of an internal
ordered list; when the buffer exceeds ``max_size`` the oldest events are
dropped and the secondary indexes are cleaned up accordingly.
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
class Activity:
    """A single activity event."""

    activity_id: int
    doc_id: str
    actor: str
    kind: str
    at: float = 0.0
    details: str = ""


@dataclass
class ActivityStats:
    """Aggregate statistics over the tracked activities."""

    total_activities: int
    unique_docs: int
    unique_actors: int
    kind_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocRecentActivity
# ---------------------------------------------------------------------------


class DocRecentActivity:
    """Thread-safe tracker of recent document activities.

    Activities are stored in insertion order in :attr:`_activities`.  The
    list is bounded by ``max_size``; when the cap is exceeded the oldest
    activity is evicted and removed from the secondary indexes.
    """

    def __init__(self, max_size: int = 1000) -> None:
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        self._lock = threading.Lock()
        self._activities: list[Activity] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_actor: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._max_size: int = max_size

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def record(
        self,
        doc_id: str,
        actor: str,
        kind: str,
        details: str = "",
        now: Optional[float] = None,
    ) -> Activity:
        """Record a new activity event and return it.

        If after appending the buffer exceeds :attr:`_max_size` the oldest
        activity is dropped from the global list and from the per-doc /
        per-actor indexes.
        """
        ts = time.time() if now is None else now
        with self._lock:
            activity_id = self._next_id
            self._next_id += 1
            activity = Activity(
                activity_id=activity_id,
                doc_id=doc_id,
                actor=actor,
                kind=kind,
                at=ts,
                details=details,
            )
            self._activities.append(activity)
            self._by_doc.setdefault(doc_id, []).append(activity_id)
            self._by_actor.setdefault(actor, []).append(activity_id)

            # Evict oldest entries to respect max_size
            while len(self._activities) > self._max_size:
                oldest = self._activities.pop(0)
                self._remove_from_index(self._by_doc, oldest.doc_id, oldest.activity_id)
                self._remove_from_index(
                    self._by_actor, oldest.actor, oldest.activity_id
                )
        return activity

    @staticmethod
    def _remove_from_index(
        index: dict[str, list[int]], key: str, activity_id: int
    ) -> None:
        ids = index.get(key)
        if not ids:
            return
        try:
            ids.remove(activity_id)
        except ValueError:
            pass
        if not ids:
            index.pop(key, None)

    # ------------------------------------------------------------------
    # Queries — recent (most-recent first)
    # ------------------------------------------------------------------

    def recent(self, limit: int = 10) -> list[Activity]:
        """Return up to *limit* most recent activities (newest first)."""
        if limit <= 0:
            return []
        with self._lock:
            tail = self._activities[-limit:]
            return list(reversed(tail))

    def recent_for_doc(self, doc_id: str, limit: int = 10) -> list[Activity]:
        """Return up to *limit* most recent activities for *doc_id*."""
        if limit <= 0:
            return []
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            chosen_ids = ids[-limit:] if limit else ids[:]
            # Build map id->Activity restricted to needed ids
            wanted = set(chosen_ids)
            mapping = {a.activity_id: a for a in self._activities if a.activity_id in wanted}
            result = [mapping[i] for i in chosen_ids if i in mapping]
            return list(reversed(result))

    def recent_for_actor(self, actor: str, limit: int = 10) -> list[Activity]:
        """Return up to *limit* most recent activities by *actor*."""
        if limit <= 0:
            return []
        with self._lock:
            ids = self._by_actor.get(actor, [])
            chosen_ids = ids[-limit:] if limit else ids[:]
            wanted = set(chosen_ids)
            mapping = {a.activity_id: a for a in self._activities if a.activity_id in wanted}
            result = [mapping[i] for i in chosen_ids if i in mapping]
            return list(reversed(result))

    def recent_of_kind(self, kind: str, limit: int = 10) -> list[Activity]:
        """Return up to *limit* most recent activities of *kind*."""
        if limit <= 0:
            return []
        with self._lock:
            matching = [a for a in self._activities if a.kind == kind]
            tail = matching[-limit:]
            return list(reversed(tail))

    def since(self, timestamp: float) -> list[Activity]:
        """Return activities with ``at >= timestamp``, sorted ascending by ``at``."""
        with self._lock:
            matching = [a for a in self._activities if a.at >= timestamp]
        matching.sort(key=lambda a: (a.at, a.activity_id))
        return matching

    # ------------------------------------------------------------------
    # Queries — active sets within a window
    # ------------------------------------------------------------------

    def active_docs(
        self, within_seconds: float = 86400, now: Optional[float] = None
    ) -> list[str]:
        """Return sorted doc_ids with at least one activity in the window."""
        ts = time.time() if now is None else now
        threshold = ts - within_seconds
        with self._lock:
            docs = {a.doc_id for a in self._activities if a.at >= threshold}
        return sorted(docs)

    def active_actors(
        self, within_seconds: float = 86400, now: Optional[float] = None
    ) -> list[str]:
        """Return sorted actors with at least one activity in the window."""
        ts = time.time() if now is None else now
        threshold = ts - within_seconds
        with self._lock:
            actors = {a.actor for a in self._activities if a.at >= threshold}
        return sorted(actors)

    # ------------------------------------------------------------------
    # Counts
    # ------------------------------------------------------------------

    def count_for_doc(self, doc_id: str) -> int:
        """Return the number of recorded activities for *doc_id*."""
        with self._lock:
            return len(self._by_doc.get(doc_id, []))

    def count_for_actor(self, actor: str) -> int:
        """Return the number of recorded activities by *actor*."""
        with self._lock:
            return len(self._by_actor.get(actor, []))

    def count_of_kind(self, kind: str) -> int:
        """Return the number of recorded activities of *kind*."""
        with self._lock:
            return sum(1 for a in self._activities if a.kind == kind)

    # ------------------------------------------------------------------
    # Clearing
    # ------------------------------------------------------------------

    def clear_doc(self, doc_id: str) -> int:
        """Drop all activities for *doc_id*.  Return number removed."""
        with self._lock:
            ids = set(self._by_doc.pop(doc_id, []))
            if not ids:
                return 0
            removed = 0
            new_activities: list[Activity] = []
            for a in self._activities:
                if a.activity_id in ids:
                    self._remove_from_index(self._by_actor, a.actor, a.activity_id)
                    removed += 1
                else:
                    new_activities.append(a)
            self._activities = new_activities
            return removed

    def clear_actor(self, actor: str) -> int:
        """Drop all activities by *actor*.  Return number removed."""
        with self._lock:
            ids = set(self._by_actor.pop(actor, []))
            if not ids:
                return 0
            removed = 0
            new_activities: list[Activity] = []
            for a in self._activities:
                if a.activity_id in ids:
                    self._remove_from_index(self._by_doc, a.doc_id, a.activity_id)
                    removed += 1
                else:
                    new_activities.append(a)
            self._activities = new_activities
            return removed

    def clear_all(self) -> int:
        """Drop every recorded activity.  Return number removed."""
        with self._lock:
            removed = len(self._activities)
            self._activities.clear()
            self._by_doc.clear()
            self._by_actor.clear()
            return removed

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> ActivityStats:
        """Return aggregate statistics for the currently tracked activities."""
        with self._lock:
            total = len(self._activities)
            unique_docs = len(self._by_doc)
            unique_actors = len(self._by_actor)
            kind_counts: dict[str, int] = {}
            for a in self._activities:
                kind_counts[a.kind] = kind_counts.get(a.kind, 0) + 1
        return ActivityStats(
            total_activities=total,
            unique_docs=unique_docs,
            unique_actors=unique_actors,
            kind_counts=kind_counts,
        )
