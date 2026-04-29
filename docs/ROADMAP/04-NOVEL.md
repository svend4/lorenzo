# 04 — Никем не сделанные направления (true novelty)

Это не frontier research (что в I-блоке), а **концепции которые никем не упакованы в production систему**, или сделаны кусочно в разных проектах но не сложены вместе. Высокий риск, неизвестность, но и потенциал для truly differentiated product.

**Документ:** часть серии ROADMAP. См. также: [00-CURRENT-STATE](./00-CURRENT-STATE.md), [01-SIMPLE](./01-SIMPLE.md), [02-MEDIUM](./02-MEDIUM.md), [03-INNOVATIVE](./03-INNOVATIVE.md), [05-PRIORITIES](./05-PRIORITIES.md).

⚠️ Каждая идея — research project на 2-3 месяца минимум. Многие могут не сработать. Но любая одна успешная — патентоспособный или article-worthy результат.

---

## N1. Document «metabolism» — живые документы

### Концепция
Файл — не статичный артефакт, а активный агент: он:
1. **Поглощает** релевантные новые фрагменты из ingest stream
2. **Помечает** свои секции как stale если появились более новые / противоречивые источники
3. **Конвергирует** к актуальной формулировке через autorewrite
4. **Откатывается** если новый source оказался unreliable (через feedback)

Документ становится самообновляющимся organism, а не frozen snapshot.

### Почему никто не сделал
- Большинство DMS / wikis treat docs as immutable user-edited artifacts
- Auto-rewrite contentious (writer ownership)
- Conflict resolution complex (что если 2 источника противоречат?)
- Редкая комбинация: ingest pipeline + auto-rewrite + version control + trust signals

### Существующие primitives для старта
- `improve_subtopic_fill.py` — вставка контента в шаблоны
- `improve_contradiction_check.py` — обнаружение противоречий
- `feedback/` — trust signals
- `timetravel/` — git history для rollback

### Этапы реализации (8-12 спринтов)

**Фаза 1: Pull mechanism (3 спринта)**
- `MetabolicDocument` wrapper: doc + metadata (sources, freshness, confidence per section)
- Watcher: новый ingest → check каждый existing doc на «есть ли relevant content»
- Suggest mode: предлагает изменения в PR-style (не auto-apply)

**Фаза 2: Auto-rewrite (3 спринта)**
- LLM-assisted: «вот старая секция, вот новый source — улучшите секцию»
- Quality gates: не применять если delta слишком большой (preserves voice)
- Audit trail: every change linked к source ingest event

**Фаза 3: Stale-marking (2 спринта)**
- Detect contradictions с newer sources
- Visual marker в rendered output: «секция X помечена как stale, последняя проверка Y»
- Notify owner через webhook

**Фаза 4: Trust loop (2 спринта)**
- Each rewrite tracked через feedback (thumbs)
- Source reliability score: track which sources lead to «good» rewrites
- Bad sources → less weight in future rewrites
- Rollback if rewrite получил много thumbs_down

**Фаза 5: Production polish (2 спринта)**
- UI for review: «вот предложенные изменения, accept / reject»
- Conflict resolution: что если 2 sources противоречат → both shown, human picks
- Owner controls: «эта секция — frozen, не трогать»

### API sketch

```python
@dataclass
class MetabolicSection:
    text: str
    sources: list[Source]
    freshness_score: float           # 0-1
    confidence: float
    last_rewrite_ts: str
    is_frozen: bool = False

@dataclass
class MetabolicDocument:
    path: Path
    sections: list[MetabolicSection]
    overall_freshness: float
    metabolism_log: list[MetabolismEvent]

class MetabolismEngine:
    def on_ingest(self, new_source: Source) -> None        # main hook
    def suggest_updates(self, doc: MetabolicDocument) -> list[Suggestion]
    def apply_suggestion(self, sugg: Suggestion, *, auto: bool = False) -> None
    def mark_stale(self, doc_path: Path, section_idx: int, reason: str) -> None
```

### Метрики успеха
- Document freshness: average ≥0.7 across corpus
- Suggestion acceptance rate: ≥40% (не too noisy)
- Voice preservation: writer review «still sounds like me» ≥80%
- Stale detection precision: ≥75%

### Риски и mitigations
- **Edit wars** между человеком и системой → frozen sections, opt-in per doc
- **Voice drift** → quality gate с similarity to original voice
- **Cascade failures** (bad source → bad rewrite → bad future): rollback chain через timetravel
- **User trust** → audit trail, easy rollback

### Этическое измерение
- Authorship attribution: кто «автор» документа после 50 rewrites?
- Provenance critical (см. I3)
- Maintainer должен видеть «доля собственного текста» metric

---

## N2. Negotiating retrieval (multi-agent bargaining)

### Концепция
Несколько retriever-агентов «торгуются» за слоты в context window:
- BM25-агент предлагает: «возьмите doc X, у меня высокий keyword match»
- Semantic-агент: «возьмите doc Y, она semantically closer»
- Graph-агент: «doc Z connected к entity в query»
- Diversity-агент: «у вас уже 3 docs про память, возьмите этот вместо для разнообразия»
- Cost-агент: «doc W длинный, не tradeoff'ится»

Аукцион: агенты bid на слоты, scoring → final passages selection.

### Почему никто не сделал
- Большинство retrieval = static fusion (RRF)
- Multi-agent systems обычно для reasoning, не для retrieval
- Cost concerns: 5+ agents на каждый query
- Concept of «diversity-agent» / «cost-agent» как peers — необычно

### Существующие primitives
- Multiple retrievers existing
- `agent/` — agent loop pattern
- `cluster/` — diversity measurement
- `budget/` — cost considerations

### Этапы реализации (6-8 спринтов)

**Фаза 1: Bid framework (2 спринта)**
- `RetrieverAgent` ABC: `bid(query, candidate_passage) → Bid {score, rationale}`
- 4-5 built-in agents
- `RetrievalAuction.run(query, candidates_pool, slots=5)` → selected

**Фаза 2: Negotiation rounds (2 спринта)**
- After initial bid: agents see others' bids → can revise
- Coalition forming: agents agree «if you take mine, I'll support yours»
- Decision rule: vickrey-style auction (second price)

**Фаза 3: Learning (2 спринта)**
- Track which selections led к good answers (feedback)
- Adjust agent voting power on success rate
- New agent types if patterns suggest

**Фаза 4: Optimization (2 спринта)**
- Cost: parallel bidding, batch LLM calls if used
- Cache: same query+candidate → same bid
- Ablation: drop low-utility agents

### API sketch

```python
@dataclass
class Bid:
    agent: str
    passage_id: str
    score: float
    rationale: str
    revisable: bool = True

class RetrieverAgent(Protocol):
    name: str
    def bid(self, query: str, candidate: Passage,
            other_bids: list[Bid] = None) -> Bid

class RetrievalAuction:
    def __init__(self, agents: list[RetrieverAgent]): ...
    def run(self, query: str, candidates: list[Passage],
            slots: int = 5, rounds: int = 2) -> AuctionResult

@dataclass
class AuctionResult:
    selected: list[Passage]
    bid_log: list[Bid]
    coalition: dict
    explanation: str
```

### Метрики успеха
- Diversity: avg cosine distance between selected ≥ baseline + 15%
- Quality: nDCG@5 ≥ baseline (no regression)
- Interpretability: rationale per selection (audit-friendly)

### Риски
- Compute cost (multiple agents per query). Решение: cheap heuristic agents preferred
- Coalition collusion → один агент doминирует. Решение: cap voting power
- Hard to debug. Решение: full bid log

---

## N3. Graph-of-thoughts над корпусом

### Концепция
Не linear chain-of-thought, а **DAG промежуточных гипотез**. Каждая нода — partial answer / fact / hypothesis с links к sources. Reasoner explores graph: confirms, refutes, refines.

Пользователь видит не финальный ответ, а **explorable graph rationale** — может развернуть «как пришли к этому».

Inspired by [Graph of Thoughts](https://arxiv.org/abs/2308.09687) — но применено не к prompt design, а к corpus reasoning.

### Почему никто не сделал
- GoT papers focus на LLM internal reasoning, не на explainable RAG
- UI complexity (graph visualization)
- Memory model (graph можно держать большим)
- Не очевидно когда graph выгоднее chain

### Существующие primitives
- `agent/planner.py` (Sprint 50) — DAG decomposition (близкий концепт)
- `workflow/` — DAG execution
- `graph/` — graph builder + visualization
- `adaptive/` — multi-hop retrieval

### Этапы реализации (8-10 спринтов)

**Фаза 1: Thought primitives (2 спринта)**
- `Thought`: id, text, type (claim | hypothesis | observation | refutation)
- `ThoughtEdge`: src→dst, relation (supports | refutes | refines | follows_from)
- `ThoughtGraph`: container, queries, traversal

**Фаза 2: Graph construction (3 спринта)**
- LLM-driven: from question + retrieved passages → initial thoughts
- Iterative: each thought спавнит follow-up thoughts (sub-questions)
- Stop conditions: max nodes, convergence (no new useful thoughts)

**Фаза 3: Aggregation (2 спринта)**
- From DAG → final answer
- Methods: weighted sum (по support), longest path, central nodes, voting
- Confidence из graph topology

**Фаза 4: UI (2 спринта)**
- D3.js / vis.js graph visualization
- Click node → see source passages
- Filter: «show only confirmed claims», «show contested»

**Фаза 5: Integration (1 спринт)**
- Endpoint `/api/got/ask`
- Output: structured GoT result (json) + render

### API sketch

```python
@dataclass
class Thought:
    id: str
    text: str
    kind: str                        # claim | hypothesis | observation | refutation
    sources: list[Source]
    confidence: float                # 0-1
    parent_ids: list[str]

@dataclass
class ThoughtEdge:
    src: str
    dst: str
    relation: str                    # supports | refutes | refines | follows_from
    weight: float = 1.0

@dataclass
class ThoughtGraph:
    question: str
    thoughts: dict[str, Thought]
    edges: list[ThoughtEdge]
    final_answer: str
    aggregation_method: str
    confidence: float

class GoTReasoner:
    def __init__(self, max_thoughts: int = 30,
                  max_depth: int = 4, retriever=None): ...
    def build(self, question: str) -> ThoughtGraph
    def aggregate(self, graph: ThoughtGraph,
                   method: str = "weighted") -> str
```

### Метрики успеха
- Reasoning depth: average ≥3 thought levels
- Source coverage: ≥80% citations grounded in sources
- User comprehension: «I understand how the answer was derived» survey ≥75%
- Comparison vs flat RAG: +20% on multi-hop reasoning benchmarks

### Риски
- Compute (multiple LLM calls). Решение: budget cap, cheap model for thought spawning
- Graph explosion. Решение: pruning, max nodes
- UI complexity. Решение: progressive disclosure (start collapsed)

---

## N4. Continual «voice» / эпистемический профиль корпуса

### Концепция
Корпус имеет устойчивый эпистемический стиль — «осторожный исследователь», «контр-консенсусный provocateur», «исторический систематизатор». Этот voice сохраняется через все retrieval/synthesis несмотря на гетерогенность источников.

При добавлении новых документов voice контролирует:
- Что добавляется (filter through epistemic match)
- Как переписывается (auto-rewrite в стиле voice)
- Как отвечает agent (всегда в этом «голосе»)

### Почему никто не сделал
- Большинство DMS / LLMs deliberately neutral
- Notion of «corpus voice» not formalized
- Trade-off: voice-фильтрация vs comprehensiveness
- Требует deep style modeling (beyond just prompt)

### Существующие primitives
- `prompts/` — versioned prompts as voice carriers
- `improve_vocabulary_richness.py` — TTR / lexical density (Sprint 27)
- `improve_passive_voice.py` — style metrics
- `improve_textrank.py` — extract characteristic sentences

### Этапы реализации (10-12 спринтов)

**Фаза 1: Voice extraction (3 спринта)**
- `EpistemicProfile` measurements:
  - Stance markers («I think», «evidence suggests», «proven that»)
  - Hedging frequency
  - Lexical sophistication (TTR, hapax)
  - Sentence structure patterns (avg length, complexity)
  - Citation density
- Per-doc profile → corpus-aggregate profile

**Фаза 2: Voice quantification (2 спринта)**
- `voice_distance(text_a, text_b) → float`
- Vector-based: 20-dim style embedding
- Comparison к canonical voice corpus (5-10 «exemplary» docs)

**Фаза 3: Voice-aware ingest (2 спринта)**
- New doc evaluated против corpus voice
- Score: «fits voice» yes/no/marginal
- Suggestions: «to fit voice, rewrite section X with more hedging»
- Optional auto-rewrite (с user approval)

**Фаза 4: Voice-preserving synthesis (3 спринта)**
- LLM-answer always через style transfer step
- Prompt: «answer this question in voice characterized by these examples»
- Few-shot examples из exemplary docs
- Output validation: voice_distance ≤ threshold

**Фаза 5: Adaptive voice (2 спринта)**
- Voice itself может evolve (slowly): track changes over time
- User intervention: «set voice to more skeptical»
- Multi-voice corpus: discrete sub-corpora с different voices

### API sketch

```python
@dataclass
class EpistemicProfile:
    stance_distribution: dict[str, float]    # «hedged»: 0.4, «certain»: 0.3
    hedging_density: float
    lexical_richness: float
    avg_sentence_length: float
    citation_density: float
    exemplary_passages: list[str]            # canonical examples

class VoiceEngine:
    def profile(self, corpus: Path) -> EpistemicProfile
    def score(self, text: str, target: EpistemicProfile) -> float   # 0-1 fit
    def transfer(self, text: str, target: EpistemicProfile) -> str  # rewrite
    def evolve(self, profile: EpistemicProfile,
                new_examples: list[str], rate: float = 0.1) -> EpistemicProfile
```

### Метрики успеха
- Voice consistency score: ≥0.85 across corpus (vs ~0.5 baseline)
- Human review «sounds consistent» ≥80%
- Style transfer fidelity: maintain meaning + match voice ≥75%
- Onboarding new contributors: «I understand the house style» faster

### Риски
- Voice rigidity excludes valuable но «off-style» content. Решение: opt-out tag per doc
- Style transfer leaks original style. Решение: ensemble of style metrics, gate
- Subjective notion of «voice». Решение: explicit examples, not abstract description

---

## N5. Federated golden datasets с privacy

### Концепция
Несколько Lorenzo-нод обмениваются eval-результатами без раскрытия запросов / документов. Используются:
- Differential privacy (DP) noise на metrics
- Homomorphic encryption (HE) для query/result
- Secure aggregation (SecAgg) для summary statistics

Глобальное улучшение через shared learning без centralization данных.

### Почему никто не сделал
- DP/HE/SecAgg — отдельные fields, мало кто комбинирует в applied form
- Federated learning (FL) обычно для models, не для datasets
- Use case: организации хотят compare без sharing
- Standardization (NPP federation extension) сложная

### Существующие primitives
- `federation/` (Sprint 36) — NPP протокол (готов для extension)
- `eval/` — golden dataset structure
- `webhooks/` — для cross-node communication

### Этапы реализации (10+ спринтов — pure research)

**Фаза 1: Threat model (1 спринт)**
- Document attacker model: who, what info, with what budget
- Privacy budget definition (ε-DP)
- Attack vectors: query inference, document inference, membership

**Фаза 2: DP noise (3 спринта)**
- Lib: opt-in `opacus` или Google's DP libraries
- Noise on per-query metrics (P/R/F1)
- Aggregate noise budget across queries

**Фаза 3: HE for query content (3 спринта)**
- Lib: opt `tenseal` (CKKS scheme)
- Limited operations: similarity comparison without decryption
- Query templates encrypted, parameters hidden

**Фаза 4: SecAgg для metrics (2 спринта)**
- Multi-party computation для sum/mean across nodes
- No single node sees other's raw metrics
- Output: aggregated «field-wide quality 78%» without per-node values

**Фаза 5: NPP extension (2 спринта)**
- New endpoint `/npp/federated-eval`
- Discovery: which peers willing to participate
- Round protocol: share, aggregate, distribute back

### API sketch

```python
@dataclass
class FederatedEvalRound:
    round_id: str
    participants: list[str]          # peer URLs
    privacy_budget: float            # epsilon
    aggregation_method: str          # secagg | dp_mean

class PrivateGoldenSet:
    """Зашифрованный golden, peer не видит content."""
    encrypted_questions: list[bytes]
    public_metrics: dict             # only aggregate stats public

class FederatedEvalCoordinator:
    def initiate_round(self, peers: list[str],
                        config: FederatedEvalRound) -> RoundResult
    def participate(self, peer_request: dict) -> dict   # incoming role
```

### Метрики успеха
- Privacy: ε ≤ 1 для acceptable noise
- Utility: aggregated metric within ±5% of true value
- Adoption: >2 organizations join федерированный round (proof-of-concept)

### Риски
- Heavy crypto dependencies (HE libraries large + slow). Митигация: opt-in module
- Difficult to audit. Решение: open-source все crypto, third-party review
- Slow (HE operations 10-100x slower). Acceptable for batch eval, not realtime

### Почему это truly novel
- HE+DP+SecAgg combo для eval (not for model training) is unique
- Knowledge management space lacks privacy-preserving cross-org collaboration
- First-mover в «trust without sharing»

---

## N6. Knowledge diffusion между корпусами

### Концепция
Концепты из корпуса A автоматически «диффундируют» в корпус B через alignment в shared embedding space. С трассировкой провенанса: «эта секция в корпусе B произошла от концептов A1, A2 + local synthesis».

Применение: organization adopts external knowledge base, integrates into own without losing attribution.

### Почему никто не сделал
- Cross-corpus alignment — research topic, no production tool
- Provenance preservation across diffusion — non-trivial
- Trust models: when accept external concepts? When reject?
- Bidirectional: A→B и B→A с feedback loops

### Существующие primitives
- `embeddings/` — shared space possible
- `federation/` — multi-node communication
- `improve_external_compare.py` — comparison с внешними источниками
- `webhooks/` — async cross-corpus events

### Этапы реализации (10 спринтов)

**Фаза 1: Cross-corpus alignment (3 спринта)**
- Joint embedding space: train на shared seed concepts (Anthropic vacancies + Habr projects есть в обоих)
- Identify «bridge concepts»: high similarity in both corpora
- Alignment matrix: mapping conceptA ↔ conceptB

**Фаза 2: Diffusion mechanism (3 спринта)**
- Trigger: new concept in A → check alignment к B
- Score: should diffuse? (high uniqueness, high relevance, fits B's voice — N4)
- Action: notify B owner, suggest insertion

**Фаза 3: Provenance graph (2 спринта)**
- DAG of concept lineage: «B-section X derived from A-passage Y + local additions Z»
- Visualization: provenance tree per section
- Audit: trace any claim к original source(s)

**Фаза 4: Trust model (2 спринта)**
- Per-corpus trust score (initialized neutral, evolves with feedback)
- Diffused content tagged с trust level
- Auto-revert if subsequent feedback negative

### API sketch

```python
@dataclass
class CorpusAlignment:
    corpus_a: str
    corpus_b: str
    shared_concepts: list[tuple[str, str, float]]  # (concept_a, concept_b, similarity)
    bridge_passages: list[tuple[Passage, Passage]]
    alignment_score: float

@dataclass
class DiffusionEvent:
    source_corpus: str
    target_corpus: str
    concept: str
    source_passages: list[Source]
    target_position: str             # where in target it goes
    confidence: float
    accepted: bool = False

class DiffusionEngine:
    def align(self, corpus_a: Path, corpus_b: Path) -> CorpusAlignment
    def detect_diffusion_candidates(self, alignment: CorpusAlignment) -> list[DiffusionEvent]
    def apply(self, event: DiffusionEvent) -> None
    def revert(self, event_id: str) -> None
```

### Метрики успеха
- Alignment quality: ≥75% бы human аннотатором as «good match»
- Diffusion acceptance rate: 30-50% (selective)
- Provenance completeness: 100% diffused content traceable

### Риски
- Echo chambers (corpora становятся похожими). Решение: diversity penalty
- Authorship issues. Решение: explicit attribution в frontmatter
- Quality degradation если bad source. Решение: trust model + revert

---

## N7. Self-organizing taxonomy

### Концепция
Категории / папки в `docs/` не задаются заранее, а **эмерджентно складываются** из паттернов:
- Кластеры запросов пользователей (что часто ищут вместе)
- Co-citation patterns (что упоминается вместе)
- Semantic similarity между документами
- Topic modeling drift over time

Структура auto-reorganizes когда natural taxonomy меняется.

### Почему никто не сделал
- Wikis / DMS use static folder hierarchies
- File-system constraints: physical movement triggers many hooks
- User confusion («где мой файл?») — mitigation requires deep UX work
- Reverse-compatibility (links break)

### Существующие primitives
- `cluster/` — k-means clustering
- `improve_topic_model.py` — TF-IDF topics (Sprint 16)
- `improve_reclassify.py` — moves docs to better section
- `feedback/` — usage signals

### Этапы реализации (8 спринтов)

**Фаза 1: Inferred taxonomy (3 спринта)**
- Continuous clustering: docs в N latent clusters
- Cluster names: extract via TF-IDF top terms или LLM-summarized
- Graph: cluster ↔ cluster через shared docs / co-citation
- Visualization: hierarchy tree (parent / child / sibling)

**Фаза 2: Stable identifiers (2 спринта)**
- Each doc has stable UUID independent of folder
- All links via UUID (or content-addressable hash)
- Folder path becomes hint, not location

**Фаза 3: Reorganize daemon (2 спринта)**
- Periodic check: cluster membership changed?
- Suggest: «document X belongs более к cluster Y, move?»
- Auto-apply if confidence high + user opted in
- Maintain redirects (old path → new path)

**Фаза 4: Drift visualization (1 спринт)**
- Animated taxonomy: how it changed last 30/90/365 days
- New emerging clusters highlighted
- Cluster mergers / splits marked

### API sketch

```python
@dataclass
class TaxonomyNode:
    id: str
    label: str                       # auto-generated or human-curated
    parent_id: str | None
    children_ids: list[str]
    docs: list[str]                  # by stable UUID
    centroid: list[float]
    last_updated: str

class SelfOrganizingTaxonomy:
    def infer(self, corpus: Path) -> dict[str, TaxonomyNode]
    def suggest_moves(self) -> list[MoveSuggestion]
    def apply_move(self, doc_id: str, new_node: str) -> None
    def visualize_drift(self, since_days: int = 30) -> str   # mermaid
```

### Метрики успеха
- Taxonomy stability: ≤5% docs move per month at steady state
- Search efficiency: «found what I wanted» ≥75% (vs <60% in static taxonomy)
- New cluster detection: detected within 7 days of emergence

### Риски
- User confusion. Решение: search-first UX, taxonomy as navigation aid only
- Frequent thrashing. Решение: hysteresis (require N consecutive checks before move)
- Lost documents. Решение: comprehensive search + redirects

---

## N8. Counterfactual corpus («что если»)

### Концепция
Sandbox-режим: «удали гипотетически документ X, посмотри на изменения downstream». Система предсказывает:
- Какие answers изменятся (какие queries затронуты)
- Какие downstream documents потеряют source
- Какие decisions / contacts / actions были основаны на X

Применение: research, decision audits, source criticism («что если этой work не существует»).

### Почему никто не сделал
- Forward-deletion easy, predicting downstream hard
- Requires comprehensive provenance graph (см. I3)
- Compute-heavy (re-evaluate corpus subset)
- Niche use case (mostly research / audit)

### Существующие primitives
- `timetravel/` — historical state queries
- `eval/` — for measuring difference
- `feedback/` — for tracking decisions linked к docs

### Этапы реализации (7 спринтов)

**Фаза 1: Provenance graph (3 спринта)**
- Track: every claim в `docs/` linked к source(s)
- Decisions log: `docs/DECISIONS.md` entries with source citations
- Eval golden also linked к source assumptions

**Фаза 2: Counterfactual engine (2 спринта)**
- `counterfactual_remove(doc_id) → CounterfactualReport`:
  - Affected queries (re-rank без doc, compare top-k)
  - Affected decisions (which links broken)
  - Cascade: docs that cited X also lose source
- Sandbox mode: changes не применяются к real corpus

**Фаза 3: Visualization (1 спринт)**
- Tree: «remove X → affects A, B, C → cascade to D, E»
- Quantification: «3 decisions, 12 queries, 4 cascade docs»
- Markdown report

**Фаза 4: «What if» queries (1 спринт)**
- Endpoint: `POST /api/counterfactual {action: «remove», target: «doc_id»}`
- Async: heavy compute, returns job_id
- Use cases: pre-deletion analysis, source value estimation

### API sketch

```python
@dataclass
class CounterfactualReport:
    action: str                      # «remove» | «add_hypothetical» | «modify»
    target: str                      # doc_id
    affected_queries: list[QueryDelta]
    affected_decisions: list[DecisionDelta]
    cascade_docs: list[str]
    severity: str                    # low | medium | high | critical

@dataclass
class QueryDelta:
    query: str
    before_top_k: list[str]
    after_top_k: list[str]
    confidence_change: float

class CounterfactualEngine:
    def remove(self, doc_id: str) -> CounterfactualReport
    def add_hypothetical(self, content: str, where: str) -> CounterfactualReport
    def value_of(self, doc_id: str) -> float  # «importance» from CF analysis
```

### Метрики успеха
- Cascade detection completeness: ≥90% (manual labelled cases)
- Compute time on 500-doc corpus: <60 sec per CF
- Decision support: «would you delete this doc?» yes/no correlates с severity rating

### Риски
- Provenance graph maintenance overhead. Митигация: batch updates
- Overestimating cascades. Решение: severity threshold gates
- Storage of provenance growth. Решение: pruning of old links

---

## N9. Personality-shaped retrieval

### Концепция
Результаты filtered through user's эпистемический profile:
- **Skeptic**: предпочитает контр-аргументы, ищет противоречия
- **Synthesizer**: high-level patterns, abstract connections
- **Explorer**: diversity over relevance, серендипитность
- **Verifier**: source authority, citation density
- **Pragmatist**: action-oriented passages

Один query → разные результаты для разных users.

### Почему никто не сделал
- Most personalization = collaborative filtering / topic profile, not cognitive style
- Cognitive style measurement non-trivial (require survey + behavioral tracking)
- UX: «my results differ from yours» confusing
- Privacy: cognitive profile sensitive

### Существующие primitives
- `profile/` (S6) — user preferences
- `feedback/` — behavioral signals
- Multiple retrievers (built-in)

### Этапы реализации (8 спринтов)

**Фаза 1: Style profiling (3 спринта)**
- 5-minute survey: 20 forced-choice questions
- Behavioral tracking: «did user explore deep into one doc or browse many»
- Output: 5-dim cognitive profile vector

**Фаза 2: Style-to-retrieval mapping (2 спринта)**
- Skeptic → boost passages с «however», «but», «contradicts»
- Explorer → MMR (max marginal relevance) для diversity
- Verifier → boost cited / authoritative
- Per-style retrieval modifiers

**Фаза 3: Adaptive learning (2 спринта)**
- Track: для each user, which results led to engagement
- Refine style profile over time (gradient updates)
- Cold start: heuristics from initial query patterns

**Фаза 4: Transparency (1 спринт)**
- «Why these results?» button → shows profile influence
- User can override: «show me default ranking»
- Profile editable by user

### API sketch

```python
@dataclass
class CognitiveProfile:
    skepticism: float                # 0-1
    synthesis: float
    exploration: float
    verification: float
    pragmatism: float
    confidence: float                # how well calibrated

class PersonalRetriever(Retriever):
    def __init__(self, base: Retriever, profile: CognitiveProfile): ...
    def search(self, query, top_k=5) -> list[Passage]
    def explain_personalization(self, results: list[Passage]) -> dict
```

### Метрики успеха
- User engagement (time-on-result): +25% over default
- «Found what I wanted» survey: +15%
- Profile stability: < 10% change per month at steady state

### Риски
- Filter bubbles. Митигация: «show me different perspective» button
- Profile inaccuracy. Решение: continuous calibration
- Privacy. Решение: per-user encrypted profile storage

---

## N10. Adversarial co-evolution

### Концепция
Система генерирует **hard questions против самой себя**:
- Questions для которых она even now дают плохие ответы
- Questions exposing gaps в corpus
- Questions designed exploit known biases retrievers / answerers

Эти questions → дополняются human-labelled answers → расширяют golden dataset → improve system → repeat.

### Почему никто не сделал
- Self-adversarial systems mostly в RL / GAN context, not RAG
- Question generation требует strong LLM
- Ethical: system finds its own weaknesses, who controls disclosure?
- Loop closure complex (need labelling pipeline)

### Существующие primitives
- `eval/` — golden dataset structure
- `experiments/` — A/B for measuring improvement
- `feedback/` — failure signals

### Этапы реализации (8 спринтов)

**Фаза 1: Adversarial generator (3 спринта)**
- LLM-driven: «look at corpus + this question pattern → generate harder version»
- Patterns: multi-hop, entity confusion, time-sensitive, contradictory premise
- Output: candidate hard questions with predicted difficulty

**Фаза 2: Difficulty validation (2 спринта)**
- Test predicted-hard на actual system: какие fail?
- Confirmed-hard added к queue
- Self-RAG (I1) reflect score / multi-agent (I2) disagreement как proxy

**Фаза 3: Active learning loop (2 спринта)**
- Hard question → human labels expected answer
- Added к golden dataset (Sprint 48)
- A/B: system re-evaluated, improvement tracked

**Фаза 4: Continuous evolution (1 спринт)**
- Periodic adversarial generation (weekly)
- Track: какие patterns (multi-hop, etc.) most often hard
- Prioritize improvements в этих directions

### API sketch

```python
@dataclass
class AdversarialQuestion:
    question: str
    pattern: str                     # multi_hop | entity_confusion | etc.
    predicted_difficulty: float      # 0-1
    actual_difficulty: float = 0.0   # measured later
    target_weakness: str             # what it tries to expose

class AdversarialGenerator:
    def generate(self, corpus: Path, n: int = 10,
                  pattern: str = "") -> list[AdversarialQuestion]
    def validate(self, questions: list[AdversarialQuestion]) -> list[AdversarialQuestion]

class CoEvolutionLoop:
    def step(self) -> CoEvolutionStats   # one iteration: generate → validate → label → eval
```

### Метрики успеха
- Hard question hit rate: ≥30% (predicted-hard actually hard)
- System improvement per loop: +1-2% eval score
- Coverage: weak patterns identified within 5 iterations

### Риски
- LLM может придумывать questions без grounding в corpus. Решение: strict «based on corpus» constraint
- Loop never converges (always finds new gaps). Решение: budget per iteration, stop when diminishing returns
- Labelling cost. Решение: prioritize by predicted impact

---

## Сводная таблица

| ID | Название | Спринтов | Risk | Novelty | Patent / publish |
|----|----------|---------:|------|---------|------------------|
| N1 | Document «metabolism» | 8-12 | Very High | Very High | Likely patentable |
| N2 | Negotiating retrieval | 6-8 | High | High | Publishable |
| N3 | Graph-of-thoughts на корпусе | 8-10 | High | High | Publishable, demo-able |
| N4 | Continual «voice» | 10-12 | Very High | Medium-High | Publishable |
| N5 | Federated golden + privacy | 10+ | Very High | Very High | Patentable, publishable |
| N6 | Knowledge diffusion | 10 | Very High | High | Publishable |
| N7 | Self-organizing taxonomy | 8 | High | Medium-High | Publishable |
| N8 | Counterfactual corpus | 7 | Medium-High | High | Publishable |
| N9 | Personality-shaped retrieval | 8 | High | High | Publishable |
| N10 | Adversarial co-evolution | 8 | High | High | Publishable |

**Общий бюджет:** ~80+ спринтов на все. Реалистично: выбрать 1-2 для глубокой реализации, остальные оставить как roadmap для возможной разработки или партнёрств.

---

## Selection criteria — какой выбрать

### Критерий 1: Уникальность
**Топ-3 наиболее уникальных:** N1 (metabolism), N5 (federated + privacy), N6 (diffusion)

### Критерий 2: Демонстрируемость
**Топ-3 для wow-демо:** N3 (graph of thoughts UI), N1 (auto-updating docs), N9 (personalized results)

### Критерий 3: Использует existing strengths Lorenzo
**Топ-3 best fit:** N3 (есть DAG primitives), N7 (есть clustering), N8 (есть timetravel)

### Критерий 4: Обозримый risk
**Топ-3 lowest risk среди novel:** N3, N7, N8

### Рекомендация
Если ОДНО — то **N3 (graph-of-thoughts на корпусе)**:
- Прямой путь от уже существующего workflow + agent + adaptive
- Visual demo сразу впечатляет
- Использует existing primitives на 60-70%
- Бюджет 8-10 спринтов реалистичен
- Publishable как research, useful как product

Если ДВА — **N3 + N1**:
- N3 даёт reasoning / UI differentiation
- N1 даёт infrastructure / corpus-as-living-organism narrative
- Together: complete unique product positioning
