"""
improve_passage_retrieval.py — BM25-поиск на уровне абзацев.

В отличие от полнотекстового поиска по файлам, ищет релевантный
АБЗАЦ внутри документа — точнее и удобнее для RAG.

Алгоритм: BM25 (Okapi BM25, k1=1.5, b=0.75).

Режимы:
  --query "текст"        — интерактивный поиск
  --index                — только построить индекс (passages.json)
  --top N                — показать N лучших результатов (по умолч.: 5)
  --section              — ограничить секцией
  --min-words N          — минимум слов в абзаце (по умолч.: 20)
  --context              — показать полный абзац (не только превью)

Запуск:
    python scripts/improve_passage_retrieval.py --index
    python scripts/improve_passage_retrieval.py --query "агент с памятью"
    python scripts/improve_passage_retrieval.py --query "RAG retrieval" --top 10
    python scripts/improve_passage_retrieval.py --query "NGT" --context
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

INDEX_PATH = DOCS / "passages.json"

TOP_N = 5
MIN_WORDS = 20
SHOW_CONTEXT = "--context" in sys.argv
BUILD_INDEX_ONLY = "--index" in sys.argv

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP_N = int(sys.argv[idx + 1])

if "--min-words" in sys.argv:
    idx = sys.argv.index("--min-words")
    if idx + 1 < len(sys.argv):
        MIN_WORDS = int(sys.argv[idx + 1])

QUERY = None
if "--query" in sys.argv:
    idx = sys.argv.index("--query")
    if idx + 1 < len(sys.argv):
        QUERY = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "SEARCH.md", "NAMED_ENTITIES.md", "CONCEPT_GRAPH.md",
    "SOURCE_MAP.md", "TIMELINE.md", "KEYWORD_INDEX.md",
    "CONTRADICTIONS.md", "PARAGRAPH_QUALITY.md",
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

# BM25 параметры
BM25_K1 = 1.5
BM25_B  = 0.75


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _tokenize(text: str) -> list[str]:
    return [
        t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
        if t not in STOPWORDS
    ]


def _extract_passages(text: str, source: str, min_words: int) -> list[dict]:
    """Разбивает файл на абзацы, возвращает [{id, source, heading, text, tokens}]."""
    clean = _clean(text)
    raw_paras = re.split(r'\n{2,}', text)

    current_heading = ""
    passages = []
    pid = 0

    for raw in raw_paras:
        raw = raw.strip()
        if not raw:
            continue

        # Заголовок
        hm = re.match(r'^#{1,3}\s+(.+)$', raw)
        if hm:
            current_heading = hm.group(1).strip()
            continue

        cleaned = _clean(raw)
        tokens = _tokenize(cleaned)
        wc = len(cleaned.split())

        if wc < min_words:
            continue

        passages.append({
            "id": f"{source}::{pid}",
            "source": source,
            "heading": current_heading,
            "text": cleaned[:400],
            "tokens": tokens,
            "wc": wc,
        })
        pid += 1

    return passages


def build_passages(files: list[Path]) -> list[dict]:
    """Строит корпус абзацев из всех файлов."""
    all_passages = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(f.relative_to(ROOT))
        passages = _extract_passages(text, rel, MIN_WORDS)
        all_passages.extend(passages)
    return all_passages


def build_bm25_index(passages: list[dict]) -> dict:
    """Строит обратный индекс для BM25."""
    df: Counter = Counter()
    total_len = 0

    for p in passages:
        total_len += p["wc"]
        for t in set(p["tokens"]):
            df[t] += 1

    N = len(passages)
    avgdl = total_len / max(N, 1)

    idf = {}
    for t, n in df.items():
        idf[t] = math.log((N - n + 0.5) / (n + 0.5) + 1)

    # Обратный индекс: term → [(passage_idx, tf)]
    inv_index: dict[str, list] = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv_index[t].append((i, tf))

    return {
        "idf": idf,
        "inv_index": dict(inv_index),
        "avgdl": avgdl,
        "N": N,
        "passage_lens": [p["wc"] for p in passages],
    }


def bm25_search(query: str, passages: list[dict], bm25: dict, top_n: int = 5) -> list[dict]:
    """Поиск по запросу с BM25-ранжированием."""
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    idf = bm25["idf"]
    inv_index = bm25["inv_index"]
    avgdl = bm25["avgdl"]
    passage_lens = bm25["passage_lens"]

    scores: dict[int, float] = defaultdict(float)

    for t in q_tokens:
        if t not in inv_index:
            continue
        t_idf = idf.get(t, 0)
        for pid, tf in inv_index[t]:
            dl = passage_lens[pid]
            norm_tf = tf * (BM25_K1 + 1) / (tf + BM25_K1 * (1 - BM25_B + BM25_B * dl / avgdl))
            scores[pid] += t_idf * norm_tf

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_n]

    results = []
    for pid, score in ranked:
        p = passages[pid]
        results.append({
            "score": round(score, 4),
            "source": p["source"],
            "heading": p["heading"],
            "text": p["text"],
            "wc": p["wc"],
        })

    return results


def save_index(passages: list[dict], path: Path) -> None:
    """Сохраняет корпус абзацев (без полных tokens для экономии места)."""
    slim = [
        {
            "id": p["id"],
            "source": p["source"],
            "heading": p["heading"],
            "text": p["text"],
            "wc": p["wc"],
        }
        for p in passages
    ]
    data = {"generated": TODAY, "passages": slim}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    print("📖 improve_passage_retrieval.py — BM25-поиск по абзацам")
    print(f"   k1={BM25_K1} b={BM25_B} | Мин. слов в абзаце: {MIN_WORDS}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "-parts" not in str(f)]
    print(f"   Файлов: {len(files)}")

    passages = build_passages(files)
    print(f"   Абзацев: {len(passages)}")

    if BUILD_INDEX_ONLY or not QUERY:
        save_index(passages, INDEX_PATH)
        print(f"   wrote: {INDEX_PATH.relative_to(ROOT)}")
        if not QUERY:
            print("\n  Используйте --query \"текст\" для поиска.")
            return

    bm25 = build_bm25_index(passages)

    if QUERY:
        print(f"\n🔎 Запрос: «{QUERY}»\n")
        results = bm25_search(QUERY, passages, bm25, TOP_N)

        if not results:
            print("  Ничего не найдено.")
            return

        for i, r in enumerate(results, 1):
            heading = f" › {r['heading']}" if r["heading"] else ""
            print(f"  {i}. [{r['score']}] {r['source']}{heading}")
            preview = r["text"]
            if not SHOW_CONTEXT:
                preview = preview[:150] + ("..." if len(r["text"]) > 150 else "")
            print(f"     {preview}")
            print()


if __name__ == "__main__":
    main()
