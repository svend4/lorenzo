"""Tests for the doc_cache_invalidation module (E262)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_cache_invalidation import (
    CacheKey,
    CacheStats,
    DocCacheInvalidation,
    InvalidationEvent,
    InvalidationStrategy,
)


# --------------------------------------------------------------------- enum
class TestInvalidationStrategy:
    def test_has_ttl(self):
        assert InvalidationStrategy.TTL.value == "ttl"

    def test_has_manual(self):
        assert InvalidationStrategy.MANUAL.value == "manual"

    def test_has_dependency(self):
        assert InvalidationStrategy.DEPENDENCY.value == "dependency"

    def test_has_tag(self):
        assert InvalidationStrategy.TAG.value == "tag"

    def test_has_pattern(self):
        assert InvalidationStrategy.PATTERN.value == "pattern"

    def test_total_members(self):
        assert len(list(InvalidationStrategy)) == 5


# ---------------------------------------------------------------- dataclass
class TestCacheKey:
    def test_basic_fields(self):
        k = CacheKey(key="k", doc_id="d", value=42, created_at=1.0)
        assert k.key == "k"
        assert k.doc_id == "d"
        assert k.value == 42
        assert k.created_at == 1.0
        assert k.expires_at is None

    def test_default_tags_empty(self):
        k = CacheKey(key="k", doc_id="d", value=None, created_at=0.0)
        assert k.tags == set()

    def test_default_dependencies_empty(self):
        k = CacheKey(key="k", doc_id="d", value=None, created_at=0.0)
        assert k.dependencies == set()

    def test_with_tags(self):
        k = CacheKey(
            key="k", doc_id="d", value=None, created_at=0.0, tags={"a", "b"}
        )
        assert k.tags == {"a", "b"}


class TestInvalidationEvent:
    def test_construction(self):
        e = InvalidationEvent(
            event_id=1,
            strategy=InvalidationStrategy.TAG,
            keys_invalidated=["k1", "k2"],
            timestamp=10.0,
        )
        assert e.event_id == 1
        assert e.strategy is InvalidationStrategy.TAG
        assert e.keys_invalidated == ["k1", "k2"]
        assert e.reason is None

    def test_reason(self):
        e = InvalidationEvent(
            event_id=1,
            strategy=InvalidationStrategy.MANUAL,
            keys_invalidated=[],
            timestamp=0.0,
            reason="why",
        )
        assert e.reason == "why"


class TestCacheStats:
    def test_construction(self):
        s = CacheStats(
            total_entries=5,
            total_invalidations=3,
            hit_count=2,
            miss_count=1,
        )
        assert s.total_entries == 5
        assert s.total_invalidations == 3


# ---------------------------------------------------------------------- set
class TestSet:
    def test_set_returns_cache_key(self):
        c = DocCacheInvalidation()
        k = c.set("a", "doc1", 1)
        assert isinstance(k, CacheKey)
        assert k.key == "a"

    def test_set_stores_value(self):
        c = DocCacheInvalidation()
        c.set("a", "doc1", 42)
        assert c.get("a") == 42

    def test_set_with_ttl(self):
        c = DocCacheInvalidation()
        k = c.set("a", "doc1", 1, ttl=10.0, now=5.0)
        assert k.expires_at == 15.0

    def test_set_with_tags(self):
        c = DocCacheInvalidation()
        c.set("a", "doc1", 1, tags={"t1", "t2"})
        assert c.tags_for("a") == {"t1", "t2"}

    def test_set_with_dependencies(self):
        c = DocCacheInvalidation()
        c.set("a", "doc1", 1, dependencies={"d1"})
        assert c.dependencies_of("a") == {"d1"}

    def test_set_overwrites(self):
        c = DocCacheInvalidation()
        c.set("a", "doc1", 1, tags={"t1"})
        c.set("a", "doc2", 2, tags={"t2"})
        assert c.get("a") == 2
        assert c.tags_for("a") == {"t2"}
        # Old indices cleaned up
        assert c.keys_with_tag("t1") == []
        assert c.keys_for_doc("doc1") == []


# ---------------------------------------------------------------------- get
class TestGet:
    def test_missing_returns_none(self):
        c = DocCacheInvalidation()
        assert c.get("missing") is None

    def test_existing_returns_value(self):
        c = DocCacheInvalidation()
        c.set("k", "d", "v")
        assert c.get("k") == "v"

    def test_get_increments_hit(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.get("k")
        assert c.stats().hit_count == 1

    def test_get_increments_miss(self):
        c = DocCacheInvalidation()
        c.get("nope")
        assert c.stats().miss_count == 1


class TestGetExpired:
    def test_get_expired_returns_none(self):
        c = DocCacheInvalidation()
        c.set("k", "d", "v", ttl=1.0, now=0.0)
        assert c.get("k", now=2.0) is None

    def test_get_expired_removes_entry(self):
        c = DocCacheInvalidation()
        c.set("k", "d", "v", ttl=1.0, now=0.0)
        c.get("k", now=2.0)
        assert c.total_entries == 0

    def test_get_expired_records_event(self):
        c = DocCacheInvalidation()
        c.set("k", "d", "v", ttl=1.0, now=0.0)
        c.get("k", now=2.0)
        events = c.recent_invalidations()
        assert any(e.strategy is InvalidationStrategy.TTL for e in events)

    def test_get_before_expiry(self):
        c = DocCacheInvalidation()
        c.set("k", "d", "v", ttl=10.0, now=0.0)
        assert c.get("k", now=5.0) == "v"


# ------------------------------------------------------------------- delete
class TestDelete:
    def test_delete_existing(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.delete("k") is True

    def test_delete_missing(self):
        c = DocCacheInvalidation()
        assert c.delete("nope") is False

    def test_delete_removes_entry(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.delete("k")
        assert c.get("k") is None

    def test_delete_cleans_indexes(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"t"}, dependencies={"dep"})
        c.delete("k")
        assert c.keys_with_tag("t") == []
        assert c.keys_for_doc("d") == []


# ---------------------------------------------------------------------- has
class TestHas:
    def test_has_existing(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.has("k") is True

    def test_has_missing(self):
        c = DocCacheInvalidation()
        assert c.has("nope") is False

    def test_has_expired(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, ttl=1.0, now=0.0)
        assert c.has("k", now=2.0) is False

    def test_has_not_yet_expired(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, ttl=10.0, now=0.0)
        assert c.has("k", now=5.0) is True

    def test_has_no_ttl(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.has("k", now=1e9) is True


# ---------------------------------------------------------- invalidate_by_doc
class TestInvalidateByDoc:
    def test_removes_keys_for_doc(self):
        c = DocCacheInvalidation()
        c.set("k1", "d1", 1)
        c.set("k2", "d1", 2)
        c.set("k3", "d2", 3)
        n = c.invalidate_by_doc("d1")
        assert n == 2
        assert c.get("k1") is None
        assert c.get("k2") is None
        assert c.get("k3") == 3

    def test_unknown_doc(self):
        c = DocCacheInvalidation()
        c.set("k1", "d1", 1)
        assert c.invalidate_by_doc("nope") == 0

    def test_records_event_with_reason(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.invalidate_by_doc("d", reason="r")
        events = c.recent_invalidations()
        assert events[-1].reason == "r"


# --------------------------------------------------------- invalidate_by_tag
class TestInvalidateByTag:
    def test_removes_tagged(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        c.set("k2", "d", 2, tags={"a", "b"})
        c.set("k3", "d", 3, tags={"b"})
        n = c.invalidate_by_tag("a")
        assert n == 2
        assert c.get("k3") == 3

    def test_unknown_tag(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"x"})
        assert c.invalidate_by_tag("nope") == 0

    def test_strategy_is_tag(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"x"})
        c.invalidate_by_tag("x")
        events = c.recent_invalidations()
        assert events[-1].strategy is InvalidationStrategy.TAG


# ------------------------------------------------------ invalidate_by_tags any
class TestInvalidateByTagsAny:
    def test_any_match(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        c.set("k2", "d", 2, tags={"b"})
        c.set("k3", "d", 3, tags={"c"})
        n = c.invalidate_by_tags({"a", "b"})
        assert n == 2
        assert c.get("k3") == 3

    def test_empty_tags(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        assert c.invalidate_by_tags(set()) == 0

    def test_no_match(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        assert c.invalidate_by_tags({"x"}) == 0


# ------------------------------------------------------ invalidate_by_tags all
class TestInvalidateByTagsAll:
    def test_all_match(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a", "b"})
        c.set("k2", "d", 2, tags={"a"})
        c.set("k3", "d", 3, tags={"a", "b", "c"})
        n = c.invalidate_by_tags({"a", "b"}, match_all=True)
        assert n == 2  # k1 and k3
        assert c.get("k2") == 2

    def test_all_no_match(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        assert c.invalidate_by_tags({"a", "b"}, match_all=True) == 0

    def test_all_with_missing_tag(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        assert c.invalidate_by_tags({"a", "nope"}, match_all=True) == 0


# ----------------------------------------------------- invalidate_by_pattern
class TestInvalidateByPattern:
    def test_prefix(self):
        c = DocCacheInvalidation()
        c.set("user:1", "d", 1)
        c.set("user:2", "d", 2)
        c.set("post:1", "d", 3)
        n = c.invalidate_by_pattern(r"^user:")
        assert n == 2
        assert c.get("post:1") == 3

    def test_suffix(self):
        c = DocCacheInvalidation()
        c.set("a.json", "d", 1)
        c.set("b.json", "d", 2)
        c.set("c.txt", "d", 3)
        n = c.invalidate_by_pattern(r"\.json$")
        assert n == 2

    def test_no_match(self):
        c = DocCacheInvalidation()
        c.set("a", "d", 1)
        assert c.invalidate_by_pattern(r"^z") == 0

    def test_strategy_is_pattern(self):
        c = DocCacheInvalidation()
        c.set("a", "d", 1)
        c.invalidate_by_pattern("a")
        assert c.recent_invalidations()[-1].strategy is InvalidationStrategy.PATTERN

    def test_invalid_regex_raises(self):
        c = DocCacheInvalidation()
        with pytest.raises(re.error if False else Exception):
            import re as _re
            c.invalidate_by_pattern("[")


# --------------------------------------------------- invalidate_dependency
class TestInvalidateDependency:
    def test_invalidates_dependents(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, dependencies={"docX"})
        c.set("k2", "d", 2, dependencies={"docX", "docY"})
        c.set("k3", "d", 3, dependencies={"docY"})
        n = c.invalidate_dependency("docX")
        assert n == 2
        assert c.get("k3") == 3

    def test_unknown_dependency(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.invalidate_dependency("nope") == 0

    def test_strategy_is_dependency(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, dependencies={"x"})
        c.invalidate_dependency("x")
        assert c.recent_invalidations()[-1].strategy is InvalidationStrategy.DEPENDENCY


# ------------------------------------------------------------ invalidate_all
class TestInvalidateAll:
    def test_clears_entries(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1)
        c.set("k2", "d", 2)
        n = c.invalidate_all()
        assert n == 2
        assert c.total_entries == 0

    def test_empty(self):
        c = DocCacheInvalidation()
        assert c.invalidate_all() == 0

    def test_records_event(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.invalidate_all(reason="reset")
        events = c.recent_invalidations()
        assert events[-1].reason == "reset"


# ------------------------------------------------------------ cleanup_expired
class TestCleanupExpired:
    def test_removes_expired(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, ttl=1.0, now=0.0)
        c.set("k2", "d", 2, ttl=10.0, now=0.0)
        n = c.cleanup_expired(now=2.0)
        assert n == 1
        assert c.get("k2", now=2.0) == 2

    def test_nothing_expired(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, ttl=10.0, now=0.0)
        assert c.cleanup_expired(now=5.0) == 0

    def test_skips_entries_without_ttl(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.cleanup_expired(now=1e9) == 0


# ----------------------------------------------------------- add_dependency
class TestAddDependency:
    def test_add_new(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.add_dependency("k", "x") is True
        assert "x" in c.dependencies_of("k")

    def test_add_duplicate(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, dependencies={"x"})
        assert c.add_dependency("k", "x") is False

    def test_add_to_missing_key(self):
        c = DocCacheInvalidation()
        assert c.add_dependency("nope", "x") is False

    def test_indexed_for_invalidation(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.add_dependency("k", "x")
        assert c.invalidate_dependency("x") == 1


# ---------------------------------------------------------------- add_tag
class TestAddTag:
    def test_add_new(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        assert c.add_tag("k", "t") is True
        assert "t" in c.tags_for("k")

    def test_add_duplicate(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"t"})
        assert c.add_tag("k", "t") is False

    def test_add_to_missing_key(self):
        c = DocCacheInvalidation()
        assert c.add_tag("nope", "t") is False

    def test_indexed_for_invalidation(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.add_tag("k", "t")
        assert c.invalidate_by_tag("t") == 1


# ---------------------------------------------------------------- tags_for
class TestTagsFor:
    def test_returns_tags(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"a", "b"})
        assert c.tags_for("k") == {"a", "b"}

    def test_empty_for_missing(self):
        c = DocCacheInvalidation()
        assert c.tags_for("nope") == set()

    def test_returns_copy(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"a"})
        result = c.tags_for("k")
        result.add("hack")
        assert c.tags_for("k") == {"a"}


# ------------------------------------------------------------ dependencies_of
class TestDependenciesOf:
    def test_returns_deps(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, dependencies={"x", "y"})
        assert c.dependencies_of("k") == {"x", "y"}

    def test_empty_for_missing(self):
        c = DocCacheInvalidation()
        assert c.dependencies_of("nope") == set()


# ------------------------------------------------------------- keys_with_tag
class TestKeysWithTag:
    def test_returns_keys(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1, tags={"a"})
        c.set("k2", "d", 2, tags={"a"})
        c.set("k3", "d", 3, tags={"b"})
        assert c.keys_with_tag("a") == ["k1", "k2"]

    def test_empty(self):
        c = DocCacheInvalidation()
        assert c.keys_with_tag("nope") == []


# ------------------------------------------------------------- keys_for_doc
class TestKeysForDoc:
    def test_returns_keys(self):
        c = DocCacheInvalidation()
        c.set("k1", "d1", 1)
        c.set("k2", "d1", 2)
        c.set("k3", "d2", 3)
        assert c.keys_for_doc("d1") == ["k1", "k2"]

    def test_empty(self):
        c = DocCacheInvalidation()
        assert c.keys_for_doc("nope") == []


# ---------------------------------------------------- recent_invalidations
class TestRecentInvalidations:
    def test_empty(self):
        c = DocCacheInvalidation()
        assert c.recent_invalidations() == []

    def test_limit(self):
        c = DocCacheInvalidation()
        for i in range(5):
            c.set(f"k{i}", "d", i)
            c.delete(f"k{i}")
        recent = c.recent_invalidations(limit=2)
        assert len(recent) == 2

    def test_order(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1)
        c.delete("k1")
        c.set("k2", "d", 2)
        c.delete("k2")
        recent = c.recent_invalidations()
        assert recent[-1].keys_invalidated == ["k2"]

    def test_limit_zero(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.delete("k")
        assert c.recent_invalidations(limit=0) == []


# -------------------------------------------------------------------- stats
class TestStats:
    def test_initial(self):
        c = DocCacheInvalidation()
        s = c.stats()
        assert s.total_entries == 0
        assert s.total_invalidations == 0
        assert s.hit_count == 0
        assert s.miss_count == 0

    def test_after_activity(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.get("k")
        c.get("nope")
        c.delete("k")
        s = c.stats()
        assert s.hit_count == 1
        assert s.miss_count == 1
        assert s.total_invalidations == 1


# ------------------------------------------------------------------ hit_rate
class TestHitRate:
    def test_zero_when_no_access(self):
        c = DocCacheInvalidation()
        assert c.stats().hit_rate == 0.0

    def test_all_hits(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.get("k")
        c.get("k")
        assert c.stats().hit_rate == 1.0

    def test_partial(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.get("k")
        c.get("nope")
        assert c.stats().hit_rate == 0.5


# ---------------------------------------------------------------- total_entries
class TestTotalEntries:
    def test_starts_zero(self):
        c = DocCacheInvalidation()
        assert c.total_entries == 0

    def test_increments(self):
        c = DocCacheInvalidation()
        c.set("k1", "d", 1)
        c.set("k2", "d", 2)
        assert c.total_entries == 2

    def test_decrements_on_delete(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.delete("k")
        assert c.total_entries == 0


# ---------------------------------------------------------------------- clear
class TestClear:
    def test_removes_all(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.clear()
        assert c.total_entries == 0

    def test_resets_stats(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.get("k")
        c.get("nope")
        c.clear()
        s = c.stats()
        assert s.hit_count == 0
        assert s.miss_count == 0
        assert s.total_invalidations == 0

    def test_resets_events(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1)
        c.delete("k")
        c.clear()
        assert c.recent_invalidations() == []


# ------------------------------------------------------------- edge cases
class TestEdgeCases:
    def test_set_none_value(self):
        c = DocCacheInvalidation()
        c.set("k", "d", None)
        assert c.has("k") is True
        # has() should remain True even when value is None
        # but get() returns None — same as missing.  This is acceptable.

    def test_set_zero_ttl_immediately_expired(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, ttl=0.0, now=0.0)
        # expires_at = 0.0, now=0.0 => now >= expires => expired
        assert c.has("k", now=0.0) is False

    def test_pattern_matches_substring(self):
        c = DocCacheInvalidation()
        c.set("abc", "d", 1)
        c.set("xbcy", "d", 2)
        n = c.invalidate_by_pattern("bc")
        assert n == 2

    def test_invalidate_by_doc_cleans_tag_index(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"t"})
        c.invalidate_by_doc("d")
        assert c.keys_with_tag("t") == []

    def test_invalidate_by_tag_cleans_doc_index(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, tags={"t"})
        c.invalidate_by_tag("t")
        assert c.keys_for_doc("d") == []

    def test_overwrite_resets_ttl(self):
        c = DocCacheInvalidation()
        c.set("k", "d", 1, ttl=1.0, now=0.0)
        c.set("k", "d", 2, ttl=100.0, now=0.0)
        assert c.get("k", now=10.0) == 2

    def test_many_entries(self):
        c = DocCacheInvalidation()
        for i in range(50):
            c.set(f"k{i}", f"doc{i % 5}", i)
        assert c.total_entries == 50
        # Each doc bucket should have 10 keys
        assert len(c.keys_for_doc("doc0")) == 10

    def test_threading_lock_exists(self):
        c = DocCacheInvalidation()
        assert hasattr(c, "_lock")
