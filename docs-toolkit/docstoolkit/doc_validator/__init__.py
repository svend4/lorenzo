"""doc_validator — validates markdown documents against configurable rules."""
from docstoolkit.doc_validator.validator import (
    Severity,
    ValidationIssue,
    ValidationResult,
    ValidationConfig,
    DocValidator,
    # Rule ID constants
    NO_H1,
    MULTIPLE_H1,
    EMPTY_SECTION,
    MISSING_FRONTMATTER,
    LONG_LINE,
    BROKEN_HEADING_HIERARCHY,
    DUPLICATE_HEADING,
    NO_CONTENT,
)

__all__ = [
    "Severity",
    "ValidationIssue",
    "ValidationResult",
    "ValidationConfig",
    "DocValidator",
    "NO_H1",
    "MULTIPLE_H1",
    "EMPTY_SECTION",
    "MISSING_FRONTMATTER",
    "LONG_LINE",
    "BROKEN_HEADING_HIERARCHY",
    "DUPLICATE_HEADING",
    "NO_CONTENT",
]
