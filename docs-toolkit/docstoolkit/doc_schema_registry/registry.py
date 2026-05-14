"""DocSchemaRegistry — thread-safe in-memory registry for document schemas (E281)."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Optional
from uuid import uuid4


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class FieldDef:
    """Definition of a single document field."""
    name: str
    field_type: str          # "str", "int", "float", "bool", "list", "dict"
    required: bool = False
    default: Any = None
    description: str = ""
    validators: list = field(default_factory=list)  # callables (stored but not invoked)


@dataclass
class DocSchema:
    """A named, versioned collection of field definitions."""
    schema_id: str
    name: str
    version: int = 1
    fields: list = field(default_factory=list)   # list[FieldDef]
    description: str = ""


@dataclass
class ValidationResult:
    """Result of validating a document against a schema."""
    schema_id: str
    doc_id: str
    valid: bool
    errors: list = field(default_factory=list)   # list[str]


@dataclass
class RegistryStats:
    """Aggregate statistics about the registry."""
    total_schemas: int
    total_fields: int
    avg_fields_per_schema: float


# ---------------------------------------------------------------------------
# Type mapping for isinstance checks
# ---------------------------------------------------------------------------

_TYPE_MAP: dict[str, Any] = {
    "str":   str,
    "int":   int,
    "float": (int, float),   # ints are also valid floats
    "bool":  bool,
    "list":  list,
    "dict":  dict,
}


def _check_type(value: Any, field_type: str) -> bool:
    """Return True if *value* matches *field_type*.

    Special case: bool must be checked before int because bool is a subclass
    of int in Python.  When the declared type is "int" we must reject bools.
    """
    if field_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if field_type == "float":
        # allow int literals for float fields, but reject bools
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    expected = _TYPE_MAP.get(field_type)
    if expected is None:
        return True  # unknown type — skip check
    return isinstance(value, expected)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class DocSchemaRegistry:
    """Thread-safe, in-memory registry for document schemas."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._schemas: dict[str, DocSchema] = {}   # schema_id → DocSchema

    # ------------------------------------------------------------------
    # Schema CRUD
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        fields: Optional[list] = None,
        description: str = "",
    ) -> DocSchema:
        """Register a new schema and return it with a generated schema_id."""
        schema_id = f"schema_{uuid4().hex[:12]}"
        schema = DocSchema(
            schema_id=schema_id,
            name=name,
            version=1,
            fields=list(fields) if fields is not None else [],
            description=description,
        )
        with self._lock:
            self._schemas[schema_id] = schema
        return schema

    def update(
        self,
        schema_id: str,
        fields: Optional[list] = None,
        description: Optional[str] = None,
    ) -> Optional[DocSchema]:
        """Update fields/description of an existing schema, incrementing version.

        Returns the updated schema, or None if schema_id does not exist.
        """
        with self._lock:
            schema = self._schemas.get(schema_id)
            if schema is None:
                return None
            if fields is not None:
                schema.fields = list(fields)
            if description is not None:
                schema.description = description
            schema.version += 1
            return schema

    def get(self, schema_id: str) -> Optional[DocSchema]:
        """Return the schema with the given id, or None."""
        with self._lock:
            return self._schemas.get(schema_id)

    def get_by_name(self, name: str) -> Optional[DocSchema]:
        """Return the first schema whose name matches, or None."""
        with self._lock:
            for schema in self._schemas.values():
                if schema.name == name:
                    return schema
        return None

    def delete(self, schema_id: str) -> bool:
        """Remove a schema. Returns True if it existed, False otherwise."""
        with self._lock:
            if schema_id in self._schemas:
                del self._schemas[schema_id]
                return True
            return False

    def schemas(self) -> list:
        """Return all schemas sorted by name."""
        with self._lock:
            return sorted(self._schemas.values(), key=lambda s: s.name)

    # ------------------------------------------------------------------
    # Field-level helpers
    # ------------------------------------------------------------------

    def add_field(self, schema_id: str, field_def: FieldDef) -> bool:
        """Append a field to an existing schema. Returns False if schema not found."""
        with self._lock:
            schema = self._schemas.get(schema_id)
            if schema is None:
                return False
            schema.fields.append(field_def)
            return True

    def remove_field(self, schema_id: str, field_name: str) -> bool:
        """Remove a field by name. Returns False if schema or field not found."""
        with self._lock:
            schema = self._schemas.get(schema_id)
            if schema is None:
                return False
            original_len = len(schema.fields)
            schema.fields = [f for f in schema.fields if f.name != field_name]
            return len(schema.fields) < original_len

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        schema_id: str,
        doc: dict,
        doc_id: str = "doc",
    ) -> ValidationResult:
        """Validate *doc* against the schema identified by *schema_id*.

        Checks:
        - Required fields are present in *doc*.
        - Present fields match their declared types.

        Returns a :class:`ValidationResult` with ``valid=False`` and an error
        message if the schema is not found.
        """
        with self._lock:
            schema = self._schemas.get(schema_id)

        if schema is None:
            return ValidationResult(
                schema_id=schema_id,
                doc_id=doc_id,
                valid=False,
                errors=["schema not found"],
            )

        errors: list[str] = []

        for fdef in schema.fields:
            if fdef.name in doc:
                value = doc[fdef.name]
                if not _check_type(value, fdef.field_type):
                    errors.append(
                        f"field '{fdef.name}' expected {fdef.field_type}, "
                        f"got {type(value).__name__}"
                    )
            elif fdef.required:
                errors.append(f"missing required field '{fdef.name}'")

        return ValidationResult(
            schema_id=schema_id,
            doc_id=doc_id,
            valid=len(errors) == 0,
            errors=errors,
        )

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> RegistryStats:
        """Return aggregate statistics about the registry."""
        with self._lock:
            total = len(self._schemas)
            total_fields = sum(len(s.fields) for s in self._schemas.values())
        avg = total_fields / total if total > 0 else 0.0
        return RegistryStats(
            total_schemas=total,
            total_fields=total_fields,
            avg_fields_per_schema=avg,
        )

    # ------------------------------------------------------------------
    # Convenience property
    # ------------------------------------------------------------------

    @property
    def total_schemas(self) -> int:
        """Number of schemas currently registered."""
        with self._lock:
            return len(self._schemas)
