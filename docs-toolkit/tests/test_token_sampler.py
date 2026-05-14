"""Tests for the E93 token-bucket sampler module (docstoolkit.token_sampler).

Covers:
- TokenBucket      (bucket.py)
- SamplingDecision (sampler.py)
- TokenBucketSampler (sampler.py)
- AdaptiveSampler  (adaptive.py)
"""
from __future__ import annotations

import math
import threading
import time

import pytest

from docstoolkit.token_sampler import (
    AdaptiveSampler,
    SamplingDecision,
    TokenBucket,
    TokenBucketSampler,
)


# =========================================================================== #
#  TokenBucket – construction & invariants                                    #
# =========================================================================== #


class TestTokenBucketConstruction:
    def test_capacity_property(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        assert b.capacity == 10

    def test_refill_rate_property(self):
        b = TokenBucket(capacity=10, refill_rate=2.5)
        assert b.refill_rate == 2.5

    def test_starts_full(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        assert b.available() == pytest.approx(10.0)

    def test_starts_full_large_capacity(self):
        b = TokenBucket(capacity=10_000, refill_rate=1.0)
        assert b.available() == pytest.approx(10_000.0)

    def test_starts_full_unit_capacity(self):
        b = TokenBucket(capacity=1, refill_rate=1.0)
        assert b.available() == pytest.approx(1.0)

    def test_negative_capacity_raises(self):
        with pytest.raises(ValueError):
            TokenBucket(capacity=-1, refill_rate=1.0)

    def test_zero_capacity_raises(self):
        with pytest.raises(ValueError):
            TokenBucket(capacity=0, refill_rate=1.0)

    def test_negative_refill_rate_raises(self):
        with pytest.raises(ValueError):
            TokenBucket(capacity=5, refill_rate=-0.1)

    def test_zero_refill_rate_allowed(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        assert b.refill_rate == 0.0

    def test_repr_runs(self):
        b = TokenBucket(capacity=5, refill_rate=1.0)
        s = repr(b)
        assert "TokenBucket" in s


# =========================================================================== #
#  TokenBucket.consume                                                        #
# =========================================================================== #


class TestTokenBucketConsume:
    def test_consume_one_succeeds_when_full(self):
        b = TokenBucket(capacity=5, refill_rate=1.0)
        assert b.consume(1) is True

    def test_consume_decrements_tokens(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(1, now=0.0)
        assert b.available(now=0.0) == pytest.approx(4.0)

    def test_consume_multiple_decrements(self):
        b = TokenBucket(capacity=10, refill_rate=0.0)
        b.consume(3, now=0.0)
        assert b.available(now=0.0) == pytest.approx(7.0)

    def test_consume_full_capacity_then_empty(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        assert b.consume(5, now=0.0) is True
        assert b.available(now=0.0) == pytest.approx(0.0)

    def test_cannot_consume_more_than_available(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        assert b.consume(6, now=0.0) is False

    def test_failed_consume_does_not_decrement(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(6, now=0.0)  # fails
        assert b.available(now=0.0) == pytest.approx(5.0)

    def test_consume_until_empty(self):
        b = TokenBucket(capacity=3, refill_rate=0.0)
        assert b.consume(1, now=0.0) is True
        assert b.consume(1, now=0.0) is True
        assert b.consume(1, now=0.0) is True
        assert b.consume(1, now=0.0) is False

    def test_consume_zero_always_true(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        assert b.consume(0, now=0.0) is True

    def test_consume_zero_does_not_decrement(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(0, now=0.0)
        assert b.available(now=0.0) == pytest.approx(5.0)

    def test_consume_negative_raises(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        with pytest.raises(ValueError):
            b.consume(-1)

    def test_consume_default_amount_is_one(self):
        b = TokenBucket(capacity=3, refill_rate=0.0)
        b.consume(now=0.0)
        assert b.available(now=0.0) == pytest.approx(2.0)


# =========================================================================== #
#  TokenBucket.try_consume                                                    #
# =========================================================================== #


class TestTokenBucketTryConsume:
    def test_try_consume_returns_tuple(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        result = b.try_consume(1, now=0.0)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_try_consume_success(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        success, remaining = b.try_consume(1, now=0.0)
        assert success is True
        assert remaining == pytest.approx(4.0)

    def test_try_consume_failure(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        success, remaining = b.try_consume(10, now=0.0)
        assert success is False
        assert remaining == pytest.approx(5.0)  # unchanged

    def test_try_consume_exact_remaining(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        success, remaining = b.try_consume(5, now=0.0)
        assert success is True
        assert remaining == pytest.approx(0.0)

    def test_try_consume_one_over(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        success, remaining = b.try_consume(6, now=0.0)
        assert success is False
        assert remaining == pytest.approx(5.0)

    def test_try_consume_default_amount(self):
        b = TokenBucket(capacity=3, refill_rate=0.0)
        success, remaining = b.try_consume(now=0.0)
        assert success is True
        assert remaining == pytest.approx(2.0)

    def test_try_consume_negative_raises(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        with pytest.raises(ValueError):
            b.try_consume(-2)

    def test_try_consume_zero(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        success, remaining = b.try_consume(0, now=0.0)
        assert success is True
        assert remaining == pytest.approx(5.0)


# =========================================================================== #
#  TokenBucket.available / refill                                             #
# =========================================================================== #


class TestTokenBucketAvailable:
    def test_available_after_no_consume(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        assert b.available() == pytest.approx(10.0)

    def test_available_after_consume(self):
        b = TokenBucket(capacity=10, refill_rate=0.0)
        b.consume(4, now=0.0)
        assert b.available(now=0.0) == pytest.approx(6.0)

    def test_available_after_refill(self):
        b = TokenBucket(capacity=10, refill_rate=2.0)
        # Burn all tokens at t=0
        b.consume(10, now=0.0)
        assert b.available(now=0.0) == pytest.approx(0.0)
        # 1 second later -> 2 tokens
        assert b.available(now=1.0) == pytest.approx(2.0)

    def test_available_refill_partial_second(self):
        b = TokenBucket(capacity=10, refill_rate=4.0)
        b.consume(10, now=0.0)
        assert b.available(now=0.5) == pytest.approx(2.0)

    def test_refill_clamped_to_capacity(self):
        b = TokenBucket(capacity=5, refill_rate=100.0)
        b.consume(5, now=0.0)
        # 10 seconds * 100 tokens/s would be 1000 tokens, but capped at 5
        assert b.available(now=10.0) == pytest.approx(5.0)

    def test_refill_does_not_overflow_when_full(self):
        b = TokenBucket(capacity=5, refill_rate=1.0)
        # No consumption, just elapse time
        assert b.available(now=100.0) == pytest.approx(5.0)

    def test_zero_refill_does_not_add(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(3, now=0.0)
        assert b.available(now=10.0) == pytest.approx(2.0)

    def test_refill_accumulates_over_time(self):
        b = TokenBucket(capacity=100, refill_rate=10.0)
        b.consume(100, now=0.0)
        assert b.available(now=1.0) == pytest.approx(10.0)
        assert b.available(now=5.0) == pytest.approx(50.0)
        assert b.available(now=20.0) == pytest.approx(100.0)  # clamped

    def test_consume_then_refill_then_consume(self):
        b = TokenBucket(capacity=10, refill_rate=5.0)
        assert b.consume(10, now=0.0) is True
        assert b.consume(5, now=0.0) is False
        # After 1 sec we have 5 tokens
        assert b.consume(5, now=1.0) is True
        # Bucket should be empty now
        assert b.available(now=1.0) == pytest.approx(0.0)

    def test_refill_internal_no_negative_delta(self):
        # available() with a "now" before last_refill should not add negative tokens
        b = TokenBucket(capacity=10, refill_rate=1.0)
        b.consume(5, now=10.0)  # last_refill now 10.0
        # If we ask with an earlier time, no tokens are deducted
        val = b.available(now=5.0)
        assert val == pytest.approx(5.0)


# =========================================================================== #
#  TokenBucket.reset                                                          #
# =========================================================================== #


class TestTokenBucketReset:
    def test_reset_after_full_consume(self):
        b = TokenBucket(capacity=10, refill_rate=0.0)
        b.consume(10, now=0.0)
        assert b.available(now=0.0) == pytest.approx(0.0)
        b.reset()
        assert b.available() == pytest.approx(10.0)

    def test_reset_after_partial_consume(self):
        b = TokenBucket(capacity=10, refill_rate=0.0)
        b.consume(3, now=0.0)
        b.reset()
        assert b.available() == pytest.approx(10.0)

    def test_reset_when_already_full(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        b.reset()
        assert b.available() == pytest.approx(10.0)

    def test_reset_returns_none(self):
        b = TokenBucket(capacity=5, refill_rate=1.0)
        assert b.reset() is None

    def test_reset_then_consume(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(5, now=0.0)
        b.reset()
        assert b.consume(1) is True

    def test_reset_resets_refill_clock(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        b.consume(5, now=0.0)
        b.reset()
        # After reset we are full again
        assert b.available() == pytest.approx(10.0)


# =========================================================================== #
#  TokenBucket.time_until_available                                           #
# =========================================================================== #


class TestTokenBucketTimeUntil:
    def test_time_until_available_when_full(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        assert b.time_until_available(1) == pytest.approx(0.0)

    def test_time_until_available_zero_amount(self):
        b = TokenBucket(capacity=10, refill_rate=1.0)
        b.consume(10, now=0.0)
        assert b.time_until_available(0, now=0.0) == pytest.approx(0.0)

    def test_time_until_available_empty_bucket(self):
        b = TokenBucket(capacity=10, refill_rate=2.0)
        b.consume(10, now=0.0)
        # Need 1 token at 2 tokens/sec -> 0.5s
        assert b.time_until_available(1, now=0.0) == pytest.approx(0.5)

    def test_time_until_available_partial_bucket(self):
        b = TokenBucket(capacity=10, refill_rate=2.0)
        b.consume(9, now=0.0)  # 1 token left
        # need 5 -> short by 4 -> 4/2 = 2s
        assert b.time_until_available(5, now=0.0) == pytest.approx(2.0)

    def test_time_until_available_higher_than_capacity_zero_rate(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(5, now=0.0)
        assert math.isinf(b.time_until_available(10, now=0.0))

    def test_time_until_available_higher_than_capacity(self):
        b = TokenBucket(capacity=5, refill_rate=1.0)
        b.consume(5, now=0.0)
        # Cannot ever reach 10 (cap is 5) but module returns time to fill cap
        val = b.time_until_available(10, now=0.0)
        # 5 needed / 1 per sec = 5.0
        assert val == pytest.approx(5.0)

    def test_time_until_available_zero_rate_empty(self):
        b = TokenBucket(capacity=5, refill_rate=0.0)
        b.consume(5, now=0.0)
        assert math.isinf(b.time_until_available(1, now=0.0))

    def test_time_until_available_negative_raises(self):
        b = TokenBucket(capacity=5, refill_rate=1.0)
        with pytest.raises(ValueError):
            b.time_until_available(-1)

    def test_time_until_available_after_some_refill(self):
        b = TokenBucket(capacity=10, refill_rate=5.0)
        b.consume(10, now=0.0)
        # at t=1 we have 5 tokens
        assert b.time_until_available(5, now=1.0) == pytest.approx(0.0)
        # need 7 -> short by 2 -> 2/5 = 0.4
        assert b.time_until_available(7, now=1.0) == pytest.approx(0.4)


# =========================================================================== #
#  TokenBucket concurrency                                                    #
# =========================================================================== #


class TestTokenBucketConcurrency:
    def test_concurrent_consume_counts_correctly(self):
        b = TokenBucket(capacity=1000, refill_rate=0.0)
        success_counter = [0]
        counter_lock = threading.Lock()

        def worker():
            for _ in range(100):
                if b.consume(1):
                    with counter_lock:
                        success_counter[0] += 1

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Workers issue 20 * 100 = 2000 consume() calls but bucket only has 1000
        assert success_counter[0] == 1000

    def test_concurrent_consume_no_tokens_become_negative(self):
        b = TokenBucket(capacity=50, refill_rate=0.0)

        def worker():
            for _ in range(20):
                b.consume(1)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert b.available() >= 0.0

    def test_concurrent_mixed_operations(self):
        b = TokenBucket(capacity=100, refill_rate=10.0)

        def consume_worker():
            for _ in range(50):
                b.consume(1)

        def available_worker():
            for _ in range(50):
                b.available()

        def reset_worker():
            for _ in range(5):
                b.reset()

        threads = (
            [threading.Thread(target=consume_worker) for _ in range(4)]
            + [threading.Thread(target=available_worker) for _ in range(4)]
            + [threading.Thread(target=reset_worker) for _ in range(2)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Nothing crashed, bucket invariants hold
        assert 0.0 <= b.available() <= 100.0


# =========================================================================== #
#  SamplingDecision enum                                                      #
# =========================================================================== #


class TestSamplingDecision:
    def test_keep_exists(self):
        assert SamplingDecision.KEEP is not None

    def test_drop_exists(self):
        assert SamplingDecision.DROP is not None

    def test_keep_and_drop_are_distinct(self):
        assert SamplingDecision.KEEP is not SamplingDecision.DROP

    def test_enum_membership(self):
        members = list(SamplingDecision)
        assert SamplingDecision.KEEP in members
        assert SamplingDecision.DROP in members

    def test_enum_two_members(self):
        assert len(list(SamplingDecision)) == 2

    def test_enum_value_keep(self):
        assert SamplingDecision.KEEP.value == "keep"

    def test_enum_value_drop(self):
        assert SamplingDecision.DROP.value == "drop"

    def test_enum_lookup_by_name(self):
        assert SamplingDecision["KEEP"] is SamplingDecision.KEEP
        assert SamplingDecision["DROP"] is SamplingDecision.DROP


# =========================================================================== #
#  TokenBucketSampler                                                         #
# =========================================================================== #


class TestTokenBucketSamplerConstruction:
    def test_rate_property(self):
        s = TokenBucketSampler(rate_per_sec=5.0)
        assert s.rate_per_sec == 5.0

    def test_default_burst_uses_rate(self):
        s = TokenBucketSampler(rate_per_sec=7.0)
        assert s.burst == 7

    def test_default_burst_min_one(self):
        s = TokenBucketSampler(rate_per_sec=0.0)
        assert s.burst == 1

    def test_default_burst_fractional_rate(self):
        s = TokenBucketSampler(rate_per_sec=0.5)
        # int(0.5) == 0, so we take max(1, 0) -> 1
        assert s.burst == 1

    def test_custom_burst(self):
        s = TokenBucketSampler(rate_per_sec=5.0, burst=20)
        assert s.burst == 20

    def test_burst_zero_raises(self):
        with pytest.raises(ValueError):
            TokenBucketSampler(rate_per_sec=5.0, burst=0)

    def test_negative_rate_raises(self):
        with pytest.raises(ValueError):
            TokenBucketSampler(rate_per_sec=-1.0)

    def test_bucket_property(self):
        s = TokenBucketSampler(rate_per_sec=5.0)
        assert isinstance(s.bucket, TokenBucket)


class TestTokenBucketSamplerShouldSample:
    def test_keep_when_token_available(self):
        s = TokenBucketSampler(rate_per_sec=1.0, burst=5)
        assert s.should_sample() is SamplingDecision.KEEP

    def test_keep_burst_size_times(self):
        s = TokenBucketSampler(rate_per_sec=1.0, burst=5)
        for _ in range(5):
            assert s.should_sample(now=0.0) is SamplingDecision.KEEP

    def test_drop_when_bucket_empty(self):
        s = TokenBucketSampler(rate_per_sec=1.0, burst=3)
        for _ in range(3):
            s.should_sample(now=0.0)
        assert s.should_sample(now=0.0) is SamplingDecision.DROP

    def test_keep_after_refill_time(self):
        s = TokenBucketSampler(rate_per_sec=10.0, burst=5)
        for _ in range(5):
            s.should_sample(now=0.0)
        # bucket empty -> drop
        assert s.should_sample(now=0.0) is SamplingDecision.DROP
        # after 1s -> 10 new tokens (capped at 5), so KEEP
        assert s.should_sample(now=1.0) is SamplingDecision.KEEP

    def test_keep_then_drop_pattern(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=2)
        assert s.should_sample(now=0.0) is SamplingDecision.KEEP
        assert s.should_sample(now=0.0) is SamplingDecision.KEEP
        assert s.should_sample(now=0.0) is SamplingDecision.DROP
        assert s.should_sample(now=0.0) is SamplingDecision.DROP

    def test_returns_sampling_decision_type(self):
        s = TokenBucketSampler(rate_per_sec=1.0, burst=2)
        d = s.should_sample()
        assert isinstance(d, SamplingDecision)

    def test_rate_zero_no_refill(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=3)
        # We can use up the bucket
        for _ in range(3):
            assert s.should_sample(now=0.0) is SamplingDecision.KEEP
        # Then we never get any back
        for t in (1.0, 100.0, 1_000_000.0):
            assert s.should_sample(now=t) is SamplingDecision.DROP


class TestTokenBucketSamplerSample:
    def test_sample_returns_subset(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=3)
        out = s.sample(range(10))
        assert len(out) == 3

    def test_sample_keeps_first_items(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=4)
        items = ["a", "b", "c", "d", "e", "f"]
        out = s.sample(items)
        assert out == ["a", "b", "c", "d"]

    def test_sample_empty_iterable(self):
        s = TokenBucketSampler(rate_per_sec=1.0, burst=5)
        out = s.sample([])
        assert out == []

    def test_sample_returns_list(self):
        s = TokenBucketSampler(rate_per_sec=1.0, burst=3)
        out = s.sample(range(5))
        assert isinstance(out, list)

    def test_sample_with_large_burst(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=100)
        out = s.sample(range(50))
        assert len(out) == 50

    def test_sample_keeps_all_when_under_burst(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=10)
        items = [1, 2, 3]
        assert s.sample(items) == [1, 2, 3]

    def test_sample_works_with_generators(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=3)
        gen = (i for i in range(10))
        out = s.sample(gen)
        assert len(out) == 3


class TestTokenBucketSamplerStats:
    def test_stats_initial(self):
        s = TokenBucketSampler(rate_per_sec=5.0, burst=10)
        st = s.stats()
        assert st["kept"] == 0
        assert st["dropped"] == 0
        assert st["rate"] == 5.0

    def test_stats_kept_count(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=5)
        for _ in range(3):
            s.should_sample(now=0.0)
        st = s.stats()
        assert st["kept"] == 3
        assert st["dropped"] == 0

    def test_stats_dropped_count(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=2)
        for _ in range(5):
            s.should_sample(now=0.0)
        st = s.stats()
        assert st["kept"] == 2
        assert st["dropped"] == 3

    def test_stats_after_sample_call(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=3)
        s.sample(range(10))
        st = s.stats()
        assert st["kept"] == 3
        assert st["dropped"] == 7

    def test_stats_rate_reflects_init(self):
        s = TokenBucketSampler(rate_per_sec=42.0, burst=10)
        assert s.stats()["rate"] == 42.0

    def test_stats_dict_has_three_keys(self):
        s = TokenBucketSampler(rate_per_sec=1.0)
        st = s.stats()
        assert set(st.keys()) == {"kept", "dropped", "rate"}


class TestTokenBucketSamplerResetStats:
    def test_reset_stats_zeros_counters(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=2)
        for _ in range(5):
            s.should_sample(now=0.0)
        s.reset_stats()
        st = s.stats()
        assert st["kept"] == 0
        assert st["dropped"] == 0

    def test_reset_stats_keeps_rate(self):
        s = TokenBucketSampler(rate_per_sec=12.5, burst=4)
        for _ in range(10):
            s.should_sample(now=0.0)
        s.reset_stats()
        assert s.stats()["rate"] == 12.5

    def test_reset_stats_returns_none(self):
        s = TokenBucketSampler(rate_per_sec=1.0)
        assert s.reset_stats() is None

    def test_reset_stats_does_not_refill_bucket(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=3)
        for _ in range(3):
            s.should_sample(now=0.0)
        s.reset_stats()
        # bucket is still empty -> drops
        assert s.should_sample(now=0.0) is SamplingDecision.DROP

    def test_stats_independent_after_reset(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=4)
        for _ in range(10):
            s.should_sample(now=0.0)
        s.reset_stats()
        # Even though bucket is empty, kept/dropped are now zero
        for _ in range(2):
            s.should_sample(now=0.0)
        st = s.stats()
        assert st["kept"] == 0
        assert st["dropped"] == 2


# =========================================================================== #
#  AdaptiveSampler                                                            #
# =========================================================================== #


class TestAdaptiveSamplerConstruction:
    def test_default_min_rate(self):
        a = AdaptiveSampler(initial_rate=10.0)
        assert a.min_rate == 0.1

    def test_default_max_rate(self):
        a = AdaptiveSampler(initial_rate=10.0)
        assert a.max_rate == 1000.0

    def test_default_adjustment_factor(self):
        a = AdaptiveSampler(initial_rate=10.0)
        assert a.adjustment_factor == 1.2

    def test_current_rate_initial(self):
        a = AdaptiveSampler(initial_rate=10.0)
        assert a.current_rate() == 10.0

    def test_current_rate_clamped_to_max(self):
        a = AdaptiveSampler(initial_rate=10_000.0, max_rate=100.0)
        assert a.current_rate() == 100.0

    def test_current_rate_clamped_to_min(self):
        a = AdaptiveSampler(initial_rate=0.01, min_rate=1.0)
        assert a.current_rate() == 1.0

    def test_invalid_initial_rate(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=0)

    def test_invalid_initial_rate_negative(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=-1)

    def test_invalid_min_rate(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=1.0, min_rate=0.0)

    def test_invalid_max_rate(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=1.0, max_rate=0.0)

    def test_invalid_min_gt_max(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=1.0, min_rate=10.0, max_rate=5.0)

    def test_invalid_adjustment_factor_one(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=1.0, adjustment_factor=1.0)

    def test_invalid_adjustment_factor_below_one(self):
        with pytest.raises(ValueError):
            AdaptiveSampler(initial_rate=1.0, adjustment_factor=0.5)

    def test_sampler_property(self):
        a = AdaptiveSampler(initial_rate=10.0)
        assert isinstance(a.sampler, TokenBucketSampler)


class TestAdaptiveSamplerFeedback:
    def test_feedback_load_high_shrinks(self):
        a = AdaptiveSampler(initial_rate=100.0, adjustment_factor=2.0)
        a.feedback(load_high=True)
        assert a.current_rate() == 50.0

    def test_feedback_load_low_grows(self):
        a = AdaptiveSampler(initial_rate=50.0, adjustment_factor=2.0)
        a.feedback(load_high=False)
        assert a.current_rate() == 100.0

    def test_feedback_high_clamps_to_min(self):
        a = AdaptiveSampler(
            initial_rate=1.0, min_rate=0.5, max_rate=100.0, adjustment_factor=10.0
        )
        a.feedback(load_high=True)
        # 1.0 / 10 = 0.1, but clamped to 0.5
        assert a.current_rate() == 0.5

    def test_feedback_low_clamps_to_max(self):
        a = AdaptiveSampler(
            initial_rate=100.0, min_rate=0.1, max_rate=200.0, adjustment_factor=10.0
        )
        a.feedback(load_high=False)
        # 100 * 10 = 1000, clamped to 200
        assert a.current_rate() == 200.0

    def test_feedback_repeated_high(self):
        a = AdaptiveSampler(
            initial_rate=64.0,
            min_rate=0.1,
            max_rate=100.0,
            adjustment_factor=2.0,
        )
        a.feedback(load_high=True)
        a.feedback(load_high=True)
        a.feedback(load_high=True)
        assert a.current_rate() == 8.0

    def test_feedback_repeated_low(self):
        a = AdaptiveSampler(
            initial_rate=1.0,
            min_rate=0.1,
            max_rate=100.0,
            adjustment_factor=2.0,
        )
        a.feedback(load_high=False)
        a.feedback(load_high=False)
        a.feedback(load_high=False)
        assert a.current_rate() == 8.0

    def test_feedback_mixed_signals(self):
        a = AdaptiveSampler(
            initial_rate=10.0,
            min_rate=0.1,
            max_rate=100.0,
            adjustment_factor=2.0,
        )
        a.feedback(load_high=True)   # 5
        a.feedback(load_high=False)  # 10
        a.feedback(load_high=False)  # 20
        a.feedback(load_high=True)   # 10
        assert a.current_rate() == 10.0

    def test_feedback_returns_none(self):
        a = AdaptiveSampler(initial_rate=10.0)
        assert a.feedback(load_high=True) is None

    def test_feedback_no_change_when_clamped_at_min(self):
        a = AdaptiveSampler(
            initial_rate=1.0,
            min_rate=1.0,
            max_rate=1000.0,
            adjustment_factor=2.0,
        )
        a.feedback(load_high=True)
        assert a.current_rate() == 1.0

    def test_feedback_no_change_when_clamped_at_max(self):
        a = AdaptiveSampler(
            initial_rate=10.0,
            min_rate=0.1,
            max_rate=10.0,
            adjustment_factor=2.0,
        )
        a.feedback(load_high=False)
        assert a.current_rate() == 10.0


class TestAdaptiveSamplerShouldSample:
    def test_should_sample_returns_sampling_decision(self):
        a = AdaptiveSampler(initial_rate=10.0)
        d = a.should_sample()
        assert isinstance(d, SamplingDecision)

    def test_should_sample_keep_initially(self):
        a = AdaptiveSampler(initial_rate=10.0)
        d = a.should_sample()
        # Initial bucket is full -> KEEP
        assert d is SamplingDecision.KEEP

    def test_should_sample_drop_when_exhausted(self):
        a = AdaptiveSampler(initial_rate=5.0, min_rate=0.1, max_rate=100.0)
        # Burst defaults to int(rate_per_sec) = 5
        for _ in range(5):
            a.should_sample(now=0.0)
        d = a.should_sample(now=0.0)
        assert d is SamplingDecision.DROP

    def test_should_sample_after_feedback(self):
        a = AdaptiveSampler(initial_rate=10.0, adjustment_factor=2.0)
        a.feedback(load_high=True)
        # Internal sampler now has rate 5.0; calling should_sample shouldn't crash.
        a.should_sample()

    def test_should_sample_pattern_zero_rate(self):
        # min_rate forces lowest possible rate
        a = AdaptiveSampler(
            initial_rate=1.0,
            min_rate=1.0,
            max_rate=10.0,
            adjustment_factor=2.0,
        )
        # Bucket capacity == 1, refill at 1/s
        assert a.should_sample(now=0.0) is SamplingDecision.KEEP
        assert a.should_sample(now=0.0) is SamplingDecision.DROP

    def test_stats_proxy(self):
        a = AdaptiveSampler(initial_rate=10.0)
        st = a.stats()
        assert "kept" in st
        assert "dropped" in st
        assert "rate" in st

    def test_stats_rate_matches_current_rate(self):
        a = AdaptiveSampler(initial_rate=10.0, adjustment_factor=2.0)
        a.feedback(load_high=True)
        assert a.stats()["rate"] == a.current_rate()


class TestAdaptiveSamplerCarryOverStats:
    def test_stats_preserved_across_feedback(self):
        a = AdaptiveSampler(initial_rate=10.0, adjustment_factor=2.0)
        for _ in range(3):
            a.should_sample(now=0.0)
        kept_before = a.stats()["kept"]
        a.feedback(load_high=True)
        # Stats should carry over – no reset on rebuild
        assert a.stats()["kept"] == kept_before


# =========================================================================== #
#  Cross-cutting behavior                                                     #
# =========================================================================== #


class TestSamplerRealClock:
    def test_default_now_uses_current_time(self):
        s = TokenBucketSampler(rate_per_sec=1000.0, burst=2)
        # With real clock, two quick calls -> both keep
        assert s.should_sample() is SamplingDecision.KEEP
        assert s.should_sample() is SamplingDecision.KEEP

    def test_bucket_default_now(self):
        b = TokenBucket(capacity=5, refill_rate=1000.0)
        # Without explicit now=, real time is used – the bucket starts full.
        assert b.consume(5) is True

    def test_consume_after_real_sleep(self):
        b = TokenBucket(capacity=2, refill_rate=10.0)
        b.consume(2)
        time.sleep(0.25)  # small sleep, 2.5 tokens regenerate
        assert b.consume(1) is True


class TestSamplerEndToEnd:
    def test_full_workflow(self):
        s = TokenBucketSampler(rate_per_sec=0.0, burst=5)
        kept = s.sample(range(100))
        st = s.stats()
        assert len(kept) == 5
        assert st["kept"] == 5
        assert st["dropped"] == 95
        s.reset_stats()
        assert s.stats() == {"kept": 0, "dropped": 0, "rate": 0.0}

    def test_adaptive_workflow(self):
        a = AdaptiveSampler(
            initial_rate=10.0,
            min_rate=1.0,
            max_rate=100.0,
            adjustment_factor=2.0,
        )
        # Simulate a load spike
        for _ in range(5):
            a.feedback(load_high=True)
        # Rate should be near min
        assert a.current_rate() == pytest.approx(1.0)
        # Simulate recovery
        for _ in range(10):
            a.feedback(load_high=False)
        assert a.current_rate() == pytest.approx(100.0)
