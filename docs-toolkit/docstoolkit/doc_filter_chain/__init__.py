"""E198 Composable document filter chain.

Public API
----------
:class:`FilterPhase`     — execution phase (PRE / MAIN / POST)
:class:`ChainFilter`     — single filter step (name, func, phase, priority, enabled)
:class:`FilterContext`   — processing context (original / current / history)
:class:`ChainResult`     — result of processing a single document
:class:`BatchResult`     — aggregated results for a batch
:class:`DocFilterChain`  — chain orchestrator
"""
from .chain import (
    BatchResult,
    ChainFilter,
    ChainResult,
    DocFilterChain,
    FilterContext,
    FilterPhase,
)

__all__ = [
    "BatchResult",
    "ChainFilter",
    "ChainResult",
    "DocFilterChain",
    "FilterContext",
    "FilterPhase",
]
