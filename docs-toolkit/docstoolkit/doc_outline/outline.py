"""Document outline implementation.

Builds hierarchical outlines from markdown documents using only stdlib.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Optional

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


@dataclass
class OutlineNode:
    """A single heading node in the outline tree."""

    level: int
    title: str
    line_num: int  # 1-based
    char_offset: int
    section_length: int = 0  # chars until next sibling/end
    children: list["OutlineNode"] = field(default_factory=list)
    parent: Optional["OutlineNode"] = field(default=None, repr=False, compare=False)


@dataclass
class OutlineStats:
    """Aggregate statistics for an outline."""

    total_nodes: int
    by_level: dict[int, int]
    max_depth: int
    avg_section_length: float
    largest_section: Optional[OutlineNode]
    smallest_section: Optional[OutlineNode]


class DocOutline:
    """Builds and queries hierarchical outlines of markdown documents."""

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------ build

    def build(self, content: str) -> list[OutlineNode]:
        """Build the outline tree.

        Returns the list of root-level nodes (the highest level present
        in the document — typically H1, but the smallest level value
        encountered is treated as the root level).
        """
        flat = self._parse(content)
        if not flat:
            return []

        total_len = len(content)
        self._compute_section_lengths(flat, total_len)

        roots: list[OutlineNode] = []
        stack: list[OutlineNode] = []

        for node in flat:
            # Pop stack until we find an ancestor with a smaller level.
            while stack and stack[-1].level >= node.level:
                stack.pop()
            if stack:
                parent = stack[-1]
                node.parent = parent
                parent.children.append(node)
            else:
                roots.append(node)
            stack.append(node)

        return roots

    def build_flat(self, content: str) -> list[OutlineNode]:
        """Build outline and return nodes in depth-first (document) order."""
        roots = self.build(content)
        result: list[OutlineNode] = []
        self._walk_dfs(roots, result)
        return result

    # ----------------------------------------------------------------- parse

    def _parse(self, content: str) -> list[OutlineNode]:
        """Parse headings from content. Skips fenced code blocks."""
        nodes: list[OutlineNode] = []
        if not content:
            return nodes

        # Walk the content line-by-line, tracking char offset of each line.
        offset = 0
        in_fence = False
        fence_marker: Optional[str] = None
        # Use splitlines(keepends=True) to compute offsets accurately.
        lines = content.splitlines(keepends=True)
        for idx, raw_line in enumerate(lines):
            line = raw_line.rstrip("\n").rstrip("\r")

            # Track fenced code blocks (``` or ~~~).
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                marker = stripped[:3]
                if not in_fence:
                    in_fence = True
                    fence_marker = marker
                elif fence_marker is not None and stripped.startswith(fence_marker):
                    in_fence = False
                    fence_marker = None
                offset += len(raw_line)
                continue

            if in_fence:
                offset += len(raw_line)
                continue

            m = _HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                nodes.append(
                    OutlineNode(
                        level=level,
                        title=title,
                        line_num=idx + 1,
                        char_offset=offset,
                    )
                )

            offset += len(raw_line)

        return nodes

    def _compute_section_lengths(
        self, flat: list[OutlineNode], total_len: int
    ) -> None:
        """Section length = chars from this heading's offset until the next
        heading at the same level OR shallower, or until end of document.
        """
        n = len(flat)
        for i, node in enumerate(flat):
            next_offset = total_len
            for j in range(i + 1, n):
                if flat[j].level <= node.level:
                    next_offset = flat[j].char_offset
                    break
            node.section_length = max(0, next_offset - node.char_offset)

    # --------------------------------------------------------------- queries

    def find_node(
        self,
        roots: list[OutlineNode],
        title: str,
        level: Optional[int] = None,
    ) -> Optional[OutlineNode]:
        """Find first node matching ``title`` (case-insensitive).

        If ``level`` is given, only nodes at that level match.
        """
        target = title.strip().lower()
        for node in self._iter_all(roots):
            if node.title.strip().lower() == target:
                if level is None or node.level == level:
                    return node
        return None

    def nodes_at_level(
        self, roots: list[OutlineNode], level: int
    ) -> list[OutlineNode]:
        """All nodes at the given level (in document order)."""
        return [n for n in self._iter_all(roots) if n.level == level]

    def descendants(self, node: OutlineNode) -> list[OutlineNode]:
        """All descendants of ``node`` in depth-first order (excludes self)."""
        out: list[OutlineNode] = []
        for child in node.children:
            out.append(child)
            out.extend(self.descendants(child))
        return out

    def ancestors(self, node: OutlineNode) -> list[OutlineNode]:
        """All ancestors of ``node`` from immediate parent to root."""
        result: list[OutlineNode] = []
        cur = node.parent
        while cur is not None:
            result.append(cur)
            cur = cur.parent
        return result

    # --------------------------------------------------------------- render

    def to_toc(
        self,
        roots: list[OutlineNode],
        max_level: int = 6,
        with_lines: bool = False,
    ) -> str:
        """Render a markdown TOC (bulleted list, indented by level)."""
        lines: list[str] = []
        for node in self._iter_all(roots):
            if node.level > max_level:
                continue
            # Indent relative to the shallowest root level.
            indent_level = node.level - (roots[0].level if roots else 1)
            if indent_level < 0:
                indent_level = 0
            prefix = "  " * indent_level + "- "
            if with_lines:
                lines.append(f"{prefix}{node.title} (L{node.line_num})")
            else:
                lines.append(f"{prefix}{node.title}")
        return "\n".join(lines)

    def to_markdown(
        self,
        roots: list[OutlineNode],
        indent: str = "  ",
        max_level: int = 6,
    ) -> str:
        """Render outline as an indented markdown list."""
        lines: list[str] = []
        base_level = roots[0].level if roots else 1
        for node in self._iter_all(roots):
            if node.level > max_level:
                continue
            depth = node.level - base_level
            if depth < 0:
                depth = 0
            lines.append(f"{indent * depth}- {node.title}")
        return "\n".join(lines)

    def to_dict(self, roots: list[OutlineNode]) -> list[dict]:
        """Convert outline to a serialisable list of dicts (recursive)."""
        return [self._node_to_dict(n) for n in roots]

    def _node_to_dict(self, node: OutlineNode) -> dict:
        return {
            "level": node.level,
            "title": node.title,
            "line_num": node.line_num,
            "char_offset": node.char_offset,
            "section_length": node.section_length,
            "children": [self._node_to_dict(c) for c in node.children],
        }

    def to_json(self, roots: list[OutlineNode]) -> str:
        """Render outline as a JSON string."""
        return json.dumps(self.to_dict(roots), ensure_ascii=False, indent=2)

    # ----------------------------------------------------------------- stats

    def stats(self, roots: list[OutlineNode]) -> OutlineStats:
        """Compute aggregate statistics."""
        all_nodes = list(self._iter_all(roots))
        total = len(all_nodes)

        by_level: dict[int, int] = {}
        for node in all_nodes:
            by_level[node.level] = by_level.get(node.level, 0) + 1

        depth = self.max_depth(roots)

        if total:
            avg = sum(n.section_length for n in all_nodes) / total
            largest = max(all_nodes, key=lambda n: n.section_length)
            smallest = min(all_nodes, key=lambda n: n.section_length)
        else:
            avg = 0.0
            largest = None
            smallest = None

        return OutlineStats(
            total_nodes=total,
            by_level=by_level,
            max_depth=depth,
            avg_section_length=avg,
            largest_section=largest,
            smallest_section=smallest,
        )

    def max_depth(self, roots: list[OutlineNode]) -> int:
        """Max nesting depth (root nodes have depth 1)."""
        if not roots:
            return 0

        def _depth(node: OutlineNode) -> int:
            if not node.children:
                return 1
            return 1 + max(_depth(c) for c in node.children)

        return max(_depth(r) for r in roots)

    def count_nodes(self, roots: list[OutlineNode]) -> int:
        """Total number of nodes in the outline."""
        return sum(1 for _ in self._iter_all(roots))

    # ----------------------------------------------------------------- utils

    def _iter_all(self, roots: list[OutlineNode]):
        """Depth-first traversal yielding every node."""
        for r in roots:
            yield r
            yield from self._iter_all(r.children)

    def _walk_dfs(
        self, roots: list[OutlineNode], out: list[OutlineNode]
    ) -> None:
        for r in roots:
            out.append(r)
            self._walk_dfs(r.children, out)
