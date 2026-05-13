"""Tests for doc_breadcrumb."""
from __future__ import annotations

import pytest

from docstoolkit.doc_breadcrumb import (
    Breadcrumb,
    BreadcrumbSeparator,
    Crumb,
    DocBreadcrumb,
)


# ---------------------------------------------------------------------------
class TestBreadcrumbSeparator:
    def test_slash_value(self):
        assert BreadcrumbSeparator.SLASH.value == " / "

    def test_arrow_value(self):
        assert BreadcrumbSeparator.ARROW.value == " → "

    def test_chevron_value(self):
        assert BreadcrumbSeparator.CHEVRON.value == " > "

    def test_pipe_value(self):
        assert BreadcrumbSeparator.PIPE.value == " | "

    def test_all_four_separators_exist(self):
        names = {s.name for s in BreadcrumbSeparator}
        assert {"SLASH", "ARROW", "CHEVRON", "PIPE"} <= names


# ---------------------------------------------------------------------------
class TestCrumb:
    def test_create_minimal(self):
        c = Crumb(doc_id="a", title="A")
        assert c.doc_id == "a"
        assert c.title == "A"
        assert c.is_root is False
        assert c.is_current is False

    def test_root_flag(self):
        c = Crumb(doc_id="r", title="Root", is_root=True)
        assert c.is_root is True

    def test_current_flag(self):
        c = Crumb(doc_id="x", title="X", is_current=True)
        assert c.is_current is True


# ---------------------------------------------------------------------------
class TestBreadcrumb:
    def test_depth_empty(self):
        b = Breadcrumb(crumbs=[], target_doc_id="x")
        assert b.depth == 0

    def test_depth_with_crumbs(self):
        b = Breadcrumb(
            crumbs=[Crumb("a", "A"), Crumb("b", "B"), Crumb("c", "C")],
            target_doc_id="c",
        )
        assert b.depth == 3

    def test_to_string_default_slash(self):
        b = Breadcrumb(crumbs=[Crumb("a", "A"), Crumb("b", "B")], target_doc_id="b")
        assert b.to_string() == "A / B"

    def test_to_markdown_links_and_current(self):
        b = Breadcrumb(
            crumbs=[
                Crumb("a", "A", is_root=True),
                Crumb("b", "B", is_current=True),
            ],
            target_doc_id="b",
        )
        md = b.to_markdown()
        assert "[A](#a)" in md
        assert "B" in md
        assert "[B]" not in md


# ---------------------------------------------------------------------------
class TestSetParent:
    def test_set_parent_basic(self):
        d = DocBreadcrumb()
        assert d.set_parent("child", "parent") is True
        assert d.ancestors("child") == ["parent"]

    def test_set_parent_none_makes_root(self):
        d = DocBreadcrumb()
        d.set_parent("a", "b")
        d.set_parent("a", None)
        assert "a" in d.roots()

    def test_self_parent_rejected(self):
        d = DocBreadcrumb()
        assert d.set_parent("a", "a") is False

    def test_registers_new_doc(self):
        d = DocBreadcrumb()
        d.set_parent("x", "y")
        assert "x" in d.path_to("x")


# ---------------------------------------------------------------------------
class TestUnsetParent:
    def test_unset_existing(self):
        d = DocBreadcrumb()
        d.set_parent("a", "b")
        assert d.unset_parent("a") is True
        assert "a" in d.roots()

    def test_unset_unknown(self):
        d = DocBreadcrumb()
        assert d.unset_parent("ghost") is False


# ---------------------------------------------------------------------------
class TestRegisterTitle:
    def test_register_title_basic(self):
        d = DocBreadcrumb()
        d.register_title("x", "Hello")
        bc = d.breadcrumb("x")
        assert bc is not None
        assert bc.crumbs[0].title == "Hello"

    def test_title_defaults_to_id(self):
        d = DocBreadcrumb()
        d.set_parent("x", None)
        bc = d.breadcrumb("x")
        assert bc.crumbs[0].title == "x"


# ---------------------------------------------------------------------------
class TestAddAlias:
    def test_add_alias_basic(self):
        d = DocBreadcrumb()
        d.register_title("canon", "Canon")
        assert d.add_alias("alias", "canon") is True
        assert d.resolve_alias("alias") == "canon"

    def test_alias_equal_canonical_rejected(self):
        d = DocBreadcrumb()
        assert d.add_alias("x", "x") is False


# ---------------------------------------------------------------------------
class TestBreadcrumbBasic:
    def test_unknown_doc_returns_none(self):
        d = DocBreadcrumb()
        assert d.breadcrumb("ghost") is None

    def test_root_only(self):
        d = DocBreadcrumb()
        d.register_title("r", "Root")
        bc = d.breadcrumb("r")
        assert bc.depth == 1
        assert bc.crumbs[0].is_root is True
        assert bc.crumbs[0].is_current is True

    def test_two_levels(self):
        d = DocBreadcrumb()
        d.register_title("r", "Root")
        d.register_title("c", "Child")
        d.set_parent("c", "r")
        bc = d.breadcrumb("c")
        assert bc.depth == 2
        assert bc.crumbs[0].doc_id == "r"
        assert bc.crumbs[1].doc_id == "c"
        assert bc.crumbs[1].is_current is True


# ---------------------------------------------------------------------------
class TestPathTo:
    def test_path_simple(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        d.set_parent("c", "b")
        assert d.path_to("c") == ["a", "b", "c"]

    def test_path_root(self):
        d = DocBreadcrumb()
        d.register_title("r", "R")
        assert d.path_to("r") == ["r"]

    def test_path_unknown_returns_empty(self):
        d = DocBreadcrumb()
        assert d.path_to("ghost") == []


# ---------------------------------------------------------------------------
class TestAncestors:
    def test_ancestors_chain(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        d.set_parent("c", "b")
        assert d.ancestors("c") == ["b", "a"]

    def test_ancestors_root(self):
        d = DocBreadcrumb()
        d.register_title("r", "r")
        assert d.ancestors("r") == []

    def test_ancestors_unknown(self):
        d = DocBreadcrumb()
        assert d.ancestors("nope") == []


# ---------------------------------------------------------------------------
class TestRoots:
    def test_multiple_roots(self):
        d = DocBreadcrumb()
        d.register_title("r1", "R1")
        d.register_title("r2", "R2")
        d.set_parent("c", "r1")
        rs = set(d.roots())
        assert {"r1", "r2"} <= rs
        assert "c" not in rs

    def test_no_roots_when_empty(self):
        d = DocBreadcrumb()
        assert d.roots() == []


# ---------------------------------------------------------------------------
class TestChildren:
    def test_children_basic(self):
        d = DocBreadcrumb()
        d.set_parent("a", "r")
        d.set_parent("b", "r")
        assert set(d.children("r")) == {"a", "b"}

    def test_children_none(self):
        d = DocBreadcrumb()
        d.register_title("x", "X")
        assert d.children("x") == []


# ---------------------------------------------------------------------------
class TestDescendants:
    def test_descendants_tree(self):
        d = DocBreadcrumb()
        d.set_parent("a", "r")
        d.set_parent("b", "r")
        d.set_parent("aa", "a")
        d.set_parent("ab", "a")
        assert set(d.descendants("r")) == {"a", "b", "aa", "ab"}

    def test_descendants_leaf(self):
        d = DocBreadcrumb()
        d.set_parent("a", "r")
        assert d.descendants("a") == []


# ---------------------------------------------------------------------------
class TestDepth:
    def test_root_depth_zero(self):
        d = DocBreadcrumb()
        d.register_title("r", "R")
        assert d.depth("r") == 0

    def test_child_depth_one(self):
        d = DocBreadcrumb()
        d.set_parent("c", "r")
        assert d.depth("c") == 1

    def test_deep_chain(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        d.set_parent("c", "b")
        d.set_parent("d", "c")
        assert d.depth("d") == 3

    def test_unknown_returns_negative(self):
        d = DocBreadcrumb()
        assert d.depth("ghost") == -1


# ---------------------------------------------------------------------------
class TestIsAncestorOf:
    def test_true_case(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        d.set_parent("c", "b")
        assert d.is_ancestor_of("a", "c") is True

    def test_false_case_sibling(self):
        d = DocBreadcrumb()
        d.set_parent("a", "r")
        d.set_parent("b", "r")
        assert d.is_ancestor_of("a", "b") is False

    def test_self_not_ancestor(self):
        d = DocBreadcrumb()
        d.register_title("x", "X")
        assert d.is_ancestor_of("x", "x") is False


# ---------------------------------------------------------------------------
class TestBreadcrumbsForAll:
    def test_returns_all_docs(self):
        d = DocBreadcrumb()
        d.register_title("r", "R")
        d.register_title("c", "C")
        d.set_parent("c", "r")
        all_bc = d.breadcrumbs_for_all()
        assert "r" in all_bc
        assert "c" in all_bc
        assert all_bc["c"].depth == 2

    def test_empty_when_no_docs(self):
        d = DocBreadcrumb()
        assert d.breadcrumbs_for_all() == {}


# ---------------------------------------------------------------------------
class TestResolveAlias:
    def test_known_alias(self):
        d = DocBreadcrumb()
        d.register_title("canon", "Canon")
        d.add_alias("a1", "canon")
        assert d.resolve_alias("a1") == "canon"

    def test_unknown_returns_input(self):
        d = DocBreadcrumb()
        assert d.resolve_alias("zzz") == "zzz"

    def test_breadcrumb_via_alias(self):
        d = DocBreadcrumb()
        d.register_title("r", "Root")
        d.add_alias("home", "r")
        bc = d.breadcrumb("home")
        assert bc is not None
        assert bc.target_doc_id == "r"


# ---------------------------------------------------------------------------
class TestSetSeparator:
    def test_default_change(self):
        d = DocBreadcrumb()
        d.set_separator(BreadcrumbSeparator.ARROW)
        # No direct getter — we verify by no exception and persistent state via attr
        assert d._default_separator == BreadcrumbSeparator.ARROW


# ---------------------------------------------------------------------------
class TestSeparatorOutput:
    def _make(self):
        d = DocBreadcrumb()
        d.register_title("a", "A")
        d.register_title("b", "B")
        d.set_parent("b", "a")
        return d.breadcrumb("b")

    def test_slash(self):
        assert self._make().to_string(BreadcrumbSeparator.SLASH) == "A / B"

    def test_arrow(self):
        assert self._make().to_string(BreadcrumbSeparator.ARROW) == "A → B"

    def test_chevron(self):
        assert self._make().to_string(BreadcrumbSeparator.CHEVRON) == "A > B"

    def test_pipe(self):
        assert self._make().to_string(BreadcrumbSeparator.PIPE) == "A | B"


# ---------------------------------------------------------------------------
class TestMarkdownOutput:
    def test_markdown_three_levels(self):
        d = DocBreadcrumb()
        d.register_title("r", "Root")
        d.register_title("s", "Section")
        d.register_title("p", "Page")
        d.set_parent("s", "r")
        d.set_parent("p", "s")
        md = d.breadcrumb("p").to_markdown()
        assert "[Root](#r)" in md
        assert "[Section](#s)" in md
        assert "Page" in md
        assert "[Page]" not in md

    def test_markdown_root_is_current(self):
        d = DocBreadcrumb()
        d.register_title("r", "R")
        md = d.breadcrumb("r").to_markdown()
        assert md == "R"


# ---------------------------------------------------------------------------
class TestCycleDetection:
    def test_simple_cycle_rejected(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        # Now making a's parent = b would create cycle
        assert d.set_parent("a", "b") is False

    def test_deep_cycle_rejected(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        d.set_parent("c", "b")
        d.set_parent("d", "c")
        # Make a's parent = d → cycle a→...→d→a
        assert d.set_parent("a", "d") is False

    def test_no_false_positive(self):
        d = DocBreadcrumb()
        d.set_parent("b", "a")
        d.set_parent("c", "a")
        # Move c under b — not a cycle
        assert d.set_parent("c", "b") is True


# ---------------------------------------------------------------------------
class TestTotalDocs:
    def test_count_increases(self):
        d = DocBreadcrumb()
        assert d.total_docs == 0
        d.register_title("a", "A")
        assert d.total_docs == 1
        d.set_parent("b", "a")
        assert d.total_docs == 2

    def test_no_double_count(self):
        d = DocBreadcrumb()
        d.register_title("a", "A")
        d.set_parent("a", None)
        assert d.total_docs == 1


# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_empties(self):
        d = DocBreadcrumb()
        d.register_title("a", "A")
        d.set_parent("b", "a")
        d.add_alias("alias", "a")
        d.clear()
        assert d.total_docs == 0
        assert d.roots() == []
        assert d.resolve_alias("alias") == "alias"


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_breadcrumb_unknown(self):
        d = DocBreadcrumb()
        assert d.breadcrumb("nope") is None

    def test_children_unknown(self):
        d = DocBreadcrumb()
        assert d.children("nope") == []

    def test_descendants_unknown(self):
        d = DocBreadcrumb()
        assert d.descendants("nope") == []

    def test_path_to_unknown(self):
        d = DocBreadcrumb()
        assert d.path_to("nope") == []

    def test_unset_root_idempotent(self):
        d = DocBreadcrumb()
        d.register_title("r", "R")
        assert d.unset_parent("r") is True
        assert "r" in d.roots()

    def test_breadcrumb_target_id_set(self):
        d = DocBreadcrumb()
        d.register_title("x", "X")
        bc = d.breadcrumb("x")
        assert bc.target_doc_id == "x"

    def test_alias_can_be_overwritten(self):
        d = DocBreadcrumb()
        d.register_title("a", "A")
        d.register_title("b", "B")
        d.add_alias("x", "a")
        d.add_alias("x", "b")
        assert d.resolve_alias("x") == "b"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
