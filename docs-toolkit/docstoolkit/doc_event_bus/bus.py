"""Internal document event bus with sync and async dispatch.

Provides:
- ``EventPriority`` and ``DispatchMode`` enums.
- ``Event`` and ``Subscription`` dataclasses.
- ``BusStats`` snapshot dataclass.
- ``DocEventBus`` — pub/sub bus with topic patterns (``*`` and ``#``
  wildcards), middleware chain, handler ordering, and an async queue
  flushed via :meth:`DocEventBus.flush_async`.

Stdlib only: ``threading`` for locks, ``queue`` for the async queue.
"""

from __future__ import annotations

import queue
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional


class EventPriority(Enum):
    """Priority levels for published events."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


class DispatchMode(Enum):
    """Dispatch modes for subscribers."""

    SYNC = "sync"
    ASYNC = "async"


@dataclass
class Event:
    """A single document event."""

    event_id: int
    topic: str
    data: dict
    timestamp: float = 0.0
    priority: EventPriority = EventPriority.NORMAL
    source: Optional[str] = None


@dataclass
class Subscription:
    """Subscription record."""

    sub_id: str
    topic_pattern: str
    handler: Callable
    priority: int = 0
    mode: DispatchMode = DispatchMode.SYNC
    enabled: bool = True


@dataclass
class BusStats:
    """Snapshot of bus statistics."""

    total_events: int
    total_subscriptions: int
    total_dispatched: int
    total_errors: int
    by_topic: Dict[str, int] = field(default_factory=dict)


class DocEventBus:
    """Thread-safe internal document event bus.

    Supports:
    - Wildcard topic patterns: ``*`` (single segment), ``#`` (multi-segment).
    - Middleware chain that can transform or drop events.
    - Sync subscribers run inline during :meth:`publish`.
    - Async subscribers are enqueued; :meth:`flush_async` drains the queue.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: Dict[str, Subscription] = {}
        self._middlewares: Dict[int, Callable[[Event], Optional[Event]]] = {}
        self._async_queue: "queue.Queue[tuple[Subscription, Event]]" = queue.Queue()
        self._sub_counter = 0
        self._mw_counter = 0
        self._event_counter = 0
        self._total_events = 0
        self._total_dispatched = 0
        self._total_errors = 0
        self._by_topic: Dict[str, int] = {}

    # ------------------------------------------------------------------ subs

    def subscribe(
        self,
        topic_pattern: str,
        handler: Callable,
        mode: DispatchMode = DispatchMode.SYNC,
        priority: int = 0,
    ) -> str:
        """Register a subscriber and return its ``sub_id``."""
        with self._lock:
            self._sub_counter += 1
            sub_id = f"sub-{self._sub_counter}"
            self._subs[sub_id] = Subscription(
                sub_id=sub_id,
                topic_pattern=topic_pattern,
                handler=handler,
                priority=priority,
                mode=mode,
                enabled=True,
            )
            return sub_id

    def unsubscribe(self, sub_id: str) -> bool:
        with self._lock:
            return self._subs.pop(sub_id, None) is not None

    def enable_subscription(self, sub_id: str) -> bool:
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.enabled = True
            return True

    def disable_subscription(self, sub_id: str) -> bool:
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.enabled = False
            return True

    # ------------------------------------------------------------ middleware

    def add_middleware(
        self, middleware: Callable[[Event], Optional[Event]]
    ) -> int:
        """Register a middleware; returns its numeric id."""
        with self._lock:
            self._mw_counter += 1
            mw_id = self._mw_counter
            self._middlewares[mw_id] = middleware
            return mw_id

    def remove_middleware(self, middleware_id: int) -> bool:
        with self._lock:
            return self._middlewares.pop(middleware_id, None) is not None

    # ---------------------------------------------------------------- match

    @staticmethod
    def matches(topic: str, pattern: str) -> bool:
        """Return True iff ``topic`` matches ``pattern``.

        Pattern grammar: dot-separated segments. ``*`` matches exactly one
        segment, ``#`` matches one or more segments. A pattern that is
        exactly ``#`` matches any non-empty topic.
        """
        if pattern == topic:
            return True
        if pattern == "#":
            return bool(topic)

        topic_parts = topic.split(".")
        pat_parts = pattern.split(".")

        return _match_parts(topic_parts, pat_parts)

    # -------------------------------------------------------------- publish

    def publish(
        self,
        topic: str,
        data: dict,
        priority: EventPriority = EventPriority.NORMAL,
        source: Optional[str] = None,
        now: float = 0.0,
    ) -> Event:
        """Publish an event and dispatch to matching subscribers."""
        with self._lock:
            self._event_counter += 1
            event = Event(
                event_id=self._event_counter,
                topic=topic,
                data=data,
                timestamp=now,
                priority=priority,
                source=source,
            )
            self._total_events += 1
            self._by_topic[topic] = self._by_topic.get(topic, 0) + 1
            middlewares = list(self._middlewares.values())

        # Run middleware chain outside the main lock.
        current: Optional[Event] = event
        for mw in middlewares:
            current = mw(current)
            if current is None:
                return event  # filtered out; still return original
        event = current

        subs = self.subscribers_for(topic, enabled_only=True)
        for sub in subs:
            if sub.mode == DispatchMode.SYNC:
                self._invoke_sync(sub, event)
            else:
                self._async_queue.put((sub, event))
        return event

    def publish_sync_only(self, topic: str, data: dict, **kwargs) -> int:
        """Publish but only dispatch to SYNC subscribers.

        Returns the number of SYNC subscribers invoked. Middleware still runs;
        async subscribers are skipped entirely.
        """
        with self._lock:
            self._event_counter += 1
            event = Event(
                event_id=self._event_counter,
                topic=topic,
                data=data,
                timestamp=kwargs.get("now", 0.0),
                priority=kwargs.get("priority", EventPriority.NORMAL),
                source=kwargs.get("source"),
            )
            self._total_events += 1
            self._by_topic[topic] = self._by_topic.get(topic, 0) + 1
            middlewares = list(self._middlewares.values())

        current: Optional[Event] = event
        for mw in middlewares:
            current = mw(current)
            if current is None:
                return 0
        event = current

        count = 0
        for sub in self.subscribers_for(topic, enabled_only=True):
            if sub.mode == DispatchMode.SYNC:
                self._invoke_sync(sub, event)
                count += 1
        return count

    # ---------------------------------------------------------------- async

    def flush_async(self) -> int:
        """Process all queued async events. Returns number dispatched."""
        count = 0
        while True:
            try:
                sub, event = self._async_queue.get_nowait()
            except queue.Empty:
                break
            self._invoke_sync(sub, event)
            count += 1
        return count

    def pending_async_count(self) -> int:
        return self._async_queue.qsize()

    # ---------------------------------------------------------------- query

    def subscribers_for(
        self, topic: str, enabled_only: bool = True
    ) -> List[Subscription]:
        """Return matching subscribers ordered by descending priority."""
        with self._lock:
            subs = [
                sub
                for sub in self._subs.values()
                if (not enabled_only or sub.enabled)
                and self.matches(topic, sub.topic_pattern)
            ]
        subs.sort(key=lambda s: (-s.priority, s.sub_id))
        return subs

    @property
    def event_count(self) -> int:
        with self._lock:
            return self._total_events

    @property
    def subscription_count(self) -> int:
        with self._lock:
            return len(self._subs)

    def stats(self) -> BusStats:
        with self._lock:
            return BusStats(
                total_events=self._total_events,
                total_subscriptions=len(self._subs),
                total_dispatched=self._total_dispatched,
                total_errors=self._total_errors,
                by_topic=dict(self._by_topic),
            )

    def clear(self) -> None:
        """Reset all subscriptions, middleware, queue, and counters."""
        with self._lock:
            self._subs.clear()
            self._middlewares.clear()
            self._sub_counter = 0
            self._mw_counter = 0
            self._event_counter = 0
            self._total_events = 0
            self._total_dispatched = 0
            self._total_errors = 0
            self._by_topic.clear()
        # Drain queue.
        while True:
            try:
                self._async_queue.get_nowait()
            except queue.Empty:
                break

    # --------------------------------------------------------------- helper

    def _invoke_sync(self, sub: Subscription, event: Event) -> None:
        try:
            sub.handler(event)
        except Exception:
            with self._lock:
                self._total_errors += 1
            return
        with self._lock:
            self._total_dispatched += 1


def _match_parts(topic_parts: List[str], pat_parts: List[str]) -> bool:
    """Recursive matcher for dot-separated segments.

    ``*`` matches exactly one segment; ``#`` matches one or more segments.
    """
    # Base cases.
    if not pat_parts:
        return not topic_parts
    if not topic_parts:
        # Remaining pattern can only match if every leftover token is ``#``
        # consuming one-or-more, which requires at least one topic token.
        return False

    head, *rest = pat_parts

    if head == "#":
        if not rest:
            # Trailing # matches the remaining (non-empty) tail.
            return len(topic_parts) >= 1
        # Try consuming 1..N topic tokens for this #.
        for i in range(1, len(topic_parts) + 1):
            if _match_parts(topic_parts[i:], rest):
                return True
        return False

    if head == "*":
        return _match_parts(topic_parts[1:], rest)

    if head == topic_parts[0]:
        return _match_parts(topic_parts[1:], rest)

    return False
