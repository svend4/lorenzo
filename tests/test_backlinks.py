"""
Тесты для scripts/improve_backlinks.py.

Покрытие:
  - extract_links()  — извлечение внутренних md-ссылок
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_backlinks")


# ── extract_links ─────────────────────────────────────────────────────────────

def test_extract_links_returns_set(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("plain text", f)
    assert isinstance(result, set)


def test_extract_links_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("", f)
    assert result == set()


def test_extract_links_skips_http(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("[Link](https://example.com)", f)
    assert len(result) == 0


def test_extract_links_skips_anchor(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n", encoding="utf-8")
    result = mod.extract_links("[Section](#heading)", f)
    assert len(result) == 0


def test_extract_links_finds_local_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    source.write_text("# Source\n", encoding="utf-8")
    result = mod.extract_links("[Link](target.md)", source)
    assert len(result) > 0


def test_extract_links_relative_path(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    sub = tmp_path / "sub"
    sub.mkdir()
    source = sub / "source.md"
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    source.write_text("# Source\n", encoding="utf-8")
    result = mod.extract_links("[Link](../target.md)", source)
    assert len(result) > 0


def test_extract_links_missing_target(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    result = mod.extract_links("[Link](nonexistent.md)", source)
    assert len(result) == 0
