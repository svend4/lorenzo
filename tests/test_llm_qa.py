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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_clear_cache_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", True)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()


def test_main_dry_run_no_index_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "INDEX_PATH", tmp_path / "search_index.json")
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_index", lambda: [])
    mod.main()


def test_tokenize_query_returns_list():
    result = mod.tokenize_query("What is agent memory?")
    assert isinstance(result, list)


def test_tokenize_query_lowercases():
    result = mod.tokenize_query("AGENT MEMORY")
    assert all(t == t.lower() for t in result)


def test_doc_text_returns_string():
    doc = {"content": "main content", "preview": "preview", "tags": ["agent"]}
    result = mod._doc_text(doc)
    assert isinstance(result, str)
    assert "main content" in result


def test_score_doc_returns_float():
    doc = {"content": "agent memory system works", "preview": "agent preview", "tags": []}
    tokens = ["agent", "memory"]
    result = mod.score_doc(doc, tokens)
    assert isinstance(result, float)
    assert result >= 0


def test_find_relevant_returns_list():
    docs = [
        {"content": "agent memory system", "preview": "", "tags": ["agent"], "path": "doc1.md"},
        {"content": "search graph knowledge", "preview": "", "tags": [], "path": "doc2.md"},
    ]
    result = mod.find_relevant("agent memory", docs, top_k=2)
    assert isinstance(result, list)
    assert len(result) <= 2


def test_build_context_returns_string():
    docs = [{"content": "Agent memory content", "path": "doc1.md", "preview": ""}]
    result = mod.build_context(docs)
    assert isinstance(result, str)


def test_cache_key_returns_string():
    result = mod._cache_key("What is agent memory?")
    assert isinstance(result, str)
    assert len(result) > 0


def test_load_cache_returns_dict_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "nonexistent.json")
    result = mod.load_cache()
    assert isinstance(result, dict)


def test_get_cached_returns_none_on_miss():
    result = mod.get_cached("nonexistent question", {})
    assert result is None


def test_put_cached_stores_answer():
    cache = {}
    mod.put_cached("What is agent?", "An agent is a system.", cache)
    assert len(cache) == 1


# ── load_cache / save_cache ───────────────────────────────────────────────────

def test_load_cache_reads_existing(tmp_path, monkeypatch):
    cache_data = {"abc123": {"question": "test?", "answer": "answer"}}
    cache_file = tmp_path / "cache.json"
    cache_file.write_text(json.dumps(cache_data), encoding="utf-8")
    monkeypatch.setattr(mod, "CACHE_PATH", cache_file)
    monkeypatch.setattr(mod, "NO_CACHE", False)
    result = mod.load_cache()
    assert "abc123" in result


def test_load_cache_bad_json_returns_empty(tmp_path, monkeypatch):
    cache_file = tmp_path / "cache.json"
    cache_file.write_text("NOT VALID JSON {{{{", encoding="utf-8")
    monkeypatch.setattr(mod, "CACHE_PATH", cache_file)
    monkeypatch.setattr(mod, "NO_CACHE", False)
    result = mod.load_cache()
    assert isinstance(result, dict)


def test_save_cache_writes_file(tmp_path, monkeypatch):
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr(mod, "CACHE_PATH", cache_file)
    monkeypatch.setattr(mod, "NO_CACHE", False)
    mod.save_cache({"key": {"answer": "val"}})
    assert cache_file.exists()


def test_save_cache_no_cache_skips(tmp_path, monkeypatch):
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr(mod, "CACHE_PATH", cache_file)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    mod.save_cache({"key": {"answer": "val"}})
    assert not cache_file.exists()


# ── append_to_qa_answers ──────────────────────────────────────────────────────

def test_append_to_qa_answers_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    docs = [{"title": "Test Doc", "path": "test.md"}]
    mod.append_to_qa_answers("What is agent?", "An agent is a system.", docs)
    assert (tmp_path / "QA_ANSWERS.md").exists()


def test_append_to_qa_answers_appends_twice(tmp_path, monkeypatch):
    qa_file = tmp_path / "QA_ANSWERS.md"
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", qa_file)
    docs = [{"title": "Doc", "path": "doc.md"}]
    mod.append_to_qa_answers("Q1?", "A1", docs)
    mod.append_to_qa_answers("Q2?", "A2", docs)
    content = qa_file.read_text(encoding="utf-8")
    assert "Q1?" in content
    assert "Q2?" in content


# ── ask_llm ───────────────────────────────────────────────────────────────────

def test_ask_llm_calls_client():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Mock answer")]
    mock_client.messages.create.return_value = mock_resp
    result = mod.ask_llm("What is agent?", "context text", mock_client)
    assert result == "Mock answer"


# ── ask_llm_with_history ──────────────────────────────────────────────────────

def test_ask_llm_with_history_empty():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Answer without history")]
    mock_client.messages.create.return_value = mock_resp
    result = mod.ask_llm_with_history("Q?", "context", [], mock_client)
    assert result == "Answer without history"


def test_ask_llm_with_history_has_history():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Answer with history")]
    mock_client.messages.create.return_value = mock_resp
    history = [{"q": "Previous question here", "a": "Previous answer here"}]
    result = mod.ask_llm_with_history("Follow-up?", "context", history, mock_client)
    assert result == "Answer with history"


def test_ask_llm_with_history_long_answer():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="New answer")]
    mock_client.messages.create.return_value = mock_resp
    # long answer > 300 chars triggers truncation path
    long_a = "x" * 400
    history = [{"q": "Long question?", "a": long_a}]
    result = mod.ask_llm_with_history("Next?", "context", history, mock_client)
    assert result == "New answer"


# ── single_question ───────────────────────────────────────────────────────────

def _qa_index():
    return [{"title": "Memory Doc", "content": "память консолидация агент systems",
             "path": "mem.md", "preview": "", "tags": ["memory"]}]


def test_single_question_dry_run(monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SAVE", False)
    result = mod.single_question("Что такое память?", _qa_index(), client=None, cache=None)
    assert result == ""


def test_single_question_cached(monkeypatch):
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SAVE", False)
    cache = {}
    mod.put_cached("Что такое память?", "Память — это хранилище.", cache)
    result = mod.single_question("Что такое память?", _qa_index(), client=None, cache=cache)
    assert result == "Память — это хранилище."


def test_single_question_with_llm(monkeypatch, tmp_path):
    from unittest.mock import MagicMock
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "cache.json")
    monkeypatch.setattr(mod, "NO_CACHE", False)
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="LLM answer")]
    mock_client.messages.create.return_value = mock_resp
    result = mod.single_question("Что такое память?", _qa_index(), mock_client, {})
    assert result == "LLM answer"


def test_single_question_with_save(monkeypatch, tmp_path):
    from unittest.mock import MagicMock
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SAVE", True)
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "cache.json")
    monkeypatch.setattr(mod, "NO_CACHE", False)
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Saved answer")]
    mock_client.messages.create.return_value = mock_resp
    result = mod.single_question("Что такое память?", _qa_index(), mock_client, {})
    assert result == "Saved answer"
    assert (tmp_path / "QA_ANSWERS.md").exists()


def test_single_question_cached_with_save(monkeypatch, tmp_path):
    from unittest.mock import MagicMock
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SAVE", True)
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    cache = {}
    mod.put_cached("Что такое память?", "Cached answer here.", cache)
    result = mod.single_question("Что такое память?", _qa_index(), client=None, cache=cache)
    assert result == "Cached answer here."
    assert (tmp_path / "QA_ANSWERS.md").exists()


# ── interactive_mode ──────────────────────────────────────────────────────────

def test_interactive_mode_exit(monkeypatch):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "SAVE", False)
    with patch("builtins.input", return_value="exit"):
        mod.interactive_mode(_qa_index(), MagicMock(), {})


def test_interactive_mode_eoferror(monkeypatch):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "SAVE", False)
    with patch("builtins.input", side_effect=EOFError()):
        mod.interactive_mode([], MagicMock(), {})


def test_interactive_mode_keyboard_interrupt(monkeypatch):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "SAVE", False)
    with patch("builtins.input", side_effect=KeyboardInterrupt()):
        mod.interactive_mode([], MagicMock(), {})


def test_interactive_mode_with_question(monkeypatch, tmp_path):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "SAVE", False)
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Interactive answer")]
    mock_client.messages.create.return_value = mock_resp
    inputs = iter(["Что такое память агент?", "exit"])
    with patch("builtins.input", side_effect=inputs):
        with patch.object(mod.time, "sleep"):
            mod.interactive_mode(_qa_index(), mock_client, {})


def test_interactive_mode_uses_cache(monkeypatch):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "SAVE", False)
    cache = {}
    mod.put_cached("Что такое память агент?", "Cached interactive answer.", cache)
    inputs = iter(["Что такое память агент?", "exit"])
    with patch("builtins.input", side_effect=inputs):
        with patch.object(mod.time, "sleep"):
            mod.interactive_mode(_qa_index(), MagicMock(), cache)


def test_interactive_mode_with_save(monkeypatch, tmp_path):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "SAVE", True)
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "cache.json")
    monkeypatch.setattr(mod, "NO_CACHE", False)
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Saved interactive answer")]
    mock_client.messages.create.return_value = mock_resp
    inputs = iter(["Что такое агент память?", "exit"])
    with patch("builtins.input", side_effect=inputs):
        with patch.object(mod.time, "sleep"):
            mod.interactive_mode(_qa_index(), mock_client, {})
    assert (tmp_path / "QA_ANSWERS.md").exists()


# ── batch_mode ────────────────────────────────────────────────────────────────

def test_batch_mode_with_questions(monkeypatch, tmp_path):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    questions_file = tmp_path / "questions.md"
    questions_file.write_text(
        "- Что такое агент с памятью консолидацией?\n"
        "- Как работает NGT Memory граф системы?\n",
        encoding="utf-8"
    )
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Batch LLM answer")]
    mock_client.messages.create.return_value = mock_resp
    cache = {}
    with patch.object(mod.time, "sleep"):
        mod.batch_mode(questions_file, _qa_index(), mock_client, cache)
    assert (tmp_path / "QA_ANSWERS.md").exists()


def test_batch_mode_cached(monkeypatch, tmp_path):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    questions_file = tmp_path / "questions.md"
    questions_file.write_text(
        "- Что такое агент с памятью консолидацией?\n",
        encoding="utf-8"
    )
    cache = {}
    mod.put_cached("Что такое агент с памятью консолидацией?", "Pre-cached answer.", cache)
    with patch.object(mod.time, "sleep"):
        mod.batch_mode(questions_file, _qa_index(), MagicMock(), cache)


def test_batch_mode_no_sources(monkeypatch, tmp_path):
    from unittest.mock import MagicMock
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    questions_file = tmp_path / "questions.md"
    questions_file.write_text("- Xyz nonexistent topic zqr?\n", encoding="utf-8")
    mod.batch_mode(questions_file, [], MagicMock(), {})


# ── main() additional ─────────────────────────────────────────────────────────

def test_main_clear_cache_file_exists(tmp_path, monkeypatch):
    cache_file = tmp_path / "qa_cache.json"
    cache_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(mod, "CACHE_PATH", cache_file)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    assert not cache_file.exists()


def test_main_cache_printed(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "NO_CACHE", False)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {"key": {"answer": "val"}})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog"])
    mod.main()
    out = capsys.readouterr().out
    assert "Кэш" in out


def test_main_no_index_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: [])
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit):
        mod.main()


def test_main_dry_run_with_question_arg(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog", "--question", "Что такое агент память?"])
    mod.main()


def test_main_dry_run_with_batch_arg(tmp_path, monkeypatch):
    questions_file = tmp_path / "questions.md"
    questions_file.write_text("- Что такое агент?\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog", "--batch", str(questions_file)])
    mod.main()


def test_main_no_anthropic_exits(tmp_path, monkeypatch):
    from unittest.mock import patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog"])
    with patch.dict(sys.modules, {"anthropic": None}):
        with pytest.raises(SystemExit):
            mod.main()


def test_main_with_question_arg_and_anthropic(tmp_path, monkeypatch):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "NO_CACHE", False)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog", "--question", "Что такое агент память?"])
    mock_anthropic = MagicMock()
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Main answer")]
    mock_client.messages.create.return_value = mock_resp
    mock_anthropic.Anthropic.return_value = mock_client
    with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
        mod.main()


def test_main_interactive_mode(tmp_path, monkeypatch):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog"])
    mock_anthropic = MagicMock()
    mock_client = MagicMock()
    mock_anthropic.Anthropic.return_value = mock_client
    with patch("builtins.input", return_value="exit"):
        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            mod.main()


def test_main_batch_mode_via_argv(tmp_path, monkeypatch):
    from unittest.mock import MagicMock, patch
    questions_file = tmp_path / "questions.md"
    questions_file.write_text("- Что такое агент память консолидация?\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLEAR_CACHE", False)
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "qa_cache.json")
    monkeypatch.setattr(mod, "QA_ANSWERS_PATH", tmp_path / "QA_ANSWERS.md")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "NO_CACHE", True)
    monkeypatch.setattr(mod, "SAVE", False)
    monkeypatch.setattr(mod, "load_cache", lambda: {})
    monkeypatch.setattr(mod, "load_index", lambda: _qa_index())
    monkeypatch.setattr(sys, "argv", ["prog", "--batch", str(questions_file)])
    mock_anthropic = MagicMock()
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Batch answer")]
    mock_client.messages.create.return_value = mock_resp
    mock_anthropic.Anthropic.return_value = mock_client
    with patch.object(mod.time, "sleep"):
        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            mod.main()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 480: __main__ block."""
    import runpy
    from unittest.mock import patch
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--dry-run"]
        monkeypatch.setattr(mod, "DOCS", tmp_path)
        monkeypatch.setattr(mod, "ROOT", tmp_path)
        script_path = str(ROOT / "scripts" / "improve_llm_qa.py")
        runpy.run_path(script_path, run_name="__main__")
    finally:
        sys.argv = orig_argv
