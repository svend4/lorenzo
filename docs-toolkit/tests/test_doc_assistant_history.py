"""Tests for docstoolkit.doc_assistant_history."""
import threading

import pytest

from docstoolkit.doc_assistant_history import (
    ConversationSummary,
    DocAssistantHistory,
    Turn,
    TurnRole,
)


# --------------------------------------------------------------------- helpers
def _h(max_turns=50, max_tokens=16000):
    return DocAssistantHistory(max_turns=max_turns, max_tokens=max_tokens)


def _seed(h, n=3, cid=None, role=TurnRole.USER, base_now=0.0):
    if cid is None:
        cid = h.create_conversation(now=base_now)
    for i in range(n):
        h.add_turn(cid, role, f"msg-{i}", tokens=5, now=base_now + i + 1)
    return cid


# --------------------------------------------------------------------- TurnRole
class TestTurnRole:
    def test_user(self):
        assert TurnRole.USER.value == "user"

    def test_assistant(self):
        assert TurnRole.ASSISTANT.value == "assistant"

    def test_system(self):
        assert TurnRole.SYSTEM.value == "system"

    def test_tool(self):
        assert TurnRole.TOOL.value == "tool"

    def test_distinct(self):
        roles = {TurnRole.USER, TurnRole.ASSISTANT, TurnRole.SYSTEM, TurnRole.TOOL}
        assert len(roles) == 4


# --------------------------------------------------------------------- Turn
class TestTurn:
    def test_create(self):
        t = Turn(turn_id=1, role=TurnRole.USER, content="hi", created_at=1.0)
        assert t.turn_id == 1
        assert t.role == TurnRole.USER
        assert t.content == "hi"
        assert t.created_at == 1.0

    def test_defaults(self):
        t = Turn(turn_id=2, role=TurnRole.SYSTEM, content="x", created_at=0.0)
        assert t.tokens == 0
        assert t.metadata == {}

    def test_metadata_independent(self):
        a = Turn(1, TurnRole.USER, "a", 0.0)
        b = Turn(2, TurnRole.USER, "b", 0.0)
        a.metadata["k"] = 1
        assert b.metadata == {}


# ---------------------------------------------------- ConversationSummary
class TestConversationSummary:
    def test_create(self):
        s = ConversationSummary(
            conversation_id="c1",
            turn_count=3,
            total_tokens=10,
            started_at=1.0,
            last_activity_at=2.0,
            roles_used={"user"},
        )
        assert s.conversation_id == "c1"
        assert s.turn_count == 3
        assert s.total_tokens == 10
        assert s.started_at == 1.0
        assert s.last_activity_at == 2.0
        assert s.roles_used == {"user"}


# ------------------------------------------------------ CreateConversation
class TestCreateConversation:
    def test_returns_id(self):
        h = _h()
        cid = h.create_conversation()
        assert isinstance(cid, str)
        assert len(cid) > 0

    def test_custom_id(self):
        h = _h()
        cid = h.create_conversation(conversation_id="my-conv")
        assert cid == "my-conv"

    def test_duplicate_raises(self):
        h = _h()
        h.create_conversation(conversation_id="x")
        with pytest.raises(ValueError):
            h.create_conversation(conversation_id="x")

    def test_with_system_prompt(self):
        h = _h()
        cid = h.create_conversation(system_prompt="You are an editor.", now=1.0)
        turns = h.get_conversation(cid)
        assert len(turns) == 1
        assert turns[0].role == TurnRole.SYSTEM
        assert turns[0].content == "You are an editor."
        assert turns[0].created_at == 1.0

    def test_without_system_prompt(self):
        h = _h()
        cid = h.create_conversation()
        assert h.get_conversation(cid) == []

    def test_unique_default_ids(self):
        h = _h()
        ids = {h.create_conversation() for _ in range(5)}
        assert len(ids) == 5


# ----------------------------------------------------------- AddTurn
class TestAddTurn:
    def test_basic(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "hello", now=1.0)
        assert isinstance(t, Turn)
        assert t.role == TurnRole.USER
        assert t.content == "hello"
        assert t.created_at == 1.0

    def test_turn_ids_increment(self):
        h = _h()
        cid = h.create_conversation()
        t1 = h.add_turn(cid, TurnRole.USER, "a")
        t2 = h.add_turn(cid, TurnRole.USER, "b")
        assert t2.turn_id == t1.turn_id + 1

    def test_token_estimation(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "one two three four")
        assert t.tokens == 4

    def test_explicit_tokens(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "hi", tokens=99)
        assert t.tokens == 99

    def test_with_metadata(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "hi", metadata={"src": "ui"})
        assert t.metadata == {"src": "ui"}

    def test_missing_conversation_returns_none(self):
        h = _h()
        assert h.add_turn("nope", TurnRole.USER, "x") is None

    def test_invalid_role_raises(self):
        h = _h()
        cid = h.create_conversation()
        with pytest.raises(TypeError):
            h.add_turn(cid, "user", "x")  # type: ignore

    def test_empty_content(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "")
        assert t.tokens == 0
        assert t.content == ""

    def test_negative_tokens_raises(self):
        h = _h()
        cid = h.create_conversation()
        with pytest.raises(ValueError):
            h.add_turn(cid, TurnRole.USER, "x", tokens=-1)


# ----------------------------------------------------------- GetTurn
class TestGetTurn:
    def test_get_existing(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "hi")
        got = h.get_turn(cid, t.turn_id)
        assert got is t

    def test_missing_turn(self):
        h = _h()
        cid = h.create_conversation()
        assert h.get_turn(cid, 999) is None

    def test_missing_conversation(self):
        h = _h()
        assert h.get_turn("nope", 1) is None


# ------------------------------------------------------ GetConversation
class TestGetConversation:
    def test_oldest_first(self):
        h = _h()
        cid = _seed(h, n=3)
        turns = h.get_conversation(cid)
        assert [t.content for t in turns] == ["msg-0", "msg-1", "msg-2"]

    def test_empty(self):
        h = _h()
        cid = h.create_conversation()
        assert h.get_conversation(cid) == []

    def test_missing(self):
        h = _h()
        assert h.get_conversation("nope") == []

    def test_limit(self):
        h = _h()
        cid = _seed(h, n=5)
        turns = h.get_conversation(cid, limit=2)
        assert [t.content for t in turns] == ["msg-3", "msg-4"]

    def test_limit_zero(self):
        h = _h()
        cid = _seed(h, n=3)
        assert h.get_conversation(cid, limit=0) == []

    def test_returns_copy(self):
        h = _h()
        cid = _seed(h, n=2)
        turns = h.get_conversation(cid)
        turns.clear()
        assert len(h.get_conversation(cid)) == 2


# ----------------------------------------------------------- RecentTurns
class TestRecentTurns:
    def test_default(self):
        h = _h()
        cid = _seed(h, n=5)
        recent = h.recent_turns(cid)
        assert len(recent) == 5

    def test_n(self):
        h = _h()
        cid = _seed(h, n=5)
        recent = h.recent_turns(cid, n=2)
        assert [t.content for t in recent] == ["msg-3", "msg-4"]

    def test_n_zero(self):
        h = _h()
        cid = _seed(h, n=2)
        assert h.recent_turns(cid, n=0) == []

    def test_empty(self):
        h = _h()
        cid = h.create_conversation()
        assert h.recent_turns(cid) == []

    def test_missing(self):
        h = _h()
        assert h.recent_turns("nope") == []


# ----------------------------------------------------------- LastTurn
class TestLastTurn:
    def test_last(self):
        h = _h()
        cid = _seed(h, n=3)
        last = h.last_turn(cid)
        assert last.content == "msg-2"

    def test_empty(self):
        h = _h()
        cid = h.create_conversation()
        assert h.last_turn(cid) is None

    def test_missing(self):
        h = _h()
        assert h.last_turn("nope") is None


# ----------------------------------------------------------- GetContext
class TestGetContext:
    def test_empty(self):
        h = _h()
        cid = h.create_conversation()
        assert h.get_context(cid) == []

    def test_missing(self):
        h = _h()
        assert h.get_context("nope") == []

    def test_all_fit(self):
        h = _h(max_tokens=1000)
        cid = _seed(h, n=3)  # 3 * 5 tokens
        ctx = h.get_context(cid)
        assert len(ctx) == 3

    def test_chronological(self):
        h = _h(max_tokens=1000)
        cid = _seed(h, n=4)
        ctx = h.get_context(cid)
        assert [t.content for t in ctx] == ["msg-0", "msg-1", "msg-2", "msg-3"]


# ----------------------------------------------- GetContextTokenBudget
class TestGetContextTokenBudget:
    def test_budget_limits(self):
        h = _h(max_tokens=1000)
        cid = h.create_conversation()
        for i in range(5):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=10)
        ctx = h.get_context(cid, max_tokens=25)
        # Only fits 2 latest (10+10=20, next 10 would exceed 25)
        assert len(ctx) == 2
        assert ctx[-1].content == "m4"
        assert ctx[0].content == "m3"

    def test_exact_fit(self):
        h = _h()
        cid = h.create_conversation()
        for i in range(3):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=10)
        ctx = h.get_context(cid, max_tokens=20)
        assert len(ctx) == 2

    def test_budget_zero(self):
        h = _h()
        cid = h.create_conversation()
        h.add_turn(cid, TurnRole.USER, "x", tokens=5)
        ctx = h.get_context(cid, max_tokens=0)
        assert ctx == []

    def test_negative_budget_treated_zero(self):
        h = _h()
        cid = h.create_conversation()
        h.add_turn(cid, TurnRole.USER, "x", tokens=5)
        ctx = h.get_context(cid, max_tokens=-5)
        assert ctx == []

    def test_default_budget_is_max_tokens(self):
        h = _h(max_tokens=15)
        cid = h.create_conversation()
        for i in range(5):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=5)
        # After auto-prune max_tokens=15 → 3 turns survive
        ctx = h.get_context(cid)
        assert sum(t.tokens for t in ctx) <= 15


# --------------------------------------------- GetContextPreservesSystem
class TestGetContextPreservesSystem:
    def test_system_always_included(self):
        h = _h()
        cid = h.create_conversation(system_prompt="SYS", now=0.0)
        for i in range(5):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=10, now=i + 1)
        ctx = h.get_context(cid, max_tokens=25)
        roles = [t.role for t in ctx]
        assert TurnRole.SYSTEM in roles
        # The system turn must appear first by chronological order
        assert ctx[0].role == TurnRole.SYSTEM

    def test_system_excluded_from_budget_calc_only_via_priority(self):
        h = _h()
        cid = h.create_conversation()
        h.add_turn(cid, TurnRole.SYSTEM, "x", tokens=5)
        h.add_turn(cid, TurnRole.USER, "u1", tokens=5)
        h.add_turn(cid, TurnRole.USER, "u2", tokens=5)
        ctx = h.get_context(cid, max_tokens=10)
        # system (5) + one user (5) = 10
        assert len(ctx) == 2
        assert any(t.role == TurnRole.SYSTEM for t in ctx)

    def test_only_system(self):
        h = _h()
        cid = h.create_conversation(system_prompt="SYS")
        ctx = h.get_context(cid, max_tokens=1000)
        assert len(ctx) == 1
        assert ctx[0].role == TurnRole.SYSTEM


# ----------------------------------------------------- ClearConversation
class TestClearConversation:
    def test_returns_count(self):
        h = _h()
        cid = _seed(h, n=4)
        assert h.clear_conversation(cid) == 4

    def test_empty_after(self):
        h = _h()
        cid = _seed(h, n=3)
        h.clear_conversation(cid)
        assert h.get_conversation(cid) == []

    def test_conversation_still_exists(self):
        h = _h()
        cid = _seed(h, n=2)
        h.clear_conversation(cid)
        assert cid in h.all_conversation_ids()

    def test_missing(self):
        h = _h()
        assert h.clear_conversation("nope") == 0


# ----------------------------------------------------------- PruneToMax
class TestPruneToMax:
    def test_no_prune_when_under(self):
        h = _h(max_turns=10, max_tokens=1000)
        cid = _seed(h, n=3)
        assert h.prune_to_max(cid) == 0
        assert len(h.get_conversation(cid)) == 3

    def test_prune_by_turn_count(self):
        h = _h(max_turns=3, max_tokens=10000)
        cid = h.create_conversation()
        for i in range(5):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=1)
        # Auto-pruned during add; explicit call drops 0
        assert len(h.get_conversation(cid)) == 3
        assert h.prune_to_max(cid) == 0

    def test_prune_drops_oldest(self):
        h = _h(max_turns=2, max_tokens=10000)
        cid = h.create_conversation()
        for i in range(4):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=1)
        turns = h.get_conversation(cid)
        assert [t.content for t in turns] == ["m2", "m3"]

    def test_prune_by_tokens(self):
        h = _h(max_turns=100, max_tokens=10)
        cid = h.create_conversation()
        for i in range(5):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=4)
        # Should be pruned to total_tokens <= 10
        assert sum(t.tokens for t in h.get_conversation(cid)) <= 10

    def test_prune_missing(self):
        h = _h()
        assert h.prune_to_max("nope") == 0

    def test_prune_returns_dropped_count(self):
        h = _h(max_turns=100, max_tokens=100)
        cid = h.create_conversation()
        for i in range(3):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=10)
        # Now shrink limits and prune
        h.max_turns = 1
        assert h.prune_to_max(cid) == 2


# --------------------------------------------------- PrunePreservesSystem
class TestPrunePreservesSystem:
    def test_system_kept_when_over_turn_limit(self):
        h = _h(max_turns=2, max_tokens=10000)
        cid = h.create_conversation(system_prompt="SYS")
        for i in range(5):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=1)
        turns = h.get_conversation(cid)
        assert any(t.role == TurnRole.SYSTEM for t in turns)

    def test_system_kept_when_over_token_limit(self):
        h = _h(max_turns=100, max_tokens=10)
        cid = h.create_conversation(system_prompt="SYS", now=0.0)  # 1 token
        for i in range(10):
            h.add_turn(cid, TurnRole.USER, f"m{i}", tokens=5)
        turns = h.get_conversation(cid)
        assert any(t.role == TurnRole.SYSTEM for t in turns)

    def test_all_system_no_drop(self):
        h = _h(max_turns=1, max_tokens=1)
        cid = h.create_conversation()
        h.add_turn(cid, TurnRole.SYSTEM, "s1", tokens=5)
        h.add_turn(cid, TurnRole.SYSTEM, "s2", tokens=5)
        h.add_turn(cid, TurnRole.SYSTEM, "s3", tokens=5)
        # All system: pruning cannot drop them
        assert len(h.get_conversation(cid)) == 3


# ----------------------------------------------------------- Summary
class TestSummary:
    def test_basic(self):
        h = _h()
        cid = h.create_conversation(now=1.0)
        h.add_turn(cid, TurnRole.USER, "hi", tokens=3, now=2.0)
        h.add_turn(cid, TurnRole.ASSISTANT, "yo", tokens=2, now=3.0)
        s = h.summary(cid)
        assert s.conversation_id == cid
        assert s.turn_count == 2
        assert s.total_tokens == 5
        assert s.started_at == 1.0
        assert s.last_activity_at == 3.0
        assert s.roles_used == {"user", "assistant"}

    def test_empty(self):
        h = _h()
        cid = h.create_conversation(now=5.0)
        s = h.summary(cid)
        assert s.turn_count == 0
        assert s.total_tokens == 0
        assert s.roles_used == set()
        assert s.started_at == 5.0

    def test_missing(self):
        h = _h()
        assert h.summary("nope") is None

    def test_with_system(self):
        h = _h()
        cid = h.create_conversation(system_prompt="S", now=1.0)
        h.add_turn(cid, TurnRole.USER, "hi", now=2.0)
        s = h.summary(cid)
        assert "system" in s.roles_used
        assert "user" in s.roles_used


# ------------------------------------------------------ ConversationCount
class TestConversationCount:
    def test_zero(self):
        h = _h()
        assert h.conversation_count == 0

    def test_increments(self):
        h = _h()
        h.create_conversation()
        h.create_conversation()
        assert h.conversation_count == 2

    def test_decrements_on_delete(self):
        h = _h()
        cid = h.create_conversation()
        h.delete_conversation(cid)
        assert h.conversation_count == 0


# ----------------------------------------------------------- TotalTurns
class TestTotalTurns:
    def test_zero(self):
        h = _h()
        assert h.total_turns == 0

    def test_counts_across_conversations(self):
        h = _h()
        c1 = h.create_conversation()
        c2 = h.create_conversation()
        h.add_turn(c1, TurnRole.USER, "a", tokens=1)
        h.add_turn(c2, TurnRole.USER, "b", tokens=1)
        h.add_turn(c2, TurnRole.USER, "c", tokens=1)
        assert h.total_turns == 3

    def test_includes_system(self):
        h = _h()
        h.create_conversation(system_prompt="S")
        assert h.total_turns == 1


# ------------------------------------------------ AllConversationIds
class TestAllConversationIds:
    def test_empty(self):
        h = _h()
        assert h.all_conversation_ids() == []

    def test_multiple(self):
        h = _h()
        c1 = h.create_conversation(conversation_id="a")
        c2 = h.create_conversation(conversation_id="b")
        ids = h.all_conversation_ids()
        assert set(ids) == {"a", "b"}


# ------------------------------------------------- DeleteConversation
class TestDeleteConversation:
    def test_returns_true(self):
        h = _h()
        cid = h.create_conversation()
        assert h.delete_conversation(cid) is True

    def test_removes(self):
        h = _h()
        cid = h.create_conversation()
        h.delete_conversation(cid)
        assert cid not in h.all_conversation_ids()

    def test_missing(self):
        h = _h()
        assert h.delete_conversation("nope") is False

    def test_can_recreate_after_delete(self):
        h = _h()
        h.create_conversation(conversation_id="x")
        h.delete_conversation("x")
        # No exception
        h.create_conversation(conversation_id="x")
        assert "x" in h.all_conversation_ids()


# ----------------------------------------------------------- Clear
class TestClear:
    def test_clear_removes_all(self):
        h = _h()
        h.create_conversation()
        h.create_conversation()
        h.clear()
        assert h.conversation_count == 0

    def test_clear_resets_total_turns(self):
        h = _h()
        cid = h.create_conversation()
        h.add_turn(cid, TurnRole.USER, "hi")
        h.clear()
        assert h.total_turns == 0

    def test_clear_idempotent(self):
        h = _h()
        h.clear()
        h.clear()
        assert h.conversation_count == 0


# ----------------------------------------------------------- EdgeCases
class TestEdgeCases:
    def test_invalid_max_turns(self):
        with pytest.raises(ValueError):
            DocAssistantHistory(max_turns=0)

    def test_invalid_max_tokens(self):
        with pytest.raises(ValueError):
            DocAssistantHistory(max_turns=10, max_tokens=0)

    def test_empty_content_zero_tokens(self):
        h = _h()
        cid = h.create_conversation()
        t = h.add_turn(cid, TurnRole.USER, "")
        assert t.tokens == 0

    def test_thread_safety(self):
        h = _h(max_turns=1000, max_tokens=100000)
        cid = h.create_conversation()

        def worker():
            for i in range(50):
                h.add_turn(cid, TurnRole.USER, f"t{i}", tokens=1)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(h.get_conversation(cid)) == 200

    def test_metadata_is_copied(self):
        h = _h()
        cid = h.create_conversation()
        md = {"k": "v"}
        t = h.add_turn(cid, TurnRole.USER, "hi", metadata=md)
        md["k"] = "changed"
        assert t.metadata["k"] == "v"

    def test_get_conversation_negative_limit(self):
        h = _h()
        cid = _seed(h, n=3)
        # Negative limit treated as zero
        assert h.get_conversation(cid, limit=-1) == []

    def test_summary_after_clear_conversation(self):
        h = _h()
        cid = h.create_conversation(now=10.0)
        h.add_turn(cid, TurnRole.USER, "hi")
        h.clear_conversation(cid)
        s = h.summary(cid)
        assert s is not None
        assert s.turn_count == 0

    def test_recent_turns_more_than_exist(self):
        h = _h()
        cid = _seed(h, n=2)
        r = h.recent_turns(cid, n=100)
        assert len(r) == 2
