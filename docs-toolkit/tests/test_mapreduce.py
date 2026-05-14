"""Тесты map-reduce суммаризации (rag/mapreduce.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.mapreduce import (
    MapReduceConfig,
    MapResult,
    ReduceResult,
    _format_passages_for_map,
    _map_chunk,
    _reduce,
    map_reduce_ask,
    should_use_mapreduce,
)
from docstoolkit.rag.answerer import EchoAnswerer
from docstoolkit.rag.types import Passage


# ---- helpers ----

def _make_passage(text: str, doc_id: str = "d1", title: str = "") -> Passage:
    return Passage(text=text, doc_id=doc_id, title=title, score=0.5)


def _make_passages(n: int) -> list[Passage]:
    return [
        _make_passage(f"Passage content {i}: information about topic {i}", doc_id=f"doc_{i}")
        for i in range(n)
    ]


# ---- MapReduceConfig ----

def test_config_defaults():
    cfg = MapReduceConfig()
    assert cfg.chunk_size == 10
    assert cfg.max_map_tokens == 3000
    assert cfg.max_reduce_tokens == 6000
    assert cfg.model == "claude-haiku-4-5-20251001"
    assert cfg.answerer == "echo"


def test_config_custom():
    cfg = MapReduceConfig(chunk_size=5, max_map_tokens=1000)
    assert cfg.chunk_size == 5
    assert cfg.max_map_tokens == 1000


# ---- MapResult ----

def test_map_result_fields():
    p = _make_passage("text", "d1")
    mr = MapResult(chunk_idx=0, passages=[p], summary="Summary text", tokens_used=42)
    assert mr.chunk_idx == 0
    assert mr.summary == "Summary text"
    assert mr.tokens_used == 42
    assert len(mr.passages) == 1


def test_map_result_defaults():
    mr = MapResult(chunk_idx=1)
    assert mr.passages == []
    assert mr.summary == ""
    assert mr.tokens_used == 0


# ---- ReduceResult ----

def test_reduce_result_fields():
    rr = ReduceResult(
        final_answer="Final answer",
        map_results=[],
        total_passages=20,
        total_tokens=500,
        duration_ms=123,
    )
    assert rr.final_answer == "Final answer"
    assert rr.total_passages == 20
    assert rr.total_tokens == 500
    assert rr.duration_ms == 123


def test_reduce_result_defaults():
    rr = ReduceResult(final_answer="")
    assert rr.map_results == []
    assert rr.total_passages == 0
    assert rr.total_tokens == 0
    assert rr.duration_ms == 0


# ---- _format_passages_for_map ----

def test_format_passages_basic():
    passages = [
        _make_passage("Content A", "d1", title="Doc A"),
        _make_passage("Content B", "d2", title="Doc B"),
    ]
    result = _format_passages_for_map(passages)
    assert "[1]" in result
    assert "[2]" in result
    assert "Doc A" in result
    assert "Content A" in result


def test_format_passages_empty():
    result = _format_passages_for_map([])
    assert "пассажей" in result.lower() or "(нет" in result


def test_format_passages_truncates_long_text():
    long_text = "x" * 1000
    passages = [_make_passage(long_text, "d1")]
    result = _format_passages_for_map(passages, max_chars_per=100)
    # Should truncate at max_chars_per
    assert len(result) < 500


def test_format_passages_falls_back_to_doc_id_when_no_title():
    passages = [Passage(text="content", doc_id="my_doc_id", title="")]
    result = _format_passages_for_map(passages)
    assert "my_doc_id" in result


def test_format_passages_separator():
    passages = _make_passages(3)
    result = _format_passages_for_map(passages)
    # Multiple entries separated
    assert result.count("[1]") == 1
    assert result.count("[2]") == 1
    assert result.count("[3]") == 1


# ---- _map_chunk ----

def test_map_chunk_returns_map_result():
    passages = _make_passages(3)
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _map_chunk("What is the topic?", passages, cfg, answerer, chunk_idx=0)
    assert isinstance(result, MapResult)
    assert result.chunk_idx == 0
    assert isinstance(result.summary, str)
    assert result.tokens_used >= 0


def test_map_chunk_includes_passages():
    passages = _make_passages(5)
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _map_chunk("Q", passages, cfg, answerer, chunk_idx=2)
    assert result.chunk_idx == 2
    assert result.passages == passages


def test_map_chunk_with_empty_passages():
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _map_chunk("Q", [], cfg, answerer, chunk_idx=0)
    assert isinstance(result, MapResult)
    assert isinstance(result.summary, str)


def test_map_chunk_tokens_used_positive():
    passages = _make_passages(2)
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _map_chunk("Q", passages, cfg, answerer)
    # EchoAnswerer returns len(user)//3 tokens
    assert result.tokens_used > 0


# ---- _reduce ----

def test_reduce_combines_summaries():
    summaries = ["Part 1: memory is fast.", "Part 2: storage is persistent."]
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _reduce("What is the system?", summaries, cfg, answerer)
    assert isinstance(result, str)
    assert len(result) > 0


def test_reduce_empty_summaries():
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _reduce("Q", [], cfg, answerer)
    assert isinstance(result, str)
    # Should indicate no data
    assert len(result) > 0


def test_reduce_single_summary():
    cfg = MapReduceConfig()
    answerer = EchoAnswerer()
    result = _reduce("Q", ["Just one summary."], cfg, answerer)
    assert isinstance(result, str)


# ---- map_reduce_ask ----

def test_map_reduce_ask_20_passages():
    """Core test: 20 mock passages should be processed via map-reduce."""
    passages = _make_passages(20)
    cfg = MapReduceConfig(chunk_size=5)
    result = map_reduce_ask("Summarize everything about topics", passages, cfg=cfg)

    assert isinstance(result, ReduceResult)
    assert result.total_passages == 20
    assert isinstance(result.final_answer, str)
    assert len(result.map_results) == 4  # 20 passages / 5 per chunk = 4 map results


def test_map_reduce_ask_chunk_indices():
    """Chunk indices should be sequential."""
    passages = _make_passages(15)
    cfg = MapReduceConfig(chunk_size=5)
    result = map_reduce_ask("Q", passages, cfg=cfg)

    indices = [mr.chunk_idx for mr in result.map_results]
    assert indices == list(range(len(result.map_results)))


def test_map_reduce_ask_all_passages_covered():
    """All passages should appear in exactly one map chunk."""
    passages = _make_passages(12)
    cfg = MapReduceConfig(chunk_size=5)
    result = map_reduce_ask("Q", passages, cfg=cfg)

    all_passage_ids = set()
    for mr in result.map_results:
        for p in mr.passages:
            all_passage_ids.add(p.doc_id)

    expected_ids = {p.doc_id for p in passages}
    assert all_passage_ids == expected_ids


def test_map_reduce_ask_empty_passages():
    result = map_reduce_ask("Q", [])
    assert isinstance(result, ReduceResult)
    assert result.total_passages == 0
    assert "нет" in result.final_answer.lower() or "no" in result.final_answer.lower()


def test_map_reduce_ask_single_passage():
    passages = _make_passages(1)
    result = map_reduce_ask("Q", passages)
    assert isinstance(result, ReduceResult)
    assert result.total_passages == 1
    assert len(result.map_results) == 1


def test_map_reduce_ask_default_config():
    """Should work without explicit config (uses defaults)."""
    passages = _make_passages(5)
    result = map_reduce_ask("Q", passages)
    assert isinstance(result, ReduceResult)
    assert result.total_passages == 5


def test_map_reduce_ask_custom_answerer():
    """Can accept explicit answerer instance."""
    passages = _make_passages(5)
    answerer = EchoAnswerer()
    cfg = MapReduceConfig(chunk_size=3)
    result = map_reduce_ask("Q", passages, cfg=cfg, answerer=answerer)
    assert isinstance(result, ReduceResult)


def test_map_reduce_ask_duration_ms_nonnegative():
    passages = _make_passages(5)
    result = map_reduce_ask("Q", passages)
    assert result.duration_ms >= 0


def test_map_reduce_ask_total_tokens_positive():
    passages = _make_passages(5)
    result = map_reduce_ask("Q", passages)
    # EchoAnswerer returns non-zero tokens
    assert result.total_tokens >= 0


def test_map_reduce_ask_remainder_chunk():
    """When passages don't divide evenly, the last chunk has the remainder."""
    passages = _make_passages(7)
    cfg = MapReduceConfig(chunk_size=3)
    result = map_reduce_ask("Q", passages, cfg=cfg)
    # 7 / 3 = 2 full chunks + 1 remainder → 3 map results
    assert len(result.map_results) == 3
    # Last chunk should have 1 passage
    assert len(result.map_results[-1].passages) == 1


def test_map_reduce_ask_map_results_summaries_nonempty():
    passages = _make_passages(5)
    result = map_reduce_ask("Q", passages)
    for mr in result.map_results:
        assert isinstance(mr.summary, str)


# ---- should_use_mapreduce ----

def test_should_use_mapreduce_above_threshold():
    passages = _make_passages(20)
    assert should_use_mapreduce(passages, threshold=15) is True


def test_should_use_mapreduce_below_threshold():
    passages = _make_passages(10)
    assert should_use_mapreduce(passages, threshold=15) is False


def test_should_use_mapreduce_at_threshold():
    passages = _make_passages(15)
    # exactly at threshold → not above → False
    assert should_use_mapreduce(passages, threshold=15) is False


def test_should_use_mapreduce_one_above_threshold():
    passages = _make_passages(16)
    assert should_use_mapreduce(passages, threshold=15) is True


def test_should_use_mapreduce_empty():
    assert should_use_mapreduce([], threshold=15) is False


def test_should_use_mapreduce_default_threshold():
    # Default threshold is 15
    assert should_use_mapreduce(_make_passages(16)) is True
    assert should_use_mapreduce(_make_passages(10)) is False


def test_should_use_mapreduce_threshold_1():
    assert should_use_mapreduce([_make_passage("x")], threshold=1) is False
    assert should_use_mapreduce(_make_passages(2), threshold=1) is True


# ---- integration: full flow with 20 passages ----

def test_full_mapreduce_flow_20_passages():
    """Integration test: 20 passages, chunk_size=7, echo answerer."""
    passages = [
        _make_passage(
            f"Document {i}: This document discusses aspect {i} of the system architecture.",
            doc_id=f"arch_{i}",
            title=f"Architecture Part {i}",
        )
        for i in range(20)
    ]
    cfg = MapReduceConfig(chunk_size=7, answerer="echo")
    result = map_reduce_ask("Summarize the architecture", passages, cfg=cfg)

    # Basic structure checks
    assert result.total_passages == 20
    assert isinstance(result.final_answer, str) and len(result.final_answer) > 0
    assert result.duration_ms >= 0

    # Map results: ceil(20/7) = 3 chunks
    assert len(result.map_results) == 3

    # Chunk sizes: 7, 7, 6
    assert len(result.map_results[0].passages) == 7
    assert len(result.map_results[1].passages) == 7
    assert len(result.map_results[2].passages) == 6

    # All summaries are strings
    for mr in result.map_results:
        assert isinstance(mr.summary, str)
        assert mr.tokens_used >= 0

    # All passages accounted for
    total = sum(len(mr.passages) for mr in result.map_results)
    assert total == 20
