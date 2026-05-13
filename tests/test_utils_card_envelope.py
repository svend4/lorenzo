"""Tests for scripts/utils_card_envelope.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("utils_card_envelope")

CardEnvelope = mod.CardEnvelope
CardEdge = mod.CardEdge


# ── Helper functions ──────────────────────────────────────────────────────────

def test_sha256_returns_string():
    result = mod._sha256("hello world")
    assert isinstance(result, str)
    assert result.startswith("sha256:")


def test_sha256_deterministic():
    assert mod._sha256("test") == mod._sha256("test")


def test_sha256_different_inputs():
    assert mod._sha256("abc") != mod._sha256("def")


def test_card_id_for_returns_string():
    result = mod._card_id_for("docs/test.md")
    assert isinstance(result, str)


def test_now_iso_returns_string():
    result = mod._now_iso()
    assert isinstance(result, str)
    assert "T" in result  # ISO format


# ── _detect_card_type ─────────────────────────────────────────────────────────

def test_detect_card_type_returns_known_type(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# My Document\n\nContent.", encoding="utf-8")
    result = mod._detect_card_type(f, "# My Document\n\nContent.")
    assert result in ("doc", "note", "fact", "person", "project", "unknown")


def test_detect_card_type_meta_name(tmp_path):
    f = tmp_path / "qa.md"
    result = mod._detect_card_type(f, "# Q&A\n\nContent.")
    assert result == "doc"


def test_detect_card_type_person_from_tags(tmp_path):
    f = tmp_path / "kksudo.md"
    text = "# kksudo\n\n<!-- tags: person, contact -->\n\nProfile."
    result = mod._detect_card_type(f, text)
    assert result == "person"


def test_detect_card_type_project_known_name(tmp_path):
    f = tmp_path / "agentfs.md"
    text = "# AgentFS\n\nFilesystem project."
    result = mod._detect_card_type(f, text)
    assert result == "project"


def test_detect_card_type_frontmatter_type(tmp_path):
    f = tmp_path / "doc.md"
    text = "---\ntype: project\n---\n\n# My Project\n\nContent."
    result = mod._detect_card_type(f, text)
    assert result == "project"


# ── CardEdge ─────────────────────────────────────────────────────────────────

def test_card_edge_to_dict():
    edge = CardEdge(to="target.md", rel="references", note="see also")
    d = edge.to_dict()
    assert d["to"] == "target.md"
    assert d["rel"] == "references"
    assert "note" in d


def test_card_edge_to_dict_no_note():
    edge = CardEdge(to="target.md", rel="related")
    d = edge.to_dict()
    assert "note" not in d


# ── CardEnvelope.from_text ────────────────────────────────────────────────────

def test_from_text_returns_card_envelope():
    card = CardEnvelope.from_text("Some text content.", source="test/doc.md")
    assert isinstance(card, CardEnvelope)


def test_from_text_has_card_id():
    card = CardEnvelope.from_text("Content.", source="test.md")
    assert card.card_id.startswith("sha256:")


def test_from_text_sets_card_type():
    card = CardEnvelope.from_text("Content.", source="test.md", card_type="note")
    assert card.card_type == "note"


def test_from_text_stores_text_in_payload():
    card = CardEnvelope.from_text("My content.", source="test.md")
    assert "My content." in card.payload.get("text", "")


# ── CardEnvelope.from_file ────────────────────────────────────────────────────

def test_from_file_returns_card_envelope(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# My Title\n\nContent here.", encoding="utf-8")
    card = CardEnvelope.from_file(f, root=tmp_path)
    assert isinstance(card, CardEnvelope)


def test_from_file_extracts_title(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# My Title\n\nContent.", encoding="utf-8")
    card = CardEnvelope.from_file(f, root=tmp_path)
    assert card.payload["title"] == "My Title"


def test_from_file_fallback_title(tmp_path):
    f = tmp_path / "my-document.md"
    f.write_text("No heading.\n\nContent.", encoding="utf-8")
    card = CardEnvelope.from_file(f, root=tmp_path)
    assert "my" in card.payload["title"].lower()


def test_from_file_extracts_tags(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n<!-- tags: memory, agent -->\n\nContent.", encoding="utf-8")
    card = CardEnvelope.from_file(f, root=tmp_path)
    assert "memory" in card.payload["tags"]
    assert "agent" in card.payload["tags"]


def test_from_file_has_wc(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nOne two three four five.", encoding="utf-8")
    card = CardEnvelope.from_file(f, root=tmp_path)
    assert isinstance(card.payload["wc"], int)
    assert card.payload["wc"] > 0


# ── CardEnvelope.from_dict / to_dict ─────────────────────────────────────────

def test_to_dict_returns_dict():
    card = CardEnvelope.from_text("Content.", source="test.md")
    d = card.to_dict()
    assert isinstance(d, dict)
    assert "card_id" in d
    assert "card_type" in d
    assert "state" in d


def test_from_dict_round_trip():
    card = CardEnvelope.from_text("Content.", source="test.md")
    d = card.to_dict()
    card2 = CardEnvelope.from_dict(d)
    assert card2.card_id == card.card_id
    assert card2.card_type == card.card_type


def test_to_json_returns_string():
    card = CardEnvelope.from_text("Content.", source="test.md")
    result = card.to_json()
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert "card_id" in parsed


# ── Mutations ────────────────────────────────────────────────────────────────

def test_add_edge():
    card = CardEnvelope.from_text("Content.", source="test.md")
    card.add_edge("other.md", rel="references")
    assert len(card.edges) == 1
    assert card.edges[0].to == "other.md"


def test_add_edge_no_duplicate():
    card = CardEnvelope.from_text("Content.", source="test.md")
    card.add_edge("other.md", rel="references")
    card.add_edge("other.md", rel="references")
    assert len(card.edges) == 1


def test_add_edge_different_rels():
    card = CardEnvelope.from_text("Content.", source="test.md")
    card.add_edge("other.md", rel="references")
    card.add_edge("other.md", rel="contradicts")
    assert len(card.edges) == 2


def test_transition_state():
    card = CardEnvelope.from_text("Content.", source="test.md")
    card.transition("normalized")
    assert card.state == "normalized"


def test_decay():
    card = CardEnvelope.from_text("Content.", source="test.md")
    card.decay()
    assert card.state == "decayed"
