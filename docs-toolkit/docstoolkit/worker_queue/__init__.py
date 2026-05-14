"""E89 Worker Queue — thread-safe in-process priority job queue.

Pure stdlib only. Designed for orchestrating CPU/IO work inside a single
process without pulling in Redis / RQ / Celery.

Quick start::

    from docstoolkit.worker_queue import (
        JobQueue, Job, WorkerConfig, WorkerPool, JobHandler,
    )

    class Echo(JobHandler):
        def handle(self, job):
            return job.payload

    q = JobQueue()
    pool = WorkerPool(q, Echo(), WorkerConfig(worker_count=2))
    pool.start()
    q.enqueue(Job(name="hi", payload={"msg": "hello"}))
    # ... do other work ...
    pool.stop()
"""
from docstoolkit.worker_queue.job import JobStatus, Job
from docstoolkit.worker_queue.queue import JobQueue
from docstoolkit.worker_queue.worker import WorkerConfig, JobHandler, WorkerPool

__all__ = [
    "JobStatus",
    "Job",
    "JobQueue",
    "WorkerConfig",
    "JobHandler",
    "WorkerPool",
]
