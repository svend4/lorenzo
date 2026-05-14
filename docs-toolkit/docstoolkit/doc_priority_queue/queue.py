"""Document priority queue with deadline-aware ordering, retries, and stats."""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional


class TaskState(Enum):
    """Lifecycle state of a task."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class Priority(IntEnum):
    """Task priority. Higher value means higher priority (HIGHEST=4)."""

    LOWEST = 0
    LOW = 1
    NORMAL = 2
    HIGH = 3
    HIGHEST = 4


@dataclass
class Task:
    """A single processing task on a document."""

    task_id: str
    doc_id: str
    action: str
    priority: Priority
    payload: dict = field(default_factory=dict)
    state: TaskState = TaskState.QUEUED
    created_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    deadline: Optional[float] = None
    attempts: int = 0
    max_attempts: int = 3
    last_error: Optional[str] = None

    def is_overdue(self, now: float) -> bool:
        """Return True if this task has a deadline at or before `now`."""
        return self.deadline is not None and self.deadline <= now


@dataclass
class QueueStats:
    """Aggregate counts across the queue."""

    total: int
    queued: int
    in_progress: int
    completed: int
    failed: int
    expired: int
    by_priority: dict
    oldest_queued_age: Optional[float] = None


class DocPriorityQueue:
    """In-memory priority queue of document processing tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- ordering
    @staticmethod
    def _sort_key(task: Task) -> tuple:
        """Return sort key. Higher priority first, earlier deadline, earlier created."""
        # Negate priority so heapq-style "smallest is first" gives HIGHEST first.
        deadline = task.deadline if task.deadline is not None else float("inf")
        return (-int(task.priority), deadline, task.created_at)

    def _queued_sorted(self) -> list[Task]:
        msgs = [t for t in self._tasks.values() if t.state == TaskState.QUEUED]
        msgs.sort(key=self._sort_key)
        return msgs

    # ---------------------------------------------------------------- enqueue
    def enqueue(
        self,
        doc_id: str,
        action: str,
        priority: Priority = Priority.NORMAL,
        payload: Optional[dict] = None,
        deadline: Optional[float] = None,
        max_attempts: int = 3,
        now: float = 0.0,
    ) -> Task:
        """Create and enqueue a new task. Returns the task."""
        task = Task(
            task_id=uuid.uuid4().hex,
            doc_id=doc_id,
            action=action,
            priority=priority,
            payload=dict(payload) if payload else {},
            state=TaskState.QUEUED,
            created_at=now,
            deadline=deadline,
            max_attempts=max_attempts,
        )
        with self._lock:
            self._tasks[task.task_id] = task
        return task

    # ---------------------------------------------------------------- dequeue / peek
    def dequeue(self, now: float = 0.0) -> Optional[Task]:
        """Pop the highest-priority queued task and mark it IN_PROGRESS."""
        with self._lock:
            queued = self._queued_sorted()
            if not queued:
                return None
            task = queued[0]
            task.state = TaskState.IN_PROGRESS
            task.started_at = now
            task.attempts += 1
            return task

    def peek(self, now: float = 0.0) -> Optional[Task]:
        """Return the highest-priority queued task without dequeueing."""
        with self._lock:
            queued = self._queued_sorted()
            return queued[0] if queued else None

    # ---------------------------------------------------------------- state transitions
    def complete(self, task_id: str, now: float = 0.0) -> bool:
        """Mark a task as COMPLETED. Returns True on success."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            if task.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.EXPIRED):
                return False
            task.state = TaskState.COMPLETED
            task.completed_at = now
            return True

    def fail(
        self,
        task_id: str,
        error: Optional[str] = None,
        retry: bool = True,
        now: float = 0.0,
    ) -> bool:
        """Mark a task as failed. If retry allowed and attempts < max, requeue."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            if task.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.EXPIRED):
                return False
            task.last_error = error
            if retry and task.attempts < task.max_attempts:
                task.state = TaskState.QUEUED
                task.started_at = None
            else:
                task.state = TaskState.FAILED
                task.completed_at = now
            return True

    def cancel(self, task_id: str) -> bool:
        """Remove a task from storage. Returns True if removed."""
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def expire_overdue(self, now: float = 0.0) -> int:
        """Mark QUEUED tasks whose deadline <= now as EXPIRED. Returns count."""
        with self._lock:
            count = 0
            for task in self._tasks.values():
                if task.state == TaskState.QUEUED and task.is_overdue(now):
                    task.state = TaskState.EXPIRED
                    task.completed_at = now
                    count += 1
            return count

    # ---------------------------------------------------------------- lookups
    def get_task(self, task_id: str) -> Optional[Task]:
        with self._lock:
            return self._tasks.get(task_id)

    def tasks_for_doc(self, doc_id: str) -> list[Task]:
        with self._lock:
            return [t for t in self._tasks.values() if t.doc_id == doc_id]

    def tasks_by_state(self, state: TaskState) -> list[Task]:
        with self._lock:
            return [t for t in self._tasks.values() if t.state == state]

    def tasks_by_action(self, action: str) -> list[Task]:
        with self._lock:
            return [t for t in self._tasks.values() if t.action == action]

    # ---------------------------------------------------------------- sizes
    def queue_size(self, now: float = 0.0) -> int:
        """Number of tasks currently in QUEUED state."""
        with self._lock:
            return sum(1 for t in self._tasks.values() if t.state == TaskState.QUEUED)

    def in_progress_size(self) -> int:
        with self._lock:
            return sum(
                1 for t in self._tasks.values() if t.state == TaskState.IN_PROGRESS
            )

    def next_deadline(self, now: float = 0.0) -> Optional[float]:
        """Return the earliest deadline among queued tasks, or None."""
        with self._lock:
            deadlines = [
                t.deadline
                for t in self._tasks.values()
                if t.state == TaskState.QUEUED and t.deadline is not None
            ]
            return min(deadlines) if deadlines else None

    # ---------------------------------------------------------------- stats
    def stats(self, now: float = 0.0) -> QueueStats:
        with self._lock:
            total = len(self._tasks)
            queued = 0
            in_progress = 0
            completed = 0
            failed = 0
            expired = 0
            by_priority: dict = {p: 0 for p in Priority}
            oldest_queued_age: Optional[float] = None
            for task in self._tasks.values():
                if task.state == TaskState.QUEUED:
                    queued += 1
                    age = now - task.created_at
                    if oldest_queued_age is None or age > oldest_queued_age:
                        oldest_queued_age = age
                elif task.state == TaskState.IN_PROGRESS:
                    in_progress += 1
                elif task.state == TaskState.COMPLETED:
                    completed += 1
                elif task.state == TaskState.FAILED:
                    failed += 1
                elif task.state == TaskState.EXPIRED:
                    expired += 1
                by_priority[task.priority] = by_priority.get(task.priority, 0) + 1
            return QueueStats(
                total=total,
                queued=queued,
                in_progress=in_progress,
                completed=completed,
                failed=failed,
                expired=expired,
                by_priority=by_priority,
                oldest_queued_age=oldest_queued_age,
            )

    # ---------------------------------------------------------------- bulk
    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()

    @property
    def total_tasks(self) -> int:
        with self._lock:
            return len(self._tasks)
