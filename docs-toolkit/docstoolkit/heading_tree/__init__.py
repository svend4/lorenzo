"""Heading tree module for docs-toolkit.

Builds and queries a hierarchical tree of markdown headings.
Pure stdlib — no external dependencies.

Usage::

    from docstoolkit.heading_tree import HeadingTree, HeadingNode

    tree = HeadingTree.build(markdown_text)

    # Flat list in document order
    for node in tree.flat():
        print(node.level, node.title, node.slug)

    # Find a heading (case-insensitive)
    intro = tree.find("Introduction")

    # All H2 headings
    h2s = tree.by_level(2)

    # Text outline
    print(tree.to_outline())

    # Markdown TOC (H1–H3)
    print(tree.to_toc(max_level=3))
"""
from docstoolkit.heading_tree.tree import HeadingNode, HeadingTree

__all__ = [
    "HeadingNode",
    "HeadingTree",
]
