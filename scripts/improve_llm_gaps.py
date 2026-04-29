"""
improve_llm_gaps.py — семантический поиск пробелов через Claude API.
Анализирует структуру документации и находит темы, которые упомянуты
но не раскрыты, противоречия, устаревшие утверждения.
Создаёт docs/LLM_GAPS.md.
Запуск: python scripts/improve_llm_gaps.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def get_doc_index() -> str:
    """Строит компактный индекс: файл → первые 2 предложения."""
    entries = []
    for f in sorted(DOCS.rglob("*.md"))[:60]:
        text = f.read_text(encoding="utf-8")
        # Первые непустые строки без заголовков
        sentences = [
            ln.strip() for ln in text.split("\n")
            if ln.strip() and not ln.startswith("#") and not ln.startswith("|")
        ][:2]
        if sentences:
            entries.append(f"- `{f.relative_to(ROOT)}`: {' '.join(sentences)[:120]}")
    return "\n".join(entries)


def get_arch_summary() -> str:
    """Читает ключевые архитектурные файлы."""
    parts = []
    candidates = [
        "01-svyazi/09-architectural-gaps.md",
        "01-svyazi/11-integration-contracts.md",
        "01-svyazi/01-executive-summary.md",
    ]
    for rel in candidates:
        p = DOCS / rel
        if p.exists():
            text = p.read_text(encoding="utf-8")
            parts.append(f"### {rel}\n" + " ".join(text.split()[:400]))
    return "\n\n".join(parts)


def call_claude_gaps(doc_index: str, arch_summary: str) -> str | None:
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

    prompt = f"""Ты архитектурный ревьюер. Проанализируй документацию проекта Svyazi 2.0.

Индекс документов ({doc_index.count(chr(10))+1} файлов):
{doc_index}

Ключевые архитектурные документы:
{arch_summary}

Найди и опиши:

1. **Семантические пробелы** — темы упомянуты, но нет отдельного документа (3-5 примеров)
2. **Противоречия** — места где документы противоречат друг другу (2-3 примера)
3. **Устаревшие утверждения** — планы помечены как будущие, но дата прошла (2-3 примера)
4. **Недостающие связи** — компоненты которые должны быть связаны, но не ссылаются друг на друга
5. **Приоритетные задачи** — что нужно документировать в первую очередь (топ-5)

Отвечай в Markdown, структурировано."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except Exception as e:
        print(f"  [!] API error: {e}")
        return None


def main():
    print("LLM Gap Analysis — поиск семантических пробелов...")

    doc_index = get_doc_index()
    arch_summary = get_arch_summary()
    print(f"  индекс: {doc_index.count(chr(10))+1} файлов")
    print(f"  архитектура: {len(arch_summary.split())} слов")

    analysis = call_claude_gaps(doc_index, arch_summary)

    lines = [
        "# LLM Gap Analysis — семантические пробелы\n",
        "_Модель: claude-haiku-4-5 · Анализ структуры и связей документации_\n",
    ]

    if analysis:
        lines.append(analysis)
    else:
        lines += [
            "_API недоступен. Запустите с ANTHROPIC_API_KEY._\n",
            "\n## Что анализируется\n",
            "- Темы упомянутые, но не задокументированные",
            "- Противоречия между документами",
            "- Устаревшие планы и утверждения",
            "- Недостающие перекрёстные ссылки",
            "- Приоритеты для развития документации",
        ]

    lines += [
        "\n---\n",
        "_Источник: docs/ (первые 60 файлов) + архитектурные документы_\n",
    ]

    out = DOCS / "LLM_GAPS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
