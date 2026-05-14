"""Tests for E403 ``doc_link_anchor`` module."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_link_anchor import Anchor, AnchorStats, DocLinkAnchor


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestAnchorDataclass:
    def test_required_fields(self):
        a = Anchor(doc_id="d1", anchor_id="a1", position=10)
        assert a.doc_id == "d1"
        assert a.anchor_id == "a1"
        assert a.position == 10

    def test_defaults(self):
        a = Anchor(doc_id="d1", anchor_id="a1", position=5)
        assert a.title == ""
        assert a.created_at == 0.0

    def test_all_fields(self):
        a = Anchor(
            doc_id="d1",
            anchor_id="a1",
            position=42,
            title="Intro",
            created_at=123.5,
        )
        assert a.title == "Intro"
        assert a.created_at == 123.5

    def test_equality(self):
        a = Anchor(doc_id="d", anchor_id="x", position=1)
        b = Anchor(doc_id="d", anchor_id="x", position=1)
        assert a == b

    def test_inequality(self):
        a = Anchor(doc_id="d", anchor_id="x", position=1)
        b = Anchor(doc_id="d", anchor_id="x", position=2)
        assert a != b


class TestAnchorStatsDataclass:
    def test_fields(self):
        s = AnchorStats(total_anchors=3, unique_docs=2, total_uses=5)
        assert s.total_anchors == 3
        assert s.unique_docs == 2
        assert s.total_uses == 5

    def test_equality(self):
        a = AnchorStats(total_anchors=0, unique_docs=0, total_uses=0)
        b = AnchorStats(total_anchors=0, unique_docs=0, total_uses=0)
        assert a == b

    def test_zero(self):
        s = AnchorStats(0, 0, 0)
        assert s.total_anchors == 0
        assert s.unique_docs == 0
        assert s.total_uses == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_store(self):
        store = DocLinkAnchor()
        assert store.all_doc_ids() == []

    def test_initial_stats(self):
        store = DocLinkAnchor()
        s = store.stats()
        assert s.total_anchors == 0
        assert s.unique_docs == 0
        assert s.total_uses == 0

    def test_has_lock(self):
        store = DocLinkAnchor()
        assert hasattr(store, "_lock")

    def test_independent_instances(self):
        s1 = DocLinkAnchor()
        s2 = DocLinkAnchor()
        s1.register("d", "a", 1)
        assert s2.stats().total_anchors == 0


# ---------------------------------------------------------------------------
# register
# ---------------------------------------------------------------------------


class TestRegister:
    def test_returns_anchor(self):
        store = DocLinkAnchor()
        a = store.register("d1", "intro", 0)
        assert isinstance(a, Anchor)

    def test_fields_populated(self):
        store = DocLinkAnchor()
        a = store.register("d1", "intro", 10, title="Intro", now=42.0)
        assert a.doc_id == "d1"
        assert a.anchor_id == "intro"
        assert a.position == 10
        assert a.title == "Intro"
        assert a.created_at == 42.0

    def test_default_title_empty(self):
        store = DocLinkAnchor()
        a = store.register("d1", "x", 1)
        assert a.title == ""

    def test_default_now(self):
        store = DocLinkAnchor()
        before = time.time()
        a = store.register("d1", "x", 1)
        after = time.time()
        assert before <= a.created_at <= after

    def test_new_increments_totals(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        store.register("d2", "a", 0)
        s = store.stats()
        assert s.total_anchors == 3
        assert s.unique_docs == 2

    def test_replace_same_key(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 1, title="old", now=1.0)
        a = store.register("d1", "x", 5, title="new", now=2.0)
        assert a.position == 5
        assert a.title == "new"
        assert store.stats().total_anchors == 1

    def test_replace_preserves_use_count(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 1)
        store.resolve_link("d1", "x")
        store.resolve_link("d1", "x")
        store.register("d1", "x", 7, title="updated")
        assert store.use_count("d1", "x") == 2

    def test_get_after_register(self):
        store = DocLinkAnchor()
        store.register("d1", "intro", 3, title="I")
        a = store.get("d1", "intro")
        assert a is not None
        assert a.title == "I"


# ---------------------------------------------------------------------------
# unregister
# ---------------------------------------------------------------------------


class TestUnregister:
    def test_unregister_existing(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        assert store.unregister("d1", "x") is True

    def test_unregister_missing(self):
        store = DocLinkAnchor()
        assert store.unregister("d1", "x") is False

    def test_removed_from_lookup(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.unregister("d1", "x")
        assert store.get("d1", "x") is None

    def test_removed_from_by_doc(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.unregister("d1", "x")
        assert "d1" not in store.all_doc_ids()

    def test_other_anchor_remains(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.register("d1", "y", 1)
        store.unregister("d1", "x")
        assert store.get("d1", "y") is not None
        assert "d1" in store.all_doc_ids()

    def test_use_count_cleared(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.resolve_link("d1", "x")
        store.unregister("d1", "x")
        assert store.use_count("d1", "x") == 0


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_existing(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 4, title="T")
        a = store.get("d1", "x")
        assert a is not None
        assert a.anchor_id == "x"
        assert a.title == "T"

    def test_get_missing(self):
        store = DocLinkAnchor()
        assert store.get("d1", "x") is None

    def test_get_does_not_increment_use(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.get("d1", "x")
        store.get("d1", "x")
        assert store.use_count("d1", "x") == 0

    def test_get_per_doc(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0, title="A")
        store.register("d2", "x", 0, title="B")
        assert store.get("d1", "x").title == "A"
        assert store.get("d2", "x").title == "B"


# ---------------------------------------------------------------------------
# resolve_link
# ---------------------------------------------------------------------------


class TestResolveLink:
    def test_returns_anchor(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        a = store.resolve_link("d1", "x")
        assert a is not None
        assert a.anchor_id == "x"

    def test_missing_returns_none(self):
        store = DocLinkAnchor()
        assert store.resolve_link("d1", "x") is None

    def test_increments_use_count(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.resolve_link("d1", "x")
        assert store.use_count("d1", "x") == 1

    def test_increments_repeatedly(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        for _ in range(5):
            store.resolve_link("d1", "x")
        assert store.use_count("d1", "x") == 5

    def test_missing_does_not_increment(self):
        store = DocLinkAnchor()
        store.resolve_link("d1", "ghost")
        assert store.use_count("d1", "ghost") == 0

    def test_stats_reflect_uses(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.register("d1", "y", 1)
        store.resolve_link("d1", "x")
        store.resolve_link("d1", "x")
        store.resolve_link("d1", "y")
        assert store.stats().total_uses == 3


# ---------------------------------------------------------------------------
# anchors_for_doc
# ---------------------------------------------------------------------------


class TestAnchorsForDoc:
    def test_empty_doc(self):
        store = DocLinkAnchor()
        assert store.anchors_for_doc("d1") == []

    def test_returns_list(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        assert isinstance(store.anchors_for_doc("d1"), list)

    def test_sorted_by_position(self):
        store = DocLinkAnchor()
        store.register("d1", "c", 30)
        store.register("d1", "a", 10)
        store.register("d1", "b", 20)
        anchors = store.anchors_for_doc("d1")
        assert [a.anchor_id for a in anchors] == ["a", "b", "c"]

    def test_only_for_given_doc(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.register("d2", "y", 0)
        anchors = store.anchors_for_doc("d1")
        assert len(anchors) == 1
        assert anchors[0].doc_id == "d1"

    def test_multiple_anchors(self):
        store = DocLinkAnchor()
        for i in range(5):
            store.register("d1", f"a{i}", i)
        assert len(store.anchors_for_doc("d1")) == 5


# ---------------------------------------------------------------------------
# anchor_at_position
# ---------------------------------------------------------------------------


class TestAnchorAtPosition:
    def test_exact_match(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 42)
        a = store.anchor_at_position("d1", 42)
        assert a is not None
        assert a.anchor_id == "x"

    def test_no_match(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 42)
        assert store.anchor_at_position("d1", 41) is None

    def test_empty_doc(self):
        store = DocLinkAnchor()
        assert store.anchor_at_position("missing", 0) is None

    def test_wrong_doc(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 5)
        assert store.anchor_at_position("d2", 5) is None


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_returns_count(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        store.register("d1", "c", 2)
        assert store.clear_doc("d1") == 3

    def test_missing_returns_zero(self):
        store = DocLinkAnchor()
        assert store.clear_doc("none") == 0

    def test_removes_anchors(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.clear_doc("d1")
        assert store.get("d1", "a") is None

    def test_does_not_affect_other_docs(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d2", "b", 0)
        store.clear_doc("d1")
        assert store.get("d2", "b") is not None

    def test_clears_use_counts(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.resolve_link("d1", "a")
        store.clear_doc("d1")
        assert store.use_count("d1", "a") == 0


# ---------------------------------------------------------------------------
# use_count
# ---------------------------------------------------------------------------


class TestUseCount:
    def test_zero_initially(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        assert store.use_count("d1", "x") == 0

    def test_missing_anchor_zero(self):
        store = DocLinkAnchor()
        assert store.use_count("d1", "missing") == 0

    def test_incremented_by_resolve(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.resolve_link("d1", "x")
        store.resolve_link("d1", "x")
        store.resolve_link("d1", "x")
        assert store.use_count("d1", "x") == 3


# ---------------------------------------------------------------------------
# most_used
# ---------------------------------------------------------------------------


class TestMostUsed:
    def test_empty(self):
        store = DocLinkAnchor()
        assert store.most_used() == []

    def test_sorted_desc(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        store.register("d1", "c", 2)
        for _ in range(3):
            store.resolve_link("d1", "a")
        for _ in range(5):
            store.resolve_link("d1", "b")
        store.resolve_link("d1", "c")
        result = store.most_used()
        counts = [c for _, c in result]
        assert counts == sorted(counts, reverse=True)
        assert result[0][0] == ("d1", "b")
        assert result[0][1] == 5

    def test_limit(self):
        store = DocLinkAnchor()
        for i in range(5):
            store.register("d1", f"a{i}", i)
            for _ in range(i + 1):
                store.resolve_link("d1", f"a{i}")
        assert len(store.most_used(limit=3)) == 3

    def test_skips_unused(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        store.resolve_link("d1", "a")
        result = store.most_used()
        assert len(result) == 1
        assert result[0][0] == ("d1", "a")

    def test_returns_tuples(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        store.resolve_link("d1", "x")
        result = store.most_used()
        assert isinstance(result[0], tuple)
        assert isinstance(result[0][0], tuple)
        assert result[0][0] == ("d1", "x")


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self):
        store = DocLinkAnchor()
        assert store.all_doc_ids() == []

    def test_sorted(self):
        store = DocLinkAnchor()
        store.register("c", "a", 0)
        store.register("a", "a", 0)
        store.register("b", "a", 0)
        assert store.all_doc_ids() == ["a", "b", "c"]

    def test_unique(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        assert store.all_doc_ids() == ["d1"]

    def test_drops_emptied_doc(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.unregister("d1", "a")
        assert store.all_doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_returns_stats_instance(self):
        store = DocLinkAnchor()
        assert isinstance(store.stats(), AnchorStats)

    def test_totals(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        store.register("d2", "a", 0)
        s = store.stats()
        assert s.total_anchors == 3
        assert s.unique_docs == 2

    def test_uses_count(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.resolve_link("d1", "a")
        store.resolve_link("d1", "a")
        assert store.stats().total_uses == 2

    def test_after_unregister(self):
        store = DocLinkAnchor()
        store.register("d1", "a", 0)
        store.register("d1", "b", 1)
        store.unregister("d1", "a")
        s = store.stats()
        assert s.total_anchors == 1
        assert s.unique_docs == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_register(self):
        store = DocLinkAnchor()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                store.register(f"d{tid}", f"a{i}", i)

        threads = [
            threading.Thread(target=worker, args=(t,))
            for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert store.stats().total_anchors == n_threads * per_thread
        assert store.stats().unique_docs == n_threads

    def test_concurrent_resolve(self):
        store = DocLinkAnchor()
        store.register("d1", "x", 0)
        n_threads = 8
        per_thread = 100

        def worker() -> None:
            for _ in range(per_thread):
                store.resolve_link("d1", "x")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert store.use_count("d1", "x") == n_threads * per_thread

    def test_concurrent_register_same_doc(self):
        store = DocLinkAnchor()

        def worker(start: int) -> None:
            for i in range(20):
                store.register("shared", f"a{start * 100 + i}", i)

        threads = [threading.Thread(target=worker, args=(s,)) for s in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert store.stats().total_anchors == 6 * 20
        assert store.all_doc_ids() == ["shared"]


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
