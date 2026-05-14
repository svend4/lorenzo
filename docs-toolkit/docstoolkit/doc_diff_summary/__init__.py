"""Doc diff summary — statistical and semantic summaries of document diffs.

Stdlib only (difflib, re).

Example::

    from docstoolkit.doc_diff_summary import DocDiffSummarizer

    s = DocDiffSummarizer()
    summary = s.summarize("# A\\nold", "# A\\nnew")
    print(summary.magnitude)        # ChangeMagnitude.MAJOR
    print(summary.similarity)       # 0.x
    print(s.summary_text(old, new)) # "+1/-1 lines, similarity 0.50 ..."
"""

from docstoolkit.doc_diff_summary.summarizer import (
    ChangeMagnitude,
    ChangeTypeStats,
    DiffSummary,
    DocDiffSummarizer,
)

__all__ = [
    "ChangeMagnitude",
    "ChangeTypeStats",
    "DiffSummary",
    "DocDiffSummarizer",
]
