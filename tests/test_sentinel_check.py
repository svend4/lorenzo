"""Tests for scripts/improve_sentinel_check.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_sentinel_check")


def test_pii_patterns_is_list():
    assert hasattr(mod, "PII_PATTERNS")
    assert isinstance(mod.PII_PATTERNS, list)
    assert len(mod.PII_PATTERNS) > 0


def test_unsafe_code_patterns_is_list():
    assert hasattr(mod, "UNSAFE_CODE_PATTERNS")
    assert isinstance(mod.UNSAFE_CODE_PATTERNS, list)
    assert len(mod.UNSAFE_CODE_PATTERNS) > 0


def test_license_risk_is_dict():
    assert hasattr(mod, "LICENSE_RISK")
    assert isinstance(mod.LICENSE_RISK, dict)
    assert "BSL" in mod.LICENSE_RISK


def test_http_re_is_compiled():
    assert hasattr(mod, "HTTP_RE")
    import re
    assert isinstance(mod.HTTP_RE, re.Pattern)


def test_scan_pii_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "clean.md"
    f.write_text("# Title\n\nNo personal information here.", encoding="utf-8")
    result = mod._scan_pii(f)
    assert isinstance(result, list)


def test_scan_pii_clean_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "clean.md"
    f.write_text("# Project\n\nThis is clean content with no PII.", encoding="utf-8")
    result = mod._scan_pii(f)
    assert result == []


def test_scan_pii_detects_email(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "PII_WHITELIST", set())
    f = tmp_path / "doc.md"
    f.write_text("Contact: user@realcompany.com for details.", encoding="utf-8")
    result = mod._scan_pii(f)
    assert any(r["issue"] == "email" for r in result)


def test_scan_pii_skips_sentinel_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "SENTINEL.md"
    f.write_text("Contact: user@example.com found.", encoding="utf-8")
    result = mod._scan_pii(f)
    assert result == []


def test_scan_pii_skips_placeholder_emails(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("Use foo@example.com as example.", encoding="utf-8")
    result = mod._scan_pii(f)
    # "example" in value → skipped
    assert not any(r["issue"] == "email" for r in result)


def test_scan_unsafe_code_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "script.py"
    f.write_text("import os\nos.path.join('a', 'b')\n", encoding="utf-8")
    result = mod._scan_unsafe_code(f)
    assert isinstance(result, list)


def test_scan_unsafe_code_detects_eval(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "script.py"
    f.write_text("result = eval(user_input)\n", encoding="utf-8")
    result = mod._scan_unsafe_code(f)
    assert any("eval" in r["issue"] for r in result)


def test_scan_unsafe_code_skips_itself(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "improve_sentinel_check.py"
    f.write_text("eval(x)\n", encoding="utf-8")
    result = mod._scan_unsafe_code(f)
    assert result == []


def test_scan_http_urls_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod._scan_http_urls(tmp_path)
    assert isinstance(result, list)


def test_scan_http_urls_finds_http(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("See http://example.com for details.", encoding="utf-8")
    result = mod._scan_http_urls(tmp_path)
    assert len(result) >= 1
    assert any("http://example.com" in r["url"] for r in result)


def test_scan_http_urls_ignores_https(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("See https://example.com for details.", encoding="utf-8")
    result = mod._scan_http_urls(tmp_path)
    assert result == []
