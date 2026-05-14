"""Build PageRank scores from intra-repository Markdown links.

Parses [[wikilinks]] and [text](relative.md) in all docs/*.md files,
builds a directed graph, and runs the standard PageRank algorithm.

Output: docs/pagerank.json — {relative_path: normalised_score, ...}

Scores are normalised so the max-scoring document = 1.0; all others
are in (0, 1].  Documents with no inbound links receive the base
(1-damping)/N share.

Usage:
    python scripts/improve_pagerank.py          # build & save
    python scripts/improve_pagerank.py --top 20 # show top-20 docs
    python scripts/improve_pagerank.py --dry-run # stats only, no save
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
OUT  = DOCS / "pagerank.json"

DAMPING  = 0.85
MAX_ITER = 60
CONV_EPS = 1e-7


# ── Link extraction ──────────────────────────────────────────────────────────

_WIKILINK_RE   = re.compile(r'\[\[([^\]|#]+)(?:[|#][^\]]*)?]]')
_MD_LINK_RE    = re.compile(r'\[[^\]]*]\(([^)]+)\)')


def _resolve_md_link(href: str, src_dir: Path) -> str | None:
    """Return repo-relative path for a [text](href), or None if external/invalid."""
    href = href.split('#')[0].split('?')[0].strip()
    if not href or href.startswith(('http', 'mailto', '//')):
        return None
    try:
        resolved = (src_dir / href).resolve()
        return str(resolved.relative_to(ROOT.resolve()))
    except (ValueError, OSError):
        return None


def _find_wiki(name: str) -> str | None:
    """Find the first docs/**/{name}.md and return its repo-relative path."""
    name = name.strip()
    for found in DOCS.rglob(f'{name}.md'):
        try:
            return str(found.relative_to(ROOT))
        except ValueError:
            pass
    return None


def extract_links(text: str, src_dir: Path) -> list[str]:
    """Return list of unique repo-relative target paths linked from *text*."""
    seen: set[str] = set()
    targets: list[str] = []

    for href in _MD_LINK_RE.findall(text):
        t = _resolve_md_link(href, src_dir)
        if t and t not in seen:
            seen.add(t)
            targets.append(t)

    for name in _WIKILINK_RE.findall(text):
        t = _find_wiki(name)
        if t and t not in seen:
            seen.add(t)
            targets.append(t)

    return targets


# ── Graph construction ────────────────────────────────────────────────────────

def build_graph() -> tuple[dict[str, list[str]], set[str]]:
    """Return (out_edges, all_nodes) for all .md files under docs/."""
    out_edges: dict[str, list[str]] = defaultdict(list)
    all_nodes: set[str] = set()

    root_resolved = ROOT.resolve()
    for f in DOCS.rglob('*.md'):
        try:
            rel = str(f.resolve().relative_to(root_resolved))
        except ValueError:
            continue
        all_nodes.add(rel)

        text = f.read_text(encoding='utf-8', errors='ignore')
        for tgt in extract_links(text, f.parent):
            if tgt != rel:
                out_edges[rel].append(tgt)
                all_nodes.add(tgt)

    return dict(out_edges), all_nodes


# ── PageRank algorithm ────────────────────────────────────────────────────────

def compute_pagerank(
    out_edges: dict[str, list[str]],
    nodes: set[str],
    damping: float = DAMPING,
    max_iter: int = MAX_ITER,
    eps: float = CONV_EPS,
) -> dict[str, float]:
    """Standard power-iteration PageRank. Returns raw (un-normalised) scores."""
    node_list = sorted(nodes)
    N = len(node_list)
    if N == 0:
        return {}

    # Build in-edge index
    in_edges: dict[str, list[str]] = defaultdict(list)
    for src, targets in out_edges.items():
        for tgt in set(targets):
            in_edges[tgt].append(src)

    # Dangling nodes (no outbound edges) — their rank leaks to all nodes
    dangling = {n for n in node_list if not out_edges.get(n)}

    pr: dict[str, float] = {n: 1.0 / N for n in node_list}

    for _ in range(max_iter):
        dangling_sum = sum(pr[n] for n in dangling) / N

        new_pr: dict[str, float] = {}
        for n in node_list:
            inbound = sum(
                pr[src] / max(len(set(out_edges.get(src, []))), 1)
                for src in in_edges.get(n, [])
            )
            new_pr[n] = (1 - damping) / N + damping * (inbound + dangling_sum)

        diff = sum(abs(new_pr[n] - pr[n]) for n in node_list)
        pr = new_pr
        if diff < eps:
            break

    return pr


def normalise(scores: dict[str, float]) -> dict[str, float]:
    """Normalise so max score = 1.0."""
    mx = max(scores.values(), default=1.0)
    return {k: v / mx for k, v in scores.items()}


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--top',     type=int, default=0, help='Show top-N docs')
    parser.add_argument('--dry-run', action='store_true',  help='Print stats, skip save')
    args = parser.parse_args()

    print("Building link graph from docs/…")
    out_edges, nodes = build_graph()
    n_links = sum(len(v) for v in out_edges.values())
    print(f"  Nodes : {len(nodes):,}")
    print(f"  Edges : {n_links:,}")

    print("Running PageRank…")
    raw    = compute_pagerank(out_edges, nodes)
    scores = normalise(raw)

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if args.top or args.dry_run:
        n = args.top or 20
        print(f"\nTop-{n} by PageRank:")
        for path, score in top[:n]:
            print(f"  {score:.4f}  {path}")

    if not args.dry_run:
        OUT.write_text(
            json.dumps(scores, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        print(f"\nSaved: {OUT}  ({len(scores):,} entries)")


if __name__ == '__main__':
    main()
