"""conv_memory — E35 Conversation Memory module.

Provides turn-level dataclasses, windowing strategies, SQLite-backed
persistence, and a high-level :class:`ConversationMemory` facade.

Typical usage::

    from docstoolkit.conv_memory import ConversationMemory, Role

    mem = ConversationMemory()
    mem.add(Role.USER, "What is RAG?")
    mem.add(Role.ASSISTANT, "RAG is Retrieval-Augmented Generation...")
    for turn in mem.context():
        print(turn.role, turn.content)
"""
from docstoolkit.conv_memory.turn import Role, ConversationTurn
from docstoolkit.conv_memory.window import WindowStrategy, MemoryWindow
from docstoolkit.conv_memory.store import ConversationStore
from docstoolkit.conv_memory.memory import ConversationMemory

__all__ = [
    # turn
    "Role",
    "ConversationTurn",
    # window
    "WindowStrategy",
    "MemoryWindow",
    # store
    "ConversationStore",
    # memory
    "ConversationMemory",
]
