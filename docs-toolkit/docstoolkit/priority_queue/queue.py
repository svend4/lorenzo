import json
import sqlite3
from pathlib import Path
from docstoolkit.priority_queue.item import PriorityJob, JobStatus, Priority

_SCHEMA = """
CREATE TABLE IF NOT EXISTS priority_jobs (
    job_id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 5,
    status TEXT NOT NULL DEFAULT 'pending',
    owner TEXT NOT NULL DEFAULT '',
    created_ts TEXT NOT NULL,
    started_ts TEXT NOT NULL DEFAULT '',
    done_ts TEXT NOT NULL DEFAULT '',
    attempt_count INTEGER NOT NULL DEFAULT 0,
    error TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_status_priority
    ON priority_jobs(status, priority DESC, created_ts ASC);
"""

class PriorityJobQueue:
    """SQLite-backed priority job queue."""

    def __init__(self, db_path=None):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def enqueue(self, job: PriorityJob) -> None:
        """Insert job (INSERT OR IGNORE — don't overwrite existing)."""
        self._conn.execute(
            "INSERT OR IGNORE INTO priority_jobs "
            "(job_id, payload, priority, status, owner, created_ts, "
            " started_ts, done_ts, attempt_count, error) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (job.job_id, job.payload, job.priority.value, job.status.value,
             job.owner, job.created_ts, job.started_ts, job.done_ts,
             job.attempt_count, job.error),
        )
        self._conn.commit()

    def dequeue(self, owner: str = "") -> PriorityJob | None:
        """Pop highest-priority pending job (optionally filtered by owner).
        Returns None if queue empty.
        Marks job as RUNNING and increments attempt_count.
        """
        from datetime import datetime
        where = "status = 'pending'"
        params = []
        if owner:
            where += " AND owner = ?"
            params.append(owner)
        row = self._conn.execute(
            f"SELECT * FROM priority_jobs WHERE {where} "
            "ORDER BY priority DESC, created_ts ASC LIMIT 1",
            params,
        ).fetchone()
        if not row:
            return None
        ts = datetime.now().isoformat(timespec='seconds')
        self._conn.execute(
            "UPDATE priority_jobs SET status='running', started_ts=?, "
            "attempt_count=attempt_count+1 WHERE job_id=?",
            (ts, row["job_id"]),
        )
        self._conn.commit()
        job = self._row_to_job(row)
        job.status = JobStatus.RUNNING
        job.started_ts = ts
        job.attempt_count += 1
        return job

    def complete(self, job_id: str, error: str = "") -> bool:
        """Mark job DONE (or FAILED if error given)."""
        from datetime import datetime
        ts = datetime.now().isoformat(timespec='seconds')
        status = JobStatus.FAILED.value if error else JobStatus.DONE.value
        cur = self._conn.execute(
            "UPDATE priority_jobs SET status=?, done_ts=?, error=? WHERE job_id=?",
            (status, ts, error, job_id),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def cancel(self, job_id: str) -> bool:
        cur = self._conn.execute(
            "UPDATE priority_jobs SET status='cancelled' WHERE job_id=? AND status='pending'",
            (job_id,),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def get(self, job_id: str) -> PriorityJob | None:
        row = self._conn.execute(
            "SELECT * FROM priority_jobs WHERE job_id=?", (job_id,)
        ).fetchone()
        return self._row_to_job(row) if row else None

    def pending_count(self, owner: str = "") -> int:
        if owner:
            return self._conn.execute(
                "SELECT COUNT(*) FROM priority_jobs WHERE status='pending' AND owner=?",
                (owner,)
            ).fetchone()[0]
        return self._conn.execute(
            "SELECT COUNT(*) FROM priority_jobs WHERE status='pending'"
        ).fetchone()[0]

    def stats(self) -> dict:
        rows = self._conn.execute(
            "SELECT status, COUNT(*) as cnt FROM priority_jobs GROUP BY status"
        ).fetchall()
        result = {s.value: 0 for s in JobStatus}
        for r in rows:
            result[r["status"]] = r["cnt"]
        return result

    def close(self):
        self._conn.close()

    def _row_to_job(self, row) -> PriorityJob:
        return PriorityJob(
            job_id=row["job_id"],
            payload=row["payload"],
            priority=Priority(row["priority"]),
            status=JobStatus(row["status"]),
            owner=row["owner"],
            created_ts=row["created_ts"],
            started_ts=row["started_ts"],
            done_ts=row["done_ts"],
            attempt_count=row["attempt_count"],
            error=row["error"],
        )
