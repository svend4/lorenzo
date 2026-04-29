"""Тесты conversation memory store."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.conversation import ConversationStore, Session, Message
from docstoolkit.conversation.store import _heuristic_summary


@pytest.fixture
def cs(tmp_path):
    s = ConversationStore(db_path=tmp_path / "c.sqlite")
    yield s
    s.close()


# ---- dataclasses ----

def test_session_auto_id_ts():
    s = Session()
    assert s.id and len(s.id) == 16
    assert s.created_ts
    assert s.updated_ts == s.created_ts


def test_message_auto_id_ts():
    m = Message(content="hi")
    assert m.id and len(m.id) == 12
    assert m.ts
    assert m.tokens >= 1  # auto-estimated


def test_message_token_estimate():
    m = Message(content="x" * 60)
    assert m.tokens == 20  # 60//3


# ---- sessions ----

def test_create_and_get_session(cs):
    sid = cs.create_session(user="alice", title="x", skill="rag")
    s = cs.get_session(sid)
    assert s is not None
    assert s.user == "alice"
    assert s.title == "x"
    assert s.skill == "rag"


def test_get_missing_returns_none(cs):
    assert cs.get_session("nonexistent") is None


def test_list_sessions_filter_by_user(cs):
    cs.create_session(user="alice")
    cs.create_session(user="bob")
    cs.create_session(user="alice")
    assert len(cs.list_sessions(user="alice")) == 2
    assert len(cs.list_sessions(user="bob")) == 1


def test_list_sessions_orders_by_updated_desc(cs):
    s1 = cs.create_session(user="x", title="first")
    s2 = cs.create_session(user="x", title="second")
    # touch s1 by appending
    cs.append(s1, role="user", content="hi")
    sessions = cs.list_sessions(user="x")
    # s1 updated last → first
    assert sessions[0].id == s1


def test_delete_session_removes_messages(cs):
    sid = cs.create_session(user="x")
    cs.append(sid, role="user", content="msg")
    cs.delete_session(sid)
    assert cs.get_session(sid) is None
    assert cs.messages(sid) == []


# ---- messages ----

def test_append_and_messages(cs):
    sid = cs.create_session(user="x")
    cs.append(sid, role="user", content="hello")
    cs.append(sid, role="assistant", content="hi back")
    msgs = cs.messages(sid)
    assert len(msgs) == 2
    assert msgs[0].role == "user"
    assert msgs[1].role == "assistant"


def test_append_updates_session_updated_ts(cs):
    sid = cs.create_session(user="x")
    s_before = cs.get_session(sid)
    import time as _t; _t.sleep(1)  # ensure ts diff (resolution = seconds)
    cs.append(sid, role="user", content="msg")
    s_after = cs.get_session(sid)
    assert s_after.updated_ts > s_before.updated_ts


def test_message_with_metadata(cs):
    sid = cs.create_session(user="x")
    cs.append(sid, role="tool", content="out", metadata={"tool": "search"})
    msgs = cs.messages(sid)
    assert msgs[0].metadata == {"tool": "search"}


# ---- history_for_llm ----

def test_history_for_llm_includes_system_prompt(cs):
    sid = cs.create_session(user="x")
    cs.append(sid, role="user", content="hi")
    h = cs.history_for_llm(sid, system_prompt="You are helpful.")
    assert h[0]["role"] == "system"
    assert "helpful" in h[0]["content"]


def test_history_for_llm_chronological(cs):
    sid = cs.create_session(user="x")
    cs.append(sid, role="user", content="q1")
    cs.append(sid, role="assistant", content="a1")
    cs.append(sid, role="user", content="q2")
    h = cs.history_for_llm(sid, max_tokens=1000)
    assert [x["content"] for x in h] == ["q1", "a1", "q2"]


def test_history_for_llm_truncates_to_budget(cs):
    sid = cs.create_session(user="x")
    # 30 chars → ~10 tokens each
    for i in range(10):
        cs.append(sid, role="user", content="x" * 30)
    h = cs.history_for_llm(sid, max_tokens=20)
    # ≤20 tokens → ≤2 messages of 10 tokens
    assert len(h) <= 2


def test_history_for_llm_includes_summary(cs):
    sid = cs.create_session(user="x")
    cs.update_summary(sid, "Talked about RAG")
    cs.append(sid, role="user", content="next?")
    h = cs.history_for_llm(sid, summarize_old=True)
    sys_msgs = [m for m in h if m["role"] == "system"]
    assert any("RAG" in m["content"] for m in sys_msgs)


# ---- squash_old ----

def test_squash_old_compresses_old_messages(cs):
    sid = cs.create_session(user="x")
    for i in range(10):
        cs.append(sid, role="user", content=f"msg {i}")
    summary = cs.squash_old(sid, keep_last=3)
    assert summary  # got something
    msgs = cs.messages(sid)
    assert len(msgs) == 3  # only last 3 remain
    # session has summary
    s = cs.get_session(sid)
    assert s.summary


def test_squash_old_below_keep_last_no_op(cs):
    sid = cs.create_session(user="x")
    cs.append(sid, role="user", content="a")
    summary = cs.squash_old(sid, keep_last=10)
    assert summary == ""
    assert len(cs.messages(sid)) == 1


def test_squash_with_custom_summarizer(cs):
    sid = cs.create_session(user="x")
    for i in range(5):
        cs.append(sid, role="user", content=f"msg {i}")
    cs.squash_old(sid, keep_last=1,
                   summarizer=lambda msgs: f"SUMMARY({len(msgs)})")
    s = cs.get_session(sid)
    assert "SUMMARY(4)" in s.summary


def test_heuristic_summary_format():
    msgs = [
        Message(role="user", content="что такое RAG?"),
        Message(role="assistant", content="это retrieval-augmented generation"),
    ]
    summ = _heuristic_summary(msgs)
    assert "U:" in summ and "A:" in summ
    assert "RAG" in summ
