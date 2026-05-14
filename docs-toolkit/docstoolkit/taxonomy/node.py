"""TaxonomyNode and TaxonomyTree data structures."""
import uuid
from dataclasses import dataclass, field


@dataclass
class TaxonomyNode:
    id: str                          # stable UUID
    label: str                       # auto-generated from top TF-IDF terms
    parent_id: str | None = None
    children_ids: list[str] = field(default_factory=list)
    doc_ids: list[str] = field(default_factory=list)   # doc paths/keys in this cluster
    top_terms: list[str] = field(default_factory=list) # top TF-IDF terms
    cohesion: float = 0.0            # avg pairwise similarity within cluster


class TaxonomyTree:
    """Container for TaxonomyNode hierarchy."""

    def __init__(self, nodes: list[TaxonomyNode]):
        self._nodes: dict[str, TaxonomyNode] = {n.id: n for n in nodes}

    def root_nodes(self) -> list[TaxonomyNode]:
        """Nodes with parent_id=None."""
        return [n for n in self._nodes.values() if n.parent_id is None]

    def children(self, node_id: str) -> list[TaxonomyNode]:
        """Nodes whose parent_id matches node_id."""
        return [n for n in self._nodes.values() if n.parent_id == node_id]

    def find_doc(self, doc_id: str) -> TaxonomyNode | None:
        """Find which node contains this doc."""
        for node in self._nodes.values():
            if doc_id in node.doc_ids:
                return node
        return None

    def all_nodes(self) -> list[TaxonomyNode]:
        return list(self._nodes.values())

    def to_markdown(self) -> str:
        """Indented tree: root nodes, then children indented with spaces."""
        lines: list[str] = []

        def _render(node: TaxonomyNode, depth: int) -> None:
            indent = "  " * depth
            doc_info = f" ({len(node.doc_ids)} docs)" if node.doc_ids else ""
            lines.append(f"{indent}- **{node.label}**{doc_info}")
            for child_id in node.children_ids:
                child = self._nodes.get(child_id)
                if child:
                    _render(child, depth + 1)

        for root in self.root_nodes():
            _render(root, 0)
        return "\n".join(lines)

    def doc_count(self) -> int:
        """Total docs across all nodes."""
        return sum(len(n.doc_ids) for n in self._nodes.values())

    def node_count(self) -> int:
        return len(self._nodes)
