"""Document outline module for docs-toolkit.

Builds hierarchical, collapsible document outlines from markdown.
Tracks line numbers, character offsets, and section lengths.
Supports TOC rendering, markdown export, JSON serialization, and stats.

Pure stdlib — only ``re`` and ``json`` are used.

Usage::

    from docstoolkit.doc_outline import DocOutline, OutlineNode, OutlineStats

    outline = DocOutline()
    roots = outline.build(markdown_text)

    # Walk the tree
    for node in outline.build_flat(markdown_text):
        print(node.level, node.title, node.line_num)

    # Render TOC
    print(outline.to_toc(roots, max_level=3, with_lines=True))

    # Stats
    stats = outline.stats(roots)
    print(stats.total_nodes, stats.max_depth)
"""
from docstoolkit.doc_outline.outline import (
    DocOutline,
    OutlineNode,
    OutlineStats,
)

__all__ = [
    "DocOutline",
    "OutlineNode",
    "OutlineStats",
]
