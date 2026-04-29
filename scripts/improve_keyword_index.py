"""
improve_keyword_index.py — инвертированный индекс: слово → файлы.

Строит инвертированный индекс без поискового движка:
  - word → [{file, count, positions, section}]
  - Быстрый offline-поиск без search_index.json
  - Поддержка биграмм (двусловных фраз)
  - Статистика: уникальных слов, охват файлов

Создаёт docs/keyword_index.json + docs/KEYWORD_INDEX.md.
Запуск:
    python scripts/improve_keyword_index.py
    python scripts/improve_keyword_index.py --section 05-habr-projects
    python scripts/improve_keyword_index.py --min-df 2
    python scripts/improve_keyword_index.py --top 50
    python scripts/improve_keyword_index.py --query "агент память"
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MIN_DF = 1        # минимальное число файлов, в которых встречается слово
TOP_WORDS = 100   # топ слов для KEYWORD_INDEX.md
BIGRAMS = True    # включить биграммы

if "--min-df" in sys.argv:
    idx = sys.argv.index("--min-df")
    if idx + 1 < len(sys.argv):
        MIN_DF = int(sys.argv[idx + 1])

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP_WORDS = int(sys.argv[idx + 1])

QUERY = None
if "--query" in sys.argv:
    idx = sys.argv.index("--query")
    if idx + 1 < len(sys.argv):
        QUERY = sys.argv[idx + 1].lower().strip()

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "KEYWORD_INDEX.md", "SEARCH.md", "NAMED_ENTITIES.md",
    "CONCEPT_GRAPH.md", "SOURCE_MAP.md", "TIMELINE.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "этот", "эта", "его", "её", "их",
    "мы", "вы", "он", "она", "они", "при", "от", "до", "об", "же",
    "бы", "ли", "да", "нет", "есть", "была", "были", "будет", "всё",
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "can", "could", "should", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "or", "and", "not", "but", "it",
    "its", "we", "you", "they", "their", "our", "this", "that",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return text


def _tokens(text: str) -> list[str]:
    return [
        t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
        if t not in STOPWORDS
    ]


def _section_of(path: Path) -> str:
    try:
        rel = path.relative_to(DOCS)
        parts = rel.parts
        return parts[0] if len(parts) > 1 else "root"
    except ValueError:
        return "unknown"


def build_index(files: list[Path]) -> dict[str, list[dict]]:
    """
    Строит инвертированный индекс.
    Returns: {word: [{file, section, count, tf}]}
    """
    index: dict[str, list[dict]] = defaultdict(list)

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        rel = str(f.relative_to(ROOT))
        section = _section_of(f)
        clean = _clean(text)
        tokens = _tokens(clean)

        if not tokens:
            continue

        freq = Counter(tokens)
        total = len(tokens)

        for word, count in freq.items():
            index[word].append({
                "file": rel,
                "section": section,
                "count": count,
                "tf": round(count / total, 5),
            })

        if BIGRAMS:
            bigram_freq: Counter = Counter()
            for i in range(len(tokens) - 1):
                bg = tokens[i] + "_" + tokens[i + 1]
                bigram_freq[bg] += 1
            for bg, count in bigram_freq.items():
                if count >= 2:
                    index[bg].append({
                        "file": rel,
                        "section": section,
                        "count": count,
                        "tf": round(count / total, 5),
                    })

    # Применяем MIN_DF
    filtered = {
        w: entries
        for w, entries in index.items()
        if len(entries) >= MIN_DF
    }

    # Сортируем вхождения по убыванию count
    for w in filtered:
        filtered[w].sort(key=lambda x: -x["count"])

    return filtered


def search(index: dict, query: str) -> list[dict]:
    """Поиск по индексу: возвращает файлы по убыванию релевантности."""
    terms = [t for t in query.lower().split() if t not in STOPWORDS and len(t) >= 3]
    if not terms:
        return []

    scores: Counter = Counter()
    for term in terms:
        for entry in index.get(term, []):
            scores[entry["file"]] += entry["tf"] * 10
        # биграммы
        if len(terms) > 1:
            for i in range(len(terms) - 1):
                bg = terms[i] + "_" + terms[i + 1]
                for entry in index.get(bg, []):
                    scores[entry["file"]] += entry["tf"] * 20  # биграммы важнее

    return [{"file": f, "score": round(s, 4)} for f, s in scores.most_common(20)]


def main() -> None:
    print("🔍 improve_keyword_index.py — инвертированный индекс")
    print(f"   MIN_DF={MIN_DF} | TOP={TOP_WORDS} | Биграммы: {BIGRAMS}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "confluence" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    index = build_index(files)

    unigrams = {w: e for w, e in index.items() if "_" not in w}
    bigrams  = {w: e for w, e in index.items() if "_" in w}

    print(f"   Уникальных слов: {len(unigrams)}")
    print(f"   Биграмм: {len(bigrams)}")
    total_entries = sum(len(e) for e in index.values())
    print(f"   Записей в индексе: {total_entries}")

    # Поиск по запросу
    if QUERY:
        print(f"\n🔎 Поиск: «{QUERY}»")
        results = search(index, QUERY)
        if results:
            for i, r in enumerate(results[:10], 1):
                print(f"  {i:2d}. {r['file']} (score: {r['score']})")
        else:
            print("  Ничего не найдено.")
        return

    # Топ слов по df (document frequency)
    top_by_df = sorted(unigrams.items(), key=lambda x: -len(x[1]))[:TOP_WORDS]

    # Markdown
    lines = [
        "# Инвертированный индекс ключевых слов\n",
        f"_Обновлено: {TODAY}_\n",
        f"Уникальных слов: **{len(unigrams)}** | Биграмм: **{len(bigrams)}** | "
        f"Файлов: **{len(files)}**\n",
        f"> `python scripts/improve_keyword_index.py --query \"ваш запрос\"` — поиск по индексу\n",
        "## Топ слов по охвату файлов\n",
        "| Слово | Файлов | Всего упоминаний |",
        "|-------|--------|-----------------|",
    ]

    for word, entries in top_by_df:
        df = len(entries)
        total_count = sum(e["count"] for e in entries)
        lines.append(f"| `{word}` | {df} | {total_count} |")

    # Топ биграмм
    top_bg = sorted(bigrams.items(), key=lambda x: -len(x[1]))[:30]
    if top_bg:
        lines += [
            "\n## Топ биграмм (устойчивые словосочетания)\n",
            "| Биграмм | Файлов | Всего |",
            "|---------|--------|-------|",
        ]
        for bg, entries in top_bg:
            phrase = bg.replace("_", " ")
            df = len(entries)
            total_count = sum(e["count"] for e in entries)
            lines.append(f"| `{phrase}` | {df} | {total_count} |")

    out_md = DOCS / "KEYWORD_INDEX.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out_md.relative_to(ROOT)}")

    # JSON (только слова с df >= MIN_DF, без биграмм для компактности)
    json_data = {
        "generated": TODAY,
        "total_words": len(unigrams),
        "total_bigrams": len(bigrams),
        "total_files": len(files),
        "index": {
            w: [{"f": e["file"], "n": e["count"]} for e in entries[:10]]
            for w, entries in sorted(unigrams.items(), key=lambda x: -len(x[1]))[:2000]
        },
        "bigrams": {
            bg.replace("_", " "): [{"f": e["file"], "n": e["count"]} for e in entries[:5]]
            for bg, entries in sorted(bigrams.items(), key=lambda x: -len(x[1]))[:500]
        },
    }
    out_json = DOCS / "keyword_index.json"
    out_json.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote: {out_json.relative_to(ROOT)}")
    print(f"  топ-5: {', '.join(w for w, _ in top_by_df[:5])}")


if __name__ == "__main__":
    main()
