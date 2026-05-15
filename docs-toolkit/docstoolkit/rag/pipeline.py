"""RAG pipeline: retrieve → assemble → answer."""
import time
from datetime import datetime

from docstoolkit.rag.types import (
    RAGQuery, AnswerResult, Passage, TraceEvent, _TraceTimer,
)
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
                  max_iters, threshold,
                  pipeline_kwargs: dict | None = None) -> AnswerResult:
    """Sprint 70 / I1 — Self-RAG loop driven by RAGPipeline single-shots.

    Each iteration runs a regular `RAGPipeline.run()` with **all** the
    reasoning/composition flags forwarded via `pipeline_kwargs`, reflects
    on the answer, and re-queries with a refined query when below
    threshold. Returns the AnswerResult of the highest-confidence iteration.

    Phase II.1 fix: `pipeline_kwargs` is a full dict of `RAGPipeline.__init__`
    kwargs, so `with_got`, `with_debate`, `with_negotiation`,
    `with_mapreduce`, `personality`, `memory`, etc. now compose with
    self-RAG instead of being silently dropped.
    """
    from docstoolkit.self_rag.reflect import reflect_on_answer

    pipeline_kwargs = pipeline_kwargs or {}
    best: AnswerResult | None = None
    best_conf: float = -1.0
    current_query = question
    outer_trace: list[TraceEvent] = []
    for it in range(max(1, max_iters)):
        t_iter = time.perf_counter()
        q = RAGQuery(question=current_query, top_k=top_k, method=method,
                     answerer=answerer, model=model)
        res = RAGPipeline(q, **pipeline_kwargs).run()
        try:
            rs = reflect_on_answer(
                question, res.answer, res.retrieved_passages,
                reflect_threshold=threshold,
            )
            conf = float(rs.score) / 10.0
        except Exception:
            conf = 0.0
            rs = None
        outer_trace.append(TraceEvent(
            stage="self_rag_iter",
            t_ms=(time.perf_counter() - t_iter) * 1000.0,
            payload={
                "iter": it + 1,
                "score": getattr(rs, "score", 0.0) if rs else 0.0,
                "confidence": conf,
                "query": current_query[:60],
            },
        ))
        if conf > best_conf:
            best, best_conf = res, conf
        if rs is not None and rs.score >= threshold:
            break
        suggested = getattr(rs, "suggested_query", "") if rs else ""
        if suggested and suggested != current_query:
            current_query = suggested
        else:
            break
    assert best is not None
    # Prepend the per-iteration trace so callers see the reflect loop first,
    # then the stages of the winning iteration's pipeline.
    best.trace = outer_trace + list(best.trace)
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
                 got_max_hypotheses: int = 5,
                 with_debate: bool = False,
                 debate_personas: list | None = None,
                 debate_max_rounds: int = 2,
                 with_mapreduce: bool = False,
                 mapreduce_chunk_size: int = 10,
                 with_negotiation: bool = False,
                 negotiation_budget: int = 5,
                 personality: object = None,
                 learning_queue: object = None,
                 memory: object = None,
                 memory_top_k: int = 3,
                 fusion: object = None):
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
        self.with_debate = with_debate
        self.debate_personas = debate_personas
        self.debate_max_rounds = debate_max_rounds
        self.with_mapreduce = with_mapreduce
        self.mapreduce_chunk_size = mapreduce_chunk_size
        self.with_negotiation = with_negotiation
        self.negotiation_budget = negotiation_budget
        self.personality = personality
        self.learning_queue = learning_queue
        self.memory = memory
        self.memory_top_k = memory_top_k
        self.fusion = fusion
        if fusion is not None and hasattr(fusion, "search"):
            # Replace retriever with a fusion-aware one
            # (caller must wrap FusedRetriever in a `.search()` adapter)
            self.retriever = fusion
        self.answerer = get_answerer(query.answerer, **{})

    def run(self) -> AnswerResult:
        t0 = time.time()
        trace: list[TraceEvent] = []

        # 0. Memory recall (Sprint 74 / I5)
        memory_context: list = []
        if self.memory is not None:
            with _TraceTimer(trace, "memory_recall") as tt:
                try:
                    memory_context = self.memory.recall_search(
                        self.query.question, top_k=self.memory_top_k,
                    )
                except Exception:
                    memory_context = []
                tt.payload["n_recalled"] = len(memory_context)

        # 1. Retrieve (over-fetch when reranking OR filtering so we have room)
        boost = 1
        if self.reranker is not None:
            boost = max(boost, 3)
        if self.filters:
            boost = max(boost, 4)
        retrieve_k = self.query.top_k * boost

        with _TraceTimer(trace, "retrieve") as tt:
            passages = self.retriever.search(self.query.question,
                                              top_k=retrieve_k)
            tt.payload["k"] = retrieve_k
            tt.payload["n_returned"] = len(passages) if passages else 0

        # 1a. Filter
        if self.filters and passages:
            with _TraceTimer(trace, "filter") as tt:
                from docstoolkit.rag.facets import apply_filters
                before = len(passages)
                passages = apply_filters(passages, self.filters)
                tt.payload["dropped"] = before - len(passages)

        # 1b. Rerank
        if self.reranker is not None and passages:
            with _TraceTimer(trace, "rerank") as tt:
                from docstoolkit.rerank.reranker import rerank as _rerank
                passages = _rerank(
                    self.query.question,
                    passages,
                    self.reranker,
                    top_k=self.query.top_k,
                )
                tt.payload["kept"] = len(passages)
        elif self.filters and passages:
            passages = passages[: self.query.top_k]

        # 1c. Personality rerank (Sprint 89 / N9)
        if self.personality is not None and passages:
            with _TraceTimer(trace, "personality_rerank"):
                try:
                    from docstoolkit.personality import PersonalRetriever
                    pr = PersonalRetriever(self.personality)
                    passages = pr.rerank(passages, query=self.query.question)
                    passages = passages[: self.query.top_k]
                except Exception:
                    pass

        # 1d. Negotiation auction (Sprint 85 / N2)
        auction_out = None
        if self.with_negotiation and passages:
            with _TraceTimer(trace, "negotiation_auction") as tt:
                try:
                    from docstoolkit.negotiation import (
                        NegotiationBroker, BrokerConfig,
                    )
                    broker = NegotiationBroker(
                        BrokerConfig(budget=self.negotiation_budget)
                    )
                    auction_out = broker.retrieve(self.query.question, passages)
                    if auction_out.selected_passages:
                        passages = auction_out.selected_passages
                        tt.payload["selected"] = len(passages)
                except Exception:
                    auction_out = None

        if not passages:
            return AnswerResult(
                answer="В корпусе не найдено документов по запросу.",
                query=self.query.question,
                method=self.query.method,
                answerer=self.query.answerer,
                duration_ms=int((time.time() - t0) * 1000),
                trace=trace,
            )

        # 2. Assemble
        with _TraceTimer(trace, "assemble") as tt:
            system, user = assemble_prompt(
                self.query.question, passages,
                max_context_tokens=self.query.max_context_tokens
            )
            tt.payload["prompt_chars"] = len(system) + len(user)

        # 3. Answer (map-reduce shortcut if requested, Sprint 78 / I10)
        mapreduce_out = None
        if self.with_mapreduce and passages:
            with _TraceTimer(trace, "mapreduce_answer") as tt:
                try:
                    from docstoolkit.rag.mapreduce import (
                        map_reduce_ask, MapReduceConfig,
                    )
                    mr_res = map_reduce_ask(
                        self.query.question, passages,
                        cfg=MapReduceConfig(
                            chunk_size=self.mapreduce_chunk_size
                        ),
                    )
                    mapreduce_out = mr_res
                    answer_text = mr_res.final_answer
                    tokens = getattr(mr_res, "total_tokens", 0)
                    cost = getattr(mr_res, "total_cost", 0.0)
                    error = ""
                    tt.payload["chunks"] = getattr(mr_res, "chunk_count", 0)
                except Exception as e:
                    answer_text = ""
                    tokens = 0
                    cost = 0.0
                    error = str(e)
        else:
            with _TraceTimer(trace, "answer") as tt:
                try:
                    answer_text, tokens, cost = self.answerer.answer(
                        system, user, model=self.query.model
                    )
                    error = ""
                    tt.payload["tokens"] = tokens
                except Exception as e:
                    answer_text = f"Ошибка LLM: {e}"
                    tokens = 0
                    cost = 0.0
                    error = str(e)

        # 3b. Multi-agent debate (Sprint 72 / I2) — runs after baseline answer
        debate_out = None
        if self.with_debate and passages:
            with _TraceTimer(trace, "debate") as tt:
                try:
                    from docstoolkit.debate import multi_agent_debate
                    debate_out = multi_agent_debate(
                        self.query.question, passages,
                        personas=self.debate_personas,
                        max_rounds=self.debate_max_rounds,
                    )
                    consensus = getattr(debate_out, "consensus", "") or \
                                getattr(debate_out, "final_answer", "")
                    if consensus:
                        answer_text = consensus
                    tt.payload["rounds"] = len(
                        getattr(debate_out, "rounds", [])
                    )
                except Exception:
                    debate_out = None

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
            with _TraceTimer(trace, "facets") as tt:
                from docstoolkit.rag.facets import aggregate_facets
                facets_out = aggregate_facets(
                    passages, fields=self.facet_fields
                )
                tt.payload["fields"] = len(facets_out)

        # 5. Provenance (Sprint 61 / I3)
        provenance_out = None
        if self.with_provenance and passages and answer_text:
            with _TraceTimer(trace, "provenance"):
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
            with _TraceTimer(trace, "got") as tt:
                try:
                    from docstoolkit.got import GoTReasoner
                    got_out = GoTReasoner(passages).reason(
                        self.query.question,
                        max_hypotheses=self.got_max_hypotheses,
                    )
                    if got_out is not None and getattr(got_out, "graph", None):
                        tt.payload["nodes"] = got_out.graph.node_count()
                except Exception:
                    got_out = None

        # 6b. Update memory with the user turn + assistant reply (Sprint 74 / I5)
        if self.memory is not None and answer_text:
            try:
                self.memory.add_interaction("user", self.query.question)
                self.memory.add_interaction("assistant", answer_text)
            except Exception:
                pass

        # 7. Active learning auto-enqueue (Sprint 73 / M6)
        if self.learning_queue is not None and passages:
            try:
                from docstoolkit.active_learning import (
                    LowConfidenceTrigger, auto_enqueue,
                )
                auto_enqueue(
                    self.query.question,
                    passages,
                    self.learning_queue,
                    LowConfidenceTrigger(threshold=0.3),
                    context={"suggested_answer": answer_text},
                )
            except Exception:
                pass

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
            debate_result=debate_out,
            mapreduce_trace=mapreduce_out,
            auction_result=auction_out,
            trace=trace,
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
        hierarchical: bool = False,
        at_commit: str = "",
        with_debate: bool = False,
        debate_personas: list | None = None,
        debate_max_rounds: int = 2,
        with_mapreduce: bool = False,
        mapreduce_chunk_size: int = 10,
        with_negotiation: bool = False,
        negotiation_budget: int = 5,
        personality: object = None,
        learning_queue: object = None,
        memory: object = None,
        memory_top_k: int = 3,
        fusion: object = None) -> AnswerResult:
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

    # Sprint 79 / I8 — time-travel: rebind corpus to a historical commit
    if at_commit:
        try:
            from docstoolkit.temporal import query_at_time
            t_ans = query_at_time(question, at_commit, top_k=top_k)
            # Build an AnswerResult directly, skipping the regular pipeline.
            ar = AnswerResult(
                answer=t_ans.answer,
                retrieved_passages=list(t_ans.passages),
                citations=[{
                    "n": i + 1,
                    "doc_id": p.doc_id,
                    "title": p.title,
                    "score": p.score,
                } for i, p in enumerate(t_ans.passages)],
                query=question,
                method=method,
                answerer=answerer,
                at_commit=t_ans.commit or at_commit,
            )
            return ar
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
    # Phase II.1 — full pipeline_kwargs dict is shared between self-RAG
    # loop and the single-shot branch, so every reasoning flag composes
    # with `self_rag=True` instead of being silently dropped.
    pipeline_kwargs = dict(
        profile=resolved_profile,
        reranker=reranker,
        filters=filters,
        with_facets=with_facets,
        facet_fields=facet_fields,
        with_provenance=with_provenance,
        with_got=with_got,
        got_max_hypotheses=got_max_hypotheses,
        with_debate=with_debate,
        debate_personas=debate_personas,
        debate_max_rounds=debate_max_rounds,
        with_mapreduce=with_mapreduce,
        mapreduce_chunk_size=mapreduce_chunk_size,
        with_negotiation=with_negotiation,
        negotiation_budget=negotiation_budget,
        personality=personality,
        learning_queue=learning_queue,
        memory=memory,
        memory_top_k=memory_top_k,
        fusion=fusion,
    )
    if self_rag:
        result = _self_rag_run(
            question,
            top_k=top_k,
            method=method,
            answerer=answerer,
            model=model,
            max_iters=self_rag_max_iters,
            threshold=self_rag_threshold,
            pipeline_kwargs=pipeline_kwargs,
        )
    else:
        result = RAGPipeline(query, **pipeline_kwargs).run()
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
