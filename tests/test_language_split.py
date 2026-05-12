"""Tests for scripts/improve_language_split.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_language_split")


def test_clean_for_lang_returns_string():
    result = mod._clean_for_lang("some text")
    assert isinstance(result, str)


def test_clean_for_lang_removes_code():
    result = mod._clean_for_lang("Before\n```python\ncode\n```\nAfter")
    assert "code" not in result


def test_clean_for_lang_removes_urls():
    result = mod._clean_for_lang("See https://example.com for details.")
    assert "https" not in result


def test_lang_stats_returns_dict():
    result = mod._lang_stats("Hello world test")
    assert isinstance(result, dict)


def test_lang_stats_required_keys():
    result = mod._lang_stats("Hello world")
    for key in ("ru", "en", "total", "ru_ratio", "en_ratio", "label"):
        assert key in result


def test_lang_stats_empty():
    result = mod._lang_stats("")
    assert result["total"] == 0
    assert result["label"] == "empty"


def test_lang_stats_russian_text():
    result = mod._lang_stats("Привет мир тест данных проекта системы")
    assert result["label"] == "RU"
    assert result["ru_ratio"] > 0.7


def test_lang_stats_english_text():
    result = mod._lang_stats("Hello world test data project system analysis")
    assert result["label"] == "EN"
    assert result["en_ratio"] > 0.7


def test_lang_stats_mixed_text():
    ru_words = "Привет мир тест " * 5
    en_words = "Hello world test " * 5
    result = mod._lang_stats(ru_words + en_words)
    assert result["label"] == "MIX"


def test_lang_stats_counts_words():
    result = mod._lang_stats("hello world test")
    assert result["total"] >= 3
    assert result["en"] >= 3


def test_split_paragraphs_returns_tuple():
    result = mod._split_paragraphs_by_lang("Some text here")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_split_paragraphs_russian_stays_in_ru():
    ru_text = "Привет мир тест данных проекта системы анализа"
    ru_out, en_out = mod._split_paragraphs_by_lang(ru_text)
    assert len(ru_out) > 0


def test_split_paragraphs_english_goes_to_en():
    en_text = "Hello world this is English text and data"
    ru_out, en_out = mod._split_paragraphs_by_lang(en_text)
    assert len(en_out) > 0


def test_lang_stats_ratios_sum_to_at_most_one():
    result = mod._lang_stats("Mixed текст with some английские words")
    assert result["ru_ratio"] + result["en_ratio"] <= 1.0 + 0.01


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_language_stats_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    mod.main()
    assert (tmp_path / "LANGUAGE_STATS.md").exists()


def test_main_language_stats_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nAgentFS is a great knowledge system.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "LANGUAGE_STATS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    mod.main()
    assert (tmp_path / "LANGUAGE_STATS.md").exists()


def test_main_language_stats_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    mod.main()
    text = (tmp_path / "LANGUAGE_STATS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── _section_of edge cases ────────────────────────────────────────────────────

def test_section_of_file_directly_in_docs(tmp_path, monkeypatch):
    """Line 65 'root' branch: file directly in DOCS → 'root'."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "README.md"
    f.touch()
    result = mod._section_of(f)
    assert result == "root"


def test_section_of_unknown_outside_docs(tmp_path, monkeypatch):
    """Lines 66-67: file NOT under DOCS → ValueError → 'unknown'."""
    import tempfile
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    other = Path(tempfile.mkdtemp()) / "file.md"
    result = mod._section_of(other)
    assert result == "unknown"


# ── _lang_stats OTHER label ───────────────────────────────────────────────────

def test_lang_stats_other_label():
    """Line 97: mixed-script words (neither Cyrillic nor Latin) → OTHER."""
    # "аb" has Cyrillic 'а' + Latin 'b': matches word regex but neither pure-ru nor pure-en
    # 8 mixed-script words + 1 RU + 1 EN → ru_r=0.1, en_r=0.1 → OTHER
    mixed_text = " ".join(["аb"] * 8 + ["ру", "en"])
    result = mod._lang_stats(mixed_text)
    assert result["label"] == "OTHER"


# ── analyze_file ──────────────────────────────────────────────────────────────

def test_analyze_file_exception_returns_none(tmp_path, monkeypatch):
    """Lines 123-124: exception during read → returns None."""
    f = tmp_path / "bad.md"
    f.write_text("content", encoding="utf-8")
    original_read = Path.read_text
    def mock_read(self, *args, **kwargs):
        if self == f:
            raise OSError("permission denied")
        return original_read(self, *args, **kwargs)
    monkeypatch.setattr(Path, "read_text", mock_read)
    result = mod.analyze_file(f)
    assert result is None


def test_analyze_file_valid_returns_dict(tmp_path, monkeypatch):
    """Lines 128-137: file with >= 20 words → returns stats dict."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    # 30 Russian words to ensure >= 20 qualifying words
    text = "Привет мир тест данных проекта системы агент память база граф " * 3
    f.write_text(text, encoding="utf-8")
    result = mod.analyze_file(f)
    assert result is not None
    assert "label" in result
    assert "file" in result


def test_analyze_file_few_words_returns_none(tmp_path, monkeypatch):
    """Lines 126-127: fewer than 20 words → returns None."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "short.md"
    f.write_text("Привет мир тест.", encoding="utf-8")
    result = mod.analyze_file(f)
    assert result is None


# ── main with rich content ────────────────────────────────────────────────────

RU_TEXT = "Привет мир тест данных проекта системы агент память база граф " * 4
EN_TEXT = "Hello world test data project system agent memory database graph " * 4
MIX_TEXT = ("Привет world тест data проекта system " * 5 + "агент memory база graph " * 5)


def test_main_with_ru_files_creates_section_stats(tmp_path, monkeypatch):
    """Lines 155, 203-211: files with enough words → section_stats populated."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "doc.md").write_text(RU_TEXT, encoding="utf-8")
    mod.main()
    text = (tmp_path / "LANGUAGE_STATS.md").read_text(encoding="utf-8")
    assert "По секциям" in text


def test_main_with_unexpected_language(tmp_path, monkeypatch):
    """Lines 178-185: EN file in RU section → unexpected section rendered."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "english.md").write_text(EN_TEXT, encoding="utf-8")
    mod.main()
    text = (tmp_path / "LANGUAGE_STATS.md").read_text(encoding="utf-8")
    assert "неожиданным" in text or "LANGUAGE_STATS" in text


def test_main_with_mix_files(tmp_path, monkeypatch):
    """Lines 192-199: MIX file → MIX section rendered."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "mixed.md").write_text(MIX_TEXT, encoding="utf-8")
    mod.main()
    text = (tmp_path / "LANGUAGE_STATS.md").read_text(encoding="utf-8")
    assert "MIX" in text or "Смешанные" in text


def test_main_split_mode_creates_files(tmp_path, monkeypatch):
    """Lines 218-231: SPLIT_MODE=True creates .ru.md and .en.md files."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", True)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    (section / "mixed.md").write_text(MIX_TEXT, encoding="utf-8")
    mod.main()
    # Check that split files were created
    ru_file = section / "mixed.ru.md"
    en_file = section / "mixed.en.md"
    assert ru_file.exists() or en_file.exists()


def test_main_split_mode_creates_ru_file(tmp_path, monkeypatch):
    """Line 227: ru.md written when ru_text is non-empty (RU-dominant paragraph)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", True)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    # Two separate paragraphs: one RU-dominant, one EN-dominant → MIX file
    ru_para = "Привет мир тест данных проекта системы агент память " * 3
    en_para = "Hello world test data project system agent memory " * 3
    mix_with_paras = f"{ru_para}\n\n{en_para}\n\n{ru_para}\n\n{en_para}"
    (section / "bilingual.md").write_text(mix_with_paras, encoding="utf-8")
    mod.main()
    ru_file = section / "bilingual.ru.md"
    assert ru_file.exists()


def test_main_split_mode_exception_on_read(tmp_path, monkeypatch):
    """Lines 222-223: exception during read_text in split loop → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", True)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    ru_para = "Привет мир тест данных проекта системы агент память " * 3
    en_para = "Hello world test data project system agent memory " * 3
    mix_with_paras = f"{ru_para}\n\n{en_para}\n\n{ru_para}\n\n{en_para}"
    target_file = section / "bilingual.md"
    target_file.write_text(mix_with_paras, encoding="utf-8")

    call_count = [0]
    original_read = Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == target_file:
            call_count[0] += 1
            if call_count[0] > 1:  # fail on 2nd call (inside split loop)
                raise OSError("mocked read error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", mock_read)
    mod.main()  # should not crash despite the exception


# ── module-level arg parsing (requires reload) ────────────────────────────────

def test_min_mix_arg_parsing():
    """Lines 35-37: --min-mix N sets MIN_MIX."""
    import sys, importlib
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-mix", "0.3"]
        importlib.reload(mod)
        assert abs(mod.MIN_MIX - 0.3) < 0.001
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_filter_arg_parsing(tmp_path):
    """Lines 41-43: --section NAME sets SECTION_FILTER."""
    import sys, importlib
    orig_argv = sys.argv[:]
    orig_docs = mod.DOCS
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
        assert "01-svyazi" in str(mod.SECTION_FILTER)
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 235: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "SPLIT_MODE", False)
    script_path = str(ROOT / "scripts" / "improve_language_split.py")
    runpy.run_path(script_path, run_name="__main__")
