"""
improve_coverage.py — матрица покрытия: какие файлы имеют summary, теги, TOC, crossrefs, статус.

Для каждого файла в целевых секциях показывает какие признаки присутствуют.
Создаёт docs/COVERAGE.md.

Запуск: python scripts/improve_coverage.py
        python scripts/improve_coverage.py --section 05-habr-projects
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = sys.argv[idx + 1]

TARGET_SECTIONS = [
    "01-svyazi", "02-anthropic-vacancies", "03-technology-combinations",
    "04-ai-collaborations", "05-habr-projects",
]
if SECTION_FILTER:
    TARGET_SECTIONS = [SECTION_FILTER]

SKIP_FILES = {"README.md", "QA.md"}

FEATURES = ["summary", "tags", "toc", "crossrefs", "status", "backlinks"]
FEATURE_LABELS = {
    "summary":   "Summary",
    "tags":      "Теги",
    "toc":       "TOC",
    "crossrefs": "CrossRefs",
    "status":    "## Статус",
    "backlinks": "Backlinks",
}


def check_features(text: str) -> dict[str, bool]:
    return {
        "summary":   bool(re.search(r'<!--\s*summary[:\s]', text)),
        "tags":      bool(re.search(r'<!--\s*tags:', text)),
        "toc":       bool(re.search(r'##\s*Содержание|<!--\s*toc|## Table of Contents', text, re.I)),
        "crossrefs": bool(re.search(r'<!--\s*see-also|## See also|## Связанные', text, re.I)),
        "status":    bool(re.search(r'<!--\s*autofill-status\s*-->', text)),
        "backlinks": bool(re.search(r'<!--\s*backlinks|## Упоминается в', text, re.I)),
    }


def _word_count(text: str) -> int:
    clean = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    clean = re.sub(r'[#*`\[\]|>]', ' ', clean)
    return len(clean.split())


def main() -> None:
    print("📋 improve_coverage.py — матрица покрытия документов")

    all_results = []
    section_stats: dict[str, dict] = {}

    for section in TARGET_SECTIONS:
        sec_path = DOCS / section
        if not sec_path.exists():
            continue
        files = [f for f in sorted(sec_path.rglob("*.md")) if f.name not in SKIP_FILES]
        if not files:
            continue

        section_results = []
        for f in files:
            text = f.read_text(encoding="utf-8")
            feats = check_features(text)
            words = _word_count(text)
            score = sum(feats.values())
            section_results.append({
                "path":     f.relative_to(ROOT),
                "section":  section,
                "words":    words,
                "features": feats,
                "score":    score,
            })

        all_results.extend(section_results)

        # Статистика по секции
        n = len(section_results)
        section_stats[section] = {
            feat: sum(1 for r in section_results if r["features"][feat])
            for feat in FEATURES
        }
        section_stats[section]["total"] = n

    # --- Построение отчёта ---
    lines = [
        "# Матрица покрытия документов\n",
        f"_Обновлено: {TODAY}_\n",
        "Условные обозначения: ✅ есть  ⬜ отсутствует\n",
    ]

    # Сводная таблица по секциям
    lines += [
        "## Сводка по секциям\n",
        "| Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks |",
        "|--------|--------|---------|------|-----|-----------|--------|-----------|",
    ]
    for section, stats in section_stats.items():
        n = stats["total"]
        cells = []
        for feat in FEATURES:
            cnt = stats[feat]
            pct = cnt * 100 // n if n else 0
            icon = "🟢" if pct >= 80 else ("🟡" if pct >= 50 else "🔴")
            cells.append(f"{icon} {cnt}/{n}")
        lines.append(f"| `{section}` | {n} | " + " | ".join(cells) + " |")
    lines.append("")

    # Файлы с низким покрытием (score < 3)
    low_coverage = [r for r in all_results if r["score"] < 3]
    low_coverage.sort(key=lambda x: x["score"])

    if low_coverage:
        lines += [
            f"## Файлы с низким покрытием (< 3 признаков) — {len(low_coverage)} файлов\n",
            "| Файл | Слов | " + " | ".join(FEATURE_LABELS[f] for f in FEATURES) + " |",
            "|------|------| " + "|".join("---" for _ in FEATURES) + " |",
        ]
        for r in low_coverage[:40]:
            cells = ["✅" if r["features"][f] else "⬜" for f in FEATURES]
            lines.append(f"| `{r['path']}` | {r['words']} | " + " | ".join(cells) + " |")
        if len(low_coverage) > 40:
            lines.append(f"\n_...и ещё {len(low_coverage)-40} файлов._")
        lines.append("")

    # Топ хорошо покрытых файлов
    full_coverage = [r for r in all_results if r["score"] == len(FEATURES)]
    lines += [
        f"## Полное покрытие — {len(full_coverage)} файлов\n",
    ]
    if full_coverage:
        for r in full_coverage[:10]:
            lines.append(f"- ✅ `{r['path']}`")
        if len(full_coverage) > 10:
            lines.append(f"- _...и ещё {len(full_coverage)-10}_")
    lines.append("")

    # Рекомендации
    lines += [
        "## Рекомендуемые действия\n",
        "```bash",
        "# Добавить summary и теги (быстро, $0)",
        "python scripts/improve_summaries.py",
        "python scripts/improve_tags.py",
        "",
        "# Добавить перекрёстные ссылки",
        "python scripts/improve_crossrefs.py",
        "python scripts/improve_backlinks.py",
        "",
        "# Заполнить блок ## Статус в проектных файлах",
        "python scripts/improve_autofill.py",
        "```",
    ]

    out = DOCS / "COVERAGE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    total = len(all_results)
    avg_score = sum(r["score"] for r in all_results) / total if total else 0
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов: {total}, средний балл: {avg_score:.1f}/{len(FEATURES)}")
    print(f"  низкое покрытие (<3): {len(low_coverage)}, полное: {len(full_coverage)}")


if __name__ == "__main__":
    main()
