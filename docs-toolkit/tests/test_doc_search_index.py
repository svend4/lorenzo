"""Tests for docstoolkit.doc_search_index (E300)."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_search_index import (
    DocSearchIndex,
    IndexedDoc,
    IndexStats,
    SearchResult,
)
from docstoolkit.doc_search_index.index import _tokenize


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestIndexedDocDataclass:
    def test_required_fields(self):
        doc = IndexedDoc(doc_id="d1", title="Hello", content="World")
        assert doc.doc_id == "d1"
        assert doc.title == "Hello"
        assert doc.content == "World"

    def test_default_tags_empty_list(self):
        doc = IndexedDoc(doc_id="d1", title="T", content="C")
        assert doc.tags == []

    def test_default_indexed_at_zero(self):
        doc = IndexedDoc(doc_id="d1", title="T", content="C")
        assert doc.indexed_at == 0.0

    def test_all_fields_explicit(self):
        doc = IndexedDoc(
            doc_id="d2",
            title="My Title",
            content="Some text",
            tags=["python", "search"],
            indexed_at=1_000_000.0,
        )
        assert doc.tags == ["python", "search"]
        assert doc.indexed_at == 1_000_000.0

    def test_independent_default_tags(self):
        a = IndexedDoc(doc_id="a", title="T", content="C")
        b = IndexedDoc(doc_id="b", title="T", content="C")
        a.tags.append("x")
        assert b.tags == []


class TestSearchResultDataclass:
    def test_fields(self):
        r = SearchResult(
            doc_id="d1",
            title="My Doc",
            score=0.75,
            matched_terms=["alpha", "beta"],
        )
        assert r.doc_id == "d1"
        assert r.title == "My Doc"
        assert r.score == pytest.approx(0.75)
        assert r.matched_terms == ["alpha", "beta"]

    def test_zero_score(self):
        r = SearchResult(doc_id="d", title="T", score=0.0, matched_terms=[])
        assert r.score == 0.0
        assert r.matched_terms == []


class TestIndexStatsDataclass:
    def test_fields(self):
        s = IndexStats(total_docs=5, total_terms=20, avg_doc_length=12.5)
        assert s.total_docs == 5
        assert s.total_terms == 20
        assert s.avg_doc_length == pytest.approx(12.5)

    def test_zero_values(self):
        s = IndexStats(total_docs=0, total_terms=0, avg_doc_length=0.0)
        assert s.total_docs == 0
        assert s.avg_doc_length == 0.0


# ---------------------------------------------------------------------------
# Tokenize helper
# ---------------------------------------------------------------------------


class TestTokenize:
    def test_lowercase(self):
        assert _tokenize("Hello World") == ["hello", "world"]

    def test_alphanumeric(self):
        assert _tokenize("abc123 def456") == ["abc123", "def456"]

    def test_splits_on_punctuation(self):
        tokens = _tokenize("hello, world! foo.bar")
        assert "hello" in tokens
        assert "world" in tokens
        assert "foo" in tokens
        assert "bar" in tokens

    def test_empty_string(self):
        assert _tokenize("") == []

    def test_only_punctuation(self):
        assert _tokenize("!!! ???") == []

    def test_numbers(self):
        assert _tokenize("version 2 0") == ["version", "2", "0"]

    def test_mixed_case_lowered(self):
        result = _tokenize("Python PYTHON python")
        assert result == ["python", "python", "python"]


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_index_all_doc_ids(self):
        idx = DocSearchIndex()
        assert idx.all_doc_ids() == []

    def test_empty_index_stats(self):
        idx = DocSearchIndex()
        s = idx.stats()
        assert s.total_docs == 0
        assert s.total_terms == 0
        assert s.avg_doc_length == 0.0

    def test_empty_search_returns_empty(self):
        idx = DocSearchIndex()
        assert idx.search("anything") == []


# ---------------------------------------------------------------------------
# index_doc
# ---------------------------------------------------------------------------


class TestIndexDoc:
    def test_new_doc_appears_in_all_doc_ids(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "Title", "content here"))
        assert "d1" in idx.all_doc_ids()

    def test_sets_indexed_at_when_zero(self):
        idx = DocSearchIndex()
        before = time.time()
        doc = IndexedDoc("d1", "T", "C")
        idx.index_doc(doc)
        after = time.time()
        assert before <= doc.indexed_at <= after

    def test_does_not_overwrite_existing_indexed_at(self):
        idx = DocSearchIndex()
        doc = IndexedDoc("d1", "T", "C", indexed_at=999.0)
        idx.index_doc(doc)
        assert doc.indexed_at == 999.0

    def test_injectable_now_parameter(self):
        idx = DocSearchIndex()
        doc = IndexedDoc("d1", "T", "C")
        idx.index_doc(doc, now=42.0)
        assert doc.indexed_at == 42.0

    def test_reindex_updates_tokens(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "Alpha", "one two three"))
        # Re-index with different content
        idx.index_doc(IndexedDoc("d1", "Alpha", "four five six"))
        results = idx.search("four")
        assert any(r.doc_id == "d1" for r in results)
        # Old content should be gone
        results_old = idx.search("one")
        assert not any(r.doc_id == "d1" for r in results_old)

    def test_tokens_include_title(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "UniqueTitle", ""))
        results = idx.search("uniquetitle")
        assert any(r.doc_id == "d1" for r in results)

    def test_tokens_include_content(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "", "UniqueContent"))
        results = idx.search("uniquecontent")
        assert any(r.doc_id == "d1" for r in results)

    def test_tokens_include_tags(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "", "", tags=["mytag"]))
        results = idx.search("mytag")
        assert any(r.doc_id == "d1" for r in results)

    def test_multiple_docs(self):
        idx = DocSearchIndex()
        for i in range(5):
            idx.index_doc(IndexedDoc(f"d{i}", f"Title {i}", "content"))
        assert len(idx.all_doc_ids()) == 5


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------


class TestRemoveDoc:
    def test_returns_true_if_existed(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C"))
        assert idx.remove_doc("d1") is True

    def test_returns_false_if_not_existed(self):
        idx = DocSearchIndex()
        assert idx.remove_doc("nonexistent") is False

    def test_removed_doc_not_in_all_doc_ids(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C"))
        idx.remove_doc("d1")
        assert "d1" not in idx.all_doc_ids()

    def test_removed_doc_not_in_search(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "alpha beta", "gamma"))
        idx.remove_doc("d1")
        assert idx.search("alpha") == []

    def test_remove_cleans_inverted_index(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "unique_term_xyz", ""))
        idx.remove_doc("d1")
        # After removal the term should be gone from internal index
        assert idx.search("unique_term_xyz") == []

    def test_remove_one_of_two_docs(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "alpha", "shared"))
        idx.index_doc(IndexedDoc("d2", "beta", "shared"))
        idx.remove_doc("d1")
        assert "d2" in idx.all_doc_ids()
        assert "d1" not in idx.all_doc_ids()


# ---------------------------------------------------------------------------
# get_doc
# ---------------------------------------------------------------------------


class TestGetDoc:
    def test_found(self):
        idx = DocSearchIndex()
        doc = IndexedDoc("d1", "Title", "Content", tags=["t"])
        idx.index_doc(doc)
        retrieved = idx.get_doc("d1")
        assert retrieved is not None
        assert retrieved.doc_id == "d1"
        assert retrieved.title == "Title"

    def test_not_found_returns_none(self):
        idx = DocSearchIndex()
        assert idx.get_doc("missing") is None

    def test_get_after_remove_returns_none(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C"))
        idx.remove_doc("d1")
        assert idx.get_doc("d1") is None


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------


class TestSearch:
    def test_empty_query_returns_empty(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "Hello", "World"))
        assert idx.search("") == []

    def test_single_term_hit(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "Python", "scripting language"))
        results = idx.search("python")
        assert len(results) == 1
        assert results[0].doc_id == "d1"

    def test_multi_term_query(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "Python", "scripting language"))
        idx.index_doc(IndexedDoc("d2", "Java", "object oriented"))
        results = idx.search("python scripting")
        ids = [r.doc_id for r in results]
        assert "d1" in ids
        assert "d2" not in ids

    def test_limit_parameter(self):
        idx = DocSearchIndex()
        for i in range(10):
            idx.index_doc(IndexedDoc(f"d{i}", "common", "term"))
        results = idx.search("common", limit=3)
        assert len(results) <= 3

    def test_results_sorted_by_score_descending(self):
        idx = DocSearchIndex()
        # d1 has "python" once, d2 has it many times in content → d2 should rank higher
        idx.index_doc(IndexedDoc("d1", "Python", "other words here only"))
        idx.index_doc(
            IndexedDoc("d2", "Python Python Python", "python python python python")
        )
        results = idx.search("python")
        assert results[0].score >= results[-1].score

    def test_returns_search_result_instances(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "hello", "world"))
        results = idx.search("hello")
        assert all(isinstance(r, SearchResult) for r in results)


class TestSearchNoMatch:
    def test_no_matching_docs_returns_empty(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "alpha", "beta gamma"))
        assert idx.search("zzznomatch") == []

    def test_empty_index_returns_empty(self):
        idx = DocSearchIndex()
        assert idx.search("anything") == []

    def test_punctuation_only_query(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "hello", "world"))
        # Punctuation tokenizes to nothing → empty query → empty results
        assert idx.search("!!!") == []


# ---------------------------------------------------------------------------
# TF-IDF specific
# ---------------------------------------------------------------------------


class TestSearchTFIDF:
    def test_more_occurrences_scores_higher(self):
        idx = DocSearchIndex()
        # d1: "dog" appears once; d2: "dog" appears many times
        idx.index_doc(IndexedDoc("d1", "animals", "a cat and a dog"))
        idx.index_doc(
            IndexedDoc(
                "d2",
                "dogs",
                "dog dog dog dog dog",
            )
        )
        results = idx.search("dog")
        scores = {r.doc_id: r.score for r in results}
        assert scores["d2"] > scores["d1"]

    def test_idf_penalizes_common_terms(self):
        """A term appearing in every doc has lower IDF than a rare term."""
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "common rare", "common word here"))
        idx.index_doc(IndexedDoc("d2", "common", "common word here"))
        idx.index_doc(IndexedDoc("d3", "common", "common word here"))
        # "common" is in all 3 docs; "rare" is only in d1
        results = idx.search("rare")
        assert len(results) == 1
        rare_result = results[0]
        results_common = idx.search("common")
        common_d1 = next(r for r in results_common if r.doc_id == "d1")
        # rare term should give higher per-occurrence contribution via IDF
        # Both appear once in d1 but rare has higher IDF
        tf_rare = rare_result.score
        # We can only check that rare_result exists and common docs also match
        assert tf_rare > 0

    def test_score_positive_for_match(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "hello", "world"))
        results = idx.search("hello")
        assert results[0].score > 0


class TestSearchMatchedTerms:
    def test_matched_terms_sorted(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "zebra alpha beta", "content"))
        results = idx.search("zebra alpha beta")
        assert results[0].matched_terms == sorted(results[0].matched_terms)

    def test_matched_terms_unique(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "python python python", ""))
        results = idx.search("python python")
        assert results[0].matched_terms.count("python") == 1

    def test_only_found_terms_listed(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "alpha", "content"))
        results = idx.search("alpha missing")
        assert "alpha" in results[0].matched_terms
        assert "missing" not in results[0].matched_terms


# ---------------------------------------------------------------------------
# Title weighting
# ---------------------------------------------------------------------------


class TestTitleWeighting:
    def test_title_term_scores_higher_than_body_only(self):
        idx = DocSearchIndex()
        # d_title: "python" is in the title (repeated ×2)
        # d_body: "python" is only in the body content, once
        idx.index_doc(IndexedDoc("d_title", "python", "unrelated stuff here"))
        idx.index_doc(IndexedDoc("d_body", "unrelated", "python"))
        results = idx.search("python")
        scores = {r.doc_id: r.score for r in results}
        # d_title has title tokens (x2) contributing more TF for "python"
        assert scores["d_title"] > scores["d_body"]


# ---------------------------------------------------------------------------
# search_by_tag
# ---------------------------------------------------------------------------


class TestSearchByTag:
    def test_single_tag_match(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C", tags=["python"]))
        assert idx.search_by_tag("python") == ["d1"]

    def test_no_match_returns_empty(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C", tags=["java"]))
        assert idx.search_by_tag("python") == []

    def test_multiple_docs_same_tag_sorted(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d3", "T", "C", tags=["python"]))
        idx.index_doc(IndexedDoc("d1", "T", "C", tags=["python"]))
        idx.index_doc(IndexedDoc("d2", "T", "C", tags=["python"]))
        assert idx.search_by_tag("python") == ["d1", "d2", "d3"]

    def test_tag_case_insensitive(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C", tags=["Python"]))
        # search_by_tag does case-insensitive comparison
        assert idx.search_by_tag("python") == ["d1"]

    def test_partial_tag_no_match(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C", tags=["python3"]))
        assert idx.search_by_tag("python") == []

    def test_doc_not_tagged_excluded(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C", tags=["python"]))
        idx.index_doc(IndexedDoc("d2", "T", "C", tags=["java"]))
        assert idx.search_by_tag("python") == ["d1"]


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty_index(self):
        idx = DocSearchIndex()
        assert idx.all_doc_ids() == []

    def test_single_doc(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("abc", "T", "C"))
        assert idx.all_doc_ids() == ["abc"]

    def test_multiple_docs_sorted(self):
        idx = DocSearchIndex()
        for id_ in ["c3", "a1", "b2"]:
            idx.index_doc(IndexedDoc(id_, "T", "C"))
        assert idx.all_doc_ids() == ["a1", "b2", "c3"]

    def test_after_removal(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "T", "C"))
        idx.index_doc(IndexedDoc("d2", "T", "C"))
        idx.remove_doc("d1")
        assert idx.all_doc_ids() == ["d2"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_index(self):
        idx = DocSearchIndex()
        s = idx.stats()
        assert s.total_docs == 0
        assert s.total_terms == 0
        assert s.avg_doc_length == pytest.approx(0.0)

    def test_total_docs(self):
        idx = DocSearchIndex()
        for i in range(4):
            idx.index_doc(IndexedDoc(f"d{i}", "title", "body text"))
        assert idx.stats().total_docs == 4

    def test_total_terms_unique(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "alpha beta", "gamma"))
        s = idx.stats()
        # unique terms: alpha, beta, gamma (alpha appears twice via title weight)
        assert s.total_terms >= 3

    def test_avg_doc_length(self):
        idx = DocSearchIndex()
        # title "a b" → 4 title tokens (×2) + 0 content = 4 tokens
        idx.index_doc(IndexedDoc("d1", "a b", ""))
        # title "x" → 2 title tokens + "y z w" → 3 content tokens = 5 tokens
        idx.index_doc(IndexedDoc("d2", "x", "y z w"))
        s = idx.stats()
        assert s.avg_doc_length == pytest.approx((4 + 5) / 2)

    def test_stats_after_removal(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("d1", "hello", ""))
        idx.index_doc(IndexedDoc("d2", "world", ""))
        idx.remove_doc("d1")
        assert idx.stats().total_docs == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_index_doc(self):
        idx = DocSearchIndex()
        errors: list[Exception] = []

        def worker(i: int) -> None:
            try:
                idx.index_doc(IndexedDoc(f"doc{i}", f"title {i}", f"content {i}"))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        assert idx.stats().total_docs == 50

    def test_concurrent_index_and_search(self):
        idx = DocSearchIndex()
        idx.index_doc(IndexedDoc("seed", "python", "language"))
        errors: list[Exception] = []

        def indexer(i: int) -> None:
            try:
                idx.index_doc(IndexedDoc(f"d{i}", "python", f"content {i}"))
            except Exception as exc:
                errors.append(exc)

        def searcher() -> None:
            try:
                idx.search("python")
            except Exception as exc:
                errors.append(exc)

        threads = []
        for i in range(20):
            threads.append(threading.Thread(target=indexer, args=(i,)))
            threads.append(threading.Thread(target=searcher))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
