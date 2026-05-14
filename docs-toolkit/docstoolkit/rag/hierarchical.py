"""Hierarchical retrieval: section → doc → passage."""
import math
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Internal TF-IDF helpers (stdlib-only, no external deps)
# ---------------------------------------------------------------------------

_STOP_WORDS = {
    # ru
    "и", "в", "на", "что", "как", "это", "для", "или", "но", "не", "по", "с", "из",
    "к", "у", "о", "за", "от", "до", "же", "ли", "бы",
    # en
    "the", "a", "an", "of", "in", "to", "is", "are", "for", "and", "or", "but",
    "with", "on", "at", "by", "as", "be", "this", "that",
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zа-яё][a-zа-яё\-]{2,}", text.lower())
    return [w for w in words if w not in _STOP_WORDS]


def _cosine_sparse(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _tfidf_vectors(corpus: list[str]) -> tuple[dict[str, float], list[dict[str, float]]]:
    """Compute IDF + TF-IDF sparse vectors for corpus.

    Returns (idf_dict, list_of_sparse_vectors).
    """
    n = len(corpus)
    df: Counter = Counter()
    token_lists = []
    for text in corpus:
        toks = _tokenize(text)
        token_lists.append(toks)
        for t in set(toks):
            df[t] += 1
    idf = {
        t: math.log((n + 1) / (cnt + 1)) + 1.0
        for t, cnt in df.items()
    }
    vecs = []
    for toks in token_lists:
        tf = Counter(toks)
        total = max(sum(tf.values()), 1)
        vec = {t: (cnt / total) * idf.get(t, 1.0) for t, cnt in tf.items()}
        vecs.append(vec)
    return idf, vecs


def _tfidf_search(
    query: str,
    keys: list[str],
    texts: list[str],
    top_k: int,
) -> list[tuple[str, float]]:
    """TF-IDF cosine search over (key, text) pairs. Returns [(key, score)]."""
    if not keys:
        return []
    idf, doc_vecs = _tfidf_vectors(texts)

    # query vector using corpus IDF
    q_toks = _tokenize(query)
    if not q_toks:
        return []
    q_tf = Counter(q_toks)
    q_total = max(sum(q_tf.values()), 1)
    q_vec = {t: (cnt / q_total) * idf.get(t, 1.0) for t, cnt in q_tf.items()}

    scored = []
    for key, dvec in zip(keys, doc_vecs):
        s = _cosine_sparse(q_vec, dvec)
        if s > 0:
            scored.append((key, s))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_k]


# ---------------------------------------------------------------------------
# HierarchicalResult
# ---------------------------------------------------------------------------

@dataclass
class HierarchicalResult:
    """Result of a hierarchical retrieval search."""
    query: str
    sections: list[tuple[str, float]] = field(default_factory=list)
    docs: list[tuple[str, float]] = field(default_factory=list)
    passages: list[Passage] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    duration_ms: int = 0


# ---------------------------------------------------------------------------
# SectionIndex
# ---------------------------------------------------------------------------

class SectionIndex:
    """Index of sections (subdirectories) in docs_dir."""

    def __init__(self, docs_dir: Path) -> None:
        self.docs_dir = docs_dir
        self._index: dict[str, str] = {}

    def build(self) -> dict[str, str]:
        """For each subdir: concatenate first 500 chars of each .md file.

        Returns {section_name: aggregate_text}.
        """
        result: dict[str, str] = {}
        if not self.docs_dir.exists():
            self._index = result
            return result
        for subdir in sorted(self.docs_dir.iterdir()):
            if not subdir.is_dir():
                continue
            parts: list[str] = []
            for md_file in sorted(subdir.rglob("*.md")):
                try:
                    text = md_file.read_text(encoding="utf-8", errors="replace")
                    parts.append(text[:500])
                except OSError:
                    pass
            if parts:
                result[subdir.name] = " ".join(parts)
        self._index = result
        return result

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """TF-IDF cosine search over section aggregate texts.

        Returns [(section_name, score)] sorted descending.
        """
        if not self._index:
            self.build()
        if not self._index:
            return []
        keys = list(self._index.keys())
        texts = [self._index[k] for k in keys]
        return _tfidf_search(query, keys, texts, top_k)


# ---------------------------------------------------------------------------
# DocIndex
# ---------------------------------------------------------------------------

class DocIndex:
    """Index of .md documents within a single section."""

    def __init__(self, docs_dir: Path, section: str) -> None:
        self.docs_dir = docs_dir
        self.section = section
        self._index: dict[str, str] = {}

    def _extract_doc_text(self, path: Path) -> str:
        """Extract title + headings + first 300 chars of body."""
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""
        lines = text.splitlines()
        title = ""
        headings: list[str] = []
        body_lines: list[str] = []
        in_body = False
        for line in lines:
            if line.startswith("#"):
                heading_text = line.lstrip("#").strip()
                if not title:
                    title = heading_text
                else:
                    headings.append(heading_text)
            else:
                if not in_body and line.strip():
                    in_body = True
                if in_body:
                    body_lines.append(line)
        body = " ".join(body_lines)[:300]
        parts = filter(None, [title, " ".join(headings), body])
        return " ".join(parts)

    def build(self) -> dict[str, str]:
        """For each .md in section: extract title + headings + first 300 chars.

        Returns {relative_doc_path: text}.
        """
        result: dict[str, str] = {}
        section_dir = self.docs_dir / self.section
        if not section_dir.exists():
            self._index = result
            return result
        for md_file in sorted(section_dir.rglob("*.md")):
            rel = str(md_file.relative_to(self.docs_dir))
            result[rel] = self._extract_doc_text(md_file)
        self._index = result
        return result

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        """TF-IDF cosine search over doc texts.

        Returns [(doc_path, score)] sorted descending.
        """
        if not self._index:
            self.build()
        if not self._index:
            return []
        keys = list(self._index.keys())
        texts = [self._index[k] for k in keys]
        return _tfidf_search(query, keys, texts, top_k)


# ---------------------------------------------------------------------------
# hierarchical_search
# ---------------------------------------------------------------------------

def hierarchical_search(
    query: str,
    *,
    docs_dir: Path | None = None,
    top_k_sections: int = 3,
    top_k_docs: int = 5,
    top_k_passages: int = 5,
    aggregation: str = "product",
) -> HierarchicalResult:
    """Three-level hierarchical retrieval.

    Level 1: SectionIndex → top sections
    Level 2: DocIndex per top section → top docs (dedup by path, keep max score)
    Level 3: Retriever filtered to top docs → passages

    aggregation: "product" → section_score * doc_score * passage_score
                 "sum"     → section_score + doc_score + passage_score
    """
    t0 = time.time()
    trace: list[str] = []
    result = HierarchicalResult(query=query)

    if docs_dir is None:
        try:
            from docstoolkit.config import load_config
            cfg = load_config()
            docs_dir = cfg.docs_dir
        except Exception:
            docs_dir = Path("docs")

    # --- Level 1: sections ---
    sec_index = SectionIndex(docs_dir)
    section_hits = sec_index.search(query, top_k=top_k_sections)
    result.sections = section_hits

    if not section_hits:
        trace.append("no sections found")
        result.trace = trace
        result.duration_ms = int((time.time() - t0) * 1000)
        return result

    for sec_name, sec_score in section_hits:
        trace.append(f"section '{sec_name}' selected (score={sec_score:.2f})")

    # --- Level 2: docs per section ---
    doc_scores: dict[str, float] = {}  # path → max_score
    # We also need section_score per doc for aggregation
    doc_section_score: dict[str, float] = {}

    for sec_name, sec_score in section_hits:
        doc_index = DocIndex(docs_dir, sec_name)
        doc_hits = doc_index.search(query, top_k=top_k_docs)
        for doc_path, doc_score in doc_hits:
            trace.append(f"  in '{sec_name}': doc '{doc_path}' ({doc_score:.2f})")
            if doc_path not in doc_scores or doc_scores[doc_path] < doc_score:
                doc_scores[doc_path] = doc_score
                doc_section_score[doc_path] = sec_score

    # Sort docs by score descending
    sorted_docs = sorted(doc_scores.items(), key=lambda x: -x[1])
    result.docs = sorted_docs

    # --- Level 3: passages via Retriever ---
    top_doc_paths = {dp for dp, _ in sorted_docs[:top_k_docs]}

    try:
        from docstoolkit.rag.retriever import Retriever
        retriever = Retriever(method="keyword")
        raw_passages = retriever.search(query, top_k=top_k_passages * 3)
    except Exception as exc:
        trace.append(f"retriever error: {exc}")
        raw_passages = []

    # Filter passages to top docs
    filtered: list[Passage] = []
    for p in raw_passages:
        # doc_id may be a full path or just a filename — match loosely
        match = any(
            p.doc_id == dp or p.doc_id.endswith(dp) or dp.endswith(p.doc_id)
            for dp in top_doc_paths
        )
        if match:
            filtered.append(p)

    # If filtering leaves nothing, use raw passages (fallback)
    if not filtered:
        filtered = raw_passages

    # Aggregate scores
    final_passages: list[Passage] = []
    for p in filtered[:top_k_passages]:
        # Find matching doc entry
        sec_sc = 1.0
        doc_sc = 1.0
        for dp, dsc in sorted_docs:
            if p.doc_id == dp or p.doc_id.endswith(dp) or dp.endswith(p.doc_id):
                doc_sc = dsc
                sec_sc = doc_section_score.get(dp, 1.0)
                break
        pass_sc = p.score if p.score > 0 else 1.0

        if aggregation == "product":
            agg_score = sec_sc * doc_sc * pass_sc
        else:
            agg_score = sec_sc + doc_sc + pass_sc

        final_passages.append(
            Passage(
                text=p.text,
                doc_id=p.doc_id,
                title=p.title,
                score=round(agg_score, 4),
            )
        )
        trace.append(
            f"    passage from '{p.doc_id}' "
            f"(agg_score={agg_score:.2f}, "
            f"sec={sec_sc:.2f}, doc={doc_sc:.2f}, pass={pass_sc:.2f})"
        )

    result.passages = final_passages
    result.trace = trace
    result.duration_ms = int((time.time() - t0) * 1000)
    return result
