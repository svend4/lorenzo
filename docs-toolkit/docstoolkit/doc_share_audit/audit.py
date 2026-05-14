"""E402 DocShareAudit core implementation.

Auditable, append-only-ish event log for document share/unshare actions.
Pure stdlib, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ShareEvent:
    """A single share/unshare audit event."""

    event_id: int = 0
    doc_id: str = ""
    actor: str = ""
    target: str = ""
    action: str = ""
    permissions: list[str] = field(default_factory=list)
    timestamp: float = 0.0
    note: str = ""


@dataclass
class AuditStats:
    """Aggregate statistics over the audit log."""

    total_events: int = 0
    unique_docs: int = 0
    unique_actors: int = 0
    unique_targets: int = 0
    action_counts: dict = field(default_factory=dict)


class DocShareAudit:
    """Auditable sharing event log for documents."""

    def __init__(self) -> None:
        self._events: list[ShareEvent] = []
        self._by_doc: dict[str, list[int]] = {}
        self._by_actor: dict[str, list[int]] = {}
        self._by_target: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------
    def log_event(
        self,
        doc_id: str,
        actor: str,
        target: str,
        action: str,
        permissions: Optional[list[str]] = None,
        note: str = "",
        now: Optional[float] = None,
    ) -> ShareEvent:
        """Append a new share-audit event and return it."""
        with self._lock:
            event_id = self._next_id
            self._next_id += 1
            ts = now if now is not None else time.time()
            perms = list(permissions) if permissions else []
            event = ShareEvent(
                event_id=event_id,
                doc_id=doc_id,
                actor=actor,
                target=target,
                action=action,
                permissions=perms,
                timestamp=ts,
                note=note,
            )
            idx = len(self._events)
            self._events.append(event)
            self._by_doc.setdefault(doc_id, []).append(idx)
            self._by_actor.setdefault(actor, []).append(idx)
            self._by_target.setdefault(target, []).append(idx)
            return event

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------
    def get_event(self, event_id: int) -> Optional[ShareEvent]:
        """Return event with given id, or ``None``."""
        with self._lock:
            # event_id is 1-based and ids are monotonic, so we can index directly
            # when no deletions have happened. After delete_old the ids are
            # preserved but positions shift, so fall back to scan.
            if 1 <= event_id <= len(self._events):
                candidate = self._events[event_id - 1]
                if candidate.event_id == event_id:
                    return candidate
            for ev in self._events:
                if ev.event_id == event_id:
                    return ev
            return None

    def _collect(
        self,
        idx_list: list[int],
        action: Optional[str],
        limit: Optional[int],
    ) -> list[ShareEvent]:
        """Helper: gather events by index list, newest first, filter+limit."""
        result: list[ShareEvent] = []
        for i in reversed(idx_list):
            ev = self._events[i]
            if action is not None and ev.action != action:
                continue
            result.append(ev)
            if limit is not None and len(result) >= limit:
                break
        return result

    def events_for_doc(
        self,
        doc_id: str,
        action: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[ShareEvent]:
        """Return events for ``doc_id``, most recent first."""
        with self._lock:
            idxs = self._by_doc.get(doc_id, [])
            return self._collect(idxs, action, limit)

    def events_for_actor(
        self,
        actor: str,
        limit: Optional[int] = None,
    ) -> list[ShareEvent]:
        """Return events authored by ``actor``, most recent first."""
        with self._lock:
            idxs = self._by_actor.get(actor, [])
            return self._collect(idxs, None, limit)

    def events_for_target(
        self,
        target: str,
        limit: Optional[int] = None,
    ) -> list[ShareEvent]:
        """Return events affecting ``target``, most recent first."""
        with self._lock:
            idxs = self._by_target.get(target, [])
            return self._collect(idxs, None, limit)

    def events_by_action(
        self,
        action: str,
        limit: Optional[int] = None,
    ) -> list[ShareEvent]:
        """Return all events with given action, most recent first."""
        with self._lock:
            result: list[ShareEvent] = []
            for ev in reversed(self._events):
                if ev.action != action:
                    continue
                result.append(ev)
                if limit is not None and len(result) >= limit:
                    break
            return result

    def events_in_range(
        self,
        start_time: float,
        end_time: float,
        doc_id: Optional[str] = None,
    ) -> list[ShareEvent]:
        """Return events with ``start_time <= timestamp <= end_time``, ascending."""
        with self._lock:
            if doc_id is not None:
                source = [self._events[i] for i in self._by_doc.get(doc_id, [])]
            else:
                source = list(self._events)
            filtered = [
                ev for ev in source if start_time <= ev.timestamp <= end_time
            ]
            filtered.sort(key=lambda e: e.timestamp)
            return filtered

    # ------------------------------------------------------------------
    # Replay
    # ------------------------------------------------------------------
    def current_shares(self, doc_id: str) -> dict:
        """Replay events for ``doc_id`` and return current target → permissions."""
        with self._lock:
            idxs = self._by_doc.get(doc_id, [])
            events_sorted = sorted(
                (self._events[i] for i in idxs),
                key=lambda e: (e.timestamp, e.event_id),
            )
            current: dict[str, list[str]] = {}
            for ev in events_sorted:
                if ev.action in ("share", "modify"):
                    current[ev.target] = list(ev.permissions)
                elif ev.action in ("unshare", "revoke"):
                    current.pop(ev.target, None)
            return current

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------
    def delete_old(self, before_timestamp: float) -> int:
        """Drop events with ``timestamp < before_timestamp``; rebuild indexes."""
        with self._lock:
            keep: list[ShareEvent] = []
            removed = 0
            for ev in self._events:
                if ev.timestamp < before_timestamp:
                    removed += 1
                else:
                    keep.append(ev)
            self._events = keep
            self._by_doc.clear()
            self._by_actor.clear()
            self._by_target.clear()
            for i, ev in enumerate(self._events):
                self._by_doc.setdefault(ev.doc_id, []).append(i)
                self._by_actor.setdefault(ev.actor, []).append(i)
                self._by_target.setdefault(ev.target, []).append(i)
            return removed

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def stats(self) -> AuditStats:
        """Return aggregate statistics."""
        with self._lock:
            action_counts: dict[str, int] = {}
            for ev in self._events:
                action_counts[ev.action] = action_counts.get(ev.action, 0) + 1
            return AuditStats(
                total_events=len(self._events),
                unique_docs=len(self._by_doc),
                unique_actors=len(self._by_actor),
                unique_targets=len(self._by_target),
                action_counts=action_counts,
            )
