"""Doc diff v2 — advanced document diff with multiple granularities.

Stdlib only (difflib, re).

Example::

    from docstoolkit.doc_diff_v2 import DocDiffV2, DiffGranularity

    d = DocDiffV2()
    chunks = d.diff("hello world", "hello there", DiffGranularity.WORD)
    print(d.inline_html("hello world", "hello there"))
"""

from docstoolkit.doc_diff_v2.differ import (
    DiffChunk,
    DiffGranularity,
    DiffOp,
    DocDiffV2,
    StructuralDiff,
    WordDiffStats,
)

__all__ = [
    "DiffChunk",
    "DiffGranularity",
    "DiffOp",
    "DocDiffV2",
    "StructuralDiff",
    "WordDiffStats",
]
