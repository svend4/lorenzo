"""M3 hierarchical + M4 auto-intent + I10 mapreduce + I8 time-travel.

These four mostly affect retrieval shape / answer-assembly, not the
reasoning loop.
"""
from __future__ import annotations

from unittest.mock import patch

from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage


class _Retriever:
    def search(self, query, top_k):
        return [
            Passage(text=f"passage about {query} number {i}",
                    doc_id=f"docs/p{i}", title=f"P{i}", score=0.9 - i * 0.1)
            for i in range(top_k)
        ]


class _Answerer:
    def answer(self, system, user, model=""):
        return f"Answer based on {user.count('passage')} passages.", 0, 0.0


def main() -> None:
    print("=" * 60)
    print("M4 — Auto-intent routing")
    print("=" * 60)
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        for q, label in [
            ("When was Anthropic founded?", "factoid"),
            ("Compare BM25 vs TF-IDF retrieval", "comparison"),
            ("Summarise the Knowledge OS architecture in one paragraph",
             "synthesis"),
        ]:
            r = ask(q, auto_intent=True)
            print(f"  [{label}] method={r.method} top_k={len(r.retrieved_passages)}")

    print("\n" + "=" * 60)
    print("I10 — Map-reduce summarisation over many passages")
    print("=" * 60)
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        r = ask("summarise everything", top_k=15,
                with_mapreduce=True, mapreduce_chunk_size=5)
    print(f"  Answer: {r.answer}")
    print(f"  Mapreduce trace: "
          f"{'present' if r.mapreduce_trace else 'absent'}")

    print("\n" + "=" * 60)
    print("I8 — Time-travel (stubbed)")
    print("=" * 60)
    from docstoolkit.temporal import TemporalAnswer

    def fake_qat(query, commit_or_ts, **kw):
        return TemporalAnswer(
            answer=f"Historical answer as of {commit_or_ts[:7]}",
            passages=[Passage(text="old", doc_id="docs/old", title="Old",
                              score=0.5)],
            timestamp="2024-01-01",
            commit=commit_or_ts,
            doc_count=1,
        )

    with patch("docstoolkit.temporal.query_at_time", fake_qat):
        r = ask("what was RAG?", at_commit="abc1234def")
    print(f"  Answer: {r.answer}")
    print(f"  at_commit: {r.at_commit}")


if __name__ == "__main__":
    main()
