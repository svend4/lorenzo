from dataclasses import dataclass, field
from docstoolkit.dlq.item import DeadLetterItem

@dataclass
class PoisonReport:
    """Report of detected poison pill jobs."""
    poison_jobs: list = field(default_factory=list)   # list[str] job_ids
    threshold: int = 3
    total_checked: int = 0

    def poison_count(self) -> int:
        return len(self.poison_jobs)

    def poison_rate(self) -> float:
        if self.total_checked == 0:
            return 0.0
        return self.poison_count() / self.total_checked


class PoisonPillDetector:
    """Detects jobs that have failed too many times (poison pills)."""

    def __init__(self, threshold: int = 3):
        """threshold: minimum attempt_count to be considered a poison pill."""
        self.threshold = threshold

    def is_poison(self, item: DeadLetterItem) -> bool:
        return item.attempt_count >= self.threshold and not item.resolved

    def scan(self, items: list) -> PoisonReport:
        """Scan list[DeadLetterItem] and return PoisonReport."""
        poison_ids = [
            item.job_id for item in items if self.is_poison(item)
        ]
        return PoisonReport(
            poison_jobs=poison_ids,
            threshold=self.threshold,
            total_checked=len(items),
        )

    def quarantine(self, items: list) -> tuple:
        """Split items into (clean, poison) lists."""
        clean = [i for i in items if not self.is_poison(i)]
        poison = [i for i in items if self.is_poison(i)]
        return clean, poison
