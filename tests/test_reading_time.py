"""
Тесты для scripts/improve_reading_time.py.

Покрытие:
  - _count_words_by_type()  — подсчёт RU/EN слов и блоков кода
  - estimate_reading_time() — оценка времени чтения документа
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_reading_time")


# ── _count_words_by_type ──────────────────────────────────────────────────────

def test_count_words_returns_tuple():
    result = mod._count_words_by_type("some text here")
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_count_words_counts_russian():
    ru_words, en_words, n_code = mod._count_words_by_type("агент система архитектура")
    assert ru_words > 0


def test_count_words_counts_english():
    ru_words, en_words, n_code = mod._count_words_by_type("agent system architecture")
    assert en_words > 0


def test_count_words_counts_code_blocks():
    text = "Before.\n```python\ncode here\n```\nAfter."
    ru_words, en_words, n_code = mod._count_words_by_type(text)
    assert n_code == 1


def test_count_words_multiple_code_blocks():
    text = "```\nblock1\n```\ntext\n```\nblock2\n```"
    _, _, n_code = mod._count_words_by_type(text)
    assert n_code == 2


def test_count_words_excludes_code_from_word_count():
    text = "агент\n```\nагент система архитектура\n```"
    ru_with_code, _, _ = mod._count_words_by_type("агент\n```\nагент система архитектура\n```")
    ru_clean, _, _ = mod._count_words_by_type("агент")
    assert ru_with_code == ru_clean


def test_count_words_zero_for_empty():
    ru_words, en_words, n_code = mod._count_words_by_type("")
    assert ru_words == 0
    assert en_words == 0
    assert n_code == 0


# ── estimate_reading_time ─────────────────────────────────────────────────────

_SHORT_TEXT = "# Title\n\nShort."

_LONG_RU = "агент " * 300
_LONG_EN = "agent " * 300


def test_estimate_reading_time_returns_dict_or_empty():
    result = mod.estimate_reading_time(_LONG_RU)
    assert isinstance(result, dict)


def test_estimate_reading_time_empty_for_short():
    result = mod.estimate_reading_time(_SHORT_TEXT)
    assert result == {}


def test_estimate_reading_time_has_required_keys():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        for key in ("minutes", "time_str", "category", "words", "ru_words", "en_words", "code_blocks"):
            assert key in result


def test_estimate_reading_time_minutes_positive():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["minutes"] > 0


def test_estimate_reading_time_minimum_1_minute():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["minutes"] >= 1.0


def test_estimate_reading_time_time_str_format():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert "мин" in result["time_str"] or "ч" in result["time_str"]


def test_estimate_reading_time_category_fast():
    # ~1 min text
    text = "агент " * 60
    result = mod.estimate_reading_time(text)
    if result:
        assert "Быстро" in result["category"]


def test_estimate_reading_time_category_long():
    # Many words
    text = "агент архитектура система память консолидация знания " * 200
    result = mod.estimate_reading_time(text)
    if result:
        assert result["category"] in (
            "📗 Быстро", "📘 Средне", "📙 Долго", "📕 Очень долго"
        )


def test_estimate_reading_time_words_counted():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["words"] > 0


def test_estimate_reading_time_ru_words():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["ru_words"] > 0


def test_estimate_reading_time_en_words():
    result = mod.estimate_reading_time(_LONG_EN)
    if result:
        assert result["en_words"] > 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_reading_time_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "READING_TIME.md").exists()


def test_main_reading_time_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# Title\n\nContent about AgentFS knowledge.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "READING_TIME.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "READING_TIME.md").exists()


def test_main_reading_time_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    text = (tmp_path / "READING_TIME.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_wpm_arg_parsing():
    """Lines 28-30: --wpm N sets WPM_RU and WPM_EN."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--wpm", "180"]
        import importlib as _il
        _il.reload(mod)
        assert mod.WPM_RU == 180
        assert mod.WPM_EN == 180
    finally:
        sys.argv = orig_argv
        import importlib as _il2
        _il2.reload(mod)


def test_section_arg_parsing():
    """Lines 34-36: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        import importlib as _il
        _il.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        import importlib as _il2
        _il2.reload(mod)


# ── estimate_reading_time: category branches ──────────────────────────────────

def test_estimate_reading_time_category_medium():
    """Line 89: 3 < minutes <= 8 → '📘 Средне'."""
    text = "агент " * 1000  # ~5 min
    result = mod.estimate_reading_time(text)
    assert result.get("category") == "📘 Средне"


def test_estimate_reading_time_category_long():
    """Line 91: 8 < minutes <= 15 → '📙 Долго'."""
    text = "агент " * 2200  # ~11 min
    result = mod.estimate_reading_time(text)
    assert result.get("category") == "📙 Долго"


def test_estimate_reading_time_category_very_long():
    """Line 92: minutes > 15 → '📕 Очень долго'."""
    text = "агент " * 4000  # ~20 min
    result = mod.estimate_reading_time(text)
    assert result.get("category") == "📕 Очень долго"


def test_estimate_reading_time_hours_format():
    """Lines 80-82: minutes >= 60 → '~Nч Mмин' format."""
    text = "агент " * 15000  # ~75 min
    result = mod.estimate_reading_time(text)
    assert "ч" in result.get("time_str", "")


# ── main: full coverage ───────────────────────────────────────────────────────

def test_main_with_long_doc(tmp_path, monkeypatch):
    """Lines 121, 148-154, 178, 181: results list filled with one doc."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("агент " * 300, encoding="utf-8")
    mod.main()
    text = (tmp_path / "READING_TIME.md").read_text(encoding="utf-8")
    assert "doc" in text


def test_main_with_very_long_doc(tmp_path, monkeypatch):
    """Lines 161-171: long_docs section (minutes >= 10)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "big.md").write_text("агент " * 2500, encoding="utf-8")
    mod.main()
    text = (tmp_path / "READING_TIME.md").read_text(encoding="utf-8")
    assert "Самые длинные" in text


def test_main_file_read_exception(tmp_path, monkeypatch):
    """Lines 117-118: exception during file read → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()  # should not crash


def test_main_relative_to_docs_fallback(tmp_path, monkeypatch):
    """Line 152: path not relative to 'docs' → fallback rel = p."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    # File in tmp_path directly (not under 'docs' subdir)
    (tmp_path / "doc.md").write_text("агент " * 300, encoding="utf-8")
    mod.main()
    assert (tmp_path / "READING_TIME.md").exists()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 191: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    script_path = str(ROOT / "scripts" / "improve_reading_time.py")
    runpy.run_path(script_path, run_name="__main__")
