"""Learned fusion for hybrid retrieval (BM25 + dense + graph scores)."""
from docstoolkit.fusion.features import FusionFeatures, extract_features
from docstoolkit.fusion.model import LearnedFusion, FusionWeights
from docstoolkit.fusion.retriever import FusedRetriever, rrf_fusion

__all__ = [
    "FusionFeatures", "extract_features",
    "LearnedFusion", "FusionWeights",
    "FusedRetriever", "rrf_fusion",
]
