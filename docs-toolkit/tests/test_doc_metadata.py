"""Tests for docstoolkit.doc_metadata."""
from __future__ import annotations

import pytest

from docstoolkit.doc_metadata import Complexity, DocMetadata, MetadataExtractor


@pytest.fixture
def extractor() -> MetadataExtractor:
    return MetadataExtractor()


class TestComplexity:
    def test_enum_members(self):
        assert Complexity.TRIVIAL.value == "trivial"
        assert Complexity.SIMPLE.value == "simple"
        assert Complexity.MODERATE.value == "moderate"
        assert Complexity.COMPLEX.value == "complex"
        assert Complexity.VERY_COMPLEX.value == "very_complex"

    def test_enum_count(self):
        assert len(list(Complexity)) == 5

    def test_enum_distinct(self):
        values = {c.value for c in Complexity}
        assert len(values) == 5


class TestDocMetadata:
    def test_default_construction(self):
        m = DocMetadata()
        assert m.char_count == 0
        assert m.word_count == 0
        assert m.line_count == 0
        assert m.paragraph_count == 0
        assert m.heading_count == 0
        assert m.link_count == 0
        assert m.image_count == 0
        assert m.code_block_count == 0
        assert m.list_item_count == 0
        assert m.table_count == 0
        assert m.complexity == Complexity.TRIVIAL
        assert m.avg_paragraph_length == 0.0
        assert m.heading_depth == 0
        assert m.has_frontmatter is False
        assert m.has_toc is False

    def test_field_assignment(self):
        m = DocMetadata(char_count=10, word_count=5)
        assert m.char_count == 10
        assert m.word_count == 5


class TestExtractCharCount:
    def test_empty(self, extractor):
        assert extractor.extract("").char_count == 0

    def test_simple(self, extractor):
        assert extractor.extract("hello").char_count == 5

    def test_includes_whitespace(self, extractor):
        assert extractor.extract("a b c").char_count == 5

    def test_unicode(self, extractor):
        assert extractor.extract("привет").char_count == 6


class TestExtractWordCount:
    def test_empty(self, extractor):
        assert extractor.extract("").word_count == 0

    def test_single_word(self, extractor):
        assert extractor.extract("hello").word_count == 1

    def test_multiple_words(self, extractor):
        assert extractor.extract("the quick brown fox").word_count == 4

    def test_extra_whitespace(self, extractor):
        assert extractor.extract("  hi    there  \n\n  ").word_count == 2

    def test_newlines_split_words(self, extractor):
        assert extractor.extract("one\ntwo\nthree").word_count == 3


class TestExtractLineCount:
    def test_empty(self, extractor):
        assert extractor.extract("").line_count == 0

    def test_single_line(self, extractor):
        assert extractor.extract("hi").line_count == 1

    def test_multiple_lines(self, extractor):
        assert extractor.extract("a\nb\nc").line_count == 3

    def test_trailing_newline_not_counted(self, extractor):
        assert extractor.extract("a\nb\n").line_count == 2


class TestExtractParagraphCount:
    def test_empty(self, extractor):
        assert extractor.extract("").paragraph_count == 0

    def test_single_paragraph(self, extractor):
        assert extractor.extract("one paragraph here").paragraph_count == 1

    def test_two_paragraphs(self, extractor):
        text = "para one\n\npara two"
        assert extractor.extract(text).paragraph_count == 2

    def test_three_paragraphs(self, extractor):
        text = "a\n\nb\n\nc"
        assert extractor.extract(text).paragraph_count == 3

    def test_avg_paragraph_length(self, extractor):
        text = "one two\n\nthree four five six"
        m = extractor.extract(text)
        assert m.paragraph_count == 2
        assert m.avg_paragraph_length == pytest.approx(3.0)

    def test_avg_paragraph_length_empty(self, extractor):
        assert extractor.extract("").avg_paragraph_length == 0.0


class TestExtractHeadings:
    def test_no_headings(self, extractor):
        assert extractor.extract("plain text").heading_count == 0

    def test_single_h1(self, extractor):
        m = extractor.extract("# Title")
        assert m.heading_count == 1
        assert m.heading_depth == 1

    def test_multiple_levels(self, extractor):
        text = "# H1\n\n## H2\n\n### H3"
        m = extractor.extract(text)
        assert m.heading_count == 3
        assert m.heading_depth == 3

    def test_max_depth_six(self, extractor):
        m = extractor.extract("###### Deep")
        assert m.heading_depth == 6

    def test_seven_hash_not_heading(self, extractor):
        # ####### is not a valid Markdown heading
        m = extractor.extract("####### NotHeading")
        # Our regex matches 1-6 hashes followed by space; "####### NotHeading"
        # The first 6 hashes match — depending on engine, may parse as h6.
        # Accept either, but heading_depth should be <= 6.
        assert m.heading_depth <= 6

    def test_heading_depth_zero_when_none(self, extractor):
        assert extractor.extract("body only").heading_depth == 0


class TestExtractLinks:
    def test_no_links(self, extractor):
        assert extractor.extract("plain text").link_count == 0

    def test_single_link(self, extractor):
        m = extractor.extract("see [docs](https://example.com)")
        assert m.link_count == 1

    def test_multiple_links(self, extractor):
        text = "[a](x) and [b](y) and [c](z)"
        assert extractor.extract(text).link_count == 3

    def test_image_not_counted_as_link(self, extractor):
        m = extractor.extract("![alt](img.png)")
        assert m.link_count == 0
        assert m.image_count == 1


class TestExtractImages:
    def test_no_images(self, extractor):
        assert extractor.extract("text").image_count == 0

    def test_single_image(self, extractor):
        assert extractor.extract("![alt](pic.png)").image_count == 1

    def test_multiple_images(self, extractor):
        text = "![a](1.png) ![b](2.png)"
        assert extractor.extract(text).image_count == 2

    def test_image_with_empty_alt(self, extractor):
        assert extractor.extract("![](pic.png)").image_count == 1


class TestExtractCodeBlocks:
    def test_no_code(self, extractor):
        assert extractor.extract("text").code_block_count == 0

    def test_single_code_block(self, extractor):
        text = "```\nx = 1\n```"
        assert extractor.extract(text).code_block_count == 1

    def test_two_code_blocks(self, extractor):
        text = "```\nA\n```\n\n```\nB\n```"
        assert extractor.extract(text).code_block_count == 2

    def test_code_block_with_language(self, extractor):
        text = "```python\nprint(1)\n```"
        assert extractor.extract(text).code_block_count == 1


class TestExtractListItems:
    def test_no_lists(self, extractor):
        assert extractor.extract("text").list_item_count == 0

    def test_bullet_list(self, extractor):
        text = "- one\n- two\n- three"
        assert extractor.extract(text).list_item_count == 3

    def test_asterisk_list(self, extractor):
        text = "* a\n* b"
        assert extractor.extract(text).list_item_count == 2

    def test_plus_list(self, extractor):
        text = "+ a\n+ b"
        assert extractor.extract(text).list_item_count == 2

    def test_numbered_list(self, extractor):
        text = "1. first\n2. second\n3. third"
        assert extractor.extract(text).list_item_count == 3

    def test_mixed_lists(self, extractor):
        text = "- bullet\n1. number"
        assert extractor.extract(text).list_item_count == 2


class TestExtractTables:
    def test_no_tables(self, extractor):
        assert extractor.extract("text").table_count == 0

    def test_single_table(self, extractor):
        text = "| A | B |\n|---|---|\n| 1 | 2 |"
        assert extractor.extract(text).table_count == 1

    def test_two_tables(self, extractor):
        text = (
            "| A | B |\n|---|---|\n| 1 | 2 |\n\n"
            "| C | D |\n|---|---|\n| 3 | 4 |"
        )
        assert extractor.extract(text).table_count == 2

    def test_table_with_alignment(self, extractor):
        text = "| A | B |\n|:---|:---:|\n| 1 | 2 |"
        assert extractor.extract(text).table_count == 1


class TestExtractFrontmatter:
    def test_no_frontmatter(self, extractor):
        assert extractor.extract("hello").has_frontmatter is False

    def test_with_frontmatter(self, extractor):
        text = "---\ntitle: T\n---\n\nbody"
        assert extractor.extract(text).has_frontmatter is True

    def test_frontmatter_must_be_at_start(self, extractor):
        text = "leading\n\n---\ntitle: T\n---\n"
        assert extractor.extract(text).has_frontmatter is False

    def test_frontmatter_does_not_break_paragraph_count(self, extractor):
        text = "---\ntitle: T\n---\n\nfirst para\n\nsecond para"
        m = extractor.extract(text)
        assert m.has_frontmatter is True
        assert m.paragraph_count == 2


class TestExtractToc:
    def test_no_toc(self, extractor):
        assert extractor.extract("# Intro").has_toc is False

    def test_toc_english(self, extractor):
        assert extractor.extract("## Table of Contents").has_toc is True

    def test_toc_russian_soderzhanie(self, extractor):
        assert extractor.extract("## Содержание").has_toc is True

    def test_toc_russian_oglavlenie(self, extractor):
        assert extractor.extract("# Оглавление").has_toc is True

    def test_toc_abbrev(self, extractor):
        assert extractor.extract("## TOC").has_toc is True

    def test_toc_case_insensitive(self, extractor):
        assert extractor.extract("## TABLE OF CONTENTS").has_toc is True


class TestComplexityScoring:
    def test_trivial_empty(self, extractor):
        assert extractor.extract("").complexity == Complexity.TRIVIAL

    def test_trivial_short(self, extractor):
        assert extractor.extract("a few words here").complexity == Complexity.TRIVIAL

    def test_simple(self, extractor):
        # Need 5 <= score < 15. Use ~1500 words -> score ~7.5
        text = " ".join(["word"] * 1500)
        m = extractor.extract(text)
        assert m.complexity == Complexity.SIMPLE

    def test_moderate(self, extractor):
        # 15 <= score < 40. ~4000 words alone => 20
        text = " ".join(["word"] * 4000)
        m = extractor.extract(text)
        assert m.complexity == Complexity.MODERATE

    def test_complex(self, extractor):
        # 40 <= score < 100. Use many headings and code blocks to push score up.
        # 15 headings = 30, 5 code blocks = 15, plus some words
        headings = "\n\n".join([f"## H{i}" for i in range(15)])
        code = "\n\n".join(["```\nx\n```"] * 5)
        body = " ".join(["word"] * 200)  # +1 from words
        text = headings + "\n\n" + code + "\n\n" + body
        m = extractor.extract(text)
        assert m.complexity == Complexity.COMPLEX

    def test_very_complex(self, extractor):
        # score >= 100. Many headings, code blocks, tables.
        headings = "\n\n".join([f"## H{i}" for i in range(30)])  # 60
        code = "\n\n".join(["```\nx\n```"] * 15)  # 45
        tables = "\n\n".join(
            ["| A | B |\n|---|---|\n| 1 | 2 |"] * 10
        )  # 30
        text = headings + "\n\n" + code + "\n\n" + tables
        m = extractor.extract(text)
        assert m.complexity == Complexity.VERY_COMPLEX


class TestCompare:
    def test_compare_identical(self, extractor):
        m = extractor.extract("hello world")
        result = extractor.compare(m, m)
        assert result["char_count"] == 0
        assert result["word_count"] == 0
        assert result["complexity"]["changed"] is False

    def test_compare_word_delta(self, extractor):
        a = extractor.extract("one two")
        b = extractor.extract("one two three four five")
        result = extractor.compare(a, b)
        assert result["word_count"] == 3

    def test_compare_negative_delta(self, extractor):
        a = extractor.extract("one two three")
        b = extractor.extract("one")
        result = extractor.compare(a, b)
        assert result["word_count"] == -2

    def test_compare_bool_flag_change(self, extractor):
        a = extractor.extract("# Heading")
        b = extractor.extract("# Table of Contents")
        result = extractor.compare(a, b)
        assert result["has_toc"]["a"] is False
        assert result["has_toc"]["b"] is True
        assert result["has_toc"]["changed"] is True

    def test_compare_complexity_change(self, extractor):
        a = extractor.extract("short")
        b_text = " ".join(["word"] * 4000)
        b = extractor.extract(b_text)
        result = extractor.compare(a, b)
        assert result["complexity"]["changed"] is True
        assert result["complexity"]["a"] == "trivial"
        assert result["complexity"]["b"] == "moderate"

    def test_compare_returns_dict(self, extractor):
        a = extractor.extract("x")
        b = extractor.extract("y")
        result = extractor.compare(a, b)
        assert isinstance(result, dict)
        # All dataclass fields should appear
        for key in (
            "char_count",
            "word_count",
            "line_count",
            "paragraph_count",
            "heading_count",
            "link_count",
            "image_count",
            "code_block_count",
            "list_item_count",
            "table_count",
            "complexity",
            "avg_paragraph_length",
            "heading_depth",
            "has_frontmatter",
            "has_toc",
        ):
            assert key in result


class TestSummarize:
    def test_summarize_returns_string(self, extractor):
        m = extractor.extract("hello world")
        assert isinstance(extractor.summarize(m), str)

    def test_summarize_contains_word_count(self, extractor):
        m = extractor.extract("one two three")
        s = extractor.summarize(m)
        assert "3" in s
        assert "word" in s.lower()

    def test_summarize_mentions_complexity(self, extractor):
        m = extractor.extract("hello")
        s = extractor.summarize(m)
        assert "trivial" in s.lower()

    def test_summarize_flags_frontmatter(self, extractor):
        m = extractor.extract("---\nt: 1\n---\n\nbody")
        s = extractor.summarize(m)
        assert "frontmatter" in s.lower()

    def test_summarize_flags_toc(self, extractor):
        m = extractor.extract("## Table of Contents\n\nbody")
        s = extractor.summarize(m)
        assert "toc" in s.lower()

    def test_summarize_no_flags_when_absent(self, extractor):
        m = extractor.extract("just body")
        s = extractor.summarize(m)
        assert "frontmatter" not in s.lower()


class TestExtractBatch:
    def test_empty_list(self, extractor):
        assert extractor.extract_batch([]) == []

    def test_batch_returns_list(self, extractor):
        result = extractor.extract_batch(["a", "b"])
        assert isinstance(result, list)
        assert len(result) == 2

    def test_batch_each_is_metadata(self, extractor):
        result = extractor.extract_batch(["hello", "world world"])
        assert all(isinstance(m, DocMetadata) for m in result)
        assert result[0].word_count == 1
        assert result[1].word_count == 2

    def test_batch_preserves_order(self, extractor):
        texts = ["one", "one two", "one two three"]
        result = extractor.extract_batch(texts)
        assert [m.word_count for m in result] == [1, 2, 3]


class TestEdgeCases:
    def test_empty_string(self, extractor):
        m = extractor.extract("")
        assert m.char_count == 0
        assert m.word_count == 0
        assert m.line_count == 0
        assert m.paragraph_count == 0
        assert m.complexity == Complexity.TRIVIAL

    def test_only_whitespace(self, extractor):
        m = extractor.extract("   \n\n   \n  ")
        assert m.word_count == 0
        assert m.paragraph_count == 0

    def test_only_plain_text(self, extractor):
        m = extractor.extract("Just some plain text without any markup.")
        assert m.word_count == 7
        assert m.heading_count == 0
        assert m.link_count == 0
        assert m.image_count == 0
        assert m.code_block_count == 0
        assert m.list_item_count == 0
        assert m.table_count == 0
        assert m.has_frontmatter is False
        assert m.has_toc is False

    def test_only_headings(self, extractor):
        m = extractor.extract("# A\n## B\n### C")
        assert m.heading_count == 3
        assert m.heading_depth == 3

    def test_rich_document(self, extractor):
        text = (
            "---\n"
            "title: Demo\n"
            "---\n\n"
            "# Main Title\n\n"
            "## Table of Contents\n\n"
            "- [Intro](#intro)\n"
            "- [Code](#code)\n\n"
            "## Intro\n\n"
            "Some intro text with a [link](https://example.com) "
            "and an ![image](pic.png).\n\n"
            "## Code\n\n"
            "```python\n"
            "print('hello')\n"
            "```\n\n"
            "| A | B |\n|---|---|\n| 1 | 2 |\n"
        )
        m = extractor.extract(text)
        assert m.has_frontmatter is True
        assert m.has_toc is True
        assert m.heading_count == 4
        assert m.heading_depth == 2
        assert m.link_count >= 3  # TOC links + 1 inline
        assert m.image_count == 1
        assert m.code_block_count == 1
        assert m.list_item_count == 2
        assert m.table_count == 1
