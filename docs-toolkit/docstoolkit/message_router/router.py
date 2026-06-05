"""Message router with topic patterns, priorities, and middleware.

Differs from ``notification_router`` (channel-based delivery records) and
``pubsub_bus`` (history-aware bus) by focusing on internal app messaging:

- topic patterns with ``*`` (single-segment) and ``#`` (multi-segment) wildcards
- per-handler integer priority (higher executes first)
- ordered middleware chain that can transform or drop messages
- thread-safe registry; handlers fire outside the lock
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
from uuid import uuid4


# ---------------------------------------------------------------------------
# Public enums / dataclasses
# ---------------------------------------------------------------------------


class MessagePriority(Enum):
    """Priority levels for a published Message."""

    CRITICAL = 3
    HIGH = 2
    NORMAL = 1
    LOW = 0


@dataclass
class Message:
    """A routed message."""

    msg_id: str
    topic: str
    payload: Any
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: float = 0.0
    headers: dict = field(default_factory=dict)


@dataclass
class HandlerInfo:
    """A subscribed handler."""

    handler_id: str
    topic_pattern: str
    handler: Callable
    priority: int = 0


@dataclass
class RouterStats:
    """Aggregate statistics for the router."""

    total_dispatched: int = 0
    total_handled: int = 0
    total_dropped: int = 0
    topics: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Topic matching
# ---------------------------------------------------------------------------


def _topic_matches(pattern: str, topic: str) -> bool:
    """Match ``topic`` against ``pattern``.

    - ``*`` matches a single segment
    - ``#`` matches one or more trailing segments (must be the last token)
    - Otherwise exact segment match
    """
    if pattern == topic:
        return True
    p_parts = pattern.split(".")
    t_parts = topic.split(".")

    for i, p in enumerate(p_parts):
        if p == "#":
            # Multi-segment wildcard must be the last pattern token, and
            # the topic must have at least one more segment here.
            return i < len(t_parts)
        if i >= len(t_parts):
            return False
        if p == "*":
            continue
        if p != t_parts[i]:
            return False

    return len(p_parts) == len(t_parts)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------


class MessageRouter:
    """Topic-based message router with middleware and priorities."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._handlers: dict[str, HandlerInfo] = {}
        self._middleware: list[tuple[int, Callable[[Message], Optional[Message]]]] = []
        self._next_mw_id: int = 1
        self._stats = RouterStats()
        self._seen_topics: set[str] = set()

    # ------------------------------------------------------------------ subscribe
    def subscribe(
        self,
        topic_pattern: str,
        handler: Callable[[Message], Any],
        priority: int = 0,
    ) -> str:
        """Register ``handler`` for messages whose topic matches ``topic_pattern``."""
        if not isinstance(topic_pattern, str) or not topic_pattern:
            raise ValueError("topic_pattern must be a non-empty string")
        if not callable(handler):
            raise TypeError("handler must be callable")

        handler_id = uuid4().hex[:12]
        info = HandlerInfo(
            handler_id=handler_id,
            topic_pattern=topic_pattern,
            handler=handler,
            priority=int(priority),
        )
        with self._lock:
            self._handlers[handler_id] = info
        return handler_id

    def unsubscribe(self, handler_id: str) -> bool:
        """Remove a handler by id; return True if it existed."""
        with self._lock:
            return self._handlers.pop(handler_id, None) is not None

    # ------------------------------------------------------------------ middleware
    def add_middleware(
        self,
        middleware: Callable[[Message], Optional[Message]],
    ) -> int:
        """Register a middleware. Returns a numeric id usable in ``remove_middleware``."""
        if not callable(middleware):
            raise TypeError("middleware must be callable")
        with self._lock:
            mw_id = self._next_mw_id
            self._next_mw_id += 1
            self._middleware.append((mw_id, middleware))
        return mw_id

    def remove_middleware(self, middleware_id: int) -> bool:
        """Remove a middleware by id; return True if it existed."""
        with self._lock:
            for idx, (mw_id, _fn) in enumerate(self._middleware):
                if mw_id == middleware_id:
                    self._middleware.pop(idx)
                    return True
            return False

    # ------------------------------------------------------------------ publish
    def publish(
        self,
        topic: str,
        payload: Any,
        priority: MessagePriority = MessagePriority.NORMAL,
        headers: dict = None,
        now: float = 0.0,
    ) -> int:
        """Publish a new message; returns the number of handlers invoked."""
        message = Message(
            msg_id=uuid4().hex[:12],
            topic=topic,
            payload=payload,
            priority=priority,
            timestamp=now,
            headers=dict(headers) if headers else {},
        )
        return self.publish_message(message)

    def publish_message(self, message: Message) -> int:
        """Publish a pre-built Message; returns the number of handlers invoked."""
        # Snapshot middleware + handlers under lock; run them outside.
        with self._lock:
            middleware = list(self._middleware)
            handler_snapshot = list(self._handlers.values())
            self._seen_topics.add(message.topic)
            self._stats.total_dispatched += 1
            self._stats.topics[message.topic] = (
                self._stats.topics.get(message.topic, 0) + 1
            )

        # Middleware chain (can transform or drop).
        current: Optional[Message] = message
        for _mw_id, mw in middleware:
            try:
                current = mw(current)
            except Exception:
                # A failing middleware drops the message.
                current = None
            if current is None:
                with self._lock:
                    self._stats.total_dropped += 1
                return 0

        # Sort handlers by priority (higher first) and filter by topic.
        matching = [h for h in handler_snapshot if _topic_matches(h.topic_pattern, current.topic)]
        matching.sort(key=lambda h: h.priority, reverse=True)

        invoked = 0
        for h in matching:
            try:
                h.handler(current)
            except Exception:
                # Errors don't stop other handlers; still counted as handled.
                pass
            invoked += 1

        with self._lock:
            self._stats.total_handled += invoked
        return invoked

    # ------------------------------------------------------------------ introspection
    def stats(self) -> RouterStats:
        """Return a snapshot of router statistics."""
        with self._lock:
            return RouterStats(
                total_dispatched=self._stats.total_dispatched,
                total_handled=self._stats.total_handled,
                total_dropped=self._stats.total_dropped,
                topics=dict(self._stats.topics),
            )

    def handlers_for(self, topic: str) -> list:
        """Return all HandlerInfo objects whose pattern matches ``topic``."""
        with self._lock:
            handlers = list(self._handlers.values())
        matching = [h for h in handlers if _topic_matches(h.topic_pattern, topic)]
        matching.sort(key=lambda h: h.priority, reverse=True)
        return matching

    def clear(self) -> None:
        """Remove all handlers, middleware, and statistics."""
        with self._lock:
            self._handlers.clear()
            self._middleware.clear()
            self._next_mw_id = 1
            self._stats = RouterStats()
            self._seen_topics.clear()

    @property
    def subscribers_count(self) -> int:
        with self._lock:
            return len(self._handlers)

    @property
    def topic_count(self) -> int:
        """Number of distinct topics ever published."""
        with self._lock:
            return len(self._seen_topics)
