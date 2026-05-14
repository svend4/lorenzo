"""Document Health Check module (E212).

Composable health check runner for documents with pluggable checkers.
Built-in checks cover title, content, links, headings, whitespace, tags,
and line length. Custom checks can be registered, enabled, or disabled.

Usage:
    from docstoolkit.doc_health_check import DocHealthCheck

    hc = DocHealthCheck()
    report = hc.run({"title": "Doc", "content": "Hello world"}, doc_id="d1")
    print(report.score, report.passed)
    for issue in report.issues:
        print(issue.severity, issue.message)
"""
from docstoolkit.doc_health_check.check import (
    DocHealthCheck,
    HealthChecker,
    HealthIssue,
    HealthReport,
    IssueSeverity,
    check_content_present,
    check_has_tags,
    check_max_line_length,
    check_no_broken_links,
    check_no_empty_headings,
    check_no_trailing_whitespace,
    check_title_present,
)

__all__ = [
    "DocHealthCheck",
    "HealthChecker",
    "HealthIssue",
    "HealthReport",
    "IssueSeverity",
    "check_content_present",
    "check_has_tags",
    "check_max_line_length",
    "check_no_broken_links",
    "check_no_empty_headings",
    "check_no_trailing_whitespace",
    "check_title_present",
]
