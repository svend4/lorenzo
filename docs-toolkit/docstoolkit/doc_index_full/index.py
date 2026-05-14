"""Full-text positional index with light stemming and proximity search.

A standalone, stdlib-only inverted index that augments simpler keyword indexes
with two extras:

* light stemming (strip common English suffixes) so ``running`` matches ``run``
* generalized proximity search across N terms with optional ordering

Tokenization uses ``re.findall(r'\\w+', text)`` with case-folding (unless
``case_sensitive=True``). All public methods are guarded by a ``threading.Lock``.
"""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional

__all__ = [
    "DocIndexFull",
    "IndexEntry",
    "IndexStats",
    "Match",
]


_TOKEN_RE = re.compile(r"\w+", re.UNICODE)

# Order matters: longer suffixes first so we don't accidentally strip "-s" off
# of "-tion" etc.
_SUFFIXES = ("tion", "ment", "ness", "ing", "ed", "ly", "s")
_MIN_STEM_LEN = 3


@dataclass
class IndexEntry:
    """A single posting: one occurrence of a term in a doc."""

    doc_id: str
    position: int
    char_offset: int


@dataclass
class Match:
    """A doc-level match for a query."""

    doc_id: str
    term: str
    positions: list[int] = field(default_factory=list)
    score: float = 1.0


@dataclass
class IndexStats:
    """Aggregate statistics about the index."""

    total_docs: int
    total_tokens: int
    unique_terms: int
    avg_doc_length: float


class DocIndexFull:
    """Inverted positional index with light stemming and proximity queries."""

    def __init__(self, case_sensitive: bool = False, stem: bool = True) -> None:
        self._case_sensitive = case_sensitive
        self._stem_enabled = stem
        # term -> doc_id -> list[(position, char_offset)]
        self._postings: dict[str, dict[str, list[tuple[int, int]]]] = {}
        # doc_id -> word count
        self._doc_lengths: dict[str, int] = {}
        # doc_id -> raw text (for snippets)
        self._doc_texts: dict[str, str] = {}
        # doc_id -> set[term] of all indexable variants present (for cleanup)
        self._doc_terms: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ---------- normalization & stemming ----------

    def _norm(self, term: str) -> str:
        return term if self._case_sensitive else term.lower()

    def _stem(self, term: str) -> str:
        """Strip a common English suffix; return ``term`` unchanged if none fits."""
        if not self._stem_enabled:
            return term
        for suf in _SUFFIXES:
            if term.endswith(suf) and len(term) - len(suf) >= _MIN_STEM_LEN:
                stem = term[: -len(suf)]
                # Collapse doubled consonants before -ing/-ed (running -> run,
                # stopped -> stop) but leave words like "pass" alone.
                if (
                    suf in ("ing", "ed")
                    and len(stem) >= _MIN_STEM_LEN + 1
                    and stem[-1] == stem[-2]
                    and stem[-1] not in "aeiou"
                ):
                    stem = stem[:-1]
                return stem
        return term

    def _variants(self, term: str) -> list[str]:
        """Return the indexable variants of a (normalized) term.

        Always includes the original. If stemming yields a different form, the
        stem is appended so that both the inflected form and the stem are
        directly looked-up-able.
        """
        out = [term]
        if self._stem_enabled:
            stemmed = self._stem(term)
            if stemmed != term:
                out.append(stemmed)
        return out

    def _tokenize(self, text: str) -> list[tuple[str, int]]:
        return [(m.group(0), m.start()) for m in _TOKEN_RE.finditer(text)]

    # ---------- mutation ----------

    def index_doc(self, doc_id: str, text: str) -> int:
        """Index a document, replacing any prior version. Returns word count."""
        with self._lock:
            self._remove_locked(doc_id)

            tokens = self._tokenize(text)
            word_count = len(tokens)
            terms_in_doc: set[str] = set()

            for position, (tok, offset) in enumerate(tokens):
                normalized = self._norm(tok)
                for variant in self._variants(normalized):
                    bucket = self._postings.setdefault(variant, {})
                    bucket.setdefault(doc_id, []).append((position, offset))
                    terms_in_doc.add(variant)

            self._doc_lengths[doc_id] = word_count
            self._doc_texts[doc_id] = text
            self._doc_terms[doc_id] = terms_in_doc
            return word_count

    def update_doc(self, doc_id: str, text: str) -> int:
        """Re-index a document (alias for :meth:`index_doc`)."""
        return self.index_doc(doc_id, text)

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
        """Remove a document. Returns ``True`` if it existed."""
        with self._lock:
            return self._remove_locked(doc_id)

    def clear(self) -> None:
        """Drop everything."""
        with self._lock:
            self._postings.clear()
            self._doc_lengths.clear()
            self._doc_texts.clear()
            self._doc_terms.clear()

    # ---------- internal helpers (assume lock held) ----------

    def _lookup_term_locked(
        self, term: str
    ) -> dict[str, list[tuple[int, int]]]:
        """Return the posting bucket for the user-supplied term.

        The lookup tries the term as-given (normalized) first, then the stem.
        Postings for whichever variant actually exists are returned.
        """
        normalized = self._norm(term)
        bucket = self._postings.get(normalized)
        if bucket:
            return bucket
        if self._stem_enabled:
            stem = self._stem(normalized)
            if stem != normalized:
                bucket = self._postings.get(stem)
                if bucket:
                    return bucket
        return {}

    # ---------- low-level lookup ----------

    def lookup(self, term: str) -> list[IndexEntry]:
        """Return every :class:`IndexEntry` for ``term`` across all docs."""
        with self._lock:
            bucket = self._lookup_term_locked(term)
            out: list[IndexEntry] = []
            for doc_id, occurrences in bucket.items():
                for position, offset in occurrences:
                    out.append(
                        IndexEntry(
                            doc_id=doc_id, position=position, char_offset=offset
                        )
                    )
            return out

    # ---------- queries ----------

    def find(self, term: str) -> list[Match]:
        """Return one :class:`Match` per doc containing ``term``."""
        with self._lock:
            bucket = self._lookup_term_locked(term)
            if not bucket:
                return []
            normalized = self._norm(term)
            hits: list[Match] = []
            for doc_id, occurrences in bucket.items():
                positions = sorted(p for p, _ in occurrences)
                hits.append(
                    Match(
                        doc_id=doc_id,
                        term=normalized,
                        positions=positions,
                        score=float(len(positions)),
                    )
                )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_phrase(self, phrase: str) -> list[Match]:
        """Find docs where the tokens of ``phrase`` occur consecutively."""
        tokens = [self._norm(t) for t, _ in self._tokenize(phrase)]
        if not tokens:
            return []
        if len(tokens) == 1:
            return self.find(tokens[0])

        with self._lock:
            buckets: list[dict[str, list[tuple[int, int]]]] = []
            for tok in tokens:
                bucket = self._lookup_term_locked(tok)
                if not bucket:
                    return []
                buckets.append(bucket)

            candidates = set(buckets[0].keys())
            for b in buckets[1:]:
                candidates &= set(b.keys())
            if not candidates:
                return []

            phrase_text = " ".join(tokens)
            hits: list[Match] = []
            for doc_id in candidates:
                # positions where token0 appears in this doc
                start_positions = sorted(p for p, _ in buckets[0][doc_id])
                later_position_sets = [
                    {p for p, _ in b[doc_id]} for b in buckets[1:]
                ]
                matched: list[int] = []
                for sp in start_positions:
                    ok = True
                    for i, positions_i in enumerate(later_position_sets, start=1):
                        if (sp + i) not in positions_i:
                            ok = False
                            break
                    if ok:
                        matched.append(sp)
                if matched:
                    hits.append(
                        Match(
                            doc_id=doc_id,
                            term=phrase_text,
                            positions=matched,
                            score=float(len(matched)),
                        )
                    )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_proximity(
        self,
        terms: list[str],
        max_distance: int = 5,
        ordered: bool = False,
    ) -> list[Match]:
        """Find docs where all ``terms`` occur within ``max_distance`` of each other.

        ``max_distance`` is the maximum gap between adjacent positions in a
        candidate window (i.e. neighbouring terms after sorting positions).
        With ``ordered=True`` the terms must appear in the given order in
        the doc.
        """
        if not terms:
            return []
        if max_distance < 0:
            return []
        normalized = [self._norm(t) for t in terms]

        with self._lock:
            buckets: list[dict[str, list[tuple[int, int]]]] = []
            for tok in normalized:
                bucket = self._lookup_term_locked(tok)
                if not bucket:
                    return []
                buckets.append(bucket)

            candidates = set(buckets[0].keys())
            for b in buckets[1:]:
                candidates &= set(b.keys())
            if not candidates:
                return []

            query_text = " ".join(normalized)
            hits: list[Match] = []
            for doc_id in candidates:
                # positions per term in this doc, sorted
                per_term_positions = [
                    sorted(p for p, _ in b[doc_id]) for b in buckets
                ]
                matches = self._proximity_windows(
                    per_term_positions, max_distance, ordered
                )
                if matches:
                    # surface the anchor position of each window
                    anchor_positions = sorted({m[0] for m in matches})
                    hits.append(
                        Match(
                            doc_id=doc_id,
                            term=query_text,
                            positions=anchor_positions,
                            score=float(len(matches)),
                        )
                    )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    @staticmethod
    def _proximity_windows(
        per_term_positions: list[list[int]],
        max_distance: int,
        ordered: bool,
    ) -> list[tuple[int, ...]]:
        """Brute-force window enumeration.

        For modest doc sizes this is fine and keeps the implementation simple.
        Returns the list of tuples ``(p_0, p_1, ..., p_{n-1})`` where each
        ``p_i`` is the chosen position of term ``i``.
        """
        if not per_term_positions:
            return []

        results: list[tuple[int, ...]] = []

        def recurse(idx: int, chosen: list[int]) -> None:
            if idx == len(per_term_positions):
                # Validate window
                if ordered:
                    sorted_chosen = chosen
                    # strictly increasing positions
                    for a, b in zip(sorted_chosen, sorted_chosen[1:]):
                        if b <= a:
                            return
                    gaps = [b - a for a, b in zip(sorted_chosen, sorted_chosen[1:])]
                else:
                    if len(set(chosen)) != len(chosen):
                        return
                    s = sorted(chosen)
                    gaps = [b - a for a, b in zip(s, s[1:])]
                if not gaps or max(gaps) <= max_distance:
                    results.append(tuple(chosen))
                return
            for pos in per_term_positions[idx]:
                chosen.append(pos)
                recurse(idx + 1, chosen)
                chosen.pop()

        recurse(0, [])
        return results

    def find_or(self, terms: list[str]) -> list[Match]:
        """OR query: docs containing at least one term."""
        if not terms:
            return []
        with self._lock:
            doc_positions: dict[str, list[int]] = {}
            for term in terms:
                bucket = self._lookup_term_locked(term)
                for doc_id, occurrences in bucket.items():
                    doc_positions.setdefault(doc_id, []).extend(
                        p for p, _ in occurrences
                    )
            if not doc_positions:
                return []
            query_text = " | ".join(self._norm(t) for t in terms)
            hits: list[Match] = []
            for doc_id, positions in doc_positions.items():
                positions.sort()
                hits.append(
                    Match(
                        doc_id=doc_id,
                        term=query_text,
                        positions=positions,
                        score=float(len(positions)),
                    )
                )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_and(self, terms: list[str]) -> list[Match]:
        """AND query: docs containing every term."""
        if not terms:
            return []
        with self._lock:
            buckets: list[dict[str, list[tuple[int, int]]]] = []
            for term in terms:
                bucket = self._lookup_term_locked(term)
                if not bucket:
                    return []
                buckets.append(bucket)
            candidates = set(buckets[0].keys())
            for b in buckets[1:]:
                candidates &= set(b.keys())
            if not candidates:
                return []
            query_text = " & ".join(self._norm(t) for t in terms)
            hits: list[Match] = []
            for doc_id in candidates:
                merged: list[int] = []
                for b in buckets:
                    merged.extend(p for p, _ in b[doc_id])
                merged.sort()
                hits.append(
                    Match(
                        doc_id=doc_id,
                        term=query_text,
                        positions=merged,
                        score=float(len(merged)),
                    )
                )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits

    def find_not(self, term: str) -> list[str]:
        """Return sorted doc_ids that do NOT contain ``term``."""
        with self._lock:
            bucket = self._lookup_term_locked(term)
            containing = set(bucket.keys()) if bucket else set()
            return sorted(set(self._doc_lengths.keys()) - containing)

    # ---------- introspection ----------

    def term_frequency(self, term: str, doc_id: Optional[str] = None) -> int:
        """Occurrences of ``term`` (corpus-wide or within ``doc_id``)."""
        with self._lock:
            bucket = self._lookup_term_locked(term)
            if not bucket:
                return 0
            if doc_id is None:
                return sum(len(v) for v in bucket.values())
            return len(bucket.get(doc_id, []))

    def doc_frequency(self, term: str) -> int:
        """Number of distinct docs containing ``term``."""
        with self._lock:
            bucket = self._lookup_term_locked(term)
            return len(bucket)

    def vocabulary(self) -> set[str]:
        """All indexed terms (including stem variants)."""
        with self._lock:
            return set(self._postings.keys())

    def doc_ids(self) -> list[str]:
        """Sorted list of indexed doc_ids."""
        with self._lock:
            return sorted(self._doc_lengths.keys())

    def stats(self) -> IndexStats:
        """Return aggregate statistics."""
        with self._lock:
            total_docs = len(self._doc_lengths)
            total_tokens = sum(self._doc_lengths.values())
            unique_terms = len(self._postings)
            avg = total_tokens / total_docs if total_docs else 0.0
            return IndexStats(
                total_docs=total_docs,
                total_tokens=total_tokens,
                unique_terms=unique_terms,
                avg_doc_length=avg,
            )

    # ---------- snippets ----------

    def snippet(
        self, doc_id: str, term: str, max_chars: int = 100
    ) -> Optional[str]:
        """Return ``~max_chars`` excerpt of ``doc_id`` centred on ``term``.

        Returns ``None`` if the doc is unknown or doesn't contain ``term``.
        """
        with self._lock:
            text = self._doc_texts.get(doc_id)
            if text is None:
                return None
            bucket = self._lookup_term_locked(term)
            if not bucket:
                return None
            occ = bucket.get(doc_id)
            if not occ:
                return None
            if max_chars <= 0:
                return ""

            best_offset = min(o for _, o in occ)
            half = max_chars // 2
            start = max(0, best_offset - half)
            end = min(len(text), start + max_chars)
            if end - start < max_chars:
                start = max(0, end - max_chars)
            snip = text[start:end]
            prefix = "..." if start > 0 else ""
            suffix = "..." if end < len(text) else ""
            return f"{prefix}{snip}{suffix}"

    @property
    def doc_count(self) -> int:
        """Number of indexed documents."""
        with self._lock:
            return len(self._doc_lengths)
