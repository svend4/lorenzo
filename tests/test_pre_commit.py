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
