"""Result fusion module for docs-toolkit (E17).

Combines ranked result lists from multiple retrieval sources using RRF,
weighted sum, Borda counting, or max-score strategies, and provides
result-level deduplication / source merging.
"""
from docstoolkit.result_fusion.result import SearchResult
from docstoolkit.result_fusion.fusion import (
    FusionMethod,
    FusionConfig,
    FusionResult,
    ResultFusion,
)
from docstoolkit.result_fusion.dedup import ResultDeduplicator

__all__ = [
    # result
    "SearchResult",
    # fusion
    "FusionMethod",
    "FusionConfig",
    "FusionResult",
    "ResultFusion",
    # dedup
    "ResultDeduplicator",
]
