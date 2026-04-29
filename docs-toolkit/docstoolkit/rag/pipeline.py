"""RAG pipeline: retrieve → assemble → answer."""
import time
from datetime import datetime

from docstoolkit.rag.types import RAGQuery, AnswerResult, Passage
from docstoolkit.rag.retriever import Retriever
from docstoolkit.rag.assembler import assemble_prompt
from docstoolkit.rag.answerer import get_answerer


class RAGPipeline:
    """Конфигурируемый pipeline RAG."""

    def __init__(self, query: RAGQuery):
        self.query = query
        self.retriever = Retriever(method=query.method, model=query.model)
        self.answerer = get_answerer(query.answerer, **{})

    def run(self) -> AnswerResult:
        t0 = time.time()

        # 1. Retrieve
        passages = self.retriever.search(self.query.question,
                                          top_k=self.query.top_k)

        if not passages:
            return AnswerResult(
                answer="В корпусе не найдено документов по запросу.",
                query=self.query.question,
                method=self.query.method,
                answerer=self.query.answerer,
                duration_ms=int((time.time() - t0) * 1000),
            )

        # 2. Assemble
        system, user = assemble_prompt(
            self.query.question, passages,
            max_context_tokens=self.query.max_context_tokens
        )

        # 3. Answer
        try:
            answer_text, tokens, cost = self.answerer.answer(
                system, user, model=self.query.model
            )
            error = ""
        except Exception as e:
            answer_text = f"Ошибка LLM: {e}"
            tokens = 0
            cost = 0.0
            error = str(e)

        # Citations
        citations = []
        if self.query.include_citations:
            for i, p in enumerate(passages, 1):
                citations.append({
                    "n": i,
                    "doc_id": p.doc_id,
                    "title": p.title,
                    "score": p.score,
                })

        duration_ms = int((time.time() - t0) * 1000)

        return AnswerResult(
            answer=answer_text,
            citations=citations,
            retrieved_passages=passages,
            query=self.query.question,
            method=self.query.method,
            answerer=self.query.answerer,
            duration_ms=duration_ms,
            cost_estimate=cost,
            tokens_used=tokens,
            error=error,
        )


def ask(question: str, *,
        top_k: int = 5,
        method: str = "hybrid",
        answerer: str = "echo",
        model: str = "claude-haiku-4-5-20251001") -> AnswerResult:
    """Удобная обёртка для one-shot запроса."""
    query = RAGQuery(
        question=question,
        top_k=top_k,
        method=method,
        answerer=answerer,
        model=model,
    )
    return RAGPipeline(query).run()
