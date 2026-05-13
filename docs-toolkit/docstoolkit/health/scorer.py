from dataclasses import dataclass
from docstoolkit.health.signals import HealthSignal, SignalLevel

# Weight of each signal level in health score
_LEVEL_WEIGHTS = {
    SignalLevel.OK: 1.0,
    SignalLevel.WARNING: 0.7,
    SignalLevel.ERROR: 0.4,
    SignalLevel.CRITICAL: 0.0,
}

@dataclass
class HealthScore:
    """Aggregate health score for the system."""
    score: float         # 0-1, weighted average of signal levels
    ok_count: int
    warning_count: int
    error_count: int
    critical_count: int
    total_signals: int

    def grade(self) -> str:
        """Letter grade: A(>=0.9), B(>=0.75), C(>=0.6), D(>=0.4), F(<0.4)"""
        if self.score >= 0.9:
            return "A"
        elif self.score >= 0.75:
            return "B"
        elif self.score >= 0.6:
            return "C"
        elif self.score >= 0.4:
            return "D"
        return "F"

    def is_healthy(self) -> bool:
        return self.critical_count == 0 and self.score >= 0.6


def compute_health_score(signals: list) -> HealthScore:
    """Compute aggregate health score from list[HealthSignal].

    score = sum(_LEVEL_WEIGHTS[s.level] for s in signals) / len(signals)
    Count each level.
    If empty signals: score=1.0, all counts=0.
    """
    if not signals:
        return HealthScore(score=1.0, ok_count=0, warning_count=0,
                          error_count=0, critical_count=0, total_signals=0)
    counts = {l: 0 for l in SignalLevel}
    total_weight = 0.0
    for s in signals:
        counts[s.level] += 1
        total_weight += _LEVEL_WEIGHTS[s.level]
    score = total_weight / len(signals)
    return HealthScore(
        score=score,
        ok_count=counts[SignalLevel.OK],
        warning_count=counts[SignalLevel.WARNING],
        error_count=counts[SignalLevel.ERROR],
        critical_count=counts[SignalLevel.CRITICAL],
        total_signals=len(signals),
    )
