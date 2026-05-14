"""Tests for docstoolkit.doc_outline."""
from __future__ import annotations

import json

import pytest

from docstoolkit.doc_outline import DocOutline, OutlineNode, OutlineStats


# --------------------------------------------------------------------- fixtures

SIMPLE_DOC = """# Title

Some intro text.

## Section A

Body A.

## Section B

Body B.
"""

NESTED_DOC = """# Root

Intro.

## Chapter 1

C1 body.

### Section 1.1

S1.1 body.

### Section 1.2

S1.2 body.

## Chapter 2

C2 body.

### Section 2.1

S2.1 body.
"""

SKIP_LEVEL_DOC = """# Top

Intro.

### Deep one

Body deep.

## Mid

Body mid.

##### Very deep

Final body.
"""

NO_HEADINGS = """Just text.
Another line.
"""

EMPTY = ""

MULTI_ROOT_DOC = """# First

A.

# Second

B.

# Third

C.
"""

CODE_FENCE_DOC = """# Real Heading

```python
# Not a heading
def foo():
    pass
```

## Another Heading
"""


@pytest.fixture
def outline() -> DocOutline:
    return DocOutline()


# ---------------------------------------------------------------- OutlineNode


class TestOutlineNode:
    def test_create_minimal(self) -> None:
        n = OutlineNode(level=1, title="X", line_num=1, char_offset=0)
        assert n.level == 1
        assert n.title == "X"
        assert n.line_num == 1
        assert n.char_offset == 0
        assert n.section_length == 0
        assert n.children == []
        assert n.parent is None

    def test_default_children_independent(self) -> None:
        a = OutlineNode(level=1, title="A", line_num=1, char_offset=0)
        b = OutlineNode(level=1, title="B", line_num=2, char_offset=10)
        a.children.append(OutlineNode(level=2, title="x", line_num=3, char_offset=20))
        assert a.children != b.children

    def test_parent_field(self) -> None:
        p = OutlineNode(level=1, title="P", line_num=1, char_offset=0)
        c = OutlineNode(level=2, title="C", line_num=2, char_offset=10, parent=p)
        assert c.parent is p

    def test_section_length_default(self) -> None:
        n = OutlineNode(level=1, title="X", line_num=1, char_offset=0)
        assert n.section_length == 0


# --------------------------------------------------------------- OutlineStats


class TestOutlineStats:
    def test_create_full(self) -> None:
        node = OutlineNode(level=1, title="x", line_num=1, char_offset=0)
        s = OutlineStats(
            total_nodes=5,
            by_level={1: 2, 2: 3},
            max_depth=2,
            avg_section_length=100.5,
            largest_section=node,
            smallest_section=node,
        )
        assert s.total_nodes == 5
        assert s.by_level == {1: 2, 2: 3}
        assert s.max_depth == 2
        assert s.avg_section_length == 100.5
        assert s.largest_section is node
        assert s.smallest_section is node

    def test_empty_stats(self) -> None:
        s = OutlineStats(
            total_nodes=0,
            by_level={},
            max_depth=0,
            avg_section_length=0.0,
            largest_section=None,
            smallest_section=None,
        )
        assert s.total_nodes == 0
        assert s.largest_section is None


# ---------------------------------------------------------------------- build


class TestBuild:
    def test_simple_doc_returns_one_root(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert len(roots) == 1
        assert roots[0].title == "Title"
        assert roots[0].level == 1

    def test_simple_doc_h2_children(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert len(roots[0].children) == 2
        assert [c.title for c in roots[0].children] == ["Section A", "Section B"]

    def test_children_have_parent_set(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        for child in roots[0].children:
            assert child.parent is roots[0]

    def test_root_has_no_parent(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert roots[0].parent is None

    def test_line_numbers_are_one_based(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert roots[0].line_num == 1
        # "## Section A" is on line 5
        assert roots[0].children[0].line_num == 5

    def test_char_offsets_are_correct(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert roots[0].char_offset == 0
        first_child = roots[0].children[0]
        # The offset should match the position of "## Section A" in the doc.
        assert SIMPLE_DOC[first_child.char_offset:].startswith("## Section A")

    def test_multi_root(self, outline: DocOutline) -> None:
        roots = outline.build(MULTI_ROOT_DOC)
        assert len(roots) == 3
        assert [r.title for r in roots] == ["First", "Second", "Third"]
        for r in roots:
            assert r.parent is None


# ----------------------------------------------------------------- build_flat


class TestBuildFlat:
    def test_returns_all_nodes(self, outline: DocOutline) -> None:
        flat = outline.build_flat(NESTED_DOC)
        assert len(flat) == 6  # 1 root + 2 chapters + 3 sections

    def test_document_order(self, outline: DocOutline) -> None:
        flat = outline.build_flat(NESTED_DOC)
        titles = [n.title for n in flat]
        assert titles == [
            "Root",
            "Chapter 1",
            "Section 1.1",
            "Section 1.2",
            "Chapter 2",
            "Section 2.1",
        ]

    def test_empty_doc(self, outline: DocOutline) -> None:
        assert outline.build_flat(EMPTY) == []

    def test_no_headings(self, outline: DocOutline) -> None:
        assert outline.build_flat(NO_HEADINGS) == []


# --------------------------------------------------------------- BuildNested


class TestBuildNested:
    def test_nested_structure(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        assert len(roots) == 1
        root = roots[0]
        assert len(root.children) == 2
        assert root.children[0].title == "Chapter 1"
        assert len(root.children[0].children) == 2
        assert root.children[0].children[0].title == "Section 1.1"

    def test_parents_set_recursively(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        ch1 = roots[0].children[0]
        s11 = ch1.children[0]
        assert s11.parent is ch1
        assert ch1.parent is roots[0]
        assert roots[0].parent is None

    def test_levels_preserved(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        ch1 = roots[0].children[0]
        s11 = ch1.children[0]
        assert roots[0].level == 1
        assert ch1.level == 2
        assert s11.level == 3


# ------------------------------------------------------------ BuildSkipLevels


class TestBuildSkipLevels:
    def test_h1_then_h3(self, outline: DocOutline) -> None:
        roots = outline.build(SKIP_LEVEL_DOC)
        # Top is h1; Deep one is h3 attached as child of Top.
        assert roots[0].title == "Top"
        assert roots[0].children[0].title == "Deep one"
        assert roots[0].children[0].level == 3

    def test_h3_then_h2_breaks_out(self, outline: DocOutline) -> None:
        roots = outline.build(SKIP_LEVEL_DOC)
        # After "Deep one" (h3), "Mid" is h2: should sit at top under Top.
        top = roots[0]
        titles = [c.title for c in top.children]
        assert "Mid" in titles
        # "Mid" is a child of "Top", not of "Deep one"
        mid = next(c for c in top.children if c.title == "Mid")
        assert mid.parent is top

    def test_h5_after_h2(self, outline: DocOutline) -> None:
        roots = outline.build(SKIP_LEVEL_DOC)
        mid = next(c for c in roots[0].children if c.title == "Mid")
        # Very deep (h5) should be nested under Mid (h2).
        assert mid.children[0].title == "Very deep"
        assert mid.children[0].level == 5


# ------------------------------------------------------------ SectionLength


class TestSectionLength:
    def test_last_section_extends_to_end(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        last = roots[0].children[-1]
        # Section length should reach end of doc.
        assert last.char_offset + last.section_length == len(SIMPLE_DOC)

    def test_section_length_positive(self, outline: DocOutline) -> None:
        flat = DocOutline().build_flat(NESTED_DOC)
        for n in flat:
            assert n.section_length > 0

    def test_section_includes_subsections(self, outline: DocOutline) -> None:
        # Chapter 1 (h2) section_length should include both subsections.
        flat = outline.build_flat(NESTED_DOC)
        ch1 = next(n for n in flat if n.title == "Chapter 1")
        s12 = next(n for n in flat if n.title == "Section 1.2")
        # Chapter 1 section extends until Chapter 2 (the next h2 or shallower).
        ch2 = next(n for n in flat if n.title == "Chapter 2")
        assert ch1.char_offset + ch1.section_length == ch2.char_offset
        # And it must encompass section 1.2's char_offset.
        assert s12.char_offset > ch1.char_offset
        assert s12.char_offset < ch1.char_offset + ch1.section_length

    def test_root_section_length_is_total(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert roots[0].section_length == len(SIMPLE_DOC)


# ---------------------------------------------------------------- FindNode


class TestFindNode:
    def test_find_by_title(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        node = outline.find_node(roots, "Chapter 1")
        assert node is not None
        assert node.title == "Chapter 1"

    def test_find_case_insensitive(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        node = outline.find_node(roots, "CHAPTER 1")
        assert node is not None
        assert node.title == "Chapter 1"

    def test_find_with_level_filter(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        node = outline.find_node(roots, "Section 1.1", level=3)
        assert node is not None
        assert node.level == 3

    def test_find_wrong_level_returns_none(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        assert outline.find_node(roots, "Section 1.1", level=2) is None

    def test_find_missing(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        assert outline.find_node(roots, "Nonexistent") is None

    def test_find_in_empty(self, outline: DocOutline) -> None:
        assert outline.find_node([], "Anything") is None


# -------------------------------------------------------------- NodesAtLevel


class TestNodesAtLevel:
    def test_level_one(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        h1s = outline.nodes_at_level(roots, 1)
        assert [n.title for n in h1s] == ["Root"]

    def test_level_two(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        h2s = outline.nodes_at_level(roots, 2)
        assert [n.title for n in h2s] == ["Chapter 1", "Chapter 2"]

    def test_level_three(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        h3s = outline.nodes_at_level(roots, 3)
        assert len(h3s) == 3

    def test_level_missing(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert outline.nodes_at_level(roots, 4) == []


# ---------------------------------------------------------------- Descendants


class TestDescendants:
    def test_root_descendants(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        d = outline.descendants(roots[0])
        assert len(d) == 5

    def test_descendants_order(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        d = outline.descendants(roots[0])
        titles = [n.title for n in d]
        assert titles == [
            "Chapter 1",
            "Section 1.1",
            "Section 1.2",
            "Chapter 2",
            "Section 2.1",
        ]

    def test_leaf_has_no_descendants(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        leaf = outline.find_node(roots, "Section 1.1")
        assert outline.descendants(leaf) == []

    def test_chapter_descendants(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        ch1 = outline.find_node(roots, "Chapter 1")
        d = outline.descendants(ch1)
        assert [n.title for n in d] == ["Section 1.1", "Section 1.2"]


# ------------------------------------------------------------------ Ancestors


class TestAncestors:
    def test_root_has_no_ancestors(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        assert outline.ancestors(roots[0]) == []

    def test_deep_node_ancestors(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        s11 = outline.find_node(roots, "Section 1.1")
        anc = outline.ancestors(s11)
        assert [n.title for n in anc] == ["Chapter 1", "Root"]

    def test_chapter_has_one_ancestor(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        ch1 = outline.find_node(roots, "Chapter 1")
        assert [n.title for n in outline.ancestors(ch1)] == ["Root"]


# ----------------------------------------------------------------------- ToToc


class TestToToc:
    def test_basic_toc(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        toc = outline.to_toc(roots)
        assert "- Title" in toc
        assert "- Section A" in toc
        assert "- Section B" in toc

    def test_toc_indented(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        toc = outline.to_toc(roots)
        lines = toc.split("\n")
        # H1 has no indent, H2 has 2 spaces, H3 has 4 spaces.
        assert lines[0] == "- Root"
        assert lines[1] == "  - Chapter 1"
        assert lines[2] == "    - Section 1.1"

    def test_toc_max_level(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        toc = outline.to_toc(roots, max_level=2)
        assert "Section 1.1" not in toc
        assert "Chapter 1" in toc

    def test_toc_with_lines(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        toc = outline.to_toc(roots, with_lines=True)
        assert "(L1)" in toc
        assert "(L5)" in toc


# -------------------------------------------------------------------- ToMarkdown


class TestToMarkdown:
    def test_default_indent(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        md = outline.to_markdown(roots)
        assert md.startswith("- Root")
        assert "  - Chapter 1" in md
        assert "    - Section 1.1" in md

    def test_custom_indent(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        md = outline.to_markdown(roots, indent="\t")
        assert "\t- Chapter 1" in md
        assert "\t\t- Section 1.1" in md

    def test_max_level_limits(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        md = outline.to_markdown(roots, max_level=2)
        assert "Section 1.1" not in md

    def test_empty_roots(self, outline: DocOutline) -> None:
        assert outline.to_markdown([]) == ""


# ----------------------------------------------------------------------- ToDict


class TestToDict:
    def test_returns_list(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        d = outline.to_dict(roots)
        assert isinstance(d, list)
        assert d[0]["title"] == "Title"

    def test_has_required_keys(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        d = outline.to_dict(roots)
        for key in ("level", "title", "line_num", "char_offset", "section_length", "children"):
            assert key in d[0]

    def test_children_recursive(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        d = outline.to_dict(roots)
        assert len(d[0]["children"]) == 2
        assert len(d[0]["children"][0]["children"]) == 2
        assert d[0]["children"][0]["children"][0]["title"] == "Section 1.1"

    def test_empty(self, outline: DocOutline) -> None:
        assert outline.to_dict([]) == []


# ----------------------------------------------------------------------- ToJson


class TestToJson:
    def test_returns_string(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert isinstance(outline.to_json(roots), str)

    def test_parses_back(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        parsed = json.loads(outline.to_json(roots))
        assert parsed[0]["title"] == "Root"
        assert parsed[0]["children"][0]["title"] == "Chapter 1"

    def test_empty_json(self, outline: DocOutline) -> None:
        assert json.loads(outline.to_json([])) == []


# ----------------------------------------------------------------------- Stats


class TestStats:
    def test_total_nodes(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        s = outline.stats(roots)
        assert s.total_nodes == 6

    def test_by_level(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        s = outline.stats(roots)
        assert s.by_level == {1: 1, 2: 2, 3: 3}

    def test_max_depth(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        s = outline.stats(roots)
        assert s.max_depth == 3

    def test_avg_section_length_positive(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        s = outline.stats(roots)
        assert s.avg_section_length > 0

    def test_largest_and_smallest(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        s = outline.stats(roots)
        assert s.largest_section is not None
        assert s.smallest_section is not None
        # Root (whole doc) should be the largest.
        assert s.largest_section.title == "Root"

    def test_empty_doc_stats(self, outline: DocOutline) -> None:
        s = outline.stats([])
        assert s.total_nodes == 0
        assert s.by_level == {}
        assert s.max_depth == 0
        assert s.avg_section_length == 0.0
        assert s.largest_section is None
        assert s.smallest_section is None


# -------------------------------------------------------------------- MaxDepth


class TestMaxDepth:
    def test_single_node(self, outline: DocOutline) -> None:
        roots = outline.build("# Only")
        assert outline.max_depth(roots) == 1

    def test_three_levels(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        assert outline.max_depth(roots) == 3

    def test_empty(self, outline: DocOutline) -> None:
        assert outline.max_depth([]) == 0

    def test_flat_multi_root(self, outline: DocOutline) -> None:
        roots = outline.build(MULTI_ROOT_DOC)
        assert outline.max_depth(roots) == 1


# ------------------------------------------------------------------ CountNodes


class TestCountNodes:
    def test_count_simple(self, outline: DocOutline) -> None:
        roots = outline.build(SIMPLE_DOC)
        assert outline.count_nodes(roots) == 3

    def test_count_nested(self, outline: DocOutline) -> None:
        roots = outline.build(NESTED_DOC)
        assert outline.count_nodes(roots) == 6

    def test_count_empty(self, outline: DocOutline) -> None:
        assert outline.count_nodes([]) == 0

    def test_count_multi_root(self, outline: DocOutline) -> None:
        roots = outline.build(MULTI_ROOT_DOC)
        assert outline.count_nodes(roots) == 3


# ----------------------------------------------------------------- EdgeCases


class TestEdgeCases:
    def test_empty_doc(self, outline: DocOutline) -> None:
        assert outline.build(EMPTY) == []

    def test_no_headings(self, outline: DocOutline) -> None:
        assert outline.build(NO_HEADINGS) == []

    def test_only_whitespace(self, outline: DocOutline) -> None:
        assert outline.build("   \n\n  \n") == []

    def test_heading_with_trailing_hashes(self, outline: DocOutline) -> None:
        roots = outline.build("# Title ##\n")
        assert roots[0].title == "Title"

    def test_h6_max_level(self, outline: DocOutline) -> None:
        doc = "# A\n###### Deep\n"
        roots = outline.build(doc)
        assert roots[0].children[0].level == 6

    def test_seven_hashes_not_heading(self, outline: DocOutline) -> None:
        # ####### exceeds max heading level — should not be parsed.
        doc = "# A\n####### Not a heading\n"
        roots = outline.build(doc)
        assert outline.count_nodes(roots) == 1

    def test_skip_fenced_code(self, outline: DocOutline) -> None:
        roots = outline.build(CODE_FENCE_DOC)
        # "# Not a heading" inside a code fence must be ignored.
        titles = [n.title for n in outline.build_flat(CODE_FENCE_DOC)]
        assert "Not a heading" not in titles
        assert "Real Heading" in titles
        assert "Another Heading" in titles

    def test_heading_without_space_ignored(self, outline: DocOutline) -> None:
        # "#NoSpace" is not a valid ATX heading.
        roots = outline.build("#NoSpace\n# Valid\n")
        assert len(roots) == 1
        assert roots[0].title == "Valid"

    def test_unicode_titles(self, outline: DocOutline) -> None:
        doc = "# Заголовок\n## Раздел\n"
        roots = outline.build(doc)
        assert roots[0].title == "Заголовок"
        assert roots[0].children[0].title == "Раздел"

    def test_json_roundtrip_unicode(self, outline: DocOutline) -> None:
        roots = outline.build("# Заголовок\n")
        parsed = json.loads(outline.to_json(roots))
        assert parsed[0]["title"] == "Заголовок"
