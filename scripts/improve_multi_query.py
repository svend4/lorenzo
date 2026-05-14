"""
improve_multi_query.py — multi-query fusion search for Svyazi 2.0.

Handles complex queries by decomposing them into focused sub-queries,
running each independently, then fusing results with weighted RRF.

Decomposition strategies (no LLM, pure rule-based):
  1. Delimiter split  — "," / ";" / " и " / " and " / " or " / " + "
  2. Clause split     — "который" / "where" / "who" / "что"
  3. Length split     — long queries (>6 tokens) → overlapping halves
  4. Single          — short queries pass through unmodified

Fusion:
  For each sub-query, run hybrid_search (TF-IDF+BM25+PageRank) and optionally
  graph_search (BFS neighbourhood). Merge with Reciprocal Rank Fusion (k=60)
  weighted by sub-query confidence. Apply PageRank boost on final scores.

Usage:
  python scripts/improve_multi_query.py --query "агент память MCP SQLite"
  python scripts/improve_multi_query.py --query "RAG + BM25 + граф знаний" --top 10
  python scripts/improve_multi_query.py --query "Svyazi CardIndex" --no-graph
  python scripts/improve_multi_query.py --decompose "агент память MCP SQLite"  # show split only
  python scripts/improve_multi_query.py --eval   # compare multi vs single query on eval set
"""

import json
import math
import re
import sys
from pathlib import Path

ROOT       = Path(__file__).parent.parent
DOCS       = ROOT / "docs"
INDEX_PATH = DOCS / "search_index.json"
GRAPH_PATH = DOCS / "CARD_GRAPH.json"

_PR_ALPHA = 0.3
_PR_CAP   = 0.4


# ── Data loading ──────────────────────────────────────────────────────────────

_INDEX:    list[dict] | None = None
_PASSAGES: list[dict] | None = None
_PAGERANK: dict[str, float] | None = None


def _load_index() -> list[dict]:
    global _INDEX
    if _INDEX is None:
        _INDEX = json.loads(INDEX_PATH.read_text(encoding="utf-8")) if INDEX_PATH.exists() else []
    return _INDEX


def _load_passages() -> list[dict]:
    global _PASSAGES
    if _PASSAGES is None:
        p = DOCS / "passages.json"
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8"))
            _PASSAGES = raw.get("passages", raw) if isinstance(raw, dict) else raw
        else:
            _PASSAGES = []
    return _PASSAGES


def _load_pagerank() -> dict[str, float]:
    global _PAGERANK
    if _PAGERANK is None:
        if GRAPH_PATH.exists():
            data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
            _PAGERANK = {n["id"]: min(n.get("pagerank", 0), _PR_CAP)
                         for n in data.get("nodes", [])}
        else:
            _PAGERANK = {}
    return _PAGERANK


# ── Tokeniser + search primitives ────────────────────────────────────────────

def _tok(text: str) -> list[str]:
    return re.findall(r"[а-яёa-z0-9]+", text.lower())


def _tfidf_search(query: str, top_k: int = 20) -> list[dict]:
    tokens = set(_tok(query))
    scored = []
    for d in _load_index():
        parts = [
            (d.get("title") or "") + " " + (d.get("title") or ""),
            d.get("summary") or "",
            d.get("content") or "",
            " ".join(d.get("tags") or []),
        ]
        words = _tok(" ".join(parts))
        if not words:
            continue
        score = sum(words.count(t) for t in tokens) / len(words)
        if score > 0:
            title_tokens = set(_tok(d.get("title") or ""))
            score *= (1 + 2.5 * len(tokens & title_tokens) / max(len(tokens), 1))
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def _bm25_search(query: str, top_k: int = 20) -> list[dict]:
    passages = _load_passages()
    tokens   = _tok(query)
    if not passages or not tokens:
        return []
    k1, b = 1.5, 0.75
    N      = len(passages)
    avgdl  = sum(len(_tok(p.get("text", ""))) for p in passages) / max(N, 1)
    idf: dict[str, float] = {}
    for t in set(tokens):
        df = sum(1 for p in passages if t in _tok(p.get("text", "")))
        idf[t] = math.log((N - df + 0.5) / (df + 0.5) + 1)
    scored: dict[str, float] = {}
    for p in passages:
        src   = p.get("source", "")
        words = _tok(p.get("text", ""))
        dl    = len(words)
        score = sum(
            idf.get(t, 0) * (words.count(t) * (k1 + 1))
            / (words.count(t) + k1 * (1 - b + b * dl / max(avgdl, 1)))
            for t in tokens
        )
        if score > 0:
            scored[src] = scored.get(src, 0) + score
    path_to_doc = {d.get("path", ""): d for d in _load_index()}
    results: list[dict] = []
    for src, _ in sorted(scored.items(), key=lambda x: x[1], reverse=True):
        if src in path_to_doc:
            results.append(path_to_doc[src])
        if len(results) >= top_k:
            break
    return results


def _hybrid_search(query: str, top_k: int = 20) -> list[dict]:
    tfidf = _tfidf_search(query, top_k * 2)
    bm25  = _bm25_search(query, top_k * 2)
    scores: dict[str, float] = {}
    for rank, d in enumerate(tfidf):
        p = d.get("path", "")
        scores[p] = scores.get(p, 0) + 0.6 * (1 / (rank + 1))
    for rank, d in enumerate(bm25):
        p = d.get("path", "")
        scores[p] = scores.get(p, 0) + 0.4 * (1 / (rank + 1))
    pr = _load_pagerank()
    for p in scores:
        scores[p] *= (1 + _PR_ALPHA * pr.get(p, 0))
    path_to_doc = {d.get("path", ""): d for d in _load_index()}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [path_to_doc[p] for p, _ in ranked[:top_k] if p in path_to_doc]


# ── Query decomposition ───────────────────────────────────────────────────────

# Delimiters that introduce a new sub-topic
_DELIMITERS = re.compile(
    r"\s*[,;]\s*|\s+(?:и|or|and|plus|\+|также|либо)\s+",
    re.IGNORECASE,
)

# Subordinating conjunctions that introduce a new clause
_CLAUSE_WORDS = re.compile(
    r"\s+(?:который|которая|которые|что|где|когда|where|who|which|that)\s+",
    re.IGNORECASE,
)


def decompose_query(query: str, max_sub: int = 3) -> list[str]:
    """Split a complex query into focused sub-queries (no LLM)."""
    query = query.strip()
    tokens = query.split()

    # Strategy 1: explicit delimiter split
    parts = [p.strip() for p in _DELIMITERS.split(query) if p.strip()]
    if len(parts) >= 2:
        long_enough = [p for p in parts if len(p.split()) >= 2]
        if len(long_enough) >= 2:
            return long_enough[:max_sub]

    # Strategy 2: clause split
    parts = [p.strip() for p in _CLAUSE_WORDS.split(query) if p.strip()]
    if len(parts) >= 2:
        long_enough = [p for p in parts if len(p.split()) >= 2]
        if len(long_enough) >= 2:
            return long_enough[:max_sub]

    # Strategy 3: overlapping halves for long queries (≥7 tokens)
    if len(tokens) >= 7:
        mid = len(tokens) // 2
        q1  = " ".join(tokens[:mid + 1])          # first half + overlap token
        q2  = " ".join(tokens[mid - 1:])           # overlap token + second half
        return [q1, q2]

    # Strategy 4: single (short query passes through)
    return [query]


# ── RRF fusion ────────────────────────────────────────────────────────────────

def _rrf_merge(
    result_lists: list[list[dict]],
    weights: list[float] | None = None,
    k: int = 60,
    top_k: int = 15,
) -> list[dict]:
    """Reciprocal Rank Fusion across multiple result lists."""
    if weights is None:
        weights = [1.0] * len(result_lists)

    scores: dict[str, float] = {}
    meta:   dict[str, dict]  = {}

    for lst, w in zip(result_lists, weights):
        for rank, d in enumerate(lst):
            path = d.get("path", "")
            if not path:
                continue
            scores[path] = scores.get(path, 0) + w / (k + rank + 1)
            if path not in meta:
                meta[path] = d

    # Apply PageRank boost
    pr = _load_pagerank()
    for p in scores:
        scores[p] *= (1 + _PR_ALPHA * pr.get(p, 0))

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for path, score in ranked[:top_k]:
        if path in meta:
            d = dict(meta[path])
            d["_mq_score"] = round(score, 5)
            results.append(d)
    return results


# ── Main multi-query search ───────────────────────────────────────────────────

def multi_query_search(
    query: str,
    top_k: int = 15,
    use_graph: bool = True,
    max_sub: int = 3,
) -> tuple[list[dict], list[str]]:
    """
    Run multi-query search. Returns (results, sub_queries).

    sub_queries shows how the query was decomposed.
    """
    sub_queries = decompose_query(query, max_sub=max_sub)

    # Run search for each sub-query
    result_lists: list[list[dict]] = []
    weights: list[float] = []

    for i, sq in enumerate(sub_queries):
        hybrid = _hybrid_search(sq, top_k=top_k * 2)
        result_lists.append(hybrid)
        # First sub-query gets slightly higher weight (often the main topic)
        weights.append(1.0 if i > 0 else 1.2)

    if len(sub_queries) > 1 and use_graph:
        # Also run graph neighbourhood on the original (unfragmented) query
        try:
            sys.path.insert(0, str(ROOT / "scripts"))
            from improve_graph_search import graph_search
            graph_res = graph_search(query, top_k=top_k, seeds=8, hops=1)
            result_lists.append(graph_res)
            weights.append(0.8)
        except Exception:
            pass

    results = _rrf_merge(result_lists, weights=weights, top_k=top_k)
    return results, sub_queries


# ── Evaluation comparison ─────────────────────────────────────────────────────

_EVAL_QUERIES = [
    ("агент память MCP SQLite консолидация", ["docs/05-habr-projects/memory/agent-memory-mcp.md",
                                               "docs/05-habr-projects/memory/yodoca.md"]),
    ("knowledge graph RAG поиск карточки",   ["docs/PROTOTYPE_SPEC.md"]),
    ("Svyazi CardIndex Card Envelope контракт", ["docs/PROTOTYPE_SPEC.md"]),
    ("BM25 TF-IDF гибридный поиск hybrid",   ["docs/PROTOTYPE_SPEC.MDMD"]),
]


def eval_comparison() -> None:
    """Compare single-query vs multi-query hit rate."""
    print("Multi-query vs single-query comparison")
    print(f"{'Query':<45} {'Single@5':<10} {'Multi@5':<10}")
    print("-" * 65)

    for query, expected in _EVAL_QUERIES:
        single = _hybrid_search(query, top_k=5)
        multi, subs = multi_query_search(query, top_k=5, use_graph=False)

        single_hit = any(d.get("path","") in expected for d in single)
        multi_hit  = any(d.get("_mq_score",0) and d.get("path","") in expected for d in multi)
        sub_str    = f"→ {len(subs)} sub-queries" if len(subs) > 1 else "→ 1 (no split)"

        print(f"  {query[:43]:<45} {'✅' if single_hit else '❌':<10} {'✅' if multi_hit else '❌':<10}  {sub_str}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args     = sys.argv[1:]
    query    = ""
    top_k    = 15
    no_graph = "--no-graph" in args
    do_eval  = "--eval" in args
    decompose_only = False

    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--query", "-q") and i + 1 < len(args):
            query = args[i + 1]; i += 2
        elif a == "--decompose" and i + 1 < len(args):
            query = args[i + 1]; decompose_only = True; i += 2
        elif a == "--top" and i + 1 < len(args):
            top_k = int(args[i + 1]); i += 2
        else:
            i += 1

    if do_eval:
        eval_comparison()
        return 0

    if not query:
        print(__doc__)
        return 0

    sub_queries = decompose_query(query)

    if decompose_only:
        print(f"Query: «{query}»")
        print(f"Decomposed into {len(sub_queries)} sub-queries:")
        for i, sq in enumerate(sub_queries, 1):
            print(f"  {i}. «{sq}»")
        return 0

    results, sub_queries = multi_query_search(query, top_k=top_k, use_graph=not no_graph)

    multi_label = f"{len(sub_queries)} sub-queries" if len(sub_queries) > 1 else "1 (not split)"
    print(f"Multi-query search: «{query}»")
    print(f"  Decomposed: {multi_label}")
    if len(sub_queries) > 1:
        for i, sq in enumerate(sub_queries, 1):
            print(f"    {i}. «{sq}»")
    print(f"  Results: {len(results)}\n")

    for i, d in enumerate(results, 1):
        title = (d.get("title") or d.get("path", "?"))[:65]
        score = d.get("_mq_score", 0)
        print(f"  {i:2d}. [{score:.5f}]  {title}")
        if d.get("summary"):
            print(f"       {d['summary'][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
