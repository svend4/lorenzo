"""Tests for docstoolkit.doc_validator — ≥50 tests covering all rules and edge cases."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.doc_validator import (
    DocValidator,
    ValidationConfig,
    ValidationResult,
    ValidationIssue,
    Severity,
    NO_H1,
    MULTIPLE_H1,
    EMPTY_SECTION,
    MISSING_FRONTMATTER,
    LONG_LINE,
    BROKEN_HEADING_HIERARCHY,
    DUPLICATE_HEADING,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validator(**kwargs) -> DocValidator:
    return DocValidator(ValidationConfig(**kwargs))


def _rule_ids(issues: list[ValidationIssue]) -> list[str]:
    return [i.rule_id for i in issues]


# ---------------------------------------------------------------------------
# TestSeverity
# ---------------------------------------------------------------------------

class TestSeverity:
    def test_error_member(self):
        assert Severity.ERROR.value == "ERROR"

    def test_warning_member(self):
        assert Severity.WARNING.value == "WARNING"

    def test_info_member(self):
        assert Severity.INFO.value == "INFO"

    def test_distinct_members(self):
        assert Severity.ERROR != Severity.WARNING
        assert Severity.WARNING != Severity.INFO
        assert Severity.ERROR != Severity.INFO

    def test_enum_identity(self):
        assert Severity("ERROR") is Severity.ERROR


# ---------------------------------------------------------------------------
# TestValidationIssue
# ---------------------------------------------------------------------------

class TestValidationIssue:
    def test_required_fields(self):
        issue = ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="oops")
        assert issue.rule_id == NO_H1
        assert issue.severity == Severity.ERROR
        assert issue.message == "oops"

    def test_optional_fields_default_none(self):
        issue = ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="x")
        assert issue.line_num is None
        assert issue.context is None

    def test_line_num_stored(self):
        issue = ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="x", line_num=5)
        assert issue.line_num == 5

    def test_context_stored(self):
        issue = ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="x", context="# Title")
        assert issue.context == "# Title"

    def test_dataclass_equality(self):
        a = ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="m")
        b = ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="m")
        assert a == b


# ---------------------------------------------------------------------------
# TestValidationResultProperties
# ---------------------------------------------------------------------------

class TestValidationResultProperties:
    def _make_result(self, *severities: Severity) -> ValidationResult:
        issues = [
            ValidationIssue(rule_id="r", severity=s, message="m")
            for s in severities
        ]
        return ValidationResult(issues=issues)

    def test_is_valid_no_issues(self):
        result = ValidationResult()
        assert result.is_valid is True

    def test_is_valid_only_warnings(self):
        result = self._make_result(Severity.WARNING, Severity.INFO)
        assert result.is_valid is True

    def test_is_valid_false_with_error(self):
        result = self._make_result(Severity.ERROR)
        assert result.is_valid is False

    def test_errors_property_filters(self):
        result = self._make_result(Severity.ERROR, Severity.WARNING, Severity.INFO)
        assert len(result.errors) == 1
        assert result.errors[0].severity == Severity.ERROR

    def test_warnings_property_filters(self):
        result = self._make_result(Severity.ERROR, Severity.WARNING, Severity.WARNING)
        assert len(result.warnings) == 2

    def test_error_count(self):
        result = self._make_result(Severity.ERROR, Severity.ERROR, Severity.WARNING)
        assert result.error_count == 2

    def test_warning_count(self):
        result = self._make_result(Severity.WARNING)
        assert result.warning_count == 1

    def test_by_rule_returns_matching(self):
        issues = [
            ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="a"),
            ValidationIssue(rule_id=MULTIPLE_H1, severity=Severity.WARNING, message="b"),
            ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="c"),
        ]
        result = ValidationResult(issues=issues)
        found = result.by_rule(NO_H1)
        assert len(found) == 2
        assert all(i.rule_id == NO_H1 for i in found)

    def test_by_rule_unknown_returns_empty(self):
        result = ValidationResult(issues=[
            ValidationIssue(rule_id=NO_H1, severity=Severity.ERROR, message="a"),
        ])
        assert result.by_rule("unknown_rule") == []

    def test_issues_default_empty(self):
        result = ValidationResult()
        assert result.issues == []


# ---------------------------------------------------------------------------
# TestCheckH1
# ---------------------------------------------------------------------------

class TestCheckH1:
    def _v(self) -> DocValidator:
        return DocValidator()

    def test_no_h1_yields_error(self):
        text = "## Some section\n\nContent here.\n"
        issues = self._v().check_h1(text)
        assert any(i.rule_id == NO_H1 and i.severity == Severity.ERROR for i in issues)

    def test_one_h1_no_issues(self):
        text = "# Title\n\nContent.\n"
        issues = self._v().check_h1(text)
        assert issues == []

    def test_multiple_h1_yields_warning(self):
        text = "# First\n\n# Second\n\nContent.\n"
        issues = self._v().check_h1(text)
        assert any(i.rule_id == MULTIPLE_H1 and i.severity == Severity.WARNING for i in issues)

    def test_multiple_h1_no_error(self):
        text = "# First\n\n# Second\n"
        issues = self._v().check_h1(text)
        assert not any(i.rule_id == NO_H1 for i in issues)

    def test_multiple_h1_reports_second_occurrence(self):
        text = "# First\n\n# Second\n\n# Third\n"
        issues = self._v().check_h1(text)
        multiple = [i for i in issues if i.rule_id == MULTIPLE_H1]
        assert len(multiple) == 2

    def test_h2_only_triggers_no_h1(self):
        text = "## Section\n\nBody.\n"
        issues = self._v().check_h1(text)
        assert _rule_ids(issues) == [NO_H1]

    def test_h1_inside_code_block_ignored(self):
        text = "```\n# not a heading\n```\n\n# Real Title\n"
        issues = self._v().check_h1(text)
        assert issues == []


# ---------------------------------------------------------------------------
# TestCheckHeadingHierarchy
# ---------------------------------------------------------------------------

class TestCheckHeadingHierarchy:
    def _v(self) -> DocValidator:
        return DocValidator()

    def test_sequential_levels_ok(self):
        text = "# H1\n## H2\n### H3\n"
        issues = self._v().check_heading_hierarchy(text)
        assert issues == []

    def test_h1_to_h3_is_violation(self):
        text = "# H1\n### H3\n"
        issues = self._v().check_heading_hierarchy(text)
        assert any(i.rule_id == BROKEN_HEADING_HIERARCHY for i in issues)

    def test_first_violation_only(self):
        text = "# H1\n### H3\n##### H5\n"
        issues = self._v().check_heading_hierarchy(text)
        bh = [i for i in issues if i.rule_id == BROKEN_HEADING_HIERARCHY]
        assert len(bh) == 1

    def test_h2_to_h4_is_violation(self):
        text = "## H2\n#### H4\n"
        issues = self._v().check_heading_hierarchy(text)
        assert any(i.rule_id == BROKEN_HEADING_HIERARCHY for i in issues)

    def test_going_back_up_is_ok(self):
        # h1 -> h2 -> h3 -> h2 is fine (going up is allowed)
        text = "# H1\n## H2\n### H3\n## H2 again\n"
        issues = self._v().check_heading_hierarchy(text)
        assert issues == []

    def test_single_heading_ok(self):
        text = "# Solo\n"
        issues = self._v().check_heading_hierarchy(text)
        assert issues == []

    def test_violation_reports_correct_line(self):
        text = "# H1\n\n### H3\n"
        issues = self._v().check_heading_hierarchy(text)
        bh = [i for i in issues if i.rule_id == BROKEN_HEADING_HIERARCHY]
        assert bh[0].line_num == 3

    def test_violation_includes_context(self):
        text = "# H1\n### H3\n"
        issues = self._v().check_heading_hierarchy(text)
        bh = [i for i in issues if i.rule_id == BROKEN_HEADING_HIERARCHY]
        assert bh[0].context is not None
        assert "H3" in bh[0].context or "###" in bh[0].context


# ---------------------------------------------------------------------------
# TestCheckDuplicateHeadings
# ---------------------------------------------------------------------------

class TestCheckDuplicateHeadings:
    def _v(self) -> DocValidator:
        return DocValidator()

    def test_no_duplicates_ok(self):
        text = "# Title\n## Intro\n## Body\n"
        assert self._v().check_duplicate_headings(text) == []

    def test_same_level_same_text_is_duplicate(self):
        text = "# Title\n## Section\n## Section\n"
        issues = self._v().check_duplicate_headings(text)
        assert any(i.rule_id == DUPLICATE_HEADING for i in issues)

    def test_different_levels_not_duplicate(self):
        text = "# Section\n## Section\n"
        assert self._v().check_duplicate_headings(text) == []

    def test_case_insensitive_duplicate(self):
        text = "## Introduction\n## introduction\n"
        issues = self._v().check_duplicate_headings(text)
        assert any(i.rule_id == DUPLICATE_HEADING for i in issues)

    def test_duplicate_reports_second_line(self):
        text = "# H1\n## Dup\n\nsome content\n\n## Dup\n"
        issues = self._v().check_duplicate_headings(text)
        dup = [i for i in issues if i.rule_id == DUPLICATE_HEADING]
        assert dup[0].line_num == 6

    def test_triple_duplicate_reports_twice(self):
        text = "## A\n## A\n## A\n"
        issues = self._v().check_duplicate_headings(text)
        dups = [i for i in issues if i.rule_id == DUPLICATE_HEADING]
        assert len(dups) == 2


# ---------------------------------------------------------------------------
# TestCheckEmptySections
# ---------------------------------------------------------------------------

class TestCheckEmptySections:
    def _v(self) -> DocValidator:
        return DocValidator()

    def test_section_with_content_ok(self):
        text = "# Title\n\nSome body text.\n"
        assert self._v().check_empty_sections(text) == []

    def test_empty_section_before_next_heading(self):
        text = "# Title\n\n## Empty\n\n## HasContent\n\nContent.\n"
        issues = self._v().check_empty_sections(text)
        empty = [i for i in issues if i.rule_id == EMPTY_SECTION]
        assert len(empty) >= 1
        assert any("Empty" in i.message for i in empty)

    def test_empty_section_at_end_of_doc(self):
        text = "# Title\n\nContent.\n\n## Orphan\n"
        issues = self._v().check_empty_sections(text)
        assert any(i.rule_id == EMPTY_SECTION for i in issues)

    def test_section_with_only_blank_lines_is_empty(self):
        text = "## Heading\n\n\n## Next\n\nContent.\n"
        issues = self._v().check_empty_sections(text)
        assert any(i.rule_id == EMPTY_SECTION for i in issues)

    def test_reports_correct_line(self):
        text = "# Title\n\nContent.\n\n## EmptySection\n\n## Other\n\nBody.\n"
        issues = self._v().check_empty_sections(text)
        empty = [i for i in issues if i.rule_id == EMPTY_SECTION]
        assert empty[0].line_num == 5


# ---------------------------------------------------------------------------
# TestCheckFrontmatter
# ---------------------------------------------------------------------------

class TestCheckFrontmatter:
    def test_no_require_frontmatter_default_skips(self):
        text = "# Title\n\nContent.\n"
        v = DocValidator(ValidationConfig(require_frontmatter=False))
        # check_frontmatter is always callable directly, but validate() skips it
        result = v.validate(text)
        assert not any(i.rule_id == MISSING_FRONTMATTER for i in result.issues)

    def test_require_frontmatter_missing_yields_warning(self):
        text = "# Title\n\nContent.\n"
        v = DocValidator(ValidationConfig(require_frontmatter=True))
        issues = v.check_frontmatter(text)
        assert any(i.rule_id == MISSING_FRONTMATTER and i.severity == Severity.WARNING for i in issues)

    def test_require_frontmatter_present_ok(self):
        text = "---\ntitle: Doc\n---\n\n# Title\n"
        v = DocValidator(ValidationConfig(require_frontmatter=True))
        issues = v.check_frontmatter(text)
        assert not any(i.rule_id == MISSING_FRONTMATTER for i in issues)

    def test_frontmatter_line_num_is_1(self):
        text = "# No frontmatter\n"
        issues = DocValidator().check_frontmatter(text)
        missing = [i for i in issues if i.rule_id == MISSING_FRONTMATTER]
        if missing:
            assert missing[0].line_num == 1

    def test_validate_includes_frontmatter_when_required(self):
        text = "# Title\n\nContent.\n"
        v = DocValidator(ValidationConfig(require_frontmatter=True))
        result = v.validate(text)
        assert any(i.rule_id == MISSING_FRONTMATTER for i in result.issues)


# ---------------------------------------------------------------------------
# TestCheckLineLength
# ---------------------------------------------------------------------------

class TestCheckLineLength:
    def _v(self, max_len: int = 0) -> DocValidator:
        return DocValidator(ValidationConfig(max_line_length=max_len))

    def test_zero_max_skips_check(self):
        long_line = "x" * 200
        issues = self._v(0).check_line_length(long_line, 0)
        assert issues == []

    def test_line_within_limit_ok(self):
        text = "Short line.\n"
        issues = self._v(100).check_line_length(text, 100)
        assert issues == []

    def test_line_exactly_at_limit_ok(self):
        text = "a" * 80 + "\n"
        issues = self._v(80).check_line_length(text, 80)
        assert issues == []

    def test_line_over_limit_yields_info(self):
        text = "a" * 81 + "\n"
        issues = self._v(80).check_line_length(text, 80)
        assert any(i.rule_id == LONG_LINE and i.severity == Severity.INFO for i in issues)

    def test_multiple_long_lines_all_reported(self):
        text = "a" * 100 + "\n" + "b" * 100 + "\n"
        issues = self._v(80).check_line_length(text, 80)
        long = [i for i in issues if i.rule_id == LONG_LINE]
        assert len(long) == 2

    def test_reports_correct_line_numbers(self):
        text = "short\n" + "x" * 100 + "\nshort\n"
        issues = self._v(80).check_line_length(text, 80)
        long = [i for i in issues if i.rule_id == LONG_LINE]
        assert long[0].line_num == 2

    def test_validate_respects_max_line_length_zero(self):
        text = "# T\n\n" + "x" * 300 + "\n"
        v = DocValidator(ValidationConfig(max_line_length=0))
        result = v.validate(text)
        assert not any(i.rule_id == LONG_LINE for i in result.issues)

    def test_validate_respects_max_line_length_nonzero(self):
        text = "# T\n\n" + "x" * 300 + "\n"
        v = DocValidator(ValidationConfig(max_line_length=80))
        result = v.validate(text)
        assert any(i.rule_id == LONG_LINE for i in result.issues)


# ---------------------------------------------------------------------------
# TestValidationConfig
# ---------------------------------------------------------------------------

class TestValidationConfig:
    def test_defaults(self):
        cfg = ValidationConfig()
        assert cfg.require_h1 is True
        assert cfg.require_frontmatter is False
        assert cfg.max_line_length == 0
        assert cfg.check_heading_hierarchy is True
        assert cfg.check_duplicate_headings is True
        assert cfg.check_empty_sections is True
        assert cfg.disabled_rules == []

    def test_custom_values(self):
        cfg = ValidationConfig(require_h1=False, max_line_length=120)
        assert cfg.require_h1 is False
        assert cfg.max_line_length == 120

    def test_disabled_rules_list(self):
        cfg = ValidationConfig(disabled_rules=[NO_H1, MULTIPLE_H1])
        assert NO_H1 in cfg.disabled_rules
        assert MULTIPLE_H1 in cfg.disabled_rules

    def test_disabled_rules_default_independent(self):
        cfg1 = ValidationConfig()
        cfg2 = ValidationConfig()
        cfg1.disabled_rules.append(NO_H1)
        assert NO_H1 not in cfg2.disabled_rules


# ---------------------------------------------------------------------------
# TestValidateIntegration
# ---------------------------------------------------------------------------

class TestValidateIntegration:
    def test_valid_doc_returns_no_errors(self):
        text = "# Title\n\nSome body content here.\n\n## Section\n\nMore text.\n"
        v = DocValidator()
        result = v.validate(text)
        assert result.is_valid

    def test_missing_h1_gives_error(self):
        text = "## No H1 here\n\nContent.\n"
        v = DocValidator()
        result = v.validate(text)
        assert not result.is_valid
        assert any(i.rule_id == NO_H1 for i in result.errors)

    def test_validate_returns_validation_result(self):
        v = DocValidator()
        result = v.validate("# Title\n")
        assert isinstance(result, ValidationResult)

    def test_require_h1_false_skips_h1_check(self):
        text = "## No H1\n\nContent.\n"
        v = DocValidator(ValidationConfig(require_h1=False))
        result = v.validate(text)
        assert not any(i.rule_id == NO_H1 for i in result.issues)

    def test_check_heading_hierarchy_false_skips(self):
        text = "# H1\n### H3\n\nContent.\n"
        v = DocValidator(ValidationConfig(check_heading_hierarchy=False))
        result = v.validate(text)
        assert not any(i.rule_id == BROKEN_HEADING_HIERARCHY for i in result.issues)

    def test_check_duplicate_headings_false_skips(self):
        text = "# H1\n\n## Dup\n\nContent.\n\n## Dup\n\nMore.\n"
        v = DocValidator(ValidationConfig(check_duplicate_headings=False))
        result = v.validate(text)
        assert not any(i.rule_id == DUPLICATE_HEADING for i in result.issues)

    def test_check_empty_sections_false_skips(self):
        text = "# H1\n\n## Empty\n\n## Other\n\nBody.\n"
        v = DocValidator(ValidationConfig(check_empty_sections=False))
        result = v.validate(text)
        assert not any(i.rule_id == EMPTY_SECTION for i in result.issues)

    def test_multiple_issues_accumulated(self):
        # No H1, broken hierarchy, duplicate heading, empty section
        text = "### Start\n\n##### Skip\n\n### Start\n\n### Other\n"
        v = DocValidator()
        result = v.validate(text)
        rule_ids = _rule_ids(result.issues)
        assert NO_H1 in rule_ids


# ---------------------------------------------------------------------------
# TestValidateBatch
# ---------------------------------------------------------------------------

class TestValidateBatch:
    def test_returns_list_of_results(self):
        texts = ["# Doc1\n\nContent.\n", "# Doc2\n\nContent.\n"]
        v = DocValidator()
        results = v.validate_batch(texts)
        assert isinstance(results, list)
        assert len(results) == 2

    def test_each_result_is_validation_result(self):
        v = DocValidator()
        results = v.validate_batch(["# A\n\nContent.\n", "## No H1\n\nContent.\n"])
        assert all(isinstance(r, ValidationResult) for r in results)

    def test_batch_independent_results(self):
        texts = [
            "# Good\n\nContent.\n",
            "## No H1\n\nContent.\n",
        ]
        v = DocValidator()
        results = v.validate_batch(texts)
        assert results[0].is_valid
        assert not results[1].is_valid

    def test_empty_batch(self):
        v = DocValidator()
        assert v.validate_batch([]) == []

    def test_single_item_batch(self):
        v = DocValidator()
        results = v.validate_batch(["# Title\n\nContent.\n"])
        assert len(results) == 1


# ---------------------------------------------------------------------------
# TestDisabledRules
# ---------------------------------------------------------------------------

class TestDisabledRules:
    def test_disabled_no_h1(self):
        text = "## No H1\n\nContent.\n"
        v = DocValidator(ValidationConfig(disabled_rules=[NO_H1]))
        result = v.validate(text)
        assert not any(i.rule_id == NO_H1 for i in result.issues)

    def test_disabled_multiple_h1(self):
        text = "# First\n\n# Second\n\nContent.\n"
        v = DocValidator(ValidationConfig(disabled_rules=[MULTIPLE_H1]))
        result = v.validate(text)
        assert not any(i.rule_id == MULTIPLE_H1 for i in result.issues)

    def test_disabled_broken_hierarchy(self):
        text = "# H1\n### H3\n\nContent.\n"
        v = DocValidator(ValidationConfig(disabled_rules=[BROKEN_HEADING_HIERARCHY]))
        result = v.validate(text)
        assert not any(i.rule_id == BROKEN_HEADING_HIERARCHY for i in result.issues)

    def test_disabled_duplicate_heading(self):
        text = "# H1\n\n## Dup\n\nContent.\n\n## Dup\n\nMore.\n"
        v = DocValidator(ValidationConfig(disabled_rules=[DUPLICATE_HEADING]))
        result = v.validate(text)
        assert not any(i.rule_id == DUPLICATE_HEADING for i in result.issues)

    def test_disabled_empty_section(self):
        text = "# H1\n\n## Empty\n\n## HasContent\n\nContent.\n"
        v = DocValidator(ValidationConfig(disabled_rules=[EMPTY_SECTION]))
        result = v.validate(text)
        assert not any(i.rule_id == EMPTY_SECTION for i in result.issues)

    def test_disabled_long_line(self):
        text = "# T\n\n" + "x" * 200 + "\n"
        v = DocValidator(ValidationConfig(max_line_length=80, disabled_rules=[LONG_LINE]))
        result = v.validate(text)
        assert not any(i.rule_id == LONG_LINE for i in result.issues)

    def test_disabled_missing_frontmatter(self):
        text = "# Title\n\nContent.\n"
        v = DocValidator(ValidationConfig(
            require_frontmatter=True,
            disabled_rules=[MISSING_FRONTMATTER],
        ))
        result = v.validate(text)
        assert not any(i.rule_id == MISSING_FRONTMATTER for i in result.issues)

    def test_disabled_multiple_rules(self):
        text = "## No H1\n### Hierarchy\n\nContent.\n"
        v = DocValidator(ValidationConfig(disabled_rules=[NO_H1, BROKEN_HEADING_HIERARCHY]))
        result = v.validate(text)
        assert not any(i.rule_id in (NO_H1, BROKEN_HEADING_HIERARCHY) for i in result.issues)


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_document(self):
        v = DocValidator()
        result = v.validate("")
        # No H1 in empty doc should give error
        assert any(i.rule_id == NO_H1 for i in result.errors)

    def test_only_whitespace(self):
        v = DocValidator()
        result = v.validate("   \n\n  \n")
        assert any(i.rule_id == NO_H1 for i in result.errors)

    def test_only_heading_no_content_is_empty_section(self):
        text = "# Title\n"
        v = DocValidator()
        result = v.validate(text)
        empty = [i for i in result.issues if i.rule_id == EMPTY_SECTION]
        assert len(empty) >= 1

    def test_h1_with_content_no_empty_section(self):
        text = "# Title\n\nContent here.\n"
        v = DocValidator()
        result = v.validate(text)
        assert not any(i.rule_id == EMPTY_SECTION for i in result.issues)

    def test_heading_in_code_block_not_counted(self):
        text = "# Real Title\n\n```\n# Not a heading\n## Also not\n```\n\nContent.\n"
        v = DocValidator()
        result = v.validate(text)
        # Should still be valid — only one real H1
        assert result.is_valid

    def test_tilde_code_block_headings_ignored(self):
        text = "# Real Title\n\n~~~\n# Fake H1\n~~~\n\nContent.\n"
        v = DocValidator()
        # Should not trigger multiple_h1
        issues = v.check_h1(text)
        assert not any(i.rule_id == MULTIPLE_H1 for i in issues)

    def test_doc_with_no_headings_at_all(self):
        text = "Just some plain text.\nNo headings here.\n"
        v = DocValidator()
        result = v.validate(text)
        assert any(i.rule_id == NO_H1 for i in result.errors)

    def test_frontmatter_present_not_missing(self):
        text = "---\ntitle: My Doc\nauthor: Alice\n---\n\n# Title\n\nContent.\n"
        v = DocValidator(ValidationConfig(require_frontmatter=True))
        result = v.validate(text)
        assert not any(i.rule_id == MISSING_FRONTMATTER for i in result.issues)

    def test_h1_immediately_followed_by_h2(self):
        # h1 -> h2 is fine, no hierarchy violation
        text = "# H1\n## H2\n\nContent.\n"
        v = DocValidator()
        result = v.validate(text)
        assert not any(i.rule_id == BROKEN_HEADING_HIERARCHY for i in result.issues)

    def test_require_h1_false_valid_no_h1(self):
        text = "## Section\n\nContent.\n"
        v = DocValidator(ValidationConfig(require_h1=False))
        result = v.validate(text)
        assert result.is_valid
