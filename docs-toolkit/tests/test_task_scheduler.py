"""Tests for the E54 task_scheduler module.

Coverage targets:
- TaskSchedule.next_run for ONCE, INTERVAL, CRON_LIKE
- TaskResult.duration()
- ScheduledTask fields and defaults
- TaskScheduler: add/remove/get/list, run_now (success + exception),
  tick triggers due tasks, ONCE disables after run, cancel, pending_count
- Retry logic (max_retries > 0)
- Threading: multiple tasks in one tick run concurrently
- Edge cases: empty scheduler, disabled task not executed, unknown task_id
"""
import threading
import time
import math

import pytest

from docstoolkit.task_scheduler import (
    ScheduleType,
    TaskSchedule,
    TaskStatus,
    TaskResult,
    ScheduledTask,
    SchedulerConfig,
    TaskScheduler,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_interval(seconds: float) -> TaskSchedule:
    return TaskSchedule(schedule_type=ScheduleType.INTERVAL, interval_seconds=seconds)


def _make_once(run_at: float = 0.0) -> TaskSchedule:
    return TaskSchedule(schedule_type=ScheduleType.ONCE, run_at=run_at)


def _make_cron(minutes=None, hours=None) -> TaskSchedule:
    return TaskSchedule(
        schedule_type=ScheduleType.CRON_LIKE,
        cron_minutes=minutes or [],
        cron_hours=hours or [],
    )


def _task(name="t", func=None, schedule=None, **kw) -> ScheduledTask:
    if func is None:
        func = lambda: None
    if schedule is None:
        schedule = _make_interval(60)
    return ScheduledTask(name=name, func=func, schedule=schedule, **kw)


# ---------------------------------------------------------------------------
# 1. ScheduleType enum
# ---------------------------------------------------------------------------

class TestScheduleTypeEnum:
    def test_values_exist(self):
        assert ScheduleType.ONCE
        assert ScheduleType.INTERVAL
        assert ScheduleType.CRON_LIKE

    def test_unique_values(self):
        vals = [st.value for st in ScheduleType]
        assert len(vals) == len(set(vals))

    def test_string_values(self):
        assert isinstance(ScheduleType.ONCE.value, str)
        assert isinstance(ScheduleType.INTERVAL.value, str)
        assert isinstance(ScheduleType.CRON_LIKE.value, str)


# ---------------------------------------------------------------------------
# 2. TaskSchedule dataclass
# ---------------------------------------------------------------------------

class TestTaskScheduleDefaults:
    def test_defaults(self):
        s = TaskSchedule(schedule_type=ScheduleType.ONCE)
        assert s.interval_seconds == 0.0
        assert s.run_at == 0.0
        assert s.cron_minutes == []
        assert s.cron_hours == []

    def test_cron_lists_are_independent(self):
        s1 = TaskSchedule(schedule_type=ScheduleType.CRON_LIKE)
        s2 = TaskSchedule(schedule_type=ScheduleType.CRON_LIKE)
        s1.cron_minutes.append(5)
        assert s2.cron_minutes == []


# ---------------------------------------------------------------------------
# 3. TaskSchedule.next_run — ONCE
# ---------------------------------------------------------------------------

class TestNextRunOnce:
    def test_run_at_zero_is_immediate(self):
        s = _make_once(run_at=0.0)
        now = time.time()
        # run_at=0 <= now so next_run returns 0 (immediate)
        nxt = s.next_run(after=now)
        assert nxt == 0.0

    def test_run_at_future(self):
        future = time.time() + 3600
        s = _make_once(run_at=future)
        now = time.time()
        assert s.next_run(after=now) == future

    def test_run_at_past(self):
        past = time.time() - 100
        s = _make_once(run_at=past)
        nxt = s.next_run(after=time.time())
        # past <= now → next_run returns past (scheduler decides to run immediately)
        assert nxt == past

    def test_run_at_exactly_now(self):
        now = time.time()
        s = _make_once(run_at=now)
        nxt = s.next_run(after=now)
        assert nxt == now

    def test_after_defaults_to_time_now(self):
        future = time.time() + 9999
        s = _make_once(run_at=future)
        # Should not raise and should return a value close to future
        nxt = s.next_run()
        assert nxt == future


# ---------------------------------------------------------------------------
# 4. TaskSchedule.next_run — INTERVAL
# ---------------------------------------------------------------------------

class TestNextRunInterval:
    def test_basic(self):
        s = _make_interval(30)
        now = 1000.0
        assert s.next_run(after=now) == 1030.0

    def test_zero_interval(self):
        s = _make_interval(0)
        now = 500.0
        assert s.next_run(after=now) == 500.0

    def test_fractional_interval(self):
        s = _make_interval(0.5)
        now = 100.0
        assert abs(s.next_run(after=now) - 100.5) < 1e-9

    def test_large_interval(self):
        s = _make_interval(86400)
        now = 0.0
        assert s.next_run(after=now) == 86400.0

    def test_after_defaults(self):
        s = _make_interval(10)
        before = time.time()
        nxt = s.next_run()
        after = time.time()
        assert before + 10 <= nxt <= after + 10 + 1  # within 1 s tolerance


# ---------------------------------------------------------------------------
# 5. TaskSchedule.next_run — CRON_LIKE
# ---------------------------------------------------------------------------

class TestNextRunCronLike:
    def _epoch_for(self, y=2024, mo=1, d=1, h=0, m=0, s=0) -> float:
        import calendar
        import time as _t
        t = _t.struct_time((y, mo, d, h, m, s, 0, 1, 0))
        return float(calendar.timegm(t))

    def test_any_minute_any_hour(self):
        """Empty lists → fires every minute."""
        s = _make_cron()
        ref = self._epoch_for(2024, 1, 1, 12, 0, 0)  # 12:00:00 UTC
        nxt = s.next_run(after=ref)
        # Should be 12:01:00
        assert nxt == ref + 60

    def test_specific_minute(self):
        s = _make_cron(minutes=[30])
        # ref = 12:00:00 → next :30 is 12:30:00
        ref = self._epoch_for(2024, 1, 1, 12, 0, 0)
        nxt = s.next_run(after=ref)
        expected = self._epoch_for(2024, 1, 1, 12, 30, 0)
        assert nxt == expected

    def test_specific_hour(self):
        s = _make_cron(hours=[14])
        # ref = 12:00:00 → search starts at 12:01:00.
        # Advance minute by minute until hour==14: first match is 14:00:00.
        ref = self._epoch_for(2024, 1, 1, 12, 0, 0)
        nxt = s.next_run(after=ref)
        expected = self._epoch_for(2024, 1, 1, 14, 0, 0)
        # nxt should be exactly 14:00:00 (minute=0, hour=14, both match)
        assert nxt == expected

    def test_specific_minute_and_hour(self):
        s = _make_cron(minutes=[45], hours=[15])
        # ref = 12:00:00 → next 15:45
        ref = self._epoch_for(2024, 1, 1, 12, 0, 0)
        nxt = s.next_run(after=ref)
        expected = self._epoch_for(2024, 1, 1, 15, 45, 0)
        assert nxt == expected

    def test_wraps_to_next_day(self):
        """If cron_hours=[2] and it's already 3:00, next run is next day at 2:xx."""
        s = _make_cron(minutes=[0], hours=[2])
        ref = self._epoch_for(2024, 1, 1, 3, 0, 0)  # 03:00 UTC
        nxt = s.next_run(after=ref)
        expected = self._epoch_for(2024, 1, 2, 2, 0, 0)  # next day 02:00
        assert nxt == expected

    def test_returns_inf_if_no_match_in_24h(self):
        """Impossible cron (e.g. minutes=[99]) returns inf."""
        s = _make_cron(minutes=[99])  # 99 is never a valid minute
        ref = time.time()
        nxt = s.next_run(after=ref)
        assert nxt == float("inf")

    def test_multiple_minutes(self):
        s = _make_cron(minutes=[0, 15, 30, 45])
        ref = self._epoch_for(2024, 1, 1, 10, 10, 0)  # 10:10
        nxt = s.next_run(after=ref)
        expected = self._epoch_for(2024, 1, 1, 10, 15, 0)
        assert nxt == expected

    def test_after_defaults_for_cron(self):
        s = _make_cron()
        nxt = s.next_run()  # should not raise
        assert nxt > time.time()


# ---------------------------------------------------------------------------
# 6. TaskResult
# ---------------------------------------------------------------------------

class TestTaskResult:
    def test_duration(self):
        r = TaskResult(
            task_id="abc",
            status=TaskStatus.COMPLETED,
            started_at=100.0,
            finished_at=105.5,
        )
        assert r.duration() == pytest.approx(5.5)

    def test_duration_zero(self):
        r = TaskResult(
            task_id="x", status=TaskStatus.FAILED,
            started_at=200.0, finished_at=200.0,
        )
        assert r.duration() == 0.0

    def test_default_return_value_is_none(self):
        r = TaskResult(
            task_id="y", status=TaskStatus.COMPLETED,
            started_at=0.0, finished_at=1.0,
        )
        assert r.return_value is None

    def test_default_error_is_empty_string(self):
        r = TaskResult(
            task_id="y", status=TaskStatus.COMPLETED,
            started_at=0.0, finished_at=1.0,
        )
        assert r.error == ""

    def test_stores_return_value(self):
        r = TaskResult(
            task_id="z", status=TaskStatus.COMPLETED,
            started_at=0.0, finished_at=1.0,
            return_value=42,
        )
        assert r.return_value == 42

    def test_stores_error(self):
        r = TaskResult(
            task_id="z", status=TaskStatus.FAILED,
            started_at=0.0, finished_at=1.0,
            error="ValueError: bad",
        )
        assert "ValueError" in r.error


# ---------------------------------------------------------------------------
# 7. TaskStatus enum
# ---------------------------------------------------------------------------

class TestTaskStatusEnum:
    def test_all_statuses_exist(self):
        statuses = {s.name for s in TaskStatus}
        assert statuses == {"PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"}

    def test_unique_values(self):
        vals = [s.value for s in TaskStatus]
        assert len(vals) == len(set(vals))


# ---------------------------------------------------------------------------
# 8. ScheduledTask
# ---------------------------------------------------------------------------

class TestScheduledTask:
    def test_auto_task_id(self):
        t = _task()
        assert isinstance(t.task_id, str)
        assert len(t.task_id) == 32  # uuid4().hex is 32 chars

    def test_unique_task_ids(self):
        ids = {_task().task_id for _ in range(20)}
        assert len(ids) == 20

    def test_custom_task_id(self):
        t = _task(task_id="my-custom-id")
        assert t.task_id == "my-custom-id"

    def test_defaults(self):
        t = _task()
        assert t.args == ()
        assert t.kwargs == {}
        assert t.max_retries == 0
        assert t.enabled is True
        assert t.last_result is None
        assert t.run_count == 0

    def test_args_kwargs_stored(self):
        t = _task(args=(1, 2), kwargs={"x": 3})
        assert t.args == (1, 2)
        assert t.kwargs == {"x": 3}

    def test_independent_kwargs_dicts(self):
        t1 = _task()
        t2 = _task()
        t1.kwargs["a"] = 1
        assert "a" not in t2.kwargs

    def test_name_stored(self):
        t = _task(name="my-task")
        assert t.name == "my-task"

    def test_schedule_stored(self):
        s = _make_interval(10)
        t = _task(schedule=s)
        assert t.schedule is s


# ---------------------------------------------------------------------------
# 9. SchedulerConfig
# ---------------------------------------------------------------------------

class TestSchedulerConfig:
    def test_defaults(self):
        cfg = SchedulerConfig()
        assert cfg.tick_interval == pytest.approx(0.1)
        assert cfg.max_workers == 4

    def test_custom(self):
        cfg = SchedulerConfig(tick_interval=1.0, max_workers=8)
        assert cfg.tick_interval == 1.0
        assert cfg.max_workers == 8


# ---------------------------------------------------------------------------
# 10. TaskScheduler — registry
# ---------------------------------------------------------------------------

class TestTaskSchedulerRegistry:
    def test_add_task_returns_id(self):
        sched = TaskScheduler()
        t = _task()
        tid = sched.add_task(t)
        assert tid == t.task_id

    def test_get_task(self):
        sched = TaskScheduler()
        t = _task()
        sched.add_task(t)
        assert sched.get_task(t.task_id) is t

    def test_get_unknown_returns_none(self):
        sched = TaskScheduler()
        assert sched.get_task("nonexistent") is None

    def test_list_tasks_empty(self):
        sched = TaskScheduler()
        assert sched.list_tasks() == []

    def test_list_tasks_returns_all(self):
        sched = TaskScheduler()
        t1, t2 = _task("a"), _task("b")
        sched.add_task(t1)
        sched.add_task(t2)
        lst = sched.list_tasks()
        assert len(lst) == 2
        assert t1 in lst
        assert t2 in lst

    def test_remove_existing(self):
        sched = TaskScheduler()
        t = _task()
        sched.add_task(t)
        assert sched.remove_task(t.task_id) is True
        assert sched.get_task(t.task_id) is None

    def test_remove_nonexistent(self):
        sched = TaskScheduler()
        assert sched.remove_task("ghost") is False

    def test_add_multiple_same_id_overwrites(self):
        sched = TaskScheduler()
        t1 = _task(task_id="fixed")
        t2 = _task(task_id="fixed")
        sched.add_task(t1)
        sched.add_task(t2)
        assert sched.get_task("fixed") is t2


# ---------------------------------------------------------------------------
# 11. TaskScheduler — run_now
# ---------------------------------------------------------------------------

class TestRunNow:
    def test_run_now_success(self):
        sched = TaskScheduler()
        t = _task(func=lambda: 99)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.status == TaskStatus.COMPLETED
        assert result.return_value == 99
        assert result.error == ""

    def test_run_now_updates_last_result(self):
        sched = TaskScheduler()
        t = _task(func=lambda: "done")
        sched.add_task(t)
        sched.run_now(t.task_id)
        assert t.last_result is not None
        assert t.last_result.status == TaskStatus.COMPLETED

    def test_run_now_increments_run_count(self):
        sched = TaskScheduler()
        t = _task(func=lambda: None)
        sched.add_task(t)
        sched.run_now(t.task_id)
        sched.run_now(t.task_id)
        assert t.run_count == 2

    def test_run_now_failure(self):
        sched = TaskScheduler()

        def boom():
            raise ValueError("oops")

        t = _task(func=boom)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.status == TaskStatus.FAILED
        assert "ValueError" in result.error
        assert "oops" in result.error
        assert result.return_value is None

    def test_run_now_unknown_task_raises(self):
        sched = TaskScheduler()
        with pytest.raises(KeyError):
            sched.run_now("does-not-exist")

    def test_run_now_result_task_id_matches(self):
        sched = TaskScheduler()
        t = _task(func=lambda: 1)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.task_id == t.task_id

    def test_run_now_duration_positive(self):
        sched = TaskScheduler()
        t = _task(func=lambda: time.sleep(0.01) or "x")
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.duration() >= 0.0

    def test_run_now_with_args(self):
        sched = TaskScheduler()
        t = _task(func=lambda a, b: a + b, args=(3, 4))
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.return_value == 7

    def test_run_now_with_kwargs(self):
        sched = TaskScheduler()
        t = _task(func=lambda x=0: x * 2, kwargs={"x": 5})
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.return_value == 10


# ---------------------------------------------------------------------------
# 12. TaskScheduler — tick
# ---------------------------------------------------------------------------

class TestTick:
    def test_empty_scheduler_tick(self):
        sched = TaskScheduler()
        results = sched.tick(now=time.time())
        assert results == []

    def test_tick_triggers_due_once_task(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="once",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),  # immediate
        )
        sched.add_task(t)
        results = sched.tick(now=time.time())
        assert len(results) == 1
        assert results[0].status == TaskStatus.COMPLETED
        assert len(calls) == 1

    def test_tick_once_disables_after_run(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="once",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        sched.tick(now=time.time())  # second tick
        assert len(calls) == 1  # still only 1
        assert t.enabled is False

    def test_tick_disabled_task_not_run(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="disabled",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),
            enabled=False,
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        assert calls == []

    def test_tick_interval_not_immediately_due(self):
        """On first tick, an INTERVAL task should NOT fire immediately."""
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="interval",
            func=lambda: calls.append(1),
            schedule=_make_interval(60),
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        assert calls == []

    def test_tick_interval_fires_after_elapsed(self):
        """Force a tick far in the future so the interval has elapsed."""
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="interval",
            func=lambda: calls.append(1),
            schedule=_make_interval(10),
        )
        sched.add_task(t)
        # First tick sets reference time
        now = time.time()
        sched.tick(now=now)
        # Second tick 20 s later — should fire
        sched.tick(now=now + 20)
        assert len(calls) == 1

    def test_tick_updates_run_count(self):
        sched = TaskScheduler()
        t = ScheduledTask(
            name="t",
            func=lambda: None,
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        assert t.run_count == 1

    def test_tick_updates_last_result(self):
        sched = TaskScheduler()
        t = ScheduledTask(
            name="t",
            func=lambda: "tick-result",
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        assert t.last_result is not None
        assert t.last_result.return_value == "tick-result"

    def test_tick_future_once_task_not_fired(self):
        sched = TaskScheduler()
        calls = []
        future_time = time.time() + 9999
        t = ScheduledTask(
            name="future",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=future_time),
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        assert calls == []

    def test_tick_multiple_due_tasks(self):
        sched = TaskScheduler()
        calls = []
        for i in range(3):
            t = ScheduledTask(
                name=f"t{i}",
                func=lambda i=i: calls.append(i),
                schedule=_make_once(run_at=0.0),
            )
            sched.add_task(t)
        sched.tick(now=time.time())
        assert len(calls) == 3

    def test_tick_returns_results_for_all_due(self):
        sched = TaskScheduler()
        for i in range(4):
            t = ScheduledTask(
                name=f"t{i}",
                func=lambda: None,
                schedule=_make_once(run_at=0.0),
            )
            sched.add_task(t)
        results = sched.tick(now=time.time())
        assert len(results) == 4

    def test_tick_failed_task_result_recorded(self):
        sched = TaskScheduler()

        def fail():
            raise RuntimeError("bang")

        t = ScheduledTask(name="fail", func=fail, schedule=_make_once(run_at=0.0))
        sched.add_task(t)
        results = sched.tick(now=time.time())
        assert results[0].status == TaskStatus.FAILED
        assert "bang" in results[0].error


# ---------------------------------------------------------------------------
# 13. Cancel
# ---------------------------------------------------------------------------

class TestCancel:
    def test_cancel_existing(self):
        sched = TaskScheduler()
        t = _task()
        sched.add_task(t)
        assert sched.cancel(t.task_id) is True
        assert t.enabled is False

    def test_cancel_nonexistent(self):
        sched = TaskScheduler()
        assert sched.cancel("ghost") is False

    def test_cancelled_task_does_not_run(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="c",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        sched.cancel(t.task_id)
        sched.tick(now=time.time())
        assert calls == []

    def test_cancel_twice(self):
        sched = TaskScheduler()
        t = _task()
        sched.add_task(t)
        assert sched.cancel(t.task_id) is True
        assert sched.cancel(t.task_id) is True  # idempotent, task still there


# ---------------------------------------------------------------------------
# 14. pending_count
# ---------------------------------------------------------------------------

class TestPendingCount:
    def test_empty_scheduler(self):
        sched = TaskScheduler()
        assert sched.pending_count() == 0

    def test_all_pending_before_run(self):
        sched = TaskScheduler()
        for _ in range(5):
            sched.add_task(_task())
        assert sched.pending_count() == 5

    def test_pending_decreases_after_tick(self):
        sched = TaskScheduler()
        t = ScheduledTask(
            name="p",
            func=lambda: None,
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        assert sched.pending_count() == 1
        sched.tick(now=time.time())
        assert sched.pending_count() == 0

    def test_pending_count_after_run_now(self):
        sched = TaskScheduler()
        t = _task(func=lambda: None)
        sched.add_task(t)
        sched.run_now(t.task_id)
        assert sched.pending_count() == 0


# ---------------------------------------------------------------------------
# 15. Retry logic
# ---------------------------------------------------------------------------

class TestRetryLogic:
    def test_succeeds_on_first_attempt_no_retry(self):
        calls = []

        def fn():
            calls.append(1)
            return "ok"

        sched = TaskScheduler()
        t = ScheduledTask(name="r", func=fn, schedule=_make_once(), max_retries=2)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.status == TaskStatus.COMPLETED
        assert len(calls) == 1

    def test_retries_on_failure(self):
        attempts = []

        def fn():
            attempts.append(1)
            raise ValueError("retry me")

        sched = TaskScheduler()
        t = ScheduledTask(name="r", func=fn, schedule=_make_once(), max_retries=3)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.status == TaskStatus.FAILED
        assert len(attempts) == 4  # 1 original + 3 retries

    def test_succeeds_on_second_attempt(self):
        attempts = []

        def fn():
            attempts.append(1)
            if len(attempts) < 2:
                raise RuntimeError("first attempt fails")
            return "success"

        sched = TaskScheduler()
        t = ScheduledTask(name="r", func=fn, schedule=_make_once(), max_retries=2)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.status == TaskStatus.COMPLETED
        assert result.return_value == "success"
        assert len(attempts) == 2

    def test_no_retries_by_default(self):
        calls = []

        def fn():
            calls.append(1)
            raise ValueError("fail")

        sched = TaskScheduler()
        t = _task(func=fn)
        sched.add_task(t)
        result = sched.run_now(t.task_id)
        assert result.status == TaskStatus.FAILED
        assert len(calls) == 1

    def test_max_retries_zero_means_one_attempt(self):
        calls = []

        def fn():
            calls.append(1)
            raise Exception("err")

        sched = TaskScheduler()
        t = ScheduledTask(name="r", func=fn, schedule=_make_once(), max_retries=0)
        sched.add_task(t)
        sched.run_now(t.task_id)
        assert len(calls) == 1

    def test_retry_via_tick(self):
        attempts = []

        def fn():
            attempts.append(1)
            raise RuntimeError("always fail")

        sched = TaskScheduler()
        t = ScheduledTask(name="r", func=fn, schedule=_make_once(), max_retries=2)
        sched.add_task(t)
        results = sched.tick(now=time.time())
        assert results[0].status == TaskStatus.FAILED
        assert len(attempts) == 3


# ---------------------------------------------------------------------------
# 16. Threading: concurrent execution
# ---------------------------------------------------------------------------

class TestThreading:
    def test_multiple_tasks_run_concurrently(self):
        """Tasks that sleep should overlap if run concurrently."""
        sched = TaskScheduler(config=SchedulerConfig(max_workers=4))
        start_times = []
        lock = threading.Lock()

        def slow_task():
            with lock:
                start_times.append(time.time())
            time.sleep(0.05)

        tasks = []
        for i in range(4):
            t = ScheduledTask(
                name=f"slow{i}",
                func=slow_task,
                schedule=_make_once(run_at=0.0),
            )
            sched.add_task(t)
            tasks.append(t)

        t0 = time.time()
        sched.tick(now=t0)
        elapsed = time.time() - t0

        # 4 tasks each sleeping 0.05s: serial = 0.2s, concurrent < 0.15s
        assert elapsed < 0.15, f"Tasks appear to run serially (elapsed={elapsed:.3f}s)"

    def test_shared_counter_incremented_correctly(self):
        """All tasks should increment a shared counter exactly N times."""
        counter = {"n": 0}
        lock = threading.Lock()

        def inc():
            with lock:
                counter["n"] += 1

        sched = TaskScheduler(config=SchedulerConfig(max_workers=8))
        N = 8
        for _ in range(N):
            t = ScheduledTask(
                name="inc",
                func=inc,
                schedule=_make_once(run_at=0.0),
            )
            sched.add_task(t)

        sched.tick(now=time.time())
        assert counter["n"] == N

    def test_tick_is_thread_safe_add_during_tick(self):
        """Adding a task from a separate thread while tick runs should not crash."""
        sched = TaskScheduler(config=SchedulerConfig(max_workers=2))

        def slow():
            time.sleep(0.02)

        # Add 4 slow tasks
        for _ in range(4):
            sched.add_task(ScheduledTask(name="s", func=slow, schedule=_make_once(run_at=0.0)))

        results = []

        def do_tick():
            results.extend(sched.tick(now=time.time()))

        tick_thread = threading.Thread(target=do_tick)
        tick_thread.start()

        # Add a new task while tick is running
        time.sleep(0.005)
        extra = ScheduledTask(name="extra", func=lambda: None, schedule=_make_once(run_at=0.0))
        sched.add_task(extra)

        tick_thread.join(timeout=2)
        # No assertion on count — just verify no exception was raised
        assert tick_thread.is_alive() is False


# ---------------------------------------------------------------------------
# 17. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_remove_then_get(self):
        sched = TaskScheduler()
        t = _task()
        sched.add_task(t)
        sched.remove_task(t.task_id)
        assert sched.get_task(t.task_id) is None

    def test_remove_nonexistent_twice(self):
        sched = TaskScheduler()
        assert sched.remove_task("x") is False
        assert sched.remove_task("x") is False

    def test_once_task_run_at_far_future_not_triggered(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="future",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=time.time() + 99999),
        )
        sched.add_task(t)
        sched.tick(now=time.time())
        assert calls == []

    def test_disabled_at_creation_never_runs(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="off",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),
            enabled=False,
        )
        sched.add_task(t)
        for _ in range(3):
            sched.tick(now=time.time())
        assert calls == []

    def test_list_tasks_is_snapshot(self):
        sched = TaskScheduler()
        t = _task()
        sched.add_task(t)
        lst = sched.list_tasks()
        sched.remove_task(t.task_id)
        # Snapshot is independent of later mutations
        assert len(lst) == 1

    def test_default_config(self):
        sched = TaskScheduler()
        assert sched._config.tick_interval == pytest.approx(0.1)
        assert sched._config.max_workers == 4

    def test_custom_config(self):
        cfg = SchedulerConfig(tick_interval=5.0, max_workers=2)
        sched = TaskScheduler(config=cfg)
        assert sched._config.max_workers == 2

    def test_run_now_does_not_disable_once_task(self):
        """run_now should NOT auto-disable ONCE tasks (only tick does)."""
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="once",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        sched.run_now(t.task_id)
        sched.run_now(t.task_id)
        assert len(calls) == 2  # both succeed
        assert t.enabled is True

    def test_tick_now_defaults_to_current_time(self):
        sched = TaskScheduler()
        calls = []
        t = ScheduledTask(
            name="now",
            func=lambda: calls.append(1),
            schedule=_make_once(run_at=0.0),
        )
        sched.add_task(t)
        sched.tick()  # no 'now' argument
        assert len(calls) == 1
