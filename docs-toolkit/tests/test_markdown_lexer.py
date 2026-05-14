"""Tests for docstoolkit.markdown_lexer — target: >= 50 tests."""
from __future__ import annotations

import pytest

from docstoolkit.markdown_lexer import MarkdownLexer, Token, TokenType


# ===========================================================================
# TokenType
# ===========================================================================


class TestTokenType:
    def test_has_heading(self):
        assert TokenType.HEADING.value == "HEADING"

    def test_has_paragraph(self):
        assert TokenType.PARAGRAPH.value == "PARAGRAPH"

    def test_has_code_block(self):
        assert TokenType.CODE_BLOCK.value == "CODE_BLOCK"

    def test_has_code_inline(self):
        assert TokenType.CODE_INLINE.value == "CODE_INLINE"

    def test_has_all_required_types(self):
        required = {
            "HEADING", "PARAGRAPH", "CODE_BLOCK", "CODE_INLINE", "LIST_ITEM",
            "NUMBERED_ITEM", "BLOCKQUOTE", "HORIZONTAL_RULE", "LINK", "IMAGE",
            "BOLD", "ITALIC", "STRIKETHROUGH", "TABLE_ROW", "FRONTMATTER",
            "COMMENT", "NEWLINE", "TEXT",
        }
        names = {t.name for t in TokenType}
        assert required.issubset(names)


# ===========================================================================
# Token
# ===========================================================================


class TestToken:
    def test_construct_basic(self):
        t = Token(token_type=TokenType.TEXT, value="hi", line_num=1)
        assert t.value == "hi"
        assert t.line_num == 1
        assert t.column == 0
        assert t.metadata == {}

    def test_metadata_default_is_independent(self):
        a = Token(TokenType.TEXT, "a", 1)
        b = Token(TokenType.TEXT, "b", 1)
        a.metadata["k"] = 1
        assert "k" not in b.metadata

    def test_with_metadata(self):
        t = Token(TokenType.HEADING, "Title", 1, 0, {"level": 1})
        assert t.metadata["level"] == 1

    def test_column_field(self):
        t = Token(TokenType.TEXT, "x", 1, column=5)
        assert t.column == 5


# ===========================================================================
# Heading
# ===========================================================================


class TestTokenizeHeading:
    def test_level_1(self):
        tokens = MarkdownLexer().tokenize("# Title")
        assert tokens[0].token_type == TokenType.HEADING
        assert tokens[0].metadata["level"] == 1
        assert tokens[0].value == "Title"

    def test_level_2(self):
        tokens = MarkdownLexer().tokenize("## Subtitle")
        assert tokens[0].metadata["level"] == 2

    def test_level_3(self):
        tokens = MarkdownLexer().tokenize("### H3")
        assert tokens[0].metadata["level"] == 3

    def test_level_6(self):
        tokens = MarkdownLexer().tokenize("###### Six")
        assert tokens[0].metadata["level"] == 6
        assert tokens[0].value == "Six"

    def test_level_7_not_heading(self):
        # 7 hashes followed by space — pattern matches up to 6, but real impl
        # uses {1,6}\s+; 7 hashes + space → won't match heading
        tokens = MarkdownLexer().tokenize("####### too many")
        # Should become paragraph
        assert tokens[0].token_type == TokenType.PARAGRAPH

    def test_heading_line_num(self):
        tokens = MarkdownLexer().tokenize("text\n# Title")
        h = [t for t in tokens if t.token_type == TokenType.HEADING][0]
        assert h.line_num == 2

    def test_heading_strips_content(self):
        tokens = MarkdownLexer().tokenize("#   Spaces  ")
        assert tokens[0].value == "Spaces"


# ===========================================================================
# Code block
# ===========================================================================


class TestTokenizeCodeBlock:
    def test_basic_code_block(self):
        text = "```\nprint(1)\n```"
        tokens = MarkdownLexer().tokenize(text)
        cbs = [t for t in tokens if t.token_type == TokenType.CODE_BLOCK]
        assert len(cbs) == 1
        assert cbs[0].value == "print(1)"

    def test_code_block_with_language(self):
        text = "```python\nx = 1\n```"
        tokens = MarkdownLexer().tokenize(text)
        cb = [t for t in tokens if t.token_type == TokenType.CODE_BLOCK][0]
        assert cb.metadata["language"] == "python"

    def test_code_block_multiline(self):
        text = "```bash\ncmd1\ncmd2\ncmd3\n```"
        cb = [t for t in MarkdownLexer().tokenize(text) if t.token_type == TokenType.CODE_BLOCK][0]
        assert "cmd1" in cb.value
        assert "cmd3" in cb.value

    def test_code_block_empty_language(self):
        text = "```\ncode\n```"
        cb = [t for t in MarkdownLexer().tokenize(text) if t.token_type == TokenType.CODE_BLOCK][0]
        assert cb.metadata["language"] == ""


# ===========================================================================
# List item
# ===========================================================================


class TestTokenizeListItem:
    def test_dash(self):
        tokens = MarkdownLexer().tokenize("- item")
        assert tokens[0].token_type == TokenType.LIST_ITEM
        assert tokens[0].value == "item"

    def test_star(self):
        tokens = MarkdownLexer().tokenize("* item")
        assert tokens[0].token_type == TokenType.LIST_ITEM

    def test_plus(self):
        tokens = MarkdownLexer().tokenize("+ item")
        assert tokens[0].token_type == TokenType.LIST_ITEM

    def test_multiple_items(self):
        text = "- a\n- b\n- c"
        items = [
            t for t in MarkdownLexer().tokenize(text)
            if t.token_type == TokenType.LIST_ITEM
        ]
        assert len(items) == 3


# ===========================================================================
# Numbered item
# ===========================================================================


class TestTokenizeNumberedItem:
    def test_basic(self):
        tokens = MarkdownLexer().tokenize("1. first")
        assert tokens[0].token_type == TokenType.NUMBERED_ITEM
        assert tokens[0].value == "first"
        assert tokens[0].metadata["number"] == 1

    def test_number_metadata(self):
        tokens = MarkdownLexer().tokenize("42. answer")
        assert tokens[0].metadata["number"] == 42

    def test_multiple_numbered(self):
        text = "1. a\n2. b\n3. c"
        items = [
            t for t in MarkdownLexer().tokenize(text)
            if t.token_type == TokenType.NUMBERED_ITEM
        ]
        assert [i.metadata["number"] for i in items] == [1, 2, 3]


# ===========================================================================
# Blockquote
# ===========================================================================


class TestTokenizeBlockquote:
    def test_basic(self):
        tokens = MarkdownLexer().tokenize("> quoted")
        assert tokens[0].token_type == TokenType.BLOCKQUOTE
        assert tokens[0].value == "quoted"

    def test_empty_blockquote(self):
        tokens = MarkdownLexer().tokenize(">")
        assert tokens[0].token_type == TokenType.BLOCKQUOTE
        assert tokens[0].value == ""

    def test_blockquote_with_spaces(self):
        tokens = MarkdownLexer().tokenize(">   spaced")
        assert tokens[0].token_type == TokenType.BLOCKQUOTE
        assert "spaced" in tokens[0].value


# ===========================================================================
# Horizontal rule
# ===========================================================================


class TestTokenizeHorizontalRule:
    def test_dashes(self):
        tokens = MarkdownLexer().tokenize("---")
        assert tokens[0].token_type == TokenType.HORIZONTAL_RULE

    def test_more_dashes(self):
        tokens = MarkdownLexer().tokenize("------")
        assert tokens[0].token_type == TokenType.HORIZONTAL_RULE

    def test_stars(self):
        tokens = MarkdownLexer().tokenize("***")
        assert tokens[0].token_type == TokenType.HORIZONTAL_RULE


# ===========================================================================
# Table row
# ===========================================================================


class TestTokenizeTableRow:
    def test_basic(self):
        tokens = MarkdownLexer().tokenize("| a | b | c |")
        assert tokens[0].token_type == TokenType.TABLE_ROW

    def test_cells_metadata(self):
        tokens = MarkdownLexer().tokenize("| x | y |")
        assert tokens[0].metadata["cells"] == ["x", "y"]

    def test_multiple_rows(self):
        text = "| a | b |\n| c | d |"
        rows = [
            t for t in MarkdownLexer().tokenize(text)
            if t.token_type == TokenType.TABLE_ROW
        ]
        assert len(rows) == 2


# ===========================================================================
# Frontmatter
# ===========================================================================


class TestTokenizeFrontmatter:
    def test_basic(self):
        text = "---\ntitle: X\n---\nbody"
        tokens = MarkdownLexer().tokenize(text)
        fm = [t for t in tokens if t.token_type == TokenType.FRONTMATTER]
        assert len(fm) == 1
        assert "title: X" in fm[0].value

    def test_frontmatter_only_at_start(self):
        text = "body\n---\nfoo: bar\n---"
        tokens = MarkdownLexer().tokenize(text)
        fm = [t for t in tokens if t.token_type == TokenType.FRONTMATTER]
        # Not at start, no frontmatter
        assert len(fm) == 0

    def test_frontmatter_multiline_content(self):
        text = "---\na: 1\nb: 2\nc: 3\n---\n"
        tokens = MarkdownLexer().tokenize(text)
        fm = [t for t in tokens if t.token_type == TokenType.FRONTMATTER][0]
        assert "a: 1" in fm.value
        assert "c: 3" in fm.value


# ===========================================================================
# Paragraph
# ===========================================================================


class TestTokenizeParagraph:
    def test_basic(self):
        tokens = MarkdownLexer().tokenize("just text")
        assert tokens[0].token_type == TokenType.PARAGRAPH
        assert tokens[0].value == "just text"

    def test_multiple_lines(self):
        text = "line1\nline2"
        paras = [
            t for t in MarkdownLexer().tokenize(text)
            if t.token_type == TokenType.PARAGRAPH
        ]
        assert len(paras) == 2


# ===========================================================================
# tokenize_block dispatch
# ===========================================================================


class TestTokenizeBlock:
    def test_blank_is_newline(self):
        tok = MarkdownLexer().tokenize_block("", 1)
        assert tok.token_type == TokenType.NEWLINE

    def test_whitespace_is_newline(self):
        tok = MarkdownLexer().tokenize_block("   ", 1)
        assert tok.token_type == TokenType.NEWLINE

    def test_heading(self):
        tok = MarkdownLexer().tokenize_block("## Two", 5)
        assert tok.token_type == TokenType.HEADING
        assert tok.line_num == 5

    def test_paragraph_default(self):
        tok = MarkdownLexer().tokenize_block("hello world", 3)
        assert tok.token_type == TokenType.PARAGRAPH
        assert tok.line_num == 3


# ===========================================================================
# Inline: Bold
# ===========================================================================


class TestTokenizeInlineBold:
    def test_star_bold(self):
        toks = MarkdownLexer().tokenize_inline("**hi**")
        bolds = [t for t in toks if t.token_type == TokenType.BOLD]
        assert bolds and bolds[0].value == "hi"

    def test_underscore_bold(self):
        toks = MarkdownLexer().tokenize_inline("__hi__")
        bolds = [t for t in toks if t.token_type == TokenType.BOLD]
        assert bolds and bolds[0].value == "hi"

    def test_bold_in_text(self):
        toks = MarkdownLexer().tokenize_inline("a **bold** word")
        bolds = [t for t in toks if t.token_type == TokenType.BOLD]
        assert len(bolds) == 1


# ===========================================================================
# Inline: Italic
# ===========================================================================


class TestTokenizeInlineItalic:
    def test_star_italic(self):
        toks = MarkdownLexer().tokenize_inline("*it*")
        its = [t for t in toks if t.token_type == TokenType.ITALIC]
        assert its and its[0].value == "it"

    def test_underscore_italic(self):
        toks = MarkdownLexer().tokenize_inline("_it_")
        its = [t for t in toks if t.token_type == TokenType.ITALIC]
        assert its and its[0].value == "it"

    def test_italic_not_inside_bold(self):
        # **xx** should be bold, not italic
        toks = MarkdownLexer().tokenize_inline("**xx**")
        types = [t.token_type for t in toks]
        assert TokenType.BOLD in types
        assert TokenType.ITALIC not in types


# ===========================================================================
# Inline: Code
# ===========================================================================


class TestTokenizeInlineCode:
    def test_basic(self):
        toks = MarkdownLexer().tokenize_inline("`x = 1`")
        codes = [t for t in toks if t.token_type == TokenType.CODE_INLINE]
        assert codes and codes[0].value == "x = 1"

    def test_code_in_text(self):
        toks = MarkdownLexer().tokenize_inline("run `cmd` now")
        codes = [t for t in toks if t.token_type == TokenType.CODE_INLINE]
        assert len(codes) == 1


# ===========================================================================
# Inline: Link
# ===========================================================================


class TestTokenizeInlineLink:
    def test_basic(self):
        toks = MarkdownLexer().tokenize_inline("[txt](http://x.com)")
        links = [t for t in toks if t.token_type == TokenType.LINK]
        assert links
        assert links[0].metadata["url"] == "http://x.com"
        assert links[0].value == "txt"

    def test_link_with_title(self):
        toks = MarkdownLexer().tokenize_inline('[t](http://x "Title")')
        l = [t for t in toks if t.token_type == TokenType.LINK][0]
        assert l.metadata["title"] == "Title"


# ===========================================================================
# Inline: Image
# ===========================================================================


class TestTokenizeInlineImage:
    def test_basic(self):
        toks = MarkdownLexer().tokenize_inline("![alt](image.png)")
        imgs = [t for t in toks if t.token_type == TokenType.IMAGE]
        assert imgs
        assert imgs[0].metadata["alt"] == "alt"
        assert imgs[0].metadata["url"] == "image.png"

    def test_image_not_link(self):
        toks = MarkdownLexer().tokenize_inline("![alt](pic.png)")
        types = [t.token_type for t in toks]
        assert TokenType.IMAGE in types
        assert TokenType.LINK not in types


# ===========================================================================
# Inline: Strikethrough
# ===========================================================================


class TestTokenizeInlineStrike:
    def test_basic(self):
        toks = MarkdownLexer().tokenize_inline("~~gone~~")
        strikes = [t for t in toks if t.token_type == TokenType.STRIKETHROUGH]
        assert strikes and strikes[0].value == "gone"


# ===========================================================================
# iter_tokens
# ===========================================================================


class TestIterTokens:
    def test_yields_tokens(self):
        tokens = list(MarkdownLexer().iter_tokens("# H\n- a"))
        assert any(t.token_type == TokenType.HEADING for t in tokens)
        assert any(t.token_type == TokenType.LIST_ITEM for t in tokens)

    def test_is_iterator(self):
        it = MarkdownLexer().iter_tokens("text")
        assert hasattr(it, "__next__")


# ===========================================================================
# filter_by_type
# ===========================================================================


class TestFilterByType:
    def test_filter_headings(self):
        lex = MarkdownLexer()
        tokens = lex.tokenize("# A\n# B\ntext")
        headings = lex.filter_by_type(tokens, TokenType.HEADING)
        assert len(headings) == 2

    def test_filter_returns_empty_for_missing(self):
        lex = MarkdownLexer()
        tokens = lex.tokenize("text")
        result = lex.filter_by_type(tokens, TokenType.HEADING)
        assert result == []


# ===========================================================================
# to_dict_list
# ===========================================================================


class TestToDictList:
    def test_basic(self):
        lex = MarkdownLexer()
        tokens = lex.tokenize("# Title")
        out = lex.to_dict_list(tokens)
        assert isinstance(out, list)
        assert out[0]["token_type"] == "HEADING"
        assert out[0]["value"] == "Title"
        assert out[0]["metadata"]["level"] == 1

    def test_serializable(self):
        import json
        lex = MarkdownLexer()
        tokens = lex.tokenize("# H\n- a\ntext")
        out = lex.to_dict_list(tokens)
        s = json.dumps(out)
        assert "HEADING" in s

    def test_preserves_line_num(self):
        lex = MarkdownLexer()
        tokens = lex.tokenize("line1\n# Heading")
        out = lex.to_dict_list(tokens)
        heading_dict = [d for d in out if d["token_type"] == "HEADING"][0]
        assert heading_dict["line_num"] == 2


# ===========================================================================
# Edge cases
# ===========================================================================


class TestEdgeCases:
    def test_empty_text(self):
        assert MarkdownLexer().tokenize("") == []

    def test_only_newlines(self):
        tokens = MarkdownLexer().tokenize("\n\n\n")
        assert all(t.token_type == TokenType.NEWLINE for t in tokens)

    def test_mixed_inline(self):
        text = "**bold** and *italic* and `code`"
        toks = MarkdownLexer().tokenize_inline(text)
        types = {t.token_type for t in toks}
        assert TokenType.BOLD in types
        assert TokenType.ITALIC in types
        assert TokenType.CODE_INLINE in types

    def test_no_markup_inline(self):
        toks = MarkdownLexer().tokenize_inline("plain text only")
        assert len(toks) == 1
        assert toks[0].token_type == TokenType.TEXT
        assert toks[0].value == "plain text only"

    def test_empty_inline(self):
        assert MarkdownLexer().tokenize_inline("") == []

    def test_comment_single_line(self):
        tokens = MarkdownLexer().tokenize("<!-- a note -->")
        comments = [t for t in tokens if t.token_type == TokenType.COMMENT]
        assert comments and "a note" in comments[0].value

    def test_multiline_comment(self):
        text = "<!--\nhello\nworld\n-->"
        tokens = MarkdownLexer().tokenize(text)
        comments = [t for t in tokens if t.token_type == TokenType.COMMENT]
        assert comments

    def test_full_document(self):
        text = (
            "---\ntitle: T\n---\n"
            "# Heading\n"
            "\n"
            "Some **bold** text.\n"
            "\n"
            "- item 1\n"
            "- item 2\n"
            "\n"
            "1. one\n"
            "2. two\n"
            "\n"
            "> quote\n"
            "\n"
            "```python\ncode\n```\n"
            "\n"
            "| a | b |\n"
            "| c | d |\n"
            "\n"
            "---\n"
        )
        tokens = MarkdownLexer().tokenize(text)
        types = {t.token_type for t in tokens}
        for expected in (
            TokenType.FRONTMATTER, TokenType.HEADING, TokenType.PARAGRAPH,
            TokenType.LIST_ITEM, TokenType.NUMBERED_ITEM,
            TokenType.BLOCKQUOTE, TokenType.CODE_BLOCK,
            TokenType.TABLE_ROW, TokenType.HORIZONTAL_RULE,
        ):
            assert expected in types, f"missing {expected}"

    def test_text_between_inline_markup(self):
        toks = MarkdownLexer().tokenize_inline("hello **world** end")
        # Should have TEXT + BOLD + TEXT
        kinds = [t.token_type for t in toks]
        assert TokenType.BOLD in kinds
        assert TokenType.TEXT in kinds

    def test_link_url_in_metadata(self):
        toks = MarkdownLexer().tokenize_inline("see [docs](https://example.com)")
        links = [t for t in toks if t.token_type == TokenType.LINK]
        assert links[0].metadata["url"] == "https://example.com"
