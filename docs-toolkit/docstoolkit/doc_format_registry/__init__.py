"""E314 DocFormatRegistry — document format/MIME type registry with validators.

Public API
----------
:class:`FormatSpec`       — a registered document format
:class:`ValidationResult` — result of validating a document against a format
:class:`FormatStats`      — aggregate statistics
:class:`DocFormatRegistry` — main interface for format management
"""

from .registry import FormatSpec, ValidationResult, FormatStats, DocFormatRegistry

__all__ = ["FormatSpec", "ValidationResult", "FormatStats", "DocFormatRegistry"]
