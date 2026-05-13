"""Tests for the doc_health_check module (E212)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_health_check import (
    DocHealthCheck,
    HealthIssue,
    HealthReport,
    IssueSeverity,
)
from docstoolkit.doc_health_check.check import (
    check_content_present,
    check_has_tags,
    check_max_line_length,
    check_no_broken_links,
    check_no_empty_headings,
    check_no_trailing_whitespace,
    check_title_present,
)


# --------------------------------------------------------------------------- #
class TestIssueSeverity:
    def test_severity_members(self):
        assert IssueSeverity.INFO.value == "info"
        assert IssueSeverity.WARNING.value == "warning"
        assert IssueSeverity.ERROR.value == "error"

    def test_severity_distinct(self):
        assert IssueSeverity.INFO != IssueSeverity.WARNING
        assert IssueSeverity.WARNING != IssueSeverity.ERROR

    def test_severity_count(self):
        assert len(list(IssueSeverity)) == 3


# --------------------------------------------------------------------------- #
class TestHealthIssue:
    def test_minimal_construction(self):
        issue = HealthIssue(
            check_name="t", severity=IssueSeverity.INFO, message="m"
        )
        assert issue.check_name == "t"
        assert issue.severity == IssueSeverity.INFO
        assert issue.message == "m"
        assert issue.line_num is None
        assert issue.field is None

    def test_full_construction(self):
        issue = HealthIssue(
            check_name="t",
            severity=IssueSeverity.ERROR,
            message="m",
            line_num=42,
            field="content",
        )
        assert issue.line_num == 42
        assert issue.field == "content"


# --------------------------------------------------------------------------- #
class TestHealthReport:
    def test_empty_report(self):
        rep = HealthReport(doc_id="d", issues=[], score=100.0, passed=True)
        assert rep.info_count == 0
        assert rep.warning_count == 0
        assert rep.error_count == 0
        assert rep.total_issues == 0

    def test_counts(self):
        issues = [
            HealthIssue("a", IssueSeverity.INFO, "m"),
            HealthIssue("b", IssueSeverity.INFO, "m"),
            HealthIssue("c", IssueSeverity.WARNING, "m"),
            HealthIssue("d", IssueSeverity.ERROR, "m"),
        ]
        rep = HealthReport(doc_id="d", issues=issues, score=70.0, passed=False)
        assert rep.info_count == 2
        assert rep.warning_count == 1
        assert rep.error_count == 1
        assert rep.total_issues == 4


# --------------------------------------------------------------------------- #
class TestRegisterCheck:
    def test_register_new_check(self):
        hc = DocHealthCheck()
        before = hc.check_count

        def custom(doc):
            return []

        hc.register_check("custom", custom)
        assert hc.check_count == before + 1
        assert "custom" in hc.available_checks()

    def test_register_replaces_existing(self):
        hc = DocHealthCheck()
        hc.register_check("dup", lambda d: [])
        hc.register_check("dup", lambda d: [])
        # Still single entry
        assert hc.available_checks().count("dup") == 1

    def test_register_disabled(self):
        hc = DocHealthCheck()
        hc.register_check("offcheck", lambda d: [], enabled=False)
        assert "offcheck" in hc.available_checks()
        assert "offcheck" not in hc.available_checks(enabled_only=True)


# --------------------------------------------------------------------------- #
class TestUnregisterCheck:
    def test_unregister_existing(self):
        hc = DocHealthCheck()
        assert hc.unregister_check("check_title_present") is True
        assert "check_title_present" not in hc.available_checks()

    def test_unregister_missing(self):
        hc = DocHealthCheck()
        assert hc.unregister_check("nope") is False


# --------------------------------------------------------------------------- #
class TestEnableDisable:
    def test_disable_existing(self):
        hc = DocHealthCheck()
        assert hc.disable_check("check_has_tags") is True
        assert "check_has_tags" not in hc.available_checks(enabled_only=True)

    def test_enable_after_disable(self):
        hc = DocHealthCheck()
        hc.disable_check("check_has_tags")
        assert hc.enable_check("check_has_tags") is True
        assert "check_has_tags" in hc.available_checks(enabled_only=True)

    def test_enable_missing(self):
        hc = DocHealthCheck()
        assert hc.enable_check("missing") is False

    def test_disable_missing(self):
        hc = DocHealthCheck()
        assert hc.disable_check("missing") is False


# --------------------------------------------------------------------------- #
class TestRunBasic:
    def test_run_returns_report(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T", "content": "Hello world content."})
        assert isinstance(report, HealthReport)

    def test_run_doc_id_default(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T", "content": "Hello world content."})
        assert report.doc_id == "doc"

    def test_run_custom_doc_id(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T", "content": "Hello world content."}, doc_id="x42")
        assert report.doc_id == "x42"

    def test_run_disabled_check_skipped(self):
        hc = DocHealthCheck()
        hc.disable_check("check_title_present")
        report = hc.run({"content": "Hello world content."})
        # error from title check shouldn't appear
        names = {i.check_name for i in report.issues}
        assert "check_title_present" not in names


# --------------------------------------------------------------------------- #
class TestRunWithError:
    def test_missing_title_produces_error(self):
        hc = DocHealthCheck()
        report = hc.run({"content": "Hello world content."})
        assert report.error_count >= 1
        assert report.passed is False

    def test_empty_title_produces_error(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "   ", "content": "Hello world content."})
        assert any(
            i.check_name == "check_title_present" and i.severity == IssueSeverity.ERROR
            for i in report.issues
        )


# --------------------------------------------------------------------------- #
class TestRunWithWarning:
    def test_short_content_produces_warning(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T", "content": "hi"})
        assert any(
            i.check_name == "check_content_present"
            and i.severity == IssueSeverity.WARNING
            for i in report.issues
        )

    def test_missing_content_produces_warning(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T"})
        assert any(
            i.check_name == "check_content_present"
            and i.severity == IssueSeverity.WARNING
            for i in report.issues
        )

    def test_empty_heading_warning(self):
        hc = DocHealthCheck()
        content = "Some intro text here.\n#\nMore body content."
        report = hc.run({"title": "T", "content": content, "tags": ["a"]})
        assert any(
            i.check_name == "check_no_empty_headings"
            and i.severity == IssueSeverity.WARNING
            for i in report.issues
        )


# --------------------------------------------------------------------------- #
class TestRunWithInfo:
    def test_missing_tags_info(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T", "content": "Hello world content."})
        assert any(
            i.check_name == "check_has_tags" and i.severity == IssueSeverity.INFO
            for i in report.issues
        )

    def test_trailing_whitespace_info(self):
        hc = DocHealthCheck()
        content = "Line with trailing space   \nClean line here"
        report = hc.run({"title": "T", "content": content, "tags": ["a"]})
        assert any(
            i.check_name == "check_no_trailing_whitespace"
            and i.severity == IssueSeverity.INFO
            for i in report.issues
        )


# --------------------------------------------------------------------------- #
class TestRunPerfect:
    def test_perfect_doc_scores_100(self):
        hc = DocHealthCheck()
        doc = {
            "title": "Perfect Doc",
            "content": "This is a sufficiently long body without trailing space.",
            "tags": ["good"],
        }
        report = hc.run(doc)
        assert report.score == 100.0
        assert report.passed is True
        assert report.total_issues == 0

    def test_perfect_doc_no_issues(self):
        hc = DocHealthCheck()
        doc = {
            "title": "Title",
            "content": "Plain prose without markdown links or headings here at all.",
            "tags": ["x"],
        }
        report = hc.run(doc)
        assert report.issues == []


# --------------------------------------------------------------------------- #
class TestRunBatch:
    def test_batch_length(self):
        hc = DocHealthCheck()
        docs = [
            {"title": "A", "content": "long enough content here", "tags": ["a"]},
            {"title": "B", "content": "long enough content here", "tags": ["b"]},
            {"title": "C", "content": "long enough content here", "tags": ["c"]},
        ]
        reports = hc.run_batch(docs)
        assert len(reports) == 3

    def test_batch_doc_ids_default(self):
        hc = DocHealthCheck()
        docs = [{"title": "A", "content": "x" * 30, "tags": ["a"]} for _ in range(2)]
        reports = hc.run_batch(docs)
        assert reports[0].doc_id == "doc_0"
        assert reports[1].doc_id == "doc_1"

    def test_batch_doc_ids_from_field(self):
        hc = DocHealthCheck()
        docs = [
            {"id": "alpha", "title": "A", "content": "x" * 30, "tags": ["a"]},
            {"id": "beta", "title": "B", "content": "x" * 30, "tags": ["b"]},
        ]
        reports = hc.run_batch(docs)
        assert reports[0].doc_id == "alpha"
        assert reports[1].doc_id == "beta"

    def test_batch_empty(self):
        hc = DocHealthCheck()
        assert hc.run_batch([]) == []


# --------------------------------------------------------------------------- #
class TestAvailableChecks:
    def test_lists_builtins(self):
        hc = DocHealthCheck()
        names = hc.available_checks()
        for n in [
            "check_title_present",
            "check_content_present",
            "check_no_broken_links",
            "check_no_empty_headings",
            "check_no_trailing_whitespace",
            "check_has_tags",
            "check_max_line_length",
        ]:
            assert n in names

    def test_enabled_only_filter(self):
        hc = DocHealthCheck()
        hc.disable_check("check_has_tags")
        enabled = hc.available_checks(enabled_only=True)
        assert "check_has_tags" not in enabled
        assert "check_title_present" in enabled


# --------------------------------------------------------------------------- #
class TestCheckCount:
    def test_initial_count(self):
        hc = DocHealthCheck()
        assert hc.check_count == 7

    def test_count_after_register(self):
        hc = DocHealthCheck()
        hc.register_check("c1", lambda d: [])
        hc.register_check("c2", lambda d: [])
        assert hc.check_count == 9

    def test_count_after_unregister(self):
        hc = DocHealthCheck()
        hc.unregister_check("check_has_tags")
        assert hc.check_count == 6


# --------------------------------------------------------------------------- #
class TestClear:
    def test_clear_removes_all(self):
        hc = DocHealthCheck()
        hc.clear()
        assert hc.check_count == 0
        assert hc.available_checks() == []

    def test_after_clear_run_no_issues(self):
        hc = DocHealthCheck()
        hc.clear()
        report = hc.run({})
        assert report.total_issues == 0
        assert report.score == 100.0
        assert report.passed is True


# --------------------------------------------------------------------------- #
class TestBuiltinTitlePresent:
    def test_present(self):
        assert check_title_present({"title": "Hi"}) == []

    def test_missing(self):
        issues = check_title_present({})
        assert len(issues) == 1
        assert issues[0].severity == IssueSeverity.ERROR

    def test_empty_string(self):
        issues = check_title_present({"title": ""})
        assert len(issues) == 1

    def test_whitespace_only(self):
        issues = check_title_present({"title": "   "})
        assert len(issues) == 1


# --------------------------------------------------------------------------- #
class TestBuiltinContentPresent:
    def test_long_content(self):
        assert check_content_present({"content": "x" * 50}) == []

    def test_short_content(self):
        issues = check_content_present({"content": "hi"})
        assert len(issues) == 1
        assert issues[0].severity == IssueSeverity.WARNING

    def test_missing_content(self):
        issues = check_content_present({})
        assert len(issues) == 1


# --------------------------------------------------------------------------- #
class TestBuiltinBrokenLinks:
    def test_good_http_link(self):
        doc = {"content": "See [docs](https://example.com/page)"}
        assert check_no_broken_links(doc) == []

    def test_relative_link(self):
        doc = {"content": "See [docs](./page.md)"}
        assert check_no_broken_links(doc) == []

    def test_anchor_link(self):
        doc = {"content": "See [top](#top)"}
        assert check_no_broken_links(doc) == []

    def test_empty_link(self):
        doc = {"content": "Click [here]()"}
        issues = check_no_broken_links(doc)
        assert len(issues) == 1
        assert issues[0].severity == IssueSeverity.WARNING

    def test_suspicious_link(self):
        doc = {"content": "See [thing](javascript:alert(1))"}
        issues = check_no_broken_links(doc)
        assert len(issues) >= 1
        assert any(i.severity == IssueSeverity.INFO for i in issues)

    def test_line_num_reported(self):
        doc = {"content": "line1\nline2 [bad]()\nline3"}
        issues = check_no_broken_links(doc)
        assert issues[0].line_num == 2


# --------------------------------------------------------------------------- #
class TestBuiltinEmptyHeadings:
    def test_no_empty_headings(self):
        doc = {"content": "# Title\nbody"}
        assert check_no_empty_headings(doc) == []

    def test_one_empty_heading(self):
        doc = {"content": "intro\n##\nbody"}
        issues = check_no_empty_headings(doc)
        assert len(issues) == 1
        assert issues[0].line_num == 2

    def test_multiple_empty_headings(self):
        doc = {"content": "#\nabc\n###\n"}
        issues = check_no_empty_headings(doc)
        assert len(issues) == 2

    def test_heading_with_spaces_only(self):
        doc = {"content": "##   "}
        issues = check_no_empty_headings(doc)
        assert len(issues) == 1


# --------------------------------------------------------------------------- #
class TestBuiltinTrailingWhitespace:
    def test_no_trailing(self):
        doc = {"content": "clean line\nanother clean"}
        assert check_no_trailing_whitespace(doc) == []

    def test_trailing_space(self):
        doc = {"content": "has trailing  \nclean"}
        issues = check_no_trailing_whitespace(doc)
        assert len(issues) == 1
        assert issues[0].line_num == 1

    def test_trailing_tab(self):
        doc = {"content": "has tab\t\nclean"}
        issues = check_no_trailing_whitespace(doc)
        assert len(issues) == 1


# --------------------------------------------------------------------------- #
class TestBuiltinHasTags:
    def test_with_tags(self):
        assert check_has_tags({"tags": ["a"]}) == []

    def test_missing_tags(self):
        issues = check_has_tags({})
        assert len(issues) == 1
        assert issues[0].severity == IssueSeverity.INFO

    def test_empty_tags(self):
        issues = check_has_tags({"tags": []})
        assert len(issues) == 1


# --------------------------------------------------------------------------- #
class TestBuiltinMaxLineLength:
    def test_short_lines(self):
        doc = {"content": "short\nstill short"}
        assert check_max_line_length(doc) == []

    def test_long_line(self):
        doc = {"content": "x" * 121}
        issues = check_max_line_length(doc)
        assert len(issues) == 1
        assert issues[0].severity == IssueSeverity.INFO

    def test_exact_boundary(self):
        doc = {"content": "x" * 120}
        assert check_max_line_length(doc) == []

    def test_multiple_long_lines(self):
        doc = {"content": ("y" * 200) + "\nshort\n" + ("z" * 150)}
        issues = check_max_line_length(doc)
        assert len(issues) == 2


# --------------------------------------------------------------------------- #
class TestScoring:
    def test_error_penalty(self):
        hc = DocHealthCheck()
        # Keep only the title check so we get a single ERROR.
        for name in hc.available_checks():
            if name != "check_title_present":
                hc.unregister_check(name)
        report = hc.run({})
        assert report.score == 80.0

    def test_warning_penalty(self):
        hc = DocHealthCheck()
        for name in hc.available_checks():
            if name != "check_content_present":
                hc.unregister_check(name)
        report = hc.run({"title": "T"})
        assert report.score == 95.0

    def test_info_penalty(self):
        hc = DocHealthCheck()
        for name in hc.available_checks():
            if name != "check_has_tags":
                hc.unregister_check(name)
        report = hc.run({"title": "T", "content": "x" * 30})
        assert report.score == 99.0

    def test_score_min_zero(self):
        hc = DocHealthCheck()
        # Pile on errors via custom checks.
        for i in range(10):
            hc.register_check(
                f"err_{i}",
                lambda d, i=i: [
                    HealthIssue(f"err_{i}", IssueSeverity.ERROR, "boom")
                ],
            )
        report = hc.run({"title": "T", "content": "x" * 30, "tags": ["a"]})
        assert report.score == 0.0
        assert report.passed is False

    def test_passed_true_when_no_errors(self):
        hc = DocHealthCheck()
        report = hc.run(
            {"title": "T", "content": "x" * 30, "tags": ["a"]}
        )
        assert report.passed is True

    def test_passed_false_when_error(self):
        hc = DocHealthCheck()
        report = hc.run({"content": "x" * 30, "tags": ["a"]})
        assert report.passed is False


# --------------------------------------------------------------------------- #
class TestCustomCheck:
    def test_custom_returning_issue(self):
        hc = DocHealthCheck()

        def my_check(doc):
            if doc.get("forbidden"):
                return [
                    HealthIssue("my_check", IssueSeverity.ERROR, "forbidden present")
                ]
            return []

        hc.register_check("my_check", my_check)
        report = hc.run({"title": "T", "content": "x" * 30, "forbidden": True})
        assert any(i.check_name == "my_check" for i in report.issues)

    def test_custom_disabled_not_run(self):
        hc = DocHealthCheck()

        def my_check(doc):
            return [HealthIssue("my_check", IssueSeverity.ERROR, "x")]

        hc.register_check("my_check", my_check, enabled=False)
        report = hc.run({"title": "T", "content": "x" * 30, "tags": ["a"]})
        assert not any(i.check_name == "my_check" for i in report.issues)

    def test_custom_exception_caught(self):
        hc = DocHealthCheck()

        def broken(doc):
            raise RuntimeError("boom")

        hc.register_check("broken", broken)
        report = hc.run({"title": "T", "content": "x" * 30, "tags": ["a"]})
        broken_issues = [i for i in report.issues if i.check_name == "broken"]
        assert len(broken_issues) == 1
        assert broken_issues[0].severity == IssueSeverity.ERROR


# --------------------------------------------------------------------------- #
class TestEdgeCases:
    def test_empty_doc(self):
        hc = DocHealthCheck()
        report = hc.run({})
        # title ERROR + content WARNING + tags INFO at minimum
        assert report.error_count >= 1
        assert report.warning_count >= 1
        assert report.info_count >= 1

    def test_non_string_content(self):
        hc = DocHealthCheck()
        # Should not raise even with weird content type.
        report = hc.run({"title": "T", "content": 12345, "tags": ["a"]})
        assert isinstance(report, HealthReport)

    def test_run_after_clear_and_register(self):
        hc = DocHealthCheck()
        hc.clear()
        hc.register_check(
            "only",
            lambda d: [HealthIssue("only", IssueSeverity.WARNING, "warn")],
        )
        report = hc.run({})
        assert report.warning_count == 1
        assert report.score == 95.0

    def test_report_dataclass_fields(self):
        hc = DocHealthCheck()
        report = hc.run({"title": "T", "content": "x" * 30, "tags": ["a"]}, doc_id="d")
        assert report.doc_id == "d"
        assert isinstance(report.issues, list)
        assert isinstance(report.score, float)
        assert isinstance(report.passed, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
