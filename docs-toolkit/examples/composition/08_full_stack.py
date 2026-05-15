"""All 17 features stacked in a single ask() call.

Stress-tests that every kwarg composes orthogonally without crashing.
Stubs out Retriever + Answerer so it runs offline.
"""
from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from docstoolkit.bandit import BanditExperiment
from docstoolkit.conversation.profile import ProfileStore, UserProfile
from docstoolkit.memory import TieredMemory
from docstoolkit.personality import CognitiveProfile
from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage
from docstoolkit.rerank.reranker import TFIDFReranker


class _Retriever:
    def search(self, query, top_k):
        return [
            Passage(text="Python is a programming language used in AI work.",
                    doc_id="docs/python", title="Python", score=0.95),
            Passage(text="RAG retrieves passages and feeds them to an LLM.",
                    doc_id="docs/rag", title="RAG", score=0.90),
            Passage(text="Yodoca is a memory system project from Habr.",
                    doc_id="memory/yodoca", title="Yodoca", score=0.85),
            Passage(text="AgentFS exposes the filesystem to agents safely.",
                    doc_id="knowledge/agentfs", title="AgentFS", score=0.80),
            Passage(text="Docker enables reproducible deployments.",
                    doc_id="ops/docker", title="Docker", score=0.70),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return ("Yodoca, AgentFS and RAG are key building blocks "
                "for memory-augmented agents."), 0, 0.0


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "profiles.sqlite"
        store = ProfileStore(db_path=db)
        store.save(UserProfile(
            user_id="alice",
            preferred_retriever="hybrid",
            preferred_sections=["memory"],
            interests=["agents"],
        ))
        store.close()

        from docstoolkit.conversation import profile as prof
        orig = prof.ProfileStore.__init__

        def _init(self, db_path=None):
            orig(self, db_path=db_path or db)

        memory = TieredMemory()
        personality = CognitiveProfile(
            skepticism=0.7, synthesis=0.5, verification=0.6,
            pragmatism=0.4, exploration=0.5,
        )

        with patch.object(prof.ProfileStore, "__init__", _init), \
             patch("docstoolkit.rag.pipeline.Retriever",
                   lambda **kw: _Retriever()), \
             patch("docstoolkit.rag.pipeline.get_answerer",
                   lambda name, **kw: _Answerer()):

            result = ask(
                "How do memory and RAG fit together for agents?",
                # Personalization (S6 + S7 + N9 + I5)
                user_id="alice",
                personality=personality,
                memory=memory,
                # Retrieval shape (S2 + M3 + M4)
                filters={"section": "memory"},
                with_facets=True,
                hierarchical=False,        # toggled by auto_intent if needed
                auto_intent=True,
                # Quality (M2 + I3)
                reranker=TFIDFReranker(),
                with_provenance=True,
                # Reasoning (I1 + I2 + N3 + I10 + N2)
                self_rag=True,
                self_rag_max_iters=2,
                with_debate=True,
                debate_max_rounds=1,
                with_got=True,
                with_negotiation=True,
                # No time-travel for this demo
                at_commit="",
                top_k=3,
            )

        print("=" * 60)
        print(f"Answer: {result.answer[:160]}")
        print("-" * 60)
        print(f"Passages retrieved: {len(result.retrieved_passages)}")
        for p in result.retrieved_passages:
            print(f"  [{p.score:.2f}] {p.doc_id}")
        print(f"\nFacets: {len(result.facets)} aggregations")
        for f in result.facets:
            print(f"  - {f.field_name}: {f.values[:3]}")
        print(f"\nProvenance: "
              f"{getattr(result.provenance, 'overall_confidence', 0):.3f}")
        print(f"GoT graph: "
              f"{result.got_result.graph.node_count() if result.got_result else 0} nodes")
        print(f"Debate rounds: "
              f"{len(result.debate_result.rounds) if result.debate_result else 0}")
        print(f"Memory recall_count after: "
              f"{memory.stats()['recall_count']}")
        print(f"Latency: {result.duration_ms} ms")
        print("=" * 60)
        print("All 17 features composed without crashing ✓")
        print()
        print(result.to_trace_markdown())


if __name__ == "__main__":
    main()
