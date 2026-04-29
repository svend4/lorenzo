"""
improve_sitemap.py — генерирует навигационную карту репозитория.
Создаёт: docs/SITEMAP.md (текстовый) + docs/sitemap.xml (XML для поиска).
Запуск: python scripts/improve_sitemap.py
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"SITEMAP.md"}

SECTION_LABELS = {
    "01-svyazi":               "Svyazi 2.0 — Архитектура системы",
    "02-anthropic-vacancies":  "Вакансии Anthropic — 436 позиций",
    "03-technology-combinations": "Комбинации технологий",
    "04-ai-collaborations":    "AI Коллаборации — ансамбли проектов",
    "05-habr-projects":        "Хабр-проекты — память и граф",
    "root":                    "Корневые мета-документы",
}

META_FILES = {
    "README.md", "GLOSSARY.md", "AUTHORS.md", "LINKS.md",
    "CROSSREFS.md", "TIMELINE.md", "TAGS.md", "SEARCH.md",
    "GRAPH.md", "MINDMAP.md", "QA.md", "PRIORITIES.md",
    "CONTACTS.md", "ACTION_ITEMS.md", "MISSING.md", "CLUSTERS.md",
    "CONSISTENCY.md", "BROKEN_LINKS.md", "CHANGELOG.md",
    "DECISIONS.md", "READING_ORDER.md", "HEALTH.md",
    "WORD_FREQ.md", "CODE_BLOCKS.md", "TABLES.md", "SIMILAR.md",
    "QUESTIONS.md", "KPI.md", "STATS.md", "DENSITY.md",
    "COMPLEXITY.md", "ENTITIES.md", "CONCEPTS.md", "COMPARE.md",
    "DUPLICATES.md", "export.csv", "search_index.json",
}


def get_title(f: Path) -> str:
    try:
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()[:60]
    except Exception:
        pass
    return f.stem


def get_word_count(f: Path) -> int:
    try:
        return len(f.read_text(encoding="utf-8").split())
    except Exception:
        return 0


def main():
    print("Генерация sitemap...")
    today = date.today().isoformat()

    # Группировка файлов
    sections: dict[str, list[Path]] = {}
    meta: list[Path] = []

    for f in sorted(DOCS.rglob("*.md")):
        rel = f.relative_to(DOCS)
        if f.name in SKIP:
            continue
        if f.name in META_FILES or len(rel.parts) == 1:
            meta.append(f)
        else:
            sec = rel.parts[0]
            sections.setdefault(sec, []).append(f)

    # SITEMAP.md
    lines = [
        "# Карта репозитория Lorenzo\n",
        f"_Обновлено: {today}_\n",
        f"**Всего файлов:** {sum(len(v) for v in sections.values()) + len(meta)}\n",

        "## Навигация\n",
        "- [Мета-документы](#мета-документы)",
    ]
    for sec in sorted(sections.keys()):
        label = SECTION_LABELS.get(sec, sec)
        lines.append(f"- [{label}](#{sec})")

    lines += ["\n---\n", "## Мета-документы\n",
              "| Документ | Описание | Слов |",
              "|----------|----------|------|"]

    META_DESC = {
        "README.md":       "Главная страница и навигация",
        "GLOSSARY.md":     "Глоссарий проектов (33 записи)",
        "AUTHORS.md":      "Авторы и контакты",
        "LINKS.md":        "Внешние ссылки",
        "CROSSREFS.md":    "Перекрёстные ссылки проектов",
        "TIMELINE.md":     "Временная шкала (800 маркеров)",
        "TAGS.md":         "Теги (316 файлов, 12 тем)",
        "SEARCH.md":       "Поисковый индекс",
        "GRAPH.md":        "Граф связей проектов",
        "MINDMAP.md":      "Майндмап в Mermaid",
        "CLUSTERS.md":     "Кластеры (384 → 120 групп)",
        "DECISIONS.md":    "Ключевые решения (150)",
        "READING_ORDER.md":"Рекомендуемый порядок чтения",
        "HEALTH.md":       "Дашборд здоровья (75/100)",
        "WORD_FREQ.md":    "Частотный анализ слов",
        "KPI.md":          "Числовые KPI (737 показателей)",
        "QUESTIONS.md":    "Открытые вопросы (484)",
        "STATS.md":        "Детальная статистика",
        "SIMILAR.md":      "Похожие документы (937 пар)",
        "DENSITY.md":      "Карта плотности тем",
        "COMPLEXITY.md":   "Оценка читаемости",
        "ENTITIES.md":     "Именованные сущности",
        "CONCEPTS.md":     "Глоссарий понятий (888)",
        "COMPARE.md":      "Сравнение с предыдущим коммитом",
        "ACTION_ITEMS.md": "Задачи и риски (490)",
        "MISSING.md":      "Пробелы знаний",
        "CONTACTS.md":     "Контакты (15 авторов)",
        "PRIORITIES.md":   "Приоритеты (TF-IDF)",
        "BROKEN_LINKS.md": "Сломанные ссылки (26)",
        "CHANGELOG.md":    "История изменений",
        "QA.md":           "Вопросы и ответы",
    }

    for f in sorted(meta, key=lambda x: x.name):
        desc = META_DESC.get(f.name, "—")
        words = get_word_count(f)
        rel = f.relative_to(ROOT)
        lines.append(f"| [{f.name}]({rel}) | {desc} | {words} |")

    # Разделы
    for sec in sorted(sections.keys()):
        label = SECTION_LABELS.get(sec, sec)
        files = sections[sec]
        lines += [
            f"\n## {label}\n",
            f"_`docs/{sec}/` — {len(files)} файлов_\n",
            "| # | Документ | Слов |",
            "|---|----------|------|",
        ]
        for i, f in enumerate(files[:50], 1):
            title = get_title(f)
            words = get_word_count(f)
            rel   = f.relative_to(ROOT)
            lines.append(f"| {i} | [{title[:50]}]({rel}) | {words} |")
        if len(files) > 50:
            lines.append(f"| ... | _ещё {len(files)-50} файлов_ | |")

    out_md = DOCS / "SITEMAP.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out_md.relative_to(ROOT)}")

    # XML sitemap
    all_files = list(DOCS.rglob("*.md"))
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in sorted(all_files):
        if f.name in SKIP:
            continue
        rel = str(f.relative_to(ROOT)).replace("\\", "/")
        xml_lines.append(f"  <url><loc>{rel}</loc><lastmod>{today}</lastmod></url>")
    xml_lines.append("</urlset>")

    out_xml = DOCS / "sitemap.xml"
    out_xml.write_text("\n".join(xml_lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out_xml.relative_to(ROOT)}")
    print(f"  мета-файлов: {len(meta)}, разделов: {len(sections)}, "
          f"всего в XML: {len(all_files)}")


if __name__ == "__main__":
    main()
