"""Session dataclass and status enum for the session manager."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class SessionStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    INVALIDATED = "invalidated"


@dataclass
class Session:
    user_id: str
    session_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    expires_at: float = 0.0  # 0 means never expires
    data: dict = field(default_factory=dict)
    status: SessionStatus = SessionStatus.ACTIVE

    def is_expired(self, now: float = None) -> bool:
        """Return True if expires_at > 0 and now > expires_at."""
        if self.expires_at == 0.0:
            return False
        if now is None:
            now = time.time()
        return now > self.expires_at

    def touch(self, now: float = None) -> None:
        """Update last_accessed to now."""
        if now is None:
            now = time.time()
        self.last_accessed = now

    def get(self, key: str, default=None):
        """Delegate key lookup to data dict."""
        return self.data.get(key, default)

    def set(self, key: str, value) -> None:
        """Delegate key assignment to data dict."""
        self.data[key] = value
