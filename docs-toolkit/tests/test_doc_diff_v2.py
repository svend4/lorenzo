"""Tests for docstoolkit.doc_diff_v2."""

from __future__ import annotations

import pytest

from docstoolkit.doc_diff_v2 import (
    DiffChunk,
    DiffGranularity,
    DiffOp,
    DocDiffV2,
    StructuralDiff,
    WordDiffStats,
)


# ---------------------------------------------------------------------------
class TestDiffGranularity:
    def test_values(self):
        assert DiffGranularity.CHAR.value == "char"
        assert DiffGranularity.WORD.value == "word"
        assert DiffGranularity.LINE.value == "line"
        assert DiffGranularity.SENTENCE.value == "sentence"
        assert DiffGranularity.PARAGRAPH.value == "paragraph"

    def test_count(self):
        assert len(list(DiffGranularity)) == 5

    def test_str_enum(self):
        # str-based enum: value equals string
        assert DiffGranularity.WORD == "word"


# ---------------------------------------------------------------------------
class TestDiffOp:
    def test_values(self):
        assert DiffOp.EQUAL.value == "equal"
        assert DiffOp.INSERT.value == "insert"
        assert DiffOp.DELETE.value == "delete"
        assert DiffOp.REPLACE.value == "replace"

    def test_count(self):
        assert len(list(DiffOp)) == 4

    def test_can_be_constructed_from_difflib_tag(self):
        # difflib uses these exact strings
        for tag in ["equal", "insert", "delete", "replace"]:
            assert DiffOp(tag).value == tag


# ---------------------------------------------------------------------------
class TestDiffChunk:
    def test_defaults(self):
        c = DiffChunk(op=DiffOp.EQUAL)
        assert c.old_text == ""
        assert c.new_text == ""
        assert c.old_start == 0
        assert c.new_start == 0

    def test_construction(self):
        c = DiffChunk(
            op=DiffOp.REPLACE,
            old_text="a",
            new_text="b",
            old_start=1,
            new_start=2,
        )
        assert c.op == DiffOp.REPLACE
        assert c.old_text == "a"
        assert c.new_text == "b"
        assert c.old_start == 1
        assert c.new_start == 2


# ---------------------------------------------------------------------------
class TestStructuralDiffDataclass:
    def test_defaults(self):
        s = StructuralDiff()
        assert s.headings_added == []
        assert s.headings_removed == []
        assert s.headings_changed == []
        assert s.paragraphs_added == 0
        assert s.paragraphs_removed == 0
        assert s.code_blocks_added == 0
        assert s.code_blocks_removed == 0

    def test_construction(self):
        s = StructuralDiff(
            headings_added=["A"],
            headings_removed=["B"],
            headings_changed=[("X", "Y")],
            paragraphs_added=1,
            paragraphs_removed=2,
            code_blocks_added=3,
            code_blocks_removed=4,
        )
        assert s.headings_added == ["A"]
        assert s.headings_removed == ["B"]
        assert s.headings_changed == [("X", "Y")]
        assert s.paragraphs_added == 1
        assert s.code_blocks_added == 3


# ---------------------------------------------------------------------------
class TestWordDiffStats:
    def test_defaults(self):
        s = WordDiffStats()
        assert s.words_added == 0
        assert s.words_removed == 0
        assert s.words_unchanged == 0
        assert s.ratio == 0.0

    def test_construction(self):
        s = WordDiffStats(words_added=5, words_removed=3, words_unchanged=10, ratio=0.7)
        assert s.words_added == 5
        assert s.ratio == 0.7


# ---------------------------------------------------------------------------
class TestDiffChars:
    def test_identical(self):
        d = DocDiffV2()
        chunks = d.diff_chars("hello", "hello")
        assert len(chunks) == 1
        assert chunks[0].op == DiffOp.EQUAL
        assert chunks[0].old_text == "hello"
        assert chunks[0].new_text == "hello"

    def test_simple_replace(self):
        d = DocDiffV2()
        chunks = d.diff_chars("cat", "bat")
        # Should have a replace + equal "at"
        ops = [c.op for c in chunks]
        assert DiffOp.REPLACE in ops or (DiffOp.DELETE in ops and DiffOp.INSERT in ops)

    def test_empty_old(self):
        d = DocDiffV2()
        chunks = d.diff_chars("", "abc")
        assert len(chunks) == 1
        assert chunks[0].op == DiffOp.INSERT
        assert chunks[0].new_text == "abc"

    def test_empty_new(self):
        d = DocDiffV2()
        chunks = d.diff_chars("abc", "")
        assert len(chunks) == 1
        assert chunks[0].op == DiffOp.DELETE
        assert chunks[0].old_text == "abc"


# ---------------------------------------------------------------------------
class TestDiffWords:
    def test_identical(self):
        d = DocDiffV2()
        chunks = d.diff_words("hello world", "hello world")
        assert all(c.op == DiffOp.EQUAL for c in chunks)
        reconstructed = "".join(c.new_text for c in chunks)
        assert reconstructed == "hello world"

    def test_word_replace(self):
        d = DocDiffV2()
        chunks = d.diff_words("hello world", "hello there")
        ops = [c.op for c in chunks]
        # somewhere we should have an insert / delete / replace
        assert any(o != DiffOp.EQUAL for o in ops)
        # reconstruct
        reconstructed_old = "".join(c.old_text for c in chunks if c.op != DiffOp.INSERT)
        reconstructed_new = "".join(c.new_text for c in chunks if c.op != DiffOp.DELETE)
        assert reconstructed_old == "hello world"
        assert reconstructed_new == "hello there"

    def test_preserves_whitespace(self):
        d = DocDiffV2()
        chunks = d.diff_words("a  b", "a  b")
        reconstructed = "".join(c.new_text for c in chunks)
        assert reconstructed == "a  b"

    def test_word_insert(self):
        d = DocDiffV2()
        chunks = d.diff_words("hello", "hello world")
        # reconstruction sanity
        rec_new = "".join(c.new_text for c in chunks if c.op != DiffOp.DELETE)
        assert rec_new == "hello world"

    def test_empty(self):
        d = DocDiffV2()
        chunks = d.diff_words("", "")
        # Either empty list or single equal chunk
        assert len(chunks) <= 1


# ---------------------------------------------------------------------------
class TestDiffLines:
    def test_identical(self):
        d = DocDiffV2()
        chunks = d.diff_lines("line1\nline2\n", "line1\nline2\n")
        assert all(c.op == DiffOp.EQUAL for c in chunks)

    def test_line_added(self):
        d = DocDiffV2()
        chunks = d.diff_lines("a\nb\n", "a\nb\nc\n")
        ops = [c.op for c in chunks]
        assert DiffOp.INSERT in ops

    def test_line_removed(self):
        d = DocDiffV2()
        chunks = d.diff_lines("a\nb\nc\n", "a\nc\n")
        ops = [c.op for c in chunks]
        assert DiffOp.DELETE in ops

    def test_reconstruction(self):
        d = DocDiffV2()
        old = "a\nb\nc\n"
        new = "a\nx\nc\n"
        chunks = d.diff_lines(old, new)
        rec_old = "".join(c.old_text for c in chunks if c.op != DiffOp.INSERT)
        rec_new = "".join(c.new_text for c in chunks if c.op != DiffOp.DELETE)
        assert rec_old == old
        assert rec_new == new


# ---------------------------------------------------------------------------
class TestDiffSentences:
    def test_identical(self):
        d = DocDiffV2()
        chunks = d.diff_sentences("Hello. World.", "Hello. World.")
        assert all(c.op == DiffOp.EQUAL for c in chunks)

    def test_sentence_changed(self):
        d = DocDiffV2()
        chunks = d.diff_sentences("Hello. World.", "Hello. Mars.")
        ops = [c.op for c in chunks]
        assert any(o != DiffOp.EQUAL for o in ops)

    def test_empty(self):
        d = DocDiffV2()
        chunks = d.diff_sentences("", "")
        assert len(chunks) <= 1


# ---------------------------------------------------------------------------
class TestDiffParagraphs:
    def test_identical(self):
        d = DocDiffV2()
        chunks = d.diff_paragraphs("para1\n\npara2", "para1\n\npara2")
        assert all(c.op == DiffOp.EQUAL for c in chunks)

    def test_paragraph_added(self):
        d = DocDiffV2()
        chunks = d.diff_paragraphs("p1", "p1\n\np2")
        ops = [c.op for c in chunks]
        assert any(o in (DiffOp.INSERT, DiffOp.REPLACE) for o in ops)

    def test_empty(self):
        d = DocDiffV2()
        chunks = d.diff_paragraphs("", "")
        assert len(chunks) <= 1


# ---------------------------------------------------------------------------
class TestWordStats:
    def test_identical(self):
        d = DocDiffV2()
        s = d.word_stats("hello world foo", "hello world foo")
        assert s.words_added == 0
        assert s.words_removed == 0
        assert s.words_unchanged == 3
        assert s.ratio == 1.0

    def test_completely_different(self):
        d = DocDiffV2()
        s = d.word_stats("aaa bbb", "ccc ddd")
        assert s.words_added == 2
        assert s.words_removed == 2
        assert s.words_unchanged == 0

    def test_partial(self):
        d = DocDiffV2()
        s = d.word_stats("hello world", "hello there")
        assert s.words_unchanged == 1
        assert s.words_added >= 1
        assert s.words_removed >= 1

    def test_empty(self):
        d = DocDiffV2()
        s = d.word_stats("", "")
        assert s.words_added == 0
        assert s.words_removed == 0
        assert s.words_unchanged == 0

    def test_ratio_range(self):
        d = DocDiffV2()
        s = d.word_stats("hello world", "hello there")
        assert 0.0 <= s.ratio <= 1.0


# ---------------------------------------------------------------------------
class TestStructuralDiffMethod:
    def test_no_changes(self):
        d = DocDiffV2()
        text = "# A\n\npara\n\n# B"
        sd = d.structural_diff(text, text)
        assert sd.headings_added == []
        assert sd.headings_removed == []
        assert sd.headings_changed == []
        assert sd.paragraphs_added == 0
        assert sd.paragraphs_removed == 0

    def test_heading_added(self):
        d = DocDiffV2()
        sd = d.structural_diff("# A", "# A\n\n# B")
        assert "B" in sd.headings_added
        assert sd.headings_removed == []

    def test_heading_removed(self):
        d = DocDiffV2()
        sd = d.structural_diff("# A\n\n# B", "# A")
        assert "B" in sd.headings_removed
        assert sd.headings_added == []

    def test_heading_changed(self):
        d = DocDiffV2()
        sd = d.structural_diff("# Old Title", "# New Title")
        # Either as changed pair or as add+remove — implementation pairs them
        assert sd.headings_changed == [("Old Title", "New Title")]

    def test_paragraphs_added(self):
        d = DocDiffV2()
        sd = d.structural_diff("p1", "p1\n\np2\n\np3")
        assert sd.paragraphs_added == 2

    def test_paragraphs_removed(self):
        d = DocDiffV2()
        sd = d.structural_diff("p1\n\np2\n\np3", "p1")
        assert sd.paragraphs_removed == 2

    def test_code_blocks_added(self):
        d = DocDiffV2()
        old = "text"
        new = "text\n\n```\ncode\n```"
        sd = d.structural_diff(old, new)
        assert sd.code_blocks_added == 1

    def test_code_blocks_removed(self):
        d = DocDiffV2()
        old = "text\n\n```\ncode\n```"
        new = "text"
        sd = d.structural_diff(old, new)
        assert sd.code_blocks_removed == 1

    def test_multiple_heading_levels(self):
        d = DocDiffV2()
        sd = d.structural_diff("# A\n\n## B\n\n### C", "# A\n\n## B")
        assert "C" in sd.headings_removed


# ---------------------------------------------------------------------------
class TestInlineHtml:
    def test_no_changes(self):
        d = DocDiffV2()
        html = d.inline_html("hello world", "hello world")
        assert html == "hello world"
        assert "<ins>" not in html
        assert "<del>" not in html

    def test_pure_insert(self):
        d = DocDiffV2()
        html = d.inline_html("hello", "hello world")
        assert "<ins>" in html

    def test_pure_delete(self):
        d = DocDiffV2()
        html = d.inline_html("hello world", "hello")
        assert "<del>" in html

    def test_replace(self):
        d = DocDiffV2()
        html = d.inline_html("hello world", "hello there")
        # Replace renders both del and ins
        assert "<del>" in html
        assert "<ins>" in html

    def test_char_granularity(self):
        d = DocDiffV2()
        html = d.inline_html("cat", "bat", DiffGranularity.CHAR)
        assert "<del>" in html or "<ins>" in html

    def test_contains_old_and_new_text(self):
        d = DocDiffV2()
        html = d.inline_html("hello world", "hello there")
        assert "world" in html
        assert "there" in html


# ---------------------------------------------------------------------------
class TestInlineMarkdown:
    def test_no_changes(self):
        d = DocDiffV2()
        md = d.inline_markdown("hello", "hello")
        assert md == "hello"

    def test_insert_marker(self):
        d = DocDiffV2()
        md = d.inline_markdown("hello", "hello world")
        assert "+" in md

    def test_delete_marker(self):
        d = DocDiffV2()
        md = d.inline_markdown("hello world", "hello")
        assert "-" in md

    def test_replace_has_both_markers(self):
        d = DocDiffV2()
        md = d.inline_markdown("hello world", "hello there")
        assert "-" in md
        assert "+" in md


# ---------------------------------------------------------------------------
class TestSummary:
    def test_no_changes(self):
        d = DocDiffV2()
        s = d.summary("hello", "hello")
        assert s["words_added"] == 0
        assert s["words_removed"] == 0
        assert s["ratio"] == 1.0
        assert s["old_length"] == 5
        assert s["new_length"] == 5

    def test_full_change(self):
        d = DocDiffV2()
        s = d.summary("aaa bbb", "ccc ddd")
        assert s["words_added"] == 2
        assert s["words_removed"] == 2

    def test_keys_present(self):
        d = DocDiffV2()
        s = d.summary("a", "b")
        for k in [
            "words_added",
            "words_removed",
            "words_unchanged",
            "ratio",
            "headings_added",
            "headings_removed",
            "headings_changed",
            "paragraphs_added",
            "paragraphs_removed",
            "code_blocks_added",
            "code_blocks_removed",
            "lines_added",
            "lines_removed",
            "old_length",
            "new_length",
        ]:
            assert k in s

    def test_summary_with_headings(self):
        d = DocDiffV2()
        s = d.summary("# A", "# A\n\n# B")
        assert s["headings_added"] == 1


# ---------------------------------------------------------------------------
class TestDispatcherDiff:
    def test_default_is_word(self):
        d = DocDiffV2()
        a = d.diff("hello world", "hello there")
        b = d.diff_words("hello world", "hello there")
        assert [(c.op, c.old_text, c.new_text) for c in a] == [
            (c.op, c.old_text, c.new_text) for c in b
        ]

    def test_char_dispatch(self):
        d = DocDiffV2()
        a = d.diff("cat", "bat", DiffGranularity.CHAR)
        b = d.diff_chars("cat", "bat")
        assert [(c.op, c.old_text, c.new_text) for c in a] == [
            (c.op, c.old_text, c.new_text) for c in b
        ]

    def test_line_dispatch(self):
        d = DocDiffV2()
        a = d.diff("a\nb\n", "a\nc\n", DiffGranularity.LINE)
        b = d.diff_lines("a\nb\n", "a\nc\n")
        assert [(c.op, c.old_text, c.new_text) for c in a] == [
            (c.op, c.old_text, c.new_text) for c in b
        ]

    def test_sentence_dispatch(self):
        d = DocDiffV2()
        a = d.diff("A. B.", "A. C.", DiffGranularity.SENTENCE)
        b = d.diff_sentences("A. B.", "A. C.")
        assert [(c.op, c.old_text, c.new_text) for c in a] == [
            (c.op, c.old_text, c.new_text) for c in b
        ]

    def test_paragraph_dispatch(self):
        d = DocDiffV2()
        a = d.diff("p1\n\np2", "p1\n\np3", DiffGranularity.PARAGRAPH)
        b = d.diff_paragraphs("p1\n\np2", "p1\n\np3")
        assert [(c.op, c.old_text, c.new_text) for c in a] == [
            (c.op, c.old_text, c.new_text) for c in b
        ]


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_strings(self):
        d = DocDiffV2()
        for g in DiffGranularity:
            chunks = d.diff("", "", g)
            assert chunks == [] or all(c.op == DiffOp.EQUAL for c in chunks)

    def test_inline_html_empty(self):
        d = DocDiffV2()
        assert d.inline_html("", "") == ""

    def test_inline_markdown_empty(self):
        d = DocDiffV2()
        assert d.inline_markdown("", "") == ""

    def test_summary_empty(self):
        d = DocDiffV2()
        s = d.summary("", "")
        assert s["words_added"] == 0
        assert s["words_removed"] == 0
        assert s["old_length"] == 0
        assert s["new_length"] == 0

    def test_unicode(self):
        d = DocDiffV2()
        chunks = d.diff_words("привет мир", "привет тут")
        rec_new = "".join(c.new_text for c in chunks if c.op != DiffOp.DELETE)
        assert rec_new == "привет тут"

    def test_unicode_html(self):
        d = DocDiffV2()
        html = d.inline_html("привет мир", "привет тут")
        assert "тут" in html

    def test_long_input(self):
        d = DocDiffV2()
        old = " ".join(f"w{i}" for i in range(200))
        new = " ".join(f"w{i}" for i in range(200))
        s = d.word_stats(old, new)
        assert s.words_unchanged == 200
        assert s.ratio == 1.0

    def test_structural_only_whitespace_paragraphs(self):
        d = DocDiffV2()
        sd = d.structural_diff("", "")
        assert sd.paragraphs_added == 0
        assert sd.paragraphs_removed == 0

    def test_invalid_granularity_raises(self):
        d = DocDiffV2()
        with pytest.raises((ValueError, AttributeError)):
            d.diff("a", "b", "bogus")  # type: ignore[arg-type]
