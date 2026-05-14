"""graph_traversal — pure-stdlib graph data structures and traversal algorithms.

E72 module for docs-toolkit.

Public API
----------
Graph, Edge, NodeId          — core data structures  (graph.py)
TraversalResult              — traversal output      (algorithms.py)
bfs, dfs, dijkstra           — traversal algorithms
has_cycle                    — cycle detection
topological_sort             — Kahn's algorithm (DAG only)
connected_components         — undirected component labelling
shortest_path                — Dijkstra-based path reconstruction
"""

from docstoolkit.graph_traversal.graph import (
    NodeId,
    Edge,
    Graph,
)
from docstoolkit.graph_traversal.algorithms import (
    TraversalResult,
    bfs,
    dfs,
    dijkstra,
    has_cycle,
    topological_sort,
    connected_components,
    shortest_path,
)

__all__ = [
    # graph.py
    "NodeId",
    "Edge",
    "Graph",
    # algorithms.py
    "TraversalResult",
    "bfs",
    "dfs",
    "dijkstra",
    "has_cycle",
    "topological_sort",
    "connected_components",
    "shortest_path",
]
