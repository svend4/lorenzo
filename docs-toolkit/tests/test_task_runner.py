"""Tests for docstoolkit.task_runner — E159."""
from __future__ import annotations

import time

import pytest

from docstoolkit.task_runner import (
    RunResult,
    TaskDef,
    TaskResult,
    TaskRunner,
    TaskStatus,
)


# ---------- helpers ----------
class CallCounter:
    def __init__(self, fail_first_n: int = 0, exc: Exception = None):
        self.fail_first_n = fail_first_n
        self.calls = 0
        self.exc = exc or RuntimeError("boom")

    def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.calls <= self.fail_first_n:
            raise self.exc
        return f"ok-{self.calls}"


def make_now(values):
    """Build a now_fn that returns successive values from a list, then repeats last."""
    seq = list(values)
    state = {"i": 0}

    def now():
        i = state["i"]
        if i < len(seq):
            state["i"] += 1
            return seq[i]
        return seq[-1]

    return now


# ---------- TaskStatus ----------
class TestTaskStatus:
    def test_members_present(self):
        assert TaskStatus.PENDING.name == "PENDING"
        assert TaskStatus.RUNNING.name == "RUNNING"
        assert TaskStatus.SUCCESS.name == "SUCCESS"
        assert TaskStatus.FAILED.name == "FAILED"
        assert TaskStatus.SKIPPED.name == "SKIPPED"
        assert TaskStatus.TIMEOUT.name == "TIMEOUT"

    def test_count(self):
        assert len(list(TaskStatus)) == 6

    def test_distinct(self):
        names = {s.name for s in TaskStatus}
        assert len(names) == 6


# ---------- TaskResult ----------
class TestTaskResult:
    def test_defaults(self):
        r = TaskResult(task_name="x", status=TaskStatus.SUCCESS)
        assert r.task_name == "x"
        assert r.status is TaskStatus.SUCCESS
        assert r.output is None
        assert r.error is None
        assert r.duration == 0.0
        assert r.attempts == 1

    def test_set_all(self):
        r = TaskResult(
            task_name="x",
            status=TaskStatus.FAILED,
            output=42,
            error="bad",
            duration=1.5,
            attempts=3,
        )
        assert r.output == 42
        assert r.error == "bad"
        assert r.duration == 1.5
        assert r.attempts == 3


# ---------- TaskDef ----------
class TestTaskDef:
    def test_minimal(self):
        t = TaskDef(name="a", func=lambda: 1)
        assert t.name == "a"
        assert t.args == ()
        assert t.kwargs == {}
        assert t.timeout is None
        assert t.max_retries == 0
        assert t.skip_on_failure is False
        assert t.condition is None

    def test_kwargs_independent(self):
        t1 = TaskDef(name="a", func=lambda: 1)
        t2 = TaskDef(name="b", func=lambda: 2)
        t1.kwargs["x"] = 9
        assert "x" not in t2.kwargs

    def test_with_args(self):
        t = TaskDef(name="a", func=lambda x, y: x + y, args=(1,), kwargs={"y": 2})
        assert t.args == (1,)
        assert t.kwargs == {"y": 2}


# ---------- RunResult ----------
class TestRunResult:
    def _mk(self, *statuses):
        return RunResult(
            task_results=[
                TaskResult(task_name=f"t{i}", status=s)
                for i, s in enumerate(statuses)
            ],
            total_duration=0.1,
        )

    def test_success_count(self):
        r = self._mk(TaskStatus.SUCCESS, TaskStatus.SUCCESS, TaskStatus.FAILED)
        assert r.success_count == 2

    def test_failure_count_failed_and_timeout(self):
        r = self._mk(
            TaskStatus.FAILED,
            TaskStatus.TIMEOUT,
            TaskStatus.SUCCESS,
            TaskStatus.SKIPPED,
        )
        assert r.failure_count == 2

    def test_all_success_true(self):
        r = self._mk(TaskStatus.SUCCESS, TaskStatus.SUCCESS)
        assert r.all_success is True

    def test_all_success_false(self):
        r = self._mk(TaskStatus.SUCCESS, TaskStatus.FAILED)
        assert r.all_success is False

    def test_all_success_empty(self):
        r = RunResult(task_results=[], total_duration=0.0)
        assert r.all_success is False

    def test_by_name_found(self):
        r = self._mk(TaskStatus.SUCCESS, TaskStatus.FAILED)
        found = r.by_name("t1")
        assert found is not None
        assert found.status is TaskStatus.FAILED

    def test_by_name_missing(self):
        r = self._mk(TaskStatus.SUCCESS)
        assert r.by_name("nope") is None


# ---------- AddTask / management ----------
class TestAddTask:
    def test_add_single(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="a", func=lambda: 1))
        assert r.task_count == 1

    def test_add_many(self):
        r = TaskRunner()
        r.add_tasks(
            [TaskDef(name=f"t{i}", func=lambda: 1) for i in range(5)]
        )
        assert r.task_count == 5

    def test_add_preserves_order(self):
        r = TaskRunner()
        r.add_tasks([TaskDef(name=n, func=lambda: 1) for n in ["a", "b", "c"]])
        assert r.task_names == ["a", "b", "c"]


# ---------- run_sequential success ----------
class TestRunSequentialSuccess:
    def test_single_task(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="a", func=lambda: 42))
        res = r.run_sequential()
        assert res.all_success
        assert res.by_name("a").output == 42
        assert res.by_name("a").attempts == 1

    def test_multiple_tasks_in_order(self):
        r = TaskRunner()
        order = []
        r.add_tasks(
            [
                TaskDef(name=n, func=lambda n=n: order.append(n) or n)
                for n in ["a", "b", "c"]
            ]
        )
        res = r.run_sequential()
        assert order == ["a", "b", "c"]
        assert [tr.task_name for tr in res.task_results] == ["a", "b", "c"]

    def test_args_and_kwargs_passed(self):
        r = TaskRunner()
        r.add_task(
            TaskDef(
                name="sum",
                func=lambda a, b, c=0: a + b + c,
                args=(1, 2),
                kwargs={"c": 3},
            )
        )
        res = r.run_sequential()
        assert res.by_name("sum").output == 6

    def test_duration_from_now_fn(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="a", func=lambda: 1))
        # batch_start=0, task_start=1, task_end=4, batch_end=5
        now = make_now([0.0, 1.0, 4.0, 5.0])
        res = r.run_sequential(now_fn=now)
        assert res.by_name("a").duration == 3.0
        assert res.total_duration == 5.0


# ---------- run_sequential failure ----------
class TestRunSequentialFailure:
    def test_failure_marks_status(self):
        r = TaskRunner()

        def bad():
            raise ValueError("nope")

        r.add_task(TaskDef(name="bad", func=bad))
        res = r.run_sequential()
        assert res.by_name("bad").status is TaskStatus.FAILED
        assert "ValueError" in res.by_name("bad").error
        assert res.all_success is False

    def test_failure_does_not_block_subsequent(self):
        r = TaskRunner()

        def bad():
            raise RuntimeError("x")

        r.add_task(TaskDef(name="bad", func=bad))
        r.add_task(TaskDef(name="good", func=lambda: "yay"))
        res = r.run_sequential()
        assert res.by_name("bad").status is TaskStatus.FAILED
        assert res.by_name("good").status is TaskStatus.SUCCESS

    def test_failure_count(self):
        r = TaskRunner()

        def bad():
            raise RuntimeError("x")

        r.add_task(TaskDef(name="b1", func=bad))
        r.add_task(TaskDef(name="b2", func=bad))
        r.add_task(TaskDef(name="ok", func=lambda: 1))
        res = r.run_sequential()
        assert res.failure_count == 2
        assert res.success_count == 1


# ---------- retry ----------
class TestRunSequentialRetry:
    def test_succeeds_second_attempt(self):
        counter = CallCounter(fail_first_n=1)
        r = TaskRunner()
        r.add_task(TaskDef(name="t", func=counter, max_retries=2))
        res = r.run_sequential()
        tr = res.by_name("t")
        assert tr.status is TaskStatus.SUCCESS
        assert tr.attempts == 2
        assert tr.output == "ok-2"

    def test_succeeds_third_attempt(self):
        counter = CallCounter(fail_first_n=2)
        r = TaskRunner()
        r.add_task(TaskDef(name="t", func=counter, max_retries=3))
        res = r.run_sequential()
        assert res.by_name("t").status is TaskStatus.SUCCESS
        assert res.by_name("t").attempts == 3


class TestRunSequentialMaxRetries:
    def test_gives_up_after_limit(self):
        counter = CallCounter(fail_first_n=999)
        r = TaskRunner()
        r.add_task(TaskDef(name="t", func=counter, max_retries=2))
        res = r.run_sequential()
        tr = res.by_name("t")
        assert tr.status is TaskStatus.FAILED
        assert tr.attempts == 3  # initial + 2 retries

    def test_no_retries_default(self):
        counter = CallCounter(fail_first_n=1)
        r = TaskRunner()
        r.add_task(TaskDef(name="t", func=counter))
        res = r.run_sequential()
        assert res.by_name("t").status is TaskStatus.FAILED
        assert res.by_name("t").attempts == 1


# ---------- skip_on_failure ----------
class TestSkipOnFailure:
    def test_skipped_instead_of_failed(self):
        r = TaskRunner()

        def bad():
            raise RuntimeError("x")

        r.add_task(TaskDef(name="t", func=bad, skip_on_failure=True))
        res = r.run_sequential()
        tr = res.by_name("t")
        assert tr.status is TaskStatus.SKIPPED
        assert tr.error is not None  # error is still captured

    def test_skip_on_failure_with_retries(self):
        counter = CallCounter(fail_first_n=99)
        r = TaskRunner()
        r.add_task(
            TaskDef(
                name="t", func=counter, max_retries=2, skip_on_failure=True
            )
        )
        res = r.run_sequential()
        tr = res.by_name("t")
        assert tr.status is TaskStatus.SKIPPED
        assert tr.attempts == 3

    def test_skip_on_failure_success_still_success(self):
        r = TaskRunner()
        r.add_task(
            TaskDef(name="t", func=lambda: 1, skip_on_failure=True)
        )
        res = r.run_sequential()
        assert res.by_name("t").status is TaskStatus.SUCCESS


# ---------- condition ----------
class TestCondition:
    def test_skipped_if_false(self):
        r = TaskRunner()
        called = []
        r.add_task(
            TaskDef(
                name="t",
                func=lambda: called.append(1),
                condition=lambda: False,
            )
        )
        res = r.run_sequential()
        assert res.by_name("t").status is TaskStatus.SKIPPED
        assert res.by_name("t").error is None
        assert called == []  # func not called

    def test_runs_if_true(self):
        r = TaskRunner()
        r.add_task(
            TaskDef(name="t", func=lambda: "ran", condition=lambda: True)
        )
        res = r.run_sequential()
        assert res.by_name("t").status is TaskStatus.SUCCESS
        assert res.by_name("t").output == "ran"

    def test_condition_exception_skips(self):
        r = TaskRunner()

        def bad_cond():
            raise ValueError("cond-failed")

        r.add_task(TaskDef(name="t", func=lambda: 1, condition=bad_cond))
        res = r.run_sequential()
        assert res.by_name("t").status is TaskStatus.SKIPPED
        assert "ValueError" in (res.by_name("t").error or "")


# ---------- run_parallel ----------
class TestRunParallel:
    def test_runs_all(self):
        r = TaskRunner()
        r.add_tasks(
            [TaskDef(name=f"t{i}", func=lambda i=i: i * 2) for i in range(5)]
        )
        res = r.run_parallel(max_workers=3)
        assert res.success_count == 5
        for i in range(5):
            assert res.by_name(f"t{i}").output == i * 2

    def test_all_success_property(self):
        r = TaskRunner()
        r.add_tasks([TaskDef(name=f"t{i}", func=lambda: 1) for i in range(3)])
        res = r.run_parallel()
        assert res.all_success

    def test_failure_isolated(self):
        r = TaskRunner()

        def bad():
            raise RuntimeError("x")

        r.add_task(TaskDef(name="bad", func=bad))
        r.add_task(TaskDef(name="ok", func=lambda: 1))
        res = r.run_parallel()
        assert res.by_name("bad").status is TaskStatus.FAILED
        assert res.by_name("ok").status is TaskStatus.SUCCESS


class TestRunParallelOrder:
    def test_results_map_by_name(self):
        r = TaskRunner()
        r.add_tasks(
            [
                TaskDef(name="alpha", func=lambda: "A"),
                TaskDef(name="beta", func=lambda: "B"),
                TaskDef(name="gamma", func=lambda: "C"),
            ]
        )
        res = r.run_parallel(max_workers=2)
        assert res.by_name("alpha").output == "A"
        assert res.by_name("beta").output == "B"
        assert res.by_name("gamma").output == "C"

    def test_result_count_matches_tasks(self):
        r = TaskRunner()
        r.add_tasks([TaskDef(name=f"t{i}", func=lambda: 1) for i in range(7)])
        res = r.run_parallel(max_workers=4)
        assert len(res.task_results) == 7

    def test_parallel_preserves_order_of_results(self):
        # Results should follow the original add order, not completion order.
        r = TaskRunner()

        def slow_fast(i):
            # earlier tasks sleep longer so completion order differs from input
            time.sleep(0.02 if i == 0 else 0.0)
            return i

        r.add_tasks(
            [TaskDef(name=f"t{i}", func=lambda i=i: slow_fast(i)) for i in range(3)]
        )
        res = r.run_parallel(max_workers=3)
        names = [tr.task_name for tr in res.task_results]
        assert names == ["t0", "t1", "t2"]


class TestRunParallelTimeout:
    def test_timeout_status(self):
        r = TaskRunner()

        def slow():
            time.sleep(0.5)
            return "done"

        r.add_task(TaskDef(name="slow", func=slow, timeout=0.05))
        res = r.run_parallel(max_workers=2)
        tr = res.by_name("slow")
        assert tr.status is TaskStatus.TIMEOUT
        assert "timed out" in (tr.error or "")

    def test_fast_task_completes_within_timeout(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="fast", func=lambda: "ok", timeout=1.0))
        res = r.run_parallel()
        assert res.by_name("fast").status is TaskStatus.SUCCESS

    def test_timeout_does_not_affect_other_tasks(self):
        r = TaskRunner()

        def slow():
            time.sleep(0.5)

        r.add_task(TaskDef(name="slow", func=slow, timeout=0.05))
        r.add_task(TaskDef(name="fast", func=lambda: "ok"))
        res = r.run_parallel(max_workers=2)
        assert res.by_name("slow").status is TaskStatus.TIMEOUT
        assert res.by_name("fast").status is TaskStatus.SUCCESS


# ---------- clear ----------
class TestClear:
    def test_clear_removes_all(self):
        r = TaskRunner()
        r.add_tasks([TaskDef(name=f"t{i}", func=lambda: 1) for i in range(3)])
        r.clear()
        assert r.task_count == 0
        assert r.task_names == []

    def test_clear_then_run(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="a", func=lambda: 1))
        r.clear()
        res = r.run_sequential()
        assert res.task_results == []


# ---------- task_count ----------
class TestTaskCount:
    def test_empty(self):
        assert TaskRunner().task_count == 0

    def test_grows(self):
        r = TaskRunner()
        for i in range(4):
            r.add_task(TaskDef(name=f"t{i}", func=lambda: 1))
            assert r.task_count == i + 1

    def test_task_names_list(self):
        r = TaskRunner()
        r.add_tasks([TaskDef(name=n, func=lambda: 1) for n in ["x", "y"]])
        assert r.task_names == ["x", "y"]


# ---------- remove_task ----------
class TestRemoveTask:
    def test_remove_existing(self):
        r = TaskRunner()
        r.add_tasks(
            [TaskDef(name=n, func=lambda: 1) for n in ["a", "b", "c"]]
        )
        assert r.remove_task("b") is True
        assert r.task_names == ["a", "c"]

    def test_remove_missing(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="a", func=lambda: 1))
        assert r.remove_task("nope") is False
        assert r.task_count == 1

    def test_remove_first_match_only(self):
        r = TaskRunner()
        r.add_tasks(
            [
                TaskDef(name="dup", func=lambda: 1),
                TaskDef(name="dup", func=lambda: 2),
            ]
        )
        r.remove_task("dup")
        assert r.task_count == 1


# ---------- edge cases ----------
class TestEdgeCases:
    def test_no_tasks_sequential(self):
        r = TaskRunner()
        res = r.run_sequential()
        assert res.task_results == []
        assert res.success_count == 0
        assert res.failure_count == 0
        assert res.all_success is False  # empty is not all-success

    def test_no_tasks_parallel(self):
        r = TaskRunner()
        res = r.run_parallel()
        assert res.task_results == []

    def test_single_task_sequential(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="solo", func=lambda: "hi"))
        res = r.run_sequential()
        assert len(res.task_results) == 1
        assert res.by_name("solo").output == "hi"

    def test_identical_names(self):
        r = TaskRunner()
        r.add_tasks(
            [
                TaskDef(name="dup", func=lambda: 1),
                TaskDef(name="dup", func=lambda: 2),
            ]
        )
        res = r.run_sequential()
        assert len(res.task_results) == 2
        # by_name returns the first match
        first = res.by_name("dup")
        assert first is not None
        assert first.output == 1

    def test_max_workers_clamped_to_one(self):
        r = TaskRunner()
        r.add_task(TaskDef(name="a", func=lambda: 1))
        res = r.run_parallel(max_workers=0)
        assert res.by_name("a").status is TaskStatus.SUCCESS

    def test_condition_in_parallel(self):
        r = TaskRunner()
        r.add_task(
            TaskDef(
                name="skipped", func=lambda: 1, condition=lambda: False
            )
        )
        r.add_task(
            TaskDef(name="ran", func=lambda: 2, condition=lambda: True)
        )
        res = r.run_parallel()
        assert res.by_name("skipped").status is TaskStatus.SKIPPED
        assert res.by_name("ran").status is TaskStatus.SUCCESS

    def test_retry_in_parallel(self):
        counter = CallCounter(fail_first_n=1)
        r = TaskRunner()
        r.add_task(TaskDef(name="t", func=counter, max_retries=3))
        res = r.run_parallel()
        assert res.by_name("t").status is TaskStatus.SUCCESS
        assert res.by_name("t").attempts == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
