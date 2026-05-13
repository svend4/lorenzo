"""TaskScheduler: tick-driven, thread-pool-backed task execution engine."""
from __future__ import annotations

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from docstoolkit.task_scheduler.schedule import ScheduleType
from docstoolkit.task_scheduler.task import ScheduledTask, TaskResult, TaskStatus


@dataclass
class SchedulerConfig:
    """Configuration for the TaskScheduler.

    Attributes:
        tick_interval: seconds between automatic ticks (informational;
            the scheduler does not self-tick — callers drive tick() manually
            or via a loop)
        max_workers: size of the ThreadPoolExecutor worker pool
    """
    tick_interval: float = 0.1
    max_workers: int = 4


class TaskScheduler:
    """Manages a registry of ScheduledTask objects and executes them.

    The scheduler is *tick-driven*: callers must call tick() periodically.
    Each tick checks which tasks are due and dispatches them to a shared
    ThreadPoolExecutor.

    Thread safety: the internal task registry is protected by a lock so that
    add_task / remove_task / tick can be called from different threads.
    """

    def __init__(self, config: Optional[SchedulerConfig] = None) -> None:
        self._config = config or SchedulerConfig()
        self._tasks: Dict[str, ScheduledTask] = {}
        self._lock = threading.Lock()
        # Track the last time each task was triggered so that INTERVAL
        # scheduling can compute the correct next_run reference point.
        self._last_triggered: Dict[str, float] = {}
        self._executor = ThreadPoolExecutor(
            max_workers=self._config.max_workers,
            thread_name_prefix="task_scheduler",
        )

    # ------------------------------------------------------------------
    # Registry management
    # ------------------------------------------------------------------

    def add_task(self, task: ScheduledTask) -> str:
        """Register a task and return its task_id."""
        with self._lock:
            self._tasks[task.task_id] = task
        return task.task_id

    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the registry. Returns True if it existed."""
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                self._last_triggered.pop(task_id, None)
                return True
            return False

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Return the task with the given id, or None."""
        with self._lock:
            return self._tasks.get(task_id)

    def list_tasks(self) -> List[ScheduledTask]:
        """Return a snapshot list of all registered tasks."""
        with self._lock:
            return list(self._tasks.values())

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def run_now(self, task_id: str) -> TaskResult:
        """Execute a task synchronously right now, ignoring its schedule.

        Applies retry logic (max_retries).  Updates task.last_result and
        task.run_count.  Does NOT disable ONCE tasks (use tick for that).

        Raises:
            KeyError: if task_id is not registered.
        """
        with self._lock:
            task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"Unknown task_id: {task_id!r}")
        result = self._execute_with_retries(task)
        with self._lock:
            # Re-fetch in case the task was removed between the two locks
            live = self._tasks.get(task_id)
            if live is not None:
                live.last_result = result
                live.run_count += 1
        return result

    def tick(self, now: float = None) -> List[TaskResult]:
        """Check all tasks and execute those that are due.

        A task is *due* when:
            - it is enabled, AND
            - its schedule.next_run(last_triggered) <= now

        For ONCE tasks: they are compared against their run_at directly
        (last_triggered is not used on first execution).

        After execution:
            - ONCE tasks are disabled (enabled = False).
            - INTERVAL/CRON_LIKE tasks remain enabled; last_triggered is
              updated to *now* so the next tick computes the correct window.

        All due tasks in one tick are submitted to the ThreadPoolExecutor
        concurrently.  The method blocks until all submitted futures complete.

        Args:
            now: reference Unix timestamp (defaults to time.time())

        Returns:
            list of TaskResult for every task that ran during this tick.
        """
        if now is None:
            now = time.time()

        with self._lock:
            tasks_snapshot = list(self._tasks.values())

        due: List[ScheduledTask] = []
        for task in tasks_snapshot:
            if not task.enabled:
                continue
            last = self._last_triggered.get(task.task_id)
            if task.schedule.schedule_type == ScheduleType.ONCE:
                # For ONCE tasks, last_triggered being None means not yet run.
                # next_run always returns run_at (possibly 0 = immediate).
                if last is not None:
                    # Already ran once; should have been disabled but guard
                    # here anyway.
                    continue
                target = task.schedule.run_at  # 0 = immediate
                if target <= now:
                    due.append(task)
            else:
                # INTERVAL / CRON_LIKE
                if last is None:
                    # First time we see this task: record the current time as
                    # the reference point so that future ticks can correctly
                    # determine when the interval has elapsed.
                    self._last_triggered[task.task_id] = now
                    last = now
                nxt = task.schedule.next_run(after=last)
                if nxt <= now:
                    due.append(task)

        if not due:
            return []

        futures = {}
        for task in due:
            future = self._executor.submit(self._execute_with_retries, task)
            futures[future] = task

        results: List[TaskResult] = []
        for future in as_completed(futures):
            task = futures[future]
            result = future.result()  # never raises; _execute_with_retries catches all

            with self._lock:
                live = self._tasks.get(task.task_id)
                if live is not None:
                    live.last_result = result
                    live.run_count += 1
                    if live.schedule.schedule_type == ScheduleType.ONCE:
                        live.enabled = False

            self._last_triggered[task.task_id] = now
            results.append(result)

        return results

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def pending_count(self) -> int:
        """Number of tasks whose last_result status is PENDING (never run)."""
        with self._lock:
            return sum(
                1
                for t in self._tasks.values()
                if t.last_result is None or t.last_result.status == TaskStatus.PENDING
            )

    def cancel(self, task_id: str) -> bool:
        """Disable a task so it will not run on future ticks.

        Returns True if the task existed, False otherwise.
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            task.enabled = False
            return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _execute_with_retries(self, task: ScheduledTask) -> TaskResult:
        """Run task.func(*task.args, **task.kwargs) with up to max_retries retries.

        Always returns a TaskResult; never raises.
        """
        attempts = task.max_retries + 1  # first attempt + retries
        last_error = ""
        started_at = time.time()

        for attempt in range(attempts):
            try:
                return_value = task.func(*task.args, **task.kwargs)
                finished_at = time.time()
                return TaskResult(
                    task_id=task.task_id,
                    status=TaskStatus.COMPLETED,
                    started_at=started_at,
                    finished_at=finished_at,
                    return_value=return_value,
                    error="",
                )
            except Exception as exc:  # noqa: BLE001
                last_error = f"{type(exc).__name__}: {exc}"
                # On last attempt, fall through to return FAILED
                if attempt < attempts - 1:
                    # Brief back-off could go here, but per spec: stdlib only
                    continue

        finished_at = time.time()
        return TaskResult(
            task_id=task.task_id,
            status=TaskStatus.FAILED,
            started_at=started_at,
            finished_at=finished_at,
            return_value=None,
            error=last_error,
        )
