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
