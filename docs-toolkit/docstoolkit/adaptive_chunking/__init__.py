"""Adaptive chunking module for docs-toolkit (E23).

Splits text into chunks using multiple strategies:
  - paragraph-based
  - heading-section-based
  - fixed-size (with optional overlap)
  - sentence-based

Auto strategy selection via StrategySelector.

Usage::

    from docstoolkit.adaptive_chunking import AdaptiveChunker, ChunkConfig, StrategySelector

    chunker = AdaptiveChunker()
    chunks = chunker.chunk_by_paragraphs(text, doc_id="my-doc")

    selector = StrategySelector()
    strategy = selector.select(text)
"""

from docstoolkit.adaptive_chunking.chunk import Chunk, ChunkType
from docstoolkit.adaptive_chunking.splitter import AdaptiveChunker, ChunkConfig
from docstoolkit.adaptive_chunking.selector import ChunkingStrategy, StrategySelector

__all__ = [
    # chunk
    "Chunk",
    "ChunkType",
    # splitter
    "AdaptiveChunker",
    "ChunkConfig",
    # selector
    "ChunkingStrategy",
    "StrategySelector",
]
