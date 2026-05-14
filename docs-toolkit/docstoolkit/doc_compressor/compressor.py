"""E148 Document compressor — stdlib-only compression of document text.

Supports GZIP, ZLIB, BZ2, LZMA, and NONE (passthrough). All textual input is
encoded as UTF-8 before compression and decoded after decompression.
"""
from __future__ import annotations

import base64
import bz2
import gzip
import lzma
import zlib
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class CompressionAlgo(Enum):
    """Supported compression algorithms."""

    GZIP = "gzip"
    ZLIB = "zlib"
    BZ2 = "bz2"
    LZMA = "lzma"
    NONE = "none"


@dataclass
class CompressionResult:
    """Result of a single compress() call."""

    original_size: int
    compressed_size: int
    algo: CompressionAlgo
    data: bytes

    @property
    def ratio(self) -> float:
        """Return compressed/original size ratio in [0, 1] (or 0 if original empty)."""
        if self.original_size == 0:
            return 0.0
        return self.compressed_size / self.original_size

    @property
    def savings_pct(self) -> float:
        """Return percentage savings vs original (negative if grew)."""
        if self.original_size == 0:
            return 0.0
        return (1.0 - self.ratio) * 100.0


class DocCompressor:
    """Compress/decompress text using stdlib compression algorithms."""

    def compress(
        self,
        text: str,
        algo: CompressionAlgo = CompressionAlgo.GZIP,
        level: int = 6,
    ) -> CompressionResult:
        """Compress *text* using *algo* at *level*. Returns CompressionResult."""
        raw = text.encode("utf-8")
        original_size = len(raw)

        if algo is CompressionAlgo.GZIP:
            data = gzip.compress(raw, compresslevel=level)
        elif algo is CompressionAlgo.ZLIB:
            data = zlib.compress(raw, level)
        elif algo is CompressionAlgo.BZ2:
            # bz2 only accepts compresslevel 1..9
            bz_level = max(1, min(9, level))
            data = bz2.compress(raw, bz_level)
        elif algo is CompressionAlgo.LZMA:
            # lzma preset is 0..9
            preset = max(0, min(9, level))
            data = lzma.compress(raw, preset=preset)
        elif algo is CompressionAlgo.NONE:
            data = raw
        else:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported algorithm: {algo!r}")

        return CompressionResult(
            original_size=original_size,
            compressed_size=len(data),
            algo=algo,
            data=data,
        )

    def decompress(self, data: bytes, algo: CompressionAlgo) -> str:
        """Decompress *data* produced by *algo* and return text."""
        if algo is CompressionAlgo.GZIP:
            raw = gzip.decompress(data)
        elif algo is CompressionAlgo.ZLIB:
            raw = zlib.decompress(data)
        elif algo is CompressionAlgo.BZ2:
            raw = bz2.decompress(data) if data else b""
        elif algo is CompressionAlgo.LZMA:
            raw = lzma.decompress(data) if data else b""
        elif algo is CompressionAlgo.NONE:
            raw = data
        else:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported algorithm: {algo!r}")

        return raw.decode("utf-8")

    def compress_to_base64(
        self,
        text: str,
        algo: CompressionAlgo = CompressionAlgo.GZIP,
    ) -> str:
        """Compress *text* and return base64-encoded ASCII string."""
        result = self.compress(text, algo=algo)
        return base64.b64encode(result.data).decode("ascii")

    def decompress_from_base64(self, b64: str, algo: CompressionAlgo) -> str:
        """Decode base64 string and decompress using *algo*."""
        data = base64.b64decode(b64.encode("ascii"))
        return self.decompress(data, algo)

    def benchmark(self, text: str) -> Dict[str, CompressionResult]:
        """Compress *text* with every algorithm and return dict keyed by algo name."""
        results: Dict[str, CompressionResult] = {}
        for algo in CompressionAlgo:
            results[algo.name] = self.compress(text, algo=algo)
        return results

    def recommend(self, text: str) -> CompressionAlgo:
        """Pick the algorithm producing the smallest output for *text*.

        NONE is excluded so we always recommend an actual compression algorithm
        (unless every compressor grows the data, in which case NONE wins).
        """
        results = self.benchmark(text)
        # Prefer the smallest compressed_size; tie-break by enum order.
        best_name = min(
            results.keys(),
            key=lambda n: (results[n].compressed_size, list(CompressionAlgo).index(CompressionAlgo[n])),
        )
        return CompressionAlgo[best_name]

    def compress_batch(
        self,
        texts: List[str],
        algo: CompressionAlgo = CompressionAlgo.GZIP,
    ) -> List[CompressionResult]:
        """Compress each text in *texts* using *algo*."""
        return [self.compress(t, algo=algo) for t in texts]

    def estimate_size(self, text: str, algo: CompressionAlgo) -> int:
        """Return the compressed size in bytes for *text* under *algo*."""
        return self.compress(text, algo=algo).compressed_size
