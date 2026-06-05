"""In-memory, thread-safe MessageQueue with priority ordering."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.message_queue.message import Message, MessagePriority, MessageStatus


# QueueFullError is defined in broker.py and re-exported from __init__.py.
# We import it lazily (inside methods) to avoid a circular import, or define a
# local alias here.  Using a forward declaration via a module-level import from
# broker would create a cycle (broker imports queue).  Instead we define the
# error in broker.py and import it only where needed.


def _queue_full_error():
    """Lazy import to break circular dependency between queue and broker."""
    from docstoolkit.message_queue.broker import QueueFullError  # noqa: PLC0415
    return QueueFullError


@dataclass
class QueueConfig:
    """Configuration for a MessageQueue.

    max_size=0 means unlimited.
    """
    max_size: int = 0
    default_priority: MessagePriority = MessagePriority.NORMAL


class MessageQueue:
    """Thread-safe, priority-ordered in-memory message queue."""

    def __init__(self, name: str, config: QueueConfig = None) -> None:
        self.name = name
        self.config: QueueConfig = config if config is not None else QueueConfig()
        self._messages: list[Message] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _pending(self, topic: Optional[str] = None) -> list[Message]:
        """Return PENDING messages, optionally filtered by topic (no lock)."""
        msgs = [m for m in self._messages if m.status == MessageStatus.PENDING]
        if topic is not None:
            msgs = [m for m in msgs if m.topic == topic]
        return msgs

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def publish(self, message: Message) -> None:
        """Add a message to the queue.

        Raises QueueFullError if max_size > 0 and the number of PENDING
        messages (for all topics) is already at the limit.
        """
        with self._lock:
            if self.config.max_size > 0:
                pending_count = sum(
                    1 for m in self._messages if m.status == MessageStatus.PENDING
                )
                if pending_count >= self.config.max_size:
                    QueueFullError = _queue_full_error()
                    raise QueueFullError(
                        f"Queue {self.name!r} is full "
                        f"(max_size={self.config.max_size})"
                    )
            self._messages.append(message)

    def consume(
        self,
        topic: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Optional[Message]:
        """Return and mark PROCESSING the highest-priority eligible message.

        Eligible = PENDING, matching *topic* (if given), and
        scheduled_at <= now (0.0 counts as immediate).

        Returns None when no eligible message exists.
        """
        if now is None:
            now = time.time()

        with self._lock:
            candidates = [
                m for m in self._messages
                if m.status == MessageStatus.PENDING
                and (topic is None or m.topic == topic)
                and (m.scheduled_at == 0.0 or m.scheduled_at <= now)
            ]
            if not candidates:
                return None
            # Highest priority value wins; ties broken by oldest created_at
            best = max(candidates, key=lambda m: (m.priority, -m.created_at))
            best.status = MessageStatus.PROCESSING
            return best

    def ack(self, message_id: str) -> bool:
        """Mark message COMPLETED. Return True if found."""
        with self._lock:
            for m in self._messages:
                if m.message_id == message_id:
                    m.status = MessageStatus.COMPLETED
                    return True
            return False

    def nack(self, message_id: str) -> bool:
        """Increment attempts; retry or dead-letter the message.

        Returns True if the message was found, False otherwise.
        """
        with self._lock:
            for m in self._messages:
                if m.message_id == message_id:
                    m.attempts += 1
                    if m.can_retry():
                        m.status = MessageStatus.PENDING
                    else:
                        m.status = MessageStatus.DEAD_LETTER
                    return True
            return False

    def size(self, topic: Optional[str] = None) -> int:
        """Count PENDING messages, optionally filtered by topic."""
        with self._lock:
            return len(self._pending(topic))

    def dead_letters(self) -> list[Message]:
        """Return all DEAD_LETTER messages."""
        with self._lock:
            return [m for m in self._messages if m.status == MessageStatus.DEAD_LETTER]

    def purge(self, topic: Optional[str] = None) -> int:
        """Remove all PENDING messages (optionally for a single topic).

        Returns the count of removed messages.
        """
        with self._lock:
            to_remove = [
                m for m in self._messages
                if m.status == MessageStatus.PENDING
                and (topic is None or m.topic == topic)
            ]
            for m in to_remove:
                self._messages.remove(m)
            return len(to_remove)
