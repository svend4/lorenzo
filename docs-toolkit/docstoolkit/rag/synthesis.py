"""Кросс-документный синтез: сравнение нескольких документов между собой."""
import time
from dataclasses import dataclass, field
from enum import Enum

from docstoolkit.rag.types import Passage
from docstoolkit.rag.answerer import get_answerer


class SynthesisMode(str, Enum):
    compare = "compare"
    summarize = "summarize"
    contrast = "contrast"
    timeline = "timeline"


@dataclass
class DocumentGroup:
    """Именованная группа пассажей для сравнения."""
    name: str
    passages: list[Passage] = field(default_factory=list)
    label: str = ""


@dataclass
class SynthesisRequest:
    """Запрос на кросс-документный синтез."""
    groups: list[DocumentGroup] = field(default_factory=list)
    question: str = ""
    mode: SynthesisMode = SynthesisMode.compare
    answerer: str = "echo"
    model: str = "claude-haiku-4-5-20251001"


@dataclass
class SynthesisResult:
    """Результат кросс-документного синтеза."""
    answer: str
    groups_summary: list[dict] = field(default_factory=list)  # per-group summary
    common_themes: list[str] = field(default_factory=list)
    differences: list[str] = field(default_factory=list)
    duration_ms: int = 0


def _format_group_passages(group: DocumentGroup, max_chars_per_passage: int = 500) -> str:
    """Форматирует пассажи группы в строку для промпта."""
    lines = []
    for i, p in enumerate(group.passages, 1):
        title = p.title or p.doc_id
        snippet = p.text[:max_chars_per_passage]
        lines.append(f"  [{i}] {title}: {snippet}")
    return "\n".join(lines) if lines else "  (пусто)"


def _build_synthesis_prompt(req: SynthesisRequest) -> tuple[str, str]:
    """Строит system + user промпт для синтеза.

    Returns:
        (system_prompt, user_message)
    """
    system = (
        "Ты — аналитик документации. Твоя задача — синтезировать информацию "
        "из нескольких групп документов и дать структурированный ответ.\n\n"
        "Правила:\n"
        "1. Используй только информацию из предоставленных пассажей.\n"
        "2. Выделяй общие темы и ключевые различия между группами.\n"
        "3. Ссылайся на группы по их названиям.\n"
        "4. Отвечай на языке вопроса."
    )

    # Build group sections
    group_sections = []
    for group in req.groups:
        label = group.label or group.name
        passages_text = _format_group_passages(group)
        group_sections.append(f"Группа «{label}»:\n{passages_text}")

    groups_block = "\n\n".join(group_sections) if group_sections else "(нет групп)"

    mode = req.mode if isinstance(req.mode, str) else req.mode.value

    if mode == "compare":
        task = (
            "Сравни эти группы: найди общие темы, ключевые различия и синтезируй вывод."
        )
    elif mode == "contrast":
        task = (
            "Выяви принципиальные противоречия и различия между группами. "
            "Что в них несовместимо или противоположно?"
        )
    elif mode == "summarize":
        task = (
            "Суммаризируй каждую группу отдельно, затем дай общий вывод по всем группам."
        )
    elif mode == "timeline":
        task = (
            "Выстрой хронологию событий и изменений из всех групп. "
            "Покажи, как темы развивались во времени."
        )
    else:
        task = "Проанализируй группы и ответь на вопрос."

    user = (
        f"# Группы документов\n\n{groups_block}\n\n"
        f"# Вопрос\n\n{req.question}\n\n"
        f"# Задача\n\n{task}"
    )

    return system, user


def _extract_themes_and_differences(answer: str) -> tuple[list[str], list[str]]:
    """Эвристически извлекает общие темы и различия из ответа LLM."""
    lines = answer.split("\n")
    common: list[str] = []
    differences: list[str] = []

    in_common = False
    in_diff = False

    common_markers = {"общ", "похож", "общее", "оба", "все группы", "совпад"}
    diff_markers = {"различ", "разниц", "отлич", "тогда как", "в отличие", "однако"}

    for line in lines:
        stripped = line.strip(" -•*#")
        if not stripped:
            continue
        low = stripped.lower()

        # Section headers
        if any(m in low for m in ("общие темы", "common", "схожее", "сходства")):
            in_common = True
            in_diff = False
            continue
        if any(m in low for m in ("различия", "differences", "contrast", "отличия")):
            in_diff = True
            in_common = False
            continue

        if in_common and len(stripped) > 10:
            common.append(stripped)
        elif in_diff and len(stripped) > 10:
            differences.append(stripped)
        else:
            # Inline detection
            if any(m in low for m in common_markers) and len(stripped) > 20:
                common.append(stripped)
            elif any(m in low for m in diff_markers) and len(stripped) > 20:
                differences.append(stripped)

    return common[:5], differences[:5]


def synthesize(req: SynthesisRequest) -> SynthesisResult:
    """Выполняет кросс-документный синтез.

    Args:
        req: параметры запроса

    Returns:
        SynthesisResult с ответом и структурированными выводами
    """
    t0 = time.time()

    answerer = get_answerer(req.answerer)
    system, user = _build_synthesis_prompt(req)

    answer_text, _tokens, _cost = answerer.answer(system, user, model=req.model)

    # Per-group summary: passage count + titles
    groups_summary = []
    for group in req.groups:
        label = group.label or group.name
        titles = [p.title or p.doc_id for p in group.passages]
        groups_summary.append({
            "name": group.name,
            "label": label,
            "passage_count": len(group.passages),
            "titles": titles,
        })

    common, differences = _extract_themes_and_differences(answer_text)

    return SynthesisResult(
        answer=answer_text,
        groups_summary=groups_summary,
        common_themes=common,
        differences=differences,
        duration_ms=int((time.time() - t0) * 1000),
    )


def compare_sections(
    section_a_docs: list[Passage],
    section_b_docs: list[Passage],
    question: str,
    **kwargs,
) -> SynthesisResult:
    """Удобная обёртка: сравнивает две группы пассажей.

    Args:
        section_a_docs: пассажи первой секции
        section_b_docs: пассажи второй секции
        question: вопрос для сравнения
        **kwargs: дополнительные параметры для SynthesisRequest
                  (answerer, model, mode)

    Returns:
        SynthesisResult
    """
    group_a = DocumentGroup(name="section_a", passages=section_a_docs, label="Секция A")
    group_b = DocumentGroup(name="section_b", passages=section_b_docs, label="Секция B")

    req = SynthesisRequest(
        groups=[group_a, group_b],
        question=question,
        mode=kwargs.get("mode", SynthesisMode.compare),
        answerer=kwargs.get("answerer", "echo"),
        model=kwargs.get("model", "claude-haiku-4-5-20251001"),
    )

    return synthesize(req)
