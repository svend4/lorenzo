"""Tests for E337 DocTagHierarchy module.

Run with:
    cd /home/user/lorenzo/docs-toolkit
    python -m pytest tests/test_doc_tag_hierarchy.py -q
"""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_tag_hierarchy import (
    DocTagHierarchy,
    TagHierarchyStats,
    TagNode,
)


# ---------------------------------------------------------------------------
# TestTagNodeDataclass
# ---------------------------------------------------------------------------

class TestTagNodeDataclass:
    def test_required_field_tag(self):
        n = TagNode(tag="python")
        assert n.tag == "python"

    def test_default_parent_is_none(self):
        n = TagNode(tag="python")
        assert n.parent is None

    def test_default_description_is_empty(self):
        n = TagNode(tag="python")
        assert n.description == ""

    def test_default_depth_is_zero(self):
        n = TagNode(tag="python")
        assert n.depth == 0

    def test_explicit_fields(self):
        n = TagNode(tag="django", parent="python", description="web framework", depth=1)
        assert n.parent == "python"
        assert n.description == "web framework"
        assert n.depth == 1

    def test_equality(self):
        n1 = TagNode(tag="a", parent="root", description="d", depth=1)
        n2 = TagNode(tag="a", parent="root", description="d", depth=1)
        assert n1 == n2

    def test_inequality_different_tag(self):
        assert TagNode(tag="a") != TagNode(tag="b")


# ---------------------------------------------------------------------------
# TestTagHierarchyStatsDataclass
# ---------------------------------------------------------------------------

class TestTagHierarchyStatsDataclass:
    def test_fields_accessible(self):
        s = TagHierarchyStats(total_tags=10, root_count=2, max_depth=4, leaf_count=5)
        assert s.total_tags == 10
        assert s.root_count == 2
        assert s.max_depth == 4
        assert s.leaf_count == 5

    def test_zero_values(self):
        s = TagHierarchyStats(total_tags=0, root_count=0, max_depth=0, leaf_count=0)
        assert s.total_tags == 0

    def test_equality(self):
        s1 = TagHierarchyStats(total_tags=1, root_count=1, max_depth=0, leaf_count=1)
        s2 = TagHierarchyStats(total_tags=1, root_count=1, max_depth=0, leaf_count=1)
        assert s1 == s2


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_construct_empty(self):
        h = DocTagHierarchy()
        assert h.all_tags() == []

    def test_construct_independent_instances(self):
        a = DocTagHierarchy()
        b = DocTagHierarchy()
        a.add_tag("x")
        assert b.all_tags() == []

    def test_initial_stats_empty(self):
        h = DocTagHierarchy()
        s = h.stats()
        assert s.total_tags == 0
        assert s.root_count == 0
        assert s.max_depth == 0
        assert s.leaf_count == 0


# ---------------------------------------------------------------------------
# TestAddTag
# ---------------------------------------------------------------------------

class TestAddTag:
    def test_add_root_tag(self):
        h = DocTagHierarchy()
        node = h.add_tag("python")
        assert node.tag == "python"
        assert node.parent is None
        assert node.depth == 0

    def test_add_root_with_description(self):
        h = DocTagHierarchy()
        node = h.add_tag("python", description="Python language")
        assert node.description == "Python language"

    def test_add_child_depth_is_one(self):
        h = DocTagHierarchy()
        h.add_tag("python")
        node = h.add_tag("django", parent="python")
        assert node.parent == "python"
        assert node.depth == 1

    def test_add_grandchild_depth_is_two(self):
        h = DocTagHierarchy()
        h.add_tag("python")
        h.add_tag("django", parent="python")
        n = h.add_tag("orm", parent="django")
        assert n.depth == 2

    def test_missing_parent_raises_value_error(self):
        h = DocTagHierarchy()
        with pytest.raises(ValueError, match="Parent not found"):
            h.add_tag("django", parent="python")

    def test_missing_parent_does_not_add_node(self):
        h = DocTagHierarchy()
        with pytest.raises(ValueError):
            h.add_tag("django", parent="python")
        assert h.get_tag("django") is None

    def test_update_existing_tag_description(self):
        h = DocTagHierarchy()
        h.add_tag("python", description="old")
        n = h.add_tag("python", description="new")
        assert n.description == "new"

    def test_update_existing_tag_parent(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b")
        h.add_tag("c", parent="a")
        n = h.add_tag("c", parent="b")
        assert n.parent == "b"
        assert n.depth == 1
        assert "c" not in [t.tag for t in h.children_of("a")]
        assert "c" in [t.tag for t in h.children_of("b")]

    def test_add_returns_tag_node_instance(self):
        h = DocTagHierarchy()
        n = h.add_tag("python")
        assert isinstance(n, TagNode)


# ---------------------------------------------------------------------------
# TestRemoveTag
# ---------------------------------------------------------------------------

class TestRemoveTag:
    def test_remove_leaf_no_children(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        assert h.remove_tag("a") == 1
        assert h.get_tag("a") is None

    def test_remove_unknown_returns_zero(self):
        h = DocTagHierarchy()
        assert h.remove_tag("nope") == 0

    def test_remove_with_children_raises_no_cascade(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c", parent="p")
        with pytest.raises(ValueError, match="Tag has children"):
            h.remove_tag("p")

    def test_remove_with_children_no_cascade_does_not_modify_state(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c", parent="p")
        with pytest.raises(ValueError):
            h.remove_tag("p")
        assert h.get_tag("p") is not None
        assert h.get_tag("c") is not None

    def test_remove_cascade_removes_descendants(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c1", parent="p")
        h.add_tag("c2", parent="p")
        h.add_tag("gc", parent="c1")
        removed = h.remove_tag("p", cascade=True)
        assert removed == 4
        assert h.get_tag("p") is None
        assert h.get_tag("c1") is None
        assert h.get_tag("c2") is None
        assert h.get_tag("gc") is None

    def test_remove_cascade_on_leaf_returns_one(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        assert h.remove_tag("a", cascade=True) == 1

    def test_remove_unlinks_from_parent(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c", parent="p")
        h.remove_tag("c")
        assert h.children_of("p") == []


# ---------------------------------------------------------------------------
# TestGetTag
# ---------------------------------------------------------------------------

class TestGetTag:
    def test_get_found(self):
        h = DocTagHierarchy()
        h.add_tag("python", description="lang")
        n = h.get_tag("python")
        assert n is not None
        assert n.tag == "python"
        assert n.description == "lang"

    def test_get_not_found(self):
        h = DocTagHierarchy()
        assert h.get_tag("nope") is None


# ---------------------------------------------------------------------------
# TestChildrenOf
# ---------------------------------------------------------------------------

class TestChildrenOf:
    def test_children_sorted_by_tag(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("zeta", parent="p")
        h.add_tag("alpha", parent="p")
        h.add_tag("mid", parent="p")
        tags = [n.tag for n in h.children_of("p")]
        assert tags == ["alpha", "mid", "zeta"]

    def test_children_empty_for_leaf(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        assert h.children_of("p") == []

    def test_children_empty_for_unknown(self):
        h = DocTagHierarchy()
        assert h.children_of("nope") == []


# ---------------------------------------------------------------------------
# TestDescendantsOf
# ---------------------------------------------------------------------------

class TestDescendantsOf:
    def test_descendants_bfs(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        h.add_tag("a", parent="root")
        h.add_tag("b", parent="root")
        h.add_tag("a1", parent="a")
        h.add_tag("b1", parent="b")
        h.add_tag("a1x", parent="a1")
        tags = [n.tag for n in h.descendants_of("root")]
        # Level 1 sorted: a, b ; Level 2 sorted: a1, b1 ; Level 3: a1x
        assert tags == ["a", "b", "a1", "b1", "a1x"]

    def test_descendants_empty_for_leaf(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        assert h.descendants_of("p") == []

    def test_descendants_empty_for_unknown(self):
        h = DocTagHierarchy()
        assert h.descendants_of("nope") == []


# ---------------------------------------------------------------------------
# TestAncestorsOf
# ---------------------------------------------------------------------------

class TestAncestorsOf:
    def test_ancestor_chain_order(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        h.add_tag("mid", parent="root")
        h.add_tag("leaf", parent="mid")
        tags = [n.tag for n in h.ancestors_of("leaf")]
        assert tags == ["mid", "root"]

    def test_ancestors_empty_for_root(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        assert h.ancestors_of("root") == []

    def test_ancestors_empty_for_unknown(self):
        h = DocTagHierarchy()
        assert h.ancestors_of("nope") == []


# ---------------------------------------------------------------------------
# TestIsDescendant
# ---------------------------------------------------------------------------

class TestIsDescendant:
    def test_direct_child_is_descendant(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c", parent="p")
        assert h.is_descendant("c", "p") is True

    def test_grandchild_is_descendant(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c", parent="p")
        h.add_tag("gc", parent="c")
        assert h.is_descendant("gc", "p") is True

    def test_not_descendant_returns_false(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("q")
        assert h.is_descendant("p", "q") is False

    def test_self_is_not_descendant(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        assert h.is_descendant("p", "p") is False

    def test_unknown_returns_false(self):
        h = DocTagHierarchy()
        assert h.is_descendant("a", "b") is False


# ---------------------------------------------------------------------------
# TestRoots
# ---------------------------------------------------------------------------

class TestRoots:
    def test_roots_sorted(self):
        h = DocTagHierarchy()
        h.add_tag("zeta")
        h.add_tag("alpha")
        h.add_tag("mid")
        tags = [n.tag for n in h.roots()]
        assert tags == ["alpha", "mid", "zeta"]

    def test_roots_excludes_children(self):
        h = DocTagHierarchy()
        h.add_tag("p")
        h.add_tag("c", parent="p")
        tags = [n.tag for n in h.roots()]
        assert tags == ["p"]

    def test_roots_empty(self):
        h = DocTagHierarchy()
        assert h.roots() == []


# ---------------------------------------------------------------------------
# TestAllTags
# ---------------------------------------------------------------------------

class TestAllTags:
    def test_all_tags_sorted(self):
        h = DocTagHierarchy()
        h.add_tag("zeta")
        h.add_tag("alpha")
        h.add_tag("beta", parent="alpha")
        tags = [n.tag for n in h.all_tags()]
        assert tags == ["alpha", "beta", "zeta"]

    def test_all_tags_empty(self):
        h = DocTagHierarchy()
        assert h.all_tags() == []


# ---------------------------------------------------------------------------
# TestMoveTag
# ---------------------------------------------------------------------------

class TestMoveTag:
    def test_move_changes_parent(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b")
        h.add_tag("c", parent="a")
        assert h.move_tag("c", "b") is True
        assert h.get_tag("c").parent == "b"

    def test_move_to_root(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("c", parent="a")
        assert h.move_tag("c", None) is True
        assert h.get_tag("c").parent is None
        assert h.get_tag("c").depth == 0

    def test_move_recomputes_depths(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b")
        h.add_tag("c", parent="a")
        h.add_tag("d", parent="c")
        h.add_tag("e", parent="d")
        h.move_tag("c", "b")
        assert h.get_tag("c").depth == 1
        assert h.get_tag("d").depth == 2
        assert h.get_tag("e").depth == 3

    def test_move_cycle_returns_false(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b", parent="a")
        h.add_tag("c", parent="b")
        # Moving "a" under "c" would create a cycle.
        assert h.move_tag("a", "c") is False
        assert h.get_tag("a").parent is None

    def test_move_self_returns_false(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        assert h.move_tag("a", "a") is False

    def test_move_unknown_tag_returns_false(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        assert h.move_tag("nope", "a") is False

    def test_move_unknown_parent_returns_false(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        assert h.move_tag("a", "nope") is False

    def test_move_to_same_parent_is_true(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b", parent="a")
        assert h.move_tag("b", "a") is True

    def test_move_updates_children_lists(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b")
        h.add_tag("c", parent="a")
        h.move_tag("c", "b")
        assert [n.tag for n in h.children_of("a")] == []
        assert [n.tag for n in h.children_of("b")] == ["c"]


# ---------------------------------------------------------------------------
# TestPathToRoot
# ---------------------------------------------------------------------------

class TestPathToRoot:
    def test_chain_order(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        h.add_tag("mid", parent="root")
        h.add_tag("leaf", parent="mid")
        assert h.path_to_root("leaf") == ["leaf", "mid", "root"]

    def test_root_single_element(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        assert h.path_to_root("root") == ["root"]

    def test_unknown_returns_empty(self):
        h = DocTagHierarchy()
        assert h.path_to_root("nope") == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_basic(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b")
        h.add_tag("c", parent="a")
        s = h.stats()
        assert s.total_tags == 3
        assert s.root_count == 2

    def test_stats_max_depth(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b", parent="a")
        h.add_tag("c", parent="b")
        h.add_tag("d", parent="c")
        assert h.stats().max_depth == 3

    def test_stats_leaf_count(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b", parent="a")
        h.add_tag("c", parent="a")
        h.add_tag("d", parent="b")
        # Leaves: c, d
        assert h.stats().leaf_count == 2

    def test_stats_root_count_only_no_parent(self):
        h = DocTagHierarchy()
        h.add_tag("a")
        h.add_tag("b")
        h.add_tag("c", parent="a")
        assert h.stats().root_count == 2

    def test_stats_empty_hierarchy(self):
        h = DocTagHierarchy()
        s = h.stats()
        assert s == TagHierarchyStats(total_tags=0, root_count=0, max_depth=0, leaf_count=0)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_add_tag(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        errors: list[BaseException] = []

        def worker(start: int, count: int) -> None:
            try:
                for i in range(start, start + count):
                    h.add_tag(f"tag_{i}", parent="root")
            except BaseException as e:  # pragma: no cover - failure path
                errors.append(e)

        threads = [
            threading.Thread(target=worker, args=(i * 100, 100)) for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # 1 root + 8 * 100 children
        assert h.stats().total_tags == 1 + 800
        assert len(h.children_of("root")) == 800

    def test_concurrent_add_and_remove(self):
        h = DocTagHierarchy()
        h.add_tag("root")
        for i in range(200):
            h.add_tag(f"t_{i}", parent="root")

        errors: list[BaseException] = []

        def remover(start: int, count: int) -> None:
            try:
                for i in range(start, start + count):
                    h.remove_tag(f"t_{i}")
            except BaseException as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=remover, args=(i * 50, 50)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert h.stats().total_tags == 1  # only root left
