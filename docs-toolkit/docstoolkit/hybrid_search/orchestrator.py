"""HybridSearchOrchestrator: fuse multiple search backends with RRF or weighted sum."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.hybrid_search.backends import SearchBackend


@dataclass
class BackendWeight:
    """Name and weight for a registered backend."""

    backend_name: str
    weight: float


@dataclass
class OrchestratorConfig:
    """Configuration for HybridSearchOrchestrator."""

    backend_weights: list[BackendWeight] = field(default_factory=list)
    fusion_method: str = "rrf"  # "rrf" or "weighted_sum"
    top_k: int = 10
    rrf_k: int = 60


@dataclass
class HybridSearchResult:
    """Result from a hybrid search query."""

    query: str
    results: list[tuple[str, float]]
    backend_results: dict[str, list[tuple[str, float]]]

    def top(self, n: int) -> list[tuple[str, float]]:
        """Return top-n results."""
        return self.results[:n]

    def doc_ids(self) -> list[str]:
        """Return list of doc_ids from results."""
        return [doc_id for doc_id, _ in self.results]


class HybridSearchOrchestrator:
    """Orchestrator that fuses results from multiple search backends.

    Supports two fusion methods:
    - ``rrf``: Reciprocal Rank Fusion — score = sum(weight * 1/(k + rank))
    - ``weighted_sum``: normalize scores per backend, then sum * weight
    """

    def __init__(self, config: OrchestratorConfig = None):
        self._config = config or OrchestratorConfig()
        # name -> (backend, weight)
        self._backends: dict[str, tuple[SearchBackend, float]] = {}

        # Pre-populate weights from config
        for bw in self._config.backend_weights:
            self._backend_weights_override = {
                bw.backend_name: bw.weight
                for bw in self._config.backend_weights
            }
            break
        else:
            self._backend_weights_override = {}

    def register(self, name: str, backend: SearchBackend, weight: float = 1.0) -> None:
        """Register a search backend with an optional weight.

        If a weight for this backend was specified in OrchestratorConfig.backend_weights,
        that weight takes precedence over the ``weight`` argument.
        """
        effective_weight = self._backend_weights_override.get(name, weight)
        self._backends[name] = (backend, effective_weight)

    def index(self, documents: dict[str, str]) -> None:
        """Index documents in all registered backends."""
        for backend, _ in self._backends.values():
            backend.index(documents)

    def search(self, query: str, top_k: int = None) -> HybridSearchResult:
        """Run query against all backends and fuse results.

        Args:
            query: search query string.
            top_k: override number of results; defaults to config.top_k.

        Returns:
            HybridSearchResult with fused ranking.
        """
        k = top_k if top_k is not None else self._config.top_k
        rrf_k = self._config.rrf_k

        # Collect per-backend results
        backend_results: dict[str, list[tuple[str, float]]] = {}
        backend_weights: dict[str, float] = {}

        for name, (backend, weight) in self._backends.items():
            # Fetch enough candidates for fusion (use larger k for better fusion)
            fetch_k = max(k * 3, 50)
            results = backend.search(query, top_k=fetch_k)
            backend_results[name] = results
            backend_weights[name] = weight

        if not backend_results:
            return HybridSearchResult(query=query, results=[], backend_results={})

        if self._config.fusion_method == "rrf":
            fused = self._fuse_rrf(backend_results, backend_weights, rrf_k, k)
        else:
            fused = self._fuse_weighted_sum(backend_results, backend_weights, k)

        return HybridSearchResult(
            query=query,
            results=fused,
            backend_results=backend_results,
        )

    def _fuse_rrf(
        self,
        backend_results: dict[str, list[tuple[str, float]]],
        backend_weights: dict[str, float],
        rrf_k: int,
        top_k: int,
    ) -> list[tuple[str, float]]:
        """Reciprocal Rank Fusion with per-backend weights.

        score(doc) = sum over backends: weight * 1 / (rrf_k + rank)
        rank is 1-based.
        """
        scores: dict[str, float] = {}
        for name, results in backend_results.items():
            weight = backend_weights.get(name, 1.0)
            for rank, (doc_id, _) in enumerate(results, start=1):
                contribution = weight * 1.0 / (rrf_k + rank)
                scores[doc_id] = scores.get(doc_id, 0.0) + contribution

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def _fuse_weighted_sum(
        self,
        backend_results: dict[str, list[tuple[str, float]]],
        backend_weights: dict[str, float],
        top_k: int,
    ) -> list[tuple[str, float]]:
        """Weighted sum fusion with per-backend score normalization.

        Normalize each backend's scores to [0, 1], then sum * weight.
        """
        scores: dict[str, float] = {}

        for name, results in backend_results.items():
            if not results:
                continue
            weight = backend_weights.get(name, 1.0)

            # Normalize scores to [0, 1]
            max_score = max(s for _, s in results)
            min_score = min(s for _, s in results)
            score_range = max_score - min_score

            for doc_id, raw_score in results:
                if score_range > 0:
                    normalized = (raw_score - min_score) / score_range
                else:
                    normalized = 1.0  # all scores equal
                scores[doc_id] = scores.get(doc_id, 0.0) + weight * normalized

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def backend_names(self) -> list[str]:
        """Return names of all registered backends."""
        return list(self._backends.keys())
