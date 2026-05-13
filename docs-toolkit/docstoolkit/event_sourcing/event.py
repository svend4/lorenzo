"""DomainEvent — base immutable event record for event sourcing."""
import time
import uuid
from dataclasses import dataclass, field


def _short_uuid() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class DomainEvent:
    """Immutable domain event record.

    Attributes:
        event_id:       Short UUID4 (8 hex chars), auto-generated.
        event_type:     Name of the event (e.g. ``"user.created"``).
        aggregate_id:   ID of the aggregate this event belongs to.
        aggregate_type: Type name of the aggregate (e.g. ``"User"``).
        payload:        Event-specific data.
        ts:             Unix timestamp (float), auto-generated.
        version:        Monotonically increasing version within the aggregate.
        metadata:       Optional extra metadata (correlation IDs, author, …).
    """

    event_type: str
    aggregate_id: str
    aggregate_type: str
    payload: dict
    event_id: str = field(default_factory=_short_uuid)
    ts: float = field(default_factory=time.time)
    version: int = 1
    metadata: dict = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a plain-dict representation suitable for JSON encoding."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "payload": self.payload,
            "ts": self.ts,
            "version": self.version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DomainEvent":
        """Reconstruct a :class:`DomainEvent` from a plain dict."""
        return cls(
            event_id=d["event_id"],
            event_type=d["event_type"],
            aggregate_id=d["aggregate_id"],
            aggregate_type=d["aggregate_type"],
            payload=d["payload"],
            ts=d["ts"],
            version=d["version"],
            metadata=d.get("metadata", {}),
        )
