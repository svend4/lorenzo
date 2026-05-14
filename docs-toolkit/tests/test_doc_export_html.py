"""Tests for E241 doc_export_html — markdown-to-HTML exporter."""
from __future__ import annotations

import pytest

from docstoolkit.doc_export_html import DocExportHtml, HtmlConfig, HtmlOutput


# ---------------------------------------------------------------------------
# Config / Output dataclasses
# ---------------------------------------------------------------------------


class TestHtmlConfig:
    def test_defaults(self):
        c = HtmlConfig()
        assert c.include_toc is False
        assert c.wrap_in_html is True
        assert c.css_class_prefix == "md-"
        assert c.link_target_blank is False
        assert c.escape_html is True
        assert c.code_language_class is True
        assert c.min_heading_for_toc == 1
        assert c.max_heading_for_toc == 3

    def test_override(self):
        c = HtmlConfig(
            include_toc=True,
            wrap_in_html=False,
            css_class_prefix="x-",
            link_target_blank=True,
            escape_html=False,
            code_language_class=False,
            min_heading_for_toc=2,
            max_heading_for_toc=4,
        )
        assert c.include_toc is True
        assert c.wrap_in_html is False
        assert c.css_class_prefix == "x-"
        assert c.link_target_blank is True
        assert c.escape_html is False
        assert c.code_language_class is False
        assert c.min_heading_for_toc == 2
        assert c.max_heading_for_toc == 4


class TestHtmlOutput:
    def test_defaults(self):
        o = HtmlOutput(html="<p>x</p>")
        assert o.html == "<p>x</p>"
        assert o.toc is None
        assert o.heading_count == 0
        assert o.link_count == 0

    def test_set_fields(self):
        o = HtmlOutput(html="<x/>", toc="<nav/>", heading_count=3, link_count=2)
        assert o.toc == "<nav/>"
        assert o.heading_count == 3
        assert o.link_count == 2


# ---------------------------------------------------------------------------
# Basic conversion
# ---------------------------------------------------------------------------


class TestConvertBasic:
    def test_returns_html_output(self):
        out = DocExportHtml().convert("hello")
        assert isinstance(out, HtmlOutput)

    def test_empty_string(self):
        out = DocExportHtml().convert("")
        assert isinstance(out.html, str)

    def test_simple_paragraph_wrapped(self):
        out = DocExportHtml().convert("just text")
        assert "<p>just text</p>" in out.html
        assert "<!DOCTYPE html>" in out.html
        assert "<body>" in out.html

    def test_no_wrap(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("hello")
        assert "<!DOCTYPE html>" not in out.html
        assert "<p>hello</p>" in out.html


# ---------------------------------------------------------------------------
# Headings
# ---------------------------------------------------------------------------


class TestConvertHeadings:
    def test_h1(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("# Title")
        assert '<h1 id="title">Title</h1>' in out.html

    def test_h2(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("## Sub")
        assert '<h2 id="sub">Sub</h2>' in out.html

    def test_h6(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("###### Six")
        assert '<h6 id="six">Six</h6>' in out.html

    def test_heading_count(self):
        md = "# a\n\n## b\n\n### c\n"
        out = DocExportHtml().convert(md)
        assert out.heading_count == 3

    def test_convert_headings_method(self):
        e = DocExportHtml(HtmlConfig(wrap_in_html=False))
        result = e.convert_headings("# Hello\nplain")
        assert "<h1" in result
        assert "plain" in result

    def test_seven_hashes_not_heading(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("####### nope")
        assert "<h7" not in out.html


# ---------------------------------------------------------------------------
# Paragraphs
# ---------------------------------------------------------------------------


class TestConvertParagraphs:
    def test_single(self):
        e = DocExportHtml()
        assert e.convert_paragraphs("hello") == "<p>hello</p>"

    def test_two_paragraphs(self):
        e = DocExportHtml()
        out = e.convert_paragraphs("a\n\nb")
        assert "<p>a</p>" in out
        assert "<p>b</p>" in out

    def test_join_lines(self):
        e = DocExportHtml()
        out = e.convert_paragraphs("first line\nsecond line")
        assert "<p>first line second line</p>" == out

    def test_skip_empty(self):
        e = DocExportHtml()
        assert e.convert_paragraphs("\n\n\n") == ""


# ---------------------------------------------------------------------------
# Unordered lists
# ---------------------------------------------------------------------------


class TestConvertLists:
    def test_basic_ul(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("- a\n- b")
        assert "<ul>" in out.html
        assert "<li>a</li>" in out.html
        assert "<li>b</li>" in out.html

    def test_star_marker(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("* x\n* y")
        assert "<ul>" in out.html
        assert "<li>x</li>" in out.html

    def test_plus_marker(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("+ z")
        assert "<li>z</li>" in out.html

    def test_convert_lists_method(self):
        e = DocExportHtml()
        result = e.convert_lists("- a\n- b\n")
        assert "<ul>" in result
        assert "<li>a</li>" in result


class TestConvertOrderedLists:
    def test_basic_ol(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("1. one\n2. two")
        assert "<ol>" in out.html
        assert "<li>one</li>" in out.html
        assert "<li>two</li>" in out.html

    def test_ol_count(self):
        e = DocExportHtml(HtmlConfig(wrap_in_html=False))
        out = e.convert("1. a\n2. b\n3. c")
        assert out.html.count("<li>") == 3


# ---------------------------------------------------------------------------
# Code blocks
# ---------------------------------------------------------------------------


class TestConvertCodeBlocks:
    def test_basic(self):
        md = "```\nprint(1)\n```"
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert "<pre><code" in out.html
        assert "print(1)" in out.html

    def test_no_inline_in_code(self):
        md = "```\n**not bold**\n```"
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert "<strong>" not in out.html
        assert "**not bold**" in out.html

    def test_escapes_code(self):
        md = "```\n<script>\n```"
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert "<script>" not in out.html
        assert "&lt;script&gt;" in out.html

    def test_method(self):
        e = DocExportHtml()
        out = e.convert_code_blocks("```\nx\n```")
        assert "<pre><code" in out


class TestConvertCodeLanguageClass:
    def test_language_class_added(self):
        md = "```python\nprint(1)\n```"
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert 'class="language-python"' in out.html

    def test_language_class_disabled(self):
        cfg = HtmlConfig(wrap_in_html=False, code_language_class=False)
        out = DocExportHtml(cfg).convert("```python\nprint(1)\n```")
        assert 'class="language-' not in out.html

    def test_no_language_no_class(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("```\nx\n```")
        assert "class=" not in out.html


# ---------------------------------------------------------------------------
# Inline emphasis
# ---------------------------------------------------------------------------


class TestConvertInlineBold:
    def test_double_star(self):
        e = DocExportHtml()
        assert "<strong>x</strong>" in e.convert_inline("**x**")

    def test_double_underscore(self):
        e = DocExportHtml()
        assert "<strong>x</strong>" in e.convert_inline("__x__")

    def test_bold_in_paragraph(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("hello **bold** world")
        assert "<strong>bold</strong>" in out.html


class TestConvertInlineItalic:
    def test_single_star(self):
        e = DocExportHtml()
        assert "<em>x</em>" in e.convert_inline("*x*")

    def test_single_underscore(self):
        e = DocExportHtml()
        assert "<em>x</em>" in e.convert_inline("_x_")

    def test_italic_in_paragraph(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("hello *it* world")
        assert "<em>it</em>" in out.html


class TestConvertInlineCode:
    def test_code(self):
        e = DocExportHtml()
        assert "<code>x</code>" in e.convert_inline("`x`")

    def test_code_escapes(self):
        e = DocExportHtml()
        out = e.convert_inline("`<a>`")
        assert "<code>&lt;a&gt;</code>" == out

    def test_code_no_inner_emphasis(self):
        e = DocExportHtml()
        out = e.convert_inline("`**not bold**`")
        assert "<strong>" not in out


class TestConvertInlineLinks:
    def test_link_basic(self):
        e = DocExportHtml()
        out = e.convert_inline("[click](https://example.com)")
        assert '<a href="https://example.com">click</a>' == out

    def test_link_count(self):
        out = DocExportHtml().convert("see [a](u1) and [b](u2)")
        assert out.link_count == 2

    def test_link_does_not_get_target_by_default(self):
        e = DocExportHtml()
        out = e.convert_inline("[x](u)")
        assert "target=" not in out


class TestConvertLinksBlankTarget:
    def test_target_blank(self):
        cfg = HtmlConfig(link_target_blank=True)
        e = DocExportHtml(cfg)
        out = e.convert_inline("[x](u)")
        assert 'target="_blank"' in out
        assert 'href="u"' in out

    def test_blank_in_full_doc(self):
        cfg = HtmlConfig(wrap_in_html=False, link_target_blank=True)
        out = DocExportHtml(cfg).convert("see [a](http://x)")
        assert 'target="_blank"' in out.html


# ---------------------------------------------------------------------------
# Blockquotes
# ---------------------------------------------------------------------------


class TestConvertBlockquotes:
    def test_basic(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("> hello")
        assert "<blockquote>hello</blockquote>" in out.html

    def test_multiline(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("> a\n> b")
        assert "<blockquote>" in out.html
        assert "a b" in out.html

    def test_method(self):
        e = DocExportHtml()
        result = e.convert_blockquotes("> x")
        assert "<blockquote>x</blockquote>" in result

    def test_blockquote_with_emphasis(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("> **strong**")
        assert "<strong>strong</strong>" in out.html


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


class TestConvertTables:
    def test_basic_table(self):
        md = "| a | b |\n| --- | --- |\n| 1 | 2 |"
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert "<table>" in out.html
        assert "<thead>" in out.html
        assert "<th>a</th>" in out.html
        assert "<tbody>" in out.html
        assert "<td>1</td>" in out.html

    def test_two_body_rows(self):
        md = "| a | b |\n| - | - |\n| 1 | 2 |\n| 3 | 4 |"
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert out.html.count("<tr>") == 3  # header + 2 body rows

    def test_method(self):
        md = "| a |\n| - |\n| 1 |\n"
        result = DocExportHtml().convert_tables(md)
        assert "<table>" in result


# ---------------------------------------------------------------------------
# Escaping
# ---------------------------------------------------------------------------


class TestEscapeHtml:
    def test_escape_basic(self):
        e = DocExportHtml()
        assert e.escape("<script>") == "&lt;script&gt;"

    def test_escape_amp(self):
        e = DocExportHtml()
        assert "&amp;" in e.escape("a & b")

    def test_inline_escapes_html(self):
        e = DocExportHtml(HtmlConfig(escape_html=True))
        out = e.convert_inline("<div>")
        assert "&lt;div&gt;" in out

    def test_inline_no_escape_when_disabled(self):
        e = DocExportHtml(HtmlConfig(escape_html=False))
        out = e.convert_inline("<div>")
        assert "<div>" in out

    def test_in_paragraph(self):
        cfg = HtmlConfig(wrap_in_html=False, escape_html=True)
        out = DocExportHtml(cfg).convert("a < b")
        assert "&lt;" in out.html


# ---------------------------------------------------------------------------
# Slug
# ---------------------------------------------------------------------------


class TestToSlug:
    def test_simple(self):
        assert DocExportHtml().to_slug("Hello World") == "hello-world"

    def test_punctuation_stripped(self):
        assert DocExportHtml().to_slug("Hello, World!") == "hello-world"

    def test_unique_increments(self):
        e = DocExportHtml()
        a = e.to_slug("Hello")
        b = e.to_slug("Hello")
        assert a == "hello"
        assert b == "hello-1"

    def test_empty(self):
        assert DocExportHtml().to_slug("") == "section"

    def test_cyrillic(self):
        slug = DocExportHtml().to_slug("Привет Мир")
        assert "-" in slug
        assert "привет" in slug


# ---------------------------------------------------------------------------
# TOC
# ---------------------------------------------------------------------------


class TestBuildToc:
    def test_basic(self):
        e = DocExportHtml(HtmlConfig(include_toc=True, wrap_in_html=False))
        toc = e.build_toc("# A\n\n## B\n\n## C\n")
        assert "<nav" in toc
        assert 'class="md-toc"' in toc
        assert 'href="#a"' in toc

    def test_links_in_doc(self):
        cfg = HtmlConfig(include_toc=True, wrap_in_html=False)
        out = DocExportHtml(cfg).convert("# Title\n\nbody")
        assert "<nav" in out.html
        assert out.toc is not None
        assert "Title" in out.toc

    def test_empty_when_no_headings(self):
        toc = DocExportHtml().build_toc("nothing here")
        assert "<nav" in toc

    def test_css_prefix(self):
        cfg = HtmlConfig(include_toc=True, css_class_prefix="docs-")
        toc = DocExportHtml(cfg).build_toc("# x")
        assert 'class="docs-toc"' in toc

    def test_nested_levels(self):
        toc = DocExportHtml(HtmlConfig()).build_toc("# a\n\n## b\n\n# c\n")
        # nested structure should contain multiple <ul>
        assert toc.count("<ul>") >= 1

    def test_skips_headings_inside_code(self):
        md = "# Real\n\n```\n# Fake\n```\n"
        toc = DocExportHtml().build_toc(md)
        assert "Real" in toc
        assert "Fake" not in toc


# ---------------------------------------------------------------------------
# Wrapping
# ---------------------------------------------------------------------------


class TestWrapInHtml:
    def test_default_wraps(self):
        out = DocExportHtml().convert("x")
        assert "<!DOCTYPE html>" in out.html
        assert "<html>" in out.html
        assert "</html>" in out.html
        assert "<body>" in out.html

    def test_no_wrap(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("x")
        assert "<!DOCTYPE html>" not in out.html
        assert "<html>" not in out.html

    def test_toc_inside_wrap(self):
        cfg = HtmlConfig(wrap_in_html=True, include_toc=True)
        out = DocExportHtml(cfg).convert("# H\n")
        assert "<!DOCTYPE html>" in out.html
        assert "<nav" in out.html


# ---------------------------------------------------------------------------
# Min/max heading levels for TOC
# ---------------------------------------------------------------------------


class TestMinMaxHeadingForToc:
    def test_max_excludes_deeper(self):
        cfg = HtmlConfig(max_heading_for_toc=2)
        toc = DocExportHtml(cfg).build_toc("# a\n\n## b\n\n### c\n")
        assert "a" in toc
        assert ">b<" in toc
        assert ">c<" not in toc

    def test_min_excludes_shallow(self):
        cfg = HtmlConfig(min_heading_for_toc=2)
        toc = DocExportHtml(cfg).build_toc("# a\n\n## b\n\n## c\n")
        assert ">a<" not in toc
        assert ">b<" in toc

    def test_only_h2(self):
        cfg = HtmlConfig(min_heading_for_toc=2, max_heading_for_toc=2)
        toc = DocExportHtml(cfg).build_toc("# a\n\n## b\n\n### c\n")
        assert ">a<" not in toc
        assert ">b<" in toc
        assert ">c<" not in toc


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_crlf_normalised(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(
            "# h\r\n\r\np\r\n"
        )
        assert "<h1" in out.html
        assert "<p>p</p>" in out.html

    def test_mixed_content(self):
        md = (
            "# Title\n\n"
            "Para with **bold** and `code`.\n\n"
            "- a\n- b\n\n"
            "```py\nx=1\n```\n\n"
            "> note\n"
        )
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert(md)
        assert "<h1" in out.html
        assert "<strong>bold</strong>" in out.html
        assert "<code>code</code>" in out.html
        assert "<ul>" in out.html
        assert "<pre>" in out.html
        assert "<blockquote>" in out.html

    def test_only_whitespace(self):
        out = DocExportHtml(HtmlConfig(wrap_in_html=False)).convert("   \n\n  ")
        assert isinstance(out.html, str)

    def test_link_in_paragraph_counts(self):
        out = DocExportHtml().convert("Click [here](http://x).")
        assert out.link_count == 1

    def test_unique_slugs_in_doc(self):
        cfg = HtmlConfig(wrap_in_html=False)
        out = DocExportHtml(cfg).convert("# Same\n\n## Same\n")
        # Both headings should still appear with distinct ids.
        assert 'id="same"' in out.html
        assert 'id="same-1"' in out.html

    def test_paragraph_with_special_chars_escaped(self):
        cfg = HtmlConfig(wrap_in_html=False)
        out = DocExportHtml(cfg).convert("if a < b and b > c")
        assert "&lt;" in out.html
        assert "&gt;" in out.html
