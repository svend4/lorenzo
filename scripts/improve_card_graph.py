"""
improve_card_graph.py — knowledge graph of approved card relationships.

Builds a directed graph from [[wikilinks]] and [text](path.md) links between
approved/normalized cards. Computes PageRank to find the most influential cards.
Outputs:
  docs/CARD_GRAPH.json  — machine-readable graph (nodes + edges + pagerank)
  docs/CARD_GRAPH.md    — human-readable report: hubs, orphans, clusters

The graph index is also used by gateway.py /api/graph endpoint.

Usage:
  python scripts/improve_card_graph.py           # build + report
  python scripts/improve_card_graph.py --top 20  # top N hubs
  python scripts/improve_card_graph.py --stats   # stats only
  python scripts/improve_card_graph.py --dot     # output Graphviz DOT
"""
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
GRAPH_JSON = DOCS / "CARD_GRAPH.json"
GRAPH_MD   = DOCS / "CARD_GRAPH.md"


# ── Card collection ──────────────────────────────────────────────────────────

def _get_state(text: str) -> str:
    m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else "raw"


def _get_title(text: str, path: Path) -> str:
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if m:
        t = m.group(1).strip()
        if t and t != "⬡":
            return t[:80]
    return path.stem.replace("-", " ").replace("_", " ")[:80]


def _get_tags(text: str) -> list[str]:
    m = re.search(r"^tags:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if m:
        return [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    m = re.search(r"<!--\s*tags:\s*([^>]+?)\s*-->", text)
    if m:
        return [t.strip() for t in m.group(1).split(",") if t.strip()]
    return []


def _extract_links(text: str, src_path: Path) -> list[str]:
    """Return list of relative paths referenced by this card."""
    targets = []
    # [[wikilinks]]
    for wl in re.findall(r"\[\[([^\]]+)\]\]", text):
        wl = wl.split("|")[0].split("#")[0].strip()
        if wl:
            targets.append(wl)
    # [text](path.md) links — only internal .md
    for _, href in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text):
        href = href.split("#")[0].strip()
        if href.endswith(".md") and not href.startswith("http"):
            targets.append(href)
    return targets


def _resolve(target: str, src_path: Path, path_index: dict[str, str]) -> str | None:
    """Resolve a link target to a canonical rel-path key."""
    # Try exact match in index
    stem = Path(target).stem.lower()
    for key in path_index:
        if Path(key).stem.lower() == stem:
            return key
    # Try relative to src directory
    resolved = (src_path.parent / target).resolve()
    rel = None
    try:
        rel = str(resolved.relative_to(ROOT.resolve()))
    except ValueError:
        pass
    if rel and rel in path_index:
        return rel
    return None


def collect_cards() -> dict[str, dict]:
    """Return {rel_path: {title, state, tags, path}} for all non-obsidian cards."""
    cards = {}
    for p in DOCS.rglob("*.md"):
        if "obsidian" in p.parts:
            continue
        if p.parent == DOCS and p.stem.isupper():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(p.relative_to(ROOT))
        cards[rel] = {
            "title": _get_title(text, p),
            "state": _get_state(text),
            "tags":  _get_tags(text),
            "path":  p,
            "text":  text,
        }
    return cards


# ── Graph construction ────────────────────────────────────────────────────────

def build_graph(cards: dict[str, dict]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Return (out_edges, in_edges) dicts: rel_path → [rel_path, ...]."""
    path_index = {k: k for k in cards}
    out_edges: dict[str, list[str]] = defaultdict(list)
    in_edges:  dict[str, list[str]] = defaultdict(list)

    for rel, card in cards.items():
        links = _extract_links(card["text"], card["path"])
        for tgt in links:
            resolved = _resolve(tgt, card["path"], path_index)
            if resolved and resolved != rel and resolved in cards:
                out_edges[rel].append(resolved)
                in_edges[resolved].append(rel)

    return dict(out_edges), dict(in_edges)


# ── PageRank ──────────────────────────────────────────────────────────────────

def pagerank(
    nodes: list[str],
    out_edges: dict[str, list[str]],
    in_edges: dict[str, list[str]],
    damping: float = 0.85,
    iterations: int = 30,
) -> dict[str, float]:
    n = len(nodes)
    if n == 0:
        return {}
    rank = {node: 1.0 / n for node in nodes}
    for _ in range(iterations):
        new_rank: dict[str, float] = {}
        for node in nodes:
            incoming = in_edges.get(node, [])
            contrib = sum(rank[src] / max(len(out_edges.get(src, [])), 1) for src in incoming)
            new_rank[node] = (1 - damping) / n + damping * contrib
        rank = new_rank
    # Normalise to 0-1
    max_r = max(rank.values()) if rank else 1
    return {k: v / max_r for k, v in rank.items()}


# ── Report generation ─────────────────────────────────────────────────────────

def write_report(
    cards: dict[str, dict],
    out_edges: dict[str, list[str]],
    in_edges: dict[str, list[str]],
    ranks: dict[str, float],
    top_n: int = 20,
) -> None:
    date = datetime.now().strftime("%Y-%m-%d")
    total_edges = sum(len(v) for v in out_edges.values())
    orphans = [r for r in cards if not out_edges.get(r) and not in_edges.get(r)]
    hubs    = sorted(ranks, key=lambda k: -ranks[k])[:top_n]

    lines = [
        "# Card Knowledge Graph — Svyazi 2.0",
        "",
        f"_Сгенерировано: {date}_",
        "",
        f"**Узлов:** {len(cards)}  **Рёбер:** {total_edges}  "
        f"**Изолированных:** {len(orphans)}  "
        f"**Среднее out-degree:** {total_edges / max(len(cards), 1):.1f}",
        "",
        "## Топ хабы (PageRank)",
        "",
        "| # | PageRank | In | Out | Путь | Теги |",
        "|---|----------|----|----|------|------|",
    ]

    for i, rel in enumerate(hubs, 1):
        r  = ranks.get(rel, 0)
        ic = len(in_edges.get(rel, []))
        oc = len(out_edges.get(rel, []))
        title = cards[rel]["title"][:45]
        tags  = ", ".join(cards[rel]["tags"][:3])
        lines.append(f"| {i} | {r:.3f} | {ic} | {oc} | `{rel}` · {title} | {tags} |")

    lines += [
        "",
        "## Изолированные карточки (нет ссылок)",
        "",
        f"Всего: **{len(orphans)}**",
        "",
    ]
    for rel in sorted(orphans)[:30]:
        title = cards[rel]["title"][:60]
        lines.append(f"- `{rel}` — {title}")
    if len(orphans) > 30:
        lines.append(f"- … и ещё {len(orphans) - 30}")

    # Tag clusters: for each tag find most connected cards
    tag_hubs: dict[str, list[tuple[float, str]]] = defaultdict(list)
    for rel, card in cards.items():
        for tag in card["tags"][:3]:
            tag_hubs[tag].append((ranks.get(rel, 0), rel))

    lines += ["", "## Хабы по тегам", ""]
    for tag, items in sorted(tag_hubs.items(), key=lambda x: -len(x[1]))[:8]:
        top = sorted(items, reverse=True)[:3]
        top_str = ", ".join(f"`{Path(r).stem}`" for _, r in top)
        lines.append(f"**{tag}** ({len(items)} карточек): {top_str}")

    GRAPH_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(
    cards: dict[str, dict],
    out_edges: dict[str, list[str]],
    ranks: dict[str, float],
) -> None:
    nodes = [
        {
            "id":       rel,
            "title":    cards[rel]["title"],
            "state":    cards[rel]["state"],
            "tags":     cards[rel]["tags"][:5],
            "pagerank": round(ranks.get(rel, 0), 4),
            "out_degree": len(out_edges.get(rel, [])),
        }
        for rel in cards
    ]
    edges = [
        {"from": src, "to": tgt}
        for src, targets in out_edges.items()
        for tgt in targets
    ]
    data = {
        "generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "stats": {
            "nodes": len(nodes),
            "edges": len(edges),
            "isolated": sum(1 for n in nodes if n["out_degree"] == 0),
        },
        "nodes": nodes,
        "edges": edges,
    }
    GRAPH_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args    = sys.argv[1:]
    top_n   = 20
    stats   = "--stats" in args
    dot_out = "--dot" in args

    for i, a in enumerate(args):
        if a == "--top" and i + 1 < len(args):
            try:
                top_n = int(args[i + 1])
            except ValueError:
                pass

    print("🕸  Card Knowledge Graph — Svyazi 2.0")
    cards = collect_cards()
    print(f"   Карточек: {len(cards)}")

    out_edges, in_edges = build_graph(cards)
    total_edges = sum(len(v) for v in out_edges.values())
    print(f"   Рёбер:   {total_edges}")

    node_list = list(cards.keys())
    ranks = pagerank(node_list, out_edges, in_edges)

    orphans = [r for r in cards if not out_edges.get(r) and not in_edges.get(r)]
    print(f"   Изолировано: {len(orphans)}")
    print(f"   Avg out-degree: {total_edges / max(len(cards), 1):.1f}")

    if stats:
        return

    write_json(cards, out_edges, ranks)
    write_report(cards, out_edges, in_edges, ranks, top_n=top_n)
    print(f"\n✅ {GRAPH_JSON.relative_to(ROOT)}")
    print(f"✅ {GRAPH_MD.relative_to(ROOT)}")

    print(f"\n— Топ-{min(top_n, 10)} хабов по PageRank —")
    hubs = sorted(ranks, key=lambda k: -ranks[k])[:10]
    for rel in hubs:
        ic = len(in_edges.get(rel, []))
        oc = len(out_edges.get(rel, []))
        print(f"  {ranks[rel]:.3f}  in={ic:3d} out={oc:3d}  {cards[rel]['title'][:55]}")

    if dot_out:
        # Minimal Graphviz DOT for top-50 hubs
        top50 = set(sorted(ranks, key=lambda k: -ranks[k])[:50])
        dot_lines = ["digraph G {", "  rankdir=LR;", "  node [shape=box, fontsize=9];"]
        for src in top50:
            for tgt in out_edges.get(src, []):
                if tgt in top50:
                    label_s = cards[src]["title"][:20].replace('"', "'")
                    label_t = cards[tgt]["title"][:20].replace('"', "'")
                    dot_lines.append(f'  "{label_s}" -> "{label_t}";')
        dot_lines.append("}")
        print("\n" + "\n".join(dot_lines))


if __name__ == "__main__":
    main()
