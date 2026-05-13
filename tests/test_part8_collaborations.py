"""Tests for scripts/part8_collaborations.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part8_collaborations")


# ── COLLAB_KEYWORDS ───────────────────────────────────────────────────────────

def test_collab_keywords_is_dict():
    assert isinstance(mod.COLLAB_KEYWORDS, dict)
    assert len(mod.COLLAB_KEYWORDS) > 0


def test_collab_keywords_values_are_tuples():
    for key, val in mod.COLLAB_KEYWORDS.items():
        assert isinstance(val, tuple)
        assert len(val) == 2


def test_collab_keywords_filenames_are_md():
    for key, (fname, _) in mod.COLLAB_KEYWORDS.items():
        assert fname.endswith(".md")


def test_collab_keywords_has_agentfs():
    assert any("agentfs" in k.lower() or "AgentFS" in k for k in mod.COLLAB_KEYWORDS)


def test_collab_keywords_has_crdt():
    assert any("crdt" in k.lower() or "CRDT" in k for k in mod.COLLAB_KEYWORDS)


def test_collab_mhtml_is_path():
    assert isinstance(mod.COLLAB_MHTML, Path)


# ── HABR_KEYWORDS ─────────────────────────────────────────────────────────────

def test_habr_keywords_is_dict():
    assert isinstance(mod.HABR_KEYWORDS, dict)
    assert len(mod.HABR_KEYWORDS) > 0


def test_habr_keywords_values_are_tuples():
    for key, val in mod.HABR_KEYWORDS.items():
        assert isinstance(val, tuple)
        assert len(val) == 2


def test_habr_keywords_filenames_are_md():
    for key, (fname, _) in mod.HABR_KEYWORDS.items():
        assert fname.endswith(".md")


def test_habr_keywords_has_yodoca():
    assert any("yodoca" in k.lower() or "Yodoca" in k for k in mod.HABR_KEYWORDS)


def test_habr_keywords_has_agentfs():
    assert any("agentfs" in k.lower() or "AgentFS" in k for k in mod.HABR_KEYWORDS)


def test_habr_keywords_has_ngt():
    assert any("ngt" in k.lower() or "NGT" in k for k in mod.HABR_KEYWORDS)


def test_habr_mhtml_is_path():
    assert isinstance(mod.HABR_MHTML, Path)


def test_habr_keywords_displays_are_strings():
    for key, (fname, display) in mod.HABR_KEYWORDS.items():
        assert isinstance(display, str)
        assert len(display) > 0


def test_run_calls_extract_and_split(monkeypatch, capsys):
    """Lines 46-50: run() calls extract_and_split for both sections."""
    call_count = [0]
    def fake_extract(mhtml_path, keywords, out_dir):
        call_count[0] += 1
    monkeypatch.setattr(mod, "extract_and_split", fake_extract)
    mod.run()
    assert call_count[0] == 2  # called for both collab and habr


def test_run_prints_headers(monkeypatch, capsys):
    """Lines 47, 50: run() prints headers for each section."""
    monkeypatch.setattr(mod, "extract_and_split", lambda *a: None)
    mod.run()
    out = capsys.readouterr().out
    assert "AI Collaborations" in out or "Habr" in out or "---" in out
