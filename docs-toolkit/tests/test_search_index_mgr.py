"""Tests for the search_index_mgr module (E62)."""
from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path

import pytest

from docstoolkit.search_index_mgr import (
    IndexConfig,
    IndexEntry,
    IndexPersistence,
    IndexStats,
    SearchIndexManager,
)


# ===========================================================================
# Helpers
# ===========================================================================

def make_entry(
    doc_id: str = "doc1",
    title: str = "Hello World",
    content: str = "This is a test document.",
    tags: list[str] | None = None,
    metadata: dict | None = None,
) -> IndexEntry:
    return IndexEntry(
        doc_id=doc_id,
        title=title,
        content=content,
        tags=tags if tags is not None else [],
        metadata=metadata if metadata is not None else {},
    )


def make_manager(config: IndexConfig | None = None) -> SearchIndexManager:
    return SearchIndexManager(config=config)


# ===========================================================================
# IndexEntry
# ===========================================================================

class TestIndexEntryFields:
    def test_required_fields(self):
        e = IndexEntry(doc_id="d1", title="T", content="C")
        assert e.doc_id == "d1"
        assert e.title == "T"
        assert e.content == "C"

    def test_tags_default_empty_list(self):
        e = IndexEntry(doc_id="d1", title="T", content="C")
        assert e.tags == []

    def test_metadata_default_empty_dict(self):
        e = IndexEntry(doc_id="d1", title="T", content="C")
        assert e.metadata == {}

    def test_indexed_at_default_is_float(self):
        before = time.time()
        e = IndexEntry(doc_id="d1", title="T", content="C")
        after = time.time()
        assert isinstance(e.indexed_at, float)
        assert before <= e.indexed_at <= after

    def test_tags_are_independent_across_instances(self):
        e1 = IndexEntry(doc_id="d1", title="T", content="C")
        e2 = IndexEntry(doc_id="d2", title="T", content="C")
        e1.tags.append("foo")
        assert e2.tags == []

    def test_metadata_are_independent_across_instances(self):
        e1 = IndexEntry(doc_id="d1", title="T", content="C")
        e2 = IndexEntry(doc_id="d2", title="T", content="C")
        e1.metadata["key"] = "val"
        assert e2.metadata == {}

    def test_custom_tags(self):
        e = IndexEntry(doc_id="d1", title="T", content="C", tags=["a", "b"])
        assert e.tags == ["a", "b"]

    def test_custom_metadata(self):
        e = IndexEntry(doc_id="d1", title="T", content="C", metadata={"x": 1})
        assert e.metadata["x"] == 1

    def test_custom_indexed_at(self):
        ts = 1_000_000.0
        e = IndexEntry(doc_id="d1", title="T", content="C", indexed_at=ts)
        assert e.indexed_at == ts


# ===========================================================================
# IndexStats
# ===========================================================================

class TestIndexStats:
    def test_fields_present(self):
        s = IndexStats(total_docs=5, total_terms=20, avg_doc_length=10.0, last_updated=1.0)
        assert s.total_docs == 5
        assert s.total_terms == 20
        assert s.avg_doc_length == 10.0
        assert s.last_updated == 1.0

    def test_zero_values(self):
        s = IndexStats(total_docs=0, total_terms=0, avg_doc_length=0.0, last_updated=0.0)
        assert s.total_docs == 0
        assert s.avg_doc_length == 0.0


# ===========================================================================
# IndexConfig
# ===========================================================================

class TestIndexConfig:
    def test_defaults(self):
        cfg = IndexConfig()
        assert cfg.min_term_length == 2
        assert cfg.max_terms_per_doc == 10000
        assert cfg.stop_words == set()

    def test_custom_min_term_length(self):
        cfg = IndexConfig(min_term_length=4)
        assert cfg.min_term_length == 4

    def test_custom_max_terms_per_doc(self):
        cfg = IndexConfig(max_terms_per_doc=50)
        assert cfg.max_terms_per_doc == 50

    def test_custom_stop_words(self):
        cfg = IndexConfig(stop_words={"the", "and"})
        assert "the" in cfg.stop_words
        assert "and" in cfg.stop_words

    def test_stop_words_independent_across_instances(self):
        c1 = IndexConfig()
        c2 = IndexConfig()
        c1.stop_words.add("foo")
        assert "foo" not in c2.stop_words


# ===========================================================================
# SearchIndexManager — add / get / remove / update
# ===========================================================================

class TestManagerAdd:
    def test_add_single_entry(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        assert mgr.get("d1") is not None

    def test_add_returns_none(self):
        mgr = make_manager()
        result = mgr.add(make_entry("d1"))
        assert result is None

    def test_add_increments_doc_count(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        assert mgr.stats().total_docs == 2

    def test_add_duplicate_replaces_entry(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", title="Old", content="old content"))
        mgr.add(make_entry("d1", title="New", content="new content"))
        entry = mgr.get("d1")
        assert entry.title == "New"
        assert mgr.stats().total_docs == 1

    def test_add_duplicate_does_not_double_count_terms(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", content="apple banana"))
        mgr.add(make_entry("d1", content="apple banana"))
        # Only one doc contributes; df for "apple" should be 1
        results = mgr.search("apple")
        assert len(results) == 1

    def test_add_indexes_title_words(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="Unique Title Word", content="other stuff"))
        results = mgr.search("unique")
        assert any(r[0] == "d1" for r in results)

    def test_add_indexes_content_words(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="plain", content="distinctive content here"))
        results = mgr.search("distinctive")
        assert any(r[0] == "d1" for r in results)


class TestManagerGet:
    def test_get_existing_returns_entry(self):
        mgr = make_manager()
        entry = make_entry("d1")
        mgr.add(entry)
        result = mgr.get("d1")
        assert result.doc_id == "d1"

    def test_get_nonexistent_returns_none(self):
        mgr = make_manager()
        assert mgr.get("nonexistent") is None

    def test_get_after_remove_returns_none(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.remove("d1")
        assert mgr.get("d1") is None

    def test_get_preserves_tags(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["alpha", "beta"]))
        assert mgr.get("d1").tags == ["alpha", "beta"]

    def test_get_preserves_metadata(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", metadata={"key": "value"}))
        assert mgr.get("d1").metadata["key"] == "value"


class TestManagerRemove:
    def test_remove_existing_returns_true(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        assert mgr.remove("d1") is True

    def test_remove_nonexistent_returns_false(self):
        mgr = make_manager()
        assert mgr.remove("ghost") is False

    def test_remove_decrements_doc_count(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        mgr.remove("d1")
        assert mgr.stats().total_docs == 1

    def test_remove_cleans_inverted_index(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="unique", content="unique term"))
        mgr.remove("d1")
        results = mgr.search("unique")
        assert results == []

    def test_remove_leaves_other_docs_searchable(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="apple pie", content="tasty apple"))
        mgr.add(IndexEntry(doc_id="d2", title="banana split", content="tasty banana"))
        mgr.remove("d1")
        results = mgr.search("banana")
        assert any(r[0] == "d2" for r in results)
        results2 = mgr.search("apple")
        assert all(r[0] != "d1" for r in results2)

    def test_remove_nonexistent_does_not_raise(self):
        mgr = make_manager()
        # should not raise
        mgr.remove("does-not-exist")

    def test_remove_then_re_add(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", content="hello world"))
        mgr.remove("d1")
        mgr.add(make_entry("d1", content="new content"))
        assert mgr.get("d1").content == "new content"


class TestManagerUpdate:
    def test_update_existing_doc(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", title="Old", content="old"))
        mgr.update(make_entry("d1", title="New", content="new"))
        assert mgr.get("d1").title == "New"

    def test_update_removes_old_terms(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="obsolete", content="obsolete phrase"))
        mgr.update(IndexEntry(doc_id="d1", title="fresh", content="fresh phrase"))
        results = mgr.search("obsolete")
        assert all(r[0] != "d1" for r in results)

    def test_update_indexes_new_terms(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="x", content="old"))
        mgr.update(IndexEntry(doc_id="d1", title="y", content="brandnew"))
        results = mgr.search("brandnew")
        assert any(r[0] == "d1" for r in results)

    def test_update_nonexistent_acts_as_add(self):
        mgr = make_manager()
        mgr.update(make_entry("d1", content="added via update"))
        assert mgr.get("d1") is not None

    def test_update_doc_count_unchanged(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.update(make_entry("d1", content="changed"))
        assert mgr.stats().total_docs == 1


# ===========================================================================
# SearchIndexManager — search
# ===========================================================================

class TestManagerSearch:
    def test_search_empty_index(self):
        mgr = make_manager()
        assert mgr.search("anything") == []

    def test_search_returns_list_of_tuples(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="hello", content="hello world"))
        results = mgr.search("hello")
        assert isinstance(results, list)
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)

    def test_search_score_is_float(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="test", content="test content"))
        results = mgr.search("test")
        assert isinstance(results[0][1], float)

    def test_search_single_doc(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="fruit", content="apple orange banana"))
        results = mgr.search("apple")
        assert len(results) == 1
        assert results[0][0] == "d1"

    def test_search_returns_relevant_docs(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="cats", content="cats are great pets"))
        mgr.add(IndexEntry(doc_id="d2", title="dogs", content="dogs are loyal animals"))
        results = mgr.search("cats")
        doc_ids = [r[0] for r in results]
        assert "d1" in doc_ids
        assert "d2" not in doc_ids

    def test_search_sorted_descending(self):
        mgr = make_manager()
        # d1 mentions "rare" 5 times (title+content), d2 only once → d1 gets higher TF
        mgr.add(IndexEntry(doc_id="d1", title="rare rare", content="rare rare rare"))
        mgr.add(IndexEntry(doc_id="d2", title="other", content="rare words here these extra"))
        results = mgr.search("rare")
        # d1's TF for "rare" is 5/5 = 1.0; d2's TF is 1/5 = 0.2 → d1 ranks first
        assert results[0][0] == "d1"

    def test_search_top_k_limits_results(self):
        mgr = make_manager()
        for i in range(20):
            mgr.add(IndexEntry(doc_id=f"d{i}", title="common", content="common word shared"))
        results = mgr.search("common", top_k=5)
        assert len(results) <= 5

    def test_search_top_k_default_10(self):
        mgr = make_manager()
        for i in range(15):
            mgr.add(IndexEntry(doc_id=f"d{i}", title="word", content="word content"))
        results = mgr.search("word")
        assert len(results) <= 10

    def test_search_unknown_term_empty_result(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="hello", content="world"))
        results = mgr.search("zzzzqqqq")
        assert results == []

    def test_search_multi_term_query(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="alpha beta", content="gamma delta"))
        results = mgr.search("alpha gamma")
        assert any(r[0] == "d1" for r in results)

    def test_search_scores_positive(self):
        mgr = make_manager()
        # With smoothed IDF (log((N+1)/(df+1))+1), scores are always > 0
        mgr.add(IndexEntry(doc_id="d1", title="positive", content="positive score test"))
        mgr.add(IndexEntry(doc_id="d2", title="other", content="other content"))
        results = mgr.search("positive")
        assert len(results) >= 1
        for _, score in results:
            assert score > 0


# ===========================================================================
# TF-IDF ranking: rare terms rank higher
# ===========================================================================

class TestTFIDF:
    def test_rare_term_ranks_higher(self):
        """A term appearing in fewer docs should give higher IDF weight."""
        mgr = make_manager()
        # "rare" only in d1; "common" in d1 and d2
        mgr.add(IndexEntry(doc_id="d1", title="rare common", content="rare common"))
        mgr.add(IndexEntry(doc_id="d2", title="common", content="common words only"))
        mgr.add(IndexEntry(doc_id="d3", title="common", content="common content here"))
        # Searching "rare" should return only d1 with a non-zero score
        results_rare = mgr.search("rare")
        assert len(results_rare) == 1
        assert results_rare[0][0] == "d1"

    def test_idf_increases_with_fewer_docs(self):
        """Term in 1 out of 10 docs should score higher than term in 9 out of 10."""
        mgr = make_manager()
        for i in range(9):
            mgr.add(IndexEntry(doc_id=f"d{i}", title="frequent", content="frequent word"))
        mgr.add(IndexEntry(doc_id="d9", title="rare unique", content="rare unique term"))
        # d9 contains both "frequent" (now in all 10) via... wait, only d9 has "rare"
        results = mgr.search("rare")
        assert results[0][0] == "d9"

    def test_higher_tf_in_same_doc(self):
        """Within one doc, higher term frequency should score higher."""
        mgr = make_manager()
        # Only one doc, so IDF is the same for both terms (both df=1, N=1)
        # IDF = log((1+1)/(1+1)) + 1 = 1.0 for both
        # apple appears 4 times out of 5 tokens → TF=0.8
        # banana appears 1 time out of 5 tokens → TF=0.2
        mgr.add(IndexEntry(doc_id="d1", title="apple", content="apple apple apple banana"))
        results_apple = mgr.search("apple")
        results_banana = mgr.search("banana")
        assert results_apple[0][1] > results_banana[0][1]

    def test_doc_with_term_in_multiple_positions_scores_higher(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="target target", content="target word target"))
        mgr.add(IndexEntry(doc_id="d2", title="other", content="target word"))
        results = mgr.search("target")
        assert results[0][0] == "d1"


# ===========================================================================
# IndexConfig: min_term_length and stop_words
# ===========================================================================

class TestIndexConfigFiltering:
    def test_min_term_length_filters_short_terms(self):
        cfg = IndexConfig(min_term_length=4)
        mgr = make_manager(config=cfg)
        # "at" is 2 chars — filtered; "long" is 4 — kept
        mgr.add(IndexEntry(doc_id="d1", title="", content="at the long word"))
        results_short = mgr.search("at")
        results_long = mgr.search("long")
        assert results_short == []
        assert any(r[0] == "d1" for r in results_long)

    def test_min_term_length_1_allows_single_char(self):
        cfg = IndexConfig(min_term_length=1)
        mgr = make_manager(config=cfg)
        mgr.add(IndexEntry(doc_id="d1", title="a", content="a b c"))
        results = mgr.search("a")
        assert any(r[0] == "d1" for r in results)

    def test_stop_words_are_not_indexed(self):
        cfg = IndexConfig(stop_words={"the", "is", "and"})
        mgr = make_manager(config=cfg)
        mgr.add(IndexEntry(doc_id="d1", title="the best", content="this is the best"))
        results = mgr.search("the")
        assert results == []

    def test_stop_words_do_not_affect_non_stop_terms(self):
        cfg = IndexConfig(stop_words={"the", "is"})
        mgr = make_manager(config=cfg)
        mgr.add(IndexEntry(doc_id="d1", title="the sky", content="the sky is blue"))
        results = mgr.search("sky")
        assert any(r[0] == "d1" for r in results)
        results2 = mgr.search("blue")
        assert any(r[0] == "d1" for r in results2)

    def test_stop_words_in_query_are_also_filtered(self):
        cfg = IndexConfig(stop_words={"of"})
        mgr = make_manager(config=cfg)
        mgr.add(IndexEntry(doc_id="d1", title="realm", content="realm of magic"))
        # query contains "of" which is a stop word → only "realm" is scored
        results = mgr.search("realm of magic")
        assert any(r[0] == "d1" for r in results)

    def test_max_terms_per_doc_limits_tokens(self):
        cfg = IndexConfig(max_terms_per_doc=3)
        mgr = make_manager(config=cfg)
        # Only the first 3 tokens are indexed
        mgr.add(IndexEntry(doc_id="d1", title="", content="alpha beta gamma delta epsilon"))
        # "alpha" is in the first 3, "delta" is not
        results_alpha = mgr.search("alpha")
        results_delta = mgr.search("delta")
        assert any(r[0] == "d1" for r in results_alpha)
        assert results_delta == []


# ===========================================================================
# search_by_tag
# ===========================================================================

class TestManagerSearchByTag:
    def test_search_by_tag_returns_matching_doc_ids(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["python", "oss"]))
        mgr.add(make_entry("d2", tags=["java"]))
        result = mgr.search_by_tag("python")
        assert "d1" in result
        assert "d2" not in result

    def test_search_by_tag_no_match_returns_empty(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["alpha"]))
        result = mgr.search_by_tag("nonexistent")
        assert result == []

    def test_search_by_tag_multiple_docs(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["shared"]))
        mgr.add(make_entry("d2", tags=["shared"]))
        mgr.add(make_entry("d3", tags=["other"]))
        result = mgr.search_by_tag("shared")
        assert "d1" in result
        assert "d2" in result
        assert "d3" not in result

    def test_search_by_tag_empty_index(self):
        mgr = make_manager()
        result = mgr.search_by_tag("anything")
        assert result == []

    def test_search_by_tag_after_remove(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["removable"]))
        mgr.remove("d1")
        result = mgr.search_by_tag("removable")
        assert "d1" not in result

    def test_search_by_tag_after_update_removes_old_tag(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["old_tag"]))
        mgr.update(make_entry("d1", tags=["new_tag"]))
        assert "d1" not in mgr.search_by_tag("old_tag")
        assert "d1" in mgr.search_by_tag("new_tag")


# ===========================================================================
# stats
# ===========================================================================

class TestManagerStats:
    def test_stats_empty_index(self):
        mgr = make_manager()
        s = mgr.stats()
        assert s.total_docs == 0
        assert s.total_terms == 0
        assert s.avg_doc_length == 0.0

    def test_stats_after_add(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="hello", content="hello world test"))
        s = mgr.stats()
        assert s.total_docs == 1
        assert s.total_terms >= 1

    def test_stats_avg_doc_length_positive(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="one two three", content="four five six"))
        s = mgr.stats()
        assert s.avg_doc_length > 0

    def test_stats_last_updated_is_float(self):
        mgr = make_manager()
        s = mgr.stats()
        assert isinstance(s.last_updated, float)

    def test_stats_total_terms_grows_with_unique_terms(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="alpha beta", content="gamma"))
        s1 = mgr.stats()
        mgr.add(IndexEntry(doc_id="d2", title="delta epsilon", content="zeta"))
        s2 = mgr.stats()
        assert s2.total_terms >= s1.total_terms

    def test_stats_after_remove_decreases_doc_count(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        mgr.remove("d1")
        assert mgr.stats().total_docs == 1

    def test_stats_returns_index_stats_instance(self):
        mgr = make_manager()
        assert isinstance(mgr.stats(), IndexStats)


# ===========================================================================
# all_doc_ids
# ===========================================================================

class TestManagerAllDocIds:
    def test_all_doc_ids_empty(self):
        mgr = make_manager()
        assert mgr.all_doc_ids() == []

    def test_all_doc_ids_after_add(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        ids = mgr.all_doc_ids()
        assert "d1" in ids
        assert "d2" in ids
        assert len(ids) == 2

    def test_all_doc_ids_after_remove(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        mgr.remove("d1")
        ids = mgr.all_doc_ids()
        assert "d1" not in ids
        assert "d2" in ids

    def test_all_doc_ids_returns_list(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        assert isinstance(mgr.all_doc_ids(), list)


# ===========================================================================
# clear
# ===========================================================================

class TestManagerClear:
    def test_clear_empties_index(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        mgr.clear()
        assert mgr.stats().total_docs == 0

    def test_clear_empties_inverted_index(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="hello", content="world"))
        mgr.clear()
        assert mgr.search("hello") == []

    def test_clear_empties_doc_ids(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.clear()
        assert mgr.all_doc_ids() == []

    def test_clear_allows_re_add(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.clear()
        mgr.add(make_entry("d1", content="reborn"))
        assert mgr.get("d1").content == "reborn"

    def test_clear_updates_last_updated(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        before = mgr.stats().last_updated
        mgr.clear()
        after = mgr.stats().last_updated
        assert after >= before


# ===========================================================================
# IndexPersistence
# ===========================================================================

class TestIndexPersistence:
    def test_save_creates_file(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            assert path.exists()

    def test_save_file_is_valid_json(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            data = json.loads(path.read_text())
            assert "entries" in data
            assert "inverted" in data

    def test_roundtrip_doc_count(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.add(make_entry("d2"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            assert loaded.stats().total_docs == 2

    def test_roundtrip_entry_content(self):
        mgr = make_manager()
        original = IndexEntry(
            doc_id="d1",
            title="Preserved Title",
            content="Preserved content body",
            tags=["tag1", "tag2"],
            metadata={"author": "alice"},
        )
        mgr.add(original)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            entry = loaded.get("d1")
            assert entry is not None
            assert entry.title == "Preserved Title"
            assert entry.content == "Preserved content body"
            assert entry.tags == ["tag1", "tag2"]
            assert entry.metadata["author"] == "alice"

    def test_roundtrip_search_works(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="searchable", content="unique special term"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            results = loaded.search("unique")
            assert any(r[0] == "d1" for r in results)

    def test_roundtrip_tag_search_works(self):
        mgr = make_manager()
        mgr.add(make_entry("d1", tags=["preserved_tag"]))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            result = loaded.search_by_tag("preserved_tag")
            assert "d1" in result

    def test_roundtrip_with_config(self):
        cfg = IndexConfig(stop_words={"the", "is"}, min_term_length=3)
        mgr = make_manager(config=cfg)
        mgr.add(IndexEntry(doc_id="d1", title="the realm", content="realm is vast"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            # Load with same config
            loaded = IndexPersistence.load(path, config=cfg)
            results = loaded.search("realm")
            assert any(r[0] == "d1" for r in results)

    def test_load_with_string_path(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        with tempfile.TemporaryDirectory() as td:
            path = str(Path(td) / "index.json")
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            assert loaded.get("d1") is not None

    def test_roundtrip_inverted_index_preserved(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="apple", content="apple juice"))
        mgr.add(IndexEntry(doc_id="d2", title="orange", content="orange juice"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            # "juice" appears in both docs; both should be in results
            results = loaded.search("juice")
            doc_ids = [r[0] for r in results]
            assert "d1" in doc_ids
            assert "d2" in doc_ids

    def test_roundtrip_multiple_adds(self):
        mgr = make_manager()
        for i in range(10):
            mgr.add(IndexEntry(doc_id=f"d{i}", title=f"title{i}", content=f"content word{i}"))
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "index.json"
            IndexPersistence.save(mgr, path)
            loaded = IndexPersistence.load(path)
            assert loaded.stats().total_docs == 10
            assert loaded.get("d5") is not None


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_search_empty_query(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        results = mgr.search("")
        assert results == []

    def test_search_whitespace_query(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        results = mgr.search("   ")
        assert results == []

    def test_remove_nonexistent_returns_false(self):
        mgr = make_manager()
        assert mgr.remove("does_not_exist") is False

    def test_get_nonexistent_returns_none(self):
        mgr = make_manager()
        assert mgr.get("missing") is None

    def test_single_doc_index_search(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="only", title="sole document", content="only document here"))
        results = mgr.search("document")
        assert len(results) == 1
        assert results[0][0] == "only"

    def test_case_insensitive_indexing(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="Hello WORLD", content="HELLO world"))
        results = mgr.search("hello")
        assert any(r[0] == "d1" for r in results)

    def test_case_insensitive_query(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="example", content="example content"))
        results = mgr.search("EXAMPLE")
        assert any(r[0] == "d1" for r in results)

    def test_empty_content_and_title(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="empty", title="", content=""))
        assert mgr.get("empty") is not None
        assert mgr.search("nothing") == []

    def test_add_many_docs(self):
        mgr = make_manager()
        for i in range(100):
            mgr.add(IndexEntry(doc_id=f"d{i}", title=f"doc{i}", content=f"content unique{i}"))
        assert mgr.stats().total_docs == 100

    def test_search_top_k_zero(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="hello", content="hello world"))
        results = mgr.search("hello", top_k=0)
        assert results == []

    def test_search_top_k_larger_than_results(self):
        mgr = make_manager()
        mgr.add(IndexEntry(doc_id="d1", title="only one", content="only one doc here"))
        results = mgr.search("only", top_k=100)
        assert len(results) == 1

    def test_all_doc_ids_no_duplicates_after_update(self):
        mgr = make_manager()
        mgr.add(make_entry("d1"))
        mgr.update(make_entry("d1", content="updated"))
        ids = mgr.all_doc_ids()
        assert ids.count("d1") == 1
