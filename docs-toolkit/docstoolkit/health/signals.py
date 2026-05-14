from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class SignalLevel(str, Enum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class HealthSignal:
    """One health signal from a subsystem."""
    name: str                    # e.g. "feedback.satisfaction_rate"
    level: SignalLevel
    value: float                 # numeric value (0-1 for rates, raw for counts)
    message: str = ""
    subsystem: str = ""          # e.g. "feedback", "eval", "governance"
    ts: str = ""

    def __post_init__(self):
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')

    def is_healthy(self) -> bool:
        return self.level == SignalLevel.OK

    def is_critical(self) -> bool:
        return self.level == SignalLevel.CRITICAL


@dataclass
class HealthCheck:
    """A named health check with threshold-based evaluation."""
    name: str
    subsystem: str
    value_fn: object = None     # callable() -> float; ignored in tests
    warn_threshold: float = 0.7
    error_threshold: float = 0.5
    critical_threshold: float = 0.3
    higher_is_better: bool = True

    def evaluate(self, value: float) -> HealthSignal:
        """Evaluate value against thresholds.

        If higher_is_better=True:
          value >= warn_threshold → OK
          value >= error_threshold → WARNING
          value >= critical_threshold → ERROR
          else → CRITICAL

        If higher_is_better=False (e.g. error rate):
          value <= critical_threshold → OK
          value <= error_threshold → WARNING
          value <= warn_threshold → ERROR
          else → CRITICAL
        """
        if self.higher_is_better:
            if value >= self.warn_threshold:
                level = SignalLevel.OK
            elif value >= self.error_threshold:
                level = SignalLevel.WARNING
            elif value >= self.critical_threshold:
                level = SignalLevel.ERROR
            else:
                level = SignalLevel.CRITICAL
        else:
            if value <= self.critical_threshold:
                level = SignalLevel.OK
            elif value <= self.error_threshold:
                level = SignalLevel.WARNING
            elif value <= self.warn_threshold:
                level = SignalLevel.ERROR
            else:
                level = SignalLevel.CRITICAL
        return HealthSignal(
            name=self.name,
            level=level,
            value=value,
            subsystem=self.subsystem,
        )
