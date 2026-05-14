"""Schema diff — recursive dict-based schema comparison (E102).

Pure stdlib only: enum, dataclasses, copy.

Public API
----------
ChangeType   — enum of change categories (ADDED/REMOVED/CHANGED/TYPE_CHANGED)
FieldChange  — single field-level change with dot-notation path, old/new values
DiffResult   — collection of FieldChange objects with helper properties & summary()
SchemaDiffer — recursive differ with ignore_paths and treat_list_as_scalar options
"""
from docstoolkit.schema_diff.differ import (
    ChangeType,
    FieldChange,
    DiffResult,
    SchemaDiffer,
)

__all__ = [
    "ChangeType",
    "FieldChange",
    "DiffResult",
    "SchemaDiffer",
]
