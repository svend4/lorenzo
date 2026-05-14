"""Tests for E392 DocTopicIndex module.

Run with:
    cd /home/user/lorenzo/docs-toolkit
    python -m pytest tests/test_doc_topic_index.py -q
"""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_topic_index import (
    DocTopicIndex,
    Topic,
    TopicAssignment,
    TopicIndexStats,
)


# ---------------------------------------------------------------------------
# TestTopicDataclass
# ---------------------------------------------------------------------------

class TestTopicDataclass:
    def test_required_fields(self):
        t = Topic(topic_id="t1", name="Machine Learning")
        assert t.topic_id == "t1"
        assert t.name == "Machine Learning"

    def test_default_description_empty(self):
        t = Topic(topic_id="t1", name="ML")
        assert t.description == ""

    def test_default_parent_is_none(self):
        t = Topic(topic_id="t1", name="ML")
        assert t.parent_topic is None

    def test_explicit_fields(self):
        t = Topic(topic_id="t1", name="N", description="d", parent_topic="root")
        assert t.description == "d"
        assert t.parent_topic == "root"

    def test_equality(self):
        a = Topic(topic_id="t1", name="N", description="d", parent_topic="p")
        b = Topic(topic_id="t1", name="N", description="d", parent_topic="p")
        assert a == b


# ---------------------------------------------------------------------------
# TestTopicAssignmentDataclass
# ---------------------------------------------------------------------------

class TestTopicAssignmentDataclass:
    def test_required_fields(self):
        a = TopicAssignment(doc_id="d1", topic_id="t1")
        assert a.doc_id == "d1"
        assert a.topic_id == "t1"

    def test_default_relevance_is_one(self):
        a = TopicAssignment(doc_id="d1", topic_id="t1")
        assert a.relevance == 1.0

    def test_default_assigned_at_is_zero(self):
        a = TopicAssignment(doc_id="d1", topic_id="t1")
        assert a.assigned_at == 0.0

    def test_explicit_fields(self):
        a = TopicAssignment(doc_id="d1", topic_id="t1", relevance=0.5, assigned_at=10.0)
        assert a.relevance == 0.5
        assert a.assigned_at == 10.0


# ---------------------------------------------------------------------------
# TestTopicIndexStatsDataclass
# ---------------------------------------------------------------------------

class TestTopicIndexStatsDataclass:
    def test_required_fields(self):
        s = TopicIndexStats(
            total_topics=1, total_assignments=2, unique_docs=3, root_topic_count=1
        )
        assert s.total_topics == 1
        assert s.total_assignments == 2
        assert s.unique_docs == 3
        assert s.root_topic_count == 1

    def test_equality(self):
        a = TopicIndexStats(1, 2, 3, 4)
        b = TopicIndexStats(1, 2, 3, 4)
        assert a == b


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_construct_empty(self):
        idx = DocTopicIndex()
        assert idx.list_topics() == []
        assert idx.root_topics() == []

    def test_initial_stats_zero(self):
        idx = DocTopicIndex()
        s = idx.stats()
        assert s.total_topics == 0
        assert s.total_assignments == 0
        assert s.unique_docs == 0
        assert s.root_topic_count == 0

    def test_independent_instances(self):
        a = DocTopicIndex()
        b = DocTopicIndex()
        a.define_topic(Topic(topic_id="t1", name="X"))
        assert b.list_topics() == []


# ---------------------------------------------------------------------------
# TestDefineTopic
# ---------------------------------------------------------------------------

class TestDefineTopic:
    def test_define_single_topic(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="ML"))
        assert idx.get_topic("t1").name == "ML"

    def test_define_with_parent(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="root", name="Root"))
        idx.define_topic(Topic(topic_id="t1", name="Child", parent_topic="root"))
        kids = idx.child_topics("root")
        assert [k.topic_id for k in kids] == ["t1"]

    def test_replace_existing_topic(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="Old"))
        idx.define_topic(Topic(topic_id="t1", name="New"))
        assert idx.get_topic("t1").name == "New"
        assert len(idx.list_topics()) == 1

    def test_replace_reassigns_parent(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="a", name="A"))
        idx.define_topic(Topic(topic_id="b", name="B"))
        idx.define_topic(Topic(topic_id="t1", name="T", parent_topic="a"))
        # change parent from a → b
        idx.define_topic(Topic(topic_id="t1", name="T", parent_topic="b"))
        assert [c.topic_id for c in idx.child_topics("a")] == []
        assert [c.topic_id for c in idx.child_topics("b")] == ["t1"]

    def test_replace_clears_parent(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="a", name="A"))
        idx.define_topic(Topic(topic_id="t1", name="T", parent_topic="a"))
        idx.define_topic(Topic(topic_id="t1", name="T"))
        assert [c.topic_id for c in idx.child_topics("a")] == []

    def test_stats_after_define(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.define_topic(Topic(topic_id="t2", name="B"))
        assert idx.stats().total_topics == 2


# ---------------------------------------------------------------------------
# TestUndefineTopic
# ---------------------------------------------------------------------------

class TestUndefineTopic:
    def test_undefine_unknown_returns_false(self):
        idx = DocTopicIndex()
        assert idx.undefine_topic("nope") is False

    def test_undefine_existing_returns_true(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        assert idx.undefine_topic("t1") is True
        assert idx.get_topic("t1") is None

    def test_undefine_removes_assignments(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1")
        idx.undefine_topic("t1")
        assert idx.topics_for_doc("d1") == []
        assert idx.docs_for_topic("t1") == []

    def test_undefine_orphans_children(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="root", name="R"))
        idx.define_topic(Topic(topic_id="c1", name="C1", parent_topic="root"))
        idx.define_topic(Topic(topic_id="c2", name="C2", parent_topic="root"))
        idx.undefine_topic("root")
        # Children should still exist with parent_topic = None
        c1 = idx.get_topic("c1")
        c2 = idx.get_topic("c2")
        assert c1 is not None and c1.parent_topic is None
        assert c2 is not None and c2.parent_topic is None

    def test_undefine_detaches_from_parent_sibling_list(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="root", name="R"))
        idx.define_topic(Topic(topic_id="c1", name="C1", parent_topic="root"))
        idx.define_topic(Topic(topic_id="c2", name="C2", parent_topic="root"))
        idx.undefine_topic("c1")
        kids = [k.topic_id for k in idx.child_topics("root")]
        assert kids == ["c2"]

    def test_undefine_updates_stats(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.define_topic(Topic(topic_id="t2", name="B"))
        idx.assign_topic("d1", "t1")
        idx.undefine_topic("t1")
        s = idx.stats()
        assert s.total_topics == 1
        assert s.total_assignments == 0


# ---------------------------------------------------------------------------
# TestGetTopic
# ---------------------------------------------------------------------------

class TestGetTopic:
    def test_get_unknown_returns_none(self):
        idx = DocTopicIndex()
        assert idx.get_topic("nope") is None

    def test_get_existing(self):
        idx = DocTopicIndex()
        t = Topic(topic_id="t1", name="ML", description="desc")
        idx.define_topic(t)
        got = idx.get_topic("t1")
        assert got is not None
        assert got.name == "ML"
        assert got.description == "desc"


# ---------------------------------------------------------------------------
# TestListTopics
# ---------------------------------------------------------------------------

class TestListTopics:
    def test_empty(self):
        idx = DocTopicIndex()
        assert idx.list_topics() == []

    def test_sorted_by_topic_id(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="z", name="Zeta"))
        idx.define_topic(Topic(topic_id="a", name="Alpha"))
        idx.define_topic(Topic(topic_id="m", name="Mu"))
        ids = [t.topic_id for t in idx.list_topics()]
        assert ids == ["a", "m", "z"]


# ---------------------------------------------------------------------------
# TestRootTopics
# ---------------------------------------------------------------------------

class TestRootTopics:
    def test_empty(self):
        idx = DocTopicIndex()
        assert idx.root_topics() == []

    def test_only_roots_returned(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="root1", name="B"))
        idx.define_topic(Topic(topic_id="root2", name="A"))
        idx.define_topic(Topic(topic_id="c1", name="C", parent_topic="root1"))
        roots = idx.root_topics()
        # sorted by name → A, B
        assert [r.topic_id for r in roots] == ["root2", "root1"]

    def test_after_orphaning(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c", name="C", parent_topic="r"))
        idx.undefine_topic("r")
        roots = idx.root_topics()
        assert [t.topic_id for t in roots] == ["c"]


# ---------------------------------------------------------------------------
# TestChildTopics
# ---------------------------------------------------------------------------

class TestChildTopics:
    def test_unknown_parent_returns_empty(self):
        idx = DocTopicIndex()
        assert idx.child_topics("nope") == []

    def test_no_children(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        assert idx.child_topics("r") == []

    def test_direct_children_sorted_by_name(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c1", name="Zeta", parent_topic="r"))
        idx.define_topic(Topic(topic_id="c2", name="Alpha", parent_topic="r"))
        idx.define_topic(Topic(topic_id="c3", name="Mu", parent_topic="r"))
        # grandchild — should not appear in direct
        idx.define_topic(Topic(topic_id="g", name="G", parent_topic="c1"))
        kids = idx.child_topics("r")
        assert [k.name for k in kids] == ["Alpha", "Mu", "Zeta"]


# ---------------------------------------------------------------------------
# TestDescendantTopics
# ---------------------------------------------------------------------------

class TestDescendantTopics:
    def test_unknown_returns_empty(self):
        idx = DocTopicIndex()
        assert idx.descendant_topics("nope") == []

    def test_no_descendants(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        assert idx.descendant_topics("r") == []

    def test_bfs_order(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="b", name="B", parent_topic="r"))
        idx.define_topic(Topic(topic_id="a", name="A", parent_topic="r"))
        idx.define_topic(Topic(topic_id="ab", name="AB", parent_topic="a"))
        idx.define_topic(Topic(topic_id="aa", name="AA", parent_topic="a"))
        descendants = idx.descendant_topics("r")
        ids = [t.topic_id for t in descendants]
        # Level 1 sorted by topic_id: a, b ; Level 2: aa, ab
        assert ids == ["a", "b", "aa", "ab"]

    def test_deep_chain(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c1", name="C1", parent_topic="r"))
        idx.define_topic(Topic(topic_id="c2", name="C2", parent_topic="c1"))
        idx.define_topic(Topic(topic_id="c3", name="C3", parent_topic="c2"))
        ids = [t.topic_id for t in idx.descendant_topics("r")]
        assert ids == ["c1", "c2", "c3"]


# ---------------------------------------------------------------------------
# TestAssignTopic
# ---------------------------------------------------------------------------

class TestAssignTopic:
    def test_assign_undefined_returns_none(self):
        idx = DocTopicIndex()
        assert idx.assign_topic("d1", "t1") is None

    def test_assign_returns_assignment(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        a = idx.assign_topic("d1", "t1", relevance=0.5, now=42.0)
        assert isinstance(a, TopicAssignment)
        assert a.doc_id == "d1"
        assert a.topic_id == "t1"
        assert a.relevance == 0.5
        assert a.assigned_at == 42.0

    def test_assign_clamps_above_one(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        a = idx.assign_topic("d1", "t1", relevance=5.0)
        assert a.relevance == 1.0

    def test_assign_clamps_below_zero(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        a = idx.assign_topic("d1", "t1", relevance=-0.5)
        assert a.relevance == 0.0

    def test_assign_overwrites_previous(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1", relevance=0.5)
        idx.assign_topic("d1", "t1", relevance=0.9)
        assignments = idx.topics_for_doc("d1")
        assert len(assignments) == 1
        assert assignments[0].relevance == 0.9

    def test_assign_uses_time_when_now_none(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        a = idx.assign_topic("d1", "t1")
        assert a.assigned_at > 0.0

    def test_assign_stats_update(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1")
        idx.assign_topic("d2", "t1")
        s = idx.stats()
        assert s.total_assignments == 2
        assert s.unique_docs == 2


# ---------------------------------------------------------------------------
# TestUnassignTopic
# ---------------------------------------------------------------------------

class TestUnassignTopic:
    def test_unassign_unknown_returns_false(self):
        idx = DocTopicIndex()
        assert idx.unassign_topic("d1", "t1") is False

    def test_unassign_existing(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1")
        assert idx.unassign_topic("d1", "t1") is True
        assert idx.topics_for_doc("d1") == []

    def test_unassign_removes_from_docs_index(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1")
        idx.unassign_topic("d1", "t1")
        assert idx.docs_for_topic("t1") == []

    def test_unassign_twice_second_false(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1")
        idx.unassign_topic("d1", "t1")
        assert idx.unassign_topic("d1", "t1") is False


# ---------------------------------------------------------------------------
# TestTopicsForDoc
# ---------------------------------------------------------------------------

class TestTopicsForDoc:
    def test_unknown_doc_empty(self):
        idx = DocTopicIndex()
        assert idx.topics_for_doc("nope") == []

    def test_sorted_by_relevance_desc(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.define_topic(Topic(topic_id="t2", name="B"))
        idx.define_topic(Topic(topic_id="t3", name="C"))
        idx.assign_topic("d1", "t1", relevance=0.3)
        idx.assign_topic("d1", "t2", relevance=0.9)
        idx.assign_topic("d1", "t3", relevance=0.6)
        ids = [a.topic_id for a in idx.topics_for_doc("d1")]
        assert ids == ["t2", "t3", "t1"]

    def test_tie_break_by_topic_id_asc(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="b", name="B"))
        idx.define_topic(Topic(topic_id="a", name="A"))
        idx.assign_topic("d1", "b", relevance=0.5)
        idx.assign_topic("d1", "a", relevance=0.5)
        ids = [a.topic_id for a in idx.topics_for_doc("d1")]
        assert ids == ["a", "b"]


# ---------------------------------------------------------------------------
# TestDocsForTopic
# ---------------------------------------------------------------------------

class TestDocsForTopic:
    def test_unknown_topic_empty(self):
        idx = DocTopicIndex()
        assert idx.docs_for_topic("nope") == []

    def test_sorted_doc_ids(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d3", "t1")
        idx.assign_topic("d1", "t1")
        idx.assign_topic("d2", "t1")
        assert idx.docs_for_topic("t1") == ["d1", "d2", "d3"]

    def test_min_relevance_filter(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1", relevance=0.2)
        idx.assign_topic("d2", "t1", relevance=0.8)
        idx.assign_topic("d3", "t1", relevance=0.5)
        result = idx.docs_for_topic("t1", min_relevance=0.5)
        assert result == ["d2", "d3"]

    def test_include_descendants(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="root", name="R"))
        idx.define_topic(Topic(topic_id="c1", name="C1", parent_topic="root"))
        idx.define_topic(Topic(topic_id="c2", name="C2", parent_topic="root"))
        idx.assign_topic("d_root", "root")
        idx.assign_topic("d_c1", "c1")
        idx.assign_topic("d_c2", "c2")
        # without descendants
        assert idx.docs_for_topic("root") == ["d_root"]
        # with descendants
        assert idx.docs_for_topic("root", include_descendants=True) == [
            "d_c1",
            "d_c2",
            "d_root",
        ]

    def test_include_descendants_deep(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c", name="C", parent_topic="r"))
        idx.define_topic(Topic(topic_id="gc", name="GC", parent_topic="c"))
        idx.assign_topic("d1", "gc")
        result = idx.docs_for_topic("r", include_descendants=True)
        assert result == ["d1"]

    def test_dedup_when_doc_in_multiple_descendants(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c1", name="C1", parent_topic="r"))
        idx.define_topic(Topic(topic_id="c2", name="C2", parent_topic="r"))
        idx.assign_topic("d1", "c1")
        idx.assign_topic("d1", "c2")
        result = idx.docs_for_topic("r", include_descendants=True)
        assert result == ["d1"]


# ---------------------------------------------------------------------------
# TestTopTopics
# ---------------------------------------------------------------------------

class TestTopTopics:
    def test_empty(self):
        idx = DocTopicIndex()
        assert idx.top_topics() == []

    def test_sorted_desc_by_count(self):
        idx = DocTopicIndex()
        for tid in ["a", "b", "c"]:
            idx.define_topic(Topic(topic_id=tid, name=tid))
        idx.assign_topic("d1", "a")
        idx.assign_topic("d2", "a")
        idx.assign_topic("d3", "a")
        idx.assign_topic("d1", "b")
        idx.assign_topic("d2", "b")
        idx.assign_topic("d1", "c")
        result = idx.top_topics()
        assert result == [("a", 3), ("b", 2), ("c", 1)]

    def test_tie_break_by_topic_id(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="b", name="B"))
        idx.define_topic(Topic(topic_id="a", name="A"))
        idx.assign_topic("d1", "a")
        idx.assign_topic("d1", "b")
        result = idx.top_topics()
        assert result == [("a", 1), ("b", 1)]

    def test_limit_applied(self):
        idx = DocTopicIndex()
        for tid in ["a", "b", "c"]:
            idx.define_topic(Topic(topic_id=tid, name=tid))
            idx.assign_topic("d1", tid)
        result = idx.top_topics(limit=2)
        assert len(result) == 2

    def test_excludes_topics_with_zero_docs(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.define_topic(Topic(topic_id="t2", name="B"))
        idx.assign_topic("d1", "t1")
        result = idx.top_topics()
        assert result == [("t1", 1)]


# ---------------------------------------------------------------------------
# TestClearDoc
# ---------------------------------------------------------------------------

class TestClearDoc:
    def test_clear_unknown_returns_zero(self):
        idx = DocTopicIndex()
        assert idx.clear_doc("nope") == 0

    def test_clear_returns_count(self):
        idx = DocTopicIndex()
        for tid in ["t1", "t2", "t3"]:
            idx.define_topic(Topic(topic_id=tid, name=tid))
            idx.assign_topic("d1", tid)
        n = idx.clear_doc("d1")
        assert n == 3

    def test_clear_removes_all_assignments(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.define_topic(Topic(topic_id="t2", name="B"))
        idx.assign_topic("d1", "t1")
        idx.assign_topic("d1", "t2")
        idx.clear_doc("d1")
        assert idx.topics_for_doc("d1") == []
        assert idx.docs_for_topic("t1") == []
        assert idx.docs_for_topic("t2") == []

    def test_clear_does_not_remove_other_docs(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))
        idx.assign_topic("d1", "t1")
        idx.assign_topic("d2", "t1")
        idx.clear_doc("d1")
        assert idx.docs_for_topic("t1") == ["d2"]


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        idx = DocTopicIndex()
        s = idx.stats()
        assert s == TopicIndexStats(0, 0, 0, 0)

    def test_with_topics_and_assignments(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c", name="C", parent_topic="r"))
        idx.assign_topic("d1", "r")
        idx.assign_topic("d2", "c")
        idx.assign_topic("d1", "c")
        s = idx.stats()
        assert s.total_topics == 2
        assert s.total_assignments == 3
        assert s.unique_docs == 2
        assert s.root_topic_count == 1

    def test_root_count_after_orphan(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="r", name="R"))
        idx.define_topic(Topic(topic_id="c", name="C", parent_topic="r"))
        idx.undefine_topic("r")
        s = idx.stats()
        assert s.total_topics == 1
        assert s.root_topic_count == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_assign_topic(self):
        idx = DocTopicIndex()
        idx.define_topic(Topic(topic_id="t1", name="A"))

        N = 50
        T = 8

        def worker(start: int):
            for i in range(N):
                idx.assign_topic(f"doc_{start}_{i}", "t1", relevance=0.5)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        result = idx.docs_for_topic("t1")
        assert len(result) == N * T

    def test_concurrent_define_and_assign(self):
        idx = DocTopicIndex()

        def define_worker():
            for i in range(30):
                idx.define_topic(Topic(topic_id=f"t{i}", name=f"T{i}"))

        def assign_worker():
            for i in range(30):
                idx.assign_topic(f"d{i}", f"t{i}")

        ts = [
            threading.Thread(target=define_worker),
            threading.Thread(target=assign_worker),
            threading.Thread(target=define_worker),
        ]
        for t in ts:
            t.start()
        for t in ts:
            t.join()

        # At least all 30 topics should be defined
        assert idx.stats().total_topics == 30
