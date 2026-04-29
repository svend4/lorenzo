"""
improve_llm_enrich.py — семантическое обогащение проектных файлов через Claude API.
Stage 3a: скрипт управляет процессом, LLM заполняет то, что regex не может.

Что делает:
  Для каждого файла в docs/05-habr-projects/ и docs/04-ai-collaborations/:
  1. Детерминированно извлекает факты (теги, упоминания, чанки)
  2. Вызывает Claude для генерации структурированного описания
  3. Сохраняет в docs/enriched/<section>/<name>-enriched.md

Требует: pip install anthropic
Стоимость: ~$0.001 на файл (claude-haiku-4-5)
           ~$0.03 для всех ~30 проектных файлов

Запуск:
    python scripts/improve_llm_enrich.py --dry-run    # план без запроса к API
    python scripts/improve_llm_enrich.py              # реальный запуск
    python scripts/improve_llm_enrich.py --section 05-habr-projects
    python scripts/improve_llm_enrich.py --model claude-haiku-4-5-20251001
"""
import re
import sys
import json
import time
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))

from utils_chunker import chunk_by_headers, estimate_tokens  # noqa: E402

DRY_RUN  = "--dry-run" in sys.argv
SECTIONS = ["05-habr-projects", "04-ai-collaborations"]
TODAY    = date.today().isoformat()
OUT_DIR  = DOCS / "enriched"

# Модель по умолчанию — haiku (дешевле для препроцессинга)
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
for arg in sys.argv:
    if arg.startswith("--model="):
        DEFAULT_MODEL = arg.split("=", 1)[1]
if "--model" in sys.argv:
    idx = sys.argv.index("--model")
    if idx + 1 < len(sys.argv):
        DEFAULT_MODEL = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = sys.argv[idx + 1]


# ---------------------------------------------------------------------------
# Stage 0: детерминированное извлечение фактов
# ---------------------------------------------------------------------------

def extract_facts(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    # Теги из комментария <!-- tags: ... -->
    tag_m = re.search(r'<!--\s*tags:\s*([^>]+)-->', text)
    tags = [t.strip() for t in tag_m.group(1).split(",")] if tag_m else []

    # Summary
    sum_m = re.search(r'<!--\s*summary[^>]*-->\s*>\s*(.+)', text)
    summary = sum_m.group(1).strip()[:300] if sum_m else ""

    # Заголовок
    title_m = re.search(r'^#\s+(.+)', text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.stem

    # Проекты из блока "**Проекты:**"
    proj_m = re.search(r'\*\*Проекты:\*\*\s*(.+)', text)
    projects = proj_m.group(1).strip() if proj_m else ""

    # Чанки по заголовкам (для длинных файлов)
    chunks = chunk_by_headers(text, max_words=1200)

    return {
        "title":    title,
        "tags":     tags,
        "summary":  summary,
        "projects": projects,
        "chunks":   chunks,
        "path":     str(path.relative_to(ROOT)),
        "tokens":   sum(estimate_tokens(c) for c in chunks),
    }


# ---------------------------------------------------------------------------
# Stage 3: LLM-генерация структурированного описания
# ---------------------------------------------------------------------------

ENRICH_PROMPT = """\
Ты помогаешь структурировать исследовательские заметки о проекте для базы знаний Svyazi 2.0.

**Проект:** {title}
**Теги:** {tags}
**Упомянутые проекты:** {projects}
**Краткое резюме:** {summary}

**Исходные фрагменты текста:**
{excerpts}

---

Напиши структурированное описание в формате Markdown. Используй ТОЛЬКО информацию из фрагментов — не придумывай.

## Что это
[2-3 предложения: какую задачу решает проект, ключевая идея]

## Ключевые особенности
- **Особенность 1:** [конкретный технический факт из текста]
- **Особенность 2:** [конкретный технический факт]
- **Особенность 3:** [конкретный технический факт]

## Статус проекта
| Параметр | Значение |
|----------|---------|
| Язык/стек | [из текста или —] |
| Лицензия | [из текста или —] |
| Ссылка | [URL если есть в тексте или —] |

## Интеграция с Svyazi
[1-2 предложения: как этот проект вписывается в слой {tags_first}]

Объём: 150-250 слов. Только Markdown, без лишних объяснений."""


def enrich_with_llm(facts: dict, client, model: str) -> str:
    """Stage 3: вызов LLM для семантического обогащения."""
    # Берём не более 3 чанков — оптимум цена/качество
    excerpts_parts = []
    for i, chunk in enumerate(facts["chunks"][:3]):
        excerpts_parts.append(f"[Фрагмент {i+1}]\n{chunk[:2000]}")
    excerpts = "\n\n".join(excerpts_parts)

    tags_first = facts["tags"][0] if facts["tags"] else "core"

    prompt = ENRICH_PROMPT.format(
        title=facts["title"],
        tags=", ".join(facts["tags"]) or "—",
        projects=facts["projects"] or "—",
        summary=facts["summary"] or "—",
        excerpts=excerpts,
        tags_first=tags_first,
    )

    resp = client.messages.create(
        model=model,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


# ---------------------------------------------------------------------------
# Сборка финального файла
# ---------------------------------------------------------------------------

ENRICHED_HEADER = """\
# {title}

<!-- summary: {summary_short} -->
<!-- tags: {tags} -->
<!-- enriched: {today} by improve_llm_enrich.py -->
<!-- source: {source_path} -->

"""

ENRICHED_FOOTER = """
---
_Обогащено автоматически: {today}_
_Источник: [{source_name}]({source_path})_
"""


def build_enriched(facts: dict, llm_content: str) -> str:
    summary_short = facts["summary"][:100] if facts["summary"] else facts["title"]
    header = ENRICHED_HEADER.format(
        title=facts["title"],
        summary_short=summary_short,
        tags=", ".join(facts["tags"]),
        today=TODAY,
        source_path=facts["path"],
    )
    footer = ENRICHED_FOOTER.format(
        today=TODAY,
        source_name=Path(facts["path"]).stem,
        source_path=facts["path"],
    )
    return header + llm_content + footer


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    print("🤖 improve_llm_enrich.py — семантическое обогащение через LLM")
    print(f"   Модель: {DEFAULT_MODEL}")
    if DRY_RUN:
        print("   Режим: dry-run (API не вызывается)\n")
    else:
        print()

    # Собираем целевые файлы
    target_sections = SECTIONS if not SECTION_FILTER else [SECTION_FILTER]
    targets: list[Path] = []
    for section in target_sections:
        sec_path = DOCS / section
        if not sec_path.exists():
            continue
        for md in sorted(sec_path.rglob("*.md")):
            if md.name in ("README.md", "QA.md"):
                continue
            targets.append(md)

    print(f"Файлов для обогащения: {len(targets)}")

    # Dry-run: показываем план
    if DRY_RUN:
        total_tokens = 0
        for path in targets:
            facts = extract_facts(path)
            t = facts["tokens"]
            total_tokens += t
            chunks_n = len(facts["chunks"])
            print(f"  {path.relative_to(DOCS)}: {chunks_n} чанков, ~{t:,} токенов")
        cost = total_tokens / 1_000_000 * 0.25
        print(f"\nИтого: ~{total_tokens:,} токенов, стоимость ~${cost:.3f}")
        return

    # Реальный запуск
    try:
        import anthropic
    except ImportError:
        print("❌ Установите anthropic: pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic()
    OUT_DIR.mkdir(exist_ok=True)

    ok = 0
    errors = 0
    for path in targets:
        # Определяем выходной путь
        section = path.relative_to(DOCS).parts[0]
        out_section = OUT_DIR / section
        out_section.mkdir(parents=True, exist_ok=True)
        out_path = out_section / f"{path.stem}-enriched.md"

        if out_path.exists():
            print(f"  ⏩ {path.stem} — уже обогащён, пропускаем")
            continue

        print(f"  🔄 {path.relative_to(DOCS)}...")
        try:
            facts = extract_facts(path)
            llm_text = enrich_with_llm(facts, client, DEFAULT_MODEL)
            enriched = build_enriched(facts, llm_text)
            out_path.write_text(enriched, encoding="utf-8")
            print(f"  ✅ → {out_path.relative_to(ROOT)}")
            ok += 1
            time.sleep(0.3)  # rate-limit
        except Exception as e:
            print(f"  ❌ {path.stem}: {e}")
            errors += 1

    print(f"\n✅ Готово: {ok} обогащено, {errors} ошибок")
    print(f"   Результаты: {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
