"""
improve_gap_filler.py — заполняет пустые секции найденным контентом (BM25).

Для каждой пустой секции (< MIN_CONTENT слов):
  1. Использует заголовок как поисковый запрос (BM25)
  2. Находит релевантные абзацы из других файлов
  3. Вставляет их как цитату-подсказку или сноску

Режимы:
  --dry-run   (по умолч.) — показывает что найдено
  --apply     — вставляет контент в файлы
  --mode cite — вставляет как blockquote с источником
  --mode link — вставляет только ссылку на файл-источник
  --top N     — брать топ-N найденных абзацев (по умолч.: 1)
  --section   — ограничить секцию

Запуск:
    python scripts/improve_gap_filler.py --dry-run
    python scripts/improve_gap_filler.py --apply --mode link --section 05-habr-projects
    python scripts/improve_gap_filler.py --apply --mode cite --top 2
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

APPLY   = "--apply" in sys.argv
DRY_RUN = not APPLY
MODE    = "link"   # cite | link
TOP     = 1
MIN_CONTENT = 15   # слов — порог "пустой секции"

if "--mode" in sys.argv:
    idx = sys.argv.index("--mode")
    if idx + 1 < len(sys.argv):
        MODE = sys.argv[idx + 1]

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP = int(sys.argv[idx + 1])

if "--min-content" in sys.argv:
    idx = sys.argv.index("--min-content")
    if idx + 1 < len(sys.argv):
        MIN_CONTENT = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "KNOWLEDGE_MAP.md", "SEARCH.md", "SUMMARIES.md", "SIMILAR_PASSAGES.md",
    "KEYWORD_INDEX.md", "CONTRADICTIONS.md", "HEADING_AUDIT.md",
    "EMPTY_SECTIONS.md", "QUESTIONS.md", "PASSIVE_VOICE.md",
    "PARAGRAPH_QUALITY.md", "VOCABULARY.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "при", "от", "до", "об", "the", "a", "an", "is", "of", "in",
    "on", "to", "for", "with", "by", "and", "not", "it", "we",
}

BM25_K1 = 1.5
BM25_B  = 0.75


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
            if t not in STOPWORDS]


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _build_corpus(files: list[Path]) -> tuple[list[dict], dict]:
    """Строит BM25-корпус абзацев из всех файлов."""
    passages = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(f.relative_to(ROOT))
        paras = re.split(r'\n{2,}', text)
        for para in paras:
            clean = _clean(para)
            tokens = _tokenize(clean)
            if len(tokens) < 15:
                continue
            passages.append({
                "source": rel,
                "text": clean[:300],
                "tokens": tokens,
                "wc": len(clean.split()),
            })

    N = len(passages)
    df: Counter = Counter()
    total_len = 0
    for p in passages:
        total_len += p["wc"]
        for t in set(p["tokens"]):
            df[t] += 1

    avgdl = total_len / max(N, 1)
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}

    inv: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))

    bm25 = {"idf": idf, "inv": dict(inv), "avgdl": avgdl,
             "lens": [p["wc"] for p in passages]}
    return passages, bm25


def _bm25_search(query: str, passages: list[dict], bm25: dict,
                 exclude_source: str, top: int) -> list[dict]:
    tokens = _tokenize(query)
    if not tokens:
        return []

    scores: dict[int, float] = defaultdict(float)
    avgdl = bm25["avgdl"]

    for t in tokens:
        idf = bm25["idf"].get(t, 0)
        for pid, tf in bm25["inv"].get(t, []):
            dl = bm25["lens"][pid]
            norm_tf = tf * (BM25_K1 + 1) / (tf + BM25_K1 * (1 - BM25_B + BM25_B * dl / avgdl))
            scores[pid] += idf * norm_tf

    results = []
    for pid, score in sorted(scores.items(), key=lambda x: -x[1])[:top * 3]:
        p = passages[pid]
        if p["source"] == exclude_source:
            continue
        results.append({**p, "score": round(score, 2)})
        if len(results) >= top:
            break

    return results


def _parse_empty_sections(text: str) -> list[dict]:
    """Возвращает список пустых секций из файла."""
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    lines = clean.splitlines()
    sections = []

    for i, line in enumerate(lines):
        m = re.match(r'^(#{2,4})\s+(.+)$', line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        # Считаем слова до следующего заголовка
        j = i + 1
        content_words = 0
        while j < len(lines):
            if re.match(r'^#{1,6}\s', lines[j]):
                break
            content_words += len(lines[j].split())
            j += 1
        if content_words < MIN_CONTENT:
            sections.append({
                "line_idx": i,
                "level": level,
                "title": title,
                "content_words": content_words,
            })

    return sections


def _insert_content(text: str, empty_sections: list[dict],
                    passages: list[dict], bm25: dict,
                    source: str, mode: str, top: int) -> tuple[str, int]:
    """Вставляет найденный контент в пустые секции. Возвращает (новый_текст, n_filled)."""
    lines = text.splitlines(keepends=True)
    n_filled = 0

    for sec in reversed(empty_sections):
        query = sec["title"]
        results = _bm25_search(query, passages, bm25, source, top)
        if not results:
            continue

        insert_lines = []
        if mode == "cite":
            for r in results:
                insert_lines.append(f"\n> **Из:** `{r['source']}`\n")
                insert_lines.append(f"> {r['text'][:200]}\n>\n")
        else:  # link mode
            for r in results:
                fname = r["source"].split("/")[-1].replace(".md", "")
                rel_path = r["source"]
                insert_lines.append(f"\n→ _См. также:_ [{fname}]({rel_path})\n")

        insert_pos = sec["line_idx"] + 1
        for k, insert_line in enumerate(insert_lines):
            lines.insert(insert_pos + k, insert_line)
        n_filled += 1

    return "".join(lines), n_filled


def main() -> None:
    mode_label = {"cite": "цитата", "link": "ссылка"}.get(MODE, MODE)
    print(f"🔧 improve_gap_filler.py — заполнение пустых секций ({mode_label})")
    print(f"   Режим: {'APPLY' if APPLY else 'dry-run'} | TOP={TOP}\n")

    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent))
    try:
        from utils_docignore import is_ignored
    except ImportError:
        is_ignored = lambda p: False

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)
             and not is_ignored(f)]
    print(f"   Файлов: {len(files)}")
    print("   Строю BM25-корпус...", end=" ", flush=True)

    # Корпус строим из всех docs, независимо от section_filter
    all_files = [f for f in sorted(DOCS.rglob("*.md"))
                 if f.name not in SKIP_FILES and "-parts" not in str(f)]
    passages, bm25 = _build_corpus(all_files)
    print(f"{len(passages)} абзацев\n")

    total_filled = 0

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        empty_secs = _parse_empty_sections(text)
        if not empty_secs:
            continue

        source = str(f.relative_to(ROOT))
        print(f"  📄 {source} ({len(empty_secs)} пустых секций)")

        for sec in empty_secs[:5]:
            query = sec["title"]
            results = _bm25_search(query, passages, bm25, source, TOP)
            if results:
                print(f"     ▸ H{sec['level']} «{sec['title'][:50]}» → "
                      f"{results[0]['source'].split('/')[-1]} (score: {results[0]['score']})")
            else:
                print(f"     ▸ H{sec['level']} «{sec['title'][:50]}» → нет результатов")

        if len(empty_secs) > 5:
            print(f"     ...ещё {len(empty_secs)-5} секций")

        if APPLY:
            new_text, n = _insert_content(text, empty_secs, passages, bm25, source, MODE, TOP)
            if n:
                f.write_text(new_text, encoding="utf-8")
                total_filled += n
        print()

    if APPLY:
        print(f"  ✅ Заполнено секций: {total_filled}")
    else:
        print("  Запустите с --apply для вставки контента.")


if __name__ == "__main__":
    main()
