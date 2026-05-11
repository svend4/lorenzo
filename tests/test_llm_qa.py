"""
Тесты для scripts/improve_llm_qa.py.

Покрытие:
  - tokenize_query()       — токенизация и фильтрация стоп-слов
  - score_doc()            — скоринг документа по токенам запроса
  - find_relevant()        — топ-k поиск по индексу
  - build_context()        — сборка контекста из документов
  - _cache_key()           — MD5-ключ кэша
  - get_cached/put_cached  — операции с кэш-словарём
  - load_index()           — чтение search_index.json
  - extract_questions_from_md() — извлечение вопросов из QUESTIONS.md
"""

import importlib
import sys
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_qa")

# ── tokenize_query ────────────────────────────────────────────────────────────

def test_tokenize_query_returns_list():
    result = mod.tokenize_query("Что такое агент с памятью?")
    assert isinstance(result, list)


def test_tokenize_query_removes_stopwords():
    result = mod.tokenize_query("что это такое и как это работает")
    assert "что" not in result
    assert "и" not in result
    assert "как" not in result
    assert "это" not in result


def test_tokenize_query_keeps_content_words():
    result = mod.tokenize_query("агент память консолидация")
    assert "агент" in result
    assert "память" in result
    assert "консолидация" in result


def test_tokenize_query_lowercases():
    result = mod.tokenize_query("AgentFS Память")
    # Tokens are lowercased by re.findall(..., query.lower())
    joined = " ".join(result)
    assert "agentfs" in joined or "память" in joined


def test_tokenize_query_empty():
    result = mod.tokenize_query("")
    assert result == []


def test_tokenize_query_only_stopwords():
    result = mod.tokenize_query("и в на что как")
    assert result == []


def test_tokenize_query_min_length():
    # Words < 2 chars after first char should not match ([а-яёa-z][а-яёa-z\-]{1,})
    result = mod.tokenize_query("я и в")
    assert result == []

# ── score_doc ─────────────────────────────────────────────────────────────────

def _make_doc(**kwargs):
    defaults = {
        "title": "Test Document",
        "path": "docs/test.md",
        "content": "Some content about agents and memory systems.",
        "preview": "",
        "tags": [],
    }
    defaults.update(kwargs)
    return defaults


def test_score_doc_zero_no_match():
    doc = _make_doc(title="Rufler", content="YAML orchestration declarative")
    score = mod.score_doc(doc, ["память", "консолидация"])
    assert score == 0.0


def test_score_doc_title_boost():
    doc_title = _make_doc(title="память агент", content="some other text")
    doc_body  = _make_doc(title="other doc", content="память агент системы")
    score_title = mod.score_doc(doc_title, ["память"])
    score_body  = mod.score_doc(doc_body,  ["память"])
    assert score_title > score_body


def test_score_doc_positive_body_match():
    doc = _make_doc(content="агент с памятью и консолидацией данных")
    score = mod.score_doc(doc, ["агент", "память"])
    assert score > 0


def test_score_doc_tags_boost():
    doc_tagged = _make_doc(tags=["memory", "agent"], content="some text")
    doc_plain  = _make_doc(tags=[], content="some text")
    score_tagged = mod.score_doc(doc_tagged, ["memory"])
    score_plain  = mod.score_doc(doc_plain,  ["memory"])
    assert score_tagged > score_plain


def test_score_doc_path_boost():
    doc_path  = _make_doc(path="docs/memory/yodoca.md", content="other content")
    doc_other = _make_doc(path="docs/knowledge/agentfs.md", content="other content")
    score_path  = mod.score_doc(doc_path,  ["memory"])
    score_other = mod.score_doc(doc_other, ["memory"])
    assert score_path > score_other


def test_score_doc_multiple_occurrences_higher():
    doc_many = _make_doc(content="агент агент агент агент")
    doc_one  = _make_doc(content="агент")
    score_many = mod.score_doc(doc_many, ["агент"])
    score_one  = mod.score_doc(doc_one,  ["агент"])
    assert score_many > score_one

# ── find_relevant ─────────────────────────────────────────────────────────────

def _sample_index():
    return [
        {"title": "Yodoca Memory", "path": "docs/yodoca.md",
         "content": "память консолидация агент decay", "tags": ["memory"]},
        {"title": "Rufler YAML", "path": "docs/rufler.md",
         "content": "yaml оркестрация декларативный агент", "tags": ["yaml"]},
        {"title": "AgentFS Knowledge", "path": "docs/agentfs.md",
         "content": "файловая система знаний kernel", "tags": ["filesystem"]},
    ]


def test_find_relevant_returns_list():
    index = _sample_index()
    result = mod.find_relevant("память консолидация", index)
    assert isinstance(result, list)


def test_find_relevant_top_k_limit():
    index = _sample_index()
    result = mod.find_relevant("агент", index, top_k=2)
    assert len(result) <= 2


def test_find_relevant_best_match_first():
    index = _sample_index()
    result = mod.find_relevant("память консолидация", index)
    # Yodoca has more memory-related content
    assert result[0]["path"] == "docs/yodoca.md"


def test_find_relevant_empty_query():
    index = _sample_index()
    result = mod.find_relevant("", index)
    assert result == []


def test_find_relevant_empty_index():
    result = mod.find_relevant("память агент", [])
    assert result == []


def test_find_relevant_only_stopwords_query():
    index = _sample_index()
    result = mod.find_relevant("и в на что", index)
    assert result == []


def test_find_relevant_no_match_returns_empty():
    index = _sample_index()
    result = mod.find_relevant("xyz_nonexistent_term_zzz_123", index)
    assert result == []

# ── build_context ─────────────────────────────────────────────────────────────

def test_build_context_returns_string():
    docs = _sample_index()[:2]
    result = mod.build_context(docs)
    assert isinstance(result, str)


def test_build_context_contains_doc_title():
    docs = [{"title": "Yodoca Memory", "path": "docs/yodoca.md",
              "content": "память консолидация", "preview": ""}]
    result = mod.build_context(docs)
    assert "Yodoca Memory" in result


def test_build_context_respects_max_chars():
    big_content = "a" * 10_000
    docs = [{"title": "Big Doc", "path": "docs/big.md",
              "content": big_content, "preview": ""}]
    result = mod.build_context(docs, max_chars=200)
    assert len(result) <= 300  # some overhead for title/path markup is ok


def test_build_context_empty_docs():
    result = mod.build_context([])
    assert result == ""


def test_build_context_uses_separator():
    docs = _sample_index()[:2]
    result = mod.build_context(docs)
    assert "---" in result

# ── _cache_key ────────────────────────────────────────────────────────────────

def test_cache_key_returns_string():
    key = mod._cache_key("Что такое NGT Memory?")
    assert isinstance(key, str)


def test_cache_key_same_input_same_key():
    key1 = mod._cache_key("Что такое NGT?")
    key2 = mod._cache_key("Что такое NGT?")
    assert key1 == key2


def test_cache_key_different_inputs_different_keys():
    key1 = mod._cache_key("Что такое NGT?")
    key2 = mod._cache_key("Что такое AgentFS?")
    assert key1 != key2


def test_cache_key_case_insensitive():
    key1 = mod._cache_key("Агент")
    key2 = mod._cache_key("агент")
    assert key1 == key2


def test_cache_key_strips_whitespace():
    key1 = mod._cache_key("  агент  ")
    key2 = mod._cache_key("агент")
    assert key1 == key2


def test_cache_key_length():
    key = mod._cache_key("test question")
    assert len(key) == 12  # MD5[:12]

# ── get_cached / put_cached ───────────────────────────────────────────────────

def test_get_cached_miss():
    cache = {}
    result = mod.get_cached("Что такое NGT?", cache)
    assert result is None


def test_put_cached_stores_answer():
    cache = {}
    mod.put_cached("Что такое NGT?", "NGT — это граф памяти.", cache)
    result = mod.get_cached("Что такое NGT?", cache)
    assert result == "NGT — это граф памяти."


def test_get_cached_case_insensitive():
    cache = {}
    mod.put_cached("Что такое NGT?", "Ответ.", cache)
    result = mod.get_cached("ЧТО ТАКОЕ NGT?", cache)
    assert result == "Ответ."


def test_put_cached_overwrites():
    cache = {}
    mod.put_cached("вопрос", "старый ответ", cache)
    mod.put_cached("вопрос", "новый ответ", cache)
    result = mod.get_cached("вопрос", cache)
    assert result == "новый ответ"

# ── load_index ────────────────────────────────────────────────────────────────

def test_load_index_returns_list(monkeypatch, tmp_path):
    idx_file = tmp_path / "search_index.json"
    idx_file.write_text(json.dumps([{"title": "Doc1", "path": "a.md"}]), encoding="utf-8")
    monkeypatch.setattr(mod, "INDEX_PATH", idx_file)
    result = mod.load_index()
    assert isinstance(result, list)
    assert len(result) == 1


def test_load_index_dict_format(monkeypatch, tmp_path):
    idx_file = tmp_path / "search_index.json"
    idx_file.write_text(json.dumps({"docs": [{"title": "Doc1"}]}), encoding="utf-8")
    monkeypatch.setattr(mod, "INDEX_PATH", idx_file)
    result = mod.load_index()
    assert isinstance(result, list)
    assert result[0]["title"] == "Doc1"


def test_load_index_missing_file(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "INDEX_PATH", tmp_path / "nonexistent.json")
    result = mod.load_index()
    assert result == []

# ── extract_questions_from_md ─────────────────────────────────────────────────

def test_extract_questions_returns_list():
    text = "## Questions\n\n- Что такое NGT Memory?\n- Как работает RAG?\n"
    result = mod.extract_questions_from_md.__wrapped__(text) if hasattr(
        mod.extract_questions_from_md, '__wrapped__') else None
    # Call directly with a tmp file
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md',
                                     encoding='utf-8', delete=False) as f:
        f.write(text)
        fname = f.name
    try:
        result = mod.extract_questions_from_md(Path(fname))
        assert isinstance(result, list)
    finally:
        os.unlink(fname)


def test_extract_questions_finds_bulleted(tmp_path):
    md = tmp_path / "questions.md"
    md.write_text(
        "# Questions\n\n"
        "- Что такое NGT Memory?\n"
        "- Как работает hybrid search?\n"
        "- Что делает AgentFS?\n",
        encoding="utf-8",
    )
    result = mod.extract_questions_from_md(md)
    assert len(result) >= 2
    assert any("NGT" in q for q in result)


def test_extract_questions_limits_to_20(tmp_path):
    md = tmp_path / "questions.md"
    lines = "\n".join(f"- Вопрос номер {i}?" for i in range(30))
    md.write_text(lines, encoding="utf-8")
    result = mod.extract_questions_from_md(md)
    assert len(result) <= 20


def test_extract_questions_ignores_short_lines(tmp_path):
    md = tmp_path / "questions.md"
    md.write_text("- Да?\n- Нет?\n- Что такое NGT Memory Associative Graph?\n",
                  encoding="utf-8")
    result = mod.extract_questions_from_md(md)
    # Short questions (≤10 chars after strip) should be skipped
    for q in result:
        assert len(q) > 10
