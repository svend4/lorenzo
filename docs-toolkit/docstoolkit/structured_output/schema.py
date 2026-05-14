"""Schema definitions for structured output parsing."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FieldType(Enum):
    """Supported field types for structured output schemas."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    DATE = "date"


@dataclass
class FieldSchema:
    """Schema definition for a single field."""

    name: str
    field_type: FieldType
    required: bool = True
    default: Any = None
    description: str = ""


@dataclass
class OutputSchema:
    """Schema definition for structured output."""

    name: str
    fields: list[FieldSchema] = field(default_factory=list)

    def required_fields(self) -> list[FieldSchema]:
        """Return list of required fields."""
        return [f for f in self.fields if f.required]

    def optional_fields(self) -> list[FieldSchema]:
        """Return list of optional fields."""
        return [f for f in self.fields if not f.required]

    def field_names(self) -> list[str]:
        """Return list of all field names."""
        return [f.name for f in self.fields]
