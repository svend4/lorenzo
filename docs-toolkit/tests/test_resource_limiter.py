"""Tests for the E112 resource_limiter module.

Covers (~85 tests):
- consume returns ALLOWED when under limit
- consume returns DENIED when over limit (usage not updated)
- consume returns WARNING when at / above warn_threshold
- Window expiry resets usage
- usage() returns correct current value
- remaining() returns correct value
- reset() clears one resource
- reset_namespace() clears all resources for a namespace
- No limit defined → always ALLOWED
- Multiple namespaces are independent
- Multiple resources are independent
- Virtual clock for deterministic window testing
- Thread safety (concurrent consume)
- add_limit overwrites existing limit
- Window boundary: exactly at window_start + window resets
- LimitResult enum values
- UsageRecord fields
- ResourceLimit fields / defaults
- close() lifecycle
- Fractional amounts
- Amount larger than the entire limit → DENIED immediately
- warn_threshold at exactly the limit value
"""
import threading
import time
import pytest

from docstoolkit.resource_limiter import (
    LimitResult,
    ResourceLimit,
    ResourceLimiter,
    UsageRecord,
)


# =========================================================================== #
#  Helpers / fixtures                                                           #
# =========================================================================== #

class VirtualClock:
    """Injectable clock whose time can be advanced manually."""

    def __init__(self, start: float = 1_000.0):
        self._t = start

    def __call__(self) -> float:
        return self._t

    def advance(self, seconds: float) -> None:
        self._t += seconds

    @property
    def now(self) -> float:
        return self._t


def make_limiter(clock=None) -> ResourceLimiter:
    """Return a fresh in-memory ResourceLimiter."""
    return ResourceLimiter(db_path=":memory:", now_fn=clock)


def api_limit(limit=10, window=60.0, warn_threshold=None) -> ResourceLimit:
    return ResourceLimit(
        resource="api_calls",
        limit=limit,
        window=window,
        warn_threshold=warn_threshold,
    )


# =========================================================================== #
#  LimitResult enum                                                             #
# =========================================================================== #

class TestLimitResult:
    def test_allowed_value(self):
        assert LimitResult.ALLOWED == "allowed"

    def test_denied_value(self):
        assert LimitResult.DENIED == "denied"

    def test_warning_value(self):
        assert LimitResult.WARNING == "warning"

    def test_is_str_enum(self):
        assert isinstance(LimitResult.ALLOWED, str)

    def test_members(self):
        members = {r.value for r in LimitResult}
        assert members == {"allowed", "denied", "warning"}


# =========================================================================== #
#  ResourceLimit dataclass                                                      #
# =========================================================================== #

class TestResourceLimit:
    def test_fields_set(self):
        rl = ResourceLimit(resource="bytes", limit=1024.0, window=30.0)
        assert rl.resource == "bytes"
        assert rl.limit == 1024.0
        assert rl.window == 30.0

    def test_warn_threshold_defaults_none(self):
        rl = ResourceLimit(resource="x", limit=10, window=5)
        assert rl.warn_threshold is None

    def test_warn_threshold_explicit(self):
        rl = ResourceLimit(resource="x", limit=10, window=5, warn_threshold=7.0)
        assert rl.warn_threshold == 7.0


# =========================================================================== #
#  UsageRecord dataclass                                                        #
# =========================================================================== #

class TestUsageRecord:
    def test_fields(self):
        rec = UsageRecord(
            namespace="ns",
            resource="api",
            used=5.0,
            limit=10.0,
            window_start=1000.0,
            result=LimitResult.ALLOWED,
        )
        assert rec.namespace == "ns"
        assert rec.resource == "api"
        assert rec.used == 5.0
        assert rec.limit == 10.0
        assert rec.window_start == 1000.0
        assert rec.result is LimitResult.ALLOWED


# =========================================================================== #
#  Basic consume — ALLOWED                                                      #
# =========================================================================== #

class TestConsumeAllowed:
    def test_single_consume_allowed(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        rec = lim.consume("user1", "api_calls")
        assert rec.result is LimitResult.ALLOWED

    def test_used_increments(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        lim.consume("user1", "api_calls")
        lim.consume("user1", "api_calls")
        assert lim.usage("user1", "api_calls") == 2.0

    def test_used_field_on_record(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        rec = lim.consume("user1", "api_calls")
        assert rec.used == 1.0

    def test_limit_field_on_record(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        rec = lim.consume("user1", "api_calls")
        assert rec.limit == 5.0

    def test_namespace_on_record(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        rec = lim.consume("ns42", "api_calls")
        assert rec.namespace == "ns42"

    def test_resource_on_record(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        rec = lim.consume("ns42", "api_calls")
        assert rec.resource == "api_calls"

    def test_consume_up_to_limit_is_allowed(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=3))
        results = [lim.consume("u", "api_calls").result for _ in range(3)]
        assert all(r is LimitResult.ALLOWED for r in results)

    def test_fractional_amount_allowed(self):
        lim = make_limiter()
        lim.add_limit(ResourceLimit("bytes", limit=100.0, window=60.0))
        rec = lim.consume("u", "bytes", amount=33.5)
        assert rec.result is LimitResult.ALLOWED
        assert rec.used == pytest.approx(33.5)

    def test_multiple_fractional_amounts(self):
        lim = make_limiter()
        lim.add_limit(ResourceLimit("bytes", limit=100.0, window=60.0))
        lim.consume("u", "bytes", amount=33.5)
        lim.consume("u", "bytes", amount=33.5)
        assert lim.usage("u", "bytes") == pytest.approx(67.0)


# =========================================================================== #
#  Consume — DENIED                                                             #
# =========================================================================== #

class TestConsumeDenied:
    def test_over_limit_returns_denied(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=2))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.DENIED

    def test_denied_does_not_update_usage(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=2))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")  # denied
        assert lim.usage("u", "api_calls") == 2.0

    def test_denied_used_field_shows_current_not_attempted(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=2))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")
        # used should reflect current (2), not 3
        assert rec.used == 2.0

    def test_denied_result_field(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=1))
        lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.DENIED

    def test_amount_exceeds_full_limit_denied_immediately(self):
        """A single consume with amount > limit should be DENIED even on empty window."""
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        rec = lim.consume("u", "api_calls", amount=10.0)
        assert rec.result is LimitResult.DENIED
        # Usage must remain 0
        assert lim.usage("u", "api_calls") == 0.0

    def test_denied_then_allowed_after_reset(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=1))
        lim.consume("u", "api_calls")
        assert lim.consume("u", "api_calls").result is LimitResult.DENIED
        lim.reset("u", "api_calls")
        assert lim.consume("u", "api_calls").result is LimitResult.ALLOWED


# =========================================================================== #
#  Consume — WARNING                                                            #
# =========================================================================== #

class TestConsumeWarning:
    def test_at_warn_threshold_returns_warning(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10, warn_threshold=5.0))
        for _ in range(4):
            lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")   # used becomes 5 → warning
        assert rec.result is LimitResult.WARNING

    def test_above_warn_threshold_still_warning(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10, warn_threshold=3.0))
        for _ in range(3):
            lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")   # 4 > 3, still warning
        assert rec.result is LimitResult.WARNING

    def test_below_warn_threshold_is_allowed(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10, warn_threshold=5.0))
        rec = lim.consume("u", "api_calls")   # used=1 < 5
        assert rec.result is LimitResult.ALLOWED

    def test_warn_threshold_equal_to_limit(self):
        """When warn_threshold == limit, the 10th call is WARNING (not DENIED)."""
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10, warn_threshold=10.0))
        for _ in range(9):
            lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")   # used=10 == limit → warning
        assert rec.result is LimitResult.WARNING

    def test_one_over_warn_threshold_is_denied_at_limit(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5, warn_threshold=4.0))
        for _ in range(5):
            lim.consume("u", "api_calls")
        rec = lim.consume("u", "api_calls")   # would be 6 > 5 → DENIED
        assert rec.result is LimitResult.DENIED

    def test_warning_usage_still_updated(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10, warn_threshold=5.0))
        for _ in range(5):
            lim.consume("u", "api_calls")
        assert lim.usage("u", "api_calls") == 5.0


# =========================================================================== #
#  Window expiry                                                                #
# =========================================================================== #

class TestWindowExpiry:
    def test_window_resets_after_expiry(self):
        clock = VirtualClock()
        lim = make_limiter(clock)
        lim.add_limit(api_limit(limit=2, window=30.0))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        # Both slots used; advance past window
        clock.advance(31.0)
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED
        assert rec.used == 1.0

    def test_usage_zero_after_window_expiry(self):
        clock = VirtualClock()
        lim = make_limiter(clock)
        lim.add_limit(api_limit(limit=5, window=10.0))
        lim.consume("u", "api_calls", amount=5.0)
        clock.advance(11.0)
        assert lim.usage("u", "api_calls") == 0.0

    def test_window_boundary_exact(self):
        """now == window_start + window should NOT reset (strictly greater than)."""
        clock = VirtualClock(start=1000.0)
        lim = make_limiter(clock)
        lim.add_limit(api_limit(limit=2, window=30.0))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        # Advance to exactly the boundary
        clock.advance(30.0)   # now == window_start + window
        rec = lim.consume("u", "api_calls")
        # Should be DENIED because window has NOT expired (not strictly >)
        assert rec.result is LimitResult.DENIED

    def test_window_just_past_boundary_resets(self):
        """now == window_start + window + epsilon resets the window."""
        clock = VirtualClock(start=1000.0)
        lim = make_limiter(clock)
        lim.add_limit(api_limit(limit=2, window=30.0))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        clock.advance(30.0 + 1e-9)
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED

    def test_multiple_windows_accumulate_correctly(self):
        clock = VirtualClock()
        lim = make_limiter(clock)
        lim.add_limit(api_limit(limit=3, window=10.0))
        for _ in range(3):
            lim.consume("u", "api_calls")
        clock.advance(11.0)
        for _ in range(3):
            lim.consume("u", "api_calls")
        # Third window, fresh start
        clock.advance(11.0)
        assert lim.usage("u", "api_calls") == 0.0


# =========================================================================== #
#  usage()                                                                      #
# =========================================================================== #

class TestUsage:
    def test_usage_zero_before_any_consume(self):
        lim = make_limiter()
        lim.add_limit(api_limit())
        assert lim.usage("u", "api_calls") == 0.0

    def test_usage_reflects_consumes(self):
        lim = make_limiter()
        lim.add_limit(api_limit())
        lim.consume("u", "api_calls", amount=3.0)
        assert lim.usage("u", "api_calls") == 3.0

    def test_usage_not_affected_by_denied(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=2))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")  # denied
        assert lim.usage("u", "api_calls") == 2.0

    def test_usage_for_unknown_resource_is_zero(self):
        lim = make_limiter()
        assert lim.usage("u", "nonexistent") == 0.0

    def test_usage_for_unlimitied_resource_tracked(self):
        """Usage is tracked even for resources without a registered limit."""
        lim = make_limiter()
        lim.consume("u", "free_resource", amount=7.0)
        assert lim.usage("u", "free_resource") == 7.0


# =========================================================================== #
#  remaining()                                                                  #
# =========================================================================== #

class TestRemaining:
    def test_remaining_equals_limit_when_no_usage(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        assert lim.remaining("u", "api_calls") == 10.0

    def test_remaining_decreases_with_usage(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.consume("u", "api_calls", amount=4.0)
        assert lim.remaining("u", "api_calls") == 6.0

    def test_remaining_zero_at_limit(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        lim.consume("u", "api_calls", amount=5.0)
        assert lim.remaining("u", "api_calls") == 0.0

    def test_remaining_resets_after_window_expiry(self):
        clock = VirtualClock()
        lim = make_limiter(clock)
        lim.add_limit(api_limit(limit=5, window=10.0))
        lim.consume("u", "api_calls", amount=5.0)
        clock.advance(11.0)
        assert lim.remaining("u", "api_calls") == 5.0

    def test_remaining_inf_when_no_limit_defined(self):
        lim = make_limiter()
        assert lim.remaining("u", "free") == float("inf")

    def test_remaining_not_negative(self):
        """After denied consume, remaining should be 0.0, not negative."""
        lim = make_limiter()
        lim.add_limit(api_limit(limit=5))
        lim.consume("u", "api_calls", amount=5.0)
        # Now try to consume more (denied) — remaining must still be 0
        lim.consume("u", "api_calls", amount=3.0)
        assert lim.remaining("u", "api_calls") == pytest.approx(0.0)


# =========================================================================== #
#  reset() and reset_namespace()                                                #
# =========================================================================== #

class TestReset:
    def test_reset_clears_usage(self):
        lim = make_limiter()
        lim.add_limit(api_limit())
        lim.consume("u", "api_calls", amount=5.0)
        lim.reset("u", "api_calls")
        assert lim.usage("u", "api_calls") == 0.0

    def test_reset_allows_consume_after_full_limit(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=1))
        lim.consume("u", "api_calls")
        lim.reset("u", "api_calls")
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED

    def test_reset_idempotent_on_missing_row(self):
        lim = make_limiter()
        lim.add_limit(api_limit())
        lim.reset("u", "api_calls")   # should not raise
        assert lim.usage("u", "api_calls") == 0.0

    def test_reset_does_not_affect_other_resource(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.add_limit(ResourceLimit("bytes", limit=1000.0, window=60.0))
        lim.consume("u", "api_calls", amount=5.0)
        lim.consume("u", "bytes", amount=200.0)
        lim.reset("u", "api_calls")
        assert lim.usage("u", "bytes") == 200.0

    def test_reset_does_not_affect_other_namespace(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.consume("u1", "api_calls", amount=3.0)
        lim.consume("u2", "api_calls", amount=4.0)
        lim.reset("u1", "api_calls")
        assert lim.usage("u2", "api_calls") == 4.0


class TestResetNamespace:
    def test_reset_namespace_returns_count(self):
        lim = make_limiter()
        lim.add_limit(api_limit())
        lim.add_limit(ResourceLimit("bytes", limit=100.0, window=10.0))
        lim.consume("u", "api_calls")
        lim.consume("u", "bytes")
        count = lim.reset_namespace("u")
        assert count == 2

    def test_reset_namespace_clears_all_resources(self):
        lim = make_limiter()
        lim.add_limit(api_limit())
        lim.add_limit(ResourceLimit("bytes", limit=100.0, window=10.0))
        lim.consume("u", "api_calls", amount=5.0)
        lim.consume("u", "bytes", amount=50.0)
        lim.reset_namespace("u")
        assert lim.usage("u", "api_calls") == 0.0
        assert lim.usage("u", "bytes") == 0.0

    def test_reset_namespace_returns_zero_for_empty_namespace(self):
        lim = make_limiter()
        assert lim.reset_namespace("nobody") == 0

    def test_reset_namespace_does_not_affect_other_namespaces(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.consume("u1", "api_calls", amount=3.0)
        lim.consume("u2", "api_calls", amount=7.0)
        lim.reset_namespace("u1")
        assert lim.usage("u2", "api_calls") == 7.0


# =========================================================================== #
#  No limit defined                                                             #
# =========================================================================== #

class TestNoLimitDefined:
    def test_no_limit_returns_allowed(self):
        lim = make_limiter()
        rec = lim.consume("u", "custom_metric")
        assert rec.result is LimitResult.ALLOWED

    def test_no_limit_tracks_usage(self):
        lim = make_limiter()
        lim.consume("u", "custom_metric", amount=42.0)
        assert lim.usage("u", "custom_metric") == 42.0

    def test_no_limit_infinite_consumes_all_allowed(self):
        lim = make_limiter()
        results = [lim.consume("u", "free", amount=1e9).result for _ in range(5)]
        assert all(r is LimitResult.ALLOWED for r in results)

    def test_no_limit_used_field_reflects_amount(self):
        lim = make_limiter()
        rec = lim.consume("u", "x", amount=7.5)
        assert rec.used == pytest.approx(7.5)

    def test_no_limit_limit_field_is_inf(self):
        lim = make_limiter()
        rec = lim.consume("u", "x")
        assert rec.limit == float("inf")


# =========================================================================== #
#  Multiple namespaces / resources independence                                 #
# =========================================================================== #

class TestIsolation:
    def test_namespaces_independent(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=3))
        for _ in range(3):
            lim.consume("user_a", "api_calls")
        # user_a is at limit; user_b should still be ALLOWED
        rec = lim.consume("user_b", "api_calls")
        assert rec.result is LimitResult.ALLOWED

    def test_resources_independent(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=2, window=60.0))
        lim.add_limit(ResourceLimit("bytes", limit=100.0, window=60.0))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        # api_calls exhausted, bytes untouched
        rec = lim.consume("u", "bytes", amount=50.0)
        assert rec.result is LimitResult.ALLOWED

    def test_namespace_counts_separate(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.consume("a", "api_calls", amount=3.0)
        lim.consume("b", "api_calls", amount=7.0)
        assert lim.usage("a", "api_calls") == 3.0
        assert lim.usage("b", "api_calls") == 7.0

    def test_remaining_separate_per_namespace(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.consume("a", "api_calls", amount=4.0)
        lim.consume("b", "api_calls", amount=9.0)
        assert lim.remaining("a", "api_calls") == 6.0
        assert lim.remaining("b", "api_calls") == 1.0


# =========================================================================== #
#  add_limit overwrites existing                                                #
# =========================================================================== #

class TestAddLimitOverwrite:
    def test_overwrite_increases_limit(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=2))
        lim.consume("u", "api_calls")
        lim.consume("u", "api_calls")
        # At limit under old config; now increase it
        lim.add_limit(api_limit(limit=10))
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED

    def test_overwrite_decreases_limit(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10))
        lim.consume("u", "api_calls", amount=3.0)
        # Shrink limit below current usage
        lim.add_limit(api_limit(limit=2))
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.DENIED

    def test_overwrite_changes_warn_threshold(self):
        lim = make_limiter()
        lim.add_limit(api_limit(limit=10, warn_threshold=None))
        lim.consume("u", "api_calls", amount=5.0)
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED
        # Now set warn_threshold below current+amount
        lim.add_limit(api_limit(limit=10, warn_threshold=5.0))
        # usage is 6, threshold is 5 → next consume should warn
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.WARNING


# =========================================================================== #
#  Thread safety                                                                #
# =========================================================================== #

class TestThreadSafety:
    def test_concurrent_consume_does_not_exceed_limit(self):
        """100 threads each calling consume once; with limit=50 exactly 50 succeed."""
        lim = make_limiter()
        lim.add_limit(api_limit(limit=50, window=3600.0))

        allowed = []
        lock = threading.Lock()

        def worker():
            rec = lim.consume("u", "api_calls")
            if rec.result is not LimitResult.DENIED:
                with lock:
                    allowed.append(1)

        threads = [threading.Thread(target=worker) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(allowed) == 50
        assert lim.usage("u", "api_calls") == 50.0

    def test_concurrent_consume_final_usage_consistent(self):
        """Sequential increments from multiple threads must be coherent."""
        lim = make_limiter()
        lim.add_limit(api_limit(limit=1000, window=3600.0))

        def worker():
            for _ in range(10):
                lim.consume("u", "api_calls")

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert lim.usage("u", "api_calls") == 100.0

    def test_concurrent_multiple_namespaces(self):
        """Each of 5 namespaces, 10 threads each, limit=20 per namespace."""
        lim = make_limiter()
        lim.add_limit(api_limit(limit=20, window=3600.0))

        def worker(ns):
            for _ in range(5):
                lim.consume(ns, "api_calls")

        threads = []
        for ns_idx in range(5):
            ns = f"ns{ns_idx}"
            for _ in range(10):
                threads.append(threading.Thread(target=worker, args=(ns,)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for ns_idx in range(5):
            ns = f"ns{ns_idx}"
            assert lim.usage(ns, "api_calls") == 20.0


# =========================================================================== #
#  Lifecycle                                                                    #
# =========================================================================== #

class TestLifecycle:
    def test_close_does_not_raise(self):
        lim = make_limiter()
        lim.close()   # should not raise

    def test_in_memory_db_path(self):
        """Explicit :memory: path works."""
        lim = ResourceLimiter(db_path=":memory:")
        lim.add_limit(api_limit())
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED
        lim.close()

    def test_file_db_path(self, tmp_path):
        """Persistent file-backed DB works across open/close."""
        db = str(tmp_path / "limits.db")
        lim = ResourceLimiter(db_path=db)
        lim.add_limit(api_limit(limit=5))
        lim.consume("u", "api_calls", amount=3.0)
        lim.close()

        # Reopen; usage should be persisted
        lim2 = ResourceLimiter(db_path=db)
        assert lim2.usage("u", "api_calls") == 3.0
        lim2.close()

    def test_custom_now_fn(self):
        clock = VirtualClock(start=500.0)
        lim = ResourceLimiter(db_path=":memory:", now_fn=clock)
        lim.add_limit(api_limit(limit=1, window=10.0))
        lim.consume("u", "api_calls")
        # Advance clock manually
        clock.advance(20.0)
        rec = lim.consume("u", "api_calls")
        assert rec.result is LimitResult.ALLOWED
        lim.close()
