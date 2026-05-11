"""Tests for scripts/improve_quality_patch.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_quality_patch")


def test_quality_score_returns_int():
    result = mod.quality_score("# Title\n\nSome content.")
    assert isinstance(result, int)


def test_quality_score_max_100():
    long_text = (
        "# Title\n\n<!-- summary -->\n<!-- tags: test -->\n\n> [!NOTE]\n> Note here.\n\n"
        + "word " * 300
        + "\n```python\ncode()\n```\n"
        + "[Link](http://example.com) " * 5
    )
    result = mod.quality_score(long_text)
    assert result <= 100


def test_quality_score_empty():
    result = mod.quality_score("")
    assert result >= 0


def test_quality_score_with_h1():
    result_with = mod.quality_score("# Title\n\nSome content.")
    result_without = mod.quality_score("No heading.\n\nSome content.")
    assert result_with > result_without


def test_quality_score_with_summary():
    result_with = mod.quality_score("# T\n\n<!-- summary -->\nSome content.")
    result_without = mod.quality_score("# T\n\nSome content.")
    assert result_with > result_without


def test_quality_score_with_tags():
    result_with = mod.quality_score("# T\n\n<!-- tags: a, b -->\nSome content.")
    result_without = mod.quality_score("# T\n\nSome content.")
    assert result_with > result_without


def test_quality_score_with_callout():
    result_with = mod.quality_score("# T\n\n> [!NOTE]\n> Info here.\n\nContent.")
    result_without = mod.quality_score("# T\n\nContent.")
    assert result_with > result_without


def test_patch_file_returns_bool(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nShort.", encoding="utf-8")
    result = mod.patch_file(f)
    assert isinstance(result, bool)


def test_patch_file_adds_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "myfile.md"
    f.write_text("# My Title\n\nContent without summary.", encoding="utf-8")
    mod.patch_file(f)
    text = f.read_text(encoding="utf-8")
    assert "<!-- summary" in text


def test_patch_file_adds_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "myfile.md"
    f.write_text("# My Title\n\nContent without tags.", encoding="utf-8")
    mod.patch_file(f)
    text = f.read_text(encoding="utf-8")
    assert "<!-- tags" in text


def test_patch_file_adds_callout(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "myfile.md"
    f.write_text("# My Title\n\nContent.", encoding="utf-8")
    mod.patch_file(f)
    text = f.read_text(encoding="utf-8")
    assert "> [!" in text


def test_patch_file_no_change_if_perfect(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    perfect = (
        "# Title\n\n<!-- summary -->\n<!-- tags: test -->\n\n> [!NOTE]\n> Info.\n\n"
        + "word " * 300
        + "\n```python\ncode()\n```\n"
        + "[Link](http://example.com) " * 5
    )
    f = tmp_path / "perfect.md"
    f.write_text(perfect, encoding="utf-8")
    if mod.quality_score(perfect) == 100:
        result = mod.patch_file(f)
        assert result is False


def test_patch_file_modifies_short_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "short.md"
    f.write_text("# My Topic\n\nShort content.", encoding="utf-8")
    result = mod.patch_file(f)
    assert result is True


def test_skip_dirs_constant():
    assert hasattr(mod, "SKIP_DIRS")
    assert isinstance(mod.SKIP_DIRS, set)
    assert "obsidian" in mod.SKIP_DIRS


def test_skip_files_constant():
    assert hasattr(mod, "SKIP_FILES")
    assert isinstance(mod.SKIP_FILES, set)
    assert "METRICS.md" in mod.SKIP_FILES


def test_toc_markers_constant():
    assert hasattr(mod, "TOC_MARKERS")
    assert isinstance(mod.TOC_MARKERS, tuple)
    assert any("toc" in m.lower() for m in mod.TOC_MARKERS)
