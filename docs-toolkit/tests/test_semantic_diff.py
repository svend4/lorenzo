"""Tests for docstoolkit.semantic_diff — E39 Semantic Diff module.

65+ tests covering DiffChunk, SemanticDiffer, DiffStats, DiffReport,
DiffReporter, and all public helpers.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.semantic_diff import (
    DiffChunk,
    DiffReport,
    DiffReporter,
    DiffStats,
    DiffType,
    SemanticDiffer,
)


# ===========================================================================
# Fixtures / shared data
# ===========================================================================

SENTENCE_A = "The cat sat on the mat. The dog ran outside. It was a sunny day."
SENTENCE_B = "The cat sat on the mat. The dog ran in the garden. A new sentence here."

PARAGRAPH_A = "First paragraph about cats.\n\nSecond paragraph about dogs.\n\nThird paragraph about birds."
PARAGRAPH_B = "First paragraph about cats.\n\nSecond paragraph about dogs, updated.\n\nFourth paragraph about fish."

WORD_OLD = "the quick brown fox jumps over the lazy dog"
WORD_NEW = "the quick red fox leaps over the lazy cat"


# ===========================================================================
# S1  Imports
# ===========================================================================

def test_import_diff_type():
    assert DiffType is not None


def test_import_diff_chunk():
    assert DiffChunk is not None


def test_import_semantic_differ():
    assert SemanticDiffer is not None


def test_import_diff_stats():
    assert DiffStats is not None


def test_import_diff_report():
    assert DiffReport is not None


def test_import_diff_reporter():
    assert DiffReporter is not None


# ===========================================================================
# S2  DiffType enum
# ===========================================================================

def test_diff_type_values():
    assert DiffType.ADDITION.value == "ADDITION"
    assert DiffType.DELETION.value == "DELETION"
    assert DiffType.MODIFICATION.value == "MODIFICATION"
    assert DiffType.REORDER.value == "REORDER"
    assert DiffType.UNCHANGED.value == "UNCHANGED"


def test_diff_type_members_count():
    assert len(DiffType) == 5


# ===========================================================================
# S3  DiffChunk — construction and fields
# ===========================================================================

def test_diff_chunk_basic_fields():
    chunk = DiffChunk(
        diff_type=DiffType.ADDITION,
        old_text="",
        new_text="hello world",
        old_pos=-1,
        new_pos=0,
        similarity=0.0,
    )
    assert chunk.diff_type == DiffType.ADDITION
    assert chunk.old_text == ""
    assert chunk.new_text == "hello world"
    assert chunk.old_pos == -1
    assert chunk.new_pos == 0
    assert chunk.similarity == 0.0


def test_diff_chunk_default_similarity():
    chunk = DiffChunk(
        diff_type=DiffType.UNCHANGED,
        old_text="text",
        new_text="text",
        old_pos=0,
        new_pos=0,
    )
    assert chunk.similarity == 1.0


def test_diff_chunk_deletion_fields():
    chunk = DiffChunk(
        diff_type=DiffType.DELETION,
        old_text="removed text here",
        new_text="",
        old_pos=2,
        new_pos=-1,
        similarity=0.0,
    )
    assert chunk.diff_type == DiffType.DELETION
    assert chunk.new_text == ""


def test_diff_chunk_modification_fields():
    chunk = DiffChunk(
        diff_type=DiffType.MODIFICATION,
        old_text="old version",
        new_text="new version",
        old_pos=1,
        new_pos=1,
        similarity=0.5,
    )
    assert chunk.similarity == 0.5
    assert chunk.diff_type == DiffType.MODIFICATION


# ===========================================================================
# S4  DiffChunk.is_significant
# ===========================================================================

def test_is_significant_addition():
    chunk = DiffChunk(DiffType.ADDITION, "", "new", -1, 0, 0.0)
    assert chunk.is_significant() is True


def test_is_significant_deletion():
    chunk = DiffChunk(DiffType.DELETION, "old", "", 0, -1, 0.0)
    assert chunk.is_significant() is True


def test_is_significant_modification():
    chunk = DiffChunk(DiffType.MODIFICATION, "old", "new", 0, 0, 0.5)
    assert chunk.is_significant() is True


def test_is_significant_reorder():
    chunk = DiffChunk(DiffType.REORDER, "text", "text", 0, 1, 1.0)
    assert chunk.is_significant() is True


def test_is_significant_unchanged_high_sim():
    chunk = DiffChunk(DiffType.UNCHANGED, "text", "text", 0, 0, 1.0)
    assert chunk.is_significant() is False


def test_is_significant_unchanged_low_sim():
    # similarity 0.5 with default threshold 0.1 → 1 - 0.1 = 0.9 → 0.5 < 0.9 → True
    chunk = DiffChunk(DiffType.UNCHANGED, "old", "new", 0, 0, 0.5)
    assert chunk.is_significant() is True


def test_is_significant_custom_threshold():
    chunk = DiffChunk(DiffType.UNCHANGED, "a", "b", 0, 0, 0.8)
    # threshold=0.3 → 1 - 0.3 = 0.7 → 0.8 >= 0.7 → NOT significant
    assert chunk.is_significant(threshold=0.3) is False
    # threshold=0.1 → 1 - 0.1 = 0.9 → 0.8 < 0.9 → IS significant
    assert chunk.is_significant(threshold=0.1) is True


def test_is_significant_boundary_sim_exactly_one():
    chunk = DiffChunk(DiffType.UNCHANGED, "x", "x", 0, 0, 1.0)
    assert chunk.is_significant(threshold=0.0) is False


# ===========================================================================
# S5  DiffChunk.summary
# ===========================================================================

def test_summary_addition():
    chunk = DiffChunk(DiffType.ADDITION, "", "one two three", -1, 0, 0.0)
    s = chunk.summary()
    assert s.startswith("ADDED:")
    assert "3" in s
    assert "words" in s


def test_summary_deletion():
    chunk = DiffChunk(DiffType.DELETION, "one two three four", "", 0, -1, 0.0)
    s = chunk.summary()
    assert s.startswith("DELETED:")
    assert "4" in s
    assert "words" in s


def test_summary_modification():
    chunk = DiffChunk(DiffType.MODIFICATION, "old text here", "new text there", 0, 0, 0.6)
    s = chunk.summary()
    assert s.startswith("MODIFIED:")
    assert "→" in s
    assert "sim" in s


def test_summary_unchanged():
    chunk = DiffChunk(DiffType.UNCHANGED, "same text", "same text", 0, 0, 1.0)
    s = chunk.summary()
    assert s.startswith("UNCHANGED:")
    assert "words" in s


def test_summary_reorder():
    chunk = DiffChunk(DiffType.REORDER, "moved text", "moved text", 3, 1, 1.0)
    s = chunk.summary()
    assert s.startswith("REORDERED:")
    assert "words" in s


def test_summary_addition_single_word():
    chunk = DiffChunk(DiffType.ADDITION, "", "hello", -1, 0, 0.0)
    s = chunk.summary()
    assert "1" in s


# ===========================================================================
# S6  SemanticDiffer — diff_sentences
# ===========================================================================

def test_diff_sentences_identical():
    differ = SemanticDiffer()
    text = "The cat sat. The dog ran. The bird flew."
    chunks = differ.diff_sentences(text, text)
    types = [c.diff_type for c in chunks]
    assert all(t == DiffType.UNCHANGED for t in types)


def test_diff_sentences_identical_similarities_all_one():
    differ = SemanticDiffer()
    text = "Hello world. Goodbye world."
    chunks = differ.diff_sentences(text, text)
    for c in chunks:
        assert c.similarity == pytest.approx(1.0, abs=0.01)


def test_diff_sentences_added_sentence():
    differ = SemanticDiffer()
    old = "The cat sat on the mat."
    new = "The cat sat on the mat. A completely new sentence appeared here today."
    chunks = differ.diff_sentences(old, new)
    types = {c.diff_type for c in chunks}
    assert DiffType.ADDITION in types


def test_diff_sentences_deleted_sentence():
    differ = SemanticDiffer()
    old = "The cat sat on the mat. An extra sentence to remove later."
    new = "The cat sat on the mat."
    chunks = differ.diff_sentences(old, new)
    types = {c.diff_type for c in chunks}
    assert DiffType.DELETION in types


def test_diff_sentences_modified_sentence():
    differ = SemanticDiffer()
    old = "The quick brown fox jumps over the fence."
    new = "The quick brown fox leaps over the barrier."
    chunks = differ.diff_sentences(old, new)
    types = {c.diff_type for c in chunks}
    # Should be MODIFICATION (high similarity but not identical)
    assert DiffType.MODIFICATION in types or DiffType.UNCHANGED in types


def test_diff_sentences_returns_list():
    differ = SemanticDiffer()
    result = differ.diff_sentences("Hello.", "Hello.")
    assert isinstance(result, list)


def test_diff_sentences_empty_both():
    differ = SemanticDiffer()
    assert differ.diff_sentences("", "") == []


def test_diff_sentences_empty_old():
    differ = SemanticDiffer()
    chunks = differ.diff_sentences("", "New sentence here.")
    assert any(c.diff_type == DiffType.ADDITION for c in chunks)


def test_diff_sentences_empty_new():
    differ = SemanticDiffer()
    chunks = differ.diff_sentences("Old sentence here.", "")
    assert any(c.diff_type == DiffType.DELETION for c in chunks)


def test_diff_sentences_chunks_are_diff_chunk_instances():
    differ = SemanticDiffer()
    chunks = differ.diff_sentences(SENTENCE_A, SENTENCE_B)
    for c in chunks:
        assert isinstance(c, DiffChunk)


def test_diff_sentences_similarity_range():
    differ = SemanticDiffer()
    chunks = differ.diff_sentences(SENTENCE_A, SENTENCE_B)
    for c in chunks:
        assert 0.0 <= c.similarity <= 1.0


# ===========================================================================
# S7  SemanticDiffer — diff_paragraphs
# ===========================================================================

def test_diff_paragraphs_identical():
    differ = SemanticDiffer()
    chunks = differ.diff_paragraphs(PARAGRAPH_A, PARAGRAPH_A)
    types = [c.diff_type for c in chunks]
    assert all(t == DiffType.UNCHANGED for t in types)


def test_diff_paragraphs_added_paragraph():
    differ = SemanticDiffer()
    old = "Para one.\n\nPara two."
    new = "Para one.\n\nPara two.\n\nBrand new paragraph with fresh content."
    chunks = differ.diff_paragraphs(old, new)
    types = {c.diff_type for c in chunks}
    assert DiffType.ADDITION in types


def test_diff_paragraphs_deleted_paragraph():
    differ = SemanticDiffer()
    old = "Para one.\n\nPara two.\n\nPara three extra."
    new = "Para one.\n\nPara two."
    chunks = differ.diff_paragraphs(old, new)
    types = {c.diff_type for c in chunks}
    assert DiffType.DELETION in types


def test_diff_paragraphs_modified_paragraph():
    differ = SemanticDiffer()
    old = "Dogs are loyal animals."
    new = "Dogs are very loyal and friendly animals."
    chunks = differ.diff_paragraphs(old, new)
    assert len(chunks) > 0


def test_diff_paragraphs_empty_both():
    differ = SemanticDiffer()
    assert differ.diff_paragraphs("", "") == []


def test_diff_paragraphs_returns_list():
    differ = SemanticDiffer()
    result = differ.diff_paragraphs(PARAGRAPH_A, PARAGRAPH_B)
    assert isinstance(result, list)


# ===========================================================================
# S8  SemanticDiffer — diff_words
# ===========================================================================

def test_diff_words_identical():
    differ = SemanticDiffer()
    chunks = differ.diff_words("hello world", "hello world")
    types = {c.diff_type for c in chunks}
    # All should be UNCHANGED
    assert types == {DiffType.UNCHANGED} or not chunks


def test_diff_words_pure_addition():
    differ = SemanticDiffer()
    chunks = differ.diff_words("hello", "hello world")
    added = [c for c in chunks if c.diff_type == DiffType.ADDITION]
    assert len(added) == 1
    assert added[0].new_text == "world"


def test_diff_words_pure_deletion():
    differ = SemanticDiffer()
    chunks = differ.diff_words("hello world", "hello")
    deleted = [c for c in chunks if c.diff_type == DiffType.DELETION]
    assert len(deleted) == 1
    assert deleted[0].old_text == "world"


def test_diff_words_no_modification_type():
    """diff_words produces only ADDITION, DELETION, UNCHANGED — no MODIFICATION."""
    differ = SemanticDiffer()
    chunks = differ.diff_words(WORD_OLD, WORD_NEW)
    for c in chunks:
        assert c.diff_type in {DiffType.ADDITION, DiffType.DELETION, DiffType.UNCHANGED}


def test_diff_words_empty_both():
    differ = SemanticDiffer()
    assert differ.diff_words("", "") == []


def test_diff_words_empty_old():
    differ = SemanticDiffer()
    chunks = differ.diff_words("", "one two three")
    assert all(c.diff_type == DiffType.ADDITION for c in chunks)
    assert len(chunks) == 3


def test_diff_words_empty_new():
    differ = SemanticDiffer()
    chunks = differ.diff_words("one two three", "")
    assert all(c.diff_type == DiffType.DELETION for c in chunks)
    assert len(chunks) == 3


def test_diff_words_changed_words():
    differ = SemanticDiffer()
    chunks = differ.diff_words("brown fox", "red fox")
    deleted = [c for c in chunks if c.diff_type == DiffType.DELETION]
    added = [c for c in chunks if c.diff_type == DiffType.ADDITION]
    assert any(c.old_text == "brown" for c in deleted)
    assert any(c.new_text == "red" for c in added)


def test_diff_words_unchanged_preserved():
    differ = SemanticDiffer()
    chunks = differ.diff_words("the fox", "the cat")
    unchanged = [c for c in chunks if c.diff_type == DiffType.UNCHANGED]
    assert any(c.old_text == "the" for c in unchanged)


def test_diff_words_returns_list():
    differ = SemanticDiffer()
    result = differ.diff_words(WORD_OLD, WORD_NEW)
    assert isinstance(result, list)


# ===========================================================================
# S9  DiffStats
# ===========================================================================

def test_diff_stats_defaults():
    stats = DiffStats()
    assert stats.added == 0
    assert stats.deleted == 0
    assert stats.modified == 0
    assert stats.unchanged == 0
    assert stats.reordered == 0


def test_diff_stats_total_changes_all_zero():
    stats = DiffStats()
    assert stats.total_changes() == 0


def test_diff_stats_total_changes():
    stats = DiffStats(added=3, deleted=2, modified=1, unchanged=5, reordered=1)
    assert stats.total_changes() == 7  # 3+2+1+1


def test_diff_stats_total_changes_unchanged_not_counted():
    stats = DiffStats(added=1, deleted=0, modified=0, unchanged=100, reordered=0)
    assert stats.total_changes() == 1


def test_diff_stats_change_rate_all_zero():
    stats = DiffStats()
    # total_changes=0, unchanged=0 → 0 / (0 + 0 + 1) = 0
    assert stats.change_rate() == pytest.approx(0.0)


def test_diff_stats_change_rate_all_changed():
    stats = DiffStats(added=10, deleted=0, modified=0, unchanged=0, reordered=0)
    # 10 / (10 + 0 + 1) ≈ 0.909
    assert stats.change_rate() == pytest.approx(10 / 11, abs=0.001)


def test_diff_stats_change_rate_mixed():
    stats = DiffStats(added=3, deleted=2, modified=1, unchanged=4, reordered=0)
    # total_changes = 6, change_rate = 6 / (6 + 4 + 1) = 6/11
    assert stats.change_rate() == pytest.approx(6 / 11, abs=0.001)


def test_diff_stats_change_rate_in_range():
    stats = DiffStats(added=5, deleted=3, modified=2, unchanged=10, reordered=1)
    rate = stats.change_rate()
    assert 0.0 <= rate <= 1.0


def test_diff_stats_reordered_counted():
    stats = DiffStats(added=0, deleted=0, modified=0, unchanged=5, reordered=2)
    assert stats.total_changes() == 2


# ===========================================================================
# S10  DiffReport
# ===========================================================================

def test_diff_report_fields():
    report = DiffReport(
        old_title="v1",
        new_title="v2",
        chunks=[],
        stats=DiffStats(),
    )
    assert report.old_title == "v1"
    assert report.new_title == "v2"
    assert report.chunks == []


def test_diff_report_significant_chunks_empty():
    report = DiffReport(old_title="a", new_title="b", chunks=[], stats=DiffStats())
    assert report.significant_chunks() == []


def test_diff_report_significant_chunks_filters():
    chunks = [
        DiffChunk(DiffType.UNCHANGED, "same", "same", 0, 0, 1.0),
        DiffChunk(DiffType.ADDITION, "", "new", -1, 1, 0.0),
        DiffChunk(DiffType.DELETION, "old", "", 2, -1, 0.0),
    ]
    report = DiffReport(old_title="a", new_title="b", chunks=chunks, stats=DiffStats())
    sig = report.significant_chunks()
    assert len(sig) == 2
    types = {c.diff_type for c in sig}
    assert DiffType.ADDITION in types
    assert DiffType.DELETION in types
    assert DiffType.UNCHANGED not in types


def test_diff_report_significant_chunks_custom_threshold():
    chunks = [
        DiffChunk(DiffType.UNCHANGED, "a", "b", 0, 0, 0.8),
    ]
    report = DiffReport(old_title="a", new_title="b", chunks=chunks, stats=DiffStats())
    # threshold=0.3 → 0.8 >= 0.7 → not significant
    assert report.significant_chunks(threshold=0.3) == []
    # threshold=0.1 → 0.8 < 0.9 → significant
    assert len(report.significant_chunks(threshold=0.1)) == 1


def test_diff_report_to_markdown_returns_string():
    report = DiffReport(old_title="old.md", new_title="new.md", chunks=[], stats=DiffStats())
    md = report.to_markdown()
    assert isinstance(md, str)
    assert len(md) > 0


def test_diff_report_to_markdown_contains_titles():
    report = DiffReport(old_title="doc_v1", new_title="doc_v2", chunks=[], stats=DiffStats())
    md = report.to_markdown()
    assert "doc_v1" in md
    assert "doc_v2" in md


def test_diff_report_to_markdown_contains_stats():
    stats = DiffStats(added=2, deleted=1, modified=0, unchanged=3, reordered=0)
    report = DiffReport(old_title="a", new_title="b", chunks=[], stats=stats)
    md = report.to_markdown()
    assert "2" in md  # added count
    assert "1" in md  # deleted count


def test_diff_report_to_markdown_no_changes_message():
    report = DiffReport(old_title="a", new_title="b", chunks=[], stats=DiffStats())
    md = report.to_markdown()
    assert "No significant changes" in md or "no significant" in md.lower()


def test_diff_report_to_markdown_with_significant_chunks():
    chunks = [
        DiffChunk(DiffType.ADDITION, "", "brand new content here", -1, 0, 0.0),
    ]
    stats = DiffStats(added=1)
    report = DiffReport(old_title="a", new_title="b", chunks=chunks, stats=stats)
    md = report.to_markdown()
    assert "ADDED" in md


# ===========================================================================
# S11  DiffReporter
# ===========================================================================

def test_diff_reporter_instantiation():
    reporter = DiffReporter()
    assert reporter is not None


def test_diff_reporter_report_returns_diff_report():
    reporter = DiffReporter()
    result = reporter.report("Hello world.", "Hello earth.")
    assert isinstance(result, DiffReport)


def test_diff_reporter_report_sentences_level():
    reporter = DiffReporter()
    result = reporter.report("Hello world.", "Hello earth.", level="sentences")
    assert isinstance(result, DiffReport)
    assert len(result.chunks) > 0


def test_diff_reporter_report_paragraphs_level():
    reporter = DiffReporter()
    result = reporter.report(PARAGRAPH_A, PARAGRAPH_B, level="paragraphs")
    assert isinstance(result, DiffReport)
    assert len(result.chunks) > 0


def test_diff_reporter_report_words_level():
    reporter = DiffReporter()
    result = reporter.report(WORD_OLD, WORD_NEW, level="words")
    assert isinstance(result, DiffReport)
    assert len(result.chunks) > 0


def test_diff_reporter_report_default_titles():
    reporter = DiffReporter()
    result = reporter.report("foo.", "bar.")
    assert result.old_title == "old"
    assert result.new_title == "new"


def test_diff_reporter_report_custom_titles():
    reporter = DiffReporter()
    result = reporter.report("foo.", "bar.", old_title="v1.md", new_title="v2.md")
    assert result.old_title == "v1.md"
    assert result.new_title == "v2.md"


def test_diff_reporter_report_stats_populated():
    reporter = DiffReporter()
    result = reporter.report(SENTENCE_A, SENTENCE_B)
    assert isinstance(result.stats, DiffStats)
    total = result.stats.total_changes() + result.stats.unchanged
    assert total == len(result.chunks)


def test_diff_reporter_identical_texts_no_changes():
    reporter = DiffReporter()
    text = "Identical text. No changes here."
    result = reporter.report(text, text)
    assert result.stats.total_changes() == 0
    assert result.stats.unchanged > 0


def test_diff_reporter_compare_sections_returns_dict():
    reporter = DiffReporter()
    old = {"intro": "Hello world.", "body": "Main content here."}
    new = {"intro": "Hello earth.", "body": "Main content here."}
    result = reporter.compare_sections(old, new)
    assert isinstance(result, dict)


def test_diff_reporter_compare_sections_keys_match():
    reporter = DiffReporter()
    old = {"intro": "Hello.", "body": "Body text.", "extra": "Only in old."}
    new = {"intro": "Hi.", "body": "Body text.", "footer": "Only in new."}
    result = reporter.compare_sections(old, new)
    # Only keys in both dicts
    assert "intro" in result
    assert "body" in result
    assert "extra" not in result
    assert "footer" not in result


def test_diff_reporter_compare_sections_reports_are_diff_reports():
    reporter = DiffReporter()
    old = {"s1": "Some text here.", "s2": "Other text there."}
    new = {"s1": "Some text here!", "s2": "Other text there."}
    result = reporter.compare_sections(old, new)
    for key, report in result.items():
        assert isinstance(report, DiffReport)


def test_diff_reporter_compare_sections_empty_dicts():
    reporter = DiffReporter()
    result = reporter.compare_sections({}, {})
    assert result == {}


def test_diff_reporter_compare_sections_no_common_keys():
    reporter = DiffReporter()
    old = {"a": "text a"}
    new = {"b": "text b"}
    result = reporter.compare_sections(old, new)
    assert result == {}


def test_diff_reporter_compare_sections_titles_contain_key():
    reporter = DiffReporter()
    old = {"intro": "Hello world."}
    new = {"intro": "Hello earth."}
    result = reporter.compare_sections(old, new)
    assert "intro" in result["intro"].old_title or "intro" in result["intro"].new_title
