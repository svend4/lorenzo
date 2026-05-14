"""E104 Config Validator — validate Python dicts against a simple schema.

Pure stdlib. No external dependencies.

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
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Type


# ---------------------------------------------------------------------------
# Schema building blocks
# ---------------------------------------------------------------------------

@dataclass
class FieldSchema:
    """Declaration of a single field in a config schema."""

    name: str
    type: Type | tuple[Type, ...] | None = None  # None = any type accepted
    required: bool = True
    default: Any = None               # used when field is missing and required=False
    min_value: float | None = None    # for numeric fields
    max_value: float | None = None
    min_length: int | None = None     # for str/list fields
    max_length: int | None = None
    pattern: str | None = None        # regex applied via re.fullmatch
    allowed_values: list | None = None
    validator: Callable[[Any], bool] | None = None  # custom fn(value) -> bool
    validator_msg: str = "custom validation failed"
    nested: "SchemaDefinition | None" = None  # recursively validate dict values


@dataclass
class SchemaDefinition:
    """A complete schema: a list of field declarations plus extra-key policy."""

    fields: list[FieldSchema]
    allow_extra: bool = False  # when False, keys not in fields are errors


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class ValidationError:
    """A single validation failure."""

    field: str
    message: str


@dataclass
class ValidationResult:
    """Accumulated result of validating a dict against a SchemaDefinition."""

    errors: list[ValidationError] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        """True when there are no errors."""
        return len(self.errors) == 0

    def __str__(self) -> str:
        """Human-readable summary of all errors."""
        if self.valid:
            return "Validation passed."
        lines = [f"{len(self.errors)} error(s):"]
        for err in self.errors:
            lines.append(f"  [{err.field}] {err.message}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

class ConfigValidator:
    """Validates Python dicts against a SchemaDefinition."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(self, data: dict, schema: SchemaDefinition) -> ValidationResult:
        """Validate *data* against *schema*. Collects all errors without short-circuiting."""
        result = ValidationResult()
        defined_names = {fs.name for fs in schema.fields}

        # 1. Check for extra keys when allow_extra is False.
        if not schema.allow_extra:
            for key in data:
                if key not in defined_names:
                    result.errors.append(
                        ValidationError(
                            field=str(key),
                            message=f"unexpected field '{key}' is not allowed by schema",
                        )
                    )

        # 2. Validate every declared field.
        for fs in schema.fields:
            value = data.get(fs.name, _MISSING)
            self._validate_field(fs, value, result, prefix="")

        return result

    def coerce(self, data: dict, schema: SchemaDefinition) -> dict:
        """Return a new dict with defaults filled in for missing optional fields.

        The original *data* dict is never modified.
        """
        out = dict(data)
        for fs in schema.fields:
            if fs.name not in out and not fs.required:
                out[fs.name] = fs.default
        return out

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_field(
        self,
        fs: FieldSchema,
        value: Any,
        result: ValidationResult,
        prefix: str,
    ) -> None:
        """Run all applicable checks for one field, appending to *result*."""
        full_name = f"{prefix}{fs.name}" if prefix else fs.name

        # Rule 1 — required field missing.
        if value is _MISSING:
            if fs.required:
                result.errors.append(
                    ValidationError(
                        field=full_name,
                        message=f"required field '{full_name}' is missing",
                    )
                )
            # Whether required or not, nothing further to validate when absent.
            return

        # Rule 3 — type check.
        if fs.type is not None and not isinstance(value, fs.type):
            expected = (
                " | ".join(t.__name__ for t in fs.type)
                if isinstance(fs.type, tuple)
                else fs.type.__name__
            )
            result.errors.append(
                ValidationError(
                    field=full_name,
                    message=(
                        f"'{full_name}' must be of type {expected}, "
                        f"got {type(value).__name__}"
                    ),
                )
            )
            # Skip further checks that depend on value semantics when the type
            # is wrong — they would produce confusing secondary errors.
            return

        # Rule 4 — min_value / max_value.
        if fs.min_value is not None and value < fs.min_value:
            result.errors.append(
                ValidationError(
                    field=full_name,
                    message=(
                        f"'{full_name}' must be >= {fs.min_value}, got {value}"
                    ),
                )
            )
        if fs.max_value is not None and value > fs.max_value:
            result.errors.append(
                ValidationError(
                    field=full_name,
                    message=(
                        f"'{full_name}' must be <= {fs.max_value}, got {value}"
                    ),
                )
            )

        # Rule 5 — min_length / max_length.
        if fs.min_length is not None or fs.max_length is not None:
            try:
                length = len(value)
            except TypeError:
                pass  # value has no len(); skip silently
            else:
                if fs.min_length is not None and length < fs.min_length:
                    result.errors.append(
                        ValidationError(
                            field=full_name,
                            message=(
                                f"'{full_name}' must have length >= {fs.min_length}, "
                                f"got {length}"
                            ),
                        )
                    )
                if fs.max_length is not None and length > fs.max_length:
                    result.errors.append(
                        ValidationError(
                            field=full_name,
                            message=(
                                f"'{full_name}' must have length <= {fs.max_length}, "
                                f"got {length}"
                            ),
                        )
                    )

        # Rule 6 — regex pattern (strings only).
        if fs.pattern is not None and isinstance(value, str):
            if re.fullmatch(fs.pattern, value) is None:
                result.errors.append(
                    ValidationError(
                        field=full_name,
                        message=(
                            f"'{full_name}' does not match pattern '{fs.pattern}'"
                        ),
                    )
                )

        # Rule 7 — allowed_values whitelist.
        if fs.allowed_values is not None and value not in fs.allowed_values:
            result.errors.append(
                ValidationError(
                    field=full_name,
                    message=(
                        f"'{full_name}' value {value!r} not in allowed values "
                        f"{fs.allowed_values!r}"
                    ),
                )
            )

        # Rule 8 — custom validator.
        if fs.validator is not None:
            try:
                ok = fs.validator(value)
            except Exception as exc:
                ok = False
                result.errors.append(
                    ValidationError(
                        field=full_name,
                        message=(
                            f"'{full_name}' custom validator raised an exception: {exc}"
                        ),
                    )
                )
            else:
                if not ok:
                    result.errors.append(
                        ValidationError(
                            field=full_name,
                            message=f"'{full_name}': {fs.validator_msg}",
                        )
                    )

        # Rule 9 — nested schema for dict values.
        if fs.nested is not None and isinstance(value, dict):
            nested_result = self.validate(value, fs.nested)
            for err in nested_result.errors:
                result.errors.append(
                    ValidationError(
                        field=f"{full_name}.{err.field}",
                        message=err.message,
                    )
                )


# ---------------------------------------------------------------------------
# Sentinel for missing values
# ---------------------------------------------------------------------------

class _MissingType:
    """Singleton sentinel that indicates a key was absent from the data dict."""

    _instance: "_MissingType | None" = None

    def __new__(cls) -> "_MissingType":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:  # pragma: no cover
        return "<MISSING>"


_MISSING = _MissingType()
