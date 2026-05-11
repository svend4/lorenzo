"""
Тесты для scripts/improve_see_also.py.

Покрытие:
  - tokenize()             — удаление стопслов, code-blocks, минимальная длина
  - jaccard()              — коэффициент Жаккара двух множеств
  - find_related()         — топ-N связанных документов по Жаккару
  - build_see_also_block() — блок "Смотрите также"
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_see_also")

# ── tokenize ──────────────────────────────────────────────────────────────────

def test_tokenize_returns_set():
    result = mod.tokenize("агент память консолидация")
    assert isinstance(result, set)


def test_tokenize_lowercases():
    result = mod.tokenize("AgentFS Memory")
    assert all(t == t.lower() for t in result)


def test_tokenize_removes_stopwords():
    result = mod.tokenize("и в на что как это для или но the a an")
    assert result == set()


def test_tokenize_keeps_content_words():
    result = mod.tokenize("агент память консолидация yodoca agentfs")
    assert "агент" in result
    assert "память" in result


def test_tokenize_min_length_4():
    # regex [а-яёa-z]{4,} → min 4 chars
    result = mod.tokenize("abc abcd abcde")
    assert "abc" not in result
    assert "abcd" in result
    assert "abcde" in result


def test_tokenize_strips_code_blocks():
    text = "обычный текст\n```python\nprint('hello')\n```\nещё текст"
    result = mod.tokenize(text)
    assert "print" not in result
    assert "hello" not in result


def test_tokenize_empty_text():
    assert mod.tokenize("") == set()


def test_tokenize_only_stopwords():
    result = mod.tokenize("и в на что")
    assert result == set()


# ── jaccard ───────────────────────────────────────────────────────────────────

def test_jaccard_identical_sets():
    s = {"агент", "память", "граф"}
    assert mod.jaccard(s, s) == 1.0


def test_jaccard_disjoint_sets():
    a = {"агент", "память"}
    b = {"yaml", "граф"}
    assert mod.jaccard(a, b) == 0.0


def test_jaccard_partial_overlap():
    a = {"агент", "память", "граф"}
    b = {"агент", "память", "yaml"}
    # intersection=2, union=4
    result = mod.jaccard(a, b)
    assert abs(result - 2 / 4) < 1e-9


def test_jaccard_empty_a():
    assert mod.jaccard(set(), {"агент"}) == 0.0


def test_jaccard_empty_b():
    assert mod.jaccard({"агент"}, set()) == 0.0


def test_jaccard_both_empty():
    assert mod.jaccard(set(), set()) == 0.0


def test_jaccard_returns_float():
    result = mod.jaccard({"a"}, {"a", "b"})
    assert isinstance(result, float)


def test_jaccard_range_0_to_1():
    a = {"агент", "память", "граф", "mcp"}
    b = {"агент", "память", "yaml", "llm"}
    result = mod.jaccard(a, b)
    assert 0.0 <= result <= 1.0


def test_jaccard_symmetric():
    a = {"агент", "память"}
    b = {"агент", "граф"}
    assert mod.jaccard(a, b) == mod.jaccard(b, a)


# ── find_related ──────────────────────────────────────────────────────────────

def _make_tokens():
    return {
        "memory1.md": {"память", "консолидация", "decay", "агент", "граф", "store"},
        "memory2.md": {"память", "консолидация", "decay", "агент", "mcp", "store"},
        "yaml1.md":   {"yaml", "оркестрация", "декларативный", "rufler", "агент"},
        "unrelated.md": {"совершенно", "другие", "слова", "никакой", "связи"},
    }


def test_find_related_returns_list():
    tokens = _make_tokens()
    result = mod.find_related("memory1.md", tokens, n=3)
    assert isinstance(result, list)


def test_find_related_excludes_self():
    tokens = _make_tokens()
    result = mod.find_related("memory1.md", tokens, n=10)
    names = [r[0] for r in result]
    assert "memory1.md" not in names


def test_find_related_respects_n():
    tokens = _make_tokens()
    result = mod.find_related("memory1.md", tokens, n=2)
    assert len(result) <= 2


def test_find_related_sorted_by_score_descending():
    tokens = _make_tokens()
    result = mod.find_related("memory1.md", tokens, n=10)
    scores = [r[1] for r in result]
    assert scores == sorted(scores, reverse=True)


def test_find_related_minimum_threshold():
    # unrelated.md has Jaccard < 0.08 with memory1.md
    tokens = _make_tokens()
    result = mod.find_related("memory1.md", tokens, n=10)
    names = [r[0] for r in result]
    assert "unrelated.md" not in names


def test_find_related_missing_fname():
    tokens = _make_tokens()
    result = mod.find_related("nonexistent.md", tokens, n=3)
    # my_tokens = set() → jaccard always 0.0 → all below threshold → empty
    assert result == []


def test_find_related_scores_are_floats():
    tokens = _make_tokens()
    result = mod.find_related("memory1.md", tokens, n=3)
    for _, score in result:
        assert isinstance(score, float)


# ── build_see_also_block ──────────────────────────────────────────────────────

def test_build_see_also_block_returns_string():
    related = [("file.md", Path("/docs/file.md"))]
    result = mod.build_see_also_block(related)
    assert isinstance(result, str)


def test_build_see_also_block_contains_marker():
    related = [("file.md", Path("/docs/file.md"))]
    result = mod.build_see_also_block(related)
    assert mod.MARKER in result


def test_build_see_also_block_contains_heading():
    related = [("file.md", Path("/docs/file.md"))]
    result = mod.build_see_also_block(related)
    assert "Смотрите также" in result


def test_build_see_also_block_contains_separator():
    related = [("file.md", Path("/docs/file.md"))]
    result = mod.build_see_also_block(related)
    assert "---" in result


def test_build_see_also_block_lists_all_entries():
    related = [
        ("alpha.md", Path("/docs/alpha.md")),
        ("beta.md", Path("/docs/beta.md")),
    ]
    result = mod.build_see_also_block(related)
    assert "alpha" in result
    assert "beta" in result


def test_build_see_also_block_uses_stem():
    related = [("my-doc.md", Path("/docs/my-doc.md"))]
    result = mod.build_see_also_block(related)
    assert "my-doc" in result


def test_build_see_also_block_empty_related():
    result = mod.build_see_also_block([])
    assert mod.MARKER in result
    assert "Смотрите также" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_see_also_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    (tmp_path / "doc1.md").write_text("# AgentFS\n\nContent memory agent.", encoding="utf-8")
    (tmp_path / "doc2.md").write_text("# Yodoca\n\nMemory consolidation.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "SEE_ALSO.md").exists()


def test_main_dry_run_no_output(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.main()
    assert not (tmp_path / "SEE_ALSO.md").exists()


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    assert (tmp_path / "SEE_ALSO.md").exists()


def test_main_see_also_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    text = (tmp_path / "SEE_ALSO.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
