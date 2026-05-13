"""Tests for docstoolkit.doc_index (E136 — fast in-memory document index).

Coverage target: >= 50 tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.doc_index import DocIndex, IndexConfig, IndexedDoc, IndexEntry


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_index(**cfg_kwargs) -> DocIndex:
    """Return an empty DocIndex with optional config overrides."""
    return DocIndex(IndexConfig(**cfg_kwargs) if cfg_kwargs else None)


def populated_index() -> DocIndex:
    idx = make_index()
    idx.add("d1", {"title": "Python programming", "body": "Learn python code and algorithms"})
    idx.add("d2", {"title": "Cooking basics", "body": "Recipes for bread and butter"})
    idx.add("d3", {"title": "Python recipes", "body": "Python tricks for cooking data"})
    return idx


# ===========================================================================
# 1. IndexedDoc dataclass
# ===========================================================================

class TestIndexedDoc:
    def test_basic_construction(self):
        doc = IndexedDoc(doc_id="x", fields={"title": "hi"})
        assert doc.doc_id == "x"
        assert doc.fields == {"title": "hi"}
        assert doc.metadata == {}

    def test_metadata_default_factory_is_independent(self):
        a = IndexedDoc(doc_id="a", fields={})
        b = IndexedDoc(doc_id="b", fields={})
        a.metadata["k"] = 1
        assert b.metadata == {}

    def test_metadata_can_be_supplied(self):
        doc = IndexedDoc(doc_id="x", fields={"t": "a"}, metadata={"author": "ada"})
        assert doc.metadata == {"author": "ada"}

    def test_fields_is_mapping(self):
        doc = IndexedDoc(doc_id="x", fields={"a": "1", "b": "2"})
        assert set(doc.fields) == {"a", "b"}


# ===========================================================================
# 2. IndexEntry dataclass
# ===========================================================================

class TestIndexEntry:
    def test_basic_fields(self):
        e = IndexEntry(doc_id="d", field="title", score=2.0, matches=1)
        assert e.doc_id == "d"
        assert e.field == "title"
        assert e.score == 2.0
        assert e.matches == 1

    def test_entries_equal_when_same(self):
        a = IndexEntry("d", "title", 2.0, 1)
        b = IndexEntry("d", "title", 2.0, 1)
        assert a == b

    def test_entries_unequal_on_diff(self):
        a = IndexEntry("d", "title", 2.0, 1)
        b = IndexEntry("d", "title", 1.0, 1)
        assert a != b


# ===========================================================================
# 3. IndexConfig
# ===========================================================================

class TestIndexConfig:
    def test_defaults(self):
        c = IndexConfig()
        assert c.field_weights == {"title": 2.0, "body": 1.0}
        assert c.case_sensitive is False
        assert c.min_token_length == 2

    def test_custom_weights(self):
        c = IndexConfig(field_weights={"x": 3.0})
        assert c.field_weights == {"x": 3.0}

    def test_case_sensitive_flag(self):
        c = IndexConfig(case_sensitive=True)
        assert c.case_sensitive is True

    def test_min_token_length(self):
        c = IndexConfig(min_token_length=4)
        assert c.min_token_length == 4

    def test_weights_factory_independent(self):
        a = IndexConfig()
        b = IndexConfig()
        a.field_weights["x"] = 9.0
        assert "x" not in b.field_weights


# ===========================================================================
# 4. Add and Get
# ===========================================================================

class TestAddAndGet:
    def test_add_then_get(self):
        idx = make_index()
        idx.add("d1", {"title": "Hello world"})
        doc = idx.get("d1")
        assert doc is not None
        assert doc.doc_id == "d1"
        assert doc.fields == {"title": "Hello world"}

    def test_get_missing_returns_none(self):
        idx = make_index()
        assert idx.get("nope") is None

    def test_add_stores_metadata(self):
        idx = make_index()
        idx.add("d1", {"title": "x"}, metadata={"k": "v"})
        assert idx.get("d1").metadata == {"k": "v"}

    def test_add_default_metadata_empty(self):
        idx = make_index()
        idx.add("d1", {"title": "x"})
        assert idx.get("d1").metadata == {}

    def test_add_replaces_existing(self):
        idx = make_index()
        idx.add("d1", {"title": "old"})
        idx.add("d1", {"title": "new"})
        assert idx.get("d1").fields == {"title": "new"}
        assert idx.count == 1

    def test_add_replaces_clears_old_tokens(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        idx.add("d1", {"title": "beta"})
        assert idx.search("alpha") == []
        hits = idx.search("beta")
        assert any(h.doc_id == "d1" for h in hits)


# ===========================================================================
# 5. Add batch
# ===========================================================================

class TestAddBatch:
    def test_add_batch_simple(self):
        idx = make_index()
        idx.add_batch([
            IndexedDoc("a", {"title": "x"}),
            IndexedDoc("b", {"title": "y"}),
        ])
        assert idx.count == 2
        assert idx.exists("a") and idx.exists("b")

    def test_add_batch_empty(self):
        idx = make_index()
        idx.add_batch([])
        assert idx.count == 0

    def test_add_batch_preserves_metadata(self):
        idx = make_index()
        idx.add_batch([IndexedDoc("a", {"title": "x"}, metadata={"v": 1})])
        assert idx.get("a").metadata == {"v": 1}


# ===========================================================================
# 6. Remove
# ===========================================================================

class TestRemove:
    def test_remove_existing_returns_true(self):
        idx = make_index()
        idx.add("d1", {"title": "x"})
        assert idx.remove("d1") is True
        assert idx.count == 0

    def test_remove_missing_returns_false(self):
        idx = make_index()
        assert idx.remove("ghost") is False

    def test_remove_clears_inverted_postings(self):
        idx = make_index()
        idx.add("d1", {"title": "unique_token"})
        idx.remove("d1")
        assert idx.search("unique_token") == []

    def test_remove_one_keeps_others(self):
        idx = populated_index()
        idx.remove("d1")
        assert not idx.exists("d1")
        assert idx.exists("d2")
        assert idx.exists("d3")


# ===========================================================================
# 7. Update
# ===========================================================================

class TestUpdate:
    def test_update_existing_returns_true(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        assert idx.update("d1", {"title": "omega"}) is True
        assert idx.get("d1").fields == {"title": "omega"}

    def test_update_missing_returns_false(self):
        idx = make_index()
        assert idx.update("ghost", {"title": "x"}) is False

    def test_update_reindexes(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        idx.update("d1", {"title": "omega"})
        assert idx.search("alpha") == []
        assert any(h.doc_id == "d1" for h in idx.search("omega"))

    def test_update_preserves_metadata(self):
        idx = make_index()
        idx.add("d1", {"title": "x"}, metadata={"author": "ada"})
        idx.update("d1", {"title": "y"})
        assert idx.get("d1").metadata == {"author": "ada"}


# ===========================================================================
# 8. Search basic
# ===========================================================================

class TestSearchBasic:
    def test_single_token_match(self):
        idx = populated_index()
        hits = idx.search("python")
        ids = {h.doc_id for h in hits}
        assert "d1" in ids
        assert "d3" in ids

    def test_returns_index_entries(self):
        idx = populated_index()
        hits = idx.search("python")
        assert all(isinstance(h, IndexEntry) for h in hits)

    def test_score_positive(self):
        idx = populated_index()
        hits = idx.search("python")
        for h in hits:
            assert h.score > 0
            assert h.matches >= 1

    def test_no_match_returns_empty(self):
        idx = populated_index()
        assert idx.search("zzzzzz_no_token") == []

    def test_sort_descending_by_score(self):
        idx = populated_index()
        hits = idx.search("python")
        scores = [h.score for h in hits]
        assert scores == sorted(scores, reverse=True)


# ===========================================================================
# 9. Multi-token queries
# ===========================================================================

class TestSearchMultiToken:
    def test_multiple_tokens_accumulate(self):
        idx = populated_index()
        hits = idx.search("python cooking")
        ids = {h.doc_id for h in hits}
        # d3 has both python and cooking
        assert "d3" in ids

    def test_multi_token_increases_matches(self):
        idx = make_index()
        idx.add("d1", {"body": "python python python"})
        hits = idx.search("python")
        assert hits[0].matches == 3

    def test_multi_token_query_sums_per_field(self):
        idx = make_index()
        idx.add("d1", {"body": "alpha beta"})
        hits = idx.search("alpha beta")
        # both alpha+beta hit the same field on d1 -> 2 matches
        assert any(h.doc_id == "d1" and h.matches == 2 for h in hits)


# ===========================================================================
# 10. Field weights
# ===========================================================================

class TestSearchFieldWeights:
    def test_title_weighted_higher_than_body(self):
        idx = make_index()
        idx.add("d1", {"title": "rare", "body": "filler text only"})
        idx.add("d2", {"title": "filler", "body": "rare appears once"})
        hits = idx.search("rare")
        top = hits[0]
        # d1 has rare in title (weight 2.0), so it must score higher.
        assert top.doc_id == "d1"
        assert top.field == "title"

    def test_custom_field_weight_overrides_default(self):
        idx = make_index(field_weights={"title": 1.0, "body": 5.0})
        idx.add("d1", {"title": "rare", "body": "filler"})
        idx.add("d2", {"title": "filler", "body": "rare"})
        hits = idx.search("rare")
        assert hits[0].doc_id == "d2"

    def test_unknown_field_defaults_weight_one(self):
        idx = make_index()
        idx.add("d1", {"tags": "alpha"})
        hits = idx.search("alpha")
        # tags has no explicit weight -> defaults to 1.0
        assert hits[0].score == 1.0


# ===========================================================================
# 11. Search field
# ===========================================================================

class TestSearchField:
    def test_search_field_restricts_results(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha", "body": "beta"})
        idx.add("d2", {"title": "beta", "body": "alpha"})
        hits = idx.search_field("alpha", "title")
        ids = {h.doc_id for h in hits}
        assert ids == {"d1"}

    def test_search_field_uses_field_weight(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        hits = idx.search_field("alpha", "title")
        assert hits[0].score == 2.0  # title weight 2.0

    def test_search_field_missing_field_returns_empty(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        assert idx.search_field("alpha", "body") == []

    def test_search_field_empty_query(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        assert idx.search_field("", "title") == []


# ===========================================================================
# 12. Top-K limiting
# ===========================================================================

class TestTopK:
    def test_top_k_limits_results(self):
        idx = make_index()
        for i in range(20):
            idx.add(f"d{i}", {"body": "alpha"})
        hits = idx.search("alpha", top_k=5)
        assert len(hits) == 5

    def test_top_k_zero_returns_empty(self):
        idx = make_index()
        idx.add("d1", {"body": "alpha"})
        assert idx.search("alpha", top_k=0) == []

    def test_top_k_larger_than_results_ok(self):
        idx = make_index()
        idx.add("d1", {"body": "alpha"})
        hits = idx.search("alpha", top_k=100)
        assert len(hits) == 1


# ===========================================================================
# 13. Case sensitive
# ===========================================================================

class TestCaseSensitive:
    def test_default_case_insensitive_match(self):
        idx = make_index()
        idx.add("d1", {"body": "Alpha BETA"})
        assert any(h.doc_id == "d1" for h in idx.search("alpha"))
        assert any(h.doc_id == "d1" for h in idx.search("beta"))

    def test_case_sensitive_mode(self):
        idx = make_index(case_sensitive=True)
        idx.add("d1", {"body": "Alpha"})
        # exact-case match works
        assert any(h.doc_id == "d1" for h in idx.search("Alpha"))
        # lowercase variant does not match
        assert idx.search("alpha") == []

    def test_case_sensitive_query_lowercased_by_default(self):
        idx = make_index()
        idx.add("d1", {"body": "Alpha"})
        assert any(h.doc_id == "d1" for h in idx.search("ALPHA"))


# ===========================================================================
# 14. Min token length
# ===========================================================================

class TestMinTokenLength:
    def test_default_filters_single_char_tokens(self):
        idx = make_index()
        idx.add("d1", {"body": "a python z"})
        # single-character tokens 'a' and 'z' should be filtered out.
        assert idx.search("a") == []
        assert any(h.doc_id == "d1" for h in idx.search("python"))

    def test_custom_min_token_length(self):
        idx = make_index(min_token_length=5)
        idx.add("d1", {"body": "tiny enormous"})
        assert idx.search("tiny") == []  # 4 chars
        assert any(h.doc_id == "d1" for h in idx.search("enormous"))

    def test_min_length_one_allows_everything(self):
        idx = make_index(min_token_length=1)
        idx.add("d1", {"body": "a b c"})
        assert any(h.doc_id == "d1" for h in idx.search("a"))


# ===========================================================================
# 15. Exists
# ===========================================================================

class TestExists:
    def test_exists_true(self):
        idx = make_index()
        idx.add("d1", {"title": "x"})
        assert idx.exists("d1") is True

    def test_exists_false(self):
        idx = make_index()
        assert idx.exists("nope") is False

    def test_exists_false_after_remove(self):
        idx = make_index()
        idx.add("d1", {"title": "x"})
        idx.remove("d1")
        assert idx.exists("d1") is False


# ===========================================================================
# 16. Count
# ===========================================================================

class TestCount:
    def test_count_empty(self):
        assert make_index().count == 0

    def test_count_increments(self):
        idx = make_index()
        idx.add("a", {"title": "x"})
        idx.add("b", {"title": "y"})
        assert idx.count == 2

    def test_count_decrements_on_remove(self):
        idx = make_index()
        idx.add("a", {"title": "x"})
        idx.add("b", {"title": "y"})
        idx.remove("a")
        assert idx.count == 1

    def test_count_unchanged_on_replace(self):
        idx = make_index()
        idx.add("a", {"title": "x"})
        idx.add("a", {"title": "y"})
        assert idx.count == 1


# ===========================================================================
# 17. Clear
# ===========================================================================

class TestClear:
    def test_clear_resets_count(self):
        idx = populated_index()
        idx.clear()
        assert idx.count == 0

    def test_clear_resets_search(self):
        idx = populated_index()
        idx.clear()
        assert idx.search("python") == []

    def test_clear_resets_field_names(self):
        idx = populated_index()
        idx.clear()
        assert idx.field_names == set()

    def test_clear_then_readd(self):
        idx = populated_index()
        idx.clear()
        idx.add("new", {"title": "fresh"})
        assert idx.count == 1
        assert any(h.doc_id == "new" for h in idx.search("fresh"))


# ===========================================================================
# 18. Field names / all_doc_ids
# ===========================================================================

class TestFieldNamesAndIds:
    def test_field_names_union(self):
        idx = make_index()
        idx.add("a", {"title": "x"})
        idx.add("b", {"body": "y", "tags": "z"})
        assert idx.field_names == {"title", "body", "tags"}

    def test_all_doc_ids_sorted(self):
        idx = make_index()
        idx.add("c", {"title": "x"})
        idx.add("a", {"title": "y"})
        idx.add("b", {"title": "z"})
        assert idx.all_doc_ids() == ["a", "b", "c"]

    def test_all_doc_ids_empty(self):
        assert make_index().all_doc_ids() == []


# ===========================================================================
# 19. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_search_on_empty_index(self):
        assert make_index().search("anything") == []

    def test_empty_query_string(self):
        idx = populated_index()
        assert idx.search("") == []

    def test_whitespace_only_query(self):
        idx = populated_index()
        assert idx.search("   \t\n") == []

    def test_query_only_short_tokens(self):
        idx = populated_index()
        # default min_token_length=2; single chars filtered.
        assert idx.search("a") == []

    def test_empty_field_value(self):
        idx = make_index()
        idx.add("d1", {"title": ""})
        assert idx.search("anything") == []
        assert idx.exists("d1")

    def test_add_with_no_fields(self):
        idx = make_index()
        idx.add("d1", {})
        assert idx.exists("d1")
        assert idx.search("anything") == []

    def test_tie_break_by_doc_id_alphabetically(self):
        idx = make_index()
        idx.add("zeta", {"body": "alpha"})
        idx.add("alpha", {"body": "alpha"})
        idx.add("mid", {"body": "alpha"})
        hits = idx.search("alpha")
        # All same score; doc_id alphabetic order.
        assert [h.doc_id for h in hits] == ["alpha", "mid", "zeta"]

    def test_unicode_tokens(self):
        idx = make_index()
        idx.add("d1", {"body": "Привет мир"})
        assert any(h.doc_id == "d1" for h in idx.search("привет"))

    def test_punctuation_stripped(self):
        idx = make_index()
        idx.add("d1", {"body": "hello, world!"})
        assert any(h.doc_id == "d1" for h in idx.search("hello"))
        assert any(h.doc_id == "d1" for h in idx.search("world"))

    def test_search_field_no_matches(self):
        idx = make_index()
        idx.add("d1", {"title": "alpha"})
        assert idx.search_field("nothing", "title") == []
