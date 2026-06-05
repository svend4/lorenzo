"""Self-RAG iterative retrieval-reflection loop."""
from dataclasses import dataclass, field
from typing import Callable

from docstoolkit.self_rag.reflect import reflect_on_answer, ReflectScore
from docstoolkit.self_rag.tokens import DecisionToken, parse_decision


@dataclass
class ReflectStep:
    iteration: int
    decision: str                     # "retrieve" | "answer" | "reflect" | "stop"
    query: str
    n_passages: int                   # how many passages were available
    answer: str
    reflect_score: float              # 0-10
    issues: list[str]                 # missing topics
    suggested_query: str = ""


@dataclass
class SelfRAGResult:
    final_answer: str
    steps: list[ReflectStep]
    total_retrievals: int
    total_iterations: int
    confidence: float                 # final reflect_score / 10


def self_rag_ask(
    question: str,
    *,
    retriever_fn: Callable[[str, int], list] | None = None,
    answerer_fn: Callable[[str, list], str] | None = None,
    max_iterations: int = 4,
    reflect_threshold: float = 7.0,
    top_k: int = 5,
) -> SelfRAGResult:
    """Self-RAG loop.

    If retriever_fn is None: always return [] (no retrieval, forces quick answer)
    If answerer_fn is None: return question[:100] as answer (echo)

    Loop:
    1. iteration 0: retrieve(question, top_k) → passages
    2. answerer_fn(query, passages) → answer
    3. reflect_on_answer(question, answer, passages) → score
    4. If score >= reflect_threshold OR iteration >= max_iterations: STOP
    5. Else: query = suggested_query, go to step 1 (re-retrieve)

    Record each iteration as ReflectStep.
    Return SelfRAGResult with all steps.
    """
    # Defaults
    if retriever_fn is None:
        retriever_fn = lambda q, k: []  # noqa: E731

    if answerer_fn is None:
        answerer_fn = lambda q, passages: q[:100]  # noqa: E731

    steps: list[ReflectStep] = []
    total_retrievals = 0
    current_query = question
    last_reflect: ReflectScore | None = None

    for iteration in range(max_iterations):
        # 1. Retrieve
        passages = retriever_fn(current_query, top_k)
        total_retrievals += 1

        # 2. Answer
        answer = answerer_fn(current_query, passages)

        # 3. Reflect
        rs = reflect_on_answer(
            question,          # always reflect against original question
            answer,
            passages,
            reflect_threshold=reflect_threshold,
        )
        last_reflect = rs

        # 4. Determine decision for this step
        is_last = (iteration == max_iterations - 1)
        if rs.score >= reflect_threshold or is_last:
            decision = "stop"
        else:
            decision = "reflect"

        step = ReflectStep(
            iteration=iteration,
            decision=decision,
            query=current_query,
            n_passages=len(passages),
            answer=answer,
            reflect_score=rs.score,
            issues=rs.missing_topics,
            suggested_query=rs.suggested_query,
        )
        steps.append(step)

        if decision == "stop":
            break

        # 5. Update query for next iteration
        current_query = rs.suggested_query

    final_answer = steps[-1].answer if steps else question[:100]
    final_score = last_reflect.score if last_reflect is not None else 0.0
    confidence = max(0.0, min(1.0, final_score / 10.0))

    return SelfRAGResult(
        final_answer=final_answer,
        steps=steps,
        total_retrievals=total_retrievals,
        total_iterations=len(steps),
        confidence=confidence,
    )
