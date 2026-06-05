"""E443 DocPinAudit — audit log for document pinning events.

Stores :class:`PinAuditEvent` records describing pin-related operations
(``pin``, ``unpin``, ``renew``, ``move``, ``transfer``) performed against
documents, with rich indexing by doc, actor and action.  All operations
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
class PinAuditEvent:
    """A single pin audit event."""

    event_id: int
    doc_id: str
    actor: str
    action: str
    timestamp: float = 0.0
    reason: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class PinAuditStats:
    """Aggregate statistics over all recorded pin audit events."""

    total_events: int
    unique_docs: int
    unique_actors: int
    action_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocPinAudit
# ---------------------------------------------------------------------------


# Actions that are considered "pin-like" for the purposes of determining the
# most recent pin event for a document.
_PIN_LIKE_ACTIONS = frozenset({"pin", "renew"})


class DocPinAudit:
    """Thread-safe audit log for document pin events.

    Events are stored in a global ordered list along with secondary indices
    mapping ``doc_id`` and ``actor`` to lists of integer event indices in
    the global list.  Event ids auto-increment from ``1``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[PinAuditEvent] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_actor: dict[str, list[int]] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def log(
        self,
        doc_id: str,
        actor: str,
        action: str,
        reason: str = "",
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> PinAuditEvent:
        """Append a new pin audit event and return it.

        Parameters
        ----------
        doc_id:
            Identifier of the pinned document.
        actor:
            User or system principal performing the action.
        action:
            One of ``"pin"``, ``"unpin"``, ``"renew"``, ``"move"`` or
            ``"transfer"``.  No validation is performed; arbitrary action
            strings are accepted.
        reason:
            Optional free-form reason describing why the action was taken.
        metadata:
            Optional mapping of additional context.  A shallow copy is stored.
        now:
            Timestamp for the event.  When ``None``, :func:`time.time` is
            used.
        """
        ts = time.time() if now is None else now
        data = dict(metadata) if metadata else {}
        with self._lock:
            event_id = self._next_id
            self._next_id += 1
            event = PinAuditEvent(
                event_id=event_id,
                doc_id=doc_id,
                actor=actor,
                action=action,
                timestamp=ts,
                reason=reason,
                metadata=data,
            )
            idx = len(self._events)
            self._events.append(event)
            self._by_doc.setdefault(doc_id, []).append(idx)
            self._by_actor.setdefault(actor, []).append(idx)
        return event

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_event(self, event_id: int) -> Optional[PinAuditEvent]:
        """Return the event with *event_id*, or ``None`` if not found."""
        with self._lock:
            idx = event_id - 1
            if 0 <= idx < len(self._events):
                ev = self._events[idx]
                if ev.event_id == event_id:
                    return ev
            # Fallback linear scan in case of inconsistency (e.g. after
            # ``delete_old`` reindexes events).
            for ev in self._events:
                if ev.event_id == event_id:
                    return ev
        return None

    def _collect(
        self,
        index_list: list[int],
        limit: Optional[int],
        action: Optional[str] = None,
    ) -> list[PinAuditEvent]:
        """Return events at the given indices, most recent first."""
        result: list[PinAuditEvent] = []
        for i in reversed(index_list):
            ev = self._events[i]
            if action is not None and ev.action != action:
                continue
            result.append(ev)
        if limit is not None:
            result = result[:limit]
        return result

    def events_for_doc(
        self,
        doc_id: str,
        action: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[PinAuditEvent]:
        """Return events for *doc_id*, most recent first.

        When *action* is given, only events whose ``action`` matches are
        returned.
        """
        with self._lock:
            indices = list(self._by_doc.get(doc_id, []))
            return self._collect(indices, limit, action=action)

    def events_for_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> list[PinAuditEvent]:
        """Return events for *actor*, most recent first."""
        with self._lock:
            indices = list(self._by_actor.get(actor, []))
            return self._collect(indices, limit)

    def events_by_action(
        self, action: str, limit: Optional[int] = None
    ) -> list[PinAuditEvent]:
        """Return events whose ``action`` matches *action*, most recent first."""
        with self._lock:
            matching = [ev for ev in self._events if ev.action == action]
        matching.reverse()
        if limit is not None:
            matching = matching[:limit]
        return matching

    def events_in_range(
        self,
        start: float,
        end: float,
        doc_id: Optional[str] = None,
    ) -> list[PinAuditEvent]:
        """Return events with ``start <= timestamp <= end`` (inclusive).

        Sorted ascending by timestamp.  When *doc_id* is given the result
        is additionally restricted to that document.
        """
        with self._lock:
            if doc_id is not None:
                source = [self._events[i] for i in self._by_doc.get(doc_id, [])]
            else:
                source = list(self._events)
        filtered = [ev for ev in source if start <= ev.timestamp <= end]
        filtered.sort(key=lambda ev: ev.timestamp)
        return filtered

    def last_pin_event_for(self, doc_id: str) -> Optional[PinAuditEvent]:
        """Return the most recent ``pin`` or ``renew`` event for *doc_id*.

        Returns ``None`` if no such event exists.
        """
        with self._lock:
            for i in reversed(self._by_doc.get(doc_id, [])):
                ev = self._events[i]
                if ev.action in _PIN_LIKE_ACTIONS:
                    return ev
        return None

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    def most_pinned_docs(self, limit: int = 10) -> list[tuple]:
        """Return ``(doc_id, pin_count)`` pairs sorted by pin count desc.

        ``pin_count`` is the number of events with ``action == "pin"`` for
        the document (``renew`` is not counted).  Ties are broken
        alphabetically by ``doc_id``.  Documents with zero ``pin`` events
        are not included.
        """
        with self._lock:
            counts: dict[str, int] = {}
            for ev in self._events:
                if ev.action == "pin":
                    counts[ev.doc_id] = counts.get(ev.doc_id, 0) + 1
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if limit is not None:
            ordered = ordered[:limit]
        return ordered

    def pin_activity_summary(self) -> dict:
        """Return ``{action: count}`` covering every observed action."""
        summary: dict[str, int] = {}
        with self._lock:
            for ev in self._events:
                summary[ev.action] = summary.get(ev.action, 0) + 1
        return summary

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def delete_old(self, before_timestamp: float) -> int:
        """Remove events with ``timestamp < before_timestamp``.

        Returns the number of removed events.  All secondary indices are
        rebuilt to remain consistent with the surviving events.
        """
        with self._lock:
            keep: list[PinAuditEvent] = []
            removed = 0
            for ev in self._events:
                if ev.timestamp < before_timestamp:
                    removed += 1
                else:
                    keep.append(ev)
            self._events = keep
            self._by_doc.clear()
            self._by_actor.clear()
            for idx, ev in enumerate(self._events):
                self._by_doc.setdefault(ev.doc_id, []).append(idx)
                self._by_actor.setdefault(ev.actor, []).append(idx)
            return removed

    def clear_all(self) -> int:
        """Remove all events.  Returns the number of removed events.

        The next event id counter is also reset back to ``1``.
        """
        with self._lock:
            removed = len(self._events)
            self._events.clear()
            self._by_doc.clear()
            self._by_actor.clear()
            self._next_id = 1
            return removed

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> PinAuditStats:
        """Return aggregate statistics over all recorded events."""
        with self._lock:
            total = len(self._events)
            unique_docs = len(self._by_doc)
            unique_actors = len(self._by_actor)
            action_counts: dict[str, int] = {}
            for ev in self._events:
                action_counts[ev.action] = action_counts.get(ev.action, 0) + 1
        return PinAuditStats(
            total_events=total,
            unique_docs=unique_docs,
            unique_actors=unique_actors,
            action_counts=action_counts,
        )
