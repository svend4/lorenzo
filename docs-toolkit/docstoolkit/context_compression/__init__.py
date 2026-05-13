"""Context compression for docs-toolkit — pure stdlib.

Modules
-------
scorer      RelevanceScore, RelevanceScorer
compressor  CompressionConfig, CompressedContext, ContextCompressor
window      ContextWindow, SlidingContextWindow
"""
from docstoolkit.context_compression.scorer import RelevanceScore, RelevanceScorer
from docstoolkit.context_compression.compressor import (
    CompressionConfig,
    CompressedContext,
    ContextCompressor,
)
from docstoolkit.context_compression.window import ContextWindow, SlidingContextWindow

__all__ = [
    # scorer
    "RelevanceScore",
    "RelevanceScorer",
    # compressor
    "CompressionConfig",
    "CompressedContext",
    "ContextCompressor",
    # window
    "ContextWindow",
    "SlidingContextWindow",
]
