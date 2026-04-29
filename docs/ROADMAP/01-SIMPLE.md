# 01 — Простые улучшения (1-3 спринта каждое)

Проверенные паттерны, низкий риск, измеримый прирост value. Каждое можно сделать за 1-3 спринта на основе уже существующих primitives.

**Документ:** часть серии ROADMAP. См. также: [00-CURRENT-STATE](./00-CURRENT-STATE.md), [02-MEDIUM](./02-MEDIUM.md), [03-INNOVATIVE](./03-INNOVATIVE.md), [04-NOVEL](./04-NOVEL.md), [05-PRIORITIES](./05-PRIORITIES.md).

---

## S1. Saved searches + alerts

### Концепция
Пользователь сохраняет частый запрос (например, «новые упоминания AgentFS»). Система периодически (или при ingest нового документа) пересчитывает результаты, и при изменениях dispatch'ит webhook / email / event.

### Зачем
- Пассивная информированность — не нужно вручную перепроверять
- Раннее обнаружение появления релевантного контента
- Основа для recommendation engine

### Существующие primitives
- `webhooks/` (Sprint 52) — диспетчер с retry/HMAC/DLQ
- `events/` (Sprint 37) — pub-sub для триггеров
- `jobs/` — для cron-like запусков
- `passage_retrieval` (BM25) — быстрый поиск

### Этапы реализации (2 спринта)

**Спринт A:**
- `docstoolkit/alerts/` модуль
- `SavedQuery` dataclass: id, query, retriever_config, last_results_hash, owner, schedule_cron
- `AlertStore` (SQLite): saved_queries + alerts таблицы
- CLI: `lorenzo alert create --query "X" --schedule daily`

**Спринт B:**
- `AlertRunner.tick()`: пересчитывает все due queries, сравнивает hash результатов
- При изменении: dispatch event `alert.fired` с diff (added/removed passages)
- Webhook subscription интеграция через events bus
- Email-channel опц. (через SMTP stdlib)

### API sketch

```python
@dataclass
class SavedQuery:
    id: str
    owner: str
    query: str
    retriever_config: dict
    schedule: str = "daily"           # cron-like or "on_ingest"
    last_run_ts: str = ""
    last_results_hash: str = ""

class AlertStore:
    def save(self, q: SavedQuery) -> str
    def list_due(self) -> list[SavedQuery]
    def update_after_run(self, qid: str, results_hash: str) -> None

class AlertRunner:
    def tick(self) -> list[FiredAlert]    # запускается периодически
```

### Метрики успеха
- Время от появления нового документа до alert: <60 сек (для on_ingest)
- False positive rate (фейковые «изменения» из-за нестабильного ranking): <5%
- Coverage: 80% saved queries проверяются по расписанию

### Риски
- Шумные queries → alert fatigue. Решение: cooldown-период между алертами
- Heavy queries замедляют систему. Решение: priority queue, лимиты per-owner

---

## S2. Faceted search UI в serve.py

### Концепция
HTML-страница `/search` с полем запроса + фасетные фильтры (author, section, date, language, tags). Уже есть `improve_faceted_search.py` — нужно поднять как HTTP-эндпоинт.

### Зачем
- Переход от CLI-only к юзабельному web UI
- Снижает порог входа для нетехнических пользователей
- Видимость для демо/презентаций

### Существующие primitives
- `serve.py` — HTTP сервер с роутингом
- `improve_faceted_search.py` — логика фильтров готова
- `improve_keyword_index.py` — инвертированный индекс
- `improve_named_entity_index.py` — entities для тегов

### Этапы реализации (2-3 спринта)

**Спринт A:** Backend
- Endpoint `GET /search?q=...&author=X&section=Y&from_date=Z`
- Endpoint `GET /facets` — возвращает available filter values
- JSON response: `{results: [...], facets: {...counts...}, total: N}`

**Спринт B:** Frontend (no-build стек)
- HTML+CSS+vanilla-JS в `static/search.html`
- Серверный рендеринг template via stdlib `string.Template` или Jinja2 (опционально)
- Реактивные фасеты: чекбоксы → query rebuild → fetch → re-render

**Спринт C (опц.):** Polish
- Highlight matched terms в snippet
- Pagination
- Permalinks (state в URL)
- Dark mode

### API sketch

```python
# в serve.py
@route("/search")
def search_endpoint(request):
    query = request.params.get("q", "")
    filters = {k: v for k, v in request.params.items() if k != "q"}
    results = faceted_search(query, **filters)
    facets = compute_facets(results)
    return json_response({"results": results, "facets": facets})
```

### Метрики успеха
- Time-to-first-result: <500ms на 500-документном корпусе
- UI usable на mobile (responsive)
- Coverage: 100% типов фильтров, что есть в `improve_faceted_search.py`

### Риски
- XSS при подсветке. Решение: HTML escaping всего user input
- Performance на больших корпусах. Решение: pagination + LIMIT в SQL

---

## S3. Document classification (auto-routing)

### Концепция
Новый документ автоматически классифицируется в одну из подпапок (01-svyazi, 02-anthropic-vacancies, ...) на основе TF-IDF центроидов существующих документов в каждой категории.

### Зачем
- Снижает manual organization labour
- Выявляет когда документ не вписывается ни в одну категорию (потенциально новая тема)
- Основа для recommendation: «если интересен этот, посмотри также эти из той же категории»

### Существующие primitives
- `improve_topic_model.py` — TF-IDF кластеризация уже есть
- `improve_cross_section.py` — связи между секциями
- `frontmatter` — категория хранится в YAML header

### Этапы реализации (1-2 спринта)

**Спринт A:**
- `docstoolkit/classifier/` модуль
- Compute centroids: для каждой подпапки → mean TF-IDF vector
- `classify(doc_text) → list[(section, score)]`
- CLI: `lorenzo classify path/to/new.md`
- Pre-commit hook опц.: warn если документ в неправильной секции

### API sketch

```python
@dataclass
class ClassificationResult:
    suggested_section: str
    confidence: float
    alternatives: list[tuple[str, float]]   # [(section, score), ...]

class TfidfClassifier:
    def fit(self, corpus: dict[str, list[str]]) -> None  # {section: [doc_texts]}
    def classify(self, text: str) -> ClassificationResult
    def explain(self, text: str) -> dict   # top contributing terms per class
```

### Метрики успеха
- Accuracy на existing corpus (re-classify and check): ≥80%
- Time-to-classify: <100ms per doc
- Confidence distribution interpretable: top-1 vs top-2 gap correlates with correctness

### Риски
- Cold-start: пустые секции имеют слабые центроиды. Решение: minimum-document threshold
- Concept drift: со временем категории смещаются. Решение: периодическая переtraining

---

## S4. Citation graph + PageRank

### Концепция
Документы ссылаются друг на друга через `[[wikilinks]]` или markdown `[text](path.md)`. Построить ориентированный граф, посчитать PageRank → влияние документа в корпусе.

### Зачем
- Identify центральные документы (которые многие читают/цитируют)
- Обнаружить «orphan» документы (никто не ссылается)
- Использовать в ranking: PageRank-boost для retrieval

### Существующие primitives
- `improve_crosslink_all.py` — извлечение ссылок
- `improve_concept_graph.py` — graph builder с DOT/Mermaid output
- `improve_backlinks.py` — обратные связи

### Этапы реализации (1 спринт)

- `docstoolkit/citations/` модуль
- `build_citation_graph(corpus_dir) → dict[doc_id, list[doc_id]]`
- `pagerank(graph, alpha=0.85, iterations=50) → dict[doc_id, score]`
- Output: `docs/CITATION_PAGERANK.md` с топ-20 + orphan list
- Опц.: интеграция в retriever как boost factor

### API sketch

```python
def build_citation_graph(corpus: Path) -> dict[str, list[str]]
def pagerank(graph: dict, alpha: float = 0.85, iterations: int = 50) -> dict[str, float]
def detect_orphans(graph: dict) -> list[str]
def detect_authorities(graph: dict, top_k: int = 10) -> list[tuple[str, float]]
```

### Метрики успеха
- Convergence: ≤50 iterations с epsilon=1e-6
- Top-10 PageRank docs visually interpretable как центральные
- Сoverage: 100% документов в графе (даже изолированные nodes)

### Риски
- Много self-citations (один документ ссылается сам на себя через TOC). Решение: фильтр в pre-processing
- Cycles при `crosslink_all` могут создать loop. Решение: PageRank сам устойчив к cycles

---

## S5. Bulk diff queries

### Концепция
«Что изменилось между набором A и набором B документов» — фасетный compare. Например: «новые проекты в `05-habr-projects/` за последний месяц vs квартал назад».

### Зачем
- Tracking прогресса research/curation work
- Periodic reports: «что нового на этой неделе»
- Onboarding: «вот ключевые изменения за время вашего отсутствия»

### Существующие primitives
- `improve_version_diff.py` — git-based семантический diff (Sprint 33)
- `improve_changelog_auto.py` — генерация changelog
- `timetravel/` — query at commit
- `digest_auto.py` — авто-дайджест за N дней

### Этапы реализации (1-2 спринта)

**Спринт A:** Расширение существующих
- `docstoolkit/diff/` модуль (extract из scripts)
- `BulkDiff(set_a, set_b)`: added / removed / modified / renamed
- Per-doc diff: structural (headings) + semantic (TF-IDF cosine of content)
- Markdown report: aggregated stats + per-doc details

**Спринт B:** Query interface
- `lorenzo diff --since 2026-01-01 --section 05-habr-projects`
- `lorenzo diff --commit-a HASH1 --commit-b HASH2`
- JSON output для интеграций

### API sketch

```python
@dataclass
class DocDiff:
    path: str
    change: str                # added | removed | modified | renamed
    headings_added: list[str]
    headings_removed: list[str]
    semantic_similarity: float  # 0-1, cosine
    line_changes: tuple[int, int]  # (added, removed)

@dataclass
class BulkDiffResult:
    added: list[DocDiff]
    removed: list[DocDiff]
    modified: list[DocDiff]
    summary: str
```

### Метрики успеха
- Время на 500-доковом diff: <10 сек
- Semantic similarity точность: human review соглашается на >80% «modified» классификаций

### Риски
- Renamed detection ложно-положительные. Решение: similarity threshold (≥0.7)
- Большие моменты в commit history замедляют. Решение: кеш per-commit fingerprint

---

## S6. Per-user preferences profile

### Концепция
Пользователь имеет JSON-профиль: preferred retriever, default top_k, preferred answerer, language, skill aliases. Все RAG-вызовы используют профиль если параметры не переопределены.

### Зачем
- Снижение friction (не нужно каждый раз указывать `--method hybrid --top-k 10`)
- Основа для personalization (S6 → дальнейшие рекомендации в M-блоке)
- Multi-tenant readiness

### Существующие primitives
- `auth/` (Sprint 39) — User-объект
- `config.py` — load_config с YAML/env
- `feedback/` — per-skill quality scores

### Этапы реализации (1 спринт)

- `docstoolkit/profile/` модуль
- `UserProfile` dataclass: stored в `~/.docstoolkit/profile.json` или `.docstoolkit/users/{id}.json`
- `load_profile(user_id) → UserProfile`
- `apply_profile(profile, kwargs) → kwargs` — defaults overlay
- Интеграция в `rag.ask`, `agent.run`, CLI: `--user X` или env `DOCSTOOLKIT_USER`

### API sketch

```python
@dataclass
class UserProfile:
    id: str
    name: str = ""
    default_method: str = "hybrid"
    default_top_k: int = 5
    default_answerer: str = "echo"
    default_model: str = ""
    language: str = "ru"
    skill_aliases: dict = field(default_factory=dict)  # {alias: skill_id}
    metadata: dict = field(default_factory=dict)

def load_profile(user_id: str, base: Path | None = None) -> UserProfile
def apply_profile(profile: UserProfile, kwargs: dict) -> dict
```

### Метрики успеха
- 100% RAG/agent calls используют profile defaults если не override
- Profile loading: <5ms
- Survives roundtrip (save/load)

### Риски
- Forgetting to apply в новых endpoints. Решение: middleware в serve.py
- Conflict с explicit args. Решение: explicit > profile > global default

---

## S7. Read-receipt + reading time tracking

### Концепция
Пользователь отмечает «прочитано» для документа. Система запоминает + использует для рекомендаций и personalized search re-ranking.

### Зачем
- Персональный «inbox» / «backlog» для непрочитанного
- Recommendations «вы прочитали X, попробуйте Y»
- Не показывать уже прочитанное в saved searches

### Существующие primitives
- `improve_reading_time.py` — оценка времени чтения (200 wpm RU)
- `feedback/` — pattern для user-state tracking
- `profile/` (S6) — per-user state

### Этапы реализации (1 спринт)

- `docstoolkit/reads/` модуль
- SQLite таблица: user, doc_id, status (unread/read/skipped/saved), ts
- `mark_read(user, doc_id)`, `list_unread(user)`, `recommendations_for(user)`
- Простые рекомендации: ближайшие documents в citation graph + cross-section concepts
- CLI: `lorenzo read --mark-read path.md`, `lorenzo recommend`

### API sketch

```python
class ReadStore:
    def mark_read(self, user: str, doc_id: str) -> None
    def list_unread(self, user: str, section: str = "") -> list[str]
    def reading_history(self, user: str, limit: int = 50) -> list[dict]

def recommendations_for(user: str, top_k: int = 10) -> list[tuple[str, float, str]]
    """returns [(doc_id, score, reason), ...]"""
```

### Метрики успеха
- Recommendation relevance: human review «good» на ≥60%
- Storage: <100KB per user для 500-доков корпуса
- Сoverage: tracking всех documents в `docs/`

### Риски
- Privacy concerns в multi-tenant. Решение: per-user database file
- Cold start для новых users. Решение: использовать popular docs как defaults

---

## Сводная таблица

| ID | Название | Спринтов | Сложность | Влияние |
|----|----------|---------:|-----------|---------|
| S1 | Saved searches + alerts | 2 | Low | Medium |
| S2 | Faceted search UI | 2-3 | Low | High (visibility) |
| S3 | Document classification | 1-2 | Low | Medium |
| S4 | Citation graph + PageRank | 1 | Low | Medium |
| S5 | Bulk diff queries | 1-2 | Low | Low |
| S6 | Per-user preferences | 1 | Low | Low (foundation) |
| S7 | Read-receipt + reads tracking | 1 | Low | Low |

**Общий бюджет:** ~10-13 спринтов на все 7. **Совокупный эффект:** превращает Lorenzo из CLI tool в multi-user knowledge platform с базовой персонализацией.

---

## Order of implementation (рекомендуемый)

1. **S6** (per-user preferences) — foundation для всего остального
2. **S2** (faceted UI) — даёт visibility, демо для других
3. **S4** (PageRank) — quick win для retrieval quality
4. **S7** (reads tracking) — нужен профиль из S6
5. **S1** (saved searches) — нужны webhooks (есть) + reads (S7)
6. **S3** (classification) — utility, не блокирует
7. **S5** (bulk diff) — nice-to-have, можно отложить
