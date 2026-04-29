"""Builder концепт-графа: NER + co-occurrence."""
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from docstoolkit.graph.ner import extract_entities, Entity, EntityKinds


@dataclass
class ConceptGraph:
    """Граф концептов: nodes + weighted edges по co-occurrence."""
    nodes: dict[str, dict] = field(default_factory=dict)  # name → {kind, count, docs}
    edges: dict[tuple[str, str], int] = field(default_factory=dict)  # (a, b) → weight
    doc_count: int = 0

    def add_node(self, name: str, kind: str, doc_id: str = ""):
        if name not in self.nodes:
            self.nodes[name] = {"kind": kind, "count": 0, "docs": set()}
        self.nodes[name]["count"] += 1
        if doc_id:
            self.nodes[name]["docs"].add(doc_id)

    def add_edge(self, a: str, b: str, weight: int = 1):
        if a == b:
            return
        # Канонический порядок (alphabetical)
        key = tuple(sorted([a, b]))
        self.edges[key] = self.edges.get(key, 0) + weight

    def top_concepts(self, n: int = 20, kind: str = "") -> list[tuple[str, dict]]:
        items = self.nodes.items()
        if kind:
            items = [(name, data) for name, data in items if data["kind"] == kind]
        return sorted(items, key=lambda x: -x[1]["count"])[:n]

    def top_pairs(self, n: int = 20) -> list[tuple[tuple[str, str], int]]:
        return sorted(self.edges.items(), key=lambda x: -x[1])[:n]

    def neighbors(self, node: str, top_k: int = 10) -> list[tuple[str, int]]:
        """Соседи ноды по убыванию веса связи."""
        result = []
        for (a, b), w in self.edges.items():
            if a == node:
                result.append((b, w))
            elif b == node:
                result.append((a, w))
        return sorted(result, key=lambda x: -x[1])[:top_k]

    def stats(self) -> dict:
        by_kind = Counter(d["kind"] for d in self.nodes.values())
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "docs": self.doc_count,
            "by_kind": dict(by_kind),
            "max_node_count": max((d["count"] for d in self.nodes.values()), default=0),
            "max_edge_weight": max(self.edges.values()) if self.edges else 0,
        }


def build_graph(docs: list[dict],
                min_entity_count: int = 2,
                max_pairs_per_doc: int = 30) -> ConceptGraph:
    """Строит концепт-граф из списка документов.

    docs: list of dicts с полями content/text + path/id.
    min_entity_count: сущности появляющиеся реже игнорируются.
    max_pairs_per_doc: ограничение на co-occurrence пары в одном документе
                      (избегать O(n²) взрывов на больших файлах).
    """
    g = ConceptGraph()
    g.doc_count = len(docs)

    # Глобальный счёт сущностей для фильтрации шума
    global_count: Counter = Counter()

    # Первый проход: собрать сущности
    docs_entities = []
    for d in docs:
        text = d.get("content", "") or d.get("text", "") or d.get("preview", "")
        doc_id = d.get("path", "") or d.get("id", "")
        if not text:
            docs_entities.append((doc_id, {}))
            continue
        ents = extract_entities(text)
        docs_entities.append((doc_id, ents))
        for kind, lst in ents.items():
            for e in lst:
                global_count[(e.text, kind)] += e.count

    # Второй проход: добавить ноды и edges
    for doc_id, ents in docs_entities:
        doc_entities_top: list[Entity] = []
        for kind, lst in ents.items():
            for e in lst:
                key = (e.text, kind)
                if global_count[key] < min_entity_count:
                    continue
                g.add_node(e.text, kind, doc_id)
                doc_entities_top.append(e)

        # Co-occurrence: топ-N в документе
        doc_entities_top.sort(key=lambda x: -x.count)
        top = doc_entities_top[:max_pairs_per_doc]
        for i, a in enumerate(top):
            for b in top[i + 1:]:
                g.add_edge(a.text, b.text)

    return g


def build_from_docs_index() -> ConceptGraph:
    """Удобная обёртка: читает search_index.json и строит граф."""
    import json
    from docstoolkit.config import load_config

    cfg = load_config()
    path = cfg.docs_dir / "search_index.json"
    if not path.exists():
        return ConceptGraph()
    data = json.loads(path.read_text(encoding="utf-8"))
    docs = data if isinstance(data, list) else data.get("docs", [])
    return build_graph(docs)
