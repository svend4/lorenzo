"""I1 self-RAG + N3 graph-of-thoughts + I2 multi-agent debate.

Three reasoning layers stacked on the same retrieval set.
"""
from __future__ import annotations

from unittest.mock import patch

from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage


class _Retriever:
    def __init__(self):
        self._calls = 0

    def search(self, query, top_k):
        self._calls += 1
        return [
            Passage(text="Python is widely used for RAG implementations.",
                    doc_id="docs/python", title="Python", score=0.9),
            Passage(text="RAG combines retrieval with generation.",
                    doc_id="docs/rag", title="RAG", score=0.85),
            Passage(text="Docker provides reproducible deployment.",
                    doc_id="ops/docker", title="Docker", score=0.7),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "Python + RAG together solve the problem.", 0, 0.0


def main() -> None:
    retriever = _Retriever()
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: retriever), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        result = ask(
            "How do Python and RAG work together?",
            self_rag=True,              # I1
            self_rag_max_iters=2,
            self_rag_threshold=8.0,
            with_got=True,              # N3
            got_max_hypotheses=3,
            with_debate=True,           # I2
            debate_max_rounds=1,
            top_k=3,
        )

    print("Answer:", result.answer)
    print(f"\nRetriever calls (self-RAG re-querying): {retriever._calls}")

    if result.got_result is not None:
        print(f"GoT graph: "
              f"{result.got_result.graph.node_count()} nodes, "
              f"{result.got_result.confirmed_count} confirmed, "
              f"{result.got_result.refuted_count} refuted")
        print(f"GoT synthesis: {result.got_result.final_answer[:100]}")

    if result.debate_result is not None:
        print(f"Debate rounds: {len(result.debate_result.rounds)}")
        if result.debate_result.rounds:
            personas = list(
                result.debate_result.rounds[-1].agent_answers.keys()
            )
            print(f"Personas: {personas}")


if __name__ == "__main__":
    main()
