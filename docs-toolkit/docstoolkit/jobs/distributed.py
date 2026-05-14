"""Distributed task processing: coordinator + local worker (SQLite-backed)."""
import json
import sqlite3
import time
import traceback
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS workers (
    id TEXT PRIMARY KEY,
    host TEXT NOT NULL DEFAULT 'localhost',
    port INTEGER NOT NULL DEFAULT 0,
    last_heartbeat REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'idle',
    tags_json TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS dtasks (
    id TEXT PRIMARY KEY,
    handler TEXT NOT NULL,
    args_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'queued',
    worker_id TEXT NOT NULL DEFAULT '',
    priority INTEGER NOT NULL DEFAULT 0,
    tags_json TEXT NOT NULL DEFAULT '[]',
    submitted_ts REAL NOT NULL DEFAULT 0,
    started_ts REAL NOT NULL DEFAULT 0,
    finished_ts REAL NOT NULL DEFAULT 0,
    result_json TEXT NOT NULL DEFAULT '{}',
    error TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_dtasks_status ON dtasks(status, priority DESC, submitted_ts);
CREATE INDEX IF NOT EXISTS idx_dtasks_worker ON dtasks(worker_id);
CREATE INDEX IF NOT EXISTS idx_workers_heartbeat ON workers(last_heartbeat);
"""


@dataclass
class WorkerConfig:
    """Configuration for a single worker process."""
    worker_id: str
    host: str = "localhost"
    port: int = 0
    max_concurrent: int = 4
    tags: list[str] = field(default_factory=list)


@dataclass
class TaskMessage:
    """A task submitted for distributed execution."""
    task_id: str
    handler: str
    args: dict = field(default_factory=dict)
    priority: int = 0
    requires_tags: list[str] = field(default_factory=list)


class DistributedCoordinator:
    """SQLite-backed distributed task coordinator.

    Uses SQLite's BEGIN IMMEDIATE transactions for atomic claim, which
    provides safe multi-process access via file locking.
    """

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "distributed.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), timeout=30,
                                    check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ----- Worker registration -----

    def register_worker(self, cfg: WorkerConfig) -> None:
        """Upsert worker record."""
        self.conn.execute(
            "INSERT OR REPLACE INTO workers "
            "(id, host, port, last_heartbeat, status, tags_json) "
            "VALUES (?, ?, ?, ?, 'idle', ?)",
            (cfg.worker_id, cfg.host, cfg.port,
             time.time(), json.dumps(cfg.tags)),
        )
        self.conn.commit()

    def heartbeat(self, worker_id: str) -> None:
        """Update worker's last_heartbeat timestamp."""
        self.conn.execute(
            "UPDATE workers SET last_heartbeat = ? WHERE id = ?",
            (time.time(), worker_id),
        )
        self.conn.commit()

    def list_workers(self, alive_since_sec: float = 60) -> list[WorkerConfig]:
        """Return workers that sent a heartbeat within alive_since_sec seconds."""
        cutoff = time.time() - alive_since_sec
        rows = self.conn.execute(
            "SELECT * FROM workers WHERE last_heartbeat >= ?", (cutoff,)
        ).fetchall()
        return [self._row_to_worker(r) for r in rows]

    # ----- Task submission -----

    def submit(self, msg: TaskMessage) -> str:
        """Insert task into queue; return task_id."""
        self.conn.execute(
            "INSERT INTO dtasks "
            "(id, handler, args_json, status, priority, tags_json, submitted_ts) "
            "VALUES (?, ?, ?, 'queued', ?, ?, ?)",
            (
                msg.task_id,
                msg.handler,
                json.dumps(msg.args, ensure_ascii=False),
                msg.priority,
                json.dumps(msg.requires_tags),
                time.time(),
            ),
        )
        self.conn.commit()
        return msg.task_id

    def claim_task(self, worker_id: str,
                   tags: list[str]) -> TaskMessage | None:
        """Atomically claim the next eligible queued task.

        A task is eligible if the worker has ALL tags required by the task
        (requires_tags). Returns None if no eligible task is available.
        """
        cur = self.conn.cursor()
        cur.execute("BEGIN IMMEDIATE")
        try:
            rows = cur.execute(
                "SELECT * FROM dtasks WHERE status = 'queued' "
                "ORDER BY priority DESC, submitted_ts LIMIT 100"
            ).fetchall()

            chosen = None
            worker_tag_set = set(tags)
            for row in rows:
                required = set(json.loads(row["tags_json"] or "[]"))
                if required.issubset(worker_tag_set):
                    chosen = row
                    break

            if not chosen:
                cur.execute("ROLLBACK")
                return None

            cur.execute(
                "UPDATE dtasks SET status = 'running', worker_id = ?, "
                "started_ts = ? WHERE id = ?",
                (worker_id, time.time(), chosen["id"]),
            )
            cur.execute("COMMIT")
        except Exception:
            cur.execute("ROLLBACK")
            raise

        # Re-fetch the updated row outside the transaction
        row = self.conn.execute(
            "SELECT * FROM dtasks WHERE id = ?", (chosen["id"],)
        ).fetchone()
        return self._row_to_task(row)

    def complete_task(self, task_id: str, result: dict) -> None:
        """Mark task as completed with result payload."""
        self.conn.execute(
            "UPDATE dtasks SET status = 'completed', finished_ts = ?, "
            "result_json = ? WHERE id = ?",
            (time.time(), json.dumps(result, ensure_ascii=False), task_id),
        )
        self.conn.commit()

    def fail_task(self, task_id: str, error: str) -> None:
        """Mark task as failed with error message."""
        self.conn.execute(
            "UPDATE dtasks SET status = 'failed', finished_ts = ?, "
            "error = ? WHERE id = ?",
            (time.time(), error[:4000], task_id),
        )
        self.conn.commit()

    def stats(self) -> dict:
        """Return summary counts of tasks by status."""
        rows = self.conn.execute(
            "SELECT status, COUNT(*) as cnt FROM dtasks GROUP BY status"
        ).fetchall()
        by_status = {r["status"]: r["cnt"] for r in rows}
        total_workers = self.conn.execute(
            "SELECT COUNT(*) FROM workers"
        ).fetchone()[0]
        alive_workers = len(self.list_workers())
        return {
            "tasks": by_status,
            "total_tasks": sum(by_status.values()),
            "total_workers": total_workers,
            "alive_workers": alive_workers,
        }

    # ----- Helpers -----

    def _row_to_worker(self, row) -> WorkerConfig:
        return WorkerConfig(
            worker_id=row["id"],
            host=row["host"],
            port=row["port"],
            tags=json.loads(row["tags_json"] or "[]"),
        )

    def _row_to_task(self, row) -> TaskMessage:
        return TaskMessage(
            task_id=row["id"],
            handler=row["handler"],
            args=json.loads(row["args_json"] or "{}"),
            priority=row["priority"],
            requires_tags=json.loads(row["tags_json"] or "[]"),
        )


class LocalWorker:
    """Single-process worker that claims and executes tasks from the coordinator."""

    def __init__(self, cfg: WorkerConfig,
                 coordinator: DistributedCoordinator,
                 registry: dict[str, Callable]):
        self.cfg = cfg
        self.coord = coordinator
        self.registry = registry

    def run_once(self) -> bool:
        """Claim one task, execute it, complete or fail.

        Returns True if a task was processed, False if no task was available.
        """
        task = self.coord.claim_task(self.cfg.worker_id, self.cfg.tags)
        if task is None:
            return False

        handler = self.registry.get(task.handler)
        if handler is None:
            self.coord.fail_task(task.task_id,
                                 f"Handler '{task.handler}' not registered")
            return True

        try:
            result = handler(task.args)
            self.coord.complete_task(task.task_id,
                                     result if isinstance(result, dict) else {})
        except Exception as exc:
            tb = traceback.format_exc()
            self.coord.fail_task(task.task_id, f"{exc}\n{tb}")

        return True

    def run_loop(self, poll_interval: float = 1.0,
                 stop_event=None) -> None:
        """Poll for tasks until stop_event is set (or KeyboardInterrupt).

        stop_event: threading.Event or any object with .is_set() method.
        """
        self.coord.register_worker(self.cfg)
        try:
            while True:
                if stop_event is not None and stop_event.is_set():
                    break
                did_work = self.run_once()
                self.coord.heartbeat(self.cfg.worker_id)
                if not did_work:
                    time.sleep(poll_interval)
        except KeyboardInterrupt:
            pass
