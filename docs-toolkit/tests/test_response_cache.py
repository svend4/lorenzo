"""Tests for docstoolkit.response_cache (E14)."""
import pytest
import time

from docstoolkit.response_cache import (
    CacheStatus,
    CacheEntry,
    ResponseCacheStore,
    CacheConfig,
    CacheLookupResult,
    ResponseCache,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_TS = 1_000_000.0  # arbitrary fixed timestamp


def make_entry(
    key="k1",
    value="v1",
    created_ts=BASE_TS,
    ttl=600.0,
    hit_count=0,
    last_accessed=BASE_TS,
) -> CacheEntry:
    return CacheEntry(
        cache_key=key,
        value=value,
        created_ts=created_ts,
        ttl_seconds=ttl,
        hit_count=hit_count,
        last_accessed=last_accessed,
    )


# ---------------------------------------------------------------------------
# CacheStatus enum
# ---------------------------------------------------------------------------

class TestCacheStatus:
    def test_values_exist(self):
        assert CacheStatus.HIT == "hit"
        assert CacheStatus.MISS == "miss"
        assert CacheStatus.STALE == "stale"
        assert CacheStatus.EXPIRED == "expired"

    def test_is_string(self):
        assert isinstance(CacheStatus.HIT, str)


# ---------------------------------------------------------------------------
# CacheEntry
# ---------------------------------------------------------------------------

class TestCacheEntryIsExpired:
    def test_not_expired_before_ttl(self):
        e = make_entry(ttl=100.0)
        assert not e.is_expired(now=BASE_TS + 50)

    def test_expired_at_ttl_boundary(self):
        e = make_entry(ttl=100.0)
        assert e.is_expired(now=BASE_TS + 100)

    def test_expired_after_ttl(self):
        e = make_entry(ttl=100.0)
        assert e.is_expired(now=BASE_TS + 200)

    def test_uses_time_when_now_not_given(self):
        # Created far in the past → must be expired regardless of wall clock
        old_entry = make_entry(created_ts=1.0, ttl=1.0)
        assert old_entry.is_expired()

    def test_just_created_not_expired(self):
        now = time.time()
        e = make_entry(created_ts=now, ttl=600.0)
        assert not e.is_expired()


class TestCacheEntryIsStale:
    def test_fresh_not_stale(self):
        e = make_entry(ttl=600.0)
        assert not e.is_stale(stale_after=300.0, now=BASE_TS + 100)

    def test_stale_when_age_gt_stale_after_and_not_expired(self):
        e = make_entry(ttl=600.0)
        assert e.is_stale(stale_after=300.0, now=BASE_TS + 400)

    def test_not_stale_when_expired(self):
        e = make_entry(ttl=600.0)
        assert not e.is_stale(stale_after=300.0, now=BASE_TS + 700)

    def test_boundary_stale_after_equals_age(self):
        # age == stale_after is NOT stale (must be strictly greater)
        e = make_entry(ttl=600.0)
        assert not e.is_stale(stale_after=300.0, now=BASE_TS + 300)

    def test_uses_time_when_now_not_given(self):
        # Fresh entry → not stale
        now = time.time()
        e = make_entry(created_ts=now, ttl=3600.0)
        assert not e.is_stale(stale_after=1800.0)


class TestCacheEntryTouch:
    def test_touch_increments_hit_count(self):
        e = make_entry(hit_count=3)
        touched = e.touch(now=BASE_TS + 10)
        assert touched.hit_count == 4

    def test_touch_updates_last_accessed(self):
        e = make_entry(last_accessed=BASE_TS)
        touched = e.touch(now=BASE_TS + 50)
        assert touched.last_accessed == BASE_TS + 50

    def test_touch_preserves_other_fields(self):
        e = make_entry(key="mykey", value="myval", ttl=300.0)
        touched = e.touch(now=BASE_TS + 1)
        assert touched.cache_key == "mykey"
        assert touched.value == "myval"
        assert touched.ttl_seconds == 300.0
        assert touched.created_ts == BASE_TS

    def test_touch_does_not_mutate_original(self):
        e = make_entry(hit_count=0)
        _ = e.touch(now=BASE_TS + 1)
        assert e.hit_count == 0

    def test_touch_uses_time_when_now_not_given(self):
        before = time.time()
        e = make_entry(last_accessed=0.0)
        touched = e.touch()
        assert touched.last_accessed >= before

    def test_touch_multiple_times(self):
        e = make_entry(hit_count=0)
        for i in range(5):
            e = e.touch(now=BASE_TS + i)
        assert e.hit_count == 5


# ---------------------------------------------------------------------------
# ResponseCacheStore
# ---------------------------------------------------------------------------

class TestResponseCacheStoreSetGet:
    def setup_method(self):
        self.store = ResponseCacheStore()

    def test_get_missing_returns_none(self):
        assert self.store.get("nonexistent") is None

    def test_set_and_get_round_trip(self):
        e = make_entry()
        self.store.set(e)
        result = self.store.get("k1")
        assert result is not None
        assert result.cache_key == "k1"
        assert result.value == "v1"

    def test_set_replaces_existing(self):
        e1 = make_entry(value="first")
        e2 = make_entry(value="second")
        self.store.set(e1)
        self.store.set(e2)
        assert self.store.get("k1").value == "second"

    def test_multiple_keys(self):
        for i in range(5):
            self.store.set(make_entry(key=f"k{i}", value=f"v{i}"))
        for i in range(5):
            assert self.store.get(f"k{i}").value == f"v{i}"

    def test_hit_count_persisted(self):
        e = make_entry(hit_count=7)
        self.store.set(e)
        assert self.store.get("k1").hit_count == 7

    def test_last_accessed_persisted(self):
        e = make_entry(last_accessed=BASE_TS + 99)
        self.store.set(e)
        assert self.store.get("k1").last_accessed == BASE_TS + 99


class TestResponseCacheStoreDelete:
    def setup_method(self):
        self.store = ResponseCacheStore()

    def test_delete_existing_returns_true(self):
        self.store.set(make_entry())
        assert self.store.delete("k1") is True

    def test_delete_removes_entry(self):
        self.store.set(make_entry())
        self.store.delete("k1")
        assert self.store.get("k1") is None

    def test_delete_nonexistent_returns_false(self):
        assert self.store.delete("ghost") is False

    def test_delete_idempotent(self):
        self.store.set(make_entry())
        self.store.delete("k1")
        assert self.store.delete("k1") is False


class TestResponseCacheStoreEvictExpired:
    def setup_method(self):
        self.store = ResponseCacheStore()

    def test_evict_expired_removes_expired(self):
        e = make_entry(ttl=10.0)
        self.store.set(e)
        removed = self.store.evict_expired(now=BASE_TS + 20)
        assert removed == 1
        assert self.store.get("k1") is None

    def test_evict_expired_keeps_fresh(self):
        e = make_entry(ttl=600.0)
        self.store.set(e)
        removed = self.store.evict_expired(now=BASE_TS + 100)
        assert removed == 0
        assert self.store.get("k1") is not None

    def test_evict_expired_mixed(self):
        self.store.set(make_entry(key="expired1", ttl=5.0))
        self.store.set(make_entry(key="expired2", ttl=5.0))
        self.store.set(make_entry(key="fresh", ttl=600.0))
        removed = self.store.evict_expired(now=BASE_TS + 10)
        assert removed == 2
        assert self.store.get("fresh") is not None

    def test_evict_expired_boundary_at_ttl(self):
        # age == ttl → expired
        e = make_entry(ttl=100.0)
        self.store.set(e)
        removed = self.store.evict_expired(now=BASE_TS + 100)
        assert removed == 1

    def test_evict_expired_uses_time_when_now_not_given(self):
        old = CacheEntry(
            cache_key="old",
            value="v",
            created_ts=1.0,
            ttl_seconds=1.0,
        )
        self.store.set(old)
        removed = self.store.evict_expired()
        assert removed == 1


class TestResponseCacheStoreEvictLRU:
    def setup_method(self):
        self.store = ResponseCacheStore()

    def _populate(self, n: int, base_accessed: float = BASE_TS):
        for i in range(n):
            e = CacheEntry(
                cache_key=f"k{i}",
                value=f"v{i}",
                created_ts=BASE_TS,
                ttl_seconds=600.0,
                hit_count=0,
                last_accessed=base_accessed + i,
            )
            self.store.set(e)

    def test_no_eviction_when_within_max(self):
        self._populate(5)
        assert self.store.evict_lru(max_size=10) == 0

    def test_evicts_correct_count(self):
        self._populate(10)
        removed = self.store.evict_lru(max_size=7)
        assert removed == 3

    def test_removes_least_recently_accessed(self):
        self._populate(5)
        # k0 has the smallest last_accessed (BASE_TS + 0)
        self.store.evict_lru(max_size=4)
        assert self.store.get("k0") is None
        assert self.store.get("k4") is not None

    def test_evict_lru_max_size_zero_removes_all(self):
        self._populate(5)
        removed = self.store.evict_lru(max_size=0)
        assert removed == 5

    def test_evict_lru_exact_max_size(self):
        self._populate(3)
        removed = self.store.evict_lru(max_size=3)
        assert removed == 0


class TestResponseCacheStoreStats:
    def setup_method(self):
        self.store = ResponseCacheStore()

    def test_empty_store_stats(self):
        s = self.store.stats()
        assert s["total_entries"] == 0
        assert s["total_hits"] == 0
        assert s["hit_rate"] == 0.0

    def test_stats_after_sets(self):
        self.store.set(make_entry(key="a", hit_count=0))
        self.store.set(make_entry(key="b", hit_count=0))
        s = self.store.stats()
        assert s["total_entries"] == 2
        assert s["total_hits"] == 0

    def test_stats_total_hits(self):
        self.store.set(make_entry(key="a", hit_count=3))
        self.store.set(make_entry(key="b", hit_count=7))
        s = self.store.stats()
        assert s["total_hits"] == 10

    def test_hit_rate_nonzero(self):
        self.store.set(make_entry(key="a", hit_count=10))
        s = self.store.stats()
        assert 0.0 < s["hit_rate"] <= 1.0

    def test_stats_after_delete(self):
        self.store.set(make_entry())
        self.store.delete("k1")
        s = self.store.stats()
        assert s["total_entries"] == 0


# ---------------------------------------------------------------------------
# ResponseCache high-level API
# ---------------------------------------------------------------------------

class TestResponseCacheGetMiss:
    def setup_method(self):
        self.cache = ResponseCache()

    def test_miss_on_empty_cache(self):
        result = self.cache.get("no_key", now=BASE_TS)
        assert result.status == CacheStatus.MISS
        assert result.value is None
        assert result.cache_key == "no_key"

    def test_miss_age_is_zero(self):
        result = self.cache.get("no_key", now=BASE_TS)
        assert result.age_seconds == 0.0


class TestResponseCacheGetHit:
    def setup_method(self):
        cfg = CacheConfig(ttl_seconds=600.0, stale_after=300.0)
        self.cache = ResponseCache(config=cfg)

    def test_hit_after_set(self):
        self.cache.set("k1", "hello", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 100)
        assert result.status == CacheStatus.HIT
        assert result.value == "hello"

    def test_hit_cache_key_preserved(self):
        self.cache.set("mykey", "myval", now=BASE_TS)
        result = self.cache.get("mykey", now=BASE_TS + 1)
        assert result.cache_key == "mykey"

    def test_hit_age_seconds_correct(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 50)
        assert result.age_seconds == pytest.approx(50.0)

    def test_hit_increments_hit_count_in_store(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        self.cache.get("k1", now=BASE_TS + 10)
        self.cache.get("k1", now=BASE_TS + 20)
        s = self.cache.stats()
        assert s["total_hits"] == 2


class TestResponseCacheGetStale:
    def setup_method(self):
        cfg = CacheConfig(ttl_seconds=600.0, stale_after=300.0)
        self.cache = ResponseCache(config=cfg)

    def test_stale_after_stale_after_but_before_ttl(self):
        self.cache.set("k1", "val", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 400)
        assert result.status == CacheStatus.STALE
        assert result.value == "val"

    def test_stale_age_correct(self):
        self.cache.set("k1", "val", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 400)
        assert result.age_seconds == pytest.approx(400.0)

    def test_stale_still_returns_value(self):
        self.cache.set("k1", "stale_val", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 500)
        assert result.value == "stale_val"


class TestResponseCacheGetExpired:
    def setup_method(self):
        cfg = CacheConfig(ttl_seconds=600.0, stale_after=300.0)
        self.cache = ResponseCache(config=cfg)

    def test_expired_after_ttl(self):
        self.cache.set("k1", "val", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 700)
        assert result.status == CacheStatus.EXPIRED
        assert result.value is None

    def test_expired_age_correct(self):
        self.cache.set("k1", "val", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 700)
        assert result.age_seconds == pytest.approx(700.0)

    def test_expired_key_preserved(self):
        self.cache.set("k1", "val", now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 700)
        assert result.cache_key == "k1"


class TestResponseCacheStatusTransitions:
    """Verify the full HIT → STALE → EXPIRED lifecycle."""

    def setup_method(self):
        cfg = CacheConfig(ttl_seconds=600.0, stale_after=300.0)
        self.cache = ResponseCache(config=cfg)

    def test_hit_to_stale_to_expired(self):
        self.cache.set("k", "v", now=BASE_TS)
        assert self.cache.get("k", now=BASE_TS + 100).status == CacheStatus.HIT
        assert self.cache.get("k", now=BASE_TS + 400).status == CacheStatus.STALE
        assert self.cache.get("k", now=BASE_TS + 700).status == CacheStatus.EXPIRED

    def test_set_resets_entry(self):
        self.cache.set("k", "v1", now=BASE_TS)
        self.cache.get("k", now=BASE_TS + 400)  # stale
        # Re-set should make it fresh again
        self.cache.set("k", "v2", now=BASE_TS + 400)
        result = self.cache.get("k", now=BASE_TS + 450)
        assert result.status == CacheStatus.HIT
        assert result.value == "v2"


class TestResponseCacheCustomTTL:
    def setup_method(self):
        cfg = CacheConfig(ttl_seconds=600.0, stale_after=300.0)
        self.cache = ResponseCache(config=cfg)

    def test_custom_ttl_shorter_than_default(self):
        self.cache.set("k1", "val", ttl_seconds=50.0, now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 60)
        assert result.status == CacheStatus.EXPIRED

    def test_custom_ttl_longer_than_default(self):
        self.cache.set("k1", "val", ttl_seconds=1200.0, now=BASE_TS)
        result = self.cache.get("k1", now=BASE_TS + 700)
        assert result.status != CacheStatus.EXPIRED

    def test_default_ttl_when_none_passed(self):
        self.cache.set("k1", "val", ttl_seconds=None, now=BASE_TS)
        # At 400s, should be stale (default stale_after=300) but not expired (ttl=600)
        result = self.cache.get("k1", now=BASE_TS + 400)
        assert result.status == CacheStatus.STALE


class TestResponseCacheInvalidate:
    def setup_method(self):
        self.cache = ResponseCache()

    def test_invalidate_existing_returns_true(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        assert self.cache.invalidate("k1") is True

    def test_invalidate_removes_entry(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        self.cache.invalidate("k1")
        result = self.cache.get("k1", now=BASE_TS + 1)
        assert result.status == CacheStatus.MISS

    def test_invalidate_nonexistent_returns_false(self):
        assert self.cache.invalidate("ghost") is False

    def test_invalidate_idempotent(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        self.cache.invalidate("k1")
        assert self.cache.invalidate("k1") is False


class TestResponseCacheEvict:
    def setup_method(self):
        cfg = CacheConfig(ttl_seconds=600.0, stale_after=300.0, max_size=5)
        self.cache = ResponseCache(config=cfg)

    def test_evict_removes_expired(self):
        self.cache.set("short", "v", ttl_seconds=10.0, now=BASE_TS)
        self.cache.set("long", "v", ttl_seconds=600.0, now=BASE_TS)
        removed = self.cache.evict(now=BASE_TS + 20)
        assert removed >= 1
        assert self.cache.get("short", now=BASE_TS + 20).status == CacheStatus.MISS

    def test_evict_lru_trim(self):
        # Insert max_size + 3 entries; use now well within ttl so none expire
        for i in range(8):
            self.cache.set(f"k{i}", f"v{i}", now=BASE_TS + i)
        # now=BASE_TS + 10 is within ttl=600, so no expired eviction;
        # 8 entries exceed max_size=5, so LRU trim removes 3
        removed = self.cache.evict(now=BASE_TS + 10)
        assert removed == 3

    def test_evict_returns_total_count(self):
        self.cache.set("exp", "v", ttl_seconds=5.0, now=BASE_TS)
        for i in range(7):
            self.cache.set(f"live{i}", "v", now=BASE_TS + i)
        # At BASE_TS+10: "exp" is expired; 7 live entries exceed max_size=5 by 2
        removed = self.cache.evict(now=BASE_TS + 10)
        assert removed == 3  # 1 expired + 2 LRU


class TestResponseCacheStats:
    def setup_method(self):
        self.cache = ResponseCache()

    def test_empty_stats(self):
        s = self.cache.stats()
        assert s["total_entries"] == 0
        assert s["total_hits"] == 0

    def test_stats_track_hits(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        self.cache.get("k1", now=BASE_TS + 10)
        self.cache.get("k1", now=BASE_TS + 20)
        s = self.cache.stats()
        assert s["total_hits"] == 2

    def test_hit_rate_after_accesses(self):
        self.cache.set("k1", "v1", now=BASE_TS)
        self.cache.get("k1", now=BASE_TS + 10)
        s = self.cache.stats()
        assert s["hit_rate"] > 0.0


class TestCacheLookupResultDataclass:
    def test_fields(self):
        r = CacheLookupResult(
            status=CacheStatus.HIT,
            value="hello",
            cache_key="k",
            age_seconds=5.0,
        )
        assert r.status == CacheStatus.HIT
        assert r.value == "hello"
        assert r.cache_key == "k"
        assert r.age_seconds == 5.0

    def test_default_age(self):
        r = CacheLookupResult(status=CacheStatus.MISS, value=None, cache_key="k")
        assert r.age_seconds == 0.0


class TestCacheConfigDataclass:
    def test_defaults(self):
        cfg = CacheConfig()
        assert cfg.ttl_seconds == 600.0
        assert cfg.stale_after == 300.0
        assert cfg.max_size == 1000

    def test_custom_values(self):
        cfg = CacheConfig(ttl_seconds=60.0, stale_after=30.0, max_size=100)
        assert cfg.ttl_seconds == 60.0
        assert cfg.stale_after == 30.0
        assert cfg.max_size == 100


class TestResponseCacheCustomStore:
    def test_accepts_custom_store(self):
        store = ResponseCacheStore(":memory:")
        cache = ResponseCache(store=store)
        cache.set("k", "v", now=BASE_TS)
        assert cache.get("k", now=BASE_TS + 1).status == CacheStatus.HIT

    def test_shared_store_between_caches(self):
        store = ResponseCacheStore(":memory:")
        c1 = ResponseCache(store=store)
        c2 = ResponseCache(store=store)
        c1.set("shared", "data", now=BASE_TS)
        assert c2.get("shared", now=BASE_TS + 1).value == "data"
