"""IntentGraphBuilder: builds and merges intent graphs from natural language queries."""
from __future__ import annotations

import re

from docstoolkit.intent_graph.graph import IntentEdge, IntentGraph
from docstoolkit.intent_graph.node import IntentNode, IntentNodeType

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_STOPWORDS: frozenset[str] = frozenset(
    {"the", "a", "an", "is", "of", "in", "on", "at", "to", "for", "by", "with", "and", "or", "not"}
)

_ACTION_PREFIXES: tuple[str, ...] = ("how", "find", "get", "show", "list", "compare")
_ACTION_SUFFIXES: tuple[str, ...] = ("ing", "ed", "ize", "ate")


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class IntentGraphBuilder:
    """Build an :class:`IntentGraph` from a plain-text query string."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, query: str) -> IntentGraph:
        """Parse *query* and return a populated :class:`IntentGraph`."""
        graph = IntentGraph()

        # Root QUERY node
        query_node = IntentNode(node_type=IntentNodeType.QUERY, label=query)
        graph.add_node(query_node)

        # Tokenise: preserve original tokens for case inspection, lowercase for logic
        raw_tokens = re.split(r"[^a-zA-Z]+", query)
        raw_tokens = [t for t in raw_tokens if t]  # drop empties

        # Build per-token classification (a token can appear in multiple categories)
        concept_nodes: list[tuple[int, IntentNode]] = []  # (original index, node)

        for idx, raw_token in enumerate(raw_tokens):
            lower = raw_token.lower()

            is_entity = raw_token[0].isupper() if raw_token else False
            is_concept = (
                len(lower) >= 4
                and lower not in _STOPWORDS
                and not is_entity
            )
            is_action = self._is_action(lower)

            if is_entity:
                node = IntentNode(node_type=IntentNodeType.ENTITY, label=raw_token)
                graph.add_node(node)
                graph.add_edge(
                    IntentEdge(
                        source_id=query_node.node_id,
                        target_id=node.node_id,
                        relation="mentions",
                    )
                )

            if is_concept:
                node = IntentNode(node_type=IntentNodeType.CONCEPT, label=lower)
                graph.add_node(node)
                graph.add_edge(
                    IntentEdge(
                        source_id=query_node.node_id,
                        target_id=node.node_id,
                        relation="contains",
                    )
                )
                concept_nodes.append((idx, node))

            if is_action:
                node = IntentNode(node_type=IntentNodeType.ACTION, label=lower)
                graph.add_node(node)
                graph.add_edge(
                    IntentEdge(
                        source_id=query_node.node_id,
                        target_id=node.node_id,
                        relation="performs",
                    )
                )

        # CONCEPT→CONCEPT co-occurrence edges for consecutive concept tokens
        # "Consecutive" means their original token indices are adjacent (differ by 1)
        for i in range(len(concept_nodes) - 1):
            idx_a, node_a = concept_nodes[i]
            idx_b, node_b = concept_nodes[i + 1]
            if idx_b - idx_a == 1:
                graph.add_edge(
                    IntentEdge(
                        source_id=node_a.node_id,
                        target_id=node_b.node_id,
                        relation="co-occurs",
                    )
                )

        return graph

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------

    @staticmethod
    def merge(graphs: list[IntentGraph]) -> IntentGraph:
        """Combine multiple graphs into one, deduplicating by (label, node_type).

        When two nodes share the same label and type, only the first-seen node is
        kept; edges are re-mapped to point at the canonical node.
        """
        merged = IntentGraph()

        # Canonical map: (label, node_type) -> canonical IntentNode
        canonical: dict[tuple[str, IntentNodeType], IntentNode] = {}
        # old_id -> canonical node_id
        id_remap: dict[str, str] = {}

        for graph in graphs:
            d = graph.to_dict()

            for node_dict in d["nodes"]:
                key = (node_dict["label"], IntentNodeType(node_dict["node_type"]))
                if key not in canonical:
                    node = IntentNode(
                        node_type=IntentNodeType(node_dict["node_type"]),
                        label=node_dict["label"],
                        weight=node_dict["weight"],
                        metadata=dict(node_dict["metadata"]),
                    )
                    # Preserve original node_id so edges still resolve after add_node
                    node.node_id = node_dict["node_id"]
                    canonical[key] = node
                    merged.add_node(node)

                id_remap[node_dict["node_id"]] = canonical[key].node_id

            for edge_dict in d["edges"]:
                src = id_remap.get(edge_dict["source_id"], edge_dict["source_id"])
                tgt = id_remap.get(edge_dict["target_id"], edge_dict["target_id"])
                # Skip self-loops that may arise from deduplication
                if src == tgt:
                    continue
                # Avoid duplicate edges (same src, tgt, relation)
                existing = merged.edges_from(src)
                duplicate = any(
                    e.target_id == tgt and e.relation == edge_dict["relation"]
                    for e in existing
                )
                if not duplicate:
                    merged.add_edge(
                        IntentEdge(
                            source_id=src,
                            target_id=tgt,
                            relation=edge_dict["relation"],
                            weight=edge_dict["weight"],
                        )
                    )

        return merged

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_action(token: str) -> bool:
        """Return True if *token* looks like an action verb."""
        if token in _ACTION_PREFIXES:
            return True
        for suffix in _ACTION_SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix):
                return True
        return False
