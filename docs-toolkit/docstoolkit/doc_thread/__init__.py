"""Document discussion thread module for docs-toolkit (E218).

Provides a discussion thread manager attached to documents with comments,
replies, threading, and reactions. Stdlib-only.

Quick start::

    from docstoolkit.doc_thread import (
        DocThread, MessageReaction, MessageStatus,
    )

    dt = DocThread()
    thread = dt.create_thread(doc_id="doc-1", created_by="alice",
                              initial_message="Looks good?", now=1.0)
    msg = dt.add_message(thread.thread_id, "bob", "Yes, LGTM", now=2.0)
    dt.add_reaction(msg.message_id, "carol", MessageReaction.LIKE)
"""
from docstoolkit.doc_thread.thread import (
    MessageReaction,
    MessageStatus,
    ThreadMessage,
    Thread,
    DocThread,
)

__all__ = [
    "MessageReaction",
    "MessageStatus",
    "ThreadMessage",
    "Thread",
    "DocThread",
]
