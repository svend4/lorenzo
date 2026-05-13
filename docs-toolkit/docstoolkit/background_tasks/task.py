"""Task dataclass and enums for the background tasks module (E78)."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskPriority(Enum):
    LOW = 1
    NORMAL = 5
    HIGH = 10


@dataclass
class Task:
    """A unit of work to be executed in the background.

    Attributes:
        task_id: short hex identifier, auto-generated
        func: callable to invoke
        args: positional arguments forwarded to func
        kwargs: keyword arguments forwarded to func
        state: current lifecycle state
        priority: scheduling priority (higher value = higher priority)
        timeout: maximum allowed run time in seconds; 0 means no limit
        created_at: Unix timestamp when the task was created
        started_at: Unix timestamp when execution began (0 if not yet started)
        finished_at: Unix timestamp when execution ended (0 if not yet finished)
        result: return value of func on SUCCESS, None otherwise
        error: string representation of the exception on FAILED/TIMEOUT, empty otherwise
    """

    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    state: TaskState = TaskState.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: float = 0.0
    created_at: float = field(default_factory=time.time)
    started_at: float = 0.0
    finished_at: float = 0.0
    result: Any = None
    error: str = ""
    task_id: str = field(default_factory=lambda: uuid4().hex[:12])

    def duration(self) -> float:
        """Wall-clock seconds between start and finish.

        Returns 0.0 if the task has not both started and finished.
        """
        if self.started_at > 0.0 and self.finished_at > 0.0:
            return self.finished_at - self.started_at
        return 0.0
