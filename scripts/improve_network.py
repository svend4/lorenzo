"""
improve_network.py — анализ сети авторов и проектов.
Строит: матрицу ко-упоминаний, центральность, кластеры авторов.
Создаёт docs/NETWORK.md + docs/network.dot (Graphviz).
Запуск: python scripts/improve_network.py
"""
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"NETWORK.md", "GRAPH.md", "ENTITIES.md"}

# Узлы сети
AUTHORS = {
    "kksudo":   "Андрей (kksudo)",
    "spbmolot": "Виталий (spbmolot)",
    "svend4":   "Lorenzo (svend4)",
}

PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "Yodoca", "NGT",
    "SENTINEL", "Rufler", "AI Factory", "LiteParse", "Firecrawl",
    "knowledge-space", "Wikontic", "MemNet", "mclaude",
    "Lorenzo", "Cowork", "ingit",
]

TECHNOLOGIES = [
    "MCP", "RAG", "LLM", "CRDT", "FastAPI", "SQLite", "Mermaid",
]

ALL_NODES = list(AUTHORS.values()) + PROJECTS + TECHNOLOGIES


def find_mentions(text: str, name: str) -> int:
    return len(re.findall(re.escape(name), text, re.IGNORECASE))


def centrality(co_matrix: dict, node: str) -> int:
    return sum(v for (a, b), v in co_matrix.items() if a == node or b == node)


def main():
    print("Анализ сети проектов и авторов...")

    all_text = ""
    file_sets: dict[str, set] = defaultdict(set)

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        all_text += text + "\n"
        rel = str(f.relative_to(ROOT))

        for node in PROJECTS + list(AUTHORS.keys()):
            if re.search(re.escape(node), text, re.IGNORECASE):
                file_sets[node].add(rel)
        for auth_key, auth_name in AUTHORS.items():
            if re.search(re.escape(auth_key), text, re.IGNORECASE):
                file_sets[auth_name].add(rel)

    # Ко-упоминания: сколько файлов содержат оба узла
    nodes = PROJECTS + list(AUTHORS.values())
    co: dict[tuple, int] = {}
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            a_key = next((k for k, v in AUTHORS.items() if v == a), a)
            b_key = next((k for k, v in AUTHORS.items() if v == b), b)
            files_a = file_sets.get(a_key, file_sets.get(a, set()))
            files_b = file_sets.get(b_key, file_sets.get(b, set()))
            common = len(files_a & files_b)
            if common >= 2:
                co[(a, b)] = common

    # Сортируем пары
    top_pairs = sorted(co.items(), key=lambda x: -x[1])

    # Центральность (сумма весов рёбер)
    central = Counter()
    for (a, b), w in co.items():
        central[a] += w
        central[b] += w

    lines = [
        "# Сеть проектов и авторов\n",
        f"**Узлов:** {len(nodes)}  **Связей:** {len(co)}\n",

        "## Топ-20 ко-упоминаемых пар\n",
        "| Пара | Общих файлов |",
        "|------|-------------|",
    ]
    for (a, b), w in top_pairs[:20]:
        lines.append(f"| **{a}** ↔ **{b}** | {w} |")

    lines += [
        "\n## Центральность узлов (влиятельность)\n",
        "| Узел | Балл центральности | Тип |",
        "|------|--------------------|-----|",
    ]
    for node, score in central.most_common(20):
        ntype = "👤 Автор" if node in AUTHORS.values() else "📦 Проект"
        lines.append(f"| **{node}** | {score} | {ntype} |")

    # Прямые связи авторов с проектами
    lines += ["\n## Авторы ↔ Проекты\n"]
    for auth_key, auth_name in AUTHORS.items():
        auth_files = file_sets.get(auth_name, file_sets.get(auth_key, set()))
        if not auth_files:
            continue
        linked = []
        for proj in PROJECTS:
            proj_files = file_sets.get(proj, set())
            common = len(auth_files & proj_files)
            if common >= 2:
                linked.append((proj, common))
        linked.sort(key=lambda x: -x[1])
        if linked:
            proj_str = ", ".join(f"**{p}** ({c})" for p, c in linked[:8])
            lines.append(f"**{auth_name}** → {proj_str}\n")

    # Graphviz DOT
    dot_lines = ["digraph network {",
                 '  rankdir=LR;',
                 '  node [shape=box, style=filled];']

    # Авторы — красные
    for auth_name in AUTHORS.values():
        dot_lines.append(f'  "{auth_name}" [fillcolor=salmon];')
    # Проекты — голубые
    for proj in PROJECTS:
        if proj in central:
            dot_lines.append(f'  "{proj}" [fillcolor=lightblue];')

    for (a, b), w in top_pairs[:30]:
        width = max(1, min(5, w // 3))
        dot_lines.append(f'  "{a}" -- "{b}" [weight={w}, penwidth={width}];')
    dot_lines.append("}")

    dot_out = DOCS / "network.dot"
    dot_out.write_text("\n".join(dot_lines) + "\n", encoding="utf-8")

    out = DOCS / "NETWORK.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  wrote: {dot_out.relative_to(ROOT)}")
    print(f"  узлов: {len(nodes)}, связей: {len(co)}")


if __name__ == "__main__":
    main()
