"""DocHealthCheck — composable document health check runner."""
from __future__ import annotations

import enum
import re
import threading
from dataclasses import dataclass, field
from typing import Callable, Optional


class IssueSeverity(enum.Enum):
    """Severity levels for health issues."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class HealthIssue:
    """Single issue reported by a health check."""

    check_name: str
    severity: IssueSeverity
    message: str
    line_num: Optional[int] = None
    field: Optional[str] = None


@dataclass
class HealthReport:
    """Aggregated health report for a single document."""

    doc_id: str
    issues: list = field(default_factory=list)
    score: float = 100.0
    passed: bool = True

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.INFO)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.WARNING)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.ERROR)

    @property
    def total_issues(self) -> int:
        return len(self.issues)


# Type alias for checker callables.
HealthChecker = Callable[[dict], list]


# ------------------------- Built-in checks -------------------------

_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
_EMPTY_HEADING_RE = re.compile(r"^#+\s*$")


def check_title_present(doc: dict) -> list:
    """ERROR if 'title' is missing or empty."""
    issues: list = []
    title = doc.get("title")
    if title is None or (isinstance(title, str) and not title.strip()):
        issues.append(
            HealthIssue(
                check_name="check_title_present",
                severity=IssueSeverity.ERROR,
                message="Document title is missing or empty",
                field="title",
            )
        )
    return issues


def check_content_present(doc: dict) -> list:
    """WARNING if 'content' is missing or very short (<10 chars)."""
    issues: list = []
    content = doc.get("content")
    if content is None or (isinstance(content, str) and len(content.strip()) < 10):
        issues.append(
            HealthIssue(
                check_name="check_content_present",
                severity=IssueSeverity.WARNING,
                message="Document content is missing or too short",
                field="content",
            )
        )
    return issues


def check_no_broken_links(doc: dict) -> list:
    """INFO/WARNING for `[text](url)` with bad URLs (loose check)."""
    issues: list = []
    content = doc.get("content", "")
    if not isinstance(content, str):
        return issues
    for line_idx, line in enumerate(content.splitlines(), start=1):
        for match in _LINK_RE.finditer(line):
            url = match.group(2).strip()
            if not url:
                issues.append(
                    HealthIssue(
                        check_name="check_no_broken_links",
                        severity=IssueSeverity.WARNING,
                        message="Empty link URL",
                        line_num=line_idx,
                        field="content",
                    )
                )
                continue
            # Loose validation: must look like http(s)/relative/anchor/mailto
            looks_ok = (
                url.startswith(("http://", "https://", "/", "#", "./", "../", "mailto:"))
                or re.match(r"^[\w\-./]+\.\w+", url) is not None
            )
            if not looks_ok:
                issues.append(
                    HealthIssue(
                        check_name="check_no_broken_links",
                        severity=IssueSeverity.INFO,
                        message=f"Suspicious link URL: {url!r}",
                        line_num=line_idx,
                        field="content",
                    )
                )
    return issues


def check_no_empty_headings(doc: dict) -> list:
    """WARNING if there are `^#+\\s*$` lines (empty headings)."""
    issues: list = []
    content = doc.get("content", "")
    if not isinstance(content, str):
        return issues
    for line_idx, line in enumerate(content.splitlines(), start=1):
        if _EMPTY_HEADING_RE.match(line):
            issues.append(
                HealthIssue(
                    check_name="check_no_empty_headings",
                    severity=IssueSeverity.WARNING,
                    message="Empty heading",
                    line_num=line_idx,
                    field="content",
                )
            )
    return issues


def check_no_trailing_whitespace(doc: dict) -> list:
    """INFO if lines have trailing whitespace."""
    issues: list = []
    content = doc.get("content", "")
    if not isinstance(content, str):
        return issues
    for line_idx, line in enumerate(content.splitlines(), start=1):
        if line and line != line.rstrip():
            issues.append(
                HealthIssue(
                    check_name="check_no_trailing_whitespace",
                    severity=IssueSeverity.INFO,
                    message="Line has trailing whitespace",
                    line_num=line_idx,
                    field="content",
                )
            )
    return issues


def check_has_tags(doc: dict) -> list:
    """INFO if 'tags' missing or empty."""
    issues: list = []
    tags = doc.get("tags")
    if tags is None or (hasattr(tags, "__len__") and len(tags) == 0):
        issues.append(
            HealthIssue(
                check_name="check_has_tags",
                severity=IssueSeverity.INFO,
                message="Document has no tags",
                field="tags",
            )
        )
    return issues


def check_max_line_length(doc: dict, max_len: int = 120) -> list:
    """INFO if any line > 120 chars."""
    issues: list = []
    content = doc.get("content", "")
    if not isinstance(content, str):
        return issues
    for line_idx, line in enumerate(content.splitlines(), start=1):
        if len(line) > max_len:
            issues.append(
                HealthIssue(
                    check_name="check_max_line_length",
                    severity=IssueSeverity.INFO,
                    message=f"Line exceeds {max_len} chars ({len(line)})",
                    line_num=line_idx,
                    field="content",
                )
            )
    return issues


_BUILTIN_CHECKS: list = [
    ("check_title_present", check_title_present),
    ("check_content_present", check_content_present),
    ("check_no_broken_links", check_no_broken_links),
    ("check_no_empty_headings", check_no_empty_headings),
    ("check_no_trailing_whitespace", check_no_trailing_whitespace),
    ("check_has_tags", check_has_tags),
    ("check_max_line_length", check_max_line_length),
]


# ------------------------- Runner -------------------------

@dataclass
class _CheckEntry:
    name: str
    func: Callable
    enabled: bool = True


class DocHealthCheck:
    """Composable health check runner.

    Built-in checks are auto-registered on construction. Custom checks
    can be added/removed/toggled at runtime. Thread-safe via internal lock.
    """

    SCORE_PENALTIES = {
        IssueSeverity.ERROR: 20,
        IssueSeverity.WARNING: 5,
        IssueSeverity.INFO: 1,
    }

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._checks: dict = {}
        for name, func in _BUILTIN_CHECKS:
            self._checks[name] = _CheckEntry(name=name, func=func, enabled=True)

    def register_check(
        self, name: str, check_func: Callable, enabled: bool = True
    ) -> None:
        """Register a new check (replaces existing with same name)."""
        with self._lock:
            self._checks[name] = _CheckEntry(name=name, func=check_func, enabled=enabled)

    def unregister_check(self, name: str) -> bool:
        """Remove a check. Returns True if removed, False if absent."""
        with self._lock:
            if name in self._checks:
                del self._checks[name]
                return True
            return False

    def enable_check(self, name: str) -> bool:
        """Enable a check. Returns True if found, False if absent."""
        with self._lock:
            entry = self._checks.get(name)
            if entry is None:
                return False
            entry.enabled = True
            return True

    def disable_check(self, name: str) -> bool:
        """Disable a check. Returns True if found, False if absent."""
        with self._lock:
            entry = self._checks.get(name)
            if entry is None:
                return False
            entry.enabled = False
            return True

    def available_checks(self, enabled_only: bool = False) -> list:
        """Return list of registered check names."""
        with self._lock:
            if enabled_only:
                return [n for n, e in self._checks.items() if e.enabled]
            return list(self._checks.keys())

    @property
    def check_count(self) -> int:
        """Number of registered checks (enabled or disabled)."""
        with self._lock:
            return len(self._checks)

    def clear(self) -> None:
        """Remove all registered checks."""
        with self._lock:
            self._checks.clear()

    def run(self, doc: dict, doc_id: str = "doc") -> HealthReport:
        """Run all enabled checks against the doc and produce a HealthReport."""
        with self._lock:
            entries = [e for e in self._checks.values() if e.enabled]

        issues: list = []
        for entry in entries:
            try:
                result = entry.func(doc)
            except Exception as exc:  # noqa: BLE001
                issues.append(
                    HealthIssue(
                        check_name=entry.name,
                        severity=IssueSeverity.ERROR,
                        message=f"Check raised exception: {exc}",
                    )
                )
                continue
            if result:
                issues.extend(result)

        score = 100.0
        for issue in issues:
            score -= self.SCORE_PENALTIES.get(issue.severity, 0)
        if score < 0:
            score = 0.0

        error_count = sum(1 for i in issues if i.severity == IssueSeverity.ERROR)
        passed = error_count == 0

        return HealthReport(
            doc_id=doc_id,
            issues=issues,
            score=score,
            passed=passed,
        )

    def run_batch(self, docs: list) -> list:
        """Run checks on each doc; uses doc.get('id', f'doc_{i}') as doc_id."""
        reports: list = []
        for i, doc in enumerate(docs):
            doc_id = str(doc.get("id", f"doc_{i}")) if isinstance(doc, dict) else f"doc_{i}"
            reports.append(self.run(doc, doc_id=doc_id))
        return reports
