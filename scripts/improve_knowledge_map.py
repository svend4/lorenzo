"""
improve_knowledge_map.py — единый дашборд всей базы знаний.

Агрегирует данные из всех отчётных файлов и строит единую карту:
  - Общая статистика корпуса
  - Топ файлов по важности (из PRIORITIES.md / SCORING.md)
  - Состояние по секциям (файлов, слов, качество)
  - Граф ключевых связей (из CONCEPT_GRAPH.md)
  - Открытые вопросы и TODO (из QUESTIONS.md)
  - Метрики качества (из HEALTH.md / METRICS.md)
  - Сущности (из NAMED_ENTITIES.md)

Создаёт docs/KNOWLEDGE_MAP.md — «стартовая страница» базы знаний.
Запуск:
    python scripts/improve_knowledge_map.py
"""
import json
import re
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

SKIP_COUNT = {
    "KNOWLEDGE_MAP.md", "SEARCH.md", "PROGRESS.md",
    "HEADING_AUDIT.md", "PARAGRAPH_QUALITY.md", "CONTRADICTIONS.md",
    "SIMILAR_PASSAGES.md", "PASSIVE_VOICE.md", "EMPTY_SECTIONS.md",
}


def _read_md(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _read_json(name: str) -> dict | list:
    p = DOCS / name
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _extract_score(text: str, label: str) -> str:
    """Ищет паттерн вида 'label: **X/Y**' или 'label** X/Y'."""
    m = re.search(rf'{re.escape(label)}[:\s*]+\*{{0,2}}([\d./]+%?)\*{{0,2}}', text, re.I)
    return m.group(1) if m else "—"


def _section_stats(docs_dir: Path) -> list[dict]:
    sections = []
    for subdir in sorted(docs_dir.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue
        md_files = [f for f in subdir.rglob("*.md")
                    if f.name not in SKIP_COUNT and "-parts" not in str(f)]
        if not md_files:
            continue
        total_words = 0
        for f in md_files:
            try:
                total_words += len(f.read_text(encoding="utf-8").split())
            except Exception:
                pass
        sections.append({
            "name": subdir.name,
            "files": len(md_files),
            "words": total_words,
            "avg_words": total_words // max(len(md_files), 1),
        })
    return sections


def _top_entities(n: int = 10) -> list[tuple[str, str, int]]:
    data = _read_json("named_entities.json")
    if not data:
        return []
    items = []
    for name, info in data.items():
        if isinstance(info, dict):
            items.append((name, info.get("type", "?"), len(info.get("files", []))))
    return sorted(items, key=lambda x: -x[2])[:n]


def _open_questions(n: int = 10) -> list[str]:
    text = _read_md("QUESTIONS.md")
    if not text:
        return []
    lines = [l.strip() for l in text.splitlines()
             if l.strip().startswith("- ") and "?" in l]
    return [l[2:].strip()[:100] for l in lines[:n]]


def _top_concepts(n: int = 8) -> list[tuple[str, int, str]]:
    data = _read_json("concept_graph.json")
    if not data or "nodes" not in data:
        return []
    nodes = sorted(data["nodes"], key=lambda x: -x.get("files", 0))[:n]
    return [(nd["id"], nd.get("files", 0), nd.get("category", "?")) for nd in nodes]


def _corpus_stats(docs_dir: Path) -> dict:
    all_md = [f for f in docs_dir.rglob("*.md")
              if f.name not in SKIP_COUNT and "-parts" not in str(f)
              and "obsidian" not in str(f)]
    total_words = 0
    for f in all_md:
        try:
            total_words += len(f.read_text(encoding="utf-8").split())
        except Exception:
            pass
    return {
        "files": len(all_md),
        "words": total_words,
    }


def _chunk_stats() -> dict:
    chunks_dir = DOCS / "chunks"
    if not chunks_dir.exists():
        return {}
    total = 0
    sections = 0
    for f in chunks_dir.glob("*.jsonl"):
        if f.name == "all_chunks.jsonl":
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
                total = len(lines)
            except Exception:
                pass
        elif f.name != "all_chunks.jsonl":
            sections += 1
    return {"total": total, "sections": sections}


def main() -> None:
    print("🗺️  improve_knowledge_map.py — карта знаний")

    corpus = _corpus_stats(DOCS)
    sections = _section_stats(DOCS)
    entities_top = _top_entities(12)
    questions = _open_questions(8)
    concepts = _top_concepts(8)
    chunks = _chunk_stats()

    # Метрики качества из существующих отчётов
    health_text   = _read_md("HEALTH.md")
    metrics_text  = _read_md("METRICS.md")
    vocab_text    = _read_md("VOCABULARY.md")
    passive_text  = _read_md("PASSIVE_VOICE.md")
    heading_text  = _read_md("HEADING_AUDIT.md")
    empty_text    = _read_md("EMPTY_SECTIONS.md")
    para_text     = _read_md("PARAGRAPH_QUALITY.md")
    lang_text     = _read_md("LANGUAGE_STATS.md")
    contra_text   = _read_md("CONTRADICTIONS.md")

    health_score  = _extract_score(health_text, "Балл")
    metrics_score = _extract_score(metrics_text, "Средний балл")
    sttr_val      = _extract_score(vocab_text, "Средний STTR")
    passive_pct   = _extract_score(passive_text, "Средний пассив")
    empty_count   = re.search(r'Пустых секций:\s*\*\*(\d+)', empty_text)
    empty_n       = empty_count.group(1) if empty_count else "—"
    # Ищем строго «Противоречий: **N**» (не «Утверждений: N | Противоречий: N»)
    contra_count  = re.search(r'\|\s*Противоречий:\s*\*\*(\d+)\*\*|'
                              r'^Противоречий:\s*\*\*(\d+)', contra_text, re.M)
    if not contra_count:
        # Fallback: строка вида «Утверждений: X | Противоречий: Y»
        contra_count = re.search(r'Противоречий:\s*\*\*(\d[\d,]*)\*\*', contra_text)
    contra_n = (contra_count.group(1) or contra_count.group(2)
                if contra_count and (contra_count.group(1) or (contra_count.lastindex or 0) >= 2)
                else contra_count.group(1) if contra_count else "—")
    # STTR: ищем в таблице корпусной статистики
    sttr_m = re.search(r'STTR[^|]+\|\s*([\d.]+)', vocab_text)
    if sttr_m:
        sttr_val = sttr_m.group(1)

    lines = [
        "# Карта базы знаний Lorenzo\n",
        f"_Обновлено: {TODAY}_\n",
        "---\n",
        "## Корпус\n",
        "| Параметр | Значение |",
        "|----------|----------|",
        f"| Документов | **{corpus['files']}** |",
        f"| Слов | **{corpus['words']:,}** |",
        f"| Секций | **{len(sections)}** |",
        f"| RAG-чанков | **{chunks.get('total', '—')}** (по {chunks.get('sections', '—')} секциям) |",
        "\n## Метрики качества\n",
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Здоровье репо | {health_score} |",
        f"| Средний балл документов | {metrics_score} |",
        f"| Словарное богатство (STTR) | {sttr_val} |",
        f"| Пассивный залог | {passive_pct} |",
        f"| Пустых секций | {empty_n} |",
        f"| Противоречий | {contra_n} |",
        "\n## По секциям\n",
        "| Секция | Файлов | Слов | Ср. слов/файл |",
        "|--------|--------|------|---------------|",
    ]

    for sec in sorted(sections, key=lambda x: -x["words"]):
        lines.append(
            f"| `{sec['name']}` | {sec['files']} | {sec['words']:,} | {sec['avg_words']} |"
        )

    if concepts:
        lines += [
            "\n## Ключевые концепты\n",
            "| Концепт | Файлов | Категория |",
            "|---------|--------|-----------|",
        ]
        for cname, cfiles, ccat in concepts:
            lines.append(f"| `{cname}` | {cfiles} | {ccat} |")

    if entities_top:
        lines += [
            "\n## Топ сущностей\n",
            "| Сущность | Тип | Файлов |",
            "|----------|-----|--------|",
        ]
        for ename, etype, efiles in entities_top:
            type_icon = {"projects": "📦", "people": "👤", "tech": "⚙️",
                         "orgs": "🏢", "dates": "📅"}.get(etype, "❓")
            lines.append(f"| `{ename}` | {type_icon} {etype} | {efiles} |")

    if questions:
        lines += ["\n## Открытые вопросы\n"]
        for q in questions:
            lines.append(f"- {q}")

    lines += [
        "\n## Быстрые команды\n",
        "```bash",
        "# Поиск",
        "python scripts/improve_passage_retrieval.py --query \"ваш запрос\"",
        "python scripts/improve_faceted_search.py --query \"ваш запрос\"",
        "python scripts/improve_keyword_index.py --query \"ваш запрос\"",
        "",
        "# Улучшение контента",
        "python scripts/improve_auto_toc.py --apply",
        "python scripts/improve_abstract.py --apply",
        "python scripts/improve_auto_linker.py --apply --types projects",
        "python scripts/improve_empty_sections.py --fill",
        "",
        "# Полный прогон",
        "python scripts/improve_run_all.py --group deeptext",
        "python scripts/improve_run_all.py --group nlpplus",
        "```\n",
        f"_Карта сгенерирована автоматически: {TODAY}_\n",
    ]

    out = DOCS / "KNOWLEDGE_MAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  корпус: {corpus['files']} файлов, {corpus['words']:,} слов")
    print(f"  секций: {len(sections)}")


if __name__ == "__main__":
    main()
