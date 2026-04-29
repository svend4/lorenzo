"""Multi-turn conversation memory: sessions, message history, context-window mgmt.

Использование:
    from docstoolkit.conversation import ConversationStore, Session

    store = ConversationStore()
    sid = store.create_session(user="alice", title="RAG questions")

    store.append(sid, role="user", content="Что такое RAG?")
    # ... LLM генерирует ...
    store.append(sid, role="assistant", content="RAG это...")

    # На следующий ход — сериализуем history с учётом max_tokens
    msgs = store.history_for_llm(sid, max_tokens=4000, summarize_old=True)
"""
from docstoolkit.conversation.store import (
    ConversationStore, Session, Message,
)

__all__ = ["ConversationStore", "Session", "Message"]
