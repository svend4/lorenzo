"""E354 DocValidationEngine — pluggable validation rule engine for documents.

Public API
----------
:class:`ValidationRule`     — a single validation rule
:class:`ValidationIssue`    — a single found issue
:class:`ValidationResult`   — result of validating a document
:class:`ValidationStats`    — aggregate statistics
:class:`DocValidationEngine` — main interface for validation
"""

from .engine import ValidationRule, ValidationIssue, ValidationResult, ValidationStats, DocValidationEngine

__all__ = ["ValidationRule", "ValidationIssue", "ValidationResult", "ValidationStats", "DocValidationEngine"]
