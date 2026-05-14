"""SQLite-backed directed graph store with nodes and edges.

A lightweight in-memory or file-persisted knowledge graph.  Uses only
the Python standard library (``sqlite3``, ``json``, ``threading``).
"""
from __future__ import annotations

import json
import sqlite3
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Node:
    """A node in the graph."""

    node_id: str
    node_type: str
    properties: dict = field(default_factory=dict)
    created_at: float = 0.0


@dataclass
class Edge:
    """A directed edge between two nodes."""

    edge_id: int
    source: str
    target: str
    relation: str
    properties: dict = field(default_factory=dict)
    created_at: float = 0.0


@dataclass
class Path:
    """A path through the graph as a sequence of nodes and edges."""

    nodes: list
    edges: list

    @property
    def length(self) -> int:
        """The number of edges in the path."""
        return len(self.edges)


@dataclass
class GraphStats:
    """Aggregate statistics about a graph."""

    node_count: int
    edge_count: int
    node_types: dict
    relations: dict

    @property
    def avg_degree(self) -> float:
        """Average degree (2 * edges / nodes)."""
        if self.node_count == 0:
            return 0.0
        return (2.0 * self.edge_count) / self.node_count


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class GraphStore:
    """SQLite-backed directed graph store.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an
        in-memory database (default).
    """

    _CREATE_NODES = """
    CREATE TABLE IF NOT EXISTS nodes (
        node_id         TEXT PRIMARY KEY,
        node_type       TEXT NOT NULL,
        properties_json TEXT NOT NULL,
        created_at      REAL NOT NULL
    )
    """

    _CREATE_EDGES = """
    CREATE TABLE IF NOT EXISTS edges (
        edge_id         INTEGER PRIMARY KEY AUTOINCREMENT,
        source          TEXT NOT NULL,
        target          TEXT NOT NULL,
        relation        TEXT NOT NULL,
        properties_json TEXT NOT NULL,
        created_at      REAL NOT NULL
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes (node_type)",
        "CREATE INDEX IF NOT EXISTS idx_edges_source ON edges (source)",
        "CREATE INDEX IF NOT EXISTS idx_edges_target ON edges (target)",
        "CREATE INDEX IF NOT EXISTS idx_edges_relation ON edges (relation)",
    ]

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(self._CREATE_NODES)
        self._conn.execute(self._CREATE_EDGES)
        for stmt in self._CREATE_INDEXES:
            self._conn.execute(stmt)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Row converters
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_node(row: tuple) -> Node:
        node_id, node_type, props_json, created_at = row
        return Node(
            node_id=node_id,
            node_type=node_type,
            properties=json.loads(props_json) if props_json else {},
            created_at=created_at,
        )

    @staticmethod
    def _row_to_edge(row: tuple) -> Edge:
        edge_id, source, target, relation, props_json, created_at = row
        return Edge(
            edge_id=edge_id,
            source=source,
            target=target,
            relation=relation,
            properties=json.loads(props_json) if props_json else {},
            created_at=created_at,
        )

    # ------------------------------------------------------------------
    # Node operations
    # ------------------------------------------------------------------

    def add_node(
        self,
        node_id: str,
        node_type: str,
        properties: Optional[dict] = None,
        now: float = 0.0,
    ) -> Node:
        """Insert or update a node, returning the stored :class:`Node`."""
        props = properties if properties is not None else {}
        props_json = json.dumps(props, ensure_ascii=False, sort_keys=True)
        with self._lock:
            self._conn.execute(
                "INSERT INTO nodes "
                "(node_id, node_type, properties_json, created_at) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(node_id) DO UPDATE SET "
                "node_type = excluded.node_type, "
                "properties_json = excluded.properties_json, "
                "created_at = excluded.created_at",
                (node_id, node_type, props_json, now),
            )
            self._conn.commit()
        return Node(
            node_id=node_id,
            node_type=node_type,
            properties=dict(props),
            created_at=now,
        )

    def get_node(self, node_id: str) -> Optional[Node]:
        """Return a node by id, or ``None``."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT node_id, node_type, properties_json, created_at "
                "FROM nodes WHERE node_id = ?",
                (node_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_node(row)

    def remove_node(self, node_id: str) -> bool:
        """Remove a node and all edges that touch it.

        Returns ``True`` if the node existed.
        """
        with self._lock:
            cur = self._conn.execute(
                "SELECT 1 FROM nodes WHERE node_id = ? LIMIT 1", (node_id,)
            )
            if cur.fetchone() is None:
                return False
            self._conn.execute(
                "DELETE FROM edges WHERE source = ? OR target = ?",
                (node_id, node_id),
            )
            self._conn.execute(
                "DELETE FROM nodes WHERE node_id = ?", (node_id,)
            )
            self._conn.commit()
        return True

    def nodes_by_type(self, node_type: str) -> list:
        """Return all nodes of the given type."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT node_id, node_type, properties_json, created_at "
                "FROM nodes WHERE node_type = ? ORDER BY node_id",
                (node_type,),
            )
            rows = cur.fetchall()
        return [self._row_to_node(r) for r in rows]

    # ------------------------------------------------------------------
    # Edge operations
    # ------------------------------------------------------------------

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        properties: Optional[dict] = None,
        now: float = 0.0,
    ) -> Edge:
        """Insert a new edge, returning the stored :class:`Edge`."""
        props = properties if properties is not None else {}
        props_json = json.dumps(props, ensure_ascii=False, sort_keys=True)
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO edges "
                "(source, target, relation, properties_json, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (source, target, relation, props_json, now),
            )
            edge_id = int(cur.lastrowid)
            self._conn.commit()
        return Edge(
            edge_id=edge_id,
            source=source,
            target=target,
            relation=relation,
            properties=dict(props),
            created_at=now,
        )

    def get_edge(self, edge_id: int) -> Optional[Edge]:
        """Return an edge by id, or ``None``."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT edge_id, source, target, relation, properties_json, "
                "created_at FROM edges WHERE edge_id = ?",
                (edge_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_edge(row)

    def remove_edge(self, edge_id: int) -> bool:
        """Remove a single edge.  Returns ``True`` if it existed."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT 1 FROM edges WHERE edge_id = ? LIMIT 1", (edge_id,)
            )
            if cur.fetchone() is None:
                return False
            self._conn.execute(
                "DELETE FROM edges WHERE edge_id = ?", (edge_id,)
            )
            self._conn.commit()
        return True

    def edges_by_relation(self, relation: str) -> list:
        """Return all edges with the given relation."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT edge_id, source, target, relation, properties_json, "
                "created_at FROM edges WHERE relation = ? ORDER BY edge_id",
                (relation,),
            )
            rows = cur.fetchall()
        return [self._row_to_edge(r) for r in rows]

    def outgoing(
        self, node_id: str, relation: Optional[str] = None
    ) -> list:
        """Return outgoing edges from ``node_id`` (optionally filtered)."""
        with self._lock:
            if relation is None:
                cur = self._conn.execute(
                    "SELECT edge_id, source, target, relation, "
                    "properties_json, created_at "
                    "FROM edges WHERE source = ? ORDER BY edge_id",
                    (node_id,),
                )
            else:
                cur = self._conn.execute(
                    "SELECT edge_id, source, target, relation, "
                    "properties_json, created_at "
                    "FROM edges WHERE source = ? AND relation = ? "
                    "ORDER BY edge_id",
                    (node_id, relation),
                )
            rows = cur.fetchall()
        return [self._row_to_edge(r) for r in rows]

    def incoming(
        self, node_id: str, relation: Optional[str] = None
    ) -> list:
        """Return incoming edges to ``node_id`` (optionally filtered)."""
        with self._lock:
            if relation is None:
                cur = self._conn.execute(
                    "SELECT edge_id, source, target, relation, "
                    "properties_json, created_at "
                    "FROM edges WHERE target = ? ORDER BY edge_id",
                    (node_id,),
                )
            else:
                cur = self._conn.execute(
                    "SELECT edge_id, source, target, relation, "
                    "properties_json, created_at "
                    "FROM edges WHERE target = ? AND relation = ? "
                    "ORDER BY edge_id",
                    (node_id, relation),
                )
            rows = cur.fetchall()
        return [self._row_to_edge(r) for r in rows]

    def neighbors(self, node_id: str, direction: str = "out") -> list:
        """Return neighbor node ids.

        ``direction``: ``"out"``, ``"in"`` or ``"both"``.
        """
        if direction not in ("out", "in", "both"):
            raise ValueError(
                f"direction must be 'out', 'in' or 'both', got: {direction!r}"
            )
        with self._lock:
            out_ids: list = []
            in_ids: list = []
            if direction in ("out", "both"):
                cur = self._conn.execute(
                    "SELECT target FROM edges WHERE source = ? "
                    "ORDER BY edge_id",
                    (node_id,),
                )
                out_ids = [r[0] for r in cur.fetchall()]
            if direction in ("in", "both"):
                cur = self._conn.execute(
                    "SELECT source FROM edges WHERE target = ? "
                    "ORDER BY edge_id",
                    (node_id,),
                )
                in_ids = [r[0] for r in cur.fetchall()]
        if direction == "out":
            return out_ids
        if direction == "in":
            return in_ids
        # "both" — preserve order: outgoing first, then incoming, dedup
        seen: set = set()
        result: list = []
        for nid in out_ids + in_ids:
            if nid not in seen:
                seen.add(nid)
                result.append(nid)
        return result

    # ------------------------------------------------------------------
    # Traversal
    # ------------------------------------------------------------------

    def find_path(
        self, source: str, target: str, max_depth: int = 5
    ) -> Optional[Path]:
        """Find the shortest directed path from ``source`` to ``target``.

        Returns a :class:`Path` instance, or ``None`` if no path exists
        within ``max_depth`` edges.  When ``source == target``, returns
        a zero-length :class:`Path` containing just that node.
        """
        if self.get_node(source) is None:
            return None
        if source == target:
            return Path(nodes=[source], edges=[])
        if self.get_node(target) is None:
            return None

        # BFS — track parent (prev_node, edge_used) for path reconstruction.
        parents: dict = {source: (None, None)}
        depths: dict = {source: 0}
        queue: deque = deque([source])
        found = False
        while queue:
            current = queue.popleft()
            cur_depth = depths[current]
            if cur_depth >= max_depth:
                continue
            edges_out = self.outgoing(current)
            for e in edges_out:
                nxt = e.target
                if nxt in parents:
                    continue
                parents[nxt] = (current, e)
                depths[nxt] = cur_depth + 1
                if nxt == target:
                    found = True
                    queue.clear()
                    break
                queue.append(nxt)
            if found:
                break
        if target not in parents:
            return None
        # Reconstruct path
        nodes_rev: list = [target]
        edges_rev: list = []
        cur = target
        while parents[cur][0] is not None:
            prev_node, prev_edge = parents[cur]
            edges_rev.append(prev_edge)
            nodes_rev.append(prev_node)
            cur = prev_node
        nodes_rev.reverse()
        edges_rev.reverse()
        return Path(nodes=nodes_rev, edges=edges_rev)

    def connected_to(self, node_id: str, depth: int = 1) -> set:
        """Return the set of node ids reachable from ``node_id`` within
        ``depth`` outgoing edges (does not include ``node_id`` itself).
        """
        if depth <= 0:
            return set()
        if self.get_node(node_id) is None:
            return set()
        visited: set = {node_id}
        result: set = set()
        frontier: list = [node_id]
        for _ in range(depth):
            next_frontier: list = []
            for nid in frontier:
                cur = self._conn.execute(
                    "SELECT target FROM edges WHERE source = ?", (nid,)
                )
                for (tgt,) in cur.fetchall():
                    if tgt not in visited:
                        visited.add(tgt)
                        result.add(tgt)
                        next_frontier.append(tgt)
            if not next_frontier:
                break
            frontier = next_frontier
        return result

    # ------------------------------------------------------------------
    # Degree
    # ------------------------------------------------------------------

    def in_degree(self, node_id: str) -> int:
        """Number of incoming edges to ``node_id``."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*) FROM edges WHERE target = ?", (node_id,)
            )
            return int(cur.fetchone()[0])

    def out_degree(self, node_id: str) -> int:
        """Number of outgoing edges from ``node_id``."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*) FROM edges WHERE source = ?", (node_id,)
            )
            return int(cur.fetchone()[0])

    def degree(self, node_id: str) -> int:
        """Total degree = in_degree + out_degree."""
        return self.in_degree(node_id) + self.out_degree(node_id)

    # ------------------------------------------------------------------
    # Stats / counts
    # ------------------------------------------------------------------

    def stats(self) -> GraphStats:
        """Return aggregate :class:`GraphStats`."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT node_type, COUNT(*) FROM nodes GROUP BY node_type"
            )
            node_types = {row[0]: int(row[1]) for row in cur.fetchall()}
            cur = self._conn.execute(
                "SELECT relation, COUNT(*) FROM edges GROUP BY relation"
            )
            relations = {row[0]: int(row[1]) for row in cur.fetchall()}
            cur = self._conn.execute("SELECT COUNT(*) FROM nodes")
            node_count = int(cur.fetchone()[0])
            cur = self._conn.execute("SELECT COUNT(*) FROM edges")
            edge_count = int(cur.fetchone()[0])
        return GraphStats(
            node_count=node_count,
            edge_count=edge_count,
            node_types=node_types,
            relations=relations,
        )

    @property
    def node_count(self) -> int:
        """Number of nodes in the graph."""
        with self._lock:
            cur = self._conn.execute("SELECT COUNT(*) FROM nodes")
            return int(cur.fetchone()[0])

    @property
    def edge_count(self) -> int:
        """Number of edges in the graph."""
        with self._lock:
            cur = self._conn.execute("SELECT COUNT(*) FROM edges")
            return int(cur.fetchone()[0])

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove every node and edge."""
        with self._lock:
            self._conn.execute("DELETE FROM edges")
            self._conn.execute("DELETE FROM nodes")
            self._conn.commit()

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()
