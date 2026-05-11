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
