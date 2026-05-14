"""Hybrid search orchestrator: BM25 + Keyword backends with RRF/weighted-sum fusion."""
from docstoolkit.hybrid_search.backends import (
    SearchBackend,
    BM25Backend,
    KeywordBackend,
)
from docstoolkit.hybrid_search.orchestrator import (
    BackendWeight,
    OrchestratorConfig,
    HybridSearchResult,
    HybridSearchOrchestrator,
)
from docstoolkit.hybrid_search.monitor import (
    SearchLatency,
    HybridSearchMonitor,
)

__all__ = [
    # backends
    "SearchBackend",
    "BM25Backend",
    "KeywordBackend",
    # orchestrator
    "BackendWeight",
    "OrchestratorConfig",
    "HybridSearchResult",
    "HybridSearchOrchestrator",
    # monitor
    "SearchLatency",
    "HybridSearchMonitor",
]
