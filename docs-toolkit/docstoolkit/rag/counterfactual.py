"""Counterfactual RAG: attribution трассировка и what-if анализ."""
import re
from dataclasses import dataclass, field
from typing import Callable

from docstoolkit.rag.types import Passage


@dataclass
class SpanAttribution:
    """Атрибуция одного спана (предложения) ответа к источнику."""
    text: str               # спан из ответа
    source_doc_id: str      # id документа-источника
    source_title: str       # заголовок документа-источника
    confidence: float       # 0-1, основан на Jaccard-overlap слов
    offset: int             # порядковый номер предложения в ответе


@dataclass
class AttributedAnswer:
    """Ответ с атрибуцией спанов к источникам."""
    answer: str
    attributions: list[SpanAttribution] = field(default_factory=list)
    unattributed_fraction: float = 0.0   # доля предложений без атрибуции (0-1)
    query: str = ""


@dataclass
class CounterfactualResult:
    """Результат counterfactual анализа: что изменилось без документа X."""
    original_answer: str
    modified_answer: str
    removed_doc_id: str
    delta: str                  # текстовый summary diff
    attribution_shift: float    # доля атрибуций, изменивших источник (0-1)


def _tokenize(text: str) -> set[str]:
    """Разбивает текст на множество слов (нижний регистр, только буквы/цифры)."""
    return set(re.findall(r'\w+', text.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity между двумя множествами."""
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union else 0.0


def _split_sentences(text: str) -> list[str]:
    """Простое разбиение на предложения по [.!?] и переносам строк."""
    # Split on sentence-ending punctuation or newlines
    raw = re.split(r'(?<=[.!?])\s+|(?<=[.!?])\n+|\n{2,}', text)
    return [s.strip() for s in raw if s.strip()]


def attribute_answer(answer: str, passages: list[Passage]) -> AttributedAnswer:
    """Атрибутирует каждое предложение ответа к пассажу-источнику.

    Алгоритм:
    - Разбить ответ на предложения
    - Для каждого предложения найти пассаж с максимальным Jaccard overlap слов
    - SpanAttribution если overlap > 0.15, иначе — неатрибутировано
    - unattributed_fraction = предложения без атрибуции / всего предложений

    Args:
        answer: текст ответа
        passages: список пассажей, использованных для ответа

    Returns:
        AttributedAnswer
    """
    sentences = _split_sentences(answer)
    if not sentences:
        return AttributedAnswer(answer=answer, unattributed_fraction=1.0)

    attributions: list[SpanAttribution] = []
    unattributed_count = 0

    for offset, sentence in enumerate(sentences):
        sent_tokens = _tokenize(sentence)
        best_score = 0.0
        best_passage: Passage | None = None

        for passage in passages:
            pass_tokens = _tokenize(passage.text)
            score = _jaccard(sent_tokens, pass_tokens)
            if score > best_score:
                best_score = score
                best_passage = passage

        if best_score >= 0.15 and best_passage is not None:
            attributions.append(SpanAttribution(
                text=sentence,
                source_doc_id=best_passage.doc_id,
                source_title=best_passage.title or best_passage.doc_id,
                confidence=best_score,
                offset=offset,
            ))
        else:
            unattributed_count += 1

    unattributed_fraction = unattributed_count / len(sentences)

    return AttributedAnswer(
        answer=answer,
        attributions=attributions,
        unattributed_fraction=unattributed_fraction,
    )


def _token_diff_summary(original: str, modified: str) -> str:
    """Суммаризирует разницу между двумя текстами на уровне токенов.

    Returns:
        Строка вида "добавлено N слов, убрано M слов"
    """
    orig_tokens = _tokenize(original)
    mod_tokens = _tokenize(modified)

    added = mod_tokens - orig_tokens
    removed = orig_tokens - mod_tokens

    parts = []
    if added:
        parts.append(f"добавлено {len(added)} слов")
    if removed:
        parts.append(f"убрано {len(removed)} слов")
    if not parts:
        parts.append("изменений нет")

    return ", ".join(parts)


def counterfactual_ask(
    question: str,
    passages: list[Passage],
    remove_doc_id: str,
    answerer_fn: Callable[[str, list[Passage]], str],
) -> CounterfactualResult:
    """Анализирует влияние одного документа на ответ.

    Запускает answerer дважды:
    1. Со всеми пассажами → original_answer
    2. Без пассажей из remove_doc_id → modified_answer

    Args:
        question: вопрос
        passages: все доступные пассажи
        remove_doc_id: doc_id документа для удаления
        answerer_fn: функция (question, passages) -> answer_text

    Returns:
        CounterfactualResult
    """
    # Run with all passages
    original_answer = answerer_fn(question, passages)

    # Run without removed doc
    filtered = [p for p in passages if p.doc_id != remove_doc_id]
    modified_answer = answerer_fn(question, filtered)

    # Compute delta
    delta = _token_diff_summary(original_answer, modified_answer)

    # Attribution shift: compare which sources changed
    orig_attr = attribute_answer(original_answer, passages)
    mod_attr = attribute_answer(modified_answer, filtered)

    # Map sentence offsets to sources
    orig_sources = {a.offset: a.source_doc_id for a in orig_attr.attributions}
    mod_sources = {a.offset: a.source_doc_id for a in mod_attr.attributions}

    all_offsets = set(orig_sources.keys()) | set(mod_sources.keys())
    changed = 0
    for off in all_offsets:
        o_src = orig_sources.get(off)
        m_src = mod_sources.get(off)
        if o_src != m_src:
            changed += 1

    attribution_shift = changed / len(all_offsets) if all_offsets else 0.0

    return CounterfactualResult(
        original_answer=original_answer,
        modified_answer=modified_answer,
        removed_doc_id=remove_doc_id,
        delta=delta,
        attribution_shift=attribution_shift,
    )


class ForensicRAG:
    """Forensic RAG: объединяет attribution и counterfactual анализ.

    Позволяет:
    - Задать вопрос с полной атрибуцией ответа к источникам
    - Объяснить влияние конкретного документа на ответ
    """

    def __init__(self, retriever, answerer_fn: Callable[[str, list[Passage]], str]):
        """
        Args:
            retriever: объект с методом search(question, top_k) -> list[Passage]
            answerer_fn: функция (question, passages) -> answer_text
        """
        self.retriever = retriever
        self.answerer_fn = answerer_fn

    def ask(self, question: str, top_k: int = 5) -> AttributedAnswer:
        """Задаёт вопрос и возвращает ответ с атрибуцией.

        Args:
            question: вопрос
            top_k: количество пассажей для retrieval

        Returns:
            AttributedAnswer с атрибуцией каждого предложения
        """
        passages = self.retriever.search(question, top_k=top_k)
        answer = self.answerer_fn(question, passages)
        result = attribute_answer(answer, passages)
        result.query = question
        return result

    def explain(self, question: str, suspect_doc_id: str,
                top_k: int = 5) -> CounterfactualResult:
        """Объясняет, как изменился бы ответ без конкретного документа.

        Args:
            question: вопрос
            suspect_doc_id: doc_id документа для удаления
            top_k: количество пассажей для retrieval

        Returns:
            CounterfactualResult с оригинальным и изменённым ответами
        """
        passages = self.retriever.search(question, top_k=top_k)
        return counterfactual_ask(question, passages, suspect_doc_id, self.answerer_fn)
