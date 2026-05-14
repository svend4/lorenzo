"""DocNotificationCenter — in-memory pub/sub notification center.

Provides:
- ``Notification`` dataclass: immutable record of a published message.
- ``Subscription`` dataclass: subscription record with topic pattern and callback.
- ``NotifStats`` dataclass: snapshot of center-wide statistics.
- ``DocNotificationCenter`` — thread-safe center with fnmatch topic patterns,
  pause/resume, history with optional topic filter, and delivery counting.

Stdlib only: ``fnmatch``, ``threading``, ``uuid``.
"""

from __future__ import annotations

import fnmatch
import threading
import uuid
from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class Notification:
    """A single published notification."""

    notif_id: int
    topic: str
    payload: dict
    timestamp: float
    sender: str = ""


@dataclass
class Subscription:
    """Subscription record: links a topic pattern to a callback."""

    sub_id: str
    topic: str           # exact match or fnmatch pattern
    callback: Callable   # called with Notification, outside lock
    active: bool = True


@dataclass
class NotifStats:
    """Snapshot of center-wide statistics."""

    total_published: int
    total_delivered: int
    total_subscriptions: int
    topics_seen: List[str]  # sorted list of unique topics published to


class DocNotificationCenter:
    """Thread-safe in-memory notification center.

    Supports:
    - fnmatch topic patterns: ``subscribe("doc.*")`` matches ``doc.created``.
    - ``subscribe("*")`` matches every single-segment topic.
    - pause / resume to temporarily suppress callbacks for a subscription.
    - history: newest-first list of past notifications, filterable by topic.
    - stats snapshot with delivery counting.

    Callbacks fire **outside** the lock to prevent deadlocks.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: dict[str, Subscription] = {}
        self._history: List[Notification] = []
        self._notif_counter: int = 0
        self._total_published: int = 0
        self._total_delivered: int = 0
        self._topics_seen: set[str] = set()

    # ---------------------------------------------------------------- subscribe

    def subscribe(
        self,
        topic: str,
        callback: Callable,
        sub_id: Optional[str] = None,
    ) -> Subscription:
        """Subscribe *callback* to a topic pattern.

        Auto-generates *sub_id* (UUID4 string) when not provided.
        Returns the new :class:`Subscription`.
        """
        if sub_id is None:
            sub_id = str(uuid.uuid4())
        sub = Subscription(sub_id=sub_id, topic=topic, callback=callback, active=True)
        with self._lock:
            self._subs[sub_id] = sub
        return sub

    def unsubscribe(self, sub_id: str) -> bool:
        """Remove subscription by *sub_id*. Returns ``True`` if it existed."""
        with self._lock:
            return self._subs.pop(sub_id, None) is not None

    def pause(self, sub_id: str) -> bool:
        """Deactivate subscription so its callback is skipped.

        Returns ``False`` if *sub_id* not found, ``True`` otherwise.
        """
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.active = False
            return True

    def resume(self, sub_id: str) -> bool:
        """Reactivate a paused subscription.

        Returns ``False`` if *sub_id* not found, ``True`` otherwise.
        """
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.active = True
            return True

    # ---------------------------------------------------------------- publish

    def publish(
        self,
        topic: str,
        payload: dict,
        sender: str = "",
        now: Optional[float] = None,
    ) -> Notification:
        """Publish a notification to *topic*.

        - Creates :class:`Notification` with auto-incrementing ``notif_id``.
        - Appends to history.
        - Calls all matching *active* subscriptions using
          ``fnmatch.fnmatch(topic, sub.topic)``.
        - Callbacks fire **outside** the lock.
        - Returns the created :class:`Notification`.
        """
        if now is None:
            import time
            now = time.time()

        with self._lock:
            self._notif_counter += 1
            notif = Notification(
                notif_id=self._notif_counter,
                topic=topic,
                payload=payload,
                timestamp=now,
                sender=sender,
            )
            self._history.append(notif)
            self._total_published += 1
            self._topics_seen.add(topic)
            # Snapshot active matching subs while holding the lock.
            matching = [
                sub
                for sub in self._subs.values()
                if sub.active and fnmatch.fnmatch(topic, sub.topic)
            ]

        # Fire callbacks outside the lock.
        delivered = 0
        for sub in matching:
            try:
                sub.callback(notif)
                delivered += 1
            except Exception:
                pass

        with self._lock:
            self._total_delivered += delivered

        return notif

    # ---------------------------------------------------------------- history

    def history(
        self,
        topic: Optional[str] = None,
        limit: int = 20,
    ) -> List[Notification]:
        """Return recent notifications, newest first.

        Filters by exact *topic* string when provided.  At most *limit* items
        are returned.
        """
        with self._lock:
            items = list(self._history)

        if topic is not None:
            items = [n for n in items if n.topic == topic]

        # Newest first.
        items.reverse()
        return items[:limit]

    def clear_history(self, topic: Optional[str] = None) -> int:
        """Clear history entries, optionally limited to *topic*.

        Returns the number of entries removed.
        """
        with self._lock:
            if topic is None:
                count = len(self._history)
                self._history.clear()
                return count
            before = len(self._history)
            self._history = [n for n in self._history if n.topic != topic]
            return before - len(self._history)

    # --------------------------------------------------------------- query

    def subscriptions(self, topic: Optional[str] = None) -> List[Subscription]:
        """Return all subscriptions, optionally filtered by exact topic match."""
        with self._lock:
            subs = list(self._subs.values())
        if topic is not None:
            subs = [s for s in subs if s.topic == topic]
        return subs

    def stats(self) -> NotifStats:
        """Return a :class:`NotifStats` snapshot."""
        with self._lock:
            return NotifStats(
                total_published=self._total_published,
                total_delivered=self._total_delivered,
                total_subscriptions=len(self._subs),
                topics_seen=sorted(self._topics_seen),
            )

    @property
    def total_subscriptions(self) -> int:
        """Current number of registered subscriptions."""
        with self._lock:
            return len(self._subs)
