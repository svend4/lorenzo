"""Content diff — structured line-level and section-level document diffing.

Stdlib only (difflib).

Example::

    from docstoolkit.content_diff import ContentDiffer, DiffResult, ChangeType

    differ = ContentDiffer()
    result = differ.diff("hello\nworld", "hello\nearth")
    print(result.summary)          # +1/-1 lines
    print(result.has_changes)      # True
    print(result.similarity)       # 0.5
"""

from docstoolkit.content_diff.differ import (
    ChangeType,
    ContentDiffer,
    DiffResult,
    LineChange,
    SectionChange,
)

__all__ = [
    "ChangeType",
    "ContentDiffer",
    "DiffResult",
    "LineChange",
    "SectionChange",
]
