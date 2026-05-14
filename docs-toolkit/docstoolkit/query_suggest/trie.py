"""Trie data structure for prefix-based query lookup."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    """Single node in a :class:`QueryTrie`.

    Attributes:
        children:  Mapping from character to child node.
        is_end:    True when this node marks the end of an inserted query.
        count:     Accumulated insertion count for the query ending here.
        query:     Full query string stored at this end node.
    """

    children: dict[str, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False
    count: int = 0
    query: str = ""


class QueryTrie:
    """Prefix trie optimised for query auto-complete.

    Queries are normalised (lowercased and stripped) before insertion so that
    lookups are case-insensitive and whitespace-insensitive at the boundaries.
    """

    def __init__(self) -> None:
        self._root = TrieNode()
        self._node_count: int = 1   # root counts as one node
        self._query_count: int = 0

    # ------------------------------------------------------------------
    # Normalisation
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(text: str) -> str:
        return text.lower().strip()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def insert(self, query: str, count: int = 1) -> None:
        """Insert *query* into the trie, accumulating *count* at the end node.

        The query is normalised before insertion.  If the query already exists,
        its stored count is incremented by *count*.
        """
        normalized = self._normalize(query)
        if not normalized:
            return

        node = self._root
        for char in normalized:
            if char not in node.children:
                node.children[char] = TrieNode()
                self._node_count += 1
            node = node.children[char]

        if not node.is_end:
            node.is_end = True
            node.query = normalized
            self._query_count += 1

        node.count += count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search(self, prefix: str) -> list[tuple[str, int]]:
        """Return all queries that start with *prefix*, sorted by count desc.

        Returns a list of ``(query, count)`` tuples.
        """
        normalized_prefix = self._normalize(prefix)
        node = self._find_node(normalized_prefix)
        if node is None:
            return []

        results: list[tuple[str, int]] = []
        self._dfs(node, results)
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def starts_with(self, prefix: str) -> bool:
        """Return True if any inserted query starts with *prefix*."""
        normalized_prefix = self._normalize(prefix)
        return self._find_node(normalized_prefix) is not None

    def node_count(self) -> int:
        """Return the total number of trie nodes (including root)."""
        return self._node_count

    def query_count(self) -> int:
        """Return the number of distinct queries inserted."""
        return self._query_count

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_node(self, prefix: str) -> "TrieNode | None":
        """Walk the trie to the node corresponding to *prefix*, or None."""
        node = self._root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self, node: TrieNode, results: list[tuple[str, int]]) -> None:
        """Depth-first traversal collecting end nodes into *results*."""
        if node.is_end:
            results.append((node.query, node.count))
        for child in node.children.values():
            self._dfs(child, results)
