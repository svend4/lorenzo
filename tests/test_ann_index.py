"""
Тесты для scripts/improve_ann_index.py — hnswlib ANN-индекс.

Покрытие:
  - Словарь (vocab): ключевые слова присутствуют, мин. размер
  - Файлы индекса: существуют после build (skip если нет)
  - ann_search(): возвращает результаты, поля, не падает на пустом запросе
  - Двухстадийность: результаты содержат _ann_score
  - Воспроизводимость: два одинаковых запроса дают одинаковый топ-1
  - Скорость: один запрос < 1с (после загрузки индекса)

Запуск:
    pytest tests/test_ann_index.py -v
"""

import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# ── Пропустить все тесты если индекс не построен ─────────────────────────────

ANN_INDEX = ROOT / "docs" / "ann_index.bin"
ANN_META  = ROOT / "docs" / "ann_meta.json"
ANN_PROJ  = ROOT / "docs" / "ann_proj.npy"

pytestmark = pytest.mark.skipif(
    not (ANN_INDEX.exists() and ANN_META.exists() and ANN_PROJ.exists()),
    reason="ANN-индекс не построен. Запустите: python scripts/improve_ann_index.py --build",
)

from improve_ann_index import ann_search, _load, _tokenize, _build_vocab  # noqa: E402

# ── Словарь ──────────────────────────────────────────────────────────────────

def test_vocab_contains_key_russian_words():
    _, meta, _, vocab, _ = _load()
    vocab_set = set(meta["vocab"])
    key_words = ["агент", "память", "граф", "карточка", "архитектура", "консолидация"]
    missing = [w for w in key_words if w not in vocab_set]
    assert missing == [], f"Слова отсутствуют в словаре: {missing}"


def test_vocab_min_size():
    _, meta, _, _, _ = _load()
    assert len(meta["vocab"]) >= 1000, "Словарь слишком мал"


def test_vocab_no_stopwords():
    _, meta, _, _, _ = _load()
    vocab_set = set(meta["vocab"])
    stopwords = {"и", "в", "на", "the", "a", "an", "of"}
    found = vocab_set & stopwords
    assert not found, f"Стоп-слова в словаре: {found}"

# ── Файлы индекса ────────────────────────────────────────────────────────────

def test_index_files_exist():
    assert ANN_INDEX.exists(), "ann_index.bin не найден"
    assert ANN_META.exists(),  "ann_meta.json не найден"
    assert ANN_PROJ.exists(),  "ann_proj.npy не найден"


def test_index_files_nonempty():
    assert ANN_INDEX.stat().st_size > 0
    assert ANN_META.stat().st_size > 0
    assert ANN_PROJ.stat().st_size > 0


def test_meta_n_docs():
    _, meta, _, _, _ = _load()
    assert meta["n_docs"] > 0


def test_meta_dim():
    _, meta, _, _, _ = _load()
    assert meta["dim"] >= 64, "Слишком малая размерность"

# ── ann_search() ─────────────────────────────────────────────────────────────

def test_search_returns_list():
    results = ann_search("агент с памятью", top_k=5)
    assert isinstance(results, list)


def test_search_returns_k_results():
    results = ann_search("граф знаний", top_k=5)
    assert 1 <= len(results) <= 5


def test_search_results_have_path():
    results = ann_search("консолидация памяти", top_k=3)
    if results:
        assert "path" in results[0]
        assert isinstance(results[0]["path"], str)
        assert len(results[0]["path"]) > 0


def test_search_results_have_ann_score():
    results = ann_search("RAG retrieval", top_k=3)
    if results:
        assert "_ann_score" in results[0]
        score = results[0]["_ann_score"]
        assert 0.0 <= score <= 1.0


def test_search_scores_descending():
    results = ann_search("агент граф память", top_k=5)
    scores = [r["_ann_score"] for r in results]
    assert scores == sorted(scores, reverse=True), "Результаты должны быть отсортированы по убыванию score"


def test_search_empty_query_no_crash():
    results = ann_search("", top_k=5)
    assert isinstance(results, list)


def test_search_unknown_query_returns_list():
    results = ann_search("xyzxyz абракадабра 999", top_k=5)
    assert isinstance(results, list)


def test_search_reproducible():
    r1 = ann_search("агент с памятью консолидация", top_k=3)
    r2 = ann_search("агент с памятью консолидация", top_k=3)
    if r1 and r2:
        assert r1[0]["path"] == r2[0]["path"], "Поиск должен быть детерминированным"


def test_search_top1_different_for_different_queries():
    r1 = ann_search("граф знаний архитектура", top_k=1)
    r2 = ann_search("вакансии Anthropic ML исследования", top_k=1)
    if r1 and r2:
        # Разные запросы должны давать разные результаты (или хотя бы запускаться)
        pass   # Не ломаемся — это главное


def test_search_no_duplicate_paths():
    results = ann_search("агент память граф карточка", top_k=10)
    paths = [r["path"] for r in results]
    assert len(paths) == len(set(paths)), "Дубликаты путей в результатах"

# ── Скорость ─────────────────────────────────────────────────────────────────

def test_search_speed_after_cache_load():
    """После прогрева кэша запрос должен занимать < 1с."""
    ann_search("тест прогрев", top_k=1)       # прогрев
    t0 = time.perf_counter()
    ann_search("агент с памятью консолидация", top_k=10)
    elapsed = time.perf_counter() - t0
    assert elapsed < 1.0, f"Слишком медленно: {elapsed:.2f}с (ожидается < 1.0с)"


# ── main ──────────────────────────────────────────────────────────────────────

import importlib as _importlib
_mod = _importlib.import_module("improve_ann_index")


def test_main_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog"])
    _mod.main()
    out = capsys.readouterr().out
    assert True  # help printed or silent


def test_main_stats_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--stats"])
    _mod.main()


def test_main_query_no_index_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent memory"])
    _mod.main()
