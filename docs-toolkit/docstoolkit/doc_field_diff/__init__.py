"""Doc field diff — field-by-field diff between two document dicts.

Stdlib only.

Example::

    from docstoolkit.doc_field_diff import DocFieldDiff, ChangeKind

    differ = DocFieldDiff()
    changes = differ.diff({"a": 1, "b": 2}, {"a": 1, "b": 3, "c": 4})
    # b CHANGED 2 -> 3, c ADDED 4
"""

from docstoolkit.doc_field_diff.diff import (
    ChangeKind,
    DiffSummary,
    DocFieldDiff,
    FieldChange,
)

__all__ = [
    "ChangeKind",
    "DiffSummary",
    "DocFieldDiff",
    "FieldChange",
]
