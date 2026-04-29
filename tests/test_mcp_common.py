"""Тесты для mcp_common.py — поиск, токенизация, кэш логов."""
import json
import tempfile
from pathlib import Path
from unittest import mock

from mcp_common import tokenize, doc_text, log_call, search


def test_tokenize_russian():
    tokens = tokenize("Это тест русского текста")
    assert 'тест' in tokens
    assert 'русского' in tokens
    assert 'текста' in tokens


def test_tokenize_english():
    tokens = tokenize("This is a test of english text")
    assert 'test' in tokens
    assert 'english' in tokens


def test_tokenize_stopwords():
    tokens = tokenize("the and a or но и")
    # стоп-слова отфильтрованы
    assert 'the' not in tokens
    assert 'и' not in tokens
    assert 'но' not in tokens


def test_doc_text_combines_fields():
    doc = {'content': 'main', 'preview': 'prev', 'summary': 'sum'}
    text = doc_text(doc)
    assert 'main' in text
    assert 'prev' in text
    assert 'sum' in text


def test_doc_text_handles_missing():
    doc = {'preview': 'only this'}
    text = doc_text(doc)
    assert 'only this' in text


def test_search_with_mock_index(monkeypatch):
    fake_index = [
        {'title': 'Yodoca memory', 'path': 'docs/memory.md',
         'tags': ['memory'], 'content': 'Yodoca implements hot path'},
        {'title': 'Other doc', 'path': 'docs/other.md',
         'tags': [], 'content': 'unrelated'},
    ]
    monkeypatch.setattr('mcp_common.load_search_index', lambda: fake_index)

    results = search('Yodoca', top_k=5)
    assert len(results) >= 1
    assert results[0]['title'] == 'Yodoca memory'


def test_log_call_writes_jsonl(tmp_path, monkeypatch):
    log_path = tmp_path / 'mcp_calls.jsonl'
    monkeypatch.setattr('mcp_common.LOG_PATH', log_path)

    log_call('lorenzo-search', 'search_docs', {'query': 'test'}, 42, 'ok')
    log_call('lorenzo-search', 'search_docs', {'query': 'b'}, 10, 'error')

    lines = log_path.read_text(encoding='utf-8').strip().splitlines()
    assert len(lines) == 2

    e1 = json.loads(lines[0])
    assert e1['server'] == 'lorenzo-search'
    assert e1['tool'] == 'search_docs'
    assert e1['duration_ms'] == 42
    assert e1['status'] == 'ok'
