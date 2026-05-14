"""DocTagHierarchy — hierarchical tag taxonomy management.

Manages a forest of tag nodes where each tag may have a parent and
multiple children.  Useful for organising documents under a hierarchical
tag taxonomy.

Stdlib only. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class TagNode:
    """A node in the tag hierarchy.

    Attributes
    ----------
    tag:
        Unique tag identifier.
    parent:
        The tag of the parent node, or ``None`` if this is a root tag.
    description:
        Free-form description for the tag.
    depth:
        Computed distance from the root; 0 for root tags.
    """

    tag: str
    parent: Optional[str] = None
    description: str = ""
    depth: int = 0


@dataclass
class TagHierarchyStats:
    """Aggregate statistics for the tag hierarchy.

    Attributes
    ----------
    total_tags:
        Number of tags registered in the hierarchy.
    root_count:
        Number of tags with no parent (depth == 0).
    max_depth:
        The deepest depth level present (0 for an empty hierarchy).
    leaf_count:
        Number of tags that have no children.
    """

    total_tags: int
    root_count: int
    max_depth: int
    leaf_count: int


class DocTagHierarchy:
    """Hierarchical tag taxonomy manager.

    Stores a forest of :class:`TagNode` objects where each node may have
    one parent and multiple children.

    Internal storage
    ----------------
    ``_nodes``    : dict[str, TagNode]   — tag → node
    ``_children`` : dict[str, list[str]] — parent tag → list of child tags
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._nodes: dict[str, TagNode] = {}
        # Maps parent tag → list of child tags (insertion order preserved).
        # Root tags are stored under the "" key.
        self._children: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock already held)
    # ------------------------------------------------------------------

    def _compute_depth(self, tag: str) -> int:
        """Walk up the parent chain to compute depth (lock must be held)."""
        depth = 0
        current = tag
        while True:
            node = self._nodes.get(current)
            if node is None or node.parent is None:
                return depth
            depth += 1
            current = node.parent

    def _recompute_subtree_depths(self, tag: str) -> None:
        """Recompute depth for tag and all descendants (lock must be held)."""
        queue: deque[str] = deque([tag])
        while queue:
            current = queue.popleft()
            node = self._nodes.get(current)
            if node is None:
                continue
            node.depth = self._compute_depth(current)
            for child in self._children.get(current, []):
                queue.append(child)

    def _is_ancestor(self, ancestor: str, tag: str) -> bool:
        """Return True if ``ancestor`` is an ancestor of ``tag`` (lock held)."""
        current = tag
        while True:
            node = self._nodes.get(current)
            if node is None or node.parent is None:
                return False
            if node.parent == ancestor:
                return True
            current = node.parent

    def _remove_child(self, parent: Optional[str], tag: str) -> None:
        """Remove ``tag`` from parent's children list (lock must be held)."""
        key = parent if parent is not None else ""
        children_list = self._children.get(key, [])
        if tag in children_list:
            children_list.remove(tag)

    def _add_child(self, parent: Optional[str], tag: str) -> None:
        """Append ``tag`` to parent's children list (lock must be held)."""
        key = parent if parent is not None else ""
        if key not in self._children:
            self._children[key] = []
        if tag not in self._children[key]:
            self._children[key].append(tag)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_tag(
        self,
        tag: str,
        parent: Optional[str] = None,
        description: str = "",
    ) -> TagNode:
        """Add or update a tag in the hierarchy.

        If the tag already exists, its ``description`` is updated and (if
        ``parent`` differs) its parent is changed and depths recomputed.

        Parameters
        ----------
        tag:
            Unique tag identifier.
        parent:
            The parent tag, or ``None`` for a root tag.
        description:
            Free-form description for the tag.

        Returns
        -------
        TagNode
            The created or updated tag node.

        Raises
        ------
        ValueError
            If ``parent`` is not ``None`` and does not exist in the hierarchy.
        """
        with self._lock:
            if parent is not None and parent not in self._nodes:
                raise ValueError("Parent not found")

            if tag in self._nodes:
                node = self._nodes[tag]
                old_parent = node.parent
                if old_parent != parent:
                    self._remove_child(old_parent, tag)
                    self._add_child(parent, tag)
                    node.parent = parent
                node.description = description
                # Recompute depths for this subtree (parent may have changed).
                self._recompute_subtree_depths(tag)
                return node

            depth = 0 if parent is None else self._nodes[parent].depth + 1
            node = TagNode(tag=tag, parent=parent, description=description, depth=depth)
            self._nodes[tag] = node
            self._add_child(parent, tag)
            return node

    def remove_tag(self, tag: str, cascade: bool = False) -> int:
        """Remove a tag from the hierarchy.

        Parameters
        ----------
        tag:
            The tag to remove.
        cascade:
            If ``True``, also remove all descendants.  If ``False`` (default)
            and the tag has any children, :class:`ValueError` is raised and
            the hierarchy is left unchanged.

        Returns
        -------
        int
            Total number of tags removed (1 in the non-cascade case;
            1 + descendants when cascading).

        Raises
        ------
        ValueError
            If ``cascade`` is ``False`` and the tag has children.
        """
        with self._lock:
            if tag not in self._nodes:
                return 0

            children = self._children.get(tag, [])
            if children and not cascade:
                raise ValueError("Tag has children")

            node = self._nodes[tag]
            parent = node.parent

            if not cascade:
                # No children → safe single removal.
                self._remove_child(parent, tag)
                del self._nodes[tag]
                self._children.pop(tag, None)
                return 1

            # Cascade: collect tag plus all descendants via BFS.
            to_remove: list[str] = []
            queue: deque[str] = deque([tag])
            while queue:
                current = queue.popleft()
                to_remove.append(current)
                for child in self._children.get(current, []):
                    queue.append(child)

            self._remove_child(parent, tag)
            for t in to_remove:
                self._nodes.pop(t, None)
                self._children.pop(t, None)
            return len(to_remove)

    def move_tag(self, tag: str, new_parent: Optional[str]) -> bool:
        """Change a tag's parent, recomputing depths.

        Parameters
        ----------
        tag:
            The tag to move.
        new_parent:
            The new parent tag, or ``None`` to promote to root.

        Returns
        -------
        bool
            ``False`` if ``tag`` is not found, if ``new_parent`` is given but
            not found, or if the move would create a cycle.  ``True``
            otherwise.
        """
        with self._lock:
            if tag not in self._nodes:
                return False
            if new_parent is not None and new_parent not in self._nodes:
                return False
            if new_parent == tag:
                return False
            if new_parent is not None and self._is_ancestor(tag, new_parent):
                return False

            node = self._nodes[tag]
            old_parent = node.parent
            if old_parent == new_parent:
                return True

            self._remove_child(old_parent, tag)
            self._add_child(new_parent, tag)
            node.parent = new_parent
            self._recompute_subtree_depths(tag)
            return True

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_tag(self, tag: str) -> Optional[TagNode]:
        """Return the node for ``tag``, or ``None`` if not found."""
        with self._lock:
            return self._nodes.get(tag)

    def children_of(self, tag: str) -> list[TagNode]:
        """Return direct children of ``tag`` sorted by tag name."""
        with self._lock:
            child_tags = self._children.get(tag, [])
            nodes = [self._nodes[t] for t in child_tags if t in self._nodes]
            return sorted(nodes, key=lambda n: n.tag)

    def descendants_of(self, tag: str) -> list[TagNode]:
        """Return all descendants in BFS order, sorted by tag at each level.

        Returns an empty list for leaf or unknown tags.
        """
        with self._lock:
            if tag not in self._nodes:
                return []
            result: list[TagNode] = []
            current_level = sorted(
                [self._nodes[t] for t in self._children.get(tag, []) if t in self._nodes],
                key=lambda n: n.tag,
            )
            while current_level:
                result.extend(current_level)
                next_level: list[TagNode] = []
                for node in current_level:
                    for child in self._children.get(node.tag, []):
                        if child in self._nodes:
                            next_level.append(self._nodes[child])
                current_level = sorted(next_level, key=lambda n: n.tag)
            return result

    def ancestors_of(self, tag: str) -> list[TagNode]:
        """Return ancestors from immediate parent up to the root."""
        with self._lock:
            result: list[TagNode] = []
            node = self._nodes.get(tag)
            if node is None:
                return result
            current = node.parent
            while current is not None:
                anc = self._nodes.get(current)
                if anc is None:
                    break
                result.append(anc)
                current = anc.parent
            return result

    def is_descendant(self, tag: str, ancestor: str) -> bool:
        """Return ``True`` if ``tag`` has ``ancestor`` somewhere above it."""
        with self._lock:
            node = self._nodes.get(tag)
            if node is None:
                return False
            current = node.parent
            while current is not None:
                if current == ancestor:
                    return True
                anc = self._nodes.get(current)
                if anc is None:
                    return False
                current = anc.parent
            return False

    def roots(self) -> list[TagNode]:
        """Return all root tags (no parent), sorted by tag name."""
        with self._lock:
            root_tags = self._children.get("", [])
            nodes = [self._nodes[t] for t in root_tags if t in self._nodes]
            return sorted(nodes, key=lambda n: n.tag)

    def all_tags(self) -> list[TagNode]:
        """Return all tag nodes sorted by tag name."""
        with self._lock:
            return sorted(self._nodes.values(), key=lambda n: n.tag)

    def path_to_root(self, tag: str) -> list[str]:
        """Return the path from ``tag`` up to the root as a list of tags.

        The first element is ``tag`` itself; the last is the root tag.
        Returns an empty list if ``tag`` is not found.
        """
        with self._lock:
            if tag not in self._nodes:
                return []
            path: list[str] = [tag]
            current: Optional[str] = self._nodes[tag].parent
            while current is not None:
                path.append(current)
                node = self._nodes.get(current)
                if node is None:
                    break
                current = node.parent
            return path

    def stats(self) -> TagHierarchyStats:
        """Return aggregate statistics for the hierarchy."""
        with self._lock:
            total_tags = len(self._nodes)
            root_count = sum(1 for n in self._nodes.values() if n.parent is None)
            max_depth = max((n.depth for n in self._nodes.values()), default=0)
            leaf_count = sum(
                1 for t in self._nodes
                if not self._children.get(t)
            )
            return TagHierarchyStats(
                total_tags=total_tags,
                root_count=root_count,
                max_depth=max_depth,
                leaf_count=leaf_count,
            )
