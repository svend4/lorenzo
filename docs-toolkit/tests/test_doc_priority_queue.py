"""Tests for docstoolkit.doc_priority_queue."""
from __future__ import annotations

import pytest

from docstoolkit.doc_priority_queue import (
    DocPriorityQueue,
    Priority,
    QueueStats,
    Task,
    TaskState,
)


# ---------------------------------------------------------------------------
class TestTaskState:
    def test_has_queued(self):
        assert TaskState.QUEUED.value == "queued"

    def test_has_in_progress(self):
        assert TaskState.IN_PROGRESS.value == "in_progress"

    def test_has_completed(self):
        assert TaskState.COMPLETED.value == "completed"

    def test_has_failed(self):
        assert TaskState.FAILED.value == "failed"

    def test_has_expired(self):
        assert TaskState.EXPIRED.value == "expired"


# ---------------------------------------------------------------------------
class TestPriority:
    def test_order_highest_greater_than_high(self):
        assert Priority.HIGHEST > Priority.HIGH

    def test_order_high_greater_than_normal(self):
        assert Priority.HIGH > Priority.NORMAL

    def test_order_normal_greater_than_low(self):
        assert Priority.NORMAL > Priority.LOW

    def test_order_low_greater_than_lowest(self):
        assert Priority.LOW > Priority.LOWEST

    def test_int_values(self):
        assert int(Priority.LOWEST) == 0
        assert int(Priority.HIGHEST) == 4


# ---------------------------------------------------------------------------
class TestTask:
    def test_create_minimal(self):
        t = Task(
            task_id="abc",
            doc_id="doc1",
            action="reindex",
            priority=Priority.NORMAL,
        )
        assert t.task_id == "abc"
        assert t.doc_id == "doc1"
        assert t.action == "reindex"
        assert t.priority == Priority.NORMAL
        assert t.state == TaskState.QUEUED
        assert t.payload == {}
        assert t.attempts == 0
        assert t.max_attempts == 3
        assert t.last_error is None

    def test_default_payload_is_independent(self):
        a = Task(task_id="a", doc_id="d", action="x", priority=Priority.LOW)
        b = Task(task_id="b", doc_id="d", action="x", priority=Priority.LOW)
        a.payload["k"] = 1
        assert b.payload == {}

    def test_deadline_optional(self):
        t = Task(task_id="a", doc_id="d", action="x", priority=Priority.LOW)
        assert t.deadline is None


# ---------------------------------------------------------------------------
class TestQueueStats:
    def test_construct(self):
        s = QueueStats(
            total=10,
            queued=3,
            in_progress=1,
            completed=4,
            failed=1,
            expired=1,
            by_priority={Priority.HIGH: 2},
        )
        assert s.total == 10
        assert s.queued == 3
        assert s.in_progress == 1
        assert s.completed == 4
        assert s.failed == 1
        assert s.expired == 1
        assert s.by_priority[Priority.HIGH] == 2
        assert s.oldest_queued_age is None


# ---------------------------------------------------------------------------
class TestEnqueue:
    def test_returns_task(self):
        q = DocPriorityQueue()
        t = q.enqueue("doc1", "reindex")
        assert isinstance(t, Task)
        assert t.doc_id == "doc1"
        assert t.action == "reindex"
        assert t.state == TaskState.QUEUED

    def test_unique_task_id(self):
        q = DocPriorityQueue()
        a = q.enqueue("d", "x")
        b = q.enqueue("d", "x")
        assert a.task_id != b.task_id

    def test_priority_default_normal(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        assert t.priority == Priority.NORMAL

    def test_priority_explicit(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", priority=Priority.HIGHEST)
        assert t.priority == Priority.HIGHEST

    def test_payload_copied(self):
        q = DocPriorityQueue()
        payload = {"key": "val"}
        t = q.enqueue("d", "x", payload=payload)
        payload["key"] = "changed"
        assert t.payload == {"key": "val"}

    def test_payload_none_becomes_empty_dict(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        assert t.payload == {}

    def test_deadline_stored(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", deadline=100.0)
        assert t.deadline == 100.0

    def test_max_attempts_stored(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", max_attempts=5)
        assert t.max_attempts == 5

    def test_created_at(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", now=42.5)
        assert t.created_at == 42.5


# ---------------------------------------------------------------------------
class TestDequeue:
    def test_empty_returns_none(self):
        q = DocPriorityQueue()
        assert q.dequeue() is None

    def test_marks_in_progress(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        t = q.dequeue(now=10.0)
        assert t.state == TaskState.IN_PROGRESS
        assert t.started_at == 10.0

    def test_increments_attempts(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        t = q.dequeue()
        assert t.attempts == 1

    def test_returns_highest_priority(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a", priority=Priority.LOW)
        q.enqueue("d", "b", priority=Priority.HIGHEST)
        q.enqueue("d", "c", priority=Priority.NORMAL)
        t = q.dequeue()
        assert t.action == "b"

    def test_skips_in_progress(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a")
        q.enqueue("d", "b")
        first = q.dequeue()
        second = q.dequeue()
        assert first.task_id != second.task_id


# ---------------------------------------------------------------------------
class TestPeek:
    def test_empty_returns_none(self):
        q = DocPriorityQueue()
        assert q.peek() is None

    def test_does_not_change_state(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        t = q.peek()
        assert t.state == TaskState.QUEUED
        # peek again returns same task
        t2 = q.peek()
        assert t2.task_id == t.task_id

    def test_returns_highest_priority(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a", priority=Priority.LOW)
        q.enqueue("d", "b", priority=Priority.HIGH)
        t = q.peek()
        assert t.action == "b"


# ---------------------------------------------------------------------------
class TestComplete:
    def test_marks_completed(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.dequeue()
        assert q.complete(t.task_id, now=50.0) is True
        got = q.get_task(t.task_id)
        assert got.state == TaskState.COMPLETED
        assert got.completed_at == 50.0

    def test_unknown_id_returns_false(self):
        q = DocPriorityQueue()
        assert q.complete("nope") is False

    def test_idempotent_complete_returns_false(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.dequeue()
        q.complete(t.task_id)
        assert q.complete(t.task_id) is False

    def test_complete_a_queued_task(self):
        """Direct completion without dequeue is allowed (no state guard)."""
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        assert q.complete(t.task_id) is True


# ---------------------------------------------------------------------------
class TestFail:
    def test_unknown_id_returns_false(self):
        q = DocPriorityQueue()
        assert q.fail("nope") is False

    def test_records_error(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.dequeue()
        q.fail(t.task_id, error="boom", retry=False)
        got = q.get_task(t.task_id)
        assert got.last_error == "boom"


# ---------------------------------------------------------------------------
class TestFailNoRetry:
    def test_marks_failed(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.dequeue()
        assert q.fail(t.task_id, error="err", retry=False, now=99.0) is True
        got = q.get_task(t.task_id)
        assert got.state == TaskState.FAILED
        assert got.completed_at == 99.0

    def test_failed_already_failed_returns_false(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.dequeue()
        q.fail(t.task_id, retry=False)
        assert q.fail(t.task_id, retry=False) is False


# ---------------------------------------------------------------------------
class TestFailRetryUntilMax:
    def test_first_failure_requeues(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", max_attempts=3)
        q.dequeue()  # attempts=1
        q.fail(t.task_id, retry=True)
        got = q.get_task(t.task_id)
        assert got.state == TaskState.QUEUED
        assert got.started_at is None
        assert got.attempts == 1

    def test_exhausts_retries(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", max_attempts=2)
        # attempt 1
        q.dequeue()
        q.fail(t.task_id, retry=True)
        got = q.get_task(t.task_id)
        assert got.state == TaskState.QUEUED  # requeued
        # attempt 2
        q.dequeue()
        q.fail(t.task_id, retry=True)
        got = q.get_task(t.task_id)
        # attempts now equals max -> FAILED
        assert got.state == TaskState.FAILED

    def test_retry_increments_attempts_on_redequeue(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", max_attempts=3)
        q.dequeue()
        q.fail(t.task_id, retry=True)
        again = q.dequeue()
        assert again.attempts == 2

    def test_max_attempts_one_no_retry(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", max_attempts=1)
        q.dequeue()  # attempts=1
        q.fail(t.task_id, retry=True)
        got = q.get_task(t.task_id)
        # 1 attempt used, max 1 -> failed
        assert got.state == TaskState.FAILED


# ---------------------------------------------------------------------------
class TestCancel:
    def test_removes_task(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        assert q.cancel(t.task_id) is True
        assert q.get_task(t.task_id) is None

    def test_unknown_returns_false(self):
        q = DocPriorityQueue()
        assert q.cancel("nope") is False

    def test_cancel_reduces_queue_size(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.enqueue("d", "y")
        q.cancel(t.task_id)
        assert q.queue_size() == 1


# ---------------------------------------------------------------------------
class TestExpireOverdue:
    def test_no_deadline_no_expiry(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        assert q.expire_overdue(now=100.0) == 0

    def test_overdue_marked_expired(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", deadline=50.0, now=0.0)
        n = q.expire_overdue(now=60.0)
        assert n == 1
        assert q.get_task(t.task_id).state == TaskState.EXPIRED

    def test_not_overdue_stays_queued(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", deadline=100.0, now=0.0)
        q.expire_overdue(now=50.0)
        assert q.get_task(t.task_id).state == TaskState.QUEUED

    def test_only_queued_expires(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", deadline=50.0, now=0.0)
        q.dequeue()  # now IN_PROGRESS
        n = q.expire_overdue(now=100.0)
        assert n == 0
        assert q.get_task(t.task_id).state == TaskState.IN_PROGRESS

    def test_returns_count(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a", deadline=10.0)
        q.enqueue("d", "b", deadline=20.0)
        q.enqueue("d", "c", deadline=200.0)
        assert q.expire_overdue(now=50.0) == 2


# ---------------------------------------------------------------------------
class TestGetTask:
    def test_returns_task(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        assert q.get_task(t.task_id) is t

    def test_unknown_returns_none(self):
        q = DocPriorityQueue()
        assert q.get_task("nope") is None


# ---------------------------------------------------------------------------
class TestTasksForDoc:
    def test_returns_matching(self):
        q = DocPriorityQueue()
        q.enqueue("doc1", "a")
        q.enqueue("doc2", "b")
        q.enqueue("doc1", "c")
        results = q.tasks_for_doc("doc1")
        assert len(results) == 2
        actions = {t.action for t in results}
        assert actions == {"a", "c"}

    def test_empty_for_unknown_doc(self):
        q = DocPriorityQueue()
        q.enqueue("doc1", "a")
        assert q.tasks_for_doc("unknown") == []


# ---------------------------------------------------------------------------
class TestTasksByState:
    def test_filters_by_state(self):
        q = DocPriorityQueue()
        t1 = q.enqueue("d", "a")
        t2 = q.enqueue("d", "b")
        q.dequeue()  # one becomes IN_PROGRESS
        queued = q.tasks_by_state(TaskState.QUEUED)
        in_progress = q.tasks_by_state(TaskState.IN_PROGRESS)
        assert len(queued) == 1
        assert len(in_progress) == 1

    def test_empty_state(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        assert q.tasks_by_state(TaskState.COMPLETED) == []


# ---------------------------------------------------------------------------
class TestTasksByAction:
    def test_filters_by_action(self):
        q = DocPriorityQueue()
        q.enqueue("d1", "reindex")
        q.enqueue("d2", "reindex")
        q.enqueue("d3", "summarize")
        reindex = q.tasks_by_action("reindex")
        assert len(reindex) == 2

    def test_unknown_action_empty(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        assert q.tasks_by_action("nope") == []


# ---------------------------------------------------------------------------
class TestQueueSize:
    def test_counts_queued_only(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a")
        q.enqueue("d", "b")
        q.dequeue()
        assert q.queue_size() == 1

    def test_empty(self):
        q = DocPriorityQueue()
        assert q.queue_size() == 0


# ---------------------------------------------------------------------------
class TestInProgressSize:
    def test_counts_in_progress(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a")
        q.enqueue("d", "b")
        q.dequeue()
        assert q.in_progress_size() == 1

    def test_empty(self):
        q = DocPriorityQueue()
        assert q.in_progress_size() == 0


# ---------------------------------------------------------------------------
class TestNextDeadline:
    def test_no_deadlines(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x")
        assert q.next_deadline() is None

    def test_earliest_deadline(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a", deadline=100.0)
        q.enqueue("d", "b", deadline=50.0)
        q.enqueue("d", "c", deadline=200.0)
        assert q.next_deadline() == 50.0

    def test_ignores_non_queued(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "a", deadline=10.0)
        q.dequeue()  # IN_PROGRESS
        q.enqueue("d", "b", deadline=100.0)
        assert q.next_deadline() == 100.0


# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        q = DocPriorityQueue()
        s = q.stats()
        assert s.total == 0
        assert s.queued == 0
        assert s.oldest_queued_age is None

    def test_counts(self):
        q = DocPriorityQueue()
        t1 = q.enqueue("d", "a", priority=Priority.HIGH)
        q.enqueue("d", "b", priority=Priority.LOW)
        t3 = q.enqueue("d", "c", priority=Priority.NORMAL)
        q.dequeue()  # one IN_PROGRESS
        q.complete(t3.task_id)
        s = q.stats()
        assert s.total == 3
        assert s.in_progress == 1
        assert s.completed == 1
        assert s.queued == 1

    def test_by_priority(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a", priority=Priority.HIGH)
        q.enqueue("d", "b", priority=Priority.HIGH)
        q.enqueue("d", "c", priority=Priority.LOW)
        s = q.stats()
        assert s.by_priority[Priority.HIGH] == 2
        assert s.by_priority[Priority.LOW] == 1

    def test_oldest_queued_age(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a", now=0.0)
        q.enqueue("d", "b", now=10.0)
        s = q.stats(now=20.0)
        assert s.oldest_queued_age == 20.0


# ---------------------------------------------------------------------------
class TestClear:
    def test_removes_all(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a")
        q.enqueue("d", "b")
        q.clear()
        assert q.total_tasks == 0
        assert q.queue_size() == 0


# ---------------------------------------------------------------------------
class TestTotalTasks:
    def test_initial_zero(self):
        q = DocPriorityQueue()
        assert q.total_tasks == 0

    def test_counts_all_states(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a")
        t = q.enqueue("d", "b")
        q.dequeue()
        q.complete(t.task_id)
        # 1 in_progress + 1 completed = 2
        assert q.total_tasks == 2


# ---------------------------------------------------------------------------
class TestPriorityOrder:
    def test_highest_first(self):
        q = DocPriorityQueue()
        q.enqueue("d", "low", priority=Priority.LOW)
        q.enqueue("d", "highest", priority=Priority.HIGHEST)
        q.enqueue("d", "normal", priority=Priority.NORMAL)
        q.enqueue("d", "high", priority=Priority.HIGH)
        q.enqueue("d", "lowest", priority=Priority.LOWEST)
        order = []
        while True:
            t = q.dequeue()
            if t is None:
                break
            order.append(t.action)
            q.complete(t.task_id)
        assert order == ["highest", "high", "normal", "low", "lowest"]


# ---------------------------------------------------------------------------
class TestDeadlineTiebreak:
    def test_earlier_deadline_first_at_same_priority(self):
        q = DocPriorityQueue()
        q.enqueue("d", "late", priority=Priority.NORMAL, deadline=200.0)
        q.enqueue("d", "early", priority=Priority.NORMAL, deadline=100.0)
        t = q.dequeue()
        assert t.action == "early"

    def test_no_deadline_after_deadline(self):
        q = DocPriorityQueue()
        q.enqueue("d", "none", priority=Priority.NORMAL)
        q.enqueue("d", "has", priority=Priority.NORMAL, deadline=50.0)
        t = q.dequeue()
        assert t.action == "has"

    def test_created_at_tiebreak(self):
        q = DocPriorityQueue()
        q.enqueue("d", "second", priority=Priority.NORMAL, now=10.0)
        q.enqueue("d", "first", priority=Priority.NORMAL, now=5.0)
        t = q.dequeue()
        assert t.action == "first"

    def test_priority_dominates_deadline(self):
        q = DocPriorityQueue()
        q.enqueue("d", "low_early", priority=Priority.LOW, deadline=10.0)
        q.enqueue("d", "high_late", priority=Priority.HIGH, deadline=1000.0)
        t = q.dequeue()
        assert t.action == "high_late"


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_enqueue_after_clear(self):
        q = DocPriorityQueue()
        q.enqueue("d", "a")
        q.clear()
        t = q.enqueue("d", "b")
        assert q.total_tasks == 1
        assert q.dequeue().task_id == t.task_id

    def test_complete_unknown_task(self):
        q = DocPriorityQueue()
        assert q.complete("missing") is False

    def test_cancel_in_progress(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x")
        q.dequeue()
        assert q.cancel(t.task_id) is True
        assert q.get_task(t.task_id) is None

    def test_expire_overdue_idempotent(self):
        q = DocPriorityQueue()
        q.enqueue("d", "x", deadline=10.0)
        q.expire_overdue(now=50.0)
        # second call: now state is EXPIRED, not QUEUED, so 0
        assert q.expire_overdue(now=50.0) == 0

    def test_fail_does_not_re_increment_attempts(self):
        """fail() itself shouldn't increment attempts; dequeue does."""
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", max_attempts=3)
        q.dequeue()  # attempts=1
        q.fail(t.task_id, retry=True)
        got = q.get_task(t.task_id)
        assert got.attempts == 1

    def test_payload_round_trip(self):
        q = DocPriorityQueue()
        t = q.enqueue("d", "x", payload={"nested": {"k": 1}})
        got = q.get_task(t.task_id)
        assert got.payload == {"nested": {"k": 1}}
