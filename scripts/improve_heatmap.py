"""
improve_heatmap.py — тепловая карта тем по разделам и файлам.
ASCII-визуализация: строки = темы, столбцы = разделы.
Создаёт docs/HEATMAP.md.
Запуск: python scripts/improve_heatmap.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"HEATMAP.md", "DENSITY.md", "STATS.md"}

TOPICS = {
    "Память/Knowledge": ["memory", "yodoca", "ngt", "knowledge", "episod", "forgetting"],
    "Агент/Оркестр":    ["agent", "агент", "rufler", "mclaude", "factory", "handoff"],
    "Безопасность":     ["sentinel", "security", "pii", "allowlist", "quarantine", "firewall"],
    "Архитектура":      ["architecture", "контракт", "envelope", "schema", "layer"],
    "MVP/Roadmap":      ["mvp", "roadmap", "итерац", "sprint", "milestone"],
    "Граф/RAG":         ["graph", "rag", "vector", "embedding", "faiss", "graphrag"],
    "Лицензия/OSS":     ["license", "лицензия", "mit", "apache", "bsl", "open source"],
    "Вакансии":         ["vacancy", "вакансии", "hiring", "anthropic", "position"],
    "Комбинации":       ["combination", "комбинац", "синерги", "ensemble", "ансамбль"],
    "Habr/Проекты":     ["habr", "хабр", "agentfs", "wikontic", "memnet"],
    "Контакты/Команда": ["kksudo", "spbmolot", "contact", "контакт", "написать"],
    "Интеграция/API":   ["mcp", "api", "protocol", "integration", "contract"],
}

SECTIONS = ["01-svyazi", "02-anthropic-vacancies",
            "03-technology-combinations", "04-ai-collaborations",
            "05-habr-projects"]


def density(text: str, keywords: list[str]) -> float:
    low = text.lower()
    count = sum(low.count(k) for k in keywords)
    words = max(len(text.split()), 1)
    return count / words * 1000  # на тысячу слов


def heat_char(val: float, max_val: float) -> str:
    if max_val == 0 or val == 0:
        return "░░"
    ratio = val / max_val
    if ratio >= 0.8: return "██"
    if ratio >= 0.6: return "▓▓"
    if ratio >= 0.4: return "▒▒"
    if ratio >= 0.2: return "░░"
    return "  "


def main():
    print("Тепловая карта тем...")

    # Собираем текст по разделам
    sec_texts: dict[str, str] = {}
    for sec in SECTIONS:
        folder = DOCS / sec
        if not folder.exists():
            continue
        text = " ".join(
            f.read_text(encoding="utf-8")
            for f in folder.rglob("*.md")
            if f.name not in SKIP
        )
        sec_texts[sec] = text

    # Матрица плотности
    matrix: dict[str, dict[str, float]] = {}
    for topic, kws in TOPICS.items():
        matrix[topic] = {}
        for sec, text in sec_texts.items():
            matrix[topic][sec] = density(text, kws)

    # Нормализуем по строкам
    row_max: dict[str, float] = {
        topic: max(matrix[topic].values()) for topic in TOPICS
    }

    lines = [
        "# Тепловая карта тем\n",
        "Плотность упоминаний каждой темы по разделам (‰ — на тысячу слов).\n",
        "```",
        "Тема                    | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr",
        "------------------------|-----------|--------------|---------|-----------|--------",
    ]

    for topic in TOPICS:
        row = matrix[topic]
        mval = row_max[topic]
        cells = []
        for sec in SECTIONS:
            val = row.get(sec, 0)
            hc  = heat_char(val, mval)
            cells.append(f"{hc}{val:4.1f}")
        padded = f"{topic:<24}"
        lines.append(f"{padded}| {' | '.join(cells)} |")

    lines += [
        "```\n",
        "_██ = максимум, ▓▓ = высокое, ▒▒ = среднее, ░░ = низкое_\n",
    ]

    # Таблица числовых значений
    lines += [
        "## Числовые значения (‰)\n",
        "| Тема | " + " | ".join(s.split("-", 1)[-1][:10] for s in SECTIONS) + " |",
        "|------|" + "|".join("-" * 12 for _ in SECTIONS) + "|",
    ]
    for topic in TOPICS:
        vals = " | ".join(f"{matrix[topic].get(s, 0):.1f}" for s in SECTIONS)
        lines.append(f"| **{topic}** | {vals} |")

    # Выводы: доминирующая тема каждого раздела
    lines += ["\n## Доминирующие темы по разделам\n"]
    for sec in SECTIONS:
        best = max(TOPICS.keys(), key=lambda t: matrix[t].get(sec, 0))
        val  = matrix[best].get(sec, 0)
        lines.append(f"- **{sec}**: {best} ({val:.1f}‰)")

    # Выводы: где каждая тема наиболее сконцентрирована
    lines += ["\n## Концентрация тем\n",
              "| Тема | Лучший раздел | Плотность |",
              "|------|--------------|-----------|"]
    for topic in TOPICS:
        best_sec = max(SECTIONS, key=lambda s: matrix[topic].get(s, 0))
        val = matrix[topic].get(best_sec, 0)
        lines.append(f"| **{topic}** | `{best_sec}` | {val:.1f}‰ |")

    out = DOCS / "HEATMAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  тем: {len(TOPICS)}, разделов: {len(sec_texts)}")


if __name__ == "__main__":
    main()
