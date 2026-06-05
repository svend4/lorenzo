"""Tests for docstoolkit.priority_queue — priority job queue with scheduling."""
import pytest
from datetime import datetime

from docstoolkit.priority_queue import (
    PriorityJob, JobStatus, Priority,
    PriorityJobQueue,
    FairShareScheduler, SchedulerConfig,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_job(job_id="j1", payload='{"x": 1}', priority=Priority.NORMAL,
             owner="alice", status=JobStatus.PENDING) -> PriorityJob:
    return PriorityJob(
        job_id=job_id,
        payload=payload,
        priority=priority,
        owner=owner,
        status=status,
    )


def fresh_queue() -> PriorityJobQueue:
    return PriorityJobQueue()  # in-memory


# ---------------------------------------------------------------------------
# Priority enum
# ---------------------------------------------------------------------------

class TestPriorityEnum:
    def test_low_value(self):
        assert Priority.LOW == 1

    def test_normal_value(self):
        assert Priority.NORMAL == 5

    def test_high_value(self):
        assert Priority.HIGH == 10

    def test_critical_value(self):
        assert Priority.CRITICAL == 100

    def test_is_int(self):
        assert isinstance(Priority.NORMAL, int)

    def test_ordering(self):
        assert Priority.LOW < Priority.NORMAL < Priority.HIGH < Priority.CRITICAL

    def test_from_int(self):
        assert Priority(10) is Priority.HIGH

    def test_all_members(self):
        names = {m.name for m in Priority}
        assert names == {"LOW", "NORMAL", "HIGH", "CRITICAL"}


# ---------------------------------------------------------------------------
# JobStatus enum
# ---------------------------------------------------------------------------

class TestJobStatusEnum:
    def test_pending_value(self):
        assert JobStatus.PENDING == "pending"

    def test_running_value(self):
        assert JobStatus.RUNNING == "running"

    def test_done_value(self):
        assert JobStatus.DONE == "done"

    def test_failed_value(self):
        assert JobStatus.FAILED == "failed"

    def test_cancelled_value(self):
        assert JobStatus.CANCELLED == "cancelled"

    def test_five_members(self):
        assert len(JobStatus) == 5

    def test_is_str(self):
        assert isinstance(JobStatus.PENDING, str)


# ---------------------------------------------------------------------------
# PriorityJob dataclass
# ---------------------------------------------------------------------------

class TestPriorityJob:
    def test_required_fields(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.job_id == "x"
        assert j.payload == "{}"

    def test_default_priority(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.priority == Priority.NORMAL

    def test_default_status(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.status == JobStatus.PENDING

    def test_default_owner_empty(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.owner == ""

    def test_default_attempt_count_zero(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.attempt_count == 0

    def test_default_error_empty(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.error == ""

    def test_created_ts_auto_set(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.created_ts != ""
        # Must be parseable ISO format
        datetime.fromisoformat(j.created_ts)

    def test_created_ts_not_overwritten_when_provided(self):
        j = PriorityJob(job_id="x", payload="{}", created_ts="2025-01-01T00:00:00")
        assert j.created_ts == "2025-01-01T00:00:00"

    def test_custom_fields(self):
        j = PriorityJob(
            job_id="abc",
            payload='{"k": "v"}',
            priority=Priority.HIGH,
            status=JobStatus.RUNNING,
            owner="bob",
            attempt_count=3,
            error="oops",
        )
        assert j.job_id == "abc"
        assert j.priority == Priority.HIGH
        assert j.status == JobStatus.RUNNING
        assert j.owner == "bob"
        assert j.attempt_count == 3
        assert j.error == "oops"

    # is_terminal
    def test_is_terminal_done(self):
        j = PriorityJob(job_id="x", payload="{}", status=JobStatus.DONE)
        assert j.is_terminal() is True

    def test_is_terminal_failed(self):
        j = PriorityJob(job_id="x", payload="{}", status=JobStatus.FAILED)
        assert j.is_terminal() is True

    def test_is_terminal_cancelled(self):
        j = PriorityJob(job_id="x", payload="{}", status=JobStatus.CANCELLED)
        assert j.is_terminal() is True

    def test_is_terminal_pending_false(self):
        j = PriorityJob(job_id="x", payload="{}", status=JobStatus.PENDING)
        assert j.is_terminal() is False

    def test_is_terminal_running_false(self):
        j = PriorityJob(job_id="x", payload="{}", status=JobStatus.RUNNING)
        assert j.is_terminal() is False

    # duration_ms
    def test_duration_ms_valid(self):
        j = PriorityJob(
            job_id="x", payload="{}",
            started_ts="2025-01-01T10:00:00",
            done_ts="2025-01-01T10:00:01",
        )
        assert j.duration_ms() == pytest.approx(1000.0)

    def test_duration_ms_two_seconds(self):
        j = PriorityJob(
            job_id="x", payload="{}",
            started_ts="2025-01-01T10:00:00",
            done_ts="2025-01-01T10:00:02",
        )
        assert j.duration_ms() == pytest.approx(2000.0)

    def test_duration_ms_empty_started(self):
        j = PriorityJob(job_id="x", payload="{}", done_ts="2025-01-01T10:00:01")
        assert j.duration_ms() == 0.0

    def test_duration_ms_empty_done(self):
        j = PriorityJob(job_id="x", payload="{}", started_ts="2025-01-01T10:00:00")
        assert j.duration_ms() == 0.0

    def test_duration_ms_both_empty(self):
        j = PriorityJob(job_id="x", payload="{}")
        assert j.duration_ms() == 0.0


# ---------------------------------------------------------------------------
# PriorityJobQueue
# ---------------------------------------------------------------------------

class TestPriorityJobQueue:
    def test_enqueue_and_get_roundtrip(self):
        q = fresh_queue()
        job = make_job("j1")
        q.enqueue(job)
        fetched = q.get("j1")
        assert fetched is not None
        assert fetched.job_id == "j1"
        assert fetched.payload == '{"x": 1}'
        assert fetched.priority == Priority.NORMAL

    def test_get_missing_returns_none(self):
        q = fresh_queue()
        assert q.get("nonexistent") is None

    def test_enqueue_idempotent(self):
        q = fresh_queue()
        job = make_job("j1")
        q.enqueue(job)
        q.enqueue(job)  # INSERT OR IGNORE — no error, no duplicate
        assert q.pending_count() == 1

    def test_dequeue_returns_highest_priority(self):
        q = fresh_queue()
        q.enqueue(make_job("low", priority=Priority.LOW))
        q.enqueue(make_job("critical", priority=Priority.CRITICAL))
        q.enqueue(make_job("normal", priority=Priority.NORMAL))
        job = q.dequeue()
        assert job.job_id == "critical"

    def test_dequeue_marks_running(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        job = q.dequeue()
        assert job.status == JobStatus.RUNNING
        stored = q.get("j1")
        assert stored.status == JobStatus.RUNNING

    def test_dequeue_increments_attempt_count(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        job = q.dequeue()
        assert job.attempt_count == 1
        stored = q.get("j1")
        assert stored.attempt_count == 1

    def test_dequeue_sets_started_ts(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        job = q.dequeue()
        assert job.started_ts != ""
        datetime.fromisoformat(job.started_ts)

    def test_dequeue_empty_returns_none(self):
        q = fresh_queue()
        assert q.dequeue() is None

    def test_dequeue_only_pending(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.dequeue()  # moves to RUNNING
        # queue has no pending left
        assert q.dequeue() is None

    def test_dequeue_owner_filter(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="alice"))
        q.enqueue(make_job("j2", owner="bob"))
        job = q.dequeue(owner="bob")
        assert job.job_id == "j2"

    def test_dequeue_owner_filter_no_match(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="alice"))
        assert q.dequeue(owner="charlie") is None

    def test_dequeue_fifo_same_priority(self):
        q = fresh_queue()
        # Same priority — earlier created_ts should come first
        j1 = PriorityJob(job_id="first", payload="{}", priority=Priority.NORMAL,
                         created_ts="2025-01-01T09:00:00")
        j2 = PriorityJob(job_id="second", payload="{}", priority=Priority.NORMAL,
                         created_ts="2025-01-01T10:00:00")
        q.enqueue(j1)
        q.enqueue(j2)
        job = q.dequeue()
        assert job.job_id == "first"

    def test_complete_no_error_marks_done(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.dequeue()
        result = q.complete("j1")
        assert result is True
        stored = q.get("j1")
        assert stored.status == JobStatus.DONE
        assert stored.done_ts != ""

    def test_complete_with_error_marks_failed(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.dequeue()
        result = q.complete("j1", error="something went wrong")
        assert result is True
        stored = q.get("j1")
        assert stored.status == JobStatus.FAILED
        assert stored.error == "something went wrong"

    def test_complete_sets_done_ts(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.dequeue()
        q.complete("j1")
        stored = q.get("j1")
        datetime.fromisoformat(stored.done_ts)

    def test_complete_missing_returns_false(self):
        q = fresh_queue()
        assert q.complete("nonexistent") is False

    def test_cancel_pending_returns_true(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        result = q.cancel("j1")
        assert result is True
        stored = q.get("j1")
        assert stored.status == JobStatus.CANCELLED

    def test_cancel_running_returns_false(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.dequeue()
        result = q.cancel("j1")
        assert result is False
        stored = q.get("j1")
        assert stored.status == JobStatus.RUNNING

    def test_cancel_missing_returns_false(self):
        q = fresh_queue()
        assert q.cancel("nonexistent") is False

    def test_pending_count_all(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="a"))
        q.enqueue(make_job("j2", owner="b"))
        q.enqueue(make_job("j3", owner="a"))
        assert q.pending_count() == 3

    def test_pending_count_decreases_after_dequeue(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.enqueue(make_job("j2"))
        assert q.pending_count() == 2
        q.dequeue()
        assert q.pending_count() == 1

    def test_pending_count_by_owner(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="alice"))
        q.enqueue(make_job("j2", owner="alice"))
        q.enqueue(make_job("j3", owner="bob"))
        assert q.pending_count(owner="alice") == 2
        assert q.pending_count(owner="bob") == 1
        assert q.pending_count(owner="charlie") == 0

    def test_stats_has_all_statuses(self):
        q = fresh_queue()
        stats = q.stats()
        for s in JobStatus:
            assert s.value in stats

    def test_stats_counts(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.enqueue(make_job("j2"))
        q.enqueue(make_job("j3"))
        q.dequeue()          # j3 or highest pri → running
        stats = q.stats()
        assert stats["pending"] == 2
        assert stats["running"] == 1

    def test_stats_empty_queue(self):
        q = fresh_queue()
        stats = q.stats()
        assert all(v == 0 for v in stats.values())

    def test_critical_dequeued_before_low(self):
        q = fresh_queue()
        q.enqueue(make_job("low", priority=Priority.LOW))
        q.enqueue(make_job("high", priority=Priority.HIGH))
        q.enqueue(make_job("critical", priority=Priority.CRITICAL))
        q.enqueue(make_job("normal", priority=Priority.NORMAL))
        order = []
        while True:
            j = q.dequeue()
            if j is None:
                break
            order.append(j.job_id)
            q.complete(j.job_id)
        assert order == ["critical", "high", "normal", "low"]

    def test_get_after_complete(self):
        q = fresh_queue()
        q.enqueue(make_job("j1"))
        q.dequeue()
        q.complete("j1")
        stored = q.get("j1")
        assert stored.status == JobStatus.DONE

    def test_close_does_not_raise(self):
        q = fresh_queue()
        q.close()  # should not raise


# ---------------------------------------------------------------------------
# SchedulerConfig
# ---------------------------------------------------------------------------

class TestSchedulerConfig:
    def test_defaults(self):
        cfg = SchedulerConfig()
        assert cfg.max_concurrent == 4
        assert cfg.fair_share_window == 10

    def test_custom_values(self):
        cfg = SchedulerConfig(max_concurrent=8, fair_share_window=5)
        assert cfg.max_concurrent == 8
        assert cfg.fair_share_window == 5


# ---------------------------------------------------------------------------
# FairShareScheduler
# ---------------------------------------------------------------------------

class TestFairShareScheduler:
    def test_next_job_returns_job(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="alice"))
        sched = FairShareScheduler(q)
        job = sched.next_job()
        assert job is not None
        assert job.job_id == "j1"

    def test_next_job_empty_queue_returns_none(self):
        q = fresh_queue()
        sched = FairShareScheduler(q)
        assert sched.next_job() is None

    def test_next_job_marks_running(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="alice"))
        sched = FairShareScheduler(q)
        job = sched.next_job()
        assert job.status == JobStatus.RUNNING

    def test_fair_share_picks_owner_with_fewest_dequeued(self):
        """Alice has 2 jobs already dequeued, Bob has 0 — Bob should go next."""
        q = fresh_queue()
        cfg = SchedulerConfig(fair_share_window=10)
        sched = FairShareScheduler(q, cfg)
        # Add pending jobs for both owners
        q.enqueue(make_job("a1", owner="alice", priority=Priority.CRITICAL))
        q.enqueue(make_job("b1", owner="bob", priority=Priority.LOW))
        # Simulate alice already has 2 in this cycle
        sched._owner_counts["alice"] = 2
        sched._owner_counts["bob"] = 0
        job = sched.next_job()
        # Bob should be picked even though alice has higher priority job
        assert job.owner == "bob"

    def test_fair_share_window_switches_owner(self):
        """After fair_share_window jobs for alice, bob gets scheduled."""
        q = fresh_queue()
        cfg = SchedulerConfig(fair_share_window=2)
        sched = FairShareScheduler(q, cfg)
        # 3 jobs for alice, 1 for bob
        for i in range(3):
            q.enqueue(make_job(f"a{i}", owner="alice", priority=Priority.NORMAL))
        q.enqueue(make_job("b1", owner="bob", priority=Priority.NORMAL))

        owners = []
        for _ in range(4):
            job = sched.next_job()
            if job:
                owners.append(job.owner)
                sched._queue.complete(job.job_id)

        # bob must appear — fair share window 2 means alice can't grab all 3 before bob
        assert "bob" in owners

    def test_fair_share_window_resets_when_all_exhausted(self):
        """When all owners hit the window, counts reset and scheduling continues."""
        q = fresh_queue()
        cfg = SchedulerConfig(fair_share_window=1)
        sched = FairShareScheduler(q, cfg)
        q.enqueue(make_job("a1", owner="alice"))
        q.enqueue(make_job("a2", owner="alice"))

        # After first dequeue alice is at window=1; only alice, so reset should happen
        j1 = sched.next_job()
        assert j1 is not None
        sched._queue.complete(j1.job_id)

        # Second job — alice was at window, reset should happen and alice gets it
        j2 = sched.next_job()
        assert j2 is not None

    def test_reset_cycle_clears_counts(self):
        q = fresh_queue()
        sched = FairShareScheduler(q)
        sched._owner_counts["alice"] = 5
        sched._owner_counts["bob"] = 3
        sched.reset_cycle()
        assert sched._owner_counts == {}

    def test_owner_counts_incremented(self):
        q = fresh_queue()
        q.enqueue(make_job("j1", owner="alice"))
        sched = FairShareScheduler(q)
        sched.next_job()
        assert sched._owner_counts.get("alice", 0) == 1

    def test_alphabetical_tiebreak(self):
        """When two owners have equal dequeue counts, alphabetically-first wins."""
        q = fresh_queue()
        cfg = SchedulerConfig(fair_share_window=10)
        sched = FairShareScheduler(q, cfg)
        q.enqueue(make_job("z1", owner="zeta", priority=Priority.NORMAL))
        q.enqueue(make_job("a1", owner="alpha", priority=Priority.NORMAL))
        # Both at 0 dequeued — alpha comes first alphabetically
        job = sched.next_job()
        assert job.owner == "alpha"

    def test_multiple_cycles(self):
        """Scheduler correctly handles multiple reset cycles."""
        q = fresh_queue()
        cfg = SchedulerConfig(fair_share_window=1)
        sched = FairShareScheduler(q, cfg)
        for i in range(4):
            q.enqueue(make_job(f"j{i}", owner="alice"))

        completed = 0
        for _ in range(4):
            job = sched.next_job()
            if job:
                sched._queue.complete(job.job_id)
                completed += 1

        assert completed == 4

    def test_scheduler_with_custom_config(self):
        q = fresh_queue()
        cfg = SchedulerConfig(max_concurrent=2, fair_share_window=3)
        sched = FairShareScheduler(q, cfg)
        assert sched._config.max_concurrent == 2
        assert sched._config.fair_share_window == 3

    def test_next_job_no_owner_filter_when_no_pending_for_eligible(self):
        """When only one owner exists and is at window, reset and serve them."""
        q = fresh_queue()
        cfg = SchedulerConfig(fair_share_window=1)
        sched = FairShareScheduler(q, cfg)
        q.enqueue(make_job("j1", owner="solo"))
        q.enqueue(make_job("j2", owner="solo"))
        sched._owner_counts["solo"] = 1  # already at window

        # All owners exhausted → reset → solo gets served
        job = sched.next_job()
        assert job is not None
        assert job.owner == "solo"
        # Counts should have been reset and then incremented
        assert sched._owner_counts.get("solo", 0) == 1
