"""Tests for ask() read-receipt integration (Sprint 60 / S7)."""
from __future__ import annotations

from pathlib import Path

import pytest

from docstoolkit.conversation.profile import ProfileStore, UserProfile
from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


class _StubRetriever:
    def __init__(self, passages):
        self._p = passages

    def search(self, query, top_k):
        return list(self._p[:top_k])


class _StubAnswerer:
    def answer(self, system, user, model=""):
        return "stub", 0, 0.0


@pytest.fixture
def patched(monkeypatch, tmp_path):
    """Patch pipeline + ProfileStore to use a tmp DB."""
    import docstoolkit.rag.pipeline as mod
    import docstoolkit.conversation.profile as prof

    db_path = tmp_path / "profiles.sqlite"
    real_store_cls = prof.ProfileStore

    def _make_store(db_path=None):
        return real_store_cls(db_path=db_path or tmp_path / "profiles.sqlite")

    monkeypatch.setattr(mod, "Retriever",
                        lambda **kw: _StubRetriever([
                            Passage(text="t1", doc_id="docA", score=0.9),
                            Passage(text="t2", doc_id="docB", score=0.8),
                        ]))
    monkeypatch.setattr(mod, "get_answerer",
                        lambda name, **kw: _StubAnswerer())

    # Patch ProfileStore() default path to tmp
    orig_init = real_store_cls.__init__

    def _init_with_tmp(self, db_path_arg=None):
        orig_init(self, db_path=db_path_arg if db_path_arg else db_path)

    monkeypatch.setattr(real_store_cls, "__init__", _init_with_tmp)
    yield db_path


def test_read_receipts_marked_for_known_user(patched):
    # Seed user
    store = ProfileStore()
    store.save(UserProfile(user_id="alice"))
    store.close()

    ask("hello", user_id="alice", top_k=2)

    store = ProfileStore()
    p = store.load("alice")
    store.close()
    assert p is not None
    assert "docA" in p.read_docs
    assert "docB" in p.read_docs


def test_read_receipts_no_user_no_writes(patched):
    ask("hello", top_k=2)  # no user_id
    store = ProfileStore()
    assert store.list_users() == []
    store.close()


def test_read_receipts_creates_user_if_absent(patched):
    """Even brand-new users get profile created on first ask()."""
    ask("hello", user_id="bob", top_k=2)
    store = ProfileStore()
    p = store.load("bob")
    store.close()
    assert p is not None
    assert "docA" in p.read_docs


def test_read_receipts_accumulate(patched):
    store = ProfileStore()
    store.save(UserProfile(user_id="alice"))
    store.close()

    ask("q1", user_id="alice", top_k=1)  # marks docA
    ask("q2", user_id="alice", top_k=2)  # marks docA, docB

    store = ProfileStore()
    p = store.load("alice")
    store.close()
    assert p.read_docs == {"docA", "docB"}
