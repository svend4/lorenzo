"""TimelineEvent dataclass and EventType enum for docs-toolkit timeline module."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum


class EventType(Enum):
    RELEASE = "release"
    ANNOUNCEMENT = "announcement"
    MILESTONE = "milestone"
    DEADLINE = "deadline"
    MEETING = "meeting"
    PUBLICATION = "publication"
    UNKNOWN = "unknown"


def _short_uuid() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class TimelineEvent:
    """A single extracted timeline event.

    Fields
    ------
    event_id        : auto-generated 8-char UUID4 hex string
    date_str        : raw extracted date string from source text
    year            : parsed year (int) or None
    month           : parsed month (int, 1-12) or None
    day             : parsed day (int, 1-31) or None
    description     : human-readable description of the event
    event_type      : EventType classification
    source_text     : surrounding context from source, max 200 chars
    confidence      : extraction confidence score, 0.0–1.0
    """

    date_str: str
    description: str
    event_type: EventType = EventType.UNKNOWN
    source_text: str = ""
    confidence: float = 0.5
    year: int | None = None
    month: int | None = None
    day: int | None = None
    event_id: str = field(default_factory=_short_uuid)

    def has_full_date(self) -> bool:
        """Return True iff year, month, and day are all set."""
        return self.year is not None and self.month is not None and self.day is not None

    def sort_key(self) -> tuple:
        """Return tuple suitable for chronological sorting.

        Unknown components sort last: year→9999, month→13, day→32.
        """
        return (
            self.year if self.year is not None else 9999,
            self.month if self.month is not None else 13,
            self.day if self.day is not None else 32,
        )
