"""Document sanitizer module for docs-toolkit.

Public API
----------
- ``SanitizationRule``   — enum of rule types (STRIP_HTML, ESCAPE_HTML, ...)
- ``SanitizerConfig``    — rule selection + allowed protocols/tags
- ``SanitizationResult`` — original/sanitized text + ``removed_items``
- ``DocSanitizer``       — main sanitizer class
"""

from docstoolkit.doc_sanitizer.sanitizer import (
    DocSanitizer,
    SanitizationResult,
    SanitizationRule,
    SanitizerConfig,
)

__all__ = [
    "DocSanitizer",
    "SanitizationResult",
    "SanitizationRule",
    "SanitizerConfig",
]
