from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class CircuitState(str, Enum):
    CLOSED = "closed"       # normal operation
    OPEN = "open"           # failing, reject calls
    HALF_OPEN = "half_open" # testing recovery

@dataclass
class CircuitStats:
    """Rolling stats for a circuit breaker."""
    total_calls: int = 0
    success_count: int = 0
    failure_count: int = 0
    rejected_count: int = 0     # calls rejected while OPEN
    last_failure_ts: str = ""
    last_success_ts: str = ""

    def failure_rate(self) -> float:
        """failure_count / (success_count + failure_count), 0.0 if no calls."""
        denom = self.success_count + self.failure_count
        if denom == 0:
            return 0.0
        return self.failure_count / denom

    def record_success(self) -> None:
        self.total_calls += 1
        self.success_count += 1
        self.last_success_ts = datetime.now().isoformat(timespec='seconds')

    def record_failure(self) -> None:
        self.total_calls += 1
        self.failure_count += 1
        self.last_failure_ts = datetime.now().isoformat(timespec='seconds')

    def record_rejected(self) -> None:
        self.total_calls += 1
        self.rejected_count += 1

    def reset(self) -> None:
        self.__init__()
