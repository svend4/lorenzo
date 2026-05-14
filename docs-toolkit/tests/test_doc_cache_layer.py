"""Tests for E339 DocCacheLayer."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_cache_layer import CacheEntry, CacheStats, DocCacheLayer


# ----------------------------------------------------------------------
# Dataclass tests
# ----------------------------------------------------------------------
class TestCacheEntryDataclass:
    def test_create_minimal(self):
        e = CacheEntry(key="a", value=1)
        assert e.key == "a"
        assert e.value == 1
        assert e.stored_at == 0.0
        assert e.expires_at is None
        assert e.hit_count == 0

    def test_create_full(self):
        e = CacheEntry(
            key="x", value="v", stored_at=1.5, expires_at=10.0, hit_count=3
        )
        assert e.stored_at == 1.5
        assert e.expires_at == 10.0
        assert e.hit_count == 3

    def test_value_can_be_any(self):
        e = CacheEntry(key="k", value={"complex": [1, 2]})
        assert e.value == {"complex": [1, 2]}

    def test_mutable_hit_count(self):
        e = CacheEntry(key="k", value=None)
        e.hit_count += 1
        assert e.hit_count == 1


class TestCacheStatsDataclass:
    def test_create(self):
        s = CacheStats(
            size=1, capacity=10, hit_count=2, miss_count=3,
            eviction_count=0, expiry_count=0,
        )
        assert s.size == 1
        assert s.capacity == 10
        assert s.hit_count == 2
        assert s.miss_count == 3
        assert s.eviction_count == 0
        assert s.expiry_count == 0

    def test_equality(self):
        a = CacheStats(0, 0, 0, 0, 0, 0)
        b = CacheStats(0, 0, 0, 0, 0, 0)
        assert a == b


# ----------------------------------------------------------------------
# Construction
# ----------------------------------------------------------------------
class TestConstruction:
    def test_default_capacity(self):
        c = DocCacheLayer()
        assert c.stats().capacity == 128

    def test_custom_capacity(self):
        c = DocCacheLayer(capacity=10)
        assert c.stats().capacity == 10

    def test_invalid_capacity_zero(self):
        with pytest.raises(ValueError):
            DocCacheLayer(capacity=0)

    def test_invalid_capacity_negative(self):
        with pytest.raises(ValueError):
            DocCacheLayer(capacity=-5)

    def test_initial_empty(self):
        c = DocCacheLayer()
        assert c.size() == 0
        s = c.stats()
        assert s.size == 0
        assert s.hit_count == 0
        assert s.miss_count == 0


# ----------------------------------------------------------------------
# Put
# ----------------------------------------------------------------------
class TestPut:
    def test_put_new_entry(self):
        c = DocCacheLayer(capacity=5)
        c.put("a", 1)
        assert c.get("a") == 1

    def test_put_update_existing(self):
        c = DocCacheLayer(capacity=5)
        c.put("a", 1)
        c.put("a", 2)
        assert c.get("a") == 2

    def test_put_update_moves_to_end(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        # Update 'a' — should move to end; 'b' becomes oldest
        c.put("a", 10)
        c.put("d", 4)  # fills cache — should evict 'b'
        assert c.peek("b") is None
        assert c.peek("a") == 10

    def test_put_eviction_when_full(self):
        c = DocCacheLayer(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)  # evicts 'a'
        assert c.peek("a") is None
        assert c.stats().eviction_count == 1

    def test_put_with_ttl(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=10, now=100.0)
        # not yet expired
        assert c.get("a", now=105.0) == 1
        # expired at now=110
        assert c.get("a", now=111.0) is None

    def test_put_explicit_now(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=1000.0)
        assert c.get("a", now=1004.0) == 1
        assert c.get("a", now=1006.0) is None


# ----------------------------------------------------------------------
# Get
# ----------------------------------------------------------------------
class TestGet:
    def test_hit_increments_counters(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.get("a")
        s = c.stats()
        assert s.hit_count == 1
        assert s.miss_count == 0

    def test_hit_increments_entry_hit_count(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.get("a")
        c.get("a")
        c.get("a")
        # entry has 3 hits — verify via stats hit_count
        assert c.stats().hit_count == 3

    def test_miss_increments_miss_counter(self):
        c = DocCacheLayer()
        c.get("absent")
        s = c.stats()
        assert s.miss_count == 1
        assert s.hit_count == 0

    def test_get_expired_returns_none(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        assert c.get("a", now=200.0) is None

    def test_get_expired_increments_expiry_and_miss(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.get("a", now=200.0)
        s = c.stats()
        assert s.expiry_count == 1
        assert s.miss_count == 1
        assert s.hit_count == 0

    def test_get_moves_to_end(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        # bump 'a' to recent
        c.get("a")
        c.put("d", 4)  # should evict 'b' (now oldest)
        assert c.peek("b") is None
        assert c.peek("a") == 1

    def test_get_returns_value(self):
        c = DocCacheLayer()
        c.put("k", {"v": 42})
        assert c.get("k") == {"v": 42}


# ----------------------------------------------------------------------
# Peek
# ----------------------------------------------------------------------
class TestPeek:
    def test_peek_returns_value(self):
        c = DocCacheLayer()
        c.put("a", 1)
        assert c.peek("a") == 1

    def test_peek_no_counter_update(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.peek("a")
        s = c.stats()
        assert s.hit_count == 0
        assert s.miss_count == 0

    def test_peek_miss_no_counter_update(self):
        c = DocCacheLayer()
        c.peek("absent")
        s = c.stats()
        assert s.hit_count == 0
        assert s.miss_count == 0

    def test_peek_no_lru_update(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.peek("a")  # should NOT move 'a' to end
        c.put("d", 4)  # evicts 'a' (oldest)
        assert c.peek("a") is None
        assert c.peek("b") == 2

    def test_peek_expired_returns_none(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        assert c.peek("a", now=200.0) is None

    def test_peek_expired_removes_entry(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.peek("a", now=200.0)
        # subsequent contains is False
        assert not c.contains("a", now=200.0)

    def test_peek_expired_increments_expiry(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.peek("a", now=200.0)
        assert c.stats().expiry_count == 1
        # but no miss counted
        assert c.stats().miss_count == 0


# ----------------------------------------------------------------------
# Delete
# ----------------------------------------------------------------------
class TestDelete:
    def test_delete_existing(self):
        c = DocCacheLayer()
        c.put("a", 1)
        assert c.delete("a") is True
        assert c.peek("a") is None

    def test_delete_absent(self):
        c = DocCacheLayer()
        assert c.delete("absent") is False


# ----------------------------------------------------------------------
# Clear
# ----------------------------------------------------------------------
class TestClear:
    def test_clear_returns_count(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        assert c.clear() == 3

    def test_clear_empties_cache(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.clear()
        assert c.size() == 0
        assert c.peek("a") is None

    def test_clear_empty(self):
        c = DocCacheLayer()
        assert c.clear() == 0


# ----------------------------------------------------------------------
# Contains
# ----------------------------------------------------------------------
class TestContains:
    def test_contains_true(self):
        c = DocCacheLayer()
        c.put("a", 1)
        assert c.contains("a") is True

    def test_contains_false(self):
        c = DocCacheLayer()
        assert c.contains("absent") is False

    def test_contains_expired_false(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        assert c.contains("a", now=200.0) is False

    def test_contains_no_lru_update(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.contains("a")
        c.put("d", 4)  # evicts oldest = 'a'
        assert c.peek("a") is None

    def test_contains_no_counter_update(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.contains("a")
        s = c.stats()
        assert s.hit_count == 0
        assert s.miss_count == 0


# ----------------------------------------------------------------------
# Size
# ----------------------------------------------------------------------
class TestSize:
    def test_size_empty(self):
        c = DocCacheLayer()
        assert c.size() == 0

    def test_size_count(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.put("b", 2)
        assert c.size() == 2

    def test_size_ignores_expired(self):
        # size counts only non-expired but does not remove them
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.put("b", 2)
        # at far future, 'a' is expired
        # but size() uses time.time() — emulate by checking stats post-purge
        # We test the contract: size returns non-expired count.
        # Using internal time.time() is fine because 'a' expired at 105.
        assert c.size() == 1
        # And entry is still there (not removed)
        assert "a" in c.keys()

    def test_size_after_eviction(self):
        c = DocCacheLayer(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        assert c.size() == 2


# ----------------------------------------------------------------------
# LRU eviction
# ----------------------------------------------------------------------
class TestLRUEviction:
    def test_oldest_evicted(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.put("d", 4)
        assert c.peek("a") is None
        assert c.peek("b") == 2
        assert c.peek("c") == 3
        assert c.peek("d") == 4

    def test_eviction_counter(self):
        c = DocCacheLayer(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.put("d", 4)
        assert c.stats().eviction_count == 2

    def test_recent_access_protects(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.get("a")
        c.put("d", 4)
        # 'b' should be evicted, 'a' protected
        assert c.peek("a") == 1
        assert c.peek("b") is None

    def test_update_protects(self):
        c = DocCacheLayer(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.put("a", 99)  # update — moves 'a' to end
        c.put("d", 4)
        assert c.peek("a") == 99
        assert c.peek("b") is None


# ----------------------------------------------------------------------
# TTL expiry
# ----------------------------------------------------------------------
class TestTTLExpiry:
    def test_no_ttl_never_expires(self):
        c = DocCacheLayer()
        c.put("a", 1, now=0.0)
        # very far future
        assert c.get("a", now=1e12) == 1

    def test_ttl_expires(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=10, now=100.0)
        assert c.get("a", now=110.5) is None

    def test_ttl_boundary(self):
        # expires_at = stored_at + ttl
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=10, now=100.0)
        # at exactly expires_at, considered expired (now >= expires_at)
        assert c.get("a", now=110.0) is None

    def test_ttl_just_before_boundary(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=10, now=100.0)
        assert c.get("a", now=109.999) == 1

    def test_ttl_zero_immediate_expiry(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=0, now=100.0)
        assert c.get("a", now=100.0) is None


# ----------------------------------------------------------------------
# Purge expired
# ----------------------------------------------------------------------
class TestPurgeExpired:
    def test_purge_count(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.put("b", 2, ttl_seconds=5, now=100.0)
        c.put("c", 3)
        assert c.purge_expired(now=200.0) == 2

    def test_purge_only_expired_removed(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.put("b", 2)
        c.purge_expired(now=200.0)
        assert c.peek("a") is None
        assert c.peek("b") == 2

    def test_purge_empty(self):
        c = DocCacheLayer()
        assert c.purge_expired(now=100.0) == 0

    def test_purge_none_expired(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.put("b", 2)
        assert c.purge_expired(now=100.0) == 0

    def test_purge_increments_expiry_count(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        c.put("b", 2, ttl_seconds=5, now=100.0)
        c.purge_expired(now=200.0)
        assert c.stats().expiry_count == 2


# ----------------------------------------------------------------------
# Keys
# ----------------------------------------------------------------------
class TestKeys:
    def test_keys_sorted(self):
        c = DocCacheLayer()
        c.put("c", 3)
        c.put("a", 1)
        c.put("b", 2)
        assert c.keys() == ["a", "b", "c"]

    def test_keys_empty(self):
        c = DocCacheLayer()
        assert c.keys() == []

    def test_keys_includes_expired(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=5, now=100.0)
        # not purged — still in list
        assert "a" in c.keys()


# ----------------------------------------------------------------------
# Stats
# ----------------------------------------------------------------------
class TestStats:
    def test_initial_stats(self):
        c = DocCacheLayer(capacity=10)
        s = c.stats()
        assert s.size == 0
        assert s.capacity == 10
        assert s.hit_count == 0
        assert s.miss_count == 0
        assert s.eviction_count == 0
        assert s.expiry_count == 0

    def test_stats_after_operations(self):
        c = DocCacheLayer(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.get("a")
        c.get("a")
        c.get("missing")
        c.put("c", 3)  # eviction
        s = c.stats()
        assert s.hit_count == 2
        assert s.miss_count == 1
        assert s.eviction_count == 1
        assert s.size == 2

    def test_stats_expiry(self):
        c = DocCacheLayer()
        c.put("a", 1, ttl_seconds=1, now=100.0)
        c.get("a", now=200.0)
        s = c.stats()
        assert s.expiry_count == 1
        assert s.miss_count == 1

    def test_stats_size_reflects_cache(self):
        c = DocCacheLayer()
        c.put("a", 1)
        c.put("b", 2)
        assert c.stats().size == 2
        c.delete("a")
        assert c.stats().size == 1


# ----------------------------------------------------------------------
# Thread safety
# ----------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_put(self):
        c = DocCacheLayer(capacity=200)

        def worker(start: int) -> None:
            for i in range(50):
                c.put(f"k{start}_{i}", i)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # All 4*50 = 200 entries fit
        assert c.size() == 200

    def test_concurrent_get_put(self):
        c = DocCacheLayer(capacity=500)
        for i in range(100):
            c.put(f"k{i}", i)

        errors: list[Exception] = []

        def reader() -> None:
            try:
                for i in range(200):
                    c.get(f"k{i % 100}")
            except Exception as e:  # pragma: no cover
                errors.append(e)

        def writer() -> None:
            try:
                for i in range(200):
                    c.put(f"w{i}", i)
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [
            threading.Thread(target=reader) for _ in range(3)
        ] + [threading.Thread(target=writer) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []

    def test_concurrent_clear_and_put(self):
        c = DocCacheLayer(capacity=100)
        errors: list[Exception] = []

        def putter() -> None:
            try:
                for i in range(100):
                    c.put(f"k{i}", i)
            except Exception as e:  # pragma: no cover
                errors.append(e)

        def clearer() -> None:
            try:
                for _ in range(20):
                    c.clear()
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [
            threading.Thread(target=putter),
            threading.Thread(target=putter),
            threading.Thread(target=clearer),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
