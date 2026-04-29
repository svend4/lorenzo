"""HybridSearcher — комбинирует keyword (TF-IDF) + semantic (embeddings) поиск.

Алгоритм:
  1. Ranking от keyword-search (быстрый, exact match boost)
  2. Ranking от semantic-search (медленнее, по смыслу)
  3. RRF (Reciprocal Rank Fusion) или взвешенная сумма
"""
from docstoolkit.embeddings.base import EmbeddingProvider, SearchResult
from docstoolkit.embeddings.tfidf import TFIDFProvider


class HybridSearcher:
    """Гибрид: 2 провайдера, агрегация рангов через RRF."""

    def __init__(self,
                 keyword: EmbeddingProvider | None = None,
                 semantic: EmbeddingProvider | None = None,
                 weights: tuple[float, float] = (0.4, 0.6),
                 rrf_k: int = 60):
        self.keyword = keyword or TFIDFProvider()
        self.semantic = semantic
        self.weights = weights
        self.rrf_k = rrf_k

    def search(self, query: str, docs: list[dict], top_k: int = 10,
               method: str = "rrf") -> list[SearchResult]:
        """method: 'rrf' (rank fusion) или 'weighted' (взвешенная сумма scores)."""
        kw_results = self.keyword.search(query, docs, top_k=top_k * 3)

        if not self.semantic:
            return kw_results[:top_k]

        sem_results = self.semantic.search(query, docs, top_k=top_k * 3)

        if method == "rrf":
            return self._rrf(kw_results, sem_results, top_k)
        return self._weighted(kw_results, sem_results, top_k)

    def _rrf(self, a: list[SearchResult], b: list[SearchResult],
             top_k: int) -> list[SearchResult]:
        """Reciprocal Rank Fusion: score(d) = Σ 1/(k + rank_i(d))"""
        scores: dict[str, float] = {}
        meta: dict[str, SearchResult] = {}
        for rank, r in enumerate(a):
            scores[r.doc_id] = scores.get(r.doc_id, 0) + 1.0 / (self.rrf_k + rank + 1)
            meta.setdefault(r.doc_id, r)
        for rank, r in enumerate(b):
            scores[r.doc_id] = scores.get(r.doc_id, 0) + 1.0 / (self.rrf_k + rank + 1)
            meta.setdefault(r.doc_id, r)

        sorted_ids = sorted(scores, key=lambda x: -scores[x])
        results = []
        for doc_id in sorted_ids[:top_k]:
            r = meta[doc_id]
            r.score = scores[doc_id]
            results.append(r)
        return results

    def _weighted(self, a: list[SearchResult], b: list[SearchResult],
                  top_k: int) -> list[SearchResult]:
        wa, wb = self.weights
        # Нормализация scores
        a_max = max((r.score for r in a), default=1)
        b_max = max((r.score for r in b), default=1)
        scores: dict[str, float] = {}
        meta: dict[str, SearchResult] = {}
        for r in a:
            norm = r.score / a_max if a_max else 0
            scores[r.doc_id] = scores.get(r.doc_id, 0) + wa * norm
            meta.setdefault(r.doc_id, r)
        for r in b:
            norm = r.score / b_max if b_max else 0
            scores[r.doc_id] = scores.get(r.doc_id, 0) + wb * norm
            meta.setdefault(r.doc_id, r)

        sorted_ids = sorted(scores, key=lambda x: -scores[x])
        results = []
        for doc_id in sorted_ids[:top_k]:
            r = meta[doc_id]
            r.score = scores[doc_id]
            results.append(r)
        return results
