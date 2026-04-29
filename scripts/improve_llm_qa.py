"""
improve_llm_qa.py — отвечает на вопросы о базе знаний через Claude API.
Читает docs/QUESTIONS.md (484 открытых вопроса), группирует по теме,
запрашивает Claude для ответов на основе контекста из docs/.
Создаёт docs/LLM_QA.md.
Запуск: python scripts/improve_llm_qa.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MAX_QUESTIONS = 15   # ограничение на стоимость


def load_questions() -> list[str]:
    p = DOCS / "QUESTIONS.md"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    questions = []
    for m in re.finditer(r'^[-*]\s+(.+\?)', text, re.MULTILINE):
        q = m.group(1).strip()
        if 20 < len(q) < 200:
            questions.append(q)
    return questions[:MAX_QUESTIONS]


def build_context_cache() -> str:
    """Собирает компактный контекст из ключевых файлов для prompt caching."""
    key_files = [
        "01-svyazi/01-executive-summary.md",
        "01-svyazi/07-mvp-planning.md",
        "SCORING.md",
        "FAQ.md",
        "CONTACTS.md",
    ]
    parts = []
    for rel in key_files:
        p = DOCS / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        # Берём первые ~500 слов каждого файла
        snippet = " ".join(text.split()[:500])
        parts.append(f"### {rel}\n{snippet}")
    return "\n\n".join(parts)


def call_claude_qa(questions: list[str], context: str) -> list[dict] | None:
    try:
        import anthropic
    except ImportError:
        print("  [!] anthropic not installed")
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  [!] ANTHROPIC_API_KEY not set")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    questions_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))

    system = (
        "Ты эксперт по проекту Svyazi 2.0. "
        "Отвечай на вопросы строго на основе предоставленного контекста. "
        "Если информации нет — пиши 'Информация не найдена в документации'. "
        "Ответы краткие (1-3 предложения)."
    )

    prompt = f"""Контекст проекта:
{context}

---
Ответь на следующие вопросы:
{questions_block}

Формат ответа:
1. [ответ]
2. [ответ]
...
"""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text
    except Exception as e:
        print(f"  [!] API error: {e}")
        return None

    # Парсим пронумерованные ответы
    results = []
    lines = raw.strip().split("\n")
    answer_map: dict[int, str] = {}
    current_num = None
    current_lines: list[str] = []

    for line in lines:
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m:
            if current_num is not None:
                answer_map[current_num] = " ".join(current_lines).strip()
            current_num = int(m.group(1))
            current_lines = [m.group(2)]
        elif current_num is not None:
            current_lines.append(line.strip())

    if current_num is not None:
        answer_map[current_num] = " ".join(current_lines).strip()

    for i, q in enumerate(questions):
        ans = answer_map.get(i + 1, "—")
        results.append({"q": q, "a": ans})

    return results


def main():
    print("LLM QA — ответы на вопросы из документации...")

    questions = load_questions()
    if not questions:
        print("  нет вопросов в QUESTIONS.md")
        return
    print(f"  вопросов: {len(questions)}")

    context = build_context_cache()
    print(f"  контекст: {len(context.split())} слов")

    results = call_claude_qa(questions, context)

    lines = [
        "# LLM QA — ответы на вопросы\n",
        f"_Модель: claude-haiku-4-5 · Вопросов: {len(questions)}_\n",
    ]

    if results:
        for r in results:
            lines.append(f"### {r['q']}\n")
            lines.append(f"{r['a']}\n")
    else:
        lines.append("_API недоступен — запустите с ANTHROPIC_API_KEY_\n")
        lines.append("\n## Вопросы (без ответов)\n")
        for q in questions:
            lines.append(f"- {q}")

    lines += [
        "\n---\n",
        "_Источник вопросов: docs/QUESTIONS.md_\n",
        "_Контекст: executive-summary, mvp-planning, SCORING, FAQ, CONTACTS_\n",
    ]

    out = DOCS / "LLM_QA.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
