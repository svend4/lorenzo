"""Tests for faceted aggregation backend (Sprint 55 / S2)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.facets import (
    FacetAggregation,
    aggregate_facets,
    apply_filters,
    facet_summary,
)
from docstoolkit.rag.types import Passage


def _p(doc_id: str, text: str = "", title: str = "",
       score: float = 0.5) -> Passage:
    return Passage(text=text, doc_id=doc_id, title=title, score=score)


# ---------------- aggregate_facets ----------------

def test_aggregate_section_basic():
    passages = [
        _p("docs/intro"),
        _p("docs/arch"),
        _p("tests/unit"),
    ]
    [agg] = aggregate_facets(passages, fields=("section",))
    assert agg.field_name == "section"
    assert dict(agg.values) == {"docs": 2, "tests": 1}


def test_aggregate_multiple_fields():
    passages = [
        _p("docs/intro", text="tag:rag intro doc"),
        _p("docs/arch", text="tag:rag tag:memory"),
    ]
    aggs = aggregate_facets(passages, fields=("section", "tag"))
    assert len(aggs) == 2
    sec = next(a for a in aggs if a.field_name == "section")
    tag = next(a for a in aggs if a.field_name == "tag")
    assert dict(sec.values) == {"docs": 2}
    assert dict(tag.values) == {"rag": 2, "memory": 1}


def test_aggregate_empty_passages():
    aggs = aggregate_facets([], fields=("section", "tag"))
    assert all(a.values == [] for a in aggs)


def test_aggregate_unknown_field_returns_empty():
    [agg] = aggregate_facets([_p("d/x")], fields=("never_existing",))
    assert agg.values == []


def test_aggregate_year_from_text_and_title():
    passages = [
        _p("d/a", text="filed in 2023 by team"),
        _p("d/b", title="Plan 2024"),
        _p("d/c", text="dated 2024"),
    ]
    [agg] = aggregate_facets(passages, fields=("year",))
    by = dict(agg.values)
    assert by.get("2024") == 2
    assert by.get("2023") == 1


def test_aggregate_year_dedup_within_passage():
    p = _p("d/x", text="2023 2023 2023 only once")
    [agg] = aggregate_facets([p], fields=("year",))
    assert dict(agg.values) == {"2023": 1}


def test_aggregate_top_n_truncates():
    passages = [_p(f"sec{i}/x") for i in range(50)]
    [agg] = aggregate_facets(passages, fields=("section",), top_n=10)
    assert len(agg.values) == 10


def test_aggregate_preserves_count_order():
    passages = [_p("a/x")] * 5 + [_p("b/x")] * 3 + [_p("c/x")]
    [agg] = aggregate_facets(passages, fields=("section",))
    # Most common first
    assert agg.values[0] == ("a", 5)
    assert agg.values[-1] == ("c", 1)


def test_aggregate_custom_extractor():
    def first_char(p: Passage) -> list[str]:
        return [p.doc_id[:1]] if p.doc_id else []

    passages = [_p("apple/x"), _p("ant/x"), _p("bear/x")]
    [agg] = aggregate_facets(
        passages,
        fields=("letter",),
        extractors={"letter": first_char},
    )
    assert dict(agg.values) == {"a": 2, "b": 1}


def test_aggregate_depth_field():
    passages = [_p("a"), _p("a/b"), _p("a/b/c"), _p("a/b/c")]
    [agg] = aggregate_facets(passages, fields=("depth",))
    by = dict(agg.values)
    assert by["1"] == 1
    assert by["2"] == 1
    assert by["3"] == 2


def test_aggregation_total_property():
    a = FacetAggregation(field_name="x", values=[("a", 3), ("b", 1)])
    assert a.total == 4


# ---------------- apply_filters ----------------

def test_filter_single_string_value():
    passages = [_p("docs/a"), _p("tests/b"), _p("docs/c")]
    out = apply_filters(passages, {"section": "docs"})
    assert {p.doc_id for p in out} == {"docs/a", "docs/c"}


def test_filter_list_value_is_or():
    passages = [_p("a/x"), _p("b/x"), _p("c/x")]
    out = apply_filters(passages, {"section": ["a", "c"]})
    assert {p.doc_id for p in out} == {"a/x", "c/x"}


def test_filter_multiple_fields_is_and():
    passages = [
        _p("a/x", text="tag:rag"),
        _p("a/y", text="tag:memory"),
        _p("b/x", text="tag:rag"),
    ]
    out = apply_filters(passages, {"section": "a", "tag": "rag"})
    assert [p.doc_id for p in out] == ["a/x"]


def test_filter_empty_returns_all():
    passages = [_p("a/x"), _p("b/x")]
    out = apply_filters(passages, {})
    assert len(out) == 2


def test_filter_unknown_field_ignored():
    passages = [_p("a/x"), _p("b/x")]
    out = apply_filters(passages, {"made_up": "foo"})
    assert len(out) == 2


def test_filter_no_matches_returns_empty():
    passages = [_p("a/x"), _p("b/x")]
    out = apply_filters(passages, {"section": "never"})
    assert out == []


def test_filter_preserves_order():
    passages = [_p("a/1"), _p("b/2"), _p("a/3"), _p("a/4")]
    out = apply_filters(passages, {"section": "a"})
    assert [p.doc_id for p in out] == ["a/1", "a/3", "a/4"]


# ---------------- facet_summary ----------------

def test_summary_renders_label_and_counts():
    aggs = [
        FacetAggregation(field_name="section", values=[("docs", 5), ("tests", 2)]),
        FacetAggregation(field_name="tag", values=[("rag", 3)]),
    ]
    s = facet_summary(aggs)
    assert "section" in s and "docs=5" in s
    assert "tag" in s and "rag=3" in s


def test_summary_skips_empty():
    aggs = [
        FacetAggregation(field_name="section", values=[]),
        FacetAggregation(field_name="tag", values=[("x", 1)]),
    ]
    s = facet_summary(aggs)
    assert "section" not in s
    assert "tag" in s


def test_summary_respects_top_n():
    aggs = [FacetAggregation(
        field_name="section",
        values=[("a", 5), ("b", 4), ("c", 3), ("d", 2), ("e", 1)],
    )]
    s = facet_summary(aggs, top_n=2)
    assert "a=5" in s and "b=4" in s
    assert "c=3" not in s
