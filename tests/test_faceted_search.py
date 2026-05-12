"""Tests for scripts/improve_faceted_search.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_faceted_search")


def test_word_count_returns_int(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("one two three four five", encoding="utf-8")
    result = mod._word_count(f)
    assert isinstance(result, int)
    assert result == 5


def test_word_count_missing_file(tmp_path):
    result = mod._word_count(tmp_path / "missing.md")
    assert result == 0


def test_file_mtime_returns_string(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("content", encoding="utf-8")
    result = mod._file_mtime(f)
    assert isinstance(result, str)
    assert len(result) == 10  # YYYY-MM-DD


def test_file_mtime_missing_file(tmp_path):
    result = mod._file_mtime(tmp_path / "missing.md")
    assert result == "unknown"


def test_load_keyword_index_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "KEYWORD_INDEX", tmp_path / "missing.json")
    result = mod._load_keyword_index()
    assert result == {}


def test_load_keyword_index_valid(tmp_path, monkeypatch):
    import json
    data = {"index": {"агент": [{"f": "docs/test.md", "n": 3}]}}
    f = tmp_path / "keyword_index.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "KEYWORD_INDEX", f)
    result = mod._load_keyword_index()
    assert "агент" in result


def test_load_entities_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ENTITIES_INDEX", tmp_path / "missing.json")
    result = mod._load_entities()
    assert result == {}


def test_load_entities_valid(tmp_path, monkeypatch):
    import json
    data = {"AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/a.md"]}}
    f = tmp_path / "named_entities.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_INDEX", f)
    result = mod._load_entities()
    assert "AgentFS" in result


def test_search_by_query_returns_dict():
    index = {
        "агент": [{"f": "docs/a.md", "n": 2}],
        "память": [{"f": "docs/a.md", "n": 1}, {"f": "docs/b.md", "n": 3}],
    }
    result = mod._search_by_query("агент память", index)
    assert isinstance(result, dict)


def test_search_by_query_scores_files():
    index = {
        "агент": [{"f": "docs/a.md", "n": 2}],
        "память": [{"f": "docs/a.md", "n": 1}, {"f": "docs/b.md", "n": 3}],
    }
    result = mod._search_by_query("агент память", index)
    assert "docs/a.md" in result
    assert "docs/b.md" in result


def test_search_by_query_bigram_bonus():
    index = {
        "агент": [{"f": "docs/a.md", "n": 1}],
        "память": [{"f": "docs/a.md", "n": 1}],
        "агент память": [{"f": "docs/a.md", "n": 2}],
    }
    result_uni = mod._search_by_query("агент память", index)
    # Bigram bonus should add 6.0 (2*3.0) more
    assert result_uni.get("docs/a.md", 0) > 2.0


def test_search_by_query_empty_index():
    result = mod._search_by_query("агент", {})
    assert result == {}


def test_search_by_query_filters_stopwords():
    index = {"для": [{"f": "docs/a.md", "n": 5}]}
    result = mod._search_by_query("для", index)
    assert result == {}


def test_filter_by_entity_returns_set():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_entity("agentfs", entities_data, None)
    assert isinstance(result, set)


def test_filter_by_entity_finds_files():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_entity("AgentFS", entities_data, None)
    assert "docs/agentfs.md" in result


def test_filter_by_entity_type_filter():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
        "svend4": {"name": "svend4", "type": "people", "files": ["docs/svend4.md"]},
    }
    result = mod._filter_by_entity("agentfs", entities_data, "people")
    assert "docs/agentfs.md" not in result


def test_filter_by_entity_no_match():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_entity("unknown_xyz_entity", entities_data, None)
    assert len(result) == 0


def test_filter_by_type_returns_set():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/agentfs.md"]},
    }
    result = mod._filter_by_type("projects", entities_data)
    assert isinstance(result, set)


def test_filter_by_type_finds_files():
    entities_data = {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": ["docs/a.md"]},
        "Yodoca": {"name": "Yodoca", "type": "projects", "files": ["docs/b.md"]},
        "svend4": {"name": "svend4", "type": "people", "files": ["docs/c.md"]},
    }
    result = mod._filter_by_type("projects", entities_data)
    assert "docs/a.md" in result
    assert "docs/b.md" in result
    assert "docs/c.md" not in result


def test_filter_by_type_empty():
    result = mod._filter_by_type("unknown_type", {})
    assert result == set()


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_filters_prints_usage(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    out = capsys.readouterr().out
    assert "фильтр" in out or "query" in out.lower() or "--query" in out


def test_main_with_query_no_index_warns(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "AgentFS")
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})
    mod.main()


def test_main_with_entity_filter_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})
    mod.main()


# ── _filter_by_entity: non-dict entry skipped ────────────────────────────────

def test_filter_by_entity_non_dict_entry_skipped():
    """Line 141: non-dict entity entry → continue."""
    entities_data = {
        "not_a_dict": "just a string",
        "Yodoca": {"name": "Yodoca", "type": "projects", "files": ["docs/yodoca.md"]},
    }
    result = mod._filter_by_entity("yodoca", entities_data, None)
    assert "docs/yodoca.md" in result


# ── exception handlers for index loading ─────────────────────────────────────

def test_load_keyword_index_invalid_json(tmp_path, monkeypatch):
    """Lines 81-82: invalid JSON → empty dict returned."""
    bad_file = tmp_path / "keyword_index.json"
    bad_file.write_text("not valid json!!!", encoding="utf-8")
    monkeypatch.setattr(mod, "KEYWORD_INDEX", bad_file)
    result = mod._load_keyword_index()
    assert result == {}


def test_load_entities_invalid_json(tmp_path, monkeypatch):
    """Lines 90-91: invalid JSON → empty dict returned."""
    bad_file = tmp_path / "named_entities.json"
    bad_file.write_text("not valid json!!!", encoding="utf-8")
    monkeypatch.setattr(mod, "ENTITIES_INDEX", bad_file)
    result = mod._load_entities()
    assert result == {}


# ── module-level arg parsing (requires reload) ────────────────────────────────

def test_query_arg_parsing():
    """Lines 44-47: --query TEXT sets QUERY."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--query", "agent memory"]
        importlib.reload(mod)
        assert mod.QUERY == "agent memory"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_entity_arg_parsing():
    """Lines 44-47: --entity TEXT sets ENTITY_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--entity", "AgentFS"]
        importlib.reload(mod)
        assert mod.ENTITY_FILTER == "AgentFS"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_top_arg_parsing():
    """Lines 50-52: --top N sets TOP."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--top", "20"]
        importlib.reload(mod)
        assert mod.TOP == 20
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_min_words_arg_parsing():
    """Lines 55-57: --min-words N sets MIN_WORDS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-words", "50"]
        importlib.reload(mod)
        assert mod.MIN_WORDS == 50
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_after_arg_parsing():
    """Lines 60-62: --after DATE sets AFTER_DATE."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--after", "2026-01-01"]
        importlib.reload(mod)
        assert mod.AFTER_DATE == "2026-01-01"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 65-67: --section TEXT sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER == "05-habr-projects"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── main with results (lines 181-272) ────────────────────────────────────────

def _setup_docs(tmp_path):
    """Helper: create docs dir with a test file, return (docs_dir, file_path_str)."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    test_file = docs_dir / "test.md"
    test_file.write_text("# Agent Memory\n\nContent about agent memory systems.", encoding="utf-8")
    return docs_dir, "docs/test.md"


def test_main_with_query_produces_results(tmp_path, monkeypatch):
    """Lines 181-182, 206-272: QUERY + index → results written to SEARCH_RESULTS.md."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent")
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {"agent": [{"f": fp, "n": 5}]})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()
    text = (docs_dir / "SEARCH_RESULTS.md").read_text(encoding="utf-8")
    assert "# Результаты поиска" in text


def test_main_with_entity_and_query_boost(tmp_path, monkeypatch):
    """Lines 190-191: ENTITY_FILTER + QUERY → scores boosted for matching files."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent")
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {"agent": [{"f": fp, "n": 3}]})
    monkeypatch.setattr(mod, "_load_entities", lambda: {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": [fp]}
    })

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_with_type_filter(tmp_path, monkeypatch):
    """Lines 196-199: TYPE_FILTER (no ENTITY_FILTER) → type-based results."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", "projects")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": [fp]}
    })

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_no_results_found(tmp_path, monkeypatch):
    """Line 202: scores empty → 'Ничего не найдено' printed, no output file."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", "UnknownXYZ")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})

    mod.main()
    assert not (tmp_path / "SEARCH_RESULTS.md").exists()


def test_main_with_section_filter(tmp_path, monkeypatch):
    """Lines 209-210: SECTION_FILTER excludes non-matching file paths."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", "05-habr")  # won't match docs/test.md
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": [fp]}
    })

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_with_min_words_filter(tmp_path, monkeypatch):
    """Lines 217-220: MIN_WORDS > 0 filters out small files."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 100)  # file has ~7 words
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": [fp]}
    })

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_with_after_date_filter(tmp_path, monkeypatch):
    """Lines 225-227: AFTER_DATE filters out files modified before date."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", "2099-01-01")  # far future → all filtered
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {})
    monkeypatch.setattr(mod, "_load_entities", lambda: {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": [fp]}
    })

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_list_format_output(tmp_path, monkeypatch):
    """Lines 266-268: OUTPUT_FORMAT='list' produces list-style output."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent")
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "list")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {"agent": [{"f": fp, "n": 5}]})
    monkeypatch.setattr(mod, "_load_entities", lambda: {})

    mod.main()
    text = (docs_dir / "SEARCH_RESULTS.md").read_text(encoding="utf-8")
    assert "1." in text


def test_main_nonexistent_file_in_scores_skipped(tmp_path, monkeypatch):
    """Line 214: file in scores doesn't exist → continue."""
    docs_dir, fp = _setup_docs(tmp_path)

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent")
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {
        "agent": [
            {"f": "docs/missing_file.md", "n": 10},  # missing → line 214
            {"f": fp, "n": 5},
        ]
    })
    monkeypatch.setattr(mod, "_load_entities", lambda: {})

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_top_limit_breaks_loop(tmp_path, monkeypatch):
    """Line 237: len(results) >= TOP → break out of loop."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "a.md").write_text("# A\n\nContent.", encoding="utf-8")
    (docs_dir / "b.md").write_text("# B\n\nContent.", encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent")
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 1)  # limit 1 → break after first result
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {
        "agent": [{"f": "docs/a.md", "n": 10}, {"f": "docs/b.md", "n": 5}]
    })
    monkeypatch.setattr(mod, "_load_entities", lambda: {})

    mod.main()
    assert (docs_dir / "SEARCH_RESULTS.md").exists()


def test_main_all_metadata_in_output(tmp_path, monkeypatch):
    """Lines 251-258: QUERY, ENTITY_FILTER, TYPE_FILTER, SECTION_FILTER all in output."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    habr_dir = docs_dir / "05-habr"
    habr_dir.mkdir()
    (habr_dir / "test.md").write_text("# Agent\n\nContent.", encoding="utf-8")
    fp = "docs/05-habr/test.md"

    monkeypatch.setattr(mod, "DOCS", docs_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent")
    monkeypatch.setattr(mod, "ENTITY_FILTER", "AgentFS")
    monkeypatch.setattr(mod, "TYPE_FILTER", "projects")
    monkeypatch.setattr(mod, "SECTION_FILTER", "05-habr")
    monkeypatch.setattr(mod, "MIN_WORDS", 0)
    monkeypatch.setattr(mod, "AFTER_DATE", None)
    monkeypatch.setattr(mod, "TOP", 15)
    monkeypatch.setattr(mod, "OUTPUT_FORMAT", "table")
    monkeypatch.setattr(mod, "_load_keyword_index", lambda: {"agent": [{"f": fp, "n": 5}]})
    monkeypatch.setattr(mod, "_load_entities", lambda: {
        "AgentFS": {"name": "AgentFS", "type": "projects", "files": [fp]}
    })

    mod.main()
    text = (docs_dir / "SEARCH_RESULTS.md").read_text(encoding="utf-8")
    assert "agent" in text.lower()
    assert "AgentFS" in text


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 276: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "ENTITY_FILTER", None)
    monkeypatch.setattr(mod, "TYPE_FILTER", None)
    script_path = str(ROOT / "scripts" / "improve_faceted_search.py")
    runpy.run_path(script_path, run_name="__main__")
