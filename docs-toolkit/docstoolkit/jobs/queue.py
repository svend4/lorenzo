"""SQLite-based job queue."""
import json
import sqlite3
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    handler TEXT NOT NULL,
    args_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    submitted_ts INTEGER NOT NULL,
    started_ts INTEGER,
    finished_ts INTEGER,
    duration_ms INTEGER,
    result_json TEXT,
    error TEXT,
    progress INTEGER DEFAULT 0,
    progress_message TEXT,
    priority INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status, priority DESC, submitted_ts);
CREATE INDEX IF NOT EXISTS idx_jobs_handler ON jobs(handler);
"""

VALID_STATUSES = {"queued", "running", "completed", "failed", "cancelled"}


@dataclass
class Job:
    id: str
    handler: str
    args: dict
    status: str = "queued"
    submitted_ts: int = 0
    started_ts: int | None = None
    finished_ts: int | None = None
    duration_ms: int = 0
    result: dict = field(default_factory=dict)
    error: str = ""
    progress: int = 0
    progress_message: str = ""
    priority: int = 0


class JobQueue:
    def __init__(self, db_path: str | Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "jobs.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ----- Submit -----

    def submit(self, handler: str, args: dict | None = None,
               priority: int = 0) -> str:
        job_id = uuid.uuid4().hex[:12]
        self.conn.execute(
            "INSERT INTO jobs (id, handler, args_json, submitted_ts, priority) "
            "VALUES (?, ?, ?, ?, ?)",
            (job_id, handler, json.dumps(args or {}, ensure_ascii=False),
             int(time.time()), priority)
        )
        self.conn.commit()
        return job_id

    # ----- Get -----

    def get(self, job_id: str) -> Job | None:
        row = self.conn.execute(
            "SELECT * FROM jobs WHERE id = ?", (job_id,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_job(row)

    def list(self, status: str = "", handler: str = "",
             limit: int = 50) -> list[Job]:
        sql = "SELECT * FROM jobs WHERE 1=1"
        params: list = []
        if status:
            sql += " AND status = ?"
            params.append(status)
        if handler:
            sql += " AND handler = ?"
            params.append(handler)
        sql += " ORDER BY submitted_ts DESC LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(sql, params).fetchall()
        return [self._row_to_job(r) for r in rows]

    # ----- Worker operations -----

    def claim_next(self) -> Job | None:
        """Атомарно: queued → running, возвращает job."""
        cur = self.conn.cursor()
        # SQLite не поддерживает FOR UPDATE; используем транзакцию
        cur.execute("BEGIN IMMEDIATE")
        try:
            row = cur.execute(
                "SELECT * FROM jobs WHERE status = 'queued' "
                "ORDER BY priority DESC, submitted_ts LIMIT 1"
            ).fetchone()
            if not row:
                cur.execute("ROLLBACK")
                return None
            cur.execute(
                "UPDATE jobs SET status = 'running', started_ts = ? WHERE id = ?",
                (int(time.time()), row["id"])
            )
            cur.execute("COMMIT")
            return self._row_to_job(self.conn.execute(
                "SELECT * FROM jobs WHERE id = ?", (row["id"],)).fetchone())
        except Exception:
            cur.execute("ROLLBACK")
            raise

    def update_progress(self, job_id: str, progress: int,
                        message: str = ""):
        self.conn.execute(
            "UPDATE jobs SET progress = ?, progress_message = ? WHERE id = ?",
            (max(0, min(100, progress)), message, job_id)
        )
        self.conn.commit()

    def complete(self, job_id: str, result: dict | None = None):
        finished = int(time.time())
        row = self.conn.execute(
            "SELECT started_ts FROM jobs WHERE id = ?", (job_id,)
        ).fetchone()
        started = row["started_ts"] if row else finished
        duration_ms = (finished - started) * 1000 if started else 0
        self.conn.execute(
            "UPDATE jobs SET status = 'completed', finished_ts = ?, "
            "duration_ms = ?, result_json = ?, progress = 100 WHERE id = ?",
            (finished, duration_ms,
             json.dumps(result or {}, ensure_ascii=False), job_id)
        )
        self.conn.commit()

    def fail(self, job_id: str, error: str):
        finished = int(time.time())
        row = self.conn.execute(
            "SELECT started_ts FROM jobs WHERE id = ?", (job_id,)
        ).fetchone()
        started = row["started_ts"] if row else finished
        duration_ms = (finished - started) * 1000 if started else 0
        self.conn.execute(
            "UPDATE jobs SET status = 'failed', finished_ts = ?, "
            "duration_ms = ?, error = ? WHERE id = ?",
            (finished, duration_ms, error[:2000], job_id)
        )
        self.conn.commit()

    def cancel(self, job_id: str) -> bool:
        cur = self.conn.execute(
            "UPDATE jobs SET status = 'cancelled', finished_ts = ? "
            "WHERE id = ? AND status IN ('queued', 'running')",
            (int(time.time()), job_id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    # ----- Helpers -----

    def _row_to_job(self, row) -> Job:
        return Job(
            id=row["id"],
            handler=row["handler"],
            args=json.loads(row["args_json"]) if row["args_json"] else {},
            status=row["status"],
            submitted_ts=row["submitted_ts"],
            started_ts=row["started_ts"],
            finished_ts=row["finished_ts"],
            duration_ms=row["duration_ms"] or 0,
            result=json.loads(row["result_json"]) if row["result_json"] else {},
            error=row["error"] or "",
            progress=row["progress"] or 0,
            progress_message=row["progress_message"] or "",
            priority=row["priority"] or 0,
        )


# ----- Module-level convenience API -----

_default_queue: JobQueue | None = None


def _get_queue() -> JobQueue:
    global _default_queue
    if _default_queue is None:
        _default_queue = JobQueue()
    return _default_queue


def submit(handler: str, args: dict | None = None, priority: int = 0) -> str:
    return _get_queue().submit(handler, args, priority)


def get_status(job_id: str) -> Job | None:
    return _get_queue().get(job_id)


def list_jobs(status: str = "", handler: str = "", limit: int = 50) -> list[Job]:
    return _get_queue().list(status, handler, limit)


def cancel(job_id: str) -> bool:
    return _get_queue().cancel(job_id)
