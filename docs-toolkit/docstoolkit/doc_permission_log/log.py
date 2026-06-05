"""Append-only permission audit log for grant/deny/revoke events.

Thread-safe, pure stdlib, in-memory implementation (E296).
"""
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class PermissionEvent:
    """A single permission change event."""

    event_id: int
    doc_id: str
    principal: str
    action: str        # "read", "write", "delete", etc.
    event_type: str    # "grant", "deny", "revoke"
    granted_by: str
    timestamp: float
    reason: str = ""


@dataclass
class PermissionSummary:
    """Aggregated state for a (doc_id, principal) relationship."""

    doc_id: str
    principal: str
    current_state: Optional[str]   # "grant", "deny", or None (revoked/unknown)
    last_event_at: float
    event_count: int


@dataclass
class PermLogStats:
    """Aggregate statistics over the full log."""

    total_events: int
    total_docs: int
    total_principals: int
    event_type_counts: Dict[str, int]  # "grant"/"deny"/"revoke" -> count


class DocPermissionLog:
    """Append-only, thread-safe in-memory log of permission events.

    Events are stored with auto-incrementing integer IDs.  All mutating
    operations hold ``_lock``; readers also hold ``_lock`` to obtain a
    consistent snapshot.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: List[PermissionEvent] = []
        self._next_id: int = 1
        # Fast-lookup index: event_id -> PermissionEvent
        self._by_id: Dict[int, PermissionEvent] = {}
        # Index: doc_id -> list[PermissionEvent]
        self._by_doc: Dict[str, List[PermissionEvent]] = {}
        # Index: principal -> list[PermissionEvent]
        self._by_principal: Dict[str, List[PermissionEvent]] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def log(
        self,
        doc_id: str,
        principal: str,
        action: str,
        event_type: str,
        granted_by: str = "",
        reason: str = "",
        now: Optional[float] = None,
    ) -> PermissionEvent:
        """Append a permission event and return it.

        Parameters
        ----------
        doc_id:
            Identifier of the document the permission concerns.
        principal:
            Identity (user, role, service account …) whose permission is
            being modified.
        action:
            Permission action, e.g. ``"read"``, ``"write"``, ``"delete"``.
        event_type:
            One of ``"grant"``, ``"deny"``, or ``"revoke"``.
        granted_by:
            Identity of the actor making the change (auditor).
        reason:
            Human-readable explanation for the change (optional).
        now:
            Override the event timestamp (useful in tests).  When ``None``
            the method uses ``0.0`` as a sentinel — callers that need real
            wall-clock time should pass ``time.time()``.
        """
        timestamp = 0.0 if now is None else now
        with self._lock:
            event = PermissionEvent(
                event_id=self._next_id,
                doc_id=doc_id,
                principal=principal,
                action=action,
                event_type=event_type,
                granted_by=granted_by,
                timestamp=timestamp,
                reason=reason,
            )
            self._next_id += 1
            self._events.append(event)
            self._by_id[event.event_id] = event
            self._by_doc.setdefault(doc_id, []).append(event)
            self._by_principal.setdefault(principal, []).append(event)
            return event

    # ------------------------------------------------------------------
    # Point lookups
    # ------------------------------------------------------------------

    def get_event(self, event_id: int) -> Optional[PermissionEvent]:
        """Return the event with *event_id*, or ``None`` if not found."""
        with self._lock:
            return self._by_id.get(event_id)

    # ------------------------------------------------------------------
    # Filtered queries  (newest first)
    # ------------------------------------------------------------------

    def events_for_doc(
        self,
        doc_id: str,
        principal: Optional[str] = None,
    ) -> List[PermissionEvent]:
        """Return events for *doc_id*, optionally filtered by *principal*.

        Results are ordered newest-first (by insertion order, which
        reflects ``log()`` call order).
        """
        with self._lock:
            events = list(self._by_doc.get(doc_id, []))
        if principal is not None:
            events = [e for e in events if e.principal == principal]
        return list(reversed(events))

    def events_for_principal(
        self,
        principal: str,
        doc_id: Optional[str] = None,
    ) -> List[PermissionEvent]:
        """Return events for *principal*, optionally filtered by *doc_id*.

        Results are ordered newest-first.
        """
        with self._lock:
            events = list(self._by_principal.get(principal, []))
        if doc_id is not None:
            events = [e for e in events if e.doc_id == doc_id]
        return list(reversed(events))

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def current_state(
        self,
        doc_id: str,
        principal: str,
        action: str,
    ) -> Optional[str]:
        """Return the most recent ``event_type`` for *(doc, principal, action)*.

        Returns ``None`` when no event has been recorded for this
        triple.
        """
        with self._lock:
            candidates = self._by_doc.get(doc_id, [])
        # Walk backwards (most-recent first) over the full doc list
        for event in reversed(candidates):
            if event.principal == principal and event.action == action:
                return event.event_type
        return None

    def summary(
        self,
        doc_id: str,
        principal: str,
    ) -> Optional["PermissionSummary"]:
        """Return a :class:`PermissionSummary` for *(doc_id, principal)*.

        Returns ``None`` if no events exist for this pair.
        """
        with self._lock:
            candidates = [
                e
                for e in self._by_doc.get(doc_id, [])
                if e.principal == principal
            ]
        if not candidates:
            return None
        last = candidates[-1]
        return PermissionSummary(
            doc_id=doc_id,
            principal=principal,
            current_state=last.event_type if last.event_type != "revoke" else None,
            last_event_at=last.timestamp,
            event_count=len(candidates),
        )

    def has_permission(
        self,
        doc_id: str,
        principal: str,
        action: str,
    ) -> bool:
        """Return ``True`` iff the current state for *(doc, principal, action)* is ``"grant"``."""
        return self.current_state(doc_id, principal, action) == "grant"

    def docs_where_granted(self, principal: str, action: str) -> List[str]:
        """Return sorted list of doc_ids where *principal* currently has a grant for *action*."""
        with self._lock:
            all_docs = list(self._by_doc.keys())
        result = []
        for doc_id in all_docs:
            if self.current_state(doc_id, principal, action) == "grant":
                result.append(doc_id)
        return sorted(result)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> PermLogStats:
        """Return aggregate statistics over all events."""
        with self._lock:
            total = len(self._events)
            total_docs = len(self._by_doc)
            total_principals = len(self._by_principal)
            counts: Dict[str, int] = {}
            for event in self._events:
                counts[event.event_type] = counts.get(event.event_type, 0) + 1
        return PermLogStats(
            total_events=total,
            total_docs=total_docs,
            total_principals=total_principals,
            event_type_counts=counts,
        )

    # ------------------------------------------------------------------
    # Property
    # ------------------------------------------------------------------

    @property
    def total_events(self) -> int:
        """Total number of events currently stored."""
        with self._lock:
            return len(self._events)
