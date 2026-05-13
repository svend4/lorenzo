"""Self-RAG: reflection-driven iterative retrieval and answering."""
from docstoolkit.self_rag.tokens import (
    DecisionToken,
    parse_decision,
    NEED_RETRIEVAL,
    NO_RETRIEVAL,
    REFLECT,
    ANSWER_OK,
    ANSWER_INSUFFICIENT,
)
from docstoolkit.self_rag.reflect import reflect_on_answer, ReflectScore
from docstoolkit.self_rag.loop import ReflectStep, SelfRAGResult, self_rag_ask

__all__ = [
    "DecisionToken",
    "parse_decision",
    "NEED_RETRIEVAL",
    "NO_RETRIEVAL",
    "REFLECT",
    "ANSWER_OK",
    "ANSWER_INSUFFICIENT",
    "reflect_on_answer",
    "ReflectScore",
    "ReflectStep",
    "SelfRAGResult",
    "self_rag_ask",
]
