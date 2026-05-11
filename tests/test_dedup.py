"""
Тесты для scripts/improve_dedup.py.

Покрытие:
  - file_hash()           — MD5 после нормализации пробелов
  - split_paragraphs()    — только абзацы длиннее 200 символов
  - paragraph_hash_map()  — {hash: paragraph_text}
  - _truncate()           — обрезка + очистка ссылок
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_dedup")

# ── file_hash ─────────────────────────────────────────────────────────────────

def test_file_hash_returns_string(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    result = mod.file_hash(f)
    assert isinstance(result, str)
    assert len(result) == 32  # MD5 hex


def test_file_hash_same_content_same_hash(tmp_path):
    f1 = tmp_path / "a.md"
    f2 = tmp_path / "b.md"
    f1.write_text("# Same content here\n\nBody.", encoding="utf-8")
    f2.write_text("# Same content here\n\nBody.", encoding="utf-8")
    assert mod.file_hash(f1) == mod.file_hash(f2)


def test_file_hash_different_content_different_hash(tmp_path):
    f1 = tmp_path / "a.md"
    f2 = tmp_path / "b.md"
    f1.write_text("# Document One\n\nBody one.", encoding="utf-8")
    f2.write_text("# Document Two\n\nBody two.", encoding="utf-8")
    assert mod.file_hash(f1) != mod.file_hash(f2)


def test_file_hash_whitespace_normalized(tmp_path):
    f1 = tmp_path / "a.md"
    f2 = tmp_path / "b.md"
    f1.write_text("# Title\n\nContent here.", encoding="utf-8")
    f2.write_text("# Title\n\n\n\nContent   here.", encoding="utf-8")
    assert mod.file_hash(f1) == mod.file_hash(f2)

# ── split_paragraphs ──────────────────────────────────────────────────────────

def test_split_paragraphs_returns_list():
    result = mod.split_paragraphs("Some text\n\nAnother paragraph.")
    assert isinstance(result, list)


def test_split_paragraphs_filters_short():
    text = "Short.\n\nAlso short.\n\n" + "x" * 250
    result = mod.split_paragraphs(text)
    assert len(result) == 1
    assert result[0].startswith("x")


def test_split_paragraphs_keeps_long():
    long_para = "А" * 250
    text = f"Short.\n\n{long_para}\n\nAnother short."
    result = mod.split_paragraphs(text)
    assert any(p.startswith("А") for p in result)


def test_split_paragraphs_empty_text():
    assert mod.split_paragraphs("") == []


def test_split_paragraphs_no_long_paragraphs():
    text = "Короткий.\n\nТоже короткий.\n\nИ этот тоже."
    assert mod.split_paragraphs(text) == []


def test_split_paragraphs_multiple_long():
    p1 = "А" * 250
    p2 = "Б" * 250
    text = f"{p1}\n\n{p2}"
    result = mod.split_paragraphs(text)
    assert len(result) == 2

# ── paragraph_hash_map ────────────────────────────────────────────────────────

def test_paragraph_hash_map_returns_dict():
    result = mod.paragraph_hash_map("Short.\n\nAlso short.")
    assert isinstance(result, dict)


def test_paragraph_hash_map_empty_for_short_text():
    result = mod.paragraph_hash_map("Too short.")
    assert result == {}


def test_paragraph_hash_map_keys_are_hashes():
    long_para = "Достаточно длинный абзац для теста " * 10
    result = mod.paragraph_hash_map(long_para)
    for key in result:
        assert len(key) == 32  # MD5


def test_paragraph_hash_map_values_are_paragraphs():
    long_para = "Длинный абзац содержит много текста " * 8
    result = mod.paragraph_hash_map(long_para)
    for val in result.values():
        assert len(val) > 200


def test_paragraph_hash_map_same_para_same_hash():
    para = "Одинаковый абзац для проверки хэша " * 8
    text = f"{para}\n\nЕщё какой-то текст который короткий.\n\n{para}"
    result = mod.paragraph_hash_map(text)
    # Same paragraph should produce same hash → only one entry
    assert len(result) == 1

# ── _truncate ─────────────────────────────────────────────────────────────────

def test_truncate_short_text_unchanged():
    text = "Короткий текст."
    assert mod._truncate(text, max_len=200) == "Короткий текст."


def test_truncate_long_text_cut():
    text = "A" * 300
    result = mod._truncate(text, max_len=200)
    assert len(result) <= 204  # 200 + "…"
    assert result.endswith("…")


def test_truncate_removes_md_links():
    text = "See [AgentFS](docs/agentfs.md) for more info about the project."
    result = mod._truncate(text)
    assert "[" not in result
    assert "]" not in result
    assert "AgentFS" in result


def test_truncate_replaces_newlines():
    text = "Line one.\nLine two.\nLine three."
    result = mod._truncate(text)
    assert "\n" not in result


def test_truncate_returns_string():
    assert isinstance(mod._truncate("text"), str)


def test_truncate_exact_limit_not_cut():
    text = "A" * 200
    result = mod._truncate(text, max_len=200)
    assert not result.endswith("…")
