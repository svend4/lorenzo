"""Tests for the Sprint 54-92 HTTP endpoints in serve.py.

Tests the underlying _api_* helpers directly to avoid spinning up a real
HTTP server (which would need a port + threads).
"""
from __future__ import annotations

import pytest

from docstoolkit import serve as srv


def test_qbool_truthy():
    for v in ("1", "true", "yes", "on", "TRUE"):
        assert srv._qbool({"f": [v]}, "f") is True


def test_qbool_falsy_default():
    assert srv._qbool({}, "f") is False
    assert srv._qbool({"f": [""]}, "f") is False
    assert srv._qbool({"f": ["0"]}, "f") is False


def test_qint_parses():
    assert srv._qint({"k": ["42"]}, "k", 5) == 42
    assert srv._qint({}, "k", 5) == 5
    assert srv._qint({"k": ["bad"]}, "k", 5) == 5


def test_qstr_default():
    assert srv._qstr({"k": ["x"]}, "k") == "x"
    assert srv._qstr({}, "k", "fallback") == "fallback"


# ---------- /api/ask ----------

def test_api_ask_missing_q():
    out = srv._api_ask({})
    assert "error" in out


def test_api_ask_basic(monkeypatch):
    """Smoke: returns shape, even with empty corpus."""
    import docstoolkit.rag.pipeline as mod
    from docstoolkit.rag.types import Passage

    class _R:
        def search(self, q, top_k):
            return [Passage(text="t", doc_id="d", title="D", score=0.5)]

    class _A:
        def answer(self, s, u, model=""):
            return "answer", 0, 0.0

    monkeypatch.setattr(mod, "Retriever", lambda **kw: _R())
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())

    out = srv._api_ask({"q": ["hello"]})
    assert "answer" in out
    assert "passages" in out


def test_api_ask_parses_filters(monkeypatch):
    """The filters string should be parsed into a dict."""
    import docstoolkit.rag.pipeline as mod
    from docstoolkit.rag.types import Passage

    captured = {}

    class _R:
        def search(self, q, top_k):
            return [Passage(text="t", doc_id="a/x", title="A", score=0.5)]

    class _A:
        def answer(self, s, u, model=""):
            return "ok", 0, 0.0

    monkeypatch.setattr(mod, "Retriever", lambda **kw: _R())
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())

    orig_pipeline = mod.RAGPipeline

    def wrap_pipeline(query, **kw):
        captured.update(kw)
        return orig_pipeline(query, **kw)

    monkeypatch.setattr(mod, "RAGPipeline", wrap_pipeline)

    srv._api_ask({"q": ["x"], "filters": ["section:a,tag:b"]})
    assert captured.get("filters") == {"section": "a", "tag": "b"}


def test_api_ask_bool_kwargs(monkeypatch):
    """with_facets=1 should flip the kwarg."""
    import docstoolkit.rag.pipeline as mod
    from docstoolkit.rag.types import Passage

    captured = {}
    orig_pipeline = mod.RAGPipeline

    class _R:
        def search(self, q, top_k):
            return [Passage(text="t", doc_id="a", title="A", score=0.5)]

    class _A:
        def answer(self, s, u, model=""):
            return "ok", 0, 0.0

    monkeypatch.setattr(mod, "Retriever", lambda **kw: _R())
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())

    def wrap(query, **kw):
        captured.update(kw)
        return orig_pipeline(query, **kw)

    monkeypatch.setattr(mod, "RAGPipeline", wrap)
    srv._api_ask({"q": ["x"], "with_facets": ["1"], "with_provenance": ["true"]})
    assert captured.get("with_facets") is True
    assert captured.get("with_provenance") is True


# ---------- /api/saved ----------

def test_api_saved_empty(tmp_path, monkeypatch):
    from docstoolkit.alerts import AlertStore

    real = AlertStore
    monkeypatch.setattr(
        "docstoolkit.rag.saved.AlertStore",
        lambda *a, **kw: real(db_path=tmp_path / "alerts.sqlite"),
    )
    out = srv._api_saved_list({})
    assert out["total"] == 0


# ---------- /api/voice ----------

def test_api_voice_basic():
    out = srv._api_voice({"text": ["Python is great. We believe RAG matters."]})
    assert "voice" in out
    assert "text_length" in out


def test_api_voice_missing_text():
    out = srv._api_voice({})
    assert "error" in out


# ---------- /api/assets ----------

def test_api_assets_returns_list(tmp_path, monkeypatch):
    # Point load_config().docs_dir at our tmp_path
    from docstoolkit.rag import advanced as adv

    monkeypatch.setattr(adv, "ask", lambda *a, **kw: None)  # not used here
    # search_assets uses load_config — patch it
    class FakeCfg:
        docs_dir = tmp_path

    monkeypatch.setattr("docstoolkit.config.load_config", lambda: FakeCfg)
    out = srv._api_assets({"q": ["test"]})
    assert "assets" in out
    assert "total" in out


# ---------- /api/kg ----------

def test_api_kg_stats_only():
    out = srv._api_kg({})
    assert "stats" in out


def test_api_kg_with_query():
    out = srv._api_kg({"q": ["Python"], "top_k": ["3"]})
    assert "stats" in out
    assert "passages" in out


# ---------- /api/profile ----------

def test_api_profile_list_users(tmp_path, monkeypatch):
    from docstoolkit.conversation.profile import ProfileStore

    real = ProfileStore
    monkeypatch.setattr(
        "docstoolkit.conversation.profile.ProfileStore",
        lambda *a, **kw: real(db_path=tmp_path / "profiles.sqlite"),
    )
    out = srv._api_profile({})
    assert "users" in out


def test_api_profile_unknown_user(tmp_path, monkeypatch):
    from docstoolkit.conversation.profile import ProfileStore

    real = ProfileStore
    monkeypatch.setattr(
        "docstoolkit.conversation.profile.ProfileStore",
        lambda *a, **kw: real(db_path=tmp_path / "profiles.sqlite"),
    )
    out = srv._api_profile({"user_id": ["ghost"]})
    assert out["exists"] is False


# ---------- /api/diff ----------

def test_api_diff_missing_params():
    srv.DocsHandler.cfg = type("C", (), {"docs_dir": "/tmp"})()
    out = srv._api_diff({})
    assert "error" in out


# ---------- /api/taxonomy ----------

def test_api_taxonomy_missing_q():
    out = srv._api_taxonomy({})
    assert "error" in out


# ---------- /api/eval/dashboard ----------

def test_api_eval_dashboard_renders(tmp_path, monkeypatch):
    from docstoolkit.online_eval import OnlineEvalStore

    real = OnlineEvalStore
    monkeypatch.setattr(
        "docstoolkit.online_eval.OnlineEvalStore",
        lambda *a, **kw: real(db_path=tmp_path / "eval.sqlite"),
    )
    html = srv._api_eval_dashboard({})
    assert html.startswith("<!doctype html>")
