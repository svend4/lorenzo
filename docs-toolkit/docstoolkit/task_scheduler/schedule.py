"""TaskSchedule: schedule types and next-run calculation.

Supports three scheduling modes:
- ONCE: run at a specific Unix timestamp (or immediately if run_at=0)
- INTERVAL: run repeatedly every interval_seconds
- CRON_LIKE: run at specific minutes/hours (cron-style, no external deps)
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum


class ScheduleType(Enum):
    ONCE = "once"
    INTERVAL = "interval"
    CRON_LIKE = "cron_like"


@dataclass
class TaskSchedule:
    """Describes when and how often a task should run.

    Args:
        schedule_type: one of ONCE, INTERVAL, CRON_LIKE
        interval_seconds: seconds between runs (INTERVAL only)
        run_at: Unix timestamp for ONCE; 0 means "run immediately"
        cron_minutes: list of allowed minutes (0-59); empty = every minute
        cron_hours: list of allowed hours (0-23); empty = every hour
    """
    schedule_type: ScheduleType
    interval_seconds: float = 0.0
    run_at: float = 0.0
    cron_minutes: list = field(default_factory=list)
    cron_hours: list = field(default_factory=list)

    def next_run(self, after: float = None) -> float:
        """Return the next Unix timestamp at which this task should run.

        Args:
            after: reference Unix timestamp (defaults to time.time())

        Returns:
            float Unix timestamp, or float('inf') if no future run exists.
        """
        if after is None:
            after = time.time()

        if self.schedule_type == ScheduleType.ONCE:
            # run_at == 0 means "run immediately" — treat as epoch 0, which
            # is always <= any realistic 'after', so we return float('inf')
            # only after the task has conceptually fired.  The scheduler calls
            # next_run(after=now) before the first run, so we must return 0
            # (or run_at) when it is >= 0 and <= after only if we haven't run
            # yet.  The simplest contract: return run_at if run_at >= after,
            # else float('inf').  When run_at==0 it is < after, so the
            # scheduler must handle the "run immediately" logic by checking
            # run_at <= now on the first tick (see TaskScheduler.tick).
            # To support "run immediately": return 0 which is always <= now.
            target = self.run_at  # may be 0 (immediate)
            if target <= after:
                # already in the past — only valid before first execution
                return target
            return target

        if self.schedule_type == ScheduleType.INTERVAL:
            return after + self.interval_seconds

        if self.schedule_type == ScheduleType.CRON_LIKE:
            return self._next_cron(after)

        return float("inf")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _next_cron(self, after: float) -> float:
        """Advance minute-by-minute until both hour and minute match."""
        import math as _math

        minutes = self.cron_minutes  # [] = every minute
        hours = self.cron_hours      # [] = every hour

        # Start from the next whole minute after 'after'
        # e.g. if after = 1000.5 → candidate starts at minute boundary 1001
        # We floor to the current minute, then add 60 s to get "next" minute.
        current_minute_start = _math.floor(after / 60) * 60
        candidate = current_minute_start + 60  # start one minute ahead

        limit = after + 24 * 3600  # search no further than 24 h

        while candidate <= limit:
            import time as _time
            t = _time.gmtime(candidate)
            m = t.tm_min
            h = t.tm_hour

            minute_ok = (not minutes) or (m in minutes)
            hour_ok = (not hours) or (h in hours)

            if minute_ok and hour_ok:
                return float(candidate)

            candidate += 60  # advance one minute

        return float("inf")
