"""E237 Document Field Validator module for docs-toolkit.

Declarative field validation rules for arbitrary document data:
types, ranges, patterns, dependencies. Pure stdlib only.

Usage::

    from docstoolkit.doc_field_validator import (
        DocFieldValidator, FieldSchema, ValidationRule,
        ValidationError, ValidationResult, FieldType, Severity,
    )

    v = DocFieldValidator()
    v.add_field("title", FieldType.STRING, required=True)
    v.add_rule("title", "min_length", 3)
    v.add_field("age", FieldType.INT)
    v.add_rule("age", "min", 0)
    v.add_rule("age", "max", 150)

    result = v.validate({"title": "Hi", "age": 25})
    assert result.valid is False  # title too short
"""
from docstoolkit.doc_field_validator.validator import (
    DocFieldValidator,
    FieldSchema,
    FieldType,
    Severity,
    ValidationError,
    ValidationResult,
    ValidationRule,
)

__all__ = [
    "DocFieldValidator",
    "FieldSchema",
    "FieldType",
    "Severity",
    "ValidationError",
    "ValidationResult",
    "ValidationRule",
]
