from dataclasses import dataclass, field
from datetime import datetime
from docstoolkit.health.signals import HealthSignal, SignalLevel, HealthCheck
from docstoolkit.health.scorer import HealthScore, compute_health_score

@dataclass
class HealthReport:
    """Full health report for the system."""
    ts: str
    score: HealthScore
    signals: list = field(default_factory=list)   # list[HealthSignal]
    subsystems: dict = field(default_factory=dict) # {subsystem: HealthScore}

    def critical_signals(self) -> list:
        return [s for s in self.signals if s.level == SignalLevel.CRITICAL]

    def signals_for(self, subsystem: str) -> list:
        return [s for s in self.signals if s.subsystem == subsystem]

    def to_dict(self) -> dict:
        return {
            "ts": self.ts,
            "score": self.score.score,
            "grade": self.score.grade(),
            "ok": self.score.ok_count,
            "warnings": self.score.warning_count,
            "errors": self.score.error_count,
            "critical": self.score.critical_count,
            "subsystems": {k: v.score for k, v in self.subsystems.items()},
        }


class HealthMonitor:
    """Collects checks and produces HealthReport."""

    def __init__(self):
        self._checks: list = []    # list[HealthCheck]

    def register(self, check: HealthCheck) -> None:
        self._checks.append(check)

    def run(self, values: dict) -> HealthReport:
        """Run all checks against provided values dict {check_name: float}.

        For each check: if check.name in values, evaluate; else skip.
        Compute overall score and per-subsystem scores.
        Return HealthReport.
        """
        signals = []
        for check in self._checks:
            if check.name in values:
                signal = check.evaluate(values[check.name])
                signals.append(signal)

        # Per-subsystem scores
        subsystems: dict = {}
        all_subsystems = set(s.subsystem for s in signals)
        for sub in all_subsystems:
            sub_signals = [s for s in signals if s.subsystem == sub]
            subsystems[sub] = compute_health_score(sub_signals)

        return HealthReport(
            ts=datetime.now().isoformat(timespec='seconds'),
            score=compute_health_score(signals),
            signals=signals,
            subsystems=subsystems,
        )
