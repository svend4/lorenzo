"""Tests for E150 docstoolkit.doc_filter."""
from __future__ import annotations

import pytest

from docstoolkit.doc_filter import (
    DocFilter,
    Document,
    FilterCondition,
    FilterOp,
    FilterResult,
)


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


def make_doc(doc_id="d1", content="hello world", **meta):
    return Document(doc_id=doc_id, content=content, metadata=dict(meta))


@pytest.fixture
def docs():
    return [
        Document("d1", "alpha beta gamma", {"author": "alice", "year": 2020, "tags": ["py", "ml"]}),
        Document("d2", "Beta launch", {"author": "bob", "year": 2021, "tags": ["js"]}),
        Document("d3", "gamma rays", {"author": "alice", "year": 2022, "tags": ["py"]}),
        Document("d4", "delta force", {"author": "carol", "year": 2023, "tags": []}),
        Document("d5", "epsilon", {"author": None, "year": 2019}),
    ]


@pytest.fixture
def df():
    return DocFilter()


# --------------------------------------------------------------------------
# Basic dataclasses
# --------------------------------------------------------------------------


class TestFilterOp:
    def test_enum_values(self):
        # Spot-check key members exist.
        assert FilterOp.EQ
        assert FilterOp.NE
        assert FilterOp.LT
        assert FilterOp.LE
        assert FilterOp.GT
        assert FilterOp.GE
        assert FilterOp.IN
        assert FilterOp.NOT_IN
        assert FilterOp.CONTAINS
        assert FilterOp.NOT_CONTAINS
        assert FilterOp.STARTSWITH
        assert FilterOp.ENDSWITH
        assert FilterOp.MATCHES
        assert FilterOp.EXISTS
        assert FilterOp.NOT_EXISTS

    def test_enum_distinct(self):
        names = {op.name for op in FilterOp}
        assert len(names) == 15


class TestFilterCondition:
    def test_construct_basic(self):
        c = FilterCondition("title", FilterOp.EQ, "foo")
        assert c.field == "title"
        assert c.op is FilterOp.EQ
        assert c.value == "foo"

    def test_default_value_is_none(self):
        c = FilterCondition("x", FilterOp.EXISTS)
        assert c.value is None

    def test_keyword_construction(self):
        c = FilterCondition(field="metadata.author", op=FilterOp.NE, value="bob")
        assert c.field == "metadata.author"


class TestDocument:
    def test_construct_minimal(self):
        d = Document("id", "content")
        assert d.doc_id == "id"
        assert d.content == "content"
        assert d.metadata == {}

    def test_metadata_default_independent(self):
        a = Document("a", "x")
        b = Document("b", "y")
        a.metadata["k"] = 1
        assert "k" not in b.metadata

    def test_with_metadata(self):
        d = Document("d", "c", {"k": 1})
        assert d.metadata["k"] == 1


class TestFilterResult:
    def test_match_count(self):
        r = FilterResult(matched=[Document("d", "c")], total_input=2)
        assert r.match_count == 1

    def test_match_rate(self):
        r = FilterResult(matched=[Document("d", "c")], total_input=2)
        assert r.match_rate == 0.5

    def test_match_rate_empty(self):
        r = FilterResult(matched=[], total_input=0)
        assert r.match_rate == 0.0

    def test_match_rate_full(self):
        d = [Document("a", "x"), Document("b", "y")]
        r = FilterResult(matched=d, total_input=2)
        assert r.match_rate == 1.0


# --------------------------------------------------------------------------
# Per-operator tests
# --------------------------------------------------------------------------


class TestFilterEq:
    def test_eq_on_metadata(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", "alice", FilterOp.EQ)
        ids = [d.doc_id for d in r.matched]
        assert ids == ["d1", "d3"]
        assert r.total_input == 5

    def test_eq_on_content(self, df, docs):
        r = df.filter_by_field(docs, "content", "epsilon", FilterOp.EQ)
        assert [d.doc_id for d in r.matched] == ["d5"]

    def test_eq_on_doc_id(self, df, docs):
        r = df.filter_by_field(docs, "doc_id", "d2", FilterOp.EQ)
        assert [d.doc_id for d in r.matched] == ["d2"]


class TestFilterNe:
    def test_ne_simple(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", "alice", FilterOp.NE)
        ids = sorted(d.doc_id for d in r.matched)
        # d5 has author=None → None != "alice" is True, so included.
        assert ids == ["d2", "d4", "d5"]

    def test_ne_missing_field_excluded(self, df, docs):
        # NE against a missing field returns False (excluded).
        r = df.filter_by_field(docs, "metadata.nope", "x", FilterOp.NE)
        assert r.matched == []


class TestFilterLtGt:
    def test_lt(self, df, docs):
        r = df.filter_by_field(docs, "metadata.year", 2021, FilterOp.LT)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d5"]

    def test_le(self, df, docs):
        r = df.filter_by_field(docs, "metadata.year", 2021, FilterOp.LE)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d2", "d5"]

    def test_gt(self, df, docs):
        r = df.filter_by_field(docs, "metadata.year", 2021, FilterOp.GT)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d3", "d4"]

    def test_ge(self, df, docs):
        r = df.filter_by_field(docs, "metadata.year", 2021, FilterOp.GE)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d2", "d3", "d4"]

    def test_lt_string(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", "bob", FilterOp.LT)
        ids = sorted(d.doc_id for d in r.matched)
        # "alice" < "bob"
        assert ids == ["d1", "d3"]


class TestFilterIn:
    def test_in_list(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", ["alice", "carol"], FilterOp.IN)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d3", "d4"]

    def test_not_in_list(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", ["alice"], FilterOp.NOT_IN)
        ids = sorted(d.doc_id for d in r.matched)
        # d2 bob, d4 carol, d5 None
        assert ids == ["d2", "d4", "d5"]

    def test_in_empty(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", [], FilterOp.IN)
        assert r.matched == []


class TestFilterContains:
    def test_contains_string(self, df, docs):
        r = df.filter_by_field(docs, "content", "gamma", FilterOp.CONTAINS)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d3"]

    def test_contains_list_element(self, df, docs):
        r = df.filter_by_field(docs, "metadata.tags", "py", FilterOp.CONTAINS)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d3"]

    def test_not_contains_string(self, df, docs):
        r = df.filter_by_field(docs, "content", "gamma", FilterOp.NOT_CONTAINS)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d2", "d4", "d5"]

    def test_not_contains_list(self, df, docs):
        r = df.filter_by_field(docs, "metadata.tags", "py", FilterOp.NOT_CONTAINS)
        ids = sorted(d.doc_id for d in r.matched)
        # d2 js (no py), d4 [] (no py); d5 has no 'tags' → NOT_CONTAINS False since missing
        assert ids == ["d2", "d4"]


class TestFilterStartsEndsWith:
    def test_startswith(self, df, docs):
        r = df.filter_by_field(docs, "content", "alpha", FilterOp.STARTSWITH)
        assert [d.doc_id for d in r.matched] == ["d1"]

    def test_endswith(self, df, docs):
        r = df.filter_by_field(docs, "content", "rays", FilterOp.ENDSWITH)
        assert [d.doc_id for d in r.matched] == ["d3"]

    def test_startswith_non_string_value_false(self, df, docs):
        r = df.filter_by_field(docs, "metadata.year", "20", FilterOp.STARTSWITH)
        assert r.matched == []


class TestFilterMatchesRegex:
    def test_matches_basic(self, df, docs):
        r = df.filter_by_field(docs, "content", r"^[Bb]eta", FilterOp.MATCHES)
        assert [d.doc_id for d in r.matched] == ["d2"]

    def test_matches_case_insensitive_flag(self, df, docs):
        r = df.filter_by_field(docs, "content", r"(?i)beta", FilterOp.MATCHES)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d2"]

    def test_matches_non_string_false(self, df, docs):
        r = df.filter_by_field(docs, "metadata.year", r"\d+", FilterOp.MATCHES)
        assert r.matched == []


class TestFilterExists:
    def test_exists_present(self, df, docs):
        r = df.filter_by_field(docs, "metadata.tags", None, FilterOp.EXISTS)
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d2", "d3", "d4"]  # d5 has no 'tags' key

    def test_exists_treats_none_as_missing(self, df, docs):
        # d5 has author=None — EXISTS should return False per spec.
        r = df.filter_by_field(docs, "metadata.author", None, FilterOp.EXISTS)
        ids = sorted(d.doc_id for d in r.matched)
        assert "d5" not in ids
        assert ids == ["d1", "d2", "d3", "d4"]

    def test_not_exists(self, df, docs):
        r = df.filter_by_field(docs, "metadata.tags", None, FilterOp.NOT_EXISTS)
        assert [d.doc_id for d in r.matched] == ["d5"]

    def test_not_exists_none_value(self, df, docs):
        r = df.filter_by_field(docs, "metadata.author", None, FilterOp.NOT_EXISTS)
        assert [d.doc_id for d in r.matched] == ["d5"]


# --------------------------------------------------------------------------
# AND / OR mode
# --------------------------------------------------------------------------


class TestFilterAndMode:
    def test_and_two_conditions(self, df, docs):
        cs = [
            FilterCondition("metadata.author", FilterOp.EQ, "alice"),
            FilterCondition("metadata.year", FilterOp.GE, 2022),
        ]
        r = df.filter(docs, cs, mode="AND")
        assert [d.doc_id for d in r.matched] == ["d3"]

    def test_and_empty_conditions(self, df, docs):
        r = df.filter(docs, [], mode="AND")
        assert r.match_count == 5

    def test_and_no_match(self, df, docs):
        cs = [
            FilterCondition("metadata.author", FilterOp.EQ, "alice"),
            FilterCondition("metadata.author", FilterOp.EQ, "bob"),
        ]
        r = df.filter(docs, cs, mode="AND")
        assert r.matched == []


class TestFilterOrMode:
    def test_or_two_conditions(self, df, docs):
        cs = [
            FilterCondition("metadata.author", FilterOp.EQ, "alice"),
            FilterCondition("metadata.author", FilterOp.EQ, "bob"),
        ]
        r = df.filter(docs, cs, mode="OR")
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d2", "d3"]

    def test_or_empty_conditions_matches_nothing(self, df, docs):
        r = df.filter(docs, [], mode="OR")
        assert r.matched == []

    def test_invalid_mode_raises(self, df, docs):
        with pytest.raises(ValueError):
            df.filter(docs, [FilterCondition("doc_id", FilterOp.EQ, "d1")], mode="XOR")

    def test_mode_case_insensitive(self, df, docs):
        cs = [FilterCondition("metadata.author", FilterOp.EQ, "alice")]
        r = df.filter(docs, cs, mode="or")
        assert len(r.matched) == 2


# --------------------------------------------------------------------------
# Higher-level helpers
# --------------------------------------------------------------------------


class TestFilterByContent:
    def test_content_substring_case_insensitive(self, df, docs):
        r = df.filter_by_content(docs, "BETA")
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d2"]

    def test_content_case_sensitive(self, df, docs):
        r = df.filter_by_content(docs, "Beta", case_sensitive=True)
        assert [d.doc_id for d in r.matched] == ["d2"]

    def test_content_no_match(self, df, docs):
        r = df.filter_by_content(docs, "qwerty")
        assert r.matched == []

    def test_content_empty_substring(self, df, docs):
        r = df.filter_by_content(docs, "")
        # empty substring is contained in everything.
        assert r.match_count == 5


class TestFilterByRegex:
    def test_regex_simple(self, df, docs):
        r = df.filter_by_regex(docs, r"gamma")
        ids = sorted(d.doc_id for d in r.matched)
        assert ids == ["d1", "d3"]

    def test_regex_anchored(self, df, docs):
        r = df.filter_by_regex(docs, r"^delta")
        assert [d.doc_id for d in r.matched] == ["d4"]

    def test_regex_no_match(self, df, docs):
        r = df.filter_by_regex(docs, r"qqqq")
        assert r.matched == []


class TestFilterByMetadata:
    def test_metadata_short_key(self, df, docs):
        r = df.filter_by_metadata(docs, "author", "bob")
        assert [d.doc_id for d in r.matched] == ["d2"]

    def test_metadata_full_path(self, df, docs):
        r = df.filter_by_metadata(docs, "metadata.author", "bob")
        assert [d.doc_id for d in r.matched] == ["d2"]

    def test_metadata_nested(self, df):
        docs = [
            Document("a", "c", {"info": {"lang": "ru"}}),
            Document("b", "c", {"info": {"lang": "en"}}),
            Document("c", "c", {"info": {}}),
        ]
        r = df.filter_by_metadata(docs, "info.lang", "ru")
        assert [d.doc_id for d in r.matched] == ["a"]


# --------------------------------------------------------------------------
# Ordering & paging
# --------------------------------------------------------------------------


class TestSortBy:
    def test_sort_asc(self, df, docs):
        out = df.sort_by(docs, "metadata.year")
        years = [d.metadata.get("year") for d in out]
        # Non-missing years sorted ascending; d5=2019 first.
        assert years[0] == 2019
        assert years[-1] == 2023

    def test_sort_desc(self, df, docs):
        out = df.sort_by(docs, "metadata.year", reverse=True)
        assert out[0].metadata["year"] == 2023
        assert out[-1].metadata["year"] == 2019

    def test_sort_string_field(self, df, docs):
        out = df.sort_by(docs, "content")
        # ASCII order: 'B' (0x42) < 'a' (0x61), so "Beta launch" sorts first.
        assert out[0].doc_id == "d2"
        assert out[-1].doc_id == "d3"  # "gamma rays" last among lowercase

    def test_sort_missing_field_sinks(self, df):
        d1 = Document("a", "c", {"k": 1})
        d2 = Document("b", "c", {})
        d3 = Document("c", "c", {"k": 3})
        out = df.sort_by([d1, d2, d3], "metadata.k")
        assert out[-1].doc_id == "b"

    def test_sort_stable(self, df):
        a = Document("a", "x", {"k": 1})
        b = Document("b", "x", {"k": 1})
        c = Document("c", "x", {"k": 1})
        out = df.sort_by([a, b, c], "metadata.k")
        assert [d.doc_id for d in out] == ["a", "b", "c"]


class TestLimit:
    def test_limit_basic(self, df, docs):
        out = df.limit(docs, 2)
        assert [d.doc_id for d in out] == ["d1", "d2"]

    def test_limit_with_offset(self, df, docs):
        out = df.limit(docs, 2, offset=2)
        assert [d.doc_id for d in out] == ["d3", "d4"]

    def test_limit_beyond_length(self, df, docs):
        out = df.limit(docs, 99)
        assert len(out) == 5

    def test_limit_zero(self, df, docs):
        assert df.limit(docs, 0) == []

    def test_limit_negative_n_treated_as_zero(self, df, docs):
        assert df.limit(docs, -3) == []

    def test_limit_negative_offset_treated_as_zero(self, df, docs):
        out = df.limit(docs, 2, offset=-5)
        assert [d.doc_id for d in out] == ["d1", "d2"]


class TestPaginate:
    def test_paginate_first_page(self, df, docs):
        page, total = df.paginate(docs, page=1, page_size=2)
        assert [d.doc_id for d in page] == ["d1", "d2"]
        assert total == 3  # 5 docs / 2 per page = 3 pages

    def test_paginate_last_partial(self, df, docs):
        page, total = df.paginate(docs, page=3, page_size=2)
        assert [d.doc_id for d in page] == ["d5"]
        assert total == 3

    def test_paginate_out_of_range(self, df, docs):
        page, total = df.paginate(docs, page=10, page_size=2)
        assert page == []
        assert total == 3

    def test_paginate_empty(self, df):
        page, total = df.paginate([], page=1, page_size=10)
        assert page == []
        assert total == 0

    def test_paginate_zero_size_raises(self, df, docs):
        with pytest.raises(ValueError):
            df.paginate(docs, page=1, page_size=0)

    def test_paginate_negative_page_clamps(self, df, docs):
        page, total = df.paginate(docs, page=-3, page_size=2)
        assert [d.doc_id for d in page] == ["d1", "d2"]
        assert total == 3


# --------------------------------------------------------------------------
# Edge cases
# --------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_docs(self, df):
        r = df.filter_by_field([], "doc_id", "x", FilterOp.EQ)
        assert r.matched == []
        assert r.total_input == 0
        assert r.match_rate == 0.0

    def test_missing_field_non_exists_op_false(self, df, docs):
        r = df.filter_by_field(docs, "metadata.zzzz", "x", FilterOp.EQ)
        assert r.matched == []

    def test_missing_field_lt_false(self, df, docs):
        r = df.filter_by_field(docs, "metadata.zzzz", 1, FilterOp.LT)
        assert r.matched == []

    def test_filter_one_wraps_single(self, df, docs):
        c = FilterCondition("metadata.author", FilterOp.EQ, "carol")
        r = df.filter_one(docs, c)
        assert [d.doc_id for d in r.matched] == ["d4"]

    def test_nested_metadata_path(self, df):
        d = Document("a", "c", {"x": {"y": {"z": 42}}})
        r = df.filter_by_field([d], "metadata.x.y.z", 42, FilterOp.EQ)
        assert len(r.matched) == 1

    def test_nested_missing_segment(self, df):
        d = Document("a", "c", {"x": {"y": 1}})
        r = df.filter_by_field([d], "metadata.x.missing.z", 42, FilterOp.EQ)
        assert r.matched == []

    def test_incompatible_comparison_returns_false(self, df):
        # Comparing str < int should be coerced to False rather than crash.
        d = Document("a", "c", {"k": "alpha"})
        r = df.filter_by_field([d], "metadata.k", 5, FilterOp.LT)
        assert r.matched == []

    def test_result_match_rate_zero_total(self):
        r = FilterResult(matched=[], total_input=0)
        assert r.match_rate == 0.0

    def test_content_field_top_level(self, df, docs):
        r = df.filter_by_field(docs, "content", "epsilon", FilterOp.CONTAINS)
        assert [d.doc_id for d in r.matched] == ["d5"]

    def test_metadata_short_field_works_top_level(self, df, docs):
        # Using a bare metadata key (no "metadata.") should resolve via metadata.
        r = df.filter_by_field(docs, "author", "carol", FilterOp.EQ)
        assert [d.doc_id for d in r.matched] == ["d4"]
