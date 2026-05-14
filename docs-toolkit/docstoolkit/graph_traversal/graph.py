"""Core graph data structure for graph_traversal module.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

NodeId = str


@dataclass
class Edge:
    source: NodeId
    target: NodeId
    weight: float = 1.0
    label: str = ""


class Graph:
    """General-purpose directed or undirected weighted graph.

    Internally stores:
      * _nodes: dict[NodeId, dict[str, Any]]   — node attribute store
      * _adj:   dict[NodeId, dict[NodeId, Edge]] — adjacency: source -> target -> Edge
      * _radj:  dict[NodeId, set[NodeId]]        — reverse adj (target -> sources) for
                                                   efficient in-degree and remove_node
    """

    def __init__(self, directed: bool = True) -> None:
        self.directed: bool = directed
        self._nodes: dict[NodeId, dict[str, Any]] = {}
        # _adj[source][target] = Edge
        self._adj: dict[NodeId, dict[NodeId, Edge]] = {}
        # _radj[target] = set of sources pointing to target
        self._radj: dict[NodeId, set[NodeId]] = {}

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------

    def add_node(self, node_id: NodeId, **attrs: Any) -> None:
        """Add a node with optional attributes.  If the node already exists,
        attributes are merged (new values overwrite existing ones)."""
        if node_id not in self._nodes:
            self._nodes[node_id] = {}
            self._adj[node_id] = {}
            self._radj[node_id] = set()
        self._nodes[node_id].update(attrs)

    def remove_node(self, node_id: NodeId) -> bool:
        """Remove a node and all incident edges.  Returns True if the node existed."""
        if node_id not in self._nodes:
            return False

        # Remove all outgoing edges from this node
        for target in list(self._adj[node_id].keys()):
            self._radj[target].discard(node_id)
        del self._adj[node_id]

        # Remove all incoming edges to this node
        for source in list(self._radj[node_id]):
            self._adj[source].pop(node_id, None)
        del self._radj[node_id]

        del self._nodes[node_id]
        return True

    def has_node(self, node_id: NodeId) -> bool:
        return node_id in self._nodes

    def nodes(self) -> list[NodeId]:
        return list(self._nodes.keys())

    def node_attrs(self, node_id: NodeId) -> dict[str, Any]:
        """Return a copy of node attributes.  Raises KeyError if node missing."""
        return dict(self._nodes[node_id])

    # ------------------------------------------------------------------
    # Edges
    # ------------------------------------------------------------------

    def add_edge(
        self,
        source: NodeId,
        target: NodeId,
        weight: float = 1.0,
        label: str = "",
    ) -> None:
        """Add an edge (source -> target).

        Auto-creates nodes if they don't exist.
        For undirected graphs the reverse edge (target -> source) is also stored
        with the same weight and label.
        """
        # Auto-add nodes
        if source not in self._nodes:
            self.add_node(source)
        if target not in self._nodes:
            self.add_node(target)

        edge = Edge(source=source, target=target, weight=weight, label=label)
        self._adj[source][target] = edge
        self._radj[target].add(source)

        if not self.directed and source != target:
            rev_edge = Edge(source=target, target=source, weight=weight, label=label)
            self._adj[target][source] = rev_edge
            self._radj[source].add(target)

    def remove_edge(self, source: NodeId, target: NodeId) -> bool:
        """Remove edge source->target.  Returns True if it existed.

        For undirected graphs the reverse edge is also removed.
        """
        if source not in self._adj or target not in self._adj[source]:
            return False
        del self._adj[source][target]
        self._radj[target].discard(source)

        if not self.directed and source != target:
            self._adj[target].pop(source, None)
            self._radj[source].discard(target)
        return True

    def has_edge(self, source: NodeId, target: NodeId) -> bool:
        return source in self._adj and target in self._adj[source]

    def edges(self) -> list[Edge]:
        """Return all edges in the graph.

        For undirected graphs each conceptual edge is stored twice internally
        (both directions); this method returns only the canonical set where
        source <= target to avoid duplicates — unless the graph is directed,
        in which case every stored edge is returned.
        """
        result: list[Edge] = []
        if self.directed:
            for targets in self._adj.values():
                result.extend(targets.values())
        else:
            seen: set[tuple[NodeId, NodeId]] = set()
            for src, targets in self._adj.items():
                for tgt, edge in targets.items():
                    key = (min(src, tgt), max(src, tgt))
                    if key not in seen:
                        seen.add(key)
                        result.append(edge)
        return result

    # ------------------------------------------------------------------
    # Neighbors and degrees
    # ------------------------------------------------------------------

    def neighbors(self, node_id: NodeId) -> list[NodeId]:
        """Return outgoing neighbors of *node_id*."""
        if node_id not in self._adj:
            return []
        return list(self._adj[node_id].keys())

    def out_degree(self, node_id: NodeId) -> int:
        if node_id not in self._adj:
            return 0
        return len(self._adj[node_id])

    def in_degree(self, node_id: NodeId) -> int:
        if node_id not in self._radj:
            return 0
        return len(self._radj[node_id])

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._nodes)

    def __repr__(self) -> str:  # pragma: no cover
        kind = "Directed" if self.directed else "Undirected"
        return f"<Graph {kind} nodes={len(self._nodes)} edges={len(self.edges())}>"
