"""Cascade dependency graph for counterfactual corpus analysis."""
import re
from collections import deque
from dataclasses import dataclass, field


@dataclass
class CascadeGraph:
    """Graph of citation dependencies between docs."""
    edges: dict[str, list[str]] = field(default_factory=dict)  # {source: [cited_doc_ids]}
    _reverse: dict[str, list[str]] = field(default_factory=dict)  # {cited: [sources]}

    def add_citation(self, source_id: str, cited_id: str) -> None:
        """Record that source_id cites cited_id."""
        if source_id not in self.edges:
            self.edges[source_id] = []
        if cited_id not in self.edges[source_id]:
            self.edges[source_id].append(cited_id)

        if cited_id not in self._reverse:
            self._reverse[cited_id] = []
        if source_id not in self._reverse[cited_id]:
            self._reverse[cited_id].append(source_id)

    def citations_of(self, doc_id: str) -> list[str]:
        """Docs that doc_id cites."""
        return list(self.edges.get(doc_id, []))

    def cited_by(self, doc_id: str) -> list[str]:
        """Docs that cite doc_id (reverse lookup)."""
        return list(self._reverse.get(doc_id, []))

    def node_count(self) -> int:
        """Total unique nodes (sources + cited)."""
        all_nodes: set[str] = set()
        all_nodes.update(self.edges.keys())
        for cited_list in self.edges.values():
            all_nodes.update(cited_list)
        return len(all_nodes)

    def edge_count(self) -> int:
        """Total citation edges."""
        return sum(len(cited_list) for cited_list in self.edges.values())


def build_cascade_graph(docs: dict[str, str]) -> CascadeGraph:
    """Extract citation graph from docs.

    For each doc: find mentions of other doc_ids (keys) in content.
    Simple: if doc_id_key appears as substring in content → citation.
    Build bidirectional index.
    """
    graph = CascadeGraph()
    doc_ids = list(docs.keys())

    for source_id, content in docs.items():
        for cited_id in doc_ids:
            if cited_id == source_id:
                continue
            if cited_id in content:
                graph.add_citation(source_id, cited_id)

    return graph


def find_cascade(
    target_doc_id: str,
    graph: CascadeGraph,
    *,
    max_depth: int = 3,
) -> list[str]:
    """BFS from target: find all docs that would lose a source if target removed.
    Returns list of doc_ids (excluding target itself).
    """
    visited: set[str] = set()
    queue: deque[tuple[str, int]] = deque()

    # Start with docs that directly cite the target
    for direct_dependent in graph.cited_by(target_doc_id):
        if direct_dependent != target_doc_id:
            queue.append((direct_dependent, 1))

    result: list[str] = []

    while queue:
        doc_id, depth = queue.popleft()
        if doc_id in visited or doc_id == target_doc_id:
            continue
        visited.add(doc_id)
        result.append(doc_id)

        if depth < max_depth:
            for dependent in graph.cited_by(doc_id):
                if dependent not in visited and dependent != target_doc_id:
                    queue.append((dependent, depth + 1))

    return result
