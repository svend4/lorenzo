"""E71 Data Validation module for docs-toolkit.

Provides stdlib-only field validation and string sanitization:

  - ValidationSeverity / ValidationError / ValidationRule (ABC)
  - Built-in rules: RequiredRule, TypeRule, RangeRule, LengthRule,
    RegexRule, ChoiceRule
  - FieldSchema / ValidationResult / DataValidator
  - SanitizeRule / DataSanitizer
  - Built-in sanitizer factories: strip_whitespace, lowercase, truncate,
    remove_html_tags

Usage::

    from docstoolkit.data_validation import (
        DataValidator, FieldSchema,
        RequiredRule, TypeRule, RangeRule,
    )

    validator = DataValidator([
        FieldSchema("name", [RequiredRule(), TypeRule(str)]),
        FieldSchema("age",  [RequiredRule(), TypeRule(int), RangeRule(0, 120)]),
    ])

    result = validator.validate({"name": "Alice", "age": 30})
    assert result.is_valid()
"""
from docstoolkit.data_validation.rules import (
    ValidationSeverity,
    ValidationError,
    ValidationRule,
    RequiredRule,
    TypeRule,
    RangeRule,
    LengthRule,
    RegexRule,
    ChoiceRule,
)
from docstoolkit.data_validation.validator import (
    FieldSchema,
    ValidationResult,
    DataValidator,
)
from docstoolkit.data_validation.sanitizer import (
    SanitizeRule,
    DataSanitizer,
    strip_whitespace,
    lowercase,
    truncate,
    remove_html_tags,
)

__all__ = [
    # rules
    "ValidationSeverity",
    "ValidationError",
    "ValidationRule",
    "RequiredRule",
    "TypeRule",
    "RangeRule",
    "LengthRule",
    "RegexRule",
    "ChoiceRule",
    # validator
    "FieldSchema",
    "ValidationResult",
    "DataValidator",
    # sanitizer
    "SanitizeRule",
    "DataSanitizer",
    "strip_whitespace",
    "lowercase",
    "truncate",
    "remove_html_tags",
]
