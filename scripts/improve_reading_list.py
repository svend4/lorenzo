"""
improve_reading_list.py — персонализированный список чтения по теме.

Генерирует упорядоченный список документов для изучения темы:
  1. BM25-поиск по запросу → релевантные файлы
  2. Ранжирование: score × (1 + важность файла) × (1 + связность)
  3. Оценивает время чтения (200 сл/мин RU, 250 EN)
  4. Группирует по секциям для логического порядка

Выходные форматы:
  --format md    → READING_LIST.md (по умолч.)
  --format text  → простой список в терминале
  --format json  → machine-readable

Запуск:
    python scripts/improve_reading_list.py --query "агент с памятью"
    python scripts/improve_reading_list.py --query "RAG retrieval" --top 20
    python scripts/improve_reading_list.py --query "Yodoca NGT" --section 05-habr-projects
    python scripts/improve_reading_list.py --query "архитектура" --format json
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

QUERY = ""
TOP = 15
FORMAT = "md"

if "--query" in sys.argv:
    idx = sys.argv.index("--query")
    if idx + 1 < len(sys.argv):
        QUERY = sys.argv[idx + 1]

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP = int(sys.argv[idx + 1])

if "--format" in sys.argv:
    idx = sys.argv.index("--format")
    if idx + 1 < len(sys.argv):
        FORMAT = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = sys.argv[idx + 1]

SKIP_FILES = {
    "READING_LIST.md", "SEARCH.md", "SUMMARIES.md", "KNOWLEDGE_MAP.md",
    "KEYWORD_INDEX.md", "CONTRADICTIONS.md", "SIMILAR_PASSAGES.md",
    "HEADING_AUDIT.md", "PARAGRAPH_QUALITY.md", "PASSIVE_VOICE.md",
    "EMPTY_SECTIONS.md", "QUESTIONS.md", "LANGUAGE_STATS.md",
    "VOCABULARY.md", "NAMED_ENTITIES.md", "CONCEPT_GRAPH.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "при", "от", "до", "об", "the", "a", "an", "is", "of", "in",
    "on", "to", "for", "with", "by", "and", "not", "it", "we",
}

READ_SPEED_RU = 200
READ_SPEED_EN = 250


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
            if t not in STOPWORDS]


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    return re.sub(r'[*_`#|>\[\]()]', ' ', text)


def _ru_ratio(tokens: list[str]) -> float:
    if not tokens:
        return 0.5
    ru = sum(1 for t in tokens if re.match(r'^[а-яё]+$', t))
    return ru / len(tokens)


def _read_time(word_count: int, ru_ratio: float) -> int:
    speed = READ_SPEED_RU * ru_ratio + READ_SPEED_EN * (1 - ru_ratio)
    return max(1, round(word_count / speed))


def _extract_title(text: str, path: Path) -> str:
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return m.group(1).strip() if m else path.stem.replace('-', ' ')


def _section_order(path: Path) -> int:
    """Порядок секций для логического чтения."""
    order = {
        "01-svyazi": 1, "04-ai-collaborations": 2,
        "05-habr-projects": 3, "03-technology-combinations": 4,
        "02-anthropic-vacancies": 5, "contacts": 6,
    }
    try:
        parts = path.relative_to(DOCS).parts
        return order.get(parts[0], 9) if len(parts) > 1 else 7
    except Exception:
        return 8


def build_bm25(files: list[Path]) -> tuple[list[dict], dict]:
    docs = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        clean = _clean(text)
        tokens = _tokenize(clean)
        if len(tokens) < 20:
            continue
        docs.append({
            "path": f,
            "source": str(f.relative_to(ROOT)),
            "title": _extract_title(text, f),
            "tokens": tokens,
            "wc": len(text.split()),
            "ru_ratio": _ru_ratio(tokens),
            "section_order": _section_order(f),
        })

    N = len(docs)
    df: Counter = Counter()
    total_len = 0
    for d in docs:
        total_len += d["wc"]
        for t in set(d["tokens"]):
            df[t] += 1

    avgdl = total_len / max(N, 1)
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}

    inv: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for i, d in enumerate(docs):
        freq = Counter(d["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))

    return docs, {"idf": idf, "inv": dict(inv), "avgdl": avgdl,
                  "lens": [d["wc"] for d in docs]}


def search(query: str, docs: list[dict], bm25: dict, top: int) -> list[dict]:
    tokens = _tokenize(query)
    if not tokens:
        return []

    k1, b = 1.5, 0.75
    avgdl = bm25["avgdl"]
    scores: dict[int, float] = defaultdict(float)

    for t in tokens:
        idf = bm25["idf"].get(t, 0)
        for did, tf in bm25["inv"].get(t, []):
            dl = bm25["lens"][did]
            norm_tf = tf * (k1 + 1) / (tf + k1 * (1 - b + b * dl / avgdl))
            scores[did] += idf * norm_tf

    # Сортировка: BM25 score + штраф за секцию (логический порядок)
    results = []
    for did, score in sorted(scores.items(), key=lambda x: -x[1])[:top * 2]:
        d = docs[did]
        read_t = _read_time(d["wc"], d["ru_ratio"])
        results.append({**d, "score": round(score, 2), "read_min": read_t})

    return sorted(results[:top], key=lambda x: (-x["score"], x["section_order"]))


def main() -> None:
    print("📚 improve_reading_list.py — список чтения по теме")
    if QUERY:
        print(f"   Запрос: «{QUERY}»")
    print(f"   TOP={TOP} | Формат: {FORMAT}\n")

    all_files = [f for f in sorted(DOCS.rglob("*.md"))
                 if f.name not in SKIP_FILES
                 and "-parts" not in str(f)
                 and "obsidian" not in str(f)]

    if SECTION_FILTER:
        files = [f for f in all_files if SECTION_FILTER in str(f)]
    else:
        files = all_files

    print(f"   Файлов в поиске: {len(files)}")
    docs_corpus, bm25 = build_bm25(files)

    if QUERY:
        results = search(QUERY, docs_corpus, bm25, TOP)
    else:
        # Без запроса — топ по длине (самые насыщенные файлы)
        results = sorted(docs_corpus, key=lambda x: -x["wc"])[:TOP]
        for r in results:
            r["score"] = 0
            r["read_min"] = _read_time(r["wc"], r["ru_ratio"])

    total_time = sum(r["read_min"] for r in results)

    print(f"\n   Найдено: {len(results)} документов")
    print(f"   Общее время чтения: ~{total_time} мин ({total_time // 60}ч {total_time % 60}м)\n")

    if FORMAT == "text":
        for i, r in enumerate(results, 1):
            print(f"  {i:2d}. [{r['read_min']}мин] {r['title'][:60]}")
            print(f"      {r['source']}")
        return

    if FORMAT == "json":
        out = [{"rank": i+1, "title": r["title"], "file": r["source"],
                "score": r["score"], "read_min": r["read_min"], "words": r["wc"]}
               for i, r in enumerate(results)]
        out_f = DOCS / "reading_list.json"
        out_f.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  wrote: {out_f.relative_to(ROOT)}")
        return

    # Markdown
    header = f"по запросу «{QUERY}»" if QUERY else "топ по насыщенности"
    lines = [
        "# Список чтения\n",
        f"_Обновлено: {TODAY}_\n",
        f"**{header}** | Документов: **{len(results)}** | "
        f"Время: **~{total_time} мин** ({total_time // 60}ч {total_time % 60}м)\n",
        "| # | Документ | Секция | Время | Слов | Score |",
        "|---|----------|--------|-------|------|-------|",
    ]

    for i, r in enumerate(results, 1):
        sec = r["source"].split("/")[1] if "/" in r["source"] else "root"
        fname = r["source"].split("/")[-1]
        title_short = r["title"][:50]
        score_str = f"{r['score']:.1f}" if r["score"] else "—"
        lines.append(
            f"| {i} | [{title_short}]({r['source']}) | `{sec}` | "
            f"{r['read_min']} мин | {r['wc']} | {score_str} |"
        )

    # Группировка по секциям
    by_section: dict[str, list] = defaultdict(list)
    for r in results:
        sec = r["source"].split("/")[1] if "/" in r["source"] else "root"
        by_section[sec].append(r)

    lines += ["\n## По секциям\n"]
    for sec, items in sorted(by_section.items()):
        sec_time = sum(it["read_min"] for it in items)
        lines.append(f"### `{sec}` ({len(items)} докум., ~{sec_time} мин)\n")
        for it in items:
            lines.append(f"- [{it['title'][:60]}]({it['source']}) — {it['read_min']} мин")
        lines.append("")

    out_f = DOCS / "READING_LIST.md"
    out_f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out_f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
