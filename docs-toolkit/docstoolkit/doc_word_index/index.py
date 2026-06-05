"""Inverted word index for fast full-text lookup across documents.

Pure stdlib implementation. Uses ``re.finditer`` for tokenization and
``threading.Lock`` for thread-safety. Tracks character positions for every
word occurrence so callers can reconstruct highlights or snippets.

Module ID: E293
"""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional

__all__ = [
    "DocWordIndex",
    "IndexEntry",
    "IndexStats",
    "SearchResult",
]

_WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class IndexEntry:
    """All occurrences of one word inside one document."""

    doc_id: str
    word: str
    positions: list[int]  # character start positions of each occurrence
    frequency: int  # == len(positions)


@dataclass
class SearchResult:
    """A ranked result returned by :meth:`DocWordIndex.search`."""

    doc_id: str
    word: str
    frequency: int
    positions: list[int]
    score: float  # frequency-based score (extensible)


@dataclass
class IndexStats:
    """Aggregate statistics about the index."""

    total_docs: int
    total_words: int       # unique words across all docs
    total_entries: int     # sum of (doc, word) pairs
    avg_words_per_doc: float


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


class DocWordIndex:
    """Inverted word index mapping words -> documents with character positions.

    Parameters
    ----------
    min_word_len:
        Words shorter than this (after lowercasing) are not indexed.
        Default is 2 so single-character noise tokens are skipped.
    """

    def __init__(self, min_word_len: int = 2) -> None:
        self._min_word_len = min_word_len
        # word -> doc_id -> [char_positions]
        self._index: dict[str, dict[str, list[int]]] = {}
        # doc_id -> set of words (for fast removal and words_in_doc)
        self._doc_words: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tokenize(self, content: str) -> dict[str, list[int]]:
        """Return {word: [char_positions]} for content after lowercasing."""
        positions: dict[str, list[int]] = {}
        for m in _WORD_RE.finditer(content.lower()):
            word = m.group()
            if len(word) >= self._min_word_len:
                positions.setdefault(word, []).append(m.start())
        return positions

    def _remove_locked(self, doc_id: str) -> int:
        """Remove all entries for *doc_id* (caller holds the lock).

        Returns the number of unique words removed.
        """
        words = self._doc_words.pop(doc_id, set())
        for word in words:
            bucket = self._index.get(word)
            if bucket is None:
                continue
            bucket.pop(doc_id, None)
            if not bucket:
                del self._index[word]
        return len(words)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def index_doc(self, doc_id: str, content: str) -> int:
        """Index *content* under *doc_id*.

        Tokenizes with ``re.findall(r'\\b\\w+\\b', content.lower())``, filters
        words shorter than *min_word_len*, and records the character start
        position of every occurrence.

        If *doc_id* was already indexed its previous entries are replaced.

        Returns the count of unique words indexed for this document.
        """
        word_positions = self._tokenize(content)
        with self._lock:
            # Replace any prior entries
            self._remove_locked(doc_id)
            self._doc_words[doc_id] = set(word_positions.keys())
            for word, positions in word_positions.items():
                bucket = self._index.setdefault(word, {})
                bucket[doc_id] = list(positions)
        return len(word_positions)

    def remove_doc(self, doc_id: str) -> int:
        """Remove all index entries for *doc_id*.

        Returns the count of unique words that were removed (0 if the document
        was not in the index).
        """
        with self._lock:
            return self._remove_locked(doc_id)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search(self, word: str, limit: Optional[int] = None) -> list[SearchResult]:
        """Find all documents that contain *word* (exact match, lowercased).

        Returns a list of :class:`SearchResult` sorted by frequency descending.
        Pass *limit* to cap the result count.
        """
        normalized = word.lower()
        with self._lock:
            bucket = self._index.get(normalized)
            if not bucket:
                return []
            results: list[SearchResult] = []
            for doc_id, positions in bucket.items():
                freq = len(positions)
                results.append(
                    SearchResult(
                        doc_id=doc_id,
                        word=normalized,
                        frequency=freq,
                        positions=list(positions),
                        score=float(freq),
                    )
                )
        results.sort(key=lambda r: (-r.score, r.doc_id))
        if limit is not None:
            results = results[:limit]
        return results

    def search_multi(self, words: list[str], mode: str = "any") -> list[str]:
        """Search for multiple words and return matching doc_ids.

        Parameters
        ----------
        words:
            List of words to search for.
        mode:
            ``"any"`` — documents containing *at least one* word (OR).
            ``"all"`` — documents containing *every* word (AND).

        Returns a sorted list of doc_ids.
        """
        if not words:
            return []
        normalized = [w.lower() for w in words]
        with self._lock:
            if mode == "all":
                # Intersection: must appear in every word's bucket
                sets: list[set[str]] = []
                for w in normalized:
                    bucket = self._index.get(w)
                    if not bucket:
                        return []
                    sets.append(set(bucket.keys()))
                result_set = sets[0]
                for s in sets[1:]:
                    result_set = result_set & s
            else:  # "any"
                result_set: set[str] = set()
                for w in normalized:
                    bucket = self._index.get(w)
                    if bucket:
                        result_set |= set(bucket.keys())
        return sorted(result_set)

    def get_entry(self, doc_id: str, word: str) -> Optional[IndexEntry]:
        """Return the :class:`IndexEntry` for *(doc_id, word)* or ``None``."""
        normalized = word.lower()
        with self._lock:
            bucket = self._index.get(normalized)
            if not bucket:
                return None
            positions = bucket.get(doc_id)
            if positions is None:
                return None
            return IndexEntry(
                doc_id=doc_id,
                word=normalized,
                positions=list(positions),
                frequency=len(positions),
            )

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def words_in_doc(self, doc_id: str) -> list[str]:
        """Return a sorted list of words indexed for *doc_id*."""
        with self._lock:
            return sorted(self._doc_words.get(doc_id, set()))

    def docs_count(self) -> int:
        """Return the number of indexed documents."""
        with self._lock:
            return len(self._doc_words)

    def word_count(self) -> int:
        """Return the number of unique words across all documents."""
        with self._lock:
            return len(self._index)

    def top_words(
        self,
        limit: int = 10,
        doc_id: Optional[str] = None,
    ) -> list[tuple[str, int]]:
        """Return ``[(word, total_freq)]`` sorted by total frequency descending.

        Parameters
        ----------
        limit:
            Maximum number of entries to return.
        doc_id:
            If given, restrict to words that appear in this document and count
            only occurrences within it.
        """
        with self._lock:
            if doc_id is not None:
                words = self._doc_words.get(doc_id, set())
                pairs: list[tuple[str, int]] = []
                for word in words:
                    bucket = self._index.get(word)
                    if bucket and doc_id in bucket:
                        pairs.append((word, len(bucket[doc_id])))
            else:
                pairs = []
                for word, bucket in self._index.items():
                    total = sum(len(pos) for pos in bucket.values())
                    pairs.append((word, total))
        pairs.sort(key=lambda p: (-p[1], p[0]))
        return pairs[:limit]

    def stats(self) -> IndexStats:
        """Return aggregate :class:`IndexStats` for the current index."""
        with self._lock:
            total_docs = len(self._doc_words)
            total_words = len(self._index)
            total_entries = sum(
                len(bucket) for bucket in self._index.values()
            )
            avg = (
                total_entries / total_docs if total_docs else 0.0
            )
            return IndexStats(
                total_docs=total_docs,
                total_words=total_words,
                total_entries=total_entries,
                avg_words_per_doc=avg,
            )
