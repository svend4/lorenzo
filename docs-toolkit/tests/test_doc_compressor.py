"""Tests for E148 doc_compressor module."""
from __future__ import annotations

import base64

import pytest

from docstoolkit.doc_compressor import (
    CompressionAlgo,
    CompressionResult,
    DocCompressor,
)


SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. " * 50
    + "Lorenzo is a knowledge OS prototype. " * 30
)


# ---------------------------------------------------------------------------
# Enum
# ---------------------------------------------------------------------------


class TestCompressionAlgo:
    def test_has_gzip(self):
        assert CompressionAlgo.GZIP.value == "gzip"

    def test_has_zlib(self):
        assert CompressionAlgo.ZLIB.value == "zlib"

    def test_has_bz2(self):
        assert CompressionAlgo.BZ2.value == "bz2"

    def test_has_lzma(self):
        assert CompressionAlgo.LZMA.value == "lzma"

    def test_has_none(self):
        assert CompressionAlgo.NONE.value == "none"

    def test_five_algos(self):
        assert len(list(CompressionAlgo)) == 5


# ---------------------------------------------------------------------------
# CompressionResult
# ---------------------------------------------------------------------------


class TestCompressionResult:
    def test_ratio_half(self):
        r = CompressionResult(original_size=100, compressed_size=50, algo=CompressionAlgo.GZIP, data=b"x")
        assert r.ratio == 0.5

    def test_ratio_zero_original(self):
        r = CompressionResult(original_size=0, compressed_size=0, algo=CompressionAlgo.GZIP, data=b"")
        assert r.ratio == 0.0

    def test_savings_pct_half(self):
        r = CompressionResult(original_size=100, compressed_size=50, algo=CompressionAlgo.GZIP, data=b"x")
        assert r.savings_pct == 50.0

    def test_savings_pct_zero_original(self):
        r = CompressionResult(original_size=0, compressed_size=0, algo=CompressionAlgo.GZIP, data=b"")
        assert r.savings_pct == 0.0

    def test_savings_pct_negative_when_grew(self):
        r = CompressionResult(original_size=10, compressed_size=20, algo=CompressionAlgo.GZIP, data=b"x")
        assert r.savings_pct < 0

    def test_fields_present(self):
        r = CompressionResult(original_size=10, compressed_size=5, algo=CompressionAlgo.GZIP, data=b"abc")
        assert r.original_size == 10
        assert r.compressed_size == 5
        assert r.algo is CompressionAlgo.GZIP
        assert r.data == b"abc"


# ---------------------------------------------------------------------------
# Per-algo round-trip
# ---------------------------------------------------------------------------


class TestCompressGzip:
    def test_round_trip(self):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.GZIP)
        assert c.decompress(result.data, CompressionAlgo.GZIP) == SAMPLE_TEXT

    def test_result_algo(self):
        c = DocCompressor()
        result = c.compress("hello", algo=CompressionAlgo.GZIP)
        assert result.algo is CompressionAlgo.GZIP

    def test_compressed_smaller_for_repeated(self):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.GZIP)
        assert result.compressed_size < result.original_size


class TestCompressZlib:
    def test_round_trip(self):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.ZLIB)
        assert c.decompress(result.data, CompressionAlgo.ZLIB) == SAMPLE_TEXT

    def test_result_algo(self):
        c = DocCompressor()
        result = c.compress("hello world", algo=CompressionAlgo.ZLIB)
        assert result.algo is CompressionAlgo.ZLIB


class TestCompressBz2:
    def test_round_trip(self):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.BZ2)
        assert c.decompress(result.data, CompressionAlgo.BZ2) == SAMPLE_TEXT

    def test_result_algo(self):
        c = DocCompressor()
        result = c.compress("data", algo=CompressionAlgo.BZ2)
        assert result.algo is CompressionAlgo.BZ2


class TestCompressLzma:
    def test_round_trip(self):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.LZMA)
        assert c.decompress(result.data, CompressionAlgo.LZMA) == SAMPLE_TEXT

    def test_result_algo(self):
        c = DocCompressor()
        result = c.compress("data", algo=CompressionAlgo.LZMA)
        assert result.algo is CompressionAlgo.LZMA


class TestCompressNone:
    def test_round_trip(self):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.NONE)
        assert c.decompress(result.data, CompressionAlgo.NONE) == SAMPLE_TEXT

    def test_no_compression(self):
        c = DocCompressor()
        text = "hello world"
        result = c.compress(text, algo=CompressionAlgo.NONE)
        assert result.compressed_size == len(text.encode("utf-8"))
        assert result.data == text.encode("utf-8")

    def test_ratio_one(self):
        c = DocCompressor()
        result = c.compress("abc", algo=CompressionAlgo.NONE)
        assert result.ratio == 1.0


# ---------------------------------------------------------------------------
# Compression levels
# ---------------------------------------------------------------------------


class TestCompressLevel:
    def test_gzip_higher_level_not_larger(self):
        c = DocCompressor()
        low = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.GZIP, level=1)
        high = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.GZIP, level=9)
        assert high.compressed_size <= low.compressed_size

    def test_zlib_higher_level_not_larger(self):
        c = DocCompressor()
        low = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.ZLIB, level=1)
        high = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.ZLIB, level=9)
        assert high.compressed_size <= low.compressed_size

    def test_bz2_round_trip_various_levels(self):
        c = DocCompressor()
        for level in (1, 5, 9):
            result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.BZ2, level=level)
            assert c.decompress(result.data, CompressionAlgo.BZ2) == SAMPLE_TEXT

    def test_lzma_round_trip_various_levels(self):
        c = DocCompressor()
        for level in (0, 6, 9):
            result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.LZMA, level=level)
            assert c.decompress(result.data, CompressionAlgo.LZMA) == SAMPLE_TEXT


# ---------------------------------------------------------------------------
# Round-trip across all algos
# ---------------------------------------------------------------------------


class TestRoundTripAllAlgos:
    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_round_trip(self, algo):
        c = DocCompressor()
        result = c.compress(SAMPLE_TEXT, algo=algo)
        assert c.decompress(result.data, algo) == SAMPLE_TEXT

    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_round_trip_short(self, algo):
        c = DocCompressor()
        text = "hi"
        result = c.compress(text, algo=algo)
        assert c.decompress(result.data, algo) == text

    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_original_size_correct(self, algo):
        c = DocCompressor()
        text = "hello"
        result = c.compress(text, algo=algo)
        assert result.original_size == len(text.encode("utf-8"))


# ---------------------------------------------------------------------------
# Base64
# ---------------------------------------------------------------------------


class TestCompressBase64:
    def test_round_trip_gzip(self):
        c = DocCompressor()
        b64 = c.compress_to_base64(SAMPLE_TEXT, algo=CompressionAlgo.GZIP)
        assert c.decompress_from_base64(b64, CompressionAlgo.GZIP) == SAMPLE_TEXT

    def test_round_trip_zlib(self):
        c = DocCompressor()
        b64 = c.compress_to_base64(SAMPLE_TEXT, algo=CompressionAlgo.ZLIB)
        assert c.decompress_from_base64(b64, CompressionAlgo.ZLIB) == SAMPLE_TEXT

    def test_round_trip_bz2(self):
        c = DocCompressor()
        b64 = c.compress_to_base64(SAMPLE_TEXT, algo=CompressionAlgo.BZ2)
        assert c.decompress_from_base64(b64, CompressionAlgo.BZ2) == SAMPLE_TEXT

    def test_round_trip_lzma(self):
        c = DocCompressor()
        b64 = c.compress_to_base64(SAMPLE_TEXT, algo=CompressionAlgo.LZMA)
        assert c.decompress_from_base64(b64, CompressionAlgo.LZMA) == SAMPLE_TEXT

    def test_round_trip_none(self):
        c = DocCompressor()
        b64 = c.compress_to_base64("plain text", algo=CompressionAlgo.NONE)
        assert c.decompress_from_base64(b64, CompressionAlgo.NONE) == "plain text"

    def test_is_ascii_string(self):
        c = DocCompressor()
        b64 = c.compress_to_base64(SAMPLE_TEXT, algo=CompressionAlgo.GZIP)
        # Should be pure ASCII
        b64.encode("ascii")  # would raise if not
        # And valid base64
        base64.b64decode(b64.encode("ascii"))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


class TestBenchmark:
    def test_returns_dict(self):
        c = DocCompressor()
        results = c.benchmark(SAMPLE_TEXT)
        assert isinstance(results, dict)

    def test_all_algos_present(self):
        c = DocCompressor()
        results = c.benchmark(SAMPLE_TEXT)
        for algo in CompressionAlgo:
            assert algo.name in results

    def test_results_are_compression_results(self):
        c = DocCompressor()
        results = c.benchmark(SAMPLE_TEXT)
        for v in results.values():
            assert isinstance(v, CompressionResult)

    def test_original_size_consistent(self):
        c = DocCompressor()
        results = c.benchmark(SAMPLE_TEXT)
        sizes = {r.original_size for r in results.values()}
        assert len(sizes) == 1  # all the same


# ---------------------------------------------------------------------------
# Recommend
# ---------------------------------------------------------------------------


class TestRecommend:
    def test_returns_valid_algo(self):
        c = DocCompressor()
        algo = c.recommend(SAMPLE_TEXT)
        assert isinstance(algo, CompressionAlgo)

    def test_recommend_short_text(self):
        c = DocCompressor()
        algo = c.recommend("x")
        assert isinstance(algo, CompressionAlgo)

    def test_recommend_repetitive_text_compresses(self):
        c = DocCompressor()
        text = "A" * 1000
        algo = c.recommend(text)
        # For highly repetitive text, recommended algo should beat NONE.
        rec_size = c.estimate_size(text, algo)
        none_size = c.estimate_size(text, CompressionAlgo.NONE)
        assert rec_size <= none_size


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------


class TestCompressBatch:
    def test_returns_list(self):
        c = DocCompressor()
        results = c.compress_batch(["a", "b", "c"], algo=CompressionAlgo.GZIP)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_each_is_result(self):
        c = DocCompressor()
        results = c.compress_batch(["one", "two"], algo=CompressionAlgo.ZLIB)
        for r in results:
            assert isinstance(r, CompressionResult)
            assert r.algo is CompressionAlgo.ZLIB

    def test_empty_input(self):
        c = DocCompressor()
        assert c.compress_batch([], algo=CompressionAlgo.GZIP) == []

    def test_round_trip_batch(self):
        c = DocCompressor()
        texts = ["alpha", "beta gamma", "delta"]
        results = c.compress_batch(texts, algo=CompressionAlgo.BZ2)
        decoded = [c.decompress(r.data, CompressionAlgo.BZ2) for r in results]
        assert decoded == texts


# ---------------------------------------------------------------------------
# Estimate size
# ---------------------------------------------------------------------------


class TestEstimateSize:
    def test_matches_compressed_size(self):
        c = DocCompressor()
        size = c.estimate_size(SAMPLE_TEXT, CompressionAlgo.GZIP)
        result = c.compress(SAMPLE_TEXT, algo=CompressionAlgo.GZIP)
        assert size == result.compressed_size

    def test_none_equals_utf8_length(self):
        c = DocCompressor()
        text = "abcdef"
        assert c.estimate_size(text, CompressionAlgo.NONE) == len(text.encode("utf-8"))

    def test_returns_int(self):
        c = DocCompressor()
        assert isinstance(c.estimate_size("hello", CompressionAlgo.LZMA), int)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_empty_text(self, algo):
        c = DocCompressor()
        result = c.compress("", algo=algo)
        assert c.decompress(result.data, algo) == ""

    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_unicode_text(self, algo):
        c = DocCompressor()
        text = "Привет, мир! 你好世界 こんにちは 🚀✨"
        result = c.compress(text, algo=algo)
        assert c.decompress(result.data, algo) == text

    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_very_short_text(self, algo):
        c = DocCompressor()
        result = c.compress("a", algo=algo)
        assert c.decompress(result.data, algo) == "a"
        assert result.original_size == 1

    @pytest.mark.parametrize("algo", list(CompressionAlgo))
    def test_newlines_and_tabs(self, algo):
        c = DocCompressor()
        text = "line1\nline2\tcol2\r\nline3"
        result = c.compress(text, algo=algo)
        assert c.decompress(result.data, algo) == text

    def test_empty_original_size_zero(self):
        c = DocCompressor()
        result = c.compress("", algo=CompressionAlgo.GZIP)
        assert result.original_size == 0

    def test_unicode_base64_round_trip(self):
        c = DocCompressor()
        text = "тест 漢字 emoji 🎉"
        b64 = c.compress_to_base64(text, algo=CompressionAlgo.GZIP)
        assert c.decompress_from_base64(b64, CompressionAlgo.GZIP) == text


# ---------------------------------------------------------------------------
# Large text
# ---------------------------------------------------------------------------


class TestLargeText:
    def _large_text(self) -> str:
        return ("The Lorenzo project is a knowledge OS prototype. " * 500)

    @pytest.mark.parametrize("algo", [
        CompressionAlgo.GZIP,
        CompressionAlgo.ZLIB,
        CompressionAlgo.BZ2,
        CompressionAlgo.LZMA,
    ])
    def test_compresses_smaller(self, algo):
        c = DocCompressor()
        result = c.compress(self._large_text(), algo=algo)
        assert result.compressed_size < result.original_size

    @pytest.mark.parametrize("algo", [
        CompressionAlgo.GZIP,
        CompressionAlgo.ZLIB,
        CompressionAlgo.BZ2,
        CompressionAlgo.LZMA,
    ])
    def test_ratio_below_one(self, algo):
        c = DocCompressor()
        result = c.compress(self._large_text(), algo=algo)
        assert 0.0 < result.ratio < 1.0

    @pytest.mark.parametrize("algo", [
        CompressionAlgo.GZIP,
        CompressionAlgo.ZLIB,
        CompressionAlgo.BZ2,
        CompressionAlgo.LZMA,
    ])
    def test_savings_positive(self, algo):
        c = DocCompressor()
        result = c.compress(self._large_text(), algo=algo)
        assert result.savings_pct > 0

    @pytest.mark.parametrize("algo", [
        CompressionAlgo.GZIP,
        CompressionAlgo.ZLIB,
        CompressionAlgo.BZ2,
        CompressionAlgo.LZMA,
    ])
    def test_round_trip_large(self, algo):
        c = DocCompressor()
        text = self._large_text()
        result = c.compress(text, algo=algo)
        assert c.decompress(result.data, algo) == text

    def test_recommend_picks_compressor(self):
        c = DocCompressor()
        text = self._large_text()
        algo = c.recommend(text)
        # For highly repetitive text, the recommended algo should not be NONE.
        assert algo is not CompressionAlgo.NONE
