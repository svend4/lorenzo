"""E398 DocActionLog — append-only structured action log.

Stores :class:`ActionEvent` records describing actions performed against
documents, with rich indexing by doc, actor, and action.  All operations
are thread-safe.
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
class ActionEvent:
    """A single action event."""

    event_id: int
    doc_id: str
    actor: str
    action: str
    timestamp: float = 0.0
    payload: dict = field(default_factory=dict)
    success: bool = True


@dataclass
class ActionStats:
    """Aggregate statistics over all logged action events."""

    total_events: int
    success_count: int
    failure_count: int
    unique_docs: int
    unique_actors: int
    unique_actions: int


# ---------------------------------------------------------------------------
# DocActionLog
# ---------------------------------------------------------------------------


class DocActionLog:
    """Thread-safe append-only structured action log.

    Events are stored in a global ordered list along with three indices
    mapping ``doc_id``, ``actor`` and ``action`` to lists of integer event
    indices in the global list.  Event ids auto-increment from ``1``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[ActionEvent] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_actor: dict[str, list[int]] = {}
        self._by_action: dict[str, list[int]] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def log_action(
        self,
        doc_id: str,
        actor: str,
        action: str,
        success: bool = True,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> ActionEvent:
        """Append a new action event and return it.

        Parameters
        ----------
        doc_id:
            Identifier of the document being acted upon.
        actor:
            User or system principal performing the action.
        action:
            Name of the action, e.g. ``"created"``, ``"edited"``.
        success:
            Whether the action succeeded.  Defaults to ``True``.
        payload:
            Optional mapping of additional context.  A shallow copy is stored.
        now:
            Timestamp for the event.  When ``None``, :func:`time.time` is used.
        """
        ts = time.time() if now is None else now
        data = dict(payload) if payload else {}
        with self._lock:
            event_id = self._next_id
            self._next_id += 1
            event = ActionEvent(
                event_id=event_id,
                doc_id=doc_id,
                actor=actor,
                action=action,
                timestamp=ts,
                payload=data,
                success=success,
            )
            idx = len(self._events)
            self._events.append(event)
            self._by_doc.setdefault(doc_id, []).append(idx)
            self._by_actor.setdefault(actor, []).append(idx)
            self._by_action.setdefault(action, []).append(idx)
        return event

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_event(self, event_id: int) -> Optional[ActionEvent]:
        """Return the event with *event_id*, or ``None`` if not found."""
        with self._lock:
            # event_id 1 corresponds to index 0
            idx = event_id - 1
            if 0 <= idx < len(self._events):
                ev = self._events[idx]
                if ev.event_id == event_id:
                    return ev
            # Fallback linear scan in case of inconsistency
            for ev in self._events:
                if ev.event_id == event_id:
                    return ev
        return None

    def _collect(
        self, index_list: list[int], limit: Optional[int]
    ) -> list[ActionEvent]:
        """Return events at the given indices, most recent first."""
        # Index list is built in insertion order; reverse for "most recent first".
        result = [self._events[i] for i in reversed(index_list)]
        if limit is not None:
            result = result[:limit]
        return result

    def events_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[ActionEvent]:
        """Return events for *doc_id*, most recent first."""
        with self._lock:
            indices = list(self._by_doc.get(doc_id, []))
            return self._collect(indices, limit)

    def events_for_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> list[ActionEvent]:
        """Return events logged by *actor*, most recent first."""
        with self._lock:
            indices = list(self._by_actor.get(actor, []))
            return self._collect(indices, limit)

    def events_by_action(
        self, action: str, limit: Optional[int] = None
    ) -> list[ActionEvent]:
        """Return events whose action matches *action*, most recent first."""
        with self._lock:
            indices = list(self._by_action.get(action, []))
            return self._collect(indices, limit)

    def events_in_range(
        self,
        start_time: float,
        end_time: float,
        doc_id: Optional[str] = None,
    ) -> list[ActionEvent]:
        """Return events with ``start_time <= timestamp <= end_time``.

        Sorted ascending by timestamp.  When *doc_id* is given the result is
        additionally restricted to that document.
        """
        with self._lock:
            if doc_id is not None:
                source = [self._events[i] for i in self._by_doc.get(doc_id, [])]
            else:
                source = list(self._events)
        filtered = [
            ev for ev in source if start_time <= ev.timestamp <= end_time
        ]
        filtered.sort(key=lambda ev: ev.timestamp)
        return filtered

    def failed_events(self, limit: int = 10) -> list[ActionEvent]:
        """Return events where ``success=False``, most recent first."""
        with self._lock:
            failures = [ev for ev in self._events if not ev.success]
        failures.reverse()
        if limit is not None:
            failures = failures[:limit]
        return failures

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    def action_counts(self) -> dict:
        """Return mapping ``action -> count`` of events with that action."""
        with self._lock:
            return {action: len(idxs) for action, idxs in self._by_action.items()}

    def actor_counts(self) -> dict:
        """Return mapping ``actor -> count`` of events from that actor."""
        with self._lock:
            return {actor: len(idxs) for actor, idxs in self._by_actor.items()}

    def top_actors(self, limit: int = 10) -> list[tuple]:
        """Return ``(actor, count)`` pairs sorted by count desc."""
        counts = self.actor_counts()
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if limit is not None:
            ordered = ordered[:limit]
        return ordered

    def top_actions(self, limit: int = 10) -> list[tuple]:
        """Return ``(action, count)`` pairs sorted by count desc."""
        counts = self.action_counts()
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if limit is not None:
            ordered = ordered[:limit]
        return ordered

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def clear_old(self, before_timestamp: float) -> int:
        """Remove events with ``timestamp < before_timestamp``.

        Returns the number of removed events.  All secondary indices are
        rebuilt to keep them consistent.
        """
        with self._lock:
            keep: list[ActionEvent] = []
            removed = 0
            for ev in self._events:
                if ev.timestamp < before_timestamp:
                    removed += 1
                else:
                    keep.append(ev)
            self._events = keep
            self._by_doc.clear()
            self._by_actor.clear()
            self._by_action.clear()
            for idx, ev in enumerate(self._events):
                self._by_doc.setdefault(ev.doc_id, []).append(idx)
                self._by_actor.setdefault(ev.actor, []).append(idx)
                self._by_action.setdefault(ev.action, []).append(idx)
            return removed

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> ActionStats:
        """Return aggregate statistics over all logged events."""
        with self._lock:
            total = len(self._events)
            success_count = sum(1 for ev in self._events if ev.success)
            failure_count = total - success_count
            unique_docs = len(self._by_doc)
            unique_actors = len(self._by_actor)
            unique_actions = len(self._by_action)
        return ActionStats(
            total_events=total,
            success_count=success_count,
            failure_count=failure_count,
            unique_docs=unique_docs,
            unique_actors=unique_actors,
            unique_actions=unique_actions,
        )
