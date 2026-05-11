"""Tests for scripts/mcp_server.py."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _load_mcp_server():
    """Load mcp_server.py catching SystemExit from missing mcp package."""
    path = ROOT / "scripts" / "mcp_server.py"
    spec = importlib.util.spec_from_file_location("mcp_server", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mcp_server"] = module
    try:
        spec.loader.exec_module(module)
    except SystemExit:
        pass
    return module


mod = _load_mcp_server()


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory retrieval")
    assert isinstance(result, list)


def test_tokenize_filters_stopwords():
    result = mod._tokenize("the agent for memory")
    assert "the" not in result
    assert "agent" in result


def test_doc_text_returns_string():
    doc = {"content": "Content here.", "preview": "Preview."}
    result = mod._doc_text(doc)
    assert isinstance(result, str)
    assert "Content here." in result


def test_doc_text_handles_empty():
    result = mod._doc_text({})
    assert isinstance(result, str)


def test_load_index_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    idx = [{"title": "Doc", "content": "text", "path": "doc.md"}]
    (tmp_path / "search_index.json").write_text(json.dumps(idx), encoding="utf-8")
    result = mod._load_index()
    assert isinstance(result, list)
    assert len(result) == 1


def test_load_index_empty_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._load_index()
    assert result == []


def test_search_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    idx = [
        {"title": "AgentFS", "content": "agent file system memory", "path": "agentfs.md"},
        {"title": "Other", "content": "unrelated topic", "path": "other.md"},
    ]
    (tmp_path / "search_index.json").write_text(json.dumps(idx), encoding="utf-8")
    result = mod._search("agent", top_k=5)
    assert isinstance(result, list)


def test_search_empty_query(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._search("")
    assert result == []


def test_extract_section_returns_string():
    text = "# Title\n\n## Section A\n\nContent A.\n\n## Section B\n\nContent B."
    result = mod._extract_section(text, "Section A")
    assert isinstance(result, str)


def test_extract_section_finds_content():
    text = "# Title\n\n## Section A\n\nContent A here.\n\n## Other"
    result = mod._extract_section(text, "Section A")
    assert "Content A here." in result


def test_extract_section_empty_when_missing():
    text = "# Title\n\nSome content."
    result = mod._extract_section(text, "Nonexistent")
    assert result == ""


def test_read_doc_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "HEALTH.md"
    f.write_text("# Health\n\nAll good.", encoding="utf-8")
    result = mod._read_doc("HEALTH.md")
    assert isinstance(result, str)
    assert "Health" in result


def test_read_doc_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._read_doc("NONEXISTENT.md")
    assert result == ""


def test_list_improve_scripts_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    (tmp_path / "improve_health.py").write_text("# script", encoding="utf-8")
    (tmp_path / "improve_metrics.py").write_text("# script", encoding="utf-8")
    result = mod._list_improve_scripts()
    assert isinstance(result, list)
    assert "improve_health.py" in result


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_root_path_attribute():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)
