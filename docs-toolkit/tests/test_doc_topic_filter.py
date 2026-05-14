"""Tests for E444 DocTopicFilter."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_topic_filter import (
    DocTopicFilter,
    FilterStats,
    TopicMembership,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------

def test_topic_membership_defaults():
    m = TopicMembership(doc_id="d1")
    assert m.doc_id == "d1"
    assert m.topics == []
    assert m.weights == {}


def test_topic_membership_with_values():
    m = TopicMembership(doc_id="d1", topics=["a", "b"], weights={"a": 0.5, "b": 1.0})
    assert m.topics == ["a", "b"]
    assert m.weights == {"a": 0.5, "b": 1.0}


def test_topic_membership_independent_defaults():
    a = TopicMembership(doc_id="a")
    b = TopicMembership(doc_id="b")
    a.topics.append("x")
    a.weights["x"] = 1.0
    assert b.topics == []
    assert b.weights == {}


def test_filter_stats_fields():
    s = FilterStats(total_docs=3, unique_topics=2, total_memberships=5)
    assert s.total_docs == 3
    assert s.unique_topics == 2
    assert s.total_memberships == 5


# ---------------------------------------------------------------------------
# assign_topic
# ---------------------------------------------------------------------------

def test_assign_topic_new_returns_true():
    f = DocTopicFilter()
    assert f.assign_topic("d1", "ml", 0.7) is True


def test_assign_topic_same_weight_returns_false():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.7)
    assert f.assign_topic("d1", "ml", 0.7) is False


def test_assign_topic_changed_weight_returns_true():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.7)
    assert f.assign_topic("d1", "ml", 0.9) is True
    assert f.weight_of("d1", "ml") == 0.9


def test_assign_topic_default_weight():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    assert f.weight_of("d1", "ml") == 1.0


def test_assign_topic_clamps_above_one():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 5.0)
    assert f.weight_of("d1", "ml") == 1.0


def test_assign_topic_clamps_below_zero():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", -0.3)
    assert f.weight_of("d1", "ml") == 0.0


def test_assign_topic_multiple_topics_per_doc():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.8)
    f.assign_topic("d1", "ai", 0.5)
    assert set(f.topics_of("d1")) == {"ml", "ai"}


def test_assign_topic_multiple_docs_per_topic():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.8)
    f.assign_topic("d2", "ml", 0.5)
    assert f.docs_in_topic("ml") == ["d1", "d2"]


# ---------------------------------------------------------------------------
# unassign_topic
# ---------------------------------------------------------------------------

def test_unassign_topic_existing_returns_true():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    assert f.unassign_topic("d1", "ml") is True


def test_unassign_topic_missing_returns_false():
    f = DocTopicFilter()
    assert f.unassign_topic("d1", "ml") is False


def test_unassign_topic_removes_membership():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.unassign_topic("d1", "ml")
    assert f.weight_of("d1", "ml") is None
    assert f.docs_in_topic("ml") == []


def test_unassign_topic_cleans_empty_doc():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.unassign_topic("d1", "ml")
    assert "d1" not in f.all_doc_ids()


def test_unassign_topic_cleans_empty_topic():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.unassign_topic("d1", "ml")
    assert "ml" not in f.all_topics()


def test_unassign_keeps_other_assignments():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    f.unassign_topic("d1", "ml")
    assert f.topics_of("d1") == ["ai"]


# ---------------------------------------------------------------------------
# set_topics
# ---------------------------------------------------------------------------

def test_set_topics_replaces_all():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.5)
    f.assign_topic("d1", "ai", 0.7)
    f.set_topics("d1", {"new": 0.9})
    assert f.topics_of("d1") == ["new"]
    assert f.weight_of("d1", "ml") is None
    assert f.weight_of("d1", "ai") is None


def test_set_topics_empty_removes_doc():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.set_topics("d1", {})
    assert "d1" not in f.all_doc_ids()


def test_set_topics_clamps_weights():
    f = DocTopicFilter()
    f.set_topics("d1", {"a": 2.0, "b": -1.0, "c": 0.5})
    assert f.weight_of("d1", "a") == 1.0
    assert f.weight_of("d1", "b") == 0.0
    assert f.weight_of("d1", "c") == 0.5


def test_set_topics_new_doc():
    f = DocTopicFilter()
    f.set_topics("d1", {"a": 0.5, "b": 0.7})
    assert sorted(f.topics_of("d1")) == ["a", "b"]


def test_set_topics_cleans_old_topic_index():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.set_topics("d1", {"ai": 1.0})
    assert "ml" not in f.all_topics()


# ---------------------------------------------------------------------------
# weight_of
# ---------------------------------------------------------------------------

def test_weight_of_missing_doc():
    f = DocTopicFilter()
    assert f.weight_of("missing", "ml") is None


def test_weight_of_missing_topic():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    assert f.weight_of("d1", "missing") is None


def test_weight_of_returns_value():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.42)
    assert f.weight_of("d1", "ml") == 0.42


# ---------------------------------------------------------------------------
# topics_of
# ---------------------------------------------------------------------------

def test_topics_of_missing_doc():
    f = DocTopicFilter()
    assert f.topics_of("nope") == []


def test_topics_of_sorted_by_weight_desc():
    f = DocTopicFilter()
    f.assign_topic("d1", "a", 0.3)
    f.assign_topic("d1", "b", 0.9)
    f.assign_topic("d1", "c", 0.5)
    assert f.topics_of("d1") == ["b", "c", "a"]


def test_topics_of_tiebreak_by_topic_asc():
    f = DocTopicFilter()
    f.assign_topic("d1", "zz", 0.5)
    f.assign_topic("d1", "aa", 0.5)
    f.assign_topic("d1", "mm", 0.5)
    assert f.topics_of("d1") == ["aa", "mm", "zz"]


# ---------------------------------------------------------------------------
# docs_in_topic
# ---------------------------------------------------------------------------

def test_docs_in_topic_missing():
    f = DocTopicFilter()
    assert f.docs_in_topic("missing") == []


def test_docs_in_topic_basic_sorted():
    f = DocTopicFilter()
    f.assign_topic("zeta", "ml", 0.5)
    f.assign_topic("alpha", "ml", 0.5)
    f.assign_topic("mid", "ml", 0.5)
    assert f.docs_in_topic("ml") == ["alpha", "mid", "zeta"]


def test_docs_in_topic_min_weight_filter():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.3)
    f.assign_topic("d2", "ml", 0.6)
    f.assign_topic("d3", "ml", 0.9)
    assert f.docs_in_topic("ml", min_weight=0.5) == ["d2", "d3"]


def test_docs_in_topic_min_weight_inclusive():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.5)
    assert f.docs_in_topic("ml", min_weight=0.5) == ["d1"]


# ---------------------------------------------------------------------------
# filter_any
# ---------------------------------------------------------------------------

def test_filter_any_empty():
    f = DocTopicFilter()
    assert f.filter_any([]) == []


def test_filter_any_or_union():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d2", "ai")
    f.assign_topic("d3", "ml")
    f.assign_topic("d4", "other")
    assert f.filter_any(["ml", "ai"]) == ["d1", "d2", "d3"]


def test_filter_any_min_weight():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.2)
    f.assign_topic("d2", "ml", 0.7)
    f.assign_topic("d3", "ai", 0.9)
    assert f.filter_any(["ml", "ai"], min_weight=0.5) == ["d2", "d3"]


def test_filter_any_dedup():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    # d1 matches both; should appear once
    assert f.filter_any(["ml", "ai"]) == ["d1"]


def test_filter_any_unknown_topic():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    assert f.filter_any(["unknown"]) == []


# ---------------------------------------------------------------------------
# filter_all
# ---------------------------------------------------------------------------

def test_filter_all_empty():
    f = DocTopicFilter()
    assert f.filter_all([]) == []


def test_filter_all_and_intersection():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    f.assign_topic("d2", "ml")
    f.assign_topic("d3", "ai")
    assert f.filter_all(["ml", "ai"]) == ["d1"]


def test_filter_all_min_weight():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.9)
    f.assign_topic("d1", "ai", 0.2)
    f.assign_topic("d2", "ml", 0.9)
    f.assign_topic("d2", "ai", 0.9)
    assert f.filter_all(["ml", "ai"], min_weight=0.5) == ["d2"]


def test_filter_all_unknown_topic_returns_empty():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    assert f.filter_all(["ml", "unknown"]) == []


def test_filter_all_single_topic():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d2", "ml")
    assert f.filter_all(["ml"]) == ["d1", "d2"]


# ---------------------------------------------------------------------------
# top_docs_in_topic
# ---------------------------------------------------------------------------

def test_top_docs_in_topic_empty():
    f = DocTopicFilter()
    assert f.top_docs_in_topic("ml") == []


def test_top_docs_in_topic_sorted_by_weight_desc():
    f = DocTopicFilter()
    f.assign_topic("low", "ml", 0.1)
    f.assign_topic("high", "ml", 0.9)
    f.assign_topic("mid", "ml", 0.5)
    result = f.top_docs_in_topic("ml")
    assert result == [("high", 0.9), ("mid", 0.5), ("low", 0.1)]


def test_top_docs_in_topic_tiebreak_by_doc_id():
    f = DocTopicFilter()
    f.assign_topic("zeta", "ml", 0.5)
    f.assign_topic("alpha", "ml", 0.5)
    result = f.top_docs_in_topic("ml")
    assert result == [("alpha", 0.5), ("zeta", 0.5)]


def test_top_docs_in_topic_limit():
    f = DocTopicFilter()
    for i in range(5):
        f.assign_topic(f"d{i}", "ml", i / 10)
    result = f.top_docs_in_topic("ml", limit=2)
    assert len(result) == 2
    assert result[0][0] == "d4"
    assert result[1][0] == "d3"


def test_top_docs_in_topic_negative_limit():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.5)
    assert f.top_docs_in_topic("ml", limit=-1) == []


def test_top_docs_in_topic_zero_limit():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml", 0.5)
    assert f.top_docs_in_topic("ml", limit=0) == []


# ---------------------------------------------------------------------------
# topic_co_membership
# ---------------------------------------------------------------------------

def test_topic_co_membership_basic():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    f.assign_topic("d2", "ml")
    f.assign_topic("d3", "ai")
    assert f.topic_co_membership("ml", "ai") == ["d1"]


def test_topic_co_membership_disjoint():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d2", "ai")
    assert f.topic_co_membership("ml", "ai") == []


def test_topic_co_membership_unknown():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    assert f.topic_co_membership("ml", "unknown") == []
    assert f.topic_co_membership("unknown", "ml") == []


def test_topic_co_membership_sorted():
    f = DocTopicFilter()
    for did in ["zeta", "alpha", "mid"]:
        f.assign_topic(did, "ml")
        f.assign_topic(did, "ai")
    assert f.topic_co_membership("ml", "ai") == ["alpha", "mid", "zeta"]


# ---------------------------------------------------------------------------
# topic_distance (Jaccard)
# ---------------------------------------------------------------------------

def test_topic_distance_identical():
    f = DocTopicFilter()
    f.assign_topic("d1", "a")
    f.assign_topic("d1", "b")
    f.assign_topic("d2", "a")
    f.assign_topic("d2", "b")
    assert f.topic_distance("d1", "d2") == 0.0


def test_topic_distance_disjoint():
    f = DocTopicFilter()
    f.assign_topic("d1", "a")
    f.assign_topic("d2", "b")
    assert f.topic_distance("d1", "d2") == 1.0


def test_topic_distance_partial_overlap():
    f = DocTopicFilter()
    f.assign_topic("d1", "a")
    f.assign_topic("d1", "b")
    f.assign_topic("d2", "b")
    f.assign_topic("d2", "c")
    # intersection={b}, union={a,b,c}; jaccard=1/3; distance=2/3
    assert abs(f.topic_distance("d1", "d2") - (2 / 3)) < 1e-9


def test_topic_distance_both_empty():
    f = DocTopicFilter()
    assert f.topic_distance("ghost1", "ghost2") == 0.0


def test_topic_distance_one_empty():
    f = DocTopicFilter()
    f.assign_topic("d1", "a")
    assert f.topic_distance("d1", "ghost") == 1.0


# ---------------------------------------------------------------------------
# clear_doc / clear_topic
# ---------------------------------------------------------------------------

def test_clear_doc_returns_count():
    f = DocTopicFilter()
    f.assign_topic("d1", "a")
    f.assign_topic("d1", "b")
    f.assign_topic("d1", "c")
    assert f.clear_doc("d1") == 3


def test_clear_doc_missing_returns_zero():
    f = DocTopicFilter()
    assert f.clear_doc("ghost") == 0


def test_clear_doc_removes_from_topic_index():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d2", "ml")
    f.clear_doc("d1")
    assert f.docs_in_topic("ml") == ["d2"]


def test_clear_doc_removes_empty_topics():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.clear_doc("d1")
    assert f.all_topics() == []


def test_clear_topic_returns_count():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d2", "ml")
    f.assign_topic("d3", "ml")
    assert f.clear_topic("ml") == 3


def test_clear_topic_missing_returns_zero():
    f = DocTopicFilter()
    assert f.clear_topic("ghost") == 0


def test_clear_topic_removes_assignment_only():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    f.clear_topic("ml")
    assert f.topics_of("d1") == ["ai"]


def test_clear_topic_removes_empty_docs():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.clear_topic("ml")
    assert f.all_doc_ids() == []


# ---------------------------------------------------------------------------
# all_doc_ids / all_topics
# ---------------------------------------------------------------------------

def test_all_doc_ids_empty():
    f = DocTopicFilter()
    assert f.all_doc_ids() == []


def test_all_doc_ids_sorted():
    f = DocTopicFilter()
    f.assign_topic("zeta", "ml")
    f.assign_topic("alpha", "ml")
    f.assign_topic("mid", "ml")
    assert f.all_doc_ids() == ["alpha", "mid", "zeta"]


def test_all_topics_empty():
    f = DocTopicFilter()
    assert f.all_topics() == []


def test_all_topics_sorted():
    f = DocTopicFilter()
    f.assign_topic("d1", "zz")
    f.assign_topic("d1", "aa")
    f.assign_topic("d1", "mm")
    assert f.all_topics() == ["aa", "mm", "zz"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

def test_stats_empty():
    f = DocTopicFilter()
    s = f.stats()
    assert s.total_docs == 0
    assert s.unique_topics == 0
    assert s.total_memberships == 0


def test_stats_after_assignments():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    f.assign_topic("d2", "ml")
    s = f.stats()
    assert s.total_docs == 2
    assert s.unique_topics == 2
    assert s.total_memberships == 3


def test_stats_after_unassign():
    f = DocTopicFilter()
    f.assign_topic("d1", "ml")
    f.assign_topic("d1", "ai")
    f.unassign_topic("d1", "ml")
    s = f.stats()
    assert s.total_docs == 1
    assert s.unique_topics == 1
    assert s.total_memberships == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

def test_thread_safety_concurrent_assign():
    f = DocTopicFilter()

    def worker(start: int, n: int) -> None:
        for i in range(start, start + n):
            f.assign_topic(f"d{i}", f"t{i % 7}", (i % 10) / 10)

    threads = [threading.Thread(target=worker, args=(i * 100, 100)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = f.stats()
    assert s.total_docs == 800
    assert s.total_memberships == 800
    assert s.unique_topics == 7


def test_thread_safety_concurrent_mixed():
    f = DocTopicFilter()
    # Pre-populate
    for i in range(50):
        f.assign_topic(f"d{i}", "ml", 0.5)

    errors: list = []

    def writer() -> None:
        try:
            for i in range(100):
                f.assign_topic(f"w{i}", "ai", 0.3)
        except Exception as e:  # pragma: no cover
            errors.append(e)

    def reader() -> None:
        try:
            for _ in range(100):
                f.docs_in_topic("ml")
                f.all_topics()
                f.stats()
        except Exception as e:  # pragma: no cover
            errors.append(e)

    def remover() -> None:
        try:
            for i in range(50):
                f.unassign_topic(f"d{i}", "ml")
        except Exception as e:  # pragma: no cover
            errors.append(e)

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=reader),
        threading.Thread(target=remover),
        threading.Thread(target=writer),
        threading.Thread(target=reader),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []


def test_thread_safety_concurrent_set_topics():
    f = DocTopicFilter()

    def worker(idx: int) -> None:
        for i in range(50):
            f.set_topics(f"d{idx}", {f"t{i % 3}": (i % 10) / 10})

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Each doc has exactly one topic at the end (last set_topics wins per-thread)
    s = f.stats()
    assert s.total_docs == 10
    # Each doc has exactly one topic (1 membership per doc) since the final
    # set_topics call gave each doc a single-topic dict.
    assert s.total_memberships == 10


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------

def test_integration_full_workflow():
    f = DocTopicFilter()
    f.assign_topic("doc1", "ml", 0.9)
    f.assign_topic("doc1", "ai", 0.7)
    f.assign_topic("doc2", "ml", 0.5)
    f.assign_topic("doc2", "data", 0.8)
    f.assign_topic("doc3", "ai", 0.6)

    assert f.filter_all(["ml", "ai"]) == ["doc1"]
    assert f.filter_any(["data", "ai"]) == ["doc1", "doc2", "doc3"]
    assert f.top_docs_in_topic("ml") == [("doc1", 0.9), ("doc2", 0.5)]
    assert f.topic_co_membership("ml", "data") == ["doc2"]

    f.clear_topic("ai")
    assert f.docs_in_topic("ai") == []
    assert f.weight_of("doc1", "ai") is None
    assert f.weight_of("doc1", "ml") == 0.9
