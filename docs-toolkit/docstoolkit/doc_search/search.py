"""Core implementation of the document search engine (E143).

Boolean and phrase search across a collection of in-memory documents.
Stdlib only — uses an inverted index for term lookups, retains the
original text for phrase/snippet/regex operations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

__all__ = [
    "MatchType",
    "SearchHit",
    "SearchQuery",
    "DocSearch",
]


_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


class MatchType(Enum):
    """How a query term should be matched against a document."""

    EXACT = "exact"
    PHRASE = "phrase"
    FUZZY = "fuzzy"
    REGEX = "regex"


@dataclass
class SearchHit:
    """A single search result."""

    doc_id: str
    match_type: MatchType
    score: float
    snippets: List[str] = field(default_factory=list)
    match_count: int = 0


@dataclass
class SearchQuery:
    """A structured query describing what to search for and how."""

    terms: List[str]
    operator: str = "AND"
    match_type: MatchType = MatchType.EXACT
    case_sensitive: bool = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str, case_sensitive: bool = False) -> List[str]:
    if not case_sensitive:
        text = text.lower()
    return _TOKEN_RE.findall(text)


def _norm(term: str, case_sensitive: bool = False) -> str:
    return term if case_sensitive else term.lower()


def _make_snippet(text: str, start: int, end: int, context: int) -> str:
    """Return a snippet of ``text`` around the [start, end) match.

    Trim to word boundaries on either side, prefix/suffix with ellipsis
    when the snippet does not start/end at the document boundary.
    """
    n = len(text)
    left = max(0, start - context)
    right = min(n, end + context)

    # Trim to word boundaries (avoid cutting words in half) unless we
    # are already at the doc edge.
    if left > 0:
        # Move left to the next non-word boundary.
        while left < start and text[left].isalnum():
            left += 1
    if right < n:
        while right > end and text[right - 1].isalnum():
            right -= 1

    snippet = text[left:right].strip()
    if left > 0:
        snippet = "..." + snippet
    if right < n:
        snippet = snippet + "..."
    return snippet


# ---------------------------------------------------------------------------
# DocSearch
# ---------------------------------------------------------------------------

class DocSearch:
    """In-memory boolean / phrase search engine."""

    def __init__(self) -> None:
        # Inverted index: token -> set of doc_ids containing the token.
        self._inverted: Dict[str, Set[str]] = {}
        # Forward store: doc_id -> original text.
        self._docs: Dict[str, str] = {}
        # Per-doc token frequency (for scoring).
        self._tf: Dict[str, Dict[str, int]] = {}

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def index(self, doc_id: str, text: str) -> None:
        """Add (or replace) a document in the index."""
        if doc_id in self._docs:
            self.remove(doc_id)
        self._docs[doc_id] = text
        tokens = _tokenize(text, case_sensitive=False)
        tf: Dict[str, int] = {}
        for tok in tokens:
            tf[tok] = tf.get(tok, 0) + 1
            self._inverted.setdefault(tok, set()).add(doc_id)
        self._tf[doc_id] = tf

    def index_batch(self, docs: Dict[str, str]) -> None:
        """Add a batch of documents."""
        for doc_id, text in docs.items():
            self.index(doc_id, text)

    def remove(self, doc_id: str) -> bool:
        """Remove a document from the index. Returns True if removed."""
        if doc_id not in self._docs:
            return False
        # Clean inverted index.
        for tok in list(self._tf.get(doc_id, {}).keys()):
            ids = self._inverted.get(tok)
            if ids is not None:
                ids.discard(doc_id)
                if not ids:
                    del self._inverted[tok]
        del self._docs[doc_id]
        self._tf.pop(doc_id, None)
        return True

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def doc_count(self) -> int:
        return len(self._docs)

    # ------------------------------------------------------------------
    # Counting
    # ------------------------------------------------------------------

    def count_matches(self, term: str) -> int:
        """Total occurrences of ``term`` across all docs (case-insensitive)."""
        key = _norm(term)
        total = 0
        for tf in self._tf.values():
            total += tf.get(key, 0)
        return total

    # ------------------------------------------------------------------
    # Snippets
    # ------------------------------------------------------------------

    def make_snippet(self, doc_id: str, term: str, context: int = 30) -> str:
        """Return a snippet around the first occurrence of ``term``."""
        text = self._docs.get(doc_id)
        if text is None:
            return ""
        # Case-insensitive search on original text.
        m = re.search(re.escape(term), text, re.IGNORECASE)
        if m is None:
            return ""
        return _make_snippet(text, m.start(), m.end(), context)

    # ------------------------------------------------------------------
    # Searching
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 10) -> List[SearchHit]:
        """Simple AND search across all whitespace-separated query terms."""
        terms = [t for t in _tokenize(query, case_sensitive=False) if t]
        if not terms:
            return []
        sq = SearchQuery(terms=terms, operator="AND", match_type=MatchType.EXACT)
        return self.search_advanced(sq, top_k=top_k)

    def search_advanced(
        self, query: SearchQuery, top_k: int = 10
    ) -> List[SearchHit]:
        """Advanced search driven by a :class:`SearchQuery`."""
        if not query.terms:
            return []

        if query.match_type is MatchType.PHRASE:
            phrase = " ".join(query.terms)
            return self.search_phrase(phrase, top_k=top_k)

        if query.match_type is MatchType.REGEX:
            # Treat each term as a regex; combine with operator.
            return self._search_regex_terms(query, top_k=top_k)

        # EXACT / FUZZY (FUZZY falls back to EXACT for stdlib-only).
        norm_terms = [_norm(t, query.case_sensitive) for t in query.terms]

        op = query.operator.upper()
        if op == "AND":
            candidates = self._and_candidates(norm_terms, query.case_sensitive)
        elif op == "OR":
            candidates = self._or_candidates(norm_terms, query.case_sensitive)
        elif op == "NOT":
            # "NOT" => docs that contain none of the terms.
            matching = self._or_candidates(norm_terms, query.case_sensitive)
            candidates = set(self._docs.keys()) - matching
        else:
            candidates = self._and_candidates(norm_terms, query.case_sensitive)

        hits: List[SearchHit] = []
        for doc_id in candidates:
            score = 0.0
            match_count = 0
            snippets: List[str] = []
            tf = self._tf.get(doc_id, {})
            for term in norm_terms:
                key = term if not query.case_sensitive else term.lower()
                # tf is always stored case-folded; case_sensitive flag affects
                # the original-text match for snippet only.
                count = tf.get(key, 0)
                if count == 0 and query.case_sensitive:
                    # Walk the original text to count case-sensitive matches.
                    count = self._count_case_sensitive(doc_id, term)
                if count > 0:
                    match_count += count
                    score += float(count)
                    snip = self.make_snippet(doc_id, term)
                    if snip:
                        snippets.append(snip)
            if match_count == 0 and op != "NOT":
                continue
            hits.append(
                SearchHit(
                    doc_id=doc_id,
                    match_type=query.match_type,
                    score=score,
                    snippets=snippets,
                    match_count=match_count,
                )
            )

        hits.sort(key=lambda h: (-h.score, h.doc_id))
        return hits[:top_k]

    def search_phrase(self, phrase: str, top_k: int = 10) -> List[SearchHit]:
        """Match the literal multi-word ``phrase`` (case-insensitive)."""
        if not phrase.strip():
            return []
        # Collapse whitespace in the query.
        normalized = re.sub(r"\s+", " ", phrase.strip())
        pattern = re.compile(
            r"\s+".join(re.escape(p) for p in normalized.split(" ")),
            re.IGNORECASE,
        )
        hits: List[SearchHit] = []
        for doc_id, text in self._docs.items():
            matches = list(pattern.finditer(text))
            if not matches:
                continue
            snippets = [
                _make_snippet(text, m.start(), m.end(), 30)
                for m in matches[:3]
            ]
            hits.append(
                SearchHit(
                    doc_id=doc_id,
                    match_type=MatchType.PHRASE,
                    score=float(len(matches)),
                    snippets=snippets,
                    match_count=len(matches),
                )
            )
        hits.sort(key=lambda h: (-h.score, h.doc_id))
        return hits[:top_k]

    def search_regex(self, pattern: str, top_k: int = 10) -> List[SearchHit]:
        """Scan each document with ``re.search`` for ``pattern``."""
        try:
            rx = re.compile(pattern)
        except re.error:
            return []
        hits: List[SearchHit] = []
        for doc_id, text in self._docs.items():
            matches = list(rx.finditer(text))
            if not matches:
                continue
            snippets = [
                _make_snippet(text, m.start(), m.end(), 30)
                for m in matches[:3]
            ]
            hits.append(
                SearchHit(
                    doc_id=doc_id,
                    match_type=MatchType.REGEX,
                    score=float(len(matches)),
                    snippets=snippets,
                    match_count=len(matches),
                )
            )
        hits.sort(key=lambda h: (-h.score, h.doc_id))
        return hits[:top_k]

    def search_boolean(
        self,
        must: List[str],
        must_not: Optional[List[str]] = None,
        should: Optional[List[str]] = None,
    ) -> List[SearchHit]:
        """Lucene-style boolean search.

        ``must`` — every term required.
        ``must_not`` — none of these terms may appear.
        ``should`` — optional terms that boost the score.
        """
        must_not = must_not or []
        should = should or []

        # Candidate set = intersection of MUST terms.
        if must:
            candidates: Set[str] = set(self._docs.keys())
            for t in must:
                ids = self._inverted.get(_norm(t), set())
                candidates &= ids
        else:
            # No mandatory terms — start from all docs (filter via should/not).
            candidates = set(self._docs.keys())

        # Exclude any docs that contain a MUST_NOT term.
        for t in must_not:
            ids = self._inverted.get(_norm(t), set())
            candidates -= ids

        hits: List[SearchHit] = []
        for doc_id in candidates:
            tf = self._tf.get(doc_id, {})
            score = 0.0
            match_count = 0
            snippets: List[str] = []
            for t in must:
                c = tf.get(_norm(t), 0)
                score += float(c)
                match_count += c
                snip = self.make_snippet(doc_id, t)
                if snip:
                    snippets.append(snip)
            for t in should:
                c = tf.get(_norm(t), 0)
                if c > 0:
                    score += 0.5 * float(c)
                    match_count += c
                    snip = self.make_snippet(doc_id, t)
                    if snip:
                        snippets.append(snip)
            # If there were no MUST terms and no SHOULD term matched,
            # skip — we don't want to return every document.
            if not must and match_count == 0 and should:
                continue
            hits.append(
                SearchHit(
                    doc_id=doc_id,
                    match_type=MatchType.EXACT,
                    score=score,
                    snippets=snippets,
                    match_count=match_count,
                )
            )

        hits.sort(key=lambda h: (-h.score, h.doc_id))
        return hits

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _and_candidates(
        self, terms: List[str], case_sensitive: bool
    ) -> Set[str]:
        if not terms:
            return set()
        if case_sensitive:
            # The inverted index is case-folded, so the lookup is a superset;
            # we filter precisely below.
            sets: List[Set[str]] = []
            for t in terms:
                sets.append(self._inverted.get(t.lower(), set()))
            candidates = set.intersection(*sets) if sets else set()
            # Now keep only docs where each term appears with exact case.
            return {
                d
                for d in candidates
                if all(self._count_case_sensitive(d, t) > 0 for t in terms)
            }
        sets = [self._inverted.get(t, set()) for t in terms]
        return set.intersection(*sets) if sets else set()

    def _or_candidates(
        self, terms: List[str], case_sensitive: bool
    ) -> Set[str]:
        out: Set[str] = set()
        for t in terms:
            ids = self._inverted.get(t.lower(), set())
            if case_sensitive:
                ids = {d for d in ids if self._count_case_sensitive(d, t) > 0}
            out |= ids
        return out

    def _count_case_sensitive(self, doc_id: str, term: str) -> int:
        text = self._docs.get(doc_id, "")
        # Whole-word match, case-sensitive.
        return len(re.findall(r"\b" + re.escape(term) + r"\b", text))

    def _search_regex_terms(
        self, query: SearchQuery, top_k: int
    ) -> List[SearchHit]:
        flags = 0 if query.case_sensitive else re.IGNORECASE
        try:
            patterns = [re.compile(t, flags) for t in query.terms]
        except re.error:
            return []
        op = query.operator.upper()
        hits: List[SearchHit] = []
        for doc_id, text in self._docs.items():
            per_term_counts = []
            all_matches = []
            for rx in patterns:
                ms = list(rx.finditer(text))
                per_term_counts.append(len(ms))
                all_matches.extend(ms)
            if op == "AND" and any(c == 0 for c in per_term_counts):
                continue
            if op == "OR" and all(c == 0 for c in per_term_counts):
                continue
            if op == "NOT" and any(c > 0 for c in per_term_counts):
                continue
            total = sum(per_term_counts)
            if op != "NOT" and total == 0:
                continue
            snippets = [
                _make_snippet(text, m.start(), m.end(), 30)
                for m in all_matches[:3]
            ]
            hits.append(
                SearchHit(
                    doc_id=doc_id,
                    match_type=MatchType.REGEX,
                    score=float(total),
                    snippets=snippets,
                    match_count=total,
                )
            )
        hits.sort(key=lambda h: (-h.score, h.doc_id))
        return hits[:top_k]
