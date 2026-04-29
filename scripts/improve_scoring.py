"""
improve_scoring.py — система оценки готовности проекта к запуску (Go/No-Go).
Проверяет 20+ критериев по 5 категориям: документация, архитектура,
команда, риски, MVP-готовность.
Создаёт docs/SCORING.md.
Запуск: python scripts/improve_scoring.py
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def file_exists(name: str) -> bool:
    return (DOCS / name).exists() or any(DOCS.rglob(name))


def file_has_content(name: str, min_words: int = 100) -> bool:
    p = DOCS / name
    if not p.exists():
        return False
    return len(p.read_text(encoding="utf-8").split()) >= min_words


def file_contains(name: str, keywords: list[str]) -> bool:
    p = DOCS / name
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8").lower()
    return any(k.lower() in text for k in keywords)


def count_md_in_section(section: str) -> int:
    folder = DOCS / section
    if not folder.exists():
        return 0
    return len(list(folder.rglob("*.md")))


def search_docs(keywords: list[str]) -> int:
    """Сколько файлов содержат хотя бы одно ключевое слово."""
    count = 0
    for f in DOCS.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8").lower()
            if any(k.lower() in text for k in keywords):
                count += 1
        except Exception:
            pass
    return count


# Критерии оценки: (название, функция-проверка, вес, описание_при_провале)
CRITERIA = {
    "Документация": [
        ("Executive Summary существует",
         lambda: file_has_content("01-svyazi/01-executive-summary.md", 200),
         10, "Нужен файл 01-executive-summary.md с описанием проекта"),
        ("Архитектурные контракты описаны",
         lambda: file_has_content("01-svyazi/11-integration-contracts.md", 100),
         10, "Нужны integration contracts"),
        ("MVP план задокументирован",
         lambda: file_has_content("01-svyazi/07-mvp-planning.md", 100),
         10, "Нужен mvp-planning.md"),
        ("Дорожная карта есть",
         lambda: file_has_content("01-svyazi/12-roadmap.md", 100),
         8, "Нужен roadmap.md"),
        ("README в каждом разделе",
         lambda: all(file_exists(f"{s}/README.md") for s in [
             "01-svyazi","02-anthropic-vacancies",
             "03-technology-combinations","04-ai-collaborations",
             "05-habr-projects"]),
         5, "Нужны README.md в каждом разделе"),
        ("Глоссарий создан",
         lambda: file_has_content("GLOSSARY.md", 50),
         5, "Нужен GLOSSARY.md"),
    ],

    "Архитектура": [
        ("Компоненты каталогизированы (20+)",
         lambda: file_contains("01-svyazi/03-component-catalog.md",
                               ["cardindex","agentfs","yodoca","sentinel","rufler"]),
         10, "Каталог компонентов неполный"),
        ("Ансамбли определены (5+)",
         lambda: file_has_content("01-svyazi/04-ensembles-overview.md", 200),
         10, "Нужны 5+ ансамблей проектов"),
        ("Архитектурные пробелы выявлены",
         lambda: file_has_content("01-svyazi/09-architectural-gaps.md", 100),
         8, "Нужен анализ архитектурных пробелов"),
        ("Безопасность и PII описаны",
         lambda: file_contains("01-svyazi/06-security-privacy.md",
                               ["pii","allowlist","quarantine"]),
         8, "Нужна политика безопасности"),
        ("Граф связей проектов построен",
         lambda: file_has_content("GRAPH.md", 50),
         5, "Нужен GRAPH.md"),
    ],

    "Команда и контакты": [
        ("Контакты авторов компонентов есть",
         lambda: file_has_content("CONTACTS.md", 100),
         10, "Нужен CONTACTS.md с авторами"),
        ("Авторы Habr-проектов найдены",
         lambda: search_docs(["kksudo","spbmolot","habr"]) >= 3,
         8, "Нужны контакты авторов Хабр-проектов"),
        ("Шаблоны для связи созданы",
         lambda: file_exists("templates/contact-outreach.md"),
         5, "Нужен шаблон contact-outreach.md"),
    ],

    "Риски": [
        ("Риски выявлены и задокументированы",
         lambda: search_docs(["риск","ограничен","не стоит"]) >= 10,
         8, "Нужен анализ рисков"),
        ("Лицензии проверены",
         lambda: search_docs(["MIT","Apache","BSL","лицензи"]) >= 5,
         8, "Нужна проверка лицензий всех компонентов"),
        ("Сломанных ссылок < 30",
         lambda: (lambda t: int(re.search(r'Найдено.*?(\d+)', t).group(1)) < 30
                  if re.search(r'Найдено.*?(\d+)', t) else True)(
                 (DOCS / "BROKEN_LINKS.md").read_text(encoding="utf-8")
                 if (DOCS / "BROKEN_LINKS.md").exists() else ""),
         5, "Слишком много сломанных ссылок"),
        ("Дублей нет",
         lambda: file_contains("DUPLICATES.md", ["0 точных дублей", "Точных дублей: 0"]),
         5, "Есть точные дубли документов"),
    ],

    "MVP-готовность": [
        ("Прогресс MVP отслеживается",
         lambda: file_has_content("PROGRESS.md", 50),
         8, "Нужен PROGRESS.md"),
        ("Action items задокументированы",
         lambda: file_has_content("ACTION_ITEMS.md", 100),
         8, "Нужны action items"),
        ("Порядок чтения задан",
         lambda: file_has_content("READING_ORDER.md", 100),
         5, "Нужен READING_ORDER.md"),
        ("Executive report создан",
         lambda: file_has_content("REPORT.md", 100),
         5, "Нужен REPORT.md"),
    ],
}


def score_to_label(pct: float) -> str:
    if pct >= 90: return "🟢 GO"
    if pct >= 70: return "🟡 УСЛОВНО GO"
    if pct >= 50: return "🟠 НЕ ГОТОВ"
    return "🔴 NO-GO"


def main():
    print("Оценка готовности проекта (Go/No-Go)...")

    total_score = 0
    max_score   = 0
    results: dict[str, list] = {}

    for category, criteria in CRITERIA.items():
        cat_score = 0
        cat_max   = 0
        cat_rows  = []
        for name, check_fn, weight, fail_msg in criteria:
            try:
                passed = check_fn()
            except Exception:
                passed = False
            earned = weight if passed else 0
            cat_score += earned
            cat_max   += weight
            total_score += earned
            max_score   += weight
            cat_rows.append((name, passed, weight, earned, fail_msg))
        results[category] = (cat_score, cat_max, cat_rows)

    pct   = int(total_score / max_score * 100) if max_score else 0
    label = score_to_label(pct)
    today = date.today().isoformat()

    lines = [
        "# Оценка готовности проекта (Go/No-Go)\n",
        f"_Дата: {today}_\n",
        f"## Итог: **{total_score}/{max_score}** ({pct}%) — {label}\n",
    ]

    for category, (cat_score, cat_max, rows) in results.items():
        cat_pct   = int(cat_score / cat_max * 100) if cat_max else 0
        cat_label = score_to_label(cat_pct)
        lines += [
            f"\n## {category} — {cat_score}/{cat_max} ({cat_pct}%) {cat_label}\n",
            "| Критерий | Статус | Вес |",
            "|----------|--------|-----|",
        ]
        for name, passed, weight, earned, fail_msg in rows:
            mark = "✅" if passed else "❌"
            lines.append(f"| {name} | {mark} | {weight} |")
            if not passed:
                lines.append(f"|  ↳ _{fail_msg}_ | | |")

    # Рекомендации
    failed = [(name, fail_msg, weight)
              for _, (_, _, rows) in results.items()
              for name, passed, weight, _, fail_msg in rows
              if not passed]
    failed.sort(key=lambda x: -x[2])

    lines += [f"\n## Приоритетные действия ({len(failed)} незакрытых)\n"]
    for i, (name, msg, w) in enumerate(failed[:10], 1):
        lines.append(f"{i}. **[вес {w}]** {msg}")

    if pct >= 90:
        lines += ["\n## ✅ Проект готов к запуску MVP!\n"]
    elif pct >= 70:
        lines += ["\n## ⚠️ Почти готов — устраните критические пробелы\n"]
    else:
        lines += ["\n## ❌ Требуется дополнительная работа перед запуском\n"]

    out = DOCS / "SCORING.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  балл: {total_score}/{max_score} ({pct}%) — {label}")


if __name__ == "__main__":
    main()
