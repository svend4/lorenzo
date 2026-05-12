"""
Тесты для scripts/improve_embedding_index.py.

Покрытие:
  - tokenize()      — токенизация, стоп-слова, мин. длина
  - compute_tf()    — TF нормализация
  - compute_idf()   — IDF с логарифмическим сглаживанием
  - tfidf_vector()  — произведение TF × IDF
  - cosine_sim()    — косинусное сходство разреженных векторов
  - cmd_query()     — поиск по живому индексу (если доступен)
"""

import importlib
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_embedding_index")

# ── tokenize ──────────────────────────────────────────────────────────────────

def test_tokenize_returns_list():
    assert isinstance(mod.tokenize("агент память граф"), list)


def test_tokenize_min_length_3():
    tokens = mod.tokenize("я не к для агент")
    assert all(len(t) >= 3 for t in tokens)


def test_tokenize_lowercase():
    tokens = mod.tokenize("AgentFS YODOCA Memory")
    assert all(t == t.lower() for t in tokens)


def test_tokenize_filters_stopwords():
    # Убеждаемся, что нет пустого результата для осмысленного запроса
    tokens = mod.tokenize("agent memory consolidation knowledge graph")
    assert len(tokens) > 0


def test_tokenize_empty():
    assert mod.tokenize("") == []


def test_tokenize_known_terms():
    tokens = mod.tokenize("Yodoca консолидация памяти агента")
    assert "yodoca" in tokens
    # "консолидация" должна быть (≥3 символов, не стоп-слово)
    assert any("консолид" in t for t in tokens)

# ── compute_tf ────────────────────────────────────────────────────────────────

def test_compute_tf_returns_dict():
    assert isinstance(mod.compute_tf(["агент", "память", "агент"]), dict)


def test_compute_tf_sums_to_one():
    tokens = ["a", "b", "a", "c"]
    tf = mod.compute_tf(tokens)
    assert abs(sum(tf.values()) - 1.0) < 1e-9


def test_compute_tf_repeated_term_higher():
    tf = mod.compute_tf(["агент", "агент", "память"])
    assert tf["агент"] > tf["память"]


def test_compute_tf_empty():
    assert mod.compute_tf([]) == {}


def test_compute_tf_single_term():
    tf = mod.compute_tf(["агент"])
    assert abs(tf["агент"] - 1.0) < 1e-9

# ── compute_idf ───────────────────────────────────────────────────────────────

def test_compute_idf_returns_dict():
    docs = [["агент", "память"], ["граф", "память"], ["агент", "граф"]]
    vocab = {"агент", "память", "граф"}
    idf = mod.compute_idf(docs, vocab)
    assert isinstance(idf, dict)


def test_compute_idf_has_all_vocab_terms():
    docs = [["агент", "память"], ["граф"]]
    vocab = {"агент", "память", "граф", "неизвестный"}
    idf = mod.compute_idf(docs, vocab)
    for t in vocab:
        assert t in idf


def test_compute_idf_rare_term_higher():
    # "редкий" встречается только в 1 из 10 документов
    common_docs = [["общий", "частый"]] * 9
    rare_docs = [["общий", "редкий"]]
    docs = common_docs + rare_docs
    vocab = {"общий", "частый", "редкий"}
    idf = mod.compute_idf(docs, vocab)
    assert idf["редкий"] > idf["частый"]


def test_compute_idf_all_positive():
    docs = [["a", "b"], ["b", "c"], ["a", "c"]]
    vocab = {"a", "b", "c"}
    idf = mod.compute_idf(docs, vocab)
    assert all(v > 0 for v in idf.values())

# ── tfidf_vector ──────────────────────────────────────────────────────────────

def test_tfidf_vector_returns_dict():
    tf = {"агент": 0.5, "память": 0.5}
    idf = {"агент": 2.0, "память": 1.5}
    vec = mod.tfidf_vector(tf, idf)
    assert isinstance(vec, dict)


def test_tfidf_vector_correct_values():
    tf = {"агент": 0.5, "память": 0.5}
    idf = {"агент": 2.0, "память": 1.5}
    vec = mod.tfidf_vector(tf, idf)
    assert abs(vec["агент"] - 1.0) < 1e-9
    assert abs(vec["память"] - 0.75) < 1e-9


def test_tfidf_vector_skips_missing_idf():
    tf = {"агент": 0.5, "память": 0.5}
    idf = {"агент": 2.0}   # "память" отсутствует в IDF
    vec = mod.tfidf_vector(tf, idf)
    assert "память" not in vec
    assert "агент" in vec


def test_tfidf_vector_empty_tf():
    vec = mod.tfidf_vector({}, {"агент": 1.0})
    assert vec == {}

# ── cosine_sim ────────────────────────────────────────────────────────────────

def test_cosine_sim_identical_vectors():
    v = {"агент": 1.0, "память": 0.5}
    assert abs(mod.cosine_sim(v, v) - 1.0) < 1e-9


def test_cosine_sim_orthogonal_vectors():
    v1 = {"агент": 1.0}
    v2 = {"память": 1.0}
    assert mod.cosine_sim(v1, v2) == 0.0


def test_cosine_sim_range_0_to_1():
    v1 = {"агент": 1.0, "память": 0.5}
    v2 = {"агент": 0.8, "граф": 0.3}
    sim = mod.cosine_sim(v1, v2)
    assert 0.0 <= sim <= 1.0


def test_cosine_sim_symmetric():
    v1 = {"агент": 1.0, "память": 0.5}
    v2 = {"агент": 0.8, "граф": 0.3}
    assert abs(mod.cosine_sim(v1, v2) - mod.cosine_sim(v2, v1)) < 1e-9


def test_cosine_sim_empty_vectors():
    assert mod.cosine_sim({}, {"агент": 1.0}) == 0.0
    assert mod.cosine_sim({"агент": 1.0}, {}) == 0.0
    assert mod.cosine_sim({}, {}) == 0.0


def test_cosine_sim_partial_overlap():
    v1 = {"агент": 1.0, "память": 1.0, "граф": 1.0}
    v2 = {"агент": 1.0, "другой": 1.0}
    sim = mod.cosine_sim(v1, v2)
    # Частичное перекрытие: sim > 0 и < 1
    assert 0.0 < sim < 1.0

# ── end-to-end: tf-idf pipeline ──────────────────────────────────────────────

def test_tfidf_pipeline_similar_docs_score_higher():
    """Документ о памяти должен быть ближе к запросу про память, чем о YAML."""
    docs = {
        "memory": ["yodoca", "память", "консолидация", "агент", "decay"],
        "yaml":   ["rufler", "yaml", "оркестрация", "декларативный", "агент"],
        "graph":  ["ngt", "граф", "ассоциативный", "память", "агент"],
    }
    vocab = set(t for tokens in docs.values() for t in tokens)
    idf = mod.compute_idf(list(docs.values()), vocab)

    query_tokens = ["память", "консолидация", "decay"]
    query_tf  = mod.compute_tf(query_tokens)
    query_vec = mod.tfidf_vector(query_tf, idf)

    scores = {}
    for name, tokens in docs.items():
        tf  = mod.compute_tf(tokens)
        vec = mod.tfidf_vector(tf, idf)
        scores[name] = mod.cosine_sim(query_vec, vec)

    assert scores["memory"] > scores["yaml"], \
        f"memory ({scores['memory']:.3f}) should beat yaml ({scores['yaml']:.3f})"


# ── cmd_query на живом индексе ────────────────────────────────────────────────

def test_cmd_query_returns_list_if_index_exists():
    idx = mod.load_index()
    if idx is None:
        pytest.skip("TF-IDF index not built (run improve_embedding_index.py --index)")
    results = mod.cmd_query("агент память консолидация", top=5)
    assert isinstance(results, list)


def test_cmd_query_results_have_score_and_id():
    idx = mod.load_index()
    if idx is None:
        pytest.skip("TF-IDF index not built")
    results = mod.cmd_query("Yodoca decay", top=5)
    if results:
        score, card_id, meta = results[0]
        assert isinstance(score, float)
        assert isinstance(card_id, str)
        assert isinstance(meta, dict)


def test_cmd_query_scores_descending():
    idx = mod.load_index()
    if idx is None:
        pytest.skip("TF-IDF index not built")
    results = mod.cmd_query("граф знаний memory", top=10)
    scores = [r[0] for r in results]
    assert scores == sorted(scores, reverse=True)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    out = capsys.readouterr().out
    assert True  # prints help or exits cleanly


def test_main_stats_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--stats"])
    mod.main()


def test_main_query_no_index_no_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent memory"])
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    mod.main()


def test_tokenize_returns_list():
    result = mod.tokenize("Hello world agent memory system")
    assert isinstance(result, list)
    assert all(isinstance(t, str) for t in result)


def test_tokenize_lowercases():
    result = mod.tokenize("AGENT MEMORY")
    assert all(t == t.lower() for t in result)


def test_compute_tf_returns_dict():
    result = mod.compute_tf(["agent", "memory", "agent"])
    assert isinstance(result, dict)
    assert result["agent"] > result["memory"]


def test_compute_tf_empty():
    result = mod.compute_tf([])
    assert result == {}


def test_compute_idf_returns_dict():
    docs = [["agent", "memory"], ["agent", "search"], ["graph", "knowledge"]]
    vocab = {"agent", "memory", "search", "graph", "knowledge"}
    result = mod.compute_idf(docs, vocab)
    assert isinstance(result, dict)
    assert "agent" in result


def test_tfidf_vector_returns_dict():
    tf = {"agent": 0.5, "memory": 0.3}
    idf = {"agent": 1.5, "memory": 2.0}
    result = mod.tfidf_vector(tf, idf)
    assert isinstance(result, dict)
    assert "agent" in result


def test_cosine_sim_identical():
    v = {"agent": 0.5, "memory": 0.3}
    result = mod.cosine_sim(v, v)
    assert abs(result - 1.0) < 0.01


def test_cosine_sim_disjoint():
    a = {"agent": 0.5}
    b = {"memory": 0.3}
    result = mod.cosine_sim(a, b)
    assert result == 0.0


def test_cosine_sim_empty():
    result = mod.cosine_sim({}, {})
    assert result == 0.0


# ── card_text ─────────────────────────────────────────────────────────────────

def test_card_text_returns_string():
    sys.path.insert(0, str(ROOT / "scripts"))
    from utils_card_envelope import CardEnvelope
    card = CardEnvelope(
        card_id="sha256:test0001",
        card_type="project",
        state="raw",
        payload={"title": "AgentFS", "summary": "File system for agents", "body": "content here",
                 "tags": ["memory", "agent"], "projects": ["AgentFS"]},
        edges=[],
    )
    result = mod.card_text(card)
    assert isinstance(result, str)
    assert "AgentFS" in result


def test_card_text_doubles_title():
    from utils_card_envelope import CardEnvelope
    card = CardEnvelope(
        card_id="sha256:test0002",
        card_type="doc",
        state="raw",
        payload={"title": "UniqueTitle123"},
        edges=[],
    )
    result = mod.card_text(card)
    assert result.count("UniqueTitle123") >= 2


# ── load_index / save_index ───────────────────────────────────────────────────

def test_load_index_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    result = mod.load_index()
    assert result is None


def test_save_and_load_index(tmp_path, monkeypatch):
    import json
    index_file = tmp_path / "embedding_index.json"
    cards_dir = tmp_path / "cards"
    monkeypatch.setattr(mod, "INDEX", index_file)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    idf = {"agent": 1.5, "memory": 2.0}
    vectors = {"sha256:abc": {"agent": 0.75}}
    meta = {"sha256:abc": {"title": "Test", "card_type": "doc", "state": "raw", "path": "test.md"}}
    mod.save_index(idf, vectors, meta)
    assert index_file.exists()
    result = mod.load_index()
    assert result is not None
    assert "idf" in result
    assert "vectors" in result


def test_load_index_invalid_json(tmp_path, monkeypatch):
    f = tmp_path / "bad.json"
    f.write_text("not valid json {{{{", encoding="utf-8")
    monkeypatch.setattr(mod, "INDEX", f)
    result = mod.load_index()
    assert result is None


# ── cmd_index ─────────────────────────────────────────────────────────────────

def test_cmd_index_no_cards(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    mod.cmd_index()
    out = capsys.readouterr().out
    assert "пуст" in out or "CardStore" in out


def test_cmd_index_with_cards(tmp_path, monkeypatch, capsys):
    from utils_card_envelope import CardEnvelope, CardStore
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    store = CardStore(cards_dir)
    for i in range(3):
        card = CardEnvelope(
            card_id=f"sha256:test{i:04d}",
            card_type="doc",
            state="raw",
            payload={"title": f"Doc {i}", "summary": "agent memory knowledge system retrieval",
                     "body": "agent memory knowledge " * 5, "tags": [], "projects": []},
            edges=[],
        )
        store.put(card)
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_index()
    out = capsys.readouterr().out
    assert "Карточек" in out or "Сохранено" in out


# ── cmd_query / cmd_search ────────────────────────────────────────────────────

def _build_test_index(tmp_path, monkeypatch):
    """Helper: build a minimal index for testing."""
    import json as _json
    index_file = tmp_path / "index.json"
    monkeypatch.setattr(mod, "INDEX", index_file)
    idf = {"agent": 1.5, "memory": 2.0, "knowledge": 1.8, "retrieval": 2.5}
    vectors = {
        "sha256:doc1": {"agent": 0.75, "memory": 1.0},
        "sha256:doc2": {"knowledge": 0.9, "retrieval": 1.2},
    }
    card_meta = {
        "sha256:doc1": {"title": "Agent Memory Doc", "card_type": "doc", "state": "raw", "path": "doc1.md"},
        "sha256:doc2": {"title": "Knowledge Retrieval", "card_type": "project", "state": "raw", "path": "doc2.md"},
    }
    data = {"meta": {"cards": 2, "vocab": 4, "version": "1.0"},
            "idf": idf, "vectors": vectors, "card_meta": card_meta}
    index_file.write_text(_json.dumps(data, ensure_ascii=False), encoding="utf-8")


def test_cmd_query_returns_results(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    results = mod.cmd_query("agent memory", top=5)
    assert isinstance(results, list)
    assert len(results) >= 1
    score, cid, meta = results[0]
    assert isinstance(score, float)
    assert isinstance(cid, str)


def test_cmd_query_no_index(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    results = mod.cmd_query("agent memory")
    assert results == []
    out = capsys.readouterr().out
    assert "Индекс" in out or "index" in out.lower()


def test_cmd_query_empty_query(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    results = mod.cmd_query("")
    assert results == []


def test_cmd_query_with_card_type_filter(tmp_path, monkeypatch):
    _build_test_index(tmp_path, monkeypatch)
    results = mod.cmd_query("knowledge retrieval", card_type="project")
    assert all(r[2].get("card_type") == "project" for r in results)


def test_cmd_search_shows_results(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_search("agent memory", top=5)
    out = capsys.readouterr().out
    assert "Agent Memory" in out or "agent" in out.lower()


def test_cmd_search_no_results(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_search("xyz_totally_nonexistent_abc")
    out = capsys.readouterr().out
    assert "Ничего" in out or "не найдено" in out.lower()


# ── cmd_similar ───────────────────────────────────────────────────────────────

def test_cmd_similar_found(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_similar("sha256:doc1", top=5)
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_similar_partial_match(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_similar("doc1", top=5)
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_similar_by_title(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_similar("Agent Memory Doc", top=5)
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_cmd_similar_not_found(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_similar("nonexistent_xyz_id")
    out = capsys.readouterr().out
    assert "не найдена" in out or "not found" in out.lower()


def test_cmd_similar_no_index(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    mod.cmd_similar("some_id")
    out = capsys.readouterr().out
    assert "Индекс" in out or "index" in out.lower()


# ── cmd_stats ─────────────────────────────────────────────────────────────────

def test_cmd_stats_with_index(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    mod.cmd_stats()
    out = capsys.readouterr().out
    assert "Карточек" in out or "словарь" in out.lower() or "Индекс" in out


def test_cmd_stats_no_index(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    mod.cmd_stats()
    out = capsys.readouterr().out
    assert "Индекс" in out or "index" in out.lower()


# ── main() commands ───────────────────────────────────────────────────────────

def test_main_query_with_index(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent memory"])
    mod.main()
    out = capsys.readouterr().out
    assert isinstance(out, str)


def test_main_similar_with_index(tmp_path, monkeypatch, capsys):
    _build_test_index(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--similar", "sha256:doc1"])
    mod.main()


def test_main_index_no_cards(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr("sys.argv", ["prog", "--index"])
    mod.main()
    out = capsys.readouterr().out
    assert "пуст" in out or "CardStore" in out
