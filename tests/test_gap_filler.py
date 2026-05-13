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


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_mode_arg_parsing():
    """Lines 41-43: --mode cite sets MODE."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--mode", "cite"]
        importlib.reload(mod)
        assert mod.MODE == "cite"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_top_arg_parsing():
    """Lines 46-48: --top N sets TOP."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--top", "3"]
        importlib.reload(mod)
        assert mod.TOP == 3
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_min_content_arg_parsing():
    """Lines 51-53: --min-content N sets MIN_CONTENT."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-content", "20"]
        importlib.reload(mod)
        assert mod.MIN_CONTENT == 20
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 57-59: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _build_corpus edge cases ──────────────────────────────────────────────────

def test_build_corpus_with_long_paragraphs(tmp_path, monkeypatch):
    """Lines 117-129: paragraphs with >= 15 tokens → corpus built."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    # 20+ content words in one paragraph
    long_para = "agent memory retrieval system knowledge graph data processing pipeline storage architecture design " * 2
    f.write_text(long_para, encoding="utf-8")
    passages, bm25 = mod._build_corpus([f])
    assert len(passages) >= 1
    assert "idf" in bm25


def test_build_corpus_skips_short_paragraphs(tmp_path, monkeypatch):
    """Line 107: paragraph with < 15 tokens → skipped."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("short text here.\n\nother short para.\n", encoding="utf-8")
    passages, bm25 = mod._build_corpus([f])
    # Short paragraphs have < 15 tokens → all skipped
    assert len(passages) == 0


def test_build_corpus_exception_handled(tmp_path, monkeypatch):
    """Lines 98-99: exception reading file → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "bad.md"
    f.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == f:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    passages, bm25 = mod._build_corpus([f])
    assert passages == []


# ── _bm25_search: break at top ────────────────────────────────────────────────

def _make_bm25(passages):
    from collections import Counter, defaultdict
    import math
    N = len(passages)
    df: Counter = Counter()
    total_len = sum(p["wc"] for p in passages)
    for p in passages:
        for t in set(p["tokens"]):
            df[t] += 1
    avgdl = total_len / max(N, 1)
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
    inv: dict = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))
    return {"idf": idf, "inv": dict(inv), "avgdl": avgdl, "lens": [p["wc"] for p in passages]}


def test_bm25_search_breaks_at_top():
    """Line 159: len(results) >= top → break."""
    passages = [
        {"source": "docs/a.md", "text": "agent memory system", "tokens": ["agent", "memory", "system"], "wc": 3},
        {"source": "docs/b.md", "text": "agent knowledge graph", "tokens": ["agent", "knowledge", "graph"], "wc": 3},
        {"source": "docs/c.md", "text": "agent retrieval data", "tokens": ["agent", "retrieval", "data"], "wc": 3},
    ]
    bm25 = _make_bm25(passages)
    result = mod._bm25_search("agent", passages, bm25, "docs/other.md", top=1)
    assert len(result) <= 1


# ── _insert_content ───────────────────────────────────────────────────────────

def test_insert_content_cite_mode():
    """Lines 209-212: mode='cite' → blockquote inserted."""
    text = "# Title\n\n## Agent Memory\n\n## Next\n\nContent.\n"
    # query "Agent Memory" tokenizes to ["agent", "memory"] which matches passages
    empty_secs = [{"line_idx": 2, "level": 2, "title": "Agent Memory", "content_words": 0}]
    passages = [
        {"source": "docs/other.md", "text": "agent memory system architecture",
         "tokens": ["agent", "memory", "system", "architecture"], "wc": 4}
    ]
    bm25 = _make_bm25(passages)
    new_text, n = mod._insert_content(text, empty_secs, passages, bm25, "docs/src.md", "cite", 1)
    assert n == 1
    assert "> **Из:**" in new_text


def test_insert_content_link_mode():
    """Lines 213-217: mode='link' → link inserted."""
    text = "# Title\n\n## Empty Section\n\n## Next\n\nContent.\n"
    empty_secs = [{"line_idx": 2, "level": 2, "title": "Empty Section", "content_words": 0}]
    passages = [
        {"source": "docs/other.md", "text": "relevant content here", "tokens": ["relevant", "content", "here"], "wc": 3}
    ]
    bm25 = _make_bm25(passages)
    new_text, n = mod._insert_content(text, empty_secs, passages, bm25, "docs/src.md", "link", 1)
    assert isinstance(new_text, str)


def test_insert_content_no_results():
    """Lines 205-206: no BM25 results for section → continue."""
    text = "# Title\n\n## EmptySection\n\n## Next\n\nContent.\n"
    empty_secs = [{"line_idx": 2, "level": 2, "title": "EmptySection", "content_words": 0}]
    passages = []
    bm25 = {"idf": {}, "inv": {}, "avgdl": 0, "lens": []}
    new_text, n = mod._insert_content(text, empty_secs, passages, bm25, "docs/src.md", "link", 1)
    assert n == 0


# ── main: edge cases ──────────────────────────────────────────────────────────

def test_main_file_read_exception(tmp_path, monkeypatch):
    """Lines 259-260: exception reading file in main loop → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()  # should not crash


def test_main_full_section_skipped(tmp_path, monkeypatch):
    """Line 264: file with no empty sections → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    # File with fully-filled sections (>= MIN_CONTENT words per section)
    (tmp_path / "doc.md").write_text(
        "# Title\n\n## Section A\n\n" + "word " * 20 + "\n\n## Section B\n\n" + "word " * 20,
        encoding="utf-8",
    )
    mod.main()  # must not crash


def test_main_many_empty_sections(tmp_path, monkeypatch):
    """Line 279: > 5 empty sections → truncation message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    sections = "".join(f"\n## Section {i}\n\n" for i in range(7))
    (tmp_path / "doc.md").write_text("# Title\n" + sections, encoding="utf-8")
    mod.main()  # must not crash


def test_main_apply_mode_with_corpus(tmp_path, monkeypatch):
    """Lines 282-285, 289: APPLY=True → writes content to file."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "MODE", "link")
    monkeypatch.setattr(mod, "TOP", 1)
    # Source file with rich content (for corpus)
    long_para = "agent memory retrieval system knowledge graph data processing pipeline storage " * 3
    (tmp_path / "source.md").write_text(long_para, encoding="utf-8")
    # Target file with empty section that matches corpus
    (tmp_path / "target.md").write_text(
        "# Title\n\n## Agent Memory\n\n## Next Section\n\n" + "word " * 5,
        encoding="utf-8",
    )
    mod.main()  # must not crash


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 295: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    script_path = str(ROOT / "scripts" / "improve_gap_filler.py")
    runpy.run_path(script_path, run_name="__main__")
