"""
improve_llm_enrich.py — обогащает короткие/stub-файлы через Claude API.
Находит файлы < 150 слов, собирает факты из соседних документов,
запрашивает Claude для генерации структурированного описания.
Создаёт docs/LLM_ENRICHED.md (отчёт).
Запуск: python scripts/improve_llm_enrich.py
"""
import os
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MARKER   = "<!-- llm-enriched -->"
SKIP     = {"LLM_ENRICHED.md", "FOOTNOTES.md", "FAQ.md", "SCORING.md"}
MAX_STUB_WORDS = 150
MAX_FILES = 20   # limit per run to control API cost


def get_context_snippets(stub_path: Path, max_snippets: int = 4) -> list[str]:
    """Собирает релевантные фрагменты из соседних файлов."""
    folder = stub_path.parent
    snippets = []
    stem = stub_path.stem.lower()

    for f in sorted(folder.rglob("*.md")):
        if f == stub_path or f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        # Ищем упоминания имени файла
        if stem.replace("-", " ") in text.lower() or stem.replace("_", " ") in text.lower():
            # Извлекаем 2-3 предложения вокруг упоминания
            for para in text.split("\n\n"):
                if stem.replace("-", " ") in para.lower():
                    clean = re.sub(r'\s+', ' ', para.strip())
                    if 30 < len(clean) < 500:
                        snippets.append(clean[:400])
                        break
        if len(snippets) >= max_snippets:
            break

    return snippets


def call_claude(stub_name: str, existing_text: str, context: list[str]) -> str | None:
    """Вызывает Claude API для обогащения контента."""
    try:
        import anthropic
    except ImportError:
        print("  [!] anthropic not installed — pip install anthropic")
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  [!] ANTHROPIC_API_KEY not set")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    context_block = "\n".join(f"- {s}" for s in context) if context else "Нет дополнительного контекста."
    prompt = f"""Ты технический писатель. Улучши и расширь следующий stub-документ на основе контекста.

Файл: {stub_name}

Текущий текст (неполный):
{existing_text.strip()[:600]}

Контекст из соседних документов:
{context_block}

Напиши структурированное Markdown-описание (150-300 слов):
- Назначение и ключевые функции
- Технические детали (если есть в контексте)
- Связи с другими компонентами
- Статус / лицензия (если известны)

Отвечай только Markdown-текстом, без преамбулы."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except Exception as e:
        print(f"  [!] API error: {e}")
        return None


def main():
    print("LLM-обогащение stub-документов...")

    stubs: list[Path] = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP or MARKER in f.read_text(encoding="utf-8"):
            continue
        words = len(f.read_text(encoding="utf-8").split())
        if 10 < words < MAX_STUB_WORDS:
            stubs.append(f)

    stubs = stubs[:MAX_FILES]
    print(f"  найдено stub-файлов: {len(stubs)}")

    enriched: list[dict] = []
    skipped = 0

    for stub in stubs:
        text = stub.read_text(encoding="utf-8")
        context = get_context_snippets(stub)
        print(f"  → {stub.relative_to(ROOT)} ({len(text.split())} слов, {len(context)} сниппетов)")

        new_content = call_claude(stub.name, text, context)
        if not new_content:
            skipped += 1
            continue

        # Пишем обогащённый вариант
        updated = text.rstrip() + f"\n\n{MARKER}\n\n{new_content.strip()}\n"
        stub.write_text(updated, encoding="utf-8")
        enriched.append({
            "file": str(stub.relative_to(ROOT)),
            "before": len(text.split()),
            "after":  len(updated.split()),
        })

    # Отчёт
    lines = [
        "# LLM-обогащение документов\n",
        f"_Модель: claude-haiku-4-5 · Обработано: {len(enriched)} · Пропущено: {skipped}_\n",
        "| Файл | Слов до | Слов после |",
        "|------|---------|-----------|",
    ]
    for r in enriched:
        lines.append(f"| `{r['file']}` | {r['before']} | {r['after']} |")

    if not enriched:
        lines.append("| — | — | — |")

    lines += [
        "\n## Как работает\n",
        "1. Находит файлы < 150 слов (stub-документы)",
        "2. Собирает контекст из соседних файлов по ключевым словам",
        "3. Отправляет в Claude Haiku запрос на структурированное описание",
        "4. Дописывает результат в конец файла с маркером `<!-- llm-enriched -->`",
        "5. Повторный запуск пропускает уже обработанные файлы\n",
        "**Стоимость:** ~$0.01–0.03 за файл (Haiku, 600 токенов вывода)\n",
    ]

    out = DOCS / "LLM_ENRICHED.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  обогащено: {len(enriched)}, пропущено: {skipped}")


if __name__ == "__main__":
    main()
