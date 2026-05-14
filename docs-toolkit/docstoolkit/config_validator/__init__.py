"""E104 Config Validator module for docs-toolkit.

Validate Python dicts against a simple schema definition. Pure stdlib only.

Supports:
  - Required / optional fields with defaults
  - Type checking (single type or tuple of types)
  - Numeric range constraints (min_value / max_value)
  - String / list length constraints (min_length / max_length)
  - Regex pattern matching via re.fullmatch
  - Allowed-values whitelist
  - Custom validator callables
  - Nested schema validation for dict-valued fields
  - Extra-key rejection when allow_extra=False (default)

Usage::

    from docstoolkit.config_validator import (
        ConfigValidator, SchemaDefinition, FieldSchema,
        ValidationResult, ValidationError,
    )

    schema = SchemaDefinition(fields=[
        FieldSchema("host", type=str),
        FieldSchema("port", type=int, min_value=1, max_value=65535),
        FieldSchema("debug", type=bool, required=False, default=False),
    ])

    validator = ConfigValidator()
    result = validator.validate({"host": "localhost", "port": 8080}, schema)
    assert result.valid

    filled = validator.coerce({"host": "localhost", "port": 8080}, schema)
    assert filled["debug"] is False
"""
from docstoolkit.config_validator.validator import (
    FieldSchema,
    SchemaDefinition,
    ValidationError,
    ValidationResult,
    ConfigValidator,
)

__all__ = [
    "FieldSchema",
    "SchemaDefinition",
    "ValidationError",
    "ValidationResult",
    "ConfigValidator",
]
