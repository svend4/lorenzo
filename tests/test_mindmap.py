"""Tests for scripts/improve_mindmap.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_mindmap")


def test_make_mindmap_returns_string():
    result = mod.make_mindmap()
    assert isinstance(result, str)


def test_make_mindmap_starts_with_mindmap():
    result = mod.make_mindmap()
    assert result.startswith("mindmap")


def test_make_mindmap_has_root():
    result = mod.make_mindmap()
    assert "root" in result


def test_make_mindmap_has_sections():
    result = mod.make_mindmap()
    assert "Svyazi" in result
    assert "Anthropic" in result


def test_make_mindmap_has_concepts():
    result = mod.make_mindmap()
    assert "CardIndex" in result
    assert "Yodoca" in result


def test_make_flow_diagram_returns_string():
    result = mod.make_flow_diagram()
    assert isinstance(result, str)


def test_make_flow_diagram_starts_with_flowchart():
    result = mod.make_flow_diagram()
    assert result.startswith("flowchart")


def test_make_flow_diagram_has_subgraphs():
    result = mod.make_flow_diagram()
    assert "subgraph" in result


def test_make_flow_diagram_has_links():
    result = mod.make_flow_diagram()
    assert "-->" in result


def test_make_flow_diagram_has_memory_group():
    result = mod.make_flow_diagram()
    assert "MEMORY" in result


def test_make_flow_diagram_has_knowledge_group():
    result = mod.make_flow_diagram()
    assert "KNOWLEDGE" in result


def test_make_mindmap_has_all_sections():
    result = mod.make_mindmap()
    for section in mod.SECTION_LABELS.values():
        assert section in result


def test_make_mindmap_has_icons():
    result = mod.make_mindmap()
    # Icons are present in SECTION_ICONS
    for icon in mod.SECTION_ICONS.values():
        assert icon in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_mindmap_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "MINDMAP.md").exists()


def test_main_mindmap_has_mermaid(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "MINDMAP.md").read_text(encoding="utf-8")
    assert "mermaid" in text
