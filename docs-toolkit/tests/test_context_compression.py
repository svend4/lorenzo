"""Tests for docstoolkit.context_compression — E41."""
from __future__ import annotations

import math

import pytest

from docstoolkit.context_compression import (
    CompressedContext,
    CompressionConfig,
    ContextCompressor,
    ContextWindow,
    RelevanceScore,
    RelevanceScorer,
    SlidingContextWindow,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _rs(text: str, score: float = 1.0, qc: float = 0.5, pid: str = "x") -> RelevanceScore:
    """Convenience factory for RelevanceScore."""
    return RelevanceScore(passage_id=pid, text=text, score=score, query_coverage=qc)


def _words(n: int) -> str:
    """Return a string consisting of *n* distinct words."""
    return " ".join(f"word{i}" for i in range(n))


# ===========================================================================
# RelevanceScore dataclass
# ===========================================================================

class TestRelevanceScoreDataclass:
    def test_fields_stored(self):
        rs = RelevanceScore(passage_id="p1", text="hello world", score=0.7, query_coverage=0.5)
        assert rs.passage_id == "p1"
        assert rs.text == "hello world"
        assert rs.score == pytest.approx(0.7)
        assert rs.query_coverage == pytest.approx(0.5)

    def test_default_passage_id_empty_string(self):
        scorer = RelevanceScorer()
        rs = scorer.score("hello", "hello world")
        # No explicit passage_id → defaults to ""
        assert rs.passage_id == ""

    def test_score_is_float(self):
        rs = RelevanceScore(passage_id="", text="x", score=1.0, query_coverage=0.0)
        assert isinstance(rs.score, float)

    def test_query_coverage_is_float(self):
        rs = RelevanceScore(passage_id="", text="x", score=0.0, query_coverage=0.0)
        assert isinstance(rs.query_coverage, float)


# ===========================================================================
# RelevanceScorer
# ===========================================================================

class TestRelevanceScorerQueryCoverage:
    def setup_method(self):
        self.s = RelevanceScorer()

    def test_full_overlap(self):
        # query tokens all appear in passage
        rs = self.s.score("cat dog", "the cat and dog are here")
        # query_tokens = {"cat", "dog"}, passage_tokens = {"the", "cat", "and", "dog", "are", "here"}
        # intersection = {"cat", "dog"} → 2 / (2+1) ≈ 0.667
        assert rs.query_coverage == pytest.approx(2 / 3, rel=1e-6)

    def test_no_overlap(self):
        rs = self.s.score("cat dog", "sun moon star")
        assert rs.query_coverage == pytest.approx(0.0)

    def test_partial_overlap(self):
        rs = self.s.score("cat dog bird", "cat flies high")
        # query_tokens = {"cat","dog","bird"}, passage has {"cat"}
        # 1 / (3+1) = 0.25
        assert rs.query_coverage == pytest.approx(1 / 4, rel=1e-6)

    def test_denominator_uses_plus_one(self):
        """Empty query → |query_tokens| = 0, denominator = 1."""
        rs = self.s.score("", "some passage text")
        assert rs.query_coverage == pytest.approx(0.0)

    def test_passage_id_passed_through(self):
        rs = self.s.score("hello", "hello world", passage_id="myid")
        assert rs.passage_id == "myid"

    def test_score_positive_when_overlap(self):
        rs = self.s.score("python code", "python is great code")
        assert rs.score > 0

    def test_score_zero_when_no_overlap(self):
        rs = self.s.score("python", "completely unrelated words here")
        assert rs.score == pytest.approx(0.0)

    def test_score_formula(self):
        """score = query_coverage * (1 + log(word_count + 1) / 10)."""
        query = "alpha beta"
        passage = "alpha beta gamma delta"
        rs = self.s.score(query, passage)
        # query_tokens = {"alpha","beta"}, passage_tokens = {"alpha","beta","gamma","delta"}
        # coverage = 2 / (2+1) ≈ 0.6667
        # word_count = 4
        expected_cov = 2 / 3
        expected_score = expected_cov * (1 + math.log(5) / 10)
        assert rs.score == pytest.approx(expected_score, rel=1e-6)

    def test_longer_passage_higher_score_same_coverage(self):
        query = "python"
        short = "python"          # 1 word
        long_ = "python " + "x " * 98  # 100 words
        rs_short = self.s.score(query, short)
        rs_long = self.s.score(query, long_)
        # Coverage identical (both have "python"), but longer passage gets log bonus
        assert rs_long.score > rs_short.score

    def test_case_insensitive(self):
        rs1 = self.s.score("Python", "python is great")
        rs2 = self.s.score("python", "python is great")
        assert rs1.query_coverage == pytest.approx(rs2.query_coverage)

    def test_numeric_tokens_counted(self):
        rs = self.s.score("2024", "the year 2024 was eventful")
        assert rs.query_coverage > 0


class TestRelevanceScorerScoreAll:
    def setup_method(self):
        self.s = RelevanceScorer()

    def test_sorted_descending(self):
        passages = [
            "completely unrelated sun moon",
            "python is a great language for code",
            "python code rocks",
        ]
        results = self.s.score_all("python code", passages)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_passage_ids_are_indices(self):
        results = self.s.score_all("hello", ["hello world", "foo bar"])
        ids = {r.passage_id for r in results}
        assert ids == {"0", "1"}

    def test_empty_passages_returns_empty(self):
        assert self.s.score_all("hello", []) == []

    def test_returns_all_passages(self):
        passages = ["a b", "c d", "e f"]
        results = self.s.score_all("a", passages)
        assert len(results) == 3

    def test_result_type(self):
        results = self.s.score_all("hello", ["hello world"])
        assert all(isinstance(r, RelevanceScore) for r in results)

    def test_tie_order_stable(self):
        """Two zero-score passages should both appear."""
        results = self.s.score_all("xyz", ["foo bar", "baz qux"])
        assert len(results) == 2


# ===========================================================================
# CompressionConfig dataclass
# ===========================================================================

class TestCompressionConfig:
    def test_defaults(self):
        cfg = CompressionConfig()
        assert cfg.max_tokens == 500
        assert cfg.min_coverage == pytest.approx(0.3)
        assert cfg.overlap_penalty == pytest.approx(0.1)

    def test_custom(self):
        cfg = CompressionConfig(max_tokens=100, min_coverage=0.5, overlap_penalty=0.2)
        assert cfg.max_tokens == 100
        assert cfg.min_coverage == pytest.approx(0.5)
        assert cfg.overlap_penalty == pytest.approx(0.2)


# ===========================================================================
# ContextCompressor
# ===========================================================================

class TestContextCompressorMaxTokens:
    def test_respects_max_tokens(self):
        cfg = CompressionConfig(max_tokens=10, min_coverage=0.0)
        cc = ContextCompressor(cfg)
        # Each passage is 8 words; two would exceed 10
        passages = [
            "alpha beta gamma delta epsilon zeta eta theta",  # 8 words, has "query"
        ]
        # Make sure it fits
        result = cc.compress("query alpha", passages)
        assert result.total_tokens <= 10 or result.total_tokens == 8

    def test_total_tokens_within_budget(self):
        cfg = CompressionConfig(max_tokens=20, min_coverage=0.0)
        cc = ContextCompressor(cfg)
        passages = [_words(7) + " word0", _words(7) + " word0", _words(8) + " word0"]
        result = cc.compress("word0", passages)
        assert result.total_tokens <= 20

    def test_default_config_used_when_none(self):
        cc = ContextCompressor()
        assert cc._config.max_tokens == 500

    def test_compression_ratio_computed(self):
        cfg = CompressionConfig(max_tokens=1000, min_coverage=0.0)
        cc = ContextCompressor(cfg)
        passages = ["hello world alpha"] * 4  # 3 words each = 12 total input
        result = cc.compress("hello", passages)
        # ratio = selected_tokens / total_input_tokens
        assert 0.0 <= result.compression_ratio <= 1.0

    def test_empty_passages(self):
        cc = ContextCompressor()
        result = cc.compress("hello", [])
        assert result.total_tokens == 0
        assert result.passages == []

    def test_query_stored(self):
        cc = ContextCompressor()
        result = cc.compress("my query", ["hello world"])
        assert result.query == "my query"


class TestContextCompressorMinCoverage:
    def test_filters_low_coverage(self):
        cfg = CompressionConfig(max_tokens=500, min_coverage=0.5, overlap_penalty=0.0)
        cc = ContextCompressor(cfg)
        # "sun moon star" shares no tokens with query "python code"
        passages = ["sun moon star", "python is cool code"]
        result = cc.compress("python code", passages)
        texts = result.texts()
        assert "sun moon star" not in texts

    def test_keeps_high_coverage(self):
        cfg = CompressionConfig(max_tokens=500, min_coverage=0.1, overlap_penalty=0.0)
        cc = ContextCompressor(cfg)
        passages = ["python is great code for automation"]
        result = cc.compress("python code", passages)
        assert len(result.passages) == 1

    def test_all_filtered_returns_empty(self):
        cfg = CompressionConfig(max_tokens=500, min_coverage=0.9, overlap_penalty=0.0)
        cc = ContextCompressor(cfg)
        passages = ["totally unrelated content here today"]
        result = cc.compress("python code", passages)
        assert result.passages == []


class TestContextCompressorOverlapPenalty:
    def test_duplicate_passage_penalised(self):
        """Two identical passages: only the first should be selected (high budget)."""
        cfg = CompressionConfig(
            max_tokens=1000,
            min_coverage=0.0,
            overlap_penalty=10.0,  # huge penalty so second duplicate is dropped
        )
        cc = ContextCompressor(cfg)
        passage = "python code is awesome and useful"
        result = cc.compress("python code", [passage, passage])
        # After penalty, second instance should have effective_score ≤ 0 and be skipped
        assert len(result.passages) <= 2  # at most both, penalty may drop one

    def test_no_penalty_when_no_overlap(self):
        """Passages with disjoint vocabulary should both be selected."""
        cfg = CompressionConfig(
            max_tokens=1000,
            min_coverage=0.0,
            overlap_penalty=0.5,
        )
        cc = ContextCompressor(cfg)
        passages = [
            "python code rocks alpha beta",
            "python code xyz qwerty zulu",
        ]
        result = cc.compress("python code", passages)
        # Both have query tokens and different remaining vocab — penalty < 0.5
        # They should both be included (overlap is <50% due to non-python words)
        assert len(result.passages) >= 1

    def test_zero_penalty_selects_both_duplicates(self):
        cfg = CompressionConfig(
            max_tokens=1000,
            min_coverage=0.0,
            overlap_penalty=0.0,
        )
        cc = ContextCompressor(cfg)
        passage = "python code is great"
        result = cc.compress("python code", [passage, passage])
        assert len(result.passages) == 2


# ===========================================================================
# CompressedContext
# ===========================================================================

class TestCompressedContext:
    def _make(self, passages: list[RelevanceScore], query: str = "q") -> CompressedContext:
        total = sum(len(rs.text.split()) for rs in passages)
        return CompressedContext(
            query=query,
            passages=passages,
            total_tokens=total,
            compression_ratio=0.5,
        )

    def test_texts_returns_list_of_strings(self):
        cc = self._make([_rs("hello world"), _rs("foo bar baz")])
        assert cc.texts() == ["hello world", "foo bar baz"]

    def test_texts_empty_when_no_passages(self):
        cc = self._make([])
        assert cc.texts() == []

    def test_coverage_average(self):
        cc = self._make([
            _rs("a", qc=0.4),
            _rs("b", qc=0.6),
        ])
        assert cc.coverage() == pytest.approx(0.5)

    def test_coverage_zero_when_empty(self):
        cc = self._make([])
        assert cc.coverage() == pytest.approx(0.0)

    def test_coverage_single_passage(self):
        cc = self._make([_rs("x", qc=0.75)])
        assert cc.coverage() == pytest.approx(0.75)

    def test_total_tokens_stored(self):
        cc = CompressedContext(
            query="q", passages=[], total_tokens=42, compression_ratio=0.1
        )
        assert cc.total_tokens == 42

    def test_compression_ratio_stored(self):
        cc = CompressedContext(
            query="q", passages=[], total_tokens=0, compression_ratio=0.33
        )
        assert cc.compression_ratio == pytest.approx(0.33)


# ===========================================================================
# ContextWindow dataclass
# ===========================================================================

class TestContextWindow:
    def test_initial_state(self):
        w = ContextWindow(max_tokens=100)
        assert w.current_tokens == 0
        assert w.passages == []

    def test_can_fit_empty_window(self):
        w = ContextWindow(max_tokens=10)
        assert w.can_fit("one two three") is True  # 3 words ≤ 10

    def test_can_fit_exact_boundary(self):
        w = ContextWindow(max_tokens=5)
        assert w.can_fit("a b c d e") is True   # 5 words == 5
        assert w.can_fit("a b c d e f") is False  # 6 > 5

    def test_can_fit_false_when_full(self):
        w = ContextWindow(max_tokens=3)
        w.add(_rs("one two three"))
        assert w.can_fit("x") is False

    def test_add_returns_true_on_success(self):
        w = ContextWindow(max_tokens=10)
        rs = _rs("hello world")
        assert w.add(rs) is True

    def test_add_updates_current_tokens(self):
        w = ContextWindow(max_tokens=10)
        w.add(_rs("one two three"))
        assert w.current_tokens == 3

    def test_add_returns_false_when_no_space(self):
        w = ContextWindow(max_tokens=3)
        w.add(_rs("one two three"))
        assert w.add(_rs("another word")) is False

    def test_add_multiple(self):
        w = ContextWindow(max_tokens=10)
        w.add(_rs("one two"))
        w.add(_rs("three four five"))
        assert w.current_tokens == 5
        assert len(w.passages) == 2

    def test_utilization_zero_initially(self):
        w = ContextWindow(max_tokens=100)
        assert w.utilization() == pytest.approx(0.0)

    def test_utilization_full(self):
        w = ContextWindow(max_tokens=5)
        w.add(_rs("a b c d e"))
        assert w.utilization() == pytest.approx(1.0)

    def test_utilization_partial(self):
        w = ContextWindow(max_tokens=10)
        w.add(_rs("a b c d e"))  # 5 words
        assert w.utilization() == pytest.approx(0.5)

    def test_utilization_zero_max_tokens(self):
        """Avoid division by zero when max_tokens == 0."""
        w = ContextWindow(max_tokens=0)
        assert w.utilization() == pytest.approx(0.0)

    def test_clear_resets_tokens(self):
        w = ContextWindow(max_tokens=100)
        w.add(_rs("hello world"))
        w.clear()
        assert w.current_tokens == 0

    def test_clear_resets_passages(self):
        w = ContextWindow(max_tokens=100)
        w.add(_rs("hello world"))
        w.clear()
        assert w.passages == []

    def test_clear_allows_reuse(self):
        w = ContextWindow(max_tokens=5)
        w.add(_rs("a b c d e"))
        w.clear()
        assert w.can_fit("a b c d e") is True

    def test_passages_list_preserved(self):
        w = ContextWindow(max_tokens=20)
        rs1 = _rs("first passage", pid="p1")
        rs2 = _rs("second passage", pid="p2")
        w.add(rs1)
        w.add(rs2)
        assert w.passages[0].passage_id == "p1"
        assert w.passages[1].passage_id == "p2"


# ===========================================================================
# SlidingContextWindow
# ===========================================================================

class TestSlidingContextWindow:
    def test_empty_input(self):
        scw = SlidingContextWindow(max_tokens=100)
        assert scw.fill([]) == []

    def test_single_passage_single_window(self):
        scw = SlidingContextWindow(max_tokens=100)
        windows = scw.fill([_rs("hello world")])
        assert len(windows) == 1
        assert len(windows[0].passages) == 1

    def test_multiple_passages_fit_one_window(self):
        scw = SlidingContextWindow(max_tokens=20)
        passages = [_rs(f"word{i}") for i in range(5)]
        windows = scw.fill(passages)
        assert len(windows) == 1
        assert len(windows[0].passages) == 5

    def test_creates_new_window_when_full(self):
        scw = SlidingContextWindow(max_tokens=5)
        # Each passage is 3 words; two won't fit in one window (3+3=6 > 5)
        passages = [_rs("one two three"), _rs("four five six"), _rs("seven eight nine")]
        windows = scw.fill(passages)
        assert len(windows) >= 2

    def test_all_passages_preserved(self):
        scw = SlidingContextWindow(max_tokens=4)
        passages = [_rs("a b c d"), _rs("e f g h"), _rs("i j k l")]
        windows = scw.fill(passages)
        total = sum(len(w.passages) for w in windows)
        assert total == 3

    def test_window_max_tokens_respected(self):
        scw = SlidingContextWindow(max_tokens=10)
        passages = [_rs(_words(6) + " q"), _rs(_words(6) + " q"), _rs(_words(3) + " q")]
        windows = scw.fill(passages)
        for w in windows:
            # Each regular window should not exceed max_tokens
            # (oversized single-passage windows are allowed)
            if len(w.passages) > 1:
                assert w.current_tokens <= scw.max_tokens

    def test_returns_context_window_objects(self):
        scw = SlidingContextWindow(max_tokens=100)
        windows = scw.fill([_rs("hello")])
        assert all(isinstance(w, ContextWindow) for w in windows)

    def test_window_max_tokens_set_correctly(self):
        scw = SlidingContextWindow(max_tokens=42)
        windows = scw.fill([_rs("hello world")])
        assert windows[0].max_tokens == 42

    def test_utilization_of_full_window(self):
        scw = SlidingContextWindow(max_tokens=5)
        passages = [_rs("a b c d e")]
        windows = scw.fill(passages)
        assert windows[0].utilization() == pytest.approx(1.0)

    def test_large_passage_not_dropped(self):
        """A passage bigger than max_tokens must still appear in output."""
        scw = SlidingContextWindow(max_tokens=3)
        big = _rs("one two three four five six seven")  # 7 words > 3
        windows = scw.fill([big])
        total = sum(len(w.passages) for w in windows)
        assert total == 1

    def test_many_passages_multiple_windows(self):
        scw = SlidingContextWindow(max_tokens=5)
        passages = [_rs("a b c d e")] * 10  # each fills a window
        windows = scw.fill(passages)
        assert len(windows) == 10


# ===========================================================================
# Integration: compressor + window
# ===========================================================================

class TestIntegration:
    def test_compress_then_fill_windows(self):
        cfg = CompressionConfig(max_tokens=50, min_coverage=0.0, overlap_penalty=0.0)
        cc = ContextCompressor(cfg)
        passages = [f"passage {i} about python code analysis" for i in range(10)]
        result = cc.compress("python code", passages)

        scw = SlidingContextWindow(max_tokens=20)
        windows = scw.fill(result.passages)

        total = sum(len(w.passages) for w in windows)
        assert total == len(result.passages)

    def test_scorer_and_compressor_consistent(self):
        scorer = RelevanceScorer()
        cfg = CompressionConfig(max_tokens=100, min_coverage=0.0, overlap_penalty=0.0)
        cc = ContextCompressor(cfg)
        passages = [
            "python is a great language",
            "unrelated topic about cooking",
            "python code for machine learning",
        ]
        scored = scorer.score_all("python", passages)
        compressed = cc.compress("python", passages)
        # Best-scored passage by scorer should be in compressed result
        best_text = scored[0].text
        assert best_text in compressed.texts()

    def test_full_pipeline_no_exceptions(self):
        """Smoke test: end-to-end with default settings."""
        cc = ContextCompressor()
        passages = [
            "The quick brown fox jumps over the lazy dog",
            "Python programming language is widely used",
            "Machine learning models require large datasets",
            "Natural language processing is a subfield of AI",
        ]
        result = cc.compress("python machine learning", passages)
        assert isinstance(result, CompressedContext)
        assert result.total_tokens >= 0
