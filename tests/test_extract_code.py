"""
Тесты для scripts/improve_extract_code.py.

Покрытие:
  - extract_blocks()  — извлечение code-блоков из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_extract_code")


def _make_file(tmp_path, name="test.md"):
    f = tmp_path / name
    f.write_text("", encoding="utf-8")
    return f


# ── extract_blocks ────────────────────────────────────────────────────────────

def test_extract_blocks_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_blocks("plain text", f)
    assert isinstance(result, list)


def test_extract_blocks_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_blocks("", f)
    assert result == []


def test_extract_blocks_finds_python(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "# Title\n\n```python\ndef hello():\n    return 'world'\n```\n"
    result = mod.extract_blocks(text, f)
    assert len(result) > 0


def test_extract_blocks_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "```python\ndef hello():\n    return 'world'\n```\n"
    result = mod.extract_blocks(text, f)
    for block in result:
        assert "lang" in block
        assert "code" in block
        assert "context" in block
        assert "file" in block
        assert "lines" in block


def test_extract_blocks_detects_language(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "```yaml\nkey: value\nother: stuff\n```\n"
    result = mod.extract_blocks(text, f)
    if result:
        assert result[0]["lang"] == "yaml"


def test_extract_blocks_empty_lang(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "```\nsome code without language marker here\n```\n"
    result = mod.extract_blocks(text, f)
    if result:
        assert result[0]["lang"] == ""


def test_extract_blocks_skips_short_code(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "```python\nshort\n```\n"
    result = mod.extract_blocks(text, f)
    assert result == []


def test_extract_blocks_counts_lines(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "```python\nline1\nline2\nline3\nline4\nline5\n```\n"
    result = mod.extract_blocks(text, f)
    if result:
        assert result[0]["lines"] == 5


def test_extract_blocks_extracts_context(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "## My Section\n\n```python\ndef hello():\n    return 'world'\n```\n"
    result = mod.extract_blocks(text, f)
    if result:
        assert "My Section" in result[0]["context"]


def test_extract_blocks_multiple_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = (
        "```python\ndef hello():\n    return 'world'\n```\n"
        "```yaml\nkey: value\nother: stuff\n```\n"
    )
    result = mod.extract_blocks(text, f)
    assert len(result) == 2
