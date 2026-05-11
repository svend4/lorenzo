"""Tests for scripts/improve_link_preview.py."""

import importlib
import sys
from pathlib import Path
from datetime import datetime, timedelta

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_link_preview")


def test_is_fresh_returns_bool():
    entry = {"checked": datetime.now().isoformat()}
    result = mod._is_fresh(entry)
    assert isinstance(result, bool)


def test_is_fresh_recent_entry():
    entry = {"checked": datetime.now().isoformat()}
    result = mod._is_fresh(entry)
    assert result is True


def test_is_fresh_old_entry():
    old_time = (datetime.now() - timedelta(days=100)).isoformat()
    entry = {"checked": old_time}
    result = mod._is_fresh(entry)
    assert result is False


def test_is_fresh_missing_checked():
    result = mod._is_fresh({})
    assert result is False


def test_is_fresh_invalid_date():
    result = mod._is_fresh({"checked": "not-a-date"})
    assert result is False


def test_extract_urls_returns_list():
    result = mod.extract_urls("See https://github.com/user/repo for details.")
    assert isinstance(result, list)


def test_extract_urls_finds_url():
    result = mod.extract_urls("See https://github.com/user/repo for details.")
    assert any("github.com" in u for u in result)


def test_extract_urls_multiple():
    text = "https://github.com/a and https://arxiv.org/b"
    result = mod.extract_urls(text)
    assert len(result) >= 2


def test_extract_urls_empty():
    result = mod.extract_urls("no urls here")
    assert result == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_empty_docs_creates_report(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "CACHE_FILE", tmp_path / "link_cache.json")
    mod.main()
    assert (tmp_path / "LINK_PREVIEW.md").exists()


def test_main_no_urls_creates_report(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "CACHE_FILE", tmp_path / "link_cache.json")
    (tmp_path / "doc.md").write_text("# Title\n\nNo links here.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "LINK_PREVIEW.md").exists()


def test_main_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "CACHE_FILE", tmp_path / "link_cache.json")
    mod.main()
    text = (tmp_path / "LINK_PREVIEW.md").read_text(encoding="utf-8")
    assert "# " in text
