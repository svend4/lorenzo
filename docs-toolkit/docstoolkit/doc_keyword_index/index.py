"""Inverted keyword index with phrase queries, proximity, and snippet generation.

Stdlib-only implementation using `re` for tokenization and `threading.Lock` for
thread-safety. Designed as a low-level primitive distinct from BM25 search.
"""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional

__all__ = [
    "DocKeywordIndex",
    "IndexEntry",
    "IndexStats",
    "MatchHit",
]


_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


@dataclass
class IndexEntry:
    """A single posting: occurrence of a term in a doc."""

    doc_id: str
    position: int  # word position in doc (0-based)
    char_offset: int  # character offset in doc (0-based)


@dataclass
class MatchHit:
    """A doc-level match: all positions where the query matched in a doc."""

    doc_id: str
    positions: list[int] = field(default_factory=list)
    char_offsets: list[int] = field(default_factory=list)
    score: int = 0


@dataclass
class IndexStats:
    """Aggregate statistics about the index."""

    total_docs: int
    total_terms: int
    total_postings: int
    avg_doc_length: float


class DocKeywordIndex:
    """Inverted index mapping terms -> postings, with phrase/proximity queries."""

    def __init__(self, case_sensitive: bool = False) -> None:
        self._case_sensitive = case_sensitive
        # term -> doc_id -> list[(position, char_offset)]
        self._postings: dict[str, dict[str, list[tuple[int, int]]]] = {}
        # doc_id -> word count
        self._doc_lengths: dict[str, int] = {}
        # doc_id -> raw text (for snippets)
        self._doc_texts: dict[str, str] = {}
        # doc_id -> set[term] for fast removal
        self._doc_terms: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ---------- normalization ----------

    def _norm(self, term: str) -> str:
        return term if self._case_sensitive else term.lower()

    def _tokenize(self, text: str) -> list[tuple[str, int]]:
        """Return list of (token, char_offset) pairs."""
        out: list[tuple[str, int]] = []
        for m in _TOKEN_RE.finditer(text):
            out.append((m.group(0), m.start()))
        return out

    # ---------- mutation ----------

    def index_doc(self, doc_id: str, text: str) -> int:
        """Index (or re-index) a document. Returns the word count."""
        with self._lock:
            # Remove any prior entries for this doc
            self._remove_locked(doc_id)

            tokens = self._tokenize(text)
            word_count = len(tokens)
            terms_in_doc: set[str] = set()

            for position, (tok, offset) in enumerate(tokens):
                term = self._norm(tok)
                bucket = self._postings.setdefault(term, {})
                bucket.setdefault(doc_id, []).append((position, offset))
                terms_in_doc.add(term)

            self._doc_lengths[doc_id] = word_count
            self._doc_texts[doc_id] = text
            self._doc_terms[doc_id] = terms_in_doc
            return word_count

    def _remove_locked(self, doc_id: str) -> bool:
        if doc_id not in self._doc_lengths:
            return False
        for term in self._doc_terms.get(doc_id, set()):
            bucket = self._postings.get(term)
            if not bucket:
                continue
            bucket.pop(doc_id, None)
            if not bucket:
                self._postings.pop(term, None)
        self._doc_lengths.pop(doc_id, None)
        self._doc_texts.pop(doc_id, None)
        self._doc_terms.pop(doc_id, None)
        return True

    def remove_doc(self, doc_id: str) -> bool:
        """Remove a document from the index. Returns True if it existed."""
        with self._lock:
            return self._remove_locked(doc_id)

    def clear(self) -> None:
        """Drop all indexed documents."""
        with self._lock:
            self._postings.clear()
            self._doc_lengths.clear()
            self._doc_texts.clear()
            self._doc_terms.clear()

    # ---------- low-level lookup ----------

    def lookup(self, term: str) -> list[IndexEntry]:
        """Return every posting for `term`, across all docs."""
        with self._lock:
            normalized = self._norm(term)
            bucket = self._postings.get(normalized)
            if not bucket:
                return []
            out: list[IndexEntry] = []
            for doc_id, occurrences in bucket.items():
                for position, offset in occurrences:
                    out.append(
                        IndexEntry(doc_id=doc_id, position=position, char_offset=offset)
                    )
            return out

    # ---------- high-level queries ----------

    def find(self, term: str) -> list[MatchHit]:
        """Return one MatchHit per doc that contains `term`."""
        with self._lock:
            normalized = self._norm(term)
            bucket = self._postings.get(normalized)
            if not bucket:
                return []
            hits: list[MatchHit] = []
            for doc_id, occurrences in bucket.items():
                positions = [p for p, _ in occurrences]
                offsets = [o for _, o in occurrences]
                hits.append(
                    MatchHit(
                        doc_id=doc_id,
                        positions=list(positions),
                        char_offsets=list(offsets),
                        score=len(positions),
                    )
                )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_phrase(self, phrase: str) -> list[MatchHit]:
        """Find docs where the tokens of `phrase` appear consecutively."""
        terms = [self._norm(t) for t, _ in self._tokenize(phrase)]
        if not terms:
            return []
        if len(terms) == 1:
            return self.find(terms[0])

        with self._lock:
            # Candidate docs = intersection of postings for all terms
            buckets = []
            for term in terms:
                bucket = self._postings.get(term)
                if not bucket:
                    return []
                buckets.append(bucket)

            candidates = set(buckets[0].keys())
            for b in buckets[1:]:
                candidates &= set(b.keys())
            if not candidates:
                return []

            hits: list[MatchHit] = []
            for doc_id in candidates:
                # positions of first term that start a valid phrase
                first_positions = {p: o for p, o in buckets[0][doc_id]}
                phrase_starts: list[tuple[int, int]] = []
                for start_pos, start_off in first_positions.items():
                    ok = True
                    for i in range(1, len(terms)):
                        positions_i = {p for p, _ in buckets[i][doc_id]}
                        if (start_pos + i) not in positions_i:
                            ok = False
                            break
                    if ok:
                        phrase_starts.append((start_pos, start_off))
                if phrase_starts:
                    phrase_starts.sort()
                    hits.append(
                        MatchHit(
                            doc_id=doc_id,
                            positions=[p for p, _ in phrase_starts],
                            char_offsets=[o for _, o in phrase_starts],
                            score=len(phrase_starts),
                        )
                    )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_any(self, terms: list[str]) -> list[MatchHit]:
        """OR query: docs containing at least one of the terms."""
        if not terms:
            return []
        with self._lock:
            doc_positions: dict[str, list[tuple[int, int]]] = {}
            for term in terms:
                normalized = self._norm(term)
                bucket = self._postings.get(normalized)
                if not bucket:
                    continue
                for doc_id, occurrences in bucket.items():
                    doc_positions.setdefault(doc_id, []).extend(occurrences)
            hits: list[MatchHit] = []
            for doc_id, occurrences in doc_positions.items():
                occurrences.sort()
                hits.append(
                    MatchHit(
                        doc_id=doc_id,
                        positions=[p for p, _ in occurrences],
                        char_offsets=[o for _, o in occurrences],
                        score=len(occurrences),
                    )
                )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_all(self, terms: list[str]) -> list[MatchHit]:
        """AND query: docs containing every term."""
        if not terms:
            return []
        with self._lock:
            normalized_terms = [self._norm(t) for t in terms]
            buckets = []
            for term in normalized_terms:
                bucket = self._postings.get(term)
                if not bucket:
                    return []
                buckets.append(bucket)
            candidates = set(buckets[0].keys())
            for b in buckets[1:]:
                candidates &= set(b.keys())
            hits: list[MatchHit] = []
            for doc_id in candidates:
                merged: list[tuple[int, int]] = []
                for b in buckets:
                    merged.extend(b[doc_id])
                merged.sort()
                hits.append(
                    MatchHit(
                        doc_id=doc_id,
                        positions=[p for p, _ in merged],
                        char_offsets=[o for _, o in merged],
                        score=len(merged),
                    )
                )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_near(
        self, term_a: str, term_b: str, distance: int = 5
    ) -> list[MatchHit]:
        """Find docs where `term_a` and `term_b` occur within `distance` words."""
        if distance < 0:
            return []
        with self._lock:
            a = self._norm(term_a)
            b = self._norm(term_b)
            bucket_a = self._postings.get(a)
            bucket_b = self._postings.get(b)
            if not bucket_a or not bucket_b:
                return []
            common = set(bucket_a.keys()) & set(bucket_b.keys())
            hits: list[MatchHit] = []
            for doc_id in common:
                a_pos = bucket_a[doc_id]
                b_pos = bucket_b[doc_id]
                matched: list[tuple[int, int]] = []
                # naive O(|a|*|b|) — fine for reasonable doc sizes
                for pa, oa in a_pos:
                    for pb, ob in b_pos:
                        if pa == pb:
                            continue
                        if abs(pa - pb) <= distance:
                            matched.append((min(pa, pb), min(oa, ob)))
                            break
                if matched:
                    matched.sort()
                    hits.append(
                        MatchHit(
                            doc_id=doc_id,
                            positions=[p for p, _ in matched],
                            char_offsets=[o for _, o in matched],
                            score=len(matched),
                        )
                    )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    # ---------- snippets ----------

    def snippet(
        self, doc_id: str, query: str, max_chars: int = 100
    ) -> Optional[str]:
        """Return a `~max_chars` snippet of `doc_id` centered on the first match.

        Returns None if the doc is unknown or contains no query term.
        """
        with self._lock:
            text = self._doc_texts.get(doc_id)
            if text is None:
                return None
            query_terms = [self._norm(t) for t, _ in self._tokenize(query)]
            if not query_terms:
                return None

            # find the earliest char offset of any query term in this doc
            best_offset: Optional[int] = None
            for term in query_terms:
                bucket = self._postings.get(term)
                if not bucket:
                    continue
                occ = bucket.get(doc_id)
                if not occ:
                    continue
                first_offset = min(o for _, o in occ)
                if best_offset is None or first_offset < best_offset:
                    best_offset = first_offset
            if best_offset is None:
                return None

            if max_chars <= 0:
                return ""

            half = max_chars // 2
            start = max(0, best_offset - half)
            end = min(len(text), start + max_chars)
            # if we hit the end, slide start back so we still get max_chars
            if end - start < max_chars:
                start = max(0, end - max_chars)
            snip = text[start:end]
            prefix = "..." if start > 0 else ""
            suffix = "..." if end < len(text) else ""
            return f"{prefix}{snip}{suffix}"

    # ---------- introspection ----------

    def term_frequency(self, term: str, doc_id: Optional[str] = None) -> int:
        """Number of occurrences of `term` (in `doc_id` if given, else corpus)."""
        with self._lock:
            normalized = self._norm(term)
            bucket = self._postings.get(normalized)
            if not bucket:
                return 0
            if doc_id is None:
                return sum(len(v) for v in bucket.values())
            return len(bucket.get(doc_id, []))

    def doc_frequency(self, term: str) -> int:
        """Number of distinct docs containing `term`."""
        with self._lock:
            bucket = self._postings.get(self._norm(term))
            return len(bucket) if bucket else 0

    def vocabulary(self) -> set[str]:
        """Set of all indexed terms."""
        with self._lock:
            return set(self._postings.keys())

    def doc_ids(self) -> list[str]:
        """Sorted list of indexed doc_ids."""
        with self._lock:
            return sorted(self._doc_lengths.keys())

    def stats(self) -> IndexStats:
        """Aggregate index statistics."""
        with self._lock:
            total_docs = len(self._doc_lengths)
            total_terms = len(self._postings)
            total_postings = sum(
                len(occ)
                for bucket in self._postings.values()
                for occ in bucket.values()
            )
            avg = (
                sum(self._doc_lengths.values()) / total_docs
                if total_docs
                else 0.0
            )
            return IndexStats(
                total_docs=total_docs,
                total_terms=total_terms,
                total_postings=total_postings,
                avg_doc_length=avg,
            )

    @property
    def doc_count(self) -> int:
        with self._lock:
            return len(self._doc_lengths)
