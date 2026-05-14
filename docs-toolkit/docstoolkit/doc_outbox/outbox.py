"""E329 DocOutbox — reliable outbox pattern for outbound document messages."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OutboxMessage:
    """A single outbound message in the outbox."""

    message_id: str
    doc_id: str
    destination: str
    payload: dict = field(default_factory=dict)
    created_at: float = 0.0
    status: str = "pending"
    attempts: int = 0
    last_attempt_at: Optional[float] = None
    last_error: str = ""


@dataclass
class OutboxStats:
    """Aggregate statistics for the outbox."""

    total: int
    pending: int
    sent: int
    failed: int
    abandoned: int


class DocOutbox:
    """Reliable outbox for outbound document messages.

    Thread-safe via :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._messages: dict[str, OutboxMessage] = {}
        self._lock = threading.Lock()

    def enqueue(
        self,
        doc_id: str,
        destination: str,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> OutboxMessage:
        """Create a pending outbox message and return it."""
        if now is None:
            now = time.time()
        msg = OutboxMessage(
            message_id=str(uuid.uuid4()),
            doc_id=doc_id,
            destination=destination,
            payload=dict(payload) if payload else {},
            created_at=now,
            status="pending",
            attempts=0,
            last_attempt_at=None,
            last_error="",
        )
        with self._lock:
            self._messages[msg.message_id] = msg
        return msg

    def mark_sent(self, message_id: str, now: Optional[float] = None) -> bool:
        """Mark a message as successfully sent."""
        if now is None:
            now = time.time()
        with self._lock:
            msg = self._messages.get(message_id)
            if msg is None:
                return False
            msg.status = "sent"
            msg.attempts += 1
            msg.last_attempt_at = now
            return True

    def mark_failed(
        self,
        message_id: str,
        error: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Mark a message as failed and record the error."""
        if now is None:
            now = time.time()
        with self._lock:
            msg = self._messages.get(message_id)
            if msg is None:
                return False
            msg.status = "failed"
            msg.attempts += 1
            msg.last_attempt_at = now
            msg.last_error = error
            return True

    def abandon(self, message_id: str, reason: str = "") -> bool:
        """Abandon a message (terminal state) with a reason."""
        with self._lock:
            msg = self._messages.get(message_id)
            if msg is None:
                return False
            msg.status = "abandoned"
            msg.last_error = reason
            return True

    def retry(self, message_id: str) -> bool:
        """Transition a failed message back to pending. No-op otherwise."""
        with self._lock:
            msg = self._messages.get(message_id)
            if msg is None:
                return False
            if msg.status != "failed":
                return False
            msg.status = "pending"
            return True

    def delete(self, message_id: str) -> bool:
        """Fully remove a message from the outbox."""
        with self._lock:
            if message_id in self._messages:
                del self._messages[message_id]
                return True
            return False

    def get(self, message_id: str) -> Optional[OutboxMessage]:
        """Return the message with the given id, or None."""
        with self._lock:
            return self._messages.get(message_id)

    def pending(self, limit: Optional[int] = None) -> list[OutboxMessage]:
        """Return pending messages, oldest first by created_at."""
        with self._lock:
            items = [m for m in self._messages.values() if m.status == "pending"]
        items.sort(key=lambda m: m.created_at)
        if limit is not None:
            items = items[:limit]
        return items

    def messages_for_doc(self, doc_id: str) -> list[OutboxMessage]:
        """Return all messages for a given doc_id, sorted by created_at."""
        with self._lock:
            items = [m for m in self._messages.values() if m.doc_id == doc_id]
        items.sort(key=lambda m: m.created_at)
        return items

    def messages_by_status(self, status: str) -> list[OutboxMessage]:
        """Return all messages with the given status, sorted by created_at."""
        with self._lock:
            items = [m for m in self._messages.values() if m.status == status]
        items.sort(key=lambda m: m.created_at)
        return items

    def failed_messages(self) -> list[OutboxMessage]:
        """Return failed messages, sorted by last_attempt_at descending."""
        with self._lock:
            items = [m for m in self._messages.values() if m.status == "failed"]
        items.sort(key=lambda m: m.last_attempt_at or 0.0, reverse=True)
        return items

    def purge_sent(self) -> int:
        """Delete all sent messages. Return the number removed."""
        with self._lock:
            ids = [mid for mid, m in self._messages.items() if m.status == "sent"]
            for mid in ids:
                del self._messages[mid]
            return len(ids)

    def stats(self) -> OutboxStats:
        """Return aggregate counts across statuses."""
        with self._lock:
            total = len(self._messages)
            pending = sum(1 for m in self._messages.values() if m.status == "pending")
            sent = sum(1 for m in self._messages.values() if m.status == "sent")
            failed = sum(1 for m in self._messages.values() if m.status == "failed")
            abandoned = sum(
                1 for m in self._messages.values() if m.status == "abandoned"
            )
        return OutboxStats(
            total=total,
            pending=pending,
            sent=sent,
            failed=failed,
            abandoned=abandoned,
        )
