"""Tests for docstoolkit.cache_invalidation — TaggedCache with TTL and tag invalidation."""
from __future__ import annotations

import sys
import threading
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.cache_invalidation import CacheEntry, TaggedCache


# ===========================================================================
# Helpers
# ===========================================================================

def make_cache(start: float = 1000.0) -> tuple[TaggedCache, list[float]]:
    """Return a (cache, clock) pair where clock[0] is the virtual time."""
    clock = [start]
    return TaggedCache(now_fn=lambda: clock[0]), clock


# ===========================================================================
# CacheEntry dataclass
# ===========================================================================

class TestCacheEntry:
    def test_default_tags_is_frozenset(self):
        e = CacheEntry(key="k", value=1)
        assert isinstance(e.tags, frozenset)
        assert e.tags == frozenset()

    def test_default_ttl_is_none(self):
        e = CacheEntry(key="k", value=1)
        assert e.ttl is None

    def test_default_created_at_is_zero(self):
        e = CacheEntry(key="k", value=1)
        assert e.created_at == 0.0

    def test_explicit_fields(self):
        e = CacheEntry(
            key="x",
            value={"a": 1},
            tags=frozenset({"t1", "t2"}),
            created_at=500.0,
            ttl=60.0,
        )
        assert e.key == "x"
        assert e.value == {"a": 1}
        assert e.tags == frozenset({"t1", "t2"})
        assert e.created_at == 500.0
        assert e.ttl == 60.0


# ===========================================================================
# Basic set / get / delete
# ===========================================================================

class TestBasicOps:
    def test_get_missing_returns_none(self):
        c, _ = make_cache()
        assert c.get("missing") is None

    def test_get_missing_returns_default(self):
        c, _ = make_cache()
        assert c.get("missing", default="fallback") == "fallback"

    def test_set_and_get(self):
        c, _ = make_cache()
        c.set("k", 42)
        assert c.get("k") == 42

    def test_set_overwrite(self):
        c, _ = make_cache()
        c.set("k", "first")
        c.set("k", "second")
        assert c.get("k") == "second"

    def test_set_none_value(self):
        c, _ = make_cache()
        c.set("k", None)
        # None is a valid value; key should exist
        assert c.exists("k")

    def test_delete_existing_returns_true(self):
        c, _ = make_cache()
        c.set("k", 1)
        assert c.delete("k") is True

    def test_delete_removes_entry(self):
        c, _ = make_cache()
        c.set("k", 1)
        c.delete("k")
        assert c.get("k") is None

    def test_delete_missing_returns_false(self):
        c, _ = make_cache()
        assert c.delete("absent") is False

    def test_get_returns_correct_type(self):
        c, _ = make_cache()
        c.set("lst", [1, 2, 3])
        assert c.get("lst") == [1, 2, 3]

    def test_set_complex_value(self):
        c, _ = make_cache()
        val = {"nested": {"a": [1, 2]}, "flag": True}
        c.set("k", val)
        assert c.get("k") == val


# ===========================================================================
# Entry without tags
# ===========================================================================

class TestNoTags:
    def test_entry_without_tags_stored(self):
        c, _ = make_cache()
        c.set("k", "hello")
        assert c.get("k") == "hello"

    def test_entry_without_tags_not_in_tag_index(self):
        c, _ = make_cache()
        c.set("k", "v")
        assert c.keys_for_tag("any_tag") == []

    def test_invalidate_tag_does_not_remove_untagged(self):
        c, _ = make_cache()
        c.set("k", "v")
        c.invalidate_tag("nonexistent")
        assert c.get("k") == "v"

    def test_get_entry_no_tags(self):
        c, _ = make_cache()
        c.set("k", 99)
        entry = c.get_entry("k")
        assert entry is not None
        assert entry.tags == frozenset()


# ===========================================================================
# TTL expiry (virtual clock — no sleep)
# ===========================================================================

class TestTTL:
    def test_entry_alive_within_ttl(self):
        c, clock = make_cache(start=1000.0)
        c.set("k", "v", ttl=60.0)
        clock[0] = 1059.9  # just before expiry
        assert c.get("k") == "v"

    def test_entry_expired_after_ttl(self):
        c, clock = make_cache(start=1000.0)
        c.set("k", "v", ttl=60.0)
        clock[0] = 1060.1  # just past expiry
        assert c.get("k") is None

    def test_exact_boundary_is_expired(self):
        # Spec: expired if now > created_at + ttl  (strictly greater)
        c, clock = make_cache(start=1000.0)
        c.set("k", "v", ttl=60.0)
        clock[0] = 1060.0  # exactly at expiry boundary → NOT expired
        assert c.get("k") == "v"

    def test_expired_returns_default(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=10.0)
        clock[0] = 11.0
        assert c.get("k", default="gone") == "gone"

    def test_no_ttl_never_expires(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v")  # no ttl
        clock[0] = 1_000_000.0
        assert c.get("k") == "v"

    def test_zero_ttl_expires_immediately(self):
        c, clock = make_cache(start=1000.0)
        c.set("k", "v", ttl=0.0)
        clock[0] = 1000.1
        assert c.get("k") is None

    def test_exists_false_on_expired(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=5.0)
        clock[0] = 6.0
        assert c.exists("k") is False

    def test_exists_true_within_ttl(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=100.0)
        clock[0] = 50.0
        assert c.exists("k") is True

    def test_expired_entry_removed_on_get(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=5.0)
        clock[0] = 10.0
        c.get("k")  # triggers lazy eviction
        assert c.size() == 0

    def test_overwrite_resets_ttl(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "old", ttl=10.0)
        clock[0] = 8.0
        c.set("k", "new", ttl=100.0)  # fresh TTL from t=8
        clock[0] = 15.0  # original would have expired, new should not
        assert c.get("k") == "new"

    def test_get_entry_returns_none_on_expired(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=5.0)
        clock[0] = 6.0
        assert c.get_entry("k") is None


# ===========================================================================
# exists / keys / size / clear
# ===========================================================================

class TestExistsKeysSizeClear:
    def test_exists_true_after_set(self):
        c, _ = make_cache()
        c.set("k", 1)
        assert c.exists("k") is True

    def test_exists_false_after_delete(self):
        c, _ = make_cache()
        c.set("k", 1)
        c.delete("k")
        assert c.exists("k") is False

    def test_exists_false_when_empty(self):
        c, _ = make_cache()
        assert c.exists("x") is False

    def test_keys_empty(self):
        c, _ = make_cache()
        assert c.keys() == []

    def test_keys_lists_all_keys(self):
        c, _ = make_cache()
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)
        assert sorted(c.keys()) == ["a", "b", "c"]

    def test_keys_excludes_expired(self):
        c, clock = make_cache(start=0.0)
        c.set("alive", 1, ttl=100.0)
        c.set("dead", 2, ttl=5.0)
        clock[0] = 10.0
        assert c.keys() == ["alive"]

    def test_size_zero_initially(self):
        c, _ = make_cache()
        assert c.size() == 0

    def test_size_after_set(self):
        c, _ = make_cache()
        c.set("a", 1)
        c.set("b", 2)
        assert c.size() == 2

    def test_size_after_delete(self):
        c, _ = make_cache()
        c.set("a", 1)
        c.set("b", 2)
        c.delete("a")
        assert c.size() == 1

    def test_size_excludes_expired(self):
        c, clock = make_cache(start=0.0)
        c.set("alive", 1, ttl=100.0)
        c.set("dead", 2, ttl=5.0)
        clock[0] = 10.0
        assert c.size() == 1

    def test_clear_removes_all(self):
        c, _ = make_cache()
        c.set("a", 1)
        c.set("b", 2)
        c.clear()
        assert c.size() == 0
        assert c.keys() == []

    def test_clear_resets_tag_index(self):
        c, _ = make_cache()
        c.set("k", 1, tags={"t"})
        c.clear()
        assert c.keys_for_tag("t") == []

    def test_get_after_clear_returns_none(self):
        c, _ = make_cache()
        c.set("k", 99)
        c.clear()
        assert c.get("k") is None


# ===========================================================================
# get_entry
# ===========================================================================

class TestGetEntry:
    def test_returns_none_on_missing(self):
        c, _ = make_cache()
        assert c.get_entry("absent") is None

    def test_returns_cache_entry(self):
        c, _ = make_cache(start=500.0)
        c.set("k", "hello", tags={"a", "b"}, ttl=30.0)
        entry = c.get_entry("k")
        assert entry is not None
        assert isinstance(entry, CacheEntry)

    def test_entry_key_correct(self):
        c, _ = make_cache()
        c.set("mykey", "v")
        assert c.get_entry("mykey").key == "mykey"  # type: ignore[union-attr]

    def test_entry_value_correct(self):
        c, _ = make_cache()
        c.set("k", [1, 2, 3])
        assert c.get_entry("k").value == [1, 2, 3]  # type: ignore[union-attr]

    def test_entry_tags_correct(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"x", "y"})
        entry = c.get_entry("k")
        assert entry is not None
        assert entry.tags == frozenset({"x", "y"})

    def test_entry_ttl_correct(self):
        c, _ = make_cache()
        c.set("k", "v", ttl=99.0)
        entry = c.get_entry("k")
        assert entry is not None
        assert entry.ttl == 99.0

    def test_entry_created_at_matches_clock(self):
        c, clock = make_cache(start=750.0)
        c.set("k", "v")
        entry = c.get_entry("k")
        assert entry is not None
        assert entry.created_at == 750.0

    def test_returns_none_on_expired(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=10.0)
        clock[0] = 11.0
        assert c.get_entry("k") is None


# ===========================================================================
# invalidate_tag
# ===========================================================================

class TestInvalidateTag:
    def test_returns_zero_for_unknown_tag(self):
        c, _ = make_cache()
        assert c.invalidate_tag("ghost") == 0

    def test_returns_count_of_removed(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t"})
        c.set("b", 2, tags={"t"})
        c.set("c", 3, tags={"t"})
        assert c.invalidate_tag("t") == 3

    def test_tagged_entries_removed(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t"})
        c.set("b", 2, tags={"t"})
        c.invalidate_tag("t")
        assert c.get("a") is None
        assert c.get("b") is None

    def test_untagged_entries_survive(self):
        c, _ = make_cache()
        c.set("tagged", 1, tags={"t"})
        c.set("untagged", 2)
        c.invalidate_tag("t")
        assert c.get("untagged") == 2

    def test_differently_tagged_entries_survive(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t1"})
        c.set("b", 2, tags={"t2"})
        c.invalidate_tag("t1")
        assert c.get("b") == 2

    def test_entry_with_multiple_tags_removed_by_one(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t1", "t2", "t3"})
        c.invalidate_tag("t2")
        assert c.get("k") is None

    def test_tag_index_cleaned_up_after_invalidation(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t"})
        c.invalidate_tag("t")
        assert c.keys_for_tag("t") == []

    def test_invalidate_same_tag_twice_is_idempotent(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t"})
        c.invalidate_tag("t")
        assert c.invalidate_tag("t") == 0  # already gone

    def test_tag_shared_across_multiple_keys(self):
        c, _ = make_cache()
        for i in range(5):
            c.set(f"key{i}", i, tags={"shared"})
        removed = c.invalidate_tag("shared")
        assert removed == 5
        assert c.size() == 0


# ===========================================================================
# invalidate_tags (multiple tags, union semantics)
# ===========================================================================

class TestInvalidateTags:
    def test_returns_zero_for_no_matches(self):
        c, _ = make_cache()
        assert c.invalidate_tags({"x", "y"}) == 0

    def test_removes_entries_matching_any_tag(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t1"})
        c.set("b", 2, tags={"t2"})
        c.set("c", 3, tags={"t3"})
        removed = c.invalidate_tags({"t1", "t2"})
        assert removed == 2
        assert c.get("a") is None
        assert c.get("b") is None
        assert c.get("c") == 3

    def test_entry_with_two_matching_tags_counted_once(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t1", "t2"})
        removed = c.invalidate_tags({"t1", "t2"})
        assert removed == 1  # entry removed once, not twice

    def test_empty_set_removes_nothing(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t"})
        assert c.invalidate_tags(set()) == 0
        assert c.get("k") == "v"

    def test_union_semantics_across_three_tags(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t1"})
        c.set("b", 2, tags={"t2"})
        c.set("c", 3, tags={"t3"})
        c.set("d", 4, tags={"other"})
        removed = c.invalidate_tags({"t1", "t2", "t3"})
        assert removed == 3
        assert c.size() == 1
        assert c.get("d") == 4

    def test_surviving_entries_intact_after_partial_invalidation(self):
        c, _ = make_cache()
        c.set("keep", 100, tags={"safe"})
        c.set("remove", 200, tags={"danger"})
        c.invalidate_tags({"danger"})
        entry = c.get_entry("keep")
        assert entry is not None
        assert entry.value == 100


# ===========================================================================
# keys_for_tag
# ===========================================================================

class TestKeysForTag:
    def test_empty_for_unknown_tag(self):
        c, _ = make_cache()
        assert c.keys_for_tag("ghost") == []

    def test_returns_keys_for_tag(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t"})
        c.set("b", 2, tags={"t"})
        assert sorted(c.keys_for_tag("t")) == ["a", "b"]

    def test_excludes_keys_without_tag(self):
        c, _ = make_cache()
        c.set("a", 1, tags={"t"})
        c.set("b", 2, tags={"other"})
        assert c.keys_for_tag("t") == ["a"]

    def test_excludes_expired_keys(self):
        c, clock = make_cache(start=0.0)
        c.set("alive", 1, tags={"t"}, ttl=100.0)
        c.set("dead", 2, tags={"t"}, ttl=5.0)
        clock[0] = 10.0
        assert c.keys_for_tag("t") == ["alive"]

    def test_empty_after_all_tagged_deleted(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t"})
        c.delete("k")
        assert c.keys_for_tag("t") == []

    def test_key_with_multiple_tags_appears_in_each(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"t1", "t2"})
        assert c.keys_for_tag("t1") == ["k"]
        assert c.keys_for_tag("t2") == ["k"]


# ===========================================================================
# purge_expired
# ===========================================================================

class TestPurgeExpired:
    def test_returns_zero_when_nothing_expired(self):
        c, _ = make_cache()
        c.set("k", "v", ttl=9999.0)
        assert c.purge_expired() == 0

    def test_returns_count_of_purged(self):
        c, clock = make_cache(start=0.0)
        c.set("a", 1, ttl=5.0)
        c.set("b", 2, ttl=5.0)
        c.set("c", 3, ttl=100.0)
        clock[0] = 10.0
        assert c.purge_expired() == 2

    def test_expired_entries_removed(self):
        c, clock = make_cache(start=0.0)
        c.set("a", 1, ttl=5.0)
        clock[0] = 10.0
        c.purge_expired()
        assert c.get("a") is None

    def test_non_expired_entries_survive(self):
        c, clock = make_cache(start=0.0)
        c.set("alive", "yes", ttl=100.0)
        c.set("dead", "no", ttl=5.0)
        clock[0] = 10.0
        c.purge_expired()
        assert c.get("alive") == "yes"

    def test_entries_without_ttl_not_purged(self):
        c, clock = make_cache(start=0.0)
        c.set("eternal", "lives")
        clock[0] = 1_000_000.0
        assert c.purge_expired() == 0
        assert c.get("eternal") == "lives"

    def test_purge_cleans_tag_index(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", tags={"t"}, ttl=5.0)
        clock[0] = 10.0
        c.purge_expired()
        assert c.keys_for_tag("t") == []

    def test_double_purge_is_idempotent(self):
        c, clock = make_cache(start=0.0)
        c.set("k", "v", ttl=5.0)
        clock[0] = 10.0
        c.purge_expired()
        assert c.purge_expired() == 0  # nothing left to purge


# ===========================================================================
# Entry with multiple tags
# ===========================================================================

class TestMultipleTags:
    def test_entry_reachable_from_all_tags(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"a", "b", "c"})
        assert "k" in c.keys_for_tag("a")
        assert "k" in c.keys_for_tag("b")
        assert "k" in c.keys_for_tag("c")

    def test_invalidating_one_tag_removes_from_all_indices(self):
        c, _ = make_cache()
        c.set("k", "v", tags={"a", "b"})
        c.invalidate_tag("a")
        assert c.keys_for_tag("b") == []

    def test_overwrite_updates_tag_index(self):
        c, _ = make_cache()
        c.set("k", "v1", tags={"old"})
        c.set("k", "v2", tags={"new"})
        assert c.keys_for_tag("old") == []
        assert "k" in c.keys_for_tag("new")


# ===========================================================================
# Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_set_does_not_corrupt(self):
        """Many threads writing distinct keys should all be readable afterwards."""
        c, _ = make_cache()
        errors: list[str] = []

        def worker(tid: int) -> None:
            for i in range(50):
                key = f"t{tid}_k{i}"
                c.set(key, tid * 1000 + i, tags={f"thread-{tid}"})

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert c.size() == 500
        if errors:
            pytest.fail("\n".join(errors))

    def test_concurrent_invalidate_does_not_raise(self):
        """Invalidating a tag while other threads set entries should not crash."""
        c, _ = make_cache()
        stop = threading.Event()

        def writer() -> None:
            i = 0
            while not stop.is_set():
                c.set(f"w{i}", i, tags={"shared"})
                i += 1

        def invalidator() -> None:
            for _ in range(200):
                c.invalidate_tag("shared")

        w = threading.Thread(target=writer)
        inv = threading.Thread(target=invalidator)
        w.start()
        inv.start()
        inv.join()
        stop.set()
        w.join()
        # No assertion on final state — we just want no exception/deadlock.

    def test_concurrent_get_and_delete(self):
        """Simultaneous reads and deletes of the same key should not raise."""
        c, _ = make_cache()
        for i in range(100):
            c.set(f"k{i}", i)

        exceptions: list[Exception] = []

        def reader() -> None:
            for i in range(100):
                try:
                    c.get(f"k{i}")
                except Exception as exc:  # noqa: BLE001
                    exceptions.append(exc)

        def deleter() -> None:
            for i in range(100):
                try:
                    c.delete(f"k{i}")
                except Exception as exc:  # noqa: BLE001
                    exceptions.append(exc)

        t1 = threading.Thread(target=reader)
        t2 = threading.Thread(target=deleter)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert exceptions == []
