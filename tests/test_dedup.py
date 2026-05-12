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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_duplicates_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc1.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    (tmp_path / "doc2.md").write_text("# Yodoca\n\nMemory consolidation agent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "DUPLICATES.md").exists()


def test_main_duplicates_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc1.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "DUPLICATES.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DUPLICATES.md").exists()


def test_main_duplicates_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DUPLICATES.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── _is_mirror ────────────────────────────────────────────────────────────────

def test_is_mirror_true_for_obsidian(tmp_path, monkeypatch):
    """Line 56: path under obsidian/ → True."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    mirror_dir = tmp_path / "obsidian"
    mirror_dir.mkdir()
    mirror_file = mirror_dir / "doc.md"
    mirror_file.touch()
    assert mod._is_mirror(mirror_file) is True


def test_is_mirror_false_for_regular(tmp_path, monkeypatch):
    """Line 56: path under regular/ → False."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    regular_dir = tmp_path / "01-svyazi"
    regular_dir.mkdir()
    regular_file = regular_dir / "doc.md"
    regular_file.touch()
    assert mod._is_mirror(regular_file) is False


# ── find_exact_duplicates ─────────────────────────────────────────────────────

def test_find_exact_duplicates_returns_group(tmp_path, monkeypatch):
    """Lines 68-70: two files with same content → one group of non-mirrors."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    content = "# Same\n\nIdentical content for both files in the dedup test."
    (tmp_path / "a.md").write_text(content, encoding="utf-8")
    (tmp_path / "b.md").write_text(content, encoding="utf-8")
    result = mod.find_exact_duplicates()
    assert len(result) == 1
    assert len(result[0]) == 2


def test_find_exact_duplicates_excludes_mirrors(tmp_path, monkeypatch):
    """Lines 68-70: one non-mirror + one mirror → excluded from duplicates."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    content = "# Same\n\nIdentical content for dedup mirror test."
    (tmp_path / "original.md").write_text(content, encoding="utf-8")
    mirror_dir = tmp_path / "obsidian"
    mirror_dir.mkdir()
    (mirror_dir / "mirror.md").write_text(content, encoding="utf-8")
    result = mod.find_exact_duplicates()
    assert len(result) == 0


# ── find_similar_files ────────────────────────────────────────────────────────

def test_find_similar_files_with_short_files_empty(tmp_path, monkeypatch):
    """Line 82 not triggered (short files → no hmap entry): result is empty."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("Short.", encoding="utf-8")
    result = mod.find_similar_files()
    assert result == []


def test_find_similar_files_finds_pair(tmp_path, monkeypatch):
    """Lines 82, 87-100: two files with same long paragraph → pair found."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    long_para = "x" * 250
    (tmp_path / "a.md").write_text(f"# A\n\n{long_para}\n", encoding="utf-8")
    (tmp_path / "b.md").write_text(f"# B\n\n{long_para}\n", encoding="utf-8")
    result = mod.find_similar_files(threshold=0.1)
    assert len(result) >= 1
    assert result[0][2] >= 0.1  # jaccard score


def test_find_similar_files_different_paragraphs(tmp_path, monkeypatch):
    """Lines 87-100: two files with different long paragraphs → no pair at high threshold."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text(f"# A\n\n{'a' * 250}\n", encoding="utf-8")
    (tmp_path / "b.md").write_text(f"# B\n\n{'b' * 250}\n", encoding="utf-8")
    result = mod.find_similar_files(threshold=0.9)
    assert result == []


# ── main with exact/similar duplicates ───────────────────────────────────────

def test_main_with_exact_duplicates_section(tmp_path, monkeypatch):
    """Lines 130-136: exact duplicates section rendered in output."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    content = "# Same\n\nIdentical content for both files test."
    (tmp_path / "a.md").write_text(content, encoding="utf-8")
    (tmp_path / "b.md").write_text(content, encoding="utf-8")
    mod.main()
    text = (tmp_path / "DUPLICATES.md").read_text(encoding="utf-8")
    assert "Точные дубли" in text


def test_main_with_similar_files_section(tmp_path, monkeypatch):
    """Lines 139-151: similar files section rendered in output."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    long_para = "x" * 250
    (tmp_path / "a.md").write_text(f"# A\n\n{long_para}\n", encoding="utf-8")
    (tmp_path / "b.md").write_text(f"# B\n\n{long_para}\n", encoding="utf-8")
    mod.main()
    text = (tmp_path / "DUPLICATES.md").read_text(encoding="utf-8")
    assert "Похожие файлы" in text


# ── module-level threshold parsing (requires reload) ─────────────────────────

def test_threshold_from_equals_arg():
    """Line 23: --threshold=X arg sets THRESHOLD."""
    import sys, importlib
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--threshold=0.3"]
        importlib.reload(mod)
        assert abs(mod.THRESHOLD - 0.3) < 0.001
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_threshold_from_space_arg():
    """Lines 25-27: --threshold X (space-separated) sets THRESHOLD."""
    import sys, importlib
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--threshold", "0.25"]
        importlib.reload(mod)
        assert abs(mod.THRESHOLD - 0.25) < 0.001
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 164: __main__ block executes main()."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    script_path = str(ROOT / "scripts" / "improve_dedup.py")
    runpy.run_path(script_path, run_name="__main__")
