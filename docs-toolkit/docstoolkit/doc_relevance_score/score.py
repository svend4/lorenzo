"""E395 DocRelevanceScore — query-document relevance scoring implementation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class RelevanceScore:
    """A single relevance score for a (query, doc_id) pair."""

    query: str
    doc_id: str
    score: float
    recorded_at: float = 0.0


@dataclass
class ScoringStats:
    """Aggregate statistics over the relevance score store."""

    total_scores: int
    unique_queries: int
    unique_docs: int
    avg_score: float


class DocRelevanceScore:
    """Query-document relevance scoring store.

    Thread-safe; uses a single :class:`threading.Lock` to guard all state.
    """

    def __init__(self) -> None:
        self._scores: dict[tuple, RelevanceScore] = {}
        self._by_query: dict[str, set[str]] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ----------------------------------------------------------------- record
    def record_score(
        self,
        query: str,
        doc_id: str,
        score: float,
        now: Optional[float] = None,
    ) -> RelevanceScore:
        """Record (or replace) a relevance score. ``score`` is clamped to [0,1]."""
        clamped = float(score)
        if clamped < 0.0:
            clamped = 0.0
        elif clamped > 1.0:
            clamped = 1.0
        ts = now if now is not None else time.time()
        with self._lock:
            entry = RelevanceScore(
                query=query,
                doc_id=doc_id,
                score=clamped,
                recorded_at=ts,
            )
            self._scores[(query, doc_id)] = entry
            self._by_query.setdefault(query, set()).add(doc_id)
            self._by_doc.setdefault(doc_id, set()).add(query)
            return entry

    # -------------------------------------------------------------------- get
    def get_score(self, query: str, doc_id: str) -> Optional[float]:
        with self._lock:
            entry = self._scores.get((query, doc_id))
            return entry.score if entry is not None else None

    # ----------------------------------------------------------------- delete
    def delete_score(self, query: str, doc_id: str) -> bool:
        with self._lock:
            if (query, doc_id) not in self._scores:
                return False
            del self._scores[(query, doc_id)]
            docs = self._by_query.get(query)
            if docs is not None:
                docs.discard(doc_id)
                if not docs:
                    del self._by_query[query]
            queries = self._by_doc.get(doc_id)
            if queries is not None:
                queries.discard(query)
                if not queries:
                    del self._by_doc[doc_id]
            return True

    # ---------------------------------------------------------------- top_docs
    def top_docs_for(
        self,
        query: str,
        limit: int = 10,
        min_score: float = 0.0,
    ) -> list[tuple]:
        with self._lock:
            doc_ids = self._by_query.get(query, set())
            results: list[tuple] = []
            for d in doc_ids:
                entry = self._scores.get((query, d))
                if entry is None:
                    continue
                if entry.score < min_score:
                    continue
                results.append((d, entry.score))
            results.sort(key=lambda x: (-x[1], x[0]))
            return results[:limit]

    # ------------------------------------------------------------- top_queries
    def top_queries_for(self, doc_id: str, limit: int = 10) -> list[tuple]:
        with self._lock:
            queries = self._by_doc.get(doc_id, set())
            results: list[tuple] = []
            for q in queries:
                entry = self._scores.get((q, doc_id))
                if entry is None:
                    continue
                results.append((q, entry.score))
            results.sort(key=lambda x: (-x[1], x[0]))
            return results[:limit]

    # ----------------------------------------------------------- scores_for_x
    def scores_for_query(self, query: str) -> list[RelevanceScore]:
        with self._lock:
            doc_ids = self._by_query.get(query, set())
            entries = [
                self._scores[(query, d)]
                for d in doc_ids
                if (query, d) in self._scores
            ]
            entries.sort(key=lambda e: (-e.score, e.doc_id))
            return entries

    def scores_for_doc(self, doc_id: str) -> list[RelevanceScore]:
        with self._lock:
            queries = self._by_doc.get(doc_id, set())
            entries = [
                self._scores[(q, doc_id)]
                for q in queries
                if (q, doc_id) in self._scores
            ]
            entries.sort(key=lambda e: (-e.score, e.query))
            return entries

    # ---------------------------------------------------------------- clearing
    def clear_query(self, query: str) -> int:
        with self._lock:
            doc_ids = self._by_query.get(query, set())
            removed = 0
            for d in list(doc_ids):
                if (query, d) in self._scores:
                    del self._scores[(query, d)]
                    removed += 1
                queries = self._by_doc.get(d)
                if queries is not None:
                    queries.discard(query)
                    if not queries:
                        del self._by_doc[d]
            self._by_query.pop(query, None)
            return removed

    def clear_doc(self, doc_id: str) -> int:
        with self._lock:
            queries = self._by_doc.get(doc_id, set())
            removed = 0
            for q in list(queries):
                if (q, doc_id) in self._scores:
                    del self._scores[(q, doc_id)]
                    removed += 1
                docs = self._by_query.get(q)
                if docs is not None:
                    docs.discard(doc_id)
                    if not docs:
                        del self._by_query[q]
            self._by_doc.pop(doc_id, None)
            return removed

    def clear_all(self) -> int:
        with self._lock:
            removed = len(self._scores)
            self._scores.clear()
            self._by_query.clear()
            self._by_doc.clear()
            return removed

    # ----------------------------------------------------------------- listing
    def all_queries(self) -> list[str]:
        with self._lock:
            return sorted(self._by_query.keys())

    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._by_doc.keys())

    # ------------------------------------------------------------------- stats
    def stats(self) -> ScoringStats:
        with self._lock:
            total = len(self._scores)
            if total == 0:
                avg = 0.0
            else:
                avg = sum(e.score for e in self._scores.values()) / total
            return ScoringStats(
                total_scores=total,
                unique_queries=len(self._by_query),
                unique_docs=len(self._by_doc),
                avg_score=avg,
            )
