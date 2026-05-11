"""Tests for scripts/review_queue.py (non-Streamlit functions)."""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _load_review_queue():
    """Load review_queue.py catching ImportError for missing streamlit."""
    path = ROOT / "scripts" / "review_queue.py"
    spec = importlib.util.spec_from_file_location("review_queue", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["review_queue"] = module
    try:
        spec.loader.exec_module(module)
    except (ImportError, SystemExit):
        pass
    return module


mod = _load_review_queue()


# ── SECTIONS ──────────────────────────────────────────────────────────────────

def test_sections_is_dict():
    assert hasattr(mod, "SECTIONS")
    assert isinstance(mod.SECTIONS, dict)
    assert len(mod.SECTIONS) > 0


def test_sections_has_svyazi():
    assert any("svyazi" in k.lower() for k in mod.SECTIONS)


def test_sections_has_habr():
    assert any("habr" in k.lower() or "05" in k for k in mod.SECTIONS)


# ── STATE_COLORS ──────────────────────────────────────────────────────────────

def test_state_colors_is_dict():
    assert hasattr(mod, "STATE_COLORS")
    assert isinstance(mod.STATE_COLORS, dict)


def test_state_colors_has_approved():
    assert "approved" in mod.STATE_COLORS


def test_state_colors_has_rejected():
    assert "rejected" in mod.STATE_COLORS


# ── _parse_frontmatter ────────────────────────────────────────────────────────

def test_parse_frontmatter_returns_dict():
    text = "---\ntitle: Test\nstate: raw\n---\n\n# Content"
    result = mod._parse_frontmatter(text)
    assert isinstance(result, dict)


def test_parse_frontmatter_extracts_title():
    text = "---\ntitle: My Title\nstate: raw\n---\n\n# Content"
    result = mod._parse_frontmatter(text)
    assert result.get("title") == "My Title"


def test_parse_frontmatter_extracts_state():
    text = "---\nstate: approved\n---\n\nContent."
    result = mod._parse_frontmatter(text)
    assert result.get("state") == "approved"


def test_parse_frontmatter_no_frontmatter():
    text = "# Just a heading\n\nContent."
    result = mod._parse_frontmatter(text)
    assert result == {}


def test_parse_frontmatter_empty_string():
    result = mod._parse_frontmatter("")
    assert result == {}


# ── _write_frontmatter ────────────────────────────────────────────────────────

def test_write_frontmatter_adds_to_existing(tmp_path):
    f = tmp_path / "card.md"
    f.write_text("---\nstate: raw\n---\n\n# Content", encoding="utf-8")
    mod._write_frontmatter(f, {"state": "approved"})
    text = f.read_text(encoding="utf-8")
    assert "approved" in text


def test_write_frontmatter_creates_frontmatter(tmp_path):
    f = tmp_path / "card.md"
    f.write_text("# Content without frontmatter", encoding="utf-8")
    mod._write_frontmatter(f, {"state": "normalized"})
    text = f.read_text(encoding="utf-8")
    assert "---" in text
    assert "normalized" in text


# ── load_queue ────────────────────────────────────────────────────────────────

def test_load_queue_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.load_queue()
    assert isinstance(result, list)


def test_load_queue_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.load_queue()
    assert result == []


def test_load_queue_finds_cards(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "card.md"
    f.write_text("---\nstate: raw\ntitle: My Card\n---\n\nContent.", encoding="utf-8")
    result = mod.load_queue()
    assert len(result) >= 1


def test_load_queue_filter_by_state(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "raw_card.md").write_text("---\nstate: raw\n---\nContent.", encoding="utf-8")
    (tmp_path / "approved_card.md").write_text("---\nstate: approved\n---\nContent.", encoding="utf-8")
    result = mod.load_queue(filter_state="raw")
    assert all(c["state"] == "raw" for c in result)


# ── approve_card / reject_card / defer_card ───────────────────────────────────

def test_approve_card_sets_state(tmp_path):
    f = tmp_path / "card.md"
    f.write_text("---\nstate: raw\n---\n\n# Card", encoding="utf-8")
    mod.approve_card(f)
    text = f.read_text(encoding="utf-8")
    assert "approved" in text


def test_reject_card_sets_state(tmp_path):
    f = tmp_path / "card.md"
    f.write_text("---\nstate: raw\n---\n\n# Card", encoding="utf-8")
    mod.reject_card(f)
    text = f.read_text(encoding="utf-8")
    assert "rejected" in text


def test_defer_card_sets_state(tmp_path):
    f = tmp_path / "card.md"
    f.write_text("---\nstate: raw\n---\n\n# Card", encoding="utf-8")
    mod.defer_card(f)
    text = f.read_text(encoding="utf-8")
    assert "deferred" in text
