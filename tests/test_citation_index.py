"""Tests for scripts/improve_citation_index.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_citation_index")


def test_domain_returns_string():
    result = mod._domain("https://github.com/user/repo")
    assert isinstance(result, str)


def test_domain_extracts_domain():
    result = mod._domain("https://github.com/user/repo")
    assert result == "github.com"


def test_domain_strips_www():
    result = mod._domain("https://www.example.com/path")
    assert not result.startswith("www.")


def test_domain_invalid_url():
    result = mod._domain("not a url")
    assert isinstance(result, str)


def test_authority_score_returns_int():
    result = mod._authority_score("https://github.com/user/repo")
    assert isinstance(result, int)


def test_authority_score_github():
    result = mod._authority_score("https://github.com/user/repo")
    assert result >= 4


def test_authority_score_arxiv():
    result = mod._authority_score("https://arxiv.org/abs/1234.5678")
    assert result >= 4


def test_authority_score_unknown():
    result = mod._authority_score("https://unknown-random-domain.xyz/page")
    assert result == 1


def test_extract_urls_returns_list():
    result = mod._extract_urls("See https://github.com/user/repo for more.")
    assert isinstance(result, list)


def test_extract_urls_finds_url():
    result = mod._extract_urls("See https://github.com/user/repo for more.")
    assert any("github.com" in u for u in result)


def test_extract_urls_skips_code_blocks():
    text = "```\nhttps://github.com/code/here\n```\nReal: https://example.com/real"
    result = mod._extract_urls(text)
    urls = " ".join(result)
    assert "code/here" not in urls


def test_extract_urls_multiple():
    text = "See https://github.com/a and https://arxiv.org/b"
    result = mod._extract_urls(text)
    assert len(result) >= 2


def test_normalize_url_returns_string():
    result = mod._normalize_url("https://github.com/user/repo.")
    assert isinstance(result, str)


def test_normalize_url_strips_trailing_period():
    result = mod._normalize_url("https://github.com/user/repo.")
    assert not result.endswith(".")


def test_normalize_url_strips_comma():
    result = mod._normalize_url("https://github.com/user/repo,")
    assert not result.endswith(",")


def test_normalize_url_no_change():
    url = "https://github.com/user/repo"
    result = mod._normalize_url(url)
    assert result == url


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_citation_index_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nSee https://github.com/user/repo for more.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "CITATION_INDEX.md").exists()


def test_main_citation_index_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nSee https://github.com/user/repo for details.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "CITATION_INDEX.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CITATION_INDEX.md").exists()


def test_main_citation_index_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "CITATION_INDEX.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
