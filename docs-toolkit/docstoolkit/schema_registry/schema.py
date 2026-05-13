"""Schema definitions: SchemaVersion, FieldDef, Schema."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

VALID_FIELD_TYPES = {"string", "integer", "float", "boolean", "array", "object"}


@dataclass
class SchemaVersion:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, s: str) -> "SchemaVersion":
        parts = s.strip().split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version string: {s!r}. Expected 'major.minor.patch'.")
        try:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            raise ValueError(f"Invalid version string: {s!r}. Parts must be integers.")
        return cls(major=major, minor=minor, patch=patch)

    def is_compatible(self, other: "SchemaVersion") -> bool:
        """Two versions are compatible if they share the same major version."""
        return self.major == other.major

    def bump_patch(self) -> "SchemaVersion":
        return SchemaVersion(self.major, self.minor, self.patch + 1)

    def bump_minor(self) -> "SchemaVersion":
        return SchemaVersion(self.major, self.minor + 1, 0)

    def bump_major(self) -> "SchemaVersion":
        return SchemaVersion(self.major + 1, 0, 0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SchemaVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other: "SchemaVersion") -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __le__(self, other: "SchemaVersion") -> bool:
        return self == other or self < other

    def __gt__(self, other: "SchemaVersion") -> bool:
        return not self <= other

    def __ge__(self, other: "SchemaVersion") -> bool:
        return not self < other

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))


@dataclass
class FieldDef:
    name: str
    field_type: str
    required: bool = True
    nullable: bool = False
    description: str = ""

    def __post_init__(self) -> None:
        if self.field_type not in VALID_FIELD_TYPES:
            raise ValueError(
                f"Invalid field_type {self.field_type!r}. "
                f"Must be one of: {sorted(VALID_FIELD_TYPES)}"
            )


def _default_schema_id() -> str:
    return uuid.uuid4().hex[:8]


def _default_created_ts() -> float:
    return time.time()


@dataclass
class Schema:
    name: str
    version: SchemaVersion
    fields: list
    description: str = ""
    schema_id: str = field(default_factory=_default_schema_id)
    created_ts: float = field(default_factory=_default_created_ts)

    def field_names(self) -> list:
        return [f.name for f in self.fields]

    def required_fields(self) -> list:
        return [f for f in self.fields if f.required]

    def get_field(self, name: str) -> Optional[FieldDef]:
        for f in self.fields:
            if f.name == name:
                return f
        return None
