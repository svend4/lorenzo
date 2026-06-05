"""Persistent SQLite-backed job queue (E110).

Provides a priority-aware, retry-capable job queue with scheduled execution
support.  Pure stdlib — no third-party dependencies required.

Quick start::

    from docstoolkit.job_queue import JobQueue, JobStatus

    q = JobQueue()                                    # in-memory by default
    job = q.enqueue("resize_image", {"path": "/tmp/photo.jpg"}, priority=1)

    ready = q.dequeue()                               # atomically → RUNNING
    if ready:
        try:
            # ... do work ...
            q.complete(ready.job_id, result={"width": 800})
        except Exception as exc:
            q.fail(ready.job_id, error=str(exc))      # auto-retry if configured

    q.close()

Scheduled jobs::

    import time
    q = JobQueue()
    q.enqueue("nightly_report", run_at=time.time() + 86400)   # tomorrow
    q.dequeue()  # returns None until run_at <= now

See :mod:`docstoolkit.job_queue.queue` for the full API reference.
"""
from docstoolkit.job_queue.queue import Job, JobQueue, JobStatus

__all__ = [
    "Job",
    "JobQueue",
    "JobStatus",
]
