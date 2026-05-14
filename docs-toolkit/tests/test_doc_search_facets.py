"""Tests for doc_search_facets module."""

import pytest

from docstoolkit.doc_search_facets import (
    DocSearchFacets,
    FacetedQuery,
    FacetedSearchResult,
    FacetField,
    FacetResult,
    FacetType,
    FacetValue,
)


# ------------------------- dataclasses / enums -------------------------


class TestFacetType:
    def test_members_exist(self):
        assert FacetType.SINGLE
        assert FacetType.MULTI
        assert FacetType.HIERARCHICAL
        assert FacetType.RANGE
        assert FacetType.DATE

    def test_distinct(self):
        members = {
            FacetType.SINGLE,
            FacetType.MULTI,
            FacetType.HIERARCHICAL,
            FacetType.RANGE,
            FacetType.DATE,
        }
        assert len(members) == 5

    def test_is_enum(self):
        assert isinstance(FacetType.SINGLE, FacetType)


class TestFacetField:
    def test_basic(self):
        f = FacetField(name="tag", facet_type=FacetType.MULTI)
        assert f.name == "tag"
        assert f.facet_type == FacetType.MULTI

    def test_display_name_default(self):
        f = FacetField(name="category", facet_type=FacetType.SINGLE)
        assert f.display_name == "category"

    def test_display_name_custom(self):
        f = FacetField(name="cat", facet_type=FacetType.SINGLE, display_name="Category")
        assert f.display_name == "Category"

    def test_hierarchical_separator_default(self):
        f = FacetField(name="path", facet_type=FacetType.HIERARCHICAL)
        assert f.hierarchical_separator == "/"


class TestFacetValue:
    def test_basic(self):
        v = FacetValue(value="python", count=5)
        assert v.value == "python"
        assert v.count == 5
        assert v.selected is False
        assert v.children == []

    def test_selected(self):
        v = FacetValue(value="x", count=1, selected=True)
        assert v.selected is True

    def test_children(self):
        child = FacetValue(value="c", count=1)
        v = FacetValue(value="p", count=2, children=[child])
        assert v.children == [child]


class TestFacetResult:
    def test_basic(self):
        f = FacetField(name="tag", facet_type=FacetType.MULTI)
        r = FacetResult(field=f, values=[FacetValue("x", 1)])
        assert r.field == f
        assert len(r.values) == 1

    def test_selected_default(self):
        f = FacetField(name="tag", facet_type=FacetType.MULTI)
        r = FacetResult(field=f, values=[])
        assert r.selected_values == []


class TestFacetedQuery:
    def test_defaults(self):
        q = FacetedQuery()
        assert q.filters == {}
        assert q.text_query is None

    def test_with_filters(self):
        q = FacetedQuery(filters={"tag": ["python"]}, text_query="agent")
        assert q.filters == {"tag": ["python"]}
        assert q.text_query == "agent"


class TestFacetedSearchResult:
    def test_basic(self):
        r = FacetedSearchResult(matching_docs=["a"], total_count=1, facets=[])
        assert r.matching_docs == ["a"]
        assert r.total_count == 1
        assert r.facets == []


# ------------------------- register facet -------------------------


class TestRegisterFacet:
    def test_register_single(self):
        s = DocSearchFacets()
        f = s.register_facet("category", FacetType.SINGLE)
        assert isinstance(f, FacetField)
        assert f.name == "category"

    def test_register_multi(self):
        s = DocSearchFacets()
        f = s.register_facet("tags", FacetType.MULTI)
        assert f.facet_type == FacetType.MULTI

    def test_register_hierarchical(self):
        s = DocSearchFacets()
        f = s.register_facet("path", FacetType.HIERARCHICAL, hierarchical_separator=".")
        assert f.facet_type == FacetType.HIERARCHICAL
        assert f.hierarchical_separator == "."

    def test_empty_name_raises(self):
        s = DocSearchFacets()
        with pytest.raises(ValueError):
            s.register_facet("", FacetType.SINGLE)

    def test_invalid_type_raises(self):
        s = DocSearchFacets()
        with pytest.raises(TypeError):
            s.register_facet("x", "not-a-type")

    def test_display_name(self):
        s = DocSearchFacets()
        f = s.register_facet("c", FacetType.SINGLE, display_name="Cat")
        assert f.display_name == "Cat"


# ------------------------- index_doc -------------------------


class TestIndexDoc:
    def test_index_single_doc(self):
        s = DocSearchFacets()
        s.register_facet("category", FacetType.SINGLE)
        s.index_doc("d1", {"category": "tech"})
        assert s.total_docs == 1

    def test_index_multi_values(self):
        s = DocSearchFacets()
        s.register_facet("tags", FacetType.MULTI)
        s.index_doc("d1", {"tags": ["python", "ml"]})
        assert s.total_docs == 1

    def test_index_with_content(self):
        s = DocSearchFacets()
        s.register_facet("category", FacetType.SINGLE)
        s.index_doc("d1", {"category": "tech"}, content="Hello world")
        assert s.total_docs == 1

    def test_index_invalid_doc_id(self):
        s = DocSearchFacets()
        with pytest.raises(ValueError):
            s.index_doc("", {})

    def test_index_invalid_fields(self):
        s = DocSearchFacets()
        with pytest.raises(TypeError):
            s.index_doc("d1", "not a dict")

    def test_overwrite_doc(self):
        s = DocSearchFacets()
        s.register_facet("category", FacetType.SINGLE)
        s.index_doc("d1", {"category": "tech"})
        s.index_doc("d1", {"category": "science"})
        assert s.total_docs == 1


# ------------------------- unindex_doc -------------------------


class TestUnindexDoc:
    def test_unindex_existing(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        assert s.unindex_doc("d1") is True
        assert s.total_docs == 0

    def test_unindex_missing(self):
        s = DocSearchFacets()
        assert s.unindex_doc("nope") is False

    def test_unindex_clears_content(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"}, content="hello")
        s.unindex_doc("d1")
        q = FacetedQuery(text_query="hello")
        assert s.search(q).total_count == 0


# ------------------------- search -------------------------


class TestSearch:
    def test_search_empty(self):
        s = DocSearchFacets()
        r = s.search(FacetedQuery())
        assert r.total_count == 0
        assert r.matching_docs == []

    def test_search_all_no_filters(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        s.index_doc("d2", {"c": "y"})
        r = s.search(FacetedQuery())
        assert r.total_count == 2

    def test_search_returns_facets(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        r = s.search(FacetedQuery())
        assert isinstance(r.facets, list)
        assert len(r.facets) == 1

    def test_search_invalid_query(self):
        s = DocSearchFacets()
        with pytest.raises(TypeError):
            s.search("not a query")


class TestSearchWithFilters:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("category", FacetType.SINGLE)
        self.s.register_facet("tags", FacetType.MULTI)
        self.s.index_doc("d1", {"category": "tech", "tags": ["py", "ml"]})
        self.s.index_doc("d2", {"category": "tech", "tags": ["py"]})
        self.s.index_doc("d3", {"category": "science", "tags": ["ml"]})

    def test_filter_single_value(self):
        r = self.s.search(FacetedQuery(filters={"category": ["tech"]}))
        assert set(r.matching_docs) == {"d1", "d2"}

    def test_filter_or_within_field(self):
        r = self.s.search(FacetedQuery(filters={"category": ["tech", "science"]}))
        assert set(r.matching_docs) == {"d1", "d2", "d3"}

    def test_filter_multi_value_field(self):
        r = self.s.search(FacetedQuery(filters={"tags": ["ml"]}))
        assert set(r.matching_docs) == {"d1", "d3"}

    def test_filter_and_across_fields(self):
        r = self.s.search(
            FacetedQuery(filters={"category": ["tech"], "tags": ["ml"]})
        )
        assert set(r.matching_docs) == {"d1"}

    def test_filter_no_match(self):
        r = self.s.search(FacetedQuery(filters={"category": ["nothing"]}))
        assert r.total_count == 0

    def test_filter_empty_list_passes_all(self):
        r = self.s.search(FacetedQuery(filters={"category": []}))
        assert r.total_count == 3


class TestSearchWithText:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("c", FacetType.SINGLE)
        self.s.index_doc("d1", {"c": "x"}, content="Hello python world")
        self.s.index_doc("d2", {"c": "y"}, content="Goodbye java")
        self.s.index_doc("d3", {"c": "z"}, content="another text")

    def test_text_query_match(self):
        r = self.s.search(FacetedQuery(text_query="python"))
        assert r.matching_docs == ["d1"]

    def test_text_query_case_insensitive(self):
        r = self.s.search(FacetedQuery(text_query="PYTHON"))
        assert r.matching_docs == ["d1"]

    def test_text_query_no_match(self):
        r = self.s.search(FacetedQuery(text_query="nonexistent"))
        assert r.total_count == 0

    def test_text_query_with_filters(self):
        r = self.s.search(
            FacetedQuery(filters={"c": ["x"]}, text_query="python")
        )
        assert r.matching_docs == ["d1"]

    def test_text_query_matches_field_value(self):
        r = self.s.search(FacetedQuery(text_query="x"))
        assert "d1" in r.matching_docs


# ------------------------- facets_for -------------------------


class TestFacetsFor:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("category", FacetType.SINGLE)
        self.s.register_facet("tags", FacetType.MULTI)
        self.s.index_doc("d1", {"category": "tech", "tags": ["py", "ml"]})
        self.s.index_doc("d2", {"category": "tech", "tags": ["py"]})
        self.s.index_doc("d3", {"category": "science", "tags": ["ml"]})

    def test_facets_for_all(self):
        results = self.s.facets_for()
        assert len(results) == 2

    def test_facets_for_subset(self):
        results = self.s.facets_for(doc_ids=["d1", "d2"])
        cat = next(r for r in results if r.field.name == "category")
        assert cat.values[0].value == "tech"
        assert cat.values[0].count == 2

    def test_facets_for_specific_field(self):
        results = self.s.facets_for(field_names=["category"])
        assert len(results) == 1
        assert results[0].field.name == "category"

    def test_facets_for_counts(self):
        results = self.s.facets_for()
        tags = next(r for r in results if r.field.name == "tags")
        counts = {v.value: v.count for v in tags.values}
        assert counts["py"] == 2
        assert counts["ml"] == 2

    def test_facets_for_empty_ids(self):
        results = self.s.facets_for(doc_ids=[])
        for r in results:
            assert all(v.count == 0 for v in r.values) or r.values == []


# ------------------------- top_values -------------------------


class TestTopValues:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("t", FacetType.MULTI)
        self.s.index_doc("d1", {"t": ["a", "b"]})
        self.s.index_doc("d2", {"t": ["a", "c"]})
        self.s.index_doc("d3", {"t": ["a"]})

    def test_top_values_ordering(self):
        values = self.s.top_values("t", top_k=3)
        assert values[0].value == "a"
        assert values[0].count == 3

    def test_top_values_limit(self):
        values = self.s.top_values("t", top_k=1)
        assert len(values) == 1

    def test_top_values_unknown_field(self):
        assert self.s.top_values("missing") == []

    def test_top_values_zero_k(self):
        assert self.s.top_values("t", top_k=0) == []

    def test_top_values_with_doc_ids(self):
        values = self.s.top_values("t", doc_ids=["d1"])
        names = {v.value for v in values}
        assert names == {"a", "b"}


# ------------------------- drill_down -------------------------


class TestDrillDown:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("path", FacetType.HIERARCHICAL)
        self.s.index_doc("d1", {"path": "tech/python/web"})
        self.s.index_doc("d2", {"path": "tech/python/ml"})
        self.s.index_doc("d3", {"path": "tech/rust"})
        self.s.index_doc("d4", {"path": "science/biology"})

    def test_drill_down_root(self):
        values = self.s.drill_down("path", parent_path="")
        names = {v.value for v in values}
        assert names == {"tech", "science"}

    def test_drill_down_level(self):
        values = self.s.drill_down("path", parent_path="tech")
        names = {v.value for v in values}
        assert names == {"tech/python", "tech/rust"}

    def test_drill_down_deep(self):
        values = self.s.drill_down("path", parent_path="tech/python")
        names = {v.value for v in values}
        assert names == {"tech/python/web", "tech/python/ml"}

    def test_drill_down_counts(self):
        values = self.s.drill_down("path", parent_path="")
        counts = {v.value: v.count for v in values}
        assert counts["tech"] == 3
        assert counts["science"] == 1

    def test_drill_down_non_hierarchical(self):
        self.s.register_facet("flat", FacetType.SINGLE)
        assert self.s.drill_down("flat") == []

    def test_drill_down_missing_field(self):
        assert self.s.drill_down("missing") == []


# ------------------------- count_for_value -------------------------


class TestCountForValue:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("c", FacetType.SINGLE)
        self.s.index_doc("d1", {"c": "x"})
        self.s.index_doc("d2", {"c": "x"})
        self.s.index_doc("d3", {"c": "y"})

    def test_count_present(self):
        assert self.s.count_for_value("c", "x") == 2

    def test_count_absent(self):
        assert self.s.count_for_value("c", "z") == 0

    def test_count_missing_field(self):
        assert self.s.count_for_value("missing", "x") == 0

    def test_count_with_doc_ids(self):
        assert self.s.count_for_value("c", "x", doc_ids=["d1"]) == 1


# ------------------------- all_field_names -------------------------


class TestAllFieldNames:
    def test_empty(self):
        s = DocSearchFacets()
        assert s.all_field_names() == []

    def test_listed(self):
        s = DocSearchFacets()
        s.register_facet("a", FacetType.SINGLE)
        s.register_facet("b", FacetType.MULTI)
        assert set(s.all_field_names()) == {"a", "b"}


# ------------------------- get_facet -------------------------


class TestGetFacet:
    def test_existing(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        f = s.get_facet("c")
        assert f is not None
        assert f.name == "c"

    def test_missing(self):
        s = DocSearchFacets()
        assert s.get_facet("nope") is None


# ------------------------- total_docs -------------------------


class TestTotalDocs:
    def test_empty(self):
        s = DocSearchFacets()
        assert s.total_docs == 0

    def test_after_indexing(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        s.index_doc("d2", {"c": "y"})
        assert s.total_docs == 2

    def test_after_unindex(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        s.unindex_doc("d1")
        assert s.total_docs == 0


# ------------------------- clear -------------------------


class TestClear:
    def test_clear_docs_and_facets(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        s.clear()
        assert s.total_docs == 0
        assert s.all_field_names() == []

    def test_clear_empty(self):
        s = DocSearchFacets()
        s.clear()
        assert s.total_docs == 0


# ------------------------- hierarchical facet -------------------------


class TestHierarchicalFacet:
    def setup_method(self):
        self.s = DocSearchFacets()
        self.s.register_facet("path", FacetType.HIERARCHICAL)
        self.s.index_doc("d1", {"path": "tech/python/web"})
        self.s.index_doc("d2", {"path": "tech/python/ml"})
        self.s.index_doc("d3", {"path": "tech/rust"})
        self.s.index_doc("d4", {"path": "science/biology"})

    def test_facets_have_tree(self):
        results = self.s.facets_for(field_names=["path"])
        assert len(results) == 1
        top = results[0]
        names = {v.value for v in top.values}
        assert "tech" in names

    def test_hierarchical_children(self):
        results = self.s.facets_for(field_names=["path"])
        top = results[0]
        tech = next(v for v in top.values if v.value == "tech")
        kids = {c.value for c in tech.children}
        assert "tech/python" in kids
        assert "tech/rust" in kids

    def test_hierarchical_filter_matches_descendants(self):
        r = self.s.search(FacetedQuery(filters={"path": ["tech"]}))
        assert set(r.matching_docs) == {"d1", "d2", "d3"}

    def test_hierarchical_filter_exact_subpath(self):
        r = self.s.search(FacetedQuery(filters={"path": ["tech/python"]}))
        assert set(r.matching_docs) == {"d1", "d2"}

    def test_custom_separator(self):
        s = DocSearchFacets()
        s.register_facet("p", FacetType.HIERARCHICAL, hierarchical_separator=".")
        s.index_doc("d1", {"p": "a.b.c"})
        values = s.drill_down("p", parent_path="a")
        assert any(v.value == "a.b" for v in values)


# ------------------------- edge cases -------------------------


class TestEdgeCases:
    def test_search_with_unregistered_filter(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        # filter on a field that wasn't registered
        r = s.search(FacetedQuery(filters={"missing": ["v"]}))
        assert r.total_count == 0

    def test_multi_field_with_set_value(self):
        s = DocSearchFacets()
        s.register_facet("t", FacetType.MULTI)
        s.index_doc("d1", {"t": {"a", "b"}})
        r = s.search(FacetedQuery(filters={"t": ["a"]}))
        assert "d1" in r.matching_docs

    def test_range_facet_filter(self):
        s = DocSearchFacets()
        s.register_facet("score", FacetType.RANGE)
        s.index_doc("d1", {"score": 10})
        s.index_doc("d2", {"score": 50})
        s.index_doc("d3", {"score": 90})
        r = s.search(FacetedQuery(filters={"score": [(20, 80)]}))
        assert r.matching_docs == ["d2"]

    def test_date_facet(self):
        s = DocSearchFacets()
        s.register_facet("date", FacetType.DATE)
        s.index_doc("d1", {"date": "2025-01-01"})
        s.index_doc("d2", {"date": "2025-02-01"})
        r = s.search(FacetedQuery(filters={"date": ["2025-01-01"]}))
        assert r.matching_docs == ["d1"]

    def test_index_doc_without_field_value(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {})
        assert s.total_docs == 1
        r = s.search(FacetedQuery(filters={"c": ["x"]}))
        assert "d1" not in r.matching_docs

    def test_facets_for_with_field_names_unknown(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        results = s.facets_for(field_names=["unknown"])
        assert results == []

    def test_search_result_selected_flag(self):
        s = DocSearchFacets()
        s.register_facet("c", FacetType.SINGLE)
        s.index_doc("d1", {"c": "x"})
        s.index_doc("d2", {"c": "y"})
        r = s.search(FacetedQuery(filters={"c": ["x"]}))
        facet_result = r.facets[0]
        assert facet_result.selected_values == ["x"]

    def test_search_isolation(self):
        s1 = DocSearchFacets()
        s2 = DocSearchFacets()
        s1.register_facet("c", FacetType.SINGLE)
        s1.index_doc("d1", {"c": "x"})
        assert s2.total_docs == 0
