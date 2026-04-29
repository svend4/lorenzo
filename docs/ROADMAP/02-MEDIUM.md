# 02 — Средние улучшения (мейнстрим современного RAG)

Современный mainstream — реализуется коммерческими RAG-фреймворками (LangChain, LlamaIndex, Haystack), но в Lorenzo пока отсутствует. Каждое — 2-5 спринтов, средний риск, существенный прирост качества.

**Документ:** часть серии ROADMAP. См. также: [00-CURRENT-STATE](./00-CURRENT-STATE.md), [01-SIMPLE](./01-SIMPLE.md), [03-INNOVATIVE](./03-INNOVATIVE.md), [04-NOVEL](./04-NOVEL.md), [05-PRIORITIES](./05-PRIORITIES.md).

---

## M1. Knowledge Graph extraction + reasoning

### Концепция
Из корпуса извлекаются триплеты `(subject, relation, object, source_doc, confidence)`. Граф хранится отдельно. Запросы поддерживают graph traversal (multi-hop): «какие проекты используют технологии, упоминаемые в вакансиях Anthropic».

### Зачем
- Multi-hop рассуждение по связям сущностей
- Factoid queries с источниками
- Visualization связей для exploration

### Существующие primitives
- `improve_named_entity_index.py` — NER без ML (regex-based)
- `improve_concept_graph.py` — концепты + связи в графе
- SQLite — для persistent graph storage

### Этапы реализации (4 спринта)

**Спринт A:** Extraction
- `docstoolkit/kg/` модуль
- Triplet extractor: rule-based (POS-pattern matching) + opt LLM-based для нормализации
- Triplet schema: (subject_id, predicate, object_id, source_doc, span, confidence)
- SQLite schema: nodes / edges / sources таблицы

**Спринт B:** Storage
- Indexed lookup: по subject, по predicate, по source
- Deduplication: same (subject, predicate, object) с разных sources → объединить с накоплением sources
- Versioning: edge может быть deprecated если source документ удалён

**Спринт C:** Querying
- `query_graph(start, max_hops=2, predicates=[...])` → паттерн matching
- Cypher-lite syntax: `MATCH (a)-[:uses]->(b)-[:author]->(c)`
- Hybrid query: «семантически близко к 'memory' + связано с 'AgentFS' через `uses`»

**Спринт D:** Integration
- Retriever plugin `kg_retriever` — берёт top-k passages где упоминается граф-путь
- Hybrid с BM25/semantic через RRF
- UI: visualisation как `improve_concept_graph.py` но интерактивно

### API sketch

```python
@dataclass
class Triplet:
    subject: str
    predicate: str
    object: str
    source_doc: str
    span: tuple[int, int]
    confidence: float

class KnowledgeGraph:
    def add(self, t: Triplet) -> None
    def query(self, pattern: str, max_hops: int = 2) -> list[Path]
    def neighbors(self, node: str, predicate: str = "") -> list[str]
    def shortest_path(self, src: str, dst: str) -> list[str] | None

class KGRetriever(Retriever):
    """Retriever plugin: возвращает passages связанные с relevant graph paths."""
```

### Метрики успеха
- Triplet extraction precision: ≥70% (human labelled subset)
- Multi-hop query response time: <500ms на 10K триплетов
- Adding KG-retriever повышает eval score на ≥10% для «factoid» класса вопросов

### Риски
- Rule-based extraction шумный. Митигация: confidence threshold, опц. LLM verification
- Граф устаревает при изменениях корпуса. Решение: хук `on_doc_change` → пересборка триплетов из этого документа

---

## M2. Cross-encoder re-ranking

### Концепция
После первичного retrieval (top-50 от BM25/semantic) прогнать через лёгкую cross-encoder модель (BGE-reranker-base, 67M params) → re-score → топ-5/10. Cross-encoder видит query+doc вместе и даёт точечную релевантность.

### Зачем
- Существенный прирост precision (+15-25% по литературе)
- Snake-oil-resistance: оценка не от sparse/dense, а от cross-attention
- Быстрая модель (~50ms на CPU для 50 docs)

### Существующие primitives
- `rag/retriever.py` — выходит ranked passages
- `embeddings/` — pluggable backend
- Optional anthropic/openai как proxy если нет local model

### Этапы реализации (3 спринта)

**Спринт A:** Reranker abstraction
- `docstoolkit/rerank/` модуль
- `Reranker` ABC: `score(query, passages) → list[float]`
- `BGEReranker`: optional dependency на `sentence-transformers` или `transformers`
- `LLMReranker`: использует LLM для скоринга через prompt

**Спринт B:** Pipeline integration
- `Retriever.search(query, top_k=5, rerank_top_k=50)` — берёт 50, реранкит, возвращает 5
- A/B test: with/without reranking на golden eval
- Кеширование cross-encoder весов (download once)

**Спринт C:** Production
- Fallback при отсутствии модели → no-op reranker
- Telemetry: rerank duration, score distribution
- CLI: `lorenzo eval --rerank bge-base` vs `--rerank none`

### API sketch

```python
class Reranker(Protocol):
    def score(self, query: str, passages: list[Passage]) -> list[float]

class BGEReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-base"): ...
    def score(self, query, passages) -> list[float]: ...

class LLMReranker:
    def __init__(self, answerer: str = "anthropic", batch_size: int = 5): ...
    def score(self, query, passages) -> list[float]: ...
```

### Метрики успеха
- Precision@5 на golden set: +15% против baseline (BM25)
- Latency overhead: <200ms p50
- Coverage: работает с любым retriever

### Риски
- Model download (~250MB BGE-base). Митигация: lazy load, cache в `.docstoolkit/models/`
- Privacy если LLMReranker uses cloud. Решение: explicit opt-in, логировать только метрики

---

## M3. Hierarchical retrieval

### Концепция
Вместо плоского поиска по passages — иерархия: corpus → section → doc → passage. На каждом уровне retrieval отбирает top-k, fan-out внутрь. Финальный merge по cumulative score.

### Зачем
- Лучше работает на корпусе с >1000 документов
- Естественная декомпозиция «о чём вообще» → «в каком документе» → «какой пассаж»
- Можно остановиться на любом уровне (для UI: показать секцию или весь док)

### Существующие primitives
- Уже есть структура `docs/01-svyazi/`, `02-anthropic-vacancies/` etc.
- `improve_outline.py` — иерархическое оглавление
- `improve_chunk_semantic.py` — passage-level chunks

### Этапы реализации (3 спринта)

**Спринт A:** Multi-level index
- Per-section index: TF-IDF центроид + summary
- Per-document index: title + abstract + headings
- Per-passage index: existing chunks
- SQLite таблицы: section_index / doc_index / passage_index

**Спринт B:** Hierarchical query
- `hierarchical_search(query, levels=["section", "doc", "passage"], top_k_per_level=[3, 5, 5])`
- На каждом уровне: search → top_k → fan_out → next level
- Aggregate score: weighted product (section_score × doc_score × passage_score)

**Спринт C:** Adaptive levels
- Если query очень specific («что говорит Yodoca про X») → начать с doc-level
- Если broad («что у нас по memory») → начать с section-level
- Heuristic: query length / specificity entropy

### API sketch

```python
@dataclass
class HierarchicalResult:
    sections: list[tuple[str, float]]
    docs: list[tuple[str, float]]
    passages: list[Passage]
    trace: list[str]                 # «section/X selected; in X: doc/Y; in Y: passage Z»

def hierarchical_search(
    query: str, *,
    levels: list[str] = ["section", "doc", "passage"],
    top_k_per_level: list[int] = [3, 5, 5],
    aggregation: str = "product",     # product | sum | rrf
) -> HierarchicalResult
```

### Метрики успеха
- Latency на 5K-документном корпусе: <300ms (vs flat: 2-3 сек)
- Recall@5 на «section-level» queries: +20% против flat
- Trace интерпретируем человеком (можно объяснить «почему»)

### Риски
- Cold start: section index пустой для маленьких разделов. Решение: fallback на flat retrieval если section <5 docs
- Inconsistent ranking между уровнями. Митигация: re-normalize scores per level

---

## M4. Query intent classification

### Концепция
Перед retrieval классифицировать query по типам: factoid / explanation / comparison / synthesis / opinion / instruction. Каждый тип → разный pipeline (e.g. comparison → fan-out per entity, synthesis → map-reduce).

### Зачем
- Лучшие результаты благодаря specialized pipelines
- Foundation для умного routing (M5: answerer choice)
- Метрики per-type → знаем где система слаба

### Существующие primitives
- `improve_question_extractor.py` — выделение вопросов из corpus
- `prompts/` (Sprint 51) — versioned prompts → разные per intent
- `router/` (Sprint 46) — failover chain

### Этапы реализации (3 спринта)

**Спринт A:** Classifier
- `docstoolkit/intent/` модуль
- Heuristic classifier (rule-based): pattern matching `что такое X` → factoid, `сравни X и Y` → comparison
- Optional ML classifier (fine-tuned small model) — позже
- 6 intent classes + `unknown` fallback

**Спринт B:** Pipeline routing
- `IntentRouter`: intent → preferred (retriever, top_k, prompt_id, post-processing)
- Default mappings configurable
- Logging: actual_intent vs detected_intent для eval

**Спринт C:** Specialized pipelines
- Comparison: extract entities → fan-out retrieval per entity → merge → LLM compares
- Synthesis: hierarchical retrieval (M3) → map-reduce summarization
- Instruction: agent loop (existing) с tool selection
- Factoid: direct top-1 passage extraction

### API sketch

```python
@dataclass
class Intent:
    label: str                       # factoid | explanation | comparison | synthesis | opinion | instruction
    confidence: float
    extracted: dict                  # e.g. comparison: {entities: [X, Y]}

class IntentClassifier:
    def classify(self, query: str) -> Intent

class IntentRouter:
    def configure(self, label: str, *, retriever: str, prompt_id: str, ...): ...
    def route(self, query: str) -> dict   # config для pipeline
```

### Метрики успеха
- Heuristic classifier accuracy: ≥75% на manual labelled queries (50)
- Per-intent eval score improvement: ≥15% для comparison, ≥10% для synthesis
- Logging позволяет manually fix mis-routed queries

### Риски
- Multilingual heuristic — RU pattern matching не покрывает всё. Решение: language-aware patterns
- Wrong routing хуже чем default. Решение: confidence threshold + fallback на universal pipeline

---

## M5. Continuous online evaluation

### Концепция
Каждый N-й (e.g. 1 из 100) production query прогоняется как eval против golden — но автоматически, в фоне. Результаты накапливаются, дрейф детектируется (precision дропнул с 80% до 65% за неделю → alert).

### Зачем
- Production confidence: знаем что система не деградировала
- Drift detection: модель/корпус/distribution меняются
- Continuous improvement loop: данные для дообучения

### Существующие primitives
- `eval/` (Sprint 48) — golden datasets
- `experiments/` — run framework
- `feedback/` — user thumbs данные
- `telemetry/` — метрики exposition

### Этапы реализации (3 спринта)

**Спринт A:** Sampling + storage
- `docstoolkit/online_eval/` модуль
- `OnlineEvalSampler`: случайно выбирает 1/N запросов
- Sample lifecycle: query → run with prod config → run with golden as comparison → store result
- SQLite таблица: online_eval_runs

**Спринт B:** Drift detection
- `compute_drift(window_days=7) → DriftReport`: comparison против baseline week
- Wilson confidence interval для precision/recall difference
- Statistical test: chi-squared / mann-whitney
- Alert via webhooks (Sprint 52) при significant drift

**Спринт C:** Dashboard
- HTML page `/eval/dashboard`: time-series charts, per-class breakdown
- Metrics: P@5, R@5, F1, citation_precision, answer_score
- Drill-down: failed queries inspection

### API sketch

```python
class OnlineEvalSampler:
    def __init__(self, sample_rate: float = 0.01): ...
    def maybe_sample(self, query: str) -> bool

class OnlineEvalRunner:
    def run_sample(self, query: str, prod_result: AnswerResult) -> OnlineEvalRun

@dataclass
class DriftReport:
    metric: str
    baseline_value: float
    current_value: float
    delta: float
    p_value: float
    significant: bool
```

### Метрики успеха
- Sample storage: <1MB/day на 1K queries/day
- Drift detection latency: alert within 24h of significant change
- Dashboard load time: <2 сек

### Риски
- Sampling bias (только simple queries попадают в выборку). Решение: stratified sampling по intent
- Cost (eval runs стоят). Решение: budget cap per day

---

## M6. Active learning queue

### Концепция
Низко-confidence retrieval results / negative feedback / known unknowns → попадают в queue для human review. Человек размечает → запись в golden dataset → автоматическое улучшение.

### Зачем
- Очерёдность для labelling: focus на самые impactful queries
- Loop: production → uncertain → human → golden → re-train/re-tune → better production
- Foundation для self-improvement

### Существующие primitives
- `feedback/` — thumbs collection
- `eval/` — golden datasets
- `online_eval` (M5) — uncertain queries
- `webhooks/` — notification

### Этапы реализации (3 спринта)

**Спринт A:** Queue
- `docstoolkit/active_learning/` модуль
- `LearningQueue` (SQLite): queued items с priority, status, owner
- Triggers: low confidence (e.g. <0.4 from adaptive retrieval), down-thumb, mismatch с golden in online eval
- Web UI / CLI для labelling

**Спринт B:** Labelling tool
- `serve.py` route `/label` с UI
- Items show query + retrieved passages + suggested answer
- Form: «выберите правильные docs», «опишите expected answer», «forbidden phrases?»
- Submit → запись в `golden/{auto_added}.yaml`

**Спринт C:** Loop closure
- Auto-rerun eval после каждого новой золотой entry
- Trigger A/B test: variant с обновлённым golden vs baseline
- Track: «labelled item → eval improvement» causality

### API sketch

```python
@dataclass
class LearningItem:
    id: str
    query: str
    passages: list[Passage]
    suggested_answer: str
    priority: float
    reason: str                      # low_confidence | down_thumb | golden_mismatch
    status: str = "pending"          # pending | labelled | skipped
    labelled_by: str = ""

class LearningQueue:
    def enqueue(self, item: LearningItem) -> str
    def next(self, owner: str) -> LearningItem | None
    def submit_label(self, item_id: str, golden: GoldenItem) -> None
```

### Метрики успеха
- Queue item resolution time: median <24h
- Per-week growth of golden dataset: ≥10 items
- Eval score improvement after each labelling batch: ≥0.5%

### Риски
- Labeller fatigue. Решение: priority queue, daily quota
- Inconsistent labelling между разными labellers. Решение: review queue, inter-rater agreement metric

---

## M7. Incremental indexing

### Концепция
Watcher (`improve_watch.py`) детектирует изменения файла → инкрементально обновляет только этот документ во всех индексах (BM25, semantic, NER, concept graph), без полной переиндексации.

### Зачем
- Near-real-time freshness
- Масштабируемость на 10K+ docs (full rebuild занимает минуты)
- Снижение compute cost

### Существующие primitives
- `improve_watch.py` — polling watcher (есть)
- `improve_passage_retrieval.py --index` — full rebuild (есть)
- SQLite — atomic updates

### Этапы реализации (3 спринта)

**Спринт A:** Index abstractions
- `Index` ABC: `add(doc)`, `remove(doc_id)`, `update(doc)`, `query(...)`
- Refactor BM25/keyword/semantic indexes под этот interface
- Persistent storage в SQLite (вместо JSON где возможно)

**Спринт B:** Incremental updates
- Watcher hook: `on_change(path) → update_indexes(path)`
- Per-index merge: BM25 — delta in inverted lists; semantic — replace embedding row
- Atomic transactions: все индексы updated together или rollback

**Спринт C:** Verification
- `lorenzo verify-index` — проверяет консистентность с диском
- Self-healing: detect drift → trigger full rebuild для драфтового slice
- Метрики: indexes_updated_total, full_rebuilds_total

### API sketch

```python
class Index(Protocol):
    def add(self, doc_id: str, content: str) -> None
    def remove(self, doc_id: str) -> None
    def update(self, doc_id: str, content: str) -> None
    def query(self, q: str, top_k: int) -> list[Hit]

class IndexCoordinator:
    """Атомарно обновляет все зарегистрированные indexes."""
    def register(self, name: str, index: Index) -> None
    def on_doc_change(self, path: Path) -> None
    def verify(self) -> dict[str, list[str]]   # {index_name: [missing_doc_ids]}
```

### Метрики успеха
- Update single doc: <500ms across all indexes
- Index drift after 1 week: 0 missing/extra entries
- Full rebuild not needed более 30 дней без degradation

### Риски
- Race conditions при concurrent updates. Решение: per-doc lock
- Index corruption. Решение: WAL + verify-on-startup

---

## M8. Cross-modal CLIP-style embeddings

### Концепция
Image+text в shared embedding space (например, CLIP). Картинка из документа извлекается, embedded → может быть retrieved by text query, и наоборот.

### Зачем
- Visual search: «найди диаграммы где упоминается AgentFS»
- Foundation для multi-modal RAG
- Text↔image alignment в curation tasks

### Существующие primitives
- `multimodal/` (Sprint 38) — multi-modal ingest
- `embeddings/` — pluggable backend
- Image extraction из markdown (`<img>` tags, attachments)

### Этапы реализации (4 спринта)

**Спринт A:** Image pipeline
- Image extractor: scan markdown для image refs → resolve paths → load
- Thumbnail generation (для UI)
- SQLite: images таблица с metadata (path, source_doc, alt, caption, ts)

**Спринт B:** Embeddings
- `CLIPEmbedder`: optional dep `clip-by-openai` или `transformers` + ViT
- `embed_image(path) → vector`, `embed_text(text) → vector` — same dim
- Batch processing для existing corpus

**Спринт C:** Cross-modal retrieval
- `ImageRetriever`: query text → top-k images by cosine
- `TextByImageRetriever`: image → top-k captions/passages
- Hybrid: text query → text passages + relevant images concatenated

**Спринт D:** UI
- Search results show inline images
- Image-first browsing: gallery view per section
- Reverse search: drag image → find related docs

### API sketch

```python
class CrossModalEmbedder:
    def embed_text(self, text: str) -> np.ndarray
    def embed_image(self, path: Path) -> np.ndarray

class ImageStore:
    def add(self, path: Path, source_doc: str, caption: str = "") -> str
    def search_by_text(self, query: str, top_k: int = 10) -> list[ImageHit]
    def search_by_image(self, path: Path, top_k: int = 10) -> list[ImageHit]
```

### Метрики успеха
- Image embedding throughput: ≥5 imgs/sec на CPU
- Cross-modal recall@10: ≥40% на manual labelled set
- Storage: ≤2KB per image (embedding + metadata)

### Риски
- Heavy dependency (CLIP ~500MB). Митигация: optional, lazy load
- Privacy (images могут содержать чувствительное). Решение: opt-in per-section

---

## Сводная таблица

| ID | Название | Спринтов | Сложность | Влияние |
|----|----------|---------:|-----------|---------|
| M1 | Knowledge Graph | 4 | Medium-High | Very High (multi-hop) |
| M2 | Cross-encoder reranking | 3 | Medium | High (precision) |
| M3 | Hierarchical retrieval | 3 | Medium | High (scale) |
| M4 | Query intent classification | 3 | Medium | High (per-type quality) |
| M5 | Continuous online eval | 3 | Medium | Very High (drift detection) |
| M6 | Active learning queue | 3 | Medium | High (closes loop) |
| M7 | Incremental indexing | 3 | Medium | High (freshness + scale) |
| M8 | Cross-modal embeddings | 4 | Medium-High | Medium (niche but unique) |

**Общий бюджет:** ~26 спринтов на все 8. Реалистично выбрать 4-5 наиболее ценных.

---

## Рекомендуемая последовательность

1. **M2** (cross-encoder reranking) — biggest quality bang for buck, low risk
2. **M5** (continuous online eval) — нужна перед всеми изменениями, чтобы видеть эффект
3. **M7** (incremental indexing) — foundation для scale
4. **M1** (knowledge graph) — главное отличие от плоского RAG
5. **M4** (intent classification) — enables per-type pipelines
6. **M3** (hierarchical) — окупается на >1K docs
7. **M6** (active learning) — closes the loop, requires M5
8. **M8** (cross-modal) — niche, отложить если нет UI приоритета
