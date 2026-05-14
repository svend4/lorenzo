"""Document chunker module for docs-toolkit (E155).

Splits documents into chunks for RAG / processing with configurable strategies:
  - FIXED_SIZE: split at chunk_size chars with overlap, prefer whitespace breaks
  - BY_PARAGRAPH: split on separator (default ``\\n\\n``)
  - BY_SENTENCE: split on sentence-ending punctuation
  - BY_HEADING: each heading + body is one chunk
  - BY_TOKEN_COUNT: tokens via str.split(), grouped to max_tokens
  - SLIDING_WINDOW: chunks of size ``window`` advanced by ``step``

Usage::

    from docstoolkit.doc_chunker import DocChunker, ChunkConfig, ChunkStrategy

    chunker = DocChunker(ChunkConfig(strategy=ChunkStrategy.BY_PARAGRAPH))
    chunks = chunker.chunk(text)
"""

from docstoolkit.doc_chunker.chunker import (
    Chunk,
    ChunkConfig,
    ChunkStrategy,
    DocChunker,
)

__all__ = [
    "Chunk",
    "ChunkConfig",
    "ChunkStrategy",
    "DocChunker",
]
