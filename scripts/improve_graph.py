"""
improve_graph.py — строит граф связей между проектами.
Создаёт docs/GRAPH.md с диаграммой Mermaid и матрицей совместных упоминаний.
Запуск: python scripts/improve_graph.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "knowledge-space", "mclaude",
    "AI Factory", "Rufler", "LiteParse", "Legal RAG", "Hybrid RAG",
    "Graph RAG", "Yodoca", "NGT Memory", "MemNet", "SENTINEL",
    "LiteLLM", "Auto AI Router", "Tool Search", "AutoResearch",
    "Wikontic", "Firecrawl", "Yjs", "Automerge",
]

# Слои архитектуры для группировки
LAYERS = {
    "ingestion":     ["Svyazi", "CardIndex", "Firecrawl"],
    "knowledge":     ["AgentFS", "knowledge-space", "Wikontic"],
    "memory":        ["Yodoca", "NGT Memory", "MemNet"],
    "rag":           ["LiteParse", "Legal RAG", "Hybrid RAG", "Graph RAG"],
    "orchestration": ["mclaude", "AI Factory", "Rufler", "AutoResearch"],
    "security":      ["SENTINEL", "LiteLLM", "Auto AI Router", "Tool Search"],
    "sync":          ["Yjs", "Automerge"],
}

# Цвета узлов по слою
LAYER_COLORS = {
    "ingestion":     "#f9c74f",
    "knowledge":     "#90be6d",
    "memory":        "#43aa8b",
    "rag":           "#4d908e",
    "orchestration": "#577590",
    "security":      "#f94144",
    "sync":          "#f8961e",
}


def count_co_mentions() -> dict[tuple[str, str], int]:
    """Считает сколько раз пара проектов упоминается в одном файле."""
    co: dict[tuple[str, str], int] = defaultdict(int)

    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8").lower()
        present = [p for p in PROJECTS if p.lower() in text]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                key = (present[i], present[j])
                co[key] += 1

    return co


def project_layer(p: str) -> str:
    for layer, members in LAYERS.items():
        if p in members:
            return layer
    return "other"


def make_mermaid(co: dict, threshold: int = 3) -> str:
    """Граф Mermaid — рёбра только при co-mention >= threshold."""
    lines = ["graph TD"]

    # Подграфы по слоям
    for layer, members in LAYERS.items():
        color = LAYER_COLORS.get(layer, "#ccc")
        lines.append(f"  subgraph {layer}[{layer.upper()}]")
        for m in members:
            safe = m.replace("-", "_").replace(" ", "_")
            lines.append(f"    {safe}[{m}]")
        lines.append("  end")

    # Рёбра
    added = set()
    for (p1, p2), count in sorted(co.items(), key=lambda x: -x[1]):
        if count < threshold:
            continue
        s1 = p1.replace("-", "_").replace(" ", "_")
        s2 = p2.replace("-", "_").replace(" ", "_")
        key = (s1, s2)
        if key in added:
            continue
        added.add(key)
        width = min(count, 5)
        lines.append(f"  {s1} -- {count} --> {s2}")

    return "\n".join(lines)


def make_matrix(co: dict) -> list[str]:
    """Текстовая матрица совместных упоминаний (топ-пары)."""
    top = sorted(co.items(), key=lambda x: -x[1])[:25]
    lines = [
        "\n## Топ совместных упоминаний\n",
        "| Проект A | Проект B | Файлов вместе |",
        "|----------|----------|---------------|",
    ]
    for (p1, p2), count in top:
        lines.append(f"| **{p1}** | **{p2}** | {count} |")
    return lines


def main():
    print("Строю граф связей проектов...")
    co = count_co_mentions()
    print(f"  пар с совместными упоминаниями: {len(co)}")

    mermaid = make_mermaid(co, threshold=2)
    matrix = make_matrix(co)

    lines = [
        "# Граф связей проектов\n",
        "Рёбра = совместные упоминания в одном файле (≥ 2 раз).\n",
        "```mermaid",
        mermaid,
        "```",
    ] + matrix

    # Также выводим DOT-формат для Graphviz
    dot_lines = ["digraph lorenzo {", '  rankdir=LR;', '  node [shape=box];']
    for layer, members in LAYERS.items():
        dot_lines.append(f'  subgraph cluster_{layer} {{')
        dot_lines.append(f'    label="{layer.upper()}";')
        for m in members:
            safe = re.sub(r'[^a-zA-Z0-9]', '_', m)
            dot_lines.append(f'    {safe} [label="{m}"];')
        dot_lines.append('  }')
    for (p1, p2), count in co.items():
        if count >= 3:
            s1 = re.sub(r'[^a-zA-Z0-9]', '_', p1)
            s2 = re.sub(r'[^a-zA-Z0-9]', '_', p2)
            dot_lines.append(f'  {s1} -> {s2} [label="{count}"];')
    dot_lines.append("}")

    lines += [
        "\n## DOT-формат (Graphviz)\n",
        "```dot",
        "\n".join(dot_lines),
        "```",
    ]

    out = DOCS / "GRAPH.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
