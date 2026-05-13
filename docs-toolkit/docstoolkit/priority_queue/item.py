from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class Priority(int, Enum):
    LOW = 1
    NORMAL = 5
    HIGH = 10
    CRITICAL = 100

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class PriorityJob:
    job_id: str
    payload: str                          # JSON string
    priority: Priority = Priority.NORMAL
    status: JobStatus = JobStatus.PENDING
    owner: str = ""                       # for fair-share grouping
    created_ts: str = ""
    started_ts: str = ""
    done_ts: str = ""
    attempt_count: int = 0
    error: str = ""

    def __post_init__(self):
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec='seconds')

    def is_terminal(self) -> bool:
        return self.status in (JobStatus.DONE, JobStatus.FAILED, JobStatus.CANCELLED)

    def duration_ms(self) -> float:
        """Elapsed ms between started_ts and done_ts. 0.0 if not available."""
        try:
            s = datetime.fromisoformat(self.started_ts)
            e = datetime.fromisoformat(self.done_ts)
            return (e - s).total_seconds() * 1000
        except Exception:
            return 0.0
