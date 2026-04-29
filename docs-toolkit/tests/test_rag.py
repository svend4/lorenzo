"""Тесты RAG pipeline."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.types import Passage, RAGQuery, AnswerResult
from docstoolkit.rag.assembler import assemble_prompt, _truncate_to_tokens
from docstoolkit.rag.answerer import EchoAnswerer, get_answerer


def test_passage_dataclass():
    p = Passage(text="hello", doc_id="d1", title="T", score=0.5)
    assert p.text == "hello"
    assert p.score == 0.5


def test_rag_query_defaults():
    q = RAGQuery(question="?")
    assert q.top_k == 5
    assert q.method == "hybrid"
    assert q.answerer == "echo"


def test_assemble_prompt_basic():
    passages = [
        Passage(text="Yodoca uses hot path", doc_id="d1", title="Yodoca", score=0.5),
        Passage(text="NGT memory is different", doc_id="d2", title="NGT", score=0.3),
    ]
    system, user = assemble_prompt("What is Yodoca?", passages)
    assert "RAG" in system or "пассаж" in system.lower()
    assert "What is Yodoca?" in user
    assert "[1]" in user
    assert "[2]" in user
    assert "Yodoca" in user
    assert "NGT" in user


def test_assemble_prompt_no_passages():
    system, user = assemble_prompt("?", [])
    assert "нет пассажей" in user.lower() or "no passages" in user.lower()


def test_assemble_prompt_truncation():
    huge = "x" * 100000
    passages = [Passage(text=huge, doc_id="d1")]
    system, user = assemble_prompt("?", passages, max_context_tokens=100)
    assert len(user) < 5000  # должно быть обрезано


def test_truncate_to_tokens():
    short = "small text"
    assert _truncate_to_tokens(short, 100) == short
    long = "x" * 1000
    truncated = _truncate_to_tokens(long, 10)
    assert len(truncated) < 100
    assert "truncated" in truncated.lower()


def test_echo_answerer_finds_first_passage():
    ea = EchoAnswerer()
    user = ("Q\n[1] **Title One**\nИсточник: `path/to/doc.md`\n\n"
            "Some content text here.\n---\n[2] **Title Two**\n...")
    answer, tokens, cost = ea.answer("system", user)
    assert "Title One" in answer
    assert "path/to/doc.md" in answer
    assert "Some content" in answer
    assert tokens > 0
    assert cost == 0.0


def test_echo_answerer_no_passages():
    ea = EchoAnswerer()
    answer, tokens, cost = ea.answer("system", "Q without passages")
    assert "Нет пассажей" in answer or "no passages" in answer.lower()


def test_get_answerer_echo():
    a = get_answerer("echo")
    assert a.name == "echo"


def test_get_answerer_unknown_falls_back():
    a = get_answerer("nonexistent")
    assert a.name == "echo"


def test_get_answerer_anthropic_without_pkg_falls_back():
    """Если anthropic не установлен — get_answerer вернёт EchoAnswerer."""
    a = get_answerer("anthropic")
    # Может быть EchoAnswerer (если anthropic не установлен) или AnthropicAnswerer
    assert a.name in ("echo", "anthropic")


def test_answer_result_to_markdown():
    r = AnswerResult(
        answer="The answer",
        citations=[{"title": "X", "doc_id": "d1", "score": 0.5}],
        query="Q",
        duration_ms=100,
        tokens_used=50,
    )
    md = r.to_markdown()
    assert "# Q" in md
    assert "The answer" in md
    assert "## Источники" in md
    assert "X" in md
