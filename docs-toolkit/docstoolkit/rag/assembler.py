"""Assembler — формирует context-aware промпт из retrieved пассажей."""
from docstoolkit.rag.types import Passage


SYSTEM_PROMPT_TMPL = """Ты — RAG ассистент, отвечающий на вопросы по корпусу документации.

Правила:
1. Используй ТОЛЬКО информацию из приведённых ниже пассажей. Не выдумывай факты.
2. Если ответа нет в пассажах — скажи "Информация не найдена в корпусе".
3. Цитируй источники в формате [N] где N — номер пассажа.
4. Отвечай на том же языке, что и вопрос.
5. Будь конкретным и кратким.
"""


def _truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Грубое: 1 токен ≈ 4 символа для лат / 2 для кир."""
    # Среднее: ~3 символа на токен
    approx_max_chars = max_tokens * 3
    if len(text) <= approx_max_chars:
        return text
    return text[:approx_max_chars] + "...[truncated]"


def assemble_prompt(question: str, passages: list[Passage],
                    max_context_tokens: int = 8000) -> tuple[str, str]:
    """Возвращает (system_prompt, user_message).

    User message содержит вопрос + пронумерованные пассажи.
    """
    # Формируем пассажи
    passage_texts = []
    total_chars = 0
    max_chars = max_context_tokens * 3  # rough conversion

    for i, p in enumerate(passages, 1):
        snippet = p.text[:1000]  # ограничение на пассаж
        block = (f"[{i}] **{p.title or p.doc_id}**\n"
                 f"Источник: `{p.doc_id}`\n"
                 f"{snippet}\n")
        if total_chars + len(block) > max_chars:
            break
        passage_texts.append(block)
        total_chars += len(block)

    context = "\n---\n\n".join(passage_texts) if passage_texts else "(нет пассажей)"

    user_message = (
        f"# Вопрос\n\n{question}\n\n"
        f"# Контекст ({len(passage_texts)} пассажей)\n\n{context}\n\n"
        f"# Задача\n\n"
        f"Ответь на вопрос, используя только приведённые пассажи. "
        f"Если в пассажах нет ответа — так и скажи."
    )

    return SYSTEM_PROMPT_TMPL, user_message
