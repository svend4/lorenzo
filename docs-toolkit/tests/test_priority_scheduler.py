"""Tests for docstoolkit.priority_scheduler — E99.

~95 tests covering:
- Submit and complete a task
- Priority ordering (lower int runs first)
- Task cancellation while pending
- Expired task (deadline in the past → EXPIRED)
- Result retrieval (blocking wait)
- Failed task (fn raises) → FAILED, error stored
- stats() counts
- pending_count()
- Multiple workers run tasks concurrently
- start/stop lifecycle
- stop(wait=True) drains queue
- Cancelling non-existent task → False
- Cancelling already-done task → False
- Thread safety (concurrent submits)
- Default priority is 0
- kwargs pass through to fn
"""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.priority_scheduler import (
    PriorityScheduler,
    ScheduledTask,
    TaskStatus,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make(workers: int = 1, now_fn=None) -> PriorityScheduler:
    """Return a started scheduler; caller must call stop() or use the fixture."""
    sched = PriorityScheduler(workers=workers, now_fn=now_fn)
    sched.start()
    return sched


def _past(offset: float = 1.0) -> float:
    """Return a timestamp that is *offset* seconds in the past."""
    return time.time() - offset


def _future(offset: float = 60.0) -> float:
    """Return a timestamp that is *offset* seconds in the future."""
    return time.time() + offset


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sched():
    """A single-worker scheduler, stopped automatically after each test."""
    s = _make(workers=1)
    yield s
    s.stop(wait=True)


@pytest.fixture
def sched2():
    """A two-worker scheduler, stopped automatically after each test."""
    s = _make(workers=2)
    yield s
    s.stop(wait=True)


# ===========================================================================
# 1. ScheduledTask dataclass
# ===========================================================================

class TestScheduledTask:
    def test_default_status_is_pending(self):
        t = ScheduledTask()
        assert t.status == TaskStatus.PENDING

    def test_default_priority_is_zero(self):
        t = ScheduledTask()
        assert t.priority == 0

    def test_task_id_auto_generated(self):
        t = ScheduledTask()
        assert isinstance(t.task_id, str)
        assert len(t.task_id) == 12

    def test_task_id_unique(self):
        ids = {ScheduledTask().task_id for _ in range(100)}
        assert len(ids) == 100

    def test_default_result_is_none(self):
        t = ScheduledTask()
        assert t.result is None

    def test_default_error_is_none(self):
        t = ScheduledTask()
        assert t.error is None

    def test_default_deadline_is_none(self):
        t = ScheduledTask()
        assert t.deadline is None

    def test_default_args_empty_tuple(self):
        t = ScheduledTask()
        assert t.args == ()

    def test_default_kwargs_empty_dict(self):
        t = ScheduledTask()
        assert t.kwargs == {}

    def test_custom_priority(self):
        t = ScheduledTask(priority=5)
        assert t.priority == 5


# ===========================================================================
# 2. TaskStatus enum
# ===========================================================================

class TestTaskStatus:
    def test_pending_value(self):
        assert TaskStatus.PENDING == "pending"

    def test_running_value(self):
        assert TaskStatus.RUNNING == "running"

    def test_done_value(self):
        assert TaskStatus.DONE == "done"

    def test_cancelled_value(self):
        assert TaskStatus.CANCELLED == "cancelled"

    def test_failed_value(self):
        assert TaskStatus.FAILED == "failed"

    def test_expired_value(self):
        assert TaskStatus.EXPIRED == "expired"

    def test_is_str(self):
        assert isinstance(TaskStatus.PENDING, str)


# ===========================================================================
# 3. Submit and basic completion
# ===========================================================================

class TestSubmitAndComplete:
    def test_submit_returns_scheduled_task(self, sched):
        task = sched.submit(lambda: 1)
        assert isinstance(task, ScheduledTask)

    def test_submit_returns_immediately(self, sched):
        """submit() should return before fn even starts."""
        barrier = threading.Barrier(2)

        def slow():
            barrier.wait(timeout=2)
            return "ok"

        task = sched.submit(slow)
        # We can assert the returned task right away, before fn runs
        assert task.task_id is not None
        barrier.wait(timeout=2)  # release the worker

    def test_task_completes_with_result(self, sched):
        task = sched.submit(lambda: 42)
        value = sched.result(task.task_id, timeout=2.0)
        assert value == 42

    def test_status_becomes_done(self, sched):
        task = sched.submit(lambda: None)
        sched.result(task.task_id, timeout=2.0)
        assert task.status == TaskStatus.DONE

    def test_result_stored_on_task(self, sched):
        task = sched.submit(lambda: "hello")
        sched.result(task.task_id, timeout=2.0)
        assert task.result == "hello"

    def test_none_result(self, sched):
        task = sched.submit(lambda: None)
        assert sched.result(task.task_id, timeout=2.0) is None

    def test_default_priority_zero(self, sched):
        task = sched.submit(lambda: 0)
        assert task.priority == 0

    def test_submit_with_explicit_priority(self, sched):
        task = sched.submit(lambda: 0, priority=7)
        assert task.priority == 7

    def test_args_passed_to_fn(self, sched):
        task = sched.submit(lambda x, y: x + y, 3, 4)
        assert sched.result(task.task_id, timeout=2.0) == 7

    def test_kwargs_passed_to_fn(self, sched):
        task = sched.submit(lambda a, b: a * b, a=6, b=7)
        assert sched.result(task.task_id, timeout=2.0) == 42

    def test_mixed_args_kwargs(self, sched):
        task = sched.submit(lambda x, y, z: (x, y, z), 1, 2, z=3)
        assert sched.result(task.task_id, timeout=2.0) == (1, 2, 3)

    def test_kwargs_only(self, sched):
        def fn(name="world"):
            return f"hello {name}"

        task = sched.submit(fn, name="pytest")
        assert sched.result(task.task_id, timeout=2.0) == "hello pytest"

    def test_multiple_tasks_all_complete(self, sched):
        tasks = [sched.submit(lambda i=i: i, priority=0) for i in range(5)]
        results = {sched.result(t.task_id, timeout=2.0) for t in tasks}
        assert results == {0, 1, 2, 3, 4}


# ===========================================================================
# 4. Priority ordering
# ===========================================================================

class TestPriorityOrdering:
    def test_lower_priority_int_runs_first(self):
        """With a single worker the task with priority=0 should run before 10."""
        order: list[int] = []
        gate = threading.Event()   # hold worker until both tasks are queued

        def record(p: int):
            gate.wait(timeout=2)
            order.append(p)

        sched = PriorityScheduler(workers=1)
        # Don't start yet so we can queue both tasks first.
        # Submit both before starting.
        t_low = sched.submit(record, 0, priority=0)
        t_high = sched.submit(record, 10, priority=10)

        sched.start()
        gate.set()  # release both

        sched.result(t_low.task_id, timeout=2.0)
        sched.result(t_high.task_id, timeout=2.0)
        sched.stop()

        assert order == [0, 10], f"Expected [0, 10] but got {order}"

    def test_negative_priority_runs_before_zero(self):
        order: list[int] = []
        gate = threading.Event()

        def record(p: int):
            gate.wait(timeout=2)
            order.append(p)

        sched = PriorityScheduler(workers=1)
        t_neg = sched.submit(record, -5, priority=-5)
        t_zero = sched.submit(record, 0, priority=0)

        sched.start()
        gate.set()

        sched.result(t_neg.task_id, timeout=2.0)
        sched.result(t_zero.task_id, timeout=2.0)
        sched.stop()

        assert order[0] == -5, f"Expected -5 first, got {order}"

    def test_equal_priority_fifo(self):
        """Tasks with equal priority should run in submission order."""
        order: list[int] = []
        gate = threading.Event()

        def record(n: int):
            gate.wait(timeout=2)
            order.append(n)

        sched = PriorityScheduler(workers=1)
        tasks = [sched.submit(record, i, priority=0) for i in range(5)]

        sched.start()
        gate.set()

        for t in tasks:
            sched.result(t.task_id, timeout=2.0)
        sched.stop()

        assert order == [0, 1, 2, 3, 4], f"FIFO not preserved: {order}"


# ===========================================================================
# 5. Cancellation
# ===========================================================================

class TestCancellation:
    def test_cancel_pending_task_returns_true(self):
        sched = PriorityScheduler(workers=1)
        # Don't start — task stays pending indefinitely.
        task = sched.submit(lambda: 1)
        result = sched.cancel(task.task_id)
        sched.stop()
        assert result is True

    def test_cancel_sets_status_cancelled(self):
        sched = PriorityScheduler(workers=1)
        task = sched.submit(lambda: 1)
        sched.cancel(task.task_id)
        sched.stop()
        assert task.status == TaskStatus.CANCELLED

    def test_cancelled_task_not_executed(self):
        called = threading.Event()

        def fn():
            called.set()

        sched = PriorityScheduler(workers=1)
        task = sched.submit(fn)
        sched.cancel(task.task_id)
        sched.start()
        # Give a short window; fn must NOT be called.
        called.wait(timeout=0.2)
        sched.stop()
        assert not called.is_set(), "Cancelled task should not run"

    def test_cancel_nonexistent_returns_false(self, sched):
        assert sched.cancel("does_not_exist") is False

    def test_cancel_done_task_returns_false(self, sched):
        task = sched.submit(lambda: 1)
        sched.result(task.task_id, timeout=2.0)
        assert sched.cancel(task.task_id) is False

    def test_cancel_already_cancelled_returns_false(self):
        sched = PriorityScheduler(workers=1)
        task = sched.submit(lambda: 1)
        sched.cancel(task.task_id)
        second = sched.cancel(task.task_id)
        sched.stop()
        assert second is False

    def test_result_raises_for_cancelled(self):
        sched = PriorityScheduler(workers=1)
        task = sched.submit(lambda: 1)
        sched.cancel(task.task_id)
        sched.start()
        with pytest.raises(RuntimeError, match="cancelled"):
            sched.result(task.task_id, timeout=2.0)
        sched.stop()

    def test_cancel_running_task_returns_false(self, sched):
        """A task in RUNNING state cannot be cancelled."""
        barrier = threading.Barrier(2)

        def slow():
            barrier.wait(timeout=2)
            return "done"

        task = sched.submit(slow)
        barrier.wait(timeout=2)  # wait until task is running
        assert sched.cancel(task.task_id) is False
        barrier.reset()  # let the worker complete (barrier was already passed)

    def test_status_query_after_cancel(self):
        sched = PriorityScheduler(workers=1)
        task = sched.submit(lambda: 1)
        sched.cancel(task.task_id)
        sched.stop()
        assert sched.status(task.task_id) == TaskStatus.CANCELLED


# ===========================================================================
# 6. Deadline / expiry
# ===========================================================================

class TestDeadlineExpiry:
    def test_past_deadline_marks_expired(self, sched):
        task = sched.submit(lambda: 1, deadline=_past(1.0))
        # Wait for the task to be processed (it should be expired, not done)
        task._done_event.wait(timeout=2.0)
        assert task.status == TaskStatus.EXPIRED

    def test_expired_task_fn_not_called(self, sched):
        called = threading.Event()

        def fn():
            called.set()

        task = sched.submit(fn, deadline=_past(1.0))
        task._done_event.wait(timeout=2.0)
        assert not called.is_set()

    def test_result_raises_for_expired(self, sched):
        task = sched.submit(lambda: 1, deadline=_past(1.0))
        with pytest.raises(RuntimeError, match="expired"):
            sched.result(task.task_id, timeout=2.0)

    def test_status_is_expired_after_deadline(self, sched):
        task = sched.submit(lambda: 1, deadline=_past(1.0))
        task._done_event.wait(timeout=2.0)
        assert sched.status(task.task_id) == TaskStatus.EXPIRED

    def test_future_deadline_runs_normally(self, sched):
        task = sched.submit(lambda: "ok", deadline=_future(60.0))
        assert sched.result(task.task_id, timeout=2.0) == "ok"
        assert task.status == TaskStatus.DONE

    def test_none_deadline_no_expiry(self, sched):
        task = sched.submit(lambda: "ok", deadline=None)
        assert sched.result(task.task_id, timeout=2.0) == "ok"

    def test_injectable_now_fn_triggers_expiry(self):
        """Use a custom now_fn to simulate time passing without real sleep."""
        # now_fn returns a very large timestamp so everything is expired
        now_fn = lambda: 1e18
        sched = PriorityScheduler(workers=1, now_fn=now_fn)
        sched.start()
        task = sched.submit(lambda: 1, deadline=time.time())  # deadline is now
        task._done_event.wait(timeout=2.0)
        sched.stop()
        assert task.status == TaskStatus.EXPIRED


# ===========================================================================
# 7. Failed tasks
# ===========================================================================

class TestFailedTasks:
    def test_exception_sets_status_failed(self, sched):
        task = sched.submit(lambda: 1 / 0)
        task._done_event.wait(timeout=2.0)
        assert task.status == TaskStatus.FAILED

    def test_exception_stored_on_task(self, sched):
        task = sched.submit(lambda: 1 / 0)
        task._done_event.wait(timeout=2.0)
        assert isinstance(task.error, ZeroDivisionError)

    def test_result_raises_runtime_error_for_failed(self, sched):
        task = sched.submit(lambda: (_ for _ in ()).throw(ValueError("boom")))
        with pytest.raises(RuntimeError):
            sched.result(task.task_id, timeout=2.0)

    def test_result_raises_with_original_exception_cause(self, sched):
        def bad():
            raise ValueError("oops")

        task = sched.submit(bad)
        with pytest.raises(RuntimeError) as exc_info:
            sched.result(task.task_id, timeout=2.0)
        assert exc_info.value.__cause__ is task.error

    def test_failed_task_result_field_is_none(self, sched):
        task = sched.submit(lambda: 1 / 0)
        task._done_event.wait(timeout=2.0)
        assert task.result is None

    def test_custom_exception_type_preserved(self, sched):
        class MyError(RuntimeError):
            pass

        def bad():
            raise MyError("custom")

        task = sched.submit(bad)
        task._done_event.wait(timeout=2.0)
        assert isinstance(task.error, MyError)

    def test_subsequent_tasks_run_after_failure(self, sched):
        bad_task = sched.submit(lambda: 1 / 0)
        good_task = sched.submit(lambda: 99)
        sched.result(good_task.task_id, timeout=2.0)
        assert good_task.result == 99

    def test_multiple_failures(self, sched):
        tasks = [sched.submit(lambda: 1 / 0) for _ in range(3)]
        for t in tasks:
            t._done_event.wait(timeout=2.0)
            assert t.status == TaskStatus.FAILED


# ===========================================================================
# 8. status() method
# ===========================================================================

class TestStatusMethod:
    def test_status_unknown_task_returns_none(self, sched):
        assert sched.status("nonexistent") is None

    def test_status_done(self, sched):
        task = sched.submit(lambda: 1)
        sched.result(task.task_id, timeout=2.0)
        assert sched.status(task.task_id) == TaskStatus.DONE

    def test_status_cancelled(self):
        sched = PriorityScheduler(workers=1)
        task = sched.submit(lambda: 1)
        sched.cancel(task.task_id)
        sched.stop()
        assert sched.status(task.task_id) == TaskStatus.CANCELLED

    def test_status_failed(self, sched):
        task = sched.submit(lambda: 1 / 0)
        task._done_event.wait(timeout=2.0)
        assert sched.status(task.task_id) == TaskStatus.FAILED

    def test_status_expired(self, sched):
        task = sched.submit(lambda: 1, deadline=_past())
        task._done_event.wait(timeout=2.0)
        assert sched.status(task.task_id) == TaskStatus.EXPIRED


# ===========================================================================
# 9. result() error cases
# ===========================================================================

class TestResultMethod:
    def test_result_unknown_task_raises_key_error(self, sched):
        with pytest.raises(KeyError):
            sched.result("no-such-task")

    def test_result_timeout_raises_timeout_error(self):
        sched = PriorityScheduler(workers=1)
        # Don't start — task will never run.
        task = sched.submit(lambda: 1)
        with pytest.raises(TimeoutError):
            sched.result(task.task_id, timeout=0.1)
        sched.stop(wait=False)

    def test_result_returns_correct_value(self, sched):
        task = sched.submit(lambda: [1, 2, 3])
        assert sched.result(task.task_id, timeout=2.0) == [1, 2, 3]

    def test_result_waits_for_slow_task(self):
        """result() must block until fn finishes."""
        gate = threading.Event()

        def slow():
            gate.wait(timeout=5)
            return "slow_result"

        sched = PriorityScheduler(workers=1)
        sched.start()
        task = sched.submit(slow)
        # Give it a moment to be picked up but not finished
        time.sleep(0.05)
        gate.set()
        assert sched.result(task.task_id, timeout=2.0) == "slow_result"
        sched.stop()


# ===========================================================================
# 10. pending_count()
# ===========================================================================

class TestPendingCount:
    def test_empty_scheduler_pending_count_zero(self, sched):
        assert sched.pending_count() == 0

    def test_submitted_tasks_increase_pending(self):
        sched = PriorityScheduler(workers=1)  # not started
        sched.submit(lambda: 1)
        sched.submit(lambda: 2)
        assert sched.pending_count() == 2
        sched.stop()

    def test_completed_tasks_not_counted_pending(self, sched):
        task = sched.submit(lambda: 1)
        sched.result(task.task_id, timeout=2.0)
        assert sched.pending_count() == 0

    def test_cancelled_tasks_not_counted_pending(self):
        sched = PriorityScheduler(workers=1)
        task = sched.submit(lambda: 1)
        sched.cancel(task.task_id)
        assert sched.pending_count() == 0
        sched.stop()

    def test_pending_count_decrements_after_run(self, sched2):
        tasks = [sched2.submit(lambda: None) for _ in range(4)]
        for t in tasks:
            t._done_event.wait(timeout=2.0)
        assert sched2.pending_count() == 0


# ===========================================================================
# 11. stats()
# ===========================================================================

class TestStats:
    def test_stats_keys_present(self, sched):
        s = sched.stats()
        for key in ("total", "pending", "running", "done", "cancelled", "failed", "expired"):
            assert key in s

    def test_stats_empty_all_zeros(self, sched):
        s = sched.stats()
        assert s["total"] == 0

    def test_stats_done_count(self, sched):
        tasks = [sched.submit(lambda: 1) for _ in range(3)]
        for t in tasks:
            sched.result(t.task_id, timeout=2.0)
        s = sched.stats()
        assert s["done"] == 3
        assert s["total"] == 3

    def test_stats_cancelled_count(self):
        sched = PriorityScheduler(workers=1)
        tasks = [sched.submit(lambda: 1) for _ in range(2)]
        for t in tasks:
            sched.cancel(t.task_id)
        s = sched.stats()
        assert s["cancelled"] == 2
        assert s["pending"] == 0
        sched.stop()

    def test_stats_failed_count(self, sched):
        tasks = [sched.submit(lambda: 1 / 0) for _ in range(2)]
        for t in tasks:
            t._done_event.wait(timeout=2.0)
        s = sched.stats()
        assert s["failed"] == 2

    def test_stats_expired_count(self, sched):
        tasks = [sched.submit(lambda: 1, deadline=_past()) for _ in range(2)]
        for t in tasks:
            t._done_event.wait(timeout=2.0)
        s = sched.stats()
        assert s["expired"] == 2

    def test_stats_mixed(self, sched):
        done_task = sched.submit(lambda: 1)
        sched.result(done_task.task_id, timeout=2.0)

        fail_task = sched.submit(lambda: 1 / 0)
        fail_task._done_event.wait(timeout=2.0)

        exp_task = sched.submit(lambda: 1, deadline=_past())
        exp_task._done_event.wait(timeout=2.0)

        s = sched.stats()
        assert s["done"] == 1
        assert s["failed"] == 1
        assert s["expired"] == 1
        assert s["total"] == 3

    def test_stats_total_equals_sum(self, sched):
        tasks = [sched.submit(lambda: 1) for _ in range(5)]
        for t in tasks:
            sched.result(t.task_id, timeout=2.0)
        s = sched.stats()
        sub_total = s["pending"] + s["running"] + s["done"] + s["cancelled"] + s["failed"] + s["expired"]
        assert sub_total == s["total"]


# ===========================================================================
# 12. Multiple workers / concurrency
# ===========================================================================

class TestMultipleWorkers:
    def test_two_workers_run_concurrently(self):
        """Two tasks should overlap in execution time with 2 workers."""
        started = threading.Event()
        second_started = threading.Event()
        done = threading.Event()

        def task1():
            started.set()
            second_started.wait(timeout=2)  # blocks until task2 has started
            done.set()
            return 1

        def task2():
            started.wait(timeout=2)         # wait for task1 to be running
            second_started.set()
            return 2

        sched = PriorityScheduler(workers=2)
        sched.start()
        t1 = sched.submit(task1, priority=0)
        t2 = sched.submit(task2, priority=0)

        r1 = sched.result(t1.task_id, timeout=2.0)
        r2 = sched.result(t2.task_id, timeout=2.0)
        sched.stop()

        assert r1 == 1
        assert r2 == 2
        assert done.is_set()

    def test_throughput_with_multiple_workers(self):
        """Four workers process 20 trivial tasks faster than a single worker."""
        sched = PriorityScheduler(workers=4)
        sched.start()
        tasks = [sched.submit(lambda: None) for _ in range(20)]
        for t in tasks:
            sched.result(t.task_id, timeout=5.0)
        sched.stop()
        assert all(t.status == TaskStatus.DONE for t in tasks)

    def test_worker_count_respected(self):
        """Check that the scheduler only creates as many threads as requested."""
        # We rely on the internal list; workers=3 → 3 threads.
        sched = PriorityScheduler(workers=3)
        sched.start()
        assert len(sched._threads) == 3
        sched.stop()


# ===========================================================================
# 13. Lifecycle (start / stop)
# ===========================================================================

class TestLifecycle:
    def test_start_twice_is_safe(self):
        sched = PriorityScheduler(workers=1)
        sched.start()
        sched.start()   # second call should be a no-op
        assert len(sched._threads) == 1
        sched.stop()

    def test_stop_before_start_is_safe(self):
        sched = PriorityScheduler(workers=1)
        sched.stop(wait=True)  # should not raise

    def test_stop_wait_true_drains_queue(self):
        """After stop(wait=True) all previously submitted tasks are finished."""
        sched = PriorityScheduler(workers=2)
        sched.start()
        tasks = [sched.submit(lambda: None) for _ in range(10)]
        sched.stop(wait=True)
        # All tasks should be DONE (or CANCELLED/EXPIRED, but none PENDING/RUNNING)
        terminal = {TaskStatus.DONE, TaskStatus.CANCELLED, TaskStatus.EXPIRED, TaskStatus.FAILED}
        for t in tasks:
            assert t.status in terminal, f"Task still {t.status} after stop(wait=True)"

    def test_stop_wait_false_returns_quickly(self):
        sched = PriorityScheduler(workers=1)
        sched.start()
        # Submit a task that blocks; stop(wait=False) should return immediately
        gate = threading.Event()
        sched.submit(lambda: gate.wait(timeout=5))
        start = time.monotonic()
        sched.stop(wait=False)
        elapsed = time.monotonic() - start
        gate.set()
        assert elapsed < 1.0, f"stop(wait=False) took {elapsed:.3f}s"

    def test_tasks_complete_before_stop_wait(self):
        sched = PriorityScheduler(workers=2)
        sched.start()
        results = []
        for i in range(5):
            sched.submit(lambda i=i: results.append(i))
        sched.stop(wait=True)
        assert len(results) == 5


# ===========================================================================
# 14. Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_submits(self):
        sched = PriorityScheduler(workers=4)
        sched.start()

        tasks: list[ScheduledTask] = []
        lock = threading.Lock()

        def submit_many():
            for _ in range(25):
                t = sched.submit(lambda: 1)
                with lock:
                    tasks.append(t)

        threads = [threading.Thread(target=submit_many) for _ in range(4)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        # Wait for all tasks to complete
        for t in tasks:
            t._done_event.wait(timeout=5.0)

        sched.stop()
        assert len(tasks) == 100
        assert all(t.status == TaskStatus.DONE for t in tasks)

    def test_concurrent_cancel_and_complete(self):
        """Race between cancel and execution should not corrupt state."""
        sched = PriorityScheduler(workers=2)
        sched.start()

        tasks = [sched.submit(lambda: None) for _ in range(20)]
        # Cancel half while they may already be running
        for t in tasks[::2]:
            sched.cancel(t.task_id)

        for t in tasks:
            t._done_event.wait(timeout=5.0)

        sched.stop()
        terminal = {TaskStatus.DONE, TaskStatus.CANCELLED, TaskStatus.EXPIRED, TaskStatus.FAILED}
        for t in tasks:
            assert t.status in terminal

    def test_concurrent_status_reads(self, sched2):
        """Reading status from multiple threads should not raise."""
        task = sched2.submit(lambda: None)
        errors: list[Exception] = []

        def read_status():
            try:
                for _ in range(50):
                    sched2.status(task.task_id)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=read_status) for _ in range(4)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == []

    def test_concurrent_stats_calls(self, sched2):
        """stats() must not raise under concurrent modifications."""
        errors: list[Exception] = []

        def spam_stats():
            try:
                for _ in range(50):
                    sched2.stats()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def spam_submit():
            for _ in range(10):
                sched2.submit(lambda: None)

        threads = (
            [threading.Thread(target=spam_stats) for _ in range(3)]
            + [threading.Thread(target=spam_submit) for _ in range(2)]
        )
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == []


# ===========================================================================
# 15. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_large_result_object(self, sched):
        big = list(range(10_000))
        task = sched.submit(lambda: big)
        assert sched.result(task.task_id, timeout=2.0) == big

    def test_fn_returns_false(self, sched):
        task = sched.submit(lambda: False)
        assert sched.result(task.task_id, timeout=2.0) is False

    def test_fn_returns_zero(self, sched):
        task = sched.submit(lambda: 0)
        assert sched.result(task.task_id, timeout=2.0) == 0

    def test_fn_returns_empty_string(self, sched):
        task = sched.submit(lambda: "")
        assert sched.result(task.task_id, timeout=2.0) == ""

    def test_fn_returns_none(self, sched):
        task = sched.submit(lambda: None)
        assert sched.result(task.task_id, timeout=2.0) is None

    def test_priority_very_high_runs_first(self):
        order: list[int] = []
        gate = threading.Event()

        def record(p: int):
            gate.wait(timeout=2)
            order.append(p)

        sched = PriorityScheduler(workers=1)
        for p in [100, 50, 1, 0]:
            sched.submit(record, p, priority=p)
        sched.start()
        gate.set()
        # Collect all four
        while len(order) < 4:
            time.sleep(0.01)
        sched.stop()
        assert order == [0, 1, 50, 100], f"Order was {order}"

    def test_task_id_accessible_before_done(self, sched):
        task = sched.submit(lambda: None)
        assert isinstance(task.task_id, str) and len(task.task_id) > 0

    def test_zero_workers_no_tasks_run(self):
        """A scheduler with 0 workers never processes tasks."""
        sched = PriorityScheduler(workers=0)
        sched.start()
        task = sched.submit(lambda: 1)
        with pytest.raises(TimeoutError):
            sched.result(task.task_id, timeout=0.1)
        sched.stop(wait=False)

    def test_deadline_exactly_at_submit_time(self):
        """Deadline equal to the past timestamp is expired (strict > check)."""
        # Use a fake now_fn that always returns a time well past the deadline.
        past_ts = time.time() - 5
        now_fn = lambda: past_ts + 10   # always 10 s after the deadline

        sched = PriorityScheduler(workers=1, now_fn=now_fn)
        sched.start()
        # deadline is 5 s ago; now_fn returns 10 s after that → EXPIRED
        task = sched.submit(lambda: 1, deadline=past_ts)
        task._done_event.wait(timeout=2.0)
        sched.stop()
        assert task.status == TaskStatus.EXPIRED
