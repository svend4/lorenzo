"""
improve_reading_order.py — строит рекомендуемый порядок чтения документов
от базовых концепций к сложным. Создаёт docs/READING_ORDER.md.
Запуск: python scripts/improve_reading_order.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Порядок разделов: от фундамента к деталям
SECTION_ORDER = [
    "01-svyazi",
    "05-habr-projects",
    "04-ai-collaborations",
    "03-technology-combinations",
    "02-anthropic-vacancies",
]

# Приоритет файлов внутри раздела (по ключевым словам)
FILE_PRIORITY = {
    "executive-summary":    1,
    "readme":               1,
    "overview":             1,
    "intro":                2,
    "methodology":          2,
    "component-catalog":    3,
    "architecture":         3,
    "gaps":                 4,
    "contracts":            4,
    "ensembles":            5,
    "security":             6,
    "mvp":                  7,
    "roadmap":              8,
    "contacts":             9,
    "limitations":          10,
    "conclusions":          11,
}

# Предварительные знания для некоторых файлов
PREREQUISITES = {
    "09-architectural-gaps.md":        ["01-executive-summary.md", "03-component-catalog.md"],
    "11-integration-contracts.md":     ["09-architectural-gaps.md"],
    "12-roadmap.md":                   ["07-mvp-planning.md", "11-integration-contracts.md"],
    "10-second-order-ensembles.md":    ["04-ensembles-overview.md"],
    "ensembles/01-knowledge-os.md":    ["01-svyazi/01-executive-summary.md"],
    "ensembles/02-forensic-rag.md":    ["01-svyazi/03-component-catalog.md"],
}

DIFFICULTY = {1: "🟢 Начало", 2: "🟡 Средний", 3: "🔴 Продвинутый"}


def file_priority(path: Path) -> int:
    name = path.stem.lower()
    for keyword, priority in FILE_PRIORITY.items():
        if keyword in name:
            return priority
    # По номеру в начале имени
    m = re.match(r'^(\d+)', name)
    return int(m.group(1)) if m else 50


def estimate_difficulty(words: int, has_code: bool, has_table: bool) -> int:
    score = 0
    if words > 1000: score += 1
    if words > 3000: score += 1
    if has_code: score += 1
    if has_table: score += 0.5
    return min(3, max(1, round(score)))


def main():
    print("Строю порядок чтения...")

    learning_path = []

    for section in SECTION_ORDER:
        folder = DOCS / section
        if not folder.exists():
            continue

        files = sorted(
            [f for f in folder.rglob("*.md")
             if f.name not in ("README.md", "QA.md")],
            key=file_priority
        )

        for f in files:
            text = f.read_text(encoding="utf-8")
            words = len(text.split())
            has_code = "```" in text
            has_table = "|---|" in text or "|--" in text
            difficulty = estimate_difficulty(words, has_code, has_table)

            title = f.stem
            for line in text.split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()[:60]
                    break

            prereqs = []
            rel = str(f.relative_to(DOCS))
            for key, deps in PREREQUISITES.items():
                if key in rel:
                    prereqs = deps

            learning_path.append({
                "path": str(f.relative_to(ROOT)),
                "section": section,
                "title": title,
                "words": words,
                "difficulty": difficulty,
                "prereqs": prereqs,
            })

    lines = [
        "# Рекомендуемый порядок чтения\n",
        "От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).\n",
        "| # | Уровень | Документ | Слов | Предварительно прочитать |",
        "|---|---------|----------|------|--------------------------|",
    ]

    for i, doc in enumerate(learning_path, 1):
        diff_label = DIFFICULTY[doc["difficulty"]]
        prereq_str = ", ".join(
            f"`{p.split('/')[-1]}`" for p in doc["prereqs"]
        ) if doc["prereqs"] else "—"
        lines.append(
            f"| {i} | {diff_label} | [{doc['title'][:45]}]({doc['path']}) "
            f"| {doc['words']} | {prereq_str} |"
        )

    # Маршруты по целям
    lines += [
        "\n## Маршруты по целям\n",

        "### 🚀 Быстрый старт (30 минут)\n",
        "1. [Executive Summary](docs/01-svyazi/01-executive-summary.md)",
        "2. [Ансамбли проектов](docs/01-svyazi/04-ensembles-overview.md)",
        "3. [MVP Planning](docs/01-svyazi/07-mvp-planning.md)\n",

        "### 🏗️ Архитектура (2 часа)\n",
        "1. [Component Catalog](docs/01-svyazi/03-component-catalog.md)",
        "2. [Architectural Gaps](docs/01-svyazi/09-architectural-gaps.md)",
        "3. [Integration Contracts](docs/01-svyazi/11-integration-contracts.md)",
        "4. [Security & Privacy](docs/01-svyazi/06-security-privacy.md)\n",

        "### 🔬 Полное исследование (1 день)\n",
        "1. Весь раздел `01-svyazi/` по порядку",
        "2. `05-habr-projects/` — отдельные проекты",
        "3. `04-ai-collaborations/` — ансамбли",
        "4. `03-technology-combinations/` — комбинации",
        "5. `02-anthropic-vacancies/` — карьерные возможности",
    ]

    out = DOCS / "READING_ORDER.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  документов в порядке чтения: {len(learning_path)}")


if __name__ == "__main__":
    main()
