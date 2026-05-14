"""Tests for E335 DocTokenBucket."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_token_bucket import BucketState, BucketStats, DocTokenBucket


class TestBucketStateDataclass:
    def test_construct_basic(self):
        s = BucketState(key="k", tokens=5.0, capacity=10.0, refill_rate=1.0)
        assert s.key == "k"
        assert s.tokens == 5.0
        assert s.capacity == 10.0
        assert s.refill_rate == 1.0
        assert s.last_refill_at == 0.0

    def test_construct_with_timestamp(self):
        s = BucketState(key="k", tokens=1.0, capacity=2.0, refill_rate=0.5, last_refill_at=100.0)
        assert s.last_refill_at == 100.0

    def test_mutable(self):
        s = BucketState(key="k", tokens=1.0, capacity=2.0, refill_rate=0.5)
        s.tokens = 0.0
        assert s.tokens == 0.0

    def test_equality(self):
        a = BucketState(key="x", tokens=1, capacity=2, refill_rate=1)
        b = BucketState(key="x", tokens=1, capacity=2, refill_rate=1)
        assert a == b


class TestBucketStatsDataclass:
    def test_construct(self):
        s = BucketStats(total_buckets=3, total_allowed=10, total_denied=2, current_total_tokens=15.5)
        assert s.total_buckets == 3
        assert s.total_allowed == 10
        assert s.total_denied == 2
        assert s.current_total_tokens == 15.5

    def test_equality(self):
        a = BucketStats(1, 2, 3, 4.0)
        b = BucketStats(1, 2, 3, 4.0)
        assert a == b

    def test_inequality(self):
        a = BucketStats(1, 2, 3, 4.0)
        b = BucketStats(1, 2, 3, 5.0)
        assert a != b


class TestConstruction:
    def test_empty(self):
        b = DocTokenBucket()
        assert b.list_keys() == []

    def test_initial_stats(self):
        b = DocTokenBucket()
        s = b.stats(now=0.0)
        assert s.total_buckets == 0
        assert s.total_allowed == 0
        assert s.total_denied == 0
        assert s.current_total_tokens == 0.0

    def test_independent_instances(self):
        a = DocTokenBucket()
        b = DocTokenBucket()
        a.register("k", 5, 1, now=0.0)
        assert b.list_keys() == []


class TestRegister:
    def test_new_default_initial(self):
        b = DocTokenBucket()
        s = b.register("k", capacity=10, refill_rate=1, now=0.0)
        assert s.key == "k"
        assert s.tokens == 10.0
        assert s.capacity == 10.0
        assert s.refill_rate == 1.0
        assert s.last_refill_at == 0.0

    def test_new_custom_initial(self):
        b = DocTokenBucket()
        s = b.register("k", capacity=10, refill_rate=1, initial_tokens=3, now=0.0)
        assert s.tokens == 3.0

    def test_initial_clamped_to_capacity(self):
        b = DocTokenBucket()
        s = b.register("k", capacity=10, refill_rate=1, initial_tokens=999, now=0.0)
        assert s.tokens == 10.0

    def test_initial_clamped_to_zero(self):
        b = DocTokenBucket()
        s = b.register("k", capacity=10, refill_rate=1, initial_tokens=-5, now=0.0)
        assert s.tokens == 0.0

    def test_replace_existing(self):
        b = DocTokenBucket()
        b.register("k", capacity=5, refill_rate=1, now=0.0)
        b.consume("k", count=2, now=0.0)
        s = b.register("k", capacity=20, refill_rate=2, now=10.0)
        assert s.capacity == 20.0
        assert s.tokens == 20.0
        assert s.refill_rate == 2.0
        assert s.last_refill_at == 10.0

    def test_register_uses_default_now(self):
        b = DocTokenBucket()
        s = b.register("k", capacity=10, refill_rate=1)
        # last_refill_at set automatically (monotonic, > 0)
        assert s.last_refill_at > 0

    def test_multiple_keys(self):
        b = DocTokenBucket()
        b.register("a", 5, 1, now=0)
        b.register("b", 10, 2, now=0)
        assert sorted(b.list_keys()) == ["a", "b"]

    def test_returns_state(self):
        b = DocTokenBucket()
        s = b.register("k", capacity=4, refill_rate=1, now=0)
        assert isinstance(s, BucketState)


class TestConsume:
    def test_success_when_available(self):
        b = DocTokenBucket()
        b.register("k", 5, 1, now=0)
        assert b.consume("k", count=2, now=0) is True

    def test_state_after_consume(self):
        b = DocTokenBucket()
        b.register("k", 5, 1, now=0)
        b.consume("k", count=2, now=0)
        st = b.get_state("k")
        assert st.tokens == 3.0

    def test_denied_when_empty(self):
        b = DocTokenBucket()
        b.register("k", 1, 0, initial_tokens=0, now=0)
        assert b.consume("k", count=1, now=0) is False

    def test_denied_when_not_enough(self):
        b = DocTokenBucket()
        b.register("k", 5, 0, now=0)
        assert b.consume("k", count=6, now=0) is False

    def test_unregistered_returns_false(self):
        b = DocTokenBucket()
        assert b.consume("missing", now=0) is False

    def test_unregistered_increments_denied(self):
        b = DocTokenBucket()
        b.consume("missing", now=0)
        s = b.stats(now=0)
        assert s.total_denied == 1
        assert s.total_allowed == 0

    def test_denied_increments_counter(self):
        b = DocTokenBucket()
        b.register("k", 1, 0, initial_tokens=0, now=0)
        b.consume("k", now=0)
        assert b.stats(now=0).total_denied == 1

    def test_allowed_increments_counter(self):
        b = DocTokenBucket()
        b.register("k", 5, 0, now=0)
        b.consume("k", now=0)
        b.consume("k", now=0)
        assert b.stats(now=0).total_allowed == 2

    def test_default_count_one(self):
        b = DocTokenBucket()
        b.register("k", 3, 0, now=0)
        b.consume("k", now=0)
        assert b.get_state("k").tokens == 2.0

    def test_exact_match(self):
        b = DocTokenBucket()
        b.register("k", 5, 0, now=0)
        assert b.consume("k", count=5, now=0) is True
        assert b.get_state("k").tokens == 0.0

    def test_consume_uses_default_now(self):
        b = DocTokenBucket()
        b.register("k", 10, 0)
        assert b.consume("k") is True


class TestRefill:
    def test_grows_over_time(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=2.0, initial_tokens=0, now=0)
        b.peek("k", now=1.0)
        assert b.get_state("k").tokens == pytest.approx(2.0)

    def test_caps_at_capacity(self):
        b = DocTokenBucket()
        b.register("k", capacity=5, refill_rate=10.0, initial_tokens=0, now=0)
        b.peek("k", now=100.0)
        assert b.get_state("k").tokens == 5.0

    def test_no_refill_zero_rate(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=0.0, initial_tokens=3, now=0)
        b.peek("k", now=100.0)
        assert b.get_state("k").tokens == 3.0

    def test_no_refill_no_time_elapsed(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=5, initial_tokens=2, now=5)
        b.peek("k", now=5)
        assert b.get_state("k").tokens == 2.0

    def test_partial_refill_then_consume(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=1.0, initial_tokens=0, now=0)
        # After 3s → 3 tokens
        assert b.consume("k", count=2, now=3.0) is True
        assert b.get_state("k").tokens == pytest.approx(1.0)

    def test_refill_updates_last_refill_at(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=1.0, initial_tokens=0, now=0)
        b.peek("k", now=7.5)
        assert b.get_state("k").last_refill_at == 7.5


class TestPeek:
    def test_returns_current(self):
        b = DocTokenBucket()
        b.register("k", 10, 0, initial_tokens=4, now=0)
        assert b.peek("k", now=0) == 4.0

    def test_refills_before_returning(self):
        b = DocTokenBucket()
        b.register("k", 10, 2, initial_tokens=0, now=0)
        assert b.peek("k", now=2) == pytest.approx(4.0)

    def test_none_for_missing(self):
        b = DocTokenBucket()
        assert b.peek("missing", now=0) is None

    def test_peek_doesnt_increment_counters(self):
        b = DocTokenBucket()
        b.register("k", 5, 0, now=0)
        b.peek("k", now=0)
        s = b.stats(now=0)
        assert s.total_allowed == 0
        assert s.total_denied == 0


class TestRestore:
    def test_adds_tokens(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=0, initial_tokens=2, now=0)
        assert b.restore("k", count=3, now=0) is True
        assert b.get_state("k").tokens == 5.0

    def test_caps_at_capacity(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=0, initial_tokens=8, now=0)
        b.restore("k", count=100, now=0)
        assert b.get_state("k").tokens == 10.0

    def test_returns_false_when_missing(self):
        b = DocTokenBucket()
        assert b.restore("missing", count=1, now=0) is False

    def test_refills_first_then_adds(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=1, initial_tokens=0, now=0)
        # at t=2, refill brings to 2, then +3 → 5
        b.restore("k", count=3, now=2.0)
        assert b.get_state("k").tokens == pytest.approx(5.0)


class TestReset:
    def test_back_to_capacity(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=1, initial_tokens=2, now=0)
        assert b.reset("k", now=5) is True
        assert b.get_state("k").tokens == 10.0

    def test_updates_last_refill_at(self):
        b = DocTokenBucket()
        b.register("k", capacity=10, refill_rate=1, now=0)
        b.reset("k", now=42)
        assert b.get_state("k").last_refill_at == 42

    def test_returns_false_when_missing(self):
        b = DocTokenBucket()
        assert b.reset("missing", now=0) is False


class TestRemove:
    def test_existing_returns_true(self):
        b = DocTokenBucket()
        b.register("k", 1, 0, now=0)
        assert b.remove("k") is True

    def test_after_remove_gone(self):
        b = DocTokenBucket()
        b.register("k", 1, 0, now=0)
        b.remove("k")
        assert b.get_state("k") is None
        assert b.list_keys() == []

    def test_missing_returns_false(self):
        b = DocTokenBucket()
        assert b.remove("missing") is False

    def test_remove_one_keeps_others(self):
        b = DocTokenBucket()
        b.register("a", 1, 0, now=0)
        b.register("b", 1, 0, now=0)
        b.remove("a")
        assert b.list_keys() == ["b"]


class TestGetState:
    def test_found(self):
        b = DocTokenBucket()
        b.register("k", capacity=4, refill_rate=1, now=0)
        st = b.get_state("k")
        assert isinstance(st, BucketState)
        assert st.key == "k"

    def test_not_found(self):
        b = DocTokenBucket()
        assert b.get_state("missing") is None


class TestListKeys:
    def test_empty(self):
        b = DocTokenBucket()
        assert b.list_keys() == []

    def test_sorted(self):
        b = DocTokenBucket()
        for k in ["zebra", "alpha", "mango", "beta"]:
            b.register(k, 1, 0, now=0)
        assert b.list_keys() == ["alpha", "beta", "mango", "zebra"]

    def test_after_remove(self):
        b = DocTokenBucket()
        b.register("a", 1, 0, now=0)
        b.register("b", 1, 0, now=0)
        b.remove("a")
        assert b.list_keys() == ["b"]


class TestStats:
    def test_totals(self):
        b = DocTokenBucket()
        b.register("a", 5, 0, now=0)
        b.register("b", 5, 0, initial_tokens=0, now=0)
        b.consume("a", now=0)
        b.consume("a", now=0)
        b.consume("b", now=0)  # denied
        s = b.stats(now=0)
        assert s.total_buckets == 2
        assert s.total_allowed == 2
        assert s.total_denied == 1

    def test_current_total_tokens_simple(self):
        b = DocTokenBucket()
        b.register("a", 5, 0, initial_tokens=3, now=0)
        b.register("b", 10, 0, initial_tokens=7, now=0)
        s = b.stats(now=0)
        assert s.current_total_tokens == 10.0

    def test_current_total_tokens_refilled(self):
        b = DocTokenBucket()
        b.register("a", 10, 1.0, initial_tokens=0, now=0)
        b.register("b", 10, 2.0, initial_tokens=0, now=0)
        s = b.stats(now=3)
        # a refills 3, b refills 6 → 9
        assert s.current_total_tokens == pytest.approx(9.0)

    def test_stats_caps_at_capacity(self):
        b = DocTokenBucket()
        b.register("a", 5, 10.0, initial_tokens=0, now=0)
        s = b.stats(now=100)
        assert s.current_total_tokens == 5.0

    def test_empty_stats(self):
        b = DocTokenBucket()
        s = b.stats(now=0)
        assert s.total_buckets == 0
        assert s.current_total_tokens == 0.0


class TestThreadSafety:
    def test_concurrent_consume(self):
        b = DocTokenBucket()
        b.register("k", capacity=1000, refill_rate=0, initial_tokens=1000, now=0)

        def worker():
            for _ in range(100):
                b.consume("k", count=1, now=0)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = b.stats(now=0)
        # Total attempts = 1000, capacity = 1000 → all allowed
        assert s.total_allowed == 1000
        assert s.total_denied == 0
        assert b.get_state("k").tokens == 0.0

    def test_concurrent_consume_with_denials(self):
        b = DocTokenBucket()
        b.register("k", capacity=500, refill_rate=0, initial_tokens=500, now=0)

        def worker():
            for _ in range(100):
                b.consume("k", count=1, now=0)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = b.stats(now=0)
        assert s.total_allowed == 500
        assert s.total_denied == 500
        assert s.total_allowed + s.total_denied == 1000

    def test_concurrent_register_and_consume(self):
        b = DocTokenBucket()

        def register_worker():
            for i in range(50):
                b.register(f"k{i}", capacity=10, refill_rate=0, now=0)

        def consume_worker():
            for i in range(50):
                b.consume(f"k{i}", count=1, now=0)

        t1 = threading.Thread(target=register_worker)
        t2 = threading.Thread(target=consume_worker)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # no exception → ok
        assert len(b.list_keys()) == 50
