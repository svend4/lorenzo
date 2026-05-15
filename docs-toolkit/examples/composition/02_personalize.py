"""S6 per-user profiles + S7 read-receipts.

Alice prefers BM25 and the "memory" section; once she sees a doc it's
penalised on subsequent calls so she discovers new content.
"""
from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from docstoolkit.conversation.profile import ProfileStore, UserProfile
from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage


class _Retriever:
    def __init__(self):
        self.last_method = None
        self._docs = [
            Passage(text="Yodoca is a memory project for agents.",
                    doc_id="memory/yodoca", title="Yodoca", score=0.9),
            Passage(text="NGT Memory tracks knowledge graphs.",
                    doc_id="memory/ngt", title="NGT", score=0.8),
            Passage(text="AgentFS exposes the filesystem as a tool.",
                    doc_id="knowledge/agentfs", title="AgentFS", score=0.7),
        ]

    def search(self, query, top_k):
        return list(self._docs[:top_k])


class _Answerer:
    def answer(self, system, user, model=""):
        return "Alice's personalised answer.", 0, 0.0


def main() -> None:
    # Use a temp DB so the demo is hermetic
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "profiles.sqlite"
        store = ProfileStore(db_path=db)
        store.save(UserProfile(
            user_id="alice",
            preferred_retriever="bm25",
            preferred_sections=["memory"],
            interests=["agents", "knowledge"],
        ))
        store.close()

        # Patch ProfileStore default db to our temp one
        from docstoolkit.conversation import profile as prof
        orig_init = prof.ProfileStore.__init__

        def _tmp_init(self, db_path=None):
            orig_init(self, db_path=db_path or db)

        with patch.object(prof.ProfileStore, "__init__", _tmp_init), \
             patch("docstoolkit.rag.pipeline.Retriever",
                   lambda **kw: _Retriever()), \
             patch("docstoolkit.rag.pipeline.get_answerer",
                   lambda name, **kw: _Answerer()):

            print("First call as alice:")
            r1 = ask("about agents", user_id="alice", top_k=2)
            for p in r1.retrieved_passages:
                print(f"  [{p.score:.2f}] {p.doc_id}")

            print("\nSecond call — already-read docs now penalised:")
            r2 = ask("about agents", user_id="alice", top_k=3)
            for p in r2.retrieved_passages:
                print(f"  [{p.score:.2f}] {p.doc_id}")

            # Verify the read tracking
            store = ProfileStore(db_path=db)
            p = store.load("alice")
            store.close()
            print(f"\nAlice's read_docs: {sorted(p.read_docs)}")


if __name__ == "__main__":
    main()
