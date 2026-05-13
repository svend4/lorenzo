"""Tests for E158 quota_tracker module."""
from __future__ import annotations

import math
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.quota_tracker import (
    QuotaError,
    QuotaLimit,
    QuotaPeriod,
    QuotaStatus,
    QuotaTracker,
)


# ----------------------------------------------------------------------- #
class TestQuotaPeriod:
    def test_members_exist(self):
        for name in ("SECOND", "MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "FOREVER"):
            assert hasattr(QuotaPeriod, name)

    def test_distinct(self):
        members = {
            QuotaPeriod.SECOND, QuotaPeriod.MINUTE, QuotaPeriod.HOUR,
            QuotaPeriod.DAY, QuotaPeriod.WEEK, QuotaPeriod.MONTH,
            QuotaPeriod.FOREVER,
        }
        assert len(members) == 7

    def test_is_enum(self):
        from enum import Enum
        assert issubclass(QuotaPeriod, Enum)


class TestQuotaLimit:
    def test_construct(self):
        lim = QuotaLimit(key="k", period=QuotaPeriod.MINUTE, max_units=10)
        assert lim.key == "k"
        assert lim.period == QuotaPeriod.MINUTE
        assert lim.max_units == 10

    def test_equality(self):
        a = QuotaLimit("k", QuotaPeriod.HOUR, 5)
        b = QuotaLimit("k", QuotaPeriod.HOUR, 5)
        assert a == b


class TestQuotaStatus:
    def test_is_exhausted_true(self):
        s = QuotaStatus("k", QuotaPeriod.MINUTE, used=10, remaining=0,
                        max_units=10, reset_at=60.0)
        assert s.is_exhausted is True

    def test_is_exhausted_false(self):
        s = QuotaStatus("k", QuotaPeriod.MINUTE, used=3, remaining=7,
                        max_units=10, reset_at=60.0)
        assert s.is_exhausted is False

    def test_utilization_half(self):
        s = QuotaStatus("k", QuotaPeriod.MINUTE, used=5, remaining=5,
                        max_units=10, reset_at=60.0)
        assert s.utilization == 0.5

    def test_utilization_zero(self):
        s = QuotaStatus("k", QuotaPeriod.MINUTE, used=0, remaining=10,
                        max_units=10, reset_at=60.0)
        assert s.utilization == 0.0

    def test_utilization_full(self):
        s = QuotaStatus("k", QuotaPeriod.MINUTE, used=10, remaining=0,
                        max_units=10, reset_at=60.0)
        assert s.utilization == 1.0


class TestSetLimit:
    def test_returns_limit(self):
        qt = QuotaTracker()
        lim = qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        assert isinstance(lim, QuotaLimit)
        assert lim.key == "k"
        assert lim.max_units == 5

    def test_replace_resets(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 3, now=0.0)
        qt.set_limit("k", QuotaPeriod.MINUTE, 10)
        assert qt.total_used("k", now=0.0) == 0

    def test_invalid_period(self):
        qt = QuotaTracker()
        with pytest.raises(QuotaError):
            qt.set_limit("k", "minute", 5)  # type: ignore[arg-type]

    def test_negative_max(self):
        qt = QuotaTracker()
        with pytest.raises(QuotaError):
            qt.set_limit("k", QuotaPeriod.MINUTE, -1)


class TestConsumeBasic:
    def test_within(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        assert qt.consume("k", 1, now=0.0) is True
        assert qt.total_used("k", now=0.0) == 1

    def test_default_units(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", now=0.0)
        assert qt.total_used("k", now=0.0) == 1

    def test_multiple(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        for _ in range(3):
            assert qt.consume("k", 1, now=0.0) is True
        assert qt.total_used("k", now=0.0) == 3


class TestConsumeExhaustion:
    def test_returns_false(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 2)
        assert qt.consume("k", 1, now=0.0) is True
        assert qt.consume("k", 1, now=0.0) is True
        assert qt.consume("k", 1, now=0.0) is False

    def test_no_increment_on_overflow(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 2)
        qt.consume("k", 2, now=0.0)
        assert qt.consume("k", 1, now=0.0) is False
        assert qt.total_used("k", now=0.0) == 2

    def test_exact_limit_allowed(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        assert qt.consume("k", 5, now=0.0) is True
        assert qt.consume("k", 1, now=0.0) is False


class TestConsumeMultiUnit:
    def test_bulk_consume(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 100)
        assert qt.consume("k", 25, now=0.0) is True
        assert qt.consume("k", 50, now=0.0) is True
        assert qt.total_used("k", now=0.0) == 75

    def test_overflow_bulk_rejected(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 10)
        assert qt.consume("k", 15, now=0.0) is False
        assert qt.total_used("k", now=0.0) == 0

    def test_zero_units_allowed(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        assert qt.consume("k", 0, now=0.0) is True
        assert qt.total_used("k", now=0.0) == 0

    def test_negative_units_raises(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        with pytest.raises(QuotaError):
            qt.consume("k", -1, now=0.0)


class TestCheck:
    def test_check_non_mutating(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        assert qt.check("k", 3, now=0.0) is True
        assert qt.total_used("k", now=0.0) == 0

    def test_check_after_consume(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 4, now=0.0)
        assert qt.check("k", 1, now=0.0) is True
        assert qt.check("k", 2, now=0.0) is False

    def test_check_unknown_key(self):
        qt = QuotaTracker()
        assert qt.check("missing", 1, now=0.0) is False

    def test_check_sees_reset(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 5, now=0.0)
        # After window expires it should accept again, without mutating
        assert qt.check("k", 1, now=120.0) is True
        # Still hasn't been touched
        assert qt.total_used("k", now=0.0) == 5


class TestWindowReset:
    def test_minute_reset(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 5, now=0.0)
        assert qt.consume("k", 1, now=30.0) is False
        # 60s elapsed → window resets
        assert qt.consume("k", 1, now=60.0) is True
        assert qt.total_used("k", now=60.0) == 1

    def test_hour_reset(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.HOUR, 3)
        qt.consume("k", 3, now=0.0)
        assert qt.consume("k", 1, now=3599.0) is False
        assert qt.consume("k", 1, now=3600.0) is True

    def test_day_reset(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.DAY, 2)
        qt.consume("k", 2, now=0.0)
        assert qt.consume("k", 1, now=86399.0) is False
        assert qt.consume("k", 1, now=86400.0) is True

    def test_window_anchored_to_first_consume(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 1, now=100.0)  # window_start = 100
        # at 159 should not reset yet
        assert qt.consume("k", 4, now=159.0) is True
        assert qt.consume("k", 1, now=159.0) is False
        # at 160 reset
        assert qt.consume("k", 1, now=160.0) is True


class TestStatus:
    def test_status_after_consume(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 10)
        qt.consume("k", 3, now=5.0)
        st = qt.status("k", now=5.0)
        assert st is not None
        assert st.used == 3
        assert st.remaining == 7
        assert st.max_units == 10
        assert st.period == QuotaPeriod.MINUTE
        assert st.key == "k"

    def test_status_unknown_returns_none(self):
        qt = QuotaTracker()
        assert qt.status("missing", now=0.0) is None

    def test_reset_at(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 10)
        qt.consume("k", 1, now=100.0)
        st = qt.status("k", now=100.0)
        assert st.reset_at == pytest.approx(160.0)

    def test_status_remaining_clamped(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 5, now=0.0)
        st = qt.status("k", now=0.0)
        assert st.remaining == 0
        assert st.is_exhausted is True


class TestReset:
    def test_reset_clears_usage(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 4, now=0.0)
        assert qt.reset("k") is True
        assert qt.total_used("k", now=0.0) == 0

    def test_reset_unknown(self):
        qt = QuotaTracker()
        assert qt.reset("nope") is False

    def test_reset_allows_consume_again(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 2)
        qt.consume("k", 2, now=0.0)
        qt.reset("k")
        assert qt.consume("k", 2, now=0.0) is True


class TestResetAll:
    def test_reset_all_counts(self):
        qt = QuotaTracker()
        qt.set_limit("a", QuotaPeriod.MINUTE, 5)
        qt.set_limit("b", QuotaPeriod.HOUR, 10)
        qt.set_limit("c", QuotaPeriod.DAY, 100)
        qt.consume("a", 1, now=0.0)
        qt.consume("b", 1, now=0.0)
        assert qt.reset_all() == 3

    def test_reset_all_clears(self):
        qt = QuotaTracker()
        qt.set_limit("a", QuotaPeriod.MINUTE, 5)
        qt.set_limit("b", QuotaPeriod.HOUR, 10)
        qt.consume("a", 3, now=0.0)
        qt.consume("b", 4, now=0.0)
        qt.reset_all()
        assert qt.total_used("a", now=0.0) == 0
        assert qt.total_used("b", now=0.0) == 0

    def test_reset_all_empty(self):
        qt = QuotaTracker()
        assert qt.reset_all() == 0


class TestAllKeys:
    def test_initial_empty(self):
        qt = QuotaTracker()
        assert qt.all_keys() == []

    def test_lists_keys(self):
        qt = QuotaTracker()
        qt.set_limit("a", QuotaPeriod.MINUTE, 5)
        qt.set_limit("b", QuotaPeriod.HOUR, 10)
        keys = qt.all_keys()
        assert set(keys) == {"a", "b"}


class TestTotalUsed:
    def test_no_limit(self):
        qt = QuotaTracker()
        assert qt.total_used("missing", now=0.0) == 0

    def test_after_consume(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 10)
        qt.consume("k", 7, now=0.0)
        assert qt.total_used("k", now=0.0) == 7

    def test_reflects_window_reset(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 10)
        qt.consume("k", 5, now=0.0)
        assert qt.total_used("k", now=120.0) == 0


class TestTryConsume:
    def test_success_returns_status(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        ok, st = qt.try_consume("k", 2, now=0.0)
        assert ok is True
        assert st.used == 2
        assert st.remaining == 3

    def test_failure_returns_status(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 5, now=0.0)
        ok, st = qt.try_consume("k", 1, now=0.0)
        assert ok is False
        assert st.used == 5
        assert st.is_exhausted is True

    def test_unknown_raises(self):
        qt = QuotaTracker()
        with pytest.raises(QuotaError):
            qt.try_consume("missing", 1, now=0.0)

    def test_status_reset_window(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        qt.consume("k", 5, now=0.0)
        ok, st = qt.try_consume("k", 1, now=120.0)
        assert ok is True
        assert st.used == 1


class TestForeverPeriod:
    def test_never_resets(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.FOREVER, 3)
        assert qt.consume("k", 3, now=0.0) is True
        # Even huge time gap — still exhausted
        assert qt.consume("k", 1, now=10**12) is False

    def test_reset_at_infinity(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.FOREVER, 5)
        qt.consume("k", 1, now=0.0)
        st = qt.status("k", now=0.0)
        assert math.isinf(st.reset_at)

    def test_manual_reset_works(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.FOREVER, 3)
        qt.consume("k", 3, now=0.0)
        qt.reset("k")
        assert qt.consume("k", 1, now=0.0) is True


class TestMultipleKeys:
    def test_keys_independent(self):
        qt = QuotaTracker()
        qt.set_limit("a", QuotaPeriod.MINUTE, 5)
        qt.set_limit("b", QuotaPeriod.MINUTE, 5)
        qt.consume("a", 5, now=0.0)
        assert qt.consume("a", 1, now=0.0) is False
        assert qt.consume("b", 1, now=0.0) is True

    def test_different_periods(self):
        qt = QuotaTracker()
        qt.set_limit("a", QuotaPeriod.MINUTE, 5)
        qt.set_limit("b", QuotaPeriod.HOUR, 5)
        qt.consume("a", 5, now=0.0)
        qt.consume("b", 5, now=0.0)
        # at 70s: minute window resets, hour does not
        assert qt.consume("a", 1, now=70.0) is True
        assert qt.consume("b", 1, now=70.0) is False

    def test_status_isolated(self):
        qt = QuotaTracker()
        qt.set_limit("a", QuotaPeriod.MINUTE, 10)
        qt.set_limit("b", QuotaPeriod.MINUTE, 10)
        qt.consume("a", 3, now=0.0)
        qt.consume("b", 7, now=0.0)
        assert qt.status("a", now=0.0).used == 3
        assert qt.status("b", now=0.0).used == 7


class TestEdgeCases:
    def test_consume_no_limit_returns_false(self):
        qt = QuotaTracker()
        assert qt.consume("missing", 1, now=0.0) is False

    def test_zero_max_rejects_everything(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 0)
        assert qt.consume("k", 1, now=0.0) is False
        assert qt.consume("k", 0, now=0.0) is True  # zero is fine

    def test_large_units(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 10**9)
        assert qt.consume("k", 10**9, now=0.0) is True
        assert qt.consume("k", 1, now=0.0) is False

    def test_negative_max_raises(self):
        qt = QuotaTracker()
        with pytest.raises(QuotaError):
            qt.set_limit("k", QuotaPeriod.MINUTE, -5)

    def test_check_negative_units(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 5)
        with pytest.raises(QuotaError):
            qt.check("k", -1, now=0.0)


class TestThreadSafety:
    def test_concurrent_consume(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 1000)
        N_THREADS = 10
        PER_THREAD = 100

        def worker():
            for _ in range(PER_THREAD):
                qt.consume("k", 1, now=0.0)

        threads = [threading.Thread(target=worker) for _ in range(N_THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly N * PER_THREAD consumes should have happened (within limit)
        assert qt.total_used("k", now=0.0) == N_THREADS * PER_THREAD

    def test_concurrent_consume_respects_limit(self):
        qt = QuotaTracker()
        qt.set_limit("k", QuotaPeriod.MINUTE, 100)
        results = []
        lock = threading.Lock()

        def worker():
            for _ in range(50):
                ok = qt.consume("k", 1, now=0.0)
                with lock:
                    results.append(ok)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        successes = sum(1 for r in results if r)
        assert successes == 100  # exactly the limit
        assert qt.total_used("k", now=0.0) == 100
