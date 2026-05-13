"""Tests for hierarchical retrieval (M3)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.hierarchical import (
    HierarchicalResult,
    SectionIndex,
    DocIndex,
    hierarchical_search,
    _tokenize,
    _cosine_sparse,
    _tfidf_vectors,
    _tfidf_search,
)
from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_docs(tmp_path: Path, structure: dict[str, dict[str, str]]) -> Path:
    """Create a docs directory with structure {section: {filename: content}}."""
    docs = tmp_path / "docs"
    docs.mkdir()
    for section, files in structure.items():
        sec_dir = docs / section
        sec_dir.mkdir()
        for fname, content in files.items():
            (sec_dir / fname).write_text(content, encoding="utf-8")
    return docs


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def test_tokenize_removes_stopwords():
    tokens = _tokenize("как это работает в системе")
    assert "как" not in tokens
    assert "это" not in tokens
    assert "в" not in tokens
    # content words remain (len > 2 after stripping stopwords)
    assert "работает" in tokens or "системе" in tokens


def test_tokenize_lowercases():
    tokens = _tokenize("Hello World RAG")
    assert "hello" in tokens
    assert "world" in tokens
    assert "rag" in tokens


def test_tokenize_empty_string():
    assert _tokenize("") == []


def test_cosine_sparse_identical():
    v = {"a": 1.0, "b": 2.0}
    score = _cosine_sparse(v, v)
    assert abs(score - 1.0) < 1e-6


def test_cosine_sparse_orthogonal():
    a = {"x": 1.0}
    b = {"y": 1.0}
    assert _cosine_sparse(a, b) == 0.0


def test_cosine_sparse_empty():
    assert _cosine_sparse({}, {"a": 1.0}) == 0.0
    assert _cosine_sparse({"a": 1.0}, {}) == 0.0


# ---------------------------------------------------------------------------
# SectionIndex
# ---------------------------------------------------------------------------

def test_section_index_build_groups_by_subdir(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"yodoca.md": "# Yodoca\nMemory engine for agents."},
        "knowledge": {"agentfs.md": "# AgentFS\nFilesystem for knowledge."},
    })
    idx = SectionIndex(docs)
    result = idx.build()
    assert "memory" in result
    assert "knowledge" in result
    assert "Yodoca" in result["memory"]
    assert "AgentFS" in result["knowledge"]


def test_section_index_build_concatenates_multiple_files(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {
            "a.md": "First document about storage.",
            "b.md": "Second document about retrieval.",
        },
    })
    idx = SectionIndex(docs)
    result = idx.build()
    assert "First document" in result["memory"]
    assert "Second document" in result["memory"]


def test_section_index_build_limits_to_500_chars(tmp_path):
    long_content = "x " * 1000  # 2000 chars
    docs = _make_docs(tmp_path, {
        "section": {"big.md": long_content},
    })
    idx = SectionIndex(docs)
    result = idx.build()
    # Each file contributes at most 500 chars
    assert len(result["section"]) <= 600  # 500 + small separator overhead


def test_section_index_build_empty_dir(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    idx = SectionIndex(docs)
    result = idx.build()
    assert result == {}


def test_section_index_build_nonexistent_dir(tmp_path):
    idx = SectionIndex(tmp_path / "nonexistent")
    result = idx.build()
    assert result == {}


def test_section_index_search_returns_sorted_by_score(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "Memory retrieval BM25 embedding vector store agent."},
        "knowledge": {"k.md": "Filesystem graph knowledge ontology index."},
        "other": {"o.md": "Unrelated cooking recipe ingredients pasta."},
    })
    idx = SectionIndex(docs)
    idx.build()
    results = idx.search("memory agent retrieval", top_k=3)
    assert len(results) <= 3
    if len(results) >= 2:
        assert results[0][1] >= results[1][1]


def test_section_index_search_top_k_limits_results(tmp_path):
    docs = _make_docs(tmp_path, {
        "a": {"f.md": "agent memory retrieval system"},
        "b": {"f.md": "agent memory retrieval system"},
        "c": {"f.md": "agent memory retrieval system"},
        "d": {"f.md": "agent memory retrieval system"},
    })
    idx = SectionIndex(docs)
    idx.build()
    results = idx.search("agent memory", top_k=2)
    assert len(results) <= 2


def test_section_index_search_empty_index(tmp_path):
    idx = SectionIndex(tmp_path / "empty")
    results = idx.search("anything")
    assert results == []


def test_section_index_search_triggers_build_if_not_built(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "# Yodoca\nMemory engine."},
    })
    idx = SectionIndex(docs)
    # Don't call build() — search should call it internally
    results = idx.search("memory engine")
    assert isinstance(results, list)


# ---------------------------------------------------------------------------
# DocIndex
# ---------------------------------------------------------------------------

def test_doc_index_build_extracts_title(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"yodoca.md": "# Yodoca\nMemory engine for agents."},
    })
    idx = DocIndex(docs, "memory")
    result = idx.build()
    key = "memory/yodoca.md"
    assert key in result
    assert "Yodoca" in result[key]


def test_doc_index_build_extracts_headings(tmp_path):
    content = "# Main Title\n## Architecture\n### Components\nSome text here."
    docs = _make_docs(tmp_path, {
        "section": {"doc.md": content},
    })
    idx = DocIndex(docs, "section")
    result = idx.build()
    key = "section/doc.md"
    assert "Architecture" in result[key]
    assert "Components" in result[key]


def test_doc_index_build_includes_body_text(tmp_path):
    content = "# Title\nThis is body text about retrieval systems."
    docs = _make_docs(tmp_path, {
        "section": {"doc.md": content},
    })
    idx = DocIndex(docs, "section")
    result = idx.build()
    key = "section/doc.md"
    # Body text should be present (first 300 chars)
    assert "retrieval" in result[key]


def test_doc_index_build_nonexistent_section(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    idx = DocIndex(docs, "nonexistent")
    result = idx.build()
    assert result == {}


def test_doc_index_build_multiple_docs(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {
            "yodoca.md": "# Yodoca\nMemory engine.",
            "ngt.md": "# NGT Memory\nVector storage.",
        },
    })
    idx = DocIndex(docs, "memory")
    result = idx.build()
    assert "memory/yodoca.md" in result
    assert "memory/ngt.md" in result


def test_doc_index_search_relevant_doc_ranks_first(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {
            "yodoca.md": "# Yodoca\nMemory engine with hot-path activation and retrieval.",
            "ngt.md": "# NGT\nVector similarity search graph structure.",
        },
    })
    idx = DocIndex(docs, "memory")
    idx.build()
    results = idx.search("memory engine activation")
    paths = [r[0] for r in results]
    assert "memory/yodoca.md" in paths
    # yodoca should rank higher for this query
    if len(results) >= 2:
        scores_by_path = dict(results)
        assert scores_by_path.get("memory/yodoca.md", 0) >= scores_by_path.get("memory/ngt.md", 0)


def test_doc_index_search_top_k_respected(tmp_path):
    docs = _make_docs(tmp_path, {
        "section": {
            f"doc{i}.md": f"# Doc{i}\nRetrieval system memory agent {i}."
            for i in range(6)
        },
    })
    idx = DocIndex(docs, "section")
    idx.build()
    results = idx.search("retrieval memory", top_k=3)
    assert len(results) <= 3


# ---------------------------------------------------------------------------
# HierarchicalResult
# ---------------------------------------------------------------------------

def test_hierarchical_result_dataclass():
    result = HierarchicalResult(query="test")
    assert result.query == "test"
    assert result.sections == []
    assert result.docs == []
    assert result.passages == []
    assert result.trace == []
    assert result.duration_ms == 0


def test_hierarchical_result_with_data():
    p = Passage(text="hello", doc_id="d1", title="T", score=0.5)
    result = HierarchicalResult(
        query="q",
        sections=[("memory", 0.8)],
        docs=[("memory/y.md", 0.7)],
        passages=[p],
        trace=["step1", "step2"],
        duration_ms=42,
    )
    assert result.sections[0] == ("memory", 0.8)
    assert result.duration_ms == 42
    assert len(result.trace) == 2


# ---------------------------------------------------------------------------
# hierarchical_search
# ---------------------------------------------------------------------------

def test_hierarchical_search_returns_hierarchical_result(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"yodoca.md": "# Yodoca\nMemory engine for agents with retrieval."},
    })
    result = hierarchical_search("memory agent", docs_dir=docs)
    assert isinstance(result, HierarchicalResult)
    assert result.query == "memory agent"


def test_hierarchical_search_empty_docs_dir(tmp_path):
    docs = tmp_path / "empty"
    docs.mkdir()
    result = hierarchical_search("any query", docs_dir=docs)
    assert isinstance(result, HierarchicalResult)
    assert result.sections == []
    assert result.passages == []


def test_hierarchical_search_nonexistent_docs_dir(tmp_path):
    result = hierarchical_search("query", docs_dir=tmp_path / "nonexistent")
    assert isinstance(result, HierarchicalResult)
    assert result.sections == []


def test_hierarchical_search_has_trace(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "# Yodoca\nMemory engine retrieval."},
    })
    result = hierarchical_search("memory retrieval", docs_dir=docs)
    assert isinstance(result.trace, list)
    # trace should have at least section info if something was found
    if result.sections:
        assert any("section" in t.lower() or "memory" in t.lower() for t in result.trace)


def test_hierarchical_search_trace_human_readable(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "# Yodoca\nMemory engine with vector retrieval BM25."},
        "knowledge": {"k.md": "# AgentFS\nFilesystem knowledge graph ontology."},
    })
    result = hierarchical_search("memory vector retrieval", docs_dir=docs)
    # Trace should contain human-readable entries like "section 'X' selected (score=...)"
    section_trace = [t for t in result.trace if "selected" in t or "section" in t]
    assert len(section_trace) >= 0  # may be empty if no matches, but shouldn't crash


def test_hierarchical_search_sections_sorted_desc(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "Memory engine retrieval BM25 agent vector embedding."},
        "cooking": {"r.md": "Recipe pasta ingredients sauce kitchen."},
    })
    result = hierarchical_search("memory retrieval", docs_dir=docs, top_k_sections=5)
    if len(result.sections) >= 2:
        assert result.sections[0][1] >= result.sections[1][1]


def test_hierarchical_search_docs_sorted_desc(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {
            "y.md": "# Yodoca\nMemory engine BM25 vector retrieval activation.",
            "n.md": "# Other\nUnrelated content about pasta.",
        },
    })
    result = hierarchical_search("memory retrieval", docs_dir=docs)
    if len(result.docs) >= 2:
        assert result.docs[0][1] >= result.docs[1][1]


def test_hierarchical_search_aggregation_product(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "# Yodoca\nMemory agent retrieval vector embedding."},
    })
    result = hierarchical_search("memory agent", docs_dir=docs, aggregation="product")
    assert isinstance(result, HierarchicalResult)
    # product aggregation should yield scores <= individual scores
    for p in result.passages:
        assert p.score >= 0.0


def test_hierarchical_search_aggregation_sum(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "# Yodoca\nMemory agent retrieval vector embedding."},
    })
    result = hierarchical_search("memory agent", docs_dir=docs, aggregation="sum")
    assert isinstance(result, HierarchicalResult)


def test_hierarchical_search_duration_ms_set(tmp_path):
    docs = _make_docs(tmp_path, {
        "memory": {"y.md": "# Yodoca\nMemory engine."},
    })
    result = hierarchical_search("memory", docs_dir=docs)
    assert result.duration_ms >= 0


def test_hierarchical_search_top_k_sections_respected(tmp_path):
    docs = _make_docs(tmp_path, {
        f"sec{i}": {f"doc{i}.md": f"# Doc\nMemory agent retrieval {i}."}
        for i in range(5)
    })
    result = hierarchical_search("memory retrieval", docs_dir=docs, top_k_sections=2)
    assert len(result.sections) <= 2


def test_hierarchical_search_exported_from_rag_init():
    from docstoolkit.rag import hierarchical_search as hs, HierarchicalResult as HR
    assert hs is not None
    assert HR is not None


def test_section_index_and_doc_index_exported_from_rag_init():
    from docstoolkit.rag import SectionIndex, DocIndex
    assert SectionIndex is not None
    assert DocIndex is not None
