"""Document dependency declaration and resolution.

Tracks typed relationships between documents (REQUIRES, RECOMMENDS,
RELATES_TO, CONFLICTS_WITH, REPLACES). Supports transitive resolution,
cycle detection, and topological build ordering on REQUIRES edges.
"""
from __future__ import annotations

import threading
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class DependencyType(Enum):
    """Types of dependencies between documents."""

    REQUIRES = "requires"
    RECOMMENDS = "recommends"
    RELATES_TO = "relates_to"
    CONFLICTS_WITH = "conflicts_with"
    REPLACES = "replaces"


@dataclass
class Dependency:
    """A single typed dependency edge from one doc to another."""

    source: str
    target: str
    dep_type: DependencyType = DependencyType.REQUIRES
    priority: int = 0
    notes: Optional[str] = None


@dataclass
class DependencyGraph:
    """Snapshot of the dependency graph for one or more docs."""

    docs: list[str]
    dependencies: list[Dependency]
    has_cycle: bool = False
    build_order: list[str] = field(default_factory=list)


@dataclass
class ResolveResult:
    """Result of resolving the REQUIRES chain to build a target doc."""

    target_doc_id: str
    chain: list[str]
    missing: list[str]
    conflicts: list[tuple[str, str]]


class DocDependency:
    """Document dependency manager with typed edges and cycle detection."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._docs: set[str] = set()
        # All edges: (source, target, dep_type) is unique key
        self._edges: dict[tuple[str, str, DependencyType], Dependency] = {}
        # Adjacency for fast lookup
        self._out: dict[str, list[Dependency]] = defaultdict(list)
        self._in: dict[str, list[Dependency]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Doc registration
    # ------------------------------------------------------------------
    def register_doc(self, doc_id: str) -> bool:
        """Ensure a doc is tracked. Returns True if newly added."""
        if not doc_id:
            return False
        with self._lock:
            if doc_id in self._docs:
                return False
            self._docs.add(doc_id)
            return True

    def unregister_doc(self, doc_id: str) -> bool:
        """Remove a doc and cascade-remove all related dependencies."""
        with self._lock:
            if doc_id not in self._docs:
                return False
            # Drop all edges touching this doc
            keys_to_drop = [
                key
                for key in self._edges
                if key[0] == doc_id or key[1] == doc_id
            ]
            for key in keys_to_drop:
                dep = self._edges.pop(key)
                self._out[dep.source] = [
                    d for d in self._out[dep.source] if d is not dep
                ]
                self._in[dep.target] = [
                    d for d in self._in[dep.target] if d is not dep
                ]
                if not self._out[dep.source]:
                    self._out.pop(dep.source, None)
                if not self._in[dep.target]:
                    self._in.pop(dep.target, None)
            self._docs.discard(doc_id)
            return True

    # ------------------------------------------------------------------
    # Dependency edges
    # ------------------------------------------------------------------
    def add_dependency(
        self,
        source: str,
        target: str,
        dep_type: DependencyType = DependencyType.REQUIRES,
        priority: int = 0,
        notes: Optional[str] = None,
    ) -> Optional[Dependency]:
        """Register a typed dependency edge. Returns the Dependency or None."""
        if not source or not target:
            return None
        if source == target:
            return None
        with self._lock:
            self._docs.add(source)
            self._docs.add(target)
            key = (source, target, dep_type)
            if key in self._edges:
                return None
            dep = Dependency(
                source=source,
                target=target,
                dep_type=dep_type,
                priority=priority,
                notes=notes,
            )
            self._edges[key] = dep
            self._out[source].append(dep)
            self._in[target].append(dep)
            return dep

    def remove_dependency(
        self,
        source: str,
        target: str,
        dep_type: Optional[DependencyType] = None,
    ) -> bool:
        """Remove one or all dep_type edges from source to target."""
        with self._lock:
            if dep_type is not None:
                key = (source, target, dep_type)
                dep = self._edges.pop(key, None)
                if dep is None:
                    return False
                self._out[source] = [d for d in self._out[source] if d is not dep]
                self._in[target] = [d for d in self._in[target] if d is not dep]
                if not self._out[source]:
                    self._out.pop(source, None)
                if not self._in[target]:
                    self._in.pop(target, None)
                return True
            # Remove all dep_types between source and target
            keys = [k for k in self._edges if k[0] == source and k[1] == target]
            if not keys:
                return False
            for key in keys:
                dep = self._edges.pop(key)
                self._out[source] = [d for d in self._out[source] if d is not dep]
                self._in[target] = [d for d in self._in[target] if d is not dep]
                if not self._out[source]:
                    self._out.pop(source, None)
                if not self._in[target]:
                    self._in.pop(target, None)
            return True

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------
    def dependencies_of(
        self,
        doc_id: str,
        dep_type: Optional[DependencyType] = None,
    ) -> list[Dependency]:
        """Outgoing edges from doc_id (optionally filtered by dep_type)."""
        with self._lock:
            deps = list(self._out.get(doc_id, []))
        if dep_type is not None:
            deps = [d for d in deps if d.dep_type == dep_type]
        return deps

    def dependents_of(
        self,
        doc_id: str,
        dep_type: Optional[DependencyType] = None,
    ) -> list[Dependency]:
        """Incoming edges to doc_id (optionally filtered by dep_type)."""
        with self._lock:
            deps = list(self._in.get(doc_id, []))
        if dep_type is not None:
            deps = [d for d in deps if d.dep_type == dep_type]
        return deps

    # ------------------------------------------------------------------
    # Transitive helpers (REQUIRES)
    # ------------------------------------------------------------------
    def requires(self, doc_id: str) -> list[str]:
        """Transitive REQUIRES targets reachable from doc_id."""
        return self._transitive(doc_id, DependencyType.REQUIRES, forward=True)

    def required_by(self, doc_id: str) -> list[str]:
        """Transitive REQUIRES sources that reach doc_id."""
        return self._transitive(doc_id, DependencyType.REQUIRES, forward=False)

    def _transitive(
        self,
        doc_id: str,
        dep_type: DependencyType,
        forward: bool,
    ) -> list[str]:
        with self._lock:
            visited: set[str] = set()
            order: list[str] = []
            queue: deque[str] = deque([doc_id])
            while queue:
                current = queue.popleft()
                edges = (
                    self._out.get(current, [])
                    if forward
                    else self._in.get(current, [])
                )
                for edge in edges:
                    if edge.dep_type != dep_type:
                        continue
                    neighbor = edge.target if forward else edge.source
                    if neighbor in visited or neighbor == doc_id:
                        continue
                    visited.add(neighbor)
                    order.append(neighbor)
                    queue.append(neighbor)
        return order

    def recommends(self, doc_id: str) -> list[str]:
        """Direct RECOMMENDS targets from doc_id."""
        return [d.target for d in self.dependencies_of(doc_id, DependencyType.RECOMMENDS)]

    def related(self, doc_id: str) -> list[str]:
        """Direct RELATES_TO neighbours (treated as undirected)."""
        out_targets = {
            d.target
            for d in self.dependencies_of(doc_id, DependencyType.RELATES_TO)
        }
        in_sources = {
            d.source
            for d in self.dependents_of(doc_id, DependencyType.RELATES_TO)
        }
        out_targets.update(in_sources)
        out_targets.discard(doc_id)
        return sorted(out_targets)

    def conflicts_with(self, doc_id: str) -> list[str]:
        """Direct CONFLICTS_WITH neighbours (undirected)."""
        out_targets = {
            d.target
            for d in self.dependencies_of(doc_id, DependencyType.CONFLICTS_WITH)
        }
        in_sources = {
            d.source
            for d in self.dependents_of(doc_id, DependencyType.CONFLICTS_WITH)
        }
        out_targets.update(in_sources)
        out_targets.discard(doc_id)
        return sorted(out_targets)

    # ------------------------------------------------------------------
    # Resolve / build order
    # ------------------------------------------------------------------
    def resolve(self, target_doc_id: str) -> ResolveResult:
        """Resolve the REQUIRES chain to build target_doc_id.

        chain: deepest-first ordering of dependencies the target needs.
        missing: docs referenced by edges but not registered.
        conflicts: pairs (a, b) where two docs in the chain conflict.
        """
        with self._lock:
            chain: list[str] = []
            visited: set[str] = set()
            missing: list[str] = []

            # BFS through REQUIRES edges
            queue: deque[str] = deque([target_doc_id])
            seen_for_missing: set[str] = set()
            while queue:
                current = queue.popleft()
                for edge in self._out.get(current, []):
                    if edge.dep_type != DependencyType.REQUIRES:
                        continue
                    nxt = edge.target
                    if nxt in visited:
                        continue
                    visited.add(nxt)
                    queue.append(nxt)
                    if nxt not in self._docs and nxt not in seen_for_missing:
                        missing.append(nxt)
                        seen_for_missing.add(nxt)

            # Build deepest-first order using topo-style DFS on REQUIRES
            colors: dict[str, int] = {}  # 0=unvisited, 1=visiting, 2=done

            def dfs(node: str) -> None:
                if colors.get(node, 0) == 2:
                    return
                if colors.get(node, 0) == 1:
                    return  # cycle, skip
                colors[node] = 1
                for edge in self._out.get(node, []):
                    if edge.dep_type != DependencyType.REQUIRES:
                        continue
                    dfs(edge.target)
                colors[node] = 2
                if node != target_doc_id:
                    chain.append(node)

            dfs(target_doc_id)

            # Compute conflicts among target + chain
            participants = set(chain)
            participants.add(target_doc_id)
            conflicts_set: set[tuple[str, str]] = set()
            for node in participants:
                for edge in self._out.get(node, []):
                    if edge.dep_type != DependencyType.CONFLICTS_WITH:
                        continue
                    if edge.target in participants:
                        pair = tuple(sorted((edge.source, edge.target)))
                        conflicts_set.add(pair)
            conflicts = sorted(conflicts_set)

        return ResolveResult(
            target_doc_id=target_doc_id,
            chain=chain,
            missing=missing,
            conflicts=conflicts,
        )

    def build_order(self, doc_ids: Optional[list[str]] = None) -> list[str]:
        """Topological sort over REQUIRES edges. Raises ValueError on cycle."""
        with self._lock:
            if doc_ids is None:
                nodes = set(self._docs)
                # Also include endpoints of REQUIRES edges
                for key in self._edges:
                    if key[2] == DependencyType.REQUIRES:
                        nodes.add(key[0])
                        nodes.add(key[1])
            else:
                nodes = set(doc_ids)

            # Build subgraph induced on `nodes` over REQUIRES edges
            in_degree: dict[str, int] = {n: 0 for n in nodes}
            adj: dict[str, list[str]] = {n: [] for n in nodes}
            for key in self._edges:
                src, tgt, dtype = key
                if dtype != DependencyType.REQUIRES:
                    continue
                if src in nodes and tgt in nodes:
                    adj[src].append(tgt)
                    in_degree[tgt] += 1

            # Kahn's algorithm. We want dependencies before dependents:
            # source REQUIRES target => target must come first.
            # In the adjacency above, edge src->tgt; in topo sort by in_degree==0,
            # roots are those with no incoming = no one REQUIRES them.
            # We need the reverse: produce targets (leaves) first.
            # So perform Kahn on reverse adjacency.
            rev_in: dict[str, int] = {n: 0 for n in nodes}
            rev_adj: dict[str, list[str]] = {n: [] for n in nodes}
            for src, targets in adj.items():
                for tgt in targets:
                    rev_adj[tgt].append(src)
                    rev_in[src] += 1

            queue: deque[str] = deque(
                sorted(n for n in nodes if rev_in[n] == 0)
            )
            order: list[str] = []
            while queue:
                node = queue.popleft()
                order.append(node)
                # Stable: sort neighbours
                for nb in sorted(rev_adj[node]):
                    rev_in[nb] -= 1
                    if rev_in[nb] == 0:
                        queue.append(nb)

            if len(order) != len(nodes):
                raise ValueError("Cycle detected in REQUIRES edges")
            return order

    def has_cycle(
        self,
        dep_type: DependencyType = DependencyType.REQUIRES,
    ) -> bool:
        """Return True if dep_type subgraph contains any cycle."""
        return bool(self.find_cycles(dep_type))

    def find_cycles(
        self,
        dep_type: DependencyType = DependencyType.REQUIRES,
    ) -> list[list[str]]:
        """Find all simple cycles in the dep_type subgraph (DFS based)."""
        with self._lock:
            # Build adjacency
            adj: dict[str, list[str]] = defaultdict(list)
            nodes: set[str] = set()
            for key in self._edges:
                src, tgt, dtype = key
                if dtype != dep_type:
                    continue
                adj[src].append(tgt)
                nodes.add(src)
                nodes.add(tgt)

        cycles: list[list[str]] = []
        seen_signatures: set[tuple[str, ...]] = set()

        def normalize(cycle: list[str]) -> tuple[str, ...]:
            # Rotate so smallest element is first; preserves direction.
            if not cycle:
                return tuple(cycle)
            min_idx = min(range(len(cycle)), key=lambda i: cycle[i])
            rotated = cycle[min_idx:] + cycle[:min_idx]
            return tuple(rotated)

        color: dict[str, int] = {n: 0 for n in nodes}
        stack: list[str] = []
        on_stack: set[str] = set()

        def dfs(node: str) -> None:
            color[node] = 1
            stack.append(node)
            on_stack.add(node)
            for nb in adj.get(node, []):
                if color.get(nb, 0) == 0:
                    dfs(nb)
                elif nb in on_stack:
                    # Found cycle from nb to node
                    idx = stack.index(nb)
                    cycle = stack[idx:]
                    sig = normalize(cycle)
                    if sig not in seen_signatures:
                        seen_signatures.add(sig)
                        cycles.append(list(sig))
            stack.pop()
            on_stack.discard(node)
            color[node] = 2

        for n in sorted(nodes):
            if color.get(n, 0) == 0:
                dfs(n)

        return cycles

    def roots(
        self,
        dep_type: DependencyType = DependencyType.REQUIRES,
    ) -> list[str]:
        """Docs with no incoming edges of dep_type."""
        with self._lock:
            incoming: dict[str, int] = defaultdict(int)
            participants: set[str] = set()
            for key in self._edges:
                src, tgt, dtype = key
                if dtype != dep_type:
                    continue
                incoming[tgt] += 1
                participants.add(src)
                participants.add(tgt)
            # Include registered docs with no edges of this type at all? Yes.
            all_nodes = set(self._docs) | participants
            return sorted(n for n in all_nodes if incoming.get(n, 0) == 0)

    def leaves(
        self,
        dep_type: DependencyType = DependencyType.REQUIRES,
    ) -> list[str]:
        """Docs with no outgoing edges of dep_type."""
        with self._lock:
            outgoing: dict[str, int] = defaultdict(int)
            participants: set[str] = set()
            for key in self._edges:
                src, tgt, dtype = key
                if dtype != dep_type:
                    continue
                outgoing[src] += 1
                participants.add(src)
                participants.add(tgt)
            all_nodes = set(self._docs) | participants
            return sorted(n for n in all_nodes if outgoing.get(n, 0) == 0)

    # ------------------------------------------------------------------
    # Graph export
    # ------------------------------------------------------------------
    def graph(self, doc_ids: Optional[list[str]] = None) -> DependencyGraph:
        """Snapshot the graph (optionally restricted to doc_ids)."""
        with self._lock:
            if doc_ids is None:
                docs = sorted(self._docs)
                deps = list(self._edges.values())
            else:
                doc_set = set(doc_ids)
                docs = sorted(doc_set & self._docs)
                deps = [
                    d
                    for d in self._edges.values()
                    if d.source in doc_set and d.target in doc_set
                ]

        has_cycle = self.has_cycle(DependencyType.REQUIRES)
        try:
            order = self.build_order(docs if doc_ids is not None else None)
        except ValueError:
            order = []
        return DependencyGraph(
            docs=docs,
            dependencies=deps,
            has_cycle=has_cycle,
            build_order=order,
        )

    # ------------------------------------------------------------------
    # Stats / housekeeping
    # ------------------------------------------------------------------
    @property
    def doc_count(self) -> int:
        with self._lock:
            return len(self._docs)

    @property
    def dependency_count(self) -> int:
        with self._lock:
            return len(self._edges)

    def clear(self) -> None:
        with self._lock:
            self._docs.clear()
            self._edges.clear()
            self._out.clear()
            self._in.clear()
