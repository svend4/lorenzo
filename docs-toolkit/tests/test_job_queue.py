"""Tests for docstoolkit.job_queue (E110).

SQLite-backed persistent job queue with priorities, retries, and
scheduled execution times.  ~90 tests covering all public methods,
edge cases, persistence, thread-safety, and virtual-time scenarios.
"""
from __future__ import annotations

import os
import tempfile
import threading
import time
from typing import Any

import pytest

from docstoolkit.job_queue import Job, JobQueue, JobStatus


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_queue(**kwargs) -> JobQueue:
    """Return a fresh in-memory JobQueue, passing any extra kwargs through."""
    return JobQueue(db_path=":memory:", **kwargs)


def _fixed_now(ts: float):
    """Return a now_fn closure that always returns *ts*."""
    return lambda: ts


def _advancing_clock(start: float = 1_000_000.0, step: float = 0.0):
    """Return a mutable clock whose value can be advanced manually."""
    state = [start]

    def now():
        return state[0]

    def advance(by: float):
        state[0] += by

    now.advance = advance      # type: ignore[attr-defined]
    now.state = state          # type: ignore[attr-defined]
    return now


# ===========================================================================
# JobStatus enum
# ===========================================================================
class TestJobStatus:
    def test_pending_value(self):
        assert JobStatus.PENDING.value == "pending"

    def test_running_value(self):
        assert JobStatus.RUNNING.value == "running"

    def test_done_value(self):
        assert JobStatus.DONE.value == "done"

    def test_failed_value(self):
        assert JobStatus.FAILED.value == "failed"

    def test_cancelled_value(self):
        assert JobStatus.CANCELLED.value == "cancelled"

    def test_scheduled_value(self):
        assert JobStatus.SCHEDULED.value == "scheduled"

    def test_is_str_subclass(self):
        assert isinstance(JobStatus.PENDING, str)

    def test_all_members(self):
        names = {m.name for m in JobStatus}
        assert names == {"PENDING", "RUNNING", "DONE", "FAILED", "CANCELLED", "SCHEDULED"}

    def test_member_count(self):
        assert len(list(JobStatus)) == 6


# ===========================================================================
# Job dataclass defaults
# ===========================================================================
class TestJobDefaults:
    def test_job_id_length(self):
        assert len(Job().job_id) == 12

    def test_job_id_unique(self):
        ids = {Job().job_id for _ in range(50)}
        assert len(ids) == 50

    def test_default_name_empty(self):
        assert Job().name == ""

    def test_default_payload_empty_dict(self):
        job = Job()
        assert job.payload == {}
        assert isinstance(job.payload, dict)

    def test_payload_independent_between_instances(self):
        a, b = Job(), Job()
        a.payload["x"] = 1
        assert "x" not in b.payload

    def test_default_priority_zero(self):
        assert Job().priority == 0

    def test_default_status_pending(self):
        assert Job().status == JobStatus.PENDING

    def test_default_run_at_zero(self):
        assert Job().run_at == 0.0

    def test_default_max_retries_zero(self):
        assert Job().max_retries == 0

    def test_default_retry_count_zero(self):
        assert Job().retry_count == 0

    def test_default_result_none(self):
        assert Job().result is None

    def test_default_error_empty(self):
        assert Job().error == ""

    def test_created_at_recent(self):
        before = time.time()
        job = Job()
        after = time.time()
        assert before <= job.created_at <= after

    def test_updated_at_recent(self):
        before = time.time()
        job = Job()
        after = time.time()
        assert before <= job.updated_at <= after


# ===========================================================================
# enqueue
# ===========================================================================
class TestEnqueue:
    def test_enqueue_returns_job(self):
        q = make_queue()
        job = q.enqueue("send_email")
        assert isinstance(job, Job)
        q.close()

    def test_enqueue_creates_pending_status(self):
        q = make_queue()
        job = q.enqueue("task")
        assert job.status == JobStatus.PENDING
        q.close()

    def test_enqueue_stores_name(self):
        q = make_queue()
        job = q.enqueue("my_task")
        assert job.name == "my_task"
        q.close()

    def test_enqueue_stores_payload(self):
        q = make_queue()
        job = q.enqueue("t", payload={"key": "value", "num": 42})
        assert job.payload == {"key": "value", "num": 42}
        q.close()

    def test_enqueue_stores_priority(self):
        q = make_queue()
        job = q.enqueue("t", priority=7)
        assert job.priority == 7
        q.close()

    def test_enqueue_stores_max_retries(self):
        q = make_queue()
        job = q.enqueue("t", max_retries=3)
        assert job.max_retries == 3
        q.close()

    def test_enqueue_stores_run_at(self):
        q = make_queue()
        future = time.time() + 3600.0
        job = q.enqueue("t", run_at=future)
        assert job.run_at == pytest.approx(future, abs=0.001)
        q.close()

    def test_enqueue_no_payload_defaults_to_empty(self):
        q = make_queue()
        job = q.enqueue("t")
        assert job.payload == {}
        q.close()

    def test_enqueue_job_id_is_12_hex_chars(self):
        q = make_queue()
        job = q.enqueue("t")
        assert len(job.job_id) == 12
        assert all(c in "0123456789abcdef" for c in job.job_id)
        q.close()

    def test_enqueue_multiple_unique_ids(self):
        q = make_queue()
        ids = [q.enqueue("t").job_id for _ in range(20)]
        assert len(set(ids)) == 20
        q.close()

    def test_enqueue_pending_count_increases(self):
        q = make_queue()
        q.enqueue("a")
        q.enqueue("b")
        assert q.pending_count() == 2
        q.close()

    def test_enqueue_persists_to_db(self):
        q = make_queue()
        job = q.enqueue("persist_me")
        fetched = q.get(job.job_id)
        assert fetched is not None
        assert fetched.name == "persist_me"
        q.close()


# ===========================================================================
# dequeue
# ===========================================================================
class TestDequeue:
    def test_dequeue_empty_returns_none(self):
        q = make_queue()
        assert q.dequeue() is None
        q.close()

    def test_dequeue_returns_job(self):
        q = make_queue()
        q.enqueue("task")
        job = q.dequeue()
        assert isinstance(job, Job)
        q.close()

    def test_dequeue_marks_running(self):
        q = make_queue()
        q.enqueue("task")
        job = q.dequeue()
        assert job.status == JobStatus.RUNNING
        q.close()

    def test_dequeue_atomically_updates_db(self):
        """The DB reflects RUNNING status after dequeue."""
        q = make_queue()
        enqueued = q.enqueue("task")
        q.dequeue()
        stored = q.get(enqueued.job_id)
        assert stored.status == JobStatus.RUNNING
        q.close()

    def test_dequeue_same_job_not_returned_twice(self):
        q = make_queue()
        q.enqueue("task")
        j1 = q.dequeue()
        j2 = q.dequeue()
        assert j1 is not None
        assert j2 is None
        q.close()

    def test_dequeue_respects_priority_order(self):
        """Lowest priority value is returned first."""
        q = make_queue()
        q.enqueue("low",  priority=10)
        q.enqueue("high", priority=1)
        q.enqueue("mid",  priority=5)
        first = q.dequeue()
        assert first.name == "high"
        q.close()

    def test_dequeue_full_priority_order(self):
        q = make_queue()
        for p, n in [(9, "nine"), (3, "three"), (1, "one"), (7, "seven")]:
            q.enqueue(n, priority=p)
        names = [q.dequeue().name for _ in range(4)]
        assert names == ["one", "three", "seven", "nine"]
        q.close()

    def test_dequeue_run_at_future_not_returned(self):
        """Job whose run_at is in the future must not be dequeued yet."""
        clock = _advancing_clock(start=1_000_000.0)
        q = make_queue(now_fn=clock)
        q.enqueue("future", run_at=1_000_100.0)   # 100 s in the future
        assert q.dequeue() is None
        q.close()

    def test_dequeue_run_at_past_is_returned(self):
        clock = _advancing_clock(start=1_000_200.0)
        q = make_queue(now_fn=clock)
        q.enqueue("past", run_at=1_000_100.0)     # 100 s in the past
        job = q.dequeue()
        assert job is not None
        assert job.name == "past"
        q.close()

    def test_dequeue_run_at_exact_now_is_returned(self):
        clock = _advancing_clock(start=1_000_000.0)
        q = make_queue(now_fn=clock)
        q.enqueue("exact", run_at=1_000_000.0)
        job = q.dequeue()
        assert job is not None
        q.close()

    def test_dequeue_run_at_zero_always_ready(self):
        q = make_queue()
        q.enqueue("immediate", run_at=0.0)
        job = q.dequeue()
        assert job is not None
        q.close()

    def test_dequeue_among_future_and_ready(self):
        """Only ready jobs are returned; future ones are skipped."""
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        q.enqueue("future", run_at=2_000.0)
        q.enqueue("ready",  run_at=500.0)
        job = q.dequeue()
        assert job.name == "ready"
        assert q.dequeue() is None
        q.close()

    def test_dequeue_decrements_pending_count(self):
        q = make_queue()
        q.enqueue("a")
        q.enqueue("b")
        q.dequeue()
        assert q.pending_count() == 1
        q.close()


# ===========================================================================
# complete
# ===========================================================================
class TestComplete:
    def test_complete_sets_done(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id)
        assert q.get(job.job_id).status == JobStatus.DONE
        q.close()

    def test_complete_stores_result_dict(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id, result={"answer": 42})
        assert q.get(job.job_id).result == {"answer": 42}
        q.close()

    def test_complete_stores_result_string(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id, result="ok")
        assert q.get(job.job_id).result == "ok"
        q.close()

    def test_complete_stores_result_none(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id)
        assert q.get(job.job_id).result is None
        q.close()

    def test_complete_stores_result_list(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id, result=[1, 2, 3])
        assert q.get(job.job_id).result == [1, 2, 3]
        q.close()

    def test_complete_updates_updated_at(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t")
        q.dequeue()
        clock.advance(10.0)
        q.complete(job.job_id)
        stored = q.get(job.job_id)
        assert stored.updated_at == pytest.approx(1_010.0, abs=0.001)
        q.close()


# ===========================================================================
# fail / retries
# ===========================================================================
class TestFail:
    def test_fail_no_retries_sets_failed(self):
        """max_retries=0 → straight to FAILED on first fail."""
        q = make_queue()
        job = q.enqueue("t", max_retries=0)
        q.dequeue()
        q.fail(job.job_id, error="boom")
        assert q.get(job.job_id).status == JobStatus.FAILED
        q.close()

    def test_fail_stores_error_message(self):
        q = make_queue()
        job = q.enqueue("t", max_retries=0)
        q.dequeue()
        q.fail(job.job_id, error="something went wrong")
        assert q.get(job.job_id).error == "something went wrong"
        q.close()

    def test_fail_with_retries_re_enqueues_pending(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=3)
        q.dequeue()
        q.fail(job.job_id, error="transient")
        stored = q.get(job.job_id)
        assert stored.status == JobStatus.PENDING
        q.close()

    def test_fail_increments_retry_count(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=3)
        q.dequeue()
        q.fail(job.job_id)
        assert q.get(job.job_id).retry_count == 1
        q.close()

    def test_fail_applies_backoff_run_at(self):
        """After first retry: run_at = now + 1*5 = now+5."""
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=2)
        q.dequeue()
        q.fail(job.job_id)
        stored = q.get(job.job_id)
        assert stored.run_at == pytest.approx(1_005.0, abs=0.001)
        q.close()

    def test_fail_second_retry_backoff(self):
        """After second retry: run_at = now + 2*5 = now+10."""
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=3)
        # first fail
        q.dequeue()
        q.fail(job.job_id)
        # second fail: clock still at 1000; dequeue won't return the job
        # (run_at is now+5), so we advance the clock
        clock.advance(6.0)
        q.dequeue()
        q.fail(job.job_id)
        stored = q.get(job.job_id)
        assert stored.retry_count == 2
        # run_at = (1000+6) + 2*5 = 1016
        assert stored.run_at == pytest.approx(1_016.0, abs=0.001)
        q.close()

    def test_fail_exhausted_retries_sets_failed(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=2)
        for i in range(3):                         # fail 3 times
            q.dequeue()
            q.fail(job.job_id)
            clock.advance(100.0)
        stored = q.get(job.job_id)
        assert stored.status == JobStatus.FAILED
        q.close()

    def test_fail_exhausted_preserves_error(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=1)
        q.dequeue()
        q.fail(job.job_id, error="first")
        clock.advance(100.0)
        q.dequeue()
        q.fail(job.job_id, error="final error")
        stored = q.get(job.job_id)
        assert stored.status == JobStatus.FAILED
        assert stored.error == "final error"
        q.close()

    def test_fail_nonexistent_job_no_error(self):
        q = make_queue()
        q.fail("nonexistent", error="ignored")     # must not raise
        q.close()

    def test_fail_max_retries_zero_immediate_fail(self):
        q = make_queue()
        job = q.enqueue("t", max_retries=0)
        q.dequeue()
        q.fail(job.job_id, error="oops")
        assert q.get(job.job_id).status == JobStatus.FAILED
        q.close()


# ===========================================================================
# cancel
# ===========================================================================
class TestCancel:
    def test_cancel_pending_returns_true(self):
        q = make_queue()
        job = q.enqueue("t")
        assert q.cancel(job.job_id) is True
        q.close()

    def test_cancel_pending_sets_cancelled(self):
        q = make_queue()
        job = q.enqueue("t")
        q.cancel(job.job_id)
        assert q.get(job.job_id).status == JobStatus.CANCELLED
        q.close()

    def test_cancel_missing_job_returns_false(self):
        q = make_queue()
        assert q.cancel("no_such_id") is False
        q.close()

    def test_cancel_done_job_returns_false(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id)
        assert q.cancel(job.job_id) is False
        q.close()

    def test_cancel_running_job_returns_false(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()                                # now RUNNING
        assert q.cancel(job.job_id) is False
        q.close()

    def test_cancel_failed_job_returns_false(self):
        q = make_queue()
        job = q.enqueue("t", max_retries=0)
        q.dequeue()
        q.fail(job.job_id)
        assert q.cancel(job.job_id) is False
        q.close()

    def test_cancel_twice_second_returns_false(self):
        q = make_queue()
        job = q.enqueue("t")
        assert q.cancel(job.job_id) is True
        assert q.cancel(job.job_id) is False
        q.close()

    def test_cancel_removes_from_pending_count(self):
        q = make_queue()
        job = q.enqueue("t")
        assert q.pending_count() == 1
        q.cancel(job.job_id)
        assert q.pending_count() == 0
        q.close()

    def test_cancelled_job_not_dequeued(self):
        q = make_queue()
        job = q.enqueue("t")
        q.cancel(job.job_id)
        assert q.dequeue() is None
        q.close()


# ===========================================================================
# get
# ===========================================================================
class TestGet:
    def test_get_existing_job(self):
        q = make_queue()
        job = q.enqueue("t")
        fetched = q.get(job.job_id)
        assert fetched is not None
        assert fetched.job_id == job.job_id
        q.close()

    def test_get_unknown_returns_none(self):
        q = make_queue()
        assert q.get("unknown") is None
        q.close()

    def test_get_returns_current_status(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        fetched = q.get(job.job_id)
        assert fetched.status == JobStatus.RUNNING
        q.close()

    def test_get_after_complete(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id, result=99)
        fetched = q.get(job.job_id)
        assert fetched.status == JobStatus.DONE
        assert fetched.result == 99
        q.close()

    def test_get_payload_roundtrips(self):
        q = make_queue()
        payload = {"nested": {"list": [1, 2, 3]}, "flag": True}
        job = q.enqueue("t", payload=payload)
        fetched = q.get(job.job_id)
        assert fetched.payload == payload
        q.close()


# ===========================================================================
# list
# ===========================================================================
class TestList:
    def test_list_all_jobs(self):
        q = make_queue()
        q.enqueue("a")
        q.enqueue("b")
        q.enqueue("c")
        assert len(q.list()) == 3
        q.close()

    def test_list_filter_by_status(self):
        q = make_queue()
        j1 = q.enqueue("a")
        j2 = q.enqueue("b")
        q.dequeue()                                # j1 → RUNNING
        pending = q.list(status=JobStatus.PENDING)
        assert len(pending) == 1
        assert pending[0].job_id == j2.job_id
        q.close()

    def test_list_filter_by_name(self):
        q = make_queue()
        q.enqueue("alpha")
        q.enqueue("beta")
        q.enqueue("alpha")
        result = q.list(name="alpha")
        assert len(result) == 2
        assert all(j.name == "alpha" for j in result)
        q.close()

    def test_list_combined_filter(self):
        q = make_queue()
        j1 = q.enqueue("alpha")
        q.enqueue("alpha")
        q.dequeue()                                # j1 → RUNNING
        result = q.list(status=JobStatus.RUNNING, name="alpha")
        assert len(result) == 1
        assert result[0].job_id == j1.job_id
        q.close()

    def test_list_ordered_by_priority_then_created_at(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        clock.advance(1.0)
        q.enqueue("c", priority=5)
        clock.advance(1.0)
        q.enqueue("a", priority=1)
        clock.advance(1.0)
        q.enqueue("b", priority=1)
        names = [j.name for j in q.list()]
        assert names == ["a", "b", "c"]
        q.close()

    def test_list_empty_queue(self):
        q = make_queue()
        assert q.list() == []
        q.close()

    def test_list_no_match_returns_empty(self):
        q = make_queue()
        q.enqueue("task")
        result = q.list(status=JobStatus.DONE)
        assert result == []
        q.close()


# ===========================================================================
# pending_count
# ===========================================================================
class TestPendingCount:
    def test_pending_count_initially_zero(self):
        q = make_queue()
        assert q.pending_count() == 0
        q.close()

    def test_pending_count_after_enqueue(self):
        q = make_queue()
        q.enqueue("a")
        q.enqueue("b")
        assert q.pending_count() == 2
        q.close()

    def test_pending_count_excludes_running(self):
        q = make_queue()
        q.enqueue("a")
        q.enqueue("b")
        q.dequeue()
        assert q.pending_count() == 1
        q.close()

    def test_pending_count_excludes_done(self):
        q = make_queue()
        job = q.enqueue("a")
        q.dequeue()
        q.complete(job.job_id)
        assert q.pending_count() == 0
        q.close()

    def test_pending_count_excludes_failed(self):
        q = make_queue()
        job = q.enqueue("a", max_retries=0)
        q.dequeue()
        q.fail(job.job_id)
        assert q.pending_count() == 0
        q.close()


# ===========================================================================
# clear_done
# ===========================================================================
class TestClearDone:
    def test_clear_done_empty_returns_zero(self):
        q = make_queue()
        assert q.clear_done() == 0
        q.close()

    def test_clear_done_removes_only_done(self):
        q = make_queue()
        j1 = q.enqueue("a")
        j2 = q.enqueue("b")
        q.dequeue()                                # j1 → RUNNING
        q.complete(j1.job_id)                      # j1 → DONE
        deleted = q.clear_done()
        assert deleted == 1
        # j2 (PENDING) must still exist
        assert q.get(j2.job_id) is not None
        q.close()

    def test_clear_done_deleted_jobs_no_longer_retrievable(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id)
        q.clear_done()
        assert q.get(job.job_id) is None
        q.close()

    def test_clear_done_does_not_touch_failed(self):
        q = make_queue()
        job = q.enqueue("t", max_retries=0)
        q.dequeue()
        q.fail(job.job_id)
        q.clear_done()
        assert q.get(job.job_id) is not None
        assert q.get(job.job_id).status == JobStatus.FAILED
        q.close()

    def test_clear_done_multiple(self):
        q = make_queue()
        jobs = [q.enqueue(f"t{i}") for i in range(5)]
        for job in jobs:
            q.dequeue()
            q.complete(job.job_id)
        count = q.clear_done()
        assert count == 5
        assert q.list() == []
        q.close()

    def test_clear_done_does_not_touch_cancelled(self):
        q = make_queue()
        job = q.enqueue("t")
        q.cancel(job.job_id)
        q.clear_done()
        assert q.get(job.job_id) is not None
        assert q.get(job.job_id).status == JobStatus.CANCELLED
        q.close()


# ===========================================================================
# Persistence (file-backed DB)
# ===========================================================================
class TestPersistence:
    def test_job_survives_queue_reopen(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "queue.db")
            q1 = JobQueue(db_path=db)
            job = q1.enqueue("persistent_task", payload={"x": 99})
            q1.close()

            q2 = JobQueue(db_path=db)
            fetched = q2.get(job.job_id)
            assert fetched is not None
            assert fetched.name == "persistent_task"
            assert fetched.payload == {"x": 99}
            q2.close()

    def test_status_survives_queue_reopen(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "queue.db")
            q1 = JobQueue(db_path=db)
            job = q1.enqueue("t")
            q1.dequeue()
            q1.complete(job.job_id, result="done!")
            q1.close()

            q2 = JobQueue(db_path=db)
            fetched = q2.get(job.job_id)
            assert fetched.status == JobStatus.DONE
            assert fetched.result == "done!"
            q2.close()

    def test_multiple_jobs_persist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "queue.db")
            q1 = JobQueue(db_path=db)
            ids = [q1.enqueue(f"job_{i}").job_id for i in range(5)]
            q1.close()

            q2 = JobQueue(db_path=db)
            all_jobs = q2.list()
            assert len(all_jobs) == 5
            assert {j.job_id for j in all_jobs} == set(ids)
            q2.close()


# ===========================================================================
# Thread safety
# ===========================================================================
class TestThreadSafety:
    def test_concurrent_enqueue(self):
        q = make_queue()
        errors: list[Exception] = []

        def enqueue_batch():
            try:
                for i in range(20):
                    q.enqueue(f"task_{i}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=enqueue_batch) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(q.list()) == 100
        q.close()

    def test_concurrent_dequeue_no_duplicates(self):
        """Each job is claimed by at most one worker."""
        q = make_queue()
        n = 50
        for i in range(n):
            q.enqueue(f"t{i}")

        claimed: list[str] = []
        lock = threading.Lock()
        errors: list[Exception] = []

        def worker():
            try:
                while True:
                    job = q.dequeue()
                    if job is None:
                        break
                    with lock:
                        claimed.append(job.job_id)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(claimed) == n
        assert len(set(claimed)) == n          # no duplicates
        q.close()

    def test_concurrent_complete_no_errors(self):
        q = make_queue()
        jobs = [q.enqueue(f"t{i}") for i in range(30)]
        for job in jobs:
            q.dequeue()

        errors: list[Exception] = []

        def completer(jid: str):
            try:
                q.complete(jid, result={"jid": jid})
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=completer, args=(j.job_id,)) for j in jobs]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        done_jobs = q.list(status=JobStatus.DONE)
        assert len(done_jobs) == 30
        q.close()


# ===========================================================================
# Virtual time (scheduled jobs)
# ===========================================================================
class TestVirtualTime:
    def test_future_job_not_ready_before_time(self):
        clock = _advancing_clock(start=0.0)
        q = make_queue(now_fn=clock)
        q.enqueue("scheduled", run_at=100.0)
        clock.advance(50.0)                        # still 50 s short
        assert q.dequeue() is None
        q.close()

    def test_future_job_ready_after_time(self):
        clock = _advancing_clock(start=0.0)
        q = make_queue(now_fn=clock)
        q.enqueue("scheduled", run_at=100.0)
        clock.advance(100.0)
        job = q.dequeue()
        assert job is not None
        assert job.name == "scheduled"
        q.close()

    def test_retry_backoff_scheduled_in_future(self):
        clock = _advancing_clock(start=1_000.0)
        q = make_queue(now_fn=clock)
        job = q.enqueue("t", max_retries=1)
        q.dequeue()
        q.fail(job.job_id, error="transient")
        # Backoff = 1*5 = 5 seconds → run_at = 1005
        assert q.dequeue() is None              # clock is at 1000, job not yet ready

        clock.advance(5.0)                      # now at 1005
        retried = q.dequeue()
        assert retried is not None
        assert retried.job_id == job.job_id
        q.close()

    def test_multiple_scheduled_jobs_ordered_by_run_at_then_priority(self):
        """Among ready jobs, lowest priority value wins; among same priority,
        earliest run_at wins."""
        clock = _advancing_clock(start=2_000.0)
        q = make_queue(now_fn=clock)
        q.enqueue("late",  priority=1, run_at=1_900.0)
        q.enqueue("early", priority=1, run_at=1_500.0)
        q.enqueue("urgent",priority=0, run_at=1_800.0)

        first = q.dequeue()
        assert first.name == "urgent"           # lowest priority value (0)
        second = q.dequeue()
        assert second.name == "early"           # same priority (1), earliest run_at
        q.close()


# ===========================================================================
# Additional edge cases
# ===========================================================================
class TestEdgeCases:
    def test_close_then_reopen_same_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "q.db")
            q = JobQueue(db_path=db)
            q.enqueue("x")
            q.close()
            # Re-opening should work fine.
            q2 = JobQueue(db_path=db)
            assert q2.pending_count() == 1
            q2.close()

    def test_enqueue_with_nested_payload(self):
        q = make_queue()
        payload = {"level1": {"level2": [1, 2, {"level3": True}]}}
        job = q.enqueue("deep", payload=payload)
        fetched = q.get(job.job_id)
        assert fetched.payload == payload
        q.close()

    def test_now_fn_injection(self):
        """Injected now_fn controls created_at / updated_at timestamps."""
        q = make_queue(now_fn=_fixed_now(42.0))
        job = q.enqueue("t")
        assert job.created_at == pytest.approx(42.0, abs=0.001)
        assert job.updated_at == pytest.approx(42.0, abs=0.001)
        q.close()

    def test_enqueue_priority_zero_default(self):
        q = make_queue()
        job = q.enqueue("t")
        assert job.priority == 0
        q.close()

    def test_fail_with_empty_error_string(self):
        q = make_queue()
        job = q.enqueue("t", max_retries=0)
        q.dequeue()
        q.fail(job.job_id, error="")
        stored = q.get(job.job_id)
        assert stored.status == JobStatus.FAILED
        assert stored.error == ""
        q.close()

    def test_complete_with_integer_result(self):
        q = make_queue()
        job = q.enqueue("t")
        q.dequeue()
        q.complete(job.job_id, result=7)
        assert q.get(job.job_id).result == 7
        q.close()

    def test_large_payload(self):
        q = make_queue()
        big = {"data": "x" * 10_000, "nums": list(range(100))}
        job = q.enqueue("big", payload=big)
        assert q.get(job.job_id).payload == big
        q.close()

    def test_many_jobs_priority_sort(self):
        q = make_queue()
        for p in reversed(range(10)):
            q.enqueue(str(p), priority=p)
        jobs = [q.dequeue() for _ in range(10)]
        priorities = [j.priority for j in jobs]
        assert priorities == list(range(10))
        q.close()

    def test_cancel_non_pending_states(self):
        """cancel on DONE, FAILED, CANCELLED all return False."""
        q = make_queue()
        j1 = q.enqueue("done")
        q.dequeue(); q.complete(j1.job_id)
        assert q.cancel(j1.job_id) is False

        j2 = q.enqueue("failed", max_retries=0)
        q.dequeue(); q.fail(j2.job_id)
        assert q.cancel(j2.job_id) is False

        j3 = q.enqueue("cancelled")
        q.cancel(j3.job_id)
        assert q.cancel(j3.job_id) is False
        q.close()
