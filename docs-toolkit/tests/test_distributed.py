"""Tests for distributed task coordinator and local worker."""
import sys
import threading
import time
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.jobs.distributed import (
    WorkerConfig,
    TaskMessage,
    DistributedCoordinator,
    LocalWorker,
)


# ---- Helpers ----

def _make_coord(tmp_path: Path) -> DistributedCoordinator:
    return DistributedCoordinator(db_path=tmp_path / "dist.sqlite")


def _make_task(handler: str = "noop", args: dict | None = None,
               priority: int = 0,
               requires_tags: list | None = None) -> TaskMessage:
    return TaskMessage(
        task_id=uuid.uuid4().hex[:12],
        handler=handler,
        args=args or {},
        priority=priority,
        requires_tags=requires_tags or [],
    )


def _make_cfg(tags: list | None = None) -> WorkerConfig:
    return WorkerConfig(
        worker_id=uuid.uuid4().hex[:8],
        tags=tags or [],
    )


# ---- DistributedCoordinator: submit / claim / complete ----

def test_submit_returns_task_id(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task("handler_a")
    tid = coord.submit(task)
    assert tid == task.task_id
    coord.close()


def test_claim_task_basic(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task("handler_a")
    coord.submit(task)

    cfg = _make_cfg()
    coord.register_worker(cfg)
    claimed = coord.claim_task(cfg.worker_id, cfg.tags)
    assert claimed is not None
    assert claimed.task_id == task.task_id
    assert claimed.handler == "handler_a"
    coord.close()


def test_claim_task_none_when_empty(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    assert coord.claim_task(cfg.worker_id, cfg.tags) is None
    coord.close()


def test_claim_task_atomically_marks_running(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task()
    coord.submit(task)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    coord.claim_task(cfg.worker_id, cfg.tags)
    # Second claim should get None (task is running)
    assert coord.claim_task(cfg.worker_id, cfg.tags) is None
    coord.close()


def test_complete_task(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task()
    coord.submit(task)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    coord.claim_task(cfg.worker_id, cfg.tags)
    coord.complete_task(task.task_id, {"answer": 42})

    row = coord.conn.execute(
        "SELECT status, result_json FROM dtasks WHERE id = ?",
        (task.task_id,)
    ).fetchone()
    import json
    assert row["status"] == "completed"
    assert json.loads(row["result_json"])["answer"] == 42
    coord.close()


def test_fail_task(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task()
    coord.submit(task)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    coord.claim_task(cfg.worker_id, cfg.tags)
    coord.fail_task(task.task_id, "Something went wrong")

    row = coord.conn.execute(
        "SELECT status, error FROM dtasks WHERE id = ?",
        (task.task_id,)
    ).fetchone()
    assert row["status"] == "failed"
    assert "Something went wrong" in row["error"]
    coord.close()


def test_priority_ordering(tmp_path):
    coord = _make_coord(tmp_path)
    low = _make_task("low_handler", priority=0)
    high = _make_task("high_handler", priority=10)
    coord.submit(low)
    coord.submit(high)

    cfg = _make_cfg()
    coord.register_worker(cfg)
    first = coord.claim_task(cfg.worker_id, cfg.tags)
    assert first.task_id == high.task_id
    coord.close()


def test_tag_filtering_worker_has_required(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task(requires_tags=["gpu"])
    coord.submit(task)

    cfg = _make_cfg(tags=["gpu", "llm"])
    coord.register_worker(cfg)
    claimed = coord.claim_task(cfg.worker_id, cfg.tags)
    assert claimed is not None
    assert claimed.task_id == task.task_id
    coord.close()


def test_tag_filtering_worker_missing_tag(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task(requires_tags=["gpu"])
    coord.submit(task)

    cfg = _make_cfg(tags=["cpu"])
    coord.register_worker(cfg)
    claimed = coord.claim_task(cfg.worker_id, cfg.tags)
    assert claimed is None
    coord.close()


def test_tag_filtering_no_requirement(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task(requires_tags=[])
    coord.submit(task)

    cfg = _make_cfg(tags=[])
    coord.register_worker(cfg)
    claimed = coord.claim_task(cfg.worker_id, cfg.tags)
    assert claimed is not None
    coord.close()


# ---- Worker registration and heartbeat ----

def test_register_worker(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = WorkerConfig(worker_id="w1", host="10.0.0.1", port=8080, tags=["cpu"])
    coord.register_worker(cfg)

    row = coord.conn.execute(
        "SELECT * FROM workers WHERE id = ?", ("w1",)
    ).fetchone()
    import json
    assert row is not None
    assert row["host"] == "10.0.0.1"
    assert row["port"] == 8080
    assert json.loads(row["tags_json"]) == ["cpu"]
    coord.close()


def test_heartbeat_updates_timestamp(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)

    t0 = coord.conn.execute(
        "SELECT last_heartbeat FROM workers WHERE id = ?",
        (cfg.worker_id,)
    ).fetchone()["last_heartbeat"]

    time.sleep(0.05)
    coord.heartbeat(cfg.worker_id)

    t1 = coord.conn.execute(
        "SELECT last_heartbeat FROM workers WHERE id = ?",
        (cfg.worker_id,)
    ).fetchone()["last_heartbeat"]

    assert t1 > t0
    coord.close()


def test_list_workers_alive(tmp_path):
    coord = _make_coord(tmp_path)
    cfg1 = _make_cfg()
    cfg2 = _make_cfg()
    coord.register_worker(cfg1)
    coord.register_worker(cfg2)

    alive = coord.list_workers(alive_since_sec=60)
    alive_ids = {w.worker_id for w in alive}
    assert cfg1.worker_id in alive_ids
    assert cfg2.worker_id in alive_ids
    coord.close()


def test_list_workers_excludes_stale(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    # Manually set heartbeat far in the past
    coord.conn.execute(
        "UPDATE workers SET last_heartbeat = ? WHERE id = ?",
        (time.time() - 9999, cfg.worker_id)
    )
    coord.conn.commit()

    alive = coord.list_workers(alive_since_sec=60)
    alive_ids = {w.worker_id for w in alive}
    assert cfg.worker_id not in alive_ids
    coord.close()


# ---- stats ----

def test_stats_initial(tmp_path):
    coord = _make_coord(tmp_path)
    s = coord.stats()
    assert s["total_tasks"] == 0
    assert s["total_workers"] == 0
    coord.close()


def test_stats_after_submit(tmp_path):
    coord = _make_coord(tmp_path)
    coord.submit(_make_task())
    coord.submit(_make_task())
    s = coord.stats()
    assert s["total_tasks"] == 2
    assert s["tasks"].get("queued", 0) == 2
    coord.close()


def test_stats_after_complete(tmp_path):
    coord = _make_coord(tmp_path)
    task = _make_task()
    coord.submit(task)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    coord.claim_task(cfg.worker_id, cfg.tags)
    coord.complete_task(task.task_id, {})
    s = coord.stats()
    assert s["tasks"].get("completed", 0) == 1
    coord.close()


# ---- LocalWorker.run_once ----

def test_local_worker_run_once_no_tasks(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)
    worker = LocalWorker(cfg, coord, registry={})
    did_work = worker.run_once()
    assert did_work is False
    coord.close()


def test_local_worker_run_once_executes_handler(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)

    results_store = []

    def my_handler(args):
        results_store.append(args.get("value"))
        return {"done": True}

    task = _make_task("my_handler", args={"value": 42})
    coord.submit(task)

    worker = LocalWorker(cfg, coord, registry={"my_handler": my_handler})
    did_work = worker.run_once()
    assert did_work is True
    assert results_store == [42]

    # Task should be completed
    row = coord.conn.execute(
        "SELECT status FROM dtasks WHERE id = ?", (task.task_id,)
    ).fetchone()
    assert row["status"] == "completed"
    coord.close()


def test_local_worker_run_once_fails_on_exception(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)

    def bad_handler(args):
        raise ValueError("intentional error")

    task = _make_task("bad_handler")
    coord.submit(task)

    worker = LocalWorker(cfg, coord, registry={"bad_handler": bad_handler})
    did_work = worker.run_once()
    assert did_work is True

    row = coord.conn.execute(
        "SELECT status, error FROM dtasks WHERE id = ?", (task.task_id,)
    ).fetchone()
    assert row["status"] == "failed"
    assert "intentional error" in row["error"]
    coord.close()


def test_local_worker_run_once_unknown_handler(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)

    task = _make_task("nonexistent_handler")
    coord.submit(task)

    worker = LocalWorker(cfg, coord, registry={})
    did_work = worker.run_once()
    assert did_work is True

    row = coord.conn.execute(
        "SELECT status, error FROM dtasks WHERE id = ?", (task.task_id,)
    ).fetchone()
    assert row["status"] == "failed"
    assert "nonexistent_handler" in row["error"]
    coord.close()


def test_local_worker_run_loop_processes_multiple(tmp_path):
    coord = _make_coord(tmp_path)
    cfg = _make_cfg()
    coord.register_worker(cfg)

    executed = []

    def handler(args):
        executed.append(args.get("n"))
        return {}

    for i in range(3):
        coord.submit(_make_task("h", args={"n": i}))

    stop = threading.Event()
    worker = LocalWorker(cfg, coord, registry={"h": handler})

    def _run():
        worker.run_loop(poll_interval=0.05, stop_event=stop)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    time.sleep(0.5)
    stop.set()
    t.join(timeout=2.0)

    assert len(executed) == 3
    assert set(executed) == {0, 1, 2}
    coord.close()
