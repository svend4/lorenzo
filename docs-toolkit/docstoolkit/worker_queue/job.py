"""Job and JobStatus definitions for the worker queue.

Pure stdlib only — no external dependencies.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class JobStatus(str, Enum):
    """Lifecycle states for a Job."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD = "dead"


@dataclass
class Job:
    """A unit of work to be processed by the worker pool.

    Attributes:
        job_id: Unique identifier (12-char hex).
        name: Optional human-readable label / handler hint.
        payload: Arbitrary data passed to the handler.
        priority: Lower number means higher priority (1 first, 5 default).
        status: Current lifecycle state.
        enqueued_at: UNIX timestamp when added to the queue.
        started_at: UNIX timestamp when last started (0 if never).
        finished_at: UNIX timestamp when finished (0 if not finished).
        attempts: Number of times the worker has tried to run this job.
        max_attempts: Cap on retries before going DEAD.
        error: Last error message (empty if none).
        result: Handler return value on success.
    """

    job_id: str = field(default_factory=lambda: uuid4().hex[:12])
    name: str = ""
    payload: dict = field(default_factory=dict)
    priority: int = 5
    status: JobStatus = JobStatus.QUEUED
    enqueued_at: float = field(default_factory=time.time)
    started_at: float = 0.0
    finished_at: float = 0.0
    attempts: int = 0
    max_attempts: int = 3
    error: str = ""
    result: Any = None
