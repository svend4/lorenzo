"""
improve_dependency_map.py — карта зависимостей: скрипты → выходные файлы.
Показывает что каждый improve_*.py производит и от чего зависит.
Создаёт docs/DEPENDENCY_MAP.md.
Запуск: python scripts/improve_dependency_map.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Ручная карта: скрипт → (выходные файлы, входные зависимости)
DEPENDENCY_MAP = {
    # Структура
    "improve_readmes.py":       (["docs/*/README.md"],                    []),
    "improve_summaries.py":     (["docs/*/README.md"],                    ["docs/**/*.md"]),
    "improve_tags.py":          (["docs/TAGS.md"],                        ["docs/**/*.md"]),
    "improve_toc.py":           (["docs/**/*.md (TOC блоки)"],            ["docs/**/*.md"]),
    "improve_glossary.py":      (["docs/GLOSSARY.md"],                    ["docs/**/*.md"]),
    # Индексы
    "improve_search_index.py":  (["docs/search_index.json"],              ["docs/**/*.md"]),
    "improve_index_update.py":  (["docs/search_index.json"],              ["docs/search_index.json"]),
    "improve_backlinks.py":     (["docs/BACKLINKS.md"],                   ["docs/**/*.md"]),
    "improve_sitemap.py":       (["docs/SITEMAP.md", "docs/sitemap.xml"], ["docs/**/*.md"]),
    # Анализ
    "improve_clusters.py":      (["docs/CLUSTERS.md"],                    ["docs/**/*.md"]),
    "improve_similar.py":       (["docs/SIMILAR.md"],                     ["docs/**/*.md"]),
    "improve_sentiment.py":     (["docs/SENTIMENT.md"],                   ["docs/**/*.md"]),
    "improve_heatmap.py":       (["docs/HEATMAP.md"],                     ["docs/TAGS.md"]),
    "improve_word_freq.py":     (["docs/WORD_FREQ.md"],                   ["docs/**/*.md"]),
    # Извлечение
    "improve_entities.py":      (["docs/ENTITIES.md"],                    ["docs/**/*.md"]),
    "improve_concepts.py":      (["docs/CONCEPTS.md"],                    ["docs/**/*.md"]),
    "improve_questions.py":     (["docs/QUESTIONS.md"],                   ["docs/**/*.md"]),
    "improve_kpi.py":           (["docs/KPI.md"],                         ["docs/**/*.md"]),
    "improve_action_items.py":  (["docs/ACTION_ITEMS.md"],                ["docs/**/*.md"]),
    "improve_decisions.py":     (["docs/DECISIONS.md"],                   ["docs/**/*.md"]),
    "improve_abbreviations.py": (["docs/ABBREVIATIONS.md"],               ["docs/**/*.md"]),
    # Качество
    "improve_validate.py":      (["docs/VALIDATION.md"],                  ["docs/**/*.md"]),
    "improve_metrics.py":       (["docs/METRICS.md"],                     ["docs/**/*.md"]),
    "improve_health.py":        (["docs/HEALTH.md"],                      ["docs/METRICS.md", "docs/VALIDATION.md"]),
    "improve_orphans.py":       (["docs/ORPHANS.md"],                     ["docs/BACKLINKS.md"]),
    "improve_scoring.py":       (["docs/SCORING.md"],                     ["docs/HEALTH.md", "docs/METRICS.md"]),
    # Граф
    "improve_network.py":       (["docs/NETWORK.md", "docs/network.dot"], ["docs/ENTITIES.md"]),
    "improve_word_cloud.py":    (["docs/WORD_CLOUD.svg", "docs/WORD_CLOUD.md"], ["docs/WORD_FREQ.md"]),
    "improve_badges.py":        (["docs/badges/*.svg"],                   ["docs/HEALTH.md", "docs/SCORING.md"]),
    # Отчёты
    "improve_stats.py":         (["docs/STATS.md"],                       ["docs/**/*.md"]),
    "improve_report.py":        (["docs/REPORT.md"],                      ["docs/STATS.md", "docs/HEALTH.md"]),
    "improve_faq.py":           (["docs/FAQ.md"],                         ["docs/**/*.md"]),
    "improve_schedule.py":      (["docs/SCHEDULE.md"],                    []),
    "improve_cost.py":          (["docs/COST.md"],                        ["docs/**/*.md"]),
    "improve_digest.py":        (["docs/DIGEST.md"],                      []),
    "improve_digest_weekly.py": (["docs/DIGEST_WEEKLY.md"],               []),
    "improve_progress.py":      (["docs/PROGRESS.md"],                    ["docs/SCORING.md"]),
    "improve_footnotes.py":     (["docs/FOOTNOTES.md", "docs/**/*.md (сноски)"], ["docs/**/*.md"]),
    # Экспорт
    "improve_export_json.py":   (["docs/export_full.json"],               ["docs/**/*.md"]),
    "improve_export_csv.py":    (["docs/export_full.csv"],                ["docs/**/*.md"]),
    "improve_export_html.py":   (["docs/export_full.html"],               ["docs/**/*.md"]),
    # Ступень 2-3
    "improve_autofill.py":      (["docs/autofilled/**"],                  ["docs/templates/**", "docs/ENTITIES.md", "docs/SCORING.md"]),
    "improve_llm_enrich.py":    (["docs/**/*.md (enriched)"],             ["docs/ENTITIES.md", "ANTHROPIC_API_KEY"]),
    "improve_llm_qa.py":        (["docs/LLM_QA.md"],                     ["docs/QUESTIONS.md", "ANTHROPIC_API_KEY"]),
    "improve_llm_gaps.py":      (["docs/LLM_GAPS.md"],                   ["docs/**/*.md", "ANTHROPIC_API_KEY"]),
    "improve_llm_summary.py":   (["docs/LLM_SUMMARIES.md"],              ["docs/*/README.md"]),
    # Мета
    "improve_tech_radar.py":    (["docs/TECH_RADAR.md"],                  []),
    "improve_onboarding.py":    (["docs/ONBOARDING.md"],                  ["docs/SCORING.md", "docs/CONTACTS.md"]),
    "improve_dependency_map.py":(["docs/DEPENDENCY_MAP.md"],              ["scripts/improve_*.py"]),
}


def main():
    print("Генерация карты зависимостей скриптов...")

    scripts_dir = ROOT / "scripts"
    existing = {f.name for f in scripts_dir.glob("improve_*.py")}
    mapped   = set(DEPENDENCY_MAP.keys())

    lines = [
        "# Карта зависимостей скриптов\n",
        "_Что каждый `improve_*.py` производит и от чего зависит._\n",
        f"**Скриптов в карте:** {len(mapped)} · "
        f"**Всего в репо:** {len(existing)}\n",

        "## Зависимости\n",
        "| Скрипт | Производит | Зависит от |",
        "|--------|-----------|-----------|",
    ]

    for script in sorted(DEPENDENCY_MAP):
        outputs, inputs = DEPENDENCY_MAP[script]
        out_str = ", ".join(f"`{o}`" for o in outputs[:2])
        if len(outputs) > 2:
            out_str += f" +{len(outputs)-2}"
        inp_str = ", ".join(f"`{i}`" for i in inputs[:2]) if inputs else "—"
        marker = "" if script in existing else " ⚠️"
        lines.append(f"| `{script}`{marker} | {out_str} | {inp_str} |")

    # Скрипты есть в репо, но нет в карте
    unmapped = sorted(existing - mapped)
    if unmapped:
        lines += [
            "\n## Скрипты без карты зависимостей\n",
            "_Существуют в репо, но не добавлены в карту:_\n",
        ]
        for s in unmapped:
            lines.append(f"- `{s}`")

    lines += [
        "\n## Порядок запуска (рекомендуемый)\n",
        "```",
        "1. structure  →  2. index  →  3. analysis  →  4. extract",
        "         ↓                                          ↓",
        "    5. quality  ←────────────────────────────  данные",
        "         ↓",
        "    6. graph  →  7. reports  →  8. export",
        "                     ↓",
        "              9. enrich (LLM, нужен API ключ)",
        "                     ↓",
        "              10. meta (tech-radar, onboarding, ...)",
        "```\n",
        "_Используй `python scripts/improve_run_all.py` для автоматического порядка._\n",
    ]

    out = DOCS / "DEPENDENCY_MAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  в карте: {len(mapped)}, в репо: {len(existing)}, без карты: {len(unmapped)}")


if __name__ == "__main__":
    main()
