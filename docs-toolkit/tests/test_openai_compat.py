"""Tests for docstoolkit.openai_compat — OpenAI-compatible chat gateway."""
from __future__ import annotations

import json
import time
import pytest

from docstoolkit.openai_compat import (
    ChatMessage, ChatRequest, ChatResponse,
    ChatChoice, ChatUsage, DeltaChunk,
    handle_chat_completion,
)
from docstoolkit.openai_compat.types import ChatRequest, ChatMessage
from docstoolkit.openai_compat.handler import stream_chat_completion


# ---------------------------------------------------------------------------
# ChatMessage
# ---------------------------------------------------------------------------

class TestChatMessage:
    def test_basic_fields(self):
        msg = ChatMessage(role="user", content="hello")
        assert msg.role == "user"
        assert msg.content == "hello"
        assert msg.name is None

    def test_from_dict(self):
        msg = ChatMessage.from_dict({"role": "assistant", "content": "hi", "name": "bot"})
        assert msg.role == "assistant"
        assert msg.content == "hi"
        assert msg.name == "bot"

    def test_from_dict_defaults(self):
        msg = ChatMessage.from_dict({})
        assert msg.role == "user"
        assert msg.content == ""

    def test_to_dict(self):
        msg = ChatMessage(role="user", content="test")
        d = msg.to_dict()
        assert d["role"] == "user"
        assert d["content"] == "test"
        assert "name" not in d  # omitted when None

    def test_to_dict_with_name(self):
        msg = ChatMessage(role="user", content="test", name="alice")
        d = msg.to_dict()
        assert d["name"] == "alice"


# ---------------------------------------------------------------------------
# ChatRequest
# ---------------------------------------------------------------------------

class TestChatRequest:
    def test_defaults(self):
        req = ChatRequest()
        assert req.model == "lorenzo-gateway"
        assert req.messages == []
        assert req.temperature == 0.7
        assert req.stream is False

    def test_from_dict_full(self):
        raw = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "hi"},
            ],
            "max_tokens": 100,
            "temperature": 0.5,
            "stream": True,
            "n": 2,
            "user": "u1",
        }
        req = ChatRequest.from_dict(raw)
        assert req.model == "gpt-4"
        assert len(req.messages) == 2
        assert req.max_tokens == 100
        assert req.temperature == 0.5
        assert req.stream is True
        assert req.n == 2
        assert req.user == "u1"

    def test_extra_kwargs_captured(self):
        raw = {"model": "x", "messages": [], "top_k": 5, "method": "hybrid"}
        req = ChatRequest.from_dict(raw)
        assert req.extra["top_k"] == 5
        assert req.extra["method"] == "hybrid"

    def test_last_user_message(self):
        req = ChatRequest(messages=[
            ChatMessage("system", "sys"),
            ChatMessage("user", "first"),
            ChatMessage("assistant", "reply"),
            ChatMessage("user", "second"),
        ])
        assert req.last_user_message == "second"

    def test_last_user_message_none_when_no_user(self):
        req = ChatRequest(messages=[ChatMessage("system", "sys")])
        assert req.last_user_message is None

    def test_system_prompt(self):
        req = ChatRequest(messages=[
            ChatMessage("system", "Be helpful"),
            ChatMessage("user", "hi"),
        ])
        assert req.system_prompt == "Be helpful"

    def test_system_prompt_none_when_absent(self):
        req = ChatRequest(messages=[ChatMessage("user", "hi")])
        assert req.system_prompt is None


# ---------------------------------------------------------------------------
# ChatUsage / ChatChoice / ChatResponse
# ---------------------------------------------------------------------------

class TestChatUsage:
    def test_to_dict(self):
        usage = ChatUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15)
        d = usage.to_dict()
        assert d == {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}


class TestChatChoice:
    def test_to_dict(self):
        msg = ChatMessage(role="assistant", content="hello")
        choice = ChatChoice(index=0, message=msg, finish_reason="stop")
        d = choice.to_dict()
        assert d["index"] == 0
        assert d["finish_reason"] == "stop"
        assert d["message"]["content"] == "hello"
        assert d["logprobs"] is None


class TestChatResponse:
    def test_auto_id_and_created(self):
        resp = ChatResponse()
        assert resp.id.startswith("chatcmpl-")
        assert resp.created > 0

    def test_to_dict_structure(self):
        resp = ChatResponse(model="test-model")
        d = resp.to_dict()
        assert d["object"] == "chat.completion"
        assert d["model"] == "test-model"
        assert "choices" in d
        assert "usage" in d


# ---------------------------------------------------------------------------
# DeltaChunk
# ---------------------------------------------------------------------------

class TestDeltaChunk:
    def test_to_sse_format(self):
        chunk = DeltaChunk(id="cid", model="m", delta_content="hello")
        sse = chunk.to_sse()
        assert sse.startswith("data: ")
        assert sse.endswith("\n\n")
        payload = json.loads(sse[len("data: "):].strip())
        assert payload["choices"][0]["delta"]["content"] == "hello"

    def test_done_sentinel(self):
        sentinel = DeltaChunk.done_sentinel("cid", "m")
        assert sentinel.finish_reason == "stop"
        assert sentinel.delta_content is None

    def test_done_sentinel_sse(self):
        sentinel = DeltaChunk.done_sentinel("cid", "m")
        sse = sentinel.to_sse()
        payload = json.loads(sse[len("data: "):].strip())
        assert payload["choices"][0]["delta"] == {}
        assert payload["choices"][0]["finish_reason"] == "stop"


# ---------------------------------------------------------------------------
# handle_chat_completion
# ---------------------------------------------------------------------------

class TestHandleChatCompletion:
    def _req(self, query="hello", system=None):
        messages = []
        if system:
            messages.append(ChatMessage("system", system))
        messages.append(ChatMessage("user", query))
        return ChatRequest(messages=messages)

    def test_stub_mode_no_rag_fn(self):
        req = self._req("world")
        resp = handle_chat_completion(req)
        assert isinstance(resp, ChatResponse)
        assert "[stub]" in resp.choices[0].message.content

    def test_rag_fn_called_with_query(self):
        calls = []
        def rag(q, **kw):
            calls.append(q)
            return "answer"

        req = self._req("my question")
        resp = handle_chat_completion(req, rag_fn=rag)
        assert resp.choices[0].message.content == "answer"
        assert len(calls) == 1
        assert "my question" in calls[0]

    def test_system_prompt_prepended(self):
        received = []
        def rag(q, **kw):
            received.append(q)
            return "ok"

        req = self._req("q", system="Be concise")
        handle_chat_completion(req, rag_fn=rag)
        assert "Be concise" in received[0]
        assert "q" in received[0]

    def test_rag_fn_exception_returns_error(self):
        def bad_rag(q, **kw):
            raise ValueError("oops")

        req = self._req("q")
        resp = handle_chat_completion(req, rag_fn=bad_rag)
        content = resp.choices[0].message.content
        assert "[Error:" in content

    def test_fallback_fn_used_on_rag_error(self):
        def bad_rag(q, **kw):
            raise RuntimeError("primary fail")

        def fallback(q, **kw):
            return "fallback answer"

        req = self._req("q")
        resp = handle_chat_completion(req, rag_fn=bad_rag, fallback_fn=fallback)
        assert resp.choices[0].message.content == "fallback answer"

    def test_fallback_fn_also_fails_returns_error(self):
        def bad_rag(q, **kw):
            raise RuntimeError("primary fail")

        def bad_fallback(q, **kw):
            raise ValueError("also bad")

        req = self._req("q")
        resp = handle_chat_completion(req, rag_fn=bad_rag, fallback_fn=bad_fallback)
        assert "[Error:" in resp.choices[0].message.content

    def test_usage_tokens_populated(self):
        req = self._req("hello")
        resp = handle_chat_completion(req)
        assert resp.usage.prompt_tokens > 0
        assert resp.usage.completion_tokens > 0
        assert resp.usage.total_tokens == resp.usage.prompt_tokens + resp.usage.completion_tokens

    def test_model_echoed_in_response(self):
        req = ChatRequest(model="my-model", messages=[ChatMessage("user", "hi")])
        resp = handle_chat_completion(req)
        assert resp.model == "my-model"

    def test_finish_reason_stop(self):
        req = self._req("q")
        resp = handle_chat_completion(req)
        assert resp.choices[0].finish_reason == "stop"

    def test_chat_history_included_in_query(self):
        received = []
        def rag(q, **kw):
            received.append(q)
            return "ok"

        req = ChatRequest(messages=[
            ChatMessage("user", "first"),
            ChatMessage("assistant", "reply"),
            ChatMessage("user", "second"),
        ])
        handle_chat_completion(req, rag_fn=rag)
        assert "first" in received[0]
        assert "reply" in received[0]
        assert "second" in received[0]

    def test_extra_kwargs_passed_to_rag(self):
        received_kw = {}
        def rag(q, **kw):
            received_kw.update(kw)
            return "ok"

        raw = {"messages": [{"role": "user", "content": "q"}], "top_k": 7, "method": "bm25"}
        req = ChatRequest.from_dict(raw)
        handle_chat_completion(req, rag_fn=rag)
        assert received_kw["top_k"] == 7
        assert received_kw["method"] == "bm25"

    def test_response_to_dict_valid(self):
        req = self._req("q")
        resp = handle_chat_completion(req)
        d = resp.to_dict()
        assert d["object"] == "chat.completion"
        assert len(d["choices"]) == 1
        assert d["choices"][0]["message"]["role"] == "assistant"


# ---------------------------------------------------------------------------
# stream_chat_completion
# ---------------------------------------------------------------------------

class TestStreamChatCompletion:
    def test_yields_chunks(self):
        req = ChatRequest(messages=[ChatMessage("user", "hi")])
        chunks = list(stream_chat_completion(req))
        assert len(chunks) >= 1

    def test_last_chunk_is_done_sentinel(self):
        req = ChatRequest(messages=[ChatMessage("user", "hi")])
        chunks = list(stream_chat_completion(req))
        last = chunks[-1]
        assert last.finish_reason == "stop"

    def test_chunks_reconstruct_answer(self):
        def rag(q, **kw):
            return "Hello, world!"

        req = ChatRequest(messages=[ChatMessage("user", "hi")])
        chunks = list(stream_chat_completion(req, rag_fn=rag))
        # Reconstruct: skip sentinel
        text = "".join(c.delta_content for c in chunks if c.delta_content)
        assert text == "Hello, world!"

    def test_all_chunks_have_same_id(self):
        req = ChatRequest(messages=[ChatMessage("user", "hi")])
        chunks = list(stream_chat_completion(req))
        ids = {c.id for c in chunks}
        assert len(ids) == 1

    def test_chunk_sse_format(self):
        req = ChatRequest(messages=[ChatMessage("user", "hi")])
        chunks = list(stream_chat_completion(req))
        for chunk in chunks:
            sse = chunk.to_sse()
            assert sse.startswith("data: ")
            assert sse.endswith("\n\n")
