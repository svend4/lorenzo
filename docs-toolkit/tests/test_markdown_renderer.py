"""Tests for docstoolkit.markdown_renderer — target: >= 50 tests."""
from __future__ import annotations

import pytest

from docstoolkit.markdown_renderer import MarkdownRenderer, RenderConfig


# ===========================================================================
# RenderConfig
# ===========================================================================

class TestRenderConfig:
    def test_default_heading_style_is_atx(self):
        assert RenderConfig().heading_style == "atx"

    def test_default_list_marker(self):
        assert RenderConfig().list_marker == "-"

    def test_default_numbered_marker(self):
        assert RenderConfig().numbered_marker == "."

    def test_default_table_alignment_is_empty_dict(self):
        cfg = RenderConfig()
        assert cfg.table_alignment == {}

    def test_table_alignment_is_independent_per_instance(self):
        a = RenderConfig()
        b = RenderConfig()
        a.table_alignment["col"] = "right"
        assert "col" not in b.table_alignment

    def test_default_bold_marker(self):
        assert RenderConfig().bold_marker == "**"

    def test_default_italic_marker(self):
        assert RenderConfig().italic_marker == "*"

    def test_default_code_fence(self):
        assert RenderConfig().code_fence == "```"

    def test_custom_config(self):
        cfg = RenderConfig(list_marker="*", bold_marker="__")
        assert cfg.list_marker == "*"
        assert cfg.bold_marker == "__"


# ===========================================================================
# Heading
# ===========================================================================

class TestHeading:
    def test_atx_level_1(self):
        r = MarkdownRenderer()
        assert r.heading("Title", 1) == "# Title\n"

    def test_atx_level_2(self):
        r = MarkdownRenderer()
        assert r.heading("Sub", 2) == "## Sub\n"

    def test_atx_level_3(self):
        assert MarkdownRenderer().heading("h", 3) == "### h\n"

    def test_atx_level_4(self):
        assert MarkdownRenderer().heading("h", 4) == "#### h\n"

    def test_atx_level_5(self):
        assert MarkdownRenderer().heading("h", 5) == "##### h\n"

    def test_atx_level_6(self):
        assert MarkdownRenderer().heading("h", 6) == "###### h\n"

    def test_default_level_is_1(self):
        assert MarkdownRenderer().heading("X") == "# X\n"

    def test_setext_level_1(self):
        r = MarkdownRenderer(RenderConfig(heading_style="setext"))
        out = r.heading("Title", 1)
        assert out == "Title\n=====\n"

    def test_setext_level_2(self):
        r = MarkdownRenderer(RenderConfig(heading_style="setext"))
        out = r.heading("Title", 2)
        assert out == "Title\n-----\n"

    def test_setext_levels_3_to_6_fallback_to_atx(self):
        r = MarkdownRenderer(RenderConfig(heading_style="setext"))
        assert r.heading("x", 3) == "### x\n"
        assert r.heading("x", 6) == "###### x\n"

    def test_invalid_level_raises(self):
        r = MarkdownRenderer()
        with pytest.raises(ValueError):
            r.heading("x", 0)
        with pytest.raises(ValueError):
            r.heading("x", 7)


# ===========================================================================
# Paragraph
# ===========================================================================

class TestParagraph:
    def test_basic(self):
        assert MarkdownRenderer().paragraph("Hello world.") == "Hello world.\n"

    def test_empty(self):
        assert MarkdownRenderer().paragraph("") == "\n"

    def test_multiline(self):
        assert MarkdownRenderer().paragraph("line1\nline2") == "line1\nline2\n"


# ===========================================================================
# Bold
# ===========================================================================

class TestBold:
    def test_default_marker(self):
        assert MarkdownRenderer().bold("x") == "**x**"

    def test_custom_marker(self):
        r = MarkdownRenderer(RenderConfig(bold_marker="__"))
        assert r.bold("x") == "__x__"

    def test_with_spaces(self):
        assert MarkdownRenderer().bold("a b c") == "**a b c**"


# ===========================================================================
# Italic
# ===========================================================================

class TestItalic:
    def test_default_marker(self):
        assert MarkdownRenderer().italic("x") == "*x*"

    def test_custom_marker(self):
        r = MarkdownRenderer(RenderConfig(italic_marker="_"))
        assert r.italic("x") == "_x_"


# ===========================================================================
# Code inline
# ===========================================================================

class TestCodeInline:
    def test_simple(self):
        assert MarkdownRenderer().code("foo") == "`foo`"

    def test_empty(self):
        assert MarkdownRenderer().code("") == "``"

    def test_with_backtick_uses_longer_fence(self):
        out = MarkdownRenderer().code("a`b")
        # Should use double backticks and pad spaces.
        assert out.startswith("`` ")
        assert out.endswith(" ``")
        assert "a`b" in out

    def test_with_double_backticks(self):
        out = MarkdownRenderer().code("a``b")
        assert out.startswith("``` ")
        assert out.endswith(" ```")


# ===========================================================================
# Code block
# ===========================================================================

class TestCodeBlock:
    def test_without_language(self):
        out = MarkdownRenderer().code_block("print('hi')")
        assert out == "```\nprint('hi')\n```\n"

    def test_with_language(self):
        out = MarkdownRenderer().code_block("print('hi')", "python")
        assert out == "```python\nprint('hi')\n```\n"

    def test_multiline_code(self):
        out = MarkdownRenderer().code_block("a\nb\nc", "")
        assert out == "```\na\nb\nc\n```\n"

    def test_already_trailing_newline(self):
        out = MarkdownRenderer().code_block("x\n", "")
        assert out == "```\nx\n```\n"

    def test_empty_code(self):
        out = MarkdownRenderer().code_block("", "")
        assert out == "```\n```\n"


# ===========================================================================
# Link
# ===========================================================================

class TestLink:
    def test_no_title(self):
        assert MarkdownRenderer().link("Anthropic", "https://anthropic.com") == "[Anthropic](https://anthropic.com)"

    def test_with_title(self):
        out = MarkdownRenderer().link("A", "https://a.io", "Tooltip")
        assert out == '[A](https://a.io "Tooltip")'

    def test_empty_text(self):
        assert MarkdownRenderer().link("", "u") == "[](u)"


# ===========================================================================
# Image
# ===========================================================================

class TestImage:
    def test_no_title(self):
        assert MarkdownRenderer().image("alt", "u.png") == "![alt](u.png)"

    def test_with_title(self):
        assert MarkdownRenderer().image("a", "u.png", "T") == '![a](u.png "T")'


# ===========================================================================
# List
# ===========================================================================

class TestList:
    def test_unordered_default_marker(self):
        out = MarkdownRenderer().list(["a", "b", "c"])
        assert out == "- a\n- b\n- c\n"

    def test_ordered(self):
        out = MarkdownRenderer().list(["a", "b", "c"], ordered=True)
        assert out == "1. a\n2. b\n3. c\n"

    def test_custom_unordered_marker_star(self):
        r = MarkdownRenderer(RenderConfig(list_marker="*"))
        assert r.list(["a"]) == "* a\n"

    def test_custom_unordered_marker_plus(self):
        r = MarkdownRenderer(RenderConfig(list_marker="+"))
        assert r.list(["a", "b"]) == "+ a\n+ b\n"

    def test_custom_numbered_marker(self):
        r = MarkdownRenderer(RenderConfig(numbered_marker=")"))
        assert r.list(["a", "b"], ordered=True) == "1) a\n2) b\n"

    def test_empty_list(self):
        assert MarkdownRenderer().list([]) == ""

    def test_single_item(self):
        assert MarkdownRenderer().list(["only"]) == "- only\n"


# ===========================================================================
# Nested list
# ===========================================================================

class TestNestedList:
    def test_flat_list_via_nested(self):
        out = MarkdownRenderer().nested_list(["a", "b"])
        assert out == "- a\n- b\n"

    def test_one_level_nesting(self):
        out = MarkdownRenderer().nested_list(["parent", ["child1", "child2"]])
        assert out == "- parent\n  - child1\n  - child2\n"

    def test_two_levels_nesting(self):
        items = ["a", ["b", ["c"]]]
        out = MarkdownRenderer().nested_list(items)
        assert out == "- a\n  - b\n    - c\n"

    def test_initial_indent_level(self):
        out = MarkdownRenderer().nested_list(["a"], indent_level=1)
        assert out == "  - a\n"

    def test_empty_nested(self):
        assert MarkdownRenderer().nested_list([]) == ""

    def test_mixed_siblings(self):
        items = ["a", "b", ["b1", "b2"], "c"]
        out = MarkdownRenderer().nested_list(items)
        assert out == "- a\n- b\n  - b1\n  - b2\n- c\n"


# ===========================================================================
# Table
# ===========================================================================

class TestTable:
    def test_basic_table(self):
        out = MarkdownRenderer().table(["A", "B"], [["1", "2"], ["3", "4"]])
        # No alignment configured -> simple separator.
        assert "| A   | B   |" in out  # padded to width 3
        assert "|-----|-----|" in out
        assert "| 1   | 2   |" in out
        assert "| 3   | 4   |" in out
        assert out.endswith("\n")

    def test_table_pads_short_rows(self):
        out = MarkdownRenderer().table(["A", "B", "C"], [["1"]])
        # The row should be padded with empty strings.
        lines = out.strip().splitlines()
        body = lines[-1]
        assert body.count("|") == 4  # 4 pipes for 3 cols

    def test_table_truncates_long_rows(self):
        out = MarkdownRenderer().table(["A"], [["1", "2", "3"]])
        lines = out.strip().splitlines()
        body = lines[-1]
        assert "2" not in body
        assert "1" in body

    def test_alignment_left(self):
        cfg = RenderConfig(table_alignment={"A": "left", "B": "right"})
        out = MarkdownRenderer(cfg).table(["A", "B"], [["1", "2"]])
        assert ":--" in out  # left marker
        assert "--:" in out   # right marker

    def test_alignment_center(self):
        cfg = RenderConfig(table_alignment={"A": "center"})
        out = MarkdownRenderer(cfg).table(["A"], [["x"]])
        assert ":-:" in out or ":---:" in out or out.count(":") >= 2

    def test_alignment_right(self):
        cfg = RenderConfig(table_alignment={"A": "right"})
        out = MarkdownRenderer(cfg).table(["A"], [["x"]])
        assert "--:" in out

    def test_empty_headers_returns_empty(self):
        assert MarkdownRenderer().table([], [["x"]]) == ""

    def test_no_rows(self):
        out = MarkdownRenderer().table(["A", "B"], [])
        # Should still produce header + separator.
        assert "| A" in out
        assert "---" in out


# ===========================================================================
# Blockquote
# ===========================================================================

class TestBlockquote:
    def test_single_line(self):
        assert MarkdownRenderer().blockquote("hello") == "> hello\n"

    def test_multiline(self):
        out = MarkdownRenderer().blockquote("a\nb\nc")
        assert out == "> a\n> b\n> c\n"

    def test_with_empty_internal_line(self):
        out = MarkdownRenderer().blockquote("a\n\nb")
        assert out == "> a\n>\n> b\n"

    def test_empty(self):
        assert MarkdownRenderer().blockquote("") == ">\n"


# ===========================================================================
# Horizontal rule
# ===========================================================================

class TestHorizontalRule:
    def test_value(self):
        assert MarkdownRenderer().horizontal_rule() == "---\n"


# ===========================================================================
# Task list
# ===========================================================================

class TestTaskList:
    def test_mixed(self):
        out = MarkdownRenderer().task_list([("done", True), ("todo", False)])
        assert out == "- [x] done\n- [ ] todo\n"

    def test_all_checked(self):
        out = MarkdownRenderer().task_list([("a", True), ("b", True)])
        assert out == "- [x] a\n- [x] b\n"

    def test_all_unchecked(self):
        out = MarkdownRenderer().task_list([("a", False)])
        assert out == "- [ ] a\n"

    def test_empty(self):
        assert MarkdownRenderer().task_list([]) == ""

    def test_custom_marker(self):
        r = MarkdownRenderer(RenderConfig(list_marker="*"))
        out = r.task_list([("x", True)])
        assert out == "* [x] x\n"


# ===========================================================================
# Definition list
# ===========================================================================

class TestDefinitionList:
    def test_single(self):
        out = MarkdownRenderer().definition_list([("Term", "Defn")])
        assert out == "Term\n: Defn\n"

    def test_multiple(self):
        out = MarkdownRenderer().definition_list([("T1", "D1"), ("T2", "D2")])
        # Each pair separated by a blank line.
        assert out == "T1\n: D1\n\nT2\n: D2\n"

    def test_empty(self):
        assert MarkdownRenderer().definition_list([]) == ""


# ===========================================================================
# Render document
# ===========================================================================

class TestRenderDocument:
    def test_simple_doc(self):
        blocks = [
            {"type": "heading", "level": 1, "text": "Title"},
            {"type": "paragraph", "text": "Hello world."},
        ]
        out = MarkdownRenderer().render_document(blocks)
        assert "# Title\n" in out
        assert "Hello world.\n" in out
        assert out.index("# Title") < out.index("Hello world.")

    def test_all_block_types(self):
        blocks = [
            {"type": "heading", "level": 2, "text": "H"},
            {"type": "paragraph", "text": "para"},
            {"type": "code_block", "text": "print(1)", "language": "py"},
            {"type": "list", "items": ["a", "b"]},
            {"type": "list", "items": ["x", "y"], "ordered": True},
            {"type": "nested_list", "items": ["a", ["a1"]]},
            {"type": "table", "headers": ["A"], "rows": [["1"]]},
            {"type": "blockquote", "text": "quote"},
            {"type": "horizontal_rule"},
            {"type": "task_list", "items": [("done", True)]},
            {"type": "definition_list", "items": [("term", "def")]},
        ]
        out = MarkdownRenderer().render_document(blocks)
        assert "## H" in out
        assert "para" in out
        assert "```py" in out
        assert "- a" in out
        assert "1. x" in out
        assert "  - a1" in out
        assert "| A" in out
        assert "> quote" in out
        assert "---" in out
        assert "- [x] done" in out
        assert "term\n: def" in out

    def test_empty_blocks_produces_empty(self):
        assert MarkdownRenderer().render_document([]) == ""

    def test_unknown_block_raises(self):
        with pytest.raises(ValueError):
            MarkdownRenderer().render_document([{"type": "wat"}])

    def test_heading_default_level(self):
        out = MarkdownRenderer().render_document([{"type": "heading", "text": "X"}])
        assert "# X" in out


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_bold_empty(self):
        assert MarkdownRenderer().bold("") == "****"

    def test_italic_empty(self):
        assert MarkdownRenderer().italic("") == "**"

    def test_link_with_special_chars(self):
        out = MarkdownRenderer().link("a [b]", "https://x.io")
        assert "a [b]" in out

    def test_table_with_varying_widths(self):
        out = MarkdownRenderer().table(["A", "longer"], [["x", "y"]])
        # column widths should accommodate the longest cell
        lines = out.strip().splitlines()
        header = lines[0]
        assert "longer" in header

    def test_setext_heading_for_short_text_underline_minimum(self):
        r = MarkdownRenderer(RenderConfig(heading_style="setext"))
        out = r.heading("X", 1)
        # underline at least 3 chars long
        underline = out.strip().splitlines()[1]
        assert len(underline) >= 3
        assert set(underline) == {"="}

    def test_nested_list_with_only_nested(self):
        # A nested block at the top with no preceding leaf should still render.
        out = MarkdownRenderer().nested_list([["a", "b"]])
        assert "  - a" in out
        assert "  - b" in out

    def test_code_block_preserves_internal_blank_lines(self):
        out = MarkdownRenderer().code_block("a\n\nb")
        assert "a\n\nb" in out

    def test_blockquote_trailing_newline_in_input(self):
        # Trailing newline yields a blank quoted line then a single trailing newline.
        out = MarkdownRenderer().blockquote("a\n")
        assert out.startswith("> a")
        assert out.endswith("\n")

    def test_list_with_unicode(self):
        out = MarkdownRenderer().list(["агент", "память"])
        assert "- агент" in out
        assert "- память" in out

    def test_table_with_unicode(self):
        out = MarkdownRenderer().table(["Имя", "Возраст"], [["Алиса", "30"]])
        assert "Имя" in out
        assert "Алиса" in out

    def test_render_document_preserves_order(self):
        blocks = [
            {"type": "paragraph", "text": "first"},
            {"type": "paragraph", "text": "second"},
            {"type": "paragraph", "text": "third"},
        ]
        out = MarkdownRenderer().render_document(blocks)
        assert out.index("first") < out.index("second") < out.index("third")
