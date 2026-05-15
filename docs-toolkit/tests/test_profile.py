"""Tests for per-user profile store and personalized retrieval."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.conversation.profile import (
    UserProfile,
    ProfileStore,
    PersonalizedRetriever,
    apply_profile,
    infer_interests,
)
from docstoolkit.rag.types import Passage


# ---- Helpers ----

def _passage(doc_id: str, title: str = "", text: str = "",
             score: float = 0.5) -> Passage:
    return Passage(text=text, doc_id=doc_id, title=title, score=score)


# ---- ProfileStore ----

@pytest.fixture
def store(tmp_path):
    s = ProfileStore(db_path=tmp_path / "profiles.sqlite")
    yield s
    s.close()


def test_profile_save_and_load(store):
    p = UserProfile(
        user_id="alice",
        interests=["memory", "RAG"],
        read_docs={"doc1", "doc2"},
        preferred_sections=["05-habr-projects"],
        preferred_retriever="bm25",
    )
    store.save(p)
    loaded = store.load("alice")
    assert loaded is not None
    assert loaded.user_id == "alice"
    assert loaded.interests == ["memory", "RAG"]
    assert loaded.read_docs == {"doc1", "doc2"}
    assert loaded.preferred_sections == ["05-habr-projects"]
    assert loaded.preferred_retriever == "bm25"


def test_profile_load_missing_returns_none(store):
    assert store.load("nobody") is None


def test_profile_save_updates_updated_ts(store):
    p = UserProfile(user_id="bob")
    store.save(p)
    first_ts = store.load("bob").updated_ts
    import time as _t; _t.sleep(1)
    store.save(p)
    second_ts = store.load("bob").updated_ts
    assert second_ts >= first_ts


def test_profile_upsert_overwrites(store):
    p = UserProfile(user_id="carol", interests=["x"])
    store.save(p)
    p.interests = ["y", "z"]
    store.save(p)
    loaded = store.load("carol")
    assert loaded.interests == ["y", "z"]


def test_mark_read_new_user(store):
    store.mark_read("dave", "doc_a")
    profile = store.load("dave")
    assert profile is not None
    assert "doc_a" in profile.read_docs


def test_mark_read_existing_user(store):
    p = UserProfile(user_id="eve", read_docs={"doc1"})
    store.save(p)
    store.mark_read("eve", "doc2")
    loaded = store.load("eve")
    assert "doc1" in loaded.read_docs
    assert "doc2" in loaded.read_docs


def test_update_interests_merges(store):
    p = UserProfile(user_id="frank", interests=["memory", "agents"])
    store.save(p)
    store.update_interests("frank", ["RAG", "agents", "search"])
    loaded = store.load("frank")
    # Original preserved, new added, no duplicates
    assert "memory" in loaded.interests
    assert "agents" in loaded.interests
    assert "RAG" in loaded.interests
    assert "search" in loaded.interests
    assert loaded.interests.count("agents") == 1


def test_update_interests_caps_at_50(store):
    p = UserProfile(user_id="grace",
                    interests=[f"term{i}" for i in range(48)])
    store.save(p)
    store.update_interests("grace", ["new1", "new2", "new3", "new4"])
    loaded = store.load("grace")
    assert len(loaded.interests) <= 50


def test_update_interests_new_user(store):
    store.update_interests("henry", ["topic1", "topic2"])
    loaded = store.load("henry")
    assert "topic1" in loaded.interests


def test_list_users(store):
    store.save(UserProfile(user_id="u1"))
    store.save(UserProfile(user_id="u2"))
    store.save(UserProfile(user_id="u3"))
    users = store.list_users()
    assert set(users) == {"u1", "u2", "u3"}


def test_list_users_empty(store):
    assert store.list_users() == []


def test_profile_default_timestamps():
    p = UserProfile(user_id="test")
    assert p.created_ts != ""
    assert p.updated_ts != ""
    assert p.updated_ts == p.created_ts


# ---- PersonalizedRetriever ----

class MockRetriever:
    """Simple mock that returns preset passages."""

    def __init__(self, passages: list[Passage]):
        self._passages = passages
        self.last_query: str = ""

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        self.last_query = query
        return self._passages[:top_k]


def test_personalized_returns_top_k():
    profile = UserProfile(user_id="u1")
    passages = [_passage(f"doc{i}", score=0.5) for i in range(10)]
    base = MockRetriever(passages)
    pr = PersonalizedRetriever(base, profile)
    results = pr.search("query", top_k=3)
    assert len(results) == 3


def test_personalized_boosts_preferred_section():
    profile = UserProfile(
        user_id="u1",
        preferred_sections=["05-habr-projects"],
    )
    passages = [
        _passage("05-habr-projects/agentfs", score=0.5),
        _passage("01-svyazi/intro", score=0.6),
        _passage("01-svyazi/arch", score=0.55),
    ]
    base = MockRetriever(passages * 2)  # enough for top_k * 2
    pr = PersonalizedRetriever(base, profile)
    results = pr.search("agents", top_k=3)
    # The preferred-section doc should end up highly ranked
    top_doc_ids = [r.doc_id for r in results]
    assert "05-habr-projects/agentfs" in top_doc_ids
    # Score should be boosted by 0.2
    preferred_result = next(r for r in results
                            if r.doc_id == "05-habr-projects/agentfs")
    assert preferred_result.score >= 0.5 + 0.2 - 1e-6


def test_personalized_penalizes_read_docs():
    profile = UserProfile(
        user_id="u1",
        read_docs={"doc_read"},
    )
    passages = [
        _passage("doc_read", score=0.9),
        _passage("doc_fresh", score=0.8),
    ]
    base = MockRetriever(passages * 2)
    pr = PersonalizedRetriever(base, profile)
    results = pr.search("query", top_k=2)
    read_result = next((r for r in results if r.doc_id == "doc_read"), None)
    if read_result:
        # Penalized by 0.1
        assert read_result.score <= 0.9 - 0.1 + 1e-6


def test_personalized_injects_interests_into_query():
    profile = UserProfile(
        user_id="u1",
        interests=["memory", "RAG"],
    )
    passages = [_passage(f"doc{i}", score=0.5) for i in range(10)]
    base = MockRetriever(passages)
    pr = PersonalizedRetriever(base, profile)
    pr.search("agents", top_k=3)
    # Interests should be appended to query
    assert "memory" in base.last_query or "RAG" in base.last_query


def test_personalized_no_interest_duplication():
    profile = UserProfile(
        user_id="u1",
        interests=["agents"],
    )
    passages = [_passage(f"doc{i}", score=0.5) for i in range(10)]
    base = MockRetriever(passages)
    pr = PersonalizedRetriever(base, profile)
    pr.search("agents topic", top_k=3)
    # "agents" is already in the query — should not be doubled
    assert base.last_query.count("agents") == 1


def test_personalized_empty_profile():
    profile = UserProfile(user_id="u1")
    passages = [_passage("d1", score=0.7), _passage("d2", score=0.6)]
    base = MockRetriever(passages * 2)
    pr = PersonalizedRetriever(base, profile)
    results = pr.search("query", top_k=2)
    assert len(results) == 2


# ---- infer_interests ----

def test_infer_interests_returns_top_n():
    passages = [
        _passage("d1", title="memory agents", text="memory storage agents retrieval"),
        _passage("d2", title="memory cache", text="memory cache performance agents"),
        _passage("d3", title="RAG pipeline", text="retrieval augmented generation RAG"),
    ]
    interests = infer_interests(passages, top_n=5)
    assert len(interests) <= 5
    assert isinstance(interests, list)
    assert all(isinstance(t, str) for t in interests)


def test_infer_interests_filters_stopwords():
    passages = [
        _passage("d1", text="the and or but for of with это и в"),
    ]
    interests = infer_interests(passages, top_n=10)
    stopwords = {"the", "and", "or", "but", "for", "of", "with",
                 "это", "и", "в"}
    for term in interests:
        assert term.lower() not in stopwords


def test_infer_interests_most_frequent_first():
    passages = [
        _passage(f"d{i}", text="memory memory memory agents")
        for i in range(5)
    ]
    interests = infer_interests(passages, top_n=3)
    if interests:
        assert interests[0] in ("memory", "agents")


def test_infer_interests_empty():
    assert infer_interests([], top_n=5) == []


# ---- apply_profile middleware (Sprint 54 / S6) ----

def test_apply_profile_unknown_user_noop(store):
    kwargs = {"top_k": 5, "method": "hybrid"}
    out = apply_profile("ghost", kwargs, store=store)
    assert out is kwargs
    assert "_profile" not in out


def test_apply_profile_loads_known_user(store):
    p = UserProfile(user_id="alice", preferred_retriever="bm25")
    store.save(p)
    kwargs = {"top_k": 5}
    out = apply_profile("alice", kwargs, store=store)
    assert out["method"] == "bm25"
    assert out["_profile"].user_id == "alice"


def test_apply_profile_does_not_overwrite_caller_method(store):
    p = UserProfile(user_id="alice", preferred_retriever="bm25")
    store.save(p)
    kwargs = {"method": "semantic"}
    out = apply_profile("alice", kwargs, store=store)
    assert out["method"] == "semantic"
    assert out["_profile"].user_id == "alice"


def test_apply_profile_returns_same_dict_for_chaining(store):
    p = UserProfile(user_id="bob", preferred_retriever="keyword")
    store.save(p)
    kwargs = {}
    assert apply_profile("bob", kwargs, store=store) is kwargs
