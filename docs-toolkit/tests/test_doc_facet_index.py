"""Tests for E378 DocFacetIndex."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_facet_index import (
    DocFacetIndex,
    FacetResult,
    FacetStats,
    FacetValue,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestFacetValueDataclass:
    def test_basic_fields(self):
        fv = FacetValue(value="python", count=3)
        assert fv.value == "python"
        assert fv.count == 3

    def test_equality(self):
        assert FacetValue("a", 1) == FacetValue("a", 1)

    def test_inequality(self):
        assert FacetValue("a", 1) != FacetValue("a", 2)

    def test_zero_count(self):
        fv = FacetValue(value="x", count=0)
        assert fv.count == 0


class TestFacetResultDataclass:
    def test_default_values_empty(self):
        fr = FacetResult(facet="tag")
        assert fr.facet == "tag"
        assert fr.values == []

    def test_with_values(self):
        values = [FacetValue("a", 2), FacetValue("b", 1)]
        fr = FacetResult(facet="lang", values=values)
        assert fr.facet == "lang"
        assert len(fr.values) == 2

    def test_default_factory_is_independent(self):
        a = FacetResult(facet="x")
        b = FacetResult(facet="y")
        a.values.append(FacetValue("v", 1))
        assert b.values == []


class TestFacetStatsDataclass:
    def test_basic(self):
        s = FacetStats(total_docs=3, total_facets=2, total_facet_assignments=5)
        assert s.total_docs == 3
        assert s.total_facets == 2
        assert s.total_facet_assignments == 5

    def test_zero_stats(self):
        s = FacetStats(0, 0, 0)
        assert s.total_docs == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_on_creation(self):
        idx = DocFacetIndex()
        assert idx.all_facets() == []

    def test_stats_empty(self):
        idx = DocFacetIndex()
        s = idx.stats()
        assert s.total_docs == 0
        assert s.total_facets == 0
        assert s.total_facet_assignments == 0

    def test_independent_instances(self):
        a = DocFacetIndex()
        b = DocFacetIndex()
        a.add_facet("d1", "lang", "py")
        assert b.all_facets() == []


# ---------------------------------------------------------------------------
# add_facet
# ---------------------------------------------------------------------------


class TestAddFacet:
    def test_add_returns_true_first_time(self):
        idx = DocFacetIndex()
        assert idx.add_facet("d1", "lang", "py") is True

    def test_add_returns_false_on_duplicate(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.add_facet("d1", "lang", "py") is False

    def test_add_multiple_values_same_facet(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "rs")
        assert idx.facets_for_doc("d1") == {"lang": ["py", "rs"]}

    def test_add_multiple_facets_same_doc(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "year", "2024")
        f = idx.facets_for_doc("d1")
        assert f == {"lang": ["py"], "year": ["2024"]}

    def test_add_indexes_into_facet_lookup(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.docs_with_facet("lang", "py") == ["d1"]

    def test_add_same_value_different_docs(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        assert idx.docs_with_facet("lang", "py") == ["d1", "d2"]


# ---------------------------------------------------------------------------
# remove_facet
# ---------------------------------------------------------------------------


class TestRemoveFacet:
    def test_remove_existing_returns_true(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.remove_facet("d1", "lang", "py") is True

    def test_remove_missing_doc_returns_false(self):
        idx = DocFacetIndex()
        assert idx.remove_facet("d1", "lang", "py") is False

    def test_remove_missing_facet_returns_false(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.remove_facet("d1", "other", "py") is False

    def test_remove_missing_value_returns_false(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.remove_facet("d1", "lang", "rs") is False

    def test_remove_clears_from_inverted_index(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.remove_facet("d1", "lang", "py")
        assert idx.docs_with_facet("lang", "py") == []

    def test_remove_clears_from_doc_view(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.remove_facet("d1", "lang", "py")
        assert idx.facets_for_doc("d1") == {}

    def test_remove_one_keeps_others(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "rs")
        idx.remove_facet("d1", "lang", "py")
        assert idx.facets_for_doc("d1") == {"lang": ["rs"]}

    def test_remove_collapses_empty_facets(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.remove_facet("d1", "lang", "py")
        assert "lang" not in idx.all_facets()


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_clear_missing_doc_returns_zero(self):
        idx = DocFacetIndex()
        assert idx.clear_doc("ghost") == 0

    def test_clear_counts_assignments(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "rs")
        idx.add_facet("d1", "year", "2024")
        assert idx.clear_doc("d1") == 3

    def test_clear_removes_doc_state(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.clear_doc("d1")
        assert idx.facets_for_doc("d1") == {}

    def test_clear_removes_from_inverted_index(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.clear_doc("d1")
        assert idx.docs_with_facet("lang", "py") == []

    def test_clear_does_not_affect_other_docs(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        idx.clear_doc("d1")
        assert idx.docs_with_facet("lang", "py") == ["d2"]


# ---------------------------------------------------------------------------
# clear_facet
# ---------------------------------------------------------------------------


class TestClearFacet:
    def test_clear_missing_facet_returns_zero(self):
        idx = DocFacetIndex()
        assert idx.clear_facet("lang") == 0

    def test_clear_counts_all_doc_value_pairs(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        idx.add_facet("d1", "lang", "rs")
        assert idx.clear_facet("lang") == 3

    def test_clear_removes_facet_globally(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.clear_facet("lang")
        assert "lang" not in idx.all_facets()

    def test_clear_keeps_other_facets_intact(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "year", "2024")
        idx.clear_facet("lang")
        assert idx.facets_for_doc("d1") == {"year": ["2024"]}

    def test_clear_removes_empty_docs(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.clear_facet("lang")
        # d1 no longer has any facets — facets_for_doc returns empty
        assert idx.facets_for_doc("d1") == {}


# ---------------------------------------------------------------------------
# facets_for_doc
# ---------------------------------------------------------------------------


class TestFacetsForDoc:
    def test_returns_empty_for_unknown(self):
        idx = DocFacetIndex()
        assert idx.facets_for_doc("ghost") == {}

    def test_values_are_sorted(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "rs")
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "go")
        assert idx.facets_for_doc("d1") == {"lang": ["go", "py", "rs"]}

    def test_returns_copy_not_internal(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        d = idx.facets_for_doc("d1")
        d["lang"].append("hacked")
        # Internal state intact
        assert idx.facets_for_doc("d1") == {"lang": ["py"]}

    def test_multiple_facets(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "year", "2024")
        result = idx.facets_for_doc("d1")
        assert set(result.keys()) == {"lang", "year"}


# ---------------------------------------------------------------------------
# docs_with_facet
# ---------------------------------------------------------------------------


class TestDocsWithFacet:
    def test_empty_when_unknown_facet(self):
        idx = DocFacetIndex()
        assert idx.docs_with_facet("lang", "py") == []

    def test_empty_when_unknown_value(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.docs_with_facet("lang", "rs") == []

    def test_returns_sorted(self):
        idx = DocFacetIndex()
        idx.add_facet("z", "lang", "py")
        idx.add_facet("a", "lang", "py")
        idx.add_facet("m", "lang", "py")
        assert idx.docs_with_facet("lang", "py") == ["a", "m", "z"]

    def test_single_match(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.docs_with_facet("lang", "py") == ["d1"]


# ---------------------------------------------------------------------------
# docs_matching
# ---------------------------------------------------------------------------


class TestDocsMatching:
    def test_empty_criteria_returns_all_docs(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "rs")
        assert idx.docs_matching({}) == ["d1", "d2"]

    def test_single_criterion(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "rs")
        assert idx.docs_matching({"lang": "py"}) == ["d1"]

    def test_and_semantics(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "year", "2024")
        idx.add_facet("d2", "lang", "py")
        idx.add_facet("d2", "year", "2023")
        assert idx.docs_matching({"lang": "py", "year": "2024"}) == ["d1"]

    def test_no_match_returns_empty(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.docs_matching({"lang": "rs"}) == []

    def test_unknown_facet_returns_empty(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        assert idx.docs_matching({"missing": "x"}) == []

    def test_result_is_sorted(self):
        idx = DocFacetIndex()
        for d in ["z", "a", "m"]:
            idx.add_facet(d, "lang", "py")
        assert idx.docs_matching({"lang": "py"}) == ["a", "m", "z"]


# ---------------------------------------------------------------------------
# facet_result
# ---------------------------------------------------------------------------


class TestFacetResult:
    def test_unknown_facet_returns_empty(self):
        idx = DocFacetIndex()
        r = idx.facet_result("missing")
        assert isinstance(r, FacetResult)
        assert r.facet == "missing"
        assert r.values == []

    def test_counts_all_when_no_candidates(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        idx.add_facet("d3", "lang", "rs")
        r = idx.facet_result("lang")
        assert r.facet == "lang"
        assert r.values == [FacetValue("py", 2), FacetValue("rs", 1)]

    def test_sorts_by_count_desc_then_value_asc(self):
        idx = DocFacetIndex()
        # Build counts: py=2, go=2, rs=1
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        idx.add_facet("d3", "lang", "go")
        idx.add_facet("d4", "lang", "go")
        idx.add_facet("d5", "lang", "rs")
        r = idx.facet_result("lang")
        assert r.values == [
            FacetValue("go", 2),
            FacetValue("py", 2),
            FacetValue("rs", 1),
        ]

    def test_candidate_filter(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        idx.add_facet("d3", "lang", "rs")
        r = idx.facet_result("lang", candidate_docs=["d1", "d3"])
        assert r.values == [FacetValue("py", 1), FacetValue("rs", 1)]

    def test_candidate_filter_drops_zero_counts(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "rs")
        r = idx.facet_result("lang", candidate_docs=["d1"])
        assert r.values == [FacetValue("py", 1)]

    def test_candidate_empty_list_yields_no_counts(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        r = idx.facet_result("lang", candidate_docs=[])
        assert r.values == []


# ---------------------------------------------------------------------------
# all_facets
# ---------------------------------------------------------------------------


class TestAllFacets:
    def test_empty(self):
        idx = DocFacetIndex()
        assert idx.all_facets() == []

    def test_sorted(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "z", "v")
        idx.add_facet("d1", "a", "v")
        idx.add_facet("d1", "m", "v")
        assert idx.all_facets() == ["a", "m", "z"]

    def test_unique(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "rs")
        assert idx.all_facets() == ["lang"]


# ---------------------------------------------------------------------------
# values_of
# ---------------------------------------------------------------------------


class TestValuesOf:
    def test_unknown_facet(self):
        idx = DocFacetIndex()
        assert idx.values_of("missing") == []

    def test_sorted_values(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "rs")
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "go")
        assert idx.values_of("lang") == ["go", "py", "rs"]

    def test_unique_values(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "py")
        assert idx.values_of("lang") == ["py"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_counts_docs(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "rs")
        assert idx.stats().total_docs == 2

    def test_counts_facets(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "year", "2024")
        assert idx.stats().total_facets == 2

    def test_counts_assignments(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "rs")
        idx.add_facet("d2", "lang", "py")
        assert idx.stats().total_facet_assignments == 3

    def test_stats_after_remove(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "lang", "rs")
        idx.remove_facet("d1", "lang", "py")
        s = idx.stats()
        assert s.total_facet_assignments == 1
        assert s.total_docs == 1
        assert s.total_facets == 1

    def test_stats_after_clear_doc(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d2", "lang", "rs")
        idx.clear_doc("d1")
        s = idx.stats()
        assert s.total_docs == 1
        assert s.total_facet_assignments == 1

    def test_stats_after_clear_facet(self):
        idx = DocFacetIndex()
        idx.add_facet("d1", "lang", "py")
        idx.add_facet("d1", "year", "2024")
        idx.clear_facet("lang")
        s = idx.stats()
        assert s.total_facets == 1
        assert s.total_facet_assignments == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_adds_unique_keys(self):
        idx = DocFacetIndex()

        def worker(i: int) -> None:
            for j in range(50):
                idx.add_facet(f"d{i}_{j}", "lang", "py")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = idx.stats()
        assert s.total_docs == 8 * 50
        assert s.total_facet_assignments == 8 * 50

    def test_concurrent_adds_same_key_idempotent(self):
        idx = DocFacetIndex()

        def worker() -> None:
            for _ in range(100):
                idx.add_facet("d1", "lang", "py")

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert idx.docs_with_facet("lang", "py") == ["d1"]
        assert idx.stats().total_facet_assignments == 1

    def test_concurrent_add_remove(self):
        idx = DocFacetIndex()
        for i in range(50):
            idx.add_facet(f"d{i}", "lang", "py")

        def adder() -> None:
            for i in range(50, 100):
                idx.add_facet(f"d{i}", "lang", "py")

        def remover() -> None:
            for i in range(50):
                idx.remove_facet(f"d{i}", "lang", "py")

        t1 = threading.Thread(target=adder)
        t2 = threading.Thread(target=remover)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Should end up with exactly the 50 new docs
        docs = idx.docs_with_facet("lang", "py")
        assert len(docs) == 50
        assert all(d.startswith("d") for d in docs)

    def test_concurrent_reads_during_writes(self):
        idx = DocFacetIndex()
        stop = threading.Event()
        errors: list = []

        def writer() -> None:
            for i in range(200):
                idx.add_facet(f"d{i}", "lang", "py")
            stop.set()

        def reader() -> None:
            try:
                while not stop.is_set():
                    idx.all_facets()
                    idx.stats()
                    idx.facet_result("lang")
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        w = threading.Thread(target=writer)
        r = threading.Thread(target=reader)
        w.start()
        r.start()
        w.join()
        r.join()

        assert errors == []
        assert idx.stats().total_docs == 200


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
