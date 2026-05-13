from dataclasses import dataclass
from docstoolkit.priority_queue.queue import PriorityJobQueue
from docstoolkit.priority_queue.item import PriorityJob, Priority

@dataclass
class SchedulerConfig:
    max_concurrent: int = 4
    fair_share_window: int = 10   # max jobs per owner before yielding

class FairShareScheduler:
    """Wraps PriorityJobQueue with fair-share allocation across owners."""

    def __init__(self, queue: PriorityJobQueue, config: SchedulerConfig | None = None):
        self._queue = queue
        self._config = config or SchedulerConfig()
        self._owner_counts: dict = {}   # {owner: jobs dequeued this cycle}

    def next_job(self) -> PriorityJob | None:
        """Pick next job respecting fair-share limits.

        Algorithm:
        1. Find owner with fewest jobs dequeued this cycle (among owners with pending jobs)
        2. Dequeue highest-priority job for that owner
        3. If all owners hit fair_share_window, reset counts and retry
        """
        # Get pending owners
        stats = self._queue._conn.execute(
            "SELECT owner, COUNT(*) as cnt FROM priority_jobs "
            "WHERE status='pending' GROUP BY owner"
        ).fetchall()
        if not stats:
            return None

        # Find owner not yet at fair_share_window with fewest dequeued
        eligible = [
            r["owner"] for r in stats
            if self._owner_counts.get(r["owner"], 0) < self._config.fair_share_window
        ]
        if not eligible:
            self._owner_counts.clear()
            eligible = [r["owner"] for r in stats]

        # Pick owner with fewest dequeued (stable: alphabetical tiebreak)
        owner = min(eligible, key=lambda o: (self._owner_counts.get(o, 0), o))
        job = self._queue.dequeue(owner=owner)
        if job:
            self._owner_counts[owner] = self._owner_counts.get(owner, 0) + 1
        return job

    def reset_cycle(self) -> None:
        """Reset fair-share counters for new scheduling cycle."""
        self._owner_counts.clear()
