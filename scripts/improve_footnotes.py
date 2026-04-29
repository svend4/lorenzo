"""
improve_footnotes.py — автоматически связывает технические термины с глоссарием.
Добавляет сноски [^term] к первому вхождению каждого термина в файле.
Создаёт docs/FOOTNOTES.md (отчёт), не ломает оригинальные файлы.
Запуск: python scripts/improve_footnotes.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

MARKER = "<!-- footnotes-added -->"
SKIP   = {"FOOTNOTES.md", "GLOSSARY.md", "ABBREVIATIONS.md", "CONCEPTS.md"}

# Термины → краткое определение для сноски
GLOSSARY = {
    "MCP":          "Model Context Protocol — протокол для AI-инструментов",
    "RAG":          "Retrieval-Augmented Generation — генерация с поиском",
    "LLM":          "Large Language Model — большая языковая модель",
    "CRDT":         "Conflict-free Replicated Data Type — бесконфликтные данные",
    "PII":          "Personally Identifiable Information — персональные данные",
    "CardIndex":    "OSS-проект: индекс знаний на карточках (MIT)",
    "AgentFS":      "OSS-проект: файловая система для AI-агентов (MIT)",
    "Yodoca":       "OSS-проект: система памяти с консолидацией (Apache 2.0)",
    "NGT":          "OSS-проект: ассоциативный граф памяти (BSL 1.1)",
    "SENTINEL":     "OSS-проект: безопасность и allowlist для MCP",
    "Rufler":       "OSS-проект: оркестратор AI-агентов",
    "Svyazi":       "Главный проект: экосистема AI-компонентов",
    "knowledge-space": "OSS-проект: база знаний 785+ карточек (MIT)",
    "Firecrawl":    "Инструмент: веб-краулер для AI (MIT)",
    "TF-IDF":       "Term Frequency–Inverse Document Frequency — метрика важности термина",
    "Jaccard":      "Коэффициент схожести множеств (0–1)",
    "BSL":          "Business Source License — коммерческая лицензия с открытым кодом",
}

# Только обрабатываем ключевые файлы (не все 460)
KEY_SECTIONS = ["01-svyazi", "04-ai-collaborations", "05-habr-projects"]


def add_footnotes(text: str, terms: dict[str, str]) -> tuple[str, int]:
    """Добавляет [^term] к первому вхождению каждого термина."""
    if MARKER in text:
        return text, 0

    # Убираем code-блоки перед обработкой (восстановим потом)
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(0))
        return f"\x00CODE{len(code_blocks)-1}\x00"

    text_clean = re.sub(r'```.*?```', save_code, text, flags=re.DOTALL)

    added = 0
    footnote_defs: list[str] = []
    used_terms: set[str] = set()

    for term, definition in terms.items():
        if term in used_terms:
            continue
        # Ищем первое вхождение термина (не внутри ссылки, не в заголовке)
        pattern = r'(?<!\[)(?<!\*\*)(?<!\w)\b' + re.escape(term) + r'\b(?!\])'
        m = re.search(pattern, text_clean)
        if not m:
            continue

        ref = f"[^{term.lower().replace('-','_').replace(' ','_')}]"
        # Вставляем ссылку на сноску
        text_clean = (text_clean[:m.end()] + ref + text_clean[m.end():])
        footnote_defs.append(f"{ref}: {definition}")
        used_terms.add(term)
        added += 1

    if added == 0:
        return text, 0

    # Восстанавливаем code-блоки
    for i, block in enumerate(code_blocks):
        text_clean = text_clean.replace(f"\x00CODE{i}\x00", block)

    # Добавляем определения сносок в конец
    footnote_section = f"\n\n{MARKER}\n\n---\n\n" + "\n\n".join(footnote_defs) + "\n"
    return text_clean + footnote_section, added


def main():
    print("Добавление сносок к терминам...")

    total_added = 0
    files_updated = 0
    term_stats: dict[str, int] = defaultdict(int)

    for sec in KEY_SECTIONS:
        folder = DOCS / sec
        if not folder.exists():
            continue
        for f in sorted(folder.rglob("*.md")):
            if f.name in SKIP:
                continue
            text = f.read_text(encoding="utf-8")
            if len(text.split()) < 100 or MARKER in text:
                continue

            new_text, n = add_footnotes(text, GLOSSARY)
            if n > 0:
                f.write_text(new_text, encoding="utf-8")
                files_updated += 1
                total_added   += n
                for term in GLOSSARY:
                    if f"[^{term.lower()}" in new_text:
                        term_stats[term] += 1

    # Отчёт
    lines = [
        "# Сноски и определения терминов\n",
        f"**Обновлено файлов:** {files_updated}  "
        f"**Вставлено сносок:** {total_added}\n",

        "## Словарь сносок\n",
        "| Термин | Определение | Файлов |",
        "|--------|-------------|--------|",
    ]
    for term, defn in sorted(GLOSSARY.items()):
        count = term_stats.get(term, 0)
        lines.append(f"| **{term}** | {defn} | {count} |")

    lines += [
        "\n## Как это работает\n",
        "При первом упоминании термина в файле добавляется `[^term]` — "
        "ссылка на сноску в конце документа.\n",
        "```markdown",
        "Используем MCP[^mcp] для подключения инструментов.",
        "",
        "[^mcp]: Model Context Protocol — протокол для AI-инструментов",
        "```",
    ]

    out = DOCS / "FOOTNOTES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов: {files_updated}, сносок: {total_added}")


if __name__ == "__main__":
    main()
