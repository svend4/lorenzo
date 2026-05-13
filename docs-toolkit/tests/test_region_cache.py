"""Tests for docstoolkit.region_cache."""
from __future__ import annotations

import os
import tempfile

import pytest

from docstoolkit.region_cache import (
    CacheEntry,
    CacheTier,
    RegionCache,
    RegionStats,
)


# ---------------------------------------------------------------------------
# CacheTier
# ---------------------------------------------------------------------------
class TestCacheTier:
    def test_has_three_members(self):
        assert {t.name for t in CacheTier} == {"L1", "L2", "MISS"}

    def test_values(self):
        assert CacheTier.L1.value == "l1"
        assert CacheTier.L2.value == "l2"
        assert CacheTier.MISS.value == "miss"

    def test_members_distinct(self):
        assert CacheTier.L1 is not CacheTier.L2
        assert CacheTier.L2 is not CacheTier.MISS


# ---------------------------------------------------------------------------
# CacheEntry
# ---------------------------------------------------------------------------
class TestCacheEntry:
    def test_defaults(self):
        e = CacheEntry(key="k", value=1, tier=CacheTier.L1)
        assert e.region == "default"
        assert e.created_at == 0.0
        assert e.accessed_at == 0.0
        assert e.access_count == 0
        assert e.expires_at is None

    def test_full_construction(self):
        e = CacheEntry(
            key="k",
            value="v",
            tier=CacheTier.L2,
            region="r",
            created_at=1.0,
            accessed_at=2.0,
            access_count=3,
            expires_at=10.0,
        )
        assert e.key == "k"
        assert e.value == "v"
        assert e.tier == CacheTier.L2
        assert e.region == "r"
        assert e.created_at == 1.0
        assert e.accessed_at == 2.0
        assert e.access_count == 3
        assert e.expires_at == 10.0


# ---------------------------------------------------------------------------
# RegionStats
# ---------------------------------------------------------------------------
class TestRegionStats:
    def test_zero_hit_rate_when_no_lookups(self):
        s = RegionStats(region="r")
        assert s.hit_rate == 0.0

    def test_hit_rate_all_hits(self):
        s = RegionStats(region="r", l1_hits=3, l2_hits=2, misses=0)
        assert s.hit_rate == 1.0

    def test_hit_rate_all_misses(self):
        s = RegionStats(region="r", l1_hits=0, l2_hits=0, misses=5)
        assert s.hit_rate == 0.0

    def test_hit_rate_mixed(self):
        s = RegionStats(region="r", l1_hits=2, l2_hits=2, misses=4)
        assert s.hit_rate == 0.5

    def test_default_sizes(self):
        s = RegionStats(region="r")
        assert s.l1_size == 0 and s.l2_size == 0


# ---------------------------------------------------------------------------
# set / get basics
# ---------------------------------------------------------------------------
class TestSetGet:
    def test_set_returns_entry(self):
        c = RegionCache()
        e = c.set("a", 1)
        assert isinstance(e, CacheEntry)
        assert e.key == "a"
        assert e.value == 1
        assert e.tier == CacheTier.L1

    def test_get_after_set(self):
        c = RegionCache()
        c.set("a", 1)
        tier, val = c.get("a")
        assert tier == CacheTier.L1
        assert val == 1

    def test_set_overwrites_value(self):
        c = RegionCache()
        c.set("a", 1)
        c.set("a", 2)
        tier, val = c.get("a")
        assert val == 2

    def test_set_overwrites_does_not_grow(self):
        c = RegionCache()
        c.set("a", 1)
        c.set("a", 2)
        assert c.size() == 1

    def test_get_various_types(self):
        c = RegionCache()
        c.set("s", "hello")
        c.set("i", 42)
        c.set("f", 3.14)
        c.set("l", [1, 2, 3])
        c.set("d", {"x": 1})
        c.set("n", None)
        c.set("b", True)
        assert c.get("s")[1] == "hello"
        assert c.get("i")[1] == 42
        assert c.get("f")[1] == 3.14
        assert c.get("l")[1] == [1, 2, 3]
        assert c.get("d")[1] == {"x": 1}
        assert c.get("n")[1] is None
        assert c.get("b")[1] is True


# ---------------------------------------------------------------------------
# L1 hit
# ---------------------------------------------------------------------------
class TestL1Hit:
    def test_freshly_set_is_l1(self):
        c = RegionCache()
        c.set("a", 1)
        tier, _ = c.get("a")
        assert tier == CacheTier.L1

    def test_l1_hit_increments_access_count(self):
        c = RegionCache()
        c.set("a", 1, now=1.0)
        c.get("a", now=2.0)
        c.get("a", now=3.0)
        stats = c.stats("default")["default"]
        assert stats.l1_hits == 2

    def test_l1_hit_updates_stats(self):
        c = RegionCache()
        c.set("a", 1)
        c.get("a")
        stats = c.stats("default")["default"]
        assert stats.l1_hits == 1
        assert stats.misses == 0


# ---------------------------------------------------------------------------
# L2 hit (after eviction)
# ---------------------------------------------------------------------------
class TestL2Hit:
    def test_evicted_entry_in_l2(self):
        c = RegionCache(l1_capacity=2)
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)  # evicts "a"
        tier, val = c.get("a")
        assert tier == CacheTier.L2
        assert val == 1

    def test_l2_hit_records_stats(self):
        c = RegionCache(l1_capacity=1)
        c.set("a", 1)
        c.set("b", 2)  # evicts a
        c.get("a")
        s = c.stats("default")["default"]
        assert s.l2_hits == 1

    def test_demoted_entry_returns_l2(self):
        c = RegionCache()
        c.set("a", 1)
        c.demote("a")
        tier, val = c.get("a")
        assert tier == CacheTier.L2
        assert val == 1

    def test_l2_hit_does_not_auto_promote(self):
        c = RegionCache()
        c.set("a", 1)
        c.demote("a")
        c.get("a")
        # Second get should still be L2 unless promoted.
        tier, _ = c.get("a")
        assert tier == CacheTier.L2


# ---------------------------------------------------------------------------
# Miss
# ---------------------------------------------------------------------------
class TestMiss:
    def test_get_missing_key(self):
        c = RegionCache()
        tier, val = c.get("nope")
        assert tier == CacheTier.MISS
        assert val is None

    def test_miss_increments_counter(self):
        c = RegionCache()
        c.get("nope")
        c.get("nada")
        s = c.stats("default")["default"]
        assert s.misses == 2

    def test_miss_does_not_count_hits(self):
        c = RegionCache()
        c.get("nope")
        s = c.stats("default")["default"]
        assert s.l1_hits == 0 and s.l2_hits == 0


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_existing_l1(self):
        c = RegionCache()
        c.set("a", 1)
        assert c.delete("a") is True
        assert c.get("a")[0] == CacheTier.MISS

    def test_delete_existing_l2(self):
        c = RegionCache()
        c.set("a", 1)
        c.demote("a")
        assert c.delete("a") is True
        assert c.get("a")[0] == CacheTier.MISS

    def test_delete_missing(self):
        c = RegionCache()
        assert c.delete("nope") is False

    def test_delete_isolates_region(self):
        c = RegionCache()
        c.set("a", 1, region="r1")
        c.set("a", 2, region="r2")
        c.delete("a", region="r1")
        assert c.get("a", region="r2")[1] == 2


# ---------------------------------------------------------------------------
# Promote (L2 -> L1)
# ---------------------------------------------------------------------------
class TestPromote:
    def test_promote_l2_entry(self):
        c = RegionCache()
        c.set("a", 1)
        c.demote("a")
        assert c.promote("a") is True
        assert c.get("a")[0] == CacheTier.L1

    def test_promote_missing(self):
        c = RegionCache()
        assert c.promote("nope") is False

    def test_promote_already_l1(self):
        c = RegionCache()
        c.set("a", 1)
        # No L2 copy — treated as success (already in L1).
        assert c.promote("a") is True
        assert c.get("a")[0] == CacheTier.L1

    def test_promote_preserves_value(self):
        c = RegionCache()
        c.set("a", {"v": 99})
        c.demote("a")
        c.promote("a")
        assert c.get("a")[1] == {"v": 99}


# ---------------------------------------------------------------------------
# Demote (L1 -> L2)
# ---------------------------------------------------------------------------
class TestDemote:
    def test_demote_l1_entry(self):
        c = RegionCache()
        c.set("a", 1)
        assert c.demote("a") is True
        assert c.get("a")[0] == CacheTier.L2

    def test_demote_missing(self):
        c = RegionCache()
        assert c.demote("nope") is False

    def test_demote_already_l2_fails(self):
        c = RegionCache()
        c.set("a", 1)
        c.demote("a")
        assert c.demote("a") is False

    def test_demote_preserves_value(self):
        c = RegionCache()
        c.set("a", [1, 2, 3])
        c.demote("a")
        assert c.get("a")[1] == [1, 2, 3]


# ---------------------------------------------------------------------------
# LRU eviction
# ---------------------------------------------------------------------------
class TestLRUEviction:
    def test_eviction_at_capacity(self):
        c = RegionCache(l1_capacity=2)
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)
        # a should now be in L2
        assert c.get("a")[0] == CacheTier.L2

    def test_recently_accessed_not_evicted(self):
        c = RegionCache(l1_capacity=2)
        c.set("a", 1)
        c.set("b", 2)
        c.get("a")  # mark a as MRU
        c.set("c", 3)  # evicts b
        assert c.get("b")[0] == CacheTier.L2
        assert c.get("a")[0] == CacheTier.L1

    def test_capacity_respected(self):
        c = RegionCache(l1_capacity=3)
        for i in range(10):
            c.set(f"k{i}", i)
        # L1 capacity must not be exceeded.
        s = c.stats()
        l1_total = sum(v.l1_size for v in s.values())
        assert l1_total == 3

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            RegionCache(l1_capacity=0)


# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------
class TestRegions:
    def test_isolated_namespaces(self):
        c = RegionCache()
        c.set("k", "one", region="r1")
        c.set("k", "two", region="r2")
        assert c.get("k", region="r1")[1] == "one"
        assert c.get("k", region="r2")[1] == "two"

    def test_regions_listed(self):
        c = RegionCache()
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r2")
        regs = c.regions()
        assert "r1" in regs and "r2" in regs

    def test_default_region(self):
        c = RegionCache()
        c.set("a", 1)
        assert "default" in c.regions()

    def test_l2_only_region_listed(self):
        c = RegionCache(l1_capacity=1)
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r2")  # evicts r1/a
        assert "r1" in c.regions()


# ---------------------------------------------------------------------------
# Expiration
# ---------------------------------------------------------------------------
class TestExpiration:
    def test_expired_returns_miss(self):
        c = RegionCache()
        c.set("a", 1, expires_at=10.0, now=1.0)
        tier, val = c.get("a", now=20.0)
        assert tier == CacheTier.MISS
        assert val is None

    def test_not_yet_expired_hits(self):
        c = RegionCache()
        c.set("a", 1, expires_at=100.0, now=1.0)
        tier, val = c.get("a", now=50.0)
        assert tier == CacheTier.L1
        assert val == 1

    def test_l2_expiration(self):
        c = RegionCache()
        c.set("a", 1, expires_at=10.0, now=1.0)
        c.demote("a")
        tier, _ = c.get("a", now=20.0)
        assert tier == CacheTier.MISS

    def test_no_expires_never_expires(self):
        c = RegionCache()
        c.set("a", 1, now=1.0)
        tier, _ = c.get("a", now=10 ** 9)
        assert tier == CacheTier.L1


# ---------------------------------------------------------------------------
# Cleanup expired
# ---------------------------------------------------------------------------
class TestCleanupExpired:
    def test_cleanup_removes_expired_l1(self):
        c = RegionCache()
        c.set("a", 1, expires_at=10.0, now=1.0)
        c.set("b", 2, expires_at=100.0, now=1.0)
        n = c.cleanup_expired(now=50.0)
        assert n == 1
        assert c.get("a", now=50.0)[0] == CacheTier.MISS
        assert c.get("b", now=50.0)[0] == CacheTier.L1

    def test_cleanup_removes_expired_l2(self):
        c = RegionCache()
        c.set("a", 1, expires_at=10.0, now=1.0)
        c.demote("a")
        n = c.cleanup_expired(now=50.0)
        assert n == 1

    def test_cleanup_nothing_to_do(self):
        c = RegionCache()
        c.set("a", 1, now=1.0)
        assert c.cleanup_expired(now=10.0) == 0

    def test_cleanup_mixed_tiers(self):
        c = RegionCache()
        c.set("a", 1, expires_at=10.0, now=1.0)
        c.set("b", 2, expires_at=10.0, now=1.0)
        c.demote("b")
        n = c.cleanup_expired(now=20.0)
        assert n == 2


# ---------------------------------------------------------------------------
# Clear region
# ---------------------------------------------------------------------------
class TestClearRegion:
    def test_clear_region_empties_it(self):
        c = RegionCache()
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r1")
        c.set("c", 3, region="r2")
        n = c.clear_region("r1")
        assert n == 2
        assert c.get("a", region="r1")[0] == CacheTier.MISS
        assert c.get("c", region="r2")[1] == 3

    def test_clear_region_includes_l2(self):
        c = RegionCache(l1_capacity=1)
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r1")  # evicts a → L2
        n = c.clear_region("r1")
        assert n == 2

    def test_clear_unknown_region(self):
        c = RegionCache()
        assert c.clear_region("nope") == 0


# ---------------------------------------------------------------------------
# Clear all
# ---------------------------------------------------------------------------
class TestClearAll:
    def test_clear_all_empties_cache(self):
        c = RegionCache()
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r2")
        n = c.clear_all()
        assert n == 2
        assert c.size() == 0

    def test_clear_all_resets_stats(self):
        c = RegionCache()
        c.set("a", 1)
        c.get("a")
        c.clear_all()
        # After clear_all, stats for default region should be gone or zeroed.
        all_stats = c.stats()
        if "default" in all_stats:
            assert all_stats["default"].l1_hits == 0

    def test_clear_all_handles_empty(self):
        c = RegionCache()
        assert c.clear_all() == 0


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_stats_single_region(self):
        c = RegionCache()
        c.set("a", 1)
        c.get("a")
        c.get("missing")
        s = c.stats("default")["default"]
        assert s.l1_hits == 1
        assert s.misses == 1

    def test_stats_all_regions(self):
        c = RegionCache()
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r2")
        c.get("a", region="r1")
        c.get("b", region="r2")
        all_stats = c.stats()
        assert "r1" in all_stats and "r2" in all_stats
        assert all_stats["r1"].l1_hits == 1
        assert all_stats["r2"].l1_hits == 1

    def test_hit_rate_computed(self):
        c = RegionCache()
        c.set("a", 1)
        c.get("a")
        c.get("x")  # miss
        s = c.stats("default")["default"]
        assert s.hit_rate == 0.5

    def test_l1_l2_sizes(self):
        c = RegionCache(l1_capacity=1)
        c.set("a", 1)
        c.set("b", 2)  # evicts a
        s = c.stats("default")["default"]
        assert s.l1_size == 1
        assert s.l2_size == 1


# ---------------------------------------------------------------------------
# Size
# ---------------------------------------------------------------------------
class TestSize:
    def test_size_total(self):
        c = RegionCache()
        c.set("a", 1)
        c.set("b", 2, region="r2")
        assert c.size() == 2

    def test_size_per_region(self):
        c = RegionCache()
        c.set("a", 1, region="r1")
        c.set("b", 2, region="r1")
        c.set("c", 3, region="r2")
        assert c.size(region="r1") == 2
        assert c.size(region="r2") == 1

    def test_size_includes_l2(self):
        c = RegionCache(l1_capacity=1)
        c.set("a", 1)
        c.set("b", 2)
        assert c.size() == 2

    def test_size_empty(self):
        c = RegionCache()
        assert c.size() == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_non_serializable_value(self):
        c = RegionCache()
        with pytest.raises(TypeError):
            c.set("a", object())

    def test_empty_key(self):
        c = RegionCache()
        c.set("", 42)
        assert c.get("")[1] == 42

    def test_unicode_key_and_region(self):
        c = RegionCache()
        c.set("ключ", "значение", region="регион")
        assert c.get("ключ", region="регион")[1] == "значение"

    def test_persistence_to_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "cache.db")
            c1 = RegionCache(db_path=path)
            c1.set("a", "kept")
            c1.demote("a")
            c1.close()
            c2 = RegionCache(db_path=path)
            tier, val = c2.get("a")
            assert tier == CacheTier.L2
            assert val == "kept"
            c2.close()

    def test_close_is_idempotent(self):
        c = RegionCache()
        c.close()
        c.close()  # must not raise

    def test_context_manager(self):
        with RegionCache() as c:
            c.set("a", 1)
            assert c.get("a")[1] == 1

    def test_set_after_demote_overrides_l2(self):
        c = RegionCache()
        c.set("a", 1)
        c.demote("a")
        c.set("a", 2)
        tier, val = c.get("a")
        assert tier == CacheTier.L1
        assert val == 2
        # And size should be 1, not 2.
        assert c.size() == 1
