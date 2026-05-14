"""Validation for structured output data against schemas."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from docstoolkit.structured_output.schema import FieldType, OutputSchema


@dataclass
class ValidationError:
    """A validation error for a specific field."""

    field: str
    message: str
    value: Any = None


class OutputValidator:
    """Validate extracted data against an OutputSchema."""

    # Boolean truthy string values
    _BOOL_TRUE = {"true", "yes", "1", "on"}
    _BOOL_FALSE = {"false", "no", "0", "off"}

    # DATE format: YYYY-MM-DD
    _DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def validate(self, data: dict, schema: OutputSchema) -> list[ValidationError]:
        """Validate data dict against schema.

        Checks:
        - Required fields are present
        - Values can be coerced to their declared types
        Returns a list of ValidationError instances (empty if valid).
        """
        errors: list[ValidationError] = []

        # Build lookup for quick access
        field_map = {f.name: f for f in schema.fields}

        # Check required fields
        for field_schema in schema.required_fields():
            if field_schema.name not in data:
                errors.append(
                    ValidationError(
                        field=field_schema.name,
                        message=f"Required field '{field_schema.name}' is missing",
                    )
                )

        # Validate types for fields that are present
        for field_name, value in data.items():
            if field_name not in field_map:
                # Unknown field — not an error, just skip
                continue
            field_schema = field_map[field_name]
            if value is None:
                if field_schema.required:
                    errors.append(
                        ValidationError(
                            field=field_name,
                            message=f"Required field '{field_name}' is None",
                            value=value,
                        )
                    )
                continue
            try:
                self.coerce(value, field_schema.field_type)
            except (ValueError, TypeError) as exc:
                errors.append(
                    ValidationError(
                        field=field_name,
                        message=str(exc),
                        value=value,
                    )
                )

        return errors

    def coerce(self, value: Any, field_type: FieldType) -> Any:
        """Coerce value to the given FieldType.

        Returns the coerced value.
        Raises ValueError if coercion is not possible.
        """
        if field_type == FieldType.STRING:
            return str(value)

        elif field_type == FieldType.INTEGER:
            if isinstance(value, bool):
                # bool is a subclass of int; treat it as an error for INTEGER
                raise ValueError(
                    f"Cannot coerce boolean {value!r} to INTEGER"
                )
            if isinstance(value, int):
                return value
            if isinstance(value, float):
                if value == int(value):
                    return int(value)
                raise ValueError(
                    f"Cannot coerce float {value!r} to INTEGER without loss"
                )
            if isinstance(value, str):
                stripped = value.strip()
                try:
                    return int(stripped)
                except ValueError:
                    pass
                # Try float then cast
                try:
                    f = float(stripped)
                    if f == int(f):
                        return int(f)
                except ValueError:
                    pass
                raise ValueError(f"Cannot coerce string {value!r} to INTEGER")
            raise ValueError(f"Cannot coerce {type(value).__name__} {value!r} to INTEGER")

        elif field_type == FieldType.FLOAT:
            if isinstance(value, bool):
                raise ValueError(
                    f"Cannot coerce boolean {value!r} to FLOAT"
                )
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                try:
                    return float(value.strip())
                except ValueError:
                    raise ValueError(f"Cannot coerce string {value!r} to FLOAT")
            raise ValueError(f"Cannot coerce {type(value).__name__} {value!r} to FLOAT")

        elif field_type == FieldType.BOOLEAN:
            if isinstance(value, bool):
                return value
            if isinstance(value, int):
                if value == 1:
                    return True
                if value == 0:
                    return False
                raise ValueError(f"Cannot coerce integer {value!r} to BOOLEAN")
            if isinstance(value, str):
                lower = value.strip().lower()
                if lower in self._BOOL_TRUE:
                    return True
                if lower in self._BOOL_FALSE:
                    return False
                raise ValueError(
                    f"Cannot coerce string {value!r} to BOOLEAN; "
                    f"expected one of: true/false/yes/no/1/0/on/off"
                )
            raise ValueError(f"Cannot coerce {type(value).__name__} {value!r} to BOOLEAN")

        elif field_type == FieldType.LIST:
            if isinstance(value, list):
                return value
            if isinstance(value, str):
                stripped = value.strip()
                try:
                    result = json.loads(stripped)
                    if isinstance(result, list):
                        return result
                    raise ValueError(
                        f"JSON parsed but result is not a list: {type(result).__name__}"
                    )
                except (json.JSONDecodeError, ValueError) as exc:
                    raise ValueError(
                        f"Cannot coerce string {value!r} to LIST: {exc}"
                    )
            raise ValueError(f"Cannot coerce {type(value).__name__} {value!r} to LIST")

        elif field_type == FieldType.DICT:
            if isinstance(value, dict):
                return value
            if isinstance(value, str):
                stripped = value.strip()
                try:
                    result = json.loads(stripped)
                    if isinstance(result, dict):
                        return result
                    raise ValueError(
                        f"JSON parsed but result is not a dict: {type(result).__name__}"
                    )
                except (json.JSONDecodeError, ValueError) as exc:
                    raise ValueError(
                        f"Cannot coerce string {value!r} to DICT: {exc}"
                    )
            raise ValueError(f"Cannot coerce {type(value).__name__} {value!r} to DICT")

        elif field_type == FieldType.DATE:
            s = str(value).strip() if not isinstance(value, str) else value.strip()
            if self._DATE_PATTERN.match(s):
                # Basic range check
                parts = s.split("-")
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                if not (1 <= month <= 12):
                    raise ValueError(f"Invalid month in date {value!r}")
                if not (1 <= day <= 31):
                    raise ValueError(f"Invalid day in date {value!r}")
                return s
            raise ValueError(
                f"Cannot coerce {value!r} to DATE; expected format YYYY-MM-DD"
            )

        else:
            raise ValueError(f"Unknown FieldType: {field_type}")
