"""Request handler for OpenAI-compatible chat completions.

Bridges an incoming :class:`ChatRequest` to a docs-toolkit RAG function and
wraps the answer in a :class:`ChatResponse`.

The *rag_fn* parameter is intentionally abstract so this module remains
decoupled from the actual retrieval implementation.  Any callable with the
signature ``(query: str, **kwargs) -> str`` works.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import re
import uuid
from typing import Any, Callable, Dict, Iterator, List, Optional

from docstoolkit.openai_compat.types import (
    ChatChoice, ChatMessage, ChatRequest, ChatResponse, ChatUsage, DeltaChunk,
)


RagFn = Callable[..., str]   # (query: str, **kwargs) -> answer: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _count_tokens(text: str) -> int:
    """Rough token count: ~4 chars per token (GPT-3 estimate)."""
    return max(1, len(text) // 4)


def _build_rag_kwargs(request: ChatRequest) -> Dict[str, Any]:
    """Extract docs-toolkit-specific kwargs from the request."""
    kwargs: Dict[str, Any] = {}
    # top_k can be passed in extra
    if "top_k" in request.extra:
        kwargs["top_k"] = request.extra["top_k"]
    if "method" in request.extra:
        kwargs["method"] = request.extra["method"]
    if request.user:
        kwargs["user_id"] = request.user
    return kwargs


def _format_chat_history(messages: List[ChatMessage]) -> str:
    """Convert chat history (excluding last user message) to a context string."""
    parts = []
    for msg in messages[:-1]:
        if msg.role == "system":
            parts.append(f"System: {msg.content}")
        elif msg.role == "assistant":
            parts.append(f"Assistant: {msg.content}")
        elif msg.role == "user":
            parts.append(f"User: {msg.content}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------

def handle_chat_completion(
    request: ChatRequest,
    rag_fn: Optional[RagFn] = None,
    fallback_fn: Optional[RagFn] = None,
) -> ChatResponse:
    """Handle a chat completion request using a docs-toolkit RAG function.

    Parameters
    ----------
    request:
        Parsed :class:`ChatRequest`.
    rag_fn:
        Primary callable ``(query: str, **kwargs) -> str``.  If None, a
        stub that echoes the query is used (useful for testing).
    fallback_fn:
        Optional secondary callable tried if *rag_fn* raises an exception.

    Returns
    -------
    :class:`ChatResponse` in OpenAI format.
    """
    query = request.last_user_message or ""
    system = request.system_prompt or ""

    # Prepend system prompt to query if not empty
    effective_query = f"{system}\n\n{query}".strip() if system else query

    # Chat history as additional context
    history = _format_chat_history(request.messages)
    if history:
        effective_query = f"{history}\n\n{effective_query}"

    rag_kwargs = _build_rag_kwargs(request)

    answer: str
    if rag_fn is not None:
        try:
            answer = rag_fn(effective_query, **rag_kwargs)
        except Exception as exc:
            if fallback_fn is not None:
                try:
                    answer = fallback_fn(effective_query, **rag_kwargs)
                except Exception:
                    answer = f"[Error: {exc}]"
            else:
                answer = f"[Error: {exc}]"
    else:
        # Stub for testing / offline mode
        answer = f"[stub] Query received: {query[:100]}"

    # Build response
    prompt_tokens = sum(_count_tokens(m.content) for m in request.messages)
    completion_tokens = _count_tokens(answer)

    return ChatResponse(
        model=request.model,
        choices=[
            ChatChoice(
                index=0,
                message=ChatMessage(role="assistant", content=answer),
                finish_reason="stop",
            )
        ],
        usage=ChatUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


def stream_chat_completion(
    request: ChatRequest,
    rag_fn: Optional[RagFn] = None,
) -> Iterator[DeltaChunk]:
    """Yield SSE delta chunks for a streaming chat completion.

    The current implementation yields the full answer as a single chunk
    (real word-by-word streaming requires an async token generator from the
    LLM backend, which is outside the stdlib-only scope).

    Parameters
    ----------
    request:
        Parsed :class:`ChatRequest`.
    rag_fn:
        RAG callable.

    Yields
    ------
    :class:`DeltaChunk`
    """
    chunk_id = f"chatcmpl-{uuid.uuid4().hex[:16]}"
    model = request.model

    # Get the full answer first
    response = handle_chat_completion(request, rag_fn=rag_fn)
    answer = response.choices[0].message.content if response.choices else ""

    # Yield content in ~20-char chunks to simulate streaming
    chunk_size = 20
    for i in range(0, max(1, len(answer)), chunk_size):
        piece = answer[i:i + chunk_size]
        yield DeltaChunk(id=chunk_id, model=model, delta_content=piece)

    yield DeltaChunk.done_sentinel(chunk_id, model)
