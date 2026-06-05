"""Tests for docstoolkit.dlq — dead letter queue, retry, poison pill detection."""
import time
import pytest
from docstoolkit.dlq import (
    DeadLetterItem, FailureReason,
    DeadLetterQueue,
    RetryPolicy, RetryResult, execute_with_retry,
    PoisonPillDetector, PoisonReport,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_item(
    job_id="job-1",
    payload='{"x": 1}',
    reason=FailureReason.ERROR,
    attempt_count=1,
    resolved=False,
    tags=None,
    error_message="",
    first_failure_ts="",
    last_failure_ts="",
):
    return DeadLetterItem(
        job_id=job_id,
        payload=payload,
        reason=reason,
        error_message=error_message,
        attempt_count=attempt_count,
        first_failure_ts=first_failure_ts,
        last_failure_ts=last_failure_ts,
        resolved=resolved,
        tags=tags if tags is not None else [],
    )


# ===========================================================================
# FailureReason
# ===========================================================================

class TestFailureReason:
    def test_timeout_value(self):
        assert FailureReason.TIMEOUT == "timeout"

    def test_error_value(self):
        assert FailureReason.ERROR == "error"

    def test_validation_value(self):
        assert FailureReason.VALIDATION == "validation"

    def test_dependency_value(self):
        assert FailureReason.DEPENDENCY == "dependency"

    def test_unknown_value(self):
        assert FailureReason.UNKNOWN == "unknown"

    def test_is_str_subclass(self):
        assert isinstance(FailureReason.ERROR, str)

    def test_five_members(self):
        assert len(FailureReason) == 5


# ===========================================================================
# DeadLetterItem
# ===========================================================================

class TestDeadLetterItem:
    def test_required_fields(self):
        item = make_item()
        assert item.job_id == "job-1"
        assert item.payload == '{"x": 1}'
        assert item.reason == FailureReason.ERROR

    def test_default_attempt_count(self):
        item = make_item()
        assert item.attempt_count == 1

    def test_default_resolved_false(self):
        item = make_item()
        assert item.resolved is False

    def test_default_tags_empty_list(self):
        item = make_item()
        assert item.tags == []

    def test_default_error_message_empty(self):
        item = make_item()
        assert item.error_message == ""

    def test_post_init_sets_first_failure_ts(self):
        item = make_item(first_failure_ts="")
        assert item.first_failure_ts != ""

    def test_post_init_sets_last_failure_ts(self):
        item = make_item(last_failure_ts="")
        assert item.last_failure_ts != ""

    def test_post_init_preserves_provided_first_ts(self):
        ts = "2026-01-01T00:00:00"
        item = make_item(first_failure_ts=ts)
        assert item.first_failure_ts == ts

    def test_post_init_preserves_provided_last_ts(self):
        ts = "2026-01-01T00:00:00"
        item = make_item(last_failure_ts=ts)
        assert item.last_failure_ts == ts

    def test_mark_resolved_sets_true(self):
        item = make_item()
        item.mark_resolved()
        assert item.resolved is True

    def test_mark_resolved_idempotent(self):
        item = make_item()
        item.mark_resolved()
        item.mark_resolved()
        assert item.resolved is True

    def test_increment_attempt_increases_count(self):
        item = make_item(attempt_count=1)
        item.increment_attempt()
        assert item.attempt_count == 2

    def test_increment_attempt_multiple_times(self):
        item = make_item(attempt_count=1)
        item.increment_attempt()
        item.increment_attempt()
        assert item.attempt_count == 3

    def test_increment_attempt_updates_last_failure_ts(self):
        item = make_item(last_failure_ts="2020-01-01T00:00:00")
        item.increment_attempt()
        assert item.last_failure_ts != "2020-01-01T00:00:00"

    def test_age_seconds_positive(self):
        item = make_item()
        assert item.age_seconds() >= 0.0

    def test_age_seconds_zero_for_bad_ts(self):
        item = make_item(first_failure_ts="not-a-timestamp")
        assert item.age_seconds() == 0.0

    def test_age_seconds_known_ts(self):
        # Item created with a past timestamp should have age > 0
        item = make_item(first_failure_ts="2020-01-01T00:00:00")
        assert item.age_seconds() > 0.0

    def test_tags_preserved(self):
        item = make_item(tags=["urgent", "retry"])
        assert item.tags == ["urgent", "retry"]


# ===========================================================================
# DeadLetterQueue
# ===========================================================================

class TestDeadLetterQueue:
    def setup_method(self):
        self.q = DeadLetterQueue()  # in-memory

    def teardown_method(self):
        self.q.close()

    def test_push_and_get_roundtrip(self):
        item = make_item(job_id="j1")
        self.q.push(item)
        fetched = self.q.get("j1")
        assert fetched is not None
        assert fetched.job_id == "j1"

    def test_get_returns_none_for_missing(self):
        assert self.q.get("nonexistent") is None

    def test_push_preserves_payload(self):
        item = make_item(job_id="j2", payload='{"key": "value"}')
        self.q.push(item)
        assert self.q.get("j2").payload == '{"key": "value"}'

    def test_push_preserves_reason(self):
        item = make_item(job_id="j3", reason=FailureReason.TIMEOUT)
        self.q.push(item)
        assert self.q.get("j3").reason == FailureReason.TIMEOUT

    def test_push_preserves_error_message(self):
        item = make_item(job_id="j4", error_message="boom")
        self.q.push(item)
        assert self.q.get("j4").error_message == "boom"

    def test_push_preserves_attempt_count(self):
        item = make_item(job_id="j5", attempt_count=5)
        self.q.push(item)
        assert self.q.get("j5").attempt_count == 5

    def test_push_replaces_existing(self):
        item1 = make_item(job_id="j6", error_message="first")
        item2 = make_item(job_id="j6", error_message="second")
        self.q.push(item1)
        self.q.push(item2)
        assert self.q.get("j6").error_message == "second"

    def test_list_pending_returns_only_unresolved(self):
        self.q.push(make_item(job_id="pending1"))
        self.q.push(make_item(job_id="pending2"))
        resolved = make_item(job_id="resolved1")
        self.q.push(resolved)
        self.q.resolve("resolved1")
        pending = self.q.list_pending()
        ids = [i.job_id for i in pending]
        assert "pending1" in ids
        assert "pending2" in ids
        assert "resolved1" not in ids

    def test_list_pending_sorted_oldest_first(self):
        # Use explicit timestamps to control order
        old = make_item(job_id="old", first_failure_ts="2025-01-01T00:00:00")
        new = make_item(job_id="new", first_failure_ts="2025-06-01T00:00:00")
        self.q.push(new)
        self.q.push(old)
        items = self.q.list_pending()
        ids = [i.job_id for i in items]
        assert ids.index("old") < ids.index("new")

    def test_list_pending_empty_queue(self):
        assert self.q.list_pending() == []

    def test_resolve_returns_true_for_found(self):
        self.q.push(make_item(job_id="rx"))
        assert self.q.resolve("rx") is True

    def test_resolve_returns_false_for_missing(self):
        assert self.q.resolve("no-such-job") is False

    def test_resolve_marks_resolved(self):
        self.q.push(make_item(job_id="ry"))
        self.q.resolve("ry")
        assert self.q.get("ry").resolved is True

    def test_increment_attempt_increases_count(self):
        self.q.push(make_item(job_id="ia1", attempt_count=2))
        self.q.increment_attempt("ia1")
        assert self.q.get("ia1").attempt_count == 3

    def test_increment_attempt_returns_true_found(self):
        self.q.push(make_item(job_id="ia2"))
        assert self.q.increment_attempt("ia2") is True

    def test_increment_attempt_returns_false_missing(self):
        assert self.q.increment_attempt("no-such") is False

    def test_stats_keys(self):
        stats = self.q.stats()
        assert "total" in stats
        assert "pending" in stats
        assert "resolved" in stats

    def test_stats_counts_correct(self):
        self.q.push(make_item(job_id="s1"))
        self.q.push(make_item(job_id="s2"))
        self.q.push(make_item(job_id="s3"))
        self.q.resolve("s1")
        stats = self.q.stats()
        assert stats["total"] == 3
        assert stats["pending"] == 2
        assert stats["resolved"] == 1

    def test_stats_empty_queue(self):
        stats = self.q.stats()
        assert stats == {"total": 0, "pending": 0, "resolved": 0}

    def test_purge_resolved_removes_resolved(self):
        self.q.push(make_item(job_id="p1"))
        self.q.push(make_item(job_id="p2"))
        self.q.resolve("p1")
        self.q.purge_resolved()
        assert self.q.get("p1") is None
        assert self.q.get("p2") is not None

    def test_purge_resolved_returns_count(self):
        self.q.push(make_item(job_id="pr1"))
        self.q.push(make_item(job_id="pr2"))
        self.q.resolve("pr1")
        self.q.resolve("pr2")
        count = self.q.purge_resolved()
        assert count == 2

    def test_purge_resolved_zero_when_none_resolved(self):
        self.q.push(make_item(job_id="pz1"))
        assert self.q.purge_resolved() == 0

    def test_tags_roundtrip(self):
        item = make_item(job_id="t1", tags=["alpha", "beta", "gamma"])
        self.q.push(item)
        fetched = self.q.get("t1")
        assert fetched.tags == ["alpha", "beta", "gamma"]

    def test_tags_empty_list_roundtrip(self):
        item = make_item(job_id="t2", tags=[])
        self.q.push(item)
        assert self.q.get("t2").tags == []

    def test_resolved_false_roundtrip(self):
        item = make_item(job_id="rf1", resolved=False)
        self.q.push(item)
        assert self.q.get("rf1").resolved is False

    def test_resolved_true_roundtrip(self):
        item = make_item(job_id="rf2")
        self.q.push(item)
        self.q.resolve("rf2")
        assert self.q.get("rf2").resolved is True


# ===========================================================================
# RetryPolicy
# ===========================================================================

class TestRetryPolicy:
    def test_default_max_attempts(self):
        p = RetryPolicy()
        assert p.max_attempts == 3

    def test_default_backoff_base(self):
        p = RetryPolicy()
        assert p.backoff_base == 1.0

    def test_default_backoff_multiplier(self):
        p = RetryPolicy()
        assert p.backoff_multiplier == 2.0

    def test_default_max_backoff(self):
        p = RetryPolicy()
        assert p.max_backoff == 60.0

    def test_wait_time_attempt_0_equals_base(self):
        p = RetryPolicy(backoff_base=2.0, backoff_multiplier=2.0)
        # 2.0 * (2.0 ** 0) = 2.0
        assert p.wait_time(0) == pytest.approx(2.0)

    def test_wait_time_attempt_1(self):
        p = RetryPolicy(backoff_base=1.0, backoff_multiplier=2.0)
        # 1.0 * (2.0 ** 1) = 2.0
        assert p.wait_time(1) == pytest.approx(2.0)

    def test_wait_time_attempt_2(self):
        p = RetryPolicy(backoff_base=1.0, backoff_multiplier=2.0)
        # 1.0 * (2.0 ** 2) = 4.0
        assert p.wait_time(2) == pytest.approx(4.0)

    def test_wait_time_capped_at_max(self):
        p = RetryPolicy(backoff_base=1.0, backoff_multiplier=2.0, max_backoff=3.0)
        # 1.0 * (2.0 ** 3) = 8.0, capped at 3.0
        assert p.wait_time(3) == pytest.approx(3.0)

    def test_wait_time_not_exceed_max_backoff(self):
        p = RetryPolicy(backoff_base=10.0, backoff_multiplier=10.0, max_backoff=5.0)
        assert p.wait_time(5) <= 5.0

    def test_custom_policy(self):
        p = RetryPolicy(max_attempts=5, backoff_base=0.5, backoff_multiplier=3.0, max_backoff=30.0)
        assert p.max_attempts == 5
        assert p.wait_time(0) == pytest.approx(0.5)


# ===========================================================================
# RetryResult
# ===========================================================================

class TestRetryResult:
    def test_success_field(self):
        r = RetryResult(success=True, attempts=1)
        assert r.success is True

    def test_attempts_field(self):
        r = RetryResult(success=True, attempts=3)
        assert r.attempts == 3

    def test_result_field_default_none(self):
        r = RetryResult(success=True, attempts=1)
        assert r.result is None

    def test_last_error_default_empty(self):
        r = RetryResult(success=False, attempts=1)
        assert r.last_error == ""

    def test_total_wait_ms_default_zero(self):
        r = RetryResult(success=True, attempts=1)
        assert r.total_wait_ms == 0.0


# ===========================================================================
# execute_with_retry
# ===========================================================================

class TestExecuteWithRetry:
    def test_success_on_first_try(self):
        result = execute_with_retry(lambda: 42)
        assert result.success is True
        assert result.attempts == 1

    def test_result_contains_return_value(self):
        result = execute_with_retry(lambda: "hello")
        assert result.result == "hello"

    def test_no_wait_on_first_success(self):
        result = execute_with_retry(lambda: True)
        assert result.total_wait_ms == 0.0

    def test_fails_once_then_succeeds(self):
        calls = [0]
        def fn():
            calls[0] += 1
            if calls[0] == 1:
                raise ValueError("first fail")
            return "ok"
        result = execute_with_retry(fn, RetryPolicy(max_attempts=3))
        assert result.success is True
        assert result.attempts == 2

    def test_fails_once_result_correct(self):
        calls = [0]
        def fn():
            calls[0] += 1
            if calls[0] < 2:
                raise RuntimeError("nope")
            return 99
        result = execute_with_retry(fn, RetryPolicy(max_attempts=3))
        assert result.result == 99

    def test_always_fails(self):
        def fn():
            raise RuntimeError("always")
        result = execute_with_retry(fn, RetryPolicy(max_attempts=3))
        assert result.success is False

    def test_always_fails_attempts_equals_max(self):
        def fn():
            raise RuntimeError("always")
        result = execute_with_retry(fn, RetryPolicy(max_attempts=4))
        assert result.attempts == 4

    def test_last_error_set_on_failure(self):
        def fn():
            raise ValueError("bad input")
        result = execute_with_retry(fn, RetryPolicy(max_attempts=2))
        assert "bad input" in result.last_error

    def test_last_error_empty_on_success(self):
        result = execute_with_retry(lambda: 1)
        assert result.last_error == ""

    def test_total_wait_ms_accumulates(self):
        # policy: base=1.0, mult=2.0, max=60 → waits after attempt 0 = 1.0s, attempt 1 = 2.0s
        # 3 failures: waits are added after attempt 0 and 1 (not after last)
        def fn():
            raise RuntimeError("x")
        policy = RetryPolicy(max_attempts=3, backoff_base=1.0, backoff_multiplier=2.0)
        result = execute_with_retry(fn, policy)
        # wait after attempt 0: 1.0s, after attempt 1: 2.0s → total 3.0s = 3000ms
        assert result.total_wait_ms == pytest.approx(3000.0)

    def test_total_wait_ms_two_failures_one_success(self):
        calls = [0]
        def fn():
            calls[0] += 1
            if calls[0] < 3:
                raise RuntimeError("fail")
            return "done"
        policy = RetryPolicy(max_attempts=5, backoff_base=1.0, backoff_multiplier=2.0)
        result = execute_with_retry(fn, policy)
        # waits after attempt 0: 1.0s, after attempt 1: 2.0s → 3000ms
        assert result.total_wait_ms == pytest.approx(3000.0)

    def test_default_policy_used_when_none(self):
        def fn():
            raise RuntimeError("fail")
        result = execute_with_retry(fn, None)
        # default is 3 attempts
        assert result.attempts == 3

    def test_args_passed_to_fn(self):
        def fn(a, b):
            return a + b
        result = execute_with_retry(fn, args=(10, 20))
        assert result.result == 30

    def test_kwargs_passed_to_fn(self):
        def fn(x=0):
            return x * 2
        result = execute_with_retry(fn, kwargs={"x": 7})
        assert result.result == 14

    def test_single_attempt_policy(self):
        def fn():
            raise RuntimeError("fail")
        result = execute_with_retry(fn, RetryPolicy(max_attempts=1))
        assert result.attempts == 1
        assert result.success is False
        assert result.total_wait_ms == 0.0


# ===========================================================================
# PoisonReport
# ===========================================================================

class TestPoisonReport:
    def test_poison_count_empty(self):
        r = PoisonReport()
        assert r.poison_count() == 0

    def test_poison_count_with_jobs(self):
        r = PoisonReport(poison_jobs=["a", "b", "c"])
        assert r.poison_count() == 3

    def test_poison_rate_zero_total(self):
        r = PoisonReport(poison_jobs=["a"], total_checked=0)
        assert r.poison_rate() == 0.0

    def test_poison_rate_calculation(self):
        r = PoisonReport(poison_jobs=["a", "b"], total_checked=10)
        assert r.poison_rate() == pytest.approx(0.2)

    def test_poison_rate_all_poison(self):
        r = PoisonReport(poison_jobs=["a", "b"], total_checked=2)
        assert r.poison_rate() == pytest.approx(1.0)

    def test_default_threshold(self):
        r = PoisonReport()
        assert r.threshold == 3

    def test_default_total_checked(self):
        r = PoisonReport()
        assert r.total_checked == 0


# ===========================================================================
# PoisonPillDetector
# ===========================================================================

class TestPoisonPillDetector:
    def test_is_poison_above_threshold(self):
        detector = PoisonPillDetector(threshold=3)
        item = make_item(attempt_count=3)
        assert detector.is_poison(item) is True

    def test_is_poison_below_threshold(self):
        detector = PoisonPillDetector(threshold=3)
        item = make_item(attempt_count=2)
        assert detector.is_poison(item) is False

    def test_is_poison_exactly_at_threshold(self):
        detector = PoisonPillDetector(threshold=3)
        item = make_item(attempt_count=3)
        assert detector.is_poison(item) is True

    def test_is_poison_resolved_item_false(self):
        detector = PoisonPillDetector(threshold=3)
        item = make_item(attempt_count=10, resolved=True)
        assert detector.is_poison(item) is False

    def test_is_poison_high_attempts_resolved_false(self):
        detector = PoisonPillDetector(threshold=3)
        item = make_item(attempt_count=100, resolved=True)
        assert detector.is_poison(item) is False

    def test_default_threshold_is_3(self):
        detector = PoisonPillDetector()
        assert detector.threshold == 3

    def test_scan_returns_poison_report(self):
        detector = PoisonPillDetector(threshold=3)
        items = [make_item(job_id="j1", attempt_count=5),
                 make_item(job_id="j2", attempt_count=1)]
        report = detector.scan(items)
        assert isinstance(report, PoisonReport)

    def test_scan_total_checked(self):
        detector = PoisonPillDetector(threshold=3)
        items = [make_item(job_id=f"j{i}", attempt_count=1) for i in range(7)]
        report = detector.scan(items)
        assert report.total_checked == 7

    def test_scan_identifies_poison_jobs(self):
        detector = PoisonPillDetector(threshold=3)
        items = [
            make_item(job_id="poison1", attempt_count=4),
            make_item(job_id="clean1", attempt_count=1),
            make_item(job_id="poison2", attempt_count=3),
        ]
        report = detector.scan(items)
        assert "poison1" in report.poison_jobs
        assert "poison2" in report.poison_jobs
        assert "clean1" not in report.poison_jobs

    def test_scan_empty_input(self):
        detector = PoisonPillDetector(threshold=3)
        report = detector.scan([])
        assert report.poison_count() == 0
        assert report.total_checked == 0

    def test_scan_threshold_in_report(self):
        detector = PoisonPillDetector(threshold=5)
        report = detector.scan([])
        assert report.threshold == 5

    def test_quarantine_splits_correctly(self):
        detector = PoisonPillDetector(threshold=3)
        items = [
            make_item(job_id="p1", attempt_count=5),
            make_item(job_id="c1", attempt_count=1),
            make_item(job_id="p2", attempt_count=3),
            make_item(job_id="c2", attempt_count=2),
        ]
        clean, poison = detector.quarantine(items)
        clean_ids = [i.job_id for i in clean]
        poison_ids = [i.job_id for i in poison]
        assert "c1" in clean_ids
        assert "c2" in clean_ids
        assert "p1" in poison_ids
        assert "p2" in poison_ids

    def test_quarantine_empty_input(self):
        detector = PoisonPillDetector()
        clean, poison = detector.quarantine([])
        assert clean == []
        assert poison == []

    def test_quarantine_all_clean(self):
        detector = PoisonPillDetector(threshold=5)
        items = [make_item(job_id=f"j{i}", attempt_count=1) for i in range(4)]
        clean, poison = detector.quarantine(items)
        assert len(clean) == 4
        assert len(poison) == 0

    def test_quarantine_all_poison(self):
        detector = PoisonPillDetector(threshold=2)
        items = [make_item(job_id=f"j{i}", attempt_count=5) for i in range(3)]
        clean, poison = detector.quarantine(items)
        assert len(clean) == 0
        assert len(poison) == 3

    def test_quarantine_returns_tuple(self):
        detector = PoisonPillDetector()
        result = detector.quarantine([])
        assert isinstance(result, tuple)
        assert len(result) == 2
