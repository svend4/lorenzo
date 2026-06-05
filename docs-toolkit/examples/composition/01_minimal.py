"""Baseline RAG ask() — no extras.

Demonstrates the simplest possible invocation. Uses the in-memory `echo`
answerer so the script runs without network access or API keys.
"""
from __future__ import annotations

from unittest.mock import patch

from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage


class _Retriever:
    def search(self, query, top_k):
        return [
            Passage(text="Python is a programming language widely used in AI.",
                    doc_id="docs/python", title="Python", score=0.92),
            Passage(text="RAG combines retrieval with generation for grounded answers.",
                    doc_id="docs/rag", title="RAG", score=0.85),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "Python + RAG are common building blocks for grounded AI.", 0, 0.0


def main() -> None:
    with patch("docstoolkit.rag.pipeline.Retriever", lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        result = ask("How does RAG work?")

    print("Answer:", result.answer)
    print("Passages:")
    for p in result.retrieved_passages:
        print(f"  [{p.score:.2f}] {p.doc_id}")
    print(f"Latency: {result.duration_ms} ms")


if __name__ == "__main__":
    main()
