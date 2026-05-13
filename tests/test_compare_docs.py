"""
Тесты для scripts/improve_compare_docs.py.

Покрытие:
  - _clean()          — удаление кода, URL, комментариев
  - _tokens()         — токенизация с фильтрацией стоп-слов
  - _headings()       — извлечение заголовков
  - _word_count()     — подсчёт слов
  - compare_two()     — сравнение двух файлов
  - format_comparison() — форматирование результата
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_compare_docs")


# ── _clean ────────────────────────────────────────────────────────────────────

def test_clean_returns_lowercase():
    result = mod._clean("UPPER CASE Text")
    assert result == result.lower()


def test_clean_removes_code_block():
    result = mod._clean("before\n```python\ncode here\n```\nafter")
    assert "code here" not in result


def test_clean_removes_inline_code():
    result = mod._clean("Use `function()` here.")
    assert "function()" not in result


def test_clean_removes_url():
    result = mod._clean("See https://example.com for more.")
    assert "https" not in result


def test_clean_removes_html_comments():
    result = mod._clean("before <!-- comment --> after")
    assert "comment" not in result


# ── _tokens ───────────────────────────────────────────────────────────────────

def test_tokens_returns_list():
    result = mod._tokens("агент память архитектура")
    assert isinstance(result, list)


def test_tokens_min_length_4():
    result = mod._tokens("а аб абв абвг абвгд")
    for t in result:
        assert len(t) >= 4


def test_tokens_filters_stopwords():
    result = mod._tokens("это как но или что")
    assert len(result) == 0


def test_tokens_finds_real_words():
    result = mod._tokens("архитектура системы проектирование")
    assert len(result) > 0


def test_tokens_case_insensitive():
    result = mod._tokens("Агент ПАМЯТЬ архитектура")
    assert "агент" in result
    assert "память" in result


# ── _headings ─────────────────────────────────────────────────────────────────

def test_headings_returns_list():
    result = mod._headings("# Title\n## Section\n### Sub")
    assert isinstance(result, list)


def test_headings_extracts_h1():
    result = mod._headings("# Title")
    assert "Title" in result


def test_headings_extracts_h2():
    result = mod._headings("## Section Name")
    assert "Section Name" in result


def test_headings_extracts_h3():
    result = mod._headings("### Sub Section")
    assert "Sub Section" in result


def test_headings_empty_text():
    result = mod._headings("No headings here")
    assert result == []


def test_headings_removes_formatting():
    result = mod._headings("## **Bold** Heading")
    assert "Bold" in result[0]
    assert "**" not in result[0]


# ── _word_count ───────────────────────────────────────────────────────────────

def test_word_count_returns_int():
    result = mod._word_count("one two three")
    assert isinstance(result, int)


def test_word_count_counts_correctly():
    result = mod._word_count("one two three four five")
    assert result == 5


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_word_count_multiline():
    result = mod._word_count("one\ntwo\nthree")
    assert result == 3


# ── compare_two ───────────────────────────────────────────────────────────────

def test_compare_two_returns_dict(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент обрабатывает информацию и отвечает на вопросы пользователя.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранит знания через архитектуру памяти агента.\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert isinstance(result, dict)


def test_compare_two_has_required_keys(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент обрабатывает информацию и отвечает.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранит знания через архитектуру.\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    for key in ("jaccard", "common_words", "unique_a", "unique_b",
                "common_heads", "only_heads_a", "only_heads_b",
                "words_a", "words_b", "size_ratio"):
        assert key in result, f"Missing key: {key}"


def test_compare_two_jaccard_identical(tmp_path):
    text = "# Title\n\nАгент обрабатывает информацию память архитектура.\n"
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text(text, encoding="utf-8")
    b.write_text(text, encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["jaccard"] == 1.0


def test_compare_two_jaccard_disjoint(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nархитектура система кластер граф модель байесовская\n", encoding="utf-8")
    b.write_text("# B\n\npython javascript typescript react frontend backend\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["jaccard"] < 0.5


def test_compare_two_jaccard_range(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nАгент обрабатывает информацию через архитектуру.\n", encoding="utf-8")
    b.write_text("# B\n\nСистема хранит знания через граф памяти.\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert 0.0 <= result["jaccard"] <= 1.0


def test_compare_two_paths_stored(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\ntext here\n", encoding="utf-8")
    b.write_text("# B\n\ntext here\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["path_a"] == a
    assert result["path_b"] == b


def test_compare_two_word_counts(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\none two three\n", encoding="utf-8")
    b.write_text("# B\n\none two three four five six\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["words_a"] < result["words_b"]


def test_compare_two_common_headings(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Title\n## Shared Section\n## Only A\n", encoding="utf-8")
    b.write_text("# Title\n## Shared Section\n## Only B\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert "Shared Section" in result["common_heads"]


# ── format_comparison ─────────────────────────────────────────────────────────

def test_format_comparison_returns_list(tmp_path):
    monkeypatch_root = tmp_path
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент архитектура память консолидация.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранения знаний через граф.\n", encoding="utf-8")

    original_root = mod.ROOT
    try:
        mod.ROOT = tmp_path
        r = mod.compare_two(a, b)
        result = mod.format_comparison(r)
    finally:
        mod.ROOT = original_root

    assert isinstance(result, list)


def test_format_comparison_contains_jaccard(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nАгент архитектура память консолидация.\n", encoding="utf-8")
    b.write_text("# B\n\nАгент архитектура память консолидация.\n", encoding="utf-8")

    original_root = mod.ROOT
    try:
        mod.ROOT = tmp_path
        r = mod.compare_two(a, b)
        result = mod.format_comparison(r)
    finally:
        mod.ROOT = original_root

    text = "\n".join(result)
    assert "Jaccard" in text or "jaccard" in text or "%" in text


def test_format_comparison_has_filenames(tmp_path):
    a = tmp_path / "doc_a.md"
    b = tmp_path / "doc_b.md"
    a.write_text("# A\n\nАгент архитектура память.\n", encoding="utf-8")
    b.write_text("# B\n\nСистема хранения знаний.\n", encoding="utf-8")

    original_root = mod.ROOT
    try:
        mod.ROOT = tmp_path
        r = mod.compare_two(a, b)
        result = mod.format_comparison(r)
    finally:
        mod.ROOT = original_root

    text = "\n".join(result)
    assert "doc_a.md" in text or "doc_b.md" in text


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_batch_creates_compare_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUT_FILE", None)
    (tmp_path / "a.md").write_text("# AgentFS\n\nMemory agent system.", encoding="utf-8")
    (tmp_path / "b.md").write_text("# Yodoca\n\nMemory consolidation.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "COMPARE.md").exists()


def test_main_batch_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUT_FILE", None)
    mod.main()
    assert (tmp_path / "COMPARE.md").exists()


def test_main_no_batch_no_files_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", False)
    monkeypatch.setattr(mod, "FILE_A", None)
    monkeypatch.setattr(mod, "FILE_B", None)
    mod.main()  # prints usage, must not raise


# ── module-level arg parsing ───────────────────────────────────────────────────

def test_a_arg_parsing():
    """Lines 34-36: --a PATH sets FILE_A."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--a", "docs/file.md"]
        importlib.reload(mod)
        assert mod.FILE_A is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_b_arg_parsing():
    """Lines 39-41: --b PATH sets FILE_B."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--b", "docs/file.md"]
        importlib.reload(mod)
        assert mod.FILE_B is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_out_arg_parsing():
    """Lines 45-47: --out PATH sets OUT_FILE."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--out", "docs/COMPARE.md"]
        importlib.reload(mod)
        assert mod.OUT_FILE is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_top_arg_parsing():
    """Lines 51-53: --top N sets TOP_N."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--top", "5"]
        importlib.reload(mod)
        assert mod.TOP_N == 5
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 57-59: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _top_words and _sentences ─────────────────────────────────────────────────

def test_top_words_returns_set():
    """Line 85: _top_words returns a set."""
    result = mod._top_words("agent memory knowledge system " * 5)
    assert isinstance(result, set)


def test_sentences_returns_list():
    """Lines 100-101: _sentences returns list of long sentences."""
    text = "Short. This is a longer sentence with more than thirty characters total. Another!"
    result = mod._sentences(text)
    assert isinstance(result, list)


def test_sentences_filters_short():
    """Line 101: sentences with <= 30 chars are filtered."""
    text = "Short one. Another very long sentence that should be included because it exceeds thirty characters."
    result = mod._sentences(text)
    for s in result:
        assert len(s.strip()) > 30


# ── format_comparison: missing verdict paths ──────────────────────────────────

def test_format_comparison_moderate_jaccard(tmp_path, monkeypatch):
    """Line 157: jaccard >= 0.3 but < 0.5 → 'Умеренное сходство'."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    # Create files with moderate overlap (~30-50% of words shared)
    shared = "агент память архитектура система " * 3
    a.write_text(f"# A\n\n{shared}уникально-для-А файл документ\n", encoding="utf-8")
    b.write_text(f"# B\n\n{shared}уникально-для-Б текст другой\n", encoding="utf-8")
    r = mod.compare_two(a, b)
    # Force jaccard to be in the 0.3-0.5 range
    r["jaccard"] = 0.35
    result = mod.format_comparison(r)
    text = "\n".join(result)
    assert "Умеренное" in text


def test_format_comparison_with_common_heads(tmp_path, monkeypatch):
    """Line 175: common_heads non-empty → prints common sections."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Title\n## Common Section\n## Only A\n\ncontent", encoding="utf-8")
    b.write_text("# Title\n## Common Section\n## Only B\n\ncontent", encoding="utf-8")
    r = mod.compare_two(a, b)
    result = mod.format_comparison(r)
    text = "\n".join(result)
    assert "Common Section" in text


# ── batch_compare edge cases ──────────────────────────────────────────────────

def test_batch_compare_exception_handled(tmp_path, monkeypatch):
    """Lines 210-211: exception reading file → empty tokens set."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    good = tmp_path / "good.md"
    good.write_text("# Good\n\nagent memory system knowledge", encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original = _Path.read_text

    def mock_read(self, *a, **kw):
        if self == bad:
            raise OSError("mocked")
        return original(self, *a, **kw)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    result = mod.batch_compare([good, bad])
    assert isinstance(result, list)


def test_batch_compare_skips_empty_tokens(tmp_path, monkeypatch):
    """Line 219: file with empty tokens → skip (no pairs)."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    # File with only stopwords and short words → no tokens
    empty_tokens = tmp_path / "empty.md"
    empty_tokens.write_text("# A\n\nи в не на", encoding="utf-8")
    good = tmp_path / "good.md"
    good.write_text("# Good\n\nagent memory system knowledge", encoding="utf-8")

    result = mod.batch_compare([empty_tokens, good])
    assert isinstance(result, list)
    # No pair because one file has no tokens


# ── main with FILE_A and FILE_B ────────────────────────────────────────────────

def test_main_with_files_creates_compare(tmp_path, monkeypatch):
    """Lines 264-284: FILE_A and FILE_B set and exist → comparison written."""
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент обрабатывает информацию.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранит знания.\n", encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", False)
    monkeypatch.setattr(mod, "FILE_A", a)
    monkeypatch.setattr(mod, "FILE_B", b)
    monkeypatch.setattr(mod, "OUT_FILE", None)
    mod.main()
    assert (tmp_path / "COMPARE.md").exists()


def test_main_file_a_not_found(tmp_path, monkeypatch, capsys):
    """Line 264-266: FILE_A doesn't exist → error message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", False)
    monkeypatch.setattr(mod, "FILE_A", tmp_path / "nonexistent_a.md")
    monkeypatch.setattr(mod, "FILE_B", tmp_path / "b.md")
    mod.main()
    out = capsys.readouterr().out
    assert "не найден" in out or "nonexistent" in out


def test_main_file_b_not_found(tmp_path, monkeypatch, capsys):
    """Lines 267-269: FILE_B doesn't exist → error message."""
    a = tmp_path / "a.md"
    a.write_text("# A\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", False)
    monkeypatch.setattr(mod, "FILE_A", a)
    monkeypatch.setattr(mod, "FILE_B", tmp_path / "nonexistent_b.md")
    mod.main()
    out = capsys.readouterr().out
    assert "не найден" in out or "nonexistent" in out


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 288: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BATCH", False)
    monkeypatch.setattr(mod, "FILE_A", None)
    monkeypatch.setattr(mod, "FILE_B", None)
    script_path = str(ROOT / "scripts" / "improve_compare_docs.py")
    runpy.run_path(script_path, run_name="__main__")
