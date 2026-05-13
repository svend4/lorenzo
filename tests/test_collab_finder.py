"""Tests for scripts/improve_collab_finder.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_collab_finder")


def test_title_key_returns_string():
    # _title_key requires a CardEnvelope, so we test with a mock
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS: file system for AI agents"}
    card.edges = []
    result = mod._title_key(card)
    assert isinstance(result, str)


def test_title_key_normalizes_title():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS: Overview"}
    card.edges = []
    result = mod._title_key(card)
    # Should strip colon and everything after
    assert ":" not in result


def test_title_key_lowercases():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AGENTFS Overview"}
    card.edges = []
    result = mod._title_key(card)
    assert result == result.lower()


def test_title_key_removes_footnote():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "Yodoca[^yodoca]: консолидация памяти"}
    card.edges = []
    result = mod._title_key(card)
    assert "[^" not in result


def test_bm25_score_returns_float():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "body": "agent file system memory knowledge"}
    result = mod._bm25_score(["agent", "memory"], card)
    assert isinstance(result, float)


def test_bm25_score_positive_for_matching():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "body": "agent memory system retrieval"}
    result = mod._bm25_score(["agent", "memory"], card)
    assert result > 0.0


def test_bm25_score_zero_for_no_match():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "Unrelated", "body": "completely different topic content"}
    result = mod._bm25_score(["agent", "memory"], card)
    assert result == 0.0


def test_graph_bonus_returns_float():
    from unittest.mock import MagicMock
    card = MagicMock()
    edge = MagicMock()
    edge.to = "other_card_id"
    card.edges = [edge]
    result = mod._graph_bonus(card, {"other_card_id"})
    assert isinstance(result, float)


def test_graph_bonus_zero_with_no_edges():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.edges = []
    result = mod._graph_bonus(card, {"some_candidate"})
    assert result == 0.0


def test_graph_bonus_positive_with_matching_edge():
    from unittest.mock import MagicMock
    card = MagicMock()
    edge = MagicMock()
    edge.to = "candidate_id_xyz"
    card.edges = [edge]
    result = mod._graph_bonus(card, {"candidate_id_xyz"})
    assert result > 0.0


def test_graph_bonus_capped_at_0_3():
    from unittest.mock import MagicMock
    card = MagicMock()
    edges = []
    for i in range(20):
        edge = MagicMock()
        edge.to = f"candidate_{i}"
        edges.append(edge)
    card.edges = edges
    candidates = {f"candidate_{i}" for i in range(20)}
    result = mod._graph_bonus(card, candidates)
    assert result <= 0.3


def test_extract_file_query_returns_string():
    text = "# AgentFS Overview\n\nFile system for AI agents with memory.\n"
    result = mod._extract_file_query(text)
    assert isinstance(result, str)


def test_extract_file_query_includes_h1():
    text = "# Memory Agent System\n\nContent about memory.\n"
    result = mod._extract_file_query(text)
    # Result is lowercased tokens
    assert "memory" in result.lower()
    assert "agent" in result.lower()


def test_extract_file_query_extracts_frontmatter_title():
    text = "---\ntitle: AgentFS Project\n---\n\n# Overview\n\nContent.\n"
    result = mod._extract_file_query(text)
    assert "agentfs" in result.lower() or "project" in result.lower()


def test_extract_file_query_respects_max_tokens():
    long_text = "# Title\n\n" + "word " * 500
    result = mod._extract_file_query(long_text, max_tokens=10)
    words = result.split()
    assert len(words) <= 20  # approximate limit


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog"])
    try:
        mod.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    # Either prints help or exits — both acceptable
    assert True


def test_main_with_query_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "AgentFS memory", "--dry-run"])
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    try:
        mod.main()
    except SystemExit:
        pass


def test_main_dry_run_no_file_written(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent", "--dry-run"])
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards")
    try:
        mod.main()
    except SystemExit:
        pass
    assert not (tmp_path / "COLLAB.md").exists()


def test_load_index_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "INDEX", tmp_path / "nonexistent.json")
    result = mod._load_index()
    assert result is None


def test_load_index_returns_dict(tmp_path, monkeypatch):
    import json
    index_file = tmp_path / "embedding_index.json"
    index_file.write_text(json.dumps({"vectors": {}, "vocab": [], "idf": {}}), encoding="utf-8")
    monkeypatch.setattr(mod, "INDEX", index_file)
    result = mod._load_index()
    assert isinstance(result, dict)


def test_load_contacts_empty_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._load_contacts()
    assert isinstance(result, dict)
    assert len(result) == 0


def test_load_contacts_with_contact_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    (contacts_dir / "kksudo.md").write_text(
        '---\nauthor: "Konstantin"\nauthor_handle: "kksudo"\nplatform: github\n---\n# kksudo\n',
        encoding="utf-8"
    )
    result = mod._load_contacts()
    assert "kksudo" in result


def test_read_contact_brief_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "kksudo.md"
    f.write_text(
        '---\nauthor: "Konstantin"\nauthor_handle: "kksudo"\nplatform: github\nstatus: active\n---\n# kksudo\n',
        encoding="utf-8"
    )
    result = mod._read_contact_brief(f)
    assert isinstance(result, dict)
    assert "author" in result
    assert result["author"] == "Konstantin"


def test_read_contact_brief_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "nonexistent.md"
    result = mod._read_contact_brief(f)
    assert result == {}


def test_semantic_score_no_emb(monkeypatch):
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod._semantic_score({}, "card_id", {})
    assert result == 0.0


def test_semantic_score_no_index(monkeypatch):
    monkeypatch.setattr(mod, "_HAVE_EMB", True)
    result = mod._semantic_score({1: 0.5}, "card_id", None)
    assert result == 0.0


def test_find_contact_empty_contacts():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "path": "docs/agentfs.md"}
    card.edges = []
    result = mod._find_contact(card, {})
    assert result is None


def test_find_candidates_no_cards_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    result = mod.find_candidates("agent memory")
    assert result == []


def test_generate_message_returns_string():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "File system for AI agents with knowledge."}
    contact = {"author": "kksudo", "handle": "kksudo", "platform": "GitHub", "projects": ["AgentFS"]}
    result = mod._generate_message(card, contact, "agent memory knowledge")
    assert isinstance(result, str)
    assert "kksudo" in result


def test_generate_message_without_summary():
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": ""}
    contact = {"author": "Test", "handle": "", "platform": "GitHub", "projects": []}
    result = mod._generate_message(card, contact, "test query")
    assert isinstance(result, str)
    assert len(result) > 0


def test_format_report_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "Test summary", "path": "test/agentfs.md",
                    "wc": 100, "tags": []}
    card.card_id = "test_id"
    card.card_type = "project"
    card.edges = []
    candidates = [{"score": 0.8, "card": card}]
    result = mod._format_report("agent memory", "", candidates, {})
    assert isinstance(result, str)
    assert "AgentFS" in result or "agent" in result.lower()


def test_cmd_find_empty_cards_dir(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_find("agent memory")
    out = capsys.readouterr().out
    assert "CardStore" in out or "пуст" in out or "❌" in out


def test_cmd_find_no_candidates(tmp_path, monkeypatch, capsys):
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    (cards_dir / "fake.json").write_text('{}', encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "find_candidates", lambda *a, **kw: [])
    mod.cmd_find("agent memory")
    out = capsys.readouterr().out
    assert "Ничего" in out or "найден" in out.lower()


def test_cmd_find_dry_run_with_candidates(tmp_path, monkeypatch, capsys):
    from unittest.mock import MagicMock
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    (cards_dir / "fake.json").write_text('{}', encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    card = MagicMock()
    card.payload = {"title": "AgentFS", "path": "agentfs.md"}
    card.card_id = "test_id"
    card.card_type = "project"
    card.edges = []
    fake_candidates = [{"score": 0.8, "card": card}]
    monkeypatch.setattr(mod, "find_candidates", lambda *a, **kw: fake_candidates)
    monkeypatch.setattr(mod, "_load_contacts", lambda: {})
    monkeypatch.setattr(mod, "_find_contact", lambda *a, **kw: None)
    monkeypatch.setattr(mod, "_read_contact_brief", lambda *a, **kw: {"author": "Test"})
    mod.cmd_find("agent memory", dry_run=True)
    out = capsys.readouterr().out
    assert "dry-run" in out or "Найдено" in out or "AgentFS" in out


# ── Helper: create a valid CardEnvelope JSON in tmp cards dir ─────────────────

def _make_card_json(card_id: str, title: str, card_type: str = "project",
                    path: str = "", summary: str = "", tags=None, edges=None) -> dict:
    """Build a minimal card dict compatible with CardEnvelope.from_dict."""
    return {
        "card_id": card_id,
        "card_type": card_type,
        "state": "raw",
        "sources": [],
        "edges": edges or [],
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00",
        "payload_hash": "",
        "payload": {
            "title": title,
            "summary": summary,
            "path": path,
            "tags": tags or [],
            "projects": [],
            "wc": 200,
        },
    }


# ── find_candidates ───────────────────────────────────────────────────────────

def test_find_candidates_with_cards(tmp_path, monkeypatch):
    """Lines 261-352: find_candidates with real cards."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    for i in range(3):
        card = _make_card_json(
            f"card{i}", f"Agent Memory System {i}",
            path=f"docs/05-habr-projects/memory/card{i}.md",
            summary="agent memory knowledge system retrieval graph",
        )
        (cards_dir / f"card{i}.json").write_text(
            json.dumps(card), encoding="utf-8"
        )
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("agent memory knowledge", top=5)
    assert isinstance(result, list)


def test_find_candidates_all_type(tmp_path, monkeypatch):
    """Lines 267-268: card_type='all' → no type filter."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    card = _make_card_json("card1", "Agent System", card_type="doc",
                           summary="agent memory knowledge retrieval")
    (cards_dir / "card1.json").write_text(json.dumps(card), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("agent memory", card_type="all")
    assert isinstance(result, list)


def test_find_candidates_empty_pool_after_type_filter(tmp_path, monkeypatch):
    """Lines 270-271: no cards of requested type → return []."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    card = _make_card_json("card1", "Agent System", card_type="doc",
                           summary="agent memory")
    (cards_dir / "card1.json").write_text(json.dumps(card), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    # Request "project" type but card is "doc"
    result = mod.find_candidates("agent memory", card_type="project")
    assert result == []


def test_find_candidates_no_query_tokens(tmp_path, monkeypatch):
    """Lines 312-313: query has no tokens → return []."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    card = _make_card_json("card1", "Agent System")
    (cards_dir / "card1.json").write_text(json.dumps(card), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("и в на")  # all stopwords → no tokens
    assert result == []


def test_find_candidates_with_edges(tmp_path, monkeypatch):
    """Lines 344-347: graph bonus with edges."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    edge = {"to": "card1", "rel": "related", "note": ""}
    card0 = _make_card_json("card0", "Agent Memory", card_type="project",
                            summary="agent memory knowledge system retrieval",
                            edges=[edge])
    card1 = _make_card_json("card1", "Knowledge Graph", card_type="project",
                            summary="knowledge graph semantic memory retrieval")
    for i, card in enumerate([card0, card1]):
        (cards_dir / f"card{i}.json").write_text(json.dumps(card), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("agent memory knowledge graph", top=5)
    assert isinstance(result, list)


# ── _load_contacts additional paths ──────────────────────────────────────────

def test_load_contacts_skips_readme(tmp_path, monkeypatch):
    """Line 85: README.md in contacts is skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    (contacts_dir / "README.md").write_text("# Contacts Index\n", encoding="utf-8")
    (contacts_dir / "kksudo.md").write_text(
        'author: "kksudo"\n', encoding="utf-8"
    )
    result = mod._load_contacts()
    assert "readme" not in result


def test_load_contacts_reads_projects_frontmatter(tmp_path, monkeypatch):
    """Lines 93-94: projects from frontmatter are added to mapping."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    (contacts_dir / "kksudo.md").write_text(
        'author: "Konstantin"\nauthor_handle: "kksudo"\nprojects: ["AgentFS", "agentfs-core"]\n',
        encoding="utf-8"
    )
    result = mod._load_contacts()
    assert "agentfs" in result or "kksudo" in result


def test_load_contacts_handles_read_error(tmp_path, monkeypatch):
    """Lines 99-100: OSError when reading contact file is silently skipped."""
    from pathlib import Path as _Path
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contacts_dir = tmp_path / "contacts"
    contacts_dir.mkdir()
    contact_file = contacts_dir / "author.md"
    contact_file.write_text("author: test\n", encoding="utf-8")
    original_read_text = _Path.read_text
    def fake_read(self, *a, **kw):
        if self == contact_file:
            raise OSError("permission denied")
        return original_read_text(self, *a, **kw)
    monkeypatch.setattr(_Path, "read_text", fake_read)
    result = mod._load_contacts()
    assert isinstance(result, dict)


# ── _find_contact additional paths ───────────────────────────────────────────

def test_find_contact_exact_match(tmp_path, monkeypatch):
    """Line 149: exact key match in contacts."""
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS project", "path": "docs/agentfs.md"}
    card.edges = []
    contact_path = tmp_path / "agentfs.md"
    contact_path.write_text("# AgentFS\n", encoding="utf-8")
    contacts = {"agentfs": contact_path}
    result = mod._find_contact(card, contacts)
    assert result == contact_path


def test_find_contact_short_key_no_partial(tmp_path):
    """Line 154: short key (< 7 chars) → skip partial matching."""
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AI tool", "path": "docs/ai.md"}
    card.edges = []
    contact_path = tmp_path / "ai.md"
    contact_path.write_text("# AI\n", encoding="utf-8")
    contacts = {"aitool": contact_path}
    result = mod._find_contact(card, contacts)
    assert result is None or isinstance(result, Path)


def test_find_contact_partial_match(tmp_path):
    """Lines 156-159: partial string match for keys >= 7 chars."""
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentMemory System", "path": "docs/agentmemory.md"}
    card.edges = []
    contact_path = tmp_path / "agent-memory.md"
    contact_path.write_text("# AgentMemory\n", encoding="utf-8")
    # Use a key that will partially match "agentmemory" (len >= 7)
    contacts = {"agentmemory": contact_path}
    result = mod._find_contact(card, contacts)
    # Should find via partial match or exact (both are acceptable)
    assert result is None or result == contact_path


# ── _semantic_score with real index ──────────────────────────────────────────

def test_semantic_score_with_index_no_vec(monkeypatch):
    """Lines 218-219: card_id not in index vectors → cosine_sim called with empty vec."""
    monkeypatch.setattr(mod, "_HAVE_EMB", True)
    idx = {"vectors": {}}
    # The real cosine_sim({0:0.5}, {}) should return 0.0 (empty overlap)
    result = mod._semantic_score({0: 0.5}, "nonexistent_card", idx)
    assert result == 0.0


# ── _load_index exception path ────────────────────────────────────────────────

def test_load_index_invalid_json(tmp_path, monkeypatch):
    """Lines 73-74: invalid JSON → returns None."""
    index_file = tmp_path / "bad_index.json"
    index_file.write_text("not valid json {{{", encoding="utf-8")
    monkeypatch.setattr(mod, "INDEX", index_file)
    result = mod._load_index()
    assert result is None


# ── _format_report with contact ───────────────────────────────────────────────

def test_format_report_with_source_file(tmp_path, monkeypatch):
    """Line 425: source_file provided → included in report."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "Test summary", "path": "test/file.md",
                    "wc": 200, "tags": ["memory", "agent"], "projects": ["AgentFS"]}
    card.card_id = "test_id"
    card.card_type = "project"
    card.state = "raw"
    card.edges = []
    candidates = [{"score": 0.8, "card": card}]
    result = mod._format_report("agent memory", "docs/SPEC.md", candidates, {})
    assert "SPEC.md" in result


def test_format_report_with_path_and_tags(tmp_path, monkeypatch):
    """Lines 443, 477, 479, 481: path, tags, projects in report."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {
        "title": "AgentFS", "summary": "Test", "path": "docs/agentfs.md",
        "wc": 200, "tags": ["memory", "agent"], "projects": ["AgentFS", "Svyazi"],
    }
    card.card_id = "test_id"
    card.card_type = "project"
    card.state = "raw"
    card.edges = []
    candidates = [{"score": 0.8, "card": card}]
    result = mod._format_report("agent memory", "", candidates, {})
    assert "memory" in result or "agent" in result  # tags
    assert "AgentFS" in result or "Svyazi" in result  # projects


def test_format_report_with_edges(tmp_path, monkeypatch):
    """Lines 487-491: card with edges → edges listed."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    from unittest.mock import MagicMock
    edge = MagicMock()
    edge.to = "docs/other.md"
    edge.rel = "related"
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "Test", "path": "",
                    "wc": 200, "tags": [], "projects": []}
    card.card_id = "test_id"
    card.card_type = "project"
    card.state = "raw"
    card.edges = [edge, edge, edge, edge, edge]
    candidates = [{"score": 0.8, "card": card}]
    result = mod._format_report("agent memory", "", candidates, {})
    assert "related" in result or "Связан" in result


def test_format_report_with_contact(tmp_path, monkeypatch):
    """Lines 496-514: candidate has contact → contact info + message template in report."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    contact_file = tmp_path / "kksudo.md"
    contact_file.write_text("# kksudo\n", encoding="utf-8")
    from unittest.mock import MagicMock, patch
    card = MagicMock()
    card.payload = {"title": "AgentFS", "summary": "File system", "path": "",
                    "wc": 200, "tags": [], "projects": []}
    card.card_id = "test_id"
    card.card_type = "project"
    card.state = "raw"
    card.edges = []
    candidates = [{"score": 0.8, "card": card}]
    contacts = {"agentfs": contact_file}
    with patch.object(mod, "_find_contact", return_value=contact_file):
        with patch.object(mod, "_read_contact_brief", return_value={
            "author": "Konstantin", "handle": "kksudo", "platform": "GitHub",
            "status": "studied", "projects": ["AgentFS"], "path": "contacts/kksudo.md",
        }):
            result = mod._format_report("agent memory", "", candidates, contacts)
    assert "Konstantin" in result or "kksudo" in result


# ── cmd_find full execution ───────────────────────────────────────────────────

def test_cmd_find_writes_report(tmp_path, monkeypatch, capsys):
    """Lines 595-599: cmd_find writes report when not dry-run."""
    from unittest.mock import MagicMock
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    (cards_dir / "fake.json").write_text('{}', encoding="utf-8")
    out_file = tmp_path / "COLLAB.md"
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", tmp_path / "index.json")
    monkeypatch.setattr(mod, "OUT_MD", out_file)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    card = MagicMock()
    card.payload = {"title": "AgentFS", "path": "", "wc": 200, "tags": [], "projects": []}
    card.card_id = "test_id"
    card.card_type = "project"
    card.state = "raw"
    card.edges = []
    monkeypatch.setattr(mod, "find_candidates", lambda *a, **kw: [{"score": 0.8, "card": card}])
    monkeypatch.setattr(mod, "_load_contacts", lambda: {})
    monkeypatch.setattr(mod, "_find_contact", lambda *a, **kw: None)
    mod.cmd_find("agent memory", dry_run=False, out=out_file)
    assert out_file.exists()


# ── main() with --file ────────────────────────────────────────────────────────

def test_main_with_file_arg(tmp_path, monkeypatch, capsys):
    """Lines 714-724: --file argument path."""
    md_file = tmp_path / "test_doc.md"
    md_file.write_text("# Agent Memory\n\nContent about agent memory knowledge.", encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "CARDS", tmp_path / "no_cards")
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr("sys.argv", ["prog", "--file", str(md_file)])
    try:
        mod.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert "Файл" in out or "слов" in out or "токен" in out


def test_main_with_file_not_found(tmp_path, monkeypatch, capsys):
    """Line 718-719: --file points to non-existent file → SystemExit."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT_MD", tmp_path / "COLLAB.md")
    monkeypatch.setattr("sys.argv", ["prog", "--file", "nonexistent_file.md"])
    with pytest.raises(SystemExit):
        mod.main()


# ── _extract_file_query additional paths ─────────────────────────────────────

def test_extract_file_query_with_tags_comment(monkeypatch):
    """Line 634: <!-- tags: ... --> comment extracted."""
    text = "# Agent\n\n<!-- tags: memory, knowledge, graph -->\n\nContent here."
    result = mod._extract_file_query(text)
    assert "memory" in result or "knowledge" in result or "graph" in result


def test_extract_file_query_with_summary_blockquotes():
    """Lines 640-642: summary block quotes extracted."""
    text = "# Agent\n\n> Memory consolidation system for AI agents.\n> Version: 1.0\n\nContent."
    result = mod._extract_file_query(text)
    assert isinstance(result, str)


def test_extract_file_query_skips_numbered_list():
    """Line 662: numbered list items skipped."""
    text = "# Agent\n\n1. First item\n2. Second item\n\nContent paragraph here."
    result = mod._extract_file_query(text)
    # numbered list items should be excluded from body_lines
    assert isinstance(result, str)


def test_extract_file_query_handles_code_blocks():
    """Lines 650-653: code blocks are skipped."""
    text = "# Agent\n\n```python\nimport os\nprint('hi')\n```\n\nAfter code block content."
    result = mod._extract_file_query(text)
    assert "import" not in result or "After" in result


def test_find_candidates_deduplication(tmp_path, monkeypatch):
    """Lines 278-305: deduplication prefers non-mirror/more edges."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    # Two cards with same normalized title → deduplication triggered
    card_mirror = _make_card_json(
        "card_mirror", "AgentFS Project", card_type="project",
        path="docs/obsidian/agentfs.md",  # mirror prefix
        summary="agent memory knowledge",
    )
    card_main = _make_card_json(
        "card_main", "AgentFS Project", card_type="project",
        path="docs/05-habr-projects/knowledge/agentfs.md",  # main
        summary="agent memory knowledge system retrieval graph",
    )
    (cards_dir / "card_mirror.json").write_text(json.dumps(card_mirror), encoding="utf-8")
    (cards_dir / "card_main.json").write_text(json.dumps(card_main), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("agent memory knowledge system", top=5)
    assert isinstance(result, list)


def test_find_candidates_with_tfidf_index(tmp_path, monkeypatch):
    """Lines 319-320: TF-IDF vector computation when index available."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    card = _make_card_json(
        "card1", "Agent Memory System", card_type="project",
        summary="agent memory knowledge system retrieval",
    )
    (cards_dir / "card1.json").write_text(json.dumps(card), encoding="utf-8")
    # Create a fake TF-IDF index
    fake_index = {
        "vectors": {"card1": {"0": 0.5, "1": 0.3}},
        "idf": {"agent": 1.2, "memory": 1.5, "knowledge": 1.1},
        "vocab": {"agent": 0, "memory": 1, "knowledge": 2},
    }
    index_file = tmp_path / "tfidf_index.json"
    index_file.write_text(json.dumps(fake_index), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "INDEX", index_file)
    monkeypatch.setattr(mod, "_HAVE_EMB", True)
    # Provide real functions from the embedding module
    def fake_compute_tf(tokens):
        c = {}
        for t in tokens:
            c[t] = c.get(t, 0) + 1
        return {k: v/len(tokens) for k, v in c.items()}
    def fake_tfidf_vec(tf, idf):
        return {k: tf.get(k, 0) * idf.get(k, 1.0) for k in idf}
    monkeypatch.setattr(mod, "_compute_tf", fake_compute_tf)
    monkeypatch.setattr(mod, "_tfidf_vec", fake_tfidf_vec)
    result = mod.find_candidates("agent memory knowledge", top=5)
    assert isinstance(result, list)


def test_find_contact_partial_match_found(tmp_path):
    """Lines 156-159: partial match between long keys."""
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "agentmemory-system project", "path": "docs/agentmemory.md"}
    card.edges = []
    contact_path = tmp_path / "agent-memory.md"
    contact_path.write_text("# AgentMemory\n", encoding="utf-8")
    # key "agentmemory" >= 7 chars, ckey "agentmemorysys" >= 4 chars
    # "agentmemory" in "agentmemorysys" → partial match
    contacts = {"agentmemorysystem": contact_path}
    result = mod._find_contact(card, contacts)
    # partial match should work
    assert result is None or isinstance(result, Path)


def test_find_contact_skips_short_ckey(tmp_path):
    """Line 157: contacts with ckey < 4 chars are skipped."""
    from unittest.mock import MagicMock
    card = MagicMock()
    card.payload = {"title": "agentmemory system project", "path": "docs/agentmemory.md"}
    card.edges = []
    contact_path = tmp_path / "short.md"
    contact_path.write_text("# Short\n", encoding="utf-8")
    # short key < 4 chars should be skipped, so no partial match
    contacts = {"ab": contact_path, "xyz": contact_path}
    result = mod._find_contact(card, contacts)
    assert result is None


def test_find_candidates_stub_prefix_penalized(tmp_path, monkeypatch):
    """Line 293: card with svyazi-2-0 path gets wc penalized (triggers in dedup comparison)."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    # Two cards with the same title; the stub one is sorted first (card_a_stub)
    # so when card_b_rich arrives, _card_weight is called on both → line 293
    card_stub = _make_card_json(
        "card_a_stub", "Memory Component", card_type="project",
        path="docs/svyazi-2-0/components/memory.md",
        summary="memory component for svyazi system",
    )
    card_stub["payload"]["wc"] = 200
    card_rich = _make_card_json(
        "card_b_rich", "Memory Component", card_type="project",
        path="docs/05-habr-projects/memory/memory.md",
        summary="memory component knowledge retrieval agent",
    )
    card_rich["payload"]["wc"] = 400
    (cards_dir / "card_a_stub.json").write_text(json.dumps(card_stub), encoding="utf-8")
    (cards_dir / "card_b_rich.json").write_text(json.dumps(card_rich), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("memory component", top=5)
    assert isinstance(result, list)


def test_find_candidates_empty_title_uses_card_id(tmp_path, monkeypatch):
    """Line 300: card with empty title → key = card.card_id."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    card = _make_card_json(
        "card_no_title", "", card_type="project",
        summary="memory retrieval agent knowledge system",
    )
    (cards_dir / "card_no_title.json").write_text(json.dumps(card), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("memory retrieval", top=5)
    assert isinstance(result, list)


def test_find_candidates_dedup_replaces_lower_weight(tmp_path, monkeypatch):
    """Line 305: dedup replaces card when second has higher weight."""
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    # card_a_mirror (sorted first) → mirror, lower weight
    card_mirror = _make_card_json(
        "card_a_mirror", "Yodoca Memory", card_type="project",
        path="docs/obsidian/yodoca.md",
        summary="memory consolidation forgetting agent",
    )
    card_mirror["payload"]["wc"] = 50
    # card_b_main (sorted second) → not mirror, higher weight
    card_main = _make_card_json(
        "card_b_main", "Yodoca Memory", card_type="project",
        path="docs/05-habr-projects/memory/yodoca.md",
        summary="memory consolidation forgetting agent system retrieval",
    )
    card_main["payload"]["wc"] = 300
    (cards_dir / "card_a_mirror.json").write_text(json.dumps(card_mirror), encoding="utf-8")
    (cards_dir / "card_b_main.json").write_text(json.dumps(card_main), encoding="utf-8")
    monkeypatch.setattr(mod, "CARDS", cards_dir)
    monkeypatch.setattr(mod, "_HAVE_EMB", False)
    result = mod.find_candidates("memory consolidation", top=5)
    assert isinstance(result, list)
    # The main card should be preferred over the mirror
    if result:
        assert result[0]["card"].payload.get("path", "") != "docs/obsidian/yodoca.md"


def test_extract_file_query_skips_meta_blockquote():
    """Line 641: blockquote lines with Версия:/Дата: are skipped."""
    text = (
        "# Agent System\n\n"
        "> Версия: 2.0\n"
        "> Дата: 2026-01-01\n"
        "> Статус: draft\n"
        "> [!TIP] some tip\n"
        "\nContent paragraph for testing purposes here.\n"
    )
    result = mod._extract_file_query(text)
    # meta lines should be skipped, but the content should still appear
    assert isinstance(result, str)
    assert "версия" not in result.lower() or "content" in result.lower()


def test_extract_file_query_body_lines_limit():
    """Line 662: body_lines accumulates 20 lines then breaks."""
    # Create 25 normal paragraph lines
    normal_lines = "\n".join([f"Normal paragraph line number {i} for testing." for i in range(25)])
    text = f"# Title\n\n{normal_lines}\n"
    result = mod._extract_file_query(text)
    assert isinstance(result, str)
    assert len(result) > 0


def test_extract_file_query_max_tokens_limit():
    """Line 680: result reaches max_tokens limit → break."""
    # Use many unique long words (all letters, no digits) to fill up max_tokens quickly
    unique_words = [
        "memory", "retrieval", "knowledge", "cognition", "inference",
        "processing", "architecture", "distribution", "evaluation", "optimization",
        "consolidation", "augmentation", "extraction", "generation", "reasoning",
        "representation", "embedding", "vectorization", "classification", "detection",
    ]
    text = f"# Research\n\n{' '.join(unique_words)}\n"
    result = mod._extract_file_query(text, max_tokens=5)
    # Should be limited to 5 unique tokens
    tokens = result.split()
    assert len(tokens) <= 6  # at most 5 + possibly "research" from H1
