"""Tests for E424 DocCapacityTracker."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_capacity_tracker import (
    CapacityBucket,
    CapacityCheck,
    CapacityStats,
    DocCapacityTracker,
)


# ---------------------------------------------------------------------------
# create_bucket
# ---------------------------------------------------------------------------


def test_create_bucket_returns_bucket() -> None:
    tracker = DocCapacityTracker()
    bucket = tracker.create_bucket("a", 10)
    assert isinstance(bucket, CapacityBucket)
    assert bucket.name == "a"
    assert bucket.capacity == 10
    assert bucket.used == 0


def test_create_bucket_stores_in_internal_dict() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    assert tracker.get_bucket("a") is not None


def test_create_bucket_zero_capacity_allowed() -> None:
    tracker = DocCapacityTracker()
    bucket = tracker.create_bucket("a", 0)
    assert bucket.capacity == 0


def test_create_bucket_negative_capacity_raises() -> None:
    tracker = DocCapacityTracker()
    with pytest.raises(ValueError):
        tracker.create_bucket("a", -1)


def test_create_bucket_with_now() -> None:
    tracker = DocCapacityTracker()
    bucket = tracker.create_bucket("a", 5, now=1000.0)
    assert bucket.created_at == 1000.0


def test_create_bucket_default_now_uses_time() -> None:
    tracker = DocCapacityTracker()
    bucket = tracker.create_bucket("a", 5)
    assert bucket.created_at > 0


def test_create_bucket_replaces_existing() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 3)
    new_bucket = tracker.create_bucket("a", 20)
    assert new_bucket.capacity == 20
    assert new_bucket.used == 0


# ---------------------------------------------------------------------------
# delete_bucket
# ---------------------------------------------------------------------------


def test_delete_bucket_existing() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    assert tracker.delete_bucket("a") is True
    assert tracker.get_bucket("a") is None


def test_delete_bucket_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.delete_bucket("missing") is False


# ---------------------------------------------------------------------------
# get_bucket
# ---------------------------------------------------------------------------


def test_get_bucket_existing() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    bucket = tracker.get_bucket("a")
    assert bucket is not None
    assert bucket.name == "a"


def test_get_bucket_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.get_bucket("missing") is None


# ---------------------------------------------------------------------------
# set_capacity
# ---------------------------------------------------------------------------


def test_set_capacity_existing() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    assert tracker.set_capacity("a", 20) is True
    assert tracker.get_bucket("a").capacity == 20  # type: ignore[union-attr]


def test_set_capacity_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.set_capacity("missing", 5) is False


def test_set_capacity_negative_raises() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    with pytest.raises(ValueError):
        tracker.set_capacity("a", -1)


def test_set_capacity_preserves_used() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 5)
    tracker.set_capacity("a", 20)
    assert tracker.get_bucket("a").used == 5  # type: ignore[union-attr]


def test_set_capacity_lower_than_used_allowed() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 8)
    assert tracker.set_capacity("a", 5) is True
    assert tracker.get_bucket("a").used == 8  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# acquire
# ---------------------------------------------------------------------------


def test_acquire_allowed_default_units() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    check = tracker.acquire("a")
    assert check.allowed is True
    assert check.requested == 1
    assert check.available == 4
    assert check.bucket == "a"


def test_acquire_allowed_multi_units() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    check = tracker.acquire("a", 3)
    assert check.allowed is True
    assert check.available == 7


def test_acquire_exactly_to_capacity() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    check = tracker.acquire("a", 5)
    assert check.allowed is True
    assert check.available == 0


def test_acquire_exceeds_capacity() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    check = tracker.acquire("a", 6)
    assert check.allowed is False
    assert check.requested == 6
    assert check.available == 5
    assert "exceeded" in check.reason.lower()


def test_acquire_after_partial_fills() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 7)
    check = tracker.acquire("a", 4)
    assert check.allowed is False


def test_acquire_missing_bucket() -> None:
    tracker = DocCapacityTracker()
    check = tracker.acquire("missing")
    assert check.allowed is False
    assert "not found" in check.reason.lower()
    assert check.bucket == "missing"


def test_acquire_returns_capacity_check_type() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    check = tracker.acquire("a")
    assert isinstance(check, CapacityCheck)


def test_acquire_negative_units_disallowed() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    check = tracker.acquire("a", -1)
    assert check.allowed is False


def test_acquire_zero_units_allowed() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    check = tracker.acquire("a", 0)
    assert check.allowed is True
    assert tracker.get_bucket("a").used == 0  # type: ignore[union-attr]


def test_acquire_increments_used() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 3)
    tracker.acquire("a", 2)
    assert tracker.get_bucket("a").used == 5  # type: ignore[union-attr]


def test_acquire_failed_does_not_increment() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    tracker.acquire("a", 4)
    tracker.acquire("a", 2)
    assert tracker.get_bucket("a").used == 4  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# release
# ---------------------------------------------------------------------------


def test_release_existing() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 5)
    assert tracker.release("a", 3) is True
    assert tracker.get_bucket("a").used == 2  # type: ignore[union-attr]


def test_release_default_units() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 5)
    tracker.release("a")
    assert tracker.get_bucket("a").used == 4  # type: ignore[union-attr]


def test_release_floors_at_zero() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 2)
    tracker.release("a", 5)
    assert tracker.get_bucket("a").used == 0  # type: ignore[union-attr]


def test_release_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.release("missing") is False


def test_release_allows_reacquire() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    tracker.acquire("a", 5)
    assert tracker.acquire("a", 1).allowed is False
    tracker.release("a", 2)
    assert tracker.acquire("a", 1).allowed is True


# ---------------------------------------------------------------------------
# try_acquire
# ---------------------------------------------------------------------------


def test_try_acquire_true() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    assert tracker.try_acquire("a", 3) is True


def test_try_acquire_false() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    assert tracker.try_acquire("a", 10) is False


def test_try_acquire_missing_bucket() -> None:
    tracker = DocCapacityTracker()
    assert tracker.try_acquire("missing") is False


# ---------------------------------------------------------------------------
# available
# ---------------------------------------------------------------------------


def test_available_empty() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    assert tracker.available("a") == 10


def test_available_partial() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 4)
    assert tracker.available("a") == 6


def test_available_full() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 10)
    assert tracker.available("a") == 0


def test_available_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.available("missing") is None


# ---------------------------------------------------------------------------
# usage_pct
# ---------------------------------------------------------------------------


def test_usage_pct_empty() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    assert tracker.usage_pct("a") == 0.0


def test_usage_pct_half() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 5)
    assert tracker.usage_pct("a") == 0.5


def test_usage_pct_full() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 10)
    assert tracker.usage_pct("a") == 1.0


def test_usage_pct_zero_capacity() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 0)
    assert tracker.usage_pct("a") == 1.0


def test_usage_pct_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.usage_pct("missing") is None


# ---------------------------------------------------------------------------
# list_buckets
# ---------------------------------------------------------------------------


def test_list_buckets_empty() -> None:
    tracker = DocCapacityTracker()
    assert tracker.list_buckets() == []


def test_list_buckets_sorted() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("c", 1)
    tracker.create_bucket("a", 2)
    tracker.create_bucket("b", 3)
    names = [b.name for b in tracker.list_buckets()]
    assert names == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# buckets_near_capacity
# ---------------------------------------------------------------------------


def test_buckets_near_capacity_default_threshold() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.create_bucket("b", 10)
    tracker.acquire("a", 9)
    tracker.acquire("b", 5)
    near = tracker.buckets_near_capacity()
    assert [b.name for b in near] == ["a"]


def test_buckets_near_capacity_custom_threshold() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.create_bucket("b", 10)
    tracker.acquire("a", 5)
    tracker.acquire("b", 6)
    near = tracker.buckets_near_capacity(threshold_pct=0.5)
    assert [b.name for b in near] == ["a", "b"]


def test_buckets_near_capacity_empty() -> None:
    tracker = DocCapacityTracker()
    assert tracker.buckets_near_capacity() == []


def test_buckets_near_capacity_zero_capacity_treated_full() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 0)
    near = tracker.buckets_near_capacity()
    assert [b.name for b in near] == ["a"]


def test_buckets_near_capacity_sorted_by_name() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("z", 10)
    tracker.create_bucket("a", 10)
    tracker.acquire("z", 10)
    tracker.acquire("a", 10)
    near = tracker.buckets_near_capacity()
    assert [b.name for b in near] == ["a", "z"]


# ---------------------------------------------------------------------------
# reset
# ---------------------------------------------------------------------------


def test_reset_existing() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 5)
    assert tracker.reset("a") is True
    assert tracker.get_bucket("a").used == 0  # type: ignore[union-attr]


def test_reset_missing() -> None:
    tracker = DocCapacityTracker()
    assert tracker.reset("missing") is False


def test_reset_preserves_capacity() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.acquire("a", 5)
    tracker.reset("a")
    assert tracker.get_bucket("a").capacity == 10  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_empty() -> None:
    tracker = DocCapacityTracker()
    assert tracker.clear() == 0


def test_clear_returns_count() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 1)
    tracker.create_bucket("b", 1)
    tracker.create_bucket("c", 1)
    assert tracker.clear() == 3
    assert tracker.list_buckets() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty() -> None:
    tracker = DocCapacityTracker()
    stats = tracker.stats()
    assert isinstance(stats, CapacityStats)
    assert stats.total_buckets == 0
    assert stats.total_capacity == 0
    assert stats.total_used == 0
    assert stats.buckets_at_capacity == 0


def test_stats_aggregates() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.create_bucket("b", 20)
    tracker.acquire("a", 3)
    tracker.acquire("b", 7)
    stats = tracker.stats()
    assert stats.total_buckets == 2
    assert stats.total_capacity == 30
    assert stats.total_used == 10
    assert stats.buckets_at_capacity == 0


def test_stats_buckets_at_capacity() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.create_bucket("b", 5)
    tracker.acquire("a", 10)
    tracker.acquire("b", 3)
    stats = tracker.stats()
    assert stats.buckets_at_capacity == 1


def test_stats_zero_capacity_bucket_counted_at_capacity() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 0)
    stats = tracker.stats()
    assert stats.buckets_at_capacity == 1


# ---------------------------------------------------------------------------
# dataclass defaults
# ---------------------------------------------------------------------------


def test_capacity_check_default_reason() -> None:
    check = CapacityCheck(
        bucket="x", allowed=True, requested=1, available=0
    )
    assert check.reason == ""


def test_capacity_bucket_defaults() -> None:
    bucket = CapacityBucket(name="x", capacity=5)
    assert bucket.used == 0
    assert bucket.created_at == 0.0


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------


def test_thread_safety_concurrent_acquire() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 100)
    successes: list[int] = []
    lock = threading.Lock()

    def worker() -> None:
        for _ in range(50):
            if tracker.try_acquire("a", 1):
                with lock:
                    successes.append(1)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # Total attempts = 500, capacity = 100, so exactly 100 successes
    assert len(successes) == 100
    assert tracker.get_bucket("a").used == 100  # type: ignore[union-attr]


def test_thread_safety_concurrent_acquire_release() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 50)

    def acquirer() -> None:
        for _ in range(200):
            tracker.try_acquire("a", 1)

    def releaser() -> None:
        for _ in range(200):
            tracker.release("a", 1)

    threads = [
        threading.Thread(target=acquirer) for _ in range(5)
    ] + [threading.Thread(target=releaser) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # No invariants violated; used must be in [0, capacity]
    used = tracker.get_bucket("a").used  # type: ignore[union-attr]
    assert 0 <= used <= 50


def test_thread_safety_concurrent_create_delete() -> None:
    tracker = DocCapacityTracker()

    def creator() -> None:
        for i in range(50):
            tracker.create_bucket(f"b{i}", 10)

    def deleter() -> None:
        for i in range(50):
            tracker.delete_bucket(f"b{i}")

    threads = [
        threading.Thread(target=creator),
        threading.Thread(target=creator),
        threading.Thread(target=deleter),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # Just verify no crash and list_buckets works
    tracker.list_buckets()


def test_thread_safety_stats_during_writes() -> None:
    tracker = DocCapacityTracker()
    for i in range(10):
        tracker.create_bucket(f"b{i}", 100)

    stop = threading.Event()

    def writer() -> None:
        while not stop.is_set():
            for i in range(10):
                tracker.try_acquire(f"b{i}", 1)
                tracker.release(f"b{i}", 1)

    def reader() -> None:
        for _ in range(100):
            stats = tracker.stats()
            assert stats.total_buckets == 10

    t_writer = threading.Thread(target=writer)
    t_reader = threading.Thread(target=reader)
    t_writer.start()
    t_reader.start()
    t_reader.join()
    stop.set()
    t_writer.join()


def test_acquire_atomic_under_contention() -> None:
    """Many threads racing on a tiny bucket — must never overshoot capacity."""
    tracker = DocCapacityTracker()
    tracker.create_bucket("tiny", 5)
    barrier = threading.Barrier(20)

    def worker() -> None:
        barrier.wait()
        for _ in range(100):
            check = tracker.acquire("tiny", 1)
            if check.allowed:
                tracker.release("tiny", 1)

    threads = [threading.Thread(target=worker) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    bucket = tracker.get_bucket("tiny")
    assert bucket is not None
    assert 0 <= bucket.used <= 5


# ---------------------------------------------------------------------------
# integration scenarios
# ---------------------------------------------------------------------------


def test_full_lifecycle() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("docs", 100)
    for _ in range(50):
        assert tracker.try_acquire("docs", 1)
    assert tracker.usage_pct("docs") == 0.5
    tracker.release("docs", 50)
    assert tracker.usage_pct("docs") == 0.0
    tracker.delete_bucket("docs")
    assert tracker.get_bucket("docs") is None


def test_multiple_buckets_independent() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 10)
    tracker.create_bucket("b", 20)
    tracker.acquire("a", 10)
    assert tracker.try_acquire("a", 1) is False
    assert tracker.try_acquire("b", 5) is True


def test_reset_after_full_allows_acquire() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    tracker.acquire("a", 5)
    assert tracker.try_acquire("a", 1) is False
    tracker.reset("a")
    assert tracker.try_acquire("a", 1) is True


def test_set_capacity_unlocks_more_acquires() -> None:
    tracker = DocCapacityTracker()
    tracker.create_bucket("a", 5)
    tracker.acquire("a", 5)
    assert tracker.try_acquire("a", 1) is False
    tracker.set_capacity("a", 10)
    assert tracker.try_acquire("a", 1) is True
