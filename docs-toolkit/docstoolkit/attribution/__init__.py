"""Counterfactual leave-one-out attribution for RAG passages."""
from docstoolkit.attribution.scorer import (
    AttributionScore, AttributionMap,
    counterfactual_attribution, embedding_attribution,
)
from docstoolkit.attribution.anomaly import detect_overreliance, AnomalyReport

__all__ = [
    "AttributionScore", "AttributionMap",
    "counterfactual_attribution", "embedding_attribution",
    "detect_overreliance", "AnomalyReport",
]
