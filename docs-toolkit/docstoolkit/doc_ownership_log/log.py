"""E440 DocOwnershipLog — append-only log of ownership transfers.

Stores :class:`OwnershipEvent` records describing ownership lifecycle events
(assign, transfer, revoke, co_assign, co_revoke) against documents.  All
operations are thread-safe.  Pure stdlib, no third-party dependencies.
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
class OwnershipEvent:
    """A single ownership event."""

    event_id: int
    doc_id: str
    action: str
    actor: str
    subject: str
    previous_owner: Optional[str] = None
    timestamp: float = 0.0
    note: str = ""


@dataclass
class OwnershipStats:
    """Aggregate statistics over all logged ownership events."""

    total_events: int
    unique_docs: int
    unique_actors: int
    unique_subjects: int
    action_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocOwnershipLog
# ---------------------------------------------------------------------------


VALID_ACTIONS = {"assign", "transfer", "revoke", "co_assign", "co_revoke"}


class DocOwnershipLog:
    """Thread-safe append-only log of document ownership events."""

    def __init__(self) -> None:
        self._events: list[OwnershipEvent] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_subject: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def log_event(
        self,
        doc_id: str,
        action: str,
        actor: str,
        subject: str,
        previous_owner: Optional[str] = None,
        note: str = "",
        now: Optional[float] = None,
    ) -> OwnershipEvent:
        """Append a new ownership event and return it."""
        if action not in VALID_ACTIONS:
            raise ValueError(
                f"invalid action {action!r}; expected one of {sorted(VALID_ACTIONS)}"
            )
        ts = now if now is not None else time.time()
        with self._lock:
            event_id = self._next_id
            self._next_id += 1
            event = OwnershipEvent(
                event_id=event_id,
                doc_id=doc_id,
                action=action,
                actor=actor,
                subject=subject,
                previous_owner=previous_owner,
                timestamp=ts,
                note=note,
            )
            self._events.append(event)
            self._by_doc.setdefault(doc_id, []).append(event_id)
            self._by_subject.setdefault(subject, []).append(event_id)
            return event

    def delete_old(self, before_timestamp: float) -> int:
        """Delete events with timestamp < before_timestamp.  Returns number deleted."""
        with self._lock:
            keep: list[OwnershipEvent] = []
            removed = 0
            for ev in self._events:
                if ev.timestamp < before_timestamp:
                    removed += 1
                else:
                    keep.append(ev)
            if removed == 0:
                return 0
            self._events = keep
            # Rebuild indexes
            self._by_doc = {}
            self._by_subject = {}
            for ev in self._events:
                self._by_doc.setdefault(ev.doc_id, []).append(ev.event_id)
                self._by_subject.setdefault(ev.subject, []).append(ev.event_id)
            return removed

    def clear_all(self) -> int:
        """Remove all events and reset id counter.  Returns previous count."""
        with self._lock:
            count = len(self._events)
            self._events = []
            self._by_doc = {}
            self._by_subject = {}
            self._next_id = 1
            return count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def get_event(self, event_id: int) -> Optional[OwnershipEvent]:
        """Return the event with the given id, or None."""
        with self._lock:
            # event_ids are 1-based and dense, but allow deletion gaps
            for ev in self._events:
                if ev.event_id == event_id:
                    return ev
            return None

    def events_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[OwnershipEvent]:
        """Return events for a doc, most recent first."""
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            # Map ids back to events; _events is append-order so id->event direct lookup
            id_to_event = {ev.event_id: ev for ev in self._events}
            evs = [id_to_event[i] for i in ids if i in id_to_event]
            evs.sort(key=lambda e: e.event_id, reverse=True)
            if limit is not None:
                evs = evs[:limit]
            return evs

    def events_for_subject(
        self, subject: str, limit: Optional[int] = None
    ) -> list[OwnershipEvent]:
        """Return events for a subject (affected user), most recent first."""
        with self._lock:
            ids = self._by_subject.get(subject, [])
            id_to_event = {ev.event_id: ev for ev in self._events}
            evs = [id_to_event[i] for i in ids if i in id_to_event]
            evs.sort(key=lambda e: e.event_id, reverse=True)
            if limit is not None:
                evs = evs[:limit]
            return evs

    def events_by_action(
        self, action: str, limit: Optional[int] = None
    ) -> list[OwnershipEvent]:
        """Return all events with the given action, most recent first."""
        with self._lock:
            evs = [ev for ev in self._events if ev.action == action]
            evs.sort(key=lambda e: e.event_id, reverse=True)
            if limit is not None:
                evs = evs[:limit]
            return evs

    def events_in_range(
        self,
        start: float,
        end: float,
        doc_id: Optional[str] = None,
    ) -> list[OwnershipEvent]:
        """Return events in [start, end] (inclusive), sorted ascending by event_id.

        If doc_id is given, filter to that document only.
        """
        with self._lock:
            if doc_id is not None:
                ids = self._by_doc.get(doc_id, [])
                id_to_event = {ev.event_id: ev for ev in self._events}
                source = [id_to_event[i] for i in ids if i in id_to_event]
            else:
                source = list(self._events)
            evs = [ev for ev in source if start <= ev.timestamp <= end]
            evs.sort(key=lambda e: e.event_id)
            return evs

    def last_assign_for(self, doc_id: str) -> Optional[OwnershipEvent]:
        """Return the most recent assign/transfer event for a doc, or None."""
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            id_to_event = {ev.event_id: ev for ev in self._events}
            evs = [id_to_event[i] for i in ids if i in id_to_event]
            evs.sort(key=lambda e: e.event_id, reverse=True)
            for ev in evs:
                if ev.action in ("assign", "transfer"):
                    return ev
            return None

    def owners_of(self, doc_id: str) -> list[str]:
        """Replay events for a doc and return current owner list.

        Semantics:
            assign     → set primary (clears prior primary if any), keeps co-owners
            transfer   → replace primary
            revoke     → remove primary
            co_assign  → add co-owner
            co_revoke  → remove co-owner
        Primary owner is index 0 if present; co-owners follow in insertion order.
        """
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            id_to_event = {ev.event_id: ev for ev in self._events}
            evs = [id_to_event[i] for i in ids if i in id_to_event]
            evs.sort(key=lambda e: e.event_id)

            primary: Optional[str] = None
            co_owners: list[str] = []

            for ev in evs:
                if ev.action == "assign":
                    primary = ev.subject
                    if ev.subject in co_owners:
                        co_owners = [c for c in co_owners if c != ev.subject]
                elif ev.action == "transfer":
                    primary = ev.subject
                    if ev.subject in co_owners:
                        co_owners = [c for c in co_owners if c != ev.subject]
                elif ev.action == "revoke":
                    if primary == ev.subject:
                        primary = None
                elif ev.action == "co_assign":
                    if ev.subject != primary and ev.subject not in co_owners:
                        co_owners.append(ev.subject)
                elif ev.action == "co_revoke":
                    co_owners = [c for c in co_owners if c != ev.subject]

            result: list[str] = []
            if primary is not None:
                result.append(primary)
            result.extend(co_owners)
            return result

    def stats(self) -> OwnershipStats:
        """Return aggregate statistics."""
        with self._lock:
            total = len(self._events)
            unique_docs = len({ev.doc_id for ev in self._events})
            unique_actors = len({ev.actor for ev in self._events})
            unique_subjects = len({ev.subject for ev in self._events})
            action_counts: dict[str, int] = {}
            for ev in self._events:
                action_counts[ev.action] = action_counts.get(ev.action, 0) + 1
            return OwnershipStats(
                total_events=total,
                unique_docs=unique_docs,
                unique_actors=unique_actors,
                unique_subjects=unique_subjects,
                action_counts=action_counts,
            )
