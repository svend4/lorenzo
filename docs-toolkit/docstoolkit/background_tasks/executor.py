"""BackgroundExecutor — thread-pool backed task executor (E78).

Uses only the Python standard library (threading, concurrent.futures).
"""
from __future__ import annotations

import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from docstoolkit.background_tasks.task import Task, TaskPriority, TaskState


@dataclass
class ExecutorConfig:
    """Configuration for :class:`BackgroundExecutor`.

    Attributes:
        max_workers: number of threads in the pool (default 4)
        queue_size: maximum number of queued (PENDING) tasks; 0 = unlimited
    """

    max_workers: int = 4
    queue_size: int = 0  # 0 = unlimited


class BackgroundExecutor:
    """Thread-pool backed executor for :class:`Task` objects.

    All public methods are thread-safe.

    Example::

        executor = BackgroundExecutor()
        task_id = executor.submit_fn(my_func, arg1, arg2, timeout=5.0)
        task = executor.wait(task_id)
        print(task.state, task.result)
        executor.shutdown()
    """

    def __init__(self, config: Optional[ExecutorConfig] = None) -> None:
        self._config = config or ExecutorConfig()
        self._pool = ThreadPoolExecutor(max_workers=self._config.max_workers)
        self._tasks: Dict[str, Task] = {}
        self._futures: Dict[str, Future] = {}
        self._lock = threading.Lock()
        # Per-task events so wait() can block efficiently
        self._events: Dict[str, threading.Event] = {}

    # ------------------------------------------------------------------
    # Submission
    # ------------------------------------------------------------------

    def submit(self, task: Task) -> str:
        """Submit a :class:`Task` for execution.

        Sets *state* to ``PENDING`` and registers the task in the internal
        registry before dispatching it to the thread pool.

        Args:
            task: the task to run.

        Returns:
            The ``task_id`` string.

        Raises:
            OverflowError: if *queue_size* > 0 and the queue is already full.
        """
        with self._lock:
            if self._config.queue_size > 0:
                pending_count = sum(
                    1 for t in self._tasks.values() if t.state == TaskState.PENDING
                )
                if pending_count >= self._config.queue_size:
                    raise OverflowError(
                        f"Queue is full ({self._config.queue_size} tasks)"
                    )
            task.state = TaskState.PENDING
            self._tasks[task.task_id] = task
            event = threading.Event()
            self._events[task.task_id] = event
            future = self._pool.submit(self._run_task, task)
            self._futures[task.task_id] = future

        return task.task_id

    def submit_fn(
        self,
        func: Callable,
        *args: Any,
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout: float = 0.0,
        **kwargs: Any,
    ) -> str:
        """Convenience wrapper: create a :class:`Task` and submit it.

        Args:
            func: callable to run.
            *args: positional arguments forwarded to *func*.
            priority: scheduling priority.
            timeout: per-task timeout in seconds; 0 = no limit.
            **kwargs: keyword arguments forwarded to *func*.

        Returns:
            The ``task_id`` string of the newly created task.
        """
        task = Task(
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout=timeout,
        )
        return self.submit(task)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get(self, task_id: str) -> Optional[Task]:
        """Return the :class:`Task` with the given *task_id*, or ``None``."""
        with self._lock:
            return self._tasks.get(task_id)

    def results(self) -> List[Task]:
        """Return all tasks that have reached a terminal state."""
        terminal = {TaskState.SUCCESS, TaskState.FAILED, TaskState.TIMEOUT, TaskState.CANCELLED}
        with self._lock:
            return [t for t in self._tasks.values() if t.state in terminal]

    def pending(self) -> List[Task]:
        """Return all tasks in the PENDING state."""
        with self._lock:
            return [t for t in self._tasks.values() if t.state == TaskState.PENDING]

    def running(self) -> List[Task]:
        """Return all tasks in the RUNNING state."""
        with self._lock:
            return [t for t in self._tasks.values() if t.state == TaskState.RUNNING]

    # ------------------------------------------------------------------
    # Control
    # ------------------------------------------------------------------

    def cancel(self, task_id: str) -> bool:
        """Attempt to cancel the task with the given *task_id*.

        Cancellation is only possible when the task is still ``PENDING``.
        If the task is already ``RUNNING`` or in a terminal state this
        method returns ``False`` without raising.

        Args:
            task_id: identifier of the task to cancel.

        Returns:
            ``True`` if the task was successfully cancelled, ``False`` otherwise.
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            if task.state != TaskState.PENDING:
                return False
            task.state = TaskState.CANCELLED
            task.finished_at = time.time()
            # Try to cancel the underlying Future (best-effort; may have already started)
            future = self._futures.get(task_id)
            if future is not None:
                future.cancel()
            event = self._events.get(task_id)
            if event is not None:
                event.set()
        return True

    def wait(self, task_id: str, timeout: Optional[float] = None) -> Task:
        """Block until the task reaches a terminal state.

        Args:
            task_id: identifier of the task to wait for.
            timeout: maximum seconds to wait; ``None`` waits indefinitely.

        Returns:
            The :class:`Task` object (possibly still ``PENDING``/``RUNNING``
            if *timeout* elapsed before completion).

        Raises:
            KeyError: if *task_id* is not registered.
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise KeyError(f"Unknown task_id: {task_id!r}")
            event = self._events.get(task_id)

        if event is not None:
            event.wait(timeout=timeout)

        with self._lock:
            return self._tasks[task_id]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def shutdown(self, wait: bool = True) -> None:
        """Shut down the executor.

        Args:
            wait: if ``True`` (default) block until all running tasks finish.
        """
        self._pool.shutdown(wait=wait)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run_task(self, task: Task) -> None:
        """Execute *task* on the calling thread (a pool worker).

        Handles state transitions, timing, timeout enforcement, and
        exception capture.  Timeout is implemented by running *func*
        on a daemon thread and joining with a deadline.
        """
        # --- Check if the task was cancelled before we even started ---
        with self._lock:
            if task.state == TaskState.CANCELLED:
                event = self._events.get(task.task_id)
                if event is not None:
                    event.set()
                return
            task.state = TaskState.RUNNING
            task.started_at = time.time()

        try:
            if task.timeout > 0.0:
                self._run_with_timeout(task)
            else:
                task.result = task.func(*task.args, **task.kwargs)
                with self._lock:
                    task.state = TaskState.SUCCESS
        except Exception as exc:  # noqa: BLE001
            with self._lock:
                # Only set FAILED if not already set to TIMEOUT
                if task.state not in (TaskState.TIMEOUT,):
                    task.state = TaskState.FAILED
                    task.error = repr(exc)
        finally:
            with self._lock:
                task.finished_at = time.time()
            event = self._events.get(task.task_id)
            if event is not None:
                event.set()

    def _run_with_timeout(self, task: Task) -> None:
        """Run *task.func* with a per-task timeout.

        Spawns a daemon thread; if it doesn't finish within *task.timeout*
        seconds the task is marked as ``TIMEOUT``.
        """
        result_holder: list = []
        exc_holder: list = []

        def _target() -> None:
            try:
                result_holder.append(task.func(*task.args, **task.kwargs))
            except Exception as exc:  # noqa: BLE001
                exc_holder.append(exc)

        worker = threading.Thread(target=_target, daemon=True)
        worker.start()
        worker.join(timeout=task.timeout)

        if worker.is_alive():
            # Thread is still running — mark as TIMEOUT
            with self._lock:
                task.state = TaskState.TIMEOUT
                task.error = f"Task exceeded timeout of {task.timeout}s"
            # We intentionally do NOT kill the daemon thread; Python has no
            # safe thread-kill mechanism.  The thread will eventually finish
            # or be reaped when the process exits.
            return

        if exc_holder:
            raise exc_holder[0]

        task.result = result_holder[0] if result_holder else None
        with self._lock:
            task.state = TaskState.SUCCESS
