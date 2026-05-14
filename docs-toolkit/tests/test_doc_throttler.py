"""Tests for docstoolkit.doc_throttler."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_throttler import (
    Bucket,
    DocThrottler,
    ThrottleConfig,
    ThrottleResult,
)


# ---------------------------------------------------------------- dataclasses


class TestThrottleConfig:
    def test_defaults(self):
        cfg = ThrottleConfig()
        assert cfg.burst_capacity == 10
        assert cfg.refill_rate == 1.0
        assert cfg.enabled is True

    def test_custom(self):
        cfg = ThrottleConfig(burst_capacity=5, refill_rate=2.5, enabled=False)
        assert cfg.burst_capacity == 5
        assert cfg.refill_rate == 2.5
        assert cfg.enabled is False

    def test_is_dataclass(self):
        cfg1 = ThrottleConfig(burst_capacity=3, refill_rate=0.5)
        cfg2 = ThrottleConfig(burst_capacity=3, refill_rate=0.5)
        assert cfg1 == cfg2


class TestBucket:
    def test_create_with_defaults(self):
        b = Bucket(
            doc_id="d1",
            tokens=10.0,
            last_refill=0.0,
            burst_capacity=10,
            refill_rate=1.0,
        )
        assert b.doc_id == "d1"
        assert b.tokens == 10.0
        assert b.total_requests == 0
        assert b.total_denied == 0
        assert b.enabled is True

    def test_with_counters(self):
        b = Bucket(
            doc_id="d1",
            tokens=3.0,
            last_refill=1.0,
            burst_capacity=5,
            refill_rate=2.0,
            total_requests=4,
            total_denied=1,
        )
        assert b.total_requests == 4
        assert b.total_denied == 1


class TestThrottleResult:
    def test_allowed(self):
        r = ThrottleResult(
            allowed=True, doc_id="d", tokens_remaining=4.0, retry_after_seconds=0.0
        )
        assert r.allowed is True
        assert r.doc_id == "d"
        assert r.tokens_remaining == 4.0
        assert r.retry_after_seconds == 0.0

    def test_denied(self):
        r = ThrottleResult(
            allowed=False, doc_id="x", tokens_remaining=0.0, retry_after_seconds=1.5
        )
        assert r.allowed is False
        assert r.retry_after_seconds == 1.5


# ----------------------------------------------------------------- basic acquire


class TestAcquireBasic:
    def test_auto_create_bucket(self):
        t = DocThrottler()
        r = t.acquire("doc1", now=0.0)
        assert r.allowed is True
        assert r.doc_id == "doc1"
        assert r.tokens_remaining == 9.0

    def test_default_consumes_one_token(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        bucket = t.peek("d", now=0.0)
        assert bucket is not None
        assert bucket.tokens == 9.0

    def test_acquire_zero_tokens(self):
        t = DocThrottler()
        r = t.acquire("d", tokens=0, now=0.0)
        assert r.allowed is True
        assert r.tokens_remaining == 10.0

    def test_acquire_multiple_tokens(self):
        t = DocThrottler()
        r = t.acquire("d", tokens=3, now=0.0)
        assert r.allowed is True
        assert r.tokens_remaining == 7.0

    def test_negative_tokens_raises(self):
        t = DocThrottler()
        with pytest.raises(ValueError):
            t.acquire("d", tokens=-1, now=0.0)

    def test_separate_buckets_per_doc(self):
        t = DocThrottler()
        t.acquire("a", tokens=5, now=0.0)
        t.acquire("b", tokens=2, now=0.0)
        assert t.peek("a", now=0.0).tokens == 5.0
        assert t.peek("b", now=0.0).tokens == 8.0

    def test_uses_default_config(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=3, refill_rate=0.5))
        r = t.acquire("x", now=0.0)
        assert r.tokens_remaining == 2.0

    def test_returns_doc_id_in_result(self):
        t = DocThrottler()
        r = t.acquire("the-doc", now=0.0)
        assert r.doc_id == "the-doc"


# ------------------------------------------------------------------- denials


class TestAcquireDenied:
    def test_denied_when_exhausted(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=0.0))
        assert t.acquire("d", now=0.0).allowed is True
        assert t.acquire("d", now=0.0).allowed is True
        r = t.acquire("d", now=0.0)
        assert r.allowed is False
        assert r.tokens_remaining == 0.0

    def test_denied_retry_after(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=1.0))
        t.acquire("d", tokens=2, now=0.0)
        r = t.acquire("d", tokens=1, now=0.0)
        assert r.allowed is False
        assert r.retry_after_seconds == pytest.approx(1.0)

    def test_request_larger_than_capacity(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=3, refill_rate=1.0))
        r = t.acquire("d", tokens=10, now=0.0)
        assert r.allowed is False
        assert r.retry_after_seconds > 0

    def test_request_larger_than_capacity_no_refill_inf(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=3, refill_rate=0.0))
        r = t.acquire("d", tokens=10, now=0.0)
        assert r.allowed is False
        assert r.retry_after_seconds == float("inf")

    def test_partial_denial_retry_time(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=2.0))
        t.acquire("d", tokens=10, now=0.0)
        r = t.acquire("d", tokens=4, now=0.0)
        assert r.allowed is False
        # need 4 tokens at 2/s = 2s
        assert r.retry_after_seconds == pytest.approx(2.0)

    def test_denied_bumps_total_denied(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        assert t.total_denied == 2


# -------------------------------------------------------------------- refill


class TestRefill:
    def test_refill_over_time(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=2.0))
        t.acquire("d", tokens=10, now=0.0)
        r = t.acquire("d", tokens=1, now=1.0)
        # after 1s we have 2 tokens, consume 1 -> 1 left
        assert r.allowed is True
        assert r.tokens_remaining == pytest.approx(1.0)

    def test_refill_caps_at_burst_capacity(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=5, refill_rate=10.0))
        t.acquire("d", tokens=5, now=0.0)
        # 100s pass — should cap at 5
        b = t.peek("d", now=100.0)
        assert b.tokens == 5.0

    def test_refill_zero_rate_no_recovery(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=0.0))
        t.acquire("d", tokens=2, now=0.0)
        b = t.peek("d", now=1000.0)
        assert b.tokens == 0.0

    def test_refill_clock_backwards_no_effect(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=5, refill_rate=1.0))
        t.acquire("d", tokens=5, now=10.0)
        b = t.peek("d", now=5.0)
        # clock went backward, no negative refill
        assert b.tokens == 0.0

    def test_refill_partial(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=1.0))
        t.acquire("d", tokens=8, now=0.0)
        b = t.peek("d", now=3.0)
        assert b.tokens == pytest.approx(5.0)


# --------------------------------------------------------------------- peek


class TestPeek:
    def test_peek_unknown_returns_none(self):
        t = DocThrottler()
        assert t.peek("missing", now=0.0) is None

    def test_peek_does_not_mutate(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=1.0))
        t.acquire("d", tokens=5, now=0.0)
        t.peek("d", now=10.0)
        t.peek("d", now=20.0)
        # peek with refill view doesn't deduct tokens
        r = t.acquire("d", tokens=1, now=20.0)
        assert r.allowed is True

    def test_peek_reflects_refill(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=1.0))
        t.acquire("d", tokens=8, now=0.0)
        b = t.peek("d", now=4.0)
        assert b.tokens == pytest.approx(6.0)

    def test_peek_includes_counters(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        b = t.peek("d", now=0.0)
        assert b.total_requests == 2
        assert b.total_denied == 1


# ----------------------------------------------------------------- wait_time


class TestWaitTime:
    def test_wait_zero_when_enough(self):
        t = DocThrottler()
        assert t.wait_time("d", 1, now=0.0) == 0.0

    def test_wait_when_empty(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=1.0))
        t.acquire("d", tokens=2, now=0.0)
        assert t.wait_time("d", 1, now=0.0) == pytest.approx(1.0)

    def test_wait_infinity_when_no_refill(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=0.0))
        t.acquire("d", tokens=2, now=0.0)
        assert t.wait_time("d", 1, now=0.0) == float("inf")

    def test_wait_negative_tokens_raises(self):
        t = DocThrottler()
        with pytest.raises(ValueError):
            t.wait_time("d", -1, now=0.0)

    def test_wait_creates_bucket(self):
        t = DocThrottler()
        assert t.wait_time("new", 1, now=0.0) == 0.0
        # bucket should now exist
        assert "new" in t.all_doc_ids()


# ----------------------------------------------------------------- configure


class TestConfigure:
    def test_configure_existing(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        ok = t.configure("d", burst_capacity=20, refill_rate=2.0)
        assert ok is True
        b = t.peek("d", now=0.0)
        assert b.burst_capacity == 20
        assert b.refill_rate == 2.0

    def test_configure_creates_bucket_if_missing(self):
        t = DocThrottler()
        ok = t.configure("new", burst_capacity=5)
        assert ok is True
        assert "new" in t.all_doc_ids()

    def test_configure_clamps_tokens_when_reduced(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=20, refill_rate=1.0))
        t.acquire("d", tokens=2, now=0.0)  # tokens = 18
        t.configure("d", burst_capacity=5)
        b = t.peek("d", now=0.0)
        assert b.tokens == 5.0

    def test_configure_only_refill_rate(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        t.configure("d", refill_rate=5.0)
        b = t.peek("d", now=0.0)
        assert b.refill_rate == 5.0
        assert b.burst_capacity == 10

    def test_configure_no_change_returns_false(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        assert t.configure("d") is False

    def test_configure_negative_capacity_raises(self):
        t = DocThrottler()
        with pytest.raises(ValueError):
            t.configure("d", burst_capacity=-1)

    def test_configure_negative_rate_raises(self):
        t = DocThrottler()
        with pytest.raises(ValueError):
            t.configure("d", refill_rate=-1.0)


# --------------------------------------------------------------------- reset


class TestReset:
    def test_reset_existing(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=5, refill_rate=0.0))
        t.acquire("d", tokens=5, now=0.0)
        assert t.reset("d") is True
        b = t.peek("d", now=0.0)
        assert b.tokens == 5.0

    def test_reset_missing(self):
        t = DocThrottler()
        assert t.reset("missing") is False

    def test_reset_keeps_counters(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)  # denied
        t.reset("d")
        b = t.peek("d", now=0.0)
        # reset restores tokens but counters remain
        assert b.tokens == 1.0
        assert b.total_requests == 2
        assert b.total_denied == 1


# ----------------------------------------------------------------- reset_all


class TestResetAll:
    def test_reset_all_empty(self):
        t = DocThrottler()
        assert t.reset_all() == 0

    def test_reset_all_multiple(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=3, refill_rate=0.0))
        t.acquire("a", tokens=3, now=0.0)
        t.acquire("b", tokens=2, now=0.0)
        t.acquire("c", tokens=1, now=0.0)
        n = t.reset_all()
        assert n == 3
        for d in ("a", "b", "c"):
            assert t.peek(d, now=0.0).tokens == 3.0


# --------------------------------------------------------------- disable/enable


class TestDisableThrottling:
    def test_disable_existing(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        was = t.disable_throttling("d")
        assert was is True  # was previously enabled

    def test_disable_already_disabled(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        t.disable_throttling("d")
        assert t.disable_throttling("d") is False

    def test_disable_allows_unlimited(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.disable_throttling("d")
        for _ in range(5):
            assert t.acquire("d", now=0.0).allowed is True

    def test_disable_creates_bucket(self):
        t = DocThrottler()
        t.disable_throttling("new")
        assert "new" in t.all_doc_ids()


class TestEnableThrottling:
    def test_enable_after_disable(self):
        t = DocThrottler()
        t.disable_throttling("d")
        was_disabled = t.enable_throttling("d")
        assert was_disabled is True

    def test_enable_already_enabled(self):
        t = DocThrottler()
        t.acquire("d", now=0.0)
        assert t.enable_throttling("d") is False

    def test_enable_restores_throttle(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.disable_throttling("d")
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        t.enable_throttling("d")
        # bucket still has full tokens since they weren't deducted
        b = t.peek("d", now=0.0)
        assert b.tokens == 1.0

    def test_enable_creates_bucket(self):
        t = DocThrottler()
        t.enable_throttling("nx")
        assert "nx" in t.all_doc_ids()


# ----------------------------------------------------------------- is_throttled


class TestIsThrottled:
    def test_unknown_doc_not_throttled(self):
        t = DocThrottler()
        assert t.is_throttled("nope") is False

    def test_full_bucket_not_throttled(self):
        t = DocThrottler()
        t.acquire("d", tokens=0, now=0.0)
        assert t.is_throttled("d") is False

    def test_exhausted_is_throttled(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=0.0))
        t.acquire("d", tokens=2, now=0.0)
        assert t.is_throttled("d") is True

    def test_disabled_not_throttled(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.acquire("d", now=0.0)
        t.disable_throttling("d")
        assert t.is_throttled("d") is False


# ----------------------------------------------------------------- set_default


class TestSetDefault:
    def test_update_burst(self):
        t = DocThrottler()
        cfg = t.set_default(burst_capacity=50)
        assert cfg.burst_capacity == 50

    def test_update_rate(self):
        t = DocThrottler()
        cfg = t.set_default(refill_rate=4.2)
        assert cfg.refill_rate == 4.2

    def test_update_applies_to_new_buckets(self):
        t = DocThrottler()
        t.set_default(burst_capacity=42, refill_rate=2.0)
        t.acquire("new", now=0.0)
        b = t.peek("new", now=0.0)
        assert b.burst_capacity == 42
        assert b.refill_rate == 2.0

    def test_update_does_not_affect_existing(self):
        t = DocThrottler()
        t.acquire("old", now=0.0)
        t.set_default(burst_capacity=999)
        b = t.peek("old", now=0.0)
        assert b.burst_capacity == 10

    def test_negative_raises(self):
        t = DocThrottler()
        with pytest.raises(ValueError):
            t.set_default(burst_capacity=-1)
        with pytest.raises(ValueError):
            t.set_default(refill_rate=-1.0)


# ----------------------------------------------------------------- all_doc_ids


class TestAllDocIds:
    def test_empty(self):
        t = DocThrottler()
        assert t.all_doc_ids() == []

    def test_sorted(self):
        t = DocThrottler()
        t.acquire("z", now=0.0)
        t.acquire("a", now=0.0)
        t.acquire("m", now=0.0)
        assert t.all_doc_ids() == ["a", "m", "z"]


# ----------------------------------------------------------------- total_requests


class TestTotalRequests:
    def test_initial_zero(self):
        t = DocThrottler()
        assert t.total_requests == 0

    def test_increments(self):
        t = DocThrottler()
        t.acquire("a", now=0.0)
        t.acquire("b", now=0.0)
        t.acquire("a", now=0.0)
        assert t.total_requests == 3

    def test_includes_denied(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)  # denied
        assert t.total_requests == 2


# ----------------------------------------------------------------- total_denied


class TestTotalDenied:
    def test_initial_zero(self):
        t = DocThrottler()
        assert t.total_denied == 0

    def test_increments_only_on_denial(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=2, refill_rate=0.0))
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        t.acquire("d", now=0.0)
        assert t.total_denied == 2

    def test_disabled_not_counted_as_denied(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.disable_throttling("d")
        for _ in range(10):
            t.acquire("d", now=0.0)
        assert t.total_denied == 0


# ----------------------------------------------------------------- most_throttled


class TestMostThrottled:
    def test_empty(self):
        t = DocThrottler()
        assert t.most_throttled() == []

    def test_ranking(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        # a: 2 denials, b: 3 denials, c: 1 denial
        t.acquire("a", now=0.0)
        t.acquire("a", now=0.0)
        t.acquire("a", now=0.0)
        t.acquire("b", now=0.0)
        t.acquire("b", now=0.0)
        t.acquire("b", now=0.0)
        t.acquire("b", now=0.0)
        t.acquire("c", now=0.0)
        t.acquire("c", now=0.0)
        result = t.most_throttled()
        assert result[0] == ("b", 3)
        assert result[1] == ("a", 2)
        assert result[2] == ("c", 1)

    def test_top_k_limit(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        for d in ("a", "b", "c"):
            t.acquire(d, now=0.0)
            t.acquire(d, now=0.0)
        assert len(t.most_throttled(top_k=2)) == 2

    def test_excludes_zero_denials(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=0.0))
        t.acquire("clean", now=0.0)
        assert t.most_throttled() == []

    def test_negative_top_k_raises(self):
        t = DocThrottler()
        with pytest.raises(ValueError):
            t.most_throttled(top_k=-1)


# --------------------------------------------------------------------- clear


class TestClear:
    def test_clear_empty(self):
        t = DocThrottler()
        t.clear()
        assert t.all_doc_ids() == []

    def test_clear_removes_buckets(self):
        t = DocThrottler()
        t.acquire("a", now=0.0)
        t.acquire("b", now=0.0)
        t.clear()
        assert t.all_doc_ids() == []
        assert t.peek("a", now=0.0) is None

    def test_clear_resets_counters(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1, refill_rate=0.0))
        t.acquire("a", now=0.0)
        t.acquire("a", now=0.0)
        t.clear()
        assert t.total_requests == 0
        assert t.total_denied == 0


# ----------------------------------------------------------------- edge cases


class TestEdgeCases:
    def test_concurrent_acquires(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=1000, refill_rate=0.0))
        results = []

        def worker():
            for _ in range(50):
                results.append(t.acquire("shared", now=0.0).allowed)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        allowed = sum(1 for r in results if r)
        assert allowed == 500
        assert t.total_requests == 500
        assert t.total_denied == 0

    def test_concurrent_partial_denials(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=20, refill_rate=0.0))
        results = []

        def worker():
            for _ in range(10):
                results.append(t.acquire("shared", now=0.0).allowed)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        allowed = sum(1 for r in results if r)
        assert allowed == 20
        assert t.total_requests == 50
        assert t.total_denied == 30

    def test_now_default_uses_time(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=10, refill_rate=1.0))
        r = t.acquire("d")  # now=None
        assert r.allowed is True

    def test_zero_capacity_always_denies(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=0, refill_rate=0.0))
        r = t.acquire("d", tokens=1, now=0.0)
        assert r.allowed is False

    def test_zero_tokens_always_allowed(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=0, refill_rate=0.0))
        r = t.acquire("d", tokens=0, now=0.0)
        assert r.allowed is True

    def test_high_refill_rate(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=100, refill_rate=1000.0))
        t.acquire("d", tokens=100, now=0.0)
        r = t.acquire("d", tokens=50, now=0.1)
        assert r.allowed is True

    def test_clear_then_use(self):
        t = DocThrottler()
        t.acquire("a", now=0.0)
        t.clear()
        r = t.acquire("a", now=0.0)
        assert r.allowed is True
        assert r.tokens_remaining == 9.0

    def test_total_requests_thread_safe(self):
        t = DocThrottler(ThrottleConfig(burst_capacity=100000, refill_rate=0.0))

        def worker():
            for _ in range(100):
                t.acquire("k", now=0.0)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        assert t.total_requests == 1000
