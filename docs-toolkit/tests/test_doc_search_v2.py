"""Tests for docstoolkit.doc_search_v2."""

import threading

import pytest

from docstoolkit.doc_search_v2 import (
    DocSearchV2,
    Facet,
    MatchMode,
    SearchHit,
    SearchRequest,
    SearchResult,
)


# ---------------------------------------------------------------- fixtures


@pytest.fixture
def empty():
    return DocSearchV2()


@pytest.fixture
def populated():
    s = DocSearchV2()
    s.add(
        "d1",
        "Python is a great programming language for data science",
        {"category": "lang", "tags": ["python", "data"], "year": 2020},
    )
    s.add(
        "d2",
        "Java is also a great programming language used widely",
        {"category": "lang", "tags": ["java"], "year": 2021},
    )
    s.add(
        "d3",
        "Machine learning models work with python and data",
        {"category": "ml", "tags": ["python", "ml"], "year": 2022},
    )
    s.add(
        "d4",
        "Cooking recipes for breakfast and dinner",
        {"category": "food", "tags": ["recipe"], "year": 2023},
    )
    return s


# ---------------------------------------------------------------- enums/dc


class TestMatchMode:
    def test_has_bm25(self):
        assert MatchMode.BM25.value == "bm25"

    def test_has_prefix(self):
        assert MatchMode.PREFIX.value == "prefix"

    def test_has_exact(self):
        assert MatchMode.EXACT.value == "exact"

    def test_has_all(self):
        assert MatchMode.ALL.value == "all"

    def test_distinct_values(self):
        vals = {m.value for m in MatchMode}
        assert len(vals) == 4


class TestSearchRequest:
    def test_minimal(self):
        r = SearchRequest(query="x")
        assert r.query == "x"
        assert r.mode == MatchMode.BM25
        assert r.top_k == 10
        assert r.min_score == 0.0

    def test_defaults_independent(self):
        r1 = SearchRequest(query="a")
        r2 = SearchRequest(query="b")
        r1.filters["k"] = 1
        assert "k" not in r2.filters

    def test_full(self):
        r = SearchRequest(
            query="hello",
            mode=MatchMode.PREFIX,
            filters={"k": "v"},
            top_k=5,
            min_score=0.5,
            boost_fields={"title": 2.0},
        )
        assert r.filters == {"k": "v"}
        assert r.boost_fields == {"title": 2.0}


class TestSearchHit:
    def test_minimal(self):
        h = SearchHit(doc_id="d", score=1.0)
        assert h.doc_id == "d"
        assert h.score == 1.0
        assert h.matched_fields == []
        assert h.snippet is None

    def test_full(self):
        h = SearchHit(
            doc_id="d", score=2.5, matched_fields=["title"], snippet="abc"
        )
        assert h.matched_fields == ["title"]
        assert h.snippet == "abc"


class TestFacet:
    def test_create(self):
        f = Facet(field="cat", values={"a": 2, "b": 1})
        assert f.field == "cat"
        assert f.values["a"] == 2


class TestSearchResult:
    def test_create(self):
        sr = SearchResult(hits=[], total=0)
        assert sr.hits == []
        assert sr.facets == []
        assert sr.query == ""

    def test_with_hits(self):
        h = SearchHit(doc_id="d", score=1.0)
        sr = SearchResult(hits=[h], total=1, query="x")
        assert sr.total == 1
        assert sr.query == "x"


# ---------------------------------------------------------------- add


class TestAdd:
    def test_add_single(self, empty):
        empty.add("d1", "hello world")
        assert empty.doc_count == 1

    def test_add_with_fields(self, empty):
        empty.add("d1", "hello", {"category": "x"})
        assert empty.doc_count == 1

    def test_add_increments_term_count(self, empty):
        empty.add("d1", "alpha beta gamma")
        assert empty.term_count() == 3

    def test_add_replaces_existing(self, empty):
        empty.add("d1", "one two three")
        empty.add("d1", "four")
        assert empty.doc_count == 1
        # vocab should reflect only the new content
        assert empty.term_count() == 1

    def test_add_empty_doc_id_raises(self, empty):
        with pytest.raises(ValueError):
            empty.add("", "content")

    def test_add_empty_content_ok(self, empty):
        empty.add("d1", "")
        assert empty.doc_count == 1
        assert empty.term_count() == 0


class TestAddBatch:
    def test_batch_adds(self, empty):
        empty.add_batch(
            [
                {"doc_id": "d1", "content": "one two"},
                {"doc_id": "d2", "content": "three four"},
            ]
        )
        assert empty.doc_count == 2

    def test_batch_with_fields(self, empty):
        empty.add_batch(
            [{"doc_id": "d1", "content": "x", "fields": {"k": 1}}]
        )
        assert empty.doc_count == 1

    def test_batch_empty(self, empty):
        empty.add_batch([])
        assert empty.doc_count == 0

    def test_batch_missing_doc_id_raises(self, empty):
        with pytest.raises(ValueError):
            empty.add_batch([{"content": "x"}])


class TestUpdate:
    def test_update_content(self, populated):
        assert populated.update("d1", content="entirely new text")
        result = populated.search_simple("python")
        ids = [h.doc_id for h in result]
        assert "d1" not in ids

    def test_update_fields(self, populated):
        assert populated.update("d1", fields={"category": "newcat"})
        req = SearchRequest(query="python", filters={"category": "newcat"})
        result = populated.search(req)
        assert all(h.doc_id == "d1" for h in result.hits)

    def test_update_missing_doc(self, populated):
        assert populated.update("nope", content="x") is False

    def test_update_keeps_content_when_none(self, populated):
        populated.update("d1", fields={"new": "tag"})
        # original content should still find d1
        hits = populated.search_simple("Python")
        assert any(h.doc_id == "d1" for h in hits)


class TestRemove:
    def test_remove_existing(self, populated):
        assert populated.remove("d1") is True
        assert populated.doc_count == 3

    def test_remove_missing(self, populated):
        assert populated.remove("nope") is False

    def test_remove_clears_terms(self, empty):
        empty.add("d1", "unique alpha")
        empty.add("d2", "alpha beta")
        empty.remove("d1")
        # 'unique' should be gone, 'alpha' and 'beta' remain
        assert empty.term_count() == 2


# ---------------------------------------------------------------- search


class TestSearchBm25:
    def test_returns_relevant_doc(self, populated):
        r = populated.search(SearchRequest(query="python"))
        assert len(r.hits) >= 1
        ids = [h.doc_id for h in r.hits]
        assert "d1" in ids or "d3" in ids

    def test_unrelated_doc_excluded(self, populated):
        r = populated.search(SearchRequest(query="python"))
        ids = [h.doc_id for h in r.hits]
        assert "d4" not in ids

    def test_scores_descending(self, populated):
        r = populated.search(SearchRequest(query="python data"))
        scores = [h.score for h in r.hits]
        assert scores == sorted(scores, reverse=True)

    def test_empty_query_returns_no_hits(self, populated):
        r = populated.search(SearchRequest(query=""))
        assert r.hits == []
        assert r.total == 0

    def test_no_match_returns_empty(self, populated):
        r = populated.search(SearchRequest(query="quantum"))
        assert r.hits == []

    def test_total_reflects_pre_topk(self, populated):
        r = populated.search(SearchRequest(query="programming", top_k=1))
        assert r.total >= 2
        assert len(r.hits) == 1


class TestSearchPrefix:
    def test_prefix_mode(self, populated):
        r = populated.search(SearchRequest(query="prog", mode=MatchMode.PREFIX))
        ids = {h.doc_id for h in r.hits}
        assert "d1" in ids and "d2" in ids

    def test_prefix_no_match(self, populated):
        r = populated.search(SearchRequest(query="zzz", mode=MatchMode.PREFIX))
        assert r.hits == []

    def test_prefix_empty(self, populated):
        r = populated.search(SearchRequest(query="", mode=MatchMode.PREFIX))
        assert r.hits == []


class TestSearchExact:
    def test_exact_match(self, empty):
        empty.add("d1", "hello world")
        r = empty.search(
            SearchRequest(query="hello world", mode=MatchMode.EXACT)
        )
        assert len(r.hits) == 1
        assert r.hits[0].doc_id == "d1"

    def test_exact_mismatch(self, empty):
        empty.add("d1", "hello world")
        r = empty.search(
            SearchRequest(query="hello", mode=MatchMode.EXACT)
        )
        assert r.hits == []

    def test_exact_score_is_one(self, empty):
        empty.add("d1", "x")
        r = empty.search(SearchRequest(query="x", mode=MatchMode.EXACT))
        assert r.hits[0].score == 1.0


class TestSearchFiltersEq:
    def test_equality_filter(self, populated):
        r = populated.search(
            SearchRequest(query="programming", filters={"category": "lang"})
        )
        for h in r.hits:
            assert h.doc_id in {"d1", "d2"}

    def test_equality_filter_no_match(self, populated):
        r = populated.search(
            SearchRequest(query="python", filters={"category": "zzz"})
        )
        assert r.hits == []

    def test_equality_filter_numeric(self, populated):
        r = populated.search(
            SearchRequest(query="programming", filters={"year": 2020})
        )
        assert all(h.doc_id == "d1" for h in r.hits)


class TestSearchFiltersList:
    def test_list_filter_any(self, populated):
        r = populated.search(
            SearchRequest(
                query="python",
                filters={"tags": ["python"]},
            )
        )
        ids = {h.doc_id for h in r.hits}
        assert ids.issubset({"d1", "d3"})

    def test_list_filter_multiple(self, populated):
        r = populated.search(
            SearchRequest(
                query="programming",
                filters={"tags": ["python", "java"]},
            )
        )
        ids = {h.doc_id for h in r.hits}
        assert "d4" not in ids

    def test_list_filter_no_match(self, populated):
        r = populated.search(
            SearchRequest(query="python", filters={"tags": ["nope"]})
        )
        assert r.hits == []


class TestSearchTopK:
    def test_topk_limits(self, populated):
        r = populated.search(SearchRequest(query="programming", top_k=1))
        assert len(r.hits) == 1

    def test_topk_zero(self, populated):
        r = populated.search(SearchRequest(query="programming", top_k=0))
        assert r.hits == []

    def test_topk_larger_than_results(self, populated):
        r = populated.search(SearchRequest(query="programming", top_k=100))
        assert len(r.hits) >= 1


class TestSearchMinScore:
    def test_min_score_filter(self, populated):
        r = populated.search(
            SearchRequest(query="python", min_score=1000.0)
        )
        assert r.hits == []

    def test_min_score_zero(self, populated):
        r = populated.search(SearchRequest(query="python", min_score=0.0))
        assert len(r.hits) >= 1

    def test_min_score_typical(self, populated):
        r = populated.search(SearchRequest(query="python", min_score=0.01))
        assert all(h.score >= 0.01 for h in r.hits)


class TestSearchBoost:
    def test_boost_field(self, empty):
        empty.add("d1", "lorem ipsum", {"title": "python tutorial"})
        empty.add("d2", "python ipsum")
        r = empty.search(
            SearchRequest(query="python", boost_fields={"title": 5.0})
        )
        # d1 has python only in boosted field; d2 has it in content.
        # With high boost weight, d1 should outscore d2.
        hits = {h.doc_id: h.score for h in r.hits}
        assert "d1" in hits
        assert hits["d1"] >= 5.0

    def test_boost_adds_matched_field(self, empty):
        empty.add("d1", "python here", {"title": "python guide"})
        r = empty.search(
            SearchRequest(query="python", boost_fields={"title": 2.0})
        )
        assert "title" in r.hits[0].matched_fields

    def test_no_boost_field_match(self, empty):
        empty.add("d1", "python text", {"title": "java book"})
        r = empty.search(
            SearchRequest(query="python", boost_fields={"title": 5.0})
        )
        assert "title" not in r.hits[0].matched_fields


class TestFacetSearch:
    def test_facet_basic(self, populated):
        r = populated.facet_search("python", ["category"])
        assert len(r.facets) == 1
        assert r.facets[0].field == "category"
        # at least one of lang/ml present
        assert any(k in r.facets[0].values for k in ("lang", "ml"))

    def test_facet_list_field(self, populated):
        r = populated.facet_search("python", ["tags"])
        assert r.facets[0].field == "tags"
        assert "python" in r.facets[0].values

    def test_facet_multiple_fields(self, populated):
        r = populated.facet_search("programming", ["category", "year"])
        assert len(r.facets) == 2
        names = [f.field for f in r.facets]
        assert "category" in names and "year" in names

    def test_facet_no_hits(self, populated):
        r = populated.facet_search("nothingmatches", ["category"])
        assert r.hits == []
        assert r.facets[0].values == {}


class TestPrefixSearch:
    def test_prefix_content(self, populated):
        hits = populated.prefix_search("prog")
        ids = {h.doc_id for h in hits}
        assert "d1" in ids

    def test_prefix_field(self, empty):
        empty.add("d1", "x", {"title": "python tutorial"})
        empty.add("d2", "x", {"title": "java book"})
        hits = empty.prefix_search("pyth", field="title")
        assert any(h.doc_id == "d1" for h in hits)
        assert not any(h.doc_id == "d2" for h in hits)

    def test_prefix_empty_string(self, populated):
        assert populated.prefix_search("") == []

    def test_prefix_topk(self, populated):
        hits = populated.prefix_search("p", top_k=1)
        assert len(hits) <= 1

    def test_prefix_missing_field(self, empty):
        empty.add("d1", "content")
        hits = empty.prefix_search("x", field="missing")
        assert hits == []


class TestExactSearch:
    def test_exact_match(self, empty):
        empty.add("d1", "hello")
        empty.add("d2", "hello world")
        hits = empty.exact_search("hello")
        assert len(hits) == 1
        assert hits[0].doc_id == "d1"

    def test_exact_no_match(self, populated):
        assert populated.exact_search("does not exist") == []

    def test_exact_empty_string(self, empty):
        empty.add("d1", "")
        empty.add("d2", "x")
        hits = empty.exact_search("")
        assert len(hits) == 1
        assert hits[0].doc_id == "d1"


class TestMakeSnippet:
    def test_snippet_contains_query(self, empty):
        empty.add(
            "d1",
            "the quick brown fox jumps over the lazy dog and runs away fast",
        )
        s = empty.make_snippet("d1", "fox", max_chars=20)
        assert "fox" in s

    def test_snippet_no_query_match(self, empty):
        empty.add("d1", "alpha beta gamma delta")
        s = empty.make_snippet("d1", "zzz", max_chars=10)
        assert s.startswith("alpha")

    def test_snippet_missing_doc(self, empty):
        assert empty.make_snippet("nope", "x") == ""

    def test_snippet_truncates(self, empty):
        empty.add("d1", "a" * 500)
        s = empty.make_snippet("d1", "", max_chars=50)
        assert len(s) <= 50

    def test_snippet_empty_query(self, empty):
        empty.add("d1", "hello world")
        s = empty.make_snippet("d1", "", max_chars=100)
        assert s == "hello world"


class TestDocCount:
    def test_zero(self, empty):
        assert empty.doc_count == 0

    def test_after_adds(self, populated):
        assert populated.doc_count == 4

    def test_after_remove(self, populated):
        populated.remove("d1")
        assert populated.doc_count == 3


class TestTermCount:
    def test_zero(self, empty):
        assert empty.term_count() == 0

    def test_positive(self, empty):
        empty.add("d1", "alpha beta")
        empty.add("d2", "beta gamma")
        assert empty.term_count() == 3

    def test_after_remove(self, empty):
        empty.add("d1", "alpha")
        empty.add("d2", "beta")
        empty.remove("d1")
        assert empty.term_count() == 1


class TestClear:
    def test_clear(self, populated):
        populated.clear()
        assert populated.doc_count == 0
        assert populated.term_count() == 0

    def test_clear_empty(self, empty):
        empty.clear()
        assert empty.doc_count == 0

    def test_clear_then_add(self, populated):
        populated.clear()
        populated.add("new", "content")
        assert populated.doc_count == 1


class TestAllDocIds:
    def test_empty(self, empty):
        assert empty.all_doc_ids() == []

    def test_populated(self, populated):
        ids = set(populated.all_doc_ids())
        assert ids == {"d1", "d2", "d3", "d4"}

    def test_after_remove(self, populated):
        populated.remove("d1")
        assert "d1" not in populated.all_doc_ids()


class TestEdgeCases:
    def test_search_empty_index(self, empty):
        r = empty.search(SearchRequest(query="anything"))
        assert r.hits == []
        assert r.total == 0

    def test_search_simple(self, populated):
        hits = populated.search_simple("python", top_k=2)
        assert len(hits) <= 2

    def test_search_query_passed_through_in_result(self, populated):
        r = populated.search(SearchRequest(query="python"))
        assert r.query == "python"

    def test_unicode_content(self, empty):
        empty.add("d1", "Привет мир Python агент")
        hits = empty.search_simple("Python")
        assert any(h.doc_id == "d1" for h in hits)

    def test_unicode_query(self, empty):
        empty.add("d1", "Привет мир")
        hits = empty.search_simple("Привет")
        assert len(hits) == 1

    def test_concurrent_writes(self):
        s = DocSearchV2()

        def worker(start):
            for i in range(20):
                s.add(f"d{start}_{i}", f"text {i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert s.doc_count == 80

    def test_all_mode(self, empty):
        empty.add("d1", "python tutorial")
        empty.add("d2", "java tutorial")
        r = empty.search(SearchRequest(query="python", mode=MatchMode.ALL))
        assert any(h.doc_id == "d1" for h in r.hits)
        # ensure ranking favors d1 (more signals)
        assert r.hits[0].doc_id == "d1"

    def test_snippet_attached_to_hits(self, populated):
        r = populated.search(SearchRequest(query="python"))
        for h in r.hits:
            assert h.snippet is not None
