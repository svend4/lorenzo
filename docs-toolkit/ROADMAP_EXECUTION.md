# Roadmap Execution Plan — все спринты от простого к сложному

Этот документ — пошаговая «карта движения» по всем 35 пунктам roadmap
(`docs/ROADMAP/`), переведённым в конкретные технические спринты с указанием
файлов, модулей, API, тестов и точек интеграции. Порядок: от Пути A (квик-вин)
через Путь B (дифференциация) до Пути C (research bets).

**Convention каждого пункта:**
1. Спринт-номер · идентификатор · название
2. Этапы (по 1 спринту каждый, ~3-5 рабочих дней)
3. Файлы и API
4. Тесты — какие классы кейсов
5. Точка интеграции (где встраивается в `rag.ask`)
6. Метрики готовности

---

## ✅ Уже сделано в коммите `a25bbae9` (Sprint 54-60)

| Sprint | ID | Что | Файлы |
|---|---|---|---|
| 54 | S6 | Per-user preferences | `conversation/profile.py`, `rag/pipeline.py` |
| 56 | S4 | PageRank boost | `citations/boost.py` |
| 56 | M5 | Online eval dashboard | `online_eval/dashboard.py` |
| 59 | M2 | Cross-encoder reranking | `rerank/reranker.py` + pipeline hook |
| 60 | S7 | Read-receipt tracking | `rag/pipeline.py` (ask() integration) |

---

# Путь A — оставшиеся спринты

## Sprint 55 · S2 · Faceted search UI (backend)

**Этап 1/3 — Aggregation backend (1 спринт)**
- Файлы: `docstoolkit/rag/facets.py` — новый
- API:
  ```python
  @dataclass
  class FacetAggregation:
      field: str
      values: list[tuple[str, int]]    # (value, count)

  def aggregate_facets(passages: list[Passage],
                       fields: list[str] = ("section", "tag", "year")
                       ) -> list[FacetAggregation]: ...
  ```
- Извлекает поля из `doc_id` (первая директория = section), frontmatter
  (через `docstoolkit.frontmatter`), metadata.
- Интеграция: `rag.ask(with_facets=True)` → новое поле `AnswerResult.facets`
- Тесты: 15 кейсов (пустой корпус, multi-section, hierarchy, missing fields)

**Этап 2/3 — Filter application (1 спринт)**
- API:
  ```python
  ask("query", filters={"section": "05-habr-projects", "tag": "memory"})
  ```
- Реализация: пре-фильтрация после retrieve, до rerank.
- Тесты: AND/OR semantics, missing-key tolerance.

**Этап 3/3 — REST endpoint в `serve.py` (1 спринт)**
- `GET /api/facets?q=...&filter=section:05-habr-projects`
- JSON response: `{passages: [...], facets: [...]}`
- Тесты: integration через TestClient.

**Точка интеграции:** `rag/pipeline.py` после retrieve, до rerank.
**DoD:** все 3 этапа покрыты тестами, документация в `FACETS.md`.

---

## Sprint 58 · M2 · BGE reranker production hardening

Базовый `BGEReranker` уже есть с fallback. Что нужно:

**Этап 1 — Batch inference (1 спринт)**
- Текущий код вызывает `model.predict(pairs)` сразу для всего batch (✓ ok),
  но `transformers` ветка обрабатывает по одному. Добавить tensor-batching
  с `torch.cuda.amp.autocast()` если доступно.
- Файл: `rerank/reranker.py:177-215`.

**Этап 2 — Cache scores (1 спринт)**
- Поскольку `(query, passage_text)` детерминированно → SQLite cache.
- `rerank/cache.py` — schema `(query_hash, passage_hash, score, ts)`.
- TTL 7 дней; eviction LRU при >100K записях.

**Этап 3 — Docker image bundle (1 спринт)**
- `docs-toolkit/Dockerfile.bge` — pre-downloads `BAAI/bge-reranker-base`.
- CI build job; published artefact.

---

# Путь B — Differentiation (Sprint 61-79)

## Sprint 61-65 · I3 · Provenance + Confidence Intervals (5 спринтов)

**Концепция:** каждое утверждение в ответе RAG помечено source span'ом и 95% CI
доверительного интервала (bootstrap по retrieval scores).

### Этап 1/5 — Claim extractor
- Файл: `docstoolkit/provenance/claims.py`
- Делит ответ на atomic claims (regex-based + LLM fallback):
  ```python
  @dataclass
  class Claim:
      text: str
      span: tuple[int, int]      # offset в answer
      doc_refs: list[str] = []   # populated next stage
      ci_low: float = 0.0
      ci_high: float = 0.0
  ```
- Тесты: разделение по punctuation, citations preservation.

### Этап 2/5 — Source linking
- `provenance/link.py`:
  - Для каждого claim: TF-IDF overlap с каждым passage
  - Top-1 passage становится источником
  - Если overlap < 0.15 → claim помечается `unsupported`
- Тесты: known-source recall, unsupported detection.

### Этап 3/5 — Bootstrap CI
- `provenance/ci.py`:
  ```python
  def bootstrap_confidence(
      claim: Claim,
      passages: list[Passage],
      n_resamples: int = 1000,
  ) -> tuple[float, float]
  ```
- Resample passage scores, refit overlap → distribution → 2.5% / 97.5% percentiles.

### Этап 4/5 — Renderer
- `provenance/render.py`:
  - Markdown rendering: `[¹](doc-id#span) {{claim}} (95% CI: 0.62-0.84)`
  - HTML rendering для serve.py
  - JSON для API consumers.

### Этап 5/5 — Integration в rag.ask
- `ask(with_provenance=True)` → AnswerResult.claims + AnswerResult.unsupported_count
- Тесты: end-to-end, performance budget <1s on 5 claims.

**Метрика:** 100% claims имеют source span; provenance latency <200ms на claim.

---

## Sprint 66-69 · M1 · Knowledge Graph (4 спринта)

### Этап 1 — Triplet extraction
- `docstoolkit/kg/extractor.py`:
  - Rule-based: POS-pattern `(NOUN, VERB, NOUN)` через простой токенизатор
  - LLM-based fallback: prompt asks for triplets
  - Schema: `Triplet(subject, predicate, object, source_doc, span, confidence)`

### Этап 2 — SQLite storage
- `kg/store.py`:
  ```sql
  CREATE TABLE nodes (id TEXT PRIMARY KEY, label TEXT);
  CREATE TABLE edges (src TEXT, pred TEXT, dst TEXT, source_doc TEXT,
                      span_start INT, span_end INT, confidence REAL,
                      created_ts TEXT,
                      PRIMARY KEY (src, pred, dst, source_doc));
  CREATE INDEX idx_edges_src ON edges(src);
  CREATE INDEX idx_edges_dst ON edges(dst);
  CREATE INDEX idx_edges_pred ON edges(pred);
  ```
- API: `KnowledgeGraph.add()`, `.neighbors()`, `.shortest_path()`.

### Этап 3 — Query language
- `kg/query.py`:
  - Cypher-lite: `MATCH (a)-[:uses]->(b)-[:author]->(c) WHERE a.label="Yodoca"`
  - Parser → AST → SQL generator
  - Multi-hop traversal с capped depth.

### Этап 4 — Retriever integration
- `kg/retriever.py`:
  - `KGRetriever` — берёт passages из source_doc'ов на graph-paths
  - Hybrid с BM25 через RRF
  - Hook в `rag.ask(method="kg")` или `method="hybrid+kg"`.

**Метрика:** triplet precision ≥70% на 100 human-labelled; multi-hop <500ms.

---

## Sprint 70-74 · I1 · Self-RAG с reflection (5 спринтов)

### Этап 1 — Decision tokens
- `docstoolkit/self_rag/tokens.py`:
  - Special markers: `[NEED_RETRIEVAL]`, `[NO_RETRIEVAL]`, `[CONFIDENT]`,
    `[NEEDS_CHECK]`
  - Trainer-free: prompt engineering для генерации этих маркеров.

### Этап 2 — Reflect step
- `self_rag/reflect.py`:
  - После ответа: prompt «оцени confidence per claim»
  - Если есть `[NEEDS_CHECK]` → re-query с другим method

### Этап 3 — Loop controller
- `self_rag/loop.py`:
  ```python
  def self_rag_ask(question, *, max_iters=3, confidence_threshold=0.65)
  ```
  - while not confident & iter < max: retrieve → answer → reflect → maybe re-retrieve.

### Этап 4 — Calibration
- `self_rag/calibrator.py`:
  - Logistic regression: features (retrieval-score-stats, overlap) → P(correct)
  - Train offline on golden dataset.

### Этап 5 — A/B test framework
- Использовать existing `docstoolkit.experiments`
- Eval: -30% hallucination rate vs baseline.

**Метрика:** halucination rate -30% (по golden answers с adversarial prompts).

---

## Sprint 75 (optional) · N3 · Graph-of-thoughts (8 спринтов)

Большой research-проект — оставлен на Путь C ниже.

---

# Путь C — Long-game (8-12 месяцев)

## Опция C1: N1 — Document «metabolism» (8-12 спринтов)

**Концепция:** документы сами эволюционируют — стареющие переписываются на основе
свежих, накапливающих знаний. Корпус — как биосистема.

### Foundation (Sprint 80-82)
- `docstoolkit/metabolism/` модуль
- `decay_curve(doc, age_days)` — exponential decay коэффициент
- `freshness_score = recency × access_frequency × citation_count`

### Core loop (Sprint 83-86)
- `rewrite_proposal(stale_doc, fresh_docs)` — LLM генерирует обновлённую версию
- `review_queue` integration (используя existing `review_queue.py`)
- Human-in-the-loop approval gate

### Quality + integration (Sprint 87-91)
- Provenance trail: каждая правка имеет from/to-revisions + sources
- A/B на качество: rewritten vs original
- Production hardening: rate limits на rewrites, cost budget

### External validation (Sprint 92-94)
- Demo на conference; paper draft
- Open-source release с CC-BY-SA documentation set

**Метрика:** rewritten docs имеют higher relevance score AND user satisfaction
∧ цитируются больше original.

---

## Опция C2: N3 — Graph-of-thoughts (8-10 спринтов)

### Sprint 95-96 — Thought primitives
- `docstoolkit/got/` модуль
- `Thought(id, content, parent_id, score, sources)`
- `ThoughtGraph` — DAG operations.

### Sprint 97-99 — Construction
- LLM driver: «expand this thought into 3 sub-thoughts»
- Pruning: low-score thoughts удаляются
- Aggregation: votes / RRF на leaf thoughts.

### Sprint 100-102 — Integration с RAG
- `got_ask(question)` → tree of thoughts с retrieval на каждом node
- Visualization: D3.js renderer в `serve.py`.

### Sprint 103-104 — Evaluation
- Compare to flat RAG on complex multi-hop questions
- Cost vs quality curve.

**Метрика:** +25% accuracy на multi-hop benchmarks; latency budget 10s.

---

## Опция C3: N5 — Federated golden datasets (10+ спринтов)

**Концепция:** несколько организаций имеют свои golden datasets, не хотят
делиться, но хотят shared eval. Используется differential privacy + secure
aggregation.

### Sprint 105-108 — DP foundations
- `docstoolkit/federated_eval/` модуль (✓ stub существует)
- Laplace noise injection в aggregated metrics
- Privacy budget tracking.

### Sprint 109-112 — Secure aggregation
- HE-based summation (через `pyfhel` или собственная light-HE)
- Threshold cryptography для multi-party.

### Sprint 113-116 — Integration
- Hook в existing `experiments` framework
- Cross-org A/B без раскрытия данных.

**Метрика:** patentable concept; first publication submitted.

---

# Полный план Hybrid — 36-48 спринтов

| Месяц | Sprints | Фокус | Что готово |
|---|---|---|---|
| 1 | 54-58 | Путь A foundation | S6, S2, S4 ✓ (S6/S4 done) |
| 2 | 59-62 | Путь A quality | M2, A/B testing ✓ (M2 done) |
| 3 | 63-66 | Путь A production | M5, S7 ✓ (S7 done) |
| 4 | 67-71 | I3 provenance | claims, CI, render, integration |
| 5 | 72-75 | M1 knowledge graph | extraction, storage, query, retriever |
| 6 | 76-80 | I1 self-RAG | tokens, reflect, loop, calibration, A/B |
| 7-9 | 81-95 | C1 или C2 (выбор) | metabolism или GoT |
| 10-12 | 96-114 | iteration + external | paper, OSS release, polish |

---

# Sprint-execution checklist (для каждого спринта)

1. **Read** existing module (если есть) — обычно есть `doc_*` модуль с похожей семантикой
2. **Plan** API surface: dataclasses + 3-5 public functions
3. **Write tests first** (BDD-style, ~15-30 кейсов на спринт)
4. **Implement** до зелёного теста
5. **Integrate** в `rag/pipeline.py` через новый kwarg в `ask()`
6. **Document** в `PROFILES.md` (или отдельный `XXX.md`)
7. **Commit** с conventional message
8. **Push** на feature branch + open PR
9. **Monitor** CI (subscribe_pr_activity); fix regressions
10. **Merge** после green

---

# Связанные документы

- [docs/ROADMAP/00-CURRENT-STATE.md](../docs/ROADMAP/00-CURRENT-STATE.md) — что есть
- [docs/ROADMAP/01-SIMPLE.md](../docs/ROADMAP/01-SIMPLE.md) — Path A items
- [docs/ROADMAP/02-MEDIUM.md](../docs/ROADMAP/02-MEDIUM.md) — Path B items (M1-M8)
- [docs/ROADMAP/03-INNOVATIVE.md](../docs/ROADMAP/03-INNOVATIVE.md) — I1-I10
- [docs/ROADMAP/04-NOVEL.md](../docs/ROADMAP/04-NOVEL.md) — N1-N10
- [docs/ROADMAP/05-PRIORITIES.md](../docs/ROADMAP/05-PRIORITIES.md) — strategy
- [PROFILES.md](PROFILES.md) — текущее состояние реализованных фич
