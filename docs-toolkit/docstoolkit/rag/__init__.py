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
from docstoolkit.rag.types import Passage, AnswerResult, RAGQuery
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

__all__ = [
    "Passage", "AnswerResult", "RAGQuery",
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
]
