"""Tests for docstoolkit.doc_diff_summary."""
from __future__ import annotations

import pytest

from docstoolkit.doc_diff_summary import (
    ChangeMagnitude,
    ChangeTypeStats,
    DiffSummary,
    DocDiffSummarizer,
)


# ---------------------------------------------------------------------------
# ChangeMagnitude
# ---------------------------------------------------------------------------

class TestChangeMagnitude:
    def test_has_trivial(self):
        assert ChangeMagnitude.TRIVIAL.value == "TRIVIAL"

    def test_has_minor(self):
        assert ChangeMagnitude.MINOR.value == "MINOR"

    def test_has_major(self):
        assert ChangeMagnitude.MAJOR.value == "MAJOR"

    def test_has_rewrite(self):
        assert ChangeMagnitude.REWRITE.value == "REWRITE"

    def test_distinct_members(self):
        members = {m for m in ChangeMagnitude}
        assert len(members) == 4


# ---------------------------------------------------------------------------
# DiffSummary
# ---------------------------------------------------------------------------

class TestDiffSummary:
    def test_default_construction(self):
        s = DiffSummary()
        assert s.lines_added == 0
        assert s.lines_removed == 0
        assert s.lines_modified == 0
        assert s.chars_added == 0
        assert s.chars_removed == 0
        assert s.sections_changed == []
        assert s.magnitude == ChangeMagnitude.TRIVIAL
        assert s.similarity == 1.0
        assert s.is_rename is False
        assert s.has_structural_changes is False

    def test_custom_values(self):
        s = DiffSummary(
            lines_added=5,
            lines_removed=3,
            magnitude=ChangeMagnitude.MAJOR,
            similarity=0.5,
        )
        assert s.lines_added == 5
        assert s.lines_removed == 3
        assert s.magnitude == ChangeMagnitude.MAJOR
        assert s.similarity == 0.5

    def test_sections_changed_isolated(self):
        a = DiffSummary()
        b = DiffSummary()
        a.sections_changed.append("Intro")
        assert b.sections_changed == []


# ---------------------------------------------------------------------------
# ChangeTypeStats
# ---------------------------------------------------------------------------

class TestChangeTypeStats:
    def test_default_construction(self):
        c = ChangeTypeStats()
        assert c.code_blocks_changed == 0
        assert c.links_changed == 0
        assert c.headings_changed == 0
        assert c.lists_changed == 0
        assert c.tables_changed == 0

    def test_custom_values(self):
        c = ChangeTypeStats(headings_changed=2, links_changed=3)
        assert c.headings_changed == 2
        assert c.links_changed == 3


# ---------------------------------------------------------------------------
# Basic
# ---------------------------------------------------------------------------

class TestSummarizeBasic:
    def test_identical(self):
        s = DocDiffSummarizer().summarize("hello", "hello")
        assert s.lines_added == 0
        assert s.lines_removed == 0
        assert s.similarity == 1.0
        assert s.magnitude == ChangeMagnitude.TRIVIAL

    def test_returns_diff_summary(self):
        s = DocDiffSummarizer().summarize("a", "b")
        assert isinstance(s, DiffSummary)

    def test_empty_to_empty(self):
        s = DocDiffSummarizer().summarize("", "")
        assert s.similarity == 1.0
        assert s.lines_added == 0
        assert s.lines_removed == 0


# ---------------------------------------------------------------------------
# Added
# ---------------------------------------------------------------------------

class TestSummarizeAdded:
    def test_single_line_added(self):
        s = DocDiffSummarizer().summarize("a", "a\nb")
        assert s.lines_added == 1
        assert s.lines_removed == 0

    def test_multiple_lines_added(self):
        s = DocDiffSummarizer().summarize("a", "a\nb\nc\nd")
        assert s.lines_added == 3

    def test_added_from_empty(self):
        s = DocDiffSummarizer().summarize("", "new content\nmore")
        assert s.lines_added >= 1
        assert s.lines_removed == 0

    def test_chars_added_tracked(self):
        s = DocDiffSummarizer().summarize("a", "a\nbcdef")
        assert s.chars_added >= 5


# ---------------------------------------------------------------------------
# Removed
# ---------------------------------------------------------------------------

class TestSummarizeRemoved:
    def test_single_line_removed(self):
        s = DocDiffSummarizer().summarize("a\nb", "a")
        assert s.lines_removed == 1
        assert s.lines_added == 0

    def test_multiple_lines_removed(self):
        s = DocDiffSummarizer().summarize("a\nb\nc\nd", "a")
        assert s.lines_removed == 3

    def test_removed_to_empty(self):
        s = DocDiffSummarizer().summarize("old content\nmore", "")
        assert s.lines_removed >= 1
        assert s.lines_added == 0

    def test_chars_removed_tracked(self):
        s = DocDiffSummarizer().summarize("a\nbcdef", "a")
        assert s.chars_removed >= 5


# ---------------------------------------------------------------------------
# Modified
# ---------------------------------------------------------------------------

class TestSummarizeModified:
    def test_modified_line(self):
        s = DocDiffSummarizer().summarize("hello", "world")
        # Either modified=1, or 1 add + 1 remove — depends on opcode classification
        assert s.lines_modified + s.lines_added + s.lines_removed >= 1

    def test_modified_one_of_many(self):
        old = "a\nb\nc\nd"
        new = "a\nX\nc\nd"
        s = DocDiffSummarizer().summarize(old, new)
        assert s.lines_modified >= 1

    def test_modified_with_chars(self):
        s = DocDiffSummarizer().summarize("hello", "helloo")
        assert s.chars_added > 0 or s.chars_removed > 0


# ---------------------------------------------------------------------------
# Similarity
# ---------------------------------------------------------------------------

class TestSimilarity:
    def test_identical_is_one(self):
        s = DocDiffSummarizer().summarize("abc", "abc")
        assert s.similarity == 1.0

    def test_completely_different(self):
        s = DocDiffSummarizer().summarize("a" * 100, "z" * 100)
        assert s.similarity < 0.1

    def test_partial_overlap_in_range(self):
        s = DocDiffSummarizer().summarize("hello world", "hello earth")
        assert 0.0 <= s.similarity <= 1.0

    def test_within_range(self):
        s = DocDiffSummarizer().summarize("aaaa", "aabb")
        assert 0.0 <= s.similarity <= 1.0


# ---------------------------------------------------------------------------
# Magnitude — TRIVIAL
# ---------------------------------------------------------------------------

class TestMagnitudeTrivial:
    def test_identical_is_trivial(self):
        s = DocDiffSummarizer().summarize("hello world", "hello world")
        assert s.magnitude == ChangeMagnitude.TRIVIAL

    def test_almost_identical_is_trivial(self):
        old = "a" * 100
        new = "a" * 100 + "b"  # ~99.5% similar
        s = DocDiffSummarizer().summarize(old, new)
        assert s.magnitude == ChangeMagnitude.TRIVIAL


# ---------------------------------------------------------------------------
# Magnitude — MINOR
# ---------------------------------------------------------------------------

class TestMagnitudeMinor:
    def test_minor_change(self):
        # ~80% similar
        old = "a" * 80
        new = "a" * 80 + "b" * 20
        s = DocDiffSummarizer().summarize(old, new)
        assert s.magnitude == ChangeMagnitude.MINOR


# ---------------------------------------------------------------------------
# Magnitude — MAJOR
# ---------------------------------------------------------------------------

class TestMagnitudeMajor:
    def test_major_change(self):
        # ~50% similar
        old = "a" * 50
        new = "a" * 50 + "z" * 50
        s = DocDiffSummarizer().summarize(old, new)
        assert s.magnitude == ChangeMagnitude.MAJOR


# ---------------------------------------------------------------------------
# Magnitude — REWRITE
# ---------------------------------------------------------------------------

class TestMagnitudeRewrite:
    def test_rewrite_completely_different(self):
        s = DocDiffSummarizer().summarize("a" * 100, "z" * 100)
        assert s.magnitude == ChangeMagnitude.REWRITE

    def test_rewrite_low_similarity(self):
        old = "the quick brown fox jumps over the lazy dog"
        new = "X" * 200
        s = DocDiffSummarizer().summarize(old, new)
        assert s.magnitude == ChangeMagnitude.REWRITE


# ---------------------------------------------------------------------------
# Structural
# ---------------------------------------------------------------------------

class TestStructuralChanges:
    def test_no_structural_when_same_headings(self):
        old = "# A\ntext"
        new = "# A\nother text"
        s = DocDiffSummarizer().summarize(old, new)
        assert s.has_structural_changes is False

    def test_structural_when_heading_added(self):
        old = "# A\ntext"
        new = "# A\ntext\n## B\nmore"
        s = DocDiffSummarizer().summarize(old, new)
        assert s.has_structural_changes is True
        assert "B" in s.sections_changed

    def test_structural_when_heading_removed(self):
        old = "# A\ntext\n## B\nmore"
        new = "# A\ntext"
        s = DocDiffSummarizer().summarize(old, new)
        assert s.has_structural_changes is True
        assert "B" in s.sections_changed

    def test_no_headings(self):
        s = DocDiffSummarizer().summarize("plain text", "plain text changed")
        assert s.has_structural_changes is False


# ---------------------------------------------------------------------------
# change_types
# ---------------------------------------------------------------------------

class TestChangeTypes:
    def test_returns_change_type_stats(self):
        c = DocDiffSummarizer().change_types("a", "b")
        assert isinstance(c, ChangeTypeStats)

    def test_no_changes(self):
        c = DocDiffSummarizer().change_types("hello", "hello")
        assert c.headings_changed == 0
        assert c.links_changed == 0
        assert c.code_blocks_changed == 0
        assert c.lists_changed == 0
        assert c.tables_changed == 0

    def test_heading_added(self):
        c = DocDiffSummarizer().change_types("text", "# Title\ntext")
        assert c.headings_changed >= 1

    def test_link_added(self):
        old = "see docs"
        new = "see [docs](http://example.com)"
        c = DocDiffSummarizer().change_types(old, new)
        assert c.links_changed >= 1

    def test_link_removed(self):
        old = "see [docs](http://example.com)"
        new = "see docs"
        c = DocDiffSummarizer().change_types(old, new)
        assert c.links_changed >= 1

    def test_code_block_added(self):
        old = "text"
        new = "text\n```python\nprint('hi')\n```"
        c = DocDiffSummarizer().change_types(old, new)
        assert c.code_blocks_changed >= 1

    def test_list_items_added(self):
        old = "intro"
        new = "intro\n- one\n- two\n- three"
        c = DocDiffSummarizer().change_types(old, new)
        assert c.lists_changed >= 1

    def test_table_added(self):
        old = "intro"
        new = "intro\n| a | b |\n| - | - |\n| 1 | 2 |"
        c = DocDiffSummarizer().change_types(old, new)
        assert c.tables_changed >= 1


# ---------------------------------------------------------------------------
# extract_changed_sections
# ---------------------------------------------------------------------------

class TestExtractChangedSections:
    def test_no_sections_when_identical(self):
        out = DocDiffSummarizer().extract_changed_sections("# A\nx", "# A\nx")
        assert out == []

    def test_added_section(self):
        out = DocDiffSummarizer().extract_changed_sections(
            "# A\nx", "# A\nx\n## B\ny"
        )
        assert "B" in out

    def test_removed_section(self):
        out = DocDiffSummarizer().extract_changed_sections(
            "# A\nx\n## B\ny", "# A\nx"
        )
        assert "B" in out

    def test_both_added_and_removed(self):
        out = DocDiffSummarizer().extract_changed_sections(
            "# Old\nx", "# New\ny"
        )
        assert "Old" in out
        assert "New" in out

    def test_returns_list(self):
        out = DocDiffSummarizer().extract_changed_sections("a", "b")
        assert isinstance(out, list)


# ---------------------------------------------------------------------------
# summary_text
# ---------------------------------------------------------------------------

class TestSummaryText:
    def test_returns_string(self):
        t = DocDiffSummarizer().summary_text("a", "b")
        assert isinstance(t, str)

    def test_contains_line_counts(self):
        t = DocDiffSummarizer().summary_text("a\nb", "a")
        assert "/-1" in t or "-1" in t

    def test_contains_similarity(self):
        t = DocDiffSummarizer().summary_text("a", "b")
        assert "similarity" in t.lower()

    def test_contains_magnitude(self):
        t = DocDiffSummarizer().summary_text("a" * 100, "z" * 100)
        assert "REWRITE" in t

    def test_identical_text(self):
        t = DocDiffSummarizer().summary_text("hello", "hello")
        assert "TRIVIAL" in t


# ---------------------------------------------------------------------------
# is_rewrite
# ---------------------------------------------------------------------------

class TestIsRewrite:
    def test_identical_not_rewrite(self):
        assert DocDiffSummarizer().is_rewrite("hello", "hello") is False

    def test_completely_different_is_rewrite(self):
        assert DocDiffSummarizer().is_rewrite("a" * 100, "z" * 100) is True

    def test_custom_threshold(self):
        # similarity 0.5 should NOT be rewrite at threshold 0.3
        assert DocDiffSummarizer().is_rewrite(
            "a" * 50, "a" * 50 + "z" * 50, threshold=0.3
        ) is False

    def test_threshold_high(self):
        # With very high threshold, almost anything is "rewrite"
        assert DocDiffSummarizer().is_rewrite(
            "hello", "hello!", threshold=0.99
        ) is True


# ---------------------------------------------------------------------------
# is_minor_edit
# ---------------------------------------------------------------------------

class TestIsMinorEdit:
    def test_identical_is_minor_edit(self):
        assert DocDiffSummarizer().is_minor_edit("hello", "hello") is True

    def test_completely_different_not_minor(self):
        assert (
            DocDiffSummarizer().is_minor_edit("a" * 100, "z" * 100) is False
        )

    def test_almost_identical_is_minor(self):
        # 1 char added to 100-char string → > 0.95 similarity
        assert (
            DocDiffSummarizer().is_minor_edit("a" * 100, "a" * 100 + "b")
            is True
        )

    def test_custom_threshold(self):
        # similarity 0.5 should NOT be minor at default 0.95
        assert (
            DocDiffSummarizer().is_minor_edit("a" * 50, "a" * 50 + "z" * 50)
            is False
        )

    def test_lower_threshold_passes(self):
        # half changed accepted at threshold 0.4
        assert (
            DocDiffSummarizer().is_minor_edit(
                "a" * 50, "a" * 50 + "z" * 50, threshold=0.4
            )
            is True
        )


# ---------------------------------------------------------------------------
# count_added/removed
# ---------------------------------------------------------------------------

class TestCounts:
    def test_count_added_lines(self):
        assert DocDiffSummarizer().count_added_lines("a", "a\nb\nc") == 2

    def test_count_removed_lines(self):
        assert DocDiffSummarizer().count_removed_lines("a\nb\nc", "a") == 2

    def test_count_added_zero_when_identical(self):
        assert DocDiffSummarizer().count_added_lines("a", "a") == 0

    def test_count_removed_zero_when_identical(self):
        assert DocDiffSummarizer().count_removed_lines("a", "a") == 0


# ---------------------------------------------------------------------------
# compare_batch
# ---------------------------------------------------------------------------

class TestCompareBatch:
    def test_empty_batch(self):
        out = DocDiffSummarizer().compare_batch([], [])
        assert out == []

    def test_single_pair(self):
        out = DocDiffSummarizer().compare_batch(["a"], ["b"])
        assert len(out) == 1
        assert isinstance(out[0], DiffSummary)

    def test_multiple_pairs(self):
        old_docs = ["one", "two", "three"]
        new_docs = ["one!", "two", "tree"]
        out = DocDiffSummarizer().compare_batch(old_docs, new_docs)
        assert len(out) == 3
        # Middle pair was identical
        assert out[1].similarity == 1.0

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError):
            DocDiffSummarizer().compare_batch(["a", "b"], ["a"])

    def test_returns_list(self):
        out = DocDiffSummarizer().compare_batch(["a"], ["a"])
        assert isinstance(out, list)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_both_empty(self):
        s = DocDiffSummarizer().summarize("", "")
        assert s.similarity == 1.0
        assert s.lines_added == 0
        assert s.lines_removed == 0
        assert s.magnitude == ChangeMagnitude.TRIVIAL

    def test_old_empty(self):
        s = DocDiffSummarizer().summarize("", "new\ntext")
        assert s.lines_added >= 1
        assert s.lines_removed == 0

    def test_new_empty(self):
        s = DocDiffSummarizer().summarize("old\ntext", "")
        assert s.lines_removed >= 1
        assert s.lines_added == 0

    def test_identical_long_documents(self):
        doc = "\n".join(f"line {i}" for i in range(100))
        s = DocDiffSummarizer().summarize(doc, doc)
        assert s.similarity == 1.0
        assert s.lines_added == 0
        assert s.magnitude == ChangeMagnitude.TRIVIAL

    def test_rename_heuristic_low_similarity(self):
        # Highly different content with different headings → possible rename
        old = "# Old Title\n" + "alpha beta gamma " * 20
        new = "# New Title\n" + "xyz uvw rst " * 30
        s = DocDiffSummarizer().summarize(old, new)
        # Either is_rename triggers, or it's classified as a REWRITE — both acceptable
        assert s.magnitude == ChangeMagnitude.REWRITE

    def test_whitespace_only_change(self):
        s = DocDiffSummarizer().summarize("hello world", "hello  world")
        assert s.magnitude in (ChangeMagnitude.TRIVIAL, ChangeMagnitude.MINOR)

    def test_unicode_content(self):
        s = DocDiffSummarizer().summarize("привет мир", "привет земля")
        assert isinstance(s, DiffSummary)
        assert 0.0 <= s.similarity <= 1.0
