"""E338 DocPubSubBus — implementation."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class PubSubEvent:
    """A single event dispatched on the bus."""

    event_id: int = 0
    event_type: str = ""
    doc_id: Optional[str] = None
    payload: dict = field(default_factory=dict)
    published_at: float = 0.0


@dataclass
class SubscriberInfo:
    """Info about a registered subscriber."""

    sub_id: str = ""
    event_pattern: str = ""
    subscribed_at: float = 0.0
    delivery_count: int = 0


@dataclass
class PubSubStats:
    """Aggregate statistics for the bus."""

    total_events: int = 0
    total_subscribers: int = 0
    total_deliveries: int = 0


class DocPubSubBus:
    """In-process publish/subscribe bus with wildcard subscriptions.

    Thread-safe via an internal lock. Callbacks fire OUTSIDE the lock so a
    slow subscriber does not block other publishers.
    """

    def __init__(self) -> None:
        self._events: list[PubSubEvent] = []
        self._subscribers: dict[str, tuple[SubscriberInfo, Callable[[PubSubEvent], None]]] = {}
        self._next_event_id: int = 1
        self._total_deliveries: int = 0
        self._lock = threading.Lock()

    # ---------------------------- subscriptions ----------------------------

    def subscribe(
        self,
        event_pattern: str,
        callback: Callable[[PubSubEvent], None],
        now: Optional[float] = None,
    ) -> SubscriberInfo:
        """Register a subscriber. Returns SubscriberInfo with new UUID."""
        ts = now if now is not None else time.time()
        info = SubscriberInfo(
            sub_id=str(uuid.uuid4()),
            event_pattern=event_pattern,
            subscribed_at=ts,
            delivery_count=0,
        )
        with self._lock:
            self._subscribers[info.sub_id] = (info, callback)
        return info

    def unsubscribe(self, sub_id: str) -> bool:
        """Remove subscriber. Return True if it existed."""
        with self._lock:
            if sub_id in self._subscribers:
                del self._subscribers[sub_id]
                return True
            return False

    # ---------------------------- publishing ----------------------------

    def publish(
        self,
        event_type: str,
        doc_id: Optional[str] = None,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> PubSubEvent:
        """Publish an event. Callbacks fire outside the lock."""
        ts = now if now is not None else time.time()
        with self._lock:
            event = PubSubEvent(
                event_id=self._next_event_id,
                event_type=event_type,
                doc_id=doc_id,
                payload=dict(payload) if payload else {},
                published_at=ts,
            )
            self._next_event_id += 1
            self._events.append(event)

            # Snapshot matching subscribers for delivery outside the lock.
            to_deliver: list[tuple[SubscriberInfo, Callable[[PubSubEvent], None]]] = []
            for info, cb in self._subscribers.values():
                if info.event_pattern == "*" or info.event_pattern == event_type:
                    info.delivery_count += 1
                    self._total_deliveries += 1
                    to_deliver.append((info, cb))

        # Deliver outside the lock.
        for _info, cb in to_deliver:
            try:
                cb(event)
            except Exception:
                # Best-effort delivery; swallow subscriber errors.
                pass

        return event

    # ---------------------------- queries ----------------------------

    def get_event(self, event_id: int) -> Optional[PubSubEvent]:
        with self._lock:
            for ev in self._events:
                if ev.event_id == event_id:
                    return ev
            return None

    def events_by_type(self, event_type: str, limit: Optional[int] = None) -> list[PubSubEvent]:
        with self._lock:
            matching = [ev for ev in self._events if ev.event_type == event_type]
        matching.sort(key=lambda e: e.published_at)
        if limit is not None:
            matching = matching[:limit]
        return matching

    def events_for_doc(self, doc_id: str, limit: Optional[int] = None) -> list[PubSubEvent]:
        with self._lock:
            matching = [ev for ev in self._events if ev.doc_id == doc_id]
        matching.sort(key=lambda e: e.published_at)
        if limit is not None:
            matching = matching[:limit]
        return matching

    def recent_events(self, limit: int = 10) -> list[PubSubEvent]:
        """Tail of history, most recent first."""
        with self._lock:
            snapshot = list(self._events)
        snapshot.sort(key=lambda e: e.published_at, reverse=True)
        return snapshot[:limit]

    def list_subscribers(self) -> list[SubscriberInfo]:
        with self._lock:
            infos = [info for info, _cb in self._subscribers.values()]
        infos.sort(key=lambda s: s.sub_id)
        return infos

    def subscriber_count_for(self, event_type: str) -> int:
        with self._lock:
            return sum(
                1
                for info, _cb in self._subscribers.values()
                if info.event_pattern == "*" or info.event_pattern == event_type
            )

    # ---------------------------- maintenance ----------------------------

    def clear_history(self) -> int:
        """Drop all events. Subscribers are preserved. Return removed count."""
        with self._lock:
            count = len(self._events)
            self._events.clear()
            return count

    def stats(self) -> PubSubStats:
        with self._lock:
            return PubSubStats(
                total_events=len(self._events),
                total_subscribers=len(self._subscribers),
                total_deliveries=self._total_deliveries,
            )
