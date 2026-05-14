"""Tests for docstoolkit.throttle_meter."""
import math

import pytest

from docstoolkit.throttle_meter import (
    Bucket,
    ThrottleConfig,
    ThrottleMeter,
    ThrottleResult,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestThrottleConfig:
    def test_basic_fields(self):
        cfg = ThrottleConfig(capacity=10, refill_rate=1.5)
        assert cfg.capacity == 10
        assert cfg.refill_rate == 1.5

    def test_equality(self):
        a = ThrottleConfig(capacity=5, refill_rate=2.0)
        b = ThrottleConfig(capacity=5, refill_rate=2.0)
        assert a == b

    def test_inequality(self):
        a = ThrottleConfig(capacity=5, refill_rate=2.0)
        b = ThrottleConfig(capacity=6, refill_rate=2.0)
        assert a != b


class TestBucket:
    def test_basic_fields(self):
        b = Bucket(
            key="k", capacity=10, refill_rate=2.0, tokens=5.0, last_refill=0.0
        )
        assert b.key == "k"
        assert b.capacity == 10
        assert b.refill_rate == 2.0
        assert b.tokens == 5.0
        assert b.last_refill == 0.0

    def test_independent_instances(self):
        b1 = Bucket("a", 10, 1.0, 5.0, 0.0)
        b2 = Bucket("a", 10, 1.0, 5.0, 0.0)
        b1.tokens = 2.0
        assert b2.tokens == 5.0


class TestThrottleResult:
    def test_allowed_result(self):
        r = ThrottleResult(allowed=True, tokens_remaining=9.0, retry_after_seconds=0.0)
        assert r.allowed
        assert r.tokens_remaining == 9.0
        assert r.retry_after_seconds == 0.0

    def test_denied_result(self):
        r = ThrottleResult(allowed=False, tokens_remaining=0.5, retry_after_seconds=2.0)
        assert not r.allowed
        assert r.retry_after_seconds == 2.0


# ---------------------------------------------------------------------------
# Configure / get_config
# ---------------------------------------------------------------------------


class TestConfigure:
    def test_configure_returns_config(self):
        tm = ThrottleMeter()
        cfg = tm.configure("k", capacity=10, refill_rate=1.0)
        assert isinstance(cfg, ThrottleConfig)
        assert cfg.capacity == 10
        assert cfg.refill_rate == 1.0

    def test_configure_creates_full_bucket(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=1.0)
        bucket = tm.peek("k", now=0.0)
        assert bucket is not None
        assert bucket.tokens == 10.0

    def test_reconfigure_resets_bucket(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=1.0)
        tm.acquire("k", tokens=5, now=0.0)
        tm.configure("k", capacity=20, refill_rate=2.0)
        bucket = tm.peek("k", now=0.0)
        assert bucket.capacity == 20
        assert bucket.tokens == 20.0
        assert bucket.refill_rate == 2.0

    def test_configure_negative_capacity_raises(self):
        tm = ThrottleMeter()
        with pytest.raises(ValueError):
            tm.configure("k", capacity=-1, refill_rate=1.0)

    def test_configure_negative_refill_raises(self):
        tm = ThrottleMeter()
        with pytest.raises(ValueError):
            tm.configure("k", capacity=10, refill_rate=-1.0)


class TestGetConfig:
    def test_get_existing(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=0.5)
        cfg = tm.get_config("k")
        assert cfg is not None
        assert cfg.capacity == 5
        assert cfg.refill_rate == 0.5

    def test_get_missing(self):
        tm = ThrottleMeter()
        assert tm.get_config("nope") is None


# ---------------------------------------------------------------------------
# Acquire — basic / burst / denied / refill
# ---------------------------------------------------------------------------


class TestAcquireBasic:
    def test_single_token(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        r = tm.acquire("k", tokens=1, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 4.0
        assert r.retry_after_seconds == 0.0

    def test_default_token_count_is_one(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        r = tm.acquire("k", now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 4.0

    def test_sequential_acquires(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=3, refill_rate=0.0)
        assert tm.acquire("k", tokens=1, now=0.0).allowed
        assert tm.acquire("k", tokens=1, now=0.0).allowed
        assert tm.acquire("k", tokens=1, now=0.0).allowed
        assert not tm.acquire("k", tokens=1, now=0.0).allowed

    def test_negative_tokens_raises(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        with pytest.raises(ValueError):
            tm.acquire("k", tokens=-1, now=0.0)


class TestAcquireBurst:
    def test_full_capacity_at_once(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=1.0)
        r = tm.acquire("k", tokens=10, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 0.0

    def test_burst_then_denied(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=1.0)
        tm.acquire("k", tokens=10, now=0.0)
        r = tm.acquire("k", tokens=1, now=0.0)
        assert not r.allowed
        assert r.retry_after_seconds == pytest.approx(1.0)

    def test_zero_tokens_always_allowed(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=2, refill_rate=1.0)
        tm.acquire("k", tokens=2, now=0.0)
        r = tm.acquire("k", tokens=0, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 0.0


class TestAcquireDenied:
    def test_denied_returns_retry_after(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=2.0)  # 2 tokens/sec
        tm.acquire("k", tokens=5, now=0.0)
        r = tm.acquire("k", tokens=4, now=0.0)
        assert not r.allowed
        # need 4 tokens, have 0, refill 2/s → 2.0s
        assert r.retry_after_seconds == pytest.approx(2.0)

    def test_denied_when_request_exceeds_capacity(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=3, refill_rate=1.0)
        r = tm.acquire("k", tokens=10, now=0.0)
        assert not r.allowed
        # need 10, have 3, refill 1/s → 7s
        assert r.retry_after_seconds == pytest.approx(7.0)

    def test_denied_with_zero_refill(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=2, refill_rate=0.0)
        tm.acquire("k", tokens=2, now=0.0)
        r = tm.acquire("k", tokens=1, now=10.0)
        assert not r.allowed
        assert r.retry_after_seconds == float("inf")

    def test_denied_tokens_remaining_reported(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        tm.acquire("k", tokens=4, now=0.0)
        r = tm.acquire("k", tokens=3, now=0.0)
        assert not r.allowed
        assert r.tokens_remaining == pytest.approx(1.0)


class TestRefill:
    def test_refills_over_time(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=2.0)
        tm.acquire("k", tokens=10, now=0.0)
        r = tm.acquire("k", tokens=4, now=2.0)
        # after 2s, +4 tokens, take 4 → 0 remaining
        assert r.allowed
        assert r.tokens_remaining == pytest.approx(0.0)

    def test_refill_clamps_to_capacity(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=5.0)
        tm.acquire("k", tokens=2, now=0.0)
        # 100 seconds later, would be 8 + 500 = 508, but cap at 10
        r = tm.acquire("k", tokens=10, now=100.0)
        assert r.allowed
        assert r.tokens_remaining == pytest.approx(0.0)

    def test_partial_refill_fractional(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        tm.acquire("k", tokens=5, now=0.0)
        r = tm.acquire("k", tokens=1, now=0.5)
        # 0.5s → +0.5 tokens → 0.5 < 1 → denied
        assert not r.allowed
        assert r.retry_after_seconds == pytest.approx(0.5)

    def test_refill_with_zero_rate(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=0.0)
        tm.acquire("k", tokens=5, now=0.0)
        r = tm.acquire("k", tokens=1, now=1000.0)
        assert not r.allowed

    def test_backwards_clock_does_not_drain(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        tm.acquire("k", tokens=2, now=10.0)  # 3 remaining
        # Clock goes backwards
        r = tm.acquire("k", tokens=1, now=5.0)
        assert r.allowed
        # No spurious refill should put it above 3 (after we took 1 → 2)
        assert r.tokens_remaining == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# Peek
# ---------------------------------------------------------------------------


class TestPeek:
    def test_peek_full_bucket(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        b = tm.peek("k", now=0.0)
        assert b is not None
        assert b.tokens == 5.0
        assert b.capacity == 5

    def test_peek_does_not_mutate(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=1.0)
        tm.acquire("k", tokens=5, now=0.0)
        # Peek at a much later time
        b1 = tm.peek("k", now=100.0)
        assert b1.tokens == 10.0  # capped at capacity in snapshot
        # Now acquire at later time — should still see full refill
        r = tm.acquire("k", tokens=10, now=100.0)
        assert r.allowed
        assert r.tokens_remaining == pytest.approx(0.0)

    def test_peek_missing_key_returns_none(self):
        tm = ThrottleMeter()
        assert tm.peek("missing", now=0.0) is None

    def test_peek_default_config(self):
        tm = ThrottleMeter()
        tm.configure_default(capacity=3, refill_rate=1.0)
        b = tm.peek("k", now=0.0)
        assert b is not None
        assert b.capacity == 3
        assert b.tokens == 3.0
        # Did not register an actual bucket
        assert tm.all_keys() == []


# ---------------------------------------------------------------------------
# wait_time
# ---------------------------------------------------------------------------


class TestWaitTime:
    def test_zero_when_enough(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        assert tm.wait_time("k", tokens=3, now=0.0) == 0.0

    def test_positive_when_short(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=2.0)
        tm.acquire("k", tokens=5, now=0.0)
        # need 4, have 0, refill 2/s → 2s
        assert tm.wait_time("k", tokens=4, now=0.0) == pytest.approx(2.0)

    def test_unconfigured_no_default_raises(self):
        tm = ThrottleMeter()
        with pytest.raises(KeyError):
            tm.wait_time("k", tokens=1, now=0.0)

    def test_uses_default_when_unconfigured(self):
        tm = ThrottleMeter()
        tm.configure_default(capacity=4, refill_rate=1.0)
        assert tm.wait_time("k", tokens=3, now=0.0) == 0.0

    def test_wait_time_does_not_consume(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        tm.wait_time("k", tokens=2, now=0.0)
        b = tm.peek("k", now=0.0)
        assert b.tokens == 5.0

    def test_wait_time_zero_refill_returns_inf(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=2, refill_rate=0.0)
        tm.acquire("k", tokens=2, now=0.0)
        assert math.isinf(tm.wait_time("k", tokens=1, now=10.0))

    def test_negative_tokens_raises(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        with pytest.raises(ValueError):
            tm.wait_time("k", tokens=-1, now=0.0)


# ---------------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------------


class TestReset:
    def test_reset_existing(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        tm.acquire("k", tokens=5, now=0.0)
        assert tm.reset("k") is True
        b = tm.peek("k", now=0.0)
        assert b.tokens == 5.0

    def test_reset_unknown_returns_false(self):
        tm = ThrottleMeter()
        assert tm.reset("nope") is False

    def test_reset_preserves_config(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=7, refill_rate=2.0)
        tm.acquire("k", tokens=4, now=0.0)
        tm.reset("k")
        cfg = tm.get_config("k")
        assert cfg.capacity == 7
        assert cfg.refill_rate == 2.0


class TestResetAll:
    def test_reset_all_count(self):
        tm = ThrottleMeter()
        tm.configure("a", capacity=5, refill_rate=1.0)
        tm.configure("b", capacity=5, refill_rate=1.0)
        tm.configure("c", capacity=5, refill_rate=1.0)
        tm.acquire("a", tokens=3, now=0.0)
        tm.acquire("b", tokens=3, now=0.0)
        n = tm.reset_all()
        assert n == 3

    def test_reset_all_empty(self):
        tm = ThrottleMeter()
        assert tm.reset_all() == 0

    def test_reset_all_restores_full_buckets(self):
        tm = ThrottleMeter()
        tm.configure("a", capacity=5, refill_rate=1.0)
        tm.configure("b", capacity=8, refill_rate=2.0)
        tm.acquire("a", tokens=5, now=0.0)
        tm.acquire("b", tokens=8, now=0.0)
        tm.reset_all()
        assert tm.peek("a", now=0.0).tokens == 5.0
        assert tm.peek("b", now=0.0).tokens == 8.0


# ---------------------------------------------------------------------------
# Default config behaviour
# ---------------------------------------------------------------------------


class TestDefaultConfig:
    def test_uses_default_for_unconfigured_key(self):
        tm = ThrottleMeter()
        tm.configure_default(capacity=3, refill_rate=1.0)
        r = tm.acquire("any_key", tokens=1, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 2.0

    def test_default_does_not_override_specific(self):
        tm = ThrottleMeter()
        tm.configure_default(capacity=3, refill_rate=1.0)
        tm.configure("k", capacity=10, refill_rate=1.0)
        r = tm.acquire("k", tokens=5, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 5.0

    def test_default_returns_config(self):
        tm = ThrottleMeter()
        cfg = tm.configure_default(capacity=4, refill_rate=2.0)
        assert isinstance(cfg, ThrottleConfig)
        assert cfg.capacity == 4
        assert cfg.refill_rate == 2.0

    def test_default_negative_raises(self):
        tm = ThrottleMeter()
        with pytest.raises(ValueError):
            tm.configure_default(capacity=-1, refill_rate=1.0)
        with pytest.raises(ValueError):
            tm.configure_default(capacity=1, refill_rate=-1.0)


class TestUnconfiguredNoDefault:
    def test_acquire_raises_key_error(self):
        tm = ThrottleMeter()
        with pytest.raises(KeyError):
            tm.acquire("missing", tokens=1, now=0.0)

    def test_wait_time_raises_key_error(self):
        tm = ThrottleMeter()
        with pytest.raises(KeyError):
            tm.wait_time("missing", tokens=1, now=0.0)


# ---------------------------------------------------------------------------
# Remove / all_keys / stats
# ---------------------------------------------------------------------------


class TestRemove:
    def test_remove_existing(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        assert tm.remove("k") is True
        assert tm.get_config("k") is None
        assert tm.peek("k", now=0.0) is None

    def test_remove_missing(self):
        tm = ThrottleMeter()
        assert tm.remove("nope") is False

    def test_remove_after_acquire(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=5, refill_rate=1.0)
        tm.acquire("k", tokens=2, now=0.0)
        assert tm.remove("k") is True
        assert "k" not in tm.all_keys()


class TestAllKeys:
    def test_empty(self):
        tm = ThrottleMeter()
        assert tm.all_keys() == []

    def test_sorted(self):
        tm = ThrottleMeter()
        tm.configure("c", capacity=1, refill_rate=1.0)
        tm.configure("a", capacity=1, refill_rate=1.0)
        tm.configure("b", capacity=1, refill_rate=1.0)
        assert tm.all_keys() == ["a", "b", "c"]

    def test_includes_default_created(self):
        tm = ThrottleMeter()
        tm.configure_default(capacity=2, refill_rate=1.0)
        tm.acquire("dyn", tokens=1, now=0.0)
        assert "dyn" in tm.all_keys()


class TestStats:
    def test_empty_stats(self):
        tm = ThrottleMeter()
        s = tm.stats()
        assert s == {"allowed_count": 0, "denied_count": 0, "total_keys": 0}

    def test_allowed_count_increments(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=3, refill_rate=0.0)
        tm.acquire("k", tokens=1, now=0.0)
        tm.acquire("k", tokens=1, now=0.0)
        s = tm.stats()
        assert s["allowed_count"] == 2
        assert s["denied_count"] == 0

    def test_denied_count_increments(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=1, refill_rate=0.0)
        tm.acquire("k", tokens=1, now=0.0)
        tm.acquire("k", tokens=1, now=0.0)
        tm.acquire("k", tokens=1, now=0.0)
        s = tm.stats()
        assert s["allowed_count"] == 1
        assert s["denied_count"] == 2

    def test_total_keys(self):
        tm = ThrottleMeter()
        tm.configure("a", capacity=1, refill_rate=1.0)
        tm.configure("b", capacity=1, refill_rate=1.0)
        assert tm.stats()["total_keys"] == 2


# ---------------------------------------------------------------------------
# Multiple keys & edge cases
# ---------------------------------------------------------------------------


class TestMultipleKeys:
    def test_independent_buckets(self):
        tm = ThrottleMeter()
        tm.configure("a", capacity=5, refill_rate=1.0)
        tm.configure("b", capacity=5, refill_rate=1.0)
        tm.acquire("a", tokens=5, now=0.0)
        r = tm.acquire("b", tokens=5, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 0.0

    def test_independent_refill(self):
        tm = ThrottleMeter()
        tm.configure("a", capacity=10, refill_rate=1.0)
        tm.configure("b", capacity=10, refill_rate=5.0)
        tm.acquire("a", tokens=10, now=0.0)
        tm.acquire("b", tokens=10, now=0.0)
        # After 1s: a has 1, b has 5
        ra = tm.acquire("a", tokens=2, now=1.0)
        rb = tm.acquire("b", tokens=2, now=1.0)
        assert not ra.allowed
        assert rb.allowed

    def test_many_keys(self):
        tm = ThrottleMeter()
        for i in range(50):
            tm.configure(f"k{i}", capacity=1, refill_rate=0.0)
        assert len(tm.all_keys()) == 50
        for i in range(50):
            assert tm.acquire(f"k{i}", tokens=1, now=0.0).allowed


class TestEdgeCases:
    def test_capacity_zero_always_denies(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=0, refill_rate=1.0)
        r = tm.acquire("k", tokens=1, now=0.0)
        assert not r.allowed

    def test_capacity_zero_zero_tokens_allowed(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=0, refill_rate=1.0)
        r = tm.acquire("k", tokens=0, now=0.0)
        assert r.allowed
        assert r.tokens_remaining == 0.0

    def test_zero_refill_rate_no_recovery(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=2, refill_rate=0.0)
        tm.acquire("k", tokens=2, now=0.0)
        for t in (1.0, 10.0, 100.0, 1e9):
            assert not tm.acquire("k", tokens=1, now=t).allowed

    def test_fractional_refill_accumulates(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=10, refill_rate=0.5)
        tm.acquire("k", tokens=10, now=0.0)
        # 4s → +2 tokens
        r = tm.acquire("k", tokens=2, now=4.0)
        assert r.allowed
        assert r.tokens_remaining == pytest.approx(0.0)

    def test_high_refill_rate(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=100, refill_rate=1000.0)
        tm.acquire("k", tokens=100, now=0.0)
        r = tm.acquire("k", tokens=100, now=0.2)
        # 0.2s × 1000/s = 200, capped at 100
        assert r.allowed
        assert r.tokens_remaining == pytest.approx(0.0)

    def test_request_exceeds_capacity_never_satisfied_in_one_shot(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=3, refill_rate=1.0)
        r = tm.acquire("k", tokens=5, now=1000.0)
        assert not r.allowed
        assert r.retry_after_seconds == pytest.approx(2.0)  # 5 - 3 = 2 tokens needed

    def test_acquire_then_reset_then_acquire(self):
        tm = ThrottleMeter()
        tm.configure("k", capacity=2, refill_rate=0.0)
        tm.acquire("k", tokens=2, now=0.0)
        assert not tm.acquire("k", tokens=1, now=0.0).allowed
        tm.reset("k")
        assert tm.acquire("k", tokens=2, now=0.0).allowed
