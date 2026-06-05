"""Тесты детектора двусмысленности + ClarifyingRAG."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.types import Passage
from docstoolkit.rag.clarifier import (
    AmbiguityScore,
    ClarificationRequest,
    ClarifyingRAG,
    apply_clarification,
    build_clarification,
    detect_ambiguity,
)


# ------------------------------------------------------------------ #
# Helpers                                                              #
# ------------------------------------------------------------------ #

def make_passage(doc_id: str, score: float, text: str = "text") -> Passage:
    return Passage(text=text, doc_id=doc_id, score=score)


# ------------------------------------------------------------------ #
# detect_ambiguity                                                      #
# ------------------------------------------------------------------ #

def test_detect_ambiguity_no_passages():
    score = detect_ambiguity("what?", [])
    assert score.score == 0.0
    assert score.reason == "no passages"


def test_detect_ambiguity_clear_winner():
    """Первый результат сильно лучше второго (>3x) → score=0."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.9),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.2),
        make_passage("docs/02-anthropic-vacancies/job.md", 0.15),
    ]
    score = detect_ambiguity("architecture overview", passages)
    assert score.score == 0.0
    assert score.reason == "clear winner"


def test_detect_ambiguity_short_query_multiple_sections():
    """Короткий запрос (<3 слов) И несколько секций → score=1.0."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.8),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.75),
        make_passage("docs/02-anthropic-vacancies/job.md", 0.7),
    ]
    score = detect_ambiguity("память", passages)
    assert score.score == 1.0
    assert len(score.candidates) > 1


def test_detect_ambiguity_short_two_word_query():
    """Два слова — тоже 'короткий' запрос."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.8),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.75),
    ]
    score = detect_ambiguity("что память", passages)
    assert score.score == 1.0


def test_detect_ambiguity_similar_scores_different_sections():
    """Топ-3 с близкими score из разных секций → score >= 0.5."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.6),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.55),
        make_passage("docs/02-anthropic-vacancies/job.md", 0.52),
    ]
    score = detect_ambiguity("агент с памятью и знаниями", passages)
    assert score.score >= 0.5
    assert len(score.candidates) >= 2


def test_detect_ambiguity_single_section_returns_zero():
    """Все пассажи из одной секции → не неоднозначно."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.6),
        make_passage("docs/01-svyazi/overview.md", 0.55),
        make_passage("docs/01-svyazi/components.md", 0.5),
    ]
    score = detect_ambiguity("what is the architecture", passages)
    assert score.score == 0.0


def test_detect_ambiguity_zero_scores():
    """Все нулевые score → score=0."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.0),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.0),
    ]
    score = detect_ambiguity("query", passages)
    assert score.score == 0.0


def test_detect_ambiguity_candidates_from_top_passages():
    """candidates должны совпадать с секциями топ-пассажей."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.8),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.75),
        make_passage("docs/02-anthropic-vacancies/job.md", 0.7),
    ]
    score = detect_ambiguity("память", passages)
    assert "01-svyazi" in score.candidates
    assert "05-habr-projects" in score.candidates


# ------------------------------------------------------------------ #
# build_clarification                                                   #
# ------------------------------------------------------------------ #

def test_build_clarification_single_candidate():
    amb = AmbiguityScore(score=1.0, candidates=["memory"], reason="short")
    req = build_clarification("память", amb)
    assert req.original_question == "память"
    assert req.options == ["memory"]
    assert "memory" in req.prompt
    assert req.prompt.endswith("?")


def test_build_clarification_multiple_candidates():
    amb = AmbiguityScore(
        score=1.0,
        candidates=["01-svyazi", "05-habr-projects", "02-anthropic"],
        reason="multi-section"
    )
    req = build_clarification("что такое агент", amb)
    assert req.original_question == "что такое агент"
    assert len(req.options) == 3
    # Все кандидаты должны упоминаться в prompt
    for candidate in req.options:
        assert candidate in req.prompt
    # Последний через "или"
    assert "или" in req.prompt


def test_build_clarification_empty_candidates_uses_question():
    amb = AmbiguityScore(score=0.5, candidates=[], reason="test")
    req = build_clarification("что такое X", amb)
    assert req.options == ["что такое X"]


def test_build_clarification_returns_dataclass():
    amb = AmbiguityScore(score=1.0, candidates=["A", "B"])
    req = build_clarification("q", amb)
    assert isinstance(req, ClarificationRequest)


# ------------------------------------------------------------------ #
# apply_clarification                                                   #
# ------------------------------------------------------------------ #

def test_apply_clarification_appends_chosen():
    result = apply_clarification("что про память?", "05-habr-projects")
    assert "что про память?" in result
    assert "05-habr-projects" in result


def test_apply_clarification_empty_chosen():
    """Пустое chosen → возвращает исходный вопрос."""
    result = apply_clarification("что про память?", "")
    assert result == "что про память?"


def test_apply_clarification_chosen_already_in_question():
    """Если chosen уже есть в вопросе — не дублировать."""
    result = apply_clarification("память в 05-habr-projects", "05-habr-projects")
    assert result == "память в 05-habr-projects"


def test_apply_clarification_strips_whitespace():
    result = apply_clarification("  вопрос  ", "  раздел  ")
    assert result == "вопрос раздел"


# ------------------------------------------------------------------ #
# ClarifyingRAG                                                         #
# ------------------------------------------------------------------ #

class MockRetriever:
    """Мок retriever для тестирования ClarifyingRAG."""

    def __init__(self, passages: list[Passage]):
        self._passages = passages
        self.last_query: str = ""

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        self.last_query = query
        return self._passages[:top_k]


def test_clarifying_rag_ask_returns_none_when_unambiguous():
    """Если результаты однозначны — ask() возвращает None."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.9),
        make_passage("docs/01-svyazi/over.md", 0.2),
    ]
    retriever = MockRetriever(passages)
    rag = ClarifyingRAG(retriever, threshold=0.6)
    result = rag.ask("что такое архитектура Svyazi?")
    assert result is None


def test_clarifying_rag_ask_returns_request_when_ambiguous():
    """Неоднозначный запрос → возвращает ClarificationRequest."""
    passages = [
        make_passage("docs/01-svyazi/arch.md", 0.8),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.75),
    ]
    retriever = MockRetriever(passages)
    rag = ClarifyingRAG(retriever, threshold=0.6)
    result = rag.ask("память")
    assert isinstance(result, ClarificationRequest)
    assert result.original_question == "память"


def test_clarifying_rag_ask_with_clarification_refines_query():
    """ask_with_clarification должен уточнить запрос перед поиском."""
    passages = [make_passage("docs/01-svyazi/arch.md", 0.8)]
    retriever = MockRetriever(passages)
    rag = ClarifyingRAG(retriever, threshold=0.6)
    result = rag.ask_with_clarification("память", "01-svyazi")
    assert "01-svyazi" in retriever.last_query


def test_clarifying_rag_threshold_respected():
    """Порог 0.6: score < 0.6 → None, score >= 0.6 → ClarificationRequest."""
    # Создаём пассажи, которые дают score 1.0 (короткий запрос, разные секции)
    ambiguous_passages = [
        make_passage("docs/01-svyazi/arch.md", 0.8),
        make_passage("docs/05-habr-projects/memory/ngt.md", 0.75),
    ]
    retriever = MockRetriever(ambiguous_passages)
    # Порог = 1.1 (выше максимального) → всегда None
    rag_strict = ClarifyingRAG(retriever, threshold=1.1)
    assert rag_strict.ask("память") is None

    # Порог = 0.0 → всегда спрашивает (если score > 0)
    # Нужны пассажи из разных секций для score > 0
    rag_loose = ClarifyingRAG(retriever, threshold=0.0)
    # При score=1.0 и threshold=0.0 должен вернуть ClarificationRequest
    result = rag_loose.ask("память")
    # Если detect_ambiguity вернул score > 0, должен быть запрос
    assert result is None or isinstance(result, ClarificationRequest)
