"""Tests for E319 DocHierarchyStore module.

Run with:
    cd /home/user/lorenzo/docs-toolkit
    python -m pytest tests/test_doc_hierarchy_store.py -q
"""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_hierarchy_store import (
    DocHierarchyStore,
    HierarchyNode,
    HierarchyStats,
)


# ---------------------------------------------------------------------------
# TestHierarchyNodeDataclass
# ---------------------------------------------------------------------------

class TestHierarchyNodeDataclass:
    def test_required_field_doc_id(self):
        n = HierarchyNode(doc_id="a")
        assert n.doc_id == "a"

    def test_default_parent_id_is_none(self):
        n = HierarchyNode(doc_id="a")
        assert n.parent_id is None

    def test_default_title_is_empty(self):
        n = HierarchyNode(doc_id="a")
        assert n.title == ""

    def test_default_position_is_zero(self):
        n = HierarchyNode(doc_id="a")
        assert n.position == 0

    def test_default_depth_is_zero(self):
        n = HierarchyNode(doc_id="a")
        assert n.depth == 0

    def test_explicit_fields(self):
        n = HierarchyNode(doc_id="x", parent_id="root", title="X Doc", position=3, depth=2)
        assert n.parent_id == "root"
        assert n.title == "X Doc"
        assert n.position == 3
        assert n.depth == 2

    def test_equality(self):
        n1 = HierarchyNode(doc_id="a", title="T", position=1, depth=0)
        n2 = HierarchyNode(doc_id="a", title="T", position=1, depth=0)
        assert n1 == n2

    def test_inequality_different_doc_id(self):
        n1 = HierarchyNode(doc_id="a")
        n2 = HierarchyNode(doc_id="b")
        assert n1 != n2


# ---------------------------------------------------------------------------
# TestHierarchyStatsDataclass
# ---------------------------------------------------------------------------

class TestHierarchyStatsDataclass:
    def test_fields_accessible(self):
        s = HierarchyStats(total_nodes=10, root_count=2, max_depth=4, leaf_count=5)
        assert s.total_nodes == 10
        assert s.root_count == 2
        assert s.max_depth == 4
        assert s.leaf_count == 5

    def test_zero_values(self):
        s = HierarchyStats(total_nodes=0, root_count=0, max_depth=0, leaf_count=0)
        assert s.total_nodes == 0

    def test_equality(self):
        s1 = HierarchyStats(total_nodes=1, root_count=1, max_depth=0, leaf_count=1)
        s2 = HierarchyStats(total_nodes=1, root_count=1, max_depth=0, leaf_count=1)
        assert s1 == s2


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_store_all_nodes_empty(self):
        s = DocHierarchyStore()
        assert s.all_nodes() == []

    def test_empty_store_roots_empty(self):
        s = DocHierarchyStore()
        assert s.roots() == []

    def test_empty_store_stats(self):
        s = DocHierarchyStore()
        st = s.stats()
        assert st.total_nodes == 0
        assert st.root_count == 0
        assert st.max_depth == 0
        assert st.leaf_count == 0


# ---------------------------------------------------------------------------
# TestAddNode
# ---------------------------------------------------------------------------

class TestAddNode:
    def test_add_root_node_returns_node(self):
        s = DocHierarchyStore()
        node = s.add_node("root")
        assert node.doc_id == "root"

    def test_root_node_has_no_parent(self):
        s = DocHierarchyStore()
        node = s.add_node("root")
        assert node.parent_id is None

    def test_root_node_depth_is_zero(self):
        s = DocHierarchyStore()
        node = s.add_node("root")
        assert node.depth == 0

    def test_child_node_depth_is_one(self):
        s = DocHierarchyStore()
        s.add_node("root")
        child = s.add_node("child", parent_id="root")
        assert child.depth == 1

    def test_grandchild_depth_is_two(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        grandchild = s.add_node("gc", parent_id="child")
        assert grandchild.depth == 2

    def test_add_node_with_title_and_position(self):
        s = DocHierarchyStore()
        node = s.add_node("a", title="Alpha", position=5)
        assert node.title == "Alpha"
        assert node.position == 5

    def test_update_existing_node(self):
        s = DocHierarchyStore()
        s.add_node("a", title="Old")
        node = s.add_node("a", title="New")
        assert node.title == "New"

    def test_update_existing_node_same_object_retrieved(self):
        s = DocHierarchyStore()
        s.add_node("a", title="Old")
        s.add_node("a", title="Updated")
        retrieved = s.get_node("a")
        assert retrieved.title == "Updated"

    def test_update_parent_updates_depth(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("middle", parent_id="root")
        s.add_node("leaf", parent_id="middle")
        # Re-add leaf directly under root
        node = s.add_node("leaf", parent_id="root")
        assert node.depth == 1

    def test_node_appears_in_all_nodes(self):
        s = DocHierarchyStore()
        s.add_node("x")
        ids = [n.doc_id for n in s.all_nodes()]
        assert "x" in ids


# ---------------------------------------------------------------------------
# TestRemoveNodeReparent
# ---------------------------------------------------------------------------

class TestRemoveNodeReparent:
    def test_reparent_returns_one(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("leaf", parent_id="mid")
        assert s.remove_node("mid", reparent_children=True) == 1

    def test_reparent_children_moved_to_grandparent(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("leaf", parent_id="mid")
        s.remove_node("mid", reparent_children=True)
        leaf = s.get_node("leaf")
        assert leaf.parent_id == "root"

    def test_reparent_depth_recomputed(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("leaf", parent_id="mid")
        s.remove_node("mid", reparent_children=True)
        leaf = s.get_node("leaf")
        assert leaf.depth == 1

    def test_reparent_removed_node_gone(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.remove_node("mid", reparent_children=True)
        assert s.get_node("mid") is None

    def test_reparent_multiple_children(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("c1", parent_id="mid")
        s.add_node("c2", parent_id="mid")
        s.remove_node("mid", reparent_children=True)
        assert s.get_node("c1").parent_id == "root"
        assert s.get_node("c2").parent_id == "root"

    def test_reparent_root_removal_children_become_roots(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        s.remove_node("root", reparent_children=True)
        child = s.get_node("child")
        assert child.parent_id is None
        assert child.depth == 0


# ---------------------------------------------------------------------------
# TestRemoveNodeCascade
# ---------------------------------------------------------------------------

class TestRemoveNodeCascade:
    def test_cascade_removes_node_and_descendants(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        s.add_node("gc", parent_id="child")
        count = s.remove_node("child", reparent_children=False)
        assert count == 2
        assert s.get_node("child") is None
        assert s.get_node("gc") is None

    def test_cascade_count_single_node(self):
        s = DocHierarchyStore()
        s.add_node("root")
        assert s.remove_node("root") == 1

    def test_cascade_deep_tree(self):
        s = DocHierarchyStore()
        s.add_node("a")
        s.add_node("b", parent_id="a")
        s.add_node("c", parent_id="b")
        s.add_node("d", parent_id="c")
        count = s.remove_node("a")
        assert count == 4
        for nid in ("a", "b", "c", "d"):
            assert s.get_node(nid) is None

    def test_cascade_nonexistent_returns_zero(self):
        s = DocHierarchyStore()
        assert s.remove_node("ghost") == 0

    def test_cascade_sibling_preserved(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("a", parent_id="root")
        s.add_node("b", parent_id="root")
        s.remove_node("a")
        assert s.get_node("b") is not None

    def test_cascade_parent_preserved(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        s.remove_node("child")
        assert s.get_node("root") is not None


# ---------------------------------------------------------------------------
# TestMoveNode
# ---------------------------------------------------------------------------

class TestMoveNode:
    def test_move_changes_parent(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("other_root")
        s.add_node("child", parent_id="root")
        result = s.move_node("child", "other_root")
        assert result is True
        assert s.get_node("child").parent_id == "other_root"

    def test_move_recomputes_depth(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("leaf", parent_id="mid")
        s.move_node("leaf", "root")
        assert s.get_node("leaf").depth == 1

    def test_move_recomputes_descendants_depth(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("other_root")
        s.add_node("parent", parent_id="root")
        s.add_node("child", parent_id="parent")
        # Move parent subtree under other_root (depth 0), child should be depth 2
        s.move_node("parent", "other_root")
        assert s.get_node("parent").depth == 1
        assert s.get_node("child").depth == 2

    def test_move_cycle_detection_direct(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        # Moving root under child would create a cycle
        result = s.move_node("root", "child")
        assert result is False

    def test_move_cycle_detection_indirect(self):
        s = DocHierarchyStore()
        s.add_node("a")
        s.add_node("b", parent_id="a")
        s.add_node("c", parent_id="b")
        # Moving a under c would create a cycle
        result = s.move_node("a", "c")
        assert result is False

    def test_move_self_returns_false(self):
        s = DocHierarchyStore()
        s.add_node("a")
        assert s.move_node("a", "a") is False

    def test_move_nonexistent_doc_returns_false(self):
        s = DocHierarchyStore()
        s.add_node("root")
        assert s.move_node("ghost", "root") is False

    def test_move_to_nonexistent_parent_returns_false(self):
        s = DocHierarchyStore()
        s.add_node("a")
        assert s.move_node("a", "nonexistent") is False

    def test_move_to_none_makes_root(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        result = s.move_node("child", None)
        assert result is True
        node = s.get_node("child")
        assert node.parent_id is None
        assert node.depth == 0


# ---------------------------------------------------------------------------
# TestGetNode
# ---------------------------------------------------------------------------

class TestGetNode:
    def test_found(self):
        s = DocHierarchyStore()
        s.add_node("a", title="Alpha")
        n = s.get_node("a")
        assert n is not None
        assert n.doc_id == "a"
        assert n.title == "Alpha"

    def test_not_found_returns_none(self):
        s = DocHierarchyStore()
        assert s.get_node("missing") is None


# ---------------------------------------------------------------------------
# TestChildren
# ---------------------------------------------------------------------------

class TestChildren:
    def test_sorted_by_position_then_doc_id(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("c", parent_id="root", position=2)
        s.add_node("a", parent_id="root", position=1)
        s.add_node("b", parent_id="root", position=1)
        kids = s.children("root")
        # position 1 before position 2; among position-1 ties, sort by doc_id
        assert kids[0].doc_id == "a"
        assert kids[1].doc_id == "b"
        assert kids[2].doc_id == "c"

    def test_empty_for_leaf(self):
        s = DocHierarchyStore()
        s.add_node("leaf")
        assert s.children("leaf") == []

    def test_empty_for_unknown(self):
        s = DocHierarchyStore()
        assert s.children("ghost") == []

    def test_returns_hierarchy_nodes(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        kids = s.children("root")
        assert len(kids) == 1
        assert isinstance(kids[0], HierarchyNode)


# ---------------------------------------------------------------------------
# TestParent
# ---------------------------------------------------------------------------

class TestParent:
    def test_found_for_child(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        p = s.parent("child")
        assert p is not None
        assert p.doc_id == "root"

    def test_none_for_root(self):
        s = DocHierarchyStore()
        s.add_node("root")
        assert s.parent("root") is None

    def test_none_for_unknown(self):
        s = DocHierarchyStore()
        assert s.parent("ghost") is None


# ---------------------------------------------------------------------------
# TestAncestors
# ---------------------------------------------------------------------------

class TestAncestors:
    def test_single_parent(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        ancs = s.ancestors("child")
        assert len(ancs) == 1
        assert ancs[0].doc_id == "root"

    def test_chain_order(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("leaf", parent_id="mid")
        ancs = s.ancestors("leaf")
        assert ancs[0].doc_id == "mid"
        assert ancs[1].doc_id == "root"

    def test_empty_for_root(self):
        s = DocHierarchyStore()
        s.add_node("root")
        assert s.ancestors("root") == []

    def test_empty_for_unknown(self):
        s = DocHierarchyStore()
        assert s.ancestors("ghost") == []


# ---------------------------------------------------------------------------
# TestDescendants
# ---------------------------------------------------------------------------

class TestDescendants:
    def test_bfs_order(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("a", parent_id="root")
        s.add_node("b", parent_id="root")
        s.add_node("c", parent_id="a")
        descs = s.descendants("root")
        # First level: a, b (sorted by doc_id); second level: c
        assert descs[0].doc_id == "a"
        assert descs[1].doc_id == "b"
        assert descs[2].doc_id == "c"

    def test_empty_for_leaf(self):
        s = DocHierarchyStore()
        s.add_node("leaf")
        assert s.descendants("leaf") == []

    def test_empty_for_unknown(self):
        s = DocHierarchyStore()
        assert s.descendants("ghost") == []

    def test_all_descendants_included(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("a", parent_id="root")
        s.add_node("b", parent_id="a")
        descs = s.descendants("root")
        doc_ids = {n.doc_id for n in descs}
        assert doc_ids == {"a", "b"}


# ---------------------------------------------------------------------------
# TestRoots
# ---------------------------------------------------------------------------

class TestRoots:
    def test_single_root(self):
        s = DocHierarchyStore()
        s.add_node("root")
        roots = s.roots()
        assert len(roots) == 1
        assert roots[0].doc_id == "root"

    def test_multiple_roots_sorted(self):
        s = DocHierarchyStore()
        s.add_node("b_root", position=0)
        s.add_node("a_root", position=0)
        s.add_node("c_root", position=1)
        roots = s.roots()
        # Same position 0 → sorted by doc_id; c_root position 1 last
        assert roots[0].doc_id == "a_root"
        assert roots[1].doc_id == "b_root"
        assert roots[2].doc_id == "c_root"

    def test_no_roots_for_empty_store(self):
        s = DocHierarchyStore()
        assert s.roots() == []

    def test_roots_excludes_children(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        roots = s.roots()
        assert all(r.parent_id is None for r in roots)
        assert len(roots) == 1


# ---------------------------------------------------------------------------
# TestAllNodes
# ---------------------------------------------------------------------------

class TestAllNodes:
    def test_sorted_by_doc_id(self):
        s = DocHierarchyStore()
        s.add_node("c")
        s.add_node("a")
        s.add_node("b")
        ids = [n.doc_id for n in s.all_nodes()]
        assert ids == ["a", "b", "c"]

    def test_empty_store(self):
        s = DocHierarchyStore()
        assert s.all_nodes() == []

    def test_count_matches(self):
        s = DocHierarchyStore()
        for i in range(5):
            s.add_node(f"node_{i}")
        assert len(s.all_nodes()) == 5


# ---------------------------------------------------------------------------
# TestPathToRoot
# ---------------------------------------------------------------------------

class TestPathToRoot:
    def test_single_node_path(self):
        s = DocHierarchyStore()
        s.add_node("root")
        assert s.path_to_root("root") == ["root"]

    def test_chain_path(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("mid", parent_id="root")
        s.add_node("leaf", parent_id="mid")
        path = s.path_to_root("leaf")
        assert path == ["leaf", "mid", "root"]

    def test_unknown_doc_returns_empty(self):
        s = DocHierarchyStore()
        assert s.path_to_root("ghost") == []

    def test_two_level_path(self):
        s = DocHierarchyStore()
        s.add_node("parent")
        s.add_node("child", parent_id="parent")
        path = s.path_to_root("child")
        assert path == ["child", "parent"]


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_store(self):
        s = DocHierarchyStore()
        st = s.stats()
        assert st.total_nodes == 0
        assert st.root_count == 0
        assert st.max_depth == 0
        assert st.leaf_count == 0

    def test_single_root_is_also_leaf(self):
        s = DocHierarchyStore()
        s.add_node("root")
        st = s.stats()
        assert st.total_nodes == 1
        assert st.root_count == 1
        assert st.max_depth == 0
        assert st.leaf_count == 1

    def test_max_depth(self):
        s = DocHierarchyStore()
        s.add_node("a")
        s.add_node("b", parent_id="a")
        s.add_node("c", parent_id="b")
        st = s.stats()
        assert st.max_depth == 2

    def test_leaf_count(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("a", parent_id="root")
        s.add_node("b", parent_id="root")
        st = s.stats()
        # root has children → not a leaf; a and b have no children → leaves
        assert st.leaf_count == 2

    def test_root_count_multiple(self):
        s = DocHierarchyStore()
        s.add_node("r1")
        s.add_node("r2")
        s.add_node("child", parent_id="r1")
        st = s.stats()
        assert st.root_count == 2

    def test_stats_after_remove(self):
        s = DocHierarchyStore()
        s.add_node("root")
        s.add_node("child", parent_id="root")
        s.remove_node("child")
        st = s.stats()
        assert st.total_nodes == 1
        assert st.leaf_count == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_add_node(self):
        """Multiple threads adding nodes must not corrupt internal state."""
        store = DocHierarchyStore()
        errors: list[Exception] = []

        def worker(thread_id: int) -> None:
            try:
                for i in range(30):
                    store.add_node(f"doc_{thread_id}_{i}", title=f"T{thread_id}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        nodes = store.all_nodes()
        ids = [n.doc_id for n in nodes]
        assert len(ids) == len(set(ids)), "Duplicate doc_ids detected"
        assert len(ids) == 8 * 30
