"""Schema validation: SchemaValidationError and SchemaValidator."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from docstoolkit.schema_registry.schema import Schema, FieldDef

_TYPE_MAP: dict = {
    "string": str,
    "integer": int,
    "float": (float, int),
    "boolean": bool,
    "array": list,
    "object": dict,
}


@dataclass
class SchemaValidationError:
    field: str
    message: str
    value: Any = None


class SchemaValidator:
    """Validates a data dict against a Schema."""

    def validate(self, data: dict, schema: Schema) -> list:
        errors: list = []

        for field_def in schema.fields:
            name = field_def.name
            present = name in data

            # Check required non-nullable fields are present
            if not present:
                if field_def.required and not field_def.nullable:
                    errors.append(
                        SchemaValidationError(
                            field=name,
                            message=f"Required field '{name}' is missing.",
                            value=None,
                        )
                    )
                # If not required or nullable, absence is fine — skip further checks
                continue

            value = data[name]

            # Handle None value
            if value is None:
                if not field_def.nullable:
                    errors.append(
                        SchemaValidationError(
                            field=name,
                            message=f"Field '{name}' is not nullable but got None.",
                            value=value,
                        )
                    )
                # Whether nullable or not, if None we skip type check
                continue

            # Type check
            expected = _TYPE_MAP.get(field_def.field_type)
            if expected is not None:
                # Special case: boolean must be checked before int because bool is subclass of int
                if field_def.field_type == "integer":
                    if not isinstance(value, int) or isinstance(value, bool):
                        errors.append(
                            SchemaValidationError(
                                field=name,
                                message=(
                                    f"Field '{name}' expects type 'integer' "
                                    f"but got {type(value).__name__!r}."
                                ),
                                value=value,
                            )
                        )
                elif field_def.field_type == "float":
                    if not isinstance(value, (float, int)) or isinstance(value, bool):
                        errors.append(
                            SchemaValidationError(
                                field=name,
                                message=(
                                    f"Field '{name}' expects type 'float' "
                                    f"but got {type(value).__name__!r}."
                                ),
                                value=value,
                            )
                        )
                elif field_def.field_type == "boolean":
                    if not isinstance(value, bool):
                        errors.append(
                            SchemaValidationError(
                                field=name,
                                message=(
                                    f"Field '{name}' expects type 'boolean' "
                                    f"but got {type(value).__name__!r}."
                                ),
                                value=value,
                            )
                        )
                elif field_def.field_type == "string":
                    if not isinstance(value, str):
                        errors.append(
                            SchemaValidationError(
                                field=name,
                                message=(
                                    f"Field '{name}' expects type 'string' "
                                    f"but got {type(value).__name__!r}."
                                ),
                                value=value,
                            )
                        )
                elif field_def.field_type == "array":
                    if not isinstance(value, list):
                        errors.append(
                            SchemaValidationError(
                                field=name,
                                message=(
                                    f"Field '{name}' expects type 'array' "
                                    f"but got {type(value).__name__!r}."
                                ),
                                value=value,
                            )
                        )
                elif field_def.field_type == "object":
                    if not isinstance(value, dict):
                        errors.append(
                            SchemaValidationError(
                                field=name,
                                message=(
                                    f"Field '{name}' expects type 'object' "
                                    f"but got {type(value).__name__!r}."
                                ),
                                value=value,
                            )
                        )

        return errors
