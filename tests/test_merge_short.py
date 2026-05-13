"""Tests for scripts/improve_merge_short.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_merge_short")


def test_min_chars_is_int():
    assert hasattr(mod, "MIN_CHARS")
    assert isinstance(mod.MIN_CHARS, int)
    assert mod.MIN_CHARS > 0


def test_merge_short_dry_run_no_changes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "section"
    subdir.mkdir()
    # Both files long enough — no merge needed
    (subdir / "a.md").write_text("a" * 200, encoding="utf-8")
    (subdir / "b.md").write_text("b" * 200, encoding="utf-8")
    mod.merge_short_files(dry_run=True)
    out = capsys.readouterr().out
    assert "0" in out


def test_merge_short_dry_run_no_short_files(tmp_path, monkeypatch, capsys):
    # dry-run with long files only — both should be reported as 0 merges
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "section"
    subdir.mkdir()
    (subdir / "a.md").write_text("a" * 200, encoding="utf-8")
    (subdir / "b.md").write_text("b" * 200, encoding="utf-8")
    mod.merge_short_files(dry_run=True)
    out = capsys.readouterr().out
    assert "0" in out


def test_merge_short_merges_files(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "section"
    subdir.mkdir()
    (subdir / "a.md").write_text("Content of A " * 20, encoding="utf-8")
    (subdir / "b.md").write_text("short", encoding="utf-8")
    mod.merge_short_files(dry_run=False)
    # b.md should be deleted and content merged into a.md
    assert not (subdir / "b.md").exists()
    a_content = (subdir / "a.md").read_text(encoding="utf-8")
    assert "short" in a_content


def test_merge_short_preserves_long_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "section"
    subdir.mkdir()
    (subdir / "a.md").write_text("a" * 200, encoding="utf-8")
    (subdir / "b.md").write_text("b" * 200, encoding="utf-8")
    mod.merge_short_files(dry_run=False)
    assert (subdir / "a.md").exists()
    assert (subdir / "b.md").exists()


def test_merge_short_skips_single_file_folders(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "section"
    subdir.mkdir()
    (subdir / "a.md").write_text("short", encoding="utf-8")  # Only one file
    mod.merge_short_files(dry_run=False)
    # Should not crash, single file cannot be merged
    assert (subdir / "a.md").exists()
