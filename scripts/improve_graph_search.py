"""
improve_graph_search.py — graph-neighbourhood search for Svyazi 2.0.

Combines TF-IDF relevance with graph topology:
  1. Find seed cards matching the query (TF-IDF top-K)
  2. Expand each seed by 1–2 hops through the card link graph
  3. Re-rank all candidates by  relevance × (1 + alpha × pagerank)
  4. Return the merged, de-duplicated, re-ranked list

This surfaces cards that are strongly *connected* to relevant cards but may
not contain the exact query keywords — genuine knowledge neighbourhood.

Outputs:
  Prints ranked results to stdout (CLI mode).
  With --json: machine-readable JSON array.

Usage:
  python scripts/improve_graph_search.py --query "агент с памятью"
  python scripts/improve_graph_search.py --query "RAG retrieval" --hops 2 --top 15
  python scripts/improve_graph_search.py --query "Yodoca" --json
  python scripts/improve_graph_search.py --query "knowledge graph" --seeds 10 --alpha 0.5
  python scripts/improve_graph_search.py --stats   # graph statistics
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

# PageRank boost weight and synthetic-hub cap
_PR_ALPHA = 0.4
_PR_CAP   = 0.4


# ── Data loading ─────────────────────────────────────────────────────────────

def _load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def _load_graph() -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, float]]:
    """Return (out_edges, in_edges, pagerank) dicts keyed by node-id (= rel-path)."""
    if not GRAPH_PATH.exists():
        return {}, {}, {}
    data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))

    out_edges: dict[str, list[str]] = {}
    in_edges:  dict[str, list[str]] = {}
    for e in data.get("edges", []):
        src, tgt = e.get("from", ""), e.get("to", "")
        out_edges.setdefault(src, []).append(tgt)
        in_edges.setdefault(tgt, []).append(src)

    pagerank: dict[str, float] = {
        n["id"]: min(n.get("pagerank", 0), _PR_CAP)
        for n in data.get("nodes", [])
    }
    return out_edges, in_edges, pagerank


# ── TF-IDF seed search ────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[а-яёa-z0-9]+", text.lower())


def _tfidf_scores(query: str, docs: list[dict]) -> dict[str, float]:
    tokens = set(_tokenize(query))
    scores: dict[str, float] = {}
    for d in docs:
        path = d.get("path", "")
        parts = [
            (d.get("title") or "") * 2,
            d.get("summary") or "",
            d.get("content") or "",
            " ".join(d.get("tags") or []),
        ]
        words = _tokenize(" ".join(parts))
        if not words:
            continue
        sc = sum(words.count(t) for t in tokens) / len(words)
        if sc > 0:
            scores[path] = sc
    return scores


# ── Graph neighbourhood expansion ────────────────────────────────────────────

def _expand(seeds: set[str], out_edges: dict, in_edges: dict, hops: int) -> set[str]:
    """BFS expansion: include all nodes within `hops` edges of any seed."""
    frontier = set(seeds)
    visited  = set(seeds)
    for _ in range(hops):
        next_frontier: set[str] = set()
        for node in frontier:
            for nb in out_edges.get(node, []):
                if nb not in visited:
                    next_frontier.add(nb)
                    visited.add(nb)
            for nb in in_edges.get(node, []):
                if nb not in visited:
                    next_frontier.add(nb)
                    visited.add(nb)
        frontier = next_frontier
    return visited


# ── Main search ───────────────────────────────────────────────────────────────

def graph_search(
    query: str,
    top_k: int = 15,
    seeds: int = 10,
    hops: int = 1,
    alpha: float = _PR_ALPHA,
) -> list[dict]:
    docs = _load_index()
    if not docs:
        return []

    out_edges, in_edges, pagerank = _load_graph()

    # Step 1: TF-IDF seed scoring
    tfidf = _tfidf_scores(query, docs)
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    seed_paths = {p for p, _ in sorted_tfidf[:seeds]}

    # Step 2: Graph neighbourhood expansion
    neighbourhood = _expand(seed_paths, out_edges, in_edges, hops)

    # Step 3: Combine relevance + PageRank for all candidates
    path_to_doc = {d.get("path", ""): d for d in docs}
    candidates: dict[str, float] = {}

    for path in neighbourhood:
        rel  = tfidf.get(path, 0)
        pr   = pagerank.get(path, 0)
        rank_bonus = 0.0
        for rank, (p, _) in enumerate(sorted_tfidf[:seeds]):
            if p == path:
                rank_bonus = 1.0 / (rank + 1)
                break
        combined = (rel + rank_bonus) * (1 + alpha * pr)
        if combined > 0 or path in seed_paths:
            candidates[path] = combined

    # Step 4: Return top-k
    ranked = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
    results = []
    for path, score in ranked[:top_k]:
        if path not in path_to_doc:
            continue
        d = dict(path_to_doc[path])
        d["_graph_score"] = round(score, 5)
        d["_pagerank"]    = round(pagerank.get(path, 0), 4)
        d["_is_seed"]     = path in seed_paths
        results.append(d)
    return results


# ── CLI ───────────────────────────────────────────────────────────────────────

def _print_stats() -> None:
    out_edges, in_edges, pagerank = _load_graph()
    nodes = set(out_edges) | set(in_edges) | set(pagerank)
    edges = sum(len(v) for v in out_edges.values())
    isolated = sum(1 for n in nodes if not out_edges.get(n) and not in_edges.get(n))
    top_hubs = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]

    print(f"Graph stats:")
    print(f"  Nodes:    {len(nodes)}")
    print(f"  Edges:    {edges}")
    print(f"  Isolated: {isolated}")
    print(f"  Top hubs (capped at {_PR_CAP}):")
    for path, pr in top_hubs:
        ic = len(in_edges.get(path, []))
        oc = len(out_edges.get(path, []))
        print(f"    {pr:.3f}  in={ic:4d} out={oc:3d}  {path}")


def main() -> int:
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return 0

    if "--stats" in args:
        _print_stats()
        return 0

    query    = ""
    top_k    = 15
    seeds    = 10
    hops     = 1
    alpha    = _PR_ALPHA
    json_out = "--json" in args

    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--query", "-q") and i + 1 < len(args):
            query = args[i + 1]; i += 2
        elif a == "--top" and i + 1 < len(args):
            top_k = int(args[i + 1]); i += 2
        elif a == "--seeds" and i + 1 < len(args):
            seeds = int(args[i + 1]); i += 2
        elif a == "--hops" and i + 1 < len(args):
            hops = int(args[i + 1]); i += 2
        elif a == "--alpha" and i + 1 < len(args):
            alpha = float(args[i + 1]); i += 2
        else:
            i += 1

    if not query:
        print("⚠  Укажите запрос: --query <текст>")
        return 1

    results = graph_search(query, top_k=top_k, seeds=seeds, hops=hops, alpha=alpha)

    if json_out:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("Ничего не найдено.")
        return 0

    print(f"Graph-neighbourhood search: «{query}»  (seeds={seeds}, hops={hops}, α={alpha})")
    print(f"  Найдено: {len(results)} результатов\n")
    for i, d in enumerate(results, 1):
        seed_mark = "🌱" if d.get("_is_seed") else "  "
        title = (d.get("title") or d.get("path", "?"))[:65]
        score = d.get("_graph_score", 0)
        pr    = d.get("_pagerank", 0)
        print(f"  {i:2d}. {seed_mark} [{score:.4f} / pr={pr:.3f}]  {title}")
        if d.get("summary"):
            print(f"       {d['summary'][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
