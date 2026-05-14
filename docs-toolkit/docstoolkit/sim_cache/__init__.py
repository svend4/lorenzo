"""Semantic similarity cache module: fingerprinting, store, and high-level cache."""
from docstoolkit.sim_cache.fingerprint import (
    Fingerprint,
    FingerprintBuilder,
    FingerprintMethod,
)
from docstoolkit.sim_cache.store import SimCacheStore, SimilarityEntry
from docstoolkit.sim_cache.cache import (
    SimCacheConfig,
    SimCacheLookupResult,
    SemanticSimilarityCache,
)

__all__ = [
    "FingerprintMethod",
    "Fingerprint",
    "FingerprintBuilder",
    "SimilarityEntry",
    "SimCacheStore",
    "SimCacheConfig",
    "SimCacheLookupResult",
    "SemanticSimilarityCache",
]
