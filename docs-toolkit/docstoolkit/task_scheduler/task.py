"""TaskResult and ScheduledTask dataclasses for the task scheduler."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from uuid import uuid4

from docstoolkit.task_scheduler.schedule import TaskSchedule


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    """Outcome of a single task execution.

    Attributes:
        task_id: identifier of the task that produced this result
        status: final TaskStatus after execution
        started_at: Unix timestamp when execution began
        finished_at: Unix timestamp when execution ended
        return_value: whatever the task callable returned (None on failure)
        error: string representation of the exception, empty on success
    """
    task_id: str
    status: TaskStatus
    started_at: float
    finished_at: float
    return_value: object = None
    error: str = ""

    def duration(self) -> float:
        """Wall-clock seconds between start and finish."""
        return self.finished_at - self.started_at


@dataclass
class ScheduledTask:
    """A callable paired with a schedule and execution metadata.

    Attributes:
        name: human-readable label
        func: callable to invoke
        schedule: when/how often to run
        task_id: auto-generated UUID hex; override to set a fixed id
        args: positional arguments forwarded to func
        kwargs: keyword arguments forwarded to func
        max_retries: how many times to re-attempt on failure (0 = no retries)
        enabled: if False the task is skipped by the scheduler
        last_result: result of the most recent execution (None if never run)
        run_count: total number of times the task has been executed
    """
    name: str
    func: Callable
    schedule: TaskSchedule
    task_id: str = field(default_factory=lambda: uuid4().hex)
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    max_retries: int = 0
    enabled: bool = True
    last_result: "TaskResult | None" = field(default=None, repr=False)
    run_count: int = 0
