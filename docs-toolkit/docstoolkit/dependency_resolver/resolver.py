"""Topological sort / dependency resolver for named items."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


class CyclicDependencyError(Exception):
    """Raised when a dependency cycle is detected."""

    def __init__(self, cycle: list[str]) -> None:
        self.cycle = cycle
        path = " -> ".join(cycle)
        super().__init__(f"Dependency cycle detected: {path}")


@dataclass
class DependencyNode:
    """A named node with a list of dependency names."""

    name: str
    deps: list[str] = field(default_factory=list)


class DependencyResolver:
    """Resolve a graph of named nodes with declared dependencies.

    Uses Kahn's algorithm (BFS) for topological sorting; cycles are detected
    as nodes left over with in-degree > 0 after the BFS is exhausted.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, DependencyNode] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def add(self, node: DependencyNode) -> None:
        """Register a node.  Duplicate names overwrite the previous entry."""
        self._nodes[node.name] = node

    def add_many(self, nodes: list[DependencyNode]) -> None:
        """Register multiple nodes at once."""
        for node in nodes:
            self.add(node)

    # ------------------------------------------------------------------
    # Management
    # ------------------------------------------------------------------

    def remove(self, name: str) -> bool:
        """Remove a node by name.  Returns True if the node was found."""
        if name in self._nodes:
            del self._nodes[name]
            return True
        return False

    def clear(self) -> None:
        """Remove all nodes."""
        self._nodes.clear()

    def node_count(self) -> int:
        """Return the number of registered nodes."""
        return len(self._nodes)

    # ------------------------------------------------------------------
    # Core resolution (Kahn's BFS)
    # ------------------------------------------------------------------

    def _kahn(self, nodes: dict[str, DependencyNode]) -> list[str]:
        """Return a topological order for *nodes* using Kahn's algorithm.

        Raises:
            ValueError: if a dep name references a node not in *nodes*.
            CyclicDependencyError: if the graph contains a cycle.
        """
        # Validate all dependency references first.
        for node in nodes.values():
            for dep in node.deps:
                if dep not in nodes:
                    raise ValueError(
                        f"Node '{node.name}' depends on unknown node '{dep}'"
                    )

        # Build in-degree map and adjacency list (dep -> list of dependents).
        in_degree: dict[str, int] = {name: 0 for name in nodes}
        dependents: dict[str, list[str]] = {name: [] for name in nodes}

        for node in nodes.values():
            for dep in node.deps:
                in_degree[node.name] += 1
                dependents[dep].append(node.name)

        # Seed queue with all nodes that have no dependencies.
        queue: deque[str] = deque(
            name for name, deg in in_degree.items() if deg == 0
        )
        order: list[str] = []

        while queue:
            name = queue.popleft()
            order.append(name)
            for dependent in dependents[name]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(nodes):
            # Some nodes were never processed → cycle exists.
            cycle = self._find_cycle(nodes)
            raise CyclicDependencyError(cycle)

        return order

    @staticmethod
    def _find_cycle(nodes: dict[str, DependencyNode]) -> list[str]:
        """Return one cycle path using iterative DFS (approximate)."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {name: WHITE for name in nodes}
        parent: dict[str, str | None] = {name: None for name in nodes}
        cycle_path: list[str] = []

        def dfs(start: str) -> bool:
            stack: list[tuple[str, int]] = [(start, 0)]  # (node, dep_index)
            path_stack: list[str] = []

            while stack:
                name, idx = stack[-1]

                if idx == 0:
                    # First visit
                    color[name] = GRAY
                    path_stack.append(name)

                deps = nodes[name].deps
                if idx < len(deps):
                    stack[-1] = (name, idx + 1)
                    dep = deps[idx]
                    if color[dep] == GRAY:
                        # Found back edge — reconstruct cycle from path_stack
                        cycle_start = dep
                        i = len(path_stack) - 1
                        while path_stack[i] != cycle_start:
                            i -= 1
                        nonlocal cycle_path
                        cycle_path = path_stack[i:] + [cycle_start]
                        return True
                    if color[dep] == WHITE:
                        parent[dep] = name
                        stack.append((dep, 0))
                else:
                    # All deps processed
                    color[name] = BLACK
                    path_stack.pop()
                    stack.pop()

            return False

        for name in nodes:
            if color[name] == WHITE:
                if dfs(name):
                    return cycle_path

        return []

    # ------------------------------------------------------------------
    # Public resolution API
    # ------------------------------------------------------------------

    def resolve(self) -> list[str]:
        """Return all nodes in topological order (dependencies before dependents).

        Raises:
            CyclicDependencyError: if the graph contains a cycle.
            ValueError: if any dependency references an unknown node.
        """
        return self._kahn(self._nodes)

    def resolve_for(self, name: str) -> list[str]:
        """Return topological order for *name* and its transitive dependencies only.

        The returned list ends with *name*; all transitive deps appear before it.

        Raises:
            KeyError: if *name* is not a registered node.
            CyclicDependencyError: if the subgraph contains a cycle.
            ValueError: if any dependency references an unknown node.
        """
        if name not in self._nodes:
            raise KeyError(f"Node '{name}' is not registered")

        # Collect *name* and all transitive deps via BFS.
        reachable: set[str] = set()
        queue: deque[str] = deque([name])
        while queue:
            current = queue.popleft()
            if current in reachable:
                continue
            reachable.add(current)
            node = self._nodes.get(current)
            if node is None:
                # Unknown dep — let _kahn raise the proper ValueError.
                continue
            for dep in node.deps:
                if dep not in reachable:
                    queue.append(dep)

        subgraph = {n: self._nodes[n] for n in reachable if n in self._nodes}
        return self._kahn(subgraph)

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    def has_cycle(self) -> bool:
        """Return True if the current graph contains a cycle."""
        try:
            self._kahn(self._nodes)
            return False
        except CyclicDependencyError:
            return True

    def dependencies_of(self, name: str) -> set[str]:
        """Return the set of all transitive dependencies of *name*.

        Does not include *name* itself.

        Raises:
            KeyError: if *name* is not a registered node.
        """
        if name not in self._nodes:
            raise KeyError(f"Node '{name}' is not registered")

        visited: set[str] = set()
        queue: deque[str] = deque(self._nodes[name].deps)
        while queue:
            dep = queue.popleft()
            if dep in visited:
                continue
            visited.add(dep)
            node = self._nodes.get(dep)
            if node is not None:
                for d in node.deps:
                    if d not in visited:
                        queue.append(d)
        return visited

    def dependents_of(self, name: str) -> set[str]:
        """Return the set of all nodes that directly or transitively depend on *name*.

        Does not include *name* itself.

        Raises:
            KeyError: if *name* is not a registered node.
        """
        if name not in self._nodes:
            raise KeyError(f"Node '{name}' is not registered")

        # Build reverse adjacency: dep -> list of nodes that list dep.
        reverse: dict[str, list[str]] = {n: [] for n in self._nodes}
        for node in self._nodes.values():
            for dep in node.deps:
                if dep in reverse:
                    reverse[dep].append(node.name)

        visited: set[str] = set()
        queue: deque[str] = deque(reverse.get(name, []))
        while queue:
            dependent = queue.popleft()
            if dependent in visited:
                continue
            visited.add(dependent)
            for further in reverse.get(dependent, []):
                if further not in visited:
                    queue.append(further)
        return visited
