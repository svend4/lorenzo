"""E429 DocDependencyResolver — thread-safe document dependency resolution.

Provides :class:`DocDependencyResolver`, a graph of documents linked by
``depends_on`` (or other named) edges, with utilities to compute topological
order (Kahn's BFS), detect cycles (DFS), and enumerate dependents/dependencies.

Pure stdlib, no third-party dependencies. All mutating and reading operations
are protected by a :class:`threading.Lock` to make the resolver safe for use
from multiple threads.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Dependency:
    """A single dependency edge: ``from_doc`` depends on ``to_doc``."""

    from_doc: str
    to_doc: str
    kind: str = "depends_on"


@dataclass
class ResolutionResult:
    """Outcome of a topological resolution attempt."""

    order: list[str] = field(default_factory=list)
    has_cycle: bool = False
    cycle_nodes: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)


@dataclass
class ResolverStats:
    """Aggregate statistics for a :class:`DocDependencyResolver`."""

    total_nodes: int
    total_dependencies: int
    resolutions_performed: int
    cycles_detected: int


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------


class DocDependencyResolver:
    """Thread-safe graph of documents with ``depends_on``-style edges.

    Internal representation:
      * ``_deps[from_doc]``    — set of docs that ``from_doc`` depends on.
      * ``_reverse[to_doc]``   — set of docs that depend on ``to_doc``.
      * ``_nodes``             — set of known doc ids (sources and targets).

    Both directions are maintained eagerly so that
    :meth:`dependencies_of` / :meth:`dependents_of` are O(deg + log deg).
    """

    def __init__(self) -> None:
        self._deps: dict[str, set[str]] = {}
        self._reverse: dict[str, set[str]] = {}
        self._nodes: set[str] = set()
        self._resolutions: int = 0
        self._cycles: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_node(self, doc_id: str) -> bool:
        """Add a bare node (no edges). Return ``True`` if newly added."""
        with self._lock:
            if doc_id in self._nodes:
                return False
            self._nodes.add(doc_id)
            self._deps.setdefault(doc_id, set())
            self._reverse.setdefault(doc_id, set())
            return True

    def add_dependency(self, dep: Dependency) -> bool:
        """Record that ``dep.from_doc`` depends on ``dep.to_doc``.

        Returns ``True`` if this edge was newly added, ``False`` if it already
        existed.  The two endpoints are auto-registered as nodes.
        """
        with self._lock:
            self._nodes.add(dep.from_doc)
            self._nodes.add(dep.to_doc)
            self._deps.setdefault(dep.from_doc, set())
            self._deps.setdefault(dep.to_doc, set())
            self._reverse.setdefault(dep.from_doc, set())
            self._reverse.setdefault(dep.to_doc, set())

            if dep.to_doc in self._deps[dep.from_doc]:
                return False
            self._deps[dep.from_doc].add(dep.to_doc)
            self._reverse[dep.to_doc].add(dep.from_doc)
            return True

    def remove_dependency(self, from_doc: str, to_doc: str) -> bool:
        """Remove the edge ``from_doc -> to_doc``. Return ``True`` if removed."""
        with self._lock:
            deps = self._deps.get(from_doc)
            if not deps or to_doc not in deps:
                return False
            deps.discard(to_doc)
            rev = self._reverse.get(to_doc)
            if rev is not None:
                rev.discard(from_doc)
            return True

    def remove_node(self, doc_id: str) -> bool:
        """Remove ``doc_id`` and every edge incident to it.

        Returns ``True`` if the node existed and was removed.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return False

            # Remove outgoing edges (doc_id depends on X).
            for target in self._deps.get(doc_id, set()):
                rev = self._reverse.get(target)
                if rev is not None:
                    rev.discard(doc_id)
            self._deps.pop(doc_id, None)

            # Remove incoming edges (X depends on doc_id).
            for src in self._reverse.get(doc_id, set()):
                outgoing = self._deps.get(src)
                if outgoing is not None:
                    outgoing.discard(doc_id)
            self._reverse.pop(doc_id, None)

            self._nodes.discard(doc_id)
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def dependencies_of(self, doc_id: str) -> list[str]:
        """Return direct dependencies of ``doc_id`` (sorted)."""
        with self._lock:
            return sorted(self._deps.get(doc_id, set()))

    def dependents_of(self, doc_id: str) -> list[str]:
        """Return direct dependents of ``doc_id`` (sorted)."""
        with self._lock:
            return sorted(self._reverse.get(doc_id, set()))

    def all_nodes(self) -> list[str]:
        """Return every registered node id (sorted)."""
        with self._lock:
            return sorted(self._nodes)

    def stats(self) -> ResolverStats:
        """Return aggregate stats (snapshot)."""
        with self._lock:
            total_edges = sum(len(targets) for targets in self._deps.values())
            return ResolverStats(
                total_nodes=len(self._nodes),
                total_dependencies=total_edges,
                resolutions_performed=self._resolutions,
                cycles_detected=self._cycles,
            )

    # ------------------------------------------------------------------
    # Cycle utilities
    # ------------------------------------------------------------------

    def has_cycle(self) -> bool:
        """Return ``True`` iff the graph contains at least one cycle."""
        with self._lock:
            return self._has_cycle_locked(self._nodes)

    def _has_cycle_locked(self, nodes: set[str]) -> bool:
        """Iterative DFS cycle detection. Caller must hold ``self._lock``."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {n: WHITE for n in nodes}

        for start in nodes:
            if color[start] != WHITE:
                continue
            stack: list[tuple[str, list[str]]] = [
                (start, sorted(self._deps.get(start, set()) & nodes))
            ]
            color[start] = GRAY
            while stack:
                node, remaining = stack[-1]
                if not remaining:
                    color[node] = BLACK
                    stack.pop()
                    continue
                nxt = remaining.pop()
                state = color.get(nxt, WHITE)
                if state == GRAY:
                    return True
                if state == WHITE:
                    color[nxt] = GRAY
                    stack.append(
                        (nxt, sorted(self._deps.get(nxt, set()) & nodes))
                    )
        return False

    def find_cycles(self) -> list[list[str]]:
        """Return all simple cycles in the graph as ordered node lists.

        Uses an iterative variant of Johnson's-style DFS (without the blocking
        optimisation): for every start node, walk forward and record any back
        edge that closes a cycle.  Cycles are de-duplicated by their canonical
        (lexicographically minimal) rotation.
        """
        with self._lock:
            return self._find_cycles_locked(self._nodes)

    def _find_cycles_locked(self, nodes: set[str]) -> list[list[str]]:
        seen: set[tuple[str, ...]] = set()
        results: list[list[str]] = []

        for start in sorted(nodes):
            # DFS from ``start``; only follow nodes >= start (lex order) so
            # each cycle is enumerated from its smallest element exactly once.
            path: list[str] = [start]
            in_path: set[str] = {start}
            iterators: list[list[str]] = [
                sorted(
                    n for n in self._deps.get(start, set())
                    if n >= start and n in nodes
                )
            ]

            while iterators:
                if not iterators[-1]:
                    iterators.pop()
                    finished = path.pop()
                    in_path.discard(finished)
                    continue
                nxt = iterators[-1].pop()
                if nxt == start and len(path) >= 1:
                    # Closed a cycle back to start.
                    cycle = list(path)
                    canon = tuple(cycle)
                    if canon not in seen:
                        seen.add(canon)
                        results.append(cycle)
                    continue
                if nxt in in_path:
                    # Back edge to a non-start in-progress node — skipped here
                    # because the cycle will also surface when DFS starts at
                    # that smaller node (we restrict to nxt >= start anyway).
                    continue
                path.append(nxt)
                in_path.add(nxt)
                iterators.append(
                    sorted(
                        n for n in self._deps.get(nxt, set())
                        if n >= start and n in nodes
                    )
                )

        return results

    # ------------------------------------------------------------------
    # Resolution (Kahn's BFS)
    # ------------------------------------------------------------------

    def resolve(self) -> ResolutionResult:
        """Return a topological order of all nodes.

        Order convention: dependencies come *before* the docs that depend on
        them.  If the graph contains a cycle, :attr:`ResolutionResult.has_cycle`
        is ``True``, :attr:`cycle_nodes` lists the nodes participating in any
        cycle, and :attr:`unresolved` lists the same set sorted.
        """
        with self._lock:
            result = self._resolve_locked(self._nodes)
            self._resolutions += 1
            if result.has_cycle:
                self._cycles += 1
            return result

    def resolve_subset(self, roots: list[str]) -> ResolutionResult:
        """Resolve only the sub-graph reachable from ``roots`` (forward).

        Reachability follows the ``depends_on`` direction, so the result
        contains every transitive dependency of every root, plus the roots
        themselves (provided they're registered).
        """
        with self._lock:
            reachable: set[str] = set()
            queue: deque[str] = deque()
            for r in roots:
                if r in self._nodes and r not in reachable:
                    reachable.add(r)
                    queue.append(r)
            while queue:
                cur = queue.popleft()
                for dep in self._deps.get(cur, set()):
                    if dep in self._nodes and dep not in reachable:
                        reachable.add(dep)
                        queue.append(dep)

            result = self._resolve_locked(reachable)
            self._resolutions += 1
            if result.has_cycle:
                self._cycles += 1
            return result

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _resolve_locked(self, nodes: set[str]) -> ResolutionResult:
        """Kahn's BFS topological sort, restricted to ``nodes``.

        Caller must hold ``self._lock``.  Within a layer, nodes are emitted
        in lexicographic order to keep results deterministic.
        """
        if not nodes:
            return ResolutionResult()

        # Build in-degree map restricted to ``nodes``.
        in_degree: dict[str, int] = {n: 0 for n in nodes}
        for n in nodes:
            for target in self._deps.get(n, set()):
                if target in in_degree:
                    # ``n`` depends on ``target``; in Kahn's algorithm we want
                    # dependencies emitted first, so the *dependent* (``n``)
                    # has its in-degree incremented.
                    in_degree[n] += 1

        # Min-heap-style: use a sorted list as the queue to keep determinism
        # without importing heapq (still O(N log N) total work).
        ready: list[str] = sorted(name for name, deg in in_degree.items() if deg == 0)
        order: list[str] = []

        # Adjacency for "what becomes ready when X is emitted": reverse edges
        # restricted to nodes.
        outgoing: dict[str, list[str]] = {n: [] for n in nodes}
        for n in nodes:
            for target in self._deps.get(n, set()):
                if target in outgoing:
                    outgoing[target].append(n)

        while ready:
            # Pop smallest for determinism.
            current = ready.pop(0)
            order.append(current)
            new_ready: list[str] = []
            for dependent in outgoing.get(current, ()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    new_ready.append(dependent)
            if new_ready:
                # Merge into ``ready`` preserving sort.
                ready.extend(new_ready)
                ready.sort()

        if len(order) == len(nodes):
            return ResolutionResult(order=order)

        # Cycle: any node with remaining in-degree > 0 belongs to or feeds a
        # cycle.  Expose them as ``cycle_nodes`` (and ``unresolved``).
        cyclic = sorted(name for name, deg in in_degree.items() if deg > 0)
        return ResolutionResult(
            order=order,
            has_cycle=True,
            cycle_nodes=cyclic,
            unresolved=list(cyclic),
        )
