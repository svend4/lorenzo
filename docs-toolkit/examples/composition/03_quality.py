"""M2 cross-encoder rerank + I3 provenance + M5 online eval.

Shows how to lift answer quality with three orthogonal mechanisms in one
ask() call.
"""
from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from docstoolkit.online_eval import (
    OnlineEvalRunner,
    OnlineEvalSampler,
    OnlineEvalStore,
)
from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage
from docstoolkit.rerank.reranker import TFIDFReranker


class _Retriever:
    """Returns intentionally mis-ordered candidates so the reranker matters."""

    def search(self, query, top_k):
        return [
            Passage(text="Docker is a container platform unrelated here.",
                    doc_id="ops/docker", title="Docker", score=0.95),
            Passage(text="RAG retrieves passages and feeds them to an LLM.",
                    doc_id="docs/rag", title="RAG", score=0.10),
            Passage(text="Python is a language used for RAG implementations.",
                    doc_id="docs/python", title="Python", score=0.50),
            Passage(text="Yodoca is a Habr memory project.",
                    doc_id="memory/yodoca", title="Yodoca", score=0.20),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "RAG combines retrieval with generation.", 0, 0.0


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        # Online eval — sample every query for the demo
        eval_store = OnlineEvalStore(db_path=Path(tmp) / "eval.sqlite")
        try:
            runner = OnlineEvalRunner(
                store=eval_store,
                sampler=OnlineEvalSampler(sample_rate=1.0),
            )

            with patch("docstoolkit.rag.pipeline.Retriever",
                       lambda **kw: _Retriever()), \
                 patch("docstoolkit.rag.pipeline.get_answerer",
                       lambda name, **kw: _Answerer()):
                result = ask(
                    "What is RAG?",
                    reranker=TFIDFReranker(),     # M2
                    with_provenance=True,          # I3
                    eval_runner=runner,            # M5
                    top_k=3,
                )

            print("Answer:", result.answer)
            print("\nReranked top passages (TF-IDF overlap with query):")
            for p in result.retrieved_passages:
                print(f"  [{p.score:.3f}] {p.doc_id}")

            if result.provenance is not None:
                print(f"\nProvenance: "
                      f"{len(result.provenance.claims)} claims, "
                      f"overall confidence "
                      f"{result.provenance.overall_confidence:.2f}")

            stats = eval_store.current_stats(days=7)
            print(f"\nOnline eval recorded — current stats: "
                  f"precision={stats.get('precision', 0):.2f}, "
                  f"f1={stats.get('f1', 0):.2f}")
        finally:
            eval_store.close()


if __name__ == "__main__":
    main()
