"""E394 DocOutlineBuilder implementation.

Builds hierarchical outlines from document headings. Pure stdlib,
thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import List

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


@dataclass
class OutlineNode:
    """A single node in a document outline."""

    doc_id: str
    heading: str
    level: int
    position: int
    children: List["OutlineNode"] = field(default_factory=list)


@dataclass
class OutlineStats:
    """Aggregate statistics across all known outlines."""

    total_docs: int
    total_nodes: int
    max_depth: int


class DocOutlineBuilder:
    """Build and query hierarchical outlines for documents."""

    def __init__(self) -> None:
        self._outlines: dict[str, list[OutlineNode]] = {}
        self._trees: dict[str, list[OutlineNode]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ add
    def add_heading(
        self, doc_id: str, heading: str, level: int, position: int
    ) -> OutlineNode:
        """Append a heading to the flat list for *doc_id*.

        Raises
        ------
        ValueError
            If *level* is not in the range 1-6.
        """
        if not isinstance(level, int) or level < 1 or level > 6:
            raise ValueError(
                f"level must be an integer in 1-6, got {level!r}"
            )
        node = OutlineNode(
            doc_id=doc_id, heading=heading, level=level, position=position
        )
        with self._lock:
            self._outlines.setdefault(doc_id, []).append(node)
            self._trees.pop(doc_id, None)
        return node

    # ---------------------------------------------------------------- build
    def build_outline(self, doc_id: str) -> list[OutlineNode]:
        """Build the tree from the flat list for *doc_id*."""
        with self._lock:
            flat = list(self._outlines.get(doc_id, []))

        flat_sorted = sorted(flat, key=lambda n: n.position)
        for n in flat_sorted:
            n.children = []

        roots: list[OutlineNode] = []
        stack: list[OutlineNode] = []
        for node in flat_sorted:
            while stack and stack[-1].level >= node.level:
                stack.pop()
            if stack:
                stack[-1].children.append(node)
            else:
                roots.append(node)
            stack.append(node)

        with self._lock:
            self._trees[doc_id] = roots
        return roots

    # ---------------------------------------------------------------- parse
    def parse_markdown(self, doc_id: str, content: str) -> list[OutlineNode]:
        """Parse markdown *content* and replace any existing outline."""
        with self._lock:
            self._outlines[doc_id] = []
            self._trees.pop(doc_id, None)

        for idx, line in enumerate(content.splitlines(), start=1):
            m = _HEADING_RE.match(line)
            if not m:
                continue
            hashes, title = m.group(1), m.group(2).strip()
            level = len(hashes)
            self.add_heading(doc_id, title, level, idx)

        return self.build_outline(doc_id)

    # ------------------------------------------------------------------ get
    def get_outline(self, doc_id: str) -> list[OutlineNode]:
        """Return the cached tree, or build it on demand."""
        with self._lock:
            cached = self._trees.get(doc_id)
        if cached is not None:
            return cached
        return self.build_outline(doc_id)

    def flat_outline(self, doc_id: str) -> list[OutlineNode]:
        """Return all nodes in *doc_id* sorted by position."""
        with self._lock:
            flat = list(self._outlines.get(doc_id, []))
        return sorted(flat, key=lambda n: n.position)

    def headings_at_level(
        self, doc_id: str, level: int
    ) -> list[OutlineNode]:
        """Return nodes whose level == *level*, sorted by position."""
        return [n for n in self.flat_outline(doc_id) if n.level == level]

    def depth(self, doc_id: str) -> int:
        """Return the maximum level present in *doc_id* (0 if empty)."""
        with self._lock:
            flat = self._outlines.get(doc_id, [])
            if not flat:
                return 0
            return max(n.level for n in flat)

    def node_count(self, doc_id: str) -> int:
        """Return the number of headings recorded for *doc_id*."""
        with self._lock:
            return len(self._outlines.get(doc_id, []))

    def clear_doc(self, doc_id: str) -> bool:
        """Remove all outline data for *doc_id*."""
        with self._lock:
            existed = doc_id in self._outlines or doc_id in self._trees
            self._outlines.pop(doc_id, None)
            self._trees.pop(doc_id, None)
            return existed

    def all_doc_ids(self) -> list[str]:
        """Return sorted list of all document ids with any outline data."""
        with self._lock:
            return sorted(self._outlines.keys())

    def stats(self) -> OutlineStats:
        """Return aggregate statistics across all known outlines."""
        with self._lock:
            total_docs = len(self._outlines)
            total_nodes = sum(len(v) for v in self._outlines.values())
            max_depth = 0
            for nodes in self._outlines.values():
                for n in nodes:
                    if n.level > max_depth:
                        max_depth = n.level
        return OutlineStats(
            total_docs=total_docs,
            total_nodes=total_nodes,
            max_depth=max_depth,
        )
