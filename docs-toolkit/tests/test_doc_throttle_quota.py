"""Tests for docstoolkit.doc_throttle_quota."""
from __future__ import annotations

import pytest

from docstoolkit.doc_throttle_quota import (
    DocThrottleQuota,
    QuotaCheckResult,
    QuotaSpec,
    TimeWindow,
    UsageRecord,
)


# ---------------------------------------------------------------- TimeWindow


class TestTimeWindow:
    def test_members(self):
        assert TimeWindow.MINUTE.value == "minute"
        assert TimeWindow.HOUR.value == "hour"
        assert TimeWindow.DAY.value == "day"
        assert TimeWindow.WEEK.value == "week"
        assert TimeWindow.MONTH.value == "month"

    def test_distinct(self):
        assert len({TimeWindow.MINUTE, TimeWindow.HOUR, TimeWindow.DAY,
                    TimeWindow.WEEK, TimeWindow.MONTH}) == 5

    def test_is_enum(self):
        from enum import Enum
        assert issubclass(TimeWindow, Enum)


# ---------------------------------------------------------------- QuotaSpec


class TestQuotaSpec:
    def test_construct(self):
        spec = QuotaSpec(action="create", window=TimeWindow.MINUTE, limit=10)
        assert spec.action == "create"
        assert spec.window == TimeWindow.MINUTE
        assert spec.limit == 10

    def test_equality(self):
        a = QuotaSpec("a", TimeWindow.HOUR, 5)
        b = QuotaSpec("a", TimeWindow.HOUR, 5)
        assert a == b


# --------------------------------------------------------------- UsageRecord


class TestUsageRecord:
    def test_defaults(self):
        rec = UsageRecord(user_id="u", action="a", window=TimeWindow.MINUTE)
        assert rec.count == 0
        assert rec.window_start == 0.0
        assert rec.last_op_at == 0.0

    def test_set_fields(self):
        rec = UsageRecord(user_id="u", action="a", window=TimeWindow.HOUR,
                          count=3, window_start=100.0, last_op_at=120.0)
        assert rec.count == 3
        assert rec.window_start == 100.0
        assert rec.last_op_at == 120.0


# ------------------------------------------------------------ QuotaCheckResult


class TestQuotaCheckResult:
    def test_construct(self):
        r = QuotaCheckResult(allowed=True, user_id="u", action="a",
                             window=TimeWindow.MINUTE, count=0, limit=5,
                             remaining=5, reset_at=60.0)
        assert r.allowed is True
        assert r.reason is None
        assert r.remaining == 5

    def test_with_reason(self):
        r = QuotaCheckResult(allowed=False, user_id="u", action="a",
                             window=TimeWindow.MINUTE, count=5, limit=5,
                             remaining=0, reset_at=60.0, reason="quota_exceeded")
        assert r.allowed is False
        assert r.reason == "quota_exceeded"


# --------------------------------------------------------------- set_quota


class TestSetQuota:
    def test_returns_spec(self):
        q = DocThrottleQuota()
        spec = q.set_quota("create", TimeWindow.MINUTE, 10)
        assert isinstance(spec, QuotaSpec)
        assert spec.limit == 10

    def test_stored(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        assert q.total_quotas == 1

    def test_replace(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("create", TimeWindow.MINUTE, 20)
        specs = q.quotas_for_action("create")
        assert len(specs) == 1
        assert specs[0].limit == 20

    def test_multiple_windows(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("create", TimeWindow.HOUR, 100)
        assert q.total_quotas == 2

    def test_negative_limit_raises(self):
        q = DocThrottleQuota()
        with pytest.raises(ValueError):
            q.set_quota("create", TimeWindow.MINUTE, -1)

    def test_zero_limit_allowed(self):
        q = DocThrottleQuota()
        spec = q.set_quota("create", TimeWindow.MINUTE, 0)
        assert spec.limit == 0


# ------------------------------------------------------------- remove_quota


class TestRemoveQuota:
    def test_remove_existing(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        assert q.remove_quota("create", TimeWindow.MINUTE) is True
        assert q.total_quotas == 0

    def test_remove_missing(self):
        q = DocThrottleQuota()
        assert q.remove_quota("create", TimeWindow.MINUTE) is False

    def test_remove_one_keeps_others(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("create", TimeWindow.HOUR, 100)
        q.remove_quota("create", TimeWindow.MINUTE)
        specs = q.quotas_for_action("create")
        assert len(specs) == 1
        assert specs[0].window == TimeWindow.HOUR

    def test_action_pruned_when_empty(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.remove_quota("create", TimeWindow.MINUTE)
        assert q.all_actions() == []


# ---------------------------------------------------------------- check


class TestCheck:
    def test_no_quota(self):
        q = DocThrottleQuota()
        assert q.check("u1", "create", now=0.0) == []

    def test_initial_allowed(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        results = q.check("u1", "create", now=0.0)
        assert len(results) == 1
        assert results[0].allowed is True
        assert results[0].remaining == 5
        assert results[0].count == 0

    def test_check_does_not_increment(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        q.check("u1", "create", now=0.0)
        q.check("u1", "create", now=0.0)
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec is not None
        assert rec.count == 0

    def test_check_at_limit_blocked(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 2)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        results = q.check("u1", "create", now=0.0)
        assert results[0].allowed is False
        assert results[0].reason == "quota_exceeded"
        assert results[0].remaining == 0

    def test_multiple_windows(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        q.set_quota("create", TimeWindow.HOUR, 100)
        results = q.check("u1", "create", now=0.0)
        assert len(results) == 2

    def test_reset_at_in_future(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        results = q.check("u1", "create", now=1000.0)
        assert results[0].reset_at == 1000.0 + 60


# ---------------------------------------------------------------- consume


class TestConsume:
    def test_no_quota_returns_true(self):
        q = DocThrottleQuota()
        ok, results = q.consume("u1", "create", now=0.0)
        assert ok is True
        assert results == []

    def test_basic_consume(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 3)
        ok, results = q.consume("u1", "create", now=0.0)
        assert ok is True
        assert results[0].count == 1
        assert results[0].remaining == 2

    def test_consume_multiple(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 3)
        for i in range(3):
            ok, _ = q.consume("u1", "create", now=0.0)
            assert ok is True
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec.count == 3

    def test_consume_updates_last_op_at(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 3)
        q.consume("u1", "create", now=10.0)
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=10.0)
        assert rec.last_op_at == 10.0


# ----------------------------------------------------------- ConsumeOverLimit


class TestConsumeOverLimit:
    def test_over_limit_denied(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 2)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        ok, results = q.consume("u1", "create", now=0.0)
        assert ok is False
        assert results[0].allowed is False
        assert results[0].reason == "quota_exceeded"

    def test_denied_does_not_increment(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 2)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec.count == 2

    def test_zero_limit_always_blocks(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 0)
        ok, results = q.consume("u1", "create", now=0.0)
        assert ok is False
        assert results[0].reason == "quota_exceeded"


# --------------------------------------------------------- ConsumeAllOrNothing


class TestConsumeAllOrNothing:
    def test_blocked_by_inner_window(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 2)
        q.set_quota("create", TimeWindow.HOUR, 100)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        ok, results = q.consume("u1", "create", now=0.0)
        assert ok is False
        # Neither counter should have been incremented past the existing values.
        hour = next(r for r in results if r.window == TimeWindow.HOUR)
        minute = next(r for r in results if r.window == TimeWindow.MINUTE)
        assert minute.count == 2
        assert hour.count == 2

    def test_blocked_by_outer_window(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 100)
        q.set_quota("create", TimeWindow.HOUR, 2)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        ok, _ = q.consume("u1", "create", now=0.0)
        assert ok is False
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec.count == 2  # not incremented to 3

    def test_all_within_increments_all(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("create", TimeWindow.HOUR, 100)
        ok, _ = q.consume("u1", "create", now=0.0)
        assert ok is True
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=0.0).count == 1
        assert q.usage("u1", "create", TimeWindow.HOUR, now=0.0).count == 1


# ---------------------------------------------------------------- usage


class TestUsage:
    def test_no_record(self):
        q = DocThrottleQuota()
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=0.0) is None

    def test_after_consume(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        q.consume("u1", "create", now=0.0)
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec is not None
        assert rec.count == 1
        assert rec.user_id == "u1"

    def test_returns_copy(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        q.consume("u1", "create", now=0.0)
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        rec.count = 999
        rec2 = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec2.count == 1

    def test_applies_window_reset(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        q.consume("u1", "create", now=0.0)
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=100.0)
        assert rec.count == 0


# ---------------------------------------------------------------- reset_user


class TestResetUser:
    def test_reset_all_for_user(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("edit", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "edit", now=0.0)
        removed = q.reset_user("u1")
        assert removed == 2
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=0.0) is None

    def test_reset_specific_action(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("edit", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "edit", now=0.0)
        removed = q.reset_user("u1", action="create")
        assert removed == 1
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=0.0) is None
        assert q.usage("u1", "edit", TimeWindow.MINUTE, now=0.0) is not None

    def test_reset_does_not_affect_other_users(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        q.consume("u2", "create", now=0.0)
        q.reset_user("u1")
        assert q.usage("u2", "create", TimeWindow.MINUTE, now=0.0) is not None

    def test_reset_missing(self):
        q = DocThrottleQuota()
        assert q.reset_user("nobody") == 0


# ------------------------------------------------------------- users_at_limit


class TestUsersAtLimit:
    def test_no_quota_returns_empty(self):
        q = DocThrottleQuota()
        assert q.users_at_limit("create", TimeWindow.MINUTE, now=0.0) == []

    def test_lists_only_at_limit(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 2)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        q.consume("u2", "create", now=0.0)
        at = q.users_at_limit("create", TimeWindow.MINUTE, now=0.0)
        assert at == ["u1"]

    def test_multiple_at_limit(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 1)
        q.consume("u1", "create", now=0.0)
        q.consume("u2", "create", now=0.0)
        at = sorted(q.users_at_limit("create", TimeWindow.MINUTE, now=0.0))
        assert at == ["u1", "u2"]

    def test_window_reset_clears(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 1)
        q.consume("u1", "create", now=0.0)
        # Far in the future: window resets and the user is no longer at limit.
        at = q.users_at_limit("create", TimeWindow.MINUTE, now=10_000.0)
        assert at == []


# ---------------------------------------------------------------- top_users


class TestTopUsers:
    def test_empty(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        assert q.top_users("create", now=0.0) == []

    def test_ranking(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 100)
        for _ in range(5):
            q.consume("u1", "create", now=0.0)
        for _ in range(2):
            q.consume("u2", "create", now=0.0)
        top = q.top_users("create", now=0.0)
        assert top[0][0] == "u1"
        assert top[0][1] == 5
        assert top[1][0] == "u2"
        assert top[1][1] == 2

    def test_top_k_limit(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 100)
        for i in range(5):
            for _ in range(i + 1):
                q.consume(f"u{i}", "create", now=0.0)
        top = q.top_users("create", top_k=2, now=0.0)
        assert len(top) == 2

    def test_aggregates_across_windows(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 100)
        q.set_quota("create", TimeWindow.HOUR, 1000)
        q.consume("u1", "create", now=0.0)
        top = q.top_users("create", now=0.0)
        # u1 counted once per window
        assert top == [("u1", 2)]


# --------------------------------------------------------- quotas_for_action


class TestQuotasForAction:
    def test_empty(self):
        q = DocThrottleQuota()
        assert q.quotas_for_action("none") == []

    def test_lists_all(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("create", TimeWindow.HOUR, 100)
        specs = q.quotas_for_action("create")
        assert len(specs) == 2
        windows = {s.window for s in specs}
        assert windows == {TimeWindow.MINUTE, TimeWindow.HOUR}


# --------------------------------------------------------------- all_actions


class TestAllActions:
    def test_empty(self):
        q = DocThrottleQuota()
        assert q.all_actions() == []

    def test_distinct(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.set_quota("create", TimeWindow.HOUR, 100)
        q.set_quota("edit", TimeWindow.MINUTE, 5)
        actions = sorted(q.all_actions())
        assert actions == ["create", "edit"]


# ---------------------------------------------------------------- cleanup


class TestCleanup:
    def test_no_records(self):
        q = DocThrottleQuota()
        assert q.cleanup(now=0.0) == 0

    def test_removes_expired(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        removed = q.cleanup(now=1000.0)
        assert removed == 1
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=1000.0) is None

    def test_keeps_active(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        removed = q.cleanup(now=10.0)
        assert removed == 0
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=10.0) is not None


# ------------------------------------------------------------- total_quotas


class TestTotalQuotas:
    def test_empty(self):
        q = DocThrottleQuota()
        assert q.total_quotas == 0

    def test_after_add(self):
        q = DocThrottleQuota()
        q.set_quota("a", TimeWindow.MINUTE, 1)
        q.set_quota("a", TimeWindow.HOUR, 1)
        q.set_quota("b", TimeWindow.DAY, 1)
        assert q.total_quotas == 3


# ---------------------------------------------------------------- clear


class TestClear:
    def test_clears_quotas_and_usage(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        q.clear()
        assert q.total_quotas == 0
        assert q.all_actions() == []
        assert q.usage("u1", "create", TimeWindow.MINUTE, now=0.0) is None


# ------------------------------------------------------------- WindowReset


class TestWindowReset:
    def test_minute_window_resets(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 2)
        q.consume("u1", "create", now=0.0)
        q.consume("u1", "create", now=0.0)
        # exactly at window boundary the next call resets
        ok, _ = q.consume("u1", "create", now=60.0)
        assert ok is True
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=60.0)
        assert rec.count == 1
        assert rec.window_start == 60.0

    def test_hour_window_seconds(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.HOUR, 1)
        q.consume("u1", "create", now=0.0)
        # 3599s in -> still blocked
        ok, _ = q.consume("u1", "create", now=3599.0)
        assert ok is False
        # 3600s -> resets
        ok, _ = q.consume("u1", "create", now=3600.0)
        assert ok is True

    def test_day_week_month_seconds(self):
        q = DocThrottleQuota()
        q.set_quota("a", TimeWindow.DAY, 1)
        q.consume("u", "a", now=0.0)
        assert q.consume("u", "a", now=86399.0)[0] is False
        assert q.consume("u", "a", now=86400.0)[0] is True

        q2 = DocThrottleQuota()
        q2.set_quota("a", TimeWindow.WEEK, 1)
        q2.consume("u", "a", now=0.0)
        assert q2.consume("u", "a", now=604800.0)[0] is True

        q3 = DocThrottleQuota()
        q3.set_quota("a", TimeWindow.MONTH, 1)
        q3.consume("u", "a", now=0.0)
        assert q3.consume("u", "a", now=2592000.0)[0] is True


# ------------------------------------------------------------- EdgeCases


class TestEdgeCases:
    def test_remove_quota_keeps_existing_usage(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 5)
        q.consume("u1", "create", now=0.0)
        q.remove_quota("create", TimeWindow.MINUTE)
        # usage record still exists
        rec = q.usage("u1", "create", TimeWindow.MINUTE, now=0.0)
        assert rec is not None

    def test_consume_after_remove_quota(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 1)
        q.consume("u1", "create", now=0.0)
        q.remove_quota("create", TimeWindow.MINUTE)
        # No quota => always allowed
        ok, results = q.consume("u1", "create", now=0.0)
        assert ok is True
        assert results == []

    def test_independent_users(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 1)
        q.consume("u1", "create", now=0.0)
        ok, _ = q.consume("u2", "create", now=0.0)
        assert ok is True

    def test_independent_actions(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 1)
        q.set_quota("edit", TimeWindow.MINUTE, 1)
        q.consume("u1", "create", now=0.0)
        ok, _ = q.consume("u1", "edit", now=0.0)
        assert ok is True

    def test_now_defaults_to_real_time(self):
        # Just smoke test that it doesn't crash and behaves like a fresh window.
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 1)
        ok, _ = q.consume("u1", "create")
        assert ok is True

    def test_top_k_zero(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 10)
        q.consume("u1", "create", now=0.0)
        assert q.top_users("create", top_k=0, now=0.0) == []

    def test_remaining_never_negative(self):
        q = DocThrottleQuota()
        q.set_quota("create", TimeWindow.MINUTE, 0)
        results = q.check("u1", "create", now=0.0)
        assert results[0].remaining == 0
