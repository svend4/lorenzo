"""Circular event buffer with replay, filtering, and time-window queries (E167).

Provides a thread-safe in-memory event buffer with bounded capacity using
``collections.deque(maxlen=capacity)``. Events are auto-assigned a sequential
``event_id``. Subscribers fire on push (not pop) and are invoked outside the
internal lock to avoid deadlocks.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class BufferEvent:
    """A single event held in the :class:`EventBuffer`."""

    event_id: int
    event_type: str
    timestamp: float
    data: dict = field(default_factory=dict)
    source: Optional[str] = None


@dataclass
class BufferStats:
    """Snapshot of buffer statistics."""

    total_capacity: int
    current_size: int
    dropped_count: int
    event_types: dict


class EventBuffer:
    """Thread-safe circular event buffer.

    The buffer holds up to ``capacity`` events. When pushing past the capacity,
    the oldest event is evicted and ``dropped_count`` is incremented.

    Subscribers registered via :meth:`subscribe` are invoked once per push
    (not on pop). Callbacks run outside the internal lock so subscribers can
    safely call back into the buffer without deadlocking.
    """

    def __init__(self, capacity: int = 1000) -> None:
        if not isinstance(capacity, int):
            raise TypeError("capacity must be an int")
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        self._capacity = capacity
        # deque(maxlen=0) silently drops everything, which is what we want.
        self._events: deque = deque(maxlen=capacity)
        self._lock = threading.Lock()
        self._next_id = 0
        self._dropped = 0
        self._subs: dict = {}
        self._next_sub_id = 0

    # -- push --------------------------------------------------------------------
    def push(
        self,
        event_type: str,
        data: Optional[dict] = None,
        source: Optional[str] = None,
        now: float = 0.0,
    ) -> BufferEvent:
        """Build and push a new event. Returns the constructed :class:`BufferEvent`."""
        with self._lock:
            event = BufferEvent(
                event_id=self._next_id,
                event_type=event_type,
                timestamp=float(now),
                data=dict(data) if data else {},
                source=source,
            )
            self._next_id += 1
            self._record_locked(event)
            subs = list(self._subs.values())
        self._fire_subs(subs, event)
        return event

    def push_event(self, event: BufferEvent) -> None:
        """Push a pre-built event. The buffer reassigns its ``event_id``."""
        if not isinstance(event, BufferEvent):
            raise TypeError("event must be a BufferEvent")
        with self._lock:
            event.event_id = self._next_id
            self._next_id += 1
            self._record_locked(event)
            subs = list(self._subs.values())
        self._fire_subs(subs, event)

    def _record_locked(self, event: BufferEvent) -> None:
        """Append *event* to the deque, tracking drops. Caller must hold the lock."""
        if self._capacity == 0:
            # Nothing can be stored; the push itself is the drop.
            self._dropped += 1
            return
        if len(self._events) == self._capacity:
            self._dropped += 1
        self._events.append(event)

    def _fire_subs(self, subs: list, event: BufferEvent) -> None:
        """Invoke each subscriber callback; swallow exceptions to protect the buffer."""
        for cb in subs:
            try:
                cb(event)
            except Exception:
                continue

    # -- pop / peek --------------------------------------------------------------
    def pop(self) -> Optional[BufferEvent]:
        """Remove and return the oldest event (FIFO), or ``None`` if empty."""
        with self._lock:
            if not self._events:
                return None
            return self._events.popleft()

    def peek(self) -> Optional[BufferEvent]:
        """Return the oldest event without removing it, or ``None`` if empty."""
        with self._lock:
            if not self._events:
                return None
            return self._events[0]

    def peek_latest(self) -> Optional[BufferEvent]:
        """Return the newest event without removing it, or ``None`` if empty."""
        with self._lock:
            if not self._events:
                return None
            return self._events[-1]

    def clear(self) -> None:
        """Remove every event currently in the buffer (counters are preserved)."""
        with self._lock:
            self._events.clear()

    # -- properties --------------------------------------------------------------
    @property
    def is_full(self) -> bool:
        with self._lock:
            return self._capacity > 0 and len(self._events) >= self._capacity

    @property
    def is_empty(self) -> bool:
        with self._lock:
            return len(self._events) == 0

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._events)

    @property
    def capacity(self) -> int:
        return self._capacity

    # -- bulk access -------------------------------------------------------------
    def all(self) -> list:
        """Return all events, oldest first."""
        with self._lock:
            return list(self._events)

    def filter_by_type(self, event_type: str) -> list:
        """Return all events with ``event_type == event_type``, oldest first."""
        with self._lock:
            return [e for e in self._events if e.event_type == event_type]

    def filter_by_source(self, source: str) -> list:
        """Return all events with ``source == source``, oldest first."""
        with self._lock:
            return [e for e in self._events if e.source == source]

    def filter_by_time(
        self,
        start: Optional[float] = None,
        end: Optional[float] = None,
    ) -> list:
        """Return events with ``start <= timestamp <= end``. Bounds are inclusive."""
        with self._lock:
            out = []
            for e in self._events:
                if start is not None and e.timestamp < start:
                    continue
                if end is not None and e.timestamp > end:
                    continue
                out.append(e)
            return out

    def count_by_type(self) -> dict:
        """Return a histogram of ``event_type`` → count over the current buffer."""
        with self._lock:
            counts: dict = {}
            for e in self._events:
                counts[e.event_type] = counts.get(e.event_type, 0) + 1
            return counts

    def stats(self) -> BufferStats:
        """Return a :class:`BufferStats` snapshot of the buffer."""
        with self._lock:
            counts: dict = {}
            for e in self._events:
                counts[e.event_type] = counts.get(e.event_type, 0) + 1
            return BufferStats(
                total_capacity=self._capacity,
                current_size=len(self._events),
                dropped_count=self._dropped,
                event_types=counts,
            )

    # -- replay ------------------------------------------------------------------
    def replay(self, start_event_id: Optional[int] = None) -> list:
        """Return all currently-buffered events with ``event_id >= start_event_id``.

        If *start_event_id* is ``None``, all buffered events are returned.
        Order is oldest first.
        """
        with self._lock:
            if start_event_id is None:
                return list(self._events)
            return [e for e in self._events if e.event_id >= start_event_id]

    # -- subscriptions -----------------------------------------------------------
    def subscribe(self, callback: Callable) -> int:
        """Register *callback* to fire on every :meth:`push`. Returns the sub_id."""
        if not callable(callback):
            raise TypeError("callback must be callable")
        with self._lock:
            sub_id = self._next_sub_id
            self._next_sub_id += 1
            self._subs[sub_id] = callback
        return sub_id

    def unsubscribe(self, sub_id: int) -> bool:
        """Remove a subscription. Returns ``True`` if it existed, else ``False``."""
        with self._lock:
            return self._subs.pop(sub_id, None) is not None
