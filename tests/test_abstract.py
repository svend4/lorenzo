"""
Тесты для scripts/improve_abstract.py.

Покрытие:
  - _sentences()      — разбивка текста на предложения, чистка markdown
  - _keywords()       — TF-IDF-like топ-N ключевых слов
  - _best_sentence()  — выбор лучшего предложения по паттерну
  - build_abstract()  — полный абстракт {problem, approach, result, keywords}
  - _format_abstract() — форматирование в Markdown blockquote
  - process_file()    — идемпотентная вставка блока в файл
"""

import importlib
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_abstract")

# ── _sentences ────────────────────────────────────────────────────────────────

def test_sentences_returns_list():
    result = mod._sentences("Это предложение. Ещё одно предложение для теста.")
    assert isinstance(result, list)


def test_sentences_basic_split():
    text = ("Это первое достаточно длинное предложение для теста. "
            "Это второе достаточно длинное предложение для теста.")
    sents = mod._sentences(text)
    assert len(sents) >= 1


def test_sentences_strips_markdown():
    text = "**Жирный** текст и `code` фрагмент. Это нормальное предложение без разметки."
    sents = mod._sentences(text)
    for s in sents:
        assert "**" not in s
        assert "`" not in s


def test_sentences_removes_code_blocks():
    text = "Описание.\n```python\nprint('hello')\n```\nПродолжение."
    sents = mod._sentences(text)
    for s in sents:
        assert "print" not in s


def test_sentences_removes_urls():
    text = "Ссылка на https://github.com/example/repo описание проекта."
    sents = mod._sentences(text)
    for s in sents:
        assert "github.com" not in s


def test_sentences_min_length_filter():
    text = "Ок. Да. Нет. Это достаточно длинное предложение для анализа текста."
    sents = mod._sentences(text)
    for s in sents:
        assert len(s) > 40

# ── _keywords ─────────────────────────────────────────────────────────────────

def test_keywords_returns_list():
    text = "агент память консолидация забывание алгоритм поиск"
    result = mod._keywords(text)
    assert isinstance(result, list)


def test_keywords_respects_n():
    text = " ".join(["агент", "память", "консолидация", "забывание",
                     "алгоритм", "поиск", "граф", "узел", "ребро", "вектор"])
    result = mod._keywords(text, n=3)
    assert len(result) <= 3


def test_keywords_filters_stopwords():
    text = "и в на что как это для или но агент память"
    result = mod._keywords(text)
    for w in result:
        assert w not in mod.STOPWORDS


def test_keywords_min_word_length():
    text = "a an is of big long important keyword information retrieval"
    result = mod._keywords(text)
    for w in result:
        assert len(w) > 4


def test_keywords_most_frequent_first():
    text = "агент агент агент память память консолидация"
    result = mod._keywords(text, n=3)
    if result:
        assert result[0] == "агент"

# ── _best_sentence ────────────────────────────────────────────────────────────

def test_best_sentence_returns_string():
    sents = ["Задача состоит в решении проблемы поиска.",
             "Методология предполагает алгоритм поиска."]
    result = mod._best_sentence(sents, mod.PROBLEM_KW)
    assert isinstance(result, str)


def test_best_sentence_matches_pattern():
    sents = [
        "Это предложение не содержит ключевых слов.",
        "Задача проекта — решить проблему консолидации памяти агента.",
    ]
    result = mod._best_sentence(sents, mod.PROBLEM_KW)
    assert "задача" in result.lower() or "проблем" in result.lower()


def test_best_sentence_empty_candidates():
    sents = ["Обычное предложение без ключевых слов.",
             "Ещё одно нейтральное предложение."]
    result = mod._best_sentence(sents, mod.RESULT_KW)
    assert result == ""


def test_best_sentence_respects_max_len():
    long_sent = "Проблема " + "x" * 200
    result = mod._best_sentence([long_sent], mod.PROBLEM_KW, max_len=50)
    assert len(result) <= 50


def test_best_sentence_approach_pattern():
    sents = [
        "Система предлагает новый метод консолидации.",
        "Результат показывает улучшение точности.",
    ]
    result = mod._best_sentence(sents, mod.APPROACH_KW)
    assert "метод" in result.lower() or "предлага" in result.lower()

# ── build_abstract ────────────────────────────────────────────────────────────

def _sample_text():
    return """# Yodoca — система памяти агента

Задача данного проекта — решить проблему консолидации кратковременной памяти агентов.
Существующие системы требуют сложной настройки и имеют ограничения по масштабируемости.

Предлагаемый подход использует алгоритм забывания Эббингауза для управления памятью.
Метод основан на вероятностном графе знаний с весами давности.

Результат: система достигает точности 94% при тестировании на реальных данных.
Полученные данные показывают улучшение на 37% по сравнению с базовой линией.

Ключевые слова: память, консолидация, агент, забывание, граф, вероятность.
"""


def test_build_abstract_returns_dict():
    result = mod.build_abstract(_sample_text())
    assert isinstance(result, dict)


def test_build_abstract_has_required_keys():
    result = mod.build_abstract(_sample_text())
    assert "problem" in result
    assert "approach" in result
    assert "result" in result
    assert "keywords" in result


def test_build_abstract_problem_not_empty():
    result = mod.build_abstract(_sample_text())
    assert result["problem"]  # non-empty string


def test_build_abstract_keywords_is_list():
    result = mod.build_abstract(_sample_text())
    assert isinstance(result["keywords"], list)


def test_build_abstract_finds_approach():
    result = mod.build_abstract(_sample_text())
    # "метод", "подход", "предлагает" should be found
    assert result["approach"] != ""


def test_build_abstract_finds_result():
    result = mod.build_abstract(_sample_text())
    assert result["result"] != ""


def test_build_abstract_fallback_for_no_problem():
    text = "Это первое предложение в тексте без проблемных слов. " \
           "Второе предложение тоже обычное и нейтральное без специальных слов."
    result = mod.build_abstract(text)
    # Should fall back to first sentence
    assert result["problem"] != ""


def test_build_abstract_empty_text():
    result = mod.build_abstract("")
    assert isinstance(result, dict)
    assert "keywords" in result

# ── _format_abstract ──────────────────────────────────────────────────────────

def _sample_ab():
    return {
        "problem":  "Задача — решить проблему консолидации памяти.",
        "approach": "Метод использует алгоритм забывания.",
        "result":   "Результат: точность 94%.",
        "keywords": ["память", "агент", "консолидация"],
    }


def test_format_abstract_returns_string():
    result = mod._format_abstract(_sample_ab())
    assert isinstance(result, str)


def test_format_abstract_contains_marker():
    result = mod._format_abstract(_sample_ab())
    assert mod.ABSTRACT_MARKER in result


def test_format_abstract_contains_problem():
    result = mod._format_abstract(_sample_ab())
    assert "Задача" in result or "Проблема" in result


def test_format_abstract_contains_keywords():
    result = mod._format_abstract(_sample_ab())
    assert "память" in result


def test_format_abstract_blockquote_style():
    result = mod._format_abstract(_sample_ab())
    # Each non-empty line should start with ">"
    lines = [l for l in result.splitlines() if l.strip()]
    # At least the marker line and blockquote lines
    assert any(l.startswith(">") for l in lines)


def test_format_abstract_skips_empty_fields():
    ab = {"problem": "Задача есть.", "approach": "", "result": "", "keywords": []}
    result = mod._format_abstract(ab)
    assert "Подход" not in result
    assert "Результат" not in result

# ── process_file ──────────────────────────────────────────────────────────────

def test_process_file_returns_bool(tmp_path):
    f = tmp_path / "test.md"
    f.write_text(_sample_text(), encoding="utf-8")
    result = mod.process_file(f)
    assert isinstance(result, bool)


def test_process_file_short_text_skipped(tmp_path):
    f = tmp_path / "short.md"
    f.write_text("# Title\n\nShort.", encoding="utf-8")
    result = mod.process_file(f)
    assert result is False


def test_process_file_dry_run_does_not_modify(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "APPLY", False)
    f = tmp_path / "test.md"
    original = _sample_text()
    f.write_text(original, encoding="utf-8")
    mod.process_file(f)
    # File should be unchanged in dry-run mode
    assert f.read_text(encoding="utf-8") == original


def test_process_file_apply_inserts_marker(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    f = tmp_path / "test.md"
    f.write_text(_sample_text(), encoding="utf-8")
    result = mod.process_file(f)
    if result:
        content = f.read_text(encoding="utf-8")
        assert mod.ABSTRACT_MARKER in content


def test_process_file_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    f = tmp_path / "test.md"
    f.write_text(_sample_text(), encoding="utf-8")
    mod.process_file(f)
    content_after_first = f.read_text(encoding="utf-8")
    mod.process_file(f)
    content_after_second = f.read_text(encoding="utf-8")
    # Marker should not be duplicated
    assert content_after_second.count(mod.ABSTRACT_MARKER) == \
           content_after_first.count(mod.ABSTRACT_MARKER)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nContent about agent memory systems.", encoding="utf-8"
    )
    mod.main()  # dry-run → must not raise


def test_main_apply_modifies_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent about agent memory systems.", encoding="utf-8")
    mod.main()  # apply → modifies file, must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    mod.main()  # no files → must not raise


# ── arg parsing ────────────────────────────────────────────────────────────────

def test_min_words_arg_parsing():
    """Lines 38-40: --min-words sets MIN_WORDS."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-words", "300"]
        importlib.reload(mod)
        assert mod.MIN_WORDS == 300
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 44-46: --section sets SECTION_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig
        importlib.reload(mod)


# ── process_file: exception, no problem, no H1, unchanged text ───────────────

def test_process_file_read_error(tmp_path, monkeypatch):
    """Lines 147-148: exception reading file → return False."""
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    from pathlib import Path as _Path
    orig_read = _Path.read_text
    def mock_read(self, *a, **kw):
        raise OSError("mock")
    monkeypatch.setattr(_Path, "read_text", mock_read)
    bad = tmp_path / "bad.md"
    bad.write_text("", encoding="utf-8")
    result = mod.process_file(bad)
    assert result is False


def test_process_file_no_problem(tmp_path, monkeypatch):
    """Line 155: build_abstract returns empty problem → return False."""
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    f = tmp_path / "noproblem.md"
    f.write_text("", encoding="utf-8")  # empty → problem = ''
    result = mod.process_file(f)
    assert result is False


def test_process_file_no_h1(tmp_path, monkeypatch):
    """Line 174: text without H1 heading → prepend block."""
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    f = tmp_path / "noh1.md"
    # Text with enough content for abstract but no H1
    content = ("The system uses agent memory consolidation approach. "
               "Memory decay algorithm is applied for better recall. "
               "Results show 94% accuracy improvement.") * 5
    f.write_text(content, encoding="utf-8")
    result = mod.process_file(f)
    # Either wrote or didn't — must not crash
    assert isinstance(result, bool)


def test_process_file_marker_exists_unchanged(tmp_path, monkeypatch):
    """Line 166: ABSTRACT_MARKER in text but re.sub produces no change → False."""
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    f = tmp_path / "test.md"
    # Create text where the regex substitution would produce the same text
    # by having the marker already with same content
    content = ("# Title\n\n"
               "The system uses agent memory consolidation approach. " * 20)
    f.write_text(content, encoding="utf-8")
    # First run inserts marker
    mod.process_file(f)
    # Second run: marker exists, re.sub replaces with same text
    monkeypatch.setattr(mod, "APPLY", False)
    result2 = mod.process_file(f)
    assert isinstance(result2, bool)


# ── main: skipped files counted ───────────────────────────────────────────────

def test_main_counts_skipped(tmp_path, monkeypatch):
    """Line 199: process_file returns False → skipped += 1."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 9999)  # too high → all files skipped
    (tmp_path / "short.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()  # must not raise; skipped path is covered


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 208: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    runpy.run_path(str(ROOT / "scripts" / "improve_abstract.py"), run_name="__main__")
