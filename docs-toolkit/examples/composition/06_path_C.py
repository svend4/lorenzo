"""Path C: N2 negotiation + N9 personality + I5 MemGPT memory + N1 metabolism.

Novel-research bets composed in one demo.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from docstoolkit.memory import TieredMemory
from docstoolkit.metabolism import propose_rewrite, rank_stale_documents
from docstoolkit.personality import CognitiveProfile
from docstoolkit.rag import ask
from docstoolkit.rag.types import Passage


class _Retriever:
    def search(self, query, top_k):
        return [
            Passage(text="Skeptical: this may be wrong, more evidence needed.",
                    doc_id="docs/skeptic", title="Skeptic", score=0.8),
            Passage(text="Synthesised: agents combine memory with retrieval.",
                    doc_id="docs/synthesis", title="Synthesis", score=0.7),
            Passage(text="Verified: experiments confirm the hypothesis.",
                    doc_id="docs/verified", title="Verified", score=0.6),
            Passage(text="Pragmatic: ship the simplest version first.",
                    doc_id="docs/pragmatic", title="Pragmatic", score=0.5),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "Memory-augmented agents are the path forward.", 0, 0.0


def _iso(days_ago: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def main() -> None:
    print("=" * 60)
    print("N9 — Personality re-ranking (skeptical profile)")
    print("=" * 60)
    profile = CognitiveProfile(
        skepticism=0.9, synthesis=0.1, verification=0.5,
        pragmatism=0.1, exploration=0.5,
    )
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        r = ask("how to build agents?", personality=profile, top_k=4)
    print("Top after personality rerank:")
    for p in r.retrieved_passages:
        print(f"  [{p.score:.3f}] {p.doc_id}")

    print("\n" + "=" * 60)
    print("I5 — MemGPT-style memory persists user/assistant turns")
    print("=" * 60)
    memory = TieredMemory()
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        ask("first question about agents", memory=memory)
        ask("second question about memory", memory=memory)
    stats = memory.stats()
    print(f"  recall_count={stats['recall_count']}, "
          f"working={stats['working_messages']}, "
          f"archival={stats['archival_count']}")

    print("\n" + "=" * 60)
    print("N2 — Multi-agent retrieval auction")
    print("=" * 60)
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        r = ask("agents and memory", with_negotiation=True,
                negotiation_budget=2, top_k=4)
    if r.auction_result is not None:
        print(f"  Selected by auction: "
              f"{len(r.auction_result.selected_passages)} passages")
        print(f"  Winning agent: {r.auction_result.winning_agent()}")
    else:
        print("  (auction returned no result)")

    print("\n" + "=" * 60)
    print("N1 — Document metabolism proposal")
    print("=" * 60)
    docs = [
        ("old/architecture", "Old text about old patterns.",
         _iso(400)),
        ("old/intro", "Intro text written years ago.",
         _iso(300)),
        ("fresh/recent", "Recent thoughts.", _iso(10)),
    ]
    stale = rank_stale_documents(docs, threshold_days=180.0)
    print(f"  Stale candidates: {[d[0] for d in stale]}")
    if stale:
        target_id, age = stale[0]
        target_content = next(c for d, c, _ in docs if d == target_id)
        proposal = propose_rewrite(
            target_id, target_content,
            sources=[("fresh/recent",
                      "Recent thoughts about old patterns updated.")],
            last_modified_iso=_iso(age.days_since_update),
            min_relevance=0.1,
        )
        print(f"  State: {proposal.target_state.value}")
        print(f"  Fragments absorbed: {len(proposal.fragments)}")


if __name__ == "__main__":
    main()
