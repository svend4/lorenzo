"""E426 DocSubscriptionLog — append-only log of subscription lifecycle events.

Pure stdlib, thread-safe in-memory implementation.
"""
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


SUBSCRIBE_EVENTS = ("subscribe", "reactivate")
UNSUBSCRIBE_EVENTS = ("unsubscribe", "expire")


@dataclass
class SubLogEntry:
    """A single subscription-log entry."""

    entry_id: int = 0
    subscriber_id: str = ""
    event: str = ""
    target: str = ""
    timestamp: float = 0.0
    details: str = ""


@dataclass
class SubLogStats:
    """Aggregated statistics over the log."""

    total_entries: int = 0
    unique_subscribers: int = 0
    unique_targets: int = 0
    event_counts: dict = field(default_factory=dict)


class DocSubscriptionLog:
    """Thread-safe in-memory append-only log of subscription events.

    Events
    ------
    - ``subscribe``  — subscriber starts following a target
    - ``unsubscribe``— subscriber explicitly stops
    - ``reactivate`` — subscriber resumes a previously stopped subscription
    - ``expire``     — subscription auto-expired

    The log preserves insertion order via auto-incrementing :attr:`entry_id`
    starting from ``1``. Secondary indexes are maintained for fast lookups
    by subscriber, target, and event type.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: list[SubLogEntry] = []
        self._by_subscriber: dict[str, list[int]] = {}
        self._by_target: dict[str, list[int]] = {}
        self._by_event: dict[str, list[int]] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _index_of(self, entry_id: int) -> Optional[int]:
        """Binary search for the list index of an entry by entry_id.

        Entries are stored in insertion order with monotonically increasing
        entry_ids, but ``delete_old`` can remove arbitrary entries, leaving
        gaps. Order is preserved either way.
        """
        lo, hi = 0, len(self._entries) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            mid_id = self._entries[mid].entry_id
            if mid_id == entry_id:
                return mid
            if mid_id < entry_id:
                lo = mid + 1
            else:
                hi = mid - 1
        return None

    def _rebuild_indexes(self) -> None:
        """Rebuild all secondary indexes from ``self._entries``."""
        self._by_subscriber = {}
        self._by_target = {}
        self._by_event = {}
        for entry in self._entries:
            self._by_subscriber.setdefault(entry.subscriber_id, []).append(entry.entry_id)
            self._by_target.setdefault(entry.target, []).append(entry.entry_id)
            self._by_event.setdefault(entry.event, []).append(entry.entry_id)

    def _entries_from_ids(self, ids: list[int]) -> list[SubLogEntry]:
        """Resolve a list of entry_ids to entries, preserving order."""
        out: list[SubLogEntry] = []
        for eid in ids:
            idx = self._index_of(eid)
            if idx is not None:
                out.append(self._entries[idx])
        return out

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def log(
        self,
        subscriber_id: str,
        event: str,
        target: str,
        details: str = "",
        now: Optional[float] = None,
    ) -> SubLogEntry:
        """Append a new entry to the log and return it."""
        ts = now if now is not None else time.time()
        with self._lock:
            entry = SubLogEntry(
                entry_id=self._next_id,
                subscriber_id=subscriber_id,
                event=event,
                target=target,
                timestamp=ts,
                details=details,
            )
            self._next_id += 1
            self._entries.append(entry)
            self._by_subscriber.setdefault(subscriber_id, []).append(entry.entry_id)
            self._by_target.setdefault(target, []).append(entry.entry_id)
            self._by_event.setdefault(event, []).append(entry.entry_id)
        return entry

    def get_entry(self, entry_id: int) -> Optional[SubLogEntry]:
        """Return entry by ``entry_id`` or ``None``."""
        with self._lock:
            idx = self._index_of(entry_id)
            if idx is None:
                return None
            return self._entries[idx]

    def entries_for_subscriber(
        self,
        subscriber_id: str,
        event: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[SubLogEntry]:
        """Return entries for a subscriber, most recent first."""
        with self._lock:
            ids = list(self._by_subscriber.get(subscriber_id, ()))
            entries = self._entries_from_ids(ids)
            if event is not None:
                entries = [e for e in entries if e.event == event]
            entries.reverse()  # most recent first
            if limit is not None:
                entries = entries[:limit]
            return entries

    def entries_for_target(
        self,
        target: str,
        limit: Optional[int] = None,
    ) -> list[SubLogEntry]:
        """Return entries for a target, most recent first."""
        with self._lock:
            ids = list(self._by_target.get(target, ()))
            entries = self._entries_from_ids(ids)
            entries.reverse()
            if limit is not None:
                entries = entries[:limit]
            return entries

    def entries_by_event(
        self,
        event: str,
        limit: Optional[int] = None,
    ) -> list[SubLogEntry]:
        """Return entries matching ``event``, most recent first."""
        with self._lock:
            ids = list(self._by_event.get(event, ()))
            entries = self._entries_from_ids(ids)
            entries.reverse()
            if limit is not None:
                entries = entries[:limit]
            return entries

    def entries_in_range(
        self,
        start: float,
        end: float,
        subscriber_id: Optional[str] = None,
    ) -> list[SubLogEntry]:
        """Return entries with ``start <= timestamp <= end`` (inclusive).

        Sorted ascending by timestamp, then by entry_id for stable ordering.
        """
        with self._lock:
            if subscriber_id is not None:
                ids = list(self._by_subscriber.get(subscriber_id, ()))
                pool = self._entries_from_ids(ids)
            else:
                pool = list(self._entries)
            filtered = [e for e in pool if start <= e.timestamp <= end]
            filtered.sort(key=lambda e: (e.timestamp, e.entry_id))
            return filtered

    def is_currently_subscribed(self, subscriber_id: str, target: str) -> bool:
        """Replay the log to determine current subscription state.

        ``subscribe`` / ``reactivate`` set the state to subscribed.
        ``unsubscribe`` / ``expire`` set the state to not subscribed.
        Returns ``False`` if no entries match.
        """
        with self._lock:
            ids = self._by_subscriber.get(subscriber_id, ())
            state = False
            found = False
            for eid in ids:
                idx = self._index_of(eid)
                if idx is None:
                    continue
                entry = self._entries[idx]
                if entry.target != target:
                    continue
                found = True
                if entry.event in SUBSCRIBE_EVENTS:
                    state = True
                elif entry.event in UNSUBSCRIBE_EVENTS:
                    state = False
            return state if found else False

    def last_event_for(
        self,
        subscriber_id: str,
        target: str,
    ) -> Optional[SubLogEntry]:
        """Return the most recent entry matching subscriber+target, or None."""
        with self._lock:
            ids = self._by_subscriber.get(subscriber_id, ())
            last: Optional[SubLogEntry] = None
            for eid in ids:
                idx = self._index_of(eid)
                if idx is None:
                    continue
                entry = self._entries[idx]
                if entry.target == target:
                    last = entry
            return last

    def subscriber_history(self, subscriber_id: str) -> dict:
        """Return mapping of target → current status ('subscribed' / 'not_subscribed')."""
        with self._lock:
            ids = self._by_subscriber.get(subscriber_id, ())
            states: dict = {}
            for eid in ids:
                idx = self._index_of(eid)
                if idx is None:
                    continue
                entry = self._entries[idx]
                if entry.event in SUBSCRIBE_EVENTS:
                    states[entry.target] = "subscribed"
                elif entry.event in UNSUBSCRIBE_EVENTS:
                    states[entry.target] = "not_subscribed"
                else:
                    states.setdefault(entry.target, "not_subscribed")
            return states

    def delete_old(self, before_timestamp: float) -> int:
        """Remove entries with ``timestamp < before_timestamp``.

        Rebuilds secondary indexes. Returns the count of removed entries.
        """
        with self._lock:
            kept: list[SubLogEntry] = []
            removed = 0
            for entry in self._entries:
                if entry.timestamp < before_timestamp:
                    removed += 1
                else:
                    kept.append(entry)
            self._entries = kept
            self._rebuild_indexes()
            return removed

    def stats(self) -> SubLogStats:
        """Return aggregate statistics over all current entries."""
        with self._lock:
            event_counts: dict = {}
            for entry in self._entries:
                event_counts[entry.event] = event_counts.get(entry.event, 0) + 1
            return SubLogStats(
                total_entries=len(self._entries),
                unique_subscribers=len(self._by_subscriber),
                unique_targets=len(self._by_target),
                event_counts=event_counts,
            )
