"""RAG pipeline: retrieve → assemble → answer."""
import time
from datetime import datetime

from docstoolkit.rag.types import RAGQuery, AnswerResult, Passage
from docstoolkit.rag.retriever import Retriever
from docstoolkit.rag.assembler import assemble_prompt
from docstoolkit.rag.answerer import get_answerer


class _StaticPassages:
    """Static retriever returning a pre-fetched passage list (for hierarchical)."""

    def __init__(self, passages: list):
        self._p = passages

    def search(self, query: str, top_k: int) -> list:
        return list(self._p[:top_k])


def _self_rag_run(question: str, *, top_k, method, answerer, model,
                  profile, reranker, filters, with_facets, facet_fields,
                  with_provenance, max_iters, threshold) -> AnswerResult:
    """Sprint 70 / I1 — Self-RAG loop driven by RAGPipeline single-shots.

    Each iteration runs a regular `RAGPipeline.run()`, reflects on the
    answer, and re-queries with a refined query when below threshold.
    Returns the AnswerResult of the highest-confidence iteration.
    """
    from docstoolkit.self_rag.reflect import reflect_on_answer

    best: AnswerResult | None = None
    best_conf: float = -1.0
    current_query = question
    iters = 0
    for it in range(max(1, max_iters)):
        iters = it + 1
        q = RAGQuery(question=current_query, top_k=top_k, method=method,
                     answerer=answerer, model=model)
        res = RAGPipeline(
            q, profile=profile, reranker=reranker, filters=filters,
            with_facets=with_facets, facet_fields=facet_fields,
            with_provenance=with_provenance,
        ).run()
        try:
            rs = reflect_on_answer(
                question, res.answer, res.retrieved_passages,
                reflect_threshold=threshold,
            )
            conf = float(rs.score) / 10.0
        except Exception:
            conf = 0.0
            rs = None
        if conf > best_conf:
            best, best_conf = res, conf
        if rs is not None and rs.score >= threshold:
            break
        # Refine query for the next attempt
        suggested = getattr(rs, "suggested_query", "") if rs else ""
        if suggested and suggested != current_query:
            current_query = suggested
        else:
            # No more progress signal — stop early
            break
    assert best is not None
    return best


class RAGPipeline:
    """Конфигурируемый pipeline RAG."""

    def __init__(self, query: RAGQuery, profile=None, reranker=None,
                 rerank_top_k: int | None = None,
                 filters: dict | None = None,
                 with_facets: bool = False,
                 facet_fields: tuple = ("section", "tag", "year"),
                 with_provenance: bool = False,
                 with_got: bool = False,
                 got_max_hypotheses: int = 5):
        self.query = query
        self.profile = profile
        self.retriever = Retriever(method=query.method, model=query.model)
        if profile is not None:
            from docstoolkit.conversation.profile import PersonalizedRetriever
            self.retriever = PersonalizedRetriever(self.retriever, profile)
        self.reranker = reranker
        self.rerank_top_k = rerank_top_k
        self.filters = filters or {}
        self.with_facets = with_facets
        self.facet_fields = facet_fields
        self.with_provenance = with_provenance
        self.with_got = with_got
        self.got_max_hypotheses = got_max_hypotheses
        self.answerer = get_answerer(query.answerer, **{})

    def run(self) -> AnswerResult:
        t0 = time.time()

        # 1. Retrieve (over-fetch when reranking OR filtering so we have room)
        boost = 1
        if self.reranker is not None:
            boost = max(boost, 3)
        if self.filters:
            boost = max(boost, 4)
        retrieve_k = self.query.top_k * boost

        passages = self.retriever.search(self.query.question,
                                          top_k=retrieve_k)

        # 1a. Filter
        if self.filters and passages:
            from docstoolkit.rag.facets import apply_filters
            passages = apply_filters(passages, self.filters)

        # 1b. Rerank
        if self.reranker is not None and passages:
            from docstoolkit.rerank.reranker import rerank as _rerank
            passages = _rerank(
                self.query.question,
                passages,
                self.reranker,
                top_k=self.query.top_k,
            )
        elif self.filters and passages:
            passages = passages[: self.query.top_k]

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

        # 4. Facets (Sprint 55 / S2)
        facets_out: list = []
        if self.with_facets and passages:
            from docstoolkit.rag.facets import aggregate_facets
            facets_out = aggregate_facets(passages, fields=self.facet_fields)

        # 5. Provenance (Sprint 61 / I3)
        provenance_out = None
        if self.with_provenance and passages and answer_text:
            try:
                from docstoolkit.provenance import ask_with_provenance
                provenance_out = ask_with_provenance(
                    self.query.question, answer_text, passages,
                )
            except Exception:
                provenance_out = None

        # 6. Graph-of-thoughts (Sprint 75 / N3)
        got_out = None
        if self.with_got and passages:
            try:
                from docstoolkit.got import GoTReasoner
                got_out = GoTReasoner(passages).reason(
                    self.query.question,
                    max_hypotheses=self.got_max_hypotheses,
                )
            except Exception:
                got_out = None

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
            facets=facets_out,
            provenance=provenance_out,
            got_result=got_out,
        )


def ask(question: str, *,
        top_k: int = 5,
        method: str = "hybrid",
        answerer: str = "echo",
        model: str = "claude-haiku-4-5-20251001",
        user_id: str = "",
        profile=None,
        eval_runner=None,
        reranker=None,
        filters: dict | None = None,
        with_facets: bool = False,
        facet_fields: tuple = ("section", "tag", "year"),
        with_provenance: bool = False,
        self_rag: bool = False,
        self_rag_max_iters: int = 3,
        self_rag_threshold: float = 7.0,
        with_got: bool = False,
        got_max_hypotheses: int = 5,
        auto_intent: bool = False,
        hierarchical: bool = False) -> AnswerResult:
    """Удобная обёртка для one-shot запроса.

    Per-user personalization (Sprint 54 / S6):
      - `user_id` non-empty → ProfileStore.load(user_id) и personalized retrieval.
      - `profile` overrides ProfileStore lookup (useful for tests).
      - Caller-provided `method` всегда побеждает `profile.preferred_retriever`.

    Continuous online eval (Sprint 56 / M5):
      - `eval_runner=OnlineEvalRunner(...)` → каждый запрос проходит через sampler,
        попавшие в выборку сравниваются с golden dataset и пишутся в SQLite.

    Cross-encoder reranking (Sprint 59 / M2):
      - `reranker=get_reranker("bge")` (или "tfidf"/"llm"/"noop") применяется
        после первичного retrieval. Pipeline сам берёт top_k*3 кандидатов
        и режет до top_k после реранкинга.
    """
    # Sprint 68 / M4 — intent-based pipeline routing
    if auto_intent:
        try:
            from docstoolkit.intent import IntentRouter
            _, cfg = IntentRouter().route(question)
            if method == "hybrid":
                method = cfg.retriever or method
            if top_k == 5:
                top_k = cfg.top_k or top_k
            if cfg.use_hierarchical and not hierarchical:
                hierarchical = True
        except Exception:
            pass

    # Sprint 67 / M3 — hierarchical retrieval shortcut
    if hierarchical:
        try:
            from docstoolkit.rag.hierarchical import hierarchical_search
            h_result = hierarchical_search(
                question, top_k_passages=top_k,
            )
            passages = list(h_result.passages)[:top_k]
            # Build a minimal AnswerResult with hierarchical passages,
            # then defer to assembler+answerer for the answer text.
            q = RAGQuery(question=question, top_k=top_k, method=method,
                         answerer=answerer, model=model)
            pipe = RAGPipeline(q, profile=profile, reranker=reranker,
                               filters=filters, with_facets=with_facets,
                               facet_fields=facet_fields,
                               with_provenance=with_provenance,
                               with_got=with_got,
                               got_max_hypotheses=got_max_hypotheses)
            # Swap in a retriever that returns the hierarchical passages
            pipe.retriever = _StaticPassages(passages)
            return pipe.run()
        except Exception:
            # Fall through to standard pipeline on any error
            pass

    explicit_method = method
    resolved_profile = profile
    if user_id and resolved_profile is None:
        from docstoolkit.conversation.profile import ProfileStore
        store = ProfileStore()
        try:
            resolved_profile = store.load(user_id)
        finally:
            store.close()
    if resolved_profile is not None and explicit_method == "hybrid":
        # Default only — honour profile's preferred_retriever.
        method = resolved_profile.preferred_retriever or method
    query = RAGQuery(
        question=question,
        top_k=top_k,
        method=method,
        answerer=answerer,
        model=model,
    )
    if self_rag:
        result = _self_rag_run(
            question,
            top_k=top_k,
            method=method,
            answerer=answerer,
            model=model,
            profile=resolved_profile,
            reranker=reranker,
            filters=filters,
            with_facets=with_facets,
            facet_fields=facet_fields,
            with_provenance=with_provenance,
            max_iters=self_rag_max_iters,
            threshold=self_rag_threshold,
        )
    else:
        result = RAGPipeline(
            query,
            profile=resolved_profile,
            reranker=reranker,
            filters=filters,
            with_facets=with_facets,
            facet_fields=facet_fields,
            with_provenance=with_provenance,
            with_got=with_got,
            got_max_hypotheses=got_max_hypotheses,
        ).run()
    if eval_runner is not None:
        try:
            eval_runner.maybe_run(question, result)
        except Exception:
            # Online eval is best-effort; never fail user requests.
            pass
    # Sprint 60 / S7 — read receipts: mark retrieved passages as "read" for the user.
    if user_id and result.retrieved_passages:
        try:
            from docstoolkit.conversation.profile import ProfileStore
            store = ProfileStore()
            try:
                for p in result.retrieved_passages:
                    if p.doc_id:
                        store.mark_read(user_id, p.doc_id)
            finally:
                store.close()
        except Exception:
            pass
    return result
