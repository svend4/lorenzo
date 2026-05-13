"""SearchIndexManager and IndexConfig for the search index manager (E62)."""
from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.search_index_mgr.index import IndexEntry, IndexStats


def _tokenize(text: str) -> list[str]:
    """Split text into lowercase tokens, stripping non-alphanumeric characters."""
    return re.findall(r"[a-zA-Z0-9Ѐ-ӿ]+", text.lower())


@dataclass
class IndexConfig:
    """Configuration for the SearchIndexManager."""

    min_term_length: int = 2
    max_terms_per_doc: int = 10000
    stop_words: set[str] = field(default_factory=set)


class SearchIndexManager:
    """In-memory search index with TF-IDF scoring."""

    def __init__(self, config: Optional[IndexConfig] = None) -> None:
        self._config = config or IndexConfig()
        # doc_id -> IndexEntry
        self._entries: dict[str, IndexEntry] = {}
        # term -> {doc_id: tf}
        self._inverted: dict[str, dict[str, float]] = {}
        # doc_id -> list of terms (for doc length tracking)
        self._doc_terms: dict[str, list[str]] = {}
        # doc_id -> set of tags
        self._tag_index: dict[str, set[str]] = {}
        self._last_updated: float = time.time()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _filter_tokens(self, tokens: list[str]) -> list[str]:
        cfg = self._config
        return [
            t for t in tokens
            if len(t) >= cfg.min_term_length and t not in cfg.stop_words
        ]

    def _compute_tf(self, tokens: list[str]) -> dict[str, float]:
        """Compute term frequencies for a list of tokens."""
        counts: dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        total = len(tokens)
        if total == 0:
            return {}
        return {t: c / total for t, c in counts.items()}

    def _index_entry(self, entry: IndexEntry) -> None:
        """Add an entry's terms to the inverted index."""
        raw_tokens = _tokenize(entry.title + " " + entry.content)
        filtered = self._filter_tokens(raw_tokens)
        # Respect max_terms_per_doc (apply to unique terms that remain)
        filtered = filtered[: self._config.max_terms_per_doc]
        tf_map = self._compute_tf(filtered)
        self._doc_terms[entry.doc_id] = filtered
        for term, tf in tf_map.items():
            if term not in self._inverted:
                self._inverted[term] = {}
            self._inverted[term][entry.doc_id] = tf

    def _remove_entry_from_index(self, doc_id: str) -> None:
        """Remove a document's contributions from the inverted index."""
        terms = self._doc_terms.pop(doc_id, [])
        seen: set[str] = set()
        for term in terms:
            if term in seen:
                continue
            seen.add(term)
            if term in self._inverted:
                self._inverted[term].pop(doc_id, None)
                if not self._inverted[term]:
                    del self._inverted[term]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, entry: IndexEntry) -> None:
        """Add a document to the index. If doc_id already exists, replaces it."""
        if entry.doc_id in self._entries:
            self._remove_entry_from_index(entry.doc_id)
            self._tag_index.pop(entry.doc_id, None)
        self._entries[entry.doc_id] = entry
        self._index_entry(entry)
        self._tag_index[entry.doc_id] = set(entry.tags)
        self._last_updated = time.time()

    def remove(self, doc_id: str) -> bool:
        """Remove a document from the index. Returns True if found, False otherwise."""
        if doc_id not in self._entries:
            return False
        self._remove_entry_from_index(doc_id)
        del self._entries[doc_id]
        self._tag_index.pop(doc_id, None)
        self._last_updated = time.time()
        return True

    def update(self, entry: IndexEntry) -> None:
        """Update an existing document. Equivalent to remove + add."""
        self.remove(entry.doc_id)
        self.add(entry)

    def get(self, doc_id: str) -> Optional[IndexEntry]:
        """Return the IndexEntry for doc_id, or None if not found."""
        return self._entries.get(doc_id)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search the index using TF-IDF scoring.

        Score per document = sum over query terms of: tf * log(N / (df + 1))
        where N = number of documents, df = number of docs containing the term.

        Returns a list of (doc_id, score) sorted by score descending, up to top_k.
        """
        n_docs = len(self._entries)
        if n_docs == 0:
            return []

        raw_tokens = _tokenize(query)
        query_terms = list(set(self._filter_tokens(raw_tokens)))

        scores: dict[str, float] = {}
        for term in query_terms:
            if term not in self._inverted:
                continue
            postings = self._inverted[term]
            df = len(postings)
            idf = math.log(n_docs / (df + 1))
            for doc_id, tf in postings.items():
                scores[doc_id] = scores.get(doc_id, 0.0) + tf * idf

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def search_by_tag(self, tag: str) -> list[str]:
        """Return all doc_ids that have the given tag."""
        return [
            doc_id
            for doc_id, tags in self._tag_index.items()
            if tag in tags
        ]

    def stats(self) -> IndexStats:
        """Return aggregate statistics for the current index."""
        total_docs = len(self._entries)
        total_terms = len(self._inverted)
        if total_docs == 0:
            avg_doc_length = 0.0
        else:
            avg_doc_length = sum(len(v) for v in self._doc_terms.values()) / total_docs
        return IndexStats(
            total_docs=total_docs,
            total_terms=total_terms,
            avg_doc_length=avg_doc_length,
            last_updated=self._last_updated,
        )

    def all_doc_ids(self) -> list[str]:
        """Return all doc_ids currently in the index."""
        return list(self._entries.keys())

    def clear(self) -> None:
        """Remove all documents and reset the index."""
        self._entries.clear()
        self._inverted.clear()
        self._doc_terms.clear()
        self._tag_index.clear()
        self._last_updated = time.time()
