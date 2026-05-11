"""Tests for scripts/improve_orphans.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_orphans")


def test_always_ok_is_set():
    assert hasattr(mod, "ALWAYS_OK")
    assert isinstance(mod.ALWAYS_OK, set)


def test_always_ok_contains_readme():
    assert "README.md" in mod.ALWAYS_OK


def test_always_ok_contains_contacts():
    assert "CONTACTS.md" in mod.ALWAYS_OK


def test_collect_all_links_returns_set(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("See [other](other.md) for more.", encoding="utf-8")
    result = mod.collect_all_links([f])
    assert isinstance(result, set)


def test_collect_all_links_finds_local_link(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    target = tmp_path / "other.md"
    target.write_text("target content", encoding="utf-8")
    f = tmp_path / "doc.md"
    f.write_text("See [other](other.md) for more.", encoding="utf-8")
    result = mod.collect_all_links([f])
    # Should contain resolved path relative to ROOT
    assert any("other.md" in r for r in result)


def test_collect_all_links_ignores_http(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("See [external](https://github.com/user/repo) for more.", encoding="utf-8")
    result = mod.collect_all_links([f])
    assert not any("github.com" in r for r in result)


def test_collect_all_links_empty_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "empty.md"
    f.write_text("No links here, just plain text.", encoding="utf-8")
    result = mod.collect_all_links([f])
    assert result == set()


def test_collect_all_links_multiple_links(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text(
        "See [a](a.md) and [b](b.md) for more.",
        encoding="utf-8"
    )
    result = mod.collect_all_links([f])
    assert len(result) >= 2


def test_collect_all_links_multiple_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f1 = tmp_path / "doc1.md"
    f1.write_text("See [a](a.md).", encoding="utf-8")
    f2 = tmp_path / "doc2.md"
    f2.write_text("See [b](b.md).", encoding="utf-8")
    result = mod.collect_all_links([f1, f2])
    assert len(result) >= 2


def test_collect_all_links_with_anchor(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("See [section](other.md#section) for more.", encoding="utf-8")
    result = mod.collect_all_links([f])
    # Anchor stripped, should still find the base file link
    assert any("other.md" in r for r in result)


def test_collect_all_links_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.collect_all_links([])
    assert result == set()
