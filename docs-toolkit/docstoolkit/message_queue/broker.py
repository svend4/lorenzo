"""Broker-level error and the MessageBroker that manages named queues."""
from __future__ import annotations

import threading
from typing import Optional

from docstoolkit.message_queue.message import Message, MessagePriority
from docstoolkit.message_queue.queue import MessageQueue, QueueConfig


class QueueFullError(Exception):
    """Raised when a publish is attempted on a full (max_size-limited) queue."""


class MessageBroker:
    """Registry of named MessageQueues with convenience publish/stats helpers."""

    def __init__(self) -> None:
        self._queues: dict[str, MessageQueue] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Queue lifecycle
    # ------------------------------------------------------------------

    def create_queue(self, name: str, config: QueueConfig = None) -> MessageQueue:
        """Create and register a new queue; return the queue object."""
        with self._lock:
            q = MessageQueue(name=name, config=config)
            self._queues[name] = q
            return q

    def get_queue(self, name: str) -> Optional[MessageQueue]:
        """Return the named queue, or None if it does not exist."""
        with self._lock:
            return self._queues.get(name)

    def delete_queue(self, name: str) -> bool:
        """Remove the named queue. Return True if it existed."""
        with self._lock:
            if name in self._queues:
                del self._queues[name]
                return True
            return False

    def queues(self) -> list[str]:
        """Return a sorted list of registered queue names."""
        with self._lock:
            return sorted(self._queues.keys())

    # ------------------------------------------------------------------
    # Publish helper
    # ------------------------------------------------------------------

    def publish(
        self,
        queue_name: str,
        topic: str,
        payload: dict = None,
        priority: MessagePriority = None,
        **kwargs,
    ) -> Message:
        """Create a Message and publish it to the named queue.

        Raises KeyError if *queue_name* is not registered.
        Raises QueueFullError (propagated from the queue) if at capacity.
        """
        with self._lock:
            queue = self._queues.get(queue_name)
        if queue is None:
            raise KeyError(f"Queue {queue_name!r} not found")

        msg_priority = priority if priority is not None else (
            queue.config.default_priority
        )
        msg = Message(
            topic=topic,
            payload=payload if payload is not None else {},
            priority=msg_priority,
            **kwargs,
        )
        queue.publish(msg)
        return msg

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return {queue_name: {size, dead_letters}} for every queue."""
        with self._lock:
            queues_snapshot = dict(self._queues)
        return {
            name: {
                "size": q.size(),
                "dead_letters": len(q.dead_letters()),
            }
            for name, q in queues_snapshot.items()
        }
