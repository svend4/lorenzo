"""In-memory publish/subscribe bus with wildcard topic matching (E90)."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from uuid import uuid4

from docstoolkit.pubsub_bus.message import Message


@dataclass
class Subscription:
    """A registered subscriber on the bus."""

    subscription_id: str
    topic_pattern: str
    callback: Callable
    filter: Optional[Callable] = None


def _match_topic(pattern: str, topic: str) -> bool:
    """Return True if *topic* matches the dotted *pattern*.

    Pattern segments:
        ``*``  matches exactly one segment.
        ``**`` matches zero or more segments (greedy).
    All other segments are matched literally.
    """
    if not isinstance(pattern, str) or not isinstance(topic, str):
        return False
    p = pattern.split(".") if pattern else [""]
    t = topic.split(".") if topic else [""]
    return _match(p, 0, t, 0)


def _match(p: list, pi: int, t: list, ti: int) -> bool:
    while pi < len(p):
        seg = p[pi]
        if seg == "**":
            # Skip consecutive ``**`` segments — they are equivalent to one.
            while pi + 1 < len(p) and p[pi + 1] == "**":
                pi += 1
            if pi == len(p) - 1:
                # Trailing ``**`` swallows the rest (including zero segments).
                return True
            # Try matching the remaining pattern against any tail of *t*.
            for k in range(ti, len(t) + 1):
                if _match(p, pi + 1, t, k):
                    return True
            return False
        if ti >= len(t):
            return False
        if seg == "*":
            pi += 1
            ti += 1
            continue
        if seg != t[ti]:
            return False
        pi += 1
        ti += 1
    return ti == len(t)


class PubSubBus:
    """Thread-safe in-memory publish/subscribe bus.

    Wildcard syntax in subscription topic patterns:
        ``*``  — exactly one dotted segment.
        ``**`` — zero or more dotted segments (greedy).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: dict[str, Subscription] = {}

    # -- subscription management -------------------------------------------------
    def subscribe(
        self,
        topic_pattern: str,
        callback: Callable,
        filter: Optional[Callable] = None,
    ) -> str:
        """Register a callback for messages matching *topic_pattern*.

        Returns the subscription_id (used by :meth:`unsubscribe`).
        """
        if not callable(callback):
            raise TypeError("callback must be callable")
        if filter is not None and not callable(filter):
            raise TypeError("filter must be callable or None")
        sub_id = uuid4().hex[:12]
        sub = Subscription(
            subscription_id=sub_id,
            topic_pattern=topic_pattern,
            callback=callback,
            filter=filter,
        )
        with self._lock:
            self._subs[sub_id] = sub
        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription by id. Returns True if removed, False otherwise."""
        with self._lock:
            return self._subs.pop(subscription_id, None) is not None

    # -- publication -------------------------------------------------------------
    def publish(
        self,
        topic: str,
        payload: Any = None,
        headers: Optional[dict] = None,
    ) -> int:
        """Build a :class:`Message` and dispatch it. Returns the number of deliveries."""
        msg = Message(
            topic=topic,
            payload=payload,
            headers=dict(headers) if headers else {},
        )
        return self.publish_message(msg)

    def publish_message(self, message: Message) -> int:
        """Dispatch an already-constructed :class:`Message`.

        Returns the count of subscriptions that received it (after filter).
        """
        # Snapshot current subscriptions to keep dispatch outside the lock.
        with self._lock:
            subs = list(self._subs.values())
        delivered = 0
        for sub in subs:
            if not _match_topic(sub.topic_pattern, message.topic):
                continue
            if sub.filter is not None:
                try:
                    if not sub.filter(message):
                        continue
                except Exception:
                    continue
            try:
                sub.callback(message)
            except Exception:
                # Callbacks must not break the bus; swallow and continue.
                continue
            delivered += 1
        return delivered

    # -- introspection -----------------------------------------------------------
    def topics(self) -> set:
        """Return the set of distinct topic patterns currently subscribed."""
        with self._lock:
            return {s.topic_pattern for s in self._subs.values()}

    def subscription_count(self, topic_pattern: Optional[str] = None) -> int:
        """Count subscriptions. If *topic_pattern* is given, only matches it exactly."""
        with self._lock:
            if topic_pattern is None:
                return len(self._subs)
            return sum(1 for s in self._subs.values() if s.topic_pattern == topic_pattern)

    def clear(self) -> None:
        """Remove every subscription."""
        with self._lock:
            self._subs.clear()
