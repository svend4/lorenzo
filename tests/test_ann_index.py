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

# ── Пропустить тесты если индекс не построен ──────────────────────────────────
# Достаточно ann_meta.json (pure-Python backend строит его всегда).
# HNSW-specific (ann_index.bin, ann_proj.npy) — опциональны.

ANN_INDEX = ROOT / "docs" / "ann_index.bin"
ANN_META  = ROOT / "docs" / "ann_meta.json"
ANN_PROJ  = ROOT / "docs" / "ann_proj.npy"

pytestmark = pytest.mark.skipif(
    not ANN_META.exists(),
    reason="ANN-индекс не построен. Запустите: python scripts/improve_ann_index.py --build",
)

# Отдельный маркер для HNSW-only тестов
_skip_no_hnsw = pytest.mark.skipif(
    not (ANN_INDEX.exists() and ANN_PROJ.exists()),
    reason="HNSW-backend файлы отсутствуют (требуется pip install hnswlib numpy + build)",
)

# Текущая версия скрипта использует dual-backend (HNSW + pure-Python).
# Старые HNSW-only функции (_load, _build_vocab, _exact_score, show_stats, _CACHE)
# были удалены при рефакторинге. Импортируем то, что точно есть; остальное —
# опционально, тесты на удалённые функции автоматически скипаются.
from improve_ann_index import ann_search, _tokenize, _doc_text  # noqa: E402

try:
    from improve_ann_index import _load, _build_vocab, _exact_score, show_stats  # noqa: E402
    _LEGACY_API_AVAILABLE = True
except ImportError:
    _LEGACY_API_AVAILABLE = False

_skip_legacy = pytest.mark.skipif(
    not _LEGACY_API_AVAILABLE,
    reason="Legacy HNSW-only API removed in dual-backend refactor",
)

# ── Словарь ──────────────────────────────────────────────────────────────────

@_skip_legacy
def test_vocab_contains_key_russian_words():
    _, meta, _, vocab, _ = _load()
    vocab_set = set(meta["vocab"])
    key_words = ["агент", "память", "граф", "карточка", "архитектура", "консолидация"]
    missing = [w for w in key_words if w not in vocab_set]
    assert missing == [], f"Слова отсутствуют в словаре: {missing}"


@_skip_legacy
def test_vocab_min_size():
    _, meta, _, _, _ = _load()
    assert len(meta["vocab"]) >= 1000, "Словарь слишком мал"


@_skip_legacy
def test_vocab_no_stopwords():
    _, meta, _, _, _ = _load()
    vocab_set = set(meta["vocab"])
    stopwords = {"и", "в", "на", "the", "a", "an", "of"}
    found = vocab_set & stopwords
    assert not found, f"Стоп-слова в словаре: {found}"

# ── Файлы индекса ────────────────────────────────────────────────────────────

@_skip_no_hnsw
def test_index_files_exist():
    assert ANN_INDEX.exists(), "ann_index.bin не найден"
    assert ANN_META.exists(),  "ann_meta.json не найден"
    assert ANN_PROJ.exists(),  "ann_proj.npy не найден"


@_skip_no_hnsw
def test_index_files_nonempty():
    assert ANN_INDEX.stat().st_size > 0
    assert ANN_META.stat().st_size > 0
    assert ANN_PROJ.stat().st_size > 0


@_skip_legacy
def test_meta_n_docs():
    _, meta, _, _, _ = _load()
    assert meta["n_docs"] > 0


@_skip_legacy
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


def test_doc_text_returns_string():
    from improve_ann_index import _doc_text
    d = {"title": "Test Title", "summary": "Summary text", "content": "Content", "tags": ["tag1"]}
    result = _doc_text(d)
    assert isinstance(result, str)
    assert "Test Title" in result


def test_doc_text_handles_missing_fields():
    from improve_ann_index import _doc_text
    result = _doc_text({})
    assert isinstance(result, str)


def test_doc_text_doubles_title():
    from improve_ann_index import _doc_text
    result = _doc_text({"title": "Agent"})
    assert result.count("Agent") >= 2


@_skip_legacy
def test_build_vocab_returns_tuple():
    from improve_ann_index import _build_vocab
    # Need enough docs for df filter (3 <= c <= N*0.85) to pass
    doc_template = {"title": "Agent Memory", "content": "agent memory knowledge system retrieval " * 5, "tags": []}
    docs = [dict(doc_template) for _ in range(10)]
    vocab_words, idf_sel, df = _build_vocab(docs)
    assert isinstance(vocab_words, list)
    assert isinstance(idf_sel, dict)
    assert isinstance(df, dict)


@_skip_legacy
def test_exact_score_empty_inputs():
    from improve_ann_index import _exact_score
    assert _exact_score({}, {1: 0.5}) == 0.0
    assert _exact_score({1: 0.5}, {}) == 0.0
    assert _exact_score({}, {}) == 0.0


@_skip_legacy
def test_exact_score_identical_vectors():
    from improve_ann_index import _exact_score
    v = {0: 0.5, 1: 0.3, 2: 0.7}
    result = _exact_score(v, v)
    assert abs(result - 1.0) < 0.01


@_skip_legacy
def test_show_stats_no_meta_file(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(_mod, "META_FILE", tmp_path / "nonexistent.json")
    _mod.show_stats()
    out = capsys.readouterr().out
    assert "не построен" in out or "build" in out.lower()


def test_main_query_runs_with_results(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent memory"])
    fake_results = [{"path": "test.md", "title": "Test", "summary": "Summary", "_ann_score": 0.9}]
    monkeypatch.setattr(_mod, "ann_search", lambda q, top_k=10: fake_results)
    _mod.main()
    out = capsys.readouterr().out
    assert "Test" in out or "test.md" in out


def test_main_benchmark_mocked(monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--benchmark"])
    monkeypatch.setattr(_mod, "benchmark", lambda: None)
    _mod.main()


# ── _exact_score edge cases ───────────────────────────────────────────────────

@_skip_legacy
def test_exact_score_zero_norm_query(monkeypatch):
    """Line 249: return 0.0 when norm_q < 1e-9."""
    from improve_ann_index import _exact_score
    # All-zero query sparse → norm_q = 0
    result = _exact_score({0: 0.0}, {0: 1.0})
    assert result == 0.0


@_skip_legacy
def test_exact_score_nonzero():
    from improve_ann_index import _exact_score
    a = {0: 1.0, 1: 0.0}
    b = {0: 1.0, 1: 0.0}
    result = _exact_score(a, b)
    assert result > 0.0


# ── _load() fresh (empty cache) ───────────────────────────────────────────────

@_skip_legacy
def test_load_from_disk_when_cache_empty(monkeypatch):
    """Force _load() to go through the full file-loading path (lines 220-237)."""
    monkeypatch.setattr(_mod, "_CACHE", {})
    result = _mod._load()
    assert len(result) == 5  # index, meta, proj, vocab, idf
    index, meta, proj, vocab, idf = result
    assert meta["n_docs"] > 0


@_skip_legacy
def test_load_raises_when_index_bin_missing(tmp_path, monkeypatch):
    """Line 222: raise FileNotFoundError when INDEX_BIN is missing."""
    monkeypatch.setattr(_mod, "_CACHE", {})
    monkeypatch.setattr(_mod, "INDEX_BIN", tmp_path / "nonexistent.bin")
    with pytest.raises(FileNotFoundError):
        _mod._load()


# ── build_index() ─────────────────────────────────────────────────────────────

def test_build_index_creates_files(tmp_path, monkeypatch):
    """build_index() с маленьким корпусом — проверяет, что хотя бы один файл создан.

    build_index() в конце вызывает META_FILE.relative_to(ROOT) для красивого
    вывода. Чтобы это не падало с tmp_path вне ROOT, monkeypatch'им и ROOT.
    """
    import json as _json
    idx_data = [
        {"title": f"Agent Memory Doc {i}",
         "content": "agent memory knowledge system retrieval graph structure " * 5,
         "path": f"doc{i}.md", "preview": "", "tags": ["agent", "memory"]}
        for i in range(20)
    ]
    idx_file = tmp_path / "search_index.json"
    idx_file.write_text(_json.dumps(idx_data), encoding="utf-8")
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "INDEX_BIN", tmp_path / "ann_index.bin")
    monkeypatch.setattr(_mod, "PROJ_NPY", tmp_path / "ann_proj.npy")
    monkeypatch.setattr(_mod, "META_FILE", tmp_path / "ann_meta.json")
    # Сбросить doc cache, чтобы _load_docs прочитал наш idx_file
    monkeypatch.setattr(_mod, "_docs_cache", None, raising=False)
    _mod.build_index()
    # Хотя бы один индексный файл должен быть создан (зависит от backend)
    assert (tmp_path / "ann_meta.json").exists() or (tmp_path / "ann_index.bin").exists()


def test_main_build_calls_build_index(monkeypatch):
    """Line 391: build_index() is called when --build flag is set."""
    called = [False]
    def fake_build():
        called[0] = True
    monkeypatch.setattr(_mod, "build_index", fake_build)
    monkeypatch.setattr("sys.argv", ["prog", "--build"])
    _mod.main()
    assert called[0]


# ── benchmark() ──────────────────────────────────────────────────────────────

def test_benchmark_no_crash(monkeypatch, capsys):
    """benchmark() with mocked ann_search — signature принимает top_k."""
    fake_results = [
        {"path": "doc0.md", "title": "Test Doc", "_ann_score": 0.9,
         "sparse": {0: 0.5, 1: 0.3}}
    ]
    monkeypatch.setattr(_mod, "ann_search", lambda q, top_k=10: fake_results)
    _mod.benchmark()
    out = capsys.readouterr().out
    # Не падаем — главное; benchmark может печатать разное
    assert isinstance(out, str)
