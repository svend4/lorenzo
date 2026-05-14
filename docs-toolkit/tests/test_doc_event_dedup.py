"""Tests for E431 DocEventDedup."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_event_dedup import (
    DedupEntry,
    DedupStats,
    DocEventDedup,
)


# --------------------------------------------------------------------- dataclasses
class TestDedupEntryDataclass:
    def test_minimal(self):
        e = DedupEntry(event_key="k", first_seen_at=1.0, last_seen_at=1.0)
        assert e.event_key == "k"
        assert e.first_seen_at == 1.0
        assert e.last_seen_at == 1.0
        assert e.hit_count == 1
        assert e.expires_at is None

    def test_full(self):
        e = DedupEntry(
            event_key="k",
            first_seen_at=1.0,
            last_seen_at=2.0,
            hit_count=5,
            expires_at=10.0,
        )
        assert e.hit_count == 5
        assert e.expires_at == 10.0

    def test_equality(self):
        a = DedupEntry(event_key="k", first_seen_at=1.0, last_seen_at=1.0)
        b = DedupEntry(event_key="k", first_seen_at=1.0, last_seen_at=1.0)
        assert a == b

    def test_inequality(self):
        a = DedupEntry(event_key="k1", first_seen_at=1.0, last_seen_at=1.0)
        b = DedupEntry(event_key="k2", first_seen_at=1.0, last_seen_at=1.0)
        assert a != b


class TestDedupStatsDataclass:
    def test_minimal(self):
        s = DedupStats(
            total_entries=0,
            total_seen=0,
            unique_events=0,
            total_filtered=0,
        )
        assert s.total_entries == 0
        assert s.total_seen == 0
        assert s.unique_events == 0
        assert s.total_filtered == 0

    def test_with_values(self):
        s = DedupStats(
            total_entries=10,
            total_seen=25,
            unique_events=8,
            total_filtered=15,
        )
        assert s.total_entries == 10
        assert s.total_seen == 25
        assert s.unique_events == 8
        assert s.total_filtered == 15


# --------------------------------------------------------------------- construction
class TestConstruction:
    def test_default_construction(self):
        d = DocEventDedup()
        assert d.stats().total_entries == 0

    def test_construction_with_ttl(self):
        d = DocEventDedup(default_ttl_seconds=60.0)
        d.record("k", now=100.0)
        entry = d.get_entry("k")
        assert entry is not None
        assert entry.expires_at == 160.0

    def test_construction_with_none_ttl(self):
        d = DocEventDedup(default_ttl_seconds=None)
        d.record("k", now=100.0)
        entry = d.get_entry("k")
        assert entry.expires_at is None


# --------------------------------------------------------------------- is_duplicate
class TestIsDuplicate:
    def test_missing_key(self):
        d = DocEventDedup()
        assert d.is_duplicate("nope") is False

    def test_existing_no_ttl(self):
        d = DocEventDedup()
        d.record("k", now=10.0)
        assert d.is_duplicate("k", now=20.0) is True

    def test_existing_within_ttl(self):
        d = DocEventDedup(default_ttl_seconds=100.0)
        d.record("k", now=10.0)
        assert d.is_duplicate("k", now=50.0) is True

    def test_expired_returns_false(self):
        d = DocEventDedup(default_ttl_seconds=10.0)
        d.record("k", now=0.0)
        assert d.is_duplicate("k", now=100.0) is False

    def test_uses_default_now(self):
        d = DocEventDedup()
        d.record("k")
        assert d.is_duplicate("k") is True


# --------------------------------------------------------------------- record
class TestRecord:
    def test_first_record_is_new(self):
        d = DocEventDedup()
        is_new, entry = d.record("k", now=5.0)
        assert is_new is True
        assert entry.event_key == "k"
        assert entry.first_seen_at == 5.0
        assert entry.last_seen_at == 5.0
        assert entry.hit_count == 1
        assert entry.expires_at is None

    def test_second_record_is_duplicate(self):
        d = DocEventDedup()
        d.record("k", now=1.0)
        is_new, entry = d.record("k", now=2.0)
        assert is_new is False
        assert entry.hit_count == 2
        assert entry.first_seen_at == 1.0
        assert entry.last_seen_at == 2.0

    def test_many_duplicates(self):
        d = DocEventDedup()
        for t in range(1, 11):
            d.record("k", now=float(t))
        entry = d.get_entry("k")
        assert entry.hit_count == 10
        assert entry.first_seen_at == 1.0
        assert entry.last_seen_at == 10.0

    def test_record_with_explicit_ttl(self):
        d = DocEventDedup()
        is_new, entry = d.record("k", ttl_seconds=30.0, now=5.0)
        assert entry.expires_at == 35.0

    def test_explicit_ttl_overrides_default(self):
        d = DocEventDedup(default_ttl_seconds=100.0)
        _, entry = d.record("k", ttl_seconds=10.0, now=0.0)
        assert entry.expires_at == 10.0

    def test_record_after_expiry_is_new(self):
        d = DocEventDedup(default_ttl_seconds=10.0)
        d.record("k", now=0.0)
        is_new, entry = d.record("k", now=100.0)
        assert is_new is True
        assert entry.hit_count == 1
        assert entry.first_seen_at == 100.0

    def test_total_filtered_incremented_on_dup(self):
        d = DocEventDedup()
        d.record("k", now=1.0)
        d.record("k", now=2.0)
        d.record("k", now=3.0)
        assert d.stats().total_filtered == 2

    def test_total_filtered_not_incremented_on_new(self):
        d = DocEventDedup()
        d.record("a")
        d.record("b")
        d.record("c")
        assert d.stats().total_filtered == 0

    def test_total_filtered_not_incremented_on_expired_reset(self):
        d = DocEventDedup(default_ttl_seconds=5.0)
        d.record("k", now=0.0)
        d.record("k", now=100.0)
        assert d.stats().total_filtered == 0

    def test_record_uses_default_now(self):
        d = DocEventDedup()
        is_new, entry = d.record("k")
        assert is_new is True
        assert entry.first_seen_at > 0

    def test_returns_tuple(self):
        d = DocEventDedup()
        result = d.record("k")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_distinct_keys_are_independent(self):
        d = DocEventDedup()
        d.record("a", now=1.0)
        d.record("b", now=2.0)
        assert d.get_entry("a").hit_count == 1
        assert d.get_entry("b").hit_count == 1


# --------------------------------------------------------------------- get_entry
class TestGetEntry:
    def test_missing_returns_none(self):
        d = DocEventDedup()
        assert d.get_entry("nope") is None

    def test_existing_returns_entry(self):
        d = DocEventDedup()
        d.record("k", now=1.0)
        entry = d.get_entry("k")
        assert entry is not None
        assert entry.event_key == "k"

    def test_returns_expired_entry_too(self):
        # get_entry has no expiration check; it returns whatever is stored.
        d = DocEventDedup(default_ttl_seconds=1.0)
        d.record("k", now=0.0)
        entry = d.get_entry("k")
        assert entry is not None


# --------------------------------------------------------------------- forget
class TestForget:
    def test_forget_existing(self):
        d = DocEventDedup()
        d.record("k")
        assert d.forget("k") is True
        assert d.get_entry("k") is None

    def test_forget_missing(self):
        d = DocEventDedup()
        assert d.forget("nope") is False

    def test_forget_twice(self):
        d = DocEventDedup()
        d.record("k")
        assert d.forget("k") is True
        assert d.forget("k") is False


# --------------------------------------------------------------------- purge_expired
class TestPurgeExpired:
    def test_no_expired(self):
        d = DocEventDedup()
        d.record("a")
        d.record("b")
        assert d.purge_expired() == 0

    def test_all_expired(self):
        d = DocEventDedup(default_ttl_seconds=1.0)
        d.record("a", now=0.0)
        d.record("b", now=0.0)
        assert d.purge_expired(now=100.0) == 2
        assert d.get_entry("a") is None
        assert d.get_entry("b") is None

    def test_some_expired(self):
        d = DocEventDedup()
        d.record("a", ttl_seconds=1.0, now=0.0)
        d.record("b", now=0.0)
        assert d.purge_expired(now=100.0) == 1
        assert d.get_entry("a") is None
        assert d.get_entry("b") is not None

    def test_purge_does_not_affect_total_filtered(self):
        d = DocEventDedup(default_ttl_seconds=1.0)
        d.record("a", now=0.0)
        d.record("a", now=0.5)  # filtered
        d.purge_expired(now=100.0)
        assert d.stats().total_filtered == 1


# --------------------------------------------------------------------- set_default_ttl
class TestSetDefaultTTL:
    def test_set_to_value(self):
        d = DocEventDedup()
        d.set_default_ttl(30.0)
        _, entry = d.record("k", now=0.0)
        assert entry.expires_at == 30.0

    def test_set_to_none(self):
        d = DocEventDedup(default_ttl_seconds=60.0)
        d.set_default_ttl(None)
        _, entry = d.record("k", now=0.0)
        assert entry.expires_at is None

    def test_change_does_not_affect_existing(self):
        d = DocEventDedup(default_ttl_seconds=60.0)
        _, entry = d.record("k", now=0.0)
        original_exp = entry.expires_at
        d.set_default_ttl(1000.0)
        assert d.get_entry("k").expires_at == original_exp


# --------------------------------------------------------------------- clear
class TestClear:
    def test_clear_empty(self):
        d = DocEventDedup()
        assert d.clear() == 0

    def test_clear_with_entries(self):
        d = DocEventDedup()
        d.record("a")
        d.record("b")
        d.record("c")
        assert d.clear() == 3
        assert d.stats().total_entries == 0

    def test_clear_resets_storage_but_not_filtered(self):
        # total_filtered is a lifetime counter; clearing entries does not reset it.
        d = DocEventDedup()
        d.record("k")
        d.record("k")
        assert d.stats().total_filtered == 1
        d.clear()
        assert d.stats().total_filtered == 1
        assert d.stats().total_entries == 0


# --------------------------------------------------------------------- all_keys
class TestAllKeys:
    def test_empty(self):
        d = DocEventDedup()
        assert d.all_keys() == []

    def test_sorted(self):
        d = DocEventDedup()
        d.record("c")
        d.record("a")
        d.record("b")
        assert d.all_keys() == ["a", "b", "c"]

    def test_excludes_expired(self):
        d = DocEventDedup()
        d.record("a", ttl_seconds=0.0001, now=0.0)
        d.record("b", now=0.0)
        time.sleep(0.01)
        keys = d.all_keys()
        assert "b" in keys
        assert "a" not in keys


# --------------------------------------------------------------------- most_seen
class TestMostSeen:
    def test_empty(self):
        d = DocEventDedup()
        assert d.most_seen() == []

    def test_order(self):
        d = DocEventDedup()
        d.record("a", now=1.0)
        for _ in range(5):
            d.record("b", now=1.0)
        for _ in range(2):
            d.record("c", now=1.0)
        result = d.most_seen()
        assert result[0].event_key == "b"
        assert result[1].event_key == "c"
        assert result[2].event_key == "a"

    def test_limit(self):
        d = DocEventDedup()
        for i in range(20):
            d.record(f"k{i}")
        assert len(d.most_seen(limit=5)) == 5

    def test_limit_zero(self):
        d = DocEventDedup()
        d.record("a")
        assert d.most_seen(limit=0) == []

    def test_negative_limit_treated_as_zero(self):
        d = DocEventDedup()
        d.record("a")
        assert d.most_seen(limit=-3) == []

    def test_tie_break_by_key(self):
        d = DocEventDedup()
        d.record("b")
        d.record("a")
        result = d.most_seen()
        # Equal hit_count → alphabetical by key
        assert [r.event_key for r in result] == ["a", "b"]


# --------------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        d = DocEventDedup()
        s = d.stats()
        assert s.total_entries == 0
        assert s.total_seen == 0
        assert s.unique_events == 0
        assert s.total_filtered == 0

    def test_basic(self):
        d = DocEventDedup()
        d.record("a", now=1.0)
        d.record("b", now=2.0)
        d.record("a", now=3.0)
        s = d.stats(now=4.0)
        assert s.total_entries == 2
        assert s.total_seen == 3
        assert s.unique_events == 2
        assert s.total_filtered == 1

    def test_unique_events_excludes_expired(self):
        d = DocEventDedup()
        d.record("a", ttl_seconds=10.0, now=0.0)
        d.record("b", now=0.0)
        s = d.stats(now=100.0)
        assert s.total_entries == 2
        assert s.unique_events == 1

    def test_returns_stats_type(self):
        d = DocEventDedup()
        s = d.stats()
        assert isinstance(s, DedupStats)


# --------------------------------------------------------------------- TTL edge cases
class TestTTLEdges:
    def test_zero_ttl_immediately_expired(self):
        d = DocEventDedup()
        d.record("k", ttl_seconds=0.0, now=10.0)
        # expires_at == now, _is_expired uses <=
        assert d.is_duplicate("k", now=10.0) is False

    def test_negative_ttl_immediately_expired(self):
        d = DocEventDedup()
        d.record("k", ttl_seconds=-1.0, now=10.0)
        assert d.is_duplicate("k", now=10.0) is False

    def test_ttl_exactly_at_boundary(self):
        d = DocEventDedup(default_ttl_seconds=10.0)
        d.record("k", now=0.0)
        # At exactly t=10 the entry expires (<=)
        assert d.is_duplicate("k", now=10.0) is False
        assert d.is_duplicate("k", now=9.999) is True


# --------------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_records_same_key(self):
        d = DocEventDedup()
        N = 200
        threads_count = 10

        def worker():
            for _ in range(N):
                d.record("shared")

        threads = [threading.Thread(target=worker) for _ in range(threads_count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        entry = d.get_entry("shared")
        assert entry.hit_count == N * threads_count
        assert d.stats().total_filtered == (N * threads_count) - 1

    def test_concurrent_records_distinct_keys(self):
        d = DocEventDedup()
        N = 100

        def worker(prefix):
            for i in range(N):
                d.record(f"{prefix}-{i}")

        threads = [
            threading.Thread(target=worker, args=(f"t{i}",)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert d.stats().total_entries == 8 * N
        assert d.stats().total_filtered == 0

    def test_concurrent_purge_and_record(self):
        d = DocEventDedup(default_ttl_seconds=0.01)
        stop = threading.Event()

        def writer():
            i = 0
            while not stop.is_set():
                d.record(f"k{i % 50}")
                i += 1

        def purger():
            while not stop.is_set():
                d.purge_expired()

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=writer),
            threading.Thread(target=purger),
        ]
        for t in threads:
            t.start()
        time.sleep(0.05)
        stop.set()
        for t in threads:
            t.join()

        # No assertion on exact values — only that no exception/deadlock occurred.
        s = d.stats()
        assert s.total_entries >= 0

    def test_concurrent_clear_and_record(self):
        d = DocEventDedup()
        stop = threading.Event()

        def writer():
            i = 0
            while not stop.is_set():
                d.record(f"k{i}")
                i += 1

        def clearer():
            while not stop.is_set():
                d.clear()

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=clearer),
        ]
        for t in threads:
            t.start()
        time.sleep(0.05)
        stop.set()
        for t in threads:
            t.join()

        # Should not crash; final state is whatever it is.
        assert d.stats().total_entries >= 0


# --------------------------------------------------------------------- integration
class TestIntegration:
    def test_typical_workflow(self):
        d = DocEventDedup(default_ttl_seconds=60.0)

        # First event of each key — new
        for key in ("evt-1", "evt-2", "evt-3"):
            is_new, _ = d.record(key, now=0.0)
            assert is_new is True

        # Duplicates within TTL — filtered
        for _ in range(5):
            is_new, _ = d.record("evt-1", now=10.0)
            assert is_new is False

        s = d.stats(now=10.0)
        assert s.total_entries == 3
        assert s.total_seen == 8
        assert s.unique_events == 3
        assert s.total_filtered == 5

        # After TTL — re-record evt-1, becomes new again
        is_new, entry = d.record("evt-1", now=200.0)
        assert is_new is True
        assert entry.hit_count == 1
        assert entry.first_seen_at == 200.0

    def test_purge_then_stats(self):
        d = DocEventDedup()
        d.record("a", ttl_seconds=1.0, now=0.0)
        d.record("b", ttl_seconds=1.0, now=0.0)
        d.record("c", now=0.0)
        removed = d.purge_expired(now=100.0)
        assert removed == 2
        s = d.stats(now=100.0)
        assert s.total_entries == 1
        assert s.unique_events == 1

    def test_forget_then_record_is_new(self):
        d = DocEventDedup()
        d.record("k", now=1.0)
        d.record("k", now=2.0)
        d.forget("k")
        is_new, entry = d.record("k", now=3.0)
        assert is_new is True
        assert entry.hit_count == 1

    def test_most_seen_after_clear_is_empty(self):
        d = DocEventDedup()
        for _ in range(3):
            d.record("k")
        d.clear()
        assert d.most_seen() == []

    def test_all_keys_after_forget(self):
        d = DocEventDedup()
        d.record("a")
        d.record("b")
        d.record("c")
        d.forget("b")
        assert d.all_keys() == ["a", "c"]

    def test_stats_total_seen_counts_hits_not_records(self):
        d = DocEventDedup()
        d.record("a")
        d.record("a")
        d.record("a")
        d.record("b")
        assert d.stats().total_seen == 4
