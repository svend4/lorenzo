"""Event and EventEnvelope dataclasses for the E84 event sourcing module."""
import time
from dataclasses import dataclass, field
from uuid import uuid4


def _short_uuid() -> str:
    """Generate a short 12-character hex UUID."""
    return uuid4().hex[:12]


@dataclass
class Event:
    """An immutable domain event record.

    Attributes
    ----------
    event_id:
        Unique identifier for the event (12 hex chars, auto-generated).
    aggregate_id:
        Identifier of the aggregate this event belongs to.
    event_type:
        Name of the event (e.g. ``"user.created"``).
    payload:
        Event-specific data.
    version:
        Monotonically increasing version within the aggregate (default 1).
    timestamp:
        Unix timestamp (float) when the event was created.
    """

    aggregate_id: str = ""
    event_type: str = ""
    event_id: str = field(default_factory=_short_uuid)
    payload: dict = field(default_factory=dict)
    version: int = 1
    timestamp: float = field(default_factory=time.time)


@dataclass
class EventEnvelope:
    """Wraps an :class:`Event` with its global sequence number.

    Attributes
    ----------
    event:
        The underlying domain event.
    sequence:
        Global ordering value assigned by the EventStore.
    """

    event: Event
    sequence: int
