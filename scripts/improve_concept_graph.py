"""
improve_concept_graph.py — граф концептов из базы знаний.

Строит граф: узлы = ключевые концепты, рёбра = совместное упоминание в одном файле.
Экспортирует в:
  - Mermaid (встраивается в markdown)
  - DOT (для Graphviz)
  - JSON (для d3.js или других инструментов)

Создаёт docs/CONCEPT_GRAPH.md + docs/concept_graph.json.
Запуск:
    python scripts/improve_concept_graph.py
    python scripts/improve_concept_graph.py --section 05-habr-projects
    python scripts/improve_concept_graph.py --min-weight 3
    python scripts/improve_concept_graph.py --format dot
    python scripts/improve_concept_graph.py --top-concepts 30
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MIN_WEIGHT = 2      # мин. совместных упоминаний для ребра
TOP_CONCEPTS = 40   # топ концептов для графа

if "--min-weight" in sys.argv:
    idx = sys.argv.index("--min-weight")
    if idx + 1 < len(sys.argv):
        MIN_WEIGHT = int(sys.argv[idx + 1])

if "--top-concepts" in sys.argv:
    idx = sys.argv.index("--top-concepts")
    if idx + 1 < len(sys.argv):
        TOP_CONCEPTS = int(sys.argv[idx + 1])

FORMAT = "mermaid"
if "--format" in sys.argv:
    idx = sys.argv.index("--format")
    if idx + 1 < len(sys.argv):
        FORMAT = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "CONCEPT_GRAPH.md", "SEARCH.md", "NAMED_ENTITIES.md",
    "OUTLINE.md", "TIMELINE.md", "SOURCE_MAP.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
    "it", "we", "you", "they", "this", "that", "be", "been", "have",
}

# Категории концептов для цветовой кодировки
CONCEPT_CATEGORIES = {
    "memory":      {"память", "memory", "хранение", "кэш", "retrieval", "vector", "embedding"},
    "agent":       {"агент", "agent", "llm", "workflow", "оркестрация", "orchestration"},
    "knowledge":   {"знани", "знание", "base", "graph", "индекс", "поиск", "search", "rag"},
    "project":     {"проект", "репозитори", "github", "oss", "agentfs", "yodoca", "ngt", "svyazi"},
    "architecture":{"архитектур", "слой", "layer", "компонент", "модуль", "api", "protocol"},
    "data":        {"данны", "data", "текст", "document", "файл", "индекс", "chunk"},
}


def _tokens(text: str, n: int = 30) -> set[str]:
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', ' ', clean)
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', clean.lower())
        if t not in STOPWORDS
    ]
    return {w for w, _ in Counter(tokens).most_common(n)}


def _category(concept: str) -> str:
    for cat, keywords in CONCEPT_CATEGORIES.items():
        for kw in keywords:
            if kw in concept:
                return cat
    return "other"


def _mermaid_id(s: str) -> str:
    return re.sub(r'[^a-zA-Zа-яёА-ЯЁ0-9]', '_', s)[:20]


def build_graph(files: list[Path]) -> tuple[dict, dict]:
    """
    Строит граф совместных упоминаний.
    Возвращает (nodes, edges).
    nodes: {concept: {count, category}}
    edges: {(a, b): weight}
    """
    # Глобальная частота концептов
    global_freq: Counter = Counter()
    # Файлы для каждого концепта
    concept_files: dict[str, set[str]] = defaultdict(set)
    # Совместные упоминания
    cooccurrence: Counter = Counter()

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(f.relative_to(ROOT))
        concepts = _tokens(text, TOP_CONCEPTS)
        global_freq.update(concepts)
        for c in concepts:
            concept_files[c].add(rel)
        # Все пары из этого файла
        concepts_list = sorted(concepts)
        for i in range(len(concepts_list)):
            for j in range(i + 1, len(concepts_list)):
                key = (concepts_list[i], concepts_list[j])
                cooccurrence[key] += 1

    # Топ концептов по частоте
    top = [c for c, _ in global_freq.most_common(TOP_CONCEPTS)]
    top_set = set(top)

    nodes = {
        c: {
            "count": global_freq[c],
            "files": len(concept_files[c]),
            "category": _category(c),
        }
        for c in top
    }

    edges = {
        (a, b): w
        for (a, b), w in cooccurrence.items()
        if a in top_set and b in top_set and w >= MIN_WEIGHT
    }

    return nodes, edges


def to_mermaid(nodes: dict, edges: dict, max_edges: int = 60) -> str:
    """Генерирует Mermaid-диаграмму."""
    CAT_SHAPES = {
        "memory":       ("[(", ")]"),
        "agent":        ("{{", "}}"),
        "knowledge":    ("[[", "]]"),
        "project":      ("(", ")"),
        "architecture": ("[/", "/]"),
        "data":         ("[\\", "\\]"),
        "other":        ("[", "]"),
    }

    lines = ["graph TD"]

    # Узлы
    for concept, data in sorted(nodes.items(), key=lambda x: -x[1]["count"]):
        nid = _mermaid_id(concept)
        cat = data["category"]
        open_b, close_b = CAT_SHAPES.get(cat, ("[", "]"))
        label = f"{concept}\\n({data['files']})"
        lines.append(f"    {nid}{open_b}\"{label}\"{close_b}")

    # Рёбра (топ по весу)
    top_edges = sorted(edges.items(), key=lambda x: -x[1])[:max_edges]
    for (a, b), w in top_edges:
        aid, bid = _mermaid_id(a), _mermaid_id(b)
        thickness = "|толстый|" if w >= 5 else ""
        lines.append(f"    {aid} -- {w} {thickness}--> {bid}")

    return "\n".join(lines)


def to_dot(nodes: dict, edges: dict) -> str:
    """Генерирует Graphviz DOT."""
    lines = [
        'digraph concept_graph {',
        '    rankdir=LR;',
        '    node [shape=box, style=filled];',
    ]
    CAT_COLORS = {
        "memory": "#AED6F1", "agent": "#A9DFBF", "knowledge": "#F9E79F",
        "project": "#F1948A", "architecture": "#D7BDE2", "data": "#FAD7A0",
        "other": "#E8E8E8",
    }
    for concept, data in nodes.items():
        nid = _mermaid_id(concept)
        color = CAT_COLORS.get(data["category"], "#E8E8E8")
        size = min(2.0, 0.5 + data["count"] / 10)
        lines.append(f'    {nid} [label="{concept}\\n({data["files"]})", fillcolor="{color}", width={size:.1f}];')

    for (a, b), w in sorted(edges.items(), key=lambda x: -x[1]):
        aid, bid = _mermaid_id(a), _mermaid_id(b)
        thickness = max(1, min(5, w))
        lines.append(f'    {aid} -> {bid} [weight={w}, penwidth={thickness}];')

    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    print("🕸️  improve_concept_graph.py — граф концептов")
    print(f"   Топ концептов: {TOP_CONCEPTS} | Мин. вес ребра: {MIN_WEIGHT}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "confluence" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    nodes, edges = build_graph(files)
    print(f"  Узлов: {len(nodes)}  |  Рёбер: {len(edges)}")

    # Markdown с Mermaid
    mermaid = to_mermaid(nodes, edges)
    lines = [
        "# Граф концептов базы знаний\n",
        f"_Обновлено: {TODAY}_\n",
        f"Концептов: **{len(nodes)}** | Связей: **{len(edges)}** (мин. вес: {MIN_WEIGHT})\n",
        "## Диаграмма\n",
        "```mermaid",
        mermaid,
        "```\n",
        "## Топ концептов по связям\n",
        "| Концепт | Файлов | Связей | Категория |",
        "|---------|--------|--------|-----------|",
    ]

    # Считаем степень каждого узла
    degree: Counter = Counter()
    for (a, b), w in edges.items():
        degree[a] += w
        degree[b] += w

    for concept, deg in degree.most_common(30):
        data = nodes[concept]
        lines.append(
            f"| `{concept}` | {data['files']} | {deg} | {data['category']} |"
        )

    if FORMAT == "dot":
        dot = to_dot(nodes, edges)
        dot_out = DOCS / "concept_graph.dot"
        dot_out.write_text(dot, encoding="utf-8")
        lines += ["\n## DOT-граф\n", "```dot", dot[:2000], "```"]
        print(f"  wrote: {dot_out.relative_to(ROOT)}")

    out_md = DOCS / "CONCEPT_GRAPH.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # JSON
    json_data = {
        "nodes": [
            {"id": c, **data} for c, data in nodes.items()
        ],
        "edges": [
            {"source": a, "target": b, "weight": w}
            for (a, b), w in edges.items()
        ],
        "generated": TODAY,
    }
    out_json = DOCS / "concept_graph.json"
    out_json.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  wrote: {out_md.relative_to(ROOT)}")
    print(f"  wrote: {out_json.relative_to(ROOT)}")
    print(f"  топ-5: {', '.join(c for c, _ in degree.most_common(5))}")


if __name__ == "__main__":
    main()
