"""
improve_export_report.py — единый сводный отчёт по всей базе знаний.

Собирает ключевые данные из всех отчётных файлов и создаёт
один документ, пригодный для:
  - презентации инвесторам / авторам проектов
  - отправки в виде PDF/EPUB через pandoc
  - быстрого ввода нового участника в контекст

Структура:
  1. Executive Summary (автогенерация)
  2. Метрики корпуса
  3. Ключевые проекты (из CONTACTS.md)
  4. Архитектурные решения (из DECISIONS.md)
  5. Открытые вопросы (из QUESTIONS.md)
  6. Топ документы для чтения (из reading_list)
  7. Рекомендации (из analysis)

Запуск:
    python scripts/improve_export_report.py
    python scripts/improve_export_report.py --title "Svyazi 2.0 — Обзор"
    python scripts/improve_export_report.py --sections all  # все секции
    python scripts/improve_export_report.py --no-projects   # без проектов
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

TITLE = "Svyazi 2.0 — Knowledge Base Report"
INCLUDE_PROJECTS = True
INCLUDE_ALL = "--sections" in sys.argv and sys.argv[sys.argv.index("--sections") + 1] == "all"

if "--title" in sys.argv:
    idx = sys.argv.index("--title")
    if idx + 1 < len(sys.argv):
        TITLE = sys.argv[idx + 1]

if "--no-projects" in sys.argv:
    INCLUDE_PROJECTS = False

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "при", "от", "до", "об", "так", "все", "они", "же",
    "the", "a", "an", "is", "of", "in", "on", "to", "for", "with",
    "by", "and", "not", "it", "we", "are", "this", "that",
    "docs", "summary", "tags", "true", "false",
}


def _read_md(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _read_json(name: str):
    p = DOCS / name
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _extract_section(text: str, heading: str, max_lines: int = 20) -> list[str]:
    """Извлекает содержимое секции по заголовку."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf'^#+\s+{re.escape(heading)}', line, re.I):
            start = i + 1
            break
    if start is None:
        return []
    result = []
    for line in lines[start:]:
        if re.match(r'^#+\s', line) and result:
            break
        if line.strip():
            result.append(line)
        if len(result) >= max_lines:
            break
    return result


def _extract_table_rows(text: str, after_heading: str) -> list[str]:
    """Извлекает строки markdown-таблицы после заголовка."""
    lines = text.splitlines()
    in_section = False
    rows = []
    for line in lines:
        if re.match(rf'^#+\s+{re.escape(after_heading)}', line, re.I):
            in_section = True
            continue
        if in_section:
            if re.match(r'^#+\s', line):
                break
            if line.startswith("|") and not line.startswith("|---"):
                rows.append(line)
    return rows


def _corpus_stats() -> dict:
    all_md = [f for f in DOCS.rglob("*.md")
              if "-parts" not in str(f) and "obsidian" not in str(f)]
    total_words = 0
    for f in all_md:
        try:
            total_words += len(f.read_text(encoding="utf-8").split())
        except Exception:
            pass
    sections = [d for d in DOCS.iterdir() if d.is_dir() and not d.name.startswith(".")]
    return {
        "files": len(all_md),
        "words": total_words,
        "sections": len(sections),
    }


def _top_projects(n: int = 8) -> list[str]:
    contacts_text = _read_md("CONTACTS.md")
    if not contacts_text:
        return []
    rows = []
    in_table = False
    for line in contacts_text.splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            if "Автор" in line or "Author" in line:
                in_table = True
                continue
            if in_table:
                rows.append(line)
    return rows[:n]


def _key_decisions(n: int = 8) -> list[str]:
    text = _read_md("DECISIONS.md")
    if not text:
        return []
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            items.append(stripped[2:].strip()[:120])
        elif re.match(r'^\d+\.', stripped):
            items.append(re.sub(r'^\d+\.\s*', '', stripped)[:120])
        if len(items) >= n:
            break
    return items


def _open_questions(n: int = 8) -> list[str]:
    text = _read_md("QUESTIONS.md")
    if not text:
        return []
    qs = [l.strip()[2:].strip()[:100]
          for l in text.splitlines()
          if l.strip().startswith("- ") and "?" in l]
    return qs[:n]


def _top_reading(n: int = 8) -> list[str]:
    """Из READING_LIST.md берём топ-N строк таблицы."""
    text = _read_md("READING_LIST.md")
    if not text:
        return []
    rows = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| #"):
            in_table = True
            continue
        if in_table and line.startswith("|") and not line.startswith("|---"):
            rows.append(line)
        elif in_table and line.startswith("##"):
            break
    return rows[:n]


def _health_metrics() -> dict:
    health_text = _read_md("HEALTH.md")
    metrics_text = _read_md("METRICS.md")
    vocab_text = _read_md("VOCABULARY.md")

    def _extr(text, label):
        m = re.search(rf'{re.escape(label)}[:\s*]+\*{{0,2}}([\d./]+%?)\*{{0,2}}', text, re.I)
        return m.group(1) if m else "—"

    health = _extr(health_text, "Балл")
    avg_doc = _extr(metrics_text, "Средний балл")
    sttr = re.search(r'STTR[^|]+\|\s*([\d.]+)', vocab_text)
    return {
        "health": health,
        "avg_doc_score": avg_doc,
        "sttr": sttr.group(1) if sttr else "—",
    }


def _generate_executive_summary(corpus: dict, metrics: dict) -> list[str]:
    """Краткий executive summary из данных."""
    lines = [
        f"**{TITLE}** — аналитический обзор базы знаний, "
        f"сгенерированный автоматически {TODAY}.\n",
        f"База содержит **{corpus['files']} документов** "
        f"объёмом **{corpus['words']:,} слов** "
        f"в **{corpus['sections']} секциях**. "
        f"Здоровье репозитория: **{metrics['health']}/100**, "
        f"средний балл документов: **{metrics['avg_doc_score']}/100**, "
        f"словарное богатство (STTR): **{metrics['sttr']}**.\n",
        "Цель базы знаний — поддержка разработки **Svyazi 2.0**, "
        "community intelligence platform, объединяющей лучшие OSS-проекты с Хабра "
        "в единую архитектуру Knowledge OS.",
    ]
    return lines


def _section_summary_table() -> list[str]:
    """Краткая таблица по секциям."""
    rows = []
    for subdir in sorted(DOCS.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue
        md_files = list(subdir.rglob("*.md"))
        if not md_files:
            continue
        total_words = 0
        for f in md_files:
            try:
                total_words += len(f.read_text(encoding="utf-8").split())
            except Exception:
                pass
        rows.append((subdir.name, len(md_files), total_words))
    rows.sort(key=lambda x: -x[2])

    LABELS = {
        "01-svyazi":               "Svyazi 2.0",
        "02-anthropic-vacancies":  "Anthropic Vacancies",
        "03-technology-combinations": "Tech Combinations",
        "04-ai-collaborations":    "AI Collaborations",
        "05-habr-projects":        "Habr Projects",
        "contacts":                "Contacts",
        "templates":               "Templates",
    }

    lines = [
        "| Секция | Файлов | Слов |",
        "|--------|--------|------|",
    ]
    for name, nfiles, nwords in rows:
        label = LABELS.get(name, name)
        lines.append(f"| **{label}** | {nfiles} | {nwords:,} |")
    return lines


def _key_entities(n: int = 10) -> list[str]:
    data = _read_json("named_entities.json")
    if not data:
        return []
    items = []
    for name, info in data.items():
        if isinstance(info, dict):
            items.append((name, info.get("type", "?"), len(info.get("files", []))))
    items.sort(key=lambda x: -x[2])
    ICONS = {"projects": "📦", "people": "👤", "tech": "⚙️", "orgs": "🏢", "dates": "📅"}
    result = []
    for ename, etype, efiles in items[:n]:
        icon = ICONS.get(etype, "❓")
        result.append(f"- {icon} **{ename}** ({etype}) — упомянут в {efiles} файлах")
    return result


def main() -> None:
    print(f"📊 improve_export_report.py — сводный отчёт")
    print(f"   Заголовок: «{TITLE}»\n")

    corpus = _corpus_stats()
    metrics = _health_metrics()
    projects = _top_projects()
    decisions = _key_decisions()
    questions = _open_questions()
    reading = _top_reading()
    entities = _key_entities()

    lines = [
        f"# {TITLE}\n",
        f"_Сгенерировано автоматически: {TODAY}_\n",
        "---\n",
    ]

    # TOC
    lines += [
        "## Содержание\n",
        "1. [Executive Summary](#executive-summary)",
        "2. [Корпус документов](#корпус-документов)",
        "3. [Ключевые проекты](#ключевые-проекты)",
        "4. [Ключевые сущности](#ключевые-сущности)",
        "5. [Архитектурные решения](#архитектурные-решения)",
        "6. [Открытые вопросы](#открытые-вопросы)",
        "7. [Рекомендуемое чтение](#рекомендуемое-чтение)",
        "",
    ]

    # Executive Summary
    lines += ["## Executive Summary\n"]
    lines += _generate_executive_summary(corpus, metrics)

    # Корпус
    lines += [
        "\n## Корпус документов\n",
        "### Общая статистика\n",
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Документов | **{corpus['files']}** |",
        f"| Слов | **{corpus['words']:,}** |",
        f"| Секций | **{corpus['sections']}** |",
        f"| Здоровье репо | **{metrics['health']}/100** |",
        f"| Средний балл | **{metrics['avg_doc_score']}/100** |",
        f"| Словарное богатство (STTR) | **{metrics['sttr']}** |",
        "\n### По секциям\n",
    ]
    lines += _section_summary_table()

    # Ключевые проекты
    if INCLUDE_PROJECTS and projects:
        lines += [
            "\n## Ключевые проекты\n",
            "_Авторы и проекты из CONTACTS.md:_\n",
            "| Автор | Проект | Слой | Приоритет |",
            "|-------|--------|------|-----------|",
        ]
        for row in projects:
            lines.append(row)

    # Ключевые сущности
    if entities:
        lines += ["\n## Ключевые сущности\n"]
        lines += entities

    # Архитектурные решения
    if decisions:
        lines += ["\n## Архитектурные решения\n",
                  "_Из DECISIONS.md:_\n"]
        for d in decisions:
            lines.append(f"- {d}")

    # Открытые вопросы
    if questions:
        lines += ["\n## Открытые вопросы\n",
                  "_Из QUESTIONS.md — вопросы, требующие решения:_\n"]
        for q in questions:
            lines.append(f"- {q}")

    # Рекомендуемое чтение
    if reading:
        lines += [
            "\n## Рекомендуемое чтение\n",
            "_Топ документов по насыщенности (из READING_LIST.md):_\n",
            "| # | Документ | Секция | Время | Слов |",
            "|---|----------|--------|-------|------|",
        ]
        for row in reading:
            lines.append(row)
    else:
        lines += [
            "\n## Рекомендуемое чтение\n",
            "_Запустите `improve_reading_list.py` для генерации списка._\n",
        ]

    lines += [
        "\n---\n",
        "## Быстрый старт\n",
        "```bash",
        "# Поиск по базе знаний",
        "python scripts/improve_passage_retrieval.py --query \"ваш запрос\"",
        "python scripts/improve_faceted_search.py --query \"RAG\" --section 05-habr-projects",
        "",
        "# Список чтения по теме",
        "python scripts/improve_reading_list.py --query \"архитектура агента\"",
        "",
        "# LLM Q&A (требует ANTHROPIC_API_KEY)",
        "python scripts/improve_llm_qa.py --question \"Что такое NGT Memory?\"",
        "```\n",
        f"_Отчёт сгенерирован автоматически скриптом `improve_export_report.py` ({TODAY})_\n",
    ]

    out = DOCS / "REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  корпус: {corpus['files']} файлов, {corpus['words']:,} слов")
    print(f"  метрики: здоровье={metrics['health']}, "
          f"балл={metrics['avg_doc_score']}, STTR={metrics['sttr']}")


if __name__ == "__main__":
    main()
