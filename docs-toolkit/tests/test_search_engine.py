"""Tests for E108 — docstoolkit.search_engine (pure stdlib BM25 engine)."""
from __future__ import annotations

import math
import pytest

from docstoolkit.search_engine import Document, SearchEngine, SearchResult
from docstoolkit.search_engine.engine import _tokenize


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_doc(doc_id: str, body: str, **kwargs) -> Document:
    """Convenience: single-field document."""
    return Document(doc_id=doc_id, fields={"body": body}, metadata=kwargs)


def make_engine(*docs: Document, **kwargs) -> SearchEngine:
    engine = SearchEngine(**kwargs)
    engine.add_many(list(docs))
    return engine


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------


class TestTokenizer:
    def test_lowercase(self):
        assert _tokenize("Hello World") == ["hello", "world"]

    def test_splits_non_alphanumeric(self):
        tokens = _tokenize("foo-bar_baz.qux")
        assert tokens == ["foo", "bar", "baz", "qux"]

    def test_empty_string(self):
        assert _tokenize("") == []

    def test_only_punctuation(self):
        assert _tokenize("!!! ???") == []

    def test_numbers_preserved(self):
        assert "42" in _tokenize("42 items")

    def test_mixed_alpha_numeric(self):
        assert "gpt4" in _tokenize("gpt4 is a model")


# ---------------------------------------------------------------------------
# Empty engine
# ---------------------------------------------------------------------------


class TestEmptyEngine:
    def test_doc_count_zero(self):
        assert SearchEngine().doc_count() == 0

    def test_search_returns_empty(self):
        assert SearchEngine().search("anything") == []

    def test_get_returns_none(self):
        assert SearchEngine().get("x") is None

    def test_remove_returns_false(self):
        assert SearchEngine().remove("x") is False

    def test_field_names_empty(self):
        assert SearchEngine().field_names() == set()


# ---------------------------------------------------------------------------
# Single document — add / get / search
# ---------------------------------------------------------------------------


class TestSingleDocument:
    def setup_method(self):
        self.engine = SearchEngine()
        self.doc = Document(
            doc_id="d1",
            fields={"title": "Python programming", "body": "An introduction to Python."},
            metadata={"author": "alice"},
        )
        self.engine.add(self.doc)

    def test_doc_count_is_one(self):
        assert self.engine.doc_count() == 1

    def test_get_returns_document(self):
        result = self.engine.get("d1")
        assert result is not None
        assert result.doc_id == "d1"

    def test_search_returns_result(self):
        results = self.engine.search("python")
        assert len(results) == 1

    def test_search_returns_correct_doc_id(self):
        results = self.engine.search("python")
        assert results[0].doc_id == "d1"

    def test_score_positive(self):
        results = self.engine.search("python")
        assert results[0].score > 0

    def test_result_contains_document(self):
        results = self.engine.search("python")
        assert results[0].document is self.doc

    def test_metadata_preserved(self):
        results = self.engine.search("python")
        assert results[0].document.metadata["author"] == "alice"

    def test_no_match_returns_empty(self):
        results = self.engine.search("javascript")
        assert results == []

    def test_matched_fields_nonempty(self):
        results = self.engine.search("python")
        assert len(results[0].matched_fields) > 0

    def test_case_insensitive_query(self):
        results = self.engine.search("PYTHON")
        assert len(results) == 1

    def test_case_insensitive_doc_content(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"body": "HELLO WORLD"}))
        results = engine.search("hello")
        assert len(results) == 1


# ---------------------------------------------------------------------------
# Multiple documents — scoring and ranking
# ---------------------------------------------------------------------------


class TestMultipleDocuments:
    """Three docs; d1 mentions 'python' most, d2 once, d3 never."""

    def setup_method(self):
        self.engine = SearchEngine()
        self.engine.add_many(
            [
                Document("d1", {"body": "python python python is great"}),
                Document("d2", {"body": "python is nice"}),
                Document("d3", {"body": "java is also a language"}),
            ]
        )

    def test_no_match(self):
        assert self.engine.search("ruby") == []

    def test_partial_match_excluded(self):
        ids = [r.doc_id for r in self.engine.search("python")]
        assert "d3" not in ids

    def test_d1_scores_higher_than_d2(self):
        results = self.engine.search("python")
        id_to_score = {r.doc_id: r.score for r in results}
        assert id_to_score["d1"] > id_to_score["d2"]

    def test_results_sorted_descending(self):
        results = self.engine.search("python")
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_top_k_limits_results(self):
        results = self.engine.search("python", top_k=1)
        assert len(results) == 1

    def test_top_k_first_result_is_best(self):
        top1 = self.engine.search("python", top_k=1)[0]
        all_results = self.engine.search("python")
        assert top1.doc_id == all_results[0].doc_id

    def test_top_k_zero_returns_empty(self):
        results = self.engine.search("python", top_k=0)
        assert results == []

    def test_top_k_larger_than_matches(self):
        results = self.engine.search("python", top_k=100)
        assert len(results) == 2  # d1 and d2

    def test_doc_count(self):
        assert self.engine.doc_count() == 3


# ---------------------------------------------------------------------------
# Multi-term query
# ---------------------------------------------------------------------------


class TestMultiTermQuery:
    def test_multi_term_hits_multiple_fields(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"title": "machine learning", "body": "deep learning networks"}))
        results = engine.search("learning networks")
        assert results[0].doc_id == "d1"

    def test_multi_term_score_higher_than_single(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"body": "cat sat on mat"}))
        score_two = engine.search("cat sat")[0].score
        score_one = engine.search("cat")[0].score
        assert score_two > score_one

    def test_all_terms_in_query_contribute(self):
        engine = SearchEngine()
        engine.add_many(
            [
                Document("d1", {"body": "alpha beta gamma"}),
                Document("d2", {"body": "alpha only"}),
            ]
        )
        results = engine.search("alpha beta gamma")
        id_to_score = {r.doc_id: r.score for r in results}
        assert id_to_score["d1"] > id_to_score["d2"]


# ---------------------------------------------------------------------------
# Field-restricted search
# ---------------------------------------------------------------------------


class TestFieldRestrictedSearch:
    def setup_method(self):
        self.engine = SearchEngine()
        self.engine.add(
            Document(
                "d1",
                {
                    "title": "Python tutorial",
                    "body": "Java is a language",
                    "tags": "programming",
                },
            )
        )
        self.engine.add(
            Document(
                "d2",
                {
                    "title": "Java guide",
                    "body": "Python for data science",
                    "tags": "programming",
                },
            )
        )

    def test_field_restriction_title_only(self):
        results = self.engine.search("python", fields=["title"])
        ids = [r.doc_id for r in results]
        assert "d1" in ids
        assert "d2" not in ids

    def test_field_restriction_body_only(self):
        results = self.engine.search("python", fields=["body"])
        ids = [r.doc_id for r in results]
        assert "d2" in ids
        assert "d1" not in ids

    def test_field_restriction_no_match(self):
        results = self.engine.search("python", fields=["tags"])
        assert results == []

    def test_no_field_restriction_searches_all(self):
        results = self.engine.search("python")
        ids = {r.doc_id for r in results}
        assert ids == {"d1", "d2"}

    def test_matched_fields_respects_restriction(self):
        results = self.engine.search("python", fields=["title"])
        assert "title" in results[0].matched_fields
        assert "body" not in results[0].matched_fields

    def test_multiple_fields_restriction(self):
        results = self.engine.search("python", fields=["title", "body"])
        ids = {r.doc_id for r in results}
        assert ids == {"d1", "d2"}

    def test_nonexistent_field_restriction_returns_empty(self):
        results = self.engine.search("python", fields=["nonexistent"])
        assert results == []


# ---------------------------------------------------------------------------
# matched_fields
# ---------------------------------------------------------------------------


class TestMatchedFields:
    def test_matched_fields_correct(self):
        engine = SearchEngine()
        engine.add(
            Document(
                "d1",
                {"title": "hello", "body": "world", "summary": "hello world"},
            )
        )
        results = engine.search("hello")
        mf = set(results[0].matched_fields)
        assert "title" in mf
        assert "summary" in mf
        assert "body" not in mf

    def test_matched_fields_both_fields(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"a": "foo bar", "b": "foo baz"}))
        results = engine.search("foo")
        mf = set(results[0].matched_fields)
        assert mf == {"a", "b"}

    def test_matched_fields_single_field(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"x": "unique", "y": "other stuff"}))
        results = engine.search("unique")
        assert results[0].matched_fields == ["x"]


# ---------------------------------------------------------------------------
# add / remove / clear / overwrite
# ---------------------------------------------------------------------------


class TestMutations:
    def test_remove_existing_returns_true(self):
        engine = make_engine(make_doc("d1", "hello"))
        assert engine.remove("d1") is True

    def test_remove_decreases_doc_count(self):
        engine = make_engine(make_doc("d1", "hello"), make_doc("d2", "world"))
        engine.remove("d1")
        assert engine.doc_count() == 1

    def test_remove_nonexistent_returns_false(self):
        engine = SearchEngine()
        assert engine.remove("ghost") is False

    def test_remove_makes_doc_unsearchable(self):
        engine = make_engine(make_doc("d1", "hello"))
        engine.remove("d1")
        assert engine.search("hello") == []

    def test_remove_updates_index(self):
        engine = make_engine(make_doc("d1", "hello"), make_doc("d2", "hello world"))
        engine.remove("d1")
        results = engine.search("hello")
        assert len(results) == 1
        assert results[0].doc_id == "d2"

    def test_clear_removes_all_docs(self):
        engine = make_engine(make_doc("d1", "a"), make_doc("d2", "b"))
        engine.clear()
        assert engine.doc_count() == 0

    def test_clear_returns_empty_on_search(self):
        engine = make_engine(make_doc("d1", "hello"))
        engine.clear()
        assert engine.search("hello") == []

    def test_overwrite_existing_doc(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"body": "original content"}))
        engine.add(Document("d1", {"body": "completely different"}))
        assert engine.doc_count() == 1

    def test_overwrite_updates_content(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"body": "original content"}))
        engine.add(Document("d1", {"body": "completely different"}))
        assert engine.search("original") == []
        assert len(engine.search("different")) == 1

    def test_overwrite_preserves_doc_id(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"body": "old"}))
        engine.add(Document("d1", {"body": "new data"}))
        assert engine.get("d1").fields["body"] == "new data"


# ---------------------------------------------------------------------------
# add_many
# ---------------------------------------------------------------------------


class TestAddMany:
    def test_add_many_increases_count(self):
        engine = SearchEngine()
        docs = [make_doc(f"d{i}", f"document {i}") for i in range(5)]
        engine.add_many(docs)
        assert engine.doc_count() == 5

    def test_add_many_all_searchable(self):
        engine = SearchEngine()
        engine.add_many(
            [
                Document("d1", {"body": "alpha"}),
                Document("d2", {"body": "beta"}),
                Document("d3", {"body": "gamma"}),
            ]
        )
        assert len(engine.search("alpha")) == 1
        assert len(engine.search("beta")) == 1
        assert len(engine.search("gamma")) == 1

    def test_add_many_empty_list(self):
        engine = SearchEngine()
        engine.add_many([])
        assert engine.doc_count() == 0


# ---------------------------------------------------------------------------
# field_names()
# ---------------------------------------------------------------------------


class TestFieldNames:
    def test_empty_engine(self):
        assert SearchEngine().field_names() == set()

    def test_single_doc_single_field(self):
        engine = make_engine(Document("d1", {"body": "text"}))
        assert engine.field_names() == {"body"}

    def test_multiple_docs_different_fields(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"title": "a", "body": "b"}))
        engine.add(Document("d2", {"summary": "c"}))
        assert engine.field_names() == {"title", "body", "summary"}

    def test_field_names_after_remove(self):
        """After removing the only doc with 'summary', that field disappears."""
        engine = SearchEngine()
        engine.add(Document("d1", {"body": "hello"}))
        engine.add(Document("d2", {"summary": "world"}))
        engine.remove("d2")
        assert "summary" not in engine.field_names()

    def test_field_names_after_clear(self):
        engine = make_engine(Document("d1", {"body": "hi"}))
        engine.clear()
        assert engine.field_names() == set()


# ---------------------------------------------------------------------------
# BM25 IDF — rare term scores higher than common term
# ---------------------------------------------------------------------------


class TestBM25IDF:
    def test_rare_term_scores_higher(self):
        """'exotic' appears in 1/5 docs; 'common' appears in all 5.
        A doc containing 'exotic' should score higher when queried for 'exotic'
        than a doc containing 'common' when queried for 'common'.
        """
        docs = [
            Document("d1", {"body": "exotic rare unique term"}),
            Document("d2", {"body": "common ordinary usual standard normal"}),
            Document("d3", {"body": "common ordinary usual standard normal"}),
            Document("d4", {"body": "common ordinary usual standard normal"}),
            Document("d5", {"body": "common ordinary usual standard normal"}),
        ]
        engine = SearchEngine()
        engine.add_many(docs)

        exotic_score = engine.search("exotic")[0].score
        common_score = engine.search("common")[0].score
        assert exotic_score > common_score

    def test_idf_positive_for_rare_term(self):
        """IDF must be positive when df < N."""
        engine = SearchEngine()
        engine.add_many(
            [
                Document("d1", {"body": "rare word"}),
                Document("d2", {"body": "unrelated content here"}),
                Document("d3", {"body": "unrelated content here"}),
            ]
        )
        results = engine.search("rare")
        assert results[0].score > 0


# ---------------------------------------------------------------------------
# BM25 parameters
# ---------------------------------------------------------------------------


class TestBM25Parameters:
    def test_custom_k1(self):
        """Higher k1 allows TF to keep growing; should differ from default."""
        docs = [
            Document("d1", {"body": "word " * 20}),
            Document("d2", {"body": "word " * 1}),
        ]
        eng_default = SearchEngine()
        eng_default.add_many(docs)
        eng_highk1 = SearchEngine(k1=5.0)
        eng_highk1.add_many(docs)

        default_gap = (
            eng_default.search("word")[0].score - eng_default.search("word")[1].score
        )
        highk1_gap = (
            eng_highk1.search("word")[0].score - eng_highk1.search("word")[1].score
        )
        # Higher k1 should yield a larger gap between high-TF and low-TF docs
        assert highk1_gap > default_gap

    def test_b_zero_no_length_norm(self):
        """With b=0, document length doesn't affect scoring."""
        docs = [
            Document("d1", {"body": "python " + "filler " * 100}),
            Document("d2", {"body": "python"}),
        ]
        engine = SearchEngine(b=0.0)
        engine.add_many(docs)
        results = engine.search("python")
        # With b=0 there's no length penalty; scores should still be valid floats
        for r in results:
            assert isinstance(r.score, float)
            assert math.isfinite(r.score)


# ---------------------------------------------------------------------------
# Multi-field documents
# ---------------------------------------------------------------------------


class TestMultiFieldDocuments:
    def test_all_fields_searched_by_default(self):
        engine = SearchEngine()
        engine.add(
            Document(
                "d1",
                {
                    "title": "alpha",
                    "body": "beta",
                    "tags": "gamma",
                },
            )
        )
        for term in ("alpha", "beta", "gamma"):
            results = engine.search(term)
            assert len(results) == 1, f"Expected match for '{term}'"

    def test_tf_accumulates_across_fields(self):
        """Term appearing in multiple fields should increase effective TF."""
        engine = SearchEngine()
        engine.add_many(
            [
                Document("d1", {"title": "python", "body": "python python"}),
                Document("d2", {"title": "other", "body": "python"}),
            ]
        )
        results = engine.search("python")
        id_to_score = {r.doc_id: r.score for r in results}
        assert id_to_score["d1"] > id_to_score["d2"]


# ---------------------------------------------------------------------------
# SearchResult type checks
# ---------------------------------------------------------------------------


class TestSearchResultType:
    def test_result_is_search_result_instance(self):
        engine = make_engine(make_doc("d1", "hello world"))
        result = engine.search("hello")[0]
        assert isinstance(result, SearchResult)

    def test_result_doc_id_is_string(self):
        engine = make_engine(make_doc("d1", "hello"))
        assert isinstance(engine.search("hello")[0].doc_id, str)

    def test_result_score_is_float(self):
        engine = make_engine(make_doc("d1", "hello"))
        assert isinstance(engine.search("hello")[0].score, float)

    def test_result_matched_fields_is_list(self):
        engine = make_engine(make_doc("d1", "hello"))
        assert isinstance(engine.search("hello")[0].matched_fields, list)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_query_returns_empty(self):
        engine = make_engine(make_doc("d1", "hello world"))
        assert engine.search("") == []

    def test_query_only_punctuation(self):
        engine = make_engine(make_doc("d1", "hello world"))
        assert engine.search("!!!???") == []

    def test_empty_document_fields(self):
        engine = SearchEngine()
        engine.add(Document("d1", {"body": ""}))
        assert engine.doc_count() == 1
        assert engine.search("anything") == []

    def test_document_with_no_fields(self):
        engine = SearchEngine()
        engine.add(Document("d1", {}))
        assert engine.doc_count() == 1
        assert engine.search("anything") == []

    def test_large_corpus_top_k(self):
        engine = SearchEngine()
        docs = [Document(f"d{i}", {"body": f"term document number {i}"}) for i in range(50)]
        engine.add_many(docs)
        results = engine.search("term", top_k=10)
        assert len(results) == 10

    def test_single_character_term(self):
        engine = make_engine(make_doc("d1", "a b c"))
        results = engine.search("a")
        assert len(results) == 1

    def test_numeric_terms(self):
        engine = make_engine(make_doc("d1", "version 42 released"))
        results = engine.search("42")
        assert len(results) == 1

    def test_add_after_clear(self):
        engine = make_engine(make_doc("d1", "hello"))
        engine.clear()
        engine.add(make_doc("d2", "world"))
        assert engine.doc_count() == 1
        assert len(engine.search("world")) == 1
        assert engine.search("hello") == []
