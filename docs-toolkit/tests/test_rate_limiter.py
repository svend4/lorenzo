"""Tests for docstoolkit.rate_limiter — token bucket, sliding window, limiter, store."""
import math
import time
import pytest

from docstoolkit.rate_limiter import (
    TokenBucket,
    SlidingWindow,
    RateLimiter,
    RateLimitResult,
    LimitConfig,
    RateLimitStore,
)


# ---------------------------------------------------------------------------
# TokenBucket
# ---------------------------------------------------------------------------

class TestTokenBucketBasic:
    def test_full_bucket_allows_first_request(self):
        tb = TokenBucket(capacity=5.0, refill_rate=1.0)
        assert tb.consume() is True

    def test_consume_reduces_tokens(self):
        start = 1000.0
        tb = TokenBucket(capacity=5.0, refill_rate=1.0, _last_refill=start)
        tb.consume(2.0, now=start)
        assert tb.available(now=start) == pytest.approx(3.0, abs=1e-6)

    def test_consume_exact_capacity(self):
        tb = TokenBucket(capacity=3.0, refill_rate=1.0)
        assert tb.consume(3.0) is True

    def test_consume_more_than_capacity_denied(self):
        tb = TokenBucket(capacity=3.0, refill_rate=1.0)
        assert tb.consume(4.0) is False

    def test_consume_more_than_capacity_does_not_modify_tokens(self):
        tb = TokenBucket(capacity=3.0, refill_rate=1.0)
        tb.consume(4.0)
        assert tb.available() == pytest.approx(3.0, abs=1e-6)

    def test_exhaust_bucket_then_denied(self):
        tb = TokenBucket(capacity=2.0, refill_rate=0.0)
        assert tb.consume(1.0) is True
        assert tb.consume(1.0) is True
        assert tb.consume(1.0) is False

    def test_available_returns_float(self):
        tb = TokenBucket(capacity=10.0, refill_rate=1.0)
        result = tb.available()
        assert isinstance(result, float)

    def test_initial_tokens_equal_capacity(self):
        tb = TokenBucket(capacity=7.0, refill_rate=2.0)
        assert tb.available() == pytest.approx(7.0, abs=1e-6)


class TestTokenBucketRefill:
    def test_refill_over_time(self):
        """Consume all tokens, then pass time via now= parameter."""
        start = 1000.0
        tb = TokenBucket(capacity=5.0, refill_rate=5.0, _last_refill=start)
        tb.consume(5.0, now=start)
        assert tb.available(now=start) == pytest.approx(0.0, abs=1e-6)
        # After 1 second at 5 tokens/sec → bucket full again
        assert tb.consume(1.0, now=start + 1.0) is True

    def test_refill_does_not_exceed_capacity(self):
        """Capacity is respected — no overfill."""
        start = 1000.0
        tb = TokenBucket(capacity=5.0, refill_rate=10.0, _last_refill=start)
        # Already full; 2 more seconds should not exceed capacity
        assert tb.available(now=start + 2.0) == pytest.approx(5.0, abs=1e-6)

    def test_partial_refill(self):
        start = 1000.0
        tb = TokenBucket(capacity=10.0, refill_rate=2.0, _last_refill=start)
        tb.consume(10.0, now=start)
        # 3 seconds → 6 tokens refilled
        assert tb.available(now=start + 3.0) == pytest.approx(6.0, abs=1e-6)

    def test_refill_with_zero_elapsed(self):
        start = 1000.0
        tb = TokenBucket(capacity=5.0, refill_rate=5.0, _last_refill=start)
        tb.consume(3.0, now=start)
        assert tb.available(now=start) == pytest.approx(2.0, abs=1e-6)

    def test_consume_after_partial_refill(self):
        start = 1000.0
        tb = TokenBucket(capacity=10.0, refill_rate=1.0, _last_refill=start)
        tb.consume(10.0, now=start)
        # 5 seconds → 5 tokens
        assert tb.consume(5.0, now=start + 5.0) is True

    def test_consume_after_partial_refill_too_many_denied(self):
        start = 1000.0
        tb = TokenBucket(capacity=10.0, refill_rate=1.0, _last_refill=start)
        tb.consume(10.0, now=start)
        # 5 seconds → only 5 tokens, requesting 6 → denied
        assert tb.consume(6.0, now=start + 5.0) is False


class TestTokenBucketTimeUntilAvailable:
    def test_time_until_available_zero_when_tokens_present(self):
        tb = TokenBucket(capacity=5.0, refill_rate=1.0)
        assert tb.time_until_available(1.0) == pytest.approx(0.0, abs=1e-9)

    def test_time_until_available_positive_after_exhaustion(self):
        start = 1000.0
        tb = TokenBucket(capacity=1.0, refill_rate=1.0, _last_refill=start)
        tb.consume(1.0, now=start)
        wait = tb.time_until_available(1.0, now=start)
        assert wait > 0.0

    def test_time_until_available_correct_value(self):
        """Exhaust 10 tokens, need 4 more, rate=2/s → wait=2.0s."""
        start = 1000.0
        tb = TokenBucket(capacity=10.0, refill_rate=2.0, _last_refill=start)
        tb.consume(10.0, now=start)
        wait = tb.time_until_available(4.0, now=start)
        assert wait == pytest.approx(2.0, abs=1e-6)

    def test_time_until_available_zero_rate_returns_inf(self):
        start = 1000.0
        tb = TokenBucket(capacity=1.0, refill_rate=0.0, _last_refill=start)
        tb.consume(1.0, now=start)
        wait = tb.time_until_available(1.0, now=start)
        assert math.isinf(wait)

    def test_time_until_available_exact_capacity(self):
        start = 1000.0
        tb = TokenBucket(capacity=5.0, refill_rate=1.0, _last_refill=start)
        tb.consume(5.0, now=start)
        wait = tb.time_until_available(5.0, now=start)
        assert wait == pytest.approx(5.0, abs=1e-6)


# ---------------------------------------------------------------------------
# SlidingWindow
# ---------------------------------------------------------------------------

class TestSlidingWindowBasic:
    def test_empty_window_allows_first_request(self):
        sw = SlidingWindow(max_requests=3, window_seconds=60.0)
        assert sw.allow() is True

    def test_first_n_requests_allowed(self):
        sw = SlidingWindow(max_requests=3, window_seconds=60.0)
        start = 1000.0
        for i in range(3):
            assert sw.allow(now=start + i * 0.01) is True

    def test_n_plus_one_request_denied(self):
        sw = SlidingWindow(max_requests=3, window_seconds=60.0)
        start = 1000.0
        for i in range(3):
            sw.allow(now=start + i * 0.01)
        assert sw.allow(now=start + 0.1) is False

    def test_old_requests_expire(self):
        sw = SlidingWindow(max_requests=2, window_seconds=10.0)
        start = 1000.0
        sw.allow(now=start)
        sw.allow(now=start + 1.0)
        # Both slots used; denied
        assert sw.allow(now=start + 2.0) is False
        # After full window + 1 second, old requests are pruned
        assert sw.allow(now=start + 11.0) is True

    def test_requests_recorded_correctly(self):
        sw = SlidingWindow(max_requests=5, window_seconds=60.0)
        start = 1000.0
        for i in range(3):
            sw.allow(now=start + float(i))
        assert sw.current_count(now=start + 3.0) == 3

    def test_allow_records_timestamp(self):
        sw = SlidingWindow(max_requests=5, window_seconds=60.0)
        start = 1000.0
        sw.allow(now=start)
        assert len(sw._timestamps) == 1
        assert sw._timestamps[0] == pytest.approx(start)

    def test_denied_does_not_record_timestamp(self):
        sw = SlidingWindow(max_requests=1, window_seconds=60.0)
        start = 1000.0
        sw.allow(now=start)
        sw.allow(now=start + 0.1)  # denied
        assert len(sw._timestamps) == 1


class TestSlidingWindowCounts:
    def test_current_count_zero_on_empty(self):
        sw = SlidingWindow(max_requests=5, window_seconds=60.0)
        assert sw.current_count() == 0

    def test_current_count_after_requests(self):
        sw = SlidingWindow(max_requests=5, window_seconds=60.0)
        start = 1000.0
        for i in range(4):
            sw.allow(now=start + float(i))
        assert sw.current_count(now=start + 4.0) == 4

    def test_remaining_equals_max_on_empty(self):
        sw = SlidingWindow(max_requests=5, window_seconds=60.0)
        assert sw.remaining() == 5

    def test_remaining_decreases_after_requests(self):
        sw = SlidingWindow(max_requests=5, window_seconds=60.0)
        start = 1000.0
        for i in range(3):
            sw.allow(now=start + float(i))
        assert sw.remaining(now=start + 3.0) == 2

    def test_remaining_zero_when_exhausted(self):
        sw = SlidingWindow(max_requests=2, window_seconds=60.0)
        start = 1000.0
        sw.allow(now=start)
        sw.allow(now=start + 0.1)
        assert sw.remaining(now=start + 0.2) == 0

    def test_remaining_never_negative(self):
        sw = SlidingWindow(max_requests=2, window_seconds=60.0)
        start = 1000.0
        for i in range(5):
            sw.allow(now=start + float(i) * 0.1)
        assert sw.remaining(now=start + 1.0) >= 0

    def test_current_count_after_window_expires(self):
        sw = SlidingWindow(max_requests=3, window_seconds=5.0)
        start = 1000.0
        for i in range(3):
            sw.allow(now=start + float(i) * 0.1)
        assert sw.current_count(now=start + 6.0) == 0


# ---------------------------------------------------------------------------
# LimitConfig
# ---------------------------------------------------------------------------

class TestLimitConfig:
    def test_fields(self):
        cfg = LimitConfig(key="user:bob", max_requests=10, window_seconds=60.0)
        assert cfg.key == "user:bob"
        assert cfg.max_requests == 10
        assert cfg.window_seconds == 60.0
        assert cfg.burst == 0

    def test_burst_field(self):
        cfg = LimitConfig(key="api:x", max_requests=5, window_seconds=1.0, burst=10)
        assert cfg.burst == 10


# ---------------------------------------------------------------------------
# RateLimitResult
# ---------------------------------------------------------------------------

class TestRateLimitResult:
    def test_bool_true_when_allowed(self):
        r = RateLimitResult(allowed=True, key="k", remaining=4, retry_after=0.0)
        assert bool(r) is True

    def test_bool_false_when_denied(self):
        r = RateLimitResult(allowed=False, key="k", remaining=0, retry_after=1.0)
        assert bool(r) is False

    def test_retry_after_zero_when_allowed(self):
        r = RateLimitResult(allowed=True, key="k", remaining=3, retry_after=0.0)
        assert r.retry_after == 0.0

    def test_retry_after_positive_when_denied(self):
        r = RateLimitResult(allowed=False, key="k", remaining=0, retry_after=0.5)
        assert r.retry_after > 0.0

    def test_remaining_field(self):
        r = RateLimitResult(allowed=True, key="k", remaining=7, retry_after=0.0)
        assert r.remaining == 7

    def test_key_field(self):
        r = RateLimitResult(allowed=True, key="user:alice", remaining=1, retry_after=0.0)
        assert r.key == "user:alice"


# ---------------------------------------------------------------------------
# RateLimiter
# ---------------------------------------------------------------------------

class TestRateLimiter:
    def _cfg(self, key="user:test", max_requests=3, window_seconds=60.0):
        return LimitConfig(key=key, max_requests=max_requests, window_seconds=window_seconds)

    def test_check_returns_rate_limit_result(self):
        rl = RateLimiter()
        result = rl.check(self._cfg())
        assert isinstance(result, RateLimitResult)

    def test_first_request_allowed(self):
        rl = RateLimiter()
        result = rl.check(self._cfg())
        assert result.allowed is True

    def test_first_n_requests_allowed(self):
        rl = RateLimiter()
        cfg = self._cfg(max_requests=5)
        for _ in range(5):
            assert rl.check(cfg).allowed is True

    def test_n_plus_one_denied(self):
        rl = RateLimiter()
        cfg = self._cfg(max_requests=3)
        for _ in range(3):
            rl.check(cfg)
        result = rl.check(cfg)
        assert result.allowed is False

    def test_reset_clears_state(self):
        rl = RateLimiter()
        cfg = self._cfg(max_requests=1)
        rl.check(cfg)
        assert rl.check(cfg).allowed is False
        rl.reset(cfg.key)
        assert rl.check(cfg).allowed is True

    def test_reset_unknown_key_no_error(self):
        rl = RateLimiter()
        rl.reset("nonexistent")  # should not raise

    def test_stats_contains_key_after_check(self):
        rl = RateLimiter()
        cfg = self._cfg(key="api:search")
        rl.check(cfg)
        s = rl.stats()
        assert "api:search" in s

    def test_stats_count_correct(self):
        rl = RateLimiter()
        cfg = self._cfg(key="api:calc", max_requests=10)
        for _ in range(4):
            rl.check(cfg)
        s = rl.stats()
        assert s["api:calc"] == 4

    def test_different_keys_are_independent(self):
        rl = RateLimiter()
        cfg_a = self._cfg(key="user:a", max_requests=1)
        cfg_b = self._cfg(key="user:b", max_requests=1)
        assert rl.check(cfg_a).allowed is True
        assert rl.check(cfg_b).allowed is True
        # Second request for a denied, b unaffected by a's exhaustion
        assert rl.check(cfg_a).allowed is False
        # b is still at 1 allowed (exhausted now too)
        assert rl.check(cfg_b).allowed is False

    def test_allowed_result_has_non_negative_remaining(self):
        rl = RateLimiter()
        result = rl.check(self._cfg(max_requests=5))
        assert result.remaining >= 0

    def test_denied_result_has_positive_retry_after(self):
        rl = RateLimiter()
        cfg = self._cfg(max_requests=1, window_seconds=30.0)
        rl.check(cfg)
        denied = rl.check(cfg)
        assert denied.retry_after > 0.0

    def test_retry_after_formula(self):
        """retry_after = window_seconds / max_requests when denied."""
        rl = RateLimiter()
        cfg = LimitConfig(key="k", max_requests=6, window_seconds=60.0)
        for _ in range(6):
            rl.check(cfg)
        result = rl.check(cfg)
        assert result.retry_after == pytest.approx(10.0, abs=1e-6)

    def test_allowed_result_retry_after_is_zero(self):
        rl = RateLimiter()
        result = rl.check(self._cfg())
        assert result.retry_after == 0.0

    def test_stats_empty_on_fresh_limiter(self):
        rl = RateLimiter()
        assert rl.stats() == {}

    def test_multiple_keys_in_stats(self):
        rl = RateLimiter()
        for key in ("a", "b", "c"):
            rl.check(LimitConfig(key=key, max_requests=10, window_seconds=60.0))
        s = rl.stats()
        assert set(s.keys()) == {"a", "b", "c"}


# ---------------------------------------------------------------------------
# RateLimitStore
# ---------------------------------------------------------------------------

class TestRateLimitStore:
    def _result(self, key="k", allowed=True, remaining=5):
        return RateLimitResult(
            allowed=allowed,
            key=key,
            remaining=remaining,
            retry_after=0.0 if allowed else 1.0,
        )

    def test_record_and_total_count(self):
        store = RateLimitStore()
        store.record(self._result())
        assert store.total_count("k") == 1

    def test_allowed_count(self):
        store = RateLimitStore()
        store.record(self._result(allowed=True))
        store.record(self._result(allowed=True))
        store.record(self._result(allowed=False))
        assert store.allowed_count("k") == 2

    def test_denied_count(self):
        store = RateLimitStore()
        store.record(self._result(allowed=True))
        store.record(self._result(allowed=False))
        store.record(self._result(allowed=False))
        assert store.denied_count("k") == 2

    def test_total_count_is_sum(self):
        store = RateLimitStore()
        for _ in range(3):
            store.record(self._result(allowed=True))
        for _ in range(2):
            store.record(self._result(allowed=False))
        assert store.total_count("k") == 5
        assert store.allowed_count("k") + store.denied_count("k") == 5

    def test_keys_are_independent(self):
        store = RateLimitStore()
        store.record(self._result(key="a", allowed=True))
        store.record(self._result(key="a", allowed=True))
        store.record(self._result(key="b", allowed=False))
        assert store.allowed_count("a") == 2
        assert store.denied_count("a") == 0
        assert store.allowed_count("b") == 0
        assert store.denied_count("b") == 1

    def test_zero_counts_for_unknown_key(self):
        store = RateLimitStore()
        assert store.total_count("nobody") == 0
        assert store.allowed_count("nobody") == 0
        assert store.denied_count("nobody") == 0

    def test_record_multiple_entries(self):
        store = RateLimitStore()
        for _ in range(10):
            store.record(self._result(allowed=True))
        assert store.total_count("k") == 10

    def test_store_with_file_path(self, tmp_path):
        db_file = tmp_path / "rl.db"
        store = RateLimitStore(db_path=db_file)
        store.record(self._result(allowed=True))
        store.close()
        # Reopen and verify persistence
        store2 = RateLimitStore(db_path=db_file)
        assert store2.total_count("k") == 1
        store2.close()

    def test_close_does_not_raise(self):
        store = RateLimitStore()
        store.close()  # should not raise


# ---------------------------------------------------------------------------
# Integration: RateLimiter + RateLimitStore
# ---------------------------------------------------------------------------

class TestRateLimiterStoreIntegration:
    def test_record_check_results(self):
        rl = RateLimiter()
        store = RateLimitStore()
        cfg = LimitConfig(key="user:x", max_requests=2, window_seconds=60.0)
        for _ in range(4):
            result = rl.check(cfg)
            store.record(result)
        assert store.allowed_count("user:x") == 2
        assert store.denied_count("user:x") == 2
        assert store.total_count("user:x") == 4
