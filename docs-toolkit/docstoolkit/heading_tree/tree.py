"""Markdown heading tree — builds and queries a hierarchical tree of headings.

Pure stdlib implementation.  No external dependencies.

Usage::

    from docstoolkit.heading_tree import HeadingTree, HeadingNode

    tree = HeadingTree.build(markdown_text)
    print(tree.to_outline())
    print(tree.to_toc(max_level=2))

    node = tree.find("Introduction")
    if node:
        print(node.slug, node.depth, node.is_leaf)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# HeadingNode
# ---------------------------------------------------------------------------

@dataclass
class HeadingNode:
    """A single heading node in the heading tree."""

    level: int
    title: str
    line_num: int
    children: list["HeadingNode"] = field(default_factory=list)
    parent: Optional["HeadingNode"] = field(default=None, repr=False, compare=False)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def slug(self) -> str:
        """URL-safe slug: lowercase, spaces→hyphens, strip non-alnum except hyphens."""
        s = self.title.lower()
        s = s.replace(" ", "-")
        s = re.sub(r"[^a-z0-9\-]", "", s)
        # collapse multiple hyphens
        s = re.sub(r"-{2,}", "-", s)
        s = s.strip("-")
        return s

    @property
    def depth(self) -> int:
        """Distance from root, 0-based (level - 1)."""
        return self.level - 1

    @property
    def is_leaf(self) -> bool:
        """True if this node has no children."""
        return len(self.children) == 0

    # ------------------------------------------------------------------
    # Traversal
    # ------------------------------------------------------------------

    def descendants(self) -> list["HeadingNode"]:
        """Return all descendant nodes in BFS order."""
        result: list[HeadingNode] = []
        queue: list[HeadingNode] = list(self.children)
        while queue:
            node = queue.pop(0)
            result.append(node)
            queue.extend(node.children)
        return result

    def ancestors(self) -> list["HeadingNode"]:
        """Return list from root to self's parent (not including self)."""
        chain: list[HeadingNode] = []
        current = self.parent
        while current is not None:
            chain.append(current)
            current = current.parent
        chain.reverse()
        return chain


# ---------------------------------------------------------------------------
# HeadingTree
# ---------------------------------------------------------------------------

@dataclass
class HeadingTree:
    """Hierarchical tree of markdown headings."""

    roots: list[HeadingNode] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def build(cls, text: str) -> "HeadingTree":
        """Parse headings from *text* and return a HeadingTree.

        Algorithm:
        - Parse lines matching ``#{1,6} text``.
        - Maintain a stack of open nodes.
        - A heading of level N closes all open nodes of level >= N.
        - Level-1 headings are roots; deeper headings become children of
          the nearest ancestor with a strictly lower level.
        """
        tree = cls()
        # stack holds currently "open" nodes — each is a potential parent
        stack: list[HeadingNode] = []

        heading_re = re.compile(r"^(#{1,6})\s+(.*)")

        for line_num, line in enumerate(text.splitlines(), start=1):
            m = heading_re.match(line)
            if not m:
                continue
            level = len(m.group(1))
            title = m.group(2).strip()
            node = HeadingNode(level=level, title=title, line_num=line_num)

            # Pop stack: remove all nodes with level >= current
            while stack and stack[-1].level >= level:
                stack.pop()

            if stack:
                # Attach as child of the top of the stack
                parent = stack[-1]
                node.parent = parent
                parent.children.append(node)
            else:
                # No parent → root
                tree.roots.append(node)

            stack.append(node)

        return tree

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def flat(self) -> list[HeadingNode]:
        """Return all HeadingNodes in document order (pre-order DFS)."""
        result: list[HeadingNode] = []

        def _walk(nodes: list[HeadingNode]) -> None:
            for node in nodes:
                result.append(node)
                _walk(node.children)

        _walk(self.roots)
        return result

    def find(self, title: str) -> Optional[HeadingNode]:
        """Case-insensitive search; return first match or None."""
        needle = title.lower()
        for node in self.flat():
            if node.title.lower() == needle:
                return node
        return None

    def find_all(self, title: str) -> list[HeadingNode]:
        """Case-insensitive search; return all matches."""
        needle = title.lower()
        return [n for n in self.flat() if n.title.lower() == needle]

    def by_level(self, level: int) -> list[HeadingNode]:
        """Return all nodes at the given heading level (1–6)."""
        return [n for n in self.flat() if n.level == level]

    @property
    def max_depth(self) -> int:
        """Maximum heading level present in the tree (0 if empty)."""
        nodes = self.flat()
        if not nodes:
            return 0
        return max(n.level for n in nodes)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def to_outline(self, indent: str = "  ") -> str:
        """Return a plain-text hierarchical outline of the headings."""
        lines: list[str] = []

        def _walk(nodes: list[HeadingNode], depth: int) -> None:
            for node in nodes:
                lines.append(f"{indent * depth}{node.title}")
                _walk(node.children, depth + 1)

        _walk(self.roots, 0)
        return "\n".join(lines)

    def to_toc(self, max_level: int = 3) -> str:
        """Return a markdown TOC with links ``- [title](#slug)``.

        Only includes headings up to *max_level*.
        Indentation is based on heading depth relative to the minimum
        level present (so an H2-only doc has no indent).
        """
        nodes = [n for n in self.flat() if n.level <= max_level]
        if not nodes:
            return ""

        min_level = min(n.level for n in nodes)
        lines: list[str] = []
        indent = "  "
        for node in nodes:
            pad = indent * (node.level - min_level)
            lines.append(f"{pad}- [{node.title}](#{node.slug})")
        return "\n".join(lines)
