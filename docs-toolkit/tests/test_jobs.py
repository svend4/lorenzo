"""Тесты jobs queue."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.jobs.queue import JobQueue
from docstoolkit.jobs.handlers import register_handler, HANDLERS


def test_queue_submit_get(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    job_id = q.submit("test_handler", {"key": "value"})
    job = q.get(job_id)
    assert job is not None
    assert job.handler == "test_handler"
    assert job.args == {"key": "value"}
    assert job.status == "queued"
    q.close()


def test_queue_list_filters(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    q.submit("handler_a")
    q.submit("handler_b")
    q.submit("handler_a", priority=5)

    all_jobs = q.list()
    assert len(all_jobs) == 3

    only_a = q.list(handler="handler_a")
    assert len(only_a) == 2

    only_queued = q.list(status="queued")
    assert len(only_queued) == 3
    q.close()


def test_queue_claim_next_atomic(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    q.submit("handler_low", priority=0)
    high_id = q.submit("handler_high", priority=10)

    job1 = q.claim_next()
    assert job1.id == high_id  # priority 10 раньше
    assert job1.status == "running"

    # Второй claim берёт low
    job2 = q.claim_next()
    assert job2.id != high_id

    # Третий — None (всё в running)
    assert q.claim_next() is None
    q.close()


def test_queue_complete(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    job_id = q.submit("h")
    q.claim_next()
    q.complete(job_id, {"result_key": "val"})

    job = q.get(job_id)
    assert job.status == "completed"
    assert job.result == {"result_key": "val"}
    assert job.progress == 100
    q.close()


def test_queue_fail(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    job_id = q.submit("h")
    q.claim_next()
    q.fail(job_id, "Something broke")

    job = q.get(job_id)
    assert job.status == "failed"
    assert "Something broke" in job.error
    q.close()


def test_queue_progress(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    job_id = q.submit("h")
    q.claim_next()
    q.update_progress(job_id, 50, "halfway")

    job = q.get(job_id)
    assert job.progress == 50
    assert job.progress_message == "halfway"
    q.close()


def test_queue_cancel(tmp_path):
    q = JobQueue(tmp_path / "test.sqlite")
    job_id = q.submit("h")
    assert q.cancel(job_id) is True
    assert q.get(job_id).status == "cancelled"

    # Нельзя отменить уже cancelled
    assert q.cancel(job_id) is False
    q.close()


def test_handler_registration():
    def my_handler(args, progress_cb=None):
        return {"ok": True}
    register_handler("my_test_handler", my_handler)
    assert "my_test_handler" in HANDLERS
    assert HANDLERS["my_test_handler"] is my_handler
