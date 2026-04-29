"""Экспорт ConceptGraph в разные форматы."""
import json
from pathlib import Path

from docstoolkit.graph.builder import ConceptGraph


_KIND_COLORS = {
    "person": "#e1e4f3",
    "project": "#d4f0d4",
    "concept": "#f3e6d4",
    "date": "#f0d4d4",
}


def export_json(g: ConceptGraph, path: str | Path | None = None) -> str:
    """Экспорт в JSON (vis.js / cytoscape compatible)."""
    nodes = [
        {
            "id": name,
            "label": name,
            "kind": data["kind"],
            "count": data["count"],
            "docs_count": len(data["docs"]),
        }
        for name, data in g.nodes.items()
    ]
    edges = [
        {"from": a, "to": b, "weight": w}
        for (a, b), w in g.edges.items()
    ]
    output = json.dumps({
        "stats": g.stats(),
        "nodes": nodes,
        "edges": edges,
    }, ensure_ascii=False, indent=2)
    if path:
        Path(path).write_text(output, encoding="utf-8")
    return output


def export_dot(g: ConceptGraph, path: str | Path | None = None,
               max_nodes: int = 50, min_edge_weight: int = 2) -> str:
    """Экспорт в Graphviz DOT."""
    top_nodes = {name for name, _ in g.top_concepts(max_nodes)}
    lines = ["graph ConceptGraph {",
             "  graph [overlap=false, splines=true, sep=0.5];",
             "  node [shape=box, style=filled];", ""]

    for name in top_nodes:
        data = g.nodes[name]
        color = _KIND_COLORS.get(data["kind"], "#eeeeee")
        safe_name = _quote(name)
        label = f'{name} ({data["count"]})'
        lines.append(f'  {safe_name} [label={_quote(label)}, fillcolor="{color}"];')

    lines.append("")
    for (a, b), w in g.edges.items():
        if a not in top_nodes or b not in top_nodes:
            continue
        if w < min_edge_weight:
            continue
        lines.append(f'  {_quote(a)} -- {_quote(b)} [penwidth={min(w/2, 5)}];')

    lines.append("}")
    output = "\n".join(lines)
    if path:
        Path(path).write_text(output, encoding="utf-8")
    return output


def export_mermaid(g: ConceptGraph, path: str | Path | None = None,
                   max_nodes: int = 30) -> str:
    """Экспорт в Mermaid graph LR."""
    top_nodes = [name for name, _ in g.top_concepts(max_nodes)]
    top_set = set(top_nodes)

    lines = ["```mermaid", "graph LR"]
    safe_id = {n: f"n{i}" for i, n in enumerate(top_nodes)}

    for name in top_nodes:
        data = g.nodes[name]
        node_id = safe_id[name]
        lines.append(f'  {node_id}["{name} ({data["count"]})"]')

    for (a, b), w in g.edges.items():
        if a not in top_set or b not in top_set or w < 2:
            continue
        lines.append(f'  {safe_id[a]} ---|{w}| {safe_id[b]}')

    lines.append("```")
    output = "\n".join(lines)
    if path:
        Path(path).write_text(output, encoding="utf-8")
    return output


def export_markdown(g: ConceptGraph, path: str | Path | None = None,
                    top_n: int = 30) -> str:
    """Экспорт в человекочитаемый markdown отчёт."""
    stats = g.stats()
    lines = [
        "# Concept Graph",
        "",
        "## Сводка",
        f"- **Узлов:** {stats['nodes']}",
        f"- **Связей:** {stats['edges']}",
        f"- **Документов проанализировано:** {stats['docs']}",
        "",
        "**По типам:**",
    ]
    for kind, n in sorted(stats['by_kind'].items()):
        lines.append(f"- {kind}: {n}")
    lines.append("")

    for kind in ["person", "project", "concept"]:
        top = g.top_concepts(top_n, kind=kind)
        if not top:
            continue
        lines.append(f"## Топ-{len(top)} {kind}\n")
        lines.append("| Имя | Упоминаний | Документов |")
        lines.append("|-----|-----------:|-----------:|")
        for name, data in top:
            lines.append(f"| `{name}` | {data['count']} | {len(data['docs'])} |")
        lines.append("")

    pairs = g.top_pairs(top_n)
    if pairs:
        lines.append(f"## Топ-{len(pairs)} связей\n")
        lines.append("| Узел A | Узел B | Вес |")
        lines.append("|--------|--------|----:|")
        for (a, b), w in pairs:
            lines.append(f"| `{a}` | `{b}` | {w} |")

    output = "\n".join(lines) + "\n"
    if path:
        Path(path).write_text(output, encoding="utf-8")
    return output


def _quote(s: str) -> str:
    """DOT-quote с экранированием."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
