"""Детектор двусмысленности запроса → уточняющий вопрос.

Если запрос неоднозначен (например "что про память?"), система возвращает
ClarificationRequest вместо того чтобы гадать.

Использование:
    from docstoolkit.rag.clarifier import detect_ambiguity, ClarifyingRAG

    rag = ClarifyingRAG(retriever, threshold=0.6)
    req = rag.ask("что про память?")
    if req:
        # Показать пользователю: req.prompt
        passages = rag.ask_with_clarification("что про память?", req.options[0])
    else:
        passages = retriever.search("что про память?")
"""
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.rag.types import Passage


@dataclass
class AmbiguityScore:
    """Оценка неоднозначности запроса."""
    score: float                        # 0.0 (однозначный) … 1.0 (очень неоднозначный)
    candidates: list[str] = field(default_factory=list)   # названия конкурирующих секций
    reason: str = ""                    # человекочитаемое объяснение


@dataclass
class ClarificationRequest:
    """Запрос уточнения у пользователя."""
    original_question: str
    options: list[str]                  # варианты конкретизации
    prompt: str                         # «Вы имеете в виду: A, B или C?»


def _section_of(passage: Passage) -> str:
    """Извлечь имя секции из doc_id/path пассажа."""
    p = Path(passage.doc_id)
    # Берём первую осмысленную часть пути: docs/01-svyazi/... → 01-svyazi
    parts = p.parts
    for part in parts:
        if part not in (".", "..", "docs", "") and not part.endswith(".md"):
            return part
    # Fallback: имя файла без расширения
    return p.stem if p.stem else passage.doc_id


def detect_ambiguity(question: str, passages: list[Passage]) -> AmbiguityScore:
    """Определить степень неоднозначности запроса.

    Логика:
    - Нет пассажей → score=0 (нечего уточнять)
    - Один явный лидер: score[0] / score[1] > 3 → score=0 (чёткий ответ)
    - Короткий запрос (<3 слов) И несколько секций → score=1.0
    - Топ-3 пассажа из разных секций с близкими score → score=0.5+
    """
    if not passages:
        return AmbiguityScore(score=0.0, reason="no passages")

    # Сортируем по убыванию score
    sorted_passages = sorted(passages, key=lambda p: -p.score)
    top = sorted_passages[:3]

    # Собираем секции топ-3
    sections: list[str] = [_section_of(p) for p in top]
    unique_sections = list(dict.fromkeys(sections))  # сохраняем порядок, удаляем дубли

    # Чёткий лидер: первый score >> второго в 3+ раза
    if len(sorted_passages) >= 2:
        s0 = sorted_passages[0].score
        s1 = sorted_passages[1].score
        if s1 > 0 and s0 / s1 > 3.0:
            return AmbiguityScore(
                score=0.0,
                candidates=unique_sections[:1],
                reason="clear winner",
            )
        if s0 <= 0:
            return AmbiguityScore(score=0.0, reason="zero scores")

    words = question.strip().split()

    # Короткий запрос + несколько секций → максимальная неоднозначность
    if len(words) < 3 and len(unique_sections) > 1:
        return AmbiguityScore(
            score=1.0,
            candidates=unique_sections[:3],
            reason="short query with multiple competing sections",
        )

    # Топ-3 из разных секций с похожими score
    if len(unique_sections) > 1:
        s0 = top[0].score
        # Все топ-пассажи достаточно близки (не в 3 раза хуже лидера)
        similar_count = sum(
            1 for p in top if s0 <= 0 or p.score / s0 >= 0.33
        )
        if similar_count >= 2:
            return AmbiguityScore(
                score=0.5 + 0.1 * min(len(unique_sections) - 1, 5),
                candidates=unique_sections[:3],
                reason="similar scores across different sections",
            )

    return AmbiguityScore(
        score=0.0,
        candidates=unique_sections[:1],
        reason="single dominant section",
    )


def build_clarification(question: str,
                        score: AmbiguityScore) -> ClarificationRequest:
    """Сформировать запрос уточнения из результата detect_ambiguity."""
    options = score.candidates if score.candidates else [question]
    if len(options) == 1:
        prompt = f"Вы имеете в виду: {options[0]}?"
    else:
        opts_str = ", ".join(options[:-1]) + " или " + options[-1]
        prompt = f"Вы имеете в виду: {opts_str}?"
    return ClarificationRequest(
        original_question=question,
        options=options,
        prompt=prompt,
    )


def apply_clarification(question: str, chosen: str) -> str:
    """Объединить исходный вопрос с выбранным уточнением в уточнённый запрос.

    Пример: ("что про память?", "05-habr-projects") → "что про память? 05-habr-projects"
    """
    question = question.strip()
    chosen = chosen.strip()
    if not chosen or chosen.lower() in question.lower():
        return question
    return f"{question} {chosen}"


class ClarifyingRAG:
    """RAG с запросом уточнения при неоднозначных запросах."""

    def __init__(self, retriever, threshold: float = 0.6):
        """
        retriever — объект с методом search(question: str, top_k: int) -> list[Passage].
        threshold  — минимальный AmbiguityScore.score для запроса уточнения.
        """
        self.retriever = retriever
        self.threshold = threshold

    def ask(self, question: str,
            top_k: int = 5) -> "ClarificationRequest | None":
        """Вернуть ClarificationRequest если запрос неоднозначен, иначе None."""
        passages = self.retriever.search(question, top_k=top_k)
        amb = detect_ambiguity(question, passages)
        if amb.score >= self.threshold:
            return build_clarification(question, amb)
        return None

    def ask_with_clarification(self, question: str,
                                chosen_option: str,
                                top_k: int = 5) -> list[Passage]:
        """Уточнить запрос и вернуть пассажи."""
        refined = apply_clarification(question, chosen_option)
        return self.retriever.search(refined, top_k=top_k)
