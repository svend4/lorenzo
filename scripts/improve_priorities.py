"""
improve_priorities.py — ранжирует файлы по важности через TF-IDF.
Ключевые термины = названия проектов + архитектурные понятия.
Создаёт docs/PRIORITIES.md.
Запуск: python scripts/improve_priorities.py
"""
import re
import math
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Термины высокой важности (вес 3)
HIGH_WEIGHT = [
    "CardIndex", "AgentFS", "Svyazi", "Evidence Envelope", "Memory Write Policy",
    "Card Envelope", "Skill Policy", "Review Record", "архитектурный зазор",
    "MVP", "prototip", "интеграционный контракт",
]
# Термины средней важности (вес 2)
MED_WEIGHT = [
    "knowledge-space", "Yodoca", "NGT Memory", "LiteParse", "Legal RAG",
    "SENTINEL", "mclaude", "AI Factory", "Rufler", "AutoResearch",
    "consolidation", "forgetting", "page-level", "evidence", "forensic",
]
# Базовые термины (вес 1)
LOW_WEIGHT = [
    "agent", "memory", "rag", "security", "orchestration", "roadmap",
    "license", "MIT", "Apache", "BSL", "локальн", "local-first",
]


def score_file(text: str) -> float:
    """Считает score файла по взвешенным терминам."""
    low = text.lower()
    score = 0.0
    word_count = max(len(text.split()), 1)

    for term in HIGH_WEIGHT:
        count = low.count(term.lower())
        score += count * 3.0

    for term in MED_WEIGHT:
        count = low.count(term.lower())
        score += count * 2.0

    for term in LOW_WEIGHT:
        count = low.count(term.lower())
        score += count * 1.0

    # Нормализуем по длине документа (TF-подобная нормализация)
    normalized = score / math.log(word_count + 2)
    return round(normalized, 2)


def get_top_terms(text: str, n: int = 5) -> list[str]:
    """Возвращает топ-N терминов по частоте встречаемости."""
    all_terms = HIGH_WEIGHT + MED_WEIGHT + LOW_WEIGHT
    low = text.lower()
    counts = [(t, low.count(t.lower())) for t in all_terms if low.count(t.lower()) > 0]
    counts.sort(key=lambda x: -x[1])
    return [t for t, _ in counts[:n]]


def main():
    print("Ранжирование файлов по важности...")
    scored = []

    for f in DOCS.rglob("*.md"):
        skip_names = {"README.md", "PRIORITIES.md", "TAGS.md", "GLOSSARY.md",
                      "CROSSREFS.md", "DUPLICATES.md", "TIMELINE.md",
                      "AUTHORS.md", "LINKS.md", "GRAPH.md", "QA.md",
                      "SEARCH.md", "TAGS.md"}
        if f.name in skip_names:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 100:
            continue

        s = score_file(text)
        top_terms = get_top_terms(text)
        words = len(text.split())
        section = f.parent.name

        scored.append({
            "path": str(f.relative_to(ROOT)),
            "score": s,
            "words": words,
            "section": section,
            "top_terms": top_terms,
        })

    scored.sort(key=lambda x: -x["score"])

    lines = [
        "# Приоритеты файлов\n",
        "Ранжирование по важности (TF-IDF по ключевым терминам архитектуры).\n",
        f"**Всего файлов:** {len(scored)}\n",
    ]

    # Топ-50
    lines += [
        "## Топ-50 самых важных файлов\n",
        "| # | Файл | Score | Слов | Ключевые термины |",
        "|---|------|-------|------|-----------------|",
    ]
    for i, e in enumerate(scored[:50], 1):
        terms = ", ".join(e["top_terms"])
        lines.append(
            f"| {i} | `{e['path']}` | **{e['score']}** | {e['words']} | {terms} |"
        )

    # По разделам
    lines.append("\n## Топ-5 по каждому разделу\n")
    by_section: dict[str, list] = defaultdict(list)
    for e in scored:
        by_section[e["section"]].append(e)

    for section in sorted(by_section.keys()):
        entries = by_section[section][:5]
        lines.append(f"\n### {section}\n")
        lines.append("| Файл | Score |")
        lines.append("|------|-------|")
        for e in entries:
            lines.append(f"| `{e['path']}` | {e['score']} |")

    out = DOCS / "PRIORITIES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  топ-1: {scored[0]['path']} (score={scored[0]['score']})")
    print(f"  топ-2: {scored[1]['path']} (score={scored[1]['score']})")
    print(f"  топ-3: {scored[2]['path']} (score={scored[2]['score']})")


if __name__ == "__main__":
    main()
