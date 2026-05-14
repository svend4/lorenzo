"""Schema registry module: schema definitions, validation, and SQLite-backed registry."""
from docstoolkit.schema_registry.schema import (
    SchemaVersion,
    FieldDef,
    Schema,
    VALID_FIELD_TYPES,
)
from docstoolkit.schema_registry.validator import (
    SchemaValidationError,
    SchemaValidator,
)
from docstoolkit.schema_registry.registry import SchemaRegistry

__all__ = [
    "SchemaVersion",
    "FieldDef",
    "Schema",
    "VALID_FIELD_TYPES",
    "SchemaValidationError",
    "SchemaValidator",
    "SchemaRegistry",
]
