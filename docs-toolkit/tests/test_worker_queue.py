"""Tests for docstoolkit.worker_queue (E89).

Pure stdlib worker queue: Job + JobQueue + WorkerPool.
"""
from __future__ import annotations

import threading
import time
from typing import Any

import pytest

from docstoolkit.worker_queue import (
    Job,
    JobHandler,
    JobQueue,
    JobStatus,
    WorkerConfig,
    WorkerPool,
)


# ---------------------------------------------------------------------------
# Helper handlers
# ---------------------------------------------------------------------------
class EchoHandler(JobHandler):
    """Returns the payload unchanged."""

    def handle(self, job: Job) -> Any:
        return job.payload


class CountingHandler(JobHandler):
    """Records every call; returns a counter value."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.calls: list[str] = []

    def handle(self, job: Job) -> Any:
        with self.lock:
            self.calls.append(job.job_id)
            return len(self.calls)


class AlwaysFailHandler(JobHandler):
    """Always raises a RuntimeError."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.attempts = 0

    def handle(self, job: Job) -> Any:
        with self.lock:
            self.attempts += 1
        raise RuntimeError("boom")


class FlakyHandler(JobHandler):
    """Fails the first N attempts, then succeeds."""

    def __init__(self, fail_until: int) -> None:
        self.fail_until = fail_until
        self.lock = threading.Lock()
        self.calls = 0

    def handle(self, job: Job) -> Any:
        with self.lock:
            self.calls += 1
            n = self.calls
        if n <= self.fail_until:
            raise ValueError(f"flaky attempt {n}")
        return "ok"


class SlowHandler(JobHandler):
    """Sleeps before returning, useful for concurrency tests."""

    def __init__(self, delay: float = 0.05) -> None:
        self.delay = delay
        self.lock = threading.Lock()
        self.active = 0
        self.max_active = 0
        self.processed = 0

    def handle(self, job: Job) -> Any:
        with self.lock:
            self.active += 1
            if self.active > self.max_active:
                self.max_active = self.active
        try:
            time.sleep(self.delay)
            return job.job_id
        finally:
            with self.lock:
                self.active -= 1
                self.processed += 1


def _wait_until(predicate, timeout: float = 2.0, interval: float = 0.005) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


# ===========================================================================
# JobStatus enum
# ===========================================================================
class TestJobStatusEnum:
    def test_queued_value(self):
        assert JobStatus.QUEUED.value == "queued"

    def test_running_value(self):
        assert JobStatus.RUNNING.value == "running"

    def test_success_value(self):
        assert JobStatus.SUCCESS.value == "success"

    def test_failed_value(self):
        assert JobStatus.FAILED.value == "failed"

    def test_retrying_value(self):
        assert JobStatus.RETRYING.value == "retrying"

    def test_dead_value(self):
        assert JobStatus.DEAD.value == "dead"

    def test_all_members_present(self):
        names = {m.name for m in JobStatus}
        assert names == {"QUEUED", "RUNNING", "SUCCESS", "FAILED", "RETRYING", "DEAD"}

    def test_status_count(self):
        assert len(list(JobStatus)) == 6

    def test_status_is_enum(self):
        from enum import Enum
        assert issubclass(JobStatus, Enum)

    def test_equality_by_identity(self):
        assert JobStatus.QUEUED is JobStatus.QUEUED


# ===========================================================================
# Job dataclass
# ===========================================================================
class TestJobDataclass:
    def test_default_job_id_length(self):
        job = Job()
        assert len(job.job_id) == 12

    def test_default_job_id_unique(self):
        a = Job()
        b = Job()
        assert a.job_id != b.job_id

    def test_default_name_empty(self):
        assert Job().name == ""

    def test_default_payload_dict(self):
        job = Job()
        assert job.payload == {}
        assert isinstance(job.payload, dict)

    def test_payload_independent_between_instances(self):
        a = Job()
        b = Job()
        a.payload["k"] = 1
        assert "k" not in b.payload

    def test_default_priority(self):
        assert Job().priority == 5

    def test_default_status_queued(self):
        assert Job().status == JobStatus.QUEUED

    def test_default_enqueued_at_is_recent(self):
        before = time.time()
        job = Job()
        after = time.time()
        assert before <= job.enqueued_at <= after

    def test_default_started_at_zero(self):
        assert Job().started_at == 0.0

    def test_default_finished_at_zero(self):
        assert Job().finished_at == 0.0

    def test_default_attempts_zero(self):
        assert Job().attempts == 0

    def test_default_max_attempts_three(self):
        assert Job().max_attempts == 3

    def test_default_error_empty(self):
        assert Job().error == ""

    def test_default_result_none(self):
        assert Job().result is None

    def test_custom_name(self):
        assert Job(name="hello").name == "hello"

    def test_custom_priority(self):
        assert Job(priority=1).priority == 1

    def test_custom_payload(self):
        job = Job(payload={"x": 10})
        assert job.payload == {"x": 10}

    def test_custom_job_id(self):
        job = Job(job_id="fixed-id")
        assert job.job_id == "fixed-id"

    def test_custom_max_attempts(self):
        assert Job(max_attempts=7).max_attempts == 7


# ===========================================================================
# JobQueue: basic enqueue / dequeue
# ===========================================================================
class TestJobQueueBasic:
    def test_new_queue_is_empty(self):
        q = JobQueue()
        assert q.is_empty()

    def test_new_queue_size_zero(self):
        assert JobQueue().size() == 0

    def test_enqueue_returns_job_id(self):
        q = JobQueue()
        job = Job(name="x")
        assert q.enqueue(job) == job.job_id

    def test_enqueue_increments_size(self):
        q = JobQueue()
        q.enqueue(Job())
        assert q.size() == 1

    def test_enqueue_two_size(self):
        q = JobQueue()
        q.enqueue(Job())
        q.enqueue(Job())
        assert q.size() == 2

    def test_is_empty_after_enqueue(self):
        q = JobQueue()
        q.enqueue(Job())
        assert not q.is_empty()

    def test_dequeue_returns_enqueued(self):
        q = JobQueue()
        j = Job(name="solo")
        q.enqueue(j)
        out = q.dequeue(timeout=0.1)
        assert out is j

    def test_dequeue_empty_with_zero_timeout(self):
        q = JobQueue()
        assert q.dequeue(timeout=0.0) is None

    def test_dequeue_empty_with_small_timeout(self):
        q = JobQueue()
        start = time.monotonic()
        out = q.dequeue(timeout=0.05)
        elapsed = time.monotonic() - start
        assert out is None
        assert elapsed >= 0.04

    def test_dequeue_decrements_size(self):
        q = JobQueue()
        q.enqueue(Job())
        q.dequeue(timeout=0.1)
        assert q.size() == 0

    def test_enqueue_sets_status_queued(self):
        q = JobQueue()
        j = Job(status=JobStatus.RETRYING)
        q.enqueue(j)
        # enqueue normalizes status back to QUEUED so dequeue can pop it.
        assert j.status == JobStatus.QUEUED


# ===========================================================================
# JobQueue: priority + FIFO
# ===========================================================================
class TestJobQueuePriority:
    def test_lower_priority_value_first(self):
        q = JobQueue()
        a = Job(name="lo", priority=10)
        b = Job(name="hi", priority=1)
        q.enqueue(a)
        q.enqueue(b)
        assert q.dequeue(timeout=0.1).name == "hi"
        assert q.dequeue(timeout=0.1).name == "lo"

    def test_three_priorities(self):
        q = JobQueue()
        q.enqueue(Job(name="mid", priority=5))
        q.enqueue(Job(name="lo", priority=9))
        q.enqueue(Job(name="hi", priority=1))
        order = [q.dequeue(timeout=0.1).name for _ in range(3)]
        assert order == ["hi", "mid", "lo"]

    def test_fifo_within_same_priority(self):
        q = JobQueue()
        names = ["a", "b", "c", "d"]
        for n in names:
            q.enqueue(Job(name=n, priority=5))
        out = [q.dequeue(timeout=0.1).name for _ in names]
        assert out == names

    def test_priority_then_fifo(self):
        q = JobQueue()
        q.enqueue(Job(name="a5", priority=5))
        q.enqueue(Job(name="b1", priority=1))
        q.enqueue(Job(name="c5", priority=5))
        q.enqueue(Job(name="d1", priority=1))
        order = [q.dequeue(timeout=0.1).name for _ in range(4)]
        assert order == ["b1", "d1", "a5", "c5"]

    def test_negative_priority_wins(self):
        q = JobQueue()
        q.enqueue(Job(name="zero", priority=0))
        q.enqueue(Job(name="neg", priority=-3))
        assert q.dequeue(timeout=0.1).name == "neg"

    def test_priority_one_beats_default(self):
        q = JobQueue()
        q.enqueue(Job(name="default"))  # priority 5 by default
        q.enqueue(Job(name="urgent", priority=1))
        assert q.dequeue(timeout=0.1).name == "urgent"


# ===========================================================================
# JobQueue: peek
# ===========================================================================
class TestJobQueuePeek:
    def test_peek_empty(self):
        assert JobQueue().peek() is None

    def test_peek_returns_top(self):
        q = JobQueue()
        a = Job(name="a", priority=5)
        b = Job(name="b", priority=1)
        q.enqueue(a)
        q.enqueue(b)
        assert q.peek() is b

    def test_peek_does_not_remove(self):
        q = JobQueue()
        q.enqueue(Job(name="only"))
        q.peek()
        assert q.size() == 1

    def test_peek_idempotent(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        assert q.peek() is q.peek()

    def test_peek_after_cancel(self):
        q = JobQueue()
        a = Job(name="a", priority=1)
        b = Job(name="b", priority=5)
        q.enqueue(a)
        q.enqueue(b)
        q.cancel(a.job_id)
        # b should now bubble up.
        assert q.peek() is b

    def test_peek_after_all_cancelled(self):
        q = JobQueue()
        a = Job()
        q.enqueue(a)
        q.cancel(a.job_id)
        assert q.peek() is None


# ===========================================================================
# JobQueue: size / is_empty
# ===========================================================================
class TestJobQueueSize:
    def test_size_tracks_enqueue_dequeue(self):
        q = JobQueue()
        for _ in range(5):
            q.enqueue(Job())
        assert q.size() == 5
        q.dequeue(timeout=0.1)
        assert q.size() == 4

    def test_is_empty_initially(self):
        assert JobQueue().is_empty()

    def test_is_empty_after_drain(self):
        q = JobQueue()
        q.enqueue(Job())
        q.dequeue(timeout=0.1)
        assert q.is_empty()

    def test_size_after_cancel(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        assert q.size() == 1
        q.cancel(j.job_id)
        assert q.size() == 0

    def test_size_after_clear(self):
        q = JobQueue()
        for _ in range(3):
            q.enqueue(Job())
        q.clear()
        assert q.size() == 0


# ===========================================================================
# JobQueue: get / cancel / clear
# ===========================================================================
class TestJobQueueGet:
    def test_get_returns_job(self):
        q = JobQueue()
        j = Job(name="x")
        q.enqueue(j)
        assert q.get(j.job_id) is j

    def test_get_unknown_returns_none(self):
        assert JobQueue().get("nope") is None

    def test_get_after_dequeue_still_returns(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        q.dequeue(timeout=0.1)
        # Job stays in registry so workers can update state.
        assert q.get(j.job_id) is j


class TestJobQueueCancel:
    def test_cancel_queued_returns_true(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        assert q.cancel(j.job_id) is True

    def test_cancel_sets_failed(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        q.cancel(j.job_id)
        assert j.status == JobStatus.FAILED

    def test_cancel_unknown_returns_false(self):
        assert JobQueue().cancel("missing") is False

    def test_cancel_twice_returns_false_second_time(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        assert q.cancel(j.job_id) is True
        assert q.cancel(j.job_id) is False

    def test_cancel_removed_from_size(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        q.cancel(j.job_id)
        assert q.size() == 0

    def test_cancel_running_returns_false(self):
        q = JobQueue()
        j = Job()
        q.enqueue(j)
        # Pop it so it is no longer QUEUED.
        q.dequeue(timeout=0.1)
        j.status = JobStatus.RUNNING
        assert q.cancel(j.job_id) is False

    def test_cancel_skips_in_dequeue(self):
        q = JobQueue()
        a = Job(name="a", priority=1)
        b = Job(name="b", priority=2)
        q.enqueue(a)
        q.enqueue(b)
        q.cancel(a.job_id)
        out = q.dequeue(timeout=0.1)
        assert out is b


class TestJobQueueClear:
    def test_clear_empty_returns_zero(self):
        assert JobQueue().clear() == 0

    def test_clear_counts_queued(self):
        q = JobQueue()
        for _ in range(4):
            q.enqueue(Job())
        assert q.clear() == 4

    def test_clear_makes_empty(self):
        q = JobQueue()
        for _ in range(3):
            q.enqueue(Job())
        q.clear()
        assert q.is_empty()

    def test_clear_marks_jobs_failed(self):
        q = JobQueue()
        jobs = [Job() for _ in range(3)]
        for j in jobs:
            q.enqueue(j)
        q.clear()
        for j in jobs:
            assert j.status == JobStatus.FAILED

    def test_clear_then_dequeue_returns_none(self):
        q = JobQueue()
        q.enqueue(Job())
        q.enqueue(Job())
        q.clear()
        assert q.dequeue(timeout=0.05) is None


# ===========================================================================
# JobQueue: blocking semantics
# ===========================================================================
class TestJobQueueBlocking:
    def test_dequeue_blocks_until_enqueue(self):
        q = JobQueue()
        result: list[Job] = []

        def consumer():
            r = q.dequeue(timeout=1.0)
            if r is not None:
                result.append(r)

        t = threading.Thread(target=consumer)
        t.start()
        time.sleep(0.05)
        j = Job(name="late")
        q.enqueue(j)
        t.join(timeout=2.0)
        assert result == [j]

    def test_dequeue_timeout_returns_none_when_starved(self):
        q = JobQueue()
        assert q.dequeue(timeout=0.05) is None

    def test_concurrent_producers(self):
        q = JobQueue()

        def produce():
            for _ in range(10):
                q.enqueue(Job())

        threads = [threading.Thread(target=produce) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert q.size() == 30


# ===========================================================================
# WorkerPool: happy path
# ===========================================================================
class TestWorkerPoolHappy:
    def test_single_job_processed(self):
        q = JobQueue()
        h = CountingHandler()
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(name="hello", payload={"x": 1})
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.result == 1
        finally:
            pool.stop()

    def test_multiple_jobs_processed(self):
        q = JobQueue()
        h = CountingHandler()
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            jobs = [Job() for _ in range(5)]
            for j in jobs:
                q.enqueue(j)
            assert _wait_until(
                lambda: all(j.status == JobStatus.SUCCESS for j in jobs),
                timeout=3.0,
            )
        finally:
            pool.stop()
        assert pool.success_count == 5

    def test_success_count_increments(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            for _ in range(3):
                q.enqueue(Job())
            assert _wait_until(lambda: pool.success_count == 3, timeout=2.0)
        finally:
            pool.stop()

    def test_processed_count_total(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            for _ in range(4):
                q.enqueue(Job())
            assert _wait_until(lambda: pool.processed_count == 4, timeout=2.0)
        finally:
            pool.stop()

    def test_failed_count_zero_when_no_failures(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            q.enqueue(Job())
            assert _wait_until(lambda: pool.processed_count == 1, timeout=2.0)
            assert pool.failed_count == 0
        finally:
            pool.stop()

    def test_job_result_recorded(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(payload={"answer": 42})
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.result == {"answer": 42}
        finally:
            pool.stop()

    def test_attempts_increments_once_on_success(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job()
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.attempts == 1
        finally:
            pool.stop()

    def test_finished_at_set_on_success(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job()
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.finished_at > 0
        finally:
            pool.stop()

    def test_started_at_set_on_success(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job()
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.started_at >= j.enqueued_at
        finally:
            pool.stop()

    def test_error_empty_on_success(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job()
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.error == ""
        finally:
            pool.stop()


# ===========================================================================
# WorkerPool: retries and DEAD
# ===========================================================================
class TestWorkerPoolRetries:
    def test_failing_handler_retried_until_dead(self):
        q = JobQueue()
        h = AlwaysFailHandler()
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=3)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.DEAD, timeout=3.0)
            assert j.attempts == 3
        finally:
            pool.stop()

    def test_dead_job_recorded_as_failed_count(self):
        q = JobQueue()
        pool = WorkerPool(q, AlwaysFailHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=2)
            q.enqueue(j)
            assert _wait_until(lambda: pool.failed_count == 1, timeout=3.0)
        finally:
            pool.stop()

    def test_max_attempts_one_no_retries(self):
        q = JobQueue()
        h = AlwaysFailHandler()
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=1)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.DEAD, timeout=2.0)
            assert j.attempts == 1
        finally:
            pool.stop()

    def test_flaky_handler_eventually_succeeds(self):
        q = JobQueue()
        h = FlakyHandler(fail_until=2)
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=5)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=3.0)
            assert j.result == "ok"
            assert j.attempts == 3
        finally:
            pool.stop()

    def test_error_message_on_failure(self):
        q = JobQueue()
        pool = WorkerPool(q, AlwaysFailHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=1)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.DEAD, timeout=2.0)
            assert "RuntimeError" in j.error
            assert "boom" in j.error
        finally:
            pool.stop()

    def test_retry_intermediate_status(self):
        """During retry the job is observable in RETRYING/QUEUED states."""
        q = JobQueue()
        h = AlwaysFailHandler()
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=3)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.DEAD, timeout=3.0)
            # Eventually three attempts were made.
            assert h.attempts == 3
        finally:
            pool.stop()

    def test_failed_count_only_on_dead(self):
        q = JobQueue()
        h = FlakyHandler(fail_until=1)
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=3)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert pool.failed_count == 0
            assert pool.success_count == 1
        finally:
            pool.stop()

    def test_processed_count_counts_dead(self):
        q = JobQueue()
        pool = WorkerPool(q, AlwaysFailHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=2)
            q.enqueue(j)
            assert _wait_until(lambda: pool.processed_count == 1, timeout=3.0)
        finally:
            pool.stop()


# ===========================================================================
# WorkerPool: lifecycle (start/stop)
# ===========================================================================
class TestWorkerPoolLifecycle:
    def test_stop_without_start_no_error(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler())
        pool.stop(wait=False)

    def test_start_then_stop_clean(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        pool.stop()
        # All threads must be done.
        for t in pool._threads:
            assert not t.is_alive()

    def test_start_is_idempotent(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=2, poll_interval=0.01))
        pool.start()
        before = len(pool._threads)
        pool.start()  # second call must be a no-op
        try:
            assert len(pool._threads) == before
        finally:
            pool.stop()

    def test_stop_wait_false(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        pool.stop(wait=False)
        # Workers will exit on next poll_interval; either way the call is safe.

    def test_can_restart_after_stop(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        pool.stop()
        pool.start()
        try:
            q.enqueue(Job())
            assert _wait_until(lambda: pool.success_count >= 1, timeout=2.0)
        finally:
            pool.stop()


# ===========================================================================
# WorkerPool: concurrency
# ===========================================================================
class TestWorkerPoolConcurrency:
    def test_multiple_workers_share_load(self):
        q = JobQueue()
        h = SlowHandler(delay=0.05)
        pool = WorkerPool(q, h, WorkerConfig(worker_count=4, poll_interval=0.005))
        pool.start()
        try:
            for _ in range(8):
                q.enqueue(Job())
            assert _wait_until(lambda: h.processed >= 8, timeout=5.0)
            # With 4 workers we expect overlap.
            assert h.max_active >= 2
        finally:
            pool.stop()

    def test_two_workers_finish_faster_than_one(self):
        """Sanity check: 2 workers visibly overlap on slow jobs."""
        q = JobQueue()
        h = SlowHandler(delay=0.03)
        pool = WorkerPool(q, h, WorkerConfig(worker_count=2, poll_interval=0.005))
        pool.start()
        try:
            for _ in range(4):
                q.enqueue(Job())
            assert _wait_until(lambda: h.processed == 4, timeout=3.0)
            assert h.max_active == 2
        finally:
            pool.stop()

    def test_worker_count_one(self):
        q = JobQueue()
        h = SlowHandler(delay=0.01)
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.005))
        pool.start()
        try:
            for _ in range(3):
                q.enqueue(Job())
            assert _wait_until(lambda: h.processed == 3, timeout=3.0)
            assert h.max_active == 1
        finally:
            pool.stop()

    def test_default_config_runs(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler())  # default WorkerConfig()
        pool.start()
        try:
            q.enqueue(Job())
            assert _wait_until(lambda: pool.success_count == 1, timeout=2.0)
        finally:
            pool.stop()

    def test_priority_respected_by_workers(self):
        q = JobQueue()

        order: list[str] = []
        lock = threading.Lock()

        class RecordHandler(JobHandler):
            def handle(self, job: Job) -> Any:
                with lock:
                    order.append(job.name)
                return None

        pool = WorkerPool(q, RecordHandler(), WorkerConfig(worker_count=1, poll_interval=0.005))
        # Enqueue first, then start, to avoid worker grabbing one before
        # both are inserted.
        q.enqueue(Job(name="low", priority=9))
        q.enqueue(Job(name="high", priority=1))
        pool.start()
        try:
            assert _wait_until(lambda: len(order) == 2, timeout=2.0)
            assert order[0] == "high"
        finally:
            pool.stop()


# ===========================================================================
# WorkerPool: handler ABC & config
# ===========================================================================
class TestHandlerAndConfig:
    def test_handler_is_abstract(self):
        with pytest.raises(TypeError):
            JobHandler()  # type: ignore[abstract]

    def test_config_defaults(self):
        c = WorkerConfig()
        assert c.worker_count == 1
        assert c.poll_interval == 0.05

    def test_config_custom_values(self):
        c = WorkerConfig(worker_count=8, poll_interval=0.2)
        assert c.worker_count == 8
        assert c.poll_interval == 0.2

    def test_pool_stores_handler(self):
        q = JobQueue()
        h = EchoHandler()
        pool = WorkerPool(q, h)
        assert pool.handler is h

    def test_pool_stores_queue(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler())
        assert pool.queue is q

    def test_pool_uses_default_config_when_none(self):
        q = JobQueue()
        pool = WorkerPool(q, EchoHandler(), config=None)
        assert isinstance(pool.config, WorkerConfig)
        assert pool.config.worker_count == 1


# ===========================================================================
# Edge cases
# ===========================================================================
class TestEdgeCases:
    def test_dequeue_with_none_timeout_blocks_until_enqueue(self):
        q = JobQueue()
        got: list[Job] = []

        def consumer():
            r = q.dequeue(timeout=None)
            if r is not None:
                got.append(r)

        t = threading.Thread(target=consumer, daemon=True)
        t.start()
        time.sleep(0.05)
        j = Job()
        q.enqueue(j)
        t.join(timeout=1.0)
        assert got == [j]

    def test_dequeue_zero_timeout_immediate(self):
        q = JobQueue()
        start = time.monotonic()
        assert q.dequeue(timeout=0.0) is None
        assert (time.monotonic() - start) < 0.05

    def test_cancel_nonexistent_does_not_raise(self):
        q = JobQueue()
        # No exception; just returns False.
        assert q.cancel("ghost") is False

    def test_clear_after_drain(self):
        q = JobQueue()
        q.enqueue(Job())
        q.dequeue(timeout=0.1)
        assert q.clear() == 0

    def test_enqueue_after_clear(self):
        q = JobQueue()
        q.enqueue(Job())
        q.clear()
        j = Job()
        q.enqueue(j)
        assert q.dequeue(timeout=0.1) is j

    def test_many_priorities(self):
        q = JobQueue()
        for p in [7, 3, 1, 9, 5]:
            q.enqueue(Job(name=str(p), priority=p))
        names = [q.dequeue(timeout=0.1).name for _ in range(5)]
        assert names == ["1", "3", "5", "7", "9"]

    def test_large_batch(self):
        q = JobQueue()
        for i in range(100):
            q.enqueue(Job(name=f"j{i}"))
        assert q.size() == 100
        seen = []
        for _ in range(100):
            seen.append(q.dequeue(timeout=0.5).name)
        assert seen == [f"j{i}" for i in range(100)]
        assert q.is_empty()

    def test_handler_returns_none(self):
        class NoneHandler(JobHandler):
            def handle(self, job: Job) -> Any:
                return None

        q = JobQueue()
        pool = WorkerPool(q, NoneHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job()
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.result is None
        finally:
            pool.stop()

    def test_handler_returns_complex_object(self):
        class ComplexHandler(JobHandler):
            def handle(self, job: Job) -> Any:
                return {"list": [1, 2, 3], "ok": True}

        q = JobQueue()
        pool = WorkerPool(q, ComplexHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job()
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.result == {"list": [1, 2, 3], "ok": True}
        finally:
            pool.stop()

    def test_get_after_failure(self):
        q = JobQueue()
        pool = WorkerPool(q, AlwaysFailHandler(), WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(max_attempts=1)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.DEAD, timeout=2.0)
            assert q.get(j.job_id) is j
        finally:
            pool.stop()

    def test_priority_unchanged_on_retry(self):
        q = JobQueue()
        h = FlakyHandler(fail_until=1)
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.01))
        pool.start()
        try:
            j = Job(priority=2, max_attempts=3)
            q.enqueue(j)
            assert _wait_until(lambda: j.status == JobStatus.SUCCESS, timeout=2.0)
            assert j.priority == 2
        finally:
            pool.stop()

    def test_distinct_jobs_have_distinct_ids(self):
        ids = {Job().job_id for _ in range(50)}
        assert len(ids) == 50

    def test_cancel_after_pool_started_skips_job(self):
        q = JobQueue()
        h = CountingHandler()
        pool = WorkerPool(q, h, WorkerConfig(worker_count=1, poll_interval=0.05))
        j = Job(name="will-cancel", priority=9)
        q.enqueue(j)
        # Cancel before worker reaches it.
        assert q.cancel(j.job_id) is True
        pool.start()
        try:
            time.sleep(0.2)
            assert j.job_id not in h.calls
        finally:
            pool.stop()
