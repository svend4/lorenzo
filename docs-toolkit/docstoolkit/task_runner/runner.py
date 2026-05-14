"""Task runner — E159.

Runs named tasks (functions) sequentially or in parallel with timing,
retries, condition-guarded execution, and result collection.

Uses only the standard library (`concurrent.futures.ThreadPoolExecutor`).
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class TaskStatus(Enum):
    """Lifecycle status of a single task execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class TaskResult:
    """Outcome of a single task execution."""

    task_name: str
    status: TaskStatus
    output: Any = None
    error: Optional[str] = None
    duration: float = 0.0
    attempts: int = 1


@dataclass
class TaskDef:
    """Definition of a task to run."""

    name: str
    func: Callable
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    timeout: Optional[float] = None
    max_retries: int = 0
    skip_on_failure: bool = False
    condition: Optional[Callable] = None


@dataclass
class RunResult:
    """Aggregate result of running a batch of tasks."""

    task_results: list
    total_duration: float

    @property
    def success_count(self) -> int:
        return sum(1 for r in self.task_results if r.status is TaskStatus.SUCCESS)

    @property
    def failure_count(self) -> int:
        return sum(
            1
            for r in self.task_results
            if r.status in (TaskStatus.FAILED, TaskStatus.TIMEOUT)
        )

    @property
    def all_success(self) -> bool:
        return bool(self.task_results) and all(
            r.status is TaskStatus.SUCCESS for r in self.task_results
        )

    def by_name(self, name: str) -> Optional[TaskResult]:
        for r in self.task_results:
            if r.task_name == name:
                return r
        return None


def _default_now() -> float:
    return time.perf_counter()


def _run_with_retries(
    task: TaskDef, now_fn: Callable[[], float]
) -> TaskResult:
    """Execute a task with retry support; no timeout enforcement."""
    # Condition gate
    if task.condition is not None:
        try:
            allowed = bool(task.condition())
        except Exception as exc:  # treat condition failure as skip
            return TaskResult(
                task_name=task.name,
                status=TaskStatus.SKIPPED,
                error=f"condition raised: {exc!r}",
                duration=0.0,
                attempts=0,
            )
        if not allowed:
            return TaskResult(
                task_name=task.name,
                status=TaskStatus.SKIPPED,
                error=None,
                duration=0.0,
                attempts=0,
            )

    attempts = 0
    start = now_fn()
    last_exc: Optional[BaseException] = None
    max_attempts = task.max_retries + 1
    while attempts < max_attempts:
        attempts += 1
        try:
            output = task.func(*task.args, **task.kwargs)
            duration = now_fn() - start
            return TaskResult(
                task_name=task.name,
                status=TaskStatus.SUCCESS,
                output=output,
                error=None,
                duration=duration,
                attempts=attempts,
            )
        except BaseException as exc:  # noqa: BLE001
            last_exc = exc

    duration = now_fn() - start
    status = TaskStatus.SKIPPED if task.skip_on_failure else TaskStatus.FAILED
    return TaskResult(
        task_name=task.name,
        status=status,
        output=None,
        error=repr(last_exc) if last_exc is not None else None,
        duration=duration,
        attempts=attempts,
    )


class TaskRunner:
    """Collects task definitions and runs them sequentially or in parallel."""

    def __init__(self) -> None:
        self._tasks: list[TaskDef] = []

    # ---- management ----
    def add_task(self, task: TaskDef) -> None:
        self._tasks.append(task)

    def add_tasks(self, tasks: list) -> None:
        for t in tasks:
            self.add_task(t)

    def clear(self) -> None:
        self._tasks.clear()

    def remove_task(self, name: str) -> bool:
        for i, t in enumerate(self._tasks):
            if t.name == name:
                del self._tasks[i]
                return True
        return False

    @property
    def task_count(self) -> int:
        return len(self._tasks)

    @property
    def task_names(self) -> list:
        return [t.name for t in self._tasks]

    # ---- execution ----
    def run_sequential(
        self, now_fn: Optional[Callable[[], float]] = None
    ) -> RunResult:
        now = now_fn or _default_now
        results: list[TaskResult] = []
        batch_start = now()
        for task in list(self._tasks):
            results.append(_run_with_retries(task, now))
        total = now() - batch_start
        return RunResult(task_results=results, total_duration=total)

    def run_parallel(
        self,
        max_workers: int = 4,
        now_fn: Optional[Callable[[], float]] = None,
    ) -> RunResult:
        now = now_fn or _default_now
        tasks = list(self._tasks)
        results: list[Optional[TaskResult]] = [None] * len(tasks)

        batch_start = now()
        if not tasks:
            return RunResult(task_results=[], total_duration=now() - batch_start)

        # Workers must be at least 1
        workers = max(1, int(max_workers))

        with ThreadPoolExecutor(max_workers=workers) as pool:
            future_to_idx = {}
            for idx, task in enumerate(tasks):
                # Check condition synchronously (cheap, deterministic ordering)
                if task.condition is not None:
                    try:
                        allowed = bool(task.condition())
                    except Exception as exc:
                        results[idx] = TaskResult(
                            task_name=task.name,
                            status=TaskStatus.SKIPPED,
                            error=f"condition raised: {exc!r}",
                            duration=0.0,
                            attempts=0,
                        )
                        continue
                    if not allowed:
                        results[idx] = TaskResult(
                            task_name=task.name,
                            status=TaskStatus.SKIPPED,
                            error=None,
                            duration=0.0,
                            attempts=0,
                        )
                        continue

                start = now()
                future = pool.submit(
                    _execute_with_retries_only, task, now, start
                )
                future_to_idx[future] = (idx, task, start)

            for future, (idx, task, start) in future_to_idx.items():
                try:
                    if task.timeout is not None:
                        result = future.result(timeout=task.timeout)
                    else:
                        result = future.result()
                    results[idx] = result
                except FuturesTimeout:
                    duration = now() - start
                    results[idx] = TaskResult(
                        task_name=task.name,
                        status=TaskStatus.TIMEOUT,
                        output=None,
                        error=f"timed out after {task.timeout}s",
                        duration=duration,
                        attempts=1,
                    )
                except BaseException as exc:  # safety net
                    duration = now() - start
                    status = (
                        TaskStatus.SKIPPED
                        if task.skip_on_failure
                        else TaskStatus.FAILED
                    )
                    results[idx] = TaskResult(
                        task_name=task.name,
                        status=status,
                        output=None,
                        error=repr(exc),
                        duration=duration,
                        attempts=1,
                    )

        total = now() - batch_start
        # All slots filled
        final = [r for r in results if r is not None]
        return RunResult(task_results=final, total_duration=total)


def _execute_with_retries_only(
    task: TaskDef, now_fn: Callable[[], float], start: float
) -> TaskResult:
    """Like _run_with_retries, but condition already checked and start time supplied."""
    attempts = 0
    last_exc: Optional[BaseException] = None
    max_attempts = task.max_retries + 1
    while attempts < max_attempts:
        attempts += 1
        try:
            output = task.func(*task.args, **task.kwargs)
            duration = now_fn() - start
            return TaskResult(
                task_name=task.name,
                status=TaskStatus.SUCCESS,
                output=output,
                error=None,
                duration=duration,
                attempts=attempts,
            )
        except BaseException as exc:  # noqa: BLE001
            last_exc = exc

    duration = now_fn() - start
    status = TaskStatus.SKIPPED if task.skip_on_failure else TaskStatus.FAILED
    return TaskResult(
        task_name=task.name,
        status=status,
        output=None,
        error=repr(last_exc) if last_exc is not None else None,
        duration=duration,
        attempts=attempts,
    )
