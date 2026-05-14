from docstoolkit.got.node import ThoughtNode, NodeType


class ThoughtGraph:
    """DAG of thought nodes."""

    def __init__(self):
        self._nodes: dict = {}  # node_id -> ThoughtNode

    def add_node(self, node: ThoughtNode) -> None:
        """Add node; update parent.children_ids for each parent."""
        self._nodes[node.node_id] = node
        for pid in node.parent_ids:
            if pid in self._nodes:
                parent = self._nodes[pid]
                if node.node_id not in parent.children_ids:
                    parent.children_ids.append(node.node_id)

    def get_node(self, node_id: str) -> ThoughtNode | None:
        return self._nodes.get(node_id)

    def roots(self) -> list:
        """Return nodes with no parents."""
        return [n for n in self._nodes.values() if not n.parent_ids]

    def leaves(self) -> list:
        """Return nodes with no children."""
        return [n for n in self._nodes.values() if not n.children_ids]

    def node_count(self) -> int:
        return len(self._nodes)

    def path_to_root(self, node_id: str) -> list:
        """Return list of node_ids from node up to a root (BFS shortest path).
        If node not found: [].
        If already a root: [node_id].
        """
        if node_id not in self._nodes:
            return []

        # BFS upwards through parent_ids
        from collections import deque

        # Each queue item is a path (list of node_ids) from starting node upward
        queue = deque([[node_id]])
        visited = {node_id}

        while queue:
            path = queue.popleft()
            current_id = path[-1]
            current_node = self._nodes.get(current_id)

            if current_node is None:
                continue

            # If current node has no parents, it's a root — return path
            if not current_node.parent_ids:
                return path

            for pid in current_node.parent_ids:
                if pid not in visited:
                    visited.add(pid)
                    queue.append(path + [pid])

        # If we exhausted the queue without finding a root (cycle or broken ref),
        # return the node itself
        return [node_id]

    def to_markdown(self) -> str:
        """Render graph as indented markdown tree starting from roots.

        Format:
        - [type] text (conf=X.XX)
          - [type] child text (conf=X.XX)
        """
        lines = []
        visited = set()

        def render(node_id: str, depth: int) -> None:
            if node_id in visited:
                return
            visited.add(node_id)
            node = self._nodes.get(node_id)
            if node is None:
                return
            indent = "  " * depth
            lines.append(f"{indent}- {node.summary()}")
            for child_id in node.children_ids:
                render(child_id, depth + 1)

        for root in self.roots():
            render(root.node_id, 0)

        return "\n".join(lines)

    def confirmed_facts(self) -> list:
        """Return nodes of type FACT."""
        return [n for n in self._nodes.values() if n.node_type == NodeType.FACT]

    def refuted_nodes(self) -> list:
        """Return nodes of type REFUTED."""
        return [n for n in self._nodes.values() if n.node_type == NodeType.REFUTED]
