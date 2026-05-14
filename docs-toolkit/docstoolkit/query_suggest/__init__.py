"""Query suggestions module: trie-based prefix lookup + SQLite history."""
from docstoolkit.query_suggest.trie import TrieNode, QueryTrie
from docstoolkit.query_suggest.history import QueryHistory
from docstoolkit.query_suggest.suggester import SuggestionConfig, Suggestion, QuerySuggester

__all__ = [
    # trie
    "TrieNode",
    "QueryTrie",
    # history
    "QueryHistory",
    # suggester
    "SuggestionConfig",
    "Suggestion",
    "QuerySuggester",
]
