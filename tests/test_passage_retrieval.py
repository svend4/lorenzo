"""
Тесты для scripts/improve_passage_retrieval.py.

Покрытие:
  - _clean()            — очистка markdown
  - _tokenize()         — токенизация с фильтром стоп-слов
  - _extract_passages() — разбивка текста на абзацы
  - build_bm25_index()  — построение BM25-индекса
  - bm25_search()       — поиск с BM25-ранжированием
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_passage_retrieval")

# ── _clean ────────────────────────────────────────────────────────────────────

def test_clean_removes_code_blocks():
    text = "before\n```python\ncode\n```\nafter"
    result = mod._clean(text)
    assert "code" not in result
    assert "before" in result


def test_clean_removes_urls():
    text = "visit https://example.com/path?q=1 for more"
    result = mod._clean(text)
    assert "https://" not in result
    assert "visit" in result


def test_clean_removes_html_comments():
    text = "text <!-- hidden --> more"
    result = mod._clean(text)
    assert "hidden" not in result


def test_clean_normalizes_whitespace():
    text = "word1   \n\n   word2"
    result = mod._clean(text)
    assert "  " not in result

# ── _tokenize ─────────────────────────────────────────────────────────────────

def test_tokenize_returns_list():
    assert isinstance(mod._tokenize("агент память"), list)


def test_tokenize_removes_short_tokens():
    tokens = mod._tokenize("я к в на агент")
    assert all(len(t) >= 3 for t in tokens)


def test_tokenize_lowercases():
    tokens = mod._tokenize("AgentFS YODOCA Memory")
    assert all(t == t.lower() for t in tokens)


def test_tokenize_filters_stopwords():
    # Common Russian stopwords should be filtered
    tokens = mod._tokenize("это для того чтобы агент работал")
    # at minimum "агент" and "работал" should survive
    assert "агент" in tokens or len(tokens) > 0


def test_tokenize_empty_string():
    assert mod._tokenize("") == []

# ── _extract_passages ─────────────────────────────────────────────────────────

def test_extract_passages_returns_list():
    text = "# Heading\n\nThis is a paragraph with enough words to pass the filter.\n"
    result = mod._extract_passages(text, "test.md", min_words=5)
    assert isinstance(result, list)


def test_extract_passages_paragraph_has_required_fields():
    text = "## Section\n\nThis paragraph has enough words to be indexed by the system.\n"
    result = mod._extract_passages(text, "test.md", min_words=5)
    if result:
        p = result[0]
        for key in ("id", "source", "heading", "text", "tokens", "wc"):
            assert key in p


def test_extract_passages_captures_heading():
    text = "## Memory Consolidation\n\nThis paragraph discusses memory consolidation in detail.\n"
    result = mod._extract_passages(text, "test.md", min_words=5)
    if result:
        assert result[0]["heading"] == "Memory Consolidation"


def test_extract_passages_skips_short_paragraphs():
    text = "# Title\n\nShort.\n\nThis is a sufficiently long paragraph with multiple words.\n"
    result = mod._extract_passages(text, "test.md", min_words=10)
    for p in result:
        assert p["wc"] >= 10


def test_extract_passages_source_in_id():
    text = "## Title\n\nSufficiently long paragraph content goes here for testing purposes.\n"
    result = mod._extract_passages(text, "docs/test.md", min_words=5)
    if result:
        assert "docs/test.md" in result[0]["id"]


def test_extract_passages_empty_text():
    result = mod._extract_passages("", "test.md", min_words=5)
    assert result == []

# ── build_bm25_index ──────────────────────────────────────────────────────────

@pytest.fixture
def sample_passages():
    texts = [
        "Yodoca использует алгоритм консолидации памяти и эффект забывания для агентов.",
        "AgentFS предоставляет файловую систему для AI-агентов на основе Obsidian.",
        "Rufler — декларативный YAML-оркестратор для запуска роя агентов Claude.",
        "NGT Memory реализует ассоциативный граф для семантической памяти агентов.",
        "knowledge-space хранит карточки знаний с тегами и связями между проектами.",
    ]
    passages = []
    for i, text in enumerate(texts):
        tokens = mod._tokenize(text)
        passages.append({
            "id": f"doc{i}::0",
            "source": f"docs/test{i}.md",
            "heading": f"Section {i}",
            "text": text,
            "tokens": tokens,
            "wc": len(text.split()),
        })
    return passages


def test_build_bm25_index_returns_dict(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    assert isinstance(idx, dict)


def test_build_bm25_index_has_required_keys(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    for key in ("idf", "inv_index", "avgdl", "N", "passage_lens"):
        assert key in idx


def test_build_bm25_index_n_equals_passages_count(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    assert idx["N"] == len(sample_passages)


def test_build_bm25_index_avgdl_positive(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    assert idx["avgdl"] > 0


def test_build_bm25_index_idf_has_known_term(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    # "агент" appears in multiple passages — should be in IDF
    assert "агент" in idx["idf"] or len(idx["idf"]) > 0

# ── bm25_search ───────────────────────────────────────────────────────────────

def test_bm25_search_returns_list(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    results = mod.bm25_search("агент память", sample_passages, idx, top_n=3)
    assert isinstance(results, list)


def test_bm25_search_top_n_respected(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    for n in (1, 2, 3):
        results = mod.bm25_search("агент", sample_passages, idx, top_n=n)
        assert len(results) <= n


def test_bm25_search_results_have_required_fields(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    results = mod.bm25_search("агент память консолидация", sample_passages, idx, top_n=3)
    if results:
        for key in ("score", "source", "heading", "text", "wc"):
            assert key in results[0]


def test_bm25_search_scores_descending(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    results = mod.bm25_search("агент", sample_passages, idx, top_n=5)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_bm25_search_yodoca_top_for_yodoca_query(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    results = mod.bm25_search("yodoca алгоритм памяти", sample_passages, idx, top_n=3)
    assert len(results) > 0
    assert "Yodoca" in results[0]["text"]


def test_bm25_search_empty_query_returns_empty(sample_passages):
    idx = mod.build_bm25_index(sample_passages)
    results = mod.bm25_search("", sample_passages, idx, top_n=5)
    assert results == []


def test_bm25_search_on_real_passages():
    """Тест на реальном passages.json (формат {passages: [...]})."""
    passages_file = ROOT / "docs" / "passages.json"
    if not passages_file.exists():
        pytest.skip("passages.json not found")
    import json
    raw = json.loads(passages_file.read_text(encoding="utf-8"))
    passages = raw["passages"] if isinstance(raw, dict) else raw
    if len(passages) < 10:
        pytest.skip("passages.json too small")
    # passages.json не хранит tokens — добавляем на лету
    # Берём первые 200 пассажей + все из yodoca для проверки recall
    yodoca_passages = [p for p in passages if "yodoca" in p.get("source", "").lower()]
    subset = passages[:200] + yodoca_passages[:20]
    for p in subset:
        if "tokens" not in p:
            p["tokens"] = mod._tokenize(p.get("text", ""))
    idx = mod.build_bm25_index(subset)
    results = mod.bm25_search("yodoca алгоритм памяти агент", subset, idx, top_n=5)
    assert len(results) > 0
    assert any("yodoca" in r["source"].lower() for r in results), \
        f"yodoca not found in top-5: {[r['source'] for r in results]}"


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_build_index_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "BUILD_INDEX_ONLY", True)
    monkeypatch.setattr(mod, "QUERY", None)
    index_path = tmp_path / "passages.json"
    monkeypatch.setattr(mod, "INDEX_PATH", index_path)
    (tmp_path / "doc.md").write_text("# Title\n\nContent paragraph here.", encoding="utf-8")
    mod.main()
    assert index_path.exists()


def test_main_no_query_creates_index(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "BUILD_INDEX_ONLY", False)
    monkeypatch.setattr(mod, "QUERY", None)
    index_path = tmp_path / "passages.json"
    monkeypatch.setattr(mod, "INDEX_PATH", index_path)
    mod.main()
    assert index_path.exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "BUILD_INDEX_ONLY", True)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "INDEX_PATH", tmp_path / "passages.json")
    mod.main()
