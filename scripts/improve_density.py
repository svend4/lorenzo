"""
improve_density.py — карта плотности тем по всем документам.
Считает упоминания ключевых тем в каждом разделе.
Показывает: какие темы раскрыты подробно, какие слабо.
Создаёт docs/DENSITY.md.
Запуск: python scripts/improve_density.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

TOPICS = {
    "Svyazi":        ["svyazi", "связи", "svyazi 2"],
    "CardIndex":     ["cardindex", "card index", "card-index", "карточки"],
    "AgentFS":       ["agentfs", "agent fs", "agent-fs", "obsidian"],
    "Yodoca":        ["yodoca", "ёдока", "yodoca"],
    "NGT-memory":    ["ngt", "memory", "ngt-memory", "ассоциативный граф"],
    "SENTINEL":      ["sentinel", "сентинел", "allowlist", "quarantine"],
    "Rufler":        ["rufler", "руфлер"],
    "AI Factory":    ["ai factory", "фабрика", "mclaude"],
    "Knowledge OS":  ["knowledge os", "knowledge-os", "knowledge space"],
    "Forensic RAG":  ["forensic", "hybrid rag", "legal rag"],
    "MCP":           ["mcp", "model context protocol"],
    "MVP":           ["mvp", "прототип", "первая итерация"],
    "Архитектура":   ["архитектур", "контракт", "envelope", "схема"],
    "Безопасность":  ["безопасност", "pii", "приватност", "security"],
    "Лицензия":      ["лицензи", "mit", "apache", "bsl", "license"],
    "Roadmap":       ["roadmap", "дорожная карта", "итерация"],
    "Вакансии":      ["вакансии", "anthropic", "vacancy", "hiring"],
    "Комбинации":    ["комбинац", "синерги", "combination"],
    "Habr":          ["хабр", "habr", "habrahabr"],
    "Контакты":      ["kksudo", "spbmolot", "андрей", "виталий", "написать"],
}

SECTIONS = [
    "01-svyazi",
    "02-anthropic-vacancies",
    "03-technology-combinations",
    "04-ai-collaborations",
    "05-habr-projects",
    "root",
]


def count_mentions(text: str, keywords: list[str]) -> int:
    low = text.lower()
    return sum(low.count(k.lower()) for k in keywords)


def make_bar(val: int, max_val: int, width: int = 15) -> str:
    if max_val == 0:
        return "░" * width
    filled = min(width, int(val / max_val * width))
    return "█" * filled + "░" * (width - filled)


def main():
    print("Карта плотности тем...")

    # Собираем тексты по разделам
    section_texts: dict[str, str] = defaultdict(str)
    for f in sorted(DOCS.rglob("*.md")):
        rel = f.relative_to(DOCS)
        sec = rel.parts[0] if len(rel.parts) > 1 else "root"
        if sec not in SECTIONS:
            sec = "root"
        section_texts[sec] += f.read_text(encoding="utf-8") + "\n"

    # Матрица: topic × section
    matrix: dict[str, dict[str, int]] = {}
    for topic, keywords in TOPICS.items():
        matrix[topic] = {}
        for sec in SECTIONS:
            matrix[topic][sec] = count_mentions(section_texts.get(sec, ""), keywords)

    lines = [
        "# Карта плотности тем\n",
        "Количество упоминаний каждой темы в каждом разделе.\n",
        "| Тема | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr | root | Итого |",
        "|------|-----------|--------------|---------|-----------|---------|------|-------|",
    ]

    topic_totals = {}
    for topic in TOPICS:
        row = matrix[topic]
        total = sum(row.values())
        topic_totals[topic] = total
        cells = " | ".join(str(row.get(s, 0)) for s in SECTIONS)
        lines.append(f"| **{topic}** | {cells} | **{total}** |")

    # Слабые темы
    weak = [(t, v) for t, v in topic_totals.items() if v < 5]
    strong = sorted(topic_totals.items(), key=lambda x: -x[1])

    lines += [
        "\n## Наиболее раскрытые темы\n",
        "| Тема | Упоминаний | Визуализация |",
        "|------|------------|-------------|",
    ]
    max_v = strong[0][1] if strong else 1
    for topic, total in strong[:10]:
        bar = make_bar(total, max_v)
        lines.append(f"| **{topic}** | {total} | `{bar}` |")

    lines += [f"\n## Слабо раскрытые темы ({len(weak)})\n"]
    if weak:
        for t, v in sorted(weak, key=lambda x: x[1]):
            lines.append(f"- **{t}**: {v} упоминаний — требует доработки")
    else:
        lines.append("_Все темы достаточно раскрыты_")

    # Раздел-лидер для каждой темы
    lines += ["\n## Где сосредоточена каждая тема\n",
              "| Тема | Основной раздел | % |",
              "|------|-----------------|---|"]
    for topic in TOPICS:
        row = matrix[topic]
        total = sum(row.values())
        if total == 0:
            continue
        best_sec = max(row, key=row.get)
        pct = int(row[best_sec] / total * 100)
        lines.append(f"| {topic} | `{best_sec}` | {pct}% |")

    out = DOCS / "DENSITY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  тем: {len(TOPICS)}, разделов: {len(SECTIONS)}")


if __name__ == "__main__":
    main()
