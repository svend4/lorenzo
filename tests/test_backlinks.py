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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_backlinks_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    (tmp_path / "doc1.md").write_text("# Doc1\n\nContent.", encoding="utf-8")
    (tmp_path / "doc2.md").write_text("# Doc2\n\n[Link](doc1.md)", encoding="utf-8")
    mod.main()
    assert (tmp_path / "BACKLINKS.md").exists()


def test_main_backlinks_md_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    (tmp_path / "doc.md").write_text("# Doc\n\nContent.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "BACKLINKS.md").read_text(encoding="utf-8")
    assert "Индекс обратных ссылок" in text


def test_main_dry_run_no_output(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--dry-run"])
    (tmp_path / "doc.md").write_text("# Doc\n\nContent.", encoding="utf-8")
    mod.main()
    assert not (tmp_path / "BACKLINKS.md").exists()


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    mod.main()
    assert (tmp_path / "BACKLINKS.md").exists()
