"""E148 Document compressor — compresses/decompresses text via stdlib algorithms.

Public API
----------
:class:`CompressionAlgo`   — enum of available compression algorithms
:class:`CompressionResult` — result of a compress() call
:class:`DocCompressor`     — main compressor class
"""
from .compressor import CompressionAlgo, CompressionResult, DocCompressor

__all__ = [
    "CompressionAlgo",
    "CompressionResult",
    "DocCompressor",
]
