"""Graph traversal and analysis algorithms.

Pure stdlib — uses collections.deque and heapq only.
"""
from __future__ import annotations

import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.graph_traversal.graph import Graph, NodeId


@dataclass
class TraversalResult:
    """Holds the output of a graph traversal."""

    visited: list[NodeId]
    """Nodes in the order they were first discovered."""

    distances: dict[NodeId, float]
    """Distance (hops or weighted) from the start node to each visited node."""

    predecessors: dict[NodeId, Optional[NodeId]]
    """Predecessor map: node -> node that discovered it (start node maps to None)."""


# ---------------------------------------------------------------------------
# BFS
# ---------------------------------------------------------------------------

def bfs(graph: Graph, start: NodeId) -> TraversalResult:
    """Breadth-first search from *start*.

    Distances are measured in hops (each edge counts as 1 regardless of weight).
    Only reachable nodes appear in the result.
    """
    if not graph.has_node(start):
        return TraversalResult(visited=[], distances={}, predecessors={})

    visited: list[NodeId] = []
    distances: dict[NodeId, float] = {start: 0.0}
    predecessors: dict[NodeId, Optional[NodeId]] = {start: None}

    queue: deque[NodeId] = deque([start])

    while queue:
        node = queue.popleft()
        visited.append(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1.0
                predecessors[neighbor] = node
                queue.append(neighbor)

    return TraversalResult(visited=visited, distances=distances, predecessors=predecessors)


# ---------------------------------------------------------------------------
# DFS (iterative)
# ---------------------------------------------------------------------------

def dfs(graph: Graph, start: NodeId) -> TraversalResult:
    """Depth-first search from *start* (iterative, using an explicit stack).

    Distances represent the discovery order index (0-based), not hop count.
    Only reachable nodes appear in the result.
    """
    if not graph.has_node(start):
        return TraversalResult(visited=[], distances={}, predecessors={})

    visited: list[NodeId] = []
    distances: dict[NodeId, float] = {}
    predecessors: dict[NodeId, Optional[NodeId]] = {start: None}
    seen: set[NodeId] = set()

    # Stack holds (node, parent)
    stack: list[tuple[NodeId, Optional[NodeId]]] = [(start, None)]

    while stack:
        node, parent = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        distances[node] = float(len(visited))
        predecessors[node] = parent
        visited.append(node)
        # Push neighbors in reverse order so that the first neighbor is
        # processed first (matches the natural adjacency order).
        for neighbor in reversed(graph.neighbors(node)):
            if neighbor not in seen:
                stack.append((neighbor, node))

    return TraversalResult(visited=visited, distances=distances, predecessors=predecessors)


# ---------------------------------------------------------------------------
# Dijkstra
# ---------------------------------------------------------------------------

def dijkstra(graph: Graph, start: NodeId) -> TraversalResult:
    """Dijkstra's shortest-path algorithm from *start*.

    Edge weights are used as-is.  Negative-weight edges are silently skipped
    (the algorithm only relaxes edges with non-negative weight contribution).

    Only reachable nodes appear in the result.
    """
    if not graph.has_node(start):
        return TraversalResult(visited=[], distances={}, predecessors={})

    INF = float("inf")
    distances: dict[NodeId, float] = {start: 0.0}
    predecessors: dict[NodeId, Optional[NodeId]] = {start: None}
    visited_set: set[NodeId] = set()
    visited_order: list[NodeId] = []

    # Min-heap: (distance, node)
    heap: list[tuple[float, NodeId]] = [(0.0, start)]

    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited_set:
            continue
        visited_set.add(node)
        visited_order.append(node)

        for neighbor in graph.neighbors(node):
            edge = graph._adj[node][neighbor]
            w = edge.weight
            # Skip negative weights — Dijkstra is undefined for them
            if w < 0:
                continue
            new_dist = dist + w
            if new_dist < distances.get(neighbor, INF):
                distances[neighbor] = new_dist
                predecessors[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))

    return TraversalResult(
        visited=visited_order,
        distances=distances,
        predecessors=predecessors,
    )


# ---------------------------------------------------------------------------
# Cycle detection
# ---------------------------------------------------------------------------

def has_cycle(graph: Graph) -> bool:
    """Return True if the graph contains at least one cycle.

    Works for both directed and undirected graphs.
    For directed graphs uses DFS with coloring (WHITE / GRAY / BLACK).
    For undirected graphs uses DFS tracking the parent node to avoid
    reporting the trivial back-edge to the immediate parent.
    Self-loops are always a cycle.
    """
    if graph.directed:
        return _has_cycle_directed(graph)
    return _has_cycle_undirected(graph)


def _has_cycle_directed(graph: Graph) -> bool:
    """DFS coloring for directed cycle detection."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[NodeId, int] = {n: WHITE for n in graph.nodes()}

    def _dfs(node: NodeId) -> bool:
        color[node] = GRAY
        for neighbor in graph.neighbors(node):
            if color[neighbor] == GRAY:
                return True  # back-edge → cycle
            if color[neighbor] == WHITE and _dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    for node in graph.nodes():
        if color[node] == WHITE:
            if _dfs(node):
                return True
    return False


def _has_cycle_undirected(graph: Graph) -> bool:
    """DFS parent-tracking for undirected cycle detection."""
    visited: set[NodeId] = set()

    def _dfs(node: NodeId, parent: Optional[NodeId]) -> bool:
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                if _dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # back-edge to non-parent → cycle
        return False

    for node in graph.nodes():
        if node not in visited:
            if _dfs(node, None):
                return True
    return False


# ---------------------------------------------------------------------------
# Topological sort (Kahn's algorithm)
# ---------------------------------------------------------------------------

def topological_sort(graph: Graph) -> list[NodeId]:
    """Return a topological ordering of a directed acyclic graph.

    Raises ValueError if the graph contains a cycle.
    The algorithm is Kahn's BFS-based approach.
    """
    # in-degree for each node
    in_deg: dict[NodeId, int] = {n: graph.in_degree(n) for n in graph.nodes()}

    queue: deque[NodeId] = deque(n for n, d in in_deg.items() if d == 0)
    order: list[NodeId] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.neighbors(node):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(graph.nodes()):
        raise ValueError("Graph contains a cycle; topological sort is not possible.")

    return order


# ---------------------------------------------------------------------------
# Connected components (treats graph as undirected)
# ---------------------------------------------------------------------------

def connected_components(graph: Graph) -> list[list[NodeId]]:
    """Return all connected components as lists of node ids.

    The graph is treated as undirected for this purpose: both the forward
    adjacency and the reverse adjacency (in-edges) are explored.
    """
    all_nodes = set(graph.nodes())
    visited: set[NodeId] = set()
    components: list[list[NodeId]] = []

    for start in all_nodes:
        if start in visited:
            continue
        # BFS treating as undirected
        component: list[NodeId] = []
        queue: deque[NodeId] = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            component.append(node)
            # Forward neighbors
            for nb in graph.neighbors(node):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
            # Reverse neighbors (incoming edges treated as undirected)
            for nb in graph._radj.get(node, set()):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        components.append(component)

    return components


# ---------------------------------------------------------------------------
# Shortest path reconstruction
# ---------------------------------------------------------------------------

def shortest_path(graph: Graph, start: NodeId, end: NodeId) -> list[NodeId]:
    """Return the shortest (minimum weight) path from *start* to *end*.

    Uses Dijkstra internally.  Returns an empty list if no path exists or
    either node is not in the graph.
    """
    if not graph.has_node(start) or not graph.has_node(end):
        return []

    result = dijkstra(graph, start)
    if end not in result.distances:
        return []

    # Reconstruct path by following predecessors from end back to start
    path: list[NodeId] = []
    current: Optional[NodeId] = end
    while current is not None:
        path.append(current)
        current = result.predecessors.get(current)

    path.reverse()

    # Sanity check: make sure path actually starts at start
    if not path or path[0] != start:
        return []

    return path
