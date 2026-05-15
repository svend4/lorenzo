# `ask()` Composition Guide — docs-toolkit

Документация **17 ортогональных фич** через single entry point
`docstoolkit.rag.ask()` плюс **18 standalone-хелперов**. Покрывает все
35 roadmap-пунктов: Path A (Quick Value), Path B (Differentiation),
Path C (Long-game).

## Полный feature-индекс

| Kwarg | Roadmap | Якорь |
|---|---|---|
| `user_id` | S6 | [Sprint 54](#sprint-54--s6--per-user-preferences) |
| `filters`, `with_facets` | S2 | [Sprint 55](#sprint-55--s2--faceted-aggregation--filters) |
| `with_provenance` | I3 | [Sprint 61](#sprint-61--i3--provenance--confidence-intervals) |
| `reranker` | M2 | [Sprint 59](#sprint-59--m2--cross-encoder-reranking) |
| `eval_runner` | M5 | [Sprint 56](#sprint-56--m5--continuous-online-eval) |
| (auto) | S7 | [Sprint 60](#sprint-60--s7--read-receipt-tracking) |
| `self_rag`, `self_rag_max_iters`, `self_rag_threshold` | I1 | [Sprint 70](#sprint-70--i1--self-rag-loop) |
| `auto_intent` | M4 | [Sprint 68 / M4](#sprint-68--m4--auto-intent-routing) |
| `hierarchical` | M3 | [Sprint 67 / M3](#sprint-67--m3--hierarchical-retrieval) |
| `with_debate`, `debate_personas`, `debate_max_rounds` | I2 | I2 (multi-agent) |
| `with_mapreduce`, `mapreduce_chunk_size` | I10 | I10 (map-reduce) |
| `with_got`, `got_max_hypotheses` | N3 | [Sprint 75](#sprint-75--n3--graph-of-thoughts) |
| `with_negotiation`, `negotiation_budget` | N2 | N2 (auction) |
| `personality` | N9 | N9 (cognitive style) |
| `learning_queue` | M6 | M6 (active learning) |
| `at_commit` | I8 | I8 (time-travel) |
| `memory`, `memory_top_k` | I5 | I5 (MemGPT) |

Standalone helpers — см. [`API.md`](API.md) и финальный
раздел "Полная композиция".

## Named presets (`docstoolkit.rag.presets`)

Чтобы не запоминать, какие флаги хорошо композируются вместе, в
`docstoolkit.rag.presets` есть шесть именованных бандлов. Каждый — тонкая
обёртка над `ask()`, поэтому любой kwarg от вызова переопределяет дефолт
пресета.

| Preset | Что включает | Когда использовать |
|---|---|---|
| `ask_personalized(q, user_id, ...)` | S6 profile + S7 read-receipts | мульти-пользовательский UI |
| `ask_high_quality(q, reranker=...)` | M2 rerank + I3 provenance | критичные ответы с CI |
| `ask_with_reasoning(q, ...)` | N3 GoT + I2 debate | глубокое объяснение, не latency |
| `ask_advanced(q, ...)` | M3 hierarchical + M4 auto-intent + I10 mapreduce | большой корпус, long-context |
| `ask_research(q, memory=..., personality=...)` | N2 negotiation + N9 personality + I5 memory | Path C research bundle |
| `ask_full_stack(q, ...)` | все 14 совместимых фич | стресс-тест / "kitchen sink" |

```python
from docstoolkit.rag import ask_high_quality
from docstoolkit.rerank.reranker import TFIDFReranker

result = ask_high_quality("What is RAG?", reranker=TFIDFReranker(), top_k=5)
# result.provenance.overall_confidence — bootstrap CI для ответа
```

**Note:** `self_rag=True` короткозамыкает pipeline и пропускает GoT/debate/
negotiation, поэтому пресеты `ask_with_reasoning` и `ask_full_stack` не
включают self-RAG по умолчанию. Передайте `self_rag=True` явно, если
предпочитаете reflect-loop вариант.

---

## Документация фичей Пути A — Quick Value (Sprint 54-60 / S6, S4, M2, M5, S7)
Все 5 фич доступны через single entry point `docstoolkit.rag.ask()`.

## Sprint 54 / S6 — Per-User Preferences

`UserProfile` хранит per-user defaults: `preferred_retriever`, `preferred_sections`,
`interests`, `read_docs`. Профиль персистится в SQLite (`.docstoolkit/profiles.sqlite`).

### CLI / Python API

```python
from docstoolkit.conversation.profile import (
    ProfileStore, UserProfile, apply_profile,
)
from docstoolkit.rag import ask

store = ProfileStore()
store.save(UserProfile(
    user_id="alice",
    preferred_retriever="bm25",
    preferred_sections=["05-habr-projects"],
    interests=["memory", "agents"],
))

# Alice's query — автоматически использует bm25 + section boost + interest injection
result = ask("Что такое RAG?", user_id="alice")
```

Приоритет: явный `method=...` в `ask()` всегда побеждает `preferred_retriever`.
Если профиль отсутствует — поведение не меняется (no-op).

### apply_profile middleware

Используется внутри `ask()`, но доступна как public API для agent.run /
custom pipelines:

```python
from docstoolkit.conversation.profile import apply_profile

kwargs = {"top_k": 5}
apply_profile("alice", kwargs)  # mutates in place + returns
# kwargs == {"top_k": 5, "method": "bm25", "_profile": <UserProfile>}
```

## Sprint 56 / S4 — Citation Graph + PageRank Boost

`PageRankBoostedRetriever` оборачивает любой retriever и поднимает в выдаче
документы с высоким PageRank по графу внутренних markdown-ссылок.

```python
from pathlib import Path
from docstoolkit.citations import PageRankBoostedRetriever
from docstoolkit.rag.retriever import Retriever

base = Retriever(method="hybrid")
boosted = PageRankBoostedRetriever(
    base=base,
    corpus_dir=Path("docs"),
    alpha=0.3,   # boost intensity
    cap=0.4,     # ceiling: no doc can multiply >1.4x
)
results = boosted.search("RAG", top_k=5)
```

PageRank вычисляется lazy при первом `search()`; кешируется в инстансе.
Для готового lookup-словаря:

```python
from docstoolkit.citations import build_pr_lookup
pr_scores = build_pr_lookup(Path("docs"))  # {doc_id: score}
```

## Sprint 56 / M5 — Continuous Online Eval

Sampler + SQLite store + drift detection + HTML dashboard:

```python
from docstoolkit.online_eval import (
    OnlineEvalSampler, OnlineEvalStore, OnlineEvalRunner,
    render_dashboard,
)
from docstoolkit.rag import ask

store   = OnlineEvalStore()
runner  = OnlineEvalRunner(
    store=store,
    golden_dataset_path=Path("docs/eval/golden.yaml"),
    sampler=OnlineEvalSampler(sample_rate=0.05),
)

# Production query — 5% сэмплируется и сравнивается с golden dataset
result = ask("вопрос", eval_runner=runner)

# Weekly drift check
for d in runner.compute_drift(window_days=7):
    if d.significant:
        print(f"DRIFT {d.metric}: {d.delta:+.3f}")

# HTML dashboard
Path("dashboard.html").write_text(render_dashboard(store), encoding="utf-8")
```

`eval_runner` — best-effort: исключения не валят пользовательский запрос.

## Sprint 59 / M2 — Cross-Encoder Reranking

Pipeline по умолчанию забирает `top_k * 3` кандидатов из retriever, режет
до `top_k` после реранкинга:

```python
from docstoolkit.rag import ask
from docstoolkit.rerank.reranker import get_reranker

# stdlib-only — TF-IDF cosine reranker
result = ask("query", reranker=get_reranker("tfidf"))

# BGE cross-encoder (опционально, fallback на TF-IDF если зависимостей нет)
result = ask("query", reranker=get_reranker("bge"))

# LLM-judge реранкинг
result = ask("query", reranker=get_reranker("llm", answerer_name="anthropic"))
```

| Реранкер | Зависимости | Качество | Скорость |
|----------|-------------|----------|----------|
| `noop`   | none        | baseline | мгновенно |
| `tfidf`  | stdlib      | +5-10% P@5 | <1ms |
| `bge`    | sentence-transformers | +15-25% P@5 | 50-200ms/passage |
| `llm`    | anthropic API | best | seconds + cost |

## Sprint 60 / S7 — Read-Receipt Tracking

При `user_id` любой `ask()` автоматически добавляет извлечённые
`doc_id` в `profile.read_docs`. `PersonalizedRetriever` затем
штрафует уже прочитанные документы (-0.1 score), создавая
"recency loop" — пользователь видит новое чаще.

```python
result1 = ask("query", user_id="alice")
# Alice прочитала doc1, doc2, doc3

result2 = ask("query", user_id="alice")
# Те же документы теперь со штрафом -0.1; новые поднимаются выше
```

Логирование чтения — best-effort, не блокирует ответ при сбое БД.

## Композиция всех фич

Все 5 sprint-фич сочетаются ортогонально:

```python
result = ask(
    "Что такое RAG?",
    user_id="alice",                     # S6 + S7
    reranker=get_reranker("bge"),        # M2
    eval_runner=runner,                  # M5
)
# 1. apply_profile → method="bm25" (Alice's preference)
# 2. PersonalizedRetriever → section boost + read penalty
# 3. retrieve top_k*3 candidates
# 4. BGE reranker → top_k
# 5. answer
# 6. sample for online eval
# 7. mark all retrieved docs as read for Alice
```

PageRank-boost применяется когда вы оборачиваете базовый Retriever:

```python
from docstoolkit.citations import PageRankBoostedRetriever
# (потребует custom pipeline; будет интегрировано в ask() в Sprint 61)
```

## Что дальше — Путь B / C

См. [`docs/ROADMAP/02-MEDIUM.md`](../docs/ROADMAP/02-MEDIUM.md),
[`03-INNOVATIVE.md`](../docs/ROADMAP/03-INNOVATIVE.md),
[`04-NOVEL.md`](../docs/ROADMAP/04-NOVEL.md).

Ближайшие задачи Пути B:
- **I3** Provenance + confidence intervals (5 спринтов)
- **M1** Knowledge graph multi-hop (4 спринта)
- **I1** Self-RAG с reflection (5 спринтов)

---

## Sprint 55 / S2 — Faceted aggregation + filters

```python
from docstoolkit.rag import ask

# Aggregate per-field counts over retrieved passages
result = ask("RAG", with_facets=True,
             facet_fields=("section", "tag", "year"))
for agg in result.facets:
    print(agg.field_name, agg.values[:5])

# Pre-filter results to a single section before answering
result = ask("RAG", filters={"section": "05-habr-projects"})

# Combined: filter + facets over the filtered set
result = ask("RAG",
             filters={"section": "docs", "tag": ["memory", "agents"]},
             with_facets=True)
```

Built-in extractors: `section`, `tag`, `year`, `depth`. Custom extractors:
```python
from docstoolkit.rag.facets import aggregate_facets

aggs = aggregate_facets(
    passages,
    fields=("letter",),
    extractors={"letter": lambda p: [p.doc_id[:1]]},
)
```

## Sprint 61 / I3 — Provenance + Confidence Intervals

```python
result = ask("Yodoca?", with_provenance=True)
if result.provenance is not None:
    print(result.provenance.to_markdown())
    # ## Claims
    # 1. Yodoca is a memory project. — confidence: 0.82 (CI: 0.71–0.91)
    #    | sources: docs/yodoca, docs/yodoca-arch
```

`ProvenancedAnswer.overall_confidence` — mean confidence over claims;
`high_confidence_claims(0.7)` filters.

## Sprint 66 / M1 — Knowledge Graph Retriever

```python
from docstoolkit.knowledge_graph import KGRetriever

kgr = KGRetriever(max_hops=2)
for doc_path in corpus:
    kgr.index_doc(doc_path, Path(doc_path).read_text(), title=...)

# Direct usage (custom pipeline)
passages = kgr.search("Yodoca and AgentFS", top_k=5)
print(kgr.stats())  # {'docs': N, 'entities': M, 'relations': R}
```

Walk-pattern: extract query entities → expand neighbours up to
`max_hops` → score docs by `|doc.entities ∩ relevant| / |relevant|`.

## Sprint 67 / M3 — Hierarchical Retrieval

```python
# section → doc → passage routing, drop into ask() pipeline:
result = ask("How does Knowledge OS handle drift?", hierarchical=True)
# trace + per-level scoring is inside `hierarchical_search` internals;
# AnswerResult only carries the final passages
```

## Sprint 68 / M4 — Auto-Intent Routing

```python
# Lets IntentRouter pick retriever + top_k based on the question type:
ask("When was Anthropic founded?", auto_intent=True)
# FACTOID → keyword + top_k=3
ask("Compare BM25 vs TF-IDF", auto_intent=True)
# COMPARISON → hybrid + top_k=10
ask("Summarise the Knowledge OS architecture", auto_intent=True)
# SYNTHESIS → hybrid + top_k=20 + hierarchical=True
```

Explicit `method`/`top_k` always wins over auto-routing.

## Sprint 70 / I1 — Self-RAG Loop

```python
result = ask(
    "What's special about Yodoca?",
    self_rag=True,
    self_rag_max_iters=3,
    self_rag_threshold=7.0,   # reflect score 0-10
)
# Internally loops: retrieve → answer → reflect → maybe re-query
# Returns the iteration with highest confidence
```

## Sprint 75 / N3 — Graph-of-Thoughts

```python
result = ask("Python and Docker?", with_got=True, got_max_hypotheses=5)
# result.got_result.graph    — ThoughtGraph (DAG)
# result.got_result.final_answer — synthesised text
# result.got_result.confirmed_count / refuted_count
```

## Sprint 80 / N1 — Document Metabolism Proposals

Structured "this doc is stale, here are absorbable fragments" report,
ready for human-in-the-loop review:

```python
from docstoolkit.metabolism import propose_rewrite, rank_stale_documents

# Pick stale candidates from a corpus
candidates = rank_stale_documents(
    [(doc_id, content, last_modified_iso) for doc_id in corpus],
    threshold_days=180.0,
)

# For each, draft a rewrite proposal from fresh sources
for doc_id, age in candidates[:5]:
    proposal = propose_rewrite(
        doc_id, target_content,
        sources=[(s_id, s_text) for s_id, s_text in fresh_pool],
        last_modified_iso=last_mod_iso,
    )
    if proposal.has_changes:
        print(proposal.to_markdown())
        # Send to review queue, or apply proposal.suggested_content
```

## Полная композиция (10 фич сразу)

```python
result = ask(
    "Что такое Knowledge OS и какие у него ограничения?",
    user_id="alice",                  # S6 + S7  (auto profile + read-receipt)
    reranker=get_reranker("bge"),     # M2       (cross-encoder rerank)
    eval_runner=runner,               # M5       (sample for online eval)
    filters={"section": "docs"},      # S2 filter
    with_facets=True,                 # S2 aggregation
    with_provenance=True,             # I3       (span-level + 95% CI)
    self_rag=True,                    # I1       (reflect loop)
    with_got=True,                    # N3       (graph-of-thoughts)
    auto_intent=True,                 # M4       (route by question type)
    hierarchical=True,                # M3       (section→doc→passage)
)

# All 10 features stack orthogonally:
result.retrieved_passages   # final ranked passages
result.facets                # aggregations
result.provenance            # ProvenancedAnswer with claims
result.got_result            # ReasoningResult with thought DAG
```

