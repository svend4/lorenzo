"""Message primitives: priority, status, and the Message dataclass."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import IntEnum, Enum
from uuid import uuid4


class MessagePriority(IntEnum):
    LOW = 1
    NORMAL = 5
    HIGH = 10
    CRITICAL = 20


class MessageStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DEAD_LETTER = "DEAD_LETTER"


@dataclass
class Message:
    topic: str
    payload: dict = field(default_factory=dict)
    priority: MessagePriority = MessagePriority.NORMAL
    status: MessageStatus = MessageStatus.PENDING
    created_at: float = field(default_factory=time.time)
    attempts: int = 0
    max_retries: int = 3
    scheduled_at: float = 0.0
    message_id: str = field(default_factory=lambda: uuid4().hex)

    def can_retry(self) -> bool:
        """Return True if there are retries remaining."""
        return self.attempts < self.max_retries
