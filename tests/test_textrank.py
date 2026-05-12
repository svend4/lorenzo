"""
Тесты для scripts/improve_textrank.py.

Покрытие:
  - _tokenize()       — токенизация с фильтрацией стоп-слов
  - _split_sentences() — разбивка текста на предложения
  - textrank()        — PageRank-алгоритм на предложениях
  - summarize_file()  — суммаризация файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_textrank")


# ── _tokenize ─────────────────────────────────────────────────────────────────

def test_tokenize_returns_set():
    result = mod._tokenize("агент архитектура память")
    assert isinstance(result, set)


def test_tokenize_lowercases():
    result = mod._tokenize("АГЕНТ АРХИТЕКТУРА")
    assert "агент" in result
    assert "архитектура" in result


def test_tokenize_min_length_3():
    result = mod._tokenize("аб абв агент")
    for t in result:
        assert len(t) >= 3


def test_tokenize_filters_stopwords():
    result = mod._tokenize("и в не на с по к из за для")
    assert len(result) == 0


def test_tokenize_handles_english():
    result = mod._tokenize("agent memory architecture")
    assert "agent" in result
    assert "memory" in result


def test_tokenize_empty():
    result = mod._tokenize("")
    assert result == set()


# ── _split_sentences ──────────────────────────────────────────────────────────

def test_split_sentences_returns_list():
    text = "Первое предложение. Второе предложение."
    result = mod._split_sentences(text)
    assert isinstance(result, list)


def test_split_sentences_splits_on_period():
    text = ("Агент обрабатывает данные из входного потока запросов пользователей. "
            "Система отвечает на запросы пользователей через интерфейс памяти.")
    result = mod._split_sentences(text)
    assert len(result) >= 1


def test_split_sentences_filters_short():
    text = "A. B. Длинное предложение с более чем восемью токенами содержания системы."
    result = mod._split_sentences(text)
    for s in result:
        assert len(s.split()) >= 8


def test_split_sentences_empty():
    result = mod._split_sentences("")
    assert result == []


def test_split_sentences_removes_code_blocks():
    text = "```python\ncode\n```\nАгент обрабатывает запросы через интерфейс памяти системы."
    result = mod._split_sentences(text)
    for s in result:
        assert "code" not in s


# ── textrank ──────────────────────────────────────────────────────────────────

_SENTENCES = [
    "Агент обрабатывает информацию через систему памяти и консолидирует знания.",
    "Система хранения использует граф для связей между понятиями архитектуры.",
    "Память агента основана на BM25-поиске и семантическом индексировании документов.",
    "Ретривер возвращает релевантные фрагменты из базы знаний через гибридный поиск.",
    "Оркестратор управляет несколькими агентами через декларативный YAML-интерфейс.",
    "Архитектура построена на принципах local-first с поддержкой CRDT-синхронизации.",
    "Интеграция с MCP-сервером обеспечивает подключение через OpenAI-совместимый API.",
]


def test_textrank_returns_list():
    result = mod.textrank(_SENTENCES, n=3)
    assert isinstance(result, list)


def test_textrank_returns_n_sentences():
    result = mod.textrank(_SENTENCES, n=3)
    assert len(result) == 3


def test_textrank_returns_subset():
    result = mod.textrank(_SENTENCES, n=3)
    for sent in result:
        assert sent in _SENTENCES


def test_textrank_fewer_sentences_than_n():
    short = _SENTENCES[:2]
    result = mod.textrank(short, n=5)
    assert result == short


def test_textrank_n_equals_length():
    result = mod.textrank(_SENTENCES[:3], n=3)
    assert result == _SENTENCES[:3]


def test_textrank_with_query():
    result = mod.textrank(_SENTENCES, n=3, query="память агент консолидация")
    assert isinstance(result, list)
    assert len(result) == 3


def test_textrank_preserves_order():
    result = mod.textrank(_SENTENCES, n=3)
    indices = [_SENTENCES.index(s) for s in result]
    assert indices == sorted(indices)


def test_textrank_empty_sentences():
    result = mod.textrank([], n=3)
    assert result == []


# ── summarize_file ────────────────────────────────────────────────────────────

def test_summarize_file_returns_dict_or_none(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nShort text.", encoding="utf-8")
    result = mod.summarize_file(f)
    assert result is None or isinstance(result, dict)


def test_summarize_file_short_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nToo short.", encoding="utf-8")
    result = mod.summarize_file(f)
    assert result is None


def test_summarize_file_long_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    content = "# Knowledge System\n\n"
    content += " ".join([
        "Агент обрабатывает информацию через систему памяти и консолидирует знания для ответов.",
        "Система хранения использует граф для связей между понятиями и концепциями архитектуры.",
        "Память агента основана на BM25-поиске и семантическом индексировании всех документов.",
        "Ретривер возвращает релевантные фрагменты из базы знаний через гибридный поиск данных.",
        "Оркестратор управляет несколькими агентами через декларативный YAML-интерфейс системы.",
        "Архитектура построена на принципах local-first с поддержкой CRDT-синхронизации данных.",
        "Интеграция с MCP-сервером обеспечивает подключение через OpenAI-совместимый API запросов.",
        "Поисковый индекс содержит более двух тысяч документов для быстрого поиска информации.",
    ] * 3) + "\n"
    f.write_text(content, encoding="utf-8")
    result = mod.summarize_file(f)
    assert result is not None
    assert isinstance(result, dict)


def test_summarize_file_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    content = "# Knowledge System\n\n"
    content += " ".join([
        "Агент обрабатывает информацию через систему памяти и консолидирует знания для ответов.",
        "Система хранения использует граф для связей между понятиями и концепциями архитектуры.",
        "Память агента основана на BM25-поиске и семантическом индексировании всех документов.",
        "Ретривер возвращает релевантные фрагменты из базы знаний через гибридный поиск данных.",
        "Оркестратор управляет несколькими агентами через декларативный YAML-интерфейс системы.",
        "Архитектура построена на принципах local-first с поддержкой CRDT-синхронизации данных.",
    ] * 5) + "\n"
    f.write_text(content, encoding="utf-8")
    result = mod.summarize_file(f)
    if result is not None:
        for key in ("file", "title", "summary", "sentences", "total_sents"):
            assert key in result


def test_summarize_file_title_extracted(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    content = "# My Special Title\n\n"
    content += " ".join([
        "Агент обрабатывает информацию через систему памяти и консолидирует знания для ответов.",
        "Система хранения использует граф для связей между понятиями и концепциями архитектуры.",
        "Память агента основана на BM25-поиске и семантическом индексировании всех документов.",
        "Ретривер возвращает релевантные фрагменты из базы знаний через гибридный поиск данных.",
        "Оркестратор управляет несколькими агентами через декларативный YAML-интерфейс системы.",
    ] * 5) + "\n"
    f.write_text(content, encoding="utf-8")
    result = mod.summarize_file(f)
    if result is not None:
        assert result["title"] == "My Special Title"


def test_summarize_file_missing_file_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "nonexistent.md"
    result = mod.summarize_file(f)
    assert result is None


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_summaries_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    mod.main()
    assert (tmp_path / "SUMMARIES.md").exists()


def test_main_summaries_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    (tmp_path / "doc.md").write_text(
        "# AgentFS\n\nContent about knowledge storage system.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "SUMMARIES.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    mod.main()
    assert (tmp_path / "SUMMARIES.md").exists()


def test_main_summaries_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    mod.main()
    text = (tmp_path / "SUMMARIES.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── module-level arg parsing ───────────────────────────────────────────────────

def test_sentences_arg_parsing():
    """Lines 33-35: --sentences N sets SENTENCES."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--sentences", "5"]
        importlib.reload(mod)
        assert mod.SENTENCES == 5
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_query_arg_parsing():
    """Lines 39-41: --query TEXT sets QUERY."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--query", "agent memory"]
        importlib.reload(mod)
        assert mod.QUERY == "agent memory"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 45-47: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
        assert "01-svyazi" in str(mod.SECTION_FILTER)
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _jaccard and _query_boost edge cases ──────────────────────────────────────

def test_jaccard_empty_first():
    """Line 89: not a → return 0.0."""
    result = mod._jaccard(set(), {"word"})
    assert result == 0.0


def test_jaccard_empty_second():
    """Line 89: not b → return 0.0."""
    result = mod._jaccard({"word"}, set())
    assert result == 0.0


def test_query_boost_empty_query():
    """Line 95: not query_tokens → return 0.0."""
    result = mod._query_boost({"agent", "memory"}, set())
    assert result == 0.0


# ── summarize_file edge cases ─────────────────────────────────────────────────

def test_summarize_file_too_few_sentences_returns_none(tmp_path, monkeypatch):
    """Line 154: len(sents) < 3 → return None."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "short_sents.md"
    # Write text with enough words but too few valid sentences (< 8 words each)
    content = "# Title\n\n" + "word " * 200 + "\n"
    f.write_text(content, encoding="utf-8")
    # Monkeypatch _split_sentences to return only 2 sentences
    monkeypatch.setattr(mod, "_split_sentences", lambda text: ["one", "two"])
    result = mod.summarize_file(f)
    assert result is None


# ── _insert_summary ────────────────────────────────────────────────────────────

_LONG_TEXT = "# Knowledge Agent\n\n" + "word " * 200

def test_insert_summary_adds_block(tmp_path, monkeypatch):
    """Lines 169-201: _insert_summary adds block to file without marker."""
    f = tmp_path / "doc.md"
    f.write_text(_LONG_TEXT, encoding="utf-8")
    sents = ["First summary sentence about agent systems.",
             "Second summary about memory architecture.",
             "Third about search and retrieval systems."]
    result = mod._insert_summary(f, sents)
    assert result is True
    content = f.read_text(encoding="utf-8")
    assert mod.SUMMARY_MARKER in content


def test_insert_summary_updates_existing_block(tmp_path, monkeypatch):
    """Lines 184-191: SUMMARY_MARKER already in text → replace."""
    marker = mod.SUMMARY_MARKER
    old_text = f"# Title\n\n{marker}\n> **Резюме** (TextRank)\n>\n> Old sentence.\n>\n\nOther content."
    f = tmp_path / "doc.md"
    f.write_text(old_text, encoding="utf-8")
    sents = ["New summary sentence here for testing purposes."]
    result = mod._insert_summary(f, sents)
    content = f.read_text(encoding="utf-8")
    assert "New summary" in content


def test_insert_summary_read_exception_returns_false(tmp_path, monkeypatch):
    """Lines 169-172: exception reading file → return False."""
    f = tmp_path / "bad.md"
    f.write_text("content", encoding="utf-8")
    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == f:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    result = mod._insert_summary(f, ["sentence"])
    assert result is False


def test_insert_summary_no_heading_prepends(tmp_path):
    """Line 198: no heading → prepend block."""
    f = tmp_path / "doc.md"
    content = "word " * 20
    f.write_text(content, encoding="utf-8")
    sents = ["Summary sentence about agent systems for testing."]
    mod._insert_summary(f, sents)
    result = f.read_text(encoding="utf-8")
    assert mod.SUMMARY_MARKER in result


# ── main with APPLY and QUERY ──────────────────────────────────────────────────

_RICH_TEXT = ("# Knowledge System\n\n"
              "Агент обрабатывает информацию через систему памяти и консолидирует знания. "
              "Система хранения использует граф для связей между понятиями архитектуры. "
              "Память агента основана на BM25-поиске и семантическом индексировании документов. "
              "Ретривер возвращает релевантные фрагменты из базы знаний через гибридный поиск. "
              "Оркестратор управляет несколькими агентами через декларативный YAML-интерфейс. "
              "Архитектура построена на принципах local-first с поддержкой CRDT-синхронизации. "
              "Интеграция с MCP-сервером обеспечивает подключение через OpenAI-совместимый API. "
              ) * 5


def test_main_with_query(tmp_path, monkeypatch):
    """Lines 208, 236: QUERY set → printed in header and in report."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "QUERY", "agent memory")
    (tmp_path / "doc.md").write_text(_RICH_TEXT, encoding="utf-8")
    mod.main()
    text = (tmp_path / "SUMMARIES.md").read_text(encoding="utf-8")
    assert "agent memory" in text or "Фокус" in text


def test_main_apply_mode(tmp_path, monkeypatch):
    """Lines 223-226, 249: APPLY=True → _insert_summary called."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "QUERY", None)
    (tmp_path / "doc.md").write_text(_RICH_TEXT, encoding="utf-8")
    mod.main()
    content = (tmp_path / "doc.md").read_text(encoding="utf-8")
    assert mod.SUMMARY_MARKER in content


def test_main_results_loop_written(tmp_path, monkeypatch):
    """Lines 238-243: results loop writes entries to SUMMARIES.md."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "QUERY", None)
    (tmp_path / "doc.md").write_text(_RICH_TEXT, encoding="utf-8")
    mod.main()
    text = (tmp_path / "SUMMARIES.md").read_text(encoding="utf-8")
    assert "##" in text


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 255: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "QUERY", None)
    script_path = str(ROOT / "scripts" / "improve_textrank.py")
    runpy.run_path(script_path, run_name="__main__")
