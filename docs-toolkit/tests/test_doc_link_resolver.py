"""Tests for docstoolkit.doc_link_resolver."""
from __future__ import annotations

import pytest

from docstoolkit.doc_link_resolver import (
    DocLinkResolver,
    LinkExtraction,
    LinkResolution,
    LinkStyle,
)


# ---------------------------------------------------------------- enums/data


class TestLinkStyle:
    def test_members_exist(self):
        assert LinkStyle.WIKI.value == "wiki"
        assert LinkStyle.MARKDOWN.value == "markdown"
        assert LinkStyle.ANCHOR.value == "anchor"
        assert LinkStyle.REFERENCE.value == "reference"

    def test_distinct(self):
        assert len({s.value for s in LinkStyle}) == 4


class TestLinkResolution:
    def test_required_fields(self):
        r = LinkResolution(
            original="[[Foo]]",
            target_doc_id="foo",
            anchor=None,
            is_resolved=True,
            style=LinkStyle.WIKI,
        )
        assert r.original == "[[Foo]]"
        assert r.target_doc_id == "foo"
        assert r.is_resolved is True
        assert r.error is None

    def test_with_error(self):
        r = LinkResolution(
            original="[[Bar]]",
            target_doc_id=None,
            anchor=None,
            is_resolved=False,
            style=LinkStyle.WIKI,
            error="missing",
        )
        assert r.is_resolved is False
        assert r.error == "missing"


class TestLinkExtraction:
    def test_default_lists(self):
        e = LinkExtraction(source_doc_id="x")
        assert e.source_doc_id == "x"
        assert e.links == []
        assert e.resolutions == []

    def test_attach_data(self):
        e = LinkExtraction(source_doc_id="x")
        e.links.append(("[[A]]", 0))
        assert len(e.links) == 1


# ---------------------------------------------------------------- register


class TestRegisterDoc:
    def test_simple(self):
        r = DocLinkResolver()
        assert r.register_doc("foo") is True
        assert r.total_docs == 1

    def test_with_title(self):
        r = DocLinkResolver()
        assert r.register_doc("foo", title="Foo Page") is True
        assert r.title_for("foo") == "Foo Page"

    def test_with_aliases(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo", aliases=["f", "foob"])
        assert "f" in r.aliases_for("foo")
        assert "foob" in r.aliases_for("foo")

    def test_duplicate(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.register_doc("foo") is False

    def test_empty_id_rejected(self):
        r = DocLinkResolver()
        assert r.register_doc("") is False

    def test_default_title_is_id(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.title_for("foo") == "foo"


class TestUnregisterDoc:
    def test_removes(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.unregister_doc("foo") is True
        assert r.total_docs == 0
        assert r.title_for("foo") is None

    def test_missing(self):
        r = DocLinkResolver()
        assert r.unregister_doc("ghost") is False

    def test_clears_title_index(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page", aliases=["fp"])
        r.unregister_doc("foo")
        assert r.id_for_title("Foo Page") is None
        assert r.id_for_title("fp") is None

    def test_drops_dependent_references(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_reference("home", "foo")
        r.unregister_doc("foo")
        assert r.resolve_reference("home") is None


class TestAddAlias:
    def test_add(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.add_alias("foo", "FooBar") is True
        assert r.id_for_title("foobar") == "foo"

    def test_unknown_doc(self):
        r = DocLinkResolver()
        assert r.add_alias("ghost", "x") is False

    def test_duplicate_alias(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.add_alias("foo", "x")
        assert r.add_alias("foo", "x") is False

    def test_empty_alias(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.add_alias("foo", "") is False


# ---------------------------------------------------------------- wiki


class TestResolveWiki:
    def test_by_title(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.resolve_wiki("Foo Page") == "foo"

    def test_full_brackets(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.resolve_wiki("[[Foo Page]]") == "foo"

    def test_with_display(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.resolve_wiki("[[Foo Page|click here]]") == "foo"

    def test_alias(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo", aliases=["F"])
        assert r.resolve_wiki("F") == "foo"

    def test_case_insensitive(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.resolve_wiki("foo page") == "foo"

    def test_unknown(self):
        r = DocLinkResolver()
        assert r.resolve_wiki("Nope") is None

    def test_empty(self):
        r = DocLinkResolver()
        assert r.resolve_wiki("") is None

    def test_wiki_with_anchor(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.resolve_wiki("Foo Page#section") == "foo"


# ---------------------------------------------------------------- markdown


class TestResolveMarkdown:
    def test_simple_md(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("foo.md") == "foo"

    def test_relative_parent(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("../foo.md") == "foo"

    def test_absolute(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("/foo.md") == "foo"

    def test_no_extension(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("foo") == "foo"

    def test_unknown(self):
        r = DocLinkResolver()
        assert r.resolve_markdown("ghost.md") is None

    def test_external(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("https://example.com") is None

    def test_anchor_only_uses_current(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("#intro", current_doc_id="foo") == "foo"

    def test_anchor_only_no_current(self):
        r = DocLinkResolver()
        assert r.resolve_markdown("#intro") is None

    def test_empty(self):
        r = DocLinkResolver()
        assert r.resolve_markdown("") is None

    def test_nested_path(self):
        r = DocLinkResolver()
        r.register_doc("guides/intro")
        assert r.resolve_markdown("guides/intro.md") == "guides/intro"

    def test_markdown_extension_variant(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_markdown("foo.markdown") == "foo"


# ---------------------------------------------------------------- anchor


class TestResolveAnchor:
    def test_current_doc(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_anchor("foo", "intro")
        assert r.resolve_anchor("#intro", current_doc_id="foo") == ("foo", "intro")

    def test_qualified(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        r.register_anchor("foo", "intro")
        assert r.resolve_anchor("foo#intro") == ("foo", "intro")

    def test_unknown_anchor(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_anchor("#missing", current_doc_id="foo") is None

    def test_no_current(self):
        r = DocLinkResolver()
        assert r.resolve_anchor("#intro") is None

    def test_empty(self):
        r = DocLinkResolver()
        assert r.resolve_anchor("") is None

    def test_no_hash(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.resolve_anchor("foo") is None

    def test_by_title(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        r.register_anchor("foo", "intro")
        assert r.resolve_anchor("Foo Page#intro") == ("foo", "intro")


# ---------------------------------------------------------------- reference


class TestResolveReference:
    def test_resolve(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_reference("home", "foo")
        assert r.resolve_reference("home") == "foo"

    def test_unknown(self):
        r = DocLinkResolver()
        assert r.resolve_reference("missing") is None

    def test_case_insensitive(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_reference("Home", "foo")
        assert r.resolve_reference("HOME") == "foo"

    def test_empty(self):
        r = DocLinkResolver()
        assert r.resolve_reference("") is None


class TestRegisterReference:
    def test_basic(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.register_reference("home", "foo") is True

    def test_unknown_doc(self):
        r = DocLinkResolver()
        assert r.register_reference("home", "ghost") is False

    def test_with_anchor(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_anchor("foo", "intro")
        assert r.register_reference("home", "foo", anchor="intro") is True

    def test_empty_name(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.register_reference("", "foo") is False


class TestRegisterAnchor:
    def test_basic(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.register_anchor("foo", "intro") is True

    def test_unknown_doc(self):
        r = DocLinkResolver()
        assert r.register_anchor("ghost", "intro") is False

    def test_empty_anchor(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.register_anchor("foo", "") is False

    def test_with_text(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        assert r.register_anchor("foo", "intro", anchor_text="Introduction") is True


# ---------------------------------------------------------------- extraction


class TestExtractLinks:
    def test_wiki_only(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        e = r.extract_links("see [[Foo]] for details")
        assert isinstance(e, LinkExtraction)
        assert len(e.resolutions) == 1
        assert e.resolutions[0].style == LinkStyle.WIKI
        assert e.resolutions[0].is_resolved

    def test_mixed_styles(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        r.register_doc("bar")
        r.register_reference("home", "foo")
        content = "see [[Foo]] and [doc](bar.md) and [label][home]"
        e = r.extract_links(content)
        styles = {res.style for res in e.resolutions}
        assert LinkStyle.WIKI in styles
        assert LinkStyle.MARKDOWN in styles
        assert LinkStyle.REFERENCE in styles

    def test_offsets(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        e = r.extract_links("A [[Foo]] B")
        assert e.links[0][1] == 2

    def test_empty_content(self):
        r = DocLinkResolver()
        e = r.extract_links("")
        assert e.resolutions == []

    def test_source_id(self):
        r = DocLinkResolver()
        e = r.extract_links("nothing", source_doc_id="src")
        assert e.source_doc_id == "src"

    def test_anchor_link_style(self):
        r = DocLinkResolver()
        r.register_doc("src")
        r.register_anchor("src", "intro")
        e = r.extract_links("[go](#intro)", source_doc_id="src")
        assert e.resolutions[0].style == LinkStyle.ANCHOR
        assert e.resolutions[0].is_resolved


class TestResolveAllLinks:
    def test_basic(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        res = r.resolve_all_links("[[Foo]] [[Bar]]")
        assert len(res) == 2
        assert res[0].is_resolved
        assert not res[1].is_resolved

    def test_preserves_order(self):
        r = DocLinkResolver()
        r.register_doc("a", title="A")
        r.register_doc("b", title="B")
        res = r.resolve_all_links("[[B]] before [[A]]")
        assert res[0].target_doc_id == "b"
        assert res[1].target_doc_id == "a"


class TestBrokenLinks:
    def test_returns_only_broken(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        res = r.broken_links("[[Foo]] [[Ghost]]")
        assert len(res) == 1
        assert res[0].original == "[[Ghost]]"

    def test_none_broken(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        assert r.broken_links("[[Foo]]") == []

    def test_all_broken(self):
        r = DocLinkResolver()
        res = r.broken_links("[[A]] [[B]]")
        assert len(res) == 2


# ---------------------------------------------------------------- generators


class TestLinkTo:
    def test_markdown_default(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        out = r.link_to("Foo Doc", "foo")
        assert out == "[Foo Doc](foo.md)"

    def test_wiki_with_title(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        out = r.link_to("Foo Page", "foo", style=LinkStyle.WIKI)
        assert out == "[[Foo Page]]"

    def test_wiki_with_display(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        out = r.link_to("click", "foo", style=LinkStyle.WIKI)
        assert out == "[[Foo Page|click]]"

    def test_anchor_style(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        out = r.link_to("here", "foo", style=LinkStyle.ANCHOR)
        assert out == "[here](#foo)"

    def test_reference_style(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        out = r.link_to("home", "foo", style=LinkStyle.REFERENCE)
        assert out == "[home][foo]"

    def test_resolves_target_by_title(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        out = r.link_to("x", "Foo Page")
        assert "foo.md" in out


# ---------------------------------------------------------------- lookups


class TestTitleFor:
    def test_existing(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo")
        assert r.title_for("foo") == "Foo"

    def test_missing(self):
        r = DocLinkResolver()
        assert r.title_for("ghost") is None


class TestIdForTitle:
    def test_exact(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.id_for_title("Foo Page") == "foo"

    def test_case_insensitive(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        assert r.id_for_title("foo page") == "foo"

    def test_missing(self):
        r = DocLinkResolver()
        assert r.id_for_title("nope") is None

    def test_alias(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo", aliases=["F"])
        assert r.id_for_title("f") == "foo"

    def test_empty(self):
        r = DocLinkResolver()
        assert r.id_for_title("") is None


class TestAliasesFor:
    def test_returns_list(self):
        r = DocLinkResolver()
        r.register_doc("foo", aliases=["a", "b"])
        assert sorted(r.aliases_for("foo")) == ["a", "b"]

    def test_unknown_doc(self):
        r = DocLinkResolver()
        assert r.aliases_for("ghost") == []

    def test_returns_copy(self):
        r = DocLinkResolver()
        r.register_doc("foo", aliases=["a"])
        out = r.aliases_for("foo")
        out.append("b")
        assert r.aliases_for("foo") == ["a"]


class TestTotalDocs:
    def test_zero(self):
        assert DocLinkResolver().total_docs == 0

    def test_increments(self):
        r = DocLinkResolver()
        r.register_doc("a")
        r.register_doc("b")
        assert r.total_docs == 2

    def test_decrements(self):
        r = DocLinkResolver()
        r.register_doc("a")
        r.unregister_doc("a")
        assert r.total_docs == 0


class TestClear:
    def test_empties_all(self):
        r = DocLinkResolver()
        r.register_doc("foo", aliases=["f"])
        r.register_anchor("foo", "intro")
        r.register_reference("home", "foo")
        r.clear()
        assert r.total_docs == 0
        assert r.id_for_title("f") is None
        assert r.resolve_reference("home") is None

    def test_idempotent(self):
        r = DocLinkResolver()
        r.clear()
        r.clear()
        assert r.total_docs == 0


# ---------------------------------------------------------------- edges


class TestEdgeCases:
    def test_wiki_pipe_display_extracted(self):
        r = DocLinkResolver()
        r.register_doc("foo", title="Foo Page")
        e = r.extract_links("[[Foo Page|nice text]]")
        assert e.resolutions[0].is_resolved
        assert e.resolutions[0].target_doc_id == "foo"

    def test_external_markdown_not_resolved(self):
        r = DocLinkResolver()
        e = r.extract_links("[ext](https://example.com)")
        assert not e.resolutions[0].is_resolved
        assert e.resolutions[0].error is not None

    def test_anchor_unknown_anchor_unresolved(self):
        r = DocLinkResolver()
        r.register_doc("src")
        e = r.extract_links("[bad](#missing)", source_doc_id="src")
        assert not e.resolutions[0].is_resolved

    def test_reference_unresolved(self):
        r = DocLinkResolver()
        e = r.extract_links("[label][nope]")
        assert e.resolutions[0].style == LinkStyle.REFERENCE
        assert not e.resolutions[0].is_resolved

    def test_no_overlap_between_ref_and_md(self):
        # [label][ref] should not be double-counted as both reference and markdown.
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_reference("home", "foo")
        e = r.extract_links("[label][home]")
        assert len(e.resolutions) == 1
        assert e.resolutions[0].style == LinkStyle.REFERENCE

    def test_threadsafe_registration(self):
        import threading
        r = DocLinkResolver()
        errors = []

        def worker(i):
            try:
                r.register_doc(f"doc{i}", title=f"Doc {i}")
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert r.total_docs == 50

    def test_nested_anchor_in_markdown(self):
        r = DocLinkResolver()
        r.register_doc("foo")
        r.register_anchor("foo", "section")
        e = r.extract_links("[go](foo.md#section)")
        assert e.resolutions[0].is_resolved
        assert e.resolutions[0].anchor == "section"

    def test_register_doc_title_collision_allowed(self):
        # Same title across two doc_ids: index reflects the last registered.
        r = DocLinkResolver()
        r.register_doc("a", title="Shared")
        r.register_doc("b", title="Shared")
        # Last-write-wins is acceptable; verify lookup yields one of them.
        assert r.id_for_title("Shared") in {"a", "b"}
