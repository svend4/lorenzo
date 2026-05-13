"""Conversation history manager for AI-assisted document workflows.

Turn-based history with context windows, pruning, and token budgets.

Использование::

    from docstoolkit.doc_assistant_history import (
        DocAssistantHistory, Turn, TurnRole, ConversationSummary,
    )

    h = DocAssistantHistory(max_turns=50, max_tokens=16000)
    cid = h.create_conversation(system_prompt="You are a helpful doc editor.")
    h.add_turn(cid, TurnRole.USER, "Summarize the intro section.")
    h.add_turn(cid, TurnRole.ASSISTANT, "Sure — the intro covers ...")

    ctx = h.get_context(cid, max_tokens=4000)
"""
from docstoolkit.doc_assistant_history.history import (
    ConversationSummary,
    DocAssistantHistory,
    Turn,
    TurnRole,
)

__all__ = [
    "ConversationSummary",
    "DocAssistantHistory",
    "Turn",
    "TurnRole",
]
