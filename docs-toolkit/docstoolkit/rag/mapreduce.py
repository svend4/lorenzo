"""Map-reduce суммаризация для запросов с >50 документами."""
import time
from dataclasses import dataclass, field
from typing import Callable

from docstoolkit.rag.types import Passage
from docstoolkit.rag.answerer import get_answerer, Answerer


@dataclass
class MapReduceConfig:
    """Конфигурация map-reduce суммаризации."""
    chunk_size: int = 10                            # пассажей на один map-chunk
    max_map_tokens: int = 3000                      # максимум токенов в map-промпте
    max_reduce_tokens: int = 6000                   # максимум токенов в reduce-промпте
    model: str = "claude-haiku-4-5-20251001"
    answerer: str = "echo"


@dataclass
class MapResult:
    """Результат обработки одного chunk."""
    chunk_idx: int
    passages: list[Passage] = field(default_factory=list)
    summary: str = ""
    tokens_used: int = 0


@dataclass
class ReduceResult:
    """Финальный результат map-reduce."""
    final_answer: str
    map_results: list[MapResult] = field(default_factory=list)
    total_passages: int = 0
    total_tokens: int = 0
    duration_ms: int = 0


def _format_passages_for_map(passages: list[Passage], max_chars_per: int = 400) -> str:
    """Форматирует пассажи для map-промпта."""
    lines = []
    for i, p in enumerate(passages, 1):
        title = p.title or p.doc_id
        snippet = p.text[:max_chars_per]
        lines.append(f"[{i}] {title}: {snippet}")
    return "\n\n".join(lines) if lines else "(нет пассажей)"


def _map_chunk(
    question: str,
    passages: list[Passage],
    cfg: MapReduceConfig,
    answerer: Answerer,
    chunk_idx: int = 0,
) -> MapResult:
    """Обрабатывает один chunk пассажей → summary.

    Args:
        question: исходный вопрос
        passages: пассажи этого chunk
        cfg: конфигурация
        answerer: LLM answerer
        chunk_idx: индекс chunk (для трассировки)

    Returns:
        MapResult с summary
    """
    passages_text = _format_passages_for_map(passages)

    system = (
        "Ты — аналитик документации. Суммаризируй предоставленные пассажи "
        "в контексте заданного вопроса. Будь кратким и конкретным. "
        "Сохраняй ключевые факты и ссылки на источники."
    )

    # Rough token budget: max_map_tokens * 3 chars
    max_chars = cfg.max_map_tokens * 3
    passages_trimmed = passages_text[:max_chars]

    user = (
        f"Вопрос: {question}\n\n"
        f"Суммаризируй следующие пассажи в контексте этого вопроса:\n\n"
        f"{passages_trimmed}"
    )

    summary, tokens, _cost = answerer.answer(system, user, model=cfg.model)

    return MapResult(
        chunk_idx=chunk_idx,
        passages=passages,
        summary=summary,
        tokens_used=tokens,
    )


def _reduce(
    question: str,
    summaries: list[str],
    cfg: MapReduceConfig,
    answerer: Answerer,
) -> str:
    """Объединяет summaries из map-фазы в финальный ответ.

    Args:
        question: исходный вопрос
        summaries: список summary из map-фазы
        cfg: конфигурация
        answerer: LLM answerer

    Returns:
        Финальный ответ
    """
    if not summaries:
        return "Нет данных для суммаризации."

    # Format summaries with indices
    summaries_block = "\n\n---\n\n".join(
        f"Часть {i + 1}:\n{s}" for i, s in enumerate(summaries)
    )

    system = (
        "Ты — аналитик документации. На основе частичных суммари дай "
        "единый связный ответ на вопрос. Синтезируй информацию из всех частей, "
        "устрани дублирование, выдели самое важное."
    )

    # Rough token budget
    max_chars = cfg.max_reduce_tokens * 3
    summaries_trimmed = summaries_block[:max_chars]

    user = (
        f"На основе следующих суммари ответь на вопрос:\n\n"
        f"Вопрос: {question}\n\n"
        f"Суммари:\n\n{summaries_trimmed}"
    )

    answer, _tokens, _cost = answerer.answer(system, user, model=cfg.model)
    return answer


def map_reduce_ask(
    question: str,
    passages: list[Passage],
    cfg: MapReduceConfig | None = None,
    answerer: Answerer | None = None,
) -> ReduceResult:
    """Выполняет map-reduce суммаризацию для большого набора пассажей.

    Алгоритм:
    1. Разбить passages на chunks по cfg.chunk_size
    2. Map: суммаризировать каждый chunk
    3. Reduce: объединить все summaries в финальный ответ

    Args:
        question: вопрос
        passages: все пассажи (может быть 50+)
        cfg: конфигурация; по умолчанию MapReduceConfig()
        answerer: LLM answerer; по умолчанию get_answerer(cfg.answerer)

    Returns:
        ReduceResult с финальным ответом и полной трассировкой
    """
    t0 = time.time()
    cfg = cfg or MapReduceConfig()
    if answerer is None:
        answerer = get_answerer(cfg.answerer)

    if not passages:
        return ReduceResult(
            final_answer="Нет пассажей для обработки.",
            total_passages=0,
            duration_ms=int((time.time() - t0) * 1000),
        )

    # Split into chunks
    chunks: list[list[Passage]] = []
    for i in range(0, len(passages), cfg.chunk_size):
        chunk = passages[i:i + cfg.chunk_size]
        chunks.append(chunk)

    # Map phase: process each chunk sequentially (no external deps)
    map_results: list[MapResult] = []
    total_tokens = 0

    for idx, chunk in enumerate(chunks):
        mr = _map_chunk(question, chunk, cfg, answerer, chunk_idx=idx)
        map_results.append(mr)
        total_tokens += mr.tokens_used

    # Reduce phase: combine summaries
    summaries = [mr.summary for mr in map_results if mr.summary]
    final_answer = _reduce(question, summaries, cfg, answerer)

    # Count reduce tokens roughly (not tracked separately for simplicity)
    total_tokens += len(final_answer) // 3

    return ReduceResult(
        final_answer=final_answer,
        map_results=map_results,
        total_passages=len(passages),
        total_tokens=total_tokens,
        duration_ms=int((time.time() - t0) * 1000),
    )


def should_use_mapreduce(passages: list[Passage], threshold: int = 15) -> bool:
    """Эвристика: использовать map-reduce если пассажей больше threshold.

    Args:
        passages: список пассажей
        threshold: порог (по умолчанию 15)

    Returns:
        True если рекомендуется map-reduce
    """
    return len(passages) > threshold
