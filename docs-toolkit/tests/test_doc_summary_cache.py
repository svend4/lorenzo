"""Tests for E401 DocSummaryCache."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_summary_cache import (
    CacheStats,
    DocSummaryCache,
    SummaryEntry,
)


# ---------------------------------------------------------------- dataclasses


class TestSummaryEntryDataclass:
    def test_required_fields(self):
        e = SummaryEntry(doc_id="d1", version="v1", summary="s")
        assert e.doc_id == "d1"
        assert e.version == "v1"
        assert e.summary == "s"

    def test_defaults(self):
        e = SummaryEntry(doc_id="d1", version="v1", summary="s")
        assert e.cached_at == 0.0
        assert e.hit_count == 0
        assert e.length == 0

    def test_custom_values(self):
        e = SummaryEntry(
            doc_id="d", version="v", summary="abc",
            cached_at=10.0, hit_count=3, length=3,
        )
        assert e.cached_at == 10.0
        assert e.hit_count == 3
        assert e.length == 3

    def test_mutability(self):
        e = SummaryEntry(doc_id="d", version="v", summary="s")
        e.hit_count += 1
        assert e.hit_count == 1

    def test_equality(self):
        a = SummaryEntry(doc_id="d", version="v", summary="s")
        b = SummaryEntry(doc_id="d", version="v", summary="s")
        assert a == b


class TestCacheStatsDataclass:
    def test_defaults(self):
        s = CacheStats()
        assert s.total_entries == 0
        assert s.unique_docs == 0
        assert s.total_hits == 0
        assert s.total_chars == 0

    def test_custom(self):
        s = CacheStats(total_entries=2, unique_docs=1, total_hits=5, total_chars=10)
        assert s.total_entries == 2
        assert s.unique_docs == 1
        assert s.total_hits == 5
        assert s.total_chars == 10

    def test_equality(self):
        a = CacheStats(1, 1, 1, 1)
        b = CacheStats(1, 1, 1, 1)
        assert a == b


# ---------------------------------------------------------------- construction


class TestConstruction:
    def test_empty_on_init(self):
        c = DocSummaryCache()
        assert c.stats().total_entries == 0

    def test_no_doc_ids(self):
        c = DocSummaryCache()
        assert c.all_doc_ids() == []

    def test_independent_instances(self):
        a = DocSummaryCache()
        b = DocSummaryCache()
        a.store("d", "v", "hello")
        assert b.stats().total_entries == 0


# ---------------------------------------------------------------- store


class TestStore:
    def test_store_new(self):
        c = DocSummaryCache()
        e = c.store("d", "v", "hello")
        assert e.summary == "hello"
        assert c.exists("d", "v")

    def test_store_length_computed(self):
        c = DocSummaryCache()
        e = c.store("d", "v", "hello")
        assert e.length == 5

    def test_store_empty_summary(self):
        c = DocSummaryCache()
        e = c.store("d", "v", "")
        assert e.length == 0

    def test_store_uses_now(self):
        c = DocSummaryCache()
        e = c.store("d", "v", "x", now=123.0)
        assert e.cached_at == 123.0

    def test_store_default_now_is_set(self):
        c = DocSummaryCache()
        e = c.store("d", "v", "x")
        assert e.cached_at > 0

    def test_store_replace(self):
        c = DocSummaryCache()
        c.store("d", "v", "first")
        c.store("d", "v", "second")
        assert c.peek("d", "v").summary == "second"

    def test_store_replace_resets_hits(self):
        c = DocSummaryCache()
        c.store("d", "v", "first")
        c.get("d", "v")
        c.get("d", "v")
        c.store("d", "v", "second")
        assert c.peek("d", "v").hit_count == 0

    def test_store_multiple_versions(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        assert c.exists("d", "v1")
        assert c.exists("d", "v2")

    def test_store_different_docs(self):
        c = DocSummaryCache()
        c.store("d1", "v", "a")
        c.store("d2", "v", "b")
        assert c.stats().unique_docs == 2


# ---------------------------------------------------------------- get


class TestGet:
    def test_get_returns_summary(self):
        c = DocSummaryCache()
        c.store("d", "v", "hello")
        assert c.get("d", "v") == "hello"

    def test_get_missing_returns_none(self):
        c = DocSummaryCache()
        assert c.get("d", "v") is None

    def test_get_increments_hit_count(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        c.get("d", "v")
        assert c.peek("d", "v").hit_count == 1

    def test_get_multiple_increments(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        for _ in range(5):
            c.get("d", "v")
        assert c.peek("d", "v").hit_count == 5

    def test_get_missing_does_not_create(self):
        c = DocSummaryCache()
        c.get("d", "v")
        assert c.stats().total_entries == 0


# ---------------------------------------------------------------- peek


class TestPeek:
    def test_peek_returns_entry(self):
        c = DocSummaryCache()
        c.store("d", "v", "hi")
        e = c.peek("d", "v")
        assert isinstance(e, SummaryEntry)
        assert e.summary == "hi"

    def test_peek_does_not_increment_hit_count(self):
        c = DocSummaryCache()
        c.store("d", "v", "hi")
        c.peek("d", "v")
        c.peek("d", "v")
        assert c.peek("d", "v").hit_count == 0

    def test_peek_missing_returns_none(self):
        c = DocSummaryCache()
        assert c.peek("d", "v") is None


# ---------------------------------------------------------------- exists


class TestExists:
    def test_exists_true(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        assert c.exists("d", "v") is True

    def test_exists_false(self):
        c = DocSummaryCache()
        assert c.exists("d", "v") is False

    def test_exists_other_version_false(self):
        c = DocSummaryCache()
        c.store("d", "v1", "x")
        assert c.exists("d", "v2") is False


# ---------------------------------------------------------------- delete


class TestDelete:
    def test_delete_existing(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        assert c.delete("d", "v") is True
        assert not c.exists("d", "v")

    def test_delete_missing(self):
        c = DocSummaryCache()
        assert c.delete("d", "v") is False

    def test_delete_removes_from_by_doc(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        c.delete("d", "v")
        assert c.versions_for("d") == []

    def test_delete_one_of_many(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        c.delete("d", "v1")
        assert c.versions_for("d") == ["v2"]


# ---------------------------------------------------------------- delete_doc


class TestDeleteDoc:
    def test_delete_doc_count(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        c.store("d", "v3", "c")
        assert c.delete_doc("d") == 3

    def test_delete_doc_missing(self):
        c = DocSummaryCache()
        assert c.delete_doc("d") == 0

    def test_delete_doc_removes_all(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        c.delete_doc("d")
        assert c.versions_for("d") == []
        assert "d" not in c.all_doc_ids()

    def test_delete_doc_leaves_others(self):
        c = DocSummaryCache()
        c.store("d1", "v", "a")
        c.store("d2", "v", "b")
        c.delete_doc("d1")
        assert c.exists("d2", "v")


# ---------------------------------------------------------------- versions_for


class TestVersionsFor:
    def test_versions_sorted(self):
        c = DocSummaryCache()
        c.store("d", "v3", "a")
        c.store("d", "v1", "b")
        c.store("d", "v2", "c")
        assert c.versions_for("d") == ["v1", "v2", "v3"]

    def test_versions_missing_doc(self):
        c = DocSummaryCache()
        assert c.versions_for("nope") == []

    def test_versions_single(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        assert c.versions_for("d") == ["v"]


# ---------------------------------------------------------------- latest_version_for


class TestLatestVersionFor:
    def test_latest_by_cached_at(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a", now=1.0)
        c.store("d", "v2", "b", now=3.0)
        c.store("d", "v3", "c", now=2.0)
        assert c.latest_version_for("d") == "v2"

    def test_latest_missing_doc(self):
        c = DocSummaryCache()
        assert c.latest_version_for("d") is None

    def test_latest_single(self):
        c = DocSummaryCache()
        c.store("d", "v", "x", now=5.0)
        assert c.latest_version_for("d") == "v"


# ---------------------------------------------------------------- top_accessed


class TestTopAccessed:
    def test_sorted_desc_by_hits(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        c.store("d", "v3", "c")
        for _ in range(3):
            c.get("d", "v2")
        c.get("d", "v3")
        top = c.top_accessed()
        assert top[0].version == "v2"
        assert top[1].version == "v3"

    def test_limit(self):
        c = DocSummaryCache()
        for i in range(10):
            c.store("d", f"v{i}", "x")
            for _ in range(i):
                c.get("d", f"v{i}")
        top = c.top_accessed(limit=3)
        assert len(top) == 3
        assert top[0].hit_count == 9

    def test_empty(self):
        c = DocSummaryCache()
        assert c.top_accessed() == []

    def test_negative_limit(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        assert c.top_accessed(limit=-1) == []


# ---------------------------------------------------------------- total_size_for


class TestTotalSizeFor:
    def test_sums_lengths(self):
        c = DocSummaryCache()
        c.store("d", "v1", "hello")  # 5
        c.store("d", "v2", "hi")     # 2
        assert c.total_size_for("d") == 7

    def test_missing_doc_zero(self):
        c = DocSummaryCache()
        assert c.total_size_for("d") == 0

    def test_single_version(self):
        c = DocSummaryCache()
        c.store("d", "v", "abc")
        assert c.total_size_for("d") == 3


# ---------------------------------------------------------------- clear


class TestClear:
    def test_clear_count(self):
        c = DocSummaryCache()
        c.store("d1", "v", "a")
        c.store("d2", "v", "b")
        assert c.clear() == 2

    def test_clear_empties(self):
        c = DocSummaryCache()
        c.store("d", "v", "a")
        c.clear()
        assert c.stats().total_entries == 0
        assert c.all_doc_ids() == []

    def test_clear_empty(self):
        c = DocSummaryCache()
        assert c.clear() == 0


# ---------------------------------------------------------------- all_doc_ids


class TestAllDocIds:
    def test_sorted(self):
        c = DocSummaryCache()
        c.store("zeta", "v", "x")
        c.store("alpha", "v", "x")
        c.store("mu", "v", "x")
        assert c.all_doc_ids() == ["alpha", "mu", "zeta"]

    def test_empty(self):
        c = DocSummaryCache()
        assert c.all_doc_ids() == []

    def test_unique(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        assert c.all_doc_ids() == ["d"]


# ---------------------------------------------------------------- stats


class TestStats:
    def test_empty(self):
        c = DocSummaryCache()
        s = c.stats()
        assert s == CacheStats(0, 0, 0, 0)

    def test_total_entries(self):
        c = DocSummaryCache()
        c.store("d", "v1", "a")
        c.store("d", "v2", "b")
        assert c.stats().total_entries == 2

    def test_unique_docs(self):
        c = DocSummaryCache()
        c.store("d1", "v", "a")
        c.store("d2", "v", "b")
        c.store("d1", "v2", "c")
        assert c.stats().unique_docs == 2

    def test_total_hits(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        c.get("d", "v")
        c.get("d", "v")
        assert c.stats().total_hits == 2

    def test_total_chars(self):
        c = DocSummaryCache()
        c.store("d", "v1", "hello")
        c.store("d", "v2", "hi")
        assert c.stats().total_chars == 7


# ---------------------------------------------------------------- thread safety


class TestThreadSafety:
    def test_concurrent_store(self):
        c = DocSummaryCache()
        N = 50
        threads = []

        def worker(i):
            c.store(f"d{i}", "v", f"summary-{i}")

        for i in range(N):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        assert c.stats().total_entries == N
        assert c.stats().unique_docs == N

    def test_concurrent_get(self):
        c = DocSummaryCache()
        c.store("d", "v", "x")
        N = 100
        threads = []

        def worker():
            c.get("d", "v")

        for _ in range(N):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        assert c.peek("d", "v").hit_count == N

    def test_concurrent_store_same_key(self):
        c = DocSummaryCache()
        N = 30
        threads = []

        def worker(i):
            c.store("d", "v", f"value-{i}")

        for i in range(N):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        assert c.exists("d", "v")
        assert c.stats().total_entries == 1


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
