"""Tests for E269 doc_index_manager."""
from __future__ import annotations

import pytest

from docstoolkit.doc_index_manager import (
    DocIndexManager,
    IndexDefinition,
    IndexedTerm,
    IndexKind,
)


# ---------------------------------------------------------------------------
# Extractor helpers
# ---------------------------------------------------------------------------
def keyword_extractor(doc_id, doc_data):
    text = doc_data.get("text", "")
    for word in text.split():
        yield word.lower(), word


def tag_extractor(doc_id, doc_data):
    for tag in doc_data.get("tags", []):
        yield tag, tag


def author_extractor(doc_id, doc_data):
    author = doc_data.get("author")
    if author:
        yield author, author


def numeric_extractor(doc_id, doc_data):
    if "year" in doc_data:
        yield str(doc_data["year"]), doc_data["year"]


def empty_extractor(doc_id, doc_data):
    return []


def failing_extractor(doc_id, doc_data):
    raise RuntimeError("boom")


# ---------------------------------------------------------------------------
class TestIndexKind:
    def test_keyword(self):
        assert IndexKind.KEYWORD.value == "keyword"

    def test_metadata(self):
        assert IndexKind.METADATA.value == "metadata"

    def test_full_text(self):
        assert IndexKind.FULL_TEXT.value == "full_text"

    def test_tags(self):
        assert IndexKind.TAGS.value == "tags"

    def test_numeric(self):
        assert IndexKind.NUMERIC.value == "numeric"


class TestIndexDefinition:
    def test_basic(self):
        d = IndexDefinition("a", IndexKind.KEYWORD, keyword_extractor)
        assert d.name == "a"
        assert d.kind is IndexKind.KEYWORD
        assert d.enabled is True

    def test_disabled(self):
        d = IndexDefinition("a", IndexKind.TAGS, tag_extractor, enabled=False)
        assert d.enabled is False


class TestIndexedTerm:
    def test_attributes(self):
        t = IndexedTerm(index_name="k", term="hello", value="hello", doc_id="d1")
        assert t.index_name == "k"
        assert t.term == "hello"
        assert t.value == "hello"
        assert t.doc_id == "d1"


class TestRegisterIndex:
    def test_register(self):
        m = DocIndexManager()
        d = m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        assert isinstance(d, IndexDefinition)
        assert d.name == "kw"

    def test_register_returns_enabled(self):
        m = DocIndexManager()
        d = m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        assert d.enabled is True

    def test_register_multiple(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        assert m.total_indexes == 2

    def test_register_overwrite(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("kw", IndexKind.TAGS, tag_extractor)
        assert m.total_indexes == 1
        assert m.get_index("kw").kind is IndexKind.TAGS


class TestUnregisterIndex:
    def test_unregister_existing(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        assert m.unregister_index("kw") is True

    def test_unregister_missing(self):
        m = DocIndexManager()
        assert m.unregister_index("nope") is False

    def test_unregister_clears_data(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello world"})
        m.unregister_index("kw")
        assert m.terms_for_doc("d1", "kw") == []


class TestEnableDisable:
    def test_disable(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        assert m.disable_index("kw") is True
        assert m.get_index("kw").enabled is False

    def test_enable(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.disable_index("kw")
        assert m.enable_index("kw") is True
        assert m.get_index("kw").enabled is True

    def test_disable_missing(self):
        m = DocIndexManager()
        assert m.disable_index("nope") is False

    def test_enable_missing(self):
        m = DocIndexManager()
        assert m.enable_index("nope") is False

    def test_disabled_index_not_indexed(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.disable_index("kw")
        res = m.index_doc("d1", {"text": "hello world"})
        assert "kw" not in res


class TestIndexDoc:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        res = m.index_doc("d1", {"text": "hello world"})
        assert res["kw"] == 2

    def test_multiple_indexes(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        res = m.index_doc("d1", {"text": "hi there", "tags": ["a", "b"]})
        assert res["kw"] == 2
        assert res["tags"] == 2

    def test_empty_extraction(self):
        m = DocIndexManager()
        m.register_index("emp", IndexKind.KEYWORD, empty_extractor)
        res = m.index_doc("d1", {})
        assert res["emp"] == 0

    def test_extraction_exception_caught(self):
        m = DocIndexManager()
        m.register_index("bad", IndexKind.KEYWORD, failing_extractor)
        # should not raise
        res = m.index_doc("d1", {})
        assert res["bad"] == 0

    def test_index_updates_doc_ids(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "x"})
        m.index_doc("d2", {"text": "y"})
        assert m.total_indexed_docs == 2


class TestUnindexDoc:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello world"})
        removed = m.unindex_doc("d1")
        assert removed == 2

    def test_unindex_unknown(self):
        m = DocIndexManager()
        assert m.unindex_doc("nope") == 0

    def test_unindex_removes_from_query(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello"})
        m.unindex_doc("d1")
        assert m.query("kw", "hello") == []


class TestReindexDoc:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello"})
        res = m.reindex_doc("d1", {"text": "world"})
        assert res["kw"] == 1
        assert m.query("kw", "hello") == []
        assert m.query("kw", "world") == ["d1"]

    def test_reindex_new_doc(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        res = m.reindex_doc("d1", {"text": "hi"})
        assert res["kw"] == 1


class TestQuery:
    def test_query_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello"})
        m.index_doc("d2", {"text": "hello world"})
        assert sorted(m.query("kw", "hello")) == ["d1", "d2"]

    def test_query_no_match(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello"})
        assert m.query("kw", "missing") == []

    def test_query_unknown_index(self):
        m = DocIndexManager()
        assert m.query("nope", "x") == []

    def test_query_single_doc(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "unique"})
        assert m.query("kw", "unique") == ["d1"]


class TestQueryMultiAnd:
    def test_and_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        m.index_doc("d1", {"text": "hello", "tags": ["red"]})
        m.index_doc("d2", {"text": "hello", "tags": ["blue"]})
        res = m.query_multi({"kw": "hello", "tags": "red"}, mode="AND")
        assert res == {"d1"}

    def test_and_no_intersection(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        m.index_doc("d1", {"text": "hi", "tags": ["a"]})
        m.index_doc("d2", {"text": "bye", "tags": ["b"]})
        res = m.query_multi({"kw": "hi", "tags": "b"}, mode="AND")
        assert res == set()

    def test_and_single_criterion(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello"})
        res = m.query_multi({"kw": "hello"}, mode="AND")
        assert res == {"d1"}


class TestQueryMultiOr:
    def test_or_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        m.index_doc("d1", {"text": "hi", "tags": ["a"]})
        m.index_doc("d2", {"text": "bye", "tags": ["b"]})
        res = m.query_multi({"kw": "hi", "tags": "b"}, mode="OR")
        assert res == {"d1", "d2"}

    def test_or_all_match(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hi"})
        m.index_doc("d2", {"text": "hi"})
        res = m.query_multi({"kw": "hi"}, mode="OR")
        assert res == {"d1", "d2"}

    def test_or_lowercase(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hi"})
        res = m.query_multi({"kw": "hi"}, mode="or")
        assert res == {"d1"}

    def test_invalid_mode(self):
        m = DocIndexManager()
        with pytest.raises(ValueError):
            m.query_multi({"x": "y"}, mode="XOR")

    def test_empty_criteria(self):
        m = DocIndexManager()
        assert m.query_multi({}) == set()


class TestTermsForIndex:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hello world"})
        terms = m.terms_for_index("kw")
        assert "hello" in terms
        assert "world" in terms

    def test_unknown_index(self):
        m = DocIndexManager()
        assert m.terms_for_index("nope") == []

    def test_sorted(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "zebra apple"})
        terms = m.terms_for_index("kw")
        assert terms == sorted(terms)


class TestTermsForDoc:
    def test_all_indexes(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        m.index_doc("d1", {"text": "hi", "tags": ["a"]})
        terms = m.terms_for_doc("d1")
        assert len(terms) == 2

    def test_filtered_index(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        m.index_doc("d1", {"text": "hi", "tags": ["a", "b"]})
        terms = m.terms_for_doc("d1", index_name="tags")
        assert len(terms) == 2
        assert all(t.index_name == "tags" for t in terms)

    def test_unknown_doc(self):
        m = DocIndexManager()
        assert m.terms_for_doc("nope") == []

    def test_term_is_indexedterm(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hi"})
        terms = m.terms_for_doc("d1")
        assert isinstance(terms[0], IndexedTerm)


class TestIndexSize:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "a b c"})
        assert m.index_size("kw") == 3

    def test_dedup(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "a b"})
        m.index_doc("d2", {"text": "a c"})
        assert m.index_size("kw") == 3

    def test_unknown(self):
        m = DocIndexManager()
        assert m.index_size("nope") == 0


class TestDocIds:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "a"})
        m.index_doc("d2", {"text": "b"})
        assert m.doc_ids() == ["d1", "d2"]

    def test_empty(self):
        m = DocIndexManager()
        assert m.doc_ids() == []


class TestIndexes:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("a", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("b", IndexKind.TAGS, tag_extractor)
        defs = m.indexes()
        assert len(defs) == 2

    def test_empty(self):
        m = DocIndexManager()
        assert m.indexes() == []


class TestGetIndex:
    def test_existing(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        assert m.get_index("kw").name == "kw"

    def test_missing(self):
        m = DocIndexManager()
        assert m.get_index("nope") is None


class TestTotalIndexes:
    def test_zero(self):
        m = DocIndexManager()
        assert m.total_indexes == 0

    def test_after_register(self):
        m = DocIndexManager()
        m.register_index("a", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("b", IndexKind.TAGS, tag_extractor)
        assert m.total_indexes == 2


class TestTotalIndexedDocs:
    def test_zero(self):
        m = DocIndexManager()
        assert m.total_indexed_docs == 0

    def test_after_indexing(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "x"})
        m.index_doc("d2", {"text": "y"})
        assert m.total_indexed_docs == 2

    def test_decreases_after_unindex(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "x"})
        m.unindex_doc("d1")
        assert m.total_indexed_docs == 0


class TestClearIndex:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "a b c"})
        cleared = m.clear_index("kw")
        assert cleared == 3
        assert m.index_size("kw") == 0

    def test_unknown(self):
        m = DocIndexManager()
        assert m.clear_index("nope") == 0

    def test_keeps_index_registered(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "a"})
        m.clear_index("kw")
        assert m.get_index("kw") is not None


class TestClear:
    def test_basic(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "x"})
        m.clear()
        assert m.total_indexes == 0
        assert m.total_indexed_docs == 0

    def test_empty_clear(self):
        m = DocIndexManager()
        m.clear()
        assert m.total_indexes == 0


class TestEdgeCases:
    def test_numeric_index(self):
        m = DocIndexManager()
        m.register_index("yr", IndexKind.NUMERIC, numeric_extractor)
        m.index_doc("d1", {"year": 2024})
        m.index_doc("d2", {"year": 2025})
        assert m.query("yr", "2024") == ["d1"]

    def test_metadata_index(self):
        m = DocIndexManager()
        m.register_index("auth", IndexKind.METADATA, author_extractor)
        m.index_doc("d1", {"author": "alice"})
        m.index_doc("d2", {"author": "bob"})
        assert m.query("auth", "alice") == ["d1"]

    def test_reindex_changes_query(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "old"})
        m.index_doc("d1", {"text": "new"})  # implicit re-index via index_doc
        assert m.query("kw", "old") == []
        assert m.query("kw", "new") == ["d1"]

    def test_multiple_docs_same_term(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        for i in range(5):
            m.index_doc(f"d{i}", {"text": "common"})
        assert len(m.query("kw", "common")) == 5

    def test_query_multi_three_indexes(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.register_index("tags", IndexKind.TAGS, tag_extractor)
        m.register_index("auth", IndexKind.METADATA, author_extractor)
        m.index_doc(
            "d1", {"text": "hello", "tags": ["a"], "author": "alice"}
        )
        m.index_doc(
            "d2", {"text": "hello", "tags": ["a"], "author": "bob"}
        )
        res = m.query_multi(
            {"kw": "hello", "tags": "a", "auth": "alice"}, mode="AND"
        )
        assert res == {"d1"}

    def test_unregister_clears_postings(self):
        m = DocIndexManager()
        m.register_index("kw", IndexKind.KEYWORD, keyword_extractor)
        m.index_doc("d1", {"text": "hi"})
        m.unregister_index("kw")
        assert m.query("kw", "hi") == []
