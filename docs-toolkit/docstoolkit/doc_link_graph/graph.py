"""DocLinkGraph — directed link graph between documents.

A specialized graph for document link relationships (citations, references,
backlinks) with extra analytics: PageRank, cycle detection, connected
components, BFS path queries.

Stdlib only. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LinkType(Enum):
    """Type of link between two documents."""

    REFERENCE = "reference"
    CITATION = "citation"
    EMBED = "embed"
    MENTION = "mention"
    FOLLOWUP = "followup"


@dataclass
class DocLink:
    """A directed link from one document to another."""

    source: str
    target: str
    link_type: LinkType
    weight: float = 1.0
    metadata: dict = field(default_factory=dict)
    created_at: float = 0.0


@dataclass
class LinkStats:
    """Aggregate stats about the link graph."""

    total_docs: int
    total_links: int
    most_linked_to: list  # list[tuple[str, int]] — top 10 by incoming
    most_linking: list  # list[tuple[str, int]] — top 10 by outgoing
    orphan_count: int  # docs with no links in or out


class DocLinkGraph:
    """Directed link graph between documents."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._docs: set = set()
        # adjacency lists
        self._out: dict = {}  # source -> list[DocLink]
        self._in: dict = {}  # target -> list[DocLink]

    # ----- documents -----

    def add_doc(self, doc_id: str) -> None:
        """Register a document. No-op if it already exists."""
        with self._lock:
            if doc_id not in self._docs:
                self._docs.add(doc_id)
                self._out.setdefault(doc_id, [])
                self._in.setdefault(doc_id, [])

    def remove_doc(self, doc_id: str) -> bool:
        """Remove a document and all incident links. Returns True if removed."""
        with self._lock:
            if doc_id not in self._docs:
                return False
            # remove outgoing
            for link in list(self._out.get(doc_id, [])):
                self._in[link.target] = [
                    l for l in self._in.get(link.target, []) if l.source != doc_id
                ]
            # remove incoming
            for link in list(self._in.get(doc_id, [])):
                self._out[link.source] = [
                    l for l in self._out.get(link.source, []) if l.target != doc_id
                ]
            self._out.pop(doc_id, None)
            self._in.pop(doc_id, None)
            self._docs.discard(doc_id)
            return True

    def all_docs(self) -> list:
        """Return all registered document IDs."""
        with self._lock:
            return sorted(self._docs)

    # ----- links -----

    def add_link(
        self,
        source: str,
        target: str,
        link_type: LinkType = LinkType.REFERENCE,
        weight: float = 1.0,
        metadata: dict = None,
        now: float = 0.0,
    ) -> DocLink:
        """Add a link source -> target. If link already exists, replace it."""
        with self._lock:
            # ensure docs exist
            for doc_id in (source, target):
                if doc_id not in self._docs:
                    self._docs.add(doc_id)
                    self._out.setdefault(doc_id, [])
                    self._in.setdefault(doc_id, [])
            # remove existing link of same (source, target) so we don't dup
            self._out[source] = [l for l in self._out[source] if l.target != target]
            self._in[target] = [l for l in self._in[target] if l.source != source]
            link = DocLink(
                source=source,
                target=target,
                link_type=link_type,
                weight=weight,
                metadata=dict(metadata) if metadata else {},
                created_at=now,
            )
            self._out[source].append(link)
            self._in[target].append(link)
            return link

    def remove_link(self, source: str, target: str) -> bool:
        """Remove a link. Returns True if removed."""
        with self._lock:
            if source not in self._out:
                return False
            before = len(self._out[source])
            self._out[source] = [l for l in self._out[source] if l.target != target]
            if len(self._out[source]) == before:
                return False
            self._in[target] = [l for l in self._in.get(target, []) if l.source != source]
            return True

    def update_link(
        self,
        source: str,
        target: str,
        weight: float = None,
        metadata: dict = None,
    ) -> bool:
        """Update weight and/or metadata of an existing link."""
        with self._lock:
            if source not in self._out:
                return False
            for link in self._out[source]:
                if link.target == target:
                    if weight is not None:
                        link.weight = weight
                    if metadata is not None:
                        link.metadata.update(metadata)
                    return True
            return False

    def forward_links(self, doc_id: str) -> list:
        """All links going out of doc_id."""
        with self._lock:
            return list(self._out.get(doc_id, []))

    def backlinks(self, doc_id: str) -> list:
        """All links coming into doc_id."""
        with self._lock:
            return list(self._in.get(doc_id, []))

    def links_by_type(self, link_type: LinkType) -> list:
        """All links with the given type."""
        with self._lock:
            result = []
            for doc_links in self._out.values():
                for link in doc_links:
                    if link.link_type == link_type:
                        result.append(link)
            return result

    def is_linked(self, source: str, target: str) -> bool:
        """True iff there's a direct link source -> target."""
        with self._lock:
            return any(l.target == target for l in self._out.get(source, []))

    # ----- traversal -----

    def path(self, source: str, target: str, max_depth: int = 5) -> Optional[list]:
        """Shortest forward path source -> target via BFS. Returns None if none."""
        with self._lock:
            if source not in self._docs or target not in self._docs:
                return None
            if source == target:
                return [source]
            visited = {source}
            queue = deque([(source, [source])])
            while queue:
                current, path = queue.popleft()
                if len(path) - 1 >= max_depth:
                    continue
                for link in self._out.get(current, []):
                    nxt = link.target
                    if nxt == target:
                        return path + [nxt]
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append((nxt, path + [nxt]))
            return None

    def descendants(self, doc_id: str, depth: int = 1) -> set:
        """All docs reachable forward from doc_id within `depth` hops."""
        with self._lock:
            if doc_id not in self._docs:
                return set()
            result: set = set()
            queue = deque([(doc_id, 0)])
            visited = {doc_id}
            while queue:
                current, d = queue.popleft()
                if d >= depth:
                    continue
                for link in self._out.get(current, []):
                    nxt = link.target
                    if nxt not in visited:
                        visited.add(nxt)
                        result.add(nxt)
                        queue.append((nxt, d + 1))
            return result

    def ancestors(self, doc_id: str, depth: int = 1) -> set:
        """All docs reachable backward from doc_id within `depth` hops."""
        with self._lock:
            if doc_id not in self._docs:
                return set()
            result: set = set()
            queue = deque([(doc_id, 0)])
            visited = {doc_id}
            while queue:
                current, d = queue.popleft()
                if d >= depth:
                    continue
                for link in self._in.get(current, []):
                    nxt = link.source
                    if nxt not in visited:
                        visited.add(nxt)
                        result.add(nxt)
                        queue.append((nxt, d + 1))
            return result

    def clusters(self) -> list:
        """Connected components (treating links as undirected)."""
        with self._lock:
            visited: set = set()
            components = []
            for doc in self._docs:
                if doc in visited:
                    continue
                comp: set = set()
                stack = [doc]
                while stack:
                    current = stack.pop()
                    if current in comp:
                        continue
                    comp.add(current)
                    for link in self._out.get(current, []):
                        if link.target not in comp:
                            stack.append(link.target)
                    for link in self._in.get(current, []):
                        if link.source not in comp:
                            stack.append(link.source)
                visited |= comp
                components.append(comp)
            return components

    def circular_refs(self) -> list:
        """Detect cycles using iterative DFS. Returns list of cycle node sequences."""
        with self._lock:
            cycles = []
            seen_cycles: set = set()
            WHITE, GRAY, BLACK = 0, 1, 2
            color = {d: WHITE for d in self._docs}

            for start in self._docs:
                if color[start] != WHITE:
                    continue
                # iterative DFS with parent tracking
                stack = [(start, iter(self._out.get(start, [])), None)]
                path = [start]
                path_set = {start}
                color[start] = GRAY
                while stack:
                    node, it, _ = stack[-1]
                    try:
                        link = next(it)
                        nxt = link.target
                        if color.get(nxt, WHITE) == GRAY:
                            # found a cycle: extract from path
                            if nxt in path_set:
                                idx = path.index(nxt)
                                cycle = path[idx:] + [nxt]
                                # canonicalize: rotate so smallest is first (without trailing dup)
                                core = cycle[:-1]
                                if core:
                                    min_idx = core.index(min(core))
                                    canon = tuple(core[min_idx:] + core[:min_idx])
                                    if canon not in seen_cycles:
                                        seen_cycles.add(canon)
                                        cycles.append(list(canon) + [canon[0]])
                        elif color.get(nxt, WHITE) == WHITE:
                            color[nxt] = GRAY
                            path.append(nxt)
                            path_set.add(nxt)
                            stack.append((nxt, iter(self._out.get(nxt, [])), node))
                    except StopIteration:
                        color[node] = BLACK
                        path.pop()
                        path_set.discard(node)
                        stack.pop()
            return cycles

    def pagerank(self, iterations: int = 20, damping: float = 0.85) -> dict:
        """Simplified iterative PageRank. Empty graph -> empty dict."""
        with self._lock:
            n = len(self._docs)
            if n == 0:
                return {}
            docs = list(self._docs)
            init = 1.0 / n
            ranks = {d: init for d in docs}
            for _ in range(iterations):
                new_ranks = {d: (1.0 - damping) / n for d in docs}
                dangling_sum = 0.0
                for d in docs:
                    out = self._out.get(d, [])
                    if not out:
                        dangling_sum += ranks[d]
                # distribute dangling across all nodes
                dangling_contrib = damping * dangling_sum / n
                for d in docs:
                    new_ranks[d] += dangling_contrib
                for d in docs:
                    out = self._out.get(d, [])
                    if not out:
                        continue
                    share = damping * ranks[d] / len(out)
                    for link in out:
                        if link.target in new_ranks:
                            new_ranks[link.target] += share
                ranks = new_ranks
            return ranks

    # ----- degrees -----

    def out_degree(self, doc_id: str) -> int:
        with self._lock:
            return len(self._out.get(doc_id, []))

    def in_degree(self, doc_id: str) -> int:
        with self._lock:
            return len(self._in.get(doc_id, []))

    def total_degree(self, doc_id: str) -> int:
        with self._lock:
            return len(self._out.get(doc_id, [])) + len(self._in.get(doc_id, []))

    def orphans(self) -> list:
        """Docs with no links in or out."""
        with self._lock:
            return sorted(
                d
                for d in self._docs
                if not self._out.get(d) and not self._in.get(d)
            )

    # ----- stats -----

    def stats(self) -> LinkStats:
        with self._lock:
            total_links = sum(len(v) for v in self._out.values())
            in_counts = [(d, len(self._in.get(d, []))) for d in self._docs]
            out_counts = [(d, len(self._out.get(d, []))) for d in self._docs]
            in_counts.sort(key=lambda x: (-x[1], x[0]))
            out_counts.sort(key=lambda x: (-x[1], x[0]))
            most_linked_to = [pair for pair in in_counts[:10] if pair[1] > 0]
            most_linking = [pair for pair in out_counts[:10] if pair[1] > 0]
            orphan_count = sum(
                1
                for d in self._docs
                if not self._out.get(d) and not self._in.get(d)
            )
            return LinkStats(
                total_docs=len(self._docs),
                total_links=total_links,
                most_linked_to=most_linked_to,
                most_linking=most_linking,
                orphan_count=orphan_count,
            )

    @property
    def link_count(self) -> int:
        with self._lock:
            return sum(len(v) for v in self._out.values())

    @property
    def doc_count(self) -> int:
        with self._lock:
            return len(self._docs)

    def clear(self) -> None:
        with self._lock:
            self._docs.clear()
            self._out.clear()
            self._in.clear()
