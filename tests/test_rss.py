"""Tests for scripts/improve_rss.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_rss")


def test_rfc822_returns_string():
    result = mod._rfc822(1700000000)
    assert isinstance(result, str)


def test_rfc822_contains_date():
    result = mod._rfc822(1700000000)
    # RFC 822 format has commas and timezone
    assert "," in result or "GMT" in result


def test_iso8601_returns_string():
    result = mod._iso8601(1700000000)
    assert isinstance(result, str)


def test_iso8601_contains_t():
    result = mod._iso8601(1700000000)
    assert "T" in result


def test_iso8601_has_utc():
    result = mod._iso8601(1700000000)
    assert "+00:00" in result or "Z" in result


def test_escape_xml_returns_string():
    result = mod._escape_xml("hello world")
    assert isinstance(result, str)


def test_escape_xml_escapes_ampersand():
    result = mod._escape_xml("a & b")
    assert "&amp;" in result
    assert " & " not in result


def test_escape_xml_escapes_less_than():
    result = mod._escape_xml("a < b")
    assert "&lt;" in result


def test_escape_xml_escapes_greater_than():
    result = mod._escape_xml("a > b")
    assert "&gt;" in result


def test_escape_xml_escapes_quotes():
    result = mod._escape_xml('say "hello"')
    assert "&quot;" in result


def test_build_description_returns_string():
    commit = {
        "subject": "Test commit",
        "files": ["docs/test.md"],
        "hash": "abc12345",
        "full_hash": "abc1234567890",
    }
    result = mod._build_description(commit)
    assert isinstance(result, str)


def test_build_description_has_subject():
    commit = {
        "subject": "Test commit message",
        "files": [],
        "hash": "abc12345",
        "full_hash": "abc1234567890",
    }
    result = mod._build_description(commit)
    assert "Test commit message" in result


def test_build_rss_returns_string():
    result = mod.build_rss([])
    assert isinstance(result, str)


def test_build_rss_starts_with_xml():
    result = mod.build_rss([])
    assert result.startswith("<?xml")


def test_build_rss_has_channel():
    result = mod.build_rss([])
    assert "<channel>" in result


def test_build_rss_with_commit():
    commits = [{
        "subject": "feat: test update",
        "files": ["docs/test.md"],
        "hash": "abc12345",
        "full_hash": "abc1234567890abc",
        "timestamp": 1700000000,
        "email": "test@example.com",
    }]
    result = mod.build_rss(commits)
    assert "feat: test update" in result


def test_build_atom_returns_string():
    result = mod.build_atom([])
    assert isinstance(result, str)


def test_build_atom_starts_with_xml():
    result = mod.build_atom([])
    assert result.startswith("<?xml")


def test_build_atom_has_feed_tag():
    result = mod.build_atom([])
    assert "<feed" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_rss_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "_get_commits", lambda: [])
    mod.main()
    assert (tmp_path / "feed.rss").exists()


def test_main_creates_atom_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "_get_commits", lambda: [])
    mod.main()
    assert (tmp_path / "feed.atom").exists()


def test_main_with_commits_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "_get_commits", lambda: [{
        "hash": "abc123", "full_hash": "abc123def456", "author": "test@test.com",
        "timestamp": 1746100000, "date": "2026-05-01",
        "subject": "feat: test commit", "files": ["docs/doc.md"]
    }])
    mod.main()
    assert (tmp_path / "feed.rss").exists()
