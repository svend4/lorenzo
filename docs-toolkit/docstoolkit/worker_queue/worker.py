"""Worker pool that consumes jobs from a JobQueue.

Each worker is a daemon thread that polls the queue, runs the supplied
handler, updates the job state, and applies a retry / dead-letter policy.
"""
from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from docstoolkit.worker_queue.job import Job, JobStatus
from docstoolkit.worker_queue.queue import JobQueue


@dataclass
class WorkerConfig:
    """Worker pool configuration."""

    worker_count: int = 1
    poll_interval: float = 0.05


class JobHandler(ABC):
    """Strategy interface for processing jobs."""

    @abstractmethod
    def handle(self, job: Job) -> Any:
        """Run a single job. Raise an exception to signal failure."""
        raise NotImplementedError


class WorkerPool:
    """A pool of worker threads pulling jobs from a queue.

    The pool is started with :meth:`start` and stopped with :meth:`stop`.
    Each worker:

    1. Calls ``queue.dequeue(timeout=poll_interval)``.
    2. If a job arrives, marks it RUNNING, calls ``handler.handle(job)``.
    3. On success: status SUCCESS, ``result`` recorded.
    4. On exception: if ``attempts < max_attempts`` the job is re-enqueued
       in state RETRYING; otherwise it goes FAILED + DEAD.

    Counters ``success_count``, ``failed_count`` and ``processed_count``
    are updated atomically.
    """

    def __init__(
        self,
        queue: JobQueue,
        handler: JobHandler,
        config: Optional[WorkerConfig] = None,
    ) -> None:
        self.queue = queue
        self.handler = handler
        self.config = config if config is not None else WorkerConfig()
        self._threads: list[threading.Thread] = []
        self._stop_event = threading.Event()
        self._started = False
        self._counter_lock = threading.Lock()
        self.success_count = 0
        self.failed_count = 0
        self.processed_count = 0

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def start(self) -> None:
        """Spawn ``worker_count`` daemon threads. Idempotent: only first
        call has an effect."""
        if self._started:
            return
        self._started = True
        self._stop_event.clear()
        for idx in range(max(1, self.config.worker_count)):
            t = threading.Thread(
                target=self._worker_loop,
                name=f"WorkerPool-{idx}",
                daemon=True,
            )
            t.start()
            self._threads.append(t)

    def stop(self, wait: bool = True) -> None:
        """Signal all workers to exit. If ``wait`` is True, join them."""
        self._stop_event.set()
        if wait:
            for t in self._threads:
                # Give workers a chance to wake from the queue's wait().
                # The queue's dequeue() uses poll_interval timeouts so they
                # will return None and observe the stop event quickly.
                t.join(timeout=max(1.0, self.config.poll_interval * 20))
        self._threads = []
        self._started = False

    # ------------------------------------------------------------------
    # Worker body
    # ------------------------------------------------------------------
    def _worker_loop(self) -> None:
        poll = max(0.001, float(self.config.poll_interval))
        while not self._stop_event.is_set():
            job = self.queue.dequeue(timeout=poll)
            if job is None:
                continue
            self._process(job)

    def _process(self, job: Job) -> None:
        # Mark running.
        job.attempts += 1
        job.status = JobStatus.RUNNING
        job.started_at = time.time()
        try:
            result = self.handler.handle(job)
        except Exception as exc:  # noqa: BLE001 - want to catch all handler errors
            self._on_failure(job, exc)
        else:
            self._on_success(job, result)

    def _on_success(self, job: Job, result: Any) -> None:
        job.result = result
        job.status = JobStatus.SUCCESS
        job.finished_at = time.time()
        job.error = ""
        with self._counter_lock:
            self.success_count += 1
            self.processed_count += 1

    def _on_failure(self, job: Job, exc: BaseException) -> None:
        job.error = f"{type(exc).__name__}: {exc}"
        if job.attempts < job.max_attempts:
            # Re-queue for another attempt.
            job.status = JobStatus.RETRYING
            job.finished_at = 0.0
            job.started_at = 0.0
            # enqueue() will flip status back to QUEUED.
            self.queue.enqueue(job)
        else:
            job.status = JobStatus.DEAD
            job.finished_at = time.time()
            with self._counter_lock:
                self.failed_count += 1
                self.processed_count += 1
