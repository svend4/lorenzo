"""E346 DocExportQueue — queue for scheduled document export jobs.

Thread-safe, stdlib-only, dataclass-based export job queue.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExportJob:
    """A single scheduled document export job."""

    job_id: str
    doc_id: str
    format: str
    requested_by: str = ""
    requested_at: float = 0.0
    status: str = "queued"  # "queued", "running", "completed", "failed", "cancelled"
    priority: int = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    output_path: str = ""
    error: str = ""


@dataclass
class ExportStats:
    """Aggregate export-queue statistics."""

    total: int
    queued: int
    running: int
    completed: int
    failed: int
    cancelled: int


class DocExportQueue:
    """In-memory, thread-safe queue for document export jobs."""

    def __init__(self) -> None:
        self._jobs: dict[str, ExportJob] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- enqueue
    def enqueue(
        self,
        doc_id: str,
        format: str,
        requested_by: str = "",
        priority: int = 0,
        now: Optional[float] = None,
    ) -> ExportJob:
        """Create and store a new queued export job."""
        if now is None:
            now = time.time()
        job = ExportJob(
            job_id=uuid.uuid4().hex,
            doc_id=doc_id,
            format=format,
            requested_by=requested_by,
            requested_at=now,
            status="queued",
            priority=priority,
        )
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    # ---------------------------------------------------------------- start
    def start_job(self, job_id: str, now: Optional[float] = None) -> bool:
        """Transition a queued job to running. Only valid from 'queued'."""
        if now is None:
            now = time.time()
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.status != "queued":
                return False
            job.status = "running"
            job.started_at = now
            return True

    # ---------------------------------------------------------------- complete
    def complete_job(
        self,
        job_id: str,
        output_path: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Mark a running job as completed. Only valid from 'running'."""
        if now is None:
            now = time.time()
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.status != "running":
                return False
            job.status = "completed"
            job.completed_at = now
            job.output_path = output_path
            return True

    # ---------------------------------------------------------------- fail
    def fail_job(
        self,
        job_id: str,
        error: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Mark a running job as failed. Only valid from 'running'."""
        if now is None:
            now = time.time()
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.status != "running":
                return False
            job.status = "failed"
            job.completed_at = now
            job.error = error
            return True

    # ---------------------------------------------------------------- cancel
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a queued or running job."""
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.status not in ("queued", "running"):
                return False
            job.status = "cancelled"
            return True

    # ---------------------------------------------------------------- lookups
    def get_job(self, job_id: str) -> Optional[ExportJob]:
        """Return the ExportJob with the given id, or None."""
        with self._lock:
            return self._jobs.get(job_id)

    def next_queued(self) -> Optional[ExportJob]:
        """Return the highest-priority queued job without changing state.

        Sort order: priority desc, then requested_at asc.
        """
        with self._lock:
            queued = [j for j in self._jobs.values() if j.status == "queued"]
        if not queued:
            return None
        queued.sort(key=lambda j: (-j.priority, j.requested_at))
        return queued[0]

    def queued_jobs(self) -> list[ExportJob]:
        """Return all queued jobs sorted by (-priority, requested_at)."""
        with self._lock:
            jobs = [j for j in self._jobs.values() if j.status == "queued"]
        jobs.sort(key=lambda j: (-j.priority, j.requested_at))
        return jobs

    def jobs_by_status(self, status: str) -> list[ExportJob]:
        """Return all jobs with the given status, sorted by requested_at."""
        with self._lock:
            jobs = [j for j in self._jobs.values() if j.status == status]
        jobs.sort(key=lambda j: j.requested_at)
        return jobs

    def jobs_for_doc(self, doc_id: str) -> list[ExportJob]:
        """Return all jobs for a given doc_id, sorted by requested_at."""
        with self._lock:
            jobs = [j for j in self._jobs.values() if j.doc_id == doc_id]
        jobs.sort(key=lambda j: j.requested_at)
        return jobs

    # ---------------------------------------------------------------- delete
    def delete_job(self, job_id: str) -> bool:
        """Fully remove a job. True if existed."""
        with self._lock:
            if job_id in self._jobs:
                del self._jobs[job_id]
                return True
            return False

    def purge_completed(self) -> int:
        """Remove all completed and failed jobs. Return count removed."""
        with self._lock:
            ids = [
                jid
                for jid, j in self._jobs.items()
                if j.status in ("completed", "failed")
            ]
            for jid in ids:
                del self._jobs[jid]
            return len(ids)

    # ---------------------------------------------------------------- stats
    def stats(self) -> ExportStats:
        """Return aggregate counts by status."""
        with self._lock:
            queued = 0
            running = 0
            completed = 0
            failed = 0
            cancelled = 0
            for job in self._jobs.values():
                if job.status == "queued":
                    queued += 1
                elif job.status == "running":
                    running += 1
                elif job.status == "completed":
                    completed += 1
                elif job.status == "failed":
                    failed += 1
                elif job.status == "cancelled":
                    cancelled += 1
            total = len(self._jobs)
        return ExportStats(
            total=total,
            queued=queued,
            running=running,
            completed=completed,
            failed=failed,
            cancelled=cancelled,
        )
