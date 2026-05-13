"""Index job queue backed by SQLite for incremental indexing (E32)."""
from __future__ import annotations

import sqlite3
import time
import uuid
from dataclasses import dataclass, field

from docstoolkit.incremental_index.change import ChangeType, DocumentChange


def _short_uuid() -> str:
    """Return a short 8-character UUID4 string."""
    return uuid.uuid4().hex[:8]


@dataclass
class IndexJob:
    job_id: str
    doc_id: str
    change_type: ChangeType
    priority: int = 5
    created_ts: float = field(default_factory=time.time)
    status: str = "pending"  # pending / running / done / failed


class IndexQueue:
    """Priority queue for index jobs, backed by SQLite."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS index_jobs (
                job_id      TEXT PRIMARY KEY,
                doc_id      TEXT NOT NULL,
                change_type TEXT NOT NULL,
                priority    INTEGER NOT NULL DEFAULT 5,
                created_ts  REAL NOT NULL,
                status      TEXT NOT NULL DEFAULT 'pending',
                error       TEXT NOT NULL DEFAULT ''
            )
            """
        )
        self._conn.commit()

    def enqueue(self, change: DocumentChange, priority: int = 5) -> IndexJob:
        """Create and persist an IndexJob for a DocumentChange."""
        job = IndexJob(
            job_id=_short_uuid(),
            doc_id=change.doc_id,
            change_type=change.change_type,
            priority=priority,
            created_ts=time.time(),
            status="pending",
        )
        self._conn.execute(
            """
            INSERT INTO index_jobs (job_id, doc_id, change_type, priority, created_ts, status, error)
            VALUES (?, ?, ?, ?, ?, ?, '')
            """,
            (job.job_id, job.doc_id, job.change_type.value, job.priority, job.created_ts, job.status),
        )
        self._conn.commit()
        return job

    def dequeue(self, n: int = 1) -> list[IndexJob]:
        """Return up to n jobs: highest priority first, FIFO within same priority.

        Returned jobs are moved to 'running' status.
        """
        rows = self._conn.execute(
            """
            SELECT job_id, doc_id, change_type, priority, created_ts, status
            FROM index_jobs
            WHERE status = 'pending'
            ORDER BY priority DESC, created_ts ASC
            LIMIT ?
            """,
            (n,),
        ).fetchall()

        jobs: list[IndexJob] = []
        for row in rows:
            self._conn.execute(
                "UPDATE index_jobs SET status = 'running' WHERE job_id = ?",
                (row["job_id"],),
            )
            jobs.append(
                IndexJob(
                    job_id=row["job_id"],
                    doc_id=row["doc_id"],
                    change_type=ChangeType(row["change_type"]),
                    priority=row["priority"],
                    created_ts=row["created_ts"],
                    status="running",
                )
            )
        self._conn.commit()
        return jobs

    def complete(self, job_id: str) -> None:
        """Mark a job as done."""
        self._conn.execute(
            "UPDATE index_jobs SET status = 'done' WHERE job_id = ?",
            (job_id,),
        )
        self._conn.commit()

    def fail(self, job_id: str, error: str = "") -> None:
        """Mark a job as failed with an optional error message."""
        self._conn.execute(
            "UPDATE index_jobs SET status = 'failed', error = ? WHERE job_id = ?",
            (error, job_id),
        )
        self._conn.commit()

    def pending_count(self) -> int:
        """Return the number of pending jobs."""
        row = self._conn.execute(
            "SELECT COUNT(*) FROM index_jobs WHERE status = 'pending'"
        ).fetchone()
        return row[0]

    def stats(self) -> dict:
        """Return counts for each status: pending, running, done, failed."""
        rows = self._conn.execute(
            "SELECT status, COUNT(*) AS cnt FROM index_jobs GROUP BY status"
        ).fetchall()
        result = {"pending": 0, "running": 0, "done": 0, "failed": 0}
        for row in rows:
            status = row["status"]
            if status in result:
                result[status] = row["cnt"]
        return result
