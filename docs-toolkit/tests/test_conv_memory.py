"""Tests for E35 conv_memory module (65+ tests)."""
from __future__ import annotations

import time
import uuid

import pytest

from docstoolkit.conv_memory import (
    ConversationMemory,
    ConversationStore,
    ConversationTurn,
    MemoryWindow,
    Role,
    WindowStrategy,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_turn(role=Role.USER, content="hello world", **kw) -> ConversationTurn:
    return ConversationTurn(role=role, content=content, **kw)


def make_turns(contents: list[str], role=Role.USER) -> list[ConversationTurn]:
    """Create turns with small ts offsets so ordering is deterministic."""
    turns = []
    base = time.time()
    for i, c in enumerate(contents):
        t = ConversationTurn(role=role, content=c, ts=base + i * 0.001)
        turns.append(t)
    return turns


# ===========================================================================
# ConversationTurn
# ===========================================================================

class TestConversationTurnDefaults:
    def test_turn_id_auto_generated(self):
        t = ConversationTurn(role=Role.USER, content="hi")
        assert isinstance(t.turn_id, str)
        assert len(t.turn_id) == 8

    def test_turn_id_unique(self):
        ids = {ConversationTurn(role=Role.USER, content="x").turn_id for _ in range(50)}
        assert len(ids) == 50

    def test_ts_auto_generated(self):
        before = time.time()
        t = ConversationTurn(role=Role.USER, content="hi")
        after = time.time()
        assert before <= t.ts <= after

    def test_metadata_default_empty_dict(self):
        t = ConversationTurn(role=Role.USER, content="hi")
        assert t.metadata == {}

    def test_metadata_not_shared_between_instances(self):
        t1 = ConversationTurn(role=Role.USER, content="a")
        t2 = ConversationTurn(role=Role.USER, content="b")
        t1.metadata["x"] = 1
        assert "x" not in t2.metadata

    def test_explicit_turn_id(self):
        t = ConversationTurn(role=Role.USER, content="hi", turn_id="abcd1234")
        assert t.turn_id == "abcd1234"

    def test_explicit_metadata(self):
        t = ConversationTurn(role=Role.USER, content="hi", metadata={"k": "v"})
        assert t.metadata["k"] == "v"


class TestRole:
    def test_role_values(self):
        assert Role.USER.value == "user"
        assert Role.ASSISTANT.value == "assistant"
        assert Role.SYSTEM.value == "system"

    def test_role_from_string(self):
        assert Role("user") is Role.USER
        assert Role("assistant") is Role.ASSISTANT
        assert Role("system") is Role.SYSTEM


class TestWordCount:
    def test_empty_string(self):
        t = make_turn(content="")
        assert t.word_count() == 0

    def test_single_word(self):
        assert make_turn(content="hello").word_count() == 1

    def test_multiple_words(self):
        assert make_turn(content="hello world foo bar").word_count() == 4

    def test_extra_spaces(self):
        # str.split() ignores leading/trailing/multiple spaces
        assert make_turn(content="  hello   world  ").word_count() == 2

    def test_russian_text(self):
        t = make_turn(content="привет мир как дела")
        assert t.word_count() == 4


class TestIsQuestion:
    # --- ends with "?"
    def test_ends_with_question_mark(self):
        assert make_turn(content="Is this a test?").is_question()

    def test_no_question_mark_no_word(self):
        assert not make_turn(content="This is a statement.").is_question()

    # --- EN question words
    def test_what(self):
        assert make_turn(content="What is RAG").is_question()

    def test_who(self):
        assert make_turn(content="Who wrote this").is_question()

    def test_where(self):
        assert make_turn(content="Where is the file").is_question()

    def test_when(self):
        assert make_turn(content="When was this written").is_question()

    def test_why(self):
        assert make_turn(content="Why does it fail").is_question()

    def test_how(self):
        assert make_turn(content="How does it work").is_question()

    def test_en_case_insensitive(self):
        assert make_turn(content="WHAT is this").is_question()
        assert make_turn(content="How Are You").is_question()

    # --- RU question words
    def test_ru_chto(self):
        assert make_turn(content="Что такое RAG").is_question()

    def test_ru_kto(self):
        assert make_turn(content="Кто автор").is_question()

    def test_ru_gde(self):
        assert make_turn(content="Где файл").is_question()

    def test_ru_kogda(self):
        assert make_turn(content="Когда это было").is_question()

    def test_ru_pochemu(self):
        assert make_turn(content="Почему ошибка").is_question()

    def test_ru_kak(self):
        assert make_turn(content="Как это работает").is_question()

    def test_ru_question_mark(self):
        assert make_turn(content="Это работает?").is_question()

    def test_not_question_plain_ru(self):
        assert not make_turn(content="Это просто утверждение.").is_question()

    def test_question_word_with_punctuation(self):
        # "what," — the comma should be stripped before matching
        assert make_turn(content="what, is this").is_question()


# ===========================================================================
# MemoryWindow
# ===========================================================================

class TestMemoryWindowLastN:
    def test_fewer_turns_than_size(self):
        w = MemoryWindow(strategy=WindowStrategy.LAST_N, size=10)
        turns = make_turns(["a", "b", "c"])
        assert w.apply(turns) == turns

    def test_exact_size(self):
        w = MemoryWindow(strategy=WindowStrategy.LAST_N, size=3)
        turns = make_turns(["a", "b", "c"])
        result = w.apply(turns)
        assert [t.content for t in result] == ["a", "b", "c"]

    def test_more_turns_than_size(self):
        w = MemoryWindow(strategy=WindowStrategy.LAST_N, size=3)
        turns = make_turns(["a", "b", "c", "d", "e"])
        result = w.apply(turns)
        assert [t.content for t in result] == ["c", "d", "e"]

    def test_empty_list(self):
        w = MemoryWindow(strategy=WindowStrategy.LAST_N, size=5)
        assert w.apply([]) == []

    def test_size_one(self):
        w = MemoryWindow(strategy=WindowStrategy.LAST_N, size=1)
        turns = make_turns(["a", "b", "c"])
        result = w.apply(turns)
        assert len(result) == 1
        assert result[0].content == "c"


class TestMemoryWindowTokenLimit:
    def test_all_fit(self):
        w = MemoryWindow(strategy=WindowStrategy.TOKEN_LIMIT, token_limit=10000)
        turns = make_turns(["one two", "three four", "five six"])
        assert len(w.apply(turns)) == 3

    def test_limit_cuts_oldest(self):
        # Each turn has 2 words => ~2 tokens each (floor(2*1.3)=2)
        # token_limit=4 should admit at most 2 turns of 2 words each
        w = MemoryWindow(strategy=WindowStrategy.TOKEN_LIMIT, token_limit=4)
        turns = make_turns(["aa bb", "cc dd", "ee ff"])
        result = w.apply(turns)
        # The last 2 turns should fit (2+2=4 tokens)
        assert len(result) <= 2
        # Most recent turn always included
        assert result[-1].content == "ee ff"

    def test_empty(self):
        w = MemoryWindow(strategy=WindowStrategy.TOKEN_LIMIT, token_limit=100)
        assert w.apply([]) == []

    def test_single_turn_within_limit(self):
        w = MemoryWindow(strategy=WindowStrategy.TOKEN_LIMIT, token_limit=100)
        turns = make_turns(["hello world"])
        result = w.apply(turns)
        assert len(result) == 1

    def test_very_small_limit(self):
        # A turn with 100 words exceeds any tiny limit
        content = " ".join(["word"] * 100)
        w = MemoryWindow(strategy=WindowStrategy.TOKEN_LIMIT, token_limit=5)
        turns = make_turns([content])
        # 100 words * 1.3 = 130 tokens > 5 → nothing fits
        result = w.apply(turns)
        assert result == []


class TestMemoryWindowSliding:
    def test_fewer_than_size(self):
        w = MemoryWindow(strategy=WindowStrategy.SLIDING, size=5)
        turns = make_turns(["a", "b", "c"])
        assert w.apply(turns) == turns

    def test_exact_size(self):
        w = MemoryWindow(strategy=WindowStrategy.SLIDING, size=3)
        turns = make_turns(["a", "b", "c"])
        result = w.apply(turns)
        assert [t.content for t in result] == ["a", "b", "c"]

    def test_last_complete_window(self):
        w = MemoryWindow(strategy=WindowStrategy.SLIDING, size=3)
        turns = make_turns(["a", "b", "c", "d", "e"])
        result = w.apply(turns)
        assert [t.content for t in result] == ["c", "d", "e"]

    def test_empty(self):
        w = MemoryWindow(strategy=WindowStrategy.SLIDING, size=3)
        assert w.apply([]) == []


class TestMemoryWindowSummary:
    def test_returns_all_turns(self):
        w = MemoryWindow(strategy=WindowStrategy.SUMMARY)
        turns = make_turns(["a", "b", "c", "d", "e", "f"])
        result = w.apply(turns)
        assert result == turns


class TestEstimatedTokens:
    def test_empty(self):
        w = MemoryWindow()
        assert w.estimated_tokens([]) == 0

    def test_known_value(self):
        # 10 words → int(10 * 1.3) = 13
        w = MemoryWindow()
        turn = make_turn(content="one two three four five six seven eight nine ten")
        assert w.estimated_tokens([turn]) == 13

    def test_multiple_turns(self):
        w = MemoryWindow()
        turns = make_turns(["a b c", "d e f"])  # 3+3 = 6 words → int(6*1.3)=7
        assert w.estimated_tokens(turns) == 7


# ===========================================================================
# ConversationStore
# ===========================================================================

class TestConversationStoreSession:
    def test_new_session_returns_id(self):
        store = ConversationStore()
        sid = store.new_session()
        assert isinstance(sid, str)
        assert len(sid) == 8

    def test_new_session_explicit_id(self):
        store = ConversationStore()
        sid = store.new_session("mysession")
        assert sid == "mysession"

    def test_get_session_ids_empty(self):
        store = ConversationStore()
        assert store.get_session_ids() == []

    def test_get_session_ids_after_create(self):
        store = ConversationStore()
        s1 = store.new_session()
        s2 = store.new_session()
        ids = store.get_session_ids()
        assert s1 in ids
        assert s2 in ids

    def test_multiple_sessions_unique(self):
        store = ConversationStore()
        ids = [store.new_session() for _ in range(20)]
        assert len(set(ids)) == 20

    def test_delete_session_returns_turn_count(self):
        store = ConversationStore()
        sid = store.new_session()
        store.add_turn(sid, make_turn(content="a"))
        store.add_turn(sid, make_turn(content="b"))
        count = store.delete_session(sid)
        assert count == 2

    def test_delete_session_removes_turns(self):
        store = ConversationStore()
        sid = store.new_session()
        store.add_turn(sid, make_turn(content="a"))
        store.delete_session(sid)
        # session is gone; new get_turns should return empty or raise — we
        # expect empty since no rows match
        assert store.get_turns(sid) == []

    def test_delete_nonexistent_session(self):
        store = ConversationStore()
        count = store.delete_session("nonexistent")
        assert count == 0


class TestConversationStoreAddGet:
    def test_add_and_get_turn(self):
        store = ConversationStore()
        sid = store.new_session()
        t = make_turn(role=Role.USER, content="hello")
        store.add_turn(sid, t)
        turns = store.get_turns(sid)
        assert len(turns) == 1
        assert turns[0].content == "hello"
        assert turns[0].role == Role.USER

    def test_get_turns_ordered_by_ts(self):
        store = ConversationStore()
        sid = store.new_session()
        base = time.time()
        for i, c in enumerate(["first", "second", "third"]):
            t = ConversationTurn(role=Role.USER, content=c, ts=base + i)
            store.add_turn(sid, t)
        turns = store.get_turns(sid)
        assert [t.content for t in turns] == ["first", "second", "third"]

    def test_get_turns_with_limit(self):
        store = ConversationStore()
        sid = store.new_session()
        base = time.time()
        for i, c in enumerate(["a", "b", "c", "d", "e"]):
            t = ConversationTurn(role=Role.USER, content=c, ts=base + i)
            store.add_turn(sid, t)
        turns = store.get_turns(sid, limit=2)
        # Should return the last 2
        assert [t.content for t in turns] == ["d", "e"]

    def test_metadata_round_trips(self):
        store = ConversationStore()
        sid = store.new_session()
        t = ConversationTurn(role=Role.USER, content="hi", metadata={"x": 42, "y": "z"})
        store.add_turn(sid, t)
        turns = store.get_turns(sid)
        assert turns[0].metadata == {"x": 42, "y": "z"}

    def test_roles_round_trip(self):
        store = ConversationStore()
        sid = store.new_session()
        for role in Role:
            store.add_turn(sid, make_turn(role=role))
        turns = store.get_turns(sid)
        roles_returned = {t.role for t in turns}
        assert roles_returned == set(Role)

    def test_turn_id_preserved(self):
        store = ConversationStore()
        sid = store.new_session()
        t = ConversationTurn(role=Role.USER, content="hi", turn_id="deadbeef")
        store.add_turn(sid, t)
        turns = store.get_turns(sid)
        assert turns[0].turn_id == "deadbeef"

    def test_isolation_between_sessions(self):
        store = ConversationStore()
        s1 = store.new_session()
        s2 = store.new_session()
        store.add_turn(s1, make_turn(content="from s1"))
        store.add_turn(s2, make_turn(content="from s2"))
        assert store.get_turns(s1)[0].content == "from s1"
        assert store.get_turns(s2)[0].content == "from s2"


class TestConversationStoreStats:
    def test_stats_empty(self):
        store = ConversationStore()
        s = store.stats()
        assert s["total_sessions"] == 0
        assert s["total_turns"] == 0
        assert s["avg_turns_per_session"] == 0.0

    def test_stats_one_session(self):
        store = ConversationStore()
        sid = store.new_session()
        store.add_turn(sid, make_turn())
        store.add_turn(sid, make_turn())
        s = store.stats()
        assert s["total_sessions"] == 1
        assert s["total_turns"] == 2
        assert s["avg_turns_per_session"] == 2.0

    def test_stats_multiple_sessions(self):
        store = ConversationStore()
        s1 = store.new_session()
        s2 = store.new_session()
        store.add_turn(s1, make_turn())
        store.add_turn(s2, make_turn())
        store.add_turn(s2, make_turn())
        s = store.stats()
        assert s["total_sessions"] == 2
        assert s["total_turns"] == 3
        assert s["avg_turns_per_session"] == 1.5


# ===========================================================================
# ConversationMemory
# ===========================================================================

class TestConversationMemoryBasic:
    def test_session_id_auto(self):
        mem = ConversationMemory()
        assert isinstance(mem.session_id(), str)
        assert len(mem.session_id()) == 8

    def test_session_id_explicit(self):
        mem = ConversationMemory(session_id="abc12345")
        assert mem.session_id() == "abc12345"

    def test_add_returns_turn(self):
        mem = ConversationMemory()
        t = mem.add(Role.USER, "hello")
        assert isinstance(t, ConversationTurn)
        assert t.content == "hello"
        assert t.role == Role.USER

    def test_add_with_metadata(self):
        mem = ConversationMemory()
        t = mem.add(Role.USER, "hi", source="test", priority=1)
        assert t.metadata["source"] == "test"
        assert t.metadata["priority"] == 1

    def test_context_no_window(self):
        mem = ConversationMemory()
        mem.add(Role.USER, "a")
        mem.add(Role.ASSISTANT, "b")
        turns = mem.context(apply_window=False)
        assert len(turns) == 2

    def test_context_with_window_default_last_n(self):
        w = MemoryWindow(strategy=WindowStrategy.LAST_N, size=2)
        mem = ConversationMemory(window=w)
        for c in ["a", "b", "c", "d"]:
            mem.add(Role.USER, c)
        result = mem.context()
        assert len(result) == 2
        assert result[-1].content == "d"

    def test_last_n(self):
        mem = ConversationMemory()
        base = time.time()
        for i, c in enumerate(["a", "b", "c", "d", "e"]):
            t = ConversationTurn(role=Role.USER, content=c, ts=base + i)
            mem._store.add_turn(mem.session_id(), t)
        result = mem.last_n(3)
        assert [t.content for t in result] == ["c", "d", "e"]

    def test_last_n_more_than_available(self):
        mem = ConversationMemory()
        mem.add(Role.USER, "only")
        result = mem.last_n(10)
        assert len(result) == 1

    def test_questions_empty(self):
        mem = ConversationMemory()
        mem.add(Role.USER, "This is a statement.")
        assert mem.questions() == []

    def test_questions_with_questions(self):
        mem = ConversationMemory()
        mem.add(Role.USER, "What is RAG?")
        mem.add(Role.ASSISTANT, "RAG is retrieval augmented generation.")
        mem.add(Role.USER, "How does it work?")
        qs = mem.questions()
        assert len(qs) == 2
        assert all(t.is_question() for t in qs)

    def test_questions_mixed_ru_en(self):
        mem = ConversationMemory()
        mem.add(Role.USER, "Что такое RAG")
        mem.add(Role.USER, "This is fine.")
        mem.add(Role.USER, "How does it work?")
        qs = mem.questions()
        assert len(qs) == 2

    def test_clear_returns_count(self):
        mem = ConversationMemory()
        mem.add(Role.USER, "a")
        mem.add(Role.USER, "b")
        count = mem.clear()
        assert count == 2

    def test_clear_empty_memory(self):
        mem = ConversationMemory()
        count = mem.clear()
        assert count == 0

    def test_shared_store(self):
        """Two ConversationMemory objects sharing a store have separate sessions."""
        store = ConversationStore()
        m1 = ConversationMemory(store=store)
        m2 = ConversationMemory(store=store)
        m1.add(Role.USER, "from m1")
        m2.add(Role.USER, "from m2")
        assert m1.session_id() != m2.session_id()
        assert len(m1.context(apply_window=False)) == 1
        assert len(m2.context(apply_window=False)) == 1

    def test_context_order_preserved(self):
        mem = ConversationMemory()
        contents = ["first", "second", "third"]
        for c in contents:
            mem.add(Role.USER, c)
        result = mem.context(apply_window=False)
        assert [t.content for t in result] == contents
