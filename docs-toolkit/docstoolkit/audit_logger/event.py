"""AuditAction enum and AuditEvent dataclass."""
import time
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class AuditAction(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SEARCH = "SEARCH"
    EXPORT = "EXPORT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"
    CONFIG_CHANGE = "CONFIG_CHANGE"


@dataclass
class AuditEvent:
    """A single audit log entry."""
    action: AuditAction
    actor: str
    resource: str
    event_id: str = field(default_factory=lambda: uuid4().hex)
    resource_id: str = ""
    details: dict = field(default_factory=dict)
    outcome: str = "success"
    ts: float = field(default_factory=time.time)
    ip_address: str = ""
    session_id: str = ""

    def to_dict(self) -> dict:
        """Return all fields; action as its string value."""
        return {
            "event_id": self.event_id,
            "action": self.action.value,
            "actor": self.actor,
            "resource": self.resource,
            "resource_id": self.resource_id,
            "details": self.details,
            "outcome": self.outcome,
            "ts": self.ts,
            "ip_address": self.ip_address,
            "session_id": self.session_id,
        }
