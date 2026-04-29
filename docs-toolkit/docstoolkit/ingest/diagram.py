"""Diagram ingest: Mermaid + PlantUML парсинг + extraction.

Извлекает узлы и связи из текстовых описаний диаграмм.
Не требует зависимостей — работает на regex.
"""
import re
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


# Mermaid: graph LR / TD / TB
_MM_NODE = re.compile(r'(\w+)\s*[\["(]([^"\])\]]+)[\]")]')
# Edge: A[label]? --> B[label]?  (skip optional [...] / (...) / {...} after node name)
_MM_EDGE = re.compile(r'(\w+)(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\})?\s*[-=]+>\s*(\w+)')
_MM_EDGE_LABEL = re.compile(
    r'(\w+)(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\})?\s*[-=]+>\s*\|([^|]+)\|\s*(\w+)'
)

# PlantUML: actor / participant / class / @startuml ... @enduml
_PU_PART = re.compile(r'(participant|actor|component|class)\s+["]?(\w+)', re.IGNORECASE)
_PU_EDGE = re.compile(r'(\w+)\s*[-]+>\s*(\w+)')


def ingest(path: Path) -> Document:
    """Принимает .mmd / .puml / .md с code blocks."""
    if not path.exists():
        raise IngestError(f"Не найден: {path}")

    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower().lstrip(".")

    diagrams = []
    if suffix in ("mmd", "mermaid"):
        diagrams = [{"kind": "mermaid", "code": text}]
    elif suffix in ("puml", "plantuml"):
        diagrams = [{"kind": "plantuml", "code": text}]
    elif suffix == "md":
        diagrams = _extract_from_md(text)
    else:
        raise IngestError(f"Diagram: неподдерживаемый формат {suffix}")

    if not diagrams:
        raise IngestError(f"В {path}: не найдено диаграмм")

    md_parts = [f"# Diagrams from {path.name}\n",
                f"**Найдено диаграмм:** {len(diagrams)}\n"]

    all_nodes = set()
    all_edges = []
    for i, d in enumerate(diagrams, 1):
        nodes, edges = _parse_diagram(d["code"], d["kind"])
        all_nodes.update(nodes)
        all_edges.extend(edges)
        md_parts.append(f"\n## Diagram {i} ({d['kind']})")
        md_parts.append(f"**Узлов:** {len(nodes)}, **связей:** {len(edges)}")
        if nodes:
            md_parts.append(f"**Узлы:** {', '.join(sorted(nodes)[:20])}")
        if edges:
            md_parts.append("**Связи:**")
            for e in edges[:10]:
                md_parts.append(f"  - {e[0]} → {e[1]}" + (f" ({e[2]})" if len(e) > 2 else ""))

    return Document(
        title=f"Diagrams: {path.stem}",
        content="\n".join(md_parts),
        source=Source.from_path(path, "diagram"),
        metadata={
            "diagram_count": len(diagrams),
            "total_nodes": len(all_nodes),
            "total_edges": len(all_edges),
            "kinds": list(set(d["kind"] for d in diagrams)),
        },
    )


def _extract_from_md(text: str) -> list[dict]:
    """Ищет ```mermaid / ```plantuml в markdown."""
    diagrams = []
    for match in re.finditer(r'```(mermaid|plantuml)\n(.*?)\n```', text, re.DOTALL):
        diagrams.append({"kind": match.group(1), "code": match.group(2)})
    # Также @startuml ... @enduml без code-fence
    for match in re.finditer(r'@startuml\n(.*?)\n@enduml', text, re.DOTALL):
        diagrams.append({"kind": "plantuml", "code": match.group(1)})
    return diagrams


def _parse_diagram(code: str, kind: str) -> tuple[set, list]:
    """Возвращает (nodes, edges) — извлечённые из кода диаграммы."""
    nodes = set()
    edges = []

    if kind == "mermaid":
        # Узлы вида A[Label] / A(Label) / A{Label}
        for m in _MM_NODE.finditer(code):
            nodes.add(m.group(1))
        # Edges с label
        for m in _MM_EDGE_LABEL.finditer(code):
            nodes.add(m.group(1))
            nodes.add(m.group(3))
            edges.append((m.group(1), m.group(3), m.group(2).strip()))
        # Простые edges
        for m in _MM_EDGE.finditer(code):
            a, b = m.group(1), m.group(2)
            if not any(e[0] == a and e[1] == b for e in edges):
                nodes.add(a)
                nodes.add(b)
                edges.append((a, b))

    elif kind == "plantuml":
        for m in _PU_PART.finditer(code):
            nodes.add(m.group(2))
        for m in _PU_EDGE.finditer(code):
            a, b = m.group(1), m.group(2)
            nodes.add(a)
            nodes.add(b)
            edges.append((a, b))

    return nodes, edges
