"""Enhanced document search engine combining BM25, prefix, exact, and faceted filtering.

Stdlib only. Thread-safe via a single re-entrant lock.
"""

from __future__ import annotations

import math
import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    if not text:
        return []
    return _TOKEN_RE.findall(text.lower())


class MatchMode(Enum):
    """Available matching strategies for a SearchRequest."""

    BM25 = "bm25"
    PREFIX = "prefix"
    EXACT = "exact"
    ALL = "all"


@dataclass
class SearchRequest:
    """Container for a search query and its parameters."""

    query: str
    mode: MatchMode = MatchMode.BM25
    filters: dict[str, Any] = field(default_factory=dict)
    top_k: int = 10
    min_score: float = 0.0
    boost_fields: dict[str, float] = field(default_factory=dict)


@dataclass
class SearchHit:
    """A single search result."""

    doc_id: str
    score: float
    matched_fields: list[str] = field(default_factory=list)
    snippet: Optional[str] = None


@dataclass
class Facet:
    """Faceted result for a single field: value -> document count."""

    field: str
    values: dict[Any, int]


@dataclass
class SearchResult:
    """Full search result with hits, total count, and facets."""

    hits: list[SearchHit]
    total: int
    facets: list[Facet] = field(default_factory=list)
    query: str = ""


class DocSearchV2:
    """Thread-safe document search engine v2."""

    K1 = 1.5
    B = 0.75

    def __init__(self) -> None:
        self._lock = threading.RLock()
        # doc_id -> raw content
        self._contents: dict[str, str] = {}
        # doc_id -> field dict
        self._fields: dict[str, dict[str, Any]] = {}
        # doc_id -> tokens list
        self._tokens: dict[str, list[str]] = {}
        # doc_id -> term frequency map
        self._tf: dict[str, dict[str, int]] = {}
        # term -> doc frequency (number of docs containing the term)
        self._df: dict[str, int] = {}
        # doc_id -> document length (token count)
        self._dl: dict[str, int] = {}
        # cached total length for avgdl
        self._total_dl: int = 0

    # ---------------------------------------------------------------- helpers

    def _index_doc(self, doc_id: str, content: str, fields: Optional[dict]) -> None:
        tokens = _tokenize(content)
        tf: dict[str, int] = {}
        for tok in tokens:
            tf[tok] = tf.get(tok, 0) + 1
        self._contents[doc_id] = content or ""
        self._fields[doc_id] = dict(fields) if fields else {}
        self._tokens[doc_id] = tokens
        self._tf[doc_id] = tf
        self._dl[doc_id] = len(tokens)
        self._total_dl += len(tokens)
        for term in tf:
            self._df[term] = self._df.get(term, 0) + 1

    def _unindex_doc(self, doc_id: str) -> None:
        tf = self._tf.get(doc_id, {})
        for term in tf:
            cnt = self._df.get(term, 0) - 1
            if cnt <= 0:
                self._df.pop(term, None)
            else:
                self._df[term] = cnt
        self._total_dl -= self._dl.get(doc_id, 0)
        self._contents.pop(doc_id, None)
        self._fields.pop(doc_id, None)
        self._tokens.pop(doc_id, None)
        self._tf.pop(doc_id, None)
        self._dl.pop(doc_id, None)

    def _avgdl(self) -> float:
        n = len(self._contents)
        if n == 0:
            return 0.0
        return self._total_dl / n

    # ---------------------------------------------------------------- ingest

    def add(self, doc_id: str, content: str, fields: Optional[dict] = None) -> None:
        """Add or replace a document."""
        if not doc_id:
            raise ValueError("doc_id must be non-empty")
        with self._lock:
            if doc_id in self._contents:
                self._unindex_doc(doc_id)
            self._index_doc(doc_id, content or "", fields)

    def add_batch(self, docs: list[dict]) -> None:
        """Add many documents. Each dict needs `doc_id`, `content`, optional `fields`."""
        with self._lock:
            for d in docs:
                doc_id = d.get("doc_id")
                if not doc_id:
                    raise ValueError("each doc must have non-empty 'doc_id'")
                content = d.get("content", "")
                fields = d.get("fields")
                self.add(doc_id, content, fields)

    def update(
        self,
        doc_id: str,
        content: Optional[str] = None,
        fields: Optional[dict] = None,
    ) -> bool:
        """Update an existing document's content and/or fields.

        Returns True when the document existed and was updated, False otherwise.
        Passing ``content=None`` keeps existing content; passing ``fields=None``
        keeps existing fields.
        """
        with self._lock:
            if doc_id not in self._contents:
                return False
            new_content = self._contents[doc_id] if content is None else content
            new_fields = self._fields[doc_id] if fields is None else fields
            self._unindex_doc(doc_id)
            self._index_doc(doc_id, new_content, new_fields)
            return True

    def remove(self, doc_id: str) -> bool:
        """Remove a document. Returns True if it was present."""
        with self._lock:
            if doc_id not in self._contents:
                return False
            self._unindex_doc(doc_id)
            return True

    def clear(self) -> None:
        with self._lock:
            self._contents.clear()
            self._fields.clear()
            self._tokens.clear()
            self._tf.clear()
            self._df.clear()
            self._dl.clear()
            self._total_dl = 0

    # ---------------------------------------------------------------- info

    @property
    def doc_count(self) -> int:
        with self._lock:
            return len(self._contents)

    def term_count(self) -> int:
        with self._lock:
            return len(self._df)

    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return list(self._contents.keys())

    # ---------------------------------------------------------------- filter

    def _passes_filters(self, doc_id: str, filters: dict[str, Any]) -> bool:
        if not filters:
            return True
        fields = self._fields.get(doc_id, {})
        for f_field, expected in filters.items():
            actual = fields.get(f_field)
            if isinstance(expected, list):
                # docs must contain any of expected, in actual (list/scalar)
                if isinstance(actual, list):
                    if not any(e in actual for e in expected):
                        return False
                else:
                    if actual not in expected:
                        return False
            else:
                if isinstance(actual, list):
                    if expected not in actual:
                        return False
                else:
                    if actual != expected:
                        return False
        return True

    # ---------------------------------------------------------------- scoring

    def _bm25_score(self, doc_id: str, query_terms: list[str]) -> float:
        if not query_terms:
            return 0.0
        N = len(self._contents)
        if N == 0:
            return 0.0
        avgdl = self._avgdl() or 1.0
        dl = self._dl.get(doc_id, 0)
        tf_map = self._tf.get(doc_id, {})
        score = 0.0
        for term in query_terms:
            tf = tf_map.get(term, 0)
            if tf == 0:
                continue
            df = self._df.get(term, 0)
            if df == 0:
                continue
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            denom = tf + self.K1 * (1 - self.B + self.B * dl / avgdl)
            score += idf * tf * (self.K1 + 1) / denom
        return score

    def _field_boost_score(
        self, doc_id: str, query_terms: list[str], boost_fields: dict[str, float]
    ) -> tuple[float, list[str]]:
        """Compute extra score for occurrences of query terms in boosted fields."""
        if not boost_fields or not query_terms:
            return 0.0, []
        fields = self._fields.get(doc_id, {})
        boost_score = 0.0
        matched: list[str] = []
        for f_name, weight in boost_fields.items():
            val = fields.get(f_name)
            if val is None:
                continue
            if isinstance(val, list):
                text = " ".join(str(v) for v in val)
            else:
                text = str(val)
            f_tokens = _tokenize(text)
            f_set = set(f_tokens)
            hits = sum(1 for t in query_terms if t in f_set)
            if hits > 0:
                boost_score += hits * weight
                matched.append(f_name)
        return boost_score, matched

    # ---------------------------------------------------------------- search

    def search(self, request: SearchRequest) -> SearchResult:
        with self._lock:
            mode = request.mode
            query = request.query or ""
            q_terms = _tokenize(query)

            # collect candidate doc_ids that pass filters
            candidates = [
                d for d in self._contents if self._passes_filters(d, request.filters)
            ]

            hits: list[SearchHit] = []

            if mode == MatchMode.EXACT:
                target = (query or "").strip()
                for d in candidates:
                    if self._contents.get(d, "") == target:
                        hits.append(
                            SearchHit(
                                doc_id=d,
                                score=1.0,
                                matched_fields=["content"],
                            )
                        )
            elif mode == MatchMode.PREFIX:
                prefix = (query or "").lower().strip()
                if prefix:
                    for d in candidates:
                        tokens = self._tokens.get(d, [])
                        prefix_hits = sum(1 for t in tokens if t.startswith(prefix))
                        if prefix_hits > 0:
                            score = float(prefix_hits)
                            boost_score, matched = self._field_boost_score(
                                d, q_terms, request.boost_fields
                            )
                            score += boost_score
                            mfields = ["content"] + matched
                            hits.append(
                                SearchHit(
                                    doc_id=d,
                                    score=score,
                                    matched_fields=mfields,
                                )
                            )
            elif mode == MatchMode.BM25:
                for d in candidates:
                    s = self._bm25_score(d, q_terms)
                    boost_score, matched = self._field_boost_score(
                        d, q_terms, request.boost_fields
                    )
                    total = s + boost_score
                    if total > 0:
                        mfields = (["content"] if s > 0 else []) + matched
                        hits.append(
                            SearchHit(
                                doc_id=d,
                                score=total,
                                matched_fields=mfields,
                            )
                        )
            elif mode == MatchMode.ALL:
                # Combine BM25 + prefix + exact signals.
                prefix = (query or "").lower().strip()
                target = (query or "").strip()
                for d in candidates:
                    bm = self._bm25_score(d, q_terms)
                    tokens = self._tokens.get(d, [])
                    prefix_hits = (
                        sum(1 for t in tokens if t.startswith(prefix)) if prefix else 0
                    )
                    exact_score = 1.0 if self._contents.get(d, "") == target else 0.0
                    boost_score, matched = self._field_boost_score(
                        d, q_terms, request.boost_fields
                    )
                    total = bm + float(prefix_hits) + exact_score + boost_score
                    if total > 0:
                        mfields: list[str] = []
                        if bm > 0 or prefix_hits > 0 or exact_score > 0:
                            mfields.append("content")
                        mfields.extend(matched)
                        hits.append(
                            SearchHit(
                                doc_id=d,
                                score=total,
                                matched_fields=mfields,
                            )
                        )
            else:  # pragma: no cover - defensive
                raise ValueError(f"unsupported mode: {mode}")

            # min_score filter
            hits = [h for h in hits if h.score >= request.min_score]
            # sort by score desc, doc_id asc for stable ordering
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            total = len(hits)
            top_k = max(0, int(request.top_k))
            hits = hits[:top_k]

            # add snippets for top hits
            for h in hits:
                h.snippet = self.make_snippet(h.doc_id, query)

            return SearchResult(
                hits=hits, total=total, facets=[], query=query
            )

    def search_simple(self, query: str, top_k: int = 10) -> list[SearchHit]:
        return self.search(SearchRequest(query=query, top_k=top_k)).hits

    def facet_search(
        self, query: str, facet_fields: list[str], top_k: int = 10
    ) -> SearchResult:
        result = self.search(SearchRequest(query=query, top_k=top_k))
        with self._lock:
            facets: list[Facet] = []
            for f_field in facet_fields:
                counter: dict[Any, int] = {}
                for h in result.hits:
                    fields = self._fields.get(h.doc_id, {})
                    val = fields.get(f_field)
                    if val is None:
                        continue
                    if isinstance(val, list):
                        for v in val:
                            counter[v] = counter.get(v, 0) + 1
                    else:
                        counter[val] = counter.get(val, 0) + 1
                facets.append(Facet(field=f_field, values=counter))
            result.facets = facets
            return result

    def prefix_search(
        self, prefix: str, field: str = "content", top_k: int = 10
    ) -> list[SearchHit]:
        with self._lock:
            p = (prefix or "").lower().strip()
            hits: list[SearchHit] = []
            if not p:
                return hits
            for d in self._contents:
                if field == "content":
                    tokens = self._tokens.get(d, [])
                else:
                    val = self._fields.get(d, {}).get(field)
                    if val is None:
                        continue
                    if isinstance(val, list):
                        text = " ".join(str(v) for v in val)
                    else:
                        text = str(val)
                    tokens = _tokenize(text)
                cnt = sum(1 for t in tokens if t.startswith(p))
                if cnt > 0:
                    hits.append(
                        SearchHit(
                            doc_id=d,
                            score=float(cnt),
                            matched_fields=[field],
                        )
                    )
            hits.sort(key=lambda h: (-h.score, h.doc_id))
            return hits[: max(0, int(top_k))]

    def exact_search(self, text: str) -> list[SearchHit]:
        with self._lock:
            target = text if text is not None else ""
            hits: list[SearchHit] = []
            for d, content in self._contents.items():
                if content == target:
                    hits.append(
                        SearchHit(
                            doc_id=d,
                            score=1.0,
                            matched_fields=["content"],
                        )
                    )
            hits.sort(key=lambda h: h.doc_id)
            return hits

    # ---------------------------------------------------------------- snippet

    def make_snippet(self, doc_id: str, query: str, max_chars: int = 100) -> str:
        with self._lock:
            content = self._contents.get(doc_id, "")
            if not content:
                return ""
            q_terms = _tokenize(query)
            if not q_terms:
                return content[:max_chars]
            lower = content.lower()
            best = -1
            for term in q_terms:
                idx = lower.find(term)
                if idx >= 0 and (best < 0 or idx < best):
                    best = idx
            if best < 0:
                return content[:max_chars]
            half = max_chars // 2
            start = max(0, best - half)
            end = min(len(content), start + max_chars)
            snippet = content[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
            return snippet
