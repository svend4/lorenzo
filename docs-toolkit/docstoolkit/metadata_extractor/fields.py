"""Field type definitions for the metadata extractor."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FieldType(Enum):
    """Supported field types for extracted metadata."""

    TEXT = "text"
    DATE = "date"
    NUMBER = "number"
    EMAIL = "email"
    URL = "url"
    PHONE = "phone"
    BOOLEAN = "boolean"


@dataclass
class ExtractedField:
    """A single field value extracted from text."""

    name: str
    value: object
    field_type: FieldType
    confidence: float = 1.0
    source_span: tuple[int, int] = (0, 0)


@dataclass
class ExtractionSchema:
    """Describes which fields to extract from a document."""

    fields: list[str] = field(default_factory=list)
