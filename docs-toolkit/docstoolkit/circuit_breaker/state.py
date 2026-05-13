"""CircuitState enum and CircuitStats dataclass."""
from dataclasses import dataclass, field
from enum import Enum


class CircuitState(str, Enum):
    """States of a circuit breaker."""
    CLOSED = "closed"       # normal: requests pass through
    OPEN = "open"           # tripped: requests fail fast
    HALF_OPEN = "half_open" # testing recovery with limited requests


@dataclass
class CircuitStats:
    """Rolling counters for a circuit breaker."""
    total_calls: int = 0
    failures: int = 0
    successes: int = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    last_failure_time: float = 0.0

    def failure_rate(self) -> float:
        """Return failures / total_calls, or 0.0 if total_calls == 0."""
        if self.total_calls == 0:
            return 0.0
        return self.failures / self.total_calls

    def reset(self) -> None:
        """Zero all fields."""
        self.total_calls = 0
        self.failures = 0
        self.successes = 0
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.last_failure_time = 0.0
