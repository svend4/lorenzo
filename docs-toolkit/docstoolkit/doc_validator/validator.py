"""doc_validator — validates markdown documents against configurable rules (stdlib only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# ---------------------------------------------------------------------------
# Rule ID constants
# ---------------------------------------------------------------------------

NO_H1 = "no_h1"
MULTIPLE_H1 = "multiple_h1"
EMPTY_SECTION = "empty_section"
MISSING_FRONTMATTER = "missing_frontmatter"
LONG_LINE = "long_line"
BROKEN_HEADING_HIERARCHY = "broken_heading_hierarchy"
DUPLICATE_HEADING = "duplicate_heading"
NO_CONTENT = "no_content"


# ---------------------------------------------------------------------------
# Severity enum
# ---------------------------------------------------------------------------

class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)')
_FRONTMATTER_START = re.compile(r'^---\s*$')


def _parse_headings(text: str) -> list[tuple[int, int, str]]:
    """Return list of (level, line_num, heading_text) for all headings.

    Line numbers are 1-based.
    Headings inside fenced code blocks are skipped.
    """
    headings: list[tuple[int, int, str]] = []
    in_fence = False
    fence_marker: str = ""
    for line_num, line in enumerate(text.splitlines(), start=1):
        stripped = line.rstrip()
        # Detect fenced code blocks (``` or ~~~)
        fence_match = re.match(r'^(`{3,}|~{3,})', stripped)
        if fence_match:
            marker = fence_match.group(1)[0]  # ` or ~
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif stripped.startswith(fence_marker * 3):
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue
        m = _HEADING_RE.match(stripped)
        if m:
            level = len(m.group(1))
            text_part = m.group(2).strip()
            headings.append((level, line_num, text_part))
    return headings


# ---------------------------------------------------------------------------
# ValidationIssue dataclass
# ---------------------------------------------------------------------------

@dataclass
class ValidationIssue:
    """A single validation problem found in a document."""

    rule_id: str
    severity: Severity
    message: str
    line_num: Optional[int] = None
    context: Optional[str] = None


# ---------------------------------------------------------------------------
# ValidationResult dataclass
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Aggregated result of validating one document."""

    issues: list[ValidationIssue] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def is_valid(self) -> bool:
        """True when there are no ERROR-severity issues."""
        return not any(i.severity == Severity.ERROR for i in self.issues)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == Severity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == Severity.WARNING]

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    def by_rule(self, rule_id: str) -> list[ValidationIssue]:
        """Return all issues matching *rule_id*."""
        return [i for i in self.issues if i.rule_id == rule_id]


# ---------------------------------------------------------------------------
# ValidationConfig dataclass
# ---------------------------------------------------------------------------

@dataclass
class ValidationConfig:
    """Configuration controlling which rules are active and their thresholds."""

    require_h1: bool = True
    require_frontmatter: bool = False
    max_line_length: int = 0          # 0 = no limit
    check_heading_hierarchy: bool = True
    check_duplicate_headings: bool = True
    check_empty_sections: bool = True
    disabled_rules: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# DocValidator class
# ---------------------------------------------------------------------------

class DocValidator:
    """Validates a markdown document against a set of configurable rules."""

    def __init__(self, config: Optional[ValidationConfig] = None) -> None:
        self.config = config or ValidationConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(self, text: str) -> ValidationResult:
        """Run all enabled checks on *text* and return a :class:`ValidationResult`."""
        cfg = self.config
        disabled = set(cfg.disabled_rules)
        issues: list[ValidationIssue] = []

        if cfg.require_h1:
            issues.extend(
                i for i in self.check_h1(text) if i.rule_id not in disabled
            )

        if cfg.check_heading_hierarchy:
            issues.extend(
                i for i in self.check_heading_hierarchy(text) if i.rule_id not in disabled
            )

        if cfg.check_duplicate_headings:
            issues.extend(
                i for i in self.check_duplicate_headings(text) if i.rule_id not in disabled
            )

        if cfg.check_empty_sections:
            issues.extend(
                i for i in self.check_empty_sections(text) if i.rule_id not in disabled
            )

        if cfg.require_frontmatter:
            issues.extend(
                i for i in self.check_frontmatter(text) if i.rule_id not in disabled
            )

        if cfg.max_line_length > 0:
            issues.extend(
                i for i in self.check_line_length(text, cfg.max_line_length)
                if i.rule_id not in disabled
            )

        return ValidationResult(issues=issues)

    def validate_batch(self, texts: list[str]) -> list[ValidationResult]:
        """Validate a list of documents and return one result per document."""
        return [self.validate(t) for t in texts]

    # ------------------------------------------------------------------
    # Individual check methods
    # ------------------------------------------------------------------

    def check_h1(self, text: str) -> list[ValidationIssue]:
        """Check for presence of exactly one H1.

        Rules triggered:
          - ``no_h1``      (ERROR)  — no H1 found
          - ``multiple_h1`` (WARNING) — more than one H1 found
        """
        issues: list[ValidationIssue] = []
        headings = _parse_headings(text)
        h1s = [(lnum, htxt) for lvl, lnum, htxt in headings if lvl == 1]

        if len(h1s) == 0:
            issues.append(ValidationIssue(
                rule_id=NO_H1,
                severity=Severity.ERROR,
                message="Document has no H1 heading.",
            ))
        elif len(h1s) > 1:
            for lnum, htxt in h1s[1:]:
                issues.append(ValidationIssue(
                    rule_id=MULTIPLE_H1,
                    severity=Severity.WARNING,
                    message=f"Multiple H1 headings found (duplicate at line {lnum}).",
                    line_num=lnum,
                    context=f"# {htxt}",
                ))
        return issues

    def check_heading_hierarchy(self, text: str) -> list[ValidationIssue]:
        """Check for skipped heading levels (e.g. H1 → H3 without H2).

        Rule triggered: ``broken_heading_hierarchy`` (WARNING).
        Only the first violation is reported.
        """
        issues: list[ValidationIssue] = []
        headings = _parse_headings(text)
        if not headings:
            return issues

        prev_level = headings[0][0]
        for lvl, lnum, htxt in headings[1:]:
            if lvl > prev_level + 1:
                issues.append(ValidationIssue(
                    rule_id=BROKEN_HEADING_HIERARCHY,
                    severity=Severity.WARNING,
                    message=(
                        f"Heading level jumps from H{prev_level} to H{lvl} "
                        f"at line {lnum} — level H{prev_level + 1} is missing."
                    ),
                    line_num=lnum,
                    context=f"{'#' * lvl} {htxt}",
                ))
                break  # only first violation
            prev_level = lvl
        return issues

    def check_duplicate_headings(self, text: str) -> list[ValidationIssue]:
        """Check for duplicate headings at the same level.

        Rule triggered: ``duplicate_heading`` (WARNING).
        """
        issues: list[ValidationIssue] = []
        headings = _parse_headings(text)
        seen: dict[tuple[int, str], int] = {}  # (level, lower_text) -> first line_num

        for lvl, lnum, htxt in headings:
            key = (lvl, htxt.lower())
            if key in seen:
                issues.append(ValidationIssue(
                    rule_id=DUPLICATE_HEADING,
                    severity=Severity.WARNING,
                    message=(
                        f"Duplicate H{lvl} heading \"{htxt}\" "
                        f"(first at line {seen[key]}, repeated at line {lnum})."
                    ),
                    line_num=lnum,
                    context=f"{'#' * lvl} {htxt}",
                ))
            else:
                seen[key] = lnum
        return issues

    def check_empty_sections(self, text: str) -> list[ValidationIssue]:
        """Check for sections with no body content (heading immediately followed
        by another heading or end of document).

        Rule triggered: ``empty_section`` (WARNING).
        """
        issues: list[ValidationIssue] = []
        lines = text.splitlines()
        n = len(lines)

        in_fence = False
        fence_marker = ""

        # Collect non-fence line indices that are headings
        heading_positions: list[int] = []  # 0-based indices
        for idx, line in enumerate(lines):
            stripped = line.rstrip()
            fence_match = re.match(r'^(`{3,}|~{3,})', stripped)
            if fence_match:
                marker = fence_match.group(1)[0]
                if not in_fence:
                    in_fence = True
                    fence_marker = marker
                elif stripped.startswith(fence_marker * 3):
                    in_fence = False
                    fence_marker = ""
                continue
            if in_fence:
                continue
            if _HEADING_RE.match(stripped):
                heading_positions.append(idx)

        for i, idx in enumerate(heading_positions):
            # The next heading starts at heading_positions[i+1], or end-of-doc
            next_heading_idx = heading_positions[i + 1] if i + 1 < len(heading_positions) else n

            # Look for any non-blank, non-heading lines between this heading and next
            has_content = False
            for j in range(idx + 1, next_heading_idx):
                if lines[j].strip():
                    has_content = True
                    break

            if not has_content:
                m = _HEADING_RE.match(lines[idx].rstrip())
                lvl = len(m.group(1)) if m else 0
                htxt = m.group(2).strip() if m else ""
                issues.append(ValidationIssue(
                    rule_id=EMPTY_SECTION,
                    severity=Severity.WARNING,
                    message=f"Section \"{htxt}\" (H{lvl}) at line {idx + 1} has no content.",
                    line_num=idx + 1,
                    context=lines[idx].rstrip(),
                ))
        return issues

    def check_frontmatter(self, text: str) -> list[ValidationIssue]:
        """Check that the document starts with a YAML frontmatter block (``---``).

        Rule triggered: ``missing_frontmatter`` (WARNING) when frontmatter is absent.
        """
        issues: list[ValidationIssue] = []
        first_line = text.splitlines()[0].rstrip() if text.strip() else ""
        if not _FRONTMATTER_START.match(first_line):
            issues.append(ValidationIssue(
                rule_id=MISSING_FRONTMATTER,
                severity=Severity.WARNING,
                message="Document does not start with a YAML frontmatter block (---).",
                line_num=1,
                context=first_line or None,
            ))
        return issues

    def check_line_length(self, text: str, max_len: int) -> list[ValidationIssue]:
        """Check for lines exceeding *max_len* characters.

        Rule triggered: ``long_line`` (INFO) per offending line.
        Does nothing when *max_len* <= 0.
        """
        issues: list[ValidationIssue] = []
        if max_len <= 0:
            return issues
        for line_num, line in enumerate(text.splitlines(), start=1):
            if len(line) > max_len:
                issues.append(ValidationIssue(
                    rule_id=LONG_LINE,
                    severity=Severity.INFO,
                    message=f"Line {line_num} exceeds max length ({len(line)} > {max_len}).",
                    line_num=line_num,
                    context=line[:80] + ("…" if len(line) > 80 else ""),
                ))
        return issues
