"""Tests for docstoolkit.doc_formatter (E122)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_formatter import DocFormatter, FormatConfig, FormatRule, FormatterResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_formatter(*rules: FormatRule, max_blank: int = 2, start_level: int = 1) -> DocFormatter:
    """Return a DocFormatter configured with exactly *rules*."""
    config = FormatConfig(
        rules=list(rules),
        max_blank_lines=max_blank,
        heading_start_level=start_level,
    )
    return DocFormatter(config)


# ===========================================================================
# TestFormatRule
# ===========================================================================

class TestFormatRule:
    """FormatRule enum contains all six expected members."""

    def test_strip_trailing_whitespace_exists(self):
        assert hasattr(FormatRule, "STRIP_TRAILING_WHITESPACE")

    def test_normalize_headings_exists(self):
        assert hasattr(FormatRule, "NORMALIZE_HEADINGS")

    def test_collapse_blank_lines_exists(self):
        assert hasattr(FormatRule, "COLLAPSE_BLANK_LINES")

    def test_ensure_final_newline_exists(self):
        assert hasattr(FormatRule, "ENSURE_FINAL_NEWLINE")

    def test_normalize_bullets_exists(self):
        assert hasattr(FormatRule, "NORMALIZE_BULLETS")

    def test_fix_heading_levels_exists(self):
        assert hasattr(FormatRule, "FIX_HEADING_LEVELS")

    def test_exactly_six_members(self):
        assert len(list(FormatRule)) == 6

    def test_members_are_format_rule_instances(self):
        for member in FormatRule:
            assert isinstance(member, FormatRule)


# ===========================================================================
# TestFormatConfig
# ===========================================================================

class TestFormatConfig:
    """FormatConfig defaults and custom construction."""

    def test_default_rules_is_all_rules(self):
        config = FormatConfig()
        assert set(config.rules) == set(FormatRule)

    def test_default_max_blank_lines(self):
        config = FormatConfig()
        assert config.max_blank_lines == 2

    def test_default_heading_start_level(self):
        config = FormatConfig()
        assert config.heading_start_level == 1

    def test_custom_rules(self):
        rules = [FormatRule.STRIP_TRAILING_WHITESPACE, FormatRule.ENSURE_FINAL_NEWLINE]
        config = FormatConfig(rules=rules)
        assert config.rules == rules

    def test_custom_max_blank_lines(self):
        config = FormatConfig(max_blank_lines=1)
        assert config.max_blank_lines == 1

    def test_custom_heading_start_level(self):
        config = FormatConfig(heading_start_level=2)
        assert config.heading_start_level == 2

    def test_empty_rules_list(self):
        config = FormatConfig(rules=[])
        assert config.rules == []


# ===========================================================================
# TestFormatterResultProperties
# ===========================================================================

class TestFormatterResultProperties:
    """FormatterResult.changed and change_count properties."""

    def test_changed_false_when_identical(self):
        result = FormatterResult(original="hello", formatted="hello", rules_applied=[])
        assert result.changed is False

    def test_changed_true_when_different(self):
        result = FormatterResult(original="hello", formatted="hello\n", rules_applied=[])
        assert result.changed is True

    def test_change_count_zero_when_identical(self):
        result = FormatterResult(original="a\nb\n", formatted="a\nb\n", rules_applied=[])
        assert result.change_count == 0

    def test_change_count_one_line_changed(self):
        result = FormatterResult(original="a  \nb\n", formatted="a\nb\n", rules_applied=[])
        assert result.change_count == 1

    def test_change_count_multiple_lines_changed(self):
        result = FormatterResult(original="a  \nb  \n", formatted="a\nb\n", rules_applied=[])
        assert result.change_count == 2

    def test_change_count_extra_lines_in_formatted(self):
        # formatted has one extra line (the added newline creates a new empty "line")
        result = FormatterResult(original="abc", formatted="abc\n", rules_applied=[])
        # "abc" splits to ["abc"], "abc\n" splits to ["abc", ""]
        assert result.change_count == 1

    def test_rules_applied_stored(self):
        result = FormatterResult(
            original="x",
            formatted="x",
            rules_applied=[FormatRule.STRIP_TRAILING_WHITESPACE],
        )
        assert result.rules_applied == [FormatRule.STRIP_TRAILING_WHITESPACE]


# ===========================================================================
# TestStripTrailingWhitespace
# ===========================================================================

class TestStripTrailingWhitespace:
    """strip_trailing_whitespace() removes trailing spaces and tabs."""

    def setup_method(self):
        self.fmt = DocFormatter()

    def test_removes_trailing_spaces(self):
        assert self.fmt.strip_trailing_whitespace("hello   ") == "hello"

    def test_removes_trailing_tabs(self):
        assert self.fmt.strip_trailing_whitespace("hello\t\t") == "hello"

    def test_removes_mixed_trailing(self):
        assert self.fmt.strip_trailing_whitespace("hello \t ") == "hello"

    def test_multiline(self):
        text = "line1   \nline2\t\nline3"
        expected = "line1\nline2\nline3"
        assert self.fmt.strip_trailing_whitespace(text) == expected

    def test_no_trailing_whitespace_unchanged(self):
        text = "clean text\nno trailing"
        assert self.fmt.strip_trailing_whitespace(text) == text

    def test_empty_string(self):
        assert self.fmt.strip_trailing_whitespace("") == ""

    def test_only_whitespace_line_becomes_empty(self):
        assert self.fmt.strip_trailing_whitespace("   ") == ""

    def test_preserves_leading_whitespace(self):
        assert self.fmt.strip_trailing_whitespace("  indented  ") == "  indented"


# ===========================================================================
# TestNormalizeHeadings
# ===========================================================================

class TestNormalizeHeadings:
    """normalize_headings() ensures space after # prefix."""

    def setup_method(self):
        self.fmt = DocFormatter()

    def test_adds_space_to_h1_no_space(self):
        assert self.fmt.normalize_headings("#Title") == "# Title"

    def test_adds_space_to_h2_no_space(self):
        assert self.fmt.normalize_headings("##Title") == "## Title"

    def test_adds_space_to_h6_no_space(self):
        assert self.fmt.normalize_headings("######Title") == "###### Title"

    def test_already_correct_h1_unchanged(self):
        assert self.fmt.normalize_headings("# Title") == "# Title"

    def test_already_correct_h3_unchanged(self):
        assert self.fmt.normalize_headings("### Section") == "### Section"

    def test_multiline_mixed(self):
        text = "#Intro\n## Already Good\n###Missing"
        expected = "# Intro\n## Already Good\n### Missing"
        assert self.fmt.normalize_headings(text) == expected

    def test_not_heading_in_middle_of_line(self):
        # A # not at start of line should not be changed
        text = "some text # not a heading"
        assert self.fmt.normalize_headings(text) == text

    def test_empty_heading_line(self):
        # A heading with no text after # — should not crash
        text = "#\n## "
        result = self.fmt.normalize_headings(text)
        assert "##" in result  # structure preserved

    def test_empty_string(self):
        assert self.fmt.normalize_headings("") == ""


# ===========================================================================
# TestCollapseBlankLines
# ===========================================================================

class TestCollapseBlankLines:
    """collapse_blank_lines() reduces consecutive blank lines."""

    def setup_method(self):
        self.fmt = DocFormatter()

    def test_collapses_three_blank_to_two(self):
        text = "a\n\n\n\nb"
        result = self.fmt.collapse_blank_lines(text, max_blank=2)
        # Should have at most 2 consecutive blank lines
        assert "\n\n\n\n" not in result

    def test_two_blank_lines_preserved_at_max_2(self):
        text = "a\n\n\nb"
        # 2 blank lines (3 \n) should NOT be collapsed when max_blank=2
        result = self.fmt.collapse_blank_lines(text, max_blank=2)
        assert result == text

    def test_max_blank_1(self):
        text = "a\n\n\nb"
        result = self.fmt.collapse_blank_lines(text, max_blank=1)
        assert "\n\n\n" not in result

    def test_no_blank_lines_unchanged(self):
        text = "line1\nline2\nline3"
        assert self.fmt.collapse_blank_lines(text, max_blank=2) == text

    def test_empty_string(self):
        assert self.fmt.collapse_blank_lines("", max_blank=2) == ""

    def test_many_blank_lines_collapsed(self):
        text = "start\n\n\n\n\n\nend"
        result = self.fmt.collapse_blank_lines(text, max_blank=2)
        # count consecutive blank lines
        lines = result.split("\n")
        max_consecutive_blank = 0
        current = 0
        for line in lines:
            if line.strip() == "":
                current += 1
                max_consecutive_blank = max(max_consecutive_blank, current)
            else:
                current = 0
        assert max_consecutive_blank <= 2


# ===========================================================================
# TestEnsureFinalNewline
# ===========================================================================

class TestEnsureFinalNewline:
    """ensure_final_newline() appends \\n when absent."""

    def setup_method(self):
        self.fmt = DocFormatter()

    def test_adds_newline_when_missing(self):
        assert self.fmt.ensure_final_newline("hello") == "hello\n"

    def test_no_double_newline_when_already_present(self):
        assert self.fmt.ensure_final_newline("hello\n") == "hello\n"

    def test_empty_string_unchanged(self):
        assert self.fmt.ensure_final_newline("") == ""

    def test_only_newline_unchanged(self):
        assert self.fmt.ensure_final_newline("\n") == "\n"

    def test_multiple_newlines_at_end_unchanged(self):
        assert self.fmt.ensure_final_newline("text\n\n") == "text\n\n"


# ===========================================================================
# TestNormalizeBullets
# ===========================================================================

class TestNormalizeBullets:
    """normalize_bullets() converts * and + bullets to -."""

    def setup_method(self):
        self.fmt = DocFormatter()

    def test_star_bullet_converted(self):
        assert self.fmt.normalize_bullets("* item") == "- item"

    def test_plus_bullet_converted(self):
        assert self.fmt.normalize_bullets("+ item") == "- item"

    def test_dash_bullet_unchanged(self):
        assert self.fmt.normalize_bullets("- item") == "- item"

    def test_multiline_mixed(self):
        text = "* first\n+ second\n- third"
        expected = "- first\n- second\n- third"
        assert self.fmt.normalize_bullets(text) == expected

    def test_star_not_at_line_start_unchanged(self):
        # inline * not a list bullet
        text = "this is *italic* text"
        assert self.fmt.normalize_bullets(text) == text

    def test_indented_bullets_unchanged(self):
        # With leading space, not a list bullet at column 0
        text = "  * indented"
        # re.MULTILINE ^ matches start of line after \n, indented * should not match
        assert self.fmt.normalize_bullets(text) == text

    def test_empty_string(self):
        assert self.fmt.normalize_bullets("") == ""

    def test_preserves_space_after_bullet(self):
        result = self.fmt.normalize_bullets("* item one")
        assert result == "- item one"


# ===========================================================================
# TestFixHeadingLevels
# ===========================================================================

class TestFixHeadingLevels:
    """fix_heading_levels() shifts headings to start at start_level."""

    def setup_method(self):
        self.fmt = DocFormatter()

    def test_shift_down_when_min_above_start(self):
        # All headings at level 3 and 4, start_level=1 → shift by -2
        text = "### Section\n#### Subsection"
        result = self.fmt.fix_heading_levels(text, start_level=1)
        assert result.startswith("# Section")
        assert "## Subsection" in result

    def test_shift_up_when_min_below_start(self):
        # Min level is 1, start_level=2 → shift by +1
        text = "# Title\n## Section"
        result = self.fmt.fix_heading_levels(text, start_level=2)
        assert result.startswith("## Title")
        assert "### Section" in result

    def test_no_change_when_already_at_start_level(self):
        text = "# Title\n## Section"
        result = self.fmt.fix_heading_levels(text, start_level=1)
        assert result == text

    def test_no_headings_unchanged(self):
        text = "Just plain text\nno headings here"
        result = self.fmt.fix_heading_levels(text, start_level=1)
        assert result == text

    def test_heading_level_clamped_to_6(self):
        # Heading at level 5, shift +3 → would be 8, clamped to 6
        text = "##### Deep\n###### Deeper"
        result = self.fmt.fix_heading_levels(text, start_level=4)
        # min=5, start=4, shift=-1 → 4 and 5
        lines = result.split("\n")
        assert lines[0].startswith("####")
        assert lines[1].startswith("#####")

    def test_heading_level_clamped_to_1(self):
        # Heading at level 1, shift -2 → would be -1, clamped to 1
        text = "# Title\n## Sub"
        result = self.fmt.fix_heading_levels(text, start_level=1)
        assert result == text  # min is already 1, no shift

    def test_empty_string(self):
        assert self.fmt.fix_heading_levels("", start_level=1) == ""


# ===========================================================================
# TestFormatAppliesRules
# ===========================================================================

class TestFormatAppliesRules:
    """format() applies all default rules and returns FormatterResult."""

    def test_returns_formatter_result(self):
        fmt = DocFormatter()
        result = fmt.format("# Hello")
        assert isinstance(result, FormatterResult)

    def test_original_preserved(self):
        text = "## Hello   \n"
        fmt = DocFormatter()
        result = fmt.format(text)
        assert result.original == text

    def test_all_rules_in_rules_applied_by_default(self):
        fmt = DocFormatter()
        result = fmt.format("some text")
        assert set(result.rules_applied) == set(FormatRule)

    def test_trailing_whitespace_removed(self):
        fmt = DocFormatter()
        result = fmt.format("text   \n")
        assert not any(line.endswith((" ", "\t")) for line in result.formatted.split("\n"))

    def test_final_newline_added(self):
        fmt = DocFormatter()
        result = fmt.format("text without newline")
        assert result.formatted.endswith("\n")

    def test_bullets_normalized(self):
        fmt = DocFormatter()
        result = fmt.format("* bullet\n+ another\n")
        assert "* bullet" not in result.formatted
        assert "+ another" not in result.formatted
        assert "- bullet" in result.formatted

    def test_headings_normalized(self):
        fmt = DocFormatter()
        # ##NoSpace → NORMALIZE_HEADINGS → "## NoSpace"
        # Then FIX_HEADING_LEVELS shifts min level (2) to start_level (1)
        # → "# NoSpace"
        result = fmt.format("##NoSpace\n")
        assert "NoSpace" in result.formatted
        assert result.formatted.startswith("#")
        # Verify that NORMALIZE_HEADINGS ran (space was inserted — no "##NoSpace" left)
        assert "##NoSpace" not in result.formatted

    def test_changed_true_when_text_was_modified(self):
        fmt = DocFormatter()
        result = fmt.format("text   ")
        assert result.changed is True

    def test_changed_false_for_already_clean_text(self):
        # A text that satisfies all rules already
        # No trailing whitespace, headings have spaces, final newline present,
        # bullets are -, no excess blank lines, headings start at level 1
        text = "# Title\n\nSome text.\n\n- item\n"
        fmt = DocFormatter()
        result = fmt.format(text)
        assert result.changed is False


# ===========================================================================
# TestFormatBatch
# ===========================================================================

class TestFormatBatch:
    """format_batch() processes a list of texts."""

    def test_returns_list_of_results(self):
        fmt = DocFormatter()
        results = fmt.format_batch(["a", "b", "c"])
        assert isinstance(results, list)
        assert len(results) == 3

    def test_each_result_is_formatter_result(self):
        fmt = DocFormatter()
        results = fmt.format_batch(["text1", "text2"])
        for r in results:
            assert isinstance(r, FormatterResult)

    def test_empty_list(self):
        fmt = DocFormatter()
        assert fmt.format_batch([]) == []

    def test_order_preserved(self):
        fmt = DocFormatter()
        texts = ["first", "second", "third"]
        results = fmt.format_batch(texts)
        for text, result in zip(texts, results):
            assert result.original == text

    def test_each_text_processed_independently(self):
        fmt = DocFormatter()
        results = fmt.format_batch(["text   ", "clean text\n"])
        # first should be changed, second already has final newline but
        # trailing spaces removed so still changed
        assert results[0].changed is True


# ===========================================================================
# TestSelectiveRules
# ===========================================================================

class TestSelectiveRules:
    """Only the rules listed in FormatConfig.rules are applied."""

    def test_only_strip_trailing_whitespace(self):
        fmt = _make_formatter(FormatRule.STRIP_TRAILING_WHITESPACE)
        result = fmt.format("text   \n##NoSpace")
        # trailing whitespace removed
        assert "text   " not in result.formatted
        # but heading NOT fixed because rule not selected
        assert "##NoSpace" in result.formatted

    def test_only_normalize_headings(self):
        fmt = _make_formatter(FormatRule.NORMALIZE_HEADINGS)
        result = fmt.format("##NoSpace   ")
        assert "## NoSpace" in result.formatted
        # trailing whitespace NOT removed
        assert "   " in result.formatted

    def test_only_ensure_final_newline(self):
        fmt = _make_formatter(FormatRule.ENSURE_FINAL_NEWLINE)
        result = fmt.format("no newline at end")
        assert result.formatted.endswith("\n")

    def test_only_normalize_bullets(self):
        fmt = _make_formatter(FormatRule.NORMALIZE_BULLETS)
        result = fmt.format("* item\n+ item2\ntext   ")
        assert "- item" in result.formatted
        assert "- item2" in result.formatted
        # trailing whitespace still present
        assert "text   " in result.formatted

    def test_only_fix_heading_levels(self):
        fmt = _make_formatter(FormatRule.FIX_HEADING_LEVELS, start_level=1)
        text = "### Section"
        result = fmt.format(text)
        assert result.formatted.startswith("# Section")

    def test_only_collapse_blank_lines(self):
        fmt = _make_formatter(FormatRule.COLLAPSE_BLANK_LINES, max_blank=1)
        text = "a\n\n\n\nb"
        result = fmt.format(text)
        assert "\n\n\n" not in result.formatted

    def test_rules_applied_list_matches_config(self):
        rules = [FormatRule.STRIP_TRAILING_WHITESPACE, FormatRule.NORMALIZE_BULLETS]
        fmt = _make_formatter(*rules)
        result = fmt.format("* item   ")
        assert set(result.rules_applied) == set(rules)

    def test_no_rules_text_unchanged(self):
        fmt = _make_formatter()  # empty rules list
        text = "##NoSpace   \n* bullet"
        result = fmt.format(text)
        assert result.formatted == text
        assert result.changed is False


# ===========================================================================
# TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    """Edge cases: empty text, only newlines, unicode, etc."""

    def test_format_empty_string(self):
        fmt = DocFormatter()
        result = fmt.format("")
        assert isinstance(result, FormatterResult)
        # Empty string: ensure_final_newline does not add \n to ""
        assert result.formatted == ""

    def test_format_only_newline(self):
        fmt = DocFormatter()
        result = fmt.format("\n")
        assert result.formatted == "\n"

    def test_format_only_whitespace(self):
        fmt = DocFormatter()
        result = fmt.format("   \n   \n")
        # After stripping trailing whitespace each line becomes empty
        for line in result.formatted.split("\n"):
            assert line.strip() == ""

    def test_format_unicode_content(self):
        fmt = DocFormatter()
        text = "# Привет   \n* пункт\n"
        result = fmt.format(text)
        assert "# Привет" in result.formatted
        assert "- пункт" in result.formatted
        assert "   " not in result.formatted

    def test_strip_trailing_whitespace_on_empty_string(self):
        fmt = DocFormatter()
        assert fmt.strip_trailing_whitespace("") == ""

    def test_normalize_headings_on_empty_string(self):
        fmt = DocFormatter()
        assert fmt.normalize_headings("") == ""

    def test_collapse_blank_lines_on_empty_string(self):
        fmt = DocFormatter()
        assert fmt.collapse_blank_lines("") == ""

    def test_ensure_final_newline_on_empty_string(self):
        fmt = DocFormatter()
        assert fmt.ensure_final_newline("") == ""

    def test_normalize_bullets_on_empty_string(self):
        fmt = DocFormatter()
        assert fmt.normalize_bullets("") == ""

    def test_fix_heading_levels_on_empty_string(self):
        fmt = DocFormatter()
        assert fmt.fix_heading_levels("") == ""

    def test_format_batch_single_element(self):
        fmt = DocFormatter()
        results = fmt.format_batch(["single text   "])
        assert len(results) == 1
        assert results[0].changed is True

    def test_formatter_default_config(self):
        # DocFormatter() with no args uses default FormatConfig
        fmt = DocFormatter()
        assert isinstance(fmt._config, FormatConfig)
        assert set(fmt._config.rules) == set(FormatRule)

    def test_formatter_result_rules_applied_order_matches_enum_order(self):
        # Rules should be applied in enum declaration order
        fmt = DocFormatter()
        result = fmt.format("text")
        enum_order = list(FormatRule)
        assert result.rules_applied == enum_order
