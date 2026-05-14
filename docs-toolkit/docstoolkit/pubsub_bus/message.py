"""Message primitive for the pub/sub bus (E90)."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Message:
    """A single message published on the bus."""

    topic: str = ""
    payload: Any = None
    message_id: str = field(default_factory=lambda: uuid4().hex[:12])
    timestamp: float = field(default_factory=time.time)
    headers: dict = field(default_factory=dict)
