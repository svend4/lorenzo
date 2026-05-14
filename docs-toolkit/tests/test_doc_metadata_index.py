"""Tests for ``docstoolkit.doc_metadata_index``."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_metadata_index import (
    DocMetadataIndex,
    MetaEntry,
    MetaStats,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def index() -> DocMetadataIndex:
    return DocMetadataIndex()


@pytest.fixture
def populated_index() -> DocMetadataIndex:
    """Three docs with overlapping metadata."""
    idx = DocMetadataIndex()
    idx.set_meta("d1", "author", "alice", now=1.0)
    idx.set_meta("d1", "lang", "en", now=1.0)
    idx.set_meta("d2", "author", "alice", now=2.0)
    idx.set_meta("d2", "lang", "ru", now=2.0)
    idx.set_meta("d3", "author", "bob", now=3.0)
    idx.set_meta("d3", "lang", "en", now=3.0)
    return idx


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestMetaEntryDataclass:
    def test_construct_with_all_fields(self) -> None:
        e = MetaEntry(doc_id="d1", key="k", value="v", updated_at=1.5)
        assert e.doc_id == "d1"
        assert e.key == "k"
        assert e.value == "v"
        assert e.updated_at == 1.5

    def test_default_updated_at_zero(self) -> None:
        e = MetaEntry(doc_id="d", key="k", value="v")
        assert e.updated_at == 0.0

    def test_equality(self) -> None:
        a = MetaEntry("d", "k", "v", 1.0)
        b = MetaEntry("d", "k", "v", 1.0)
        assert a == b

    def test_inequality_on_value(self) -> None:
        a = MetaEntry("d", "k", "v1", 1.0)
        b = MetaEntry("d", "k", "v2", 1.0)
        assert a != b


class TestMetaStatsDataclass:
    def test_construct(self) -> None:
        s = MetaStats(total_entries=10, unique_docs=3, unique_keys=4)
        assert s.total_entries == 10
        assert s.unique_docs == 3
        assert s.unique_keys == 4

    def test_equality(self) -> None:
        assert MetaStats(1, 1, 1) == MetaStats(1, 1, 1)

    def test_inequality(self) -> None:
        assert MetaStats(1, 1, 1) != MetaStats(2, 1, 1)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_index(self, index: DocMetadataIndex) -> None:
        assert index.all_keys() == []
        assert index.all_doc_ids() == []

    def test_initial_stats(self, index: DocMetadataIndex) -> None:
        stats = index.stats()
        assert stats == MetaStats(total_entries=0, unique_docs=0, unique_keys=0)

    def test_independent_instances(self) -> None:
        a = DocMetadataIndex()
        b = DocMetadataIndex()
        a.set_meta("d", "k", "v")
        assert b.get_meta("d", "k") is None


# ---------------------------------------------------------------------------
# set_meta
# ---------------------------------------------------------------------------


class TestSetMeta:
    def test_returns_meta_entry(self, index: DocMetadataIndex) -> None:
        e = index.set_meta("d1", "author", "alice", now=1.0)
        assert isinstance(e, MetaEntry)
        assert e.doc_id == "d1"
        assert e.key == "author"
        assert e.value == "alice"
        assert e.updated_at == 1.0

    def test_creates_new_entry(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "author", "alice")
        assert index.get_meta("d1", "author") == "alice"

    def test_replace_overwrites_value(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "author", "alice", now=1.0)
        index.set_meta("d1", "author", "bob", now=2.0)
        assert index.get_meta("d1", "author") == "bob"

    def test_replace_updates_timestamp(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "author", "alice", now=1.0)
        index.set_meta("d1", "author", "bob", now=2.0)
        entry = index.get_entry("d1", "author")
        assert entry is not None
        assert entry.updated_at == 2.0

    def test_replace_updates_inverted_index(
        self, index: DocMetadataIndex
    ) -> None:
        index.set_meta("d1", "author", "alice")
        index.set_meta("d1", "author", "bob")
        # The old value bucket must be gone.
        assert index.docs_with("author", "alice") == []
        assert index.docs_with("author", "bob") == ["d1"]

    def test_replace_keeps_by_doc(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "author", "alice")
        index.set_meta("d1", "author", "bob")
        assert index.meta_for_doc("d1") == {"author": "bob"}

    def test_multiple_keys_same_doc(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "author", "alice")
        index.set_meta("d1", "lang", "en")
        assert index.meta_for_doc("d1") == {"author": "alice", "lang": "en"}

    def test_multiple_docs_same_key(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "author", "alice")
        index.set_meta("d2", "author", "alice")
        assert sorted(index.docs_with("author", "alice")) == ["d1", "d2"]

    def test_now_none_uses_time_time(self, index: DocMetadataIndex) -> None:
        import time

        before = time.time()
        e = index.set_meta("d1", "k", "v")
        after = time.time()
        assert before <= e.updated_at <= after

    def test_now_explicit_zero(self, index: DocMetadataIndex) -> None:
        e = index.set_meta("d1", "k", "v", now=0.0)
        assert e.updated_at == 0.0


# ---------------------------------------------------------------------------
# get_meta
# ---------------------------------------------------------------------------


class TestGetMeta:
    def test_missing_returns_none(self, index: DocMetadataIndex) -> None:
        assert index.get_meta("nope", "k") is None

    def test_returns_value(self, populated_index: DocMetadataIndex) -> None:
        assert populated_index.get_meta("d1", "author") == "alice"

    def test_wrong_doc(self, populated_index: DocMetadataIndex) -> None:
        assert populated_index.get_meta("dX", "author") is None

    def test_wrong_key(self, populated_index: DocMetadataIndex) -> None:
        assert populated_index.get_meta("d1", "unknown") is None


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------


class TestGetEntry:
    def test_missing_returns_none(self, index: DocMetadataIndex) -> None:
        assert index.get_entry("d", "k") is None

    def test_returns_full_entry(
        self, populated_index: DocMetadataIndex
    ) -> None:
        e = populated_index.get_entry("d1", "author")
        assert e == MetaEntry(
            doc_id="d1", key="author", value="alice", updated_at=1.0
        )

    def test_returns_copy_not_mutating_internal(
        self, index: DocMetadataIndex
    ) -> None:
        index.set_meta("d1", "k", "v", now=1.0)
        e = index.get_entry("d1", "k")
        assert e is not None
        e.value = "MUTATED"
        # Internal state untouched.
        assert index.get_meta("d1", "k") == "v"


# ---------------------------------------------------------------------------
# delete_meta
# ---------------------------------------------------------------------------


class TestDeleteMeta:
    def test_delete_existing_returns_true(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.delete_meta("d1", "author") is True

    def test_delete_missing_returns_false(
        self, index: DocMetadataIndex
    ) -> None:
        assert index.delete_meta("d", "k") is False

    def test_delete_removes_from_entries(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.delete_meta("d1", "author")
        assert populated_index.get_meta("d1", "author") is None

    def test_delete_updates_inverted(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.delete_meta("d1", "author")
        assert "d1" not in populated_index.docs_with("author", "alice")

    def test_delete_updates_by_doc(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.delete_meta("d1", "author")
        assert "author" not in populated_index.meta_for_doc("d1")

    def test_delete_last_entry_removes_doc(
        self, index: DocMetadataIndex
    ) -> None:
        index.set_meta("d1", "k", "v")
        index.delete_meta("d1", "k")
        assert "d1" not in index.all_doc_ids()


# ---------------------------------------------------------------------------
# meta_for_doc
# ---------------------------------------------------------------------------


class TestMetaForDoc:
    def test_empty_for_unknown(self, index: DocMetadataIndex) -> None:
        assert index.meta_for_doc("nope") == {}

    def test_full_metadata(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.meta_for_doc("d1") == {
            "author": "alice",
            "lang": "en",
        }

    def test_returns_copy(self, populated_index: DocMetadataIndex) -> None:
        d = populated_index.meta_for_doc("d1")
        d["author"] = "MUTATED"
        # The next call must still return the original mapping.
        assert populated_index.meta_for_doc("d1")["author"] == "alice"


# ---------------------------------------------------------------------------
# docs_with
# ---------------------------------------------------------------------------


class TestDocsWith:
    def test_empty_for_unknown(self, index: DocMetadataIndex) -> None:
        assert index.docs_with("k", "v") == []

    def test_single_match(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.docs_with("author", "bob") == ["d3"]

    def test_multiple_matches_sorted(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.docs_with("author", "alice") == ["d1", "d2"]

    def test_sorted_order(self, index: DocMetadataIndex) -> None:
        for doc in ["zeta", "alpha", "mu"]:
            index.set_meta(doc, "k", "v")
        assert index.docs_with("k", "v") == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------------------
# docs_with_key
# ---------------------------------------------------------------------------


class TestDocsWithKey:
    def test_empty_for_unknown(self, index: DocMetadataIndex) -> None:
        assert index.docs_with_key("missing") == []

    def test_returns_all_docs_with_key(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.docs_with_key("author") == ["d1", "d2", "d3"]

    def test_sorted(self, index: DocMetadataIndex) -> None:
        for doc in ["c", "a", "b"]:
            index.set_meta(doc, "k", f"v_{doc}")
        assert index.docs_with_key("k") == ["a", "b", "c"]

    def test_different_values_still_listed(
        self, populated_index: DocMetadataIndex
    ) -> None:
        # All three docs have the "lang" key with different values.
        assert populated_index.docs_with_key("lang") == ["d1", "d2", "d3"]


# ---------------------------------------------------------------------------
# values_for_key
# ---------------------------------------------------------------------------


class TestValuesForKey:
    def test_empty_for_unknown(self, index: DocMetadataIndex) -> None:
        assert index.values_for_key("missing") == []

    def test_unique_values(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.values_for_key("author") == ["alice", "bob"]

    def test_sorted_values(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "k", "zeta")
        index.set_meta("d2", "k", "alpha")
        index.set_meta("d3", "k", "mu")
        assert index.values_for_key("k") == ["alpha", "mu", "zeta"]

    def test_duplicates_collapsed(self, index: DocMetadataIndex) -> None:
        index.set_meta("d1", "k", "v")
        index.set_meta("d2", "k", "v")
        index.set_meta("d3", "k", "v")
        assert index.values_for_key("k") == ["v"]


# ---------------------------------------------------------------------------
# find_by_filter
# ---------------------------------------------------------------------------


class TestFindByFilter:
    def test_empty_filters_returns_empty(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.find_by_filter({}) == []

    def test_single_filter(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.find_by_filter({"author": "alice"}) == [
            "d1",
            "d2",
        ]

    def test_and_match(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.find_by_filter(
            {"author": "alice", "lang": "en"}
        ) == ["d1"]

    def test_no_match(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert (
            populated_index.find_by_filter(
                {"author": "alice", "lang": "fr"}
            )
            == []
        )

    def test_unknown_key(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert (
            populated_index.find_by_filter({"unknown": "x"}) == []
        )

    def test_sorted_results(self, index: DocMetadataIndex) -> None:
        for doc in ["zeta", "alpha", "mu"]:
            index.set_meta(doc, "k", "v")
        assert index.find_by_filter({"k": "v"}) == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_clear_unknown_returns_zero(
        self, index: DocMetadataIndex
    ) -> None:
        assert index.clear_doc("nope") == 0

    def test_clear_returns_count(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.clear_doc("d1") == 2

    def test_clear_removes_all_entries(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_doc("d1")
        assert populated_index.meta_for_doc("d1") == {}

    def test_clear_updates_inverted(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_doc("d1")
        assert "d1" not in populated_index.docs_with("author", "alice")
        assert "d1" not in populated_index.docs_with("lang", "en")

    def test_clear_does_not_affect_other_docs(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_doc("d1")
        assert populated_index.meta_for_doc("d2") == {
            "author": "alice",
            "lang": "ru",
        }


# ---------------------------------------------------------------------------
# clear_key
# ---------------------------------------------------------------------------


class TestClearKey:
    def test_clear_unknown_returns_zero(
        self, index: DocMetadataIndex
    ) -> None:
        assert index.clear_key("nope") == 0

    def test_clear_returns_count(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.clear_key("author") == 3

    def test_clear_removes_key_from_all_docs(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_key("author")
        for doc in ["d1", "d2", "d3"]:
            assert "author" not in populated_index.meta_for_doc(doc)

    def test_clear_keeps_other_keys(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_key("author")
        assert populated_index.meta_for_doc("d1") == {"lang": "en"}

    def test_clear_updates_inverted(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_key("author")
        assert populated_index.docs_with("author", "alice") == []
        assert populated_index.docs_with("author", "bob") == []
        assert populated_index.values_for_key("author") == []


# ---------------------------------------------------------------------------
# all_keys
# ---------------------------------------------------------------------------


class TestAllKeys:
    def test_empty(self, index: DocMetadataIndex) -> None:
        assert index.all_keys() == []

    def test_sorted_unique(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.all_keys() == ["author", "lang"]

    def test_extra_keys_sorted(self, index: DocMetadataIndex) -> None:
        index.set_meta("d", "zeta", "v")
        index.set_meta("d", "alpha", "v")
        index.set_meta("d", "mu", "v")
        assert index.all_keys() == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self, index: DocMetadataIndex) -> None:
        assert index.all_doc_ids() == []

    def test_sorted_unique(
        self, populated_index: DocMetadataIndex
    ) -> None:
        assert populated_index.all_doc_ids() == ["d1", "d2", "d3"]

    def test_after_clear_doc(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_doc("d2")
        assert populated_index.all_doc_ids() == ["d1", "d3"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_stats(self, index: DocMetadataIndex) -> None:
        assert index.stats() == MetaStats(0, 0, 0)

    def test_after_inserts(
        self, populated_index: DocMetadataIndex
    ) -> None:
        s = populated_index.stats()
        assert s.total_entries == 6
        assert s.unique_docs == 3
        assert s.unique_keys == 2

    def test_after_delete(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.delete_meta("d1", "author")
        s = populated_index.stats()
        assert s.total_entries == 5
        assert s.unique_docs == 3
        assert s.unique_keys == 2

    def test_after_clear_doc(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_doc("d1")
        s = populated_index.stats()
        assert s.total_entries == 4
        assert s.unique_docs == 2
        assert s.unique_keys == 2

    def test_after_clear_key(
        self, populated_index: DocMetadataIndex
    ) -> None:
        populated_index.clear_key("author")
        s = populated_index.stats()
        assert s.total_entries == 3
        assert s.unique_docs == 3
        assert s.unique_keys == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_set_meta_same_key(self) -> None:
        idx = DocMetadataIndex()
        results: list = []

        def worker(i: int) -> None:
            for j in range(50):
                idx.set_meta(f"doc_{i}", f"key_{j}", f"v_{i}_{j}")
            results.append(i)

        threads = [
            threading.Thread(target=worker, args=(i,)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = idx.stats()
        # 8 docs × 50 keys.
        assert s.total_entries == 8 * 50
        assert s.unique_docs == 8
        assert s.unique_keys == 50
        assert sorted(results) == list(range(8))

    def test_concurrent_replace_same_pair(self) -> None:
        idx = DocMetadataIndex()

        def worker(i: int) -> None:
            for _ in range(100):
                idx.set_meta("doc", "key", f"v_{i}")

        threads = [
            threading.Thread(target=worker, args=(i,)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly one entry, value is one of the workers' values.
        assert idx.stats() == MetaStats(
            total_entries=1, unique_docs=1, unique_keys=1
        )
        val = idx.get_meta("doc", "key")
        assert val is not None and val.startswith("v_")
        # Inverted index must be consistent with the final value.
        assert idx.docs_with("key", val) == ["doc"]
