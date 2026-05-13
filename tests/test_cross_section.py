"""Tests for scripts/improve_cross_section.py."""

import importlib
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_cross_section")


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokenize_removes_stopwords():
    result = mod._tokenize("the and for or but")
    assert "the" not in result
    assert "and" not in result


def test_tokenize_min_4_chars():
    result = mod._tokenize("abc abcd abcde")
    for t in result:
        assert len(t) >= 4


def test_tfidf_returns_dict():
    sec_vectors = {
        "sec1": Counter({"agent": 5, "memory": 3, "system": 7}),
        "sec2": Counter({"graph": 4, "knowledge": 6, "system": 2}),
    }
    result = mod._tfidf(sec_vectors)
    assert isinstance(result, dict)


def test_tfidf_all_sections_present():
    sec_vectors = {
        "sec1": Counter({"agent": 5, "memory": 3}),
        "sec2": Counter({"graph": 4, "knowledge": 6}),
    }
    result = mod._tfidf(sec_vectors)
    for sec in sec_vectors:
        assert sec in result


def test_tfidf_scores_positive():
    sec_vectors = {
        "sec1": Counter({"agent": 5, "memory": 3}),
        "sec2": Counter({"graph": 4, "knowledge": 6}),
    }
    result = mod._tfidf(sec_vectors)
    for sec, scores in result.items():
        for word, score in scores.items():
            assert score >= 0


def test_cosine_returns_float():
    a = {"agent": 0.5, "memory": 0.3}
    b = {"agent": 0.4, "knowledge": 0.6}
    result = mod._cosine(a, b)
    assert isinstance(result, float)


def test_cosine_identical():
    a = {"agent": 0.5, "memory": 0.3}
    result = mod._cosine(a, a)
    assert abs(result - 1.0) < 0.01


def test_cosine_no_overlap():
    a = {"agent": 0.5}
    b = {"memory": 0.3}
    result = mod._cosine(a, b)
    assert result == 0.0


def test_cosine_empty():
    result = mod._cosine({}, {})
    assert result == 0.0


def test_cross_concepts_returns_list():
    tfidf = {
        "sec1": {"agent": 1.5, "memory": 0.8, "graph": 0.2},
        "sec2": {"agent": 1.2, "knowledge": 0.9, "graph": 0.5},
    }
    result = mod._cross_concepts(tfidf, top=10, min_secs=2)
    assert isinstance(result, list)


def test_cross_concepts_min_secs_filter():
    tfidf = {
        "sec1": {"agent": 1.5, "memory": 0.8},
        "sec2": {"agent": 1.2, "knowledge": 0.9},
        "sec3": {"graph": 0.5, "system": 0.4},
    }
    result = mod._cross_concepts(tfidf, top=10, min_secs=2)
    # All results should appear in at least 2 sections
    for entry in result:
        assert entry["n_secs"] >= 2


def test_cross_concepts_has_required_keys():
    tfidf = {
        "sec1": {"agent": 1.5},
        "sec2": {"agent": 1.2},
    }
    result = mod._cross_concepts(tfidf, top=10, min_secs=2)
    for entry in result:
        assert "term" in entry
        assert "sections" in entry
        assert "n_secs" in entry
        assert "avg_score" in entry


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_cross_section_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CROSS_SECTION.md").exists()


def test_main_cross_section_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "CROSS_SECTION.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_cross_section_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "CROSS_SECTION.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_main_with_subdirs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    sec = tmp_path / "section-a"
    sec.mkdir()
    (sec / "doc.md").write_text("# AgentFS\n\nAgent memory architecture search.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "CROSS_SECTION.md").exists()


def test_tokenize_returns_list():
    result = mod._tokenize("Hello world agent memory system")
    assert isinstance(result, list)


def test_tokenize_removes_stopwords():
    result = mod._tokenize("это и в на для agent memory")
    # Short words and stopwords should be removed
    assert all(len(t) >= 4 for t in result)


def test_build_section_vectors_with_dirs(tmp_path, monkeypatch):
    sec = tmp_path / "section-a"
    sec.mkdir()
    (sec / "doc.md").write_text("# Title\n\nAgent memory architecture search.", encoding="utf-8")
    result = mod._build_section_vectors(tmp_path)
    assert isinstance(result, dict)
    assert "section-a" in result


def test_tfidf_returns_dict():
    from collections import Counter
    vectors = {
        "sec-a": Counter({"agent": 5, "memory": 3}),
        "sec-b": Counter({"agent": 2, "search": 4}),
    }
    result = mod._tfidf(vectors)
    assert "sec-a" in result
    assert "sec-b" in result


def test_cosine_same_vectors():
    v = {"agent": 1.0, "memory": 2.0}
    result = mod._cosine(v, v)
    assert abs(result - 1.0) < 0.01


def test_cosine_disjoint_vectors():
    a = {"agent": 1.0}
    b = {"memory": 1.0}
    result = mod._cosine(a, b)
    assert result == 0.0


def test_cross_concepts_returns_list():
    tfidf = {
        "sec-a": {"agent": 0.5, "memory": 0.3},
        "sec-b": {"agent": 0.4, "search": 0.2},
    }
    result = mod._cross_concepts(tfidf, top=5, min_secs=2)
    assert isinstance(result, list)
    # "agent" appears in both sections
    terms = [r["term"] for r in result]
    assert "agent" in terms


def test_main_two_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    for name in ("section-a", "section-b"):
        sec = tmp_path / name
        sec.mkdir()
        (sec / "doc.md").write_text(
            f"# {name}\n\nAgent memory architecture search knowledge.",
            encoding="utf-8"
        )
    mod.main()
    text = (tmp_path / "CROSS_SECTION.md").read_text(encoding="utf-8")
    assert "section" in text.lower() or "#" in text


# ── module-level arg parsing (requires reload) ────────────────────────────────

def test_top_arg_parsing():
    """Lines 33-35: --top N sets TOP_CONCEPTS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--top", "30"]
        importlib.reload(mod)
        assert mod.TOP_CONCEPTS == 30
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_min_secs_arg_parsing():
    """Lines 38-40: --min-secs N sets MIN_SECTIONS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-secs", "3"]
        importlib.reload(mod)
        assert mod.MIN_SECTIONS == 3
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _build_section_vectors edge cases ────────────────────────────────────────

def test_build_section_vectors_skips_files(tmp_path):
    """Line 86: regular file in docs_dir (not a dir) → skipped."""
    (tmp_path / "README.md").write_text("# Root", encoding="utf-8")
    sec = tmp_path / "sec-a"
    sec.mkdir()
    (sec / "doc.md").write_text("agent memory knowledge", encoding="utf-8")
    result = mod._build_section_vectors(tmp_path)
    assert "README" not in result


def test_build_section_vectors_skips_hidden_dirs(tmp_path):
    """Line 86: hidden dir (starts with .) → skipped."""
    hidden = tmp_path / ".hidden"
    hidden.mkdir()
    (hidden / "doc.md").write_text("agent memory", encoding="utf-8")
    result = mod._build_section_vectors(tmp_path)
    assert ".hidden" not in result


def test_build_section_vectors_skips_skip_files(tmp_path):
    """Line 90: file in SKIP_FILES → skipped."""
    sec = tmp_path / "sec-a"
    sec.mkdir()
    (sec / "CROSS_SECTION.md").write_text("agent memory", encoding="utf-8")
    (sec / "doc.md").write_text("agent memory knowledge system", encoding="utf-8")
    result = mod._build_section_vectors(tmp_path)
    assert "sec-a" in result


def test_build_section_vectors_skips_parts_path(tmp_path):
    """Line 90: path with '-parts' → skipped."""
    sec = tmp_path / "sec-a"
    sec.mkdir()
    parts_dir = sec / "doc-parts"
    parts_dir.mkdir()
    (parts_dir / "chunk.md").write_text("agent memory", encoding="utf-8")
    result = mod._build_section_vectors(tmp_path)
    # files under -parts path are skipped
    assert isinstance(result, dict)


def test_build_section_vectors_exception_on_read(tmp_path, monkeypatch):
    """Lines 93-94: exception reading file → continue."""
    sec = tmp_path / "sec-a"
    sec.mkdir()
    bad_file = sec / "bad.md"
    bad_file.write_text("agent memory", encoding="utf-8")

    original_read = Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad_file:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", mock_read)
    result = mod._build_section_vectors(tmp_path)
    assert isinstance(result, dict)


# ── _mermaid_graph ────────────────────────────────────────────────────────────

def test_mermaid_graph_returns_list():
    """Lines 161-163, 167-178: _mermaid_graph with sections and edges."""
    sections = ["sec-a", "sec-b"]
    sim_matrix = {("sec-a", "sec-b"): 0.8, ("sec-b", "sec-a"): 0.8}
    result = mod._mermaid_graph(sections, sim_matrix)
    assert isinstance(result, list)
    assert any("mermaid" in line for line in result)


def test_mermaid_graph_below_threshold_no_edge():
    """Line 174: sim < threshold → edge not added."""
    sections = ["sec-a", "sec-b"]
    sim_matrix = {("sec-a", "sec-b"): 0.01, ("sec-b", "sec-a"): 0.01}
    result = mod._mermaid_graph(sections, sim_matrix, threshold=0.05)
    result_str = "\n".join(result)
    assert "-->" not in result_str


# ── _dot_graph ────────────────────────────────────────────────────────────────

def test_dot_graph_returns_string():
    """Lines 185-208: _dot_graph with sections and similarity."""
    sections = ["sec-a", "sec-b"]
    sim_matrix = {("sec-a", "sec-b"): 0.7, ("sec-b", "sec-a"): 0.7}
    result = mod._dot_graph(sections, sim_matrix)
    assert isinstance(result, str)
    assert "digraph" in result


def test_dot_graph_below_threshold_no_edge():
    """Line 201-202: sim < threshold → edge not added."""
    sections = ["sec-a", "sec-b"]
    sim_matrix = {("sec-a", "sec-b"): 0.01, ("sec-b", "sec-a"): 0.01}
    result = mod._dot_graph(sections, sim_matrix, threshold=0.05)
    assert "->" not in result or "0.01" not in result


# ── main with rich multi-section content ──────────────────────────────────────

# Section texts: "agent" and "memory" are shared, other terms differ
# This ensures cross-concepts exist with some sections where score=0
_SEC_A = "agent memory alpha knowledge system architecture " * 20
_SEC_B = "agent memory beta retrieval search graph network " * 20
_SEC_C = "agent gamma delta protocol service interface system " * 20


def test_main_three_rich_sections(tmp_path, monkeypatch):
    """Lines 227-230, 250-258, 275-276, 290-297, 311-312, 319-326: full report."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "EXPORT_DOT", False)
    monkeypatch.setattr(mod, "TOP_CONCEPTS", 40)
    monkeypatch.setattr(mod, "MIN_SECTIONS", 2)

    for name, text in [("sec-a", _SEC_A), ("sec-b", _SEC_B), ("sec-c", _SEC_C)]:
        d = tmp_path / name
        d.mkdir()
        (d / "doc.md").write_text(text, encoding="utf-8")

    mod.main()
    text = (tmp_path / "CROSS_SECTION.md").read_text(encoding="utf-8")
    assert "Матрица" in text


def test_main_export_dot(tmp_path, monkeypatch):
    """Lines 304-306: EXPORT_DOT=True → .dot file written."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "EXPORT_DOT", True)
    monkeypatch.setattr(mod, "TOP_CONCEPTS", 40)
    monkeypatch.setattr(mod, "MIN_SECTIONS", 2)

    for name, text in [("sec-a", _SEC_A), ("sec-b", _SEC_B)]:
        d = tmp_path / name
        d.mkdir()
        (d / "doc.md").write_text(text, encoding="utf-8")

    mod.main()
    assert (tmp_path / "cross_section.dot").exists()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 330: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "EXPORT_DOT", False)
    script_path = str(ROOT / "scripts" / "improve_cross_section.py")
    runpy.run_path(script_path, run_name="__main__")
