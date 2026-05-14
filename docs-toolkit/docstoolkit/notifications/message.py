from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class NotificationLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Channel(str, Enum):
    LOG = "log"
    STORE = "store"
    EMAIL = "email"     # stub (no real sending)
    SLACK = "slack"     # stub
    NULL = "null"       # discard


@dataclass
class Notification:
    title: str
    body: str
    level: NotificationLevel = NotificationLevel.INFO
    source: str = ""    # module/system that generated it
    tags: list = field(default_factory=list)
    ts: str = ""
    notification_id: str = ""

    def __post_init__(self):
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')
        if not self.notification_id:
            import hashlib
            self.notification_id = hashlib.md5(
                f"{self.title}{self.ts}".encode()
            ).hexdigest()[:12]

    def is_urgent(self) -> bool:
        return self.level in (NotificationLevel.ERROR, NotificationLevel.CRITICAL)

    def to_dict(self) -> dict:
        return {
            "notification_id": self.notification_id,
            "title": self.title,
            "body": self.body,
            "level": self.level.value,
            "source": self.source,
            "tags": self.tags,
            "ts": self.ts,
        }
