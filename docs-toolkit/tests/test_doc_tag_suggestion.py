"""Tests for E419 DocTagSuggestion."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_tag_suggestion import (
    DocTagSuggestion,
    SuggestionStats,
    TagSuggestion,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
def test_tag_suggestion_dataclass_basic():
    s = TagSuggestion(tag="python", confidence=0.5)
    assert s.tag == "python"
    assert s.confidence == 0.5
    assert s.reason == ""


def test_tag_suggestion_dataclass_with_reason():
    s = TagSuggestion(tag="x", confidence=0.9, reason="co-occurs with: y")
    assert s.reason == "co-occurs with: y"


def test_suggestion_stats_dataclass():
    st = SuggestionStats(total_docs=3, unique_tags=4, total_assignments=8)
    assert st.total_docs == 3
    assert st.unique_tags == 4
    assert st.total_assignments == 8


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
def test_empty_engine_stats():
    e = DocTagSuggestion()
    st = e.stats()
    assert st.total_docs == 0
    assert st.unique_tags == 0
    assert st.total_assignments == 0


def test_empty_all_tags():
    e = DocTagSuggestion()
    assert e.all_tags() == []


def test_empty_all_doc_ids():
    e = DocTagSuggestion()
    assert e.all_doc_ids() == []


# ---------------------------------------------------------------------------
# record_tags
# ---------------------------------------------------------------------------
def test_record_tags_basic():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c"])
    assert e.tags_for_doc("d1") == ["a", "b", "c"]


def test_record_tags_sorted_output():
    e = DocTagSuggestion()
    e.record_tags("d1", ["zebra", "alpha", "mango"])
    assert e.tags_for_doc("d1") == ["alpha", "mango", "zebra"]


def test_record_tags_replaces_existing():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d1", ["x", "y"])
    assert e.tags_for_doc("d1") == ["x", "y"]
    assert e.docs_with_tag("a") == []
    assert e.docs_with_tag("b") == []


def test_record_tags_empty_removes_doc():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d1", [])
    assert e.tags_for_doc("d1") == []
    assert "d1" not in e.all_doc_ids()


def test_record_tags_ignores_empty_strings():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "", "b"])
    assert e.tags_for_doc("d1") == ["a", "b"]


def test_record_tags_dedups():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "a", "b"])
    assert e.tags_for_doc("d1") == ["a", "b"]


def test_record_tags_updates_inverse_index():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a"])
    e.record_tags("d2", ["a"])
    assert e.docs_with_tag("a") == ["d1", "d2"]


def test_record_tags_cooccurrence_built():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["a", "b"])
    pairs = e.cooccurring_with("a")
    assert pairs == [("b", 2)]


def test_record_tags_replaces_cooccurrence():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d1", ["a", "c"])
    # b/a co-occurrence should be gone
    pairs_a = dict(e.cooccurring_with("a"))
    assert pairs_a.get("b") is None
    assert pairs_a.get("c") == 1


def test_record_tags_overlap_only_adjusts_delta():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c"])
    # Now replace with overlap: cooc (a,b) had 1, after replace still has it
    e.record_tags("d1", ["a", "b", "d"])
    pairs_a = dict(e.cooccurring_with("a"))
    assert pairs_a.get("b") == 1
    assert pairs_a.get("d") == 1
    assert pairs_a.get("c") is None


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------
def test_clear_doc_removes_tags():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.clear_doc("d1")
    assert e.tags_for_doc("d1") == []


def test_clear_doc_updates_inverse():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a"])
    e.record_tags("d2", ["a"])
    e.clear_doc("d1")
    assert e.docs_with_tag("a") == ["d2"]


def test_clear_doc_removes_orphan_tags():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.clear_doc("d1")
    assert "a" not in e.all_tags()
    assert "b" not in e.all_tags()


def test_clear_doc_adjusts_cooccurrence():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["a", "b"])
    e.clear_doc("d1")
    pairs = e.cooccurring_with("a")
    assert pairs == [("b", 1)]


def test_clear_doc_nonexistent_silent():
    e = DocTagSuggestion()
    e.clear_doc("ghost")  # should not raise


def test_clear_doc_then_stats():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.clear_doc("d1")
    st = e.stats()
    assert st.total_docs == 0
    assert st.unique_tags == 0
    assert st.total_assignments == 0


# ---------------------------------------------------------------------------
# add_tag
# ---------------------------------------------------------------------------
def test_add_tag_new():
    e = DocTagSuggestion()
    assert e.add_tag("d1", "python") is True
    assert e.tags_for_doc("d1") == ["python"]


def test_add_tag_duplicate():
    e = DocTagSuggestion()
    e.add_tag("d1", "python")
    assert e.add_tag("d1", "python") is False


def test_add_tag_empty_string():
    e = DocTagSuggestion()
    assert e.add_tag("d1", "") is False
    assert e.tags_for_doc("d1") == []


def test_add_tag_updates_cooccurrence():
    e = DocTagSuggestion()
    e.add_tag("d1", "a")
    e.add_tag("d1", "b")
    assert e.cooccurring_with("a") == [("b", 1)]


def test_add_tag_updates_inverse_index():
    e = DocTagSuggestion()
    e.add_tag("d1", "tag")
    assert e.docs_with_tag("tag") == ["d1"]


def test_add_tag_to_existing_doc():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a"])
    e.add_tag("d1", "b")
    assert e.tags_for_doc("d1") == ["a", "b"]


def test_add_tag_cooccurs_with_existing():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.add_tag("d1", "c")
    pairs_a = dict(e.cooccurring_with("a"))
    assert pairs_a["b"] == 1
    assert pairs_a["c"] == 1


# ---------------------------------------------------------------------------
# remove_tag
# ---------------------------------------------------------------------------
def test_remove_tag_existing():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    assert e.remove_tag("d1", "a") is True
    assert e.tags_for_doc("d1") == ["b"]


def test_remove_tag_missing():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a"])
    assert e.remove_tag("d1", "ghost") is False


def test_remove_tag_unknown_doc():
    e = DocTagSuggestion()
    assert e.remove_tag("ghost", "x") is False


def test_remove_tag_updates_cooccurrence():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.remove_tag("d1", "a")
    assert e.cooccurring_with("a") == []
    assert e.cooccurring_with("b") == []


def test_remove_tag_drops_orphan():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a"])
    e.remove_tag("d1", "a")
    assert "a" not in e.all_tags()
    assert "d1" not in e.all_doc_ids()


def test_remove_tag_keeps_doc_when_others_remain():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.remove_tag("d1", "a")
    assert "d1" in e.all_doc_ids()


# ---------------------------------------------------------------------------
# popular_tags
# ---------------------------------------------------------------------------
def test_popular_tags_basic():
    e = DocTagSuggestion()
    e.record_tags("d1", ["python", "ml"])
    e.record_tags("d2", ["python"])
    e.record_tags("d3", ["python", "ml", "data"])
    pop = e.popular_tags()
    assert pop[0] == ("python", 3)
    assert pop[1] == ("ml", 2)


def test_popular_tags_sort_by_name_on_tie():
    e = DocTagSuggestion()
    e.record_tags("d1", ["zeta", "alpha"])
    pop = e.popular_tags()
    # Both have count 1 — alpha first
    assert pop == [("alpha", 1), ("zeta", 1)]


def test_popular_tags_limit():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c", "d"])
    pop = e.popular_tags(limit=2)
    assert len(pop) == 2


def test_popular_tags_empty():
    e = DocTagSuggestion()
    assert e.popular_tags() == []


def test_popular_tags_negative_limit_returns_all():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c"])
    assert len(e.popular_tags(limit=-1)) == 3


# ---------------------------------------------------------------------------
# cooccurring_with
# ---------------------------------------------------------------------------
def test_cooccurring_with_basic():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c"])
    e.record_tags("d2", ["a", "b"])
    co = dict(e.cooccurring_with("a"))
    assert co["b"] == 2
    assert co["c"] == 1


def test_cooccurring_with_unknown_tag():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a"])
    assert e.cooccurring_with("ghost") == []


def test_cooccurring_with_sorted_by_count_desc():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "x"])
    e.record_tags("d2", ["a", "y"])
    e.record_tags("d3", ["a", "y"])
    co = e.cooccurring_with("a")
    assert co[0] == ("y", 2)
    assert co[1] == ("x", 1)


def test_cooccurring_with_limit():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c", "d"])
    co = e.cooccurring_with("a", limit=2)
    assert len(co) == 2


# ---------------------------------------------------------------------------
# suggest_for_doc
# ---------------------------------------------------------------------------
def test_suggest_for_doc_basic():
    e = DocTagSuggestion()
    # ml co-occurs with python often; suggest for a doc with python
    e.record_tags("d1", ["python", "ml"])
    e.record_tags("d2", ["python", "ml"])
    e.record_tags("d3", ["python", "ml"])
    e.record_tags("d4", ["python"])
    e.record_tags("d_target", ["python"])
    suggestions = e.suggest_for_doc("d_target")
    tags = [s.tag for s in suggestions]
    assert "ml" in tags
    assert "python" not in tags  # excluded — already present


def test_suggest_for_doc_excludes_existing():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["a", "b"])
    e.record_tags("d_target", ["a", "b"])
    suggestions = e.suggest_for_doc("d_target")
    for s in suggestions:
        assert s.tag not in ("a", "b")


def test_suggest_for_doc_unknown():
    e = DocTagSuggestion()
    assert e.suggest_for_doc("ghost") == []


def test_suggest_for_doc_returns_tag_suggestion_objects():
    e = DocTagSuggestion()
    e.record_tags("d1", ["python", "ml"])
    e.record_tags("d_target", ["python"])
    suggestions = e.suggest_for_doc("d_target")
    assert all(isinstance(s, TagSuggestion) for s in suggestions)


def test_suggest_for_doc_confidence_capped_at_1():
    e = DocTagSuggestion()
    # Two cross-pairs combine: a→b and c→b both give max ratio
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["c", "b"])
    e.record_tags("d_target", ["a", "c"])
    suggestions = e.suggest_for_doc("d_target")
    # b should be top suggestion; a→b=1/1, c→b=1/1, sum=2.0 capped at 1.0
    assert suggestions[0].tag == "b"
    assert suggestions[0].confidence == 1.0


def test_suggest_for_doc_confidence_fractional():
    e = DocTagSuggestion()
    # 2 docs have "a", 1 of those also has "b" → ratio = 1/2 = 0.5
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["a"])
    suggestions = e.suggest_for_tags(["a"])
    assert suggestions[0].tag == "b"
    assert suggestions[0].confidence == pytest.approx(0.5)


def test_suggest_for_doc_aggregates_across_source_tags():
    e = DocTagSuggestion()
    # Both source tags co-occur with "c" — confidence summed
    e.record_tags("d1", ["a", "c"])
    e.record_tags("d2", ["b", "c"])
    e.record_tags("d_target", ["a", "b"])
    suggestions = e.suggest_for_doc("d_target")
    by_tag = {s.tag: s.confidence for s in suggestions}
    # a→c contributes 1/1 = 1.0, b→c contributes 1/1 = 1.0 → sum capped at 1.0
    assert by_tag["c"] == 1.0


def test_suggest_for_doc_reason_lists_sources():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "c"])
    e.record_tags("d2", ["b", "c"])
    e.record_tags("d_target", ["a", "b"])
    suggestions = e.suggest_for_doc("d_target")
    by_tag = {s.tag: s for s in suggestions}
    assert "a" in by_tag["c"].reason
    assert "b" in by_tag["c"].reason
    assert by_tag["c"].reason.startswith("co-occurs with:")


def test_suggest_for_doc_limit():
    e = DocTagSuggestion()
    e.record_tags("d1", ["x", "a", "b", "c", "d", "e"])
    e.record_tags("d_target", ["x"])
    suggestions = e.suggest_for_doc("d_target", limit=2)
    assert len(suggestions) == 2


def test_suggest_for_doc_sorted_by_confidence_desc():
    e = DocTagSuggestion()
    # b co-occurs with x in 2 docs, c in 1
    e.record_tags("d1", ["x", "b"])
    e.record_tags("d2", ["x", "b"])
    e.record_tags("d3", ["x", "c"])
    e.record_tags("d_target", ["x"])
    suggestions = e.suggest_for_doc("d_target")
    assert suggestions[0].tag == "b"
    assert suggestions[1].tag == "c"


# ---------------------------------------------------------------------------
# suggest_for_tags
# ---------------------------------------------------------------------------
def test_suggest_for_tags_basic():
    e = DocTagSuggestion()
    e.record_tags("d1", ["python", "ml"])
    e.record_tags("d2", ["python", "ml"])
    suggestions = e.suggest_for_tags(["python"])
    tags = [s.tag for s in suggestions]
    assert "ml" in tags


def test_suggest_for_tags_excludes_input():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    suggestions = e.suggest_for_tags(["a"])
    for s in suggestions:
        assert s.tag != "a"


def test_suggest_for_tags_explicit_exclude():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b", "c"])
    suggestions = e.suggest_for_tags(["a"], exclude=["b"])
    tags = [s.tag for s in suggestions]
    assert "b" not in tags
    assert "c" in tags


def test_suggest_for_tags_unknown_input():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    assert e.suggest_for_tags(["unknown"]) == []


def test_suggest_for_tags_empty_input():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    assert e.suggest_for_tags([]) == []


def test_suggest_for_tags_ignores_empty_strings():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["a", "b"])
    suggestions = e.suggest_for_tags(["a", ""])
    tags = [s.tag for s in suggestions]
    assert "b" in tags


def test_suggest_for_tags_limit():
    e = DocTagSuggestion()
    e.record_tags("d1", ["x", "a", "b", "c"])
    suggestions = e.suggest_for_tags(["x"], limit=2)
    assert len(suggestions) == 2


# ---------------------------------------------------------------------------
# tags_for_doc / docs_with_tag
# ---------------------------------------------------------------------------
def test_tags_for_doc_unknown():
    e = DocTagSuggestion()
    assert e.tags_for_doc("ghost") == []


def test_docs_with_tag_unknown():
    e = DocTagSuggestion()
    assert e.docs_with_tag("ghost") == []


def test_docs_with_tag_sorted():
    e = DocTagSuggestion()
    e.record_tags("zebra_doc", ["t"])
    e.record_tags("alpha_doc", ["t"])
    assert e.docs_with_tag("t") == ["alpha_doc", "zebra_doc"]


# ---------------------------------------------------------------------------
# all_tags / all_doc_ids / stats
# ---------------------------------------------------------------------------
def test_all_tags_sorted_unique():
    e = DocTagSuggestion()
    e.record_tags("d1", ["b", "a"])
    e.record_tags("d2", ["a", "c"])
    assert e.all_tags() == ["a", "b", "c"]


def test_all_doc_ids_sorted():
    e = DocTagSuggestion()
    e.record_tags("z", ["t"])
    e.record_tags("a", ["t"])
    assert e.all_doc_ids() == ["a", "z"]


def test_stats_counts_correct():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.record_tags("d2", ["a", "c", "d"])
    st = e.stats()
    assert st.total_docs == 2
    assert st.unique_tags == 4
    assert st.total_assignments == 5


def test_stats_after_mutation():
    e = DocTagSuggestion()
    e.record_tags("d1", ["a", "b"])
    e.add_tag("d1", "c")
    st = e.stats()
    assert st.total_assignments == 3
    assert st.unique_tags == 3


# ---------------------------------------------------------------------------
# Integration scenarios
# ---------------------------------------------------------------------------
def test_full_workflow():
    e = DocTagSuggestion()
    e.record_tags("doc1", ["python", "ml", "ai"])
    e.record_tags("doc2", ["python", "ml"])
    e.record_tags("doc3", ["python", "web"])

    assert "python" in e.all_tags()
    pop = e.popular_tags(limit=1)
    assert pop[0][0] == "python"

    suggestions = e.suggest_for_tags(["python"], limit=3)
    tag_names = [s.tag for s in suggestions]
    assert "ml" in tag_names


def test_co_occurrence_pair_canonical():
    """Internal: pairs are stored alphabetically."""
    e = DocTagSuggestion()
    e.record_tags("d1", ["zebra", "alpha"])
    # Pair should be ('alpha', 'zebra')
    assert ("alpha", "zebra") in e._cooccurrence
    assert ("zebra", "alpha") not in e._cooccurrence


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
def test_thread_safety_concurrent_record():
    e = DocTagSuggestion()
    n_threads = 20
    n_per = 50

    def worker(idx: int):
        for j in range(n_per):
            e.record_tags(f"t{idx}_d{j}", [f"tag{j % 5}", f"common"])

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    st = e.stats()
    assert st.total_docs == n_threads * n_per
    # Every doc has 2 tags
    assert st.total_assignments == n_threads * n_per * 2


def test_thread_safety_concurrent_add_remove():
    e = DocTagSuggestion()
    e.record_tags("doc", ["seed"])

    def adder():
        for i in range(100):
            e.add_tag(f"doc{i}", "common")

    def remover():
        for i in range(50):
            e.remove_tag(f"doc{i}", "common")

    t1 = threading.Thread(target=adder)
    t2 = threading.Thread(target=remover)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # No exception; engine remains consistent
    st = e.stats()
    assert st.total_docs >= 0
    assert st.unique_tags >= 0


def test_thread_safety_concurrent_reads():
    e = DocTagSuggestion()
    for i in range(50):
        e.record_tags(f"d{i}", ["a", "b", "c"])

    results: list[int] = []

    def reader():
        for _ in range(100):
            results.append(len(e.all_tags()))

    threads = [threading.Thread(target=reader) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # All reads should see consistent count of 3
    assert all(r == 3 for r in results)


def test_thread_safety_mixed_operations():
    e = DocTagSuggestion()

    def writer(idx: int):
        for j in range(20):
            e.record_tags(f"w{idx}_d{j}", [f"t{j}", "shared"])

    def reader():
        for _ in range(50):
            e.popular_tags()
            e.all_tags()

    def clearer(idx: int):
        for j in range(10):
            e.clear_doc(f"w{idx}_d{j}")

    threads = []
    for i in range(5):
        threads.append(threading.Thread(target=writer, args=(i,)))
        threads.append(threading.Thread(target=reader))
        threads.append(threading.Thread(target=clearer, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # Should complete without error
    assert e.stats().total_docs >= 0
