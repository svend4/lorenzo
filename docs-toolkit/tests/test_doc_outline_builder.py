"""Tests for E394 DocOutlineBuilder."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_outline_builder import (
    DocOutlineBuilder,
    OutlineNode,
    OutlineStats,
)


# ---------------------------------------------------------------------- node
class TestOutlineNodeDataclass:
    def test_construct_basic(self):
        n = OutlineNode(doc_id="d", heading="H", level=1, position=1)
        assert n.doc_id == "d"
        assert n.heading == "H"
        assert n.level == 1
        assert n.position == 1
        assert n.children == []

    def test_children_default_empty(self):
        n = OutlineNode(doc_id="d", heading="H", level=2, position=10)
        assert n.children == []

    def test_children_independent_per_instance(self):
        a = OutlineNode(doc_id="d", heading="A", level=1, position=1)
        b = OutlineNode(doc_id="d", heading="B", level=1, position=2)
        a.children.append(
            OutlineNode(doc_id="d", heading="C", level=2, position=3)
        )
        assert b.children == []

    def test_equality(self):
        a = OutlineNode(doc_id="d", heading="H", level=1, position=1)
        b = OutlineNode(doc_id="d", heading="H", level=1, position=1)
        assert a == b

    def test_children_appendable(self):
        a = OutlineNode(doc_id="d", heading="A", level=1, position=1)
        c = OutlineNode(doc_id="d", heading="B", level=2, position=2)
        a.children.append(c)
        assert a.children == [c]


# ----------------------------------------------------------------- stats DC
class TestOutlineStatsDataclass:
    def test_construct(self):
        s = OutlineStats(total_docs=2, total_nodes=5, max_depth=3)
        assert s.total_docs == 2
        assert s.total_nodes == 5
        assert s.max_depth == 3

    def test_equality(self):
        a = OutlineStats(total_docs=1, total_nodes=1, max_depth=1)
        b = OutlineStats(total_docs=1, total_nodes=1, max_depth=1)
        assert a == b

    def test_inequality(self):
        a = OutlineStats(total_docs=1, total_nodes=1, max_depth=1)
        b = OutlineStats(total_docs=2, total_nodes=1, max_depth=1)
        assert a != b


# --------------------------------------------------------------- construction
class TestConstruction:
    def test_empty_builder(self):
        b = DocOutlineBuilder()
        assert b.all_doc_ids() == []
        assert b.stats() == OutlineStats(
            total_docs=0, total_nodes=0, max_depth=0
        )

    def test_independent_state(self):
        b1 = DocOutlineBuilder()
        b2 = DocOutlineBuilder()
        b1.add_heading("d", "x", 1, 1)
        assert b2.all_doc_ids() == []

    def test_initial_outline_empty(self):
        b = DocOutlineBuilder()
        assert b.get_outline("missing") == []

    def test_initial_flat_empty(self):
        b = DocOutlineBuilder()
        assert b.flat_outline("missing") == []


# ---------------------------------------------------------------- add_heading
class TestAddHeading:
    def test_add_returns_node(self):
        b = DocOutlineBuilder()
        n = b.add_heading("d", "Intro", 1, 1)
        assert isinstance(n, OutlineNode)
        assert n.heading == "Intro"
        assert n.level == 1
        assert n.position == 1

    def test_add_multiple(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "B", 2, 2)
        assert b.node_count("d") == 2

    def test_invalid_level_zero(self):
        b = DocOutlineBuilder()
        with pytest.raises(ValueError):
            b.add_heading("d", "A", 0, 1)

    def test_invalid_level_seven(self):
        b = DocOutlineBuilder()
        with pytest.raises(ValueError):
            b.add_heading("d", "A", 7, 1)

    def test_invalid_level_negative(self):
        b = DocOutlineBuilder()
        with pytest.raises(ValueError):
            b.add_heading("d", "A", -1, 1)

    def test_invalid_level_non_int(self):
        b = DocOutlineBuilder()
        with pytest.raises(ValueError):
            b.add_heading("d", "A", "1", 1)  # type: ignore[arg-type]

    def test_levels_1_through_6(self):
        b = DocOutlineBuilder()
        for lvl in range(1, 7):
            b.add_heading("d", f"L{lvl}", lvl, lvl)
        assert b.node_count("d") == 6

    def test_separate_docs(self):
        b = DocOutlineBuilder()
        b.add_heading("a", "A", 1, 1)
        b.add_heading("b", "B", 1, 1)
        assert sorted(b.all_doc_ids()) == ["a", "b"]


# -------------------------------------------------------------- build_outline
class TestBuildOutline:
    def test_single_root(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "Top", 1, 1)
        roots = b.build_outline("d")
        assert len(roots) == 1
        assert roots[0].heading == "Top"

    def test_simple_parent_child(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.1", 2, 2)
        roots = b.build_outline("d")
        assert len(roots) == 1
        assert len(roots[0].children) == 1
        assert roots[0].children[0].heading == "A.1"

    def test_deep_nesting(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "L1", 1, 1)
        b.add_heading("d", "L2", 2, 2)
        b.add_heading("d", "L3", 3, 3)
        b.add_heading("d", "L4", 4, 4)
        roots = b.build_outline("d")
        cur = roots[0]
        for expected in ["L2", "L3", "L4"]:
            assert len(cur.children) == 1
            cur = cur.children[0]
            assert cur.heading == expected

    def test_siblings(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.1", 2, 2)
        b.add_heading("d", "A.2", 2, 3)
        roots = b.build_outline("d")
        assert len(roots[0].children) == 2

    def test_multiple_roots(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "B", 1, 2)
        roots = b.build_outline("d")
        assert [r.heading for r in roots] == ["A", "B"]

    def test_returning_to_higher_level(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.1", 2, 2)
        b.add_heading("d", "A.1.1", 3, 3)
        b.add_heading("d", "A.2", 2, 4)
        roots = b.build_outline("d")
        a = roots[0]
        assert [c.heading for c in a.children] == ["A.1", "A.2"]
        assert [c.heading for c in a.children[0].children] == ["A.1.1"]

    def test_skipped_levels(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.x.x", 3, 2)
        roots = b.build_outline("d")
        assert roots[0].children[0].heading == "A.x.x"

    def test_topmost_level_not_one(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "Only", 3, 1)
        roots = b.build_outline("d")
        assert len(roots) == 1
        assert roots[0].level == 3

    def test_empty_doc(self):
        b = DocOutlineBuilder()
        assert b.build_outline("missing") == []

    def test_cached(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        first = b.build_outline("d")
        second = b.get_outline("d")
        assert first is second


# ------------------------------------------------------------ parse_markdown
class TestParseMarkdown:
    def test_single_heading(self):
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", "# Hello")
        assert len(roots) == 1
        assert roots[0].heading == "Hello"
        assert roots[0].level == 1

    def test_multiple_levels(self):
        text = "# A\n## A.1\n### A.1.1\n## A.2\n# B\n"
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", text)
        assert [r.heading for r in roots] == ["A", "B"]
        a = roots[0]
        assert [c.heading for c in a.children] == ["A.1", "A.2"]
        assert [c.heading for c in a.children[0].children] == ["A.1.1"]

    def test_line_numbers_as_position(self):
        text = "intro\n# A\nbody\n## B\n"
        b = DocOutlineBuilder()
        b.parse_markdown("d", text)
        flat = b.flat_outline("d")
        assert flat[0].position == 2
        assert flat[1].position == 4

    def test_replaces_existing(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "Old", 1, 1)
        b.parse_markdown("d", "# New")
        flat = b.flat_outline("d")
        assert len(flat) == 1
        assert flat[0].heading == "New"

    def test_empty_content(self):
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", "")
        assert roots == []
        assert b.node_count("d") == 0

    def test_no_headings(self):
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", "just text\nmore text")
        assert roots == []

    def test_level_six(self):
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", "###### Deep")
        assert roots[0].level == 6

    def test_seven_hashes_ignored(self):
        # 7+ hashes are not valid markdown headings → not parsed.
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", "####### Too deep")
        assert roots == []

    def test_trailing_hashes_stripped(self):
        b = DocOutlineBuilder()
        roots = b.parse_markdown("d", "# Title #")
        assert roots[0].heading == "Title"


# ----------------------------------------------------------------- get_outline
class TestGetOutline:
    def test_returns_cached(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        first = b.build_outline("d")
        second = b.get_outline("d")
        assert first is second

    def test_builds_when_missing(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        roots = b.get_outline("d")
        assert len(roots) == 1

    def test_empty_doc(self):
        b = DocOutlineBuilder()
        assert b.get_outline("missing") == []

    def test_add_invalidates_cache(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.build_outline("d")
        b.add_heading("d", "B", 1, 2)
        roots = b.get_outline("d")
        assert len(roots) == 2


# --------------------------------------------------------------- flat_outline
class TestFlatOutline:
    def test_sorted_by_position(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "C", 1, 3)
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "B", 1, 2)
        flat = b.flat_outline("d")
        assert [n.heading for n in flat] == ["A", "B", "C"]

    def test_empty(self):
        assert DocOutlineBuilder().flat_outline("x") == []

    def test_returns_list_copy_ok(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        flat = b.flat_outline("d")
        flat.append("garbage")  # type: ignore[arg-type]
        # internal state should not be polluted
        assert b.node_count("d") == 1


# ----------------------------------------------------------- headings_at_level
class TestHeadingsAtLevel:
    def test_filter_level_one(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.1", 2, 2)
        b.add_heading("d", "B", 1, 3)
        out = b.headings_at_level("d", 1)
        assert [n.heading for n in out] == ["A", "B"]

    def test_filter_level_two(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.1", 2, 2)
        out = b.headings_at_level("d", 2)
        assert [n.heading for n in out] == ["A.1"]

    def test_filter_none(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        assert b.headings_at_level("d", 4) == []

    def test_sorted_by_position(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "B", 1, 10)
        b.add_heading("d", "A", 1, 1)
        out = b.headings_at_level("d", 1)
        assert [n.heading for n in out] == ["A", "B"]


# ----------------------------------------------------------------------- depth
class TestDepth:
    def test_no_doc(self):
        assert DocOutlineBuilder().depth("missing") == 0

    def test_single_level(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        assert b.depth("d") == 1

    def test_max_level(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "B", 3, 2)
        b.add_heading("d", "C", 2, 3)
        assert b.depth("d") == 3


# ------------------------------------------------------------------ node_count
class TestNodeCount:
    def test_zero(self):
        assert DocOutlineBuilder().node_count("x") == 0

    def test_counts(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "B", 1, 2)
        b.add_heading("d", "C", 1, 3)
        assert b.node_count("d") == 3

    def test_per_doc(self):
        b = DocOutlineBuilder()
        b.add_heading("a", "A", 1, 1)
        b.add_heading("b", "B", 1, 1)
        b.add_heading("b", "B2", 1, 2)
        assert b.node_count("a") == 1
        assert b.node_count("b") == 2


# ------------------------------------------------------------------ clear_doc
class TestClearDoc:
    def test_clear_existing(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        assert b.clear_doc("d") is True
        assert b.node_count("d") == 0

    def test_clear_missing(self):
        b = DocOutlineBuilder()
        assert b.clear_doc("missing") is False

    def test_clear_removes_from_all_doc_ids(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.clear_doc("d")
        assert "d" not in b.all_doc_ids()

    def test_clear_clears_tree_cache(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.build_outline("d")
        b.clear_doc("d")
        assert b.get_outline("d") == []


# ---------------------------------------------------------------- all_doc_ids
class TestAllDocIds:
    def test_empty(self):
        assert DocOutlineBuilder().all_doc_ids() == []

    def test_sorted(self):
        b = DocOutlineBuilder()
        b.add_heading("c", "x", 1, 1)
        b.add_heading("a", "x", 1, 1)
        b.add_heading("b", "x", 1, 1)
        assert b.all_doc_ids() == ["a", "b", "c"]

    def test_unique(self):
        b = DocOutlineBuilder()
        b.add_heading("a", "x", 1, 1)
        b.add_heading("a", "y", 1, 2)
        assert b.all_doc_ids() == ["a"]


# --------------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        s = DocOutlineBuilder().stats()
        assert s == OutlineStats(total_docs=0, total_nodes=0, max_depth=0)

    def test_single_doc(self):
        b = DocOutlineBuilder()
        b.add_heading("d", "A", 1, 1)
        b.add_heading("d", "A.1", 2, 2)
        s = b.stats()
        assert s.total_docs == 1
        assert s.total_nodes == 2
        assert s.max_depth == 2

    def test_multi_doc(self):
        b = DocOutlineBuilder()
        b.add_heading("a", "A", 1, 1)
        b.add_heading("a", "B", 3, 2)
        b.add_heading("b", "C", 2, 1)
        s = b.stats()
        assert s.total_docs == 2
        assert s.total_nodes == 3
        assert s.max_depth == 3


# --------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_add_heading(self):
        b = DocOutlineBuilder()
        errors: list[BaseException] = []

        def worker(start: int):
            try:
                for i in range(50):
                    b.add_heading(
                        "d", f"H{start}-{i}", 1, start * 1000 + i
                    )
            except BaseException as exc:  # pragma: no cover - safety net
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert b.node_count("d") == 8 * 50

    def test_concurrent_add_separate_docs(self):
        b = DocOutlineBuilder()

        def worker(doc: str):
            for i in range(30):
                b.add_heading(doc, f"H{i}", 1, i)

        threads = [
            threading.Thread(target=worker, args=(f"d{i}",))
            for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert b.all_doc_ids() == [f"d{i}" for i in range(5)]
        for i in range(5):
            assert b.node_count(f"d{i}") == 30

    def test_concurrent_add_and_clear(self):
        b = DocOutlineBuilder()
        for i in range(20):
            b.add_heading("d", f"H{i}", 1, i)

        def adder():
            for i in range(50):
                b.add_heading("e", f"E{i}", 1, i)

        def clearer():
            for _ in range(5):
                b.clear_doc("d")

        t1 = threading.Thread(target=adder)
        t2 = threading.Thread(target=clearer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert b.node_count("e") == 50
