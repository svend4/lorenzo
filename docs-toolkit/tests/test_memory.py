"""Tests for the tiered memory module (MemGPT-style)."""
import pytest
import time

from docstoolkit.memory import (
    WorkingMemory,
    RecallMemory,
    ArchivalMemory,
    RecallItem,
    ArchivalFact,
    TieredMemory,
    MemoryTools,
    build_memory_tools,
)


# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def working():
    return WorkingMemory(max_messages=5)


@pytest.fixture
def recall():
    return RecallMemory(db_path=":memory:", user_id="test_user")


@pytest.fixture
def archival():
    return ArchivalMemory(db_path=":memory:", user_id="test_user")


@pytest.fixture
def tiered():
    return TieredMemory(db_path=":memory:", user_id="test_user", working_max=5)


@pytest.fixture
def tools():
    return build_memory_tools(db_path=":memory:", user_id="test_tools")


# ── WorkingMemory tests ────────────────────────────────────────────────────

class TestWorkingMemory:
    def test_add_single_message(self, working):
        working.add("user", "Hello world")
        assert len(working.messages) == 1

    def test_add_preserves_role(self, working):
        working.add("assistant", "Hello back")
        assert working.messages[0]["role"] == "assistant"

    def test_add_preserves_content(self, working):
        working.add("user", "Test content")
        assert working.messages[0]["content"] == "Test content"

    def test_add_includes_ts(self, working):
        working.add("user", "Timestamped")
        assert "ts" in working.messages[0]
        assert working.messages[0]["ts"]

    def test_to_context_round_trip(self, working):
        working.add("user", "Hello")
        working.add("assistant", "World")
        ctx = working.to_context()
        assert "Hello" in ctx
        assert "World" in ctx

    def test_to_context_contains_all_messages(self, working):
        msgs = [("user", "Msg A"), ("assistant", "Msg B"), ("user", "Msg C")]
        for role, content in msgs:
            working.add(role, content)
        ctx = working.to_context()
        for _, content in msgs:
            assert content in ctx

    def test_to_context_contains_roles(self, working):
        working.add("user", "Hello")
        ctx = working.to_context()
        assert "user" in ctx

    def test_to_context_empty(self, working):
        ctx = working.to_context()
        assert ctx == ""

    def test_max_messages_eviction(self):
        wm = WorkingMemory(max_messages=3)
        for i in range(5):
            wm.add("user", f"msg {i}")
        assert len(wm.messages) == 3

    def test_max_messages_evicts_oldest(self):
        wm = WorkingMemory(max_messages=3)
        wm.add("user", "oldest")
        wm.add("user", "middle")
        wm.add("user", "newest1")
        wm.add("user", "newest2")
        contents = [m["content"] for m in wm.messages]
        assert "oldest" not in contents
        assert "newest2" in contents

    def test_clear_empties_messages(self, working):
        working.add("user", "Should be cleared")
        working.add("assistant", "Also cleared")
        working.clear()
        assert len(working.messages) == 0

    def test_clear_idempotent(self, working):
        working.clear()
        working.clear()
        assert len(working.messages) == 0

    def test_token_estimate_rough(self, working):
        working.add("user", "a" * 100)  # 100 chars
        est = working.token_estimate()
        assert est == 25  # 100 // 4

    def test_token_estimate_multiple_messages(self, working):
        working.add("user", "a" * 80)   # 80 chars
        working.add("assistant", "b" * 40)  # 40 chars
        est = working.token_estimate()
        assert est == 30  # (80 + 40) // 4

    def test_token_estimate_empty(self, working):
        assert working.token_estimate() == 0

    def test_max_messages_default(self):
        wm = WorkingMemory()
        assert wm.max_messages == 20


# ── RecallItem / ArchivalFact dataclass tests ──────────────────────────────

class TestDataclasses:
    def test_recall_item_fields(self):
        item = RecallItem(id="abc", content="test", role="user", ts="2024-01-01")
        assert item.id == "abc"
        assert item.content == "test"
        assert item.role == "user"
        assert item.ts == "2024-01-01"

    def test_recall_item_default_tags(self):
        item = RecallItem(id="x", content="c", role="user", ts="t")
        assert item.tags == []

    def test_recall_item_default_importance(self):
        item = RecallItem(id="x", content="c", role="user", ts="t")
        assert item.importance == 0.5

    def test_recall_item_custom_tags(self):
        item = RecallItem(id="x", content="c", role="user", ts="t", tags=["a", "b"])
        assert item.tags == ["a", "b"]

    def test_archival_fact_fields(self):
        fact = ArchivalFact(id="f1", text="some fact")
        assert fact.id == "f1"
        assert fact.text == "some fact"

    def test_archival_fact_default_tags(self):
        fact = ArchivalFact(id="f1", text="fact")
        assert fact.tags == []

    def test_archival_fact_default_importance(self):
        fact = ArchivalFact(id="f1", text="fact")
        assert fact.importance == 0.5

    def test_archival_fact_default_source_ids(self):
        fact = ArchivalFact(id="f1", text="fact")
        assert fact.source_ids == []

    def test_archival_fact_default_created_ts(self):
        fact = ArchivalFact(id="f1", text="fact")
        assert fact.created_ts == ""


# ── RecallMemory tests ─────────────────────────────────────────────────────

class TestRecallMemory:
    def _make_item(self, content: str, role: str = "user") -> RecallItem:
        import uuid
        from datetime import datetime, timezone
        return RecallItem(
            id=uuid.uuid4().hex[:16],
            content=content,
            role=role,
            ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )

    def test_store_returns_id(self, recall):
        item = self._make_item("hello")
        returned_id = recall.store(item)
        assert returned_id == item.id

    def test_get_round_trip(self, recall):
        item = self._make_item("hello world")
        recall.store(item)
        fetched = recall.get(item.id)
        assert fetched is not None
        assert fetched.content == "hello world"
        assert fetched.id == item.id

    def test_get_missing_returns_none(self, recall):
        assert recall.get("nonexistent_id") is None

    def test_search_relevant_ranked_higher(self, recall):
        item_relevant = self._make_item("machine learning neural network deep learning")
        item_unrelated = self._make_item("the quick brown fox jumps over the lazy dog")
        recall.store(item_relevant)
        recall.store(item_unrelated)
        results = recall.search("neural network machine learning", top_k=2)
        assert len(results) > 0
        assert results[0].id == item_relevant.id

    def test_search_top_k_respected(self, recall):
        for i in range(10):
            recall.store(self._make_item(f"test content item {i}"))
        results = recall.search("test content", top_k=3)
        assert len(results) <= 3

    def test_search_empty_returns_empty(self, recall):
        results = recall.search("nothing here")
        assert results == []

    def test_list_recent_most_recent_first(self, recall):
        import uuid as _uuid
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        item1 = RecallItem(
            id=_uuid.uuid4().hex[:16],
            content="first message",
            role="user",
            ts=(now - timedelta(seconds=10)).isoformat(timespec="seconds"),
        )
        item2 = RecallItem(
            id=_uuid.uuid4().hex[:16],
            content="second message",
            role="user",
            ts=now.isoformat(timespec="seconds"),
        )
        recall.store(item1)
        recall.store(item2)
        recent = recall.list_recent(limit=5)
        # Most recent should be first
        contents = [r.content for r in recent]
        assert contents.index("second message") < contents.index("first message")

    def test_list_recent_limit(self, recall):
        for i in range(10):
            recall.store(self._make_item(f"msg {i}"))
        recent = recall.list_recent(limit=4)
        assert len(recent) == 4

    def test_count_matches_stored(self, recall):
        assert recall.count() == 0
        for i in range(5):
            recall.store(self._make_item(f"item {i}"))
        assert recall.count() == 5

    def test_user_isolation(self):
        """Different user_id must not see other user's items."""
        recall_a = RecallMemory(db_path=":memory:", user_id="alice")
        recall_b = RecallMemory(db_path=":memory:", user_id="bob")
        import uuid
        from datetime import datetime, timezone
        item = RecallItem(
            id=uuid.uuid4().hex[:16],
            content="alice secret",
            role="user",
            ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        recall_a.store(item)
        # Bob should see nothing
        assert recall_b.count() == 0
        assert recall_b.get(item.id) is None

    def test_user_isolation_shared_db(self, tmp_path):
        """Users sharing the same DB file are isolated."""
        db = str(tmp_path / "shared.sqlite")
        recall_a = RecallMemory(db_path=db, user_id="alice")
        recall_b = RecallMemory(db_path=db, user_id="bob")
        import uuid
        from datetime import datetime, timezone
        item = RecallItem(
            id=uuid.uuid4().hex[:16],
            content="only alice",
            role="user",
            ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        recall_a.store(item)
        assert recall_a.count() == 1
        assert recall_b.count() == 0


# ── ArchivalMemory tests ───────────────────────────────────────────────────

class TestArchivalMemory:
    def test_archive_returns_id(self, archival):
        fact_id = archival.archive("Python is great")
        assert fact_id
        assert isinstance(fact_id, str)

    def test_get_round_trip(self, archival):
        fact_id = archival.archive("the sky is blue", tags=["nature"])
        fact = archival.get(fact_id)
        assert fact is not None
        assert fact.text == "the sky is blue"
        assert "nature" in fact.tags

    def test_get_missing_returns_none(self, archival):
        assert archival.get("no_such_fact") is None

    def test_forget_returns_true_if_existed(self, archival):
        fact_id = archival.archive("temporary fact")
        result = archival.forget(fact_id)
        assert result is True

    def test_forget_returns_false_if_not_existed(self, archival):
        result = archival.forget("ghost_id")
        assert result is False

    def test_forget_removes_from_db(self, archival):
        fact_id = archival.archive("to be deleted")
        archival.forget(fact_id)
        assert archival.get(fact_id) is None

    def test_forget_removes_from_search(self, archival):
        fact_id = archival.archive("unique pattern xyz123")
        archival.forget(fact_id)
        results = archival.search("unique pattern xyz123")
        ids = [f.id for f in results]
        assert fact_id not in ids

    def test_search_by_content(self, archival):
        archival.archive("user prefers dark mode theme")
        archival.archive("user lives in New York city")
        results = archival.search("dark mode theme", top_k=5)
        texts = [f.text for f in results]
        assert any("dark mode" in t for t in texts)

    def test_list_by_tag_filters(self, archival):
        archival.archive("fact about python", tags=["python", "programming"])
        archival.archive("fact about javascript", tags=["javascript"])
        archival.archive("python version 3.12", tags=["python"])
        python_facts = archival.list_by_tag("python")
        assert len(python_facts) == 2
        for f in python_facts:
            assert "python" in f.tags

    def test_list_by_tag_empty(self, archival):
        archival.archive("some fact", tags=["other"])
        result = archival.list_by_tag("nonexistent_tag")
        assert result == []

    def test_count_matches_stored(self, archival):
        assert archival.count() == 0
        archival.archive("fact 1")
        archival.archive("fact 2")
        archival.archive("fact 3")
        assert archival.count() == 3

    def test_count_decrements_after_forget(self, archival):
        fact_id = archival.archive("deletable")
        assert archival.count() == 1
        archival.forget(fact_id)
        assert archival.count() == 0

    def test_source_ids_stored(self, archival):
        fact_id = archival.archive("derived fact", source_ids=["src1", "src2"])
        fact = archival.get(fact_id)
        assert fact.source_ids == ["src1", "src2"]

    def test_importance_stored(self, archival):
        fact_id = archival.archive("important", importance=0.9)
        fact = archival.get(fact_id)
        assert abs(fact.importance - 0.9) < 0.001


# ── TieredMemory tests ─────────────────────────────────────────────────────

class TestTieredMemory:
    def test_add_interaction_adds_to_working(self, tiered):
        tiered.add_interaction("user", "Hello tiered")
        assert len(tiered.working.messages) == 1

    def test_add_interaction_persists_to_recall(self, tiered):
        tiered.add_interaction("user", "Remembered message")
        assert tiered.recall.count() == 1

    def test_add_interaction_both_tiers_updated(self, tiered):
        tiered.add_interaction("user", "msg1")
        tiered.add_interaction("assistant", "msg2")
        assert len(tiered.working.messages) == 2
        assert tiered.recall.count() == 2

    def test_stats_has_all_keys(self, tiered):
        s = tiered.stats()
        assert "working_messages" in s
        assert "recall_count" in s
        assert "archival_count" in s
        assert "user_id" in s

    def test_stats_user_id_correct(self, tiered):
        assert tiered.stats()["user_id"] == "test_user"

    def test_stats_counts_accurate(self, tiered):
        tiered.add_interaction("user", "hello")
        tiered.archive("important fact")
        s = tiered.stats()
        assert s["working_messages"] == 1
        assert s["recall_count"] == 1
        assert s["archival_count"] == 1

    def test_squash_moves_to_recall(self, tiered):
        tiered.add_interaction("user", "msg1")
        tiered.add_interaction("assistant", "msg2")
        initial_recall = tiered.recall.count()
        # Clear working without adding to recall again (add_interaction already did)
        tiered.working.clear()
        # Now manually add messages to working to test squash
        tiered.working.add("user", "msg3")
        tiered.working.add("assistant", "msg4")
        count = tiered.squash_working_to_recall()
        assert count == 2
        assert len(tiered.working.messages) == 0
        assert tiered.recall.count() == initial_recall + 2

    def test_squash_clears_working(self, tiered):
        tiered.working.add("user", "in working")
        tiered.squash_working_to_recall()
        assert len(tiered.working.messages) == 0

    def test_squash_returns_count(self, tiered):
        tiered.working.add("user", "a")
        tiered.working.add("user", "b")
        tiered.working.add("user", "c")
        count = tiered.squash_working_to_recall()
        assert count == 3

    def test_squash_empty_returns_zero(self, tiered):
        count = tiered.squash_working_to_recall()
        assert count == 0

    def test_recall_search_delegates(self, tiered):
        tiered.add_interaction("user", "python programming language")
        results = tiered.recall_search("python", top_k=5)
        assert len(results) >= 1

    def test_archival_search_delegates(self, tiered):
        tiered.archive("python is a programming language")
        results = tiered.archival_search("python programming", top_k=5)
        assert len(results) >= 1

    def test_forget_delegates_to_archival(self, tiered):
        fact_id = tiered.archive("to forget")
        result = tiered.forget(fact_id)
        assert result is True
        assert tiered.archival.get(fact_id) is None

    def test_forget_nonexistent(self, tiered):
        result = tiered.forget("ghost_id")
        assert result is False

    def test_context_for_llm_contains_working_memory(self, tiered):
        tiered.add_interaction("user", "what is MemGPT")
        ctx = tiered.context_for_llm(query="MemGPT")
        assert "Working Memory" in ctx

    def test_context_for_llm_contains_recall(self, tiered):
        tiered.add_interaction("user", "test recall section")
        ctx = tiered.context_for_llm(query="recall")
        assert "Recall" in ctx

    def test_context_for_llm_contains_message_content(self, tiered):
        tiered.add_interaction("user", "unique_query_token_xyz")
        ctx = tiered.context_for_llm(query="unique_query_token_xyz")
        assert "unique_query_token_xyz" in ctx

    def test_context_for_llm_no_query(self, tiered):
        tiered.add_interaction("user", "some message")
        ctx = tiered.context_for_llm()
        assert "Working Memory" in ctx

    def test_archive_returns_id(self, tiered):
        fact_id = tiered.archive("test fact")
        assert fact_id
        assert isinstance(fact_id, str)


# ── MemoryTools tests ──────────────────────────────────────────────────────

class TestMemoryTools:
    def test_search_recall_returns_string(self, tools):
        tools.memory.add_interaction("user", "test message for recall")
        result = tools.search_recall("test message")
        assert isinstance(result, str)

    def test_search_recall_no_results_returns_string(self, tools):
        result = tools.search_recall("nothing here xyz")
        assert isinstance(result, str)

    def test_archive_fact_returns_confirmation(self, tools):
        result = tools.archive_fact("user likes coffee")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_archive_fact_contains_archived(self, tools):
        result = tools.archive_fact("user likes tea")
        # Should confirm archival (either "archived" or fact_id in message)
        lower = result.lower()
        assert "archived" in lower or "fact_" in result

    def test_archive_fact_with_tags(self, tools):
        result = tools.archive_fact("prefers dark theme", tags="ui,preferences")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_forget_fact_existing_returns_confirmation(self, tools):
        fact_id = tools.memory.archive("to be forgotten")
        result = tools.forget_fact(fact_id)
        assert isinstance(result, str)
        assert fact_id in result or "removed" in result.lower()

    def test_forget_fact_missing_returns_error_string(self, tools):
        """Should return error string, not raise exception."""
        result = tools.forget_fact("nonexistent_fact_id")
        assert isinstance(result, str)
        assert "not found" in result.lower() or "nonexistent" in result.lower()

    def test_forget_fact_no_exception(self, tools):
        """Must not raise any exception for missing fact."""
        try:
            tools.forget_fact("ghost_id_12345")
        except Exception as e:
            pytest.fail(f"forget_fact raised an exception: {e}")

    def test_memory_stats_returns_string(self, tools):
        result = tools.memory_stats()
        assert isinstance(result, str)

    def test_memory_stats_contains_user(self, tools):
        result = tools.memory_stats()
        assert "test_tools" in result

    def test_memory_stats_contains_counts(self, tools):
        tools.memory.add_interaction("user", "hello")
        result = tools.memory_stats()
        # Should mention numeric counts somewhere
        assert any(char.isdigit() for char in result)

    def test_list_tools_returns_list(self, tools):
        result = tools.list_tools()
        assert isinstance(result, list)

    def test_list_tools_non_empty(self, tools):
        result = tools.list_tools()
        assert len(result) > 0

    def test_list_tools_each_has_name(self, tools):
        result = tools.list_tools()
        for tool in result:
            assert "name" in tool
            assert isinstance(tool["name"], str)

    def test_list_tools_each_has_description(self, tools):
        result = tools.list_tools()
        for tool in result:
            assert "description" in tool

    def test_list_tools_each_has_parameters(self, tools):
        result = tools.list_tools()
        for tool in result:
            assert "parameters" in tool
            assert isinstance(tool["parameters"], dict)

    def test_build_memory_tools_factory(self):
        mt = build_memory_tools(db_path=":memory:", user_id="factory_test")
        assert isinstance(mt, MemoryTools)
        assert isinstance(mt.memory, TieredMemory)
        assert mt.memory._user_id == "factory_test"
