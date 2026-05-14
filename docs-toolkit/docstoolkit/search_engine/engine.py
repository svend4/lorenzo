"""In-memory full-text search engine with inverted index and BM25 scoring.

Pure stdlib implementation — no external dependencies.
"""
from __future__ import annotations

import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Document:
    """A document to be indexed.

    Parameters
    ----------
    doc_id:
        Unique identifier for the document.
    fields:
        Mapping of field name to text content.
    metadata:
        Arbitrary extra data preserved and returned with search results.
    """

    doc_id: str
    fields: dict[str, str]
    metadata: dict = field(default_factory=dict)


@dataclass
class SearchResult:
    """A single search result.

    Parameters
    ----------
    doc_id:
        Identifier of the matched document.
    score:
        BM25 relevance score (higher is more relevant).
    document:
        The original :class:`Document` object.
    matched_fields:
        Field names that contain at least one query term.
    """

    doc_id: str
    score: float
    document: Document
    matched_fields: list[str]


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------


def _tokenize(text: str) -> list[str]:
    """Lowercase text and extract alphanumeric tokens.

    Returns a list of non-empty tokens (no punctuation, no whitespace).
    """
    return re.findall(r"[a-z0-9]+", text.lower())


# ---------------------------------------------------------------------------
# Search Engine
# ---------------------------------------------------------------------------


class SearchEngine:
    """In-memory full-text search engine backed by a BM25 inverted index.

    Parameters
    ----------
    k1:
        Term-frequency saturation parameter (default 1.5).
    b:
        Field-length normalisation parameter (default 0.75).

    Notes
    -----
    All documents are stored entirely in memory.  The index is rebuilt
    incrementally: adding or removing a single document updates the
    inverted index, document-length table, and IDF cache without a full
    re-index.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self._k1 = k1
        self._b = b

        # doc_id → Document
        self._docs: dict[str, Document] = {}

        # doc_id → total token count (across all fields)
        self._doc_lengths: dict[str, int] = {}

        # doc_id → {field_name → [tokens]}  (used for field-restricted search)
        self._field_tokens: dict[str, dict[str, list[str]]] = {}

        # inverted index: term → {doc_id → term_frequency}
        self._index: dict[str, dict[str, int]] = defaultdict(dict)

        # running total of all token lengths (for avgdl computation)
        self._total_tokens: int = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _all_field_names(self) -> set[str]:
        """Return every field name seen across all indexed documents."""
        names: set[str] = set()
        for field_map in self._field_tokens.values():
            names.update(field_map.keys())
        return names

    def _doc_length(self, doc_id: str) -> int:
        return self._doc_lengths.get(doc_id, 0)

    def _avgdl(self) -> float:
        n = len(self._docs)
        return self._total_tokens / n if n > 0 else 0.0

    def _idf(self, term: str) -> float:
        """Robertson-Walker IDF: ln((N - df + 0.5) / (df + 0.5) + 1)."""
        n = len(self._docs)
        df = len(self._index.get(term, {}))
        return math.log((n - df + 0.5) / (df + 0.5) + 1)

    def _index_doc(self, doc: Document) -> None:
        """Add *doc* to all internal data structures."""
        doc_id = doc.doc_id
        self._docs[doc_id] = doc

        field_token_map: dict[str, list[str]] = {}
        total_tf: dict[str, int] = defaultdict(int)
        total_len = 0

        for fname, text in doc.fields.items():
            tokens = _tokenize(text)
            field_token_map[fname] = tokens
            total_len += len(tokens)
            for tok in tokens:
                total_tf[tok] += 1

        self._field_tokens[doc_id] = field_token_map
        self._doc_lengths[doc_id] = total_len
        self._total_tokens += total_len

        for term, tf in total_tf.items():
            self._index[term][doc_id] = tf

    def _remove_doc(self, doc_id: str) -> None:
        """Remove *doc_id* from all internal data structures."""
        if doc_id not in self._docs:
            return

        # Remove from inverted index
        field_token_map = self._field_tokens.get(doc_id, {})
        seen_terms: set[str] = set()
        for tokens in field_token_map.values():
            seen_terms.update(tokens)

        for term in seen_terms:
            if term in self._index:
                self._index[term].pop(doc_id, None)
                if not self._index[term]:
                    del self._index[term]

        # Update running length total
        self._total_tokens -= self._doc_lengths.pop(doc_id, 0)

        del self._field_tokens[doc_id]
        del self._docs[doc_id]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, doc: Document) -> None:
        """Index *doc*.  Overwrites silently if ``doc_id`` already exists."""
        if doc.doc_id in self._docs:
            self._remove_doc(doc.doc_id)
        self._index_doc(doc)

    def add_many(self, docs: list[Document]) -> None:
        """Index a collection of documents in order."""
        for doc in docs:
            self.add(doc)

    def remove(self, doc_id: str) -> bool:
        """Remove the document with *doc_id* from the index.

        Returns ``True`` if the document existed, ``False`` otherwise.
        """
        if doc_id not in self._docs:
            return False
        self._remove_doc(doc_id)
        return True

    def get(self, doc_id: str) -> Document | None:
        """Return the :class:`Document` for *doc_id*, or ``None``."""
        return self._docs.get(doc_id)

    def doc_count(self) -> int:
        """Return the number of currently indexed documents."""
        return len(self._docs)

    def clear(self) -> None:
        """Remove all documents and reset the index."""
        self._docs.clear()
        self._doc_lengths.clear()
        self._field_tokens.clear()
        self._index.clear()
        self._total_tokens = 0

    def field_names(self) -> set[str]:
        """Return all field names present across the indexed documents."""
        return self._all_field_names()

    def search(
        self,
        query: str,
        top_k: int = 10,
        fields: list[str] | None = None,
    ) -> list[SearchResult]:
        """Search for *query* using BM25 scoring.

        Parameters
        ----------
        query:
            Query string.  Tokenised the same way as document text.
        top_k:
            Maximum number of results to return (default 10).
        fields:
            When given, only tokens in these fields contribute to the score.
            Documents where none of the listed fields contain a query term
            are excluded from results.

        Returns
        -------
        list[SearchResult]
            Up to *top_k* results sorted by BM25 score descending.
            Returns an empty list when there are no matches.
        """
        if not self._docs:
            return []

        query_terms = _tokenize(query)
        if not query_terms:
            return []

        avgdl = self._avgdl()
        k1 = self._k1
        b = self._b

        # scores[doc_id] → cumulative BM25 score
        scores: dict[str, float] = {}
        # matched_fields[doc_id] → set of field names matching at least one term
        matched_fields: dict[str, set[str]] = defaultdict(set)

        for term in query_terms:
            if term not in self._index:
                continue

            idf = self._idf(term)
            postings = self._index[term]  # {doc_id: tf_across_all_fields}

            for doc_id, tf_total in postings.items():
                # Field-restriction: if `fields` is given, recompute tf from
                # only the requested fields (and skip doc if zero contribution).
                if fields is not None:
                    field_map = self._field_tokens.get(doc_id, {})
                    tf_restricted = 0
                    contributing_fields: list[str] = []
                    for fname in fields:
                        field_toks = field_map.get(fname, [])
                        cnt = field_toks.count(term)
                        if cnt:
                            tf_restricted += cnt
                            contributing_fields.append(fname)
                    if tf_restricted == 0:
                        continue
                    tf = tf_restricted
                    matched_fields[doc_id].update(contributing_fields)
                else:
                    tf = tf_total
                    # record which fields matched
                    field_map = self._field_tokens.get(doc_id, {})
                    for fname, toks in field_map.items():
                        if term in toks:
                            matched_fields[doc_id].add(fname)

                dl = self._doc_lengths.get(doc_id, 0)
                norm_dl = dl / avgdl if avgdl > 0 else 1.0
                denom = tf + k1 * (1 - b + b * norm_dl)
                bm25 = idf * (tf * (k1 + 1)) / denom if denom != 0 else 0.0

                scores[doc_id] = scores.get(doc_id, 0.0) + bm25

        if not scores:
            return []

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results: list[SearchResult] = []
        for doc_id, score in ranked[:top_k]:
            results.append(
                SearchResult(
                    doc_id=doc_id,
                    score=score,
                    document=self._docs[doc_id],
                    matched_fields=sorted(matched_fields.get(doc_id, set())),
                )
            )
        return results
