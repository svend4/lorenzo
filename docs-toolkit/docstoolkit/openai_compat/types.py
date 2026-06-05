"""Data types mirroring the OpenAI Chat Completions API schema.

These are simple dataclasses — no Pydantic dependency.

References:
    https://platform.openai.com/docs/api-reference/chat/create
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Request types
# ---------------------------------------------------------------------------

@dataclass
class ChatMessage:
    """A single message in the chat history."""
    role: str          # "system" | "user" | "assistant" | "tool"
    content: str
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ChatMessage":
        return cls(
            role=d.get("role", "user"),
            content=d.get("content", ""),
            name=d.get("name"),
        )

    def to_dict(self) -> dict:
        out: dict = {"role": self.role, "content": self.content}
        if self.name:
            out["name"] = self.name
        return out


@dataclass
class ChatRequest:
    """OpenAI-compatible chat completions request."""
    model: str = "lorenzo-gateway"
    messages: List[ChatMessage] = field(default_factory=list)
    max_tokens: Optional[int] = None
    temperature: float = 0.7
    top_p: float = 1.0
    stream: bool = False
    n: int = 1
    stop: Optional[List[str]] = None
    user: Optional[str] = None
    # Extension: pass-through kwargs for docs-toolkit RAG
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "ChatRequest":
        messages = [ChatMessage.from_dict(m) for m in d.get("messages", [])]
        return cls(
            model=d.get("model", "lorenzo-gateway"),
            messages=messages,
            max_tokens=d.get("max_tokens"),
            temperature=float(d.get("temperature", 0.7)),
            top_p=float(d.get("top_p", 1.0)),
            stream=bool(d.get("stream", False)),
            n=int(d.get("n", 1)),
            stop=d.get("stop"),
            user=d.get("user"),
            extra={k: v for k, v in d.items() if k not in (
                "model", "messages", "max_tokens", "temperature",
                "top_p", "stream", "n", "stop", "user",
            )},
        )

    @property
    def last_user_message(self) -> Optional[str]:
        """Extract the most recent user message content."""
        for msg in reversed(self.messages):
            if msg.role == "user":
                return msg.content
        return None

    @property
    def system_prompt(self) -> Optional[str]:
        """Extract the system prompt, if any."""
        for msg in self.messages:
            if msg.role == "system":
                return msg.content
        return None


# ---------------------------------------------------------------------------
# Response types
# ---------------------------------------------------------------------------

@dataclass
class ChatUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def to_dict(self) -> dict:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass
class ChatChoice:
    index: int = 0
    message: Optional[ChatMessage] = None
    finish_reason: str = "stop"
    logprobs: None = None

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "message": self.message.to_dict() if self.message else None,
            "finish_reason": self.finish_reason,
            "logprobs": self.logprobs,
        }


@dataclass
class ChatResponse:
    """OpenAI-compatible chat completions response."""
    id: str = field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex[:16]}")
    object: str = "chat.completion"
    created: int = field(default_factory=lambda: int(time.time()))
    model: str = "lorenzo-gateway"
    choices: List[ChatChoice] = field(default_factory=list)
    usage: ChatUsage = field(default_factory=ChatUsage)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "object": self.object,
            "created": self.created,
            "model": self.model,
            "choices": [c.to_dict() for c in self.choices],
            "usage": self.usage.to_dict(),
        }


# ---------------------------------------------------------------------------
# Streaming delta
# ---------------------------------------------------------------------------

@dataclass
class DeltaChunk:
    """A single SSE chunk for streaming completions."""
    id: str
    model: str
    delta_content: Optional[str] = None
    finish_reason: Optional[str] = None
    index: int = 0

    def to_sse(self) -> str:
        """Format as Server-Sent Event string."""
        import json
        payload = {
            "id": self.id,
            "object": "chat.completion.chunk",
            "model": self.model,
            "choices": [{
                "index": self.index,
                "delta": {"content": self.delta_content} if self.delta_content else {},
                "finish_reason": self.finish_reason,
            }],
        }
        return f"data: {json.dumps(payload)}\n\n"

    @classmethod
    def done_sentinel(cls, chunk_id: str, model: str) -> "DeltaChunk":
        return cls(id=chunk_id, model=model, finish_reason="stop")
