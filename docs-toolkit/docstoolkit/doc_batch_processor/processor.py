"""DocBatchProcessor — job-based batch processing with progress tracking (E297).

Processes documents in configurable batches with per-job progress counters,
configurable error tolerance, cancel/delete lifecycle, and full thread safety
via a single :class:`threading.Lock`.

Uses only the Python standard library.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------

@dataclass
class BatchJob:
    """State record for a single batch job.

    Attributes:
        job_id:       Unique identifier (auto-generated UUID string).
        name:         Human-readable label supplied at creation time.
        total_items:  Total number of items to process.
        processed:    Items processed so far (success + failure).
        succeeded:    Items that completed without error.
        failed:       Items that raised an exception.
        status:       One of ``"pending"``, ``"running"``, ``"completed"``,
                      ``"failed"``, ``"cancelled"``.
        started_at:   Unix timestamp when :meth:`DocBatchProcessor.run_job`
                      began (0.0 if not yet started).
        completed_at: Unix timestamp when the job finished (0.0 if not done).
        errors:       Human-readable error strings collected during processing.
    """

    job_id: str
    name: str
    total_items: int
    processed: int = 0
    succeeded: int = 0
    failed: int = 0
    status: str = "pending"
    started_at: float = 0.0
    completed_at: float = 0.0
    errors: list[str] = field(default_factory=list)


@dataclass
class BatchResult:
    """Summary returned by :meth:`DocBatchProcessor.run_job`.

    Attributes:
        job_id:      Identifier of the job that was executed.
        total:       Total items attempted.
        succeeded:   Items processed without error.
        failed:      Items that raised an exception.
        duration_ms: Wall-clock duration in milliseconds.
        errors:      Error messages collected during processing.
    """

    job_id: str
    total: int
    succeeded: int
    failed: int
    duration_ms: float
    errors: list[str]


# ---------------------------------------------------------------------------
# Main processor
# ---------------------------------------------------------------------------

class DocBatchProcessor:
    """Job-based batch processor with progress tracking and error handling.

    Thread-safe: all mutations to the internal job registry are protected by a
    single :class:`threading.Lock`.  ``run_job`` itself executes synchronously
    in the calling thread.

    Args:
        batch_size:  Number of items per processing batch (default 10).
        max_errors:  Error tolerance policy.
                     ``0`` — abort on the very first error (``failed > 0``
                     triggers abort immediately after the first failing item).
                     ``N > 0`` — continue until *failed* exceeds *N*, then abort.

    Example::

        proc = DocBatchProcessor(batch_size=5, max_errors=2)
        job  = proc.create_job("demo", ["a", "b", "c"])
        result = proc.run_job(job.job_id, str.upper)
        assert result.succeeded == 3
    """

    def __init__(self, batch_size: int = 10, max_errors: int = 0) -> None:
        if batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        self._batch_size = batch_size
        self._max_errors = max_errors
        self._jobs: dict[str, BatchJob] = {}
        self._items: dict[str, list[Any]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Job lifecycle
    # ------------------------------------------------------------------

    def create_job(self, name: str, items: list[Any]) -> BatchJob:
        """Create and register a new batch job.

        Args:
            name:  Human-readable label for the job.
            items: List of items to process.

        Returns:
            :class:`BatchJob` with ``status='pending'`` and a freshly
            generated UUID ``job_id``.
        """
        job_id = str(uuid.uuid4())
        job = BatchJob(
            job_id=job_id,
            name=name,
            total_items=len(items),
        )
        with self._lock:
            self._jobs[job_id] = job
            self._items[job_id] = list(items)
        return job

    def run_job(
        self,
        job_id: str,
        processor_fn: Callable[[Any], Any],
        now: Optional[float] = None,
    ) -> Optional[BatchResult]:
        """Execute a pending job synchronously.

        Applies *processor_fn* to each item in batches of ``self.batch_size``.
        Updates ``job.processed``, ``job.succeeded``, and ``job.failed`` as
        items complete.  Collects errors as strings in ``job.errors``.

        Abort logic (governed by ``max_errors``):

        - ``max_errors == 0``: abort after the *first* failure
          (i.e. when ``failed > 0``).
        - ``max_errors > 0``:  abort when ``failed > max_errors``.

        On normal completion the job status is set to ``"completed"``.
        On abort it is set to ``"failed"``.
        If the job is not found, returns ``None``.

        Args:
            job_id:       ID of the job to run.
            processor_fn: Callable applied to each item.
            now:          Optional fixed timestamp (for deterministic testing).

        Returns:
            :class:`BatchResult` on success or abort, ``None`` if not found.
        """
        with self._lock:
            if job_id not in self._jobs:
                return None
            job = self._jobs[job_id]
            items = list(self._items.get(job_id, []))

        # Cannot run a cancelled or already-finished job
        if job.status not in ("pending", "running"):
            return None

        start_ts = now if now is not None else time.time()
        with self._lock:
            job.status = "running"
            job.started_at = start_ts

        aborted = False
        for batch_start in range(0, max(len(items), 1), self._batch_size):
            batch = items[batch_start: batch_start + self._batch_size]
            for item in batch:
                # Check if cancelled between items
                with self._lock:
                    current_status = job.status
                if current_status == "cancelled":
                    aborted = True
                    break

                try:
                    processor_fn(item)
                    with self._lock:
                        job.processed += 1
                        job.succeeded += 1
                except Exception as exc:  # noqa: BLE001
                    with self._lock:
                        job.processed += 1
                        job.failed += 1
                        job.errors.append(str(exc))
                    # Abort check
                    with self._lock:
                        failed_now = job.failed
                    if self._max_errors == 0 or failed_now > self._max_errors:
                        aborted = True

                if aborted:
                    break
            if aborted:
                break

        end_ts = now if now is not None else time.time()
        duration_ms = (end_ts - start_ts) * 1000.0

        with self._lock:
            if job.status != "cancelled":
                job.status = "failed" if aborted else "completed"
            job.completed_at = end_ts
            result = BatchResult(
                job_id=job_id,
                total=job.processed,
                succeeded=job.succeeded,
                failed=job.failed,
                duration_ms=duration_ms,
                errors=list(job.errors),
            )
        return result

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def get_job(self, job_id: str) -> Optional[BatchJob]:
        """Return the :class:`BatchJob` for *job_id*, or ``None`` if not found."""
        with self._lock:
            return self._jobs.get(job_id)

    def job_progress(self, job_id: str) -> Optional[float]:
        """Return progress as a float in ``[0.0, 1.0]``, or ``None`` if not found.

        Returns ``0.0`` for a job with zero total items (avoids division by zero).
        Returns ``1.0`` for a completed/failed/cancelled job regardless of counters.
        """
        with self._lock:
            job = self._jobs.get(job_id)
        if job is None:
            return None
        if job.total_items == 0:
            return 0.0
        return min(1.0, job.processed / job.total_items)

    def list_jobs(self, status: Optional[str] = None) -> list[BatchJob]:
        """Return all registered jobs, optionally filtered by *status*.

        Args:
            status: If given, only jobs with ``job.status == status`` are
                    returned.  Pass ``None`` to return all jobs.

        Returns:
            List of :class:`BatchJob` instances (unordered).
        """
        with self._lock:
            jobs = list(self._jobs.values())
        if status is not None:
            jobs = [j for j in jobs if j.status == status]
        return jobs

    @property
    def total_jobs(self) -> int:
        """Total number of registered jobs (all statuses)."""
        with self._lock:
            return len(self._jobs)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def cancel_job(self, job_id: str) -> bool:
        """Mark a pending or running job as ``'cancelled'``.

        Args:
            job_id: ID of the job to cancel.

        Returns:
            ``True`` if the job existed and its status was ``'pending'`` or
            ``'running'`` (and has now been changed to ``'cancelled'``).
            ``False`` otherwise.
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return False
            if job.status in ("pending", "running"):
                job.status = "cancelled"
                return True
            return False

    def delete_job(self, job_id: str) -> bool:
        """Remove a job record from the registry.

        Args:
            job_id: ID of the job to delete.

        Returns:
            ``True`` if the job existed and was removed, ``False`` otherwise.
        """
        with self._lock:
            if job_id in self._jobs:
                del self._jobs[job_id]
                self._items.pop(job_id, None)
                return True
            return False
