"""Thread-safe priority job queue.

Uses heapq under a Lock + Condition for waiters. Lower priority value wins;
ties are broken by insertion order (FIFO).
"""
from __future__ import annotations

import heapq
import itertools
import threading
import time
from typing import Optional

from docstoolkit.worker_queue.job import Job, JobStatus


class JobQueue:
    """Thread-safe priority queue with a registry of all known jobs.

    The registry tracks jobs in any non-terminal state (QUEUED, RUNNING,
    RETRYING). Finished jobs (SUCCESS, FAILED, DEAD) remain in the registry
    so workers can update their result and clients can inspect them via
    ``get(job_id)``.

    Cancelled jobs stay in the heap until naturally dequeued, but are
    filtered out at that point so ``cancel`` is O(1).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        # Heap entries: (priority, counter, job_id). Counter preserves FIFO.
        self._heap: list[tuple[int, int, str]] = []
        self._counter = itertools.count()
        # All jobs we know about, indexed by id.
        self._registry: dict[str, Job] = {}
        # Active queued count: jobs in the heap that are still QUEUED.
        # (Cancelled entries remain in heap but are skipped when popped.)
        self._queued_count = 0

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def enqueue(self, job: Job) -> str:
        """Add a job to the queue and return its job_id."""
        with self._cond:
            # Ensure status reflects queued state on (re)enqueue.
            job.status = JobStatus.QUEUED
            self._registry[job.job_id] = job
            heapq.heappush(
                self._heap,
                (job.priority, next(self._counter), job.job_id),
            )
            self._queued_count += 1
            self._cond.notify()
            return job.job_id

    def dequeue(self, timeout: Optional[float] = None) -> Optional[Job]:
        """Pop and return the highest-priority queued job.

        If the queue is empty, block up to ``timeout`` seconds. Returns
        ``None`` if no job is available within that window. A ``timeout``
        of ``None`` waits forever; ``0`` returns immediately when empty.
        """
        with self._cond:
            deadline = (time.monotonic() + timeout) if timeout is not None else None
            while True:
                job = self._pop_valid_locked()
                if job is not None:
                    return job
                # Empty (or only stale entries). Wait.
                if timeout is None:
                    self._cond.wait()
                    continue
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return None
                self._cond.wait(timeout=remaining)

    def peek(self) -> Optional[Job]:
        """Return the next job without removing it, or None if empty."""
        with self._lock:
            # Skip stale entries without mutating the queued count.
            while self._heap:
                _, _, jid = self._heap[0]
                job = self._registry.get(jid)
                if job is not None and job.status == JobStatus.QUEUED:
                    return job
                # Remove the stale top entry and keep looking.
                heapq.heappop(self._heap)
            return None

    def cancel(self, job_id: str) -> bool:
        """Mark a QUEUED job as FAILED. Returns True if it was queued."""
        with self._cond:
            job = self._registry.get(job_id)
            if job is None or job.status != JobStatus.QUEUED:
                return False
            job.status = JobStatus.FAILED
            job.finished_at = time.time()
            job.error = job.error or "cancelled"
            self._queued_count = max(0, self._queued_count - 1)
            # Notify in case a waiter is hanging on a heap that is now
            # effectively empty.
            self._cond.notify_all()
            return True

    def clear(self) -> int:
        """Remove all queued jobs. Returns the number cleared."""
        with self._cond:
            cleared = 0
            for _, _, jid in self._heap:
                job = self._registry.get(jid)
                if job is not None and job.status == JobStatus.QUEUED:
                    job.status = JobStatus.FAILED
                    job.finished_at = time.time()
                    job.error = job.error or "cleared"
                    cleared += 1
            self._heap.clear()
            self._queued_count = 0
            self._cond.notify_all()
            return cleared

    # ------------------------------------------------------------------
    # Read-only
    # ------------------------------------------------------------------
    def size(self) -> int:
        """Number of jobs currently waiting to be dequeued."""
        with self._lock:
            return self._queued_count

    def is_empty(self) -> bool:
        """True when no jobs are waiting to be dequeued."""
        return self.size() == 0

    def get(self, job_id: str) -> Optional[Job]:
        """Look up a job by id; returns None if unknown."""
        with self._lock:
            return self._registry.get(job_id)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _pop_valid_locked(self) -> Optional[Job]:
        """Pop the next still-QUEUED job. Caller must hold ``self._lock``."""
        while self._heap:
            _, _, jid = heapq.heappop(self._heap)
            job = self._registry.get(jid)
            if job is None:
                # Should not happen but be defensive.
                continue
            if job.status != JobStatus.QUEUED:
                # Stale entry (cancelled / cleared). Skip without touching
                # _queued_count (already adjusted at cancel/clear time).
                continue
            self._queued_count = max(0, self._queued_count - 1)
            return job
        return None
