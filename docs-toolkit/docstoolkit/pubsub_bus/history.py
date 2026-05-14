"""Per-topic ring-buffer history of published messages (E90)."""
from __future__ import annotations

import threading
from collections import deque
from typing import Optional

from docstoolkit.pubsub_bus.message import Message


class MessageHistory:
    """Bounded per-topic history of :class:`Message` objects.

    Each topic gets its own deque capped at *max_size* — the newest message
    pushes the oldest out (FIFO eviction).
    """

    def __init__(self, max_size: int = 1000) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._lock = threading.Lock()
        self._buf: dict[str, deque] = {}

    @property
    def max_size(self) -> int:
        return self._max_size

    def record(self, message: Message) -> None:
        """Append *message* to its topic's history."""
        if not isinstance(message, Message):
            raise TypeError("message must be a Message instance")
        with self._lock:
            dq = self._buf.get(message.topic)
            if dq is None:
                dq = deque(maxlen=self._max_size)
                self._buf[message.topic] = dq
            dq.append(message)

    def get_topic(self, topic: str, limit: int = 100) -> list:
        """Return up to *limit* most recent messages for *topic*, newest first."""
        if limit < 0:
            limit = 0
        with self._lock:
            dq = self._buf.get(topic)
            if not dq:
                return []
            # Newest first; deque iteration is oldest-first, so reverse.
            items = list(dq)
        items.reverse()
        return items[:limit]

    def count_topic(self, topic: str) -> int:
        """Return the number of stored messages for *topic*."""
        with self._lock:
            dq = self._buf.get(topic)
            return len(dq) if dq else 0

    def clear(self, topic: Optional[str] = None) -> None:
        """Clear history. If *topic* is None, drop everything."""
        with self._lock:
            if topic is None:
                self._buf.clear()
            else:
                self._buf.pop(topic, None)

    def all_topics(self) -> list:
        """Return a list of all topics currently holding history."""
        with self._lock:
            return list(self._buf.keys())
