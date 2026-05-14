import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EventCategory(str, Enum):
    AUTH = "auth"
    ACCESS = "access"
    MUTATION = "mutation"
    ADMIN = "admin"
    SYSTEM = "system"


@dataclass
class AuditEvent:
    """One immutable audit log entry."""
    event_id: str
    category: EventCategory
    action: str                # e.g. "doc.create", "user.login"
    actor: str                 # user_id or "system"
    resource: str = ""         # e.g. doc_id
    detail: dict = field(default_factory=dict)
    ts: str = ""
    prev_hash: str = ""        # hash of previous event (chain)
    event_hash: str = ""       # hash of this event's content

    def __post_init__(self):
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')

    def compute_hash(self) -> str:
        """SHA-256 of canonical JSON: event_id, category, action, actor,
        resource, ts, prev_hash (sorted keys, no whitespace).
        Returns hex[:32].
        """
        data = {
            "event_id": self.event_id,
            "category": self.category.value if isinstance(self.category, EventCategory) else self.category,
            "action": self.action,
            "actor": self.actor,
            "resource": self.resource,
            "ts": self.ts,
            "prev_hash": self.prev_hash,
        }
        canonical = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode()).hexdigest()[:32]

    def seal(self) -> None:
        """Compute and store event_hash."""
        self.event_hash = self.compute_hash()

    def verify(self) -> bool:
        """Return True if stored event_hash matches recomputed hash."""
        return self.event_hash == self.compute_hash()
