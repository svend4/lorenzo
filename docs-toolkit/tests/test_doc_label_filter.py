"""Tests for E414 DocLabelFilter."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_label_filter import DocLabelFilter, FilterStats, LabelSet


# ----------------------------------------------------------------------
# Construction / dataclasses
# ----------------------------------------------------------------------


def test_label_set_default_labels():
    ls = LabelSet(doc_id="d1")
    assert ls.doc_id == "d1"
    assert ls.labels == []


def test_label_set_explicit_labels():
    ls = LabelSet(doc_id="d2", labels=["a", "b"])
    assert ls.labels == ["a", "b"]


def test_filter_stats_fields():
    s = FilterStats(total_docs=2, unique_labels=3, total_label_assignments=5)
    assert s.total_docs == 2
    assert s.unique_labels == 3
    assert s.total_label_assignments == 5


def test_init_empty():
    f = DocLabelFilter()
    assert f.all_labels() == []
    assert f.all_doc_ids() == []
    st = f.stats()
    assert st.total_docs == 0
    assert st.unique_labels == 0
    assert st.total_label_assignments == 0


# ----------------------------------------------------------------------
# add_labels
# ----------------------------------------------------------------------


def test_add_labels_returns_added_count():
    f = DocLabelFilter()
    assert f.add_labels("d1", ["x", "y"]) == 2


def test_add_labels_dedupes_existing():
    f = DocLabelFilter()
    f.add_labels("d1", ["x", "y"])
    assert f.add_labels("d1", ["x", "z"]) == 1
    assert f.get_labels("d1") == ["x", "y", "z"]


def test_add_labels_duplicate_in_input():
    f = DocLabelFilter()
    assert f.add_labels("d1", ["x", "x", "y"]) == 2
    assert f.get_labels("d1") == ["x", "y"]


def test_add_labels_empty_list():
    f = DocLabelFilter()
    assert f.add_labels("d1", []) == 0
    assert f.all_doc_ids() == []


def test_add_labels_multiple_docs():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["a", "b"])
    assert f.docs_with_label("a") == ["d1", "d2"]
    assert f.docs_with_label("b") == ["d2"]


# ----------------------------------------------------------------------
# remove_labels
# ----------------------------------------------------------------------


def test_remove_labels_existing():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b", "c"])
    assert f.remove_labels("d1", ["a", "b"]) == 2
    assert f.get_labels("d1") == ["c"]


def test_remove_labels_not_present():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    assert f.remove_labels("d1", ["x", "y"]) == 0
    assert f.get_labels("d1") == ["a"]


def test_remove_labels_unknown_doc():
    f = DocLabelFilter()
    assert f.remove_labels("nope", ["x"]) == 0


def test_remove_labels_partial_match():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    assert f.remove_labels("d1", ["a", "x"]) == 1


def test_remove_labels_drops_empty_doc():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.remove_labels("d1", ["a"])
    assert f.all_doc_ids() == []


def test_remove_labels_drops_empty_label_index():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.remove_labels("d1", ["a"])
    assert f.all_labels() == []


# ----------------------------------------------------------------------
# set_labels
# ----------------------------------------------------------------------


def test_set_labels_returns_label_set():
    f = DocLabelFilter()
    res = f.set_labels("d1", ["b", "a"])
    assert isinstance(res, LabelSet)
    assert res.doc_id == "d1"
    assert res.labels == ["a", "b"]


def test_set_labels_replaces_existing():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    res = f.set_labels("d1", ["c", "d"])
    assert res.labels == ["c", "d"]
    assert f.get_labels("d1") == ["c", "d"]


def test_set_labels_empty_clears_doc():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.set_labels("d1", [])
    assert f.all_doc_ids() == []
    assert f.all_labels() == []


def test_set_labels_deduplicates():
    f = DocLabelFilter()
    res = f.set_labels("d1", ["x", "x", "y"])
    assert res.labels == ["x", "y"]


def test_set_labels_removes_orphan_label():
    f = DocLabelFilter()
    f.add_labels("d1", ["only"])
    f.set_labels("d1", ["other"])
    assert "only" not in f.all_labels()
    assert "other" in f.all_labels()


def test_set_labels_keeps_label_used_by_others():
    f = DocLabelFilter()
    f.add_labels("d1", ["shared"])
    f.add_labels("d2", ["shared"])
    f.set_labels("d1", [])
    assert "shared" in f.all_labels()
    assert f.docs_with_label("shared") == ["d2"]


# ----------------------------------------------------------------------
# get_labels
# ----------------------------------------------------------------------


def test_get_labels_sorted():
    f = DocLabelFilter()
    f.add_labels("d1", ["c", "a", "b"])
    assert f.get_labels("d1") == ["a", "b", "c"]


def test_get_labels_unknown_doc():
    f = DocLabelFilter()
    assert f.get_labels("nope") == []


# ----------------------------------------------------------------------
# clear_doc
# ----------------------------------------------------------------------


def test_clear_doc_returns_count():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b", "c"])
    assert f.clear_doc("d1") == 3


def test_clear_doc_empties_state():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    f.clear_doc("d1")
    assert f.get_labels("d1") == []
    assert f.all_doc_ids() == []
    assert f.all_labels() == []


def test_clear_doc_unknown():
    f = DocLabelFilter()
    assert f.clear_doc("ghost") == 0


def test_clear_doc_preserves_shared_labels():
    f = DocLabelFilter()
    f.add_labels("d1", ["x"])
    f.add_labels("d2", ["x"])
    f.clear_doc("d1")
    assert "x" in f.all_labels()
    assert f.docs_with_label("x") == ["d2"]


# ----------------------------------------------------------------------
# filter_any (OR)
# ----------------------------------------------------------------------


def test_filter_any_basic():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    f.add_labels("d3", ["c"])
    assert f.filter_any(["a", "b"]) == ["d1", "d2"]


def test_filter_any_empty_returns_empty():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    assert f.filter_any([]) == []


def test_filter_any_no_matches():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    assert f.filter_any(["nope"]) == []


def test_filter_any_dedupes_docs():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    assert f.filter_any(["a", "b"]) == ["d1"]


# ----------------------------------------------------------------------
# filter_all (AND)
# ----------------------------------------------------------------------


def test_filter_all_basic():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    f.add_labels("d2", ["a"])
    assert f.filter_all(["a", "b"]) == ["d1"]


def test_filter_all_empty_returns_all_docs():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    assert f.filter_all([]) == ["d1", "d2"]


def test_filter_all_missing_label_short_circuits():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    assert f.filter_all(["a", "ghost"]) == []


def test_filter_all_single_label():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["a"])
    assert f.filter_all(["a"]) == ["d1", "d2"]


def test_filter_all_three_labels():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b", "c"])
    f.add_labels("d2", ["a", "b"])
    assert f.filter_all(["a", "b", "c"]) == ["d1"]


# ----------------------------------------------------------------------
# filter_none (NOT)
# ----------------------------------------------------------------------


def test_filter_none_basic():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    f.add_labels("d3", ["c"])
    assert f.filter_none(["a"]) == ["d2", "d3"]


def test_filter_none_empty_returns_all():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    assert f.filter_none([]) == ["d1", "d2"]


def test_filter_none_excludes_multiple():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    f.add_labels("d3", ["c"])
    assert f.filter_none(["a", "b"]) == ["d3"]


def test_filter_none_excludes_all():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["a"])
    assert f.filter_none(["a"]) == []


# ----------------------------------------------------------------------
# filter_combo
# ----------------------------------------------------------------------


def test_filter_combo_basic():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "x"])
    f.add_labels("d2", ["a"])
    f.add_labels("d3", ["a", "y"])
    assert f.filter_combo(["a"], ["x"]) == ["d2", "d3"]


def test_filter_combo_both_empty_returns_all_docs():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    assert f.filter_combo([], []) == ["d1", "d2"]


def test_filter_combo_empty_must_have_with_exclusion():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    assert f.filter_combo([], ["a"]) == ["d2"]


def test_filter_combo_empty_must_not_have():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    f.add_labels("d2", ["a"])
    assert f.filter_combo(["a"], []) == ["d1", "d2"]


def test_filter_combo_must_have_unknown_label():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    assert f.filter_combo(["nope"], []) == []


def test_filter_combo_complex():
    f = DocLabelFilter()
    f.add_labels("d1", ["python", "tutorial"])
    f.add_labels("d2", ["python", "tutorial", "outdated"])
    f.add_labels("d3", ["python", "reference"])
    f.add_labels("d4", ["go", "tutorial"])
    assert f.filter_combo(["python", "tutorial"], ["outdated"]) == ["d1"]


# ----------------------------------------------------------------------
# docs_with_label
# ----------------------------------------------------------------------


def test_docs_with_label_sorted():
    f = DocLabelFilter()
    f.add_labels("z", ["t"])
    f.add_labels("a", ["t"])
    f.add_labels("m", ["t"])
    assert f.docs_with_label("t") == ["a", "m", "z"]


def test_docs_with_label_unknown():
    f = DocLabelFilter()
    assert f.docs_with_label("ghost") == []


# ----------------------------------------------------------------------
# top_labels
# ----------------------------------------------------------------------


def test_top_labels_by_count_desc():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    f.add_labels("d2", ["a"])
    f.add_labels("d3", ["a", "c"])
    top = f.top_labels()
    assert top[0] == ("a", 3)


def test_top_labels_limit():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b", "c", "d"])
    assert len(f.top_labels(limit=2)) == 2


def test_top_labels_tiebreak_alpha():
    f = DocLabelFilter()
    f.add_labels("d1", ["b"])
    f.add_labels("d2", ["a"])
    top = f.top_labels()
    # both count == 1, alphabetical
    assert top == [("a", 1), ("b", 1)]


def test_top_labels_empty():
    f = DocLabelFilter()
    assert f.top_labels() == []


def test_top_labels_negative_limit_returns_empty():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    assert f.top_labels(limit=-3) == []


def test_top_labels_default_limit_10():
    f = DocLabelFilter()
    for i in range(15):
        f.add_labels(f"d{i}", [f"lbl{i}"])
    assert len(f.top_labels()) == 10


# ----------------------------------------------------------------------
# all_labels / all_doc_ids
# ----------------------------------------------------------------------


def test_all_labels_sorted_unique():
    f = DocLabelFilter()
    f.add_labels("d1", ["c", "a"])
    f.add_labels("d2", ["b", "a"])
    assert f.all_labels() == ["a", "b", "c"]


def test_all_doc_ids_sorted():
    f = DocLabelFilter()
    f.add_labels("zeta", ["x"])
    f.add_labels("alpha", ["x"])
    assert f.all_doc_ids() == ["alpha", "zeta"]


def test_all_doc_ids_excludes_cleared():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["b"])
    f.clear_doc("d1")
    assert f.all_doc_ids() == ["d2"]


# ----------------------------------------------------------------------
# stats
# ----------------------------------------------------------------------


def test_stats_counts():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    f.add_labels("d2", ["a"])
    s = f.stats()
    assert s.total_docs == 2
    assert s.unique_labels == 2
    assert s.total_label_assignments == 3


def test_stats_after_clear():
    f = DocLabelFilter()
    f.add_labels("d1", ["a", "b"])
    f.clear_doc("d1")
    s = f.stats()
    assert s.total_docs == 0
    assert s.unique_labels == 0
    assert s.total_label_assignments == 0


# ----------------------------------------------------------------------
# Encapsulation: returned collections should not affect internal state
# ----------------------------------------------------------------------


def test_returned_label_list_is_independent():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    lst = f.get_labels("d1")
    lst.append("hack")
    assert f.get_labels("d1") == ["a"]


def test_set_labels_input_mutation_does_not_affect_state():
    f = DocLabelFilter()
    inputs = ["a", "b"]
    f.set_labels("d1", inputs)
    inputs.append("c")
    assert f.get_labels("d1") == ["a", "b"]


# ----------------------------------------------------------------------
# Thread safety
# ----------------------------------------------------------------------


def test_thread_safety_concurrent_adds():
    f = DocLabelFilter()
    errors: list[Exception] = []

    def worker(doc_id: str, n: int) -> None:
        try:
            for i in range(n):
                f.add_labels(doc_id, [f"l{i}"])
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(exc)

    threads = [
        threading.Thread(target=worker, args=(f"d{t}", 50))
        for t in range(8)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(f.all_doc_ids()) == 8
    for did in f.all_doc_ids():
        assert len(f.get_labels(did)) == 50


def test_thread_safety_mixed_ops():
    f = DocLabelFilter()
    errors: list[Exception] = []

    def adder() -> None:
        try:
            for i in range(100):
                f.add_labels("shared", [f"l{i}"])
        except Exception as exc:
            errors.append(exc)

    def remover() -> None:
        try:
            for i in range(100):
                f.remove_labels("shared", [f"l{i}"])
        except Exception as exc:
            errors.append(exc)

    def reader() -> None:
        try:
            for _ in range(100):
                f.stats()
                f.all_labels()
                f.get_labels("shared")
        except Exception as exc:
            errors.append(exc)

    threads = [
        threading.Thread(target=adder),
        threading.Thread(target=adder),
        threading.Thread(target=remover),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors


def test_thread_safety_concurrent_set_labels():
    f = DocLabelFilter()
    errors: list[Exception] = []

    def worker(idx: int) -> None:
        try:
            for i in range(30):
                f.set_labels(f"d{idx}", [f"x{i}", f"y{i}"])
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    # Each doc should end with the last set of labels (size 2).
    for did in f.all_doc_ids():
        assert len(f.get_labels(did)) == 2


# ----------------------------------------------------------------------
# Integration scenarios
# ----------------------------------------------------------------------


def test_full_lifecycle_scenario():
    f = DocLabelFilter()
    # populate
    f.add_labels("d1", ["python", "tutorial"])
    f.add_labels("d2", ["python", "reference"])
    f.add_labels("d3", ["go", "tutorial"])
    f.add_labels("d4", ["python", "tutorial", "deprecated"])

    # AND
    assert f.filter_all(["python", "tutorial"]) == ["d1", "d4"]
    # OR
    assert f.filter_any(["go", "reference"]) == ["d2", "d3"]
    # NOT
    assert f.filter_none(["go"]) == ["d1", "d2", "d4"]
    # Combo
    assert f.filter_combo(["python", "tutorial"], ["deprecated"]) == ["d1"]

    # Modify and re-check
    f.remove_labels("d4", ["deprecated"])
    assert f.filter_combo(["python", "tutorial"], ["deprecated"]) == ["d1", "d4"]

    # Cleanup
    f.clear_doc("d3")
    assert "go" not in f.all_labels()
    assert "d3" not in f.all_doc_ids()


def test_repeated_set_labels_idempotent():
    f = DocLabelFilter()
    res1 = f.set_labels("d1", ["a", "b"])
    res2 = f.set_labels("d1", ["a", "b"])
    assert res1.labels == res2.labels == ["a", "b"]
    assert f.stats().total_label_assignments == 2


def test_stats_unique_labels_independent_of_doc_count():
    f = DocLabelFilter()
    f.add_labels("d1", ["a"])
    f.add_labels("d2", ["a"])
    f.add_labels("d3", ["a"])
    s = f.stats()
    assert s.unique_labels == 1
    assert s.total_docs == 3
    assert s.total_label_assignments == 3


def test_add_then_remove_then_re_add():
    f = DocLabelFilter()
    f.add_labels("d1", ["x"])
    f.remove_labels("d1", ["x"])
    assert f.all_doc_ids() == []
    f.add_labels("d1", ["x"])
    assert f.get_labels("d1") == ["x"]


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
