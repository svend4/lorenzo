# 03 — Инновационные направления (frontier research)

Современный research frontier (2024-2026): уже опубликованы paper'ы, есть прототипы, но мало production-grade реализаций. Каждое — 4-8 спринтов, требует исследовательского подхода.

**Документ:** часть серии ROADMAP. См. также: [00-CURRENT-STATE](./00-CURRENT-STATE.md), [01-SIMPLE](./01-SIMPLE.md), [02-MEDIUM](./02-MEDIUM.md), [04-NOVEL](./04-NOVEL.md), [05-PRIORITIES](./05-PRIORITIES.md).

---

## I1. Self-RAG с reflection

### Концепция
LLM сам решает на каждом шаге: (a) использовать parametric knowledge без retrieval, (b) сделать retrieval, (c) ответ. После генерации ответа — отдельный reflection step: «достаточно ли подтверждений? есть ли противоречия с источниками?». Если нет — retry с reformulated query.

Базируется на работе [Self-RAG: Learning to Retrieve, Generate, and Critique](https://arxiv.org/abs/2310.11511) (Asai et al., 2023).

### Зачем
- Меньше unnecessary retrieval (latency + cost) для общеизвестных факт
- Меньше hallucinations через reflection-driven re-retrieval
- Самокритика → confidence calibration

### Существующие primitives
- `agent/loop.py` — уже есть think→act→observe цикл, надо добавить retrieve-decision
- `adaptive/` (Sprint 53) — multi-hop с reformulation
- `prompts/` — versioned prompts (для critic prompts)
- `feedback/` — для training reflection scoring

### Этапы реализации (5 спринтов)

**Спринт A:** Decision tokens
- Special tokens в prompt: `[NEED_RETRIEVAL]`, `[NO_RETRIEVAL_NEEDED]`, `[REFLECT]`, `[ANSWER_OK]`, `[ANSWER_INSUFFICIENT]`
- Parser для decision tokens из LLM output
- Fallback: если LLM не выдаёт токены — defаult к retrieval

**Спринт B:** Reflect step
- После initial answer: prompt LLM с «critique your answer using these sources»
- Output structure: `{score: 0-10, missing: [topics], contradictions: [pairs], suggested_query: str}`
- Если score <7 → retrieve more → regenerate

**Спринт C:** Loop control
- Max iterations cap (e.g. 4)
- Stop conditions: high reflect score | exhausted | budget exceeded
- Tracing: каждый step логируется в SelfRAGTrace

**Спринт D:** Calibration
- Использовать feedback (Sprint 43) для калибровки reflect score → actual quality
- Если reflect_score 8 коррелирует с user thumbs_down → adjust threshold

**Спринт E:** A/B production
- Compare с baseline RAG: same questions, same corpus, разные answer methods
- Метрики: hallucination_rate (manual annotation), latency, cost, user_satisfaction

### API sketch

```python
@dataclass
class ReflectStep:
    iteration: int
    decision: str                    # retrieve | answer | reflect | stop
    query: str
    passages: list[Passage]
    answer: str
    reflect_score: float            # 0-10
    issues: list[str]               # missing topics, contradictions
    suggested_query: str = ""

@dataclass
class SelfRAGResult:
    final_answer: str
    steps: list[ReflectStep]
    total_retrievals: int
    total_iterations: int
    confidence: float                # final calibrated confidence

def self_rag_ask(question: str, *, max_iterations: int = 4,
                  reflect_threshold: float = 7.0,
                  retriever: Retriever | None = None,
                  answerer: str = "anthropic") -> SelfRAGResult
```

### Метрики успеха
- Hallucination rate: -30% против baseline
- Average retrievals per query: -25% (skipped когда не нужно)
- Latency p50: +20% (overhead reflect), но total cost -15% (fewer LLM calls)
- Calibration: reflect_score correlates с user_thumbs at ρ ≥ 0.6

### Риски
- LLM не следует decision token convention. Митигация: structured output (JSON mode), few-shot examples
- Reflect step может «застрять» (всегда low confidence). Решение: max_iter + fallback ответ с disclaimer
- Дороговизна reflect calls. Митигация: используется cheaper model (Haiku) для reflect, expensive для answer

---

## I2. Multi-agent debate

### Концепция
3 параллельных агента с разными perspectives (skeptic, synthesizer, devil's advocate) генерируют ответы независимо → debate round (cross-critique) → final synthesizer aggregates с weighted voting. Базируется на работе [Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325).

### Зачем
- Снижение systematic biases отдельной модели
- Лучше чем single-agent на reasoning tasks (+15-20% по литературе)
- Diverse perspectives → robust output

### Существующие primitives
- `agent/loop.py` — single agent runner
- `workflow/dag.py` — parallel execution через `run_async`
- `prompts/` — разные prompts per persona
- `experiments/` — для A/B сравнения с single-agent

### Этапы реализации (5 спринтов)

**Спринт A:** Persona system
- `Persona` dataclass: name, system_prompt, temperature, retrieval_bias
- 3 built-in: SkepticPersona, SynthesizerPersona, ContrarianPersona
- Каждая использует свой prompt template + (опц.) разный retriever

**Спринт B:** Parallel debate workflow
- `DebateWorkflow`: workflow DAG с 3 parallel agent_run + 1 debate step + 1 synthesis
- Уже есть workflow primitives — wire up
- Trace: each agent's intermediate answer + debate transcript

**Спринт C:** Debate round
- Каждый агент видит ответы других + critique prompt: «найдите ошибки/упущения у others»
- Output: refined version + critique notes
- Опционально: 2+ rounds debate

**Спринт D:** Synthesis с voting
- Aggregator agent: получает все final answers + voting (majority / weighted by reflect_score)
- Output: consensus answer + dissenting opinions section
- Confidence: based на agreement (high if all agree, low if split)

**Спринт E:** Cost-quality trade-off
- 3x agent cost vs single-agent quality gain
- Adaptive: simple queries → single agent, complex → multi-agent
- Budget guard integration (Sprint 45)

### API sketch

```python
@dataclass
class Persona:
    name: str
    system_prompt: str
    temperature: float = 0.7
    retriever_method: str = "hybrid"

@dataclass
class DebateRound:
    round: int
    agent_answers: dict[str, str]    # {persona_name: answer}
    critiques: dict[str, dict]       # {critic_name: {target_name: critique}}

@dataclass
class DebateResult:
    consensus: str
    dissenting: list[str]
    confidence: float                # 0-1, based на agreement
    rounds: list[DebateRound]
    total_cost: float

def multi_agent_debate(question: str, *,
                        personas: list[Persona] | None = None,
                        max_rounds: int = 2,
                        synthesizer: Persona | None = None) -> DebateResult
```

### Метрики успеха
- Reasoning accuracy на benchmark queries: +15% против single-agent
- Hallucination rate: -25% (один агент catches другого)
- Cost: ~3x single-agent (acceptable для high-stakes queries)
- Confidence calibration: high-confidence outputs точнее на 20%

### Риски
- Group-think (все агенты согласны но неправы). Митигация: contrarian persona обязательна
- Slow (3x latency). Решение: параллелизация (workflow.run_async)
- Сложно отлаживать. Решение: debate transcript полностью логируется

---

## I3. Provenance с confidence intervals

### Концепция
Каждое утверждение в ответе линкуется к конкретным source spans. Дополнительно: bootstrap confidence interval на «насколько надёжно это утверждение». Например: «Yodoca использует hot path activation [confidence: 92% (95% CI: 85-97%)] [sources: yodoca.md:line 23, memory-arch.md:line 45]».

### Зачем
- Source attribution на span-level (не doc-level)
- Quantified uncertainty per claim — пользователь знает чему доверять
- Foundation для counterfactual probing (I7)

### Существующие primitives
- `rag/assembler.py` — citations [n] уже есть на passage-level
- `feedback/` — Wilson confidence calculation (Sprint 43)
- `eval/` — citation P/R/F1 метрики

### Этапы реализации (5 спринтов)

**Спринт A:** Claim extraction
- После LLM-ответа: parser выделяет atomic claims
- Heuristic: split on sentences, filter for factual statements (subject-predicate-object)
- Optional: LLM-assisted claim extraction для complex prose

**Спринт B:** Source linking
- Для каждой claim: search в retrieved passages для матчей
- Match strategy: exact phrase, paraphrase (TF-IDF cosine), entity overlap
- Output: `claim_supports[claim_id] = [(passage_id, span, similarity)]`

**Спринт C:** Confidence intervals
- Bootstrap: сэмплируем passages случайно из retrieved set, переспрашиваем LLM
- Распределение «as confirmed» по сэмплам → CI
- Альтернатива: ensemble через multi-agent (I2) → variance даёт CI

**Спринт D:** Output formatting
- Structured output: `Answer { text, claims: [Claim], sources: [Source] }`
- Markdown rendering с inline confidence + clickable source links
- JSON для API consumers

**Спринт E:** UI / interaction
- Hover на claim → highlight source span в исходном документе
- Filter answer: «show only claims with confidence >80%»
- Audit trail для compliance use cases

### API sketch

```python
@dataclass
class Claim:
    id: str
    text: str
    confidence: float                # 0-1
    confidence_ci: tuple[float, float]  # (low, high) 95% CI
    sources: list[Source]

@dataclass
class Source:
    doc_id: str
    span: tuple[int, int]            # (start_char, end_char)
    similarity: float                # 0-1

@dataclass
class ProvenancedAnswer:
    text: str                        # human-readable
    claims: list[Claim]
    sources: list[Source]
    overall_confidence: float

def ask_with_provenance(question: str, *,
                         bootstrap_samples: int = 30,
                         retriever: Retriever | None = None) -> ProvenancedAnswer
```

### Метрики успеха
- Claim-source linking precision: ≥85% (manual labelled subset)
- CI coverage: 95% CI содержит «true» confidence (manual annotation) ≥90%
- User trust survey: +30% «уверены в ответе» против baseline
- Audit trail completeness: 100% claims имеют ≥1 source

### Риски
- Claims могут не покрываться источниками (LLM добавил «from world knowledge»). Решение: explicit «no source» flag
- Heavy compute (30 LLM calls per query). Митигация: opt-in mode для critical queries
- Source span resolution в long passages непросто. Решение: sentence-level granularity

---

## I4. Counterfactual probing (attribution map)

### Концепция
«Как бы изменился ответ, если убрать документ X из retrieval set?» — система автоматически перезапускает RAG с leave-one-out по top-k passages, измеряет diff в ответе, строит attribution map: «doc X внёс 30% содержания, doc Y — 15%, doc Z — 5%».

Базируется на работе [Attribution and Influence Functions for LLMs](https://arxiv.org/abs/2308.03296).

### Зачем
- Debugging RAG: понять почему был странный ответ
- Source criticism: «был ли doc X ключевым или просто фоновым»
- Detecting outliers: один документ диспропорционально влияет → suspicious

### Существующие primitives
- `rag/ask` — pipeline с явным retrieval set
- `feedback/` — для recording attribution decisions
- `experiments/` — для batch counterfactual runs

### Этапы реализации (4 спринта)

**Спринт A:** Leave-one-out runner
- `counterfactual_attribution(query, passages, k=top_k)`:
  - For each passage in top_k: убрать → re-ask → measure diff
  - Diff metric: edit distance / semantic similarity / claim overlap
- Output: per-passage influence score

**Спринт B:** Approximation для performance
- N+1 LLM calls дороги. Альтернативы:
  - Random subset masking: убираем 2-3 passages случайно K раз
  - Embedding-based proxy: similarity passage → answer как proxy для influence
  - Hybrid: точный для top-3, approx для tail

**Спринт C:** Visualization
- Markdown report: passages sorted by influence
- HTML interactive: bar chart, hover → show passage content
- Diff highlighting: что именно изменилось в answer

**Спринт D:** Anomaly detection
- Если один passage даёт >50% influence → flag «over-reliance»
- Pattern: хороший ответ должен быть «balanced» (no single source dominant)
- Alert через events bus

### API sketch

```python
@dataclass
class AttributionScore:
    passage_id: str
    doc_id: str
    influence: float                 # 0-1
    rank_change: int                 # how much answer-rank changed when removed
    semantic_diff: float
    claim_loss: list[str]            # what claims disappeared

@dataclass
class AttributionMap:
    query: str
    base_answer: str
    scores: list[AttributionScore]
    is_balanced: bool                # no passage > 50%

def counterfactual_attribution(query: str, *,
                                passages: list[Passage],
                                method: str = "exact",  # exact | sampled | embedding
                                samples: int = 10) -> AttributionMap
```

### Метрики успеха
- Influence scores correlation с manual «importance» annotation: ρ ≥ 0.7
- Balanced answers: ≥80% (proxy для good retrieval)
- Anomaly precision: «over-reliance» flag находит actual hallucinations в 70% случаев

### Риски
- Cost: N+1 LLM calls на query. Решение: opt-in для debugging mode, default off
- Stochastic LLMs дают разные ответы на same input. Решение: temperature=0 для attribution runs
- Ill-defined «influence» metric. Решение: multiple metrics, weighted combination

---

## I5. Memory-augmented LLM (MemGPT-style)

### Концепция
Внешняя долговременная память для LLM с tiered storage:
- **Working memory** (in-context): что у LLM прямо сейчас
- **Recall memory** (retrievable): полная история, retrieved as needed
- **Archival memory** (long-term): сжатые knowledge / facts learned

LLM сам решает: «запиши это в archival», «загрузи это из recall», «забудь это». Inspired by [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560).

### Зачем
- Coherent multi-session interactions (LLM «помнит» что было неделю назад)
- Knowledge accumulation: LLM learns from user corrections
- Foundation для personal AI assistant

### Существующие primitives
- `conversation/` (Sprint 49) — sessions + squash-summarize (близкий концепт)
- `feedback/` — что user одобрил/отверг
- `embeddings/` — для recall search

### Этапы реализации (6 спринтов)

**Спринт A:** Tier abstractions
- `WorkingMemory` (in-context messages): list[Message]
- `RecallMemory` (full history searchable): SQLite + vectors
- `ArchivalMemory` (semantic facts): structured KB
- Per-user namespacing

**Спринт B:** Memory-management tools
- LLM получает «memory tools»: `search_recall(query)`, `archive(text, tags)`, `forget(id)`
- Через agent loop (existing) → LLM выбирает когда использовать
- Logging: какие tools, как часто

**Спринт C:** Auto-archival heuristics
- При squash старого conversation history: extract «learned facts»
  - User preferences (anti-pattern: «не использую X»)
  - Stable facts о пользователе
  - Resolved questions (которые повторялись)
- Запись в archival с auto-tags

**Спринт D:** Recall ranking
- Multiple signals: recency, frequency, semantic relevance, user-marked importance
- Learning to rank: какие recall items привели к user satisfaction
- Cold start: simple cosine similarity

**Спринт E:** Forget mechanism
- Explicit user command: «забудь что я говорил про X»
- Auto-forget: items неиспользуемые >N дней + low importance
- GDPR-compliance: full purge per-user

**Спринт F:** Personal AI agent
- End-to-end demo: chat assistant который помнит month-long context
- Comparison с stateless baseline (no memory)
- Eval: «remembered correctly N out of M facts after 1 week»

### API sketch

```python
class TieredMemory:
    def add_to_working(self, msg: Message) -> None
    def archive(self, text: str, tags: list[str], importance: float = 0.5) -> str
    def recall(self, query: str, top_k: int = 5) -> list[RecallItem]
    def forget(self, item_id: str) -> None
    def stats(self) -> dict

class MemoryAugmentedAgent(AgentLoop):
    """Agent с автоматическим memory management."""
    def __init__(self, memory: TieredMemory, *args, **kwargs): ...
```

### Метрики успеха
- Multi-session coherence: «remembered correctly» on test queries: ≥80%
- Storage growth: linear with interactions, sub-linear after squash
- Latency overhead: <300ms per interaction (recall search)

### Риски
- Memory bloat (всё накапливается). Решение: aggressive auto-forget + size limits
- LLM забывает использовать memory tools. Митигация: prompt engineering + few-shot
- Privacy concerns. Решение: encryption at rest, per-user encryption keys

---

## I6. Hybrid sparse+dense+graph retrieval с learned fusion

### Концепция
3 источника relevance: BM25 (sparse), embeddings (dense), KG (graph). Сейчас RRF (Reciprocal Rank Fusion) использует фиксированный weight. Replace на learned fusion: на golden dataset обучается небольшая модель (logistic regression / GBM) предсказывающая relevance из 3 scores.

### Зачем
- Каждый retriever силен в разном — learned fusion адаптируется автоматически
- +5-15% improvement по литературе ([Reciprocal Rank Fusion outperforms Condorcet (2009)] vs learned)
- Online learning: модель улучшается с feedback

### Существующие primitives
- `rag/retriever.py` — hybrid (RRF) уже есть
- `kg/` (M1) — knowledge graph retriever
- `feedback/` — relevance signal
- `embeddings/` — dense retriever

### Этапы реализации (5 спринтов)

**Спринт A:** Per-method scores extraction
- Refactor: вместо ranks для RRF, expose raw scores BM25/dense/graph
- Normalize scores per method (z-score или min-max)
- Cache: same query → same scores (avoid re-computation)

**Спринт B:** Training pipeline
- Dataset: (query, passage, BM25_score, dense_score, graph_score, is_relevant)
- Sources of `is_relevant`: golden datasets (Sprint 48), feedback thumbs (Sprint 43)
- Train logistic regression на этих 3 features (+ optional: query length, passage length)

**Спринт C:** Inference
- `LearnedFusion.score(query, passage)` returns predicted relevance
- A/B vs RRF baseline на eval
- Production: gradual rollout с canary 10%

**Спринт D:** Online adaptation
- Periodic retraining (weekly) с накопленным feedback
- Concept drift detection: model accuracy drops → trigger retrain
- Versioning: hold rollback версия

**Спринт E:** Per-intent fusion weights
- Объединить с M4 (intent classification): factoid queries → BM25-heavy weights, synthesis → dense-heavy
- Train per-intent models или single model с intent feature
- Ablation study: marginal benefit per feature

### API sketch

```python
@dataclass
class FusionFeatures:
    bm25_score: float
    dense_score: float
    graph_score: float
    query_length: int
    passage_length: int
    intent: str = ""

class LearnedFusion:
    def __init__(self, model_path: Path | None = None): ...
    def fit(self, training_data: list[tuple[FusionFeatures, bool]]) -> None
    def score(self, features: FusionFeatures) -> float
    def explain(self, features: FusionFeatures) -> dict[str, float]  # SHAP-like

class HybridRetrieverLearned(Retriever):
    def search(self, query, top_k=5) -> list[Passage]
    # internally: BM25 + dense + graph → features → fusion → rank
```

### Метрики успеха
- nDCG@10 на golden eval: +10% против RRF baseline
- Per-intent gains: +20% для tags-related queries (где graph помогает)
- Online learning: model improves +1-2% precision per 1000 feedback events

### Риски
- Overfit на small golden set. Митигация: regularization, cross-validation, large-test
- Feature engineering — graph_score bias if KG sparse. Решение: train с / без graph как ablation
- Inference overhead. Решение: model fits в memory, prediction <1ms

---

## I7. Bandit-allocated A/B testing

### Концепция
Вместо фиксированного 50/50 split между prompt/retriever variants — **multi-armed bandit** автоматически allocate больше traffic к лучшему variant'у. Использует Thompson sampling: посчитан posterior на success rate, sampled, выбран highest sample.

### Зачем
- Минимизирует «regret»: меньше показов плохого variant'а
- Adapt к non-stationary distributions (что было лучшим вчера может быть хуже завтра)
- Экономия compute: не нужно полный N=1000 traffic split для significance

### Существующие primitives
- `experiments/` (Sprint 44) — A/B framework
- `feedback/` (Sprint 43) — Wilson score (близкий концепт)
- `prompts/` — variant pool

### Этапы реализации (4 спринта)

**Спринт A:** Bandit primitives
- `docstoolkit/bandit/` модуль
- `BetaBernoulliArm`: posterior на success/failure (success = thumbs_up)
- `ThompsonSamplingBandit`: select_arm(), update(arm, reward)
- Persistent state: SQLite, per-arm (alpha, beta) updated online

**Спринт B:** Integration
- `BanditExperiment` extends `Experiment`: variants → arms
- Each query runs through bandit-selected variant
- Update arm после feedback receipt

**Спринт C:** Cold start + exploration floor
- При новом arm: высокая variance posterior → exploration
- Floor exploration: minimum 5% traffic к каждому arm даже если loser
- Time-weighted: recent feedback важнее старого (decay)

**Спринт D:** Reporting
- Dashboard: per-arm posterior visualization (Beta distribution shapes)
- Allocation history over time
- Auto-promote winner: if one arm posterior >X% → make it default

### API sketch

```python
class BetaBernoulliArm:
    def __init__(self, alpha: float = 1.0, beta: float = 1.0): ...
    def update(self, success: bool, weight: float = 1.0) -> None
    def sample(self) -> float        # ~ Beta(alpha, beta)
    def mean(self) -> float
    def posterior_ci(self, q: float = 0.95) -> tuple[float, float]

class ThompsonBandit:
    def __init__(self, arms: dict[str, BetaBernoulliArm]): ...
    def select(self) -> str          # arm name to use
    def update(self, arm: str, reward: float) -> None
    def winner(self, confidence: float = 0.95) -> str | None
```

### Метрики успеха
- Regret (cumulative loss vs always-best): -50% против random allocation
- Time to detect winner: -30% против fixed split
- Robustness к non-stationary: detected switch <1 day

### Риски
- Confounders (пользователи разные между периодами). Решение: stratification
- Feedback delay (thumbs приходит позже). Решение: pending arms tracked
- Cold restart после big deploy. Решение: prior reset, exploration boost

---

## I8. Differential queries по времени

### Концепция
Запросы вида: «как изменился консенсус по теме X с 2023 по 2026?», «что новое мы узнали про Yodoca за последние 6 месяцев», «какие документы устарели». Использует git history corpus + temporal embedding analysis.

### Зачем
- Tracking evolution of knowledge / opinions
- Identifying stale content
- Historical context для current queries

### Существующие primitives
- `timetravel/` (Sprint 41) — git-based queries
- `improve_version_diff.py` — semantic diff между commits
- `cluster/` — для temporal clustering
- `feedback/` — temporal feedback patterns

### Этапы реализации (5 спринтов)

**Спринт A:** Temporal corpus snapshots
- `corpus_at(commit_hash) → indexable corpus`
- Snapshot caching (avoid re-checkout): pre-compute index per N commits
- API: `query_at_time(query, ts)` returns answer как было «тогда»

**Спринт B:** Temporal diff queries
- `diff_corpus(commit_a, commit_b, query=None)`:
  - Если query = None: structural diff (added/removed/modified docs)
  - Если query: semantic diff (different answer? different sources?)
- Output: timeline visualization

**Спринт C:** Concept evolution
- For concept X: trace mentions over time (frequency, sentiment, contexts)
- TimelineEvent: «X впервые упомянут 2025-03», «X ассоциировался с Y до 2025-09», «X поменял semantic neighbors»
- Markdown timeline output

**Спринт D:** Stale content detection
- Heuristic: документ не upd'd >N месяцев, contradictions с newer docs, low recent retrieval
- Score: `staleness = age_score + contradiction_score - centrality_score`
- List в `docs/STALE.md`

**Спринт E:** «Time machine» UI
- Slider: drag временной point → query at that time
- Side-by-side: «then vs now» для same query
- Use cases: research, retrospectives

### API sketch

```python
@dataclass
class TemporalAnswer:
    answer: str
    citations: list[Citation]
    timestamp: str
    commit: str

@dataclass
class ConceptEvolution:
    concept: str
    timeline: list[tuple[str, dict]]  # [(ts, {mentions, neighbors, contexts})]
    stability_score: float            # 0-1, how stable over time
    notable_changes: list[str]

def query_at_time(query: str, ts: str | datetime) -> TemporalAnswer
def evolve_concept(concept: str, *, since: str = "", until: str = "") -> ConceptEvolution
def detect_stale(threshold_days: int = 180) -> list[StaleDoc]
```

### Метрики успеха
- Snapshot speed: query_at_time <2 sec (with caching)
- Concept evolution: timeline events match human-annotated «interesting moments» ≥80%
- Stale detection: precision ≥75% (manual review)

### Риски
- Storage: snapshot indexes занимают место. Решение: incremental + lazy regen
- Git rewrite history (squash merges): timeline broken. Решение: monotonic timestamp from commit ts
- Compute heavy. Решение: async processing, results cached

---

## I9. Self-improving prompts (genetic algorithm)

### Концепция
Prompts эволюционируют автоматически через GA: population из N prompt variants → evaluate против golden + feedback → select top → crossover/mutate → next generation. Best promoted в prompt library.

Inspired by [PromptBreeder](https://arxiv.org/abs/2309.16797) и [Self-Refine](https://arxiv.org/abs/2303.17651).

### Зачем
- No-touch prompt improvement
- Discover non-obvious prompt formulations
- Адаптация к specific corpus / use case

### Существующие primitives
- `prompts/` (Sprint 51) — versioned prompt registry
- `experiments/` — A/B framework
- `feedback/` — Wilson scoring как fitness
- `eval/` — golden как fitness

### Этапы реализации (5 спринтов)

**Спринт A:** Population + fitness
- `Population[Prompt]` — initial: hand-crafted seed prompts
- `Fitness(prompt) → float`: A/B run на N golden queries → eval score
- Cache fitness (same template hash → same score)

**Спринт B:** Mutation operators
- `Rephrase`: paraphrase one sentence (LLM-assisted)
- `Inject`: add instruction («be concise», «use bullet points»)
- `Remove`: drop redundant clause
- `Reorder`: swap sentences
- Mutation probability per operator

**Спринт C:** Crossover
- Take sections from 2 parent prompts → combine
- Sentence-level crossover: split на sentences, randomly select from each parent
- Validate: rendered output не slabs или not-malformed

**Спринт D:** Selection + GA loop
- Tournament selection: pick K random, take best
- Elitism: top 20% survive untouched
- Generations: 10-30
- Stop conditions: fitness plateau or budget exhausted

**Спринт E:** Production integration
- Best evolved prompt → register в PromptLibrary as new version
- A/B test against current production version
- Auto-promote if statistically significant winner (Wilson)

### API sketch

```python
@dataclass
class GAConfig:
    population_size: int = 20
    generations: int = 15
    mutation_rate: float = 0.3
    crossover_rate: float = 0.5
    elite_count: int = 4
    fitness_samples: int = 30

class PromptGA:
    def __init__(self, base_prompt: Prompt, fitness_fn: Callable[[Prompt], float],
                  config: GAConfig | None = None): ...
    def evolve(self) -> list[tuple[Prompt, float]]   # ranked best→worst
    def best(self) -> Prompt
    def history(self) -> list[GenerationStats]
```

### Метрики успеха
- Final fitness vs initial: +20-40% improvement (typical GA gains)
- Diversity: ≥5 distinct «good» prompts (avoid premature convergence)
- Cost: budget cap per evolution run (~$5-20 в LLM cost)

### Риски
- Reward hacking: GA finds prompts что работают на golden но не generalize. Митигация: holdout test set
- LLM-mutation produces malformed prompts. Решение: validation pre-fitness
- Cost runaway. Решение: hard budget cap

---

## I10. Hierarchical map-reduce summarization

### Концепция
Для long-context queries (e.g. «обобщи всю секцию 05-habr-projects»): map step — суммаризировать каждый документ независимо, reduce step — синтезировать summaries → meta-summary. Recursive до final coherent output.

### Зачем
- Обход context window limits (any model)
- Coherent summarization больших корпусов
- Foundation для «what do we know about X» queries

### Существующие primitives
- `improve_textrank.py` — extractive summarization (Sprint 30)
- `improve_abstract.py` — auto-abstract per file
- `workflow/` — DAG для map-reduce
- `cluster/` — для grouping in reduce step

### Этапы реализации (4 спринта)

**Спринт A:** Map step
- Per-doc summarizer: TextRank (free) or LLM-based
- Cache summaries: doc_hash → summary
- Parallel: workflow run_async для N docs

**Спринт B:** Reduce step
- Group similar summaries (via clustering)
- Per-cluster meta-summary (LLM combines)
- Recursive если cluster meta-summaries всё ещё много

**Спринт C:** Query-aware
- При query: filter summaries по relevance к query (TF-IDF)
- Reduce focuses на relevant subset
- Output: structured `{topic: summary}` instead of monolithic blob

**Спринт D:** Caching + invalidation
- Doc summary stale если doc updated → regenerate
- Cluster summary stale if any constituent updated → regenerate
- Lazy: only recompute on demand

### API sketch

```python
@dataclass
class HierarchicalSummary:
    topic: str
    summary: str
    sources: list[str]
    sub_summaries: list["HierarchicalSummary"]   # nested
    coverage: float                              # % of corpus covered

def summarize_corpus(*, section: str = "", query: str = "",
                      max_summary_length: int = 2000,
                      method: str = "llm",  # llm | textrank | hybrid
                      ) -> HierarchicalSummary
```

### Метрики успеха
- Coverage: 100% relevant docs included
- Coherence: human review «reads like single coherent text»: ≥70%
- Latency: 5K-doc summary <30 sec (with caching)

### Риски
- Information loss in map step. Митигация: 2-3 sentences per source min
- Bias amplification: если одна тема over-represented в corpus, dominates summary. Решение: per-source weighting

---

## Сводная таблица

| ID | Название | Спринтов | Risk | Impact |
|----|----------|---------:|------|--------|
| I1 | Self-RAG с reflection | 5 | Medium | Very High (hallucinations) |
| I2 | Multi-agent debate | 5 | Medium | High (reasoning) |
| I3 | Provenance + CI | 5 | Medium-High | Very High (trust) |
| I4 | Counterfactual probing | 4 | Medium | Medium (debugging) |
| I5 | Memory-augmented (MemGPT) | 6 | High | Very High (personal AI) |
| I6 | Learned fusion (sparse+dense+graph) | 5 | Medium | High (quality) |
| I7 | Bandit A/B allocation | 4 | Low-Medium | Medium (efficiency) |
| I8 | Differential temporal queries | 5 | Medium | High (unique capability) |
| I9 | Self-improving prompts (GA) | 5 | Medium-High | Medium-High |
| I10 | Map-reduce hierarchical summary | 4 | Low-Medium | High (long context) |

**Общий бюджет:** ~48 спринтов на все 10. Реалистично выбрать 3-4 наиболее ценных.

---

## Рекомендуемый порядок

1. **I1** (Self-RAG) — biggest hallucination reduction, low overhead
2. **I3** (Provenance + CI) — foundation для trust, complementary с I1
3. **I7** (Bandit A/B) — quick win для experimentation efficiency
4. **I10** (Map-reduce) — нужно для production-grade long-context
5. **I8** (Differential temporal) — unique selling point
6. **I6** (Learned fusion) — следующий шаг после M2 cross-encoder
7. **I2** (Multi-agent debate) — для high-stakes queries
8. **I4** (Counterfactual probing) — для debugging
9. **I5** (Memory-augmented) — большая работа, окупится только в long-term assistant use case
10. **I9** (GA prompts) — research-y, отложить до stable foundation
