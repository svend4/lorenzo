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
