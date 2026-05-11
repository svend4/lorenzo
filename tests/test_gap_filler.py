"""Tests for scripts/improve_gap_filler.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_gap_filler")


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory retrieval system")
    assert isinstance(result, list)


def test_tokenize_filters_short():
    result = mod._tokenize("a bb ccc dddd")
    # Only tokens >= 3 chars
    assert "a" not in result
    assert "bb" not in result
    assert "ccc" in result


def test_tokenize_filters_stopwords():
    result = mod._tokenize("для и в на")
    assert result == []


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code_blocks():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_clean_removes_html_comments():
    result = mod._clean("Before <!-- comment --> After")
    assert "comment" not in result


def test_clean_removes_urls():
    result = mod._clean("See https://github.com/user/repo for details")
    assert "github.com" not in result


def test_parse_empty_sections_returns_list():
    text = "# Title\n\n## Section A\n\n## Section B\nContent here with words."
    result = mod._parse_empty_sections(text)
    assert isinstance(result, list)


def test_parse_empty_sections_finds_empty():
    text = "# Title\n\n## Empty Section\n\n## Section B\n\nContent " * 10
    result = mod._parse_empty_sections(text)
    # Empty Section has no content
    assert any(s["title"] == "Empty Section" for s in result)


def test_parse_empty_sections_skips_full():
    text = "# Title\n\n## Full Section\n\n" + "content word " * 20 + "\n\n"
    result = mod._parse_empty_sections(text)
    assert not any(s["title"] == "Full Section" for s in result)


def test_parse_empty_sections_has_required_keys():
    text = "# Title\n\n## Empty\n\n## Next\nContent."
    result = mod._parse_empty_sections(text)
    for sec in result:
        assert "line_idx" in sec
        assert "level" in sec
        assert "title" in sec
        assert "content_words" in sec


def test_bm25_search_returns_list():
    passages = [
        {"source": "docs/other.md", "text": "agent memory retrieval", "tokens": ["agent", "memory", "retrieval"], "wc": 3},
        {"source": "docs/other.md", "text": "knowledge graph system", "tokens": ["knowledge", "graph", "system"], "wc": 3},
    ]
    avgdl = sum(p["wc"] for p in passages) / len(passages)
    from collections import Counter, defaultdict
    import math
    N = len(passages)
    df = Counter()
    for p in passages:
        for t in set(p["tokens"]):
            df[t] += 1
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
    inv = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))
    bm25 = {"idf": idf, "inv": dict(inv), "avgdl": avgdl, "lens": [p["wc"] for p in passages]}
    result = mod._bm25_search("agent memory", passages, bm25, "docs/source.md", top=5)
    assert isinstance(result, list)


def test_bm25_search_excludes_source():
    passages = [
        {"source": "docs/source.md", "text": "agent memory retrieval", "tokens": ["agent", "memory", "retrieval"], "wc": 3},
    ]
    from collections import Counter, defaultdict
    import math
    N = len(passages)
    df = Counter()
    for p in passages:
        for t in set(p["tokens"]):
            df[t] += 1
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
    inv = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))
    bm25 = {"idf": idf, "inv": dict(inv), "avgdl": 3, "lens": [3]}
    result = mod._bm25_search("agent", passages, bm25, "docs/source.md", top=5)
    # Should exclude source file
    assert all(r["source"] != "docs/source.md" for r in result)


def test_bm25_search_empty_tokens():
    result = mod._bm25_search("и в на", {}, {}, "source.md", top=5)
    assert result == []


def test_min_content_is_int():
    assert hasattr(mod, "MIN_CONTENT")
    assert isinstance(mod.MIN_CONTENT, int)
    assert mod.MIN_CONTENT > 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # dry-run → no output file, must not raise


def test_main_dry_run_with_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    (tmp_path / "doc.md").write_text(
        "# Title\n\n## Empty Section\n\n## Another Empty Section\n",
        encoding="utf-8"
    )
    mod.main()  # must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # must not raise
