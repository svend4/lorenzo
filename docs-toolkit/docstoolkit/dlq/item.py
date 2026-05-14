from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class FailureReason(str, Enum):
    TIMEOUT = "timeout"
    ERROR = "error"
    VALIDATION = "validation"
    DEPENDENCY = "dependency"
    UNKNOWN = "unknown"

@dataclass
class DeadLetterItem:
    """A failed job entry in the dead letter queue."""
    job_id: str
    payload: str          # JSON-serializable job payload (as string)
    reason: FailureReason
    error_message: str = ""
    attempt_count: int = 1
    first_failure_ts: str = ""
    last_failure_ts: str = ""
    resolved: bool = False
    tags: list = field(default_factory=list)  # list[str]

    def __post_init__(self):
        now = datetime.now().isoformat(timespec='seconds')
        if not self.first_failure_ts:
            self.first_failure_ts = now
        if not self.last_failure_ts:
            self.last_failure_ts = now

    def mark_resolved(self) -> None:
        self.resolved = True

    def increment_attempt(self) -> None:
        self.attempt_count += 1
        self.last_failure_ts = datetime.now().isoformat(timespec='seconds')

    def age_seconds(self) -> float:
        """Seconds since first_failure_ts. Returns 0.0 on parse error."""
        try:
            first = datetime.fromisoformat(self.first_failure_ts)
            return (datetime.now() - first).total_seconds()
        except Exception:
            return 0.0
