"""
improve_llm_summary.py — каскадная суммаризация больших документов через Claude API.
Stage 3b: map-reduce для документов любого размера.

Алгоритм:
  1. chunk_by_headers() — разбивка на секции
  2. LLM: summarize(chunk) → мини-резюме (map)
  3. LLM: synthesize(мини-резюме) → финальное резюме (reduce)
  4. Сохраняет в docs/DIGEST.md (обновляет секции)

Стоимость: ~$0.002 на документ (haiku). Весь репо: ~$0.15

Запуск:
    python scripts/improve_llm_summary.py --dry-run
    python scripts/improve_llm_summary.py
    python scripts/improve_llm_summary.py --file docs/05-habr-projects/memory/yodoca.md
    python scripts/improve_llm_summary.py --section 01-svyazi
"""
import re
import sys
import time
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))

from utils_chunker import chunk_by_headers, estimate_tokens, iter_md_files  # noqa: E402

DRY_RUN = "--dry-run" in sys.argv
TODAY   = date.today().isoformat()
MODEL   = "claude-haiku-4-5-20251001"

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = sys.argv[idx + 1]

FILE_FILTER = None
if "--file" in sys.argv:
    idx = sys.argv.index("--file")
    if idx + 1 < len(sys.argv):
        FILE_FILTER = ROOT / sys.argv[idx + 1]

# Минимум слов для суммаризации — короткие файлы пропускаем
MIN_WORDS = 300


# ---------------------------------------------------------------------------
# Промпты
# ---------------------------------------------------------------------------

MAP_PROMPT = """\
Кратко суммируй этот фрагмент документа в 2-3 предложениях.
Сохраняй конкретные факты, имена проектов, технические детали.
Не добавляй ничего от себя.

{chunk}"""

REDUCE_PROMPT = """\
На основе этих резюме фрагментов одного документа напиши единое связное резюме.

Документ: {title}

Фрагменты:
{summaries}

Напиши резюме в формате:
**Суть:** [1 предложение — главная идея]

**Ключевые факты:**
- [факт 1]
- [факт 2]
- [факт 3]

**Связь с Svyazi:** [1 предложение — как это используется]

Объём: 100-150 слов. Только Markdown."""


# ---------------------------------------------------------------------------
# Stage 3b: map-reduce суммаризация
# ---------------------------------------------------------------------------

def summarize_chunks(chunks: list[str], client, title: str) -> str:
    """Map: суммаризуем каждый чанк → Reduce: синтезируем финальное резюме."""
    if len(chunks) == 1:
        # Документ помещается в один чанк — суммаризуем напрямую
        resp = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": MAP_PROMPT.format(chunk=chunks[0][:3000])}],
        )
        return resp.content[0].text.strip()

    # Map: суммаризуем каждый чанк
    mini_summaries = []
    for i, chunk in enumerate(chunks):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": MAP_PROMPT.format(chunk=chunk[:2500])}],
        )
        mini_summaries.append(f"[{i+1}] {resp.content[0].text.strip()}")
        time.sleep(0.2)

    # Reduce: синтезируем
    summaries_text = "\n\n".join(mini_summaries)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content":
            REDUCE_PROMPT.format(title=title, summaries=summaries_text)}],
    )
    return resp.content[0].text.strip()


# ---------------------------------------------------------------------------
# Работа с DIGEST.md
# ---------------------------------------------------------------------------

DIGEST_PATH = DOCS / "DIGEST.md"

DIGEST_HEADER = f"""\
# Дайджест документов

<!-- summary: Автоматические резюме ключевых документов -->
<!-- tags: digest, summaries -->

_Обновлено: {TODAY}_

Каскадная суммаризация через LLM (claude-haiku-4-5).
Алгоритм: chunk → map(summarize) → reduce(synthesize).

"""

ENTRY_TEMPLATE = """\
## {title}

_Файл: [{rel_path}]({rel_path}) | Слов: {words} | Чанков: {chunks_n} | {date}_

{summary}

---
"""


def load_digest() -> dict[str, str]:
    """Загружает существующие записи DIGEST.md как {path_key: content}."""
    if not DIGEST_PATH.exists():
        return {}
    text = DIGEST_PATH.read_text(encoding="utf-8")
    # Ищем секции: ## Title\n_Файл: path ...
    result = {}
    for m in re.finditer(r'## .+?\n_Файл: \[([^\]]+)\]', text):
        result[m.group(1)] = True
    return result


def append_to_digest(entry: str) -> None:
    if not DIGEST_PATH.exists():
        DIGEST_PATH.write_text(DIGEST_HEADER, encoding="utf-8")
    with open(DIGEST_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def collect_targets() -> list[Path]:
    if FILE_FILTER:
        return [FILE_FILTER] if FILE_FILTER.exists() else []

    skip = {
        "README.md", "QA.md", "TAGS.md", "SIMILAR.md", "CONTACTS.md",
        "DECISIONS.md", "ACTION_ITEMS.md", "ENTITIES.md", "METRICS.md",
        "HEALTH.md", "SCORING.md", "CLUSTERS.md", "BACKLINKS.md", "DIGEST.md",
    }
    targets = []
    search_root = DOCS / SECTION_FILTER if SECTION_FILTER else DOCS
    for path in sorted(search_root.rglob("*.md")):
        if path.name in skip:
            continue
        text = path.read_text(encoding="utf-8")
        if len(text.split()) >= MIN_WORDS:
            targets.append(path)
    return targets


def main():
    print("📝 improve_llm_summary.py — каскадная суммаризация (map-reduce)")
    print(f"   Модель: {MODEL}")
    if DRY_RUN:
        print("   Режим: dry-run\n")

    targets = collect_targets()
    existing = load_digest()
    new_targets = [p for p in targets
                   if str(p.relative_to(ROOT)).replace("\\", "/") not in existing]

    print(f"Файлов всего: {len(targets)}, новых: {len(new_targets)}\n")

    if DRY_RUN:
        total_tokens = 0
        for path in new_targets[:20]:  # показываем первые 20
            text = path.read_text(encoding="utf-8")
            chunks = chunk_by_headers(text)
            t = sum(estimate_tokens(c) for c in chunks)
            total_tokens += t
            print(f"  {path.relative_to(DOCS)}: {len(chunks)} чанков, ~{t:,} токенов")
        if len(new_targets) > 20:
            print(f"  ... и ещё {len(new_targets) - 20} файлов")
        cost = total_tokens / 1_000_000 * 0.25 * 2  # map + reduce
        print(f"\nОценка стоимости (map+reduce): ~${cost:.3f}")
        return

    try:
        import anthropic
    except ImportError:
        print("❌ Установите anthropic: pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic()
    ok = 0

    for path in new_targets:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        text = path.read_text(encoding="utf-8")
        words = len(text.split())
        chunks = chunk_by_headers(text)

        title_m = re.search(r'^#\s+(.+)', text, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else path.stem

        print(f"  🔄 {path.relative_to(DOCS)} ({len(chunks)} чанков)...")
        try:
            summary = summarize_chunks(chunks, client, title)
            entry = ENTRY_TEMPLATE.format(
                title=title,
                rel_path=rel,
                words=words,
                chunks_n=len(chunks),
                date=TODAY,
                summary=summary,
            )
            append_to_digest(entry)
            print(f"  ✅ добавлено в DIGEST.md")
            ok += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  ❌ {path.stem}: {e}")

    print(f"\n✅ Суммаризовано: {ok} файлов → docs/DIGEST.md")


if __name__ == "__main__":
    main()
