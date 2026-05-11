"""Tests for scripts/organize_docs.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("organize_docs")


# ── Constants ────────────────────────────────────────────────────────────────

def test_readme_content_is_string():
    assert isinstance(mod.README_CONTENT, str)
    assert len(mod.README_CONTENT) > 0


def test_readme_content_has_heading():
    assert mod.README_CONTENT.strip().startswith("#")


def test_docs_readme_is_string():
    assert isinstance(mod.DOCS_README, str)
    assert len(mod.DOCS_README) > 0


def test_docs_readme_has_sections():
    assert "01-svyazi" in mod.DOCS_README or "навигаци" in mod.DOCS_README.lower()


# ── write_readme_files ────────────────────────────────────────────────────────

def test_write_readme_files_creates_root_readme(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    (tmp_path / "docs").mkdir()

    mod.write_readme_files()

    assert (tmp_path / "README.md").exists()


def test_write_readme_files_creates_docs_readme(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setattr(mod, "DOCS", docs)

    mod.write_readme_files()

    assert (docs / "README.md").exists()


# ── module attributes ─────────────────────────────────────────────────────────

def test_root_is_path():
    assert isinstance(mod.ROOT, Path)


def test_docs_is_path():
    assert isinstance(mod.DOCS, Path)
