"""TF-IDF inverted index for full-text document search.

Stdlib-only implementation using `re` for tokenization and `threading.Lock`
for thread-safety.
"""

from __future__ import annotations

import math
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

__all__ = [
    "IndexedDoc",
    "SearchResult",
    "IndexStats",
    "DocSearchIndex",
]

_TOKEN_RE = re.compile(r"\b[a-zA-Z0-9]+\b")


def _tokenize(text: str) -> list[str]:
    """Return lowercase alphanumeric tokens from *text*."""
    return [t.lower() for t in _TOKEN_RE.findall(text)]


@dataclass
class IndexedDoc:
    """A single document entry in the index."""

    doc_id: str
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    indexed_at: float = 0.0


@dataclass
class SearchResult:
    """A single search result with TF-IDF score."""

    doc_id: str
    title: str
    score: float
    matched_terms: list[str]


@dataclass
class IndexStats:
    """Aggregate statistics for the index."""

    total_docs: int
    total_terms: int          # unique terms in the index
    avg_doc_length: float     # average token count per doc


class DocSearchIndex:
    """Inverted index with TF-IDF scoring.

    Thread-safe: all public methods acquire ``_lock`` for the duration of
    the operation.
    """

    def __init__(self) -> None:
        self._docs: dict[str, IndexedDoc] = {}
        self._doc_tokens: dict[str, list[str]] = {}
        # term -> set of doc_ids
        self._inverted: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def index_doc(
        self,
        doc: IndexedDoc,
        *,
        now: Optional[float] = None,
    ) -> None:
        """Index or re-index *doc*.

        Title tokens are repeated twice to give them extra weight.
        Tag strings are appended as tokens as well.
        """
        with self._lock:
            # Remove previous entries for this doc_id, if any.
            self._remove_locked(doc.doc_id)

            # Build token list: title (×2) + content + tags
            title_tokens = _tokenize(doc.title)
            content_tokens = _tokenize(doc.content)
            tag_tokens: list[str] = []
            for tag in doc.tags:
                tag_tokens.extend(_tokenize(tag))

            tokens = title_tokens + title_tokens + content_tokens + tag_tokens

            # Stamp indexed_at if not already set
            if doc.indexed_at == 0.0:
                doc.indexed_at = now if now is not None else time.time()

            self._docs[doc.doc_id] = doc
            self._doc_tokens[doc.doc_id] = tokens

            # Populate inverted index
            for term in tokens:
                self._inverted.setdefault(term, set()).add(doc.doc_id)

    def remove_doc(self, doc_id: str) -> bool:
        """Remove *doc_id* from the index. Returns True if it existed."""
        with self._lock:
            return self._remove_locked(doc_id)

    def _remove_locked(self, doc_id: str) -> bool:
        """Internal removal — caller must hold ``_lock``."""
        if doc_id not in self._docs:
            return False

        tokens = self._doc_tokens.pop(doc_id, [])
        for term in set(tokens):
            bucket = self._inverted.get(term)
            if bucket is not None:
                bucket.discard(doc_id)
                if not bucket:
                    del self._inverted[term]

        del self._docs[doc_id]
        return True

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get_doc(self, doc_id: str) -> Optional[IndexedDoc]:
        """Return the indexed :class:`IndexedDoc` for *doc_id*, or None."""
        with self._lock:
            return self._docs.get(doc_id)

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search the index using TF-IDF scoring.

        Only documents that contain at least one query term are returned.
        Results are sorted by score descending.
        """
        with self._lock:
            query_terms = list(set(_tokenize(query)))
            if not query_terms:
                return []

            total_docs = len(self._docs)
            if total_docs == 0:
                return []

            # Collect candidate doc_ids (union of all posting lists)
            candidate_ids: set[str] = set()
            for term in query_terms:
                candidate_ids |= self._inverted.get(term, set())

            results: list[SearchResult] = []
            for doc_id in candidate_ids:
                tokens = self._doc_tokens[doc_id]
                token_count = len(tokens)
                if token_count == 0:
                    continue

                score = 0.0
                matched: list[str] = []

                for term in query_terms:
                    tf_count = tokens.count(term)
                    if tf_count == 0:
                        continue
                    matched.append(term)
                    tf = tf_count / token_count
                    df = len(self._inverted.get(term, set()))
                    idf = math.log(1 + total_docs / (1 + df))
                    score += tf * idf

                if matched:
                    results.append(
                        SearchResult(
                            doc_id=doc_id,
                            title=self._docs[doc_id].title,
                            score=score,
                            matched_terms=sorted(matched),
                        )
                    )

            results.sort(key=lambda r: (-r.score, r.doc_id))
            return results[:limit]

    def search_by_tag(self, tag: str) -> list[str]:
        """Return sorted list of doc_ids that have *tag* in their tags list."""
        with self._lock:
            tag_lower = tag.lower()
            return sorted(
                doc_id
                for doc_id, doc in self._docs.items()
                if any(t.lower() == tag_lower for t in doc.tags)
            )

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of all indexed doc IDs."""
        with self._lock:
            return sorted(self._docs.keys())

    def stats(self) -> IndexStats:
        """Return aggregate statistics for the index."""
        with self._lock:
            total_docs = len(self._docs)
            total_terms = len(self._inverted)
            if total_docs:
                avg_doc_length = sum(
                    len(toks) for toks in self._doc_tokens.values()
                ) / total_docs
            else:
                avg_doc_length = 0.0
            return IndexStats(
                total_docs=total_docs,
                total_terms=total_terms,
                avg_doc_length=avg_doc_length,
            )
