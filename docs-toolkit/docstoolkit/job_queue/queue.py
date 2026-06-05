"""Persistent SQLite-backed job queue (E110).

Jobs have priorities, statuses, retry counts, and scheduled execution times.
A worker loop can poll the DB and run ready jobs.

Pure stdlib only.  Thread-safe via a threading.Lock.  WAL mode is enabled for
better concurrent read/write behaviour.

Typical usage::

    from docstoolkit.job_queue import JobQueue, JobStatus

    q = JobQueue(":memory:")
    job = q.enqueue("send_email", {"to": "alice@example.com"})
    ready = q.dequeue()           # returns the job and marks it RUNNING
    q.complete(ready.job_id, result={"sent": True})
    q.close()
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
from uuid import uuid4


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"  # run_at is in the future


@dataclass
class Job:
    job_id: str = field(default_factory=lambda: uuid4().hex[:12])
    name: str = ""
    payload: dict = field(default_factory=dict)
    priority: int = 0            # lower = higher priority
    status: JobStatus = JobStatus.PENDING
    run_at: float = 0.0          # epoch seconds; 0 = run immediately
    max_retries: int = 0
    retry_count: int = 0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    result: Any = None
    error: str = ""


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS jobs (
    job_id      TEXT    PRIMARY KEY,
    name        TEXT    NOT NULL DEFAULT '',
    payload     TEXT    NOT NULL DEFAULT '{}',
    priority    INTEGER NOT NULL DEFAULT 0,
    status      TEXT    NOT NULL DEFAULT 'pending',
    run_at      REAL    NOT NULL DEFAULT 0,
    max_retries INTEGER NOT NULL DEFAULT 0,
    retry_count INTEGER NOT NULL DEFAULT 0,
    created_at  REAL    NOT NULL,
    updated_at  REAL    NOT NULL,
    result      TEXT,
    error       TEXT    NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_jobs_dequeue
    ON jobs (status, run_at, priority);
CREATE INDEX IF NOT EXISTS idx_jobs_status
    ON jobs (status);
CREATE INDEX IF NOT EXISTS idx_jobs_name
    ON jobs (name);
"""


# ---------------------------------------------------------------------------
# JobQueue
# ---------------------------------------------------------------------------

class JobQueue:
    """Persistent, thread-safe job queue backed by SQLite.

    Parameters
    ----------
    db_path:
        File path for the SQLite database, or ``":memory:"`` for a transient
        in-memory database.
    now_fn:
        Callable that returns the current time as a float (epoch seconds).
        Defaults to :func:`time.time`.  Inject a custom function in tests to
        control virtual time.
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        now_fn: Optional[Callable[[], float]] = None,
    ) -> None:
        self._db_path = db_path
        self._now = now_fn if now_fn is not None else time.time
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def enqueue(
        self,
        name: str,
        payload: Optional[dict] = None,
        priority: int = 0,
        run_at: float = 0.0,
        max_retries: int = 0,
    ) -> Job:
        """Add a job to the queue and return the created :class:`Job`."""
        now = self._now()
        job = Job(
            name=name,
            payload=payload or {},
            priority=priority,
            status=JobStatus.PENDING,
            run_at=run_at,
            max_retries=max_retries,
            retry_count=0,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO jobs
                    (job_id, name, payload, priority, status, run_at,
                     max_retries, retry_count, created_at, updated_at,
                     result, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, '')
                """,
                (
                    job.job_id,
                    job.name,
                    json.dumps(job.payload, ensure_ascii=False),
                    job.priority,
                    job.status.value,
                    job.run_at,
                    job.max_retries,
                    job.retry_count,
                    job.created_at,
                    job.updated_at,
                ),
            )
            self._conn.commit()
        return job

    def dequeue(self) -> Optional[Job]:
        """Pick the next ready PENDING job and atomically mark it RUNNING.

        Selection criteria: ``status = 'pending'`` AND ``run_at <= now``,
        ordered by ``priority ASC`` (lowest = most urgent), then
        ``run_at ASC``.

        Returns ``None`` when no job is ready.
        Uses ``BEGIN IMMEDIATE`` to prevent concurrent workers from claiming
        the same row.
        """
        now = self._now()
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("BEGIN IMMEDIATE")
            try:
                row = cur.execute(
                    """
                    SELECT * FROM jobs
                    WHERE  status = 'pending'
                      AND  run_at <= ?
                    ORDER  BY priority ASC, run_at ASC
                    LIMIT  1
                    """,
                    (now,),
                ).fetchone()
                if row is None:
                    cur.execute("ROLLBACK")
                    return None
                updated_at = self._now()
                cur.execute(
                    "UPDATE jobs SET status = 'running', updated_at = ? WHERE job_id = ?",
                    (updated_at, row["job_id"]),
                )
                cur.execute("COMMIT")
            except Exception:
                cur.execute("ROLLBACK")
                raise
            # Re-read the freshly updated row outside the transaction.
            fresh = self._conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?", (row["job_id"],)
            ).fetchone()
            return self._row_to_job(fresh)

    def complete(self, job_id: str, result: Any = None) -> None:
        """Mark *job_id* as DONE and store an optional *result*."""
        now = self._now()
        result_json = json.dumps(result, ensure_ascii=False) if result is not None else None
        with self._lock:
            self._conn.execute(
                """
                UPDATE jobs
                SET status = 'done', result = ?, updated_at = ?
                WHERE job_id = ?
                """,
                (result_json, now, job_id),
            )
            self._conn.commit()

    def fail(self, job_id: str, error: str = "") -> None:
        """Handle a job failure.

        If ``retry_count < max_retries`` the job is re-enqueued as PENDING
        with exponential-ish back-off (``retry_count * 5`` extra seconds).
        Otherwise the job is marked FAILED.
        """
        now = self._now()
        with self._lock:
            row = self._conn.execute(
                "SELECT retry_count, max_retries FROM jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
            if row is None:
                return

            retry_count: int = row["retry_count"]
            max_retries: int = row["max_retries"]

            if retry_count < max_retries:
                new_retry_count = retry_count + 1
                backoff = new_retry_count * 5          # seconds
                new_run_at = now + backoff
                self._conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'pending',
                        retry_count = ?,
                        run_at = ?,
                        error = ?,
                        updated_at = ?
                    WHERE job_id = ?
                    """,
                    (new_retry_count, new_run_at, error, now, job_id),
                )
            else:
                self._conn.execute(
                    """
                    UPDATE jobs
                    SET status = 'failed', error = ?, updated_at = ?
                    WHERE job_id = ?
                    """,
                    (error, now, job_id),
                )
            self._conn.commit()

    def cancel(self, job_id: str) -> bool:
        """Cancel a PENDING or SCHEDULED job.

        Returns ``True`` if the job was found in a cancellable state and was
        cancelled; ``False`` otherwise.
        """
        now = self._now()
        with self._lock:
            cur = self._conn.execute(
                """
                UPDATE jobs
                SET status = 'cancelled', updated_at = ?
                WHERE job_id = ?
                  AND status IN ('pending', 'scheduled')
                """,
                (now, job_id),
            )
            self._conn.commit()
            return cur.rowcount > 0

    def get(self, job_id: str) -> Optional[Job]:
        """Return the :class:`Job` with *job_id*, or ``None`` if not found."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
        return self._row_to_job(row) if row is not None else None

    def list(
        self,
        status: Optional[JobStatus] = None,
        name: Optional[str] = None,
    ) -> list[Job]:
        """Return jobs matching optional filters.

        Results are ordered by ``priority ASC``, then ``created_at ASC``.
        """
        sql = "SELECT * FROM jobs WHERE 1=1"
        params: list[Any] = []
        if status is not None:
            sql += " AND status = ?"
            params.append(status.value)
        if name is not None:
            sql += " AND name = ?"
            params.append(name)
        sql += " ORDER BY priority ASC, created_at ASC"
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_job(r) for r in rows]

    def pending_count(self) -> int:
        """Return the number of PENDING jobs."""
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) FROM jobs WHERE status = 'pending'"
            ).fetchone()
        return row[0]

    def clear_done(self) -> int:
        """Delete all DONE jobs.  Returns the number of rows deleted."""
        with self._lock:
            cur = self._conn.execute("DELETE FROM jobs WHERE status = 'done'")
            self._conn.commit()
            return cur.rowcount

    def close(self) -> None:
        """Close the underlying database connection."""
        with self._lock:
            self._conn.close()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_job(row: sqlite3.Row) -> Job:
        result_raw = row["result"]
        result_value: Any = None
        if result_raw is not None:
            try:
                result_value = json.loads(result_raw)
            except (json.JSONDecodeError, TypeError):
                result_value = result_raw

        payload_raw = row["payload"]
        payload: dict = {}
        if payload_raw:
            try:
                payload = json.loads(payload_raw)
            except (json.JSONDecodeError, TypeError):
                payload = {}

        return Job(
            job_id=row["job_id"],
            name=row["name"] or "",
            payload=payload,
            priority=row["priority"],
            status=JobStatus(row["status"]),
            run_at=row["run_at"],
            max_retries=row["max_retries"],
            retry_count=row["retry_count"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            result=result_value,
            error=row["error"] or "",
        )
