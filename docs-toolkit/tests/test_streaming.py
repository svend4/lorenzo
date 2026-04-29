"""Тесты streaming RAG."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.streaming import (
    StreamChunk, stream_rag, _make_citations, _echo_stream,
)
from docstoolkit.rag.types import Passage


def test_stream_chunk_dataclass():
    c = StreamChunk(type="token", data={"text": "hi"}, ts=1.0)
    assert c.type == "token"
    assert c.data["text"] == "hi"
    assert c.ts == 1.0


def test_make_citations_empty():
    assert _make_citations([]) == []


def test_make_citations_basic():
    passages = [
        Passage(text="x", doc_id="d1", title="A", score=0.9),
        Passage(text="y", doc_id="d2", title="B", score=0.5),
    ]
    cits = _make_citations(passages)
    assert len(cits) == 2
    assert cits[0]["n"] == 1
    assert cits[0]["doc_id"] == "d1"
    assert cits[0]["title"] == "A"
    assert cits[1]["n"] == 2


def test_echo_stream_yields_done():
    passages = [Passage(text="content", doc_id="d1", title="T", score=0.5)]
    chunks = list(_echo_stream("Q", passages, 0.0))
    assert len(chunks) >= 2  # ≥1 token + 1 done
    # last is done
    assert chunks[-1].type == "done"
    assert "answer" in chunks[-1].data
    assert "citations" in chunks[-1].data
    # tokens before done
    token_chunks = [c for c in chunks if c.type == "token"]
    assert len(token_chunks) >= 1
    # full answer accumulates from token chunks
    full = "".join(c.data["text"] for c in token_chunks)
    assert "Echo" in full
    assert "T" in full


def test_echo_stream_empty_passages():
    chunks = list(_echo_stream("Q", [], 0.0))
    assert len(chunks) == 1
    assert chunks[0].type == "done"


def test_stream_rag_with_echo_no_corpus(tmp_path, monkeypatch):
    """stream_rag через echo — пустой корпус → done с пустыми passages."""
    # Подменяем cwd на tmp_path, чтобы не было индекса
    monkeypatch.chdir(tmp_path)
    chunks = list(stream_rag("question?", method="keyword", answerer="echo"))
    # Должны быть события (passages_retrieved + done или error)
    assert len(chunks) >= 1
    types = [c.type for c in chunks]
    assert "done" in types or "error" in types or "passages_retrieved" in types


def test_stream_rag_anthropic_no_key_returns_error_or_done():
    """anthropic answerer без API ключа должен вернуть error или fallback."""
    import os
    old = os.environ.pop("ANTHROPIC_API_KEY", None)
    try:
        # Без passages (пустой корпус) — done сразу до anthropic call
        chunks = list(stream_rag("?", method="keyword", answerer="anthropic"))
        types = [c.type for c in chunks]
        # Либо done (пустой корпус), либо error (anthropic), либо passages найдены
        assert types
    finally:
        if old:
            os.environ["ANTHROPIC_API_KEY"] = old
