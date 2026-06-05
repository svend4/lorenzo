"""Priority-based task scheduler — E99.

Uses :class:`queue.PriorityQueue` and :class:`threading.Thread` (stdlib only).

Queue entries are ``(priority, seq, task)`` tuples so that tasks with equal
priority are processed in submission order (FIFO tie-breaking via a monotonic
sequence counter).

Worker loop behaviour
---------------------
* Dequeue entry.
* If the task was cancelled  → skip (CANCELLED already set by :meth:`cancel`).
* If a deadline was given and it has already passed → mark EXPIRED and skip.
* Otherwise run ``fn(*args, **kwargs)``, capture result *or* exception.
* Signal the per-task :class:`threading.Event` so that :meth:`result` unblocks.

Thread safety
-------------
``_registry`` (task_id → ScheduledTask) is protected by ``_lock``.
``_seq`` is incremented via the same lock.
"""
from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    CANCELLED = "cancelled"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class ScheduledTask:
    task_id: str = field(default_factory=lambda: uuid4().hex[:12])
    priority: int = 0           # lower number = higher priority
    fn: Callable = None
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    deadline: float | None = None   # absolute Unix timestamp; None = no expiry
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Exception | None = None

    # Internal synchronisation — not part of the public interface.
    _done_event: threading.Event = field(
        default_factory=threading.Event, repr=False, compare=False
    )


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

_SENTINEL = object()   # poison-pill placed in queue to stop workers


class PriorityScheduler:
    """Priority-based task scheduler backed by worker threads.

    Parameters
    ----------
    workers:
        Number of background worker threads.  Defaults to 2.
    now_fn:
        Callable that returns the current time as a float (Unix seconds).
        Defaults to :func:`time.time`.  Inject a custom function in tests to
        avoid real-time dependencies.

    Examples
    --------
    >>> sched = PriorityScheduler(workers=2)
    >>> sched.start()
    >>> task = sched.submit(lambda x: x * 2, 21, priority=0)
    >>> sched.result(task.task_id)
    42
    >>> sched.stop()
    """

    def __init__(
        self,
        workers: int = 2,
        now_fn: Callable[[], float] | None = None,
    ) -> None:
        self._workers_count = workers
        self._now = now_fn if now_fn is not None else time.time

        self._q: queue.PriorityQueue = queue.PriorityQueue()
        self._lock = threading.Lock()
        self._registry: dict[str, ScheduledTask] = {}
        self._seq = 0          # monotonic tie-breaker
        self._threads: list[threading.Thread] = []
        self._started = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start worker threads.  Safe to call only once."""
        if self._started:
            return
        self._started = True
        for i in range(self._workers_count):
            t = threading.Thread(
                target=self._worker_loop,
                name=f"priority-scheduler-worker-{i}",
                daemon=True,
            )
            t.start()
            self._threads.append(t)

    def stop(self, wait: bool = True) -> None:
        """Stop worker threads.

        Parameters
        ----------
        wait:
            If *True* (default) drain the queue and wait for all workers to
            finish.  If *False* enqueue sentinels immediately and return.
        """
        if not self._started:
            return
        # One sentinel per worker so every thread exits its loop.
        # PriorityQueue is a min-heap: lower tuple → dequeued first.
        # We want sentinels to be processed *after* all real tasks that
        # were already in the queue, so we give them the highest possible
        # (priority, seq) values.
        sentinel_priority = 999_999_999
        for _ in self._threads:
            with self._lock:
                self._seq += 1
                seq = self._seq
            self._q.put((sentinel_priority, seq, _SENTINEL))
        if wait:
            for t in self._threads:
                t.join()
        self._started = False
        self._threads.clear()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit(
        self,
        fn: Callable,
        *args,
        priority: int = 0,
        deadline: float | None = None,
        **kwargs,
    ) -> ScheduledTask:
        """Add *fn* to the queue and return a :class:`ScheduledTask` immediately.

        Parameters
        ----------
        fn:
            Callable to execute.
        *args:
            Positional arguments forwarded to *fn*.
        priority:
            Lower number = higher priority.  Default ``0``.
        deadline:
            Absolute Unix timestamp.  If the worker picks up the task after
            this point the task is marked :attr:`TaskStatus.EXPIRED` and
            *fn* is not called.  ``None`` means no expiry.
        **kwargs:
            Keyword arguments forwarded to *fn*.
        """
        task = ScheduledTask(
            priority=priority,
            fn=fn,
            args=args,
            kwargs=kwargs,
            deadline=deadline,
        )
        with self._lock:
            self._seq += 1
            seq = self._seq
            self._registry[task.task_id] = task
        # PriorityQueue is a min-heap; lower tuple sorts first.
        self._q.put((priority, seq, task))
        return task

    def cancel(self, task_id: str) -> bool:
        """Mark a *pending* task as :attr:`TaskStatus.CANCELLED`.

        Returns ``True`` if the task existed *and* was still pending.
        Returns ``False`` if the task is not found, already running, done,
        failed, expired, or already cancelled.
        """
        with self._lock:
            task = self._registry.get(task_id)
            if task is None:
                return False
            if task.status != TaskStatus.PENDING:
                return False
            task.status = TaskStatus.CANCELLED
            task._done_event.set()
            return True

    def status(self, task_id: str) -> TaskStatus | None:
        """Return the current :class:`TaskStatus` of *task_id*, or ``None``."""
        with self._lock:
            task = self._registry.get(task_id)
            return task.status if task is not None else None

    def result(self, task_id: str, timeout: float = 5.0) -> Any:
        """Block until the task finishes and return its result value.

        Parameters
        ----------
        timeout:
            Maximum seconds to wait.  Defaults to ``5.0``.

        Raises
        ------
        KeyError
            If *task_id* is not found in the registry.
        TimeoutError
            If the task does not finish within *timeout* seconds.
        RuntimeError
            If the task was cancelled, expired, or failed.
        """
        with self._lock:
            task = self._registry.get(task_id)
        if task is None:
            raise KeyError(f"Unknown task_id: {task_id!r}")

        finished = task._done_event.wait(timeout=timeout)
        if not finished:
            raise TimeoutError(
                f"Task {task_id!r} did not complete within {timeout}s"
            )

        if task.status == TaskStatus.CANCELLED:
            raise RuntimeError(f"Task {task_id!r} was cancelled")
        if task.status == TaskStatus.EXPIRED:
            raise RuntimeError(f"Task {task_id!r} expired before execution")
        if task.status == TaskStatus.FAILED:
            raise RuntimeError(
                f"Task {task_id!r} failed: {task.error}"
            ) from task.error

        return task.result

    def pending_count(self) -> int:
        """Number of tasks currently in :attr:`TaskStatus.PENDING` state."""
        with self._lock:
            return sum(
                1
                for t in self._registry.values()
                if t.status == TaskStatus.PENDING
            )

    def stats(self) -> dict:
        """Return a dict with counts keyed by status name.

        Keys: ``total``, ``pending``, ``running``, ``done``, ``cancelled``,
        ``failed``, ``expired``.
        """
        counts: dict[str, int] = {
            "total": 0,
            "pending": 0,
            "running": 0,
            "done": 0,
            "cancelled": 0,
            "failed": 0,
            "expired": 0,
        }
        with self._lock:
            for task in self._registry.values():
                counts["total"] += 1
                counts[task.status.value] += 1
        return counts

    # ------------------------------------------------------------------
    # Internal worker
    # ------------------------------------------------------------------

    def _worker_loop(self) -> None:
        """Background worker: pull tasks from the queue and execute them."""
        while True:
            priority, seq, item = self._q.get()
            try:
                if item is _SENTINEL:
                    return

                task: ScheduledTask = item

                # ---- Check if already cancelled --------------------------
                with self._lock:
                    current_status = task.status
                if current_status == TaskStatus.CANCELLED:
                    continue

                # ---- Check deadline (expiry) ------------------------------
                if task.deadline is not None and self._now() > task.deadline:
                    with self._lock:
                        task.status = TaskStatus.EXPIRED
                    task._done_event.set()
                    continue

                # ---- Mark running and execute ----------------------------
                with self._lock:
                    task.status = TaskStatus.RUNNING

                try:
                    value = task.fn(*task.args, **task.kwargs)
                    with self._lock:
                        task.result = value
                        task.status = TaskStatus.DONE
                except Exception as exc:  # noqa: BLE001
                    with self._lock:
                        task.error = exc
                        task.status = TaskStatus.FAILED
                finally:
                    task._done_event.set()

            finally:
                self._q.task_done()
