"""Intent graph structure: edges and the graph container."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from docstoolkit.intent_graph.node import IntentNode, IntentNodeType


@dataclass
class IntentEdge:
    """A directed edge between two intent nodes.

    Attributes:
        source_id: ID of the source node.
        target_id: ID of the target node.
        relation: Semantic label for the relationship.
        weight: Edge weight (default 1.0).
    """

    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0


class IntentGraph:
    """A directed graph of intent nodes and edges."""

    def __init__(self) -> None:
        self._nodes: dict[str, IntentNode] = {}
        # adjacency: source_id -> list of edges
        self._edges_out: dict[str, list[IntentEdge]] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_node(self, node: IntentNode) -> None:
        """Add a node to the graph (idempotent by node_id)."""
        if node.node_id not in self._nodes:
            self._nodes[node.node_id] = node
            self._edges_out.setdefault(node.node_id, [])

    def add_edge(self, edge: IntentEdge) -> None:
        """Add a directed edge.  Source and target nodes must already exist."""
        self._edges_out.setdefault(edge.source_id, [])
        self._edges_out[edge.source_id].append(edge)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_node(self, node_id: str) -> IntentNode | None:
        """Return the node with *node_id*, or None if not present."""
        return self._nodes.get(node_id)

    def neighbors(self, node_id: str) -> list[IntentNode]:
        """Return all nodes connected by any edge in either direction."""
        result: dict[str, IntentNode] = {}

        # outgoing edges (source == node_id)
        for edge in self._edges_out.get(node_id, []):
            target = self._nodes.get(edge.target_id)
            if target is not None:
                result[target.node_id] = target

        # incoming edges (target == node_id)
        for src_id, edges in self._edges_out.items():
            if src_id == node_id:
                continue
            for edge in edges:
                if edge.target_id == node_id:
                    src_node = self._nodes.get(src_id)
                    if src_node is not None:
                        result[src_id] = src_node

        return list(result.values())

    def edges_from(self, node_id: str) -> list[IntentEdge]:
        """Return all edges whose source is *node_id*."""
        return list(self._edges_out.get(node_id, []))

    def nodes_by_type(self, node_type: IntentNodeType) -> list[IntentNode]:
        """Return all nodes of a given type."""
        return [n for n in self._nodes.values() if n.node_type == node_type]

    def node_count(self) -> int:
        """Total number of nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Total number of edges."""
        return sum(len(edges) for edges in self._edges_out.values())

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the graph."""
        nodes = [
            {
                "node_id": n.node_id,
                "node_type": n.node_type.value,
                "label": n.label,
                "weight": n.weight,
                "metadata": n.metadata,
            }
            for n in self._nodes.values()
        ]
        edges = [
            {
                "source_id": e.source_id,
                "target_id": e.target_id,
                "relation": e.relation,
                "weight": e.weight,
            }
            for edges_list in self._edges_out.values()
            for e in edges_list
        ]
        return {"nodes": nodes, "edges": edges}
