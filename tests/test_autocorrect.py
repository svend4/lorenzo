"""Tests for scripts/improve_autocorrect.py."""

import importlib
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_autocorrect")


def test_replacements_is_list():
    assert hasattr(mod, "REPLACEMENTS")
    assert isinstance(mod.REPLACEMENTS, list)


def test_replacements_not_empty():
    assert len(mod.REPLACEMENTS) > 0


def test_replacements_have_pattern_and_canonical():
    for item in mod.REPLACEMENTS:
        assert len(item) == 2, f"Replacement item {item} must be (pattern, canonical)"
        pattern, canonical = item
        assert isinstance(pattern, str)
        assert isinstance(canonical, str)


def test_fix_file_returns_int(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", True)
    f = tmp_path / "test.md"
    f.write_text("knowledge_space is awesome", encoding="utf-8")
    result = mod.fix_file(f)
    assert isinstance(result, int)


def test_fix_file_detects_knowledge_space(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", True)
    f = tmp_path / "test.md"
    f.write_text("knowledge_space is a great project", encoding="utf-8")
    count = mod.fix_file(f)
    assert count > 0


def test_fix_file_no_changes_for_correct_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", True)
    f = tmp_path / "test.md"
    f.write_text("knowledge-space and AgentFS are good projects", encoding="utf-8")
    count = mod.fix_file(f)
    assert count == 0


def test_fix_file_applies_changes_when_not_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", False)
    f = tmp_path / "test.md"
    f.write_text("knowledge_space is awesome", encoding="utf-8")
    mod.fix_file(f)
    content = f.read_text(encoding="utf-8")
    assert "knowledge-space" in content
    assert "knowledge_space" not in content


def test_fix_file_dry_run_does_not_modify(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", True)
    f = tmp_path / "test.md"
    original = "knowledge_space is awesome"
    f.write_text(original, encoding="utf-8")
    mod.fix_file(f)
    # File should be unchanged in dry-run
    assert f.read_text(encoding="utf-8") == original


def test_fix_file_ngt_memory(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", False)
    f = tmp_path / "test.md"
    f.write_text("NGT-Memory is a project", encoding="utf-8")
    mod.fix_file(f)
    content = f.read_text(encoding="utf-8")
    assert "NGT Memory" in content


def test_fix_file_agentfs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", False)
    f = tmp_path / "test.md"
    f.write_text("Agent FS is great", encoding="utf-8")
    mod.fix_file(f)
    content = f.read_text(encoding="utf-8")
    assert "AgentFS" in content


def test_fix_file_multiple_replacements(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", False)
    f = tmp_path / "test.md"
    f.write_text("knowledge_space and NGT-Memory are both good", encoding="utf-8")
    count = mod.fix_file(f)
    assert count >= 2


def test_fix_file_card_index(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", False)
    f = tmp_path / "test.md"
    f.write_text("Card Index is central to the system", encoding="utf-8")
    mod.fix_file(f)
    content = f.read_text(encoding="utf-8")
    assert "CardIndex" in content


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    (tmp_path / "doc.md").write_text("Using agentfs in this document.", encoding="utf-8")
    mod.main()  # dry-run → no file changes, must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # no files → must not raise


def test_main_apply_modifies_terms(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    (tmp_path / "doc.md").write_text("Using agentfs in this document.", encoding="utf-8")
    mod.main()  # apply → may modify file, must not raise
