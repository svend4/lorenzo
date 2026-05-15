# `docs-toolkit` — Development Status & Forward Roadmap

> Версия документа: **2026-05-15**, ветка `claude/continue-development-BrDvi`,
> HEAD = `6c33cbe5`.
> Документ описывает текущее состояние реализации и пошаговый план развития.
> Технические детали (файлы, сигнатуры, тесты, exit-критерии) приведены для
> каждого этапа.

---

## 0. TL;DR

| Метрика | Значение |
|---|---|
| Модулей в `docstoolkit/` | **498** Python-пакетов |
| Тестовых файлов | **538** (`tests/test_*.py`) |
| Строк production-кода | **~169 000** (`find docstoolkit -name "*.py" \| xargs wc -l`) |
| Версия пакета (`pyproject.toml`) | `0.1.0` |
| Версия в `CHANGELOG.md` | `0.3.0` (в `[Unreleased]`, к релизу) |
| Roadmap coverage | **35 / 35** пунктов (Path A/B/C) |
| `ask()` kwargs | **17 ортогональных** |
| Named presets | **6** (`docstoolkit.rag.presets`) |
| Standalone helpers | **18** (advanced/saved/bulk_diff/bandit_ask) |
| Composition demos | **8** скриптов в `examples/composition/` |
| Bench suites | **8** (frontmatter, embeddings, search, graph, jobs, cluster, **ask_features**, **helpers**) |
| Bench overhead | `ask_baseline` ≈ **40 μs**; самая дорогая фича — `with_negotiation` (+107 μs) |

---

## 1. Что реализовано — детальная карта

### 1.1. Архитектурный фундамент (версия 0.1.0)

| Подсистема | Модуль | Что предоставляет |
|---|---|---|
| Конфиг | `config.py`, `config_mgmt`, `config_store` | `Config`, `load_config()`, layered settings, hot-reload, TOML/JSON Schema валидация |
| Контракт документа | `frontmatter.py`, `core.py` | `extract_frontmatter()`, `write_doc()`, frontmatter-валидация по JSON Schema |
| Plugin discovery | `plugins.py`, `plugin_system`, `plugin_sandbox` | PEP 621 entry-points, изолированный sandbox |
| CLI | `cli.py` | `init`, `doc new/validate/list-templates`, `ingest`, `serve`, `doctor`, `search`, `plugins list/inspect`, `index build/update/clear/stats`, `skills list/test` |
| HTTP-сервер | `serve.py`, `web` | FastAPI с эндпоинтами для RAG, eval, saved, voice, assets, taxonomy, diff, KG, profile |
| Embeddings | `embeddings/`, `embedding_store` | `TFIDFProvider` (stdlib), `SentenceTransformersProvider` (опц.), SQLite cache, IDF-инвалидация |
| Ingest | `ingest/` | markdown, html, mhtml, jupyter (stdlib); pdf/epub/docx (опц.); web: url, arxiv, hackernews, habr |
| Search | `hybrid_search`, `search_engine`, `search_index_mgr` | RRF + weighted fusion, инкрементальный индекс |

### 1.2. RAG Composition Surface — `docstoolkit.rag`

**Файлы** (`wc -l docstoolkit/rag/*.py`):

```
adaptive.py      184    multi-hop с confidence threshold
advanced.py      374    standalone helpers (probe_counterfactual, measure_voice, …)
answerer.py      239    EchoAnswerer / AnthropicAnswerer / OpenAIAnswerer / OllamaAnswerer
assembler.py      56    промпт-шаблон с цитатами
bandit_ask.py     75    ask_with_bandit(exp, variants) — multi-armed bandit A/B
bulk_diff.py      88    diff_corpus_dirs() / diff_commits() / diff_since_days()
clarifier.py     168    detect_ambiguity / build_clarification / ClarifyingRAG
counterfactual.py 241   attribute_answer / counterfactual_ask / ForensicRAG
facets.py        184    aggregate_facets() + apply_filters()
hierarchical.py  359    SectionIndex / DocIndex / hierarchical_search()
mapreduce.py     216    map_reduce_ask() для long-context
pipeline.py      533    ask() + RAGPipeline (центральная точка композиции)
presets.py       153    6 именованных бандлов (новое в 6c33cbe5)
retriever.py      87    Retriever + retrieve_passages()
saved.py          98    save_query() + run_due_alerts() (саге́ы и cron-алёрты)
streaming.py     212    SSE-стриминг ответа
synthesis.py     222    synthesize / compare_sections (cross-doc)
types.py          62    Passage / AnswerResult / RAGQuery (датаклассы)
```

**Композиция через единый `ask()` — 17 ортогональных kwargs:**

| Kwarg | Sprint | ID | Что делает |
|---|---|---|---|
| `user_id`, `profile` | 54 | S6 | Per-user preferences (`ProfileStore` → SQLite) |
| `eval_runner` | 56 | M5 | Continuous online eval (`OnlineEvalRunner` сэмплирует) |
| `reranker` | 59 | M2 | Cross-encoder rerank (TF-IDF / BGE / LLM-judge / noop), берёт `top_k*3` |
| auto | 60 | S7 | Read-receipts (auto-mark при `user_id`) |
| `filters`, `with_facets`, `facet_fields` | 55 | S2 | Фасет-агрегация + фильтрация |
| `with_provenance` | 61-65 | I3 | Claim-extraction + source linking + bootstrap CI |
| `self_rag`, `self_rag_max_iters`, `self_rag_threshold` | 70-74 | I1 | Reflect-loop с decision tokens |
| `hierarchical` | 67 | M3 | SectionIndex → DocIndex → passage-level |
| `auto_intent` | 68 | M4 | `IntentRouter` → подбор retriever/top_k/hierarchical |
| `at_commit` | 79 | I8 | Time-travel: rebind corpus к историческому commit |
| `with_debate`, `debate_personas`, `debate_max_rounds` | 72 | I2 | Multi-agent debate с агрегацией ответов |
| `with_got`, `got_max_hypotheses` | 75 | N3 | Graph-of-thoughts: гипотезы + confirm/refute |
| `with_mapreduce`, `mapreduce_chunk_size` | 78 | I10 | Long-context map-reduce синтез |
| `with_negotiation`, `negotiation_budget` | 85 | N2 | Аукцион 5 агентов за пассажи |
| `personality` | 89 | N9 | `CognitiveProfile` rerank (skepticism / synthesis / …) |
| `learning_queue` | 73 | M6 | Auto-enqueue в active-learning очередь |
| `memory`, `memory_top_k` | 74 | I5 | `TieredMemory` (MemGPT-style) |
| `fusion` | 91 | I6 | Learned fusion adapter |

**Standalone helpers (18) — в `rag/advanced.py`, `rag/saved.py`, `rag/bulk_diff.py`, `rag/bandit_ask.py`:**

```
# rag/advanced.py
probe_counterfactual(question, corpus, doc_id)  → severity, affected   # I4
measure_voice(text)  → {claim_ratio, hedge_ratio, …}                   # N4
diffuse_knowledge(src_corpus, tgt_corpus, threshold)                   # N6
build_taxonomy_ask(corpus)                                              # N7
search_assets(query, mode="text|image")                                 # M8
co_evolve_seeds(seeds, generations)                                    # S3 extension
incremental_index_docs(paths)                                          # M7
classify_docs(paths)                                                   # S3
federated_aggregate(local_metrics, epsilon)                            # N5

# rag/saved.py
save_query(name, query, schedule_cron, alert_threshold)                # S1
run_due_alerts(store) → fired alerts                                   # S1

# rag/bulk_diff.py
diff_corpus_dirs(a, b)                                                 # S5
diff_commits(repo, sha_a, sha_b)                                       # S5
diff_since_days(repo, days)                                            # S5

# rag/bandit_ask.py
ask_with_bandit(query, exp, variants)                                  # I7
evaluate_record(exp, picked, result, success_threshold)                # I7

# Path C heavy
propose_rewrite(doc_id, content, sources, last_modified_iso)           # N1
rank_stale_documents(docs, threshold_days)                             # N1
evolve_prompt(seeds, fitness_fn, generations)                          # I9
```

### 1.3. Named presets (`docstoolkit/rag/presets.py`, 6c33cbe5)

```
ask_personalized(q, user_id, **kw)       → S6 + S7
ask_high_quality(q, *, reranker=None)    → M2 + I3
ask_with_reasoning(q, **kw)              → N3 + I2 (без self-RAG — конфликт)
ask_advanced(q, **kw)                    → M3 + M4 + I10
ask_research(q, *, memory=None, personality=None) → N2 + N9 + I5
ask_full_stack(q, *, user_id="", memory=None, personality=None, reranker=None)
                                          → 14 совместимых фич одновременно
```

Каждый пресет — тонкая обёртка через `setdefault`, поэтому caller-supplied
kwarg всегда побеждает дефолт.

### 1.4. Composition examples (8 demo-скриптов)

| Файл | Демонстрирует |
|---|---|
| `examples/composition/01_minimal.py` | Baseline single-call RAG |
| `examples/composition/02_personalize.py` | S6 + S7 |
| `examples/composition/03_quality.py` | M2 + I3 + M5 |
| `examples/composition/04_reasoning.py` | I1 + N3 + I2 |
| `examples/composition/05_advanced.py` | M3 + M4 + I10 + I8 |
| `examples/composition/06_path_C.py` | N2 + N9 + I5 + N1 |
| `examples/composition/07_standalone.py` | Helpers: bandit, voice, taxonomy, bulk diff, counterfactual, asset search, diffusion |
| `examples/composition/08_full_stack.py` | Все 17 фич одновременно |

Каждый скрипт self-contained: создаёт in-memory corpus, патчит `Retriever`/`Answerer`,
печатает результат. Запускаются offline.

### 1.5. Benchmark infrastructure

**`bench/runner.py`** — runner + history + regression-check (533 строки).

**Suites:** `frontmatter`, `embeddings`, `search`, `graph`, `jobs`, `cluster`,
`ask_features` (10 бенчей), `helpers` (3 бенча).

**Результаты замеров на stubbed Retriever+Answerer (см. `bench/BENCHMARKS.md`):**

| Bench | Median | Delta vs baseline |
|---|---:|---:|
| `ask_baseline` | 0.043 ms | — |
| `ask_with_facets` | 0.077 ms | +34 μs |
| `ask_with_provenance` | 0.052 ms | +9 μs |
| `ask_rerank_tfidf` | 0.098 ms | +55 μs |
| `ask_self_rag` (2 iters) | 0.120 ms | +77 μs |
| `ask_with_debate` (1 round) | 0.092 ms | +49 μs |
| `ask_with_got` (3 hyp) | 0.085 ms | +42 μs |
| `ask_with_mapreduce` | 0.062 ms | +19 μs |
| `ask_with_negotiation` | 0.150 ms | +107 μs |
| `ask_compose_5` | 0.337 ms | +294 μs |

`ask_compose_5` (baseline + facets + provenance + rerank + self_rag + got)
демонстрирует sub-linear composition overhead — общий cost ниже суммы
индивидуальных вкладов (~50 μs shared overhead).

**CI integration:** `.github/workflows/benchmark.yml` запускает все suites
на push/PR, сохраняет JSON артефакт, и (на PR) сравнивает с baseline
с порогом 50% регрессии.

### 1.6. Известные технические ограничения

1. **`self_rag` ⊥ `with_got` / `with_debate` / `with_negotiation`** — `_self_rag_run` в `pipeline.py:21` имеет собственный цикл и не пробрасывает эти флаги. Поэтому пресеты `ask_with_reasoning` и `ask_full_stack` сознательно не включают self-RAG по умолчанию.
2. **Version mismatch:** `pyproject.toml` v0.1.0 vs `CHANGELOG.md` `[Unreleased]` под версией 0.3.0. Bump запланирован.
3. **`bench/history.jsonl` пуст** — baseline для PR regression-check появится после первого push в main.

---

## 2. Дорожная карта — фазы развития

Карта построена по принципу **«сначала консолидация, потом расширение»**:
сначала фиксируем поверхность API и стабилизируем pipeline, затем
устраняем технический долг, далее расширяем функциональность.

Каждая фаза — это _набор связных коммитов_, не календарный спринт.
Указан **порядок зависимостей**, **точки интеграции**, **тесты**, **DoD**.

### Условные обозначения

- 📦 — новый модуль / файл
- 🔧 — изменение существующего файла
- 🧪 — тестовый артефакт
- 📝 — документация
- ⚡ — performance / cost
- 🚦 — gating CI / релизные ворота

---

## Фаза I — Релизная консолидация (1-2 коммита)

**Цель:** перевести ветку из «build-out» режима в «release-ready». Никаких
новых фич — только синхронизация версий, документации, гарантия что
полный `pytest` зелёный.

### I.1 — Version bump до 0.3.0

- 🔧 `pyproject.toml` — `version = "0.3.0"`
- 🔧 `docstoolkit/__init__.py` — добавить `__version__ = "0.3.0"` (если ещё нет)
- 🔧 `CHANGELOG.md` — переместить блок `[Unreleased]` в `[0.3.0] — 2026-05-15`,
  завести пустой `[Unreleased]`
- 🔧 `README.md` строка статуса — обновить версию
- 🧪 `tests/test_version.py` — smoke-тест на чтение `__version__`

**Exit criteria:** `python -c "import docstoolkit; print(docstoolkit.__version__)"`
печатает `0.3.0`. CHANGELOG соответствует Keep-a-Changelog.

### I.2 — Полный pytest baseline + perf budget

- 🚦 Запустить `pytest -q --durations=20` локально, зафиксировать число
  passing/failing/skipped и top-20 самых медленных
- 📝 `docs-toolkit/TEST_BASELINE.md` — таблица с числом тестов и общим временем
- 🔧 `.github/workflows/test.yml` — если общий runtime > 5 минут, добавить
  `pytest -n auto` (xdist) или маркеры `slow`

**Exit criteria:** все тесты зелёные на CI, общий runtime < 5 минут.

### I.3 — Бенчмарк baseline в репо

- 🔧 Сделать ручной `python -m bench.runner --save` на main после merge
- 🔧 Закоммитить `bench/history.jsonl` (1 запись)
- 📝 `bench/BENCHMARKS.md` — пометить baseline-запись

**Exit criteria:** CI PR-regression-check теперь имеет с чем сравнивать.

---

## Фаза II — Pipeline cleanup (3-4 коммита)

**Цель:** устранить ключевое архитектурное ограничение — взаимная
исключительность `self_rag` и `with_got` / `with_debate` /
`with_negotiation` — и упростить `pipeline.py`.

### II.1 — Decompose `_self_rag_run` в pipeline-stage

**Проблема:** `_self_rag_run` в `pipeline.py:21-67` — это _параллельная
вторая реализация_ pipeline-loop'а, которая не пробрасывает reasoning-флаги.
Из-за этого пресет `ask_with_reasoning` вынужден исключить self-RAG.

**План:**

- 🔧 `docstoolkit/rag/pipeline.py` — превратить self-RAG в **post-processing stage**:
  - `RAGPipeline.run()` возвращает первый ответ
  - Если `self_rag=True`, вызывается `_self_rag_reflect_step(result, pipeline)` который дёргает `pipeline` повторно с уточнённым запросом
  - GoT / debate / negotiation остаются в `RAGPipeline.run()` и работают на каждой итерации
- 📦 `docstoolkit/rag/_stages.py` (вынести вспомогательные функции этапов)
- 🧪 `tests/test_self_rag_with_reasoning.py` — кейс `self_rag=True, with_got=True` → result.got_result != None
- 🧪 `tests/test_self_rag_isolated.py` — обратная совместимость: одиночный self_rag работает как раньше

**Точка интеграции:** `ask()` уже принимает все эти kwargs, изменения
полностью прозрачны для caller.

**Exit criteria:** `ask(self_rag=True, with_got=True).got_result is not None`,
без регрессий в существующих self_rag тестах.

### II.2 — Обновить `ask_with_reasoning` и `ask_full_stack` пресеты

- 🔧 `docstoolkit/rag/presets.py` — включить `self_rag=True` обратно в оба пресета
- 🔧 `PROFILES.md` — убрать «Note: self_rag short-circuits…»
- 🔧 `docstoolkit/rag/presets.py` docstrings — обновить
- 🧪 `tests/test_rag_presets.py` — добавить кейс `ask_with_reasoning()` → self_rag-trace И got_result

**Exit criteria:** оба пресета используют все три механизма reasoning одновременно.

### II.3 — Унифицировать сборку `AnswerResult`

**Проблема:** разные ветки в `ask()` (hierarchical / time-travel / self-RAG)
строят `AnswerResult` руками, что повышает риск пропустить новое поле.

- 🔧 `docstoolkit/rag/pipeline.py` — экстрактнуть `_finalize_answer_result()` helper
- 🧪 `tests/test_answer_result_fields.py` — round-trip всех полей через каждую ветку

**Exit criteria:** все ветки `ask()` проходят через единый finalization-helper.

### II.4 — `RAGPipeline` параметры → dataclass

**Проблема:** `RAGPipeline.__init__` имеет 18 параметров, что хрупко.

- 📦 `docstoolkit/rag/_config.py` — `@dataclass(frozen=True) class PipelineConfig`
- 🔧 `RAGPipeline.__init__(query, config: PipelineConfig)`
- 🔧 `ask()` строит `PipelineConfig` из kwargs (обратная совместимость 100%)
- 🧪 `tests/test_pipeline_config.py`

**Exit criteria:** публичный `ask()` API без изменений, внутри — type-safe конфиг.

---

## Фаза III — Quality observability (2-3 коммита)

**Цель:** дать пользователю инструменты увидеть _что произошло_ внутри
композиции, не просто финальный ответ.

### III.1 — `AnswerResult.trace` поле

- 🔧 `docstoolkit/rag/types.py` — добавить `trace: list[TraceEvent]`
- 📦 `docstoolkit/rag/_trace.py` — `TraceEvent(stage, t_ms, payload)`
- 🔧 `RAGPipeline.run()` — emit events на каждой стадии (retrieve/filter/rerank/synthesize/…)
- 🔧 `_self_rag_run` (или новый stage из II.1) — emit reflect-iter events
- 🧪 `tests/test_trace.py` — порядок стадий, payload-shape

**Exit criteria:** `result.trace` непустой, события упорядочены по `t_ms`,
сумма стадий примерно совпадает с `result.duration_ms`.

### III.2 — `AnswerResult.to_trace_markdown()`

- 🔧 `docstoolkit/rag/types.py` — рендер trace в markdown-table
- 🔧 `examples/composition/08_full_stack.py` — печатать trace в финале
- 📝 `PROFILES.md` — раздел «Inspecting composition trace»

**Exit criteria:** одной строкой `print(result.to_trace_markdown())` пользователь
видит, сколько каждая фича отъела времени.

### III.3 — `serve.py` экспорт trace в JSON

- 🔧 `docstoolkit/serve.py` — `/api/ask` ответ включает `trace` если `?trace=1`
- 🔧 OpenAPI-описание (для FastAPI auto-docs)
- 🧪 integration test через TestClient

**Exit criteria:** HTTP-клиент получает trace без изменений серверного кода
у пользователя.

---

## Фаза IV — Performance pass (2-3 коммита) ⚡

**Цель:** атаковать самую дорогую фичу (`with_negotiation`, +107 μs) и
снизить shared overhead композиции.

### IV.1 — Профайл `with_negotiation`

- 🚦 Запустить `python -m cProfile -o /tmp/neg.prof -c "..."` на 1000-итер. цикле
- 📝 `bench/PROFILING.md` — top-10 hot spots с интерпретацией
- 🔧 Возможные направления:
  - кешировать TF-IDF фичи `Passage` между агентами (сейчас, вероятно, пересчитывается)
  - сократить число агентов с 5 до 3 для `negotiation_budget < 3`
  - `auction` без полного перебора при ясном фаворите

**Exit criteria:** `with_negotiation` overhead ≤ 70 μs (-35%) без потери
качества (golden-set метрика не падает > 2%).

### IV.2 — Shared retrieval cache внутри pipeline

**Проблема:** debate/GoT могут повторно запрашивать одни и те же пассажи.

- 📦 `docstoolkit/rag/_retrieval_cache.py` — LRU кеш `(query_hash, top_k) → passages`
  с TTL на длительность одного `ask()` вызова
- 🔧 `RAGPipeline.run()` — обернуть `retriever.search` в кеш
- 🧪 `tests/test_retrieval_cache.py` — проверка одного вызова retrieve при N агентах
- ⚡ Bench update: ожидаем `ask_compose_5` падает с ~300 μs до ~220 μs

**Exit criteria:** число вызовов `Retriever.search` в полной композиции ≤ 2
(вместо текущих 5+).

### IV.3 — Lazy provenance

**Проблема:** `with_provenance=True` стоит +9 μs всегда, даже когда никто
не запрашивает provenance.

- 🔧 `docstoolkit/rag/pipeline.py` — `provenance` строится в `AnswerResult.__post_init__`
  только при первом обращении (либо `compute_now=True` явно)
- 🧪 `tests/test_lazy_provenance.py`

**Exit criteria:** `ask(with_provenance=True)` без обращения к `.provenance`
имеет overhead ≤ 2 μs.

---

## Фаза V — Расширение Path C — Knowledge Graph deepening (4-6 коммитов)

**Цель:** довести `knowledge_graph` модуль до production-readiness и
интегрировать в основной pipeline.

### V.1 — KG persistence layer

- 🔧 `docstoolkit/knowledge_graph/store.py` — SQLite-backed `TripleStore`
  - schema: `subject, predicate, object, doc_id, span, score, ts`
  - индексы по `subject`, `object`, `predicate`
- 🧪 `tests/test_kg_store.py`

### V.2 — KG-driven retriever

- 📦 `docstoolkit/rag/kg_retriever.py` — `KGRetriever` который:
  1. Извлекает entities из запроса
  2. Делает 1-2-hop expansion по графу
  3. Превращает соседние документы в boost-scores для базового retrieval
- 🔧 `RAGPipeline` — новый `kg_boost` kwarg
- 🧪 `tests/test_kg_retriever.py` — golden recall@10 повышение

### V.3 — KG query DSL

- 📦 `docstoolkit/knowledge_graph/query.py` — мини-язык
  ```
  ?x -[author]-> "Alice", ?x -[mentions]-> ?topic, ?topic.tag = "memory"
  ```
- 🧪 `tests/test_kg_query.py`

### V.4 — Bench suite `kg`

- 🔧 `bench/runner.py` — `_suite_kg()` с 4-5 бенчами
- 🔧 `bench/BENCHMARKS.md` — новый раздел

**Exit criteria:** `ask(kg_boost=True)` повышает recall@5 на golden-set
не менее чем на 5%; KG overhead ≤ 200 μs на запрос.

---

## Фаза VI — Federation Sprint 105-116 — реальная реализация (5+ коммитов)

**Цель:** перевести `federated_eval` модуль из stub-состояния в работающий
сценарий с дифференциальной приватностью.

### VI.1 — DP foundations

- 🔧 `docstoolkit/federated_eval/dp.py` — реализация Laplace + Gaussian noise
  с параметром `epsilon`
- 🧪 `tests/test_dp_noise.py` — Hoeffding-bound на отклонение

### VI.2 — Secure aggregation

- 📦 `docstoolkit/federated_eval/aggregate.py` — secure sum с masking shares
  (без полного MPC — простой semi-honest protocol)
- 🧪 `tests/test_secure_aggregate.py`

### VI.3 — NPP federation интеграция

- 🔧 `docstoolkit/federation/npp.py` — endpoints `/npp/eval/contribute`,
  `/npp/eval/aggregate`
- 🧪 `tests/test_federation_npp.py` — N-node simulation

**Exit criteria:** 3-node simulation выдаёт корректный (±ε) средний P/R/F1
без раскрытия per-node данных.

---

## Фаза VII — Plugin marketplace surface (3-4 коммита)

**Цель:** превратить `plugin_system` в реальный публикуемый интерфейс.

### VII.1 — Standard plugin contract

- 📝 `docs-toolkit/PLUGIN_CONTRACT.md` — спецификация: entry-points,
  обязательные методы (`name`, `version`, `register`), capability flags
- 📦 `examples/example-plugin-pack/` — уже существует, добавить minimal-plugin

### VII.2 — Plugin sandbox hardening

- 🔧 `docstoolkit/plugin_sandbox/` — ограничения по subprocess / network / fs
- 🧪 `tests/test_plugin_sandbox.py` — verify denied capabilities

### VII.3 — Marketplace index

- 📦 `docstoolkit/plugins/registry.py` — `discover_remote(url)`,
  установка через `pip install <plugin>` + автоматическая активация

**Exit criteria:** третий пакет можно установить и активировать без правок
кода `docs-toolkit`.

---

## Фаза VIII — Production deployment patterns (2-3 коммита)

**Цель:** дать готовые рецепты деплоя.

### VIII.1 — Docker images

- 🔧 `Dockerfile` — multi-stage build с pinned deps
- 🔧 `Dockerfile.bge` — pre-downloads `BAAI/bge-reranker-base` (упоминался в roadmap, не реализован)
- 🔧 CI: workflow для публикации в GHCR

### VIII.2 — Helm chart

- 📦 `deploy/helm/docs-toolkit/` — values для serve.py + Postgres + Redis
- 📝 `deploy/README.md` — quickstart

### VIII.3 — OpenAI-compatible gateway

- 🔧 `docstoolkit/serve.py` — `/v1/chat/completions` (уже частично есть в Lorenzo gateway.py, портировать)
- 🧪 integration test с `openai` SDK как клиент

**Exit criteria:** `docker run docs-toolkit serve` поднимает рабочий
OpenAI-compatible эндпоинт.

---

## Фаза IX — Documentation expansion (2-3 коммита) 📝

**Цель:** сделать порог входа минимальным.

### IX.1 — Cookbook

- 📦 `COOKBOOK.md` — 10 рецептов по задачам:
  - «Хочу RAG над моими markdown-файлами» → `01_minimal`
  - «Хочу проверить, что ответ опирается на источники» → `ask_high_quality` + `result.provenance`
  - «Хочу A/B протестировать retrievers» → `ask_with_bandit`
  - «Хочу обнаружить устаревшие документы» → `rank_stale_documents`
  - и т.д.

### IX.2 — Architecture deep-dive

- 📦 `ARCHITECTURE.md` — диаграмма слоёв, ADR-style решения
- Mermaid-диаграммы pipeline / federation / plugin lifecycle

### IX.3 — Migration guide

- 📦 `MIGRATING.md` — для пользователей `langchain`, `llama-index` —
  mapping API концепций

---

## 3. Карта приоритетов

```
                 │ Quick win │ Medium effort │ Big bet
─────────────────┼───────────┼───────────────┼───────────
 User-visible    │   I.1     │     III.1     │   V.1-4
 quality         │   II.1-2  │     III.2     │   VI.1-3
─────────────────┼───────────┼───────────────┼───────────
 Performance     │           │     IV.1-3    │
─────────────────┼───────────┼───────────────┼───────────
 Ops / DX        │   I.2-3   │     IX.1-3    │   VII, VIII
```

**Рекомендованная очерёдность исполнения:**

1. **Фаза I** (1-2 дня) — закрывает релиз 0.3.0
2. **Фаза II** (3-5 дней) — устраняет ключевое архитектурное ограничение
3. **Фаза III** (2-3 дня) — даёт пользователям observability
4. **Фаза IV** (2-3 дня) — performance, измеримый эффект на бенчмарках
5. Далее распараллеливаем: **V** (KG) и **IX** (docs) можно делать одновременно
6. **VI**, **VII**, **VIII** — самостоятельные большие куски, очерёдность по бизнес-приоритету

---

## 4. Risk register

| Риск | Уровень | Митигация |
|---|---|---|
| Pipeline rewrite (II.1) ломает обратную совместимость | средний | контрактные тесты на каждую ветку `ask()` до изменений |
| Performance optimization (IV) даёт регрессии по качеству | низкий | golden-set evaluation gate в CI перед merge |
| KG (Фаза V) — большой объём кода, можно растянуть | высокий | строгий cut-off по DoD каждой подфазы; merge по частям |
| Federation (Фаза VI) — DP корректность сложная | высокий | пригласить cryptography review (внешний аудит) |
| Plugin marketplace (VII) требует governance | средний | сначала private registry, потом public |

---

## 5. Метрики прогресса

Отслеживать в `bench/history.jsonl` + новом `docs-toolkit/QUALITY_HISTORY.md`:

- **Recall@5 / Recall@10** на golden-set (после Фазы V — ожидаем +5%)
- **`ask_compose_5` median** (после Фазы IV — ожидаем -25%)
- **Test count** (после Фазы II — ожидаем +30 тестов)
- **Test runtime** (поддерживать < 5 минут CI)
- **Public API surface** (`__all__` суммарно) — стабилизировать после II

---

## 6. Что НЕ делаем (явный non-goals)

- **Vector DB integration** (Pinecone/Weaviate/…) — `docs-toolkit` строго
  local-first, vector cache через SQLite остаётся каноном
- **Cloud-only features** — всё должно работать offline
- **Multi-language ports** — Python остаётся единственным SDK
- **GUI / desktop app** — серверная сторона + любой UI поверх HTTP
- **Real-time collaboration** (Yjs/CRDT) — вне scope

---

## Приложение A — Команды для воспроизведения текущего состояния

```bash
cd /home/user/lorenzo/docs-toolkit

# Smoke check
pip install -e .
python -c "from docstoolkit.rag import ask, ask_high_quality; print('OK')"

# Запуск всех демо
for f in examples/composition/0*.py; do
    echo "=== $f ==="
    python "$f"
done

# Бенчмарки
python -m bench.runner                              # все suites
python -m bench.runner --suite ask_features helpers # композиционные

# Точечные тесты
pytest tests/test_rag_presets.py -v
pytest tests/test_bench_new_suites.py -v

# Полный CI-эквивалент
pytest -q  # ~5 минут
```

---

## Приложение B — Файлы, изменённые на текущей ветке

```
docs-toolkit/
├── ROADMAP_EXECUTION.md           (новый, 7110f0d2)
├── PROFILES.md                    (новый, 461487bf, расширен 1a8bb3a2, 6c33cbe5)
├── CHANGELOG.md                   (обновлён несколько раз)
├── bench/
│   ├── runner.py                  (расширен: +ask_features, +helpers suites)
│   └── BENCHMARKS.md              (новый, ea28a6aa)
├── docstoolkit/rag/
│   ├── pipeline.py                (расширен: +все 17 ask() kwargs)
│   ├── presets.py                 (новый, 6c33cbe5)
│   ├── advanced.py                (новый: 9 helpers)
│   ├── saved.py                   (новый: S1)
│   ├── bulk_diff.py               (новый: S5)
│   ├── bandit_ask.py              (новый: I7)
│   └── ... (все 19 модулей)
├── examples/composition/          (новый каталог, 8 скриптов)
└── tests/
    ├── test_bench_new_suites.py   (новый)
    ├── test_rag_presets.py        (новый, 6c33cbe5)
    └── ... (~250 новых тестов фич)

.github/workflows/
└── benchmark.yml                  (обновлён: + ask_features, + helpers)
```

---

*Документ обновляется при закрытии каждой фазы.*
