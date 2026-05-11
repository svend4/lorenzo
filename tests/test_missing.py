"""Tests for scripts/improve_missing.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_missing")


def test_expected_coverage_is_dict():
    assert hasattr(mod, "EXPECTED_COVERAGE")
    assert isinstance(mod.EXPECTED_COVERAGE, dict)


def test_expected_coverage_has_entries():
    assert len(mod.EXPECTED_COVERAGE) > 0


def test_expected_coverage_entries_have_min_files():
    for term, thresholds in mod.EXPECTED_COVERAGE.items():
        assert "min_files" in thresholds, f"Missing min_files for {term}"


def test_expected_coverage_entries_have_min_words():
    for term, thresholds in mod.EXPECTED_COVERAGE.items():
        assert "min_words" in thresholds, f"Missing min_words for {term}"


def test_expected_coverage_contains_svyazi():
    assert "Svyazi" in mod.EXPECTED_COVERAGE


def test_expected_coverage_contains_agentfs():
    assert "AgentFS" in mod.EXPECTED_COVERAGE


def test_measure_coverage_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("AgentFS is a great project", encoding="utf-8")
    result = mod.measure_coverage("AgentFS")
    assert isinstance(result, dict)


def test_measure_coverage_has_files_key(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.measure_coverage("NonExistentTerm")
    assert "files" in result
    assert "words" in result


def test_measure_coverage_finds_term(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("Svyazi is mentioned here in this paragraph", encoding="utf-8")
    result = mod.measure_coverage("Svyazi")
    assert len(result["files"]) == 1


def test_measure_coverage_missing_term(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("no relevant content here", encoding="utf-8")
    result = mod.measure_coverage("UniqueTermXYZ")
    assert len(result["files"]) == 0
    assert result["words"] == 0


def test_measure_coverage_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("AGENTFS mentioned in lowercase agentfs context", encoding="utf-8")
    result = mod.measure_coverage("agentfs")
    assert len(result["files"]) == 1


def test_measure_coverage_counts_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("Yodoca is used here\n\nSome other paragraph without the term", encoding="utf-8")
    result = mod.measure_coverage("Yodoca")
    assert result["words"] > 0


def test_measure_coverage_multiple_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("Rufler is a project", encoding="utf-8")
    (tmp_path / "b.md").write_text("Rufler mentioned again", encoding="utf-8")
    result = mod.measure_coverage("Rufler")
    assert len(result["files"]) == 2
