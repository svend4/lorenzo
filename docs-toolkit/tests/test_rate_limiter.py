"""Tests for the E52 rate limiter module (docstoolkit.rate_limiter).

Covers:
- TokenBucket  (bucket.py)
- FixedWindowCounter  (bucket.py)
- SlidingWindowCounter  (bucket.py)
- RateLimiter  (registry.py)
- RateLimitResult / RateLimitConfig / RateLimitStrategy  (limiter.py)
- Legacy types preserved for backwards-compatibility
"""
import math
import time
import threading
import pytest

from docstoolkit.rate_limiter import (
    RateLimitStrategy,
    RateLimitConfig,
    RateLimitResult,
    TokenBucket,
    FixedWindowCounter,
    SlidingWindowCounter,
    RateLimiter,
)
# Legacy imports must still work
from docstoolkit.rate_limiter import (
    LimitConfig,
    SlidingWindow,
    RateLimitStore,
    _LegacyRateLimiter,
    _LegacyRateLimitResult,
)

# =========================================================================== #
#  RateLimitStrategy & RateLimitConfig                                         #
# =========================================================================== #

class TestRateLimitConfig:
    def test_default_strategy_is_sliding_window(self):
        cfg = RateLimitConfig()
        assert cfg.strategy is RateLimitStrategy.SLIDING_WINDOW

    def test_default_requests_per_second(self):
        cfg = RateLimitConfig()
        assert cfg.requests_per_second == 10.0

    def test_default_burst_size(self):
        cfg = RateLimitConfig()
        assert cfg.burst_size == 20

    def test_default_window_seconds(self):
        cfg = RateLimitConfig()
        assert cfg.window_seconds == 1.0

    def test_custom_strategy(self):
        cfg = RateLimitConfig(strategy=RateLimitStrategy.TOKEN_BUCKET)
        assert cfg.strategy is RateLimitStrategy.TOKEN_BUCKET

    def test_custom_requests_per_second(self):
        cfg = RateLimitConfig(requests_per_second=5.0)
        assert cfg.requests_per_second == 5.0

    def test_custom_burst_size(self):
        cfg = RateLimitConfig(burst_size=50)
        assert cfg.burst_size == 50

    def test_strategy_enum_values(self):
        assert RateLimitStrategy.FIXED_WINDOW.value == "fixed_window"
        assert RateLimitStrategy.SLIDING_WINDOW.value == "sliding_window"
        assert RateLimitStrategy.TOKEN_BUCKET.value == "token_bucket"

    def test_config_is_dataclass(self):
        cfg = RateLimitConfig(requests_per_second=2.0, burst_size=5)
        assert cfg.requests_per_second == 2.0
        assert cfg.burst_size == 5


# =========================================================================== #
#  RateLimitResult                                                              #
# =========================================================================== #

class TestRateLimitResult:
    def test_allowed_true(self):
        r = RateLimitResult(allowed=True, remaining=5, reset_after=0.0, retry_after=0.0)
        assert r.allowed is True

    def test_allowed_false(self):
        r = RateLimitResult(allowed=False, remaining=0, reset_after=1.0, retry_after=1.0)
        assert r.allowed is False

    def test_remaining_field(self):
        r = RateLimitResult(allowed=True, remaining=7, reset_after=0.0, retry_after=0.0)
        assert r.remaining == 7

    def test_reset_after_zero_when_allowed(self):
        r = RateLimitResult(allowed=True, remaining=3, reset_after=0.0, retry_after=0.0)
        assert r.reset_after == 0.0

    def test_retry_after_zero_when_allowed(self):
        r = RateLimitResult(allowed=True, remaining=3, reset_after=0.0, retry_after=0.0)
        assert r.retry_after == 0.0

    def test_retry_after_positive_when_denied(self):
        r = RateLimitResult(allowed=False, remaining=0, reset_after=0.5, retry_after=0.5)
        assert r.retry_after > 0.0

    def test_reset_after_positive_when_denied(self):
        r = RateLimitResult(allowed=False, remaining=0, reset_after=2.0, retry_after=2.0)
        assert r.reset_after > 0.0

    def test_remaining_zero_when_exhausted(self):
        r = RateLimitResult(allowed=False, remaining=0, reset_after=1.0, retry_after=1.0)
        assert r.remaining == 0


# =========================================================================== #
#  TokenBucket                                                                  #
# =========================================================================== #

class TestTokenBucketConsume:
    def test_consume_single_allowed(self):
        tb = TokenBucket(capacity=5, refill_rate=1.0)
        result = tb.consume()
        assert result.allowed is True

    def test_consume_returns_rate_limit_result(self):
        tb = TokenBucket(capacity=5, refill_rate=1.0)
        result = tb.consume()
        assert isinstance(result, RateLimitResult)

    def test_consume_multiple_tokens(self):
        tb = TokenBucket(capacity=10, refill_rate=1.0)
        result = tb.consume(5)
        assert result.allowed is True

    def test_consume_reduces_available(self):
        tb = TokenBucket(capacity=10, refill_rate=0.0)
        tb.consume(3)
        assert tb.available() == 7

    def test_consume_exact_capacity(self):
        tb = TokenBucket(capacity=5, refill_rate=0.0)
        result = tb.consume(5)
        assert result.allowed is True

    def test_consume_over_capacity_denied(self):
        tb = TokenBucket(capacity=5, refill_rate=0.0)
        result = tb.consume(6)
        assert result.allowed is False

    def test_consume_over_capacity_does_not_modify_tokens(self):
        tb = TokenBucket(capacity=5, refill_rate=0.0)
        tb.consume(6)
        assert tb.available() == 5

    def test_exhaust_then_denied(self):
        tb = TokenBucket(capacity=3, refill_rate=0.0)
        for _ in range(3):
            tb.consume()
        result = tb.consume()
        assert result.allowed is False

    def test_remaining_decreases_after_consume(self):
        tb = TokenBucket(capacity=10, refill_rate=0.0)
        r1 = tb.consume(3)
        assert r1.remaining == 7

    def test_retry_after_zero_when_allowed(self):
        tb = TokenBucket(capacity=5, refill_rate=1.0)
        result = tb.consume()
        assert result.retry_after == 0.0

    def test_retry_after_positive_when_denied(self):
        tb = TokenBucket(capacity=1, refill_rate=1.0)
        tb.consume()
        result = tb.consume()
        assert result.retry_after > 0.0

    def test_reset_after_positive_when_denied(self):
        tb = TokenBucket(capacity=1, refill_rate=1.0)
        tb.consume()
        result = tb.consume()
        assert result.reset_after > 0.0

    def test_burst_capacity(self):
        """All burst tokens can be consumed in one go."""
        tb = TokenBucket(capacity=20, refill_rate=1.0)
        result = tb.consume(20)
        assert result.allowed is True


class TestTokenBucketRefill:
    def test_refill_over_time(self):
        """Consume all; sleep 0.1s; partial refill allows new consume."""
        tb = TokenBucket(capacity=10, refill_rate=20.0)  # 20 tok/s → 2 tok in 0.1s
        # exhaust
        for _ in range(10):
            tb.consume()
        assert tb.available() == 0
        time.sleep(0.1)
        # expect at least 1 token refilled
        assert tb.available() >= 1

    def test_refill_does_not_exceed_capacity(self):
        """A full bucket cannot overflow after time passes."""
        tb = TokenBucket(capacity=5, refill_rate=100.0)
        time.sleep(0.05)
        assert tb.available() <= 5

    def test_consume_after_refill_allowed(self):
        tb = TokenBucket(capacity=2, refill_rate=20.0)  # refill quickly
        tb.consume(2)
        assert tb.available() == 0
        time.sleep(0.1)
        result = tb.consume()
        assert result.allowed is True

    def test_reset_restores_full_capacity(self):
        tb = TokenBucket(capacity=5, refill_rate=0.0)
        tb.consume(5)
        assert tb.available() == 0
        tb.reset()
        assert tb.available() == 5

    def test_reset_allows_new_consume(self):
        tb = TokenBucket(capacity=1, refill_rate=0.0)
        tb.consume()
        tb.reset()
        result = tb.consume()
        assert result.allowed is True


class TestTokenBucketThreadSafety:
    def test_concurrent_consume_no_over_drain(self):
        """No more tokens should be consumed than the bucket contains."""
        capacity = 50
        tb = TokenBucket(capacity=capacity, refill_rate=0.0)
        successes = []
        lock = threading.Lock()

        def worker():
            result = tb.consume()
            if result.allowed:
                with lock:
                    successes.append(1)

        threads = [threading.Thread(target=worker) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(successes) <= capacity


# =========================================================================== #
#  FixedWindowCounter                                                           #
# =========================================================================== #

class TestFixedWindowCounter:
    def test_first_request_allowed(self):
        fw = FixedWindowCounter(limit=5, window_seconds=60.0)
        assert fw.increment().allowed is True

    def test_returns_rate_limit_result(self):
        fw = FixedWindowCounter(limit=5, window_seconds=60.0)
        assert isinstance(fw.increment(), RateLimitResult)

    def test_under_limit_allowed(self):
        fw = FixedWindowCounter(limit=5, window_seconds=60.0)
        for _ in range(4):
            assert fw.increment().allowed is True

    def test_at_limit_allowed(self):
        fw = FixedWindowCounter(limit=3, window_seconds=60.0)
        for _ in range(3):
            fw.increment()
        # fourth should be denied
        assert fw.increment().allowed is False

    def test_over_limit_denied(self):
        fw = FixedWindowCounter(limit=2, window_seconds=60.0)
        fw.increment()
        fw.increment()
        result = fw.increment()
        assert result.allowed is False

    def test_remaining_decreases(self):
        fw = FixedWindowCounter(limit=5, window_seconds=60.0)
        r = fw.increment()
        assert r.remaining == 4

    def test_remaining_zero_at_limit(self):
        fw = FixedWindowCounter(limit=1, window_seconds=60.0)
        r = fw.increment()
        assert r.remaining == 0

    def test_retry_after_zero_when_allowed(self):
        fw = FixedWindowCounter(limit=5, window_seconds=60.0)
        r = fw.increment()
        assert r.retry_after == 0.0

    def test_retry_after_positive_when_denied(self):
        fw = FixedWindowCounter(limit=1, window_seconds=60.0)
        fw.increment()
        r = fw.increment()
        assert r.retry_after > 0.0

    def test_window_expiry_resets_counter(self):
        """After the window expires the counter resets and requests are allowed again."""
        fw = FixedWindowCounter(limit=2, window_seconds=0.1)
        fw.increment()
        fw.increment()
        assert fw.increment().allowed is False
        time.sleep(0.15)
        assert fw.increment().allowed is True

    def test_reset_clears_counter(self):
        fw = FixedWindowCounter(limit=1, window_seconds=60.0)
        fw.increment()
        assert fw.increment().allowed is False
        fw.reset()
        assert fw.increment().allowed is True

    def test_reset_after_is_finite(self):
        fw = FixedWindowCounter(limit=5, window_seconds=1.0)
        r = fw.increment()
        assert math.isfinite(r.reset_after)


# =========================================================================== #
#  SlidingWindowCounter                                                         #
# =========================================================================== #

class TestSlidingWindowCounter:
    def test_first_request_allowed(self):
        sw = SlidingWindowCounter(limit=5, window_seconds=60.0)
        assert sw.increment().allowed is True

    def test_returns_rate_limit_result(self):
        sw = SlidingWindowCounter(limit=5, window_seconds=60.0)
        assert isinstance(sw.increment(), RateLimitResult)

    def test_under_limit_allowed(self):
        sw = SlidingWindowCounter(limit=5, window_seconds=60.0)
        for _ in range(4):
            assert sw.increment().allowed is True

    def test_at_limit_denied(self):
        sw = SlidingWindowCounter(limit=3, window_seconds=60.0)
        for _ in range(3):
            sw.increment()
        result = sw.increment()
        assert result.allowed is False

    def test_remaining_decreases(self):
        sw = SlidingWindowCounter(limit=5, window_seconds=60.0)
        r = sw.increment()
        assert r.remaining == 4

    def test_remaining_zero_when_exhausted(self):
        sw = SlidingWindowCounter(limit=2, window_seconds=60.0)
        sw.increment()
        sw.increment()
        r = sw.increment()
        assert r.remaining == 0

    def test_retry_after_zero_when_allowed(self):
        sw = SlidingWindowCounter(limit=5, window_seconds=60.0)
        assert sw.increment().retry_after == 0.0

    def test_retry_after_positive_when_denied(self):
        sw = SlidingWindowCounter(limit=1, window_seconds=60.0)
        sw.increment()
        r = sw.increment()
        assert r.retry_after > 0.0

    def test_old_entries_evicted_allow_new_request(self):
        """Old timestamps slide out of the window so new requests are allowed."""
        sw = SlidingWindowCounter(limit=2, window_seconds=0.1)
        sw.increment()
        sw.increment()
        assert sw.increment().allowed is False
        time.sleep(0.15)
        assert sw.increment().allowed is True

    def test_reset_clears_timestamps(self):
        sw = SlidingWindowCounter(limit=1, window_seconds=60.0)
        sw.increment()
        assert sw.increment().allowed is False
        sw.reset()
        assert sw.increment().allowed is True

    def test_window_tracking_precise(self):
        """Only requests within the window count toward the limit."""
        sw = SlidingWindowCounter(limit=3, window_seconds=0.1)
        sw.increment()
        sw.increment()
        sw.increment()
        assert sw.increment().allowed is False
        time.sleep(0.12)
        # All old entries evicted; all 3 slots free again
        for _ in range(3):
            assert sw.increment().allowed is True

    def test_reset_after_non_negative(self):
        sw = SlidingWindowCounter(limit=1, window_seconds=1.0)
        sw.increment()
        r = sw.increment()
        assert r.reset_after >= 0.0


# =========================================================================== #
#  RateLimiter (registry)                                                       #
# =========================================================================== #

class TestRateLimiterDefaults:
    def test_instantiate_no_args(self):
        rl = RateLimiter()
        assert rl is not None

    def test_default_config_is_sliding_window(self):
        rl = RateLimiter()
        assert rl._config.strategy is RateLimitStrategy.SLIDING_WINDOW

    def test_keys_empty_on_fresh_instance(self):
        rl = RateLimiter()
        assert rl.keys() == []

    def test_check_returns_rate_limit_result(self):
        rl = RateLimiter()
        result = rl.check("user:alice")
        assert isinstance(result, RateLimitResult)

    def test_first_check_allowed(self):
        rl = RateLimiter()
        result = rl.check("user:alice")
        assert result.allowed is True

    def test_key_created_after_first_check(self):
        rl = RateLimiter()
        rl.check("user:bob")
        assert "user:bob" in rl.keys()


class TestRateLimiterPerKeyIsolation:
    def test_different_keys_are_independent(self):
        # limit = requests_per_second * window_seconds = 1.0 * 1.0 = 1
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            requests_per_second=1.0,
            window_seconds=1.0,
        )
        rl = RateLimiter(config=cfg)
        # exhaust key_a
        rl.check("key_a")
        r_a = rl.check("key_a")
        assert r_a.allowed is False
        # key_b is unaffected
        r_b = rl.check("key_b")
        assert r_b.allowed is True

    def test_multiple_keys_tracked(self):
        rl = RateLimiter()
        for k in ("x", "y", "z"):
            rl.check(k)
        assert set(rl.keys()) == {"x", "y", "z"}

    def test_keys_sorted(self):
        rl = RateLimiter()
        for k in ("c", "a", "b"):
            rl.check(k)
        assert rl.keys() == ["a", "b", "c"]


class TestRateLimiterReset:
    def test_reset_single_key(self):
        # limit = requests_per_second * window_seconds = 1.0 * 1.0 = 1
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            requests_per_second=1.0,
            window_seconds=1.0,
        )
        rl = RateLimiter(config=cfg)
        rl.check("k")
        assert rl.check("k").allowed is False
        rl.reset("k")
        assert rl.check("k").allowed is True

    def test_reset_unknown_key_no_error(self):
        rl = RateLimiter()
        rl.reset("does_not_exist")  # must not raise

    def test_reset_all(self):
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            requests_per_second=1.0,
            window_seconds=60.0,
        )
        rl = RateLimiter(config=cfg)
        for k in ("a", "b", "c"):
            rl.check(k)
            rl.check(k)  # exhaust
        rl.reset_all()
        for k in ("a", "b", "c"):
            assert rl.check(k).allowed is True

    def test_keys_still_present_after_reset(self):
        """reset() resets the counter but keeps the key registered."""
        rl = RateLimiter()
        rl.check("k")
        rl.reset("k")
        assert "k" in rl.keys()


class TestRateLimiterStrategies:
    def test_token_bucket_strategy(self):
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.TOKEN_BUCKET,
            requests_per_second=10.0,
            burst_size=5,
        )
        rl = RateLimiter(config=cfg)
        for _ in range(5):
            assert rl.check("k").allowed is True
        assert rl.check("k").allowed is False

    def test_fixed_window_strategy(self):
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.FIXED_WINDOW,
            requests_per_second=2.0,
            window_seconds=1.0,
        )
        rl = RateLimiter(config=cfg)
        # limit = 2 * 1 = 2
        assert rl.check("k").allowed is True
        assert rl.check("k").allowed is True
        assert rl.check("k").allowed is False

    def test_sliding_window_strategy(self):
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            requests_per_second=3.0,
            window_seconds=1.0,
        )
        rl = RateLimiter(config=cfg)
        # limit = 3 * 1 = 3
        for _ in range(3):
            assert rl.check("k").allowed is True
        assert rl.check("k").allowed is False

    def test_custom_config_passed_correctly(self):
        cfg = RateLimitConfig(
            strategy=RateLimitStrategy.TOKEN_BUCKET,
            burst_size=10,
            requests_per_second=5.0,
        )
        rl = RateLimiter(config=cfg)
        assert rl._config.burst_size == 10
        assert rl._config.requests_per_second == 5.0


# =========================================================================== #
#  Legacy backwards-compatibility                                               #
# =========================================================================== #

class TestLegacyCompatibility:
    def test_legacy_limit_config_fields(self):
        cfg = LimitConfig(key="user:bob", max_requests=10, window_seconds=60.0)
        assert cfg.key == "user:bob"
        assert cfg.max_requests == 10
        assert cfg.window_seconds == 60.0
        assert cfg.burst == 0

    def test_legacy_limiter_check_allowed(self):
        rl = _LegacyRateLimiter()
        cfg = LimitConfig(key="x", max_requests=5, window_seconds=60.0)
        result = rl.check(cfg)
        assert result.allowed is True

    def test_legacy_limiter_check_denied(self):
        rl = _LegacyRateLimiter()
        cfg = LimitConfig(key="x", max_requests=1, window_seconds=60.0)
        rl.check(cfg)
        result = rl.check(cfg)
        assert result.allowed is False

    def test_legacy_result_has_key_field(self):
        rl = _LegacyRateLimiter()
        cfg = LimitConfig(key="user:alice", max_requests=5, window_seconds=60.0)
        result = rl.check(cfg)
        assert result.key == "user:alice"

    def test_legacy_sliding_window_allow(self):
        sw = SlidingWindow(max_requests=3, window_seconds=60.0)
        start = 1000.0
        for i in range(3):
            assert sw.allow(now=start + float(i)) is True
        assert sw.allow(now=start + 3.0) is False

    def test_rate_limit_store_record_and_count(self):
        store = RateLimitStore()
        result = _LegacyRateLimitResult(
            allowed=True, key="k", remaining=4, retry_after=0.0
        )
        store.record(result)
        assert store.total_count("k") == 1
        store.close()
