"""Tests for scripts/verify_coverage.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("verify_coverage")


def test_key_terms_is_list():
    assert hasattr(mod, "KEY_TERMS")
    assert isinstance(mod.KEY_TERMS, list)
    assert len(mod.KEY_TERMS) > 0


def test_key_terms_are_strings():
    for term in mod.KEY_TERMS:
        assert isinstance(term, str)


def test_key_terms_include_known_projects():
    terms_lower = [t.lower() for t in mod.KEY_TERMS]
    assert any("agentfs" in t for t in terms_lower)
    assert any("yodoca" in t for t in terms_lower)


def test_count_chars_md_returns_int(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Hello World\n\nContent here.", encoding="utf-8")
    result = mod.count_chars_md(f)
    assert isinstance(result, int)
    assert result > 0


def test_count_chars_md_correct_count(tmp_path):
    text = "# Title\n\nContent."
    f = tmp_path / "doc.md"
    f.write_text(text, encoding="utf-8")
    result = mod.count_chars_md(f)
    assert result == len(text)


def test_count_docs_chars_returns_int(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Hello\n\nContent.", encoding="utf-8")
    result = mod.count_docs_chars()
    assert isinstance(result, int)
    assert result > 0


def test_count_docs_chars_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_docs_chars()
    assert result == 0


def test_check_terms_in_docs_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("AgentFS is a project for file system.", encoding="utf-8")
    result = mod.check_terms_in_docs(["AgentFS", "Nonexistent"])
    assert isinstance(result, dict)


def test_check_terms_in_docs_finds_present_term(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("AgentFS is a project.", encoding="utf-8")
    result = mod.check_terms_in_docs(["AgentFS"])
    assert result["AgentFS"] is True


def test_check_terms_in_docs_missing_term(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("Only unrelated content.", encoding="utf-8")
    result = mod.check_terms_in_docs(["AgentFS"])
    assert result["AgentFS"] is False


def test_check_h2_coverage_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    md = tmp_path / "source.md"
    md.write_text("# Title\n\n## Section One\n\nContent.\n\n## Section Two\n\nMore.", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text("Section One is documented.", encoding="utf-8")
    found, missing = mod.check_h2_coverage(md)
    assert isinstance(found, list)
    assert isinstance(missing, list)


def test_check_h2_coverage_finds_existing(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    monkeypatch.setattr(mod, "DOCS", docs_dir)
    md = tmp_path / "source.md"
    md.write_text("# Title\n\n## Section One\n\nContent.", encoding="utf-8")
    doc = docs_dir / "doc.md"
    doc.write_text("Section One is documented here in detail.", encoding="utf-8")
    found, missing = mod.check_h2_coverage(md)
    assert "Section One" in found


def test_check_h2_coverage_detects_missing(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    monkeypatch.setattr(mod, "DOCS", docs_dir)
    # source.md is NOT inside docs_dir so it won't be scanned
    md = tmp_path / "source.md"
    md.write_text("# Title\n\n## Nonexistent Section XYZ\n\nContent.", encoding="utf-8")
    doc = docs_dir / "unrelated.md"
    doc.write_text("Completely unrelated content about something else.", encoding="utf-8")
    found, missing = mod.check_h2_coverage(md)
    assert "Nonexistent Section XYZ" in missing


def test_check_short_files_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.check_short_files(min_chars=100)
    assert isinstance(result, list)


def test_check_short_files_finds_short(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "short.md"
    f.write_text("Hi.", encoding="utf-8")
    result = mod.check_short_files(min_chars=100)
    paths = [p for p, _ in result]
    assert f in paths


def test_check_short_files_excludes_long(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "long.md"
    f.write_text("# Title\n\n" + "word " * 100, encoding="utf-8")
    result = mod.check_short_files(min_chars=100)
    paths = [p for p, _ in result]
    assert f not in paths


def test_check_short_files_sorted_by_size(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "tiny.md").write_text("Hi.", encoding="utf-8")
    (tmp_path / "small.md").write_text("Hello world.", encoding="utf-8")
    result = mod.check_short_files(min_chars=100)
    if len(result) >= 2:
        sizes = [s for _, s in result]
        assert sizes == sorted(sizes)
