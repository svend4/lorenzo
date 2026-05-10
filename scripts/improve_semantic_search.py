"""
improve_semantic_search.py — Unified semantic search over the knowledge base.

Combines three ranking signals in one CLI:
  1. TF-IDF cosine  — card-level semantic similarity (cards/tfidf_index.json)
  2. BM25 passages  — paragraph-level keyword search  (docs/passages.json)
  3. Full-text      — simple substring match across all docs

Commands:
  --query TEXT        Search across all three modes, merge results
  --mode semantic     Only TF-IDF card search
  --mode bm25         Only BM25 passage search
  --mode full         Only full-text substring search
  --type TYPE         Filter cards by type: project|doc|person|all
  --section SECTION   Restrict to a docs/ sub-section (e.g. 05-habr-projects)
  --top N             Number of results per mode (default 10)
  --json              Output as JSON

Examples:
    python scripts/improve_semantic_search.py --query "агент память консолидация"
    python scripts/improve_semantic_search.py --query "RAG retrieval" --mode semantic --type project
    python scripts/improve_semantic_search.py --query "Yodoca" --mode bm25 --top 5
    python scripts/improve_semantic_search.py --query "CardIndex" --mode full --section 01-svyazi
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
CARDS   = ROOT / "cards"
SCRIPTS = ROOT / "scripts"

INDEX   = CARDS / "tfidf_index.json"
PASSAGES = DOCS / "passages.json"

sys.path.insert(0, str(SCRIPTS))
from utils_card_envelope import CardStore, CardEnvelope

# ─────────────────────────────────────────────────────────────────────
# Загрузка данных
# ─────────────────────────────────────────────────────────────────────

_tfidf_idx: dict | None = None
_passages:  list | None = None


def _get_tfidf() -> dict | None:
    global _tfidf_idx
    if _tfidf_idx is None and INDEX.exists():
        try:
            _tfidf_idx = json.loads(INDEX.read_text(encoding="utf-8"))
        except Exception:
            pass
    return _tfidf_idx


def _get_passages() -> list:
    global _passages
    if _passages is None:
        if PASSAGES.exists():
            try:
                data = json.loads(PASSAGES.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    _passages = data
                elif isinstance(data, dict):
                    _passages = data.get("passages", data.get("items", []))
                else:
                    _passages = []
            except Exception:
                _passages = []
        else:
            _passages = []
    return _passages


# ─────────────────────────────────────────────────────────────────────
# Токенизация (одна функция на все три режима)
# ─────────────────────────────────────────────────────────────────────

_STOPWORDS = {
    "и","в","на","что","как","это","для","или","но","по","к","из","а","не","с",
    "о","от","за","до","то","же","при","уже","так","ещё","бы","ли","его","её",
    "the","a","an","of","in","to","is","for","with","by","and","or","but","on",
    "at","from","are","was","were","be","been","have","has","that","this","it",
}


def tokenize(text: str, min_len: int = 3) -> list[str]:
    raw = re.findall(r'[а-яёa-z]{%d,}' % min_len, text.lower())
    return [t for t in raw if t not in _STOPWORDS]


# ─────────────────────────────────────────────────────────────────────
# Режим 1: TF-IDF (card-level)
# ─────────────────────────────────────────────────────────────────────

def _cosine_sim(v1: dict, v2: dict) -> float:
    if not v1 or not v2:
        return 0.0
    dot = sum(v1.get(t, 0.0) * v2.get(t, 0.0) for t in v2)
    n1  = math.sqrt(sum(x*x for x in v1.values()))
    n2  = math.sqrt(sum(x*x for x in v2.values()))
    return dot / (n1 * n2) if n1 and n2 else 0.0


def search_semantic(query: str, top: int = 10,
                    card_type: str = "", section: str = "") -> list[dict]:
    """TF-IDF cosine search over CardStore."""
    idx = _get_tfidf()
    if not idx:
        return []

    idf     = idx["idf"]
    vectors = idx["vectors"]
    meta    = idx["card_meta"]

    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    tf_map = Counter(q_tokens)
    total  = len(q_tokens)
    q_tf   = {t: c / total for t, c in tf_map.items()}
    q_vec  = {t: q_tf[t] * idf[t] for t in q_tf if t in idf}

    results = []
    for cid, vec in vectors.items():
        m = meta.get(cid, {})
        if card_type and card_type != "all" and m.get("card_type") != card_type:
            continue
        if section and section not in m.get("path", ""):
            continue
        score = _cosine_sim(q_vec, vec)
        if score > 0.0:
            results.append({
                "mode":  "semantic",
                "score": round(score, 4),
                "card_id": cid,
                "title": m.get("title", cid[:20]),
                "card_type": m.get("card_type", "doc"),
                "path":  m.get("path", ""),
                "state": m.get("state", ""),
            })

    results.sort(key=lambda x: -x["score"])
    return results[:top]


# ─────────────────────────────────────────────────────────────────────
# Режим 2: BM25 passages
# ─────────────────────────────────────────────────────────────────────

def search_bm25(query: str, top: int = 10, section: str = "",
                k1: float = 1.5, b: float = 0.75) -> list[dict]:
    """BM25 search over indexed passages (docs/passages.json)."""
    passages = _get_passages()
    if not passages:
        return []

    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    # Filter by section
    pool = passages
    if section:
        pool = [p for p in passages
                if section in p.get("source", p.get("file", p.get("id", "")))]

    if not pool:
        return []

    avg_dl = max(sum(len(p.get("text", "").split()) for p in pool) / len(pool), 1)

    results = []
    for p in pool:
        text  = p.get("text", "")
        tokens = text.lower().split()
        tf_map = Counter(tokens)
        dl     = len(tokens)
        score  = 0.0
        for qt in q_tokens:
            tf = tf_map.get(qt, 0)
            if tf == 0:
                continue
            idf     = math.log(2.0)
            tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avg_dl))
            score  += idf * tf_norm
        if score > 0:
            snippet = text[:200].replace("\n", " ")
            filepath = p.get("source", p.get("file", p.get("id", "").split("::")[0]))
            heading  = p.get("heading", "")
            results.append({
                "mode":     "bm25",
                "score":    round(score, 4),
                "file":     filepath,
                "heading":  heading,
                "snippet":  snippet,
            })

    results.sort(key=lambda x: -x["score"])
    return results[:top]


# ─────────────────────────────────────────────────────────────────────
# Режим 3: Full-text substring
# ─────────────────────────────────────────────────────────────────────

def search_fulltext(query: str, top: int = 10, section: str = "") -> list[dict]:
    """Substring full-text search across docs/ files."""
    q_lower = query.lower()
    q_tokens = tokenize(query)

    scope = DOCS / section if section else DOCS
    if not scope.exists():
        return []

    results = []
    for md_file in scope.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        text_lower = text.lower()
        if q_lower not in text_lower and not all(t in text_lower for t in q_tokens):
            continue

        # Count matches
        count = sum(text_lower.count(t) for t in q_tokens)
        # Extract snippet around first match
        idx = text_lower.find(q_tokens[0] if q_tokens else q_lower)
        start = max(0, idx - 80)
        end   = min(len(text), idx + 200)
        snippet = text[start:end].replace("\n", " ").strip()

        rel_path = str(md_file.relative_to(ROOT))
        results.append({
            "mode":    "full",
            "score":   count,
            "file":    rel_path,
            "snippet": snippet,
        })

    results.sort(key=lambda x: -x["score"])
    return results[:top]


# ─────────────────────────────────────────────────────────────────────
# Объединение результатов (hybrid merge)
# ─────────────────────────────────────────────────────────────────────

def search_hybrid(query: str, top: int = 10,
                  card_type: str = "", section: str = "") -> list[dict]:
    """Merges semantic + BM25 + full-text with reciprocal rank fusion."""
    sem_res = search_semantic(query, top=top * 2, card_type=card_type, section=section)
    bm25_res = search_bm25(query, top=top * 2, section=section)

    # Normalise scores to [0, 1]
    def _norm(lst: list[dict], key: str = "score") -> None:
        mx = max((r[key] for r in lst), default=1.0) or 1.0
        for r in lst:
            r[key] = r[key] / mx

    _norm(sem_res)
    _norm(bm25_res)

    # RRF with k=60
    k   = 60
    rrf: dict[str, float] = {}
    meta: dict[str, dict] = {}

    for rank, r in enumerate(sem_res):
        key = r.get("path") or r.get("card_id") or r["title"]
        rrf[key]  = rrf.get(key, 0) + 1.0 / (k + rank + 1)
        meta[key] = r

    for rank, r in enumerate(bm25_res):
        key = r.get("file", "") or r.get("title", "")
        rrf[key]  = rrf.get(key, 0) + 1.0 / (k + rank + 1)
        if key not in meta:
            meta[key] = r

    merged = sorted(rrf.items(), key=lambda x: -x[1])[:top]
    results = []
    for k, v in merged:
        r = dict(meta[k])
        r["mode"]  = "hybrid"
        r["score"] = round(v, 5)
        # Normalise: BM25 results use "file"/"heading" instead of "title"/"path"
        if "title" not in r:
            r["title"] = r.get("heading", "") or Path(r.get("file", k)).stem
        if "path" not in r:
            r["path"] = r.get("file", "")
        if "card_type" not in r:
            r["card_type"] = ""
        results.append(r)
    return results


# ─────────────────────────────────────────────────────────────────────
# Вывод
# ─────────────────────────────────────────────────────────────────────

def _print_results(results: list[dict], mode: str, query: str) -> None:
    if not results:
        print(f"  Ничего не найдено (mode={mode}, query=«{query}»)")
        return

    mode_label = {"semantic": "TF-IDF карточки", "bm25": "BM25 абзацы",
                  "full": "Полнотекст", "hybrid": "Гибрид"}.get(mode, mode)
    print(f"\n  {mode_label} — «{query}» — {len(results)} результатов:\n")

    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        if mode in ("semantic", "hybrid"):
            title = r.get("title", "")[:55]
            ctype = r.get("card_type", "")
            path  = r.get("path", "")
            print(f"  {i:2}. [{score:.4f}] {ctype:8}  {title}")
            if path:
                print(f"        {path}")
        elif mode == "bm25":
            filepath = r.get("file", "")
            heading  = r.get("heading", "")[:50]
            snippet  = r.get("snippet", "")[:120]
            print(f"  {i:2}. [{score:.3f}]  {filepath}")
            if heading:
                print(f"        § {heading}")
            if snippet:
                print(f"        …{snippet}…")
        else:  # full
            filepath = r.get("file", "")
            snippet  = r.get("snippet", "")[:120]
            hits     = int(r.get("score", 0))
            print(f"  {i:2}. [{hits} вхожд.]  {filepath}")
            if snippet:
                print(f"        …{snippet}…")
    print()


# ─────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified semantic search: TF-IDF + BM25 + full-text"
    )
    parser.add_argument("--query",   required=True, metavar="ТЕКСТ",
                        help="Поисковый запрос")
    parser.add_argument("--mode",    default="hybrid",
                        choices=["hybrid", "semantic", "bm25", "full"],
                        help="Режим поиска (по умолч. hybrid)")
    parser.add_argument("--type",    default="", metavar="ТИП",
                        choices=["", "project", "doc", "person", "note", "fact", "all"],
                        help="Фильтр по типу карточки (для semantic/hybrid)")
    parser.add_argument("--section", default="", metavar="РАЗДЕЛ",
                        help="Ограничить поиск разделом docs/ (напр. 05-habr-projects)")
    parser.add_argument("--top",     type=int, default=10,
                        help="Число результатов")
    parser.add_argument("--json",    action="store_true",
                        help="Вывод в формате JSON")
    args = parser.parse_args()

    query   = args.query
    mode    = args.mode
    top     = args.top
    section = args.section
    ctype   = args.type

    if mode == "hybrid":
        results = search_hybrid(query, top=top, card_type=ctype, section=section)
    elif mode == "semantic":
        results = search_semantic(query, top=top, card_type=ctype, section=section)
    elif mode == "bm25":
        results = search_bm25(query, top=top, section=section)
    else:
        results = search_fulltext(query, top=top, section=section)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        _print_results(results, mode, query)


if __name__ == "__main__":
    main()
