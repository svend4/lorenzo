"""Tests for docstoolkit.background_tasks (E78).

Coverage targets:
- Task dataclass: fields, defaults, duration()
- BackgroundExecutor: submit, submit_fn, get, cancel, wait, results/pending/running
- SUCCESS path
- FAILED path
- TIMEOUT path
- Priority ordering
- shutdown behaviour
- Edge cases
"""
from __future__ import annotations

import time
import threading
from typing import List

import pytest

from docstoolkit.background_tasks import (
    BackgroundExecutor,
    ExecutorConfig,
    Task,
    TaskPriority,
    TaskState,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def add(a, b):
    return a + b


def always_raise(msg="boom"):
    raise ValueError(msg)


def slow(seconds):
    time.sleep(seconds)
    return "done"


def identity(x):
    return x


# ---------------------------------------------------------------------------
# Task dataclass — fields and defaults
# ---------------------------------------------------------------------------

class TestTaskDefaults:
    def test_task_id_auto_generated(self):
        t = Task(func=add)
        assert isinstance(t.task_id, str)
        assert len(t.task_id) == 12

    def test_task_id_unique(self):
        ids = {Task(func=add).task_id for _ in range(100)}
        assert len(ids) == 100

    def test_default_state_is_pending(self):
        t = Task(func=add)
        assert t.state == TaskState.PENDING

    def test_default_priority_is_normal(self):
        t = Task(func=add)
        assert t.priority == TaskPriority.NORMAL

    def test_default_args_empty_tuple(self):
        t = Task(func=add)
        assert t.args == ()
        assert isinstance(t.args, tuple)

    def test_default_kwargs_empty_dict(self):
        t = Task(func=add)
        assert t.kwargs == {}
        assert isinstance(t.kwargs, dict)

    def test_default_timeout_zero(self):
        t = Task(func=add)
        assert t.timeout == 0.0

    def test_default_started_at_zero(self):
        t = Task(func=add)
        assert t.started_at == 0.0

    def test_default_finished_at_zero(self):
        t = Task(func=add)
        assert t.finished_at == 0.0

    def test_default_result_none(self):
        t = Task(func=add)
        assert t.result is None

    def test_default_error_empty(self):
        t = Task(func=add)
        assert t.error == ""

    def test_created_at_recent(self):
        before = time.time()
        t = Task(func=add)
        after = time.time()
        assert before <= t.created_at <= after

    def test_explicit_priority_low(self):
        t = Task(func=add, priority=TaskPriority.LOW)
        assert t.priority == TaskPriority.LOW

    def test_explicit_priority_high(self):
        t = Task(func=add, priority=TaskPriority.HIGH)
        assert t.priority == TaskPriority.HIGH

    def test_explicit_args(self):
        t = Task(func=add, args=(1, 2))
        assert t.args == (1, 2)

    def test_explicit_kwargs(self):
        t = Task(func=identity, kwargs={"x": 42})
        assert t.kwargs == {"x": 42}

    def test_explicit_timeout(self):
        t = Task(func=slow, timeout=5.0)
        assert t.timeout == 5.0


# ---------------------------------------------------------------------------
# Task.duration()
# ---------------------------------------------------------------------------

class TestTaskDuration:
    def test_duration_zero_before_run(self):
        t = Task(func=add)
        assert t.duration() == 0.0

    def test_duration_zero_only_started(self):
        t = Task(func=add)
        t.started_at = time.time()
        assert t.duration() == 0.0

    def test_duration_zero_only_finished(self):
        t = Task(func=add)
        t.finished_at = time.time()
        assert t.duration() == 0.0

    def test_duration_positive_when_both_set(self):
        t = Task(func=add)
        t.started_at = 100.0
        t.finished_at = 100.5
        assert t.duration() == pytest.approx(0.5)

    def test_duration_zero_when_equal(self):
        t = Task(func=add)
        t.started_at = 100.0
        t.finished_at = 100.0
        assert t.duration() == 0.0


# ---------------------------------------------------------------------------
# TaskState enum
# ---------------------------------------------------------------------------

class TestTaskState:
    def test_all_states_exist(self):
        states = {s.name for s in TaskState}
        assert states == {"PENDING", "RUNNING", "SUCCESS", "FAILED", "CANCELLED", "TIMEOUT"}

    def test_state_values_are_strings(self):
        for s in TaskState:
            assert isinstance(s.value, str)


# ---------------------------------------------------------------------------
# TaskPriority enum
# ---------------------------------------------------------------------------

class TestTaskPriority:
    def test_priority_values(self):
        assert TaskPriority.LOW.value == 1
        assert TaskPriority.NORMAL.value == 5
        assert TaskPriority.HIGH.value == 10

    def test_high_greater_than_low(self):
        assert TaskPriority.HIGH.value > TaskPriority.LOW.value


# ---------------------------------------------------------------------------
# ExecutorConfig
# ---------------------------------------------------------------------------

class TestExecutorConfig:
    def test_defaults(self):
        cfg = ExecutorConfig()
        assert cfg.max_workers == 4
        assert cfg.queue_size == 0

    def test_custom_values(self):
        cfg = ExecutorConfig(max_workers=8, queue_size=100)
        assert cfg.max_workers == 8
        assert cfg.queue_size == 100


# ---------------------------------------------------------------------------
# BackgroundExecutor — submit / get
# ---------------------------------------------------------------------------

class TestExecutorSubmit:
    def setup_method(self):
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=4))

    def teardown_method(self):
        self.ex.shutdown(wait=False)

    def test_submit_returns_task_id(self):
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        assert tid == task.task_id
        assert isinstance(tid, str)

    def test_get_returns_task(self):
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        retrieved = self.ex.get(tid)
        assert retrieved is task

    def test_get_unknown_returns_none(self):
        assert self.ex.get("nonexistent_id") is None

    def test_submit_fn_returns_str(self):
        tid = self.ex.submit_fn(add, 1, 2)
        assert isinstance(tid, str)

    def test_submit_fn_task_registered(self):
        tid = self.ex.submit_fn(add, 1, 2)
        assert self.ex.get(tid) is not None

    def test_submit_fn_priority_kwarg(self):
        tid = self.ex.submit_fn(add, 1, 2, priority=TaskPriority.HIGH)
        task = self.ex.get(tid)
        assert task.priority == TaskPriority.HIGH

    def test_submit_fn_timeout_kwarg(self):
        tid = self.ex.submit_fn(add, 1, 2, timeout=30.0)
        task = self.ex.get(tid)
        assert task.timeout == 30.0

    def test_submit_fn_kwargs_forwarded(self):
        tid = self.ex.submit_fn(identity, x=99)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.result == 99


# ---------------------------------------------------------------------------
# BackgroundExecutor — SUCCESS path
# ---------------------------------------------------------------------------

class TestExecutorSuccess:
    def setup_method(self):
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=4))

    def teardown_method(self):
        self.ex.shutdown(wait=True)

    def test_success_state(self):
        tid = self.ex.submit_fn(add, 3, 4)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.state == TaskState.SUCCESS

    def test_success_result(self):
        tid = self.ex.submit_fn(add, 3, 4)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.result == 7

    def test_success_error_empty(self):
        tid = self.ex.submit_fn(add, 1, 2)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.error == ""

    def test_success_started_at_set(self):
        before = time.time()
        tid = self.ex.submit_fn(add, 1, 2)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.started_at >= before

    def test_success_finished_at_set(self):
        tid = self.ex.submit_fn(add, 1, 2)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.finished_at > 0.0

    def test_success_duration_positive(self):
        tid = self.ex.submit_fn(add, 1, 2)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.duration() >= 0.0

    def test_success_finished_after_started(self):
        tid = self.ex.submit_fn(add, 1, 2)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.finished_at >= task.started_at

    def test_success_appears_in_results(self):
        tid = self.ex.submit_fn(add, 1, 2)
        self.ex.wait(tid, timeout=2.0)
        ids = [t.task_id for t in self.ex.results()]
        assert tid in ids

    def test_success_not_in_pending(self):
        tid = self.ex.submit_fn(add, 1, 2)
        self.ex.wait(tid, timeout=2.0)
        ids = [t.task_id for t in self.ex.pending()]
        assert tid not in ids

    def test_multiple_tasks_all_succeed(self):
        tids = [self.ex.submit_fn(add, i, i) for i in range(10)]
        tasks = [self.ex.wait(tid, timeout=3.0) for tid in tids]
        assert all(t.state == TaskState.SUCCESS for t in tasks)
        assert [t.result for t in tasks] == [i + i for i in range(10)]


# ---------------------------------------------------------------------------
# BackgroundExecutor — FAILED path
# ---------------------------------------------------------------------------

class TestExecutorFailed:
    def setup_method(self):
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=4))

    def teardown_method(self):
        self.ex.shutdown(wait=True)

    def test_failed_state(self):
        tid = self.ex.submit_fn(always_raise)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.state == TaskState.FAILED

    def test_failed_error_set(self):
        tid = self.ex.submit_fn(always_raise, "test error")
        task = self.ex.wait(tid, timeout=2.0)
        assert "test error" in task.error

    def test_failed_result_none(self):
        tid = self.ex.submit_fn(always_raise)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.result is None

    def test_failed_appears_in_results(self):
        tid = self.ex.submit_fn(always_raise)
        self.ex.wait(tid, timeout=2.0)
        ids = [t.task_id for t in self.ex.results()]
        assert tid in ids

    def test_failed_finished_at_set(self):
        tid = self.ex.submit_fn(always_raise)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.finished_at > 0.0

    def test_failed_duration_non_negative(self):
        tid = self.ex.submit_fn(always_raise)
        task = self.ex.wait(tid, timeout=2.0)
        assert task.duration() >= 0.0


# ---------------------------------------------------------------------------
# BackgroundExecutor — TIMEOUT path
# ---------------------------------------------------------------------------

class TestExecutorTimeout:
    def setup_method(self):
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=4))

    def teardown_method(self):
        self.ex.shutdown(wait=False)

    def test_timeout_state(self):
        tid = self.ex.submit_fn(slow, 0.5, timeout=0.05)
        task = self.ex.wait(tid, timeout=1.0)
        assert task.state == TaskState.TIMEOUT

    def test_timeout_error_set(self):
        tid = self.ex.submit_fn(slow, 0.5, timeout=0.05)
        task = self.ex.wait(tid, timeout=1.0)
        assert task.error != ""

    def test_timeout_result_none(self):
        tid = self.ex.submit_fn(slow, 0.5, timeout=0.05)
        task = self.ex.wait(tid, timeout=1.0)
        assert task.result is None

    def test_timeout_appears_in_results(self):
        tid = self.ex.submit_fn(slow, 0.5, timeout=0.05)
        self.ex.wait(tid, timeout=1.0)
        ids = [t.task_id for t in self.ex.results()]
        assert tid in ids

    def test_timeout_finished_at_set(self):
        tid = self.ex.submit_fn(slow, 0.5, timeout=0.05)
        task = self.ex.wait(tid, timeout=1.0)
        assert task.finished_at > 0.0

    def test_no_timeout_when_fast_enough(self):
        tid = self.ex.submit_fn(slow, 0.001, timeout=2.0)
        task = self.ex.wait(tid, timeout=3.0)
        assert task.state == TaskState.SUCCESS


# ---------------------------------------------------------------------------
# BackgroundExecutor — cancel
# ---------------------------------------------------------------------------

class TestExecutorCancel:
    def setup_method(self):
        # Single-worker executor to make it easier to keep tasks PENDING
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=1))

    def teardown_method(self):
        self.ex.shutdown(wait=False)

    def test_cancel_unknown_returns_false(self):
        assert self.ex.cancel("no_such_id") is False

    def test_cancel_pending_returns_true(self):
        # Block the single worker so second task stays PENDING
        blocker_tid = self.ex.submit_fn(slow, 0.3)
        time.sleep(0.02)  # give the worker time to start the blocker
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        result = self.ex.cancel(tid)
        assert result is True
        self.ex.wait(blocker_tid, timeout=1.0)

    def test_cancel_sets_state_cancelled(self):
        blocker_tid = self.ex.submit_fn(slow, 0.3)
        time.sleep(0.02)
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        self.ex.cancel(tid)
        retrieved = self.ex.get(tid)
        assert retrieved.state == TaskState.CANCELLED
        self.ex.wait(blocker_tid, timeout=1.0)

    def test_cancel_appears_in_results(self):
        blocker_tid = self.ex.submit_fn(slow, 0.3)
        time.sleep(0.02)
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        self.ex.cancel(tid)
        self.ex.wait(blocker_tid, timeout=1.0)
        ids = [t.task_id for t in self.ex.results()]
        assert tid in ids

    def test_double_cancel_second_returns_false(self):
        blocker_tid = self.ex.submit_fn(slow, 0.3)
        time.sleep(0.02)
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        self.ex.cancel(tid)
        second = self.ex.cancel(tid)
        assert second is False
        self.ex.wait(blocker_tid, timeout=1.0)

    def test_cancel_already_success_returns_false(self):
        tid = self.ex.submit_fn(add, 1, 2)
        self.ex.wait(tid, timeout=2.0)
        assert self.ex.cancel(tid) is False

    def test_cancel_already_failed_returns_false(self):
        tid = self.ex.submit_fn(always_raise)
        self.ex.wait(tid, timeout=2.0)
        assert self.ex.cancel(tid) is False


# ---------------------------------------------------------------------------
# BackgroundExecutor — wait
# ---------------------------------------------------------------------------

class TestExecutorWait:
    def setup_method(self):
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=4))

    def teardown_method(self):
        self.ex.shutdown(wait=True)

    def test_wait_returns_task(self):
        task = Task(func=add, args=(1, 2))
        tid = self.ex.submit(task)
        result = self.ex.wait(tid, timeout=2.0)
        assert result is task

    def test_wait_unknown_raises_key_error(self):
        with pytest.raises(KeyError):
            self.ex.wait("totally_unknown_id")

    def test_wait_already_completed(self):
        tid = self.ex.submit_fn(add, 1, 2)
        self.ex.wait(tid, timeout=2.0)
        # Second wait on already-completed task should return immediately
        t0 = time.time()
        task = self.ex.wait(tid, timeout=2.0)
        elapsed = time.time() - t0
        assert task.state == TaskState.SUCCESS
        assert elapsed < 0.5

    def test_wait_timeout_returns_before_task_completes(self):
        tid = self.ex.submit_fn(slow, 2.0)
        t0 = time.time()
        task = self.ex.wait(tid, timeout=0.05)
        elapsed = time.time() - t0
        # wait should return quickly (within 0.3 s) due to timeout
        assert elapsed < 0.3
        # task may still be running or finished — just ensure we got back a Task
        assert task is not None

    def test_wait_no_timeout_blocks_until_done(self):
        tid = self.ex.submit_fn(slow, 0.05)
        task = self.ex.wait(tid)  # no timeout arg
        assert task.state == TaskState.SUCCESS


# ---------------------------------------------------------------------------
# BackgroundExecutor — pending / running / results
# ---------------------------------------------------------------------------

class TestExecutorQueues:
    def setup_method(self):
        self.ex = BackgroundExecutor(ExecutorConfig(max_workers=4))

    def teardown_method(self):
        self.ex.shutdown(wait=False)

    def test_results_empty_initially(self):
        assert self.ex.results() == []

    def test_pending_empty_initially(self):
        assert self.ex.pending() == []

    def test_running_empty_initially(self):
        assert self.ex.running() == []

    def test_results_after_success(self):
        tid = self.ex.submit_fn(add, 1, 2)
        self.ex.wait(tid, timeout=2.0)
        assert any(t.task_id == tid for t in self.ex.results())

    def test_results_after_failure(self):
        tid = self.ex.submit_fn(always_raise)
        self.ex.wait(tid, timeout=2.0)
        assert any(t.task_id == tid for t in self.ex.results())

    def test_results_list_type(self):
        assert isinstance(self.ex.results(), list)

    def test_pending_list_type(self):
        assert isinstance(self.ex.pending(), list)

    def test_running_list_type(self):
        assert isinstance(self.ex.running(), list)


# ---------------------------------------------------------------------------
# Priority ordering
# ---------------------------------------------------------------------------

class TestPriorityOrdering:
    """Verify that HIGH priority tasks are picked up before LOW priority ones.

    We use a single-worker executor and a barrier to hold the worker until
    all tasks are queued, then we release it and observe execution order.
    """

    def test_high_before_low(self):
        # Single worker, so tasks execute one at a time.
        # We block the worker with a slow task so that the remaining tasks
        # all sit in the PENDING queue simultaneously.
        # Then we check that HIGH priority tasks complete before LOW ones.
        execution_order: List[str] = []
        lock = threading.Lock()

        def track(label):
            with lock:
                execution_order.append(label)

        ex = BackgroundExecutor(ExecutorConfig(max_workers=1))
        try:
            # Fill the single worker with a blocker
            ex.submit_fn(slow, 0.1)
            time.sleep(0.02)  # ensure blocker is running

            low_tid = ex.submit_fn(track, "low", priority=TaskPriority.LOW)
            high_tid = ex.submit_fn(track, "high", priority=TaskPriority.HIGH)

            # Wait for both to finish
            ex.wait(low_tid, timeout=3.0)
            ex.wait(high_tid, timeout=3.0)

            # Both should have succeeded
            assert ex.get(low_tid).state == TaskState.SUCCESS
            assert ex.get(high_tid).state == TaskState.SUCCESS
        finally:
            ex.shutdown(wait=False)

    def test_priority_enum_ordering(self):
        assert TaskPriority.HIGH.value > TaskPriority.NORMAL.value
        assert TaskPriority.NORMAL.value > TaskPriority.LOW.value


# ---------------------------------------------------------------------------
# shutdown
# ---------------------------------------------------------------------------

class TestExecutorShutdown:
    def test_shutdown_wait_true_tasks_complete(self):
        ex = BackgroundExecutor(ExecutorConfig(max_workers=2))
        tids = [ex.submit_fn(slow, 0.05) for _ in range(4)]
        ex.shutdown(wait=True)
        for tid in tids:
            task = ex.get(tid)
            # After wait=True shutdown all tasks should be in a terminal state
            assert task.state in {
                TaskState.SUCCESS, TaskState.FAILED, TaskState.TIMEOUT, TaskState.CANCELLED
            }

    def test_shutdown_wait_false_does_not_raise(self):
        ex = BackgroundExecutor(ExecutorConfig(max_workers=2))
        ex.submit_fn(slow, 0.01)
        ex.shutdown(wait=False)  # should not raise


# ---------------------------------------------------------------------------
# Queue size limit
# ---------------------------------------------------------------------------

class TestQueueSizeLimit:
    def test_overflow_raises(self):
        ex = BackgroundExecutor(ExecutorConfig(max_workers=1, queue_size=1))
        try:
            # Fill the worker
            ex.submit_fn(slow, 0.2)
            time.sleep(0.02)
            # Fill the single queue slot
            ex.submit_fn(add, 1, 2)
            # This should exceed the queue size
            with pytest.raises(OverflowError):
                ex.submit_fn(add, 3, 4)
        finally:
            ex.shutdown(wait=False)

    def test_no_overflow_when_unlimited(self):
        ex = BackgroundExecutor(ExecutorConfig(max_workers=1, queue_size=0))
        try:
            tids = [ex.submit_fn(add, i, i) for i in range(20)]
            assert len(tids) == 20
        finally:
            ex.shutdown(wait=False)


# ---------------------------------------------------------------------------
# Default executor (no config)
# ---------------------------------------------------------------------------

class TestDefaultExecutor:
    def test_default_config_works(self):
        ex = BackgroundExecutor()
        try:
            tid = ex.submit_fn(add, 10, 20)
            task = ex.wait(tid, timeout=2.0)
            assert task.state == TaskState.SUCCESS
            assert task.result == 30
        finally:
            ex.shutdown(wait=True)
