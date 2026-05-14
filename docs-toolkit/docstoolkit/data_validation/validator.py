"""Validator and schema types for the E71 Data Validation module."""
from dataclasses import dataclass, field
from typing import Any

from docstoolkit.data_validation.rules import (
    ValidationError,
    ValidationRule,
    ValidationSeverity,
)


@dataclass
class FieldSchema:
    """Describes the validation rules that apply to a single field."""
    field_name: str
    rules: list[ValidationRule] = field(default_factory=list)
    description: str = ""


@dataclass
class ValidationResult:
    """Accumulated result of one or more field validations."""
    errors: list[ValidationError] = field(default_factory=list)

    def is_valid(self) -> bool:
        """Return True only when there are no ERROR-severity entries."""
        return not any(e.severity == ValidationSeverity.ERROR for e in self.errors)

    def has_warnings(self) -> bool:
        """Return True when at least one WARNING-severity entry exists."""
        return any(e.severity == ValidationSeverity.WARNING for e in self.errors)

    def errors_for(self, field: str) -> list[ValidationError]:
        """Return all errors whose field matches *field*."""
        return [e for e in self.errors if e.field == field]

    def add(self, error: ValidationError) -> None:
        """Append *error* to the result."""
        self.errors.append(error)


class DataValidator:
    """Validate a data dict against a collection of FieldSchemas."""

    def __init__(self, schemas: list[FieldSchema] | None = None) -> None:
        self._schemas: list[FieldSchema] = list(schemas) if schemas else []

    def add_schema(self, schema: FieldSchema) -> None:
        """Register an additional FieldSchema."""
        self._schemas.append(schema)

    def validate(self, data: dict) -> ValidationResult:
        """Run all rules for every registered schema against *data*.

        Fields present in *data* but without a schema are not checked.
        """
        result = ValidationResult()
        for schema in self._schemas:
            value = data.get(schema.field_name)
            for rule in schema.rules:
                for error in rule.validate(schema.field_name, value):
                    result.add(error)
        return result

    def validate_field(self, field_name: str, value: Any) -> ValidationResult:
        """Validate a single field by name using its registered schema."""
        result = ValidationResult()
        for schema in self._schemas:
            if schema.field_name == field_name:
                for rule in schema.rules:
                    for error in rule.validate(field_name, value):
                        result.add(error)
        return result

    def is_valid(self, data: dict) -> bool:
        """Return True only when validate(data) produces no ERROR-severity errors."""
        return self.validate(data).is_valid()
