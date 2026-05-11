"""Tests for scripts/improve_pre_commit.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_pre_commit")


def test_pre_commit_config_is_string():
    assert hasattr(mod, "PRE_COMMIT_CONFIG")
    assert isinstance(mod.PRE_COMMIT_CONFIG, str)


def test_pre_commit_config_is_yaml():
    assert "repos:" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_has_hooks():
    assert "hooks:" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_has_spellcheck():
    assert "spellcheck" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_has_broken_links():
    assert "broken-links" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_has_search_index():
    assert "search-index" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_targets_markdown():
    assert ".md$" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_has_standard_hooks():
    assert "trailing-whitespace" in mod.PRE_COMMIT_CONFIG
    assert "end-of-file-fixer" in mod.PRE_COMMIT_CONFIG


def test_pre_commit_config_uses_pre_commit_hooks_repo():
    assert "pre-commit/pre-commit-hooks" in mod.PRE_COMMIT_CONFIG


def test_dry_run_attribute_exists():
    assert hasattr(mod, "DRY_RUN")
    assert isinstance(mod.DRY_RUN, bool)


def test_today_is_string():
    assert hasattr(mod, "TODAY")
    assert isinstance(mod.TODAY, str)
    assert len(mod.TODAY) == 10  # YYYY-MM-DD


def test_root_is_path():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_pre_commit_yaml(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "INSTALL", False)
    mod.main()
    assert (tmp_path / ".pre-commit-config.yaml").exists()


def test_main_yaml_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "INSTALL", False)
    mod.main()
    text = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "repos:" in text or "hooks:" in text


def test_main_dry_run_no_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "INSTALL", False)
    mod.main()
    assert not (tmp_path / ".pre-commit-config.yaml").exists()


def test_main_updates_gitignore(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "INSTALL", False)
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("# existing\n*.pyc\n", encoding="utf-8")
    mod.main()
    content = gitignore.read_text(encoding="utf-8")
    assert ".pre-commit-cache" in content
