"""DocDependencyGraph — directed dependency graph for documents.

Tracks directed "A depends on B" relationships between document IDs with
full cycle detection, topological sort (Kahn's algorithm), and reachability
queries.

Stdlib only. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field


@dataclass
class DependencyEdge:
    """A single directed dependency between two documents.

    ``from_doc`` depends on ``to_doc``.
    """

    from_doc: str
    to_doc: str
    kind: str = "depends_on"


@dataclass
class GraphStats:
    """Aggregate statistics for the dependency graph.

    Attributes
    ----------
    total_nodes:
        Number of unique doc IDs registered in the graph.
    total_edges:
        Total number of directed dependency edges.
    root_count:
        Nodes with in-degree 0 — nothing depends on them as a target
        (i.e. no other doc declares a dependency *on* them).
    leaf_count:
        Nodes with out-degree 0 — they do not depend on any other doc.
    """

    total_nodes: int
    total_edges: int
    root_count: int
    leaf_count: int


class DocDependencyGraph:
    """Directed dependency graph for document IDs.

    An edge ``from_doc -> to_doc`` means "from_doc depends on to_doc".

    Internal storage
    ----------------
    ``_nodes``  : set[str]                       — all known doc IDs
    ``_out``    : dict[str, dict[str, str]]      — _out[from_doc][to_doc] = kind
    ``_in``     : dict[str, set[str]]            — _in[to_doc] = {from_docs}
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._nodes: set[str] = set()
        self._out: dict[str, dict[str, str]] = {}   # from_doc -> {to_doc: kind}
        self._in: dict[str, set[str]] = {}           # to_doc   -> {from_doc, ...}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock already held)
    # ------------------------------------------------------------------

    def _register(self, doc_id: str) -> None:
        """Ensure doc_id exists in all structures (lock must be held)."""
        if doc_id not in self._nodes:
            self._nodes.add(doc_id)
            self._out.setdefault(doc_id, {})
            self._in.setdefault(doc_id, set())

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_dependency(
        self, from_doc: str, to_doc: str, kind: str = "depends_on"
    ) -> bool:
        """Add a directed edge ``from_doc -> to_doc``.

        Both nodes are automatically registered.

        Returns
        -------
        bool
            ``True`` if the edge is new; ``False`` if it already existed
            (the ``kind`` is *not* updated in that case).
        """
        with self._lock:
            self._register(from_doc)
            self._register(to_doc)
            if to_doc in self._out[from_doc]:
                return False
            self._out[from_doc][to_doc] = kind
            self._in[to_doc].add(from_doc)
            return True

    def remove_dependency(self, from_doc: str, to_doc: str) -> bool:
        """Remove the edge ``from_doc -> to_doc``.

        Both nodes remain registered even if their edge count drops to zero.

        Returns
        -------
        bool
            ``True`` if the edge existed and was removed; ``False`` otherwise.
        """
        with self._lock:
            if from_doc not in self._out or to_doc not in self._out[from_doc]:
                return False
            del self._out[from_doc][to_doc]
            self._in[to_doc].discard(from_doc)
            return True

    def remove_doc(self, doc_id: str) -> int:
        """Remove a document and all its incident edges.

        Parameters
        ----------
        doc_id:
            The document to remove.

        Returns
        -------
        int
            Number of edges that were removed.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return 0

            removed = 0

            # Remove outgoing edges: doc_id -> X
            for to_doc in list(self._out.get(doc_id, {}).keys()):
                self._in[to_doc].discard(doc_id)
                removed += 1
            self._out.pop(doc_id, None)

            # Remove incoming edges: X -> doc_id
            for from_doc in list(self._in.get(doc_id, set())):
                self._out[from_doc].pop(doc_id, None)
                removed += 1
            self._in.pop(doc_id, None)

            self._nodes.discard(doc_id)
            return removed

    # ------------------------------------------------------------------
    # Query — neighbours
    # ------------------------------------------------------------------

    def dependencies_of(self, doc_id: str) -> list[str]:
        """Sorted list of docs that ``doc_id`` directly depends on (outgoing)."""
        with self._lock:
            return sorted(self._out.get(doc_id, {}).keys())

    def dependents_of(self, doc_id: str) -> list[str]:
        """Sorted list of docs that directly depend on ``doc_id`` (incoming)."""
        with self._lock:
            return sorted(self._in.get(doc_id, set()))

    def has_dependency(self, from_doc: str, to_doc: str) -> bool:
        """True iff a direct edge ``from_doc -> to_doc`` exists."""
        with self._lock:
            return to_doc in self._out.get(from_doc, {})

    # ------------------------------------------------------------------
    # Query — collections
    # ------------------------------------------------------------------

    def all_docs(self) -> list[str]:
        """Sorted list of all registered document IDs."""
        with self._lock:
            return sorted(self._nodes)

    def edges(self) -> list[DependencyEdge]:
        """All edges sorted by ``(from_doc, to_doc, kind)``."""
        with self._lock:
            result: list[DependencyEdge] = []
            for from_doc, targets in self._out.items():
                for to_doc, kind in targets.items():
                    result.append(DependencyEdge(from_doc=from_doc, to_doc=to_doc, kind=kind))
            result.sort(key=lambda e: (e.from_doc, e.to_doc, e.kind))
            return result

    def edges_from(self, doc_id: str) -> list[DependencyEdge]:
        """All edges originating from ``doc_id``, sorted by ``(to_doc, kind)``."""
        with self._lock:
            result: list[DependencyEdge] = [
                DependencyEdge(from_doc=doc_id, to_doc=to_doc, kind=kind)
                for to_doc, kind in self._out.get(doc_id, {}).items()
            ]
            result.sort(key=lambda e: (e.to_doc, e.kind))
            return result

    def edges_to(self, doc_id: str) -> list[DependencyEdge]:
        """All edges pointing to ``doc_id``, sorted by ``(from_doc, kind)``."""
        with self._lock:
            result: list[DependencyEdge] = [
                DependencyEdge(
                    from_doc=from_doc,
                    to_doc=doc_id,
                    kind=self._out[from_doc][doc_id],
                )
                for from_doc in self._in.get(doc_id, set())
                if doc_id in self._out.get(from_doc, {})
            ]
            result.sort(key=lambda e: (e.from_doc, e.kind))
            return result

    # ------------------------------------------------------------------
    # Graph algorithms
    # ------------------------------------------------------------------

    def has_cycle(self) -> bool:
        """True if the graph contains at least one cycle (iterative DFS)."""
        with self._lock:
            WHITE, GRAY, BLACK = 0, 1, 2
            color: dict[str, int] = {n: WHITE for n in self._nodes}

            for start in self._nodes:
                if color[start] != WHITE:
                    continue
                # Iterative DFS
                stack: list[tuple[str, object]] = [
                    (start, iter(self._out.get(start, {}).keys()))
                ]
                color[start] = GRAY
                while stack:
                    node, children = stack[-1]
                    try:
                        child = next(children)  # type: ignore[call-overload]
                        c = color.get(child, WHITE)
                        if c == GRAY:
                            return True
                        if c == WHITE:
                            color[child] = GRAY
                            stack.append(
                                (child, iter(self._out.get(child, {}).keys()))
                            )
                    except StopIteration:
                        color[node] = BLACK
                        stack.pop()
            return False

    def topological_sort(self) -> list[str]:
        """Kahn's BFS topological sort — dependencies come first.

        Returns
        -------
        list[str]
            All nodes in an order where every dependency appears before
            the document that depends on it.

        Raises
        ------
        ValueError
            If the graph contains cycles.
        """
        with self._lock:
            # in-degree of each node within the current graph
            in_deg: dict[str, int] = {n: len(self._in.get(n, set())) for n in self._nodes}
            queue: deque[str] = deque(sorted(n for n, d in in_deg.items() if d == 0))
            result: list[str] = []

            while queue:
                node = queue.popleft()
                result.append(node)
                for child in sorted(self._out.get(node, {}).keys()):
                    in_deg[child] -= 1
                    if in_deg[child] == 0:
                        queue.append(child)

            if len(result) != len(self._nodes):
                raise ValueError("Graph has cycles")
            return result

    def reachable_from(self, doc_id: str) -> list[str]:
        """Sorted list of all docs reachable from ``doc_id`` via dependency edges.

        ``doc_id`` itself is excluded from the result.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return []
            visited: set[str] = {doc_id}
            queue: deque[str] = deque([doc_id])
            while queue:
                current = queue.popleft()
                for child in self._out.get(current, {}).keys():
                    if child not in visited:
                        visited.add(child)
                        queue.append(child)
            visited.discard(doc_id)
            return sorted(visited)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> GraphStats:
        """Aggregate statistics for the current graph."""
        with self._lock:
            total_nodes = len(self._nodes)
            total_edges = sum(len(v) for v in self._out.values())
            root_count = sum(
                1 for n in self._nodes if not self._in.get(n)
            )
            leaf_count = sum(
                1 for n in self._nodes if not self._out.get(n)
            )
            return GraphStats(
                total_nodes=total_nodes,
                total_edges=total_edges,
                root_count=root_count,
                leaf_count=leaf_count,
            )
