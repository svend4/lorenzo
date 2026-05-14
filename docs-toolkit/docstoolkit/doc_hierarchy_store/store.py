"""DocHierarchyStore — tree-structured document hierarchy management.

Manages a forest of document nodes where each node may have a parent,
children, and an ordering position among its siblings.

Stdlib only. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HierarchyNode:
    """A node in the document hierarchy.

    Attributes
    ----------
    doc_id:
        Unique identifier for this document node.
    parent_id:
        The doc_id of the parent node, or ``None`` if this is a root node.
    title:
        Human-readable title for the node.
    position:
        Ordering among siblings; lower values come first.
    depth:
        Computed distance from the root; 0 for root nodes.
    """

    doc_id: str
    parent_id: Optional[str] = None
    title: str = ""
    position: int = 0
    depth: int = 0


@dataclass
class HierarchyStats:
    """Aggregate statistics for the document hierarchy.

    Attributes
    ----------
    total_nodes:
        Number of nodes registered in the hierarchy.
    root_count:
        Number of nodes with no parent (depth == 0).
    max_depth:
        The deepest depth level present (0 for an empty hierarchy).
    leaf_count:
        Number of nodes that have no children.
    """

    total_nodes: int
    root_count: int
    max_depth: int
    leaf_count: int


class DocHierarchyStore:
    """Tree-structured document hierarchy manager.

    Stores a forest of :class:`HierarchyNode` objects where each node
    can have one parent and multiple ordered children.

    Internal storage
    ----------------
    ``_nodes``    : dict[str, HierarchyNode] — doc_id → node
    ``_children`` : dict[str, list[str]]     — parent_id → ordered child doc_ids
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._nodes: dict[str, HierarchyNode] = {}
        # Maps parent_id → list of child doc_ids (insertion order preserved)
        self._children: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock already held)
    # ------------------------------------------------------------------

    def _compute_depth(self, doc_id: str) -> int:
        """Walk up the parent chain to compute depth (lock must be held)."""
        depth = 0
        current = doc_id
        while True:
            node = self._nodes.get(current)
            if node is None or node.parent_id is None:
                return depth
            depth += 1
            current = node.parent_id

    def _recompute_subtree_depths(self, doc_id: str) -> None:
        """Recompute depth for doc_id and all its descendants (lock must be held)."""
        # BFS from doc_id
        queue: deque[str] = deque([doc_id])
        while queue:
            current = queue.popleft()
            node = self._nodes.get(current)
            if node is None:
                continue
            node.depth = self._compute_depth(current)
            for child_id in self._children.get(current, []):
                queue.append(child_id)

    def _is_ancestor(self, ancestor_id: str, doc_id: str) -> bool:
        """Return True if ancestor_id is an ancestor of doc_id (lock must be held)."""
        current = doc_id
        while True:
            node = self._nodes.get(current)
            if node is None or node.parent_id is None:
                return False
            if node.parent_id == ancestor_id:
                return True
            current = node.parent_id

    def _remove_child(self, parent_id: Optional[str], doc_id: str) -> None:
        """Remove doc_id from parent's children list (lock must be held)."""
        key = parent_id if parent_id is not None else ""
        children_list = self._children.get(key, [])
        if doc_id in children_list:
            children_list.remove(doc_id)

    def _add_child(self, parent_id: Optional[str], doc_id: str) -> None:
        """Append doc_id to parent's children list (lock must be held)."""
        key = parent_id if parent_id is not None else ""
        if key not in self._children:
            self._children[key] = []
        if doc_id not in self._children[key]:
            self._children[key].append(doc_id)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_node(
        self,
        doc_id: str,
        parent_id: Optional[str] = None,
        title: str = "",
        position: int = 0,
    ) -> HierarchyNode:
        """Add or update a node in the hierarchy.

        If the node already exists, its ``parent_id``, ``title``, and
        ``position`` are updated and depth is recomputed.  When the parent
        changes the old parent's children list is updated accordingly.

        Parameters
        ----------
        doc_id:
            Unique identifier for the node.
        parent_id:
            doc_id of the parent, or ``None`` for a root node.
        title:
            Human-readable label.
        position:
            Ordering hint among siblings (lower = earlier).

        Returns
        -------
        HierarchyNode
            The created or updated node.
        """
        with self._lock:
            if doc_id in self._nodes:
                node = self._nodes[doc_id]
                old_parent = node.parent_id
                # Update parent reference in children lists if it changed
                if old_parent != parent_id:
                    self._remove_child(old_parent, doc_id)
                    self._add_child(parent_id, doc_id)
                node.parent_id = parent_id
                node.title = title
                node.position = position
            else:
                node = HierarchyNode(
                    doc_id=doc_id,
                    parent_id=parent_id,
                    title=title,
                    position=position,
                    depth=0,
                )
                self._nodes[doc_id] = node
                self._add_child(parent_id, doc_id)

            # Compute depth
            depth = 0
            current = doc_id
            while True:
                n = self._nodes.get(current)
                if n is None or n.parent_id is None:
                    break
                depth += 1
                current = n.parent_id
            node.depth = depth

            return node

    def remove_node(self, doc_id: str, reparent_children: bool = False) -> int:
        """Remove a node from the hierarchy.

        Parameters
        ----------
        doc_id:
            The node to remove.
        reparent_children:
            If ``True``, direct children of the removed node are reassigned
            to the removed node's parent (they keep their position values
            and their depths are recomputed).
            If ``False`` (default), all descendants are removed recursively.

        Returns
        -------
        int
            Total count of nodes removed (1 + descendants when cascading,
            or 1 when reparenting).
        """
        with self._lock:
            if doc_id not in self._nodes:
                return 0

            node = self._nodes[doc_id]
            grandparent_id = node.parent_id

            if reparent_children:
                # Move direct children to grandparent
                direct_children = list(self._children.get(doc_id, []))
                for child_id in direct_children:
                    child = self._nodes.get(child_id)
                    if child is not None:
                        child.parent_id = grandparent_id
                        self._add_child(grandparent_id, child_id)
                # Clear this node's children list
                self._children.pop(doc_id, None)

                # Remove this node from its parent's children list
                self._remove_child(grandparent_id, doc_id)
                del self._nodes[doc_id]

                # Recompute depths for reparented children and their subtrees
                for child_id in direct_children:
                    self._recompute_subtree_depths(child_id)

                return 1
            else:
                # Cascade: collect all descendants via BFS then remove them
                to_remove: list[str] = []
                queue: deque[str] = deque([doc_id])
                while queue:
                    current = queue.popleft()
                    to_remove.append(current)
                    for child_id in self._children.get(current, []):
                        queue.append(child_id)

                # Remove this subtree from its parent's children list
                self._remove_child(grandparent_id, doc_id)

                # Remove all nodes and their children mappings
                for nid in to_remove:
                    self._nodes.pop(nid, None)
                    self._children.pop(nid, None)

                return len(to_remove)

    def move_node(self, doc_id: str, new_parent_id: Optional[str]) -> bool:
        """Change a node's parent in the hierarchy.

        Recomputes ``depth`` for the node and all its descendants.

        Parameters
        ----------
        doc_id:
            The node to move.
        new_parent_id:
            The new parent's doc_id, or ``None`` to promote to root.

        Returns
        -------
        bool
            ``False`` if ``doc_id`` is not found, if ``new_parent_id`` is
            not found (and is not ``None``), or if the move would create a
            cycle (i.e. ``new_parent_id`` is a descendant of ``doc_id``).
            ``True`` on success.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return False
            if new_parent_id is not None and new_parent_id not in self._nodes:
                return False
            # Cycle check: new_parent_id must not be doc_id itself or a descendant
            if new_parent_id == doc_id:
                return False
            if new_parent_id is not None and self._is_ancestor(doc_id, new_parent_id):
                return False

            node = self._nodes[doc_id]
            old_parent_id = node.parent_id

            if old_parent_id == new_parent_id:
                # No actual change needed; still a success
                return True

            # Update children lists
            self._remove_child(old_parent_id, doc_id)
            self._add_child(new_parent_id, doc_id)

            # Update the node's parent reference
            node.parent_id = new_parent_id

            # Recompute depths for this node and all descendants
            self._recompute_subtree_depths(doc_id)

            return True

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_node(self, doc_id: str) -> Optional[HierarchyNode]:
        """Return the node for ``doc_id``, or ``None`` if not found."""
        with self._lock:
            return self._nodes.get(doc_id)

    def children(self, doc_id: str) -> list[HierarchyNode]:
        """Return direct children of ``doc_id`` sorted by ``(position, doc_id)``."""
        with self._lock:
            child_ids = self._children.get(doc_id, [])
            nodes = [self._nodes[cid] for cid in child_ids if cid in self._nodes]
            return sorted(nodes, key=lambda n: (n.position, n.doc_id))

    def parent(self, doc_id: str) -> Optional[HierarchyNode]:
        """Return the parent node of ``doc_id``, or ``None`` if root or not found."""
        with self._lock:
            node = self._nodes.get(doc_id)
            if node is None or node.parent_id is None:
                return None
            return self._nodes.get(node.parent_id)

    def ancestors(self, doc_id: str) -> list[HierarchyNode]:
        """Return ancestors from immediate parent up to the root (in that order).

        Returns an empty list for root nodes or unknown doc IDs.
        """
        with self._lock:
            result: list[HierarchyNode] = []
            node = self._nodes.get(doc_id)
            if node is None:
                return result
            current_id = node.parent_id
            while current_id is not None:
                current = self._nodes.get(current_id)
                if current is None:
                    break
                result.append(current)
                current_id = current.parent_id
            return result

    def descendants(self, doc_id: str) -> list[HierarchyNode]:
        """Return all descendants in BFS order, sorted by ``(depth, doc_id)`` at each level.

        Returns an empty list for leaf nodes or unknown doc IDs.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return []
            result: list[HierarchyNode] = []
            # BFS level by level; sort each level by doc_id
            current_level = sorted(
                [self._nodes[cid] for cid in self._children.get(doc_id, []) if cid in self._nodes],
                key=lambda n: n.doc_id,
            )
            while current_level:
                result.extend(current_level)
                next_level: list[HierarchyNode] = []
                for node in current_level:
                    for cid in self._children.get(node.doc_id, []):
                        if cid in self._nodes:
                            next_level.append(self._nodes[cid])
                current_level = sorted(next_level, key=lambda n: n.doc_id)
            return result

    def roots(self) -> list[HierarchyNode]:
        """Return all root nodes (no parent), sorted by ``(position, doc_id)``."""
        with self._lock:
            # Roots are nodes stored under the "" key in _children (parent_id=None)
            root_ids = self._children.get("", [])
            nodes = [self._nodes[rid] for rid in root_ids if rid in self._nodes]
            return sorted(nodes, key=lambda n: (n.position, n.doc_id))

    def all_nodes(self) -> list[HierarchyNode]:
        """Return all nodes sorted by ``doc_id``."""
        with self._lock:
            return sorted(self._nodes.values(), key=lambda n: n.doc_id)

    def path_to_root(self, doc_id: str) -> list[str]:
        """Return the path from ``doc_id`` up to the root as a list of doc_ids.

        The first element is ``doc_id`` itself; the last is the root's doc_id.
        Returns an empty list if ``doc_id`` is not found.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return []
            path: list[str] = [doc_id]
            current_id: Optional[str] = self._nodes[doc_id].parent_id
            while current_id is not None:
                path.append(current_id)
                node = self._nodes.get(current_id)
                if node is None:
                    break
                current_id = node.parent_id
            return path

    def stats(self) -> HierarchyStats:
        """Return aggregate statistics for the hierarchy."""
        with self._lock:
            total_nodes = len(self._nodes)
            root_count = sum(1 for n in self._nodes.values() if n.parent_id is None)
            max_depth = max((n.depth for n in self._nodes.values()), default=0)
            leaf_count = sum(
                1 for doc_id, n in self._nodes.items()
                if not self._children.get(doc_id)
            )
            return HierarchyStats(
                total_nodes=total_nodes,
                root_count=root_count,
                max_depth=max_depth,
                leaf_count=leaf_count,
            )
