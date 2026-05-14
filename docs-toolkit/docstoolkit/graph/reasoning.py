"""Knowledge graph reasoning: TripletStore + multi-hop queries."""
import json
import re
import sqlite3
import uuid
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.graph.builder import ConceptGraph


SCHEMA = """
CREATE TABLE IF NOT EXISTS triplets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    doc_id TEXT NOT NULL DEFAULT '',
    confidence REAL NOT NULL DEFAULT 1.0
);
CREATE INDEX IF NOT EXISTS idx_tri_subject ON triplets(subject);
CREATE INDEX IF NOT EXISTS idx_tri_object ON triplets(object);
CREATE INDEX IF NOT EXISTS idx_tri_predicate ON triplets(predicate);
"""

# Heuristic extraction patterns: (pattern, predicate_label)
# Each pattern has two named groups: subj and obj
_PATTERNS_RU = [
    (re.compile(r'(?P<subj>[A-Za-zА-Яа-яёЁ][\w\-]*)\s+использует\s+(?P<obj>[A-Za-zА-Яа-яёЁ][\w\-]*)'), "использует"),
    (re.compile(r'(?P<subj>[A-Za-zА-Яа-яёЁ][\w\-]*)\s+основан\s+на\s+(?P<obj>[A-Za-zА-Яа-яёЁ][\w\-]*)'), "основан на"),
    (re.compile(r'(?P<subj>[A-Za-zА-Яа-яёЁ][\w\-]*)\s+является\s+(?P<obj>[A-Za-zА-Яа-яёЁ][\w\-]*)'), "является"),
    (re.compile(r'(?P<subj>[A-Za-zА-Яа-яёЁ][\w\-]*)\s+—\s+это\s+(?P<obj>[A-Za-zА-Яа-яёЁ][\w\-]*)'), "это"),
    (re.compile(r'(?P<subj>[A-Za-zА-Яа-яёЁ][\w\-]*)\s+это\s+(?P<obj>[A-Za-zА-Яа-яёЁ][\w\-]*)'), "это"),
]

_PATTERNS_EN = [
    (re.compile(r'(?P<subj>[A-Za-z][\w\-]*)\s+uses\s+(?P<obj>[A-Za-z][\w\-]*)'), "uses"),
    (re.compile(r'(?P<subj>[A-Za-z][\w\-]*)\s+is\s+based\s+on\s+(?P<obj>[A-Za-z][\w\-]*)'), "is based on"),
    (re.compile(r'(?P<subj>[A-Za-z][\w\-]*)\s+is\s+a\s+(?P<obj>[A-Za-z][\w\-]*)'), "is a"),
    (re.compile(r'(?P<subj>[A-Za-z][\w\-]*)\s+is\s+an?\s+(?P<obj>[A-Za-z][\w\-]*)'), "is a"),
    (re.compile(r'(?P<subj>[A-Za-z][\w\-]*)\s+integrates\s+with\s+(?P<obj>[A-Za-z][\w\-]*)'), "integrates with"),
    (re.compile(r'(?P<subj>[A-Za-z][\w\-]*)\s+extends\s+(?P<obj>[A-Za-z][\w\-]*)'), "extends"),
]

_ALL_PATTERNS = _PATTERNS_RU + _PATTERNS_EN

# Short tokens we skip as subjects/objects
_SKIP_TOKENS = {
    "он", "она", "оно", "они", "мы", "вы", "я",
    "the", "a", "an", "it", "this", "that", "they",
    "и", "в", "на", "или", "не", "для",
}


class TripletStore:
    """SQLite-backed store for subject-predicate-object triplets."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "triplets.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def add(self, subject: str, predicate: str, object: str,
            doc_id: str = "", confidence: float = 1.0) -> int:
        """Insert a triplet, return its id."""
        cur = self.conn.execute(
            "INSERT INTO triplets (subject, predicate, object, doc_id, confidence) "
            "VALUES (?, ?, ?, ?, ?)",
            (subject.strip(), predicate.strip(), object.strip(),
             doc_id, confidence),
        )
        self.conn.commit()
        return cur.lastrowid

    def find(self, subject: str | None = None,
             predicate: str | None = None,
             object: str | None = None) -> list[tuple]:
        """Filter triplets by any combination of s/p/o.

        Returns list of (id, subject, predicate, object, doc_id, confidence).
        """
        sql = "SELECT * FROM triplets WHERE 1=1"
        params: list = []
        if subject is not None:
            sql += " AND subject = ?"
            params.append(subject)
        if predicate is not None:
            sql += " AND predicate = ?"
            params.append(predicate)
        if object is not None:
            sql += " AND object = ?"
            params.append(object)
        rows = self.conn.execute(sql, params).fetchall()
        return [(r["id"], r["subject"], r["predicate"],
                 r["object"], r["doc_id"], r["confidence"]) for r in rows]

    def extract_from_text(self, text: str, doc_id: str) -> int:
        """Heuristic extraction from text; returns count of added triplets."""
        added = 0
        for pattern, predicate in _ALL_PATTERNS:
            for m in pattern.finditer(text):
                subj = m.group("subj").strip()
                obj = m.group("obj").strip()
                if (subj.lower() in _SKIP_TOKENS or obj.lower() in _SKIP_TOKENS
                        or len(subj) < 2 or len(obj) < 2):
                    continue
                self.add(subj, predicate, obj, doc_id)
                added += 1
        return added

    def stats(self) -> dict:
        total = self.conn.execute("SELECT COUNT(*) FROM triplets").fetchone()[0]
        subjects = self.conn.execute(
            "SELECT COUNT(DISTINCT subject) FROM triplets").fetchone()[0]
        objects = self.conn.execute(
            "SELECT COUNT(DISTINCT object) FROM triplets").fetchone()[0]
        predicates = self.conn.execute(
            "SELECT COUNT(DISTINCT predicate) FROM triplets").fetchone()[0]
        docs = self.conn.execute(
            "SELECT COUNT(DISTINCT doc_id) FROM triplets WHERE doc_id != ''").fetchone()[0]
        return {
            "total": total,
            "subjects": subjects,
            "objects": objects,
            "predicates": predicates,
            "docs": docs,
        }


class GraphReasoner:
    """Multi-hop reasoning over ConceptGraph + TripletStore."""

    def __init__(self, graph: ConceptGraph,
                 store: TripletStore | None = None):
        self.graph = graph
        self.store = store

    def find_connected(self, start: str, hops: int = 2) -> list[str]:
        """BFS from start node up to N hops; returns all reachable node names."""
        if start not in self.graph.nodes:
            return []
        visited: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(start, 0)])
        visited.add(start)
        while queue:
            node, depth = queue.popleft()
            if depth >= hops:
                continue
            for neighbor, _ in self.graph.neighbors(node, top_k=50):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        visited.discard(start)
        return sorted(visited)

    def multi_hop_query(self, conditions: list[tuple[str, str]]) -> list[str]:
        """Return subjects satisfying ALL (predicate, object) conditions.

        conditions: list of (predicate, object) pairs.
        Requires a TripletStore to be set.
        """
        if not self.store or not conditions:
            return []

        result_sets: list[set[str]] = []
        for predicate, obj in conditions:
            rows = self.store.find(predicate=predicate, object=obj)
            result_sets.append({r[1] for r in rows})  # r[1] = subject

        if not result_sets:
            return []
        # Intersection of all sets
        common = result_sets[0]
        for s in result_sets[1:]:
            common = common & s
        return sorted(common)

    def explain_path(self, a: str, b: str) -> list[str]:
        """Shortest path between two concepts via graph edges.

        Returns [a, ..., b] or [] if not reachable.
        """
        if a not in self.graph.nodes or b not in self.graph.nodes:
            return []
        if a == b:
            return [a]

        # BFS with parent tracking
        parent: dict[str, str | None] = {a: None}
        queue: deque[str] = deque([a])
        found = False
        while queue:
            node = queue.popleft()
            if node == b:
                found = True
                break
            for neighbor, _ in self.graph.neighbors(node, top_k=100):
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)

        if not found:
            return []
        # Reconstruct path
        path: list[str] = []
        cur: str | None = b
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path.reverse()
        return path

    def answer_graph_query(self, question: str) -> str:
        """Heuristic: detect entity names in question, find their connections.

        Returns a text summary of what was found.
        """
        # Find entities from question that appear as graph nodes
        words = re.findall(r'\b\w[\w\-]*\b', question)
        matched_nodes = [w for w in words if w in self.graph.nodes]

        if not matched_nodes:
            return "No known entities found in question."

        lines: list[str] = [f"Entities found: {', '.join(matched_nodes)}"]
        for node in matched_nodes[:3]:  # limit output
            neighbors = self.graph.neighbors(node, top_k=5)
            if neighbors:
                nbr_str = ", ".join(f"{n}(w={w})" for n, w in neighbors)
                lines.append(f"  {node} -> {nbr_str}")
            reachable = self.find_connected(node, hops=2)
            if reachable:
                lines.append(f"  {node} 2-hop: {', '.join(reachable[:10])}")
            if self.store:
                triplets = self.store.find(subject=node)
                for t in triplets[:3]:
                    lines.append(f"  {t[1]} [{t[2]}] {t[3]}")

        return "\n".join(lines)
