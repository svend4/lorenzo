"""
improve_llm_summary.py — генерирует AI-саммари для каждого раздела docs/.
Читает README.md каждого раздела + первые файлы, просит Claude написать
краткое резюме раздела (3-5 предложений). Создаёт docs/LLM_SUMMARIES.md.
Запуск: python scripts/improve_llm_summary.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SECTIONS = [
    ("01-svyazi",               "Архитектура Svyazi 2.0"),
    ("02-anthropic-vacancies",  "Вакансии Anthropic"),
    ("03-technology-combinations", "Комбинации технологий"),
    ("04-ai-collaborations",    "AI-коллаборации"),
    ("05-habr-projects",        "Хабр-проекты"),
]


def load_section_text(section_dir: Path, max_words: int = 800) -> str:
    """Загружает первые N слов из раздела."""
    parts = []
    # Сначала README
    readme = section_dir / "README.md"
    if readme.exists():
        parts.append(readme.read_text(encoding="utf-8"))

    # Потом первые 3 файла
    for f in sorted(section_dir.rglob("*.md")):
        if f.name == "README.md":
            continue
        parts.append(f.read_text(encoding="utf-8"))
        if sum(len(p.split()) for p in parts) >= max_words:
            break

    combined = "\n\n".join(parts)
    words = combined.split()
    return " ".join(words[:max_words])


def call_claude_summary(section_name: str, text: str) -> str | None:
    try:
        import anthropic
    except ImportError:
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Напиши краткое резюме раздела документации проекта Svyazi 2.0.

Раздел: **{section_name}**

Содержимое (фрагмент):
{text[:2000]}

Напиши 3-5 предложений:
1. О чём этот раздел
2. Ключевые темы или компоненты
3. Как это связано с проектом Svyazi 2.0
4. Что можно найти в документах

Только текст резюме, без преамбулы и заголовков."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        print(f"  [!] API error для {section_name}: {e}")
        return None


def fallback_summary(section_dir: Path, section_name: str) -> str:
    """Автоматическое резюме без API."""
    files = list(section_dir.rglob("*.md"))
    total_words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)
    return (
        f"Раздел **{section_name}** содержит {len(files)} документов "
        f"({total_words:,} слов). "
        f"Файлы: {', '.join(f.name for f in sorted(files)[:5])}."
    )


def main():
    print("LLM саммари разделов документации...")

    use_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    print(f"  режим: {'Claude API' if use_api else 'fallback (нет ANTHROPIC_API_KEY)'}")

    results: list[dict] = []

    for folder, name in SECTIONS:
        section_dir = DOCS / folder
        if not section_dir.exists():
            continue

        text = load_section_text(section_dir)
        files = list(section_dir.rglob("*.md"))
        words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)

        print(f"  → {folder} ({len(files)} файлов, {words:,} слов)")

        if use_api:
            summary = call_claude_summary(name, text)
        else:
            summary = None

        if not summary:
            summary = fallback_summary(section_dir, name)

        results.append({
            "folder": folder,
            "name":   name,
            "files":  len(files),
            "words":  words,
            "summary": summary,
        })

    lines = [
        "# AI-саммари разделов документации\n",
        f"_Модель: claude-haiku-4-5 · Разделов: {len(results)}_\n",
    ]

    for r in results:
        lines += [
            f"## {r['name']}\n",
            f"_`docs/{r['folder']}/` · {r['files']} файлов · {r['words']:,} слов_\n",
            f"{r['summary']}\n",
        ]

    lines += [
        "---\n",
        "_Запустите с `ANTHROPIC_API_KEY` для AI-генерации резюме._\n",
        "_Без ключа — автоматическое резюме на основе метаданных._\n",
    ]

    out = DOCS / "LLM_SUMMARIES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
