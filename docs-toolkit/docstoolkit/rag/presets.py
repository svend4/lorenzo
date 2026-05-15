"""Named bundles of `ask()` kwargs for common use-cases.

Each preset is a thin wrapper that forwards extra kwargs, so any caller-supplied
flag still wins over the preset default. The bundles mirror the demos in
`examples/composition/`:

- `ask_personalized`  — Sprint 54 / S6 (user profile) + S7 read-receipts
- `ask_high_quality`  — M2 rerank + I3 provenance + M5 online eval
- `ask_with_reasoning` — I1 self-RAG + N3 graph-of-thoughts + I2 debate
- `ask_advanced`      — M3 hierarchical + M4 auto-intent + I10 mapreduce
- `ask_research`      — N2 negotiation + N9 personality + I5 MemGPT memory
- `ask_full_stack`    — every feature stacked (matches `08_full_stack.py`)

Example:
    from docstoolkit.rag.presets import ask_high_quality
    from docstoolkit.rerank.reranker import TFIDFReranker

    result = ask_high_quality(
        "What is RAG?",
        reranker=TFIDFReranker(),
        top_k=5,
    )
"""
from __future__ import annotations

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import AnswerResult


def ask_personalized(question: str, user_id: str, **kwargs) -> AnswerResult:
    """S6 per-user preferences + S7 read-receipts.

    Loads `UserProfile` for `user_id` and applies `preferred_retriever`,
    `preferred_sections`, `interests`; auto-records read-receipts.
    """
    kwargs.setdefault("top_k", 5)
    return ask(question, user_id=user_id, **kwargs)


def ask_high_quality(question: str, *, reranker=None, **kwargs) -> AnswerResult:
    """M2 cross-encoder rerank + I3 provenance + M5 online eval.

    Pass `reranker=TFIDFReranker()` (or `BGEReranker()`) for production
    reranking; defaults to None which falls back to plain hybrid ordering.
    """
    if reranker is not None:
        kwargs["reranker"] = reranker
    kwargs.setdefault("with_provenance", True)
    kwargs.setdefault("top_k", 5)
    return ask(question, **kwargs)


def ask_with_reasoning(question: str, **kwargs) -> AnswerResult:
    """I1 self-RAG + N3 graph-of-thoughts + I2 multi-agent debate.

    Heaviest of the presets — runs reflect loop, GoT hypothesis graph,
    and debate rounds. Since Phase II.1 (commit unifying `_self_rag_run`
    with `pipeline_kwargs`) all three compose orthogonally; the last
    iteration's `got_result` / `debate_result` are visible on the final
    `AnswerResult`.

    Use for high-stakes queries where reasoning depth matters more than
    latency.
    """
    kwargs.setdefault("self_rag", True)
    kwargs.setdefault("self_rag_max_iters", 2)
    kwargs.setdefault("with_got", True)
    kwargs.setdefault("got_max_hypotheses", 3)
    kwargs.setdefault("with_debate", True)
    kwargs.setdefault("debate_max_rounds", 1)
    kwargs.setdefault("top_k", 5)
    return ask(question, **kwargs)


def ask_advanced(question: str, **kwargs) -> AnswerResult:
    """M3 hierarchical + M4 auto-intent routing + I10 mapreduce synthesis.

    Best for long-context queries over large corpora where retrieval shape
    and chunk synthesis matter more than reasoning depth.
    """
    kwargs.setdefault("hierarchical", True)
    kwargs.setdefault("auto_intent", True)
    kwargs.setdefault("with_mapreduce", True)
    kwargs.setdefault("mapreduce_chunk_size", 10)
    kwargs.setdefault("top_k", 5)
    return ask(question, **kwargs)


def ask_research(
    question: str,
    *,
    memory=None,
    personality=None,
    **kwargs,
) -> AnswerResult:
    """N2 negotiation + N9 personality + I5 MemGPT memory.

    Path C research bundle: auction-based retrieval, cognitive-style rerank,
    and tiered memory. Pass `memory=TieredMemory()` to persist conversation
    history; pass `personality=CognitiveProfile(...)` to bias retrieval.
    """
    if memory is not None:
        kwargs["memory"] = memory
    if personality is not None:
        kwargs["personality"] = personality
    kwargs.setdefault("with_negotiation", True)
    kwargs.setdefault("negotiation_budget", 3)
    kwargs.setdefault("top_k", 5)
    return ask(question, **kwargs)


def ask_full_stack(
    question: str,
    *,
    user_id: str = "",
    memory=None,
    personality=None,
    reranker=None,
    **kwargs,
) -> AnswerResult:
    """Every feature in one call — matches `examples/composition/08_full_stack.py`.

    Stress-test bundle; expect ~300-500 μs of overhead vs `ask()` baseline
    on a stubbed Retriever/Answerer (real retrieval/LLM cost dominates).
    """
    if user_id:
        kwargs["user_id"] = user_id
    if memory is not None:
        kwargs["memory"] = memory
    if personality is not None:
        kwargs["personality"] = personality
    if reranker is not None:
        kwargs["reranker"] = reranker
    kwargs.setdefault("with_facets", True)
    kwargs.setdefault("auto_intent", True)
    kwargs.setdefault("with_provenance", True)
    # Phase II.1: self_rag now composes with got/debate/negotiation.
    kwargs.setdefault("self_rag", True)
    kwargs.setdefault("self_rag_max_iters", 2)
    kwargs.setdefault("with_debate", True)
    kwargs.setdefault("debate_max_rounds", 1)
    kwargs.setdefault("with_got", True)
    kwargs.setdefault("got_max_hypotheses", 3)
    kwargs.setdefault("with_negotiation", True)
    kwargs.setdefault("negotiation_budget", 3)
    kwargs.setdefault("top_k", 3)
    return ask(question, **kwargs)


__all__ = [
    "ask_personalized",
    "ask_high_quality",
    "ask_with_reasoning",
    "ask_advanced",
    "ask_research",
    "ask_full_stack",
]
