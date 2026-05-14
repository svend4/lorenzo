"""Core types for the rate quota module."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class QuotaPeriod(Enum):
    """Rate quota period expressed in seconds."""

    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400


@dataclass
class QuotaDefinition:
    """Definition of a rate quota."""

    key: str
    limit: int
    period: QuotaPeriod
    description: str = ""


@dataclass
class QuotaUsage:
    """Current usage information for a quota in a window."""

    key: str
    count: int
    limit: int
    period: QuotaPeriod
    reset_at: float  # Unix timestamp when current window ends/resets

    @property
    def remaining(self) -> int:
        """Number of operations still available; never negative."""
        return max(0, self.limit - self.count)


class QuotaExceeded(Exception):
    """Raised when a consume would exceed the quota limit."""

    def __init__(self, key: str, usage: QuotaUsage):
        self.key = key
        self.usage = usage
        super().__init__(
            f"Quota '{key}' exceeded: count={usage.count} limit={usage.limit}"
        )
