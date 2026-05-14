"""Tests for docstoolkit.heading_tree — ≥45 tests."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.heading_tree import HeadingTree, HeadingNode


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _simple_tree() -> HeadingTree:
    """H1 → H2, H2 → H3 structure."""
    text = "\n".join([
        "# Root",
        "## Child A",
        "### Grandchild A1",
        "### Grandchild A2",
        "## Child B",
        "### Grandchild B1",
    ])
    return HeadingTree.build(text)


# ---------------------------------------------------------------------------
# TestHeadingNodeProperties
# ---------------------------------------------------------------------------

class TestHeadingNodeProperties:
    def test_slug_basic(self):
        node = HeadingNode(level=1, title="Hello World", line_num=1)
        assert node.slug == "hello-world"

    def test_slug_special_chars_stripped(self):
        node = HeadingNode(level=2, title="My (Great) Section!", line_num=1)
        assert node.slug == "my-great-section"

    def test_slug_lowercase(self):
        node = HeadingNode(level=1, title="UPPERCASE TITLE", line_num=1)
        assert node.slug == "uppercase-title"

    def test_slug_multiple_spaces_become_multiple_hyphens_then_collapsed(self):
        node = HeadingNode(level=1, title="A  B", line_num=1)
        # two spaces → two hyphens → collapsed to one
        assert node.slug == "a-b"

    def test_slug_already_hyphenated(self):
        node = HeadingNode(level=1, title="step-by-step", line_num=1)
        assert node.slug == "step-by-step"

    def test_slug_numbers_preserved(self):
        node = HeadingNode(level=1, title="Version 2.0 Release", line_num=1)
        assert node.slug == "version-20-release"

    def test_depth_level1(self):
        node = HeadingNode(level=1, title="Root", line_num=1)
        assert node.depth == 0

    def test_depth_level2(self):
        node = HeadingNode(level=2, title="Sub", line_num=2)
        assert node.depth == 1

    def test_depth_level6(self):
        node = HeadingNode(level=6, title="Deep", line_num=10)
        assert node.depth == 5

    def test_is_leaf_no_children(self):
        node = HeadingNode(level=1, title="Lone", line_num=1)
        assert node.is_leaf is True

    def test_is_leaf_with_children(self):
        parent = HeadingNode(level=1, title="Parent", line_num=1)
        child = HeadingNode(level=2, title="Child", line_num=2, parent=parent)
        parent.children.append(child)
        assert parent.is_leaf is False

    def test_is_leaf_child_is_leaf(self):
        parent = HeadingNode(level=1, title="Parent", line_num=1)
        child = HeadingNode(level=2, title="Child", line_num=2, parent=parent)
        parent.children.append(child)
        assert child.is_leaf is True


# ---------------------------------------------------------------------------
# TestHeadingNodeDescendants
# ---------------------------------------------------------------------------

class TestHeadingNodeDescendants:
    def test_descendants_leaf_empty(self):
        node = HeadingNode(level=1, title="Leaf", line_num=1)
        assert node.descendants() == []

    def test_descendants_single_child(self):
        tree = HeadingTree.build("# Root\n## Child")
        root = tree.roots[0]
        desc = root.descendants()
        assert len(desc) == 1
        assert desc[0].title == "Child"

    def test_descendants_bfs_order(self):
        tree = _simple_tree()
        root = tree.roots[0]
        desc = root.descendants()
        titles = [n.title for n in desc]
        # BFS: children before grandchildren
        assert titles.index("Child A") < titles.index("Grandchild A1")
        assert titles.index("Child B") < titles.index("Grandchild B1")
        assert titles.index("Child A") < titles.index("Child B")

    def test_descendants_count(self):
        tree = _simple_tree()
        root = tree.roots[0]
        assert len(root.descendants()) == 5  # A, A1, A2, B, B1

    def test_descendants_subtree(self):
        tree = _simple_tree()
        child_a = tree.roots[0].children[0]
        desc = child_a.descendants()
        titles = [n.title for n in desc]
        assert set(titles) == {"Grandchild A1", "Grandchild A2"}


# ---------------------------------------------------------------------------
# TestHeadingNodeAncestors
# ---------------------------------------------------------------------------

class TestHeadingNodeAncestors:
    def test_ancestors_root_empty(self):
        tree = _simple_tree()
        assert tree.roots[0].ancestors() == []

    def test_ancestors_child_has_one(self):
        tree = _simple_tree()
        child_a = tree.roots[0].children[0]
        ancs = child_a.ancestors()
        assert len(ancs) == 1
        assert ancs[0].title == "Root"

    def test_ancestors_grandchild_order(self):
        tree = _simple_tree()
        gc = tree.roots[0].children[0].children[0]  # Grandchild A1
        ancs = gc.ancestors()
        assert [n.title for n in ancs] == ["Root", "Child A"]

    def test_ancestors_does_not_include_self(self):
        tree = _simple_tree()
        root = tree.roots[0]
        assert root not in root.ancestors()

    def test_ancestors_from_root_to_parent(self):
        tree = _simple_tree()
        gc = tree.roots[0].children[1].children[0]  # Grandchild B1
        ancs = gc.ancestors()
        assert ancs[0].title == "Root"
        assert ancs[-1].title == "Child B"


# ---------------------------------------------------------------------------
# TestHeadingTreeBuildFlat
# ---------------------------------------------------------------------------

class TestHeadingTreeBuildFlat:
    def test_build_single_h1(self):
        tree = HeadingTree.build("# Hello")
        assert len(tree.roots) == 1
        assert tree.roots[0].title == "Hello"
        assert tree.roots[0].level == 1

    def test_build_multiple_h1s(self):
        tree = HeadingTree.build("# A\n# B\n# C")
        assert len(tree.roots) == 3

    def test_build_line_numbers(self):
        tree = HeadingTree.build("# First\n\n# Second")
        assert tree.roots[0].line_num == 1
        assert tree.roots[1].line_num == 3

    def test_build_strips_title(self):
        tree = HeadingTree.build("#   Spaced Title  ")
        assert tree.roots[0].title == "Spaced Title"

    def test_build_ignores_non_headings(self):
        text = "Some paragraph.\n# Real Heading\nMore text."
        tree = HeadingTree.build(text)
        assert len(tree.roots) == 1
        assert tree.roots[0].title == "Real Heading"


# ---------------------------------------------------------------------------
# TestHeadingTreeBuildNested
# ---------------------------------------------------------------------------

class TestHeadingTreeBuildNested:
    def test_h1_h2_parent_child(self):
        tree = HeadingTree.build("# Parent\n## Child")
        assert len(tree.roots) == 1
        parent = tree.roots[0]
        assert len(parent.children) == 1
        assert parent.children[0].title == "Child"

    def test_parent_set_correctly(self):
        tree = HeadingTree.build("# Parent\n## Child")
        child = tree.roots[0].children[0]
        assert child.parent is tree.roots[0]

    def test_sibling_h2s(self):
        tree = HeadingTree.build("# Root\n## A\n## B")
        assert len(tree.roots[0].children) == 2

    def test_three_level_nesting(self):
        tree = _simple_tree()
        root = tree.roots[0]
        child_a = root.children[0]
        assert len(child_a.children) == 2
        assert child_a.children[0].title == "Grandchild A1"

    def test_multiple_roots_with_children(self):
        text = "# R1\n## R1-A\n# R2\n## R2-A"
        tree = HeadingTree.build(text)
        assert len(tree.roots) == 2
        assert len(tree.roots[0].children) == 1
        assert len(tree.roots[1].children) == 1

    def test_h2_becomes_root_without_h1(self):
        tree = HeadingTree.build("## Top\n### Below")
        assert len(tree.roots) == 1
        assert tree.roots[0].level == 2
        assert tree.roots[0].children[0].level == 3


# ---------------------------------------------------------------------------
# TestHeadingTreeBuildSkipLevels
# ---------------------------------------------------------------------------

class TestHeadingTreeBuildSkipLevels:
    def test_h1_then_h3_skipping_h2(self):
        tree = HeadingTree.build("# Root\n### Deep")
        root = tree.roots[0]
        assert len(root.children) == 1
        assert root.children[0].level == 3

    def test_h1_h3_h2_restructure(self):
        # After h3 under h1, an h2 should become sibling of... nothing deeper
        tree = HeadingTree.build("# Root\n### Deep\n## Back")
        root = tree.roots[0]
        # Both ### and ## are children of # Root
        assert len(root.children) == 2
        assert root.children[0].level == 3
        assert root.children[1].level == 2

    def test_h1_h4_parent_is_h1(self):
        tree = HeadingTree.build("# Root\n#### VeryDeep")
        assert tree.roots[0].children[0].level == 4
        assert tree.roots[0].children[0].parent.level == 1


# ---------------------------------------------------------------------------
# TestHeadingTreeFlat
# ---------------------------------------------------------------------------

class TestHeadingTreeFlat:
    def test_flat_document_order(self):
        tree = _simple_tree()
        titles = [n.title for n in tree.flat()]
        assert titles == [
            "Root", "Child A", "Grandchild A1", "Grandchild A2",
            "Child B", "Grandchild B1",
        ]

    def test_flat_empty_tree(self):
        tree = HeadingTree.build("no headings here")
        assert tree.flat() == []

    def test_flat_single_heading(self):
        tree = HeadingTree.build("# Only")
        assert len(tree.flat()) == 1

    def test_flat_line_num_order(self):
        tree = _simple_tree()
        line_nums = [n.line_num for n in tree.flat()]
        assert line_nums == sorted(line_nums)


# ---------------------------------------------------------------------------
# TestHeadingTreeFind
# ---------------------------------------------------------------------------

class TestHeadingTreeFind:
    def test_find_existing(self):
        tree = _simple_tree()
        node = tree.find("Child A")
        assert node is not None
        assert node.title == "Child A"

    def test_find_case_insensitive(self):
        tree = _simple_tree()
        assert tree.find("child a") is not None
        assert tree.find("CHILD A") is not None
        assert tree.find("cHiLd A") is not None

    def test_find_not_found_returns_none(self):
        tree = _simple_tree()
        assert tree.find("Nonexistent") is None

    def test_find_all_multiple_matches(self):
        text = "# Section\n## Notes\n# Other\n## Notes"
        tree = HeadingTree.build(text)
        results = tree.find_all("notes")
        assert len(results) == 2

    def test_find_all_no_match_empty_list(self):
        tree = _simple_tree()
        assert tree.find_all("XYZ") == []

    def test_find_returns_first_match(self):
        text = "# Section\n## Notes\n# Other\n## Notes"
        tree = HeadingTree.build(text)
        node = tree.find("Notes")
        assert node.line_num == 2  # first occurrence


# ---------------------------------------------------------------------------
# TestHeadingTreeByLevel
# ---------------------------------------------------------------------------

class TestHeadingTreeByLevel:
    def test_by_level_h1(self):
        tree = _simple_tree()
        h1s = tree.by_level(1)
        assert len(h1s) == 1
        assert h1s[0].title == "Root"

    def test_by_level_h2(self):
        tree = _simple_tree()
        h2s = tree.by_level(2)
        assert len(h2s) == 2
        assert {n.title for n in h2s} == {"Child A", "Child B"}

    def test_by_level_h3(self):
        tree = _simple_tree()
        h3s = tree.by_level(3)
        assert len(h3s) == 3

    def test_by_level_nonexistent(self):
        tree = _simple_tree()
        assert tree.by_level(6) == []


# ---------------------------------------------------------------------------
# TestHeadingTreeMaxDepth
# ---------------------------------------------------------------------------

class TestHeadingTreeMaxDepth:
    def test_max_depth_empty(self):
        tree = HeadingTree.build("")
        assert tree.max_depth == 0

    def test_max_depth_single_h1(self):
        tree = HeadingTree.build("# Only")
        assert tree.max_depth == 1

    def test_max_depth_three_levels(self):
        tree = _simple_tree()
        assert tree.max_depth == 3

    def test_max_depth_h2_only(self):
        tree = HeadingTree.build("## A\n## B\n## C")
        assert tree.max_depth == 2

    def test_max_depth_all_six_levels(self):
        text = "\n".join(f"{'#' * i} H{i}" for i in range(1, 7))
        tree = HeadingTree.build(text)
        assert tree.max_depth == 6


# ---------------------------------------------------------------------------
# TestToOutline
# ---------------------------------------------------------------------------

class TestToOutline:
    def test_outline_basic_indentation(self):
        tree = HeadingTree.build("# Root\n## Child")
        outline = tree.to_outline()
        lines = outline.splitlines()
        assert lines[0] == "Root"
        assert lines[1] == "  Child"

    def test_outline_three_levels(self):
        tree = HeadingTree.build("# R\n## C\n### G")
        lines = tree.to_outline().splitlines()
        assert lines[0] == "R"
        assert lines[1] == "  C"
        assert lines[2] == "    G"

    def test_outline_custom_indent(self):
        tree = HeadingTree.build("# R\n## C")
        lines = tree.to_outline(indent="\t").splitlines()
        assert lines[1] == "\tC"

    def test_outline_empty_tree(self):
        tree = HeadingTree.build("no headings")
        assert tree.to_outline() == ""

    def test_outline_contains_all_titles(self):
        tree = _simple_tree()
        outline = tree.to_outline()
        for title in ["Root", "Child A", "Grandchild A1", "Child B"]:
            assert title in outline


# ---------------------------------------------------------------------------
# TestToToc
# ---------------------------------------------------------------------------

class TestToToc:
    def test_toc_basic_link_format(self):
        tree = HeadingTree.build("# Introduction")
        toc = tree.to_toc()
        assert "- [Introduction](#introduction)" in toc

    def test_toc_max_level_filters(self):
        tree = _simple_tree()
        toc = tree.to_toc(max_level=2)
        assert "Grandchild A1" not in toc
        assert "Child A" in toc

    def test_toc_max_level_1(self):
        tree = _simple_tree()
        toc = tree.to_toc(max_level=1)
        lines = [l.strip() for l in toc.splitlines() if l.strip()]
        assert len(lines) == 1
        assert "Root" in lines[0]

    def test_toc_default_max_level_3(self):
        tree = _simple_tree()
        toc = tree.to_toc()
        assert "Grandchild A1" in toc

    def test_toc_indentation_reflects_depth(self):
        tree = HeadingTree.build("# Root\n## Child\n### Grandchild")
        lines = tree.to_toc().splitlines()
        # Root at depth 0 → no indent
        assert lines[0].startswith("- ")
        # Child at depth 1 → two spaces
        assert lines[1].startswith("  - ")
        # Grandchild at depth 2 → four spaces
        assert lines[2].startswith("    - ")

    def test_toc_slug_in_link(self):
        tree = HeadingTree.build("# My Section Title")
        toc = tree.to_toc()
        assert "#my-section-title" in toc

    def test_toc_empty_tree_returns_empty_string(self):
        tree = HeadingTree.build("plain text")
        assert tree.to_toc() == ""

    def test_toc_max_level_higher_than_present(self):
        tree = HeadingTree.build("# Only H1s\n# Another")
        toc = tree.to_toc(max_level=6)
        assert toc.count("- [") == 2


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_text(self):
        tree = HeadingTree.build("")
        assert tree.roots == []
        assert tree.flat() == []
        assert tree.max_depth == 0
        assert tree.to_outline() == ""
        assert tree.to_toc() == ""

    def test_no_headings_in_text(self):
        tree = HeadingTree.build("Just some text.\nAnother paragraph.")
        assert tree.roots == []

    def test_single_heading(self):
        tree = HeadingTree.build("# Solo")
        assert len(tree.flat()) == 1
        node = tree.flat()[0]
        assert node.title == "Solo"
        assert node.is_leaf
        assert node.parent is None
        assert node.ancestors() == []
        assert node.descendants() == []

    def test_all_same_level(self):
        tree = HeadingTree.build("## A\n## B\n## C\n## D")
        assert len(tree.roots) == 4
        for r in tree.roots:
            assert r.is_leaf

    def test_heading_with_inline_code(self):
        tree = HeadingTree.build("# Use `build()` method")
        assert tree.roots[0].title == "Use `build()` method"

    def test_heading_level_6(self):
        tree = HeadingTree.build("###### Deepest")
        assert tree.roots[0].level == 6
        assert tree.roots[0].depth == 5

    def test_non_heading_hash_ignored(self):
        # '#' not at start of line or no space → not a heading
        tree = HeadingTree.build("text # not a heading\n# Real Heading")
        assert len(tree.roots) == 1
        assert tree.roots[0].title == "Real Heading"

    def test_flat_all_nodes_accounted(self):
        tree = _simple_tree()
        assert len(tree.flat()) == 6

    def test_roots_have_no_parent(self):
        tree = _simple_tree()
        for root in tree.roots:
            assert root.parent is None
