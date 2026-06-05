"""Tests for docstoolkit.content_diff module.

Covers: ChangeType, LineChange, DiffResult properties, ContentDiffer methods,
        edge cases, and section-level diffing.
"""
from __future__ import annotations

import pytest

from docstoolkit.content_diff import (
    ChangeType,
    ContentDiffer,
    DiffResult,
    LineChange,
    SectionChange,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_differ() -> ContentDiffer:
    return ContentDiffer()


def make_result(changes: list[LineChange]) -> DiffResult:
    return DiffResult(changes=changes)


# ---------------------------------------------------------------------------
# TestChangeType
# ---------------------------------------------------------------------------

class TestChangeType:
    def test_members_exist(self):
        assert ChangeType.ADDED
        assert ChangeType.REMOVED
        assert ChangeType.UNCHANGED
        assert ChangeType.MODIFIED

    def test_values(self):
        assert ChangeType.ADDED.value == "ADDED"
        assert ChangeType.REMOVED.value == "REMOVED"
        assert ChangeType.UNCHANGED.value == "UNCHANGED"
        assert ChangeType.MODIFIED.value == "MODIFIED"

    def test_enum_count(self):
        assert len(ChangeType) == 4

    def test_identity(self):
        assert ChangeType.ADDED is ChangeType.ADDED
        assert ChangeType.ADDED is not ChangeType.REMOVED


# ---------------------------------------------------------------------------
# TestLineChange
# ---------------------------------------------------------------------------

class TestLineChange:
    def test_basic_creation(self):
        lc = LineChange(line_num_old=1, line_num_new=1, content="hello", change_type=ChangeType.UNCHANGED)
        assert lc.line_num_old == 1
        assert lc.line_num_new == 1
        assert lc.content == "hello"
        assert lc.change_type == ChangeType.UNCHANGED

    def test_added_line_no_old(self):
        lc = LineChange(line_num_old=None, line_num_new=5, content="new line", change_type=ChangeType.ADDED)
        assert lc.line_num_old is None
        assert lc.line_num_new == 5

    def test_removed_line_no_new(self):
        lc = LineChange(line_num_old=3, line_num_new=None, content="old line", change_type=ChangeType.REMOVED)
        assert lc.line_num_old == 3
        assert lc.line_num_new is None

    def test_empty_content(self):
        lc = LineChange(line_num_old=1, line_num_new=1, content="", change_type=ChangeType.UNCHANGED)
        assert lc.content == ""


# ---------------------------------------------------------------------------
# TestDiffResultProperties
# ---------------------------------------------------------------------------

class TestDiffResultProperties:
    def _build(self, types: list[ChangeType]) -> DiffResult:
        changes = [
            LineChange(
                line_num_old=i if t != ChangeType.ADDED else None,
                line_num_new=i if t != ChangeType.REMOVED else None,
                content=f"line {i}",
                change_type=t,
            )
            for i, t in enumerate(types, 1)
        ]
        return DiffResult(changes=changes)

    def test_added_count(self):
        r = self._build([ChangeType.ADDED, ChangeType.ADDED, ChangeType.UNCHANGED])
        assert r.added_count == 2

    def test_removed_count(self):
        r = self._build([ChangeType.REMOVED, ChangeType.UNCHANGED])
        assert r.removed_count == 1

    def test_unchanged_count(self):
        r = self._build([ChangeType.UNCHANGED, ChangeType.UNCHANGED, ChangeType.ADDED])
        assert r.unchanged_count == 2

    def test_similarity_all_unchanged(self):
        r = self._build([ChangeType.UNCHANGED, ChangeType.UNCHANGED])
        assert r.similarity == 1.0

    def test_similarity_half(self):
        r = self._build([ChangeType.UNCHANGED, ChangeType.ADDED])
        assert r.similarity == pytest.approx(0.5)

    def test_similarity_empty(self):
        r = DiffResult(changes=[])
        assert r.similarity == 1.0

    def test_has_changes_true(self):
        r = self._build([ChangeType.UNCHANGED, ChangeType.ADDED])
        assert r.has_changes is True

    def test_has_changes_false(self):
        r = self._build([ChangeType.UNCHANGED, ChangeType.UNCHANGED])
        assert r.has_changes is False

    def test_has_changes_removed(self):
        r = self._build([ChangeType.REMOVED])
        assert r.has_changes is True

    def test_summary_format(self):
        r = self._build([ChangeType.ADDED, ChangeType.ADDED, ChangeType.REMOVED, ChangeType.UNCHANGED])
        assert r.summary == "+2/-1 lines"

    def test_summary_no_changes(self):
        r = self._build([ChangeType.UNCHANGED])
        assert r.summary == "+0/-0 lines"


# ---------------------------------------------------------------------------
# TestContentDifferIdentical
# ---------------------------------------------------------------------------

class TestContentDifferIdentical:
    def setup_method(self):
        self.d = make_differ()

    def test_identical_single_line(self):
        r = self.d.diff("hello", "hello")
        assert r.has_changes is False
        assert r.unchanged_count == 1

    def test_identical_multiline(self):
        text = "line one\nline two\nline three"
        r = self.d.diff(text, text)
        assert r.has_changes is False
        assert r.added_count == 0
        assert r.removed_count == 0

    def test_identical_similarity_one(self):
        text = "foo\nbar\nbaz"
        r = self.d.diff(text, text)
        assert r.similarity == 1.0

    def test_identical_line_numbers_match(self):
        r = self.d.diff("alpha\nbeta", "alpha\nbeta")
        for change in r.changes:
            assert change.line_num_old == change.line_num_new


# ---------------------------------------------------------------------------
# TestContentDifferAddLines
# ---------------------------------------------------------------------------

class TestContentDifferAddLines:
    def setup_method(self):
        self.d = make_differ()

    def test_add_line_at_end(self):
        r = self.d.diff("line1\nline2", "line1\nline2\nline3")
        assert r.added_count == 1
        assert r.removed_count == 0

    def test_add_line_at_beginning(self):
        r = self.d.diff("line2\nline3", "line1\nline2\nline3")
        assert r.added_count == 1
        assert r.removed_count == 0

    def test_add_line_in_middle(self):
        r = self.d.diff("line1\nline3", "line1\nline2\nline3")
        assert r.added_count == 1
        assert r.removed_count == 0

    def test_add_multiple_lines(self):
        r = self.d.diff("only", "only\nextra1\nextra2\nextra3")
        assert r.added_count == 3

    def test_add_to_empty(self):
        r = self.d.diff("", "new line")
        assert r.added_count == 1
        assert r.removed_count == 0

    def test_added_line_has_no_old_num(self):
        r = self.d.diff("a", "a\nb")
        added = [c for c in r.changes if c.change_type == ChangeType.ADDED]
        assert len(added) == 1
        assert added[0].line_num_old is None

    def test_added_line_content(self):
        r = self.d.diff("first", "first\nsecond")
        added = [c for c in r.changes if c.change_type == ChangeType.ADDED]
        assert added[0].content == "second"


# ---------------------------------------------------------------------------
# TestContentDifferRemoveLines
# ---------------------------------------------------------------------------

class TestContentDifferRemoveLines:
    def setup_method(self):
        self.d = make_differ()

    def test_remove_line_at_end(self):
        r = self.d.diff("line1\nline2\nline3", "line1\nline2")
        assert r.removed_count == 1
        assert r.added_count == 0

    def test_remove_line_at_beginning(self):
        r = self.d.diff("line1\nline2\nline3", "line2\nline3")
        assert r.removed_count == 1

    def test_remove_line_in_middle(self):
        r = self.d.diff("line1\nline2\nline3", "line1\nline3")
        assert r.removed_count == 1

    def test_remove_all_lines(self):
        r = self.d.diff("a\nb\nc", "")
        assert r.removed_count == 3
        assert r.added_count == 0

    def test_removed_line_has_no_new_num(self):
        r = self.d.diff("a\nb", "a")
        removed = [c for c in r.changes if c.change_type == ChangeType.REMOVED]
        assert removed[0].line_num_new is None

    def test_removed_line_content(self):
        r = self.d.diff("keep\ndelete_me", "keep")
        removed = [c for c in r.changes if c.change_type == ChangeType.REMOVED]
        assert removed[0].content == "delete_me"


# ---------------------------------------------------------------------------
# TestContentDifferModify
# ---------------------------------------------------------------------------

class TestContentDifferModify:
    def setup_method(self):
        self.d = make_differ()

    def test_replace_one_line(self):
        r = self.d.diff("hello world", "hello earth")
        assert r.has_changes is True
        # replaced = 1 removed + 1 added
        assert r.removed_count >= 1
        assert r.added_count >= 1

    def test_mixed_add_remove(self):
        r = self.d.diff("a\nb\nc", "a\nd\nc")
        assert r.has_changes is True
        assert r.removed_count >= 1
        assert r.added_count >= 1
        assert r.unchanged_count >= 2

    def test_summary_reflects_counts(self):
        r = self.d.diff("x\ny\nz", "x\nw\nz")
        assert r.summary.startswith("+")
        assert "/-" in r.summary

    def test_similarity_decreases_with_changes(self):
        r_same = self.d.diff("a\nb\nc", "a\nb\nc")
        r_diff = self.d.diff("a\nb\nc", "x\ny\nz")
        assert r_same.similarity > r_diff.similarity


# ---------------------------------------------------------------------------
# TestUnifiedDiff
# ---------------------------------------------------------------------------

class TestUnifiedDiff:
    def setup_method(self):
        self.d = make_differ()

    def test_returns_string(self):
        result = self.d.unified_diff("old\ntext", "new\ntext")
        assert isinstance(result, str)

    def test_contains_plus_lines(self):
        result = self.d.unified_diff("hello", "world")
        assert "+" in result

    def test_contains_minus_lines(self):
        result = self.d.unified_diff("hello", "world")
        assert "-" in result

    def test_identical_texts_empty_diff(self):
        result = self.d.unified_diff("same\ntext", "same\ntext")
        assert result == ""

    def test_context_parameter_respected(self):
        old = "\n".join(str(i) for i in range(20))
        new = "\n".join(str(i) if i != 10 else "changed" for i in range(20))
        result_ctx3 = self.d.unified_diff(old, new, context=3)
        result_ctx0 = self.d.unified_diff(old, new, context=0)
        # More context = longer output
        assert len(result_ctx3) > len(result_ctx0)

    def test_unified_diff_headers(self):
        result = self.d.unified_diff("a", "b")
        assert "---" in result or "+++" in result

    def test_added_line_marker(self):
        result = self.d.unified_diff("keep", "keep\nnew_line")
        assert "+new_line" in result


# ---------------------------------------------------------------------------
# TestIsSimilar
# ---------------------------------------------------------------------------

class TestIsSimilar:
    def setup_method(self):
        self.d = make_differ()

    def test_identical_texts_similar(self):
        assert self.d.is_similar("hello world", "hello world") is True

    def test_completely_different_not_similar(self):
        assert self.d.is_similar("aaaa", "bbbb") is False

    def test_default_threshold_80_percent(self):
        # 9/10 chars identical → ratio ~0.95
        assert self.d.is_similar("hello world", "hello worXd") is True

    def test_custom_threshold_zero_always_similar(self):
        assert self.d.is_similar("abc", "xyz", threshold=0.0) is True

    def test_custom_threshold_one_only_identical(self):
        assert self.d.is_similar("hello", "hellx", threshold=1.0) is False
        assert self.d.is_similar("hello", "hello", threshold=1.0) is True

    def test_threshold_boundary(self):
        # When ratio == threshold, should return True (>=)
        old = "abcd"
        new = "abcd"
        ratio = 1.0
        assert self.d.is_similar(old, new, threshold=ratio) is True

    def test_slightly_changed_text(self):
        original = "The quick brown fox jumps over the lazy dog"
        changed  = "The quick brown cat jumps over the lazy dog"
        assert self.d.is_similar(original, changed, threshold=0.8) is True

    def test_heavily_changed_not_similar(self):
        original = "The quick brown fox"
        changed  = "Completely unrelated content here"
        assert self.d.is_similar(original, changed, threshold=0.9) is False


# ---------------------------------------------------------------------------
# TestExtractChanges
# ---------------------------------------------------------------------------

class TestExtractChanges:
    def setup_method(self):
        self.d = make_differ()

    def test_returns_dict_with_keys(self):
        result = self.d.extract_changes("a", "b")
        assert "added" in result
        assert "removed" in result

    def test_added_lines_correct(self):
        result = self.d.extract_changes("line1", "line1\nline2")
        assert "line2" in result["added"]

    def test_removed_lines_correct(self):
        result = self.d.extract_changes("line1\nline2", "line1")
        assert "line2" in result["removed"]

    def test_identical_no_changes(self):
        result = self.d.extract_changes("same", "same")
        assert result["added"] == []
        assert result["removed"] == []

    def test_empty_old(self):
        result = self.d.extract_changes("", "new content")
        assert "new content" in result["added"]
        assert result["removed"] == []

    def test_empty_new(self):
        result = self.d.extract_changes("old content", "")
        assert "old content" in result["removed"]
        assert result["added"] == []

    def test_values_are_lists(self):
        result = self.d.extract_changes("a\nb", "a\nc")
        assert isinstance(result["added"], list)
        assert isinstance(result["removed"], list)


# ---------------------------------------------------------------------------
# TestDiffSections
# ---------------------------------------------------------------------------

class TestDiffSections:
    def setup_method(self):
        self.d = make_differ()

    def test_returns_list(self):
        result = self.d.diff_sections("# A\nhello", "# A\nhello")
        assert isinstance(result, list)

    def test_elements_are_section_change(self):
        result = self.d.diff_sections("# A\nhello", "# A\nworld")
        for item in result:
            assert isinstance(item, SectionChange)

    def test_identical_sections_unchanged(self):
        text = "# Section One\nsome content\n\n# Section Two\nmore content"
        result = self.d.diff_sections(text, text)
        for sc in result:
            assert sc.change_type == ChangeType.UNCHANGED

    def test_added_section(self):
        old = "# Existing\ncontent"
        new = "# Existing\ncontent\n\n# New Section\nnew stuff"
        result = self.d.diff_sections(old, new)
        headings = {sc.heading: sc.change_type for sc in result}
        assert headings.get("# New Section") == ChangeType.ADDED

    def test_removed_section(self):
        old = "# Keep\ncontent\n\n# Remove\nold stuff"
        new = "# Keep\ncontent"
        result = self.d.diff_sections(old, new)
        headings = {sc.heading: sc.change_type for sc in result}
        assert headings.get("# Remove") == ChangeType.REMOVED

    def test_modified_section(self):
        old = "# Section\noriginal line"
        new = "# Section\nchanged line"
        result = self.d.diff_sections(old, new)
        # result[0] is the empty preamble section; result[1] is "# Section"
        section = next(sc for sc in result if sc.heading == "# Section")
        assert section.change_type == ChangeType.MODIFIED

    def test_section_heading_preserved(self):
        old = "# My Heading\ntext"
        new = "# My Heading\ntext"
        result = self.d.diff_sections(old, new)
        assert any(sc.heading == "# My Heading" for sc in result)

    def test_no_headings_treated_as_one_section(self):
        old = "line one\nline two"
        new = "line one\nline two"
        result = self.d.diff_sections(old, new)
        assert len(result) == 1
        assert result[0].change_type == ChangeType.UNCHANGED

    def test_changes_list_populated(self):
        old = "# S\nold"
        new = "# S\nnew"
        result = self.d.diff_sections(old, new)
        # Find the modified heading section (not the empty preamble)
        section = next(sc for sc in result if sc.heading == "# S")
        assert len(section.changes) > 0


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def setup_method(self):
        self.d = make_differ()

    def test_both_empty(self):
        r = self.d.diff("", "")
        assert r.has_changes is False
        assert r.changes == []

    def test_old_empty_new_nonempty(self):
        r = self.d.diff("", "hello\nworld")
        assert r.added_count == 2
        assert r.removed_count == 0

    def test_old_nonempty_new_empty(self):
        r = self.d.diff("hello\nworld", "")
        assert r.removed_count == 2
        assert r.added_count == 0

    def test_single_line_identical(self):
        r = self.d.diff("x", "x")
        assert r.unchanged_count == 1

    def test_whitespace_only_lines(self):
        r = self.d.diff("   ", "   ")
        assert r.has_changes is False

    def test_whitespace_differs(self):
        r = self.d.diff("  ", "   ")
        assert r.has_changes is True

    def test_large_text_no_exception(self):
        text = "\n".join(f"line {i}" for i in range(500))
        r = self.d.diff(text, text)
        assert r.has_changes is False

    def test_extract_changes_both_empty(self):
        result = self.d.extract_changes("", "")
        assert result["added"] == []
        assert result["removed"] == []

    def test_unified_diff_empty_texts(self):
        result = self.d.unified_diff("", "")
        assert result == ""

    def test_diff_sections_both_empty(self):
        result = self.d.diff_sections("", "")
        # Should return a list (possibly with one empty section)
        assert isinstance(result, list)

    def test_is_similar_empty_texts(self):
        # Two empty strings are identical
        assert self.d.is_similar("", "") is True
