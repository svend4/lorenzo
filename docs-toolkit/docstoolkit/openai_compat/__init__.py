"""OpenAI-compatible chat completions gateway (Phase XVII.3).

Provides a request/response model that matches the OpenAI ``/v1/chat/completions``
API format, allowing any OpenAI-compatible client to use the docs-toolkit RAG
backend as a drop-in LLM endpoint.

No HTTP server is included here — callers are responsible for routing the raw
request body to :func:`handle_chat_completion` and returning the response.
Integrates with ``serve.py`` or any WSGI/ASGI framework.

Pure stdlib — no external dependencies (the HTTP layer is left to the caller).

Usage (in serve.py or similar)::

    from docstoolkit.openai_compat import handle_chat_completion, ChatRequest

    body = json.loads(raw_request_body)
    request = ChatRequest.from_dict(body)
    response = handle_chat_completion(request, rag_fn=my_ask_fn)
    return json.dumps(response.to_dict())
"""
from docstoolkit.openai_compat.types import (
    ChatMessage, ChatRequest, ChatResponse,
    ChatChoice, ChatUsage, DeltaChunk,
)
from docstoolkit.openai_compat.handler import handle_chat_completion

__all__ = [
    "ChatMessage", "ChatRequest", "ChatResponse",
    "ChatChoice", "ChatUsage", "DeltaChunk",
    "handle_chat_completion",
]
