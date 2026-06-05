"""RAG (Retrieval-Augmented Generation) для docs-toolkit.

Архитектура: 3 слоя
  1. Retriever — поиск top-K релевантных пассажей (через embeddings/HybridSearcher)
  2. Assembler — формирование context-aware промпта с цитатами
  3. Answerer — LLM-вызов (Anthropic/Echo/любой через интерфейс)

Использование:
    from docstoolkit.rag import ask

    answer = ask("Что такое Yodoca?", top_k=5)
    # → AnswerResult с answer + citations + retrieved_passages
"""
from docstoolkit.rag.types import Passage, AnswerResult, RAGQuery, TraceEvent
from docstoolkit.rag.retriever import retrieve_passages, Retriever
from docstoolkit.rag.assembler import assemble_prompt
from docstoolkit.rag.answerer import (
    Answerer, EchoAnswerer, AnthropicAnswerer, get_answerer,
)
from docstoolkit.rag.pipeline import ask, RAGPipeline
from docstoolkit.rag.synthesis import (
    synthesize, compare_sections, SynthesisRequest, SynthesisResult,
    DocumentGroup, SynthesisMode,
)
from docstoolkit.rag.counterfactual import (
    attribute_answer, counterfactual_ask, ForensicRAG,
    AttributedAnswer, CounterfactualResult, SpanAttribution,
)
from docstoolkit.rag.mapreduce import (
    map_reduce_ask, should_use_mapreduce,
    MapReduceConfig, ReduceResult,
)
from docstoolkit.rag.clarifier import (
    detect_ambiguity, build_clarification, apply_clarification,
    ClarifyingRAG, AmbiguityScore, ClarificationRequest,
)
from docstoolkit.rag.hierarchical import (
    hierarchical_search, HierarchicalResult, SectionIndex, DocIndex,
)
from docstoolkit.rag.presets import (
    ask_personalized, ask_high_quality, ask_with_reasoning,
    ask_advanced, ask_research, ask_full_stack,
)

__all__ = [
    "Passage", "AnswerResult", "RAGQuery", "TraceEvent",
    "Retriever", "retrieve_passages",
    "assemble_prompt",
    "Answerer", "EchoAnswerer", "AnthropicAnswerer", "get_answerer",
    "ask", "RAGPipeline",
    # Gap 2: Cross-document synthesis
    "synthesize", "compare_sections", "SynthesisRequest", "SynthesisResult",
    "DocumentGroup", "SynthesisMode",
    # Gap 8: Counterfactual / forensic RAG
    "attribute_answer", "counterfactual_ask", "ForensicRAG",
    "AttributedAnswer", "CounterfactualResult", "SpanAttribution",
    # Gap 10: True long-context map-reduce
    "map_reduce_ask", "should_use_mapreduce", "MapReduceConfig", "ReduceResult",
    # Gap 4: Active clarification
    "detect_ambiguity", "build_clarification", "apply_clarification",
    "ClarifyingRAG", "AmbiguityScore", "ClarificationRequest",
    # M3: Hierarchical retrieval
    "hierarchical_search", "HierarchicalResult", "SectionIndex", "DocIndex",
    # Presets: named bundles of ask() kwargs
    "ask_personalized", "ask_high_quality", "ask_with_reasoning",
    "ask_advanced", "ask_research", "ask_full_stack",
]
