"""Priority inbox: message queue with priority, categories, expiration and read state."""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import IntEnum, Enum
from typing import Optional


class Priority(IntEnum):
    """Message priority. Lower value means higher priority (URGENT=0 is highest)."""

    URGENT = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class MessageStatus(Enum):
    """Lifecycle status of a message."""

    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass
class Message:
    """A single inbox message."""

    msg_id: str
    subject: str
    body: str
    priority: Priority
    category: str = "default"
    received_at: float = 0.0
    expires_at: Optional[float] = None
    status: MessageStatus = MessageStatus.UNREAD
    metadata: dict = field(default_factory=dict)

    def is_expired(self, now: float) -> bool:
        """Return True if this message has an expiration in the past."""
        return self.expires_at is not None and self.expires_at <= now


@dataclass
class InboxStats:
    """Aggregate counts across the inbox."""

    total: int
    unread: int
    read: int
    archived: int
    by_priority: dict
    by_category: dict


class PriorityInbox:
    """In-memory priority message inbox with categories and expiration."""

    def __init__(self) -> None:
        self._messages: dict[str, Message] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- add
    def add(
        self,
        subject: str,
        body: str,
        priority: Priority = Priority.NORMAL,
        category: str = "default",
        expires_at: Optional[float] = None,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> Message:
        """Create a new message and add it to the inbox. Returns the message."""
        msg = Message(
            msg_id=uuid.uuid4().hex,
            subject=subject,
            body=body,
            priority=priority,
            category=category,
            received_at=now,
            expires_at=expires_at,
            status=MessageStatus.UNREAD,
            metadata=dict(metadata) if metadata else {},
        )
        with self._lock:
            self._messages[msg.msg_id] = msg
        return msg

    def add_message(self, message: Message) -> None:
        """Insert a pre-built message. Overwrites any message with the same id."""
        with self._lock:
            self._messages[message.msg_id] = message

    # ---------------------------------------------------------------- peek / pop
    def _active_unread(self, now: float) -> list[Message]:
        """Return list of UNREAD, non-expired messages sorted by priority+received."""
        msgs = [
            m
            for m in self._messages.values()
            if m.status == MessageStatus.UNREAD and not m.is_expired(now)
        ]
        msgs.sort(key=lambda m: (int(m.priority), m.received_at))
        return msgs

    def peek(self, now: float = 0.0) -> Optional[Message]:
        """Highest-priority UNREAD message that is not expired."""
        with self._lock:
            msgs = self._active_unread(now)
            return msgs[0] if msgs else None

    def pop(self, now: float = 0.0) -> Optional[Message]:
        """Peek + mark READ atomically."""
        with self._lock:
            msgs = self._active_unread(now)
            if not msgs:
                return None
            msg = msgs[0]
            msg.status = MessageStatus.READ
            return msg

    # ---------------------------------------------------------------- state changes
    def mark_read(self, msg_id: str) -> bool:
        with self._lock:
            msg = self._messages.get(msg_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.status = MessageStatus.READ
            return True

    def mark_unread(self, msg_id: str) -> bool:
        with self._lock:
            msg = self._messages.get(msg_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.status = MessageStatus.UNREAD
            return True

    def archive(self, msg_id: str) -> bool:
        with self._lock:
            msg = self._messages.get(msg_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.status = MessageStatus.ARCHIVED
            return True

    def delete(self, msg_id: str) -> bool:
        """Remove the message from storage entirely."""
        with self._lock:
            if msg_id in self._messages:
                del self._messages[msg_id]
                return True
            return False

    # ---------------------------------------------------------------- lookups
    def get(self, msg_id: str) -> Optional[Message]:
        with self._lock:
            return self._messages.get(msg_id)

    def list_unread(
        self, category: Optional[str] = None, now: float = 0.0
    ) -> list[Message]:
        with self._lock:
            msgs = self._active_unread(now)
            if category is not None:
                msgs = [m for m in msgs if m.category == category]
            return msgs

    def list_by_priority(
        self, priority: Priority, now: float = 0.0
    ) -> list[Message]:
        with self._lock:
            msgs = [
                m
                for m in self._messages.values()
                if m.priority == priority
                and m.status == MessageStatus.UNREAD
                and not m.is_expired(now)
            ]
            msgs.sort(key=lambda m: m.received_at)
            return msgs

    def list_by_category(
        self, category: str, now: float = 0.0
    ) -> list[Message]:
        """All non-deleted, non-expired, non-archived messages in a category."""
        with self._lock:
            msgs = [
                m
                for m in self._messages.values()
                if m.category == category
                and m.status != MessageStatus.ARCHIVED
                and not m.is_expired(now)
            ]
            msgs.sort(key=lambda m: (int(m.priority), m.received_at))
            return msgs

    def count_unread(self, now: float = 0.0) -> int:
        with self._lock:
            return sum(
                1
                for m in self._messages.values()
                if m.status == MessageStatus.UNREAD and not m.is_expired(now)
            )

    # ---------------------------------------------------------------- stats
    def stats(self, now: float = 0.0) -> InboxStats:
        with self._lock:
            total = 0
            unread = 0
            read = 0
            archived = 0
            by_priority: dict = {p: 0 for p in Priority}
            by_category: dict = {}
            for m in self._messages.values():
                if m.is_expired(now):
                    continue
                total += 1
                if m.status == MessageStatus.UNREAD:
                    unread += 1
                elif m.status == MessageStatus.READ:
                    read += 1
                elif m.status == MessageStatus.ARCHIVED:
                    archived += 1
                by_priority[m.priority] = by_priority.get(m.priority, 0) + 1
                by_category[m.category] = by_category.get(m.category, 0) + 1
            return InboxStats(
                total=total,
                unread=unread,
                read=read,
                archived=archived,
                by_priority=by_priority,
                by_category=by_category,
            )

    # ---------------------------------------------------------------- cleanup
    def cleanup_expired(self, now: float = 0.0) -> int:
        """Permanently remove expired messages. Returns count removed."""
        with self._lock:
            expired_ids = [
                mid for mid, m in self._messages.items() if m.is_expired(now)
            ]
            for mid in expired_ids:
                del self._messages[mid]
            return len(expired_ids)

    def clear(self) -> None:
        with self._lock:
            self._messages.clear()
