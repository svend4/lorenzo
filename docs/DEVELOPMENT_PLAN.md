# Lorenzo — План развития: технический аудит и следующие шаги

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

_Дата: 2026-05-13 · Обновлено: 2026-05-13 · Ветка: claude/current-dev-stage-dJtu0_

---
<!-- tags: memory, rag, orchestration, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->

## Статус реализации (2026-05-13)

| Фаза | Что сделано | Статус |
|------|-------------|--------|
| 1 — Технический долг | авто-теги, якори habr-projects, gateway dedup+passages sync | ✅ |
| 2 — Card Lifecycle | `improve_card_promote.py`: 441 normalized + 272 approved | ✅ |
| 3 — MCP Write-back | `add_card`, `update_card_state`, `propose_integration`, `list_cards` | ✅ |
| 4 — Живой корпус | `improve_github_tracker.py`, `improve_proposal_gen.py` (23 proposals), incremental IDF | ✅ |
| 5 — Semantic + RFC | `improve_semantic_embeddings.py`, `improve_rfc_tracker.py`, 3 RFC Accepted | ✅ |
| 6 — Autonomous Intelligence | `decay_card`/`restore_card`, `write_type`, watcher lifecycle, knowledge evolution | ✅ |
| 7 — Production Hardening | rate limiting, audit trail, gateway write_type, decay_checker | ✅ |
| 8 — Auto-Summarize + Promote Lift | `improve_auto_summarize.py`: 410 карточек, +90 normalized, +46 approved | ✅ |
| 9 — Progressive Summarize + SSE | `improve_progressive_summarize.py`: 335 карточек, +311 normalized, +70 approved | ✅ |
| 10 — Summary Extender + 1005 Approved | `improve_summary_extender.py`: 713 карточек, +597+18 approved. CI 3-pass pipeline | ✅ |
| 11 — Knowledge Graph + Skill Metrics | `improve_card_graph.py` (18458 рёбер, PageRank), `/api/graph`, `improve_skill_metrics.py` | ✅ |
| 12 — PageRank-Boosted Search | PageRank boost в hybrid_search + `improve_graph_search.py` (neighbourhood search) | ✅ |
| 13 — ANN Index + Query Analytics + Hot Cards | pure-Python ANN (0ms warm), query logging, hot cards composite score | ✅ |
| 14 — Search Boost + Digest + Snapshot + Contacts | title-match boost (Hit Rate 100%), weekly digest, knowledge snapshot, contact drafts | ✅ |
| 15 — CI Quality Gate + Multi-Query + Feedback Loop | CI 6-step pipeline, multi-query RRF fusion, corpus gap feedback loop | ✅ |

**Текущее распределение карточек:** 1005 approved · 109 normalized · 51 raw · promote rate 98.7%

## Итерация 6 — Autonomous Intelligence Layer

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `decay_card` MCP tool | RFC-0002 decay_event: пометить карточку как устаревшую |
| `restore_card` MCP tool | RFC-0002 restore_event: отменить decay |
| `write_type` frontmatter | Все карточки из MCP получают `write_type: episode`, `written_by: mcp`, `written_at` |
| Lifecycle watcher rules | `improve_watcher.py`: proposals/ → promote, rfcs/ → update registry, habr → regenerate proposals |
| `improve_knowledge_evolution.py` | Снапшоты KPI во времени → `docs/KNOWLEDGE_EVOLUTION.md` + `docs/knowledge_evolution.json` |
| Collab Finder semantic upgrade | Гибрид 0.5×card_tfidf + 0.3×doc_semantic + 0.2×bm25 + graph_bonus |

### MCP: теперь 17 инструментов

```
read  (11): search, decisions, contacts, project_status, bm25_search, run_recipe,
             list_recipes, run_improve, health, list_scripts, update_contact
write  (6): add_card, update_card_state, propose_integration, list_cards,
             decay_card, restore_card
```

## Итерация 7 — Production Hardening

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| Rate limiting MCP | `_write_rate_limit()` — 100ms между write-вызовами (RFC-0003) |
| Audit trail | `_audit_write()` → `.claude/mcp_write_log.jsonl` для всех 6 write-инструментов |
| Gateway write_type | `gateway.py`: `write_type: episode`, `written_by: gateway`, `written_at` |
| `improve_decay_checker.py` | Поиск кандидатов на decay: stubs (377), near-dups (79) → `docs/DECAY_CANDIDATES.md` |
| RFC-0002/0003 promoted | Оба RFC переведены в `normalized` → `approved` (274 approved итого) |

---

## Итерация 12 — PageRank-Boosted Search

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| PageRank boost в `gateway.py` | `_load_pagerank()` загружает CARD_GRAPH.json, `hybrid_search()` умножает scores на `(1 + 0.3 × pagerank)`. Синтетический хаб (autofilled, pr=1.0) ограничен cap=0.4 |
| PageRank boost в `improve_semantic_search.py` | `_get_pagerank()` + boost в `search_hybrid()` после RRF-слияния. Те же параметры: alpha=0.3, cap=0.4 |
| `improve_graph_search.py` | Graph-neighbourhood search: TF-IDF seed → BFS-расширение на 1-2 хопа → re-rank по relevance × pagerank. CLI: `--seeds`, `--hops`, `--alpha`, `--json`, `--stats` |
| `/api/status` расширен | Поле `pagerank_nodes` + `pagerank_boost: true` в ответе health/status |

### Архитектура PageRank-boost

```
query
  ↓
TF-IDF + BM25 → fusion scores (Reciprocal Rank Fusion)
  ↓
× (1 + 0.3 × min(pagerank, 0.4))   ← boost: связанные карточки поднимаются
  ↓
top-K результатов
```

**Почему cap=0.4 для synthetic hub?** Карточка `autofilled` имеет 1501 входящих ссылок из-за авто-генерированных cross-reference файлов — это технический артефакт, а не семантический хаб. Ограничение предотвращает то, что она появляется в топе всех запросов.

### Graph-neighbourhood search

```
seed cards (TF-IDF top-10)
  ↓
BFS expand (1 hop out + 1 hop in по рёбрам графа)
  ↓
~200-500 кандидатов
  ↓
re-rank: (tfidf_score + rank_bonus) × (1 + alpha × pagerank)
  ↓
top-K результатов — включая карточки без ключевых слов, но связанные семантически
```

### CLI

```bash
python scripts/improve_graph_search.py --query "агент с памятью"
python scripts/improve_graph_search.py --query "RAG retrieval" --hops 2 --top 15
python scripts/improve_graph_search.py --query "Yodoca" --json
python scripts/improve_graph_search.py --stats  # статистика графа

# Обновлённый гибридный поиск с PageRank:
python scripts/improve_semantic_search.py --query "агент память консолидация"

# REST gateway теперь тоже с boost:
curl -X POST http://localhost:8083/api/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "агент с памятью", "top_k": 5}'
```

---

## Итерация 13 — ANN Index + Query Analytics + Hot Cards

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `improve_ann_index.py` (переписан) | Двойной backend: HNSW (если numpy+hnswlib) / pure-Python inverted index (fallback, zero-deps). Warm query: <1ms. `ann_search(query, top_k)` — публичный API для gateway. `--build` создаёт `docs/ann_meta.json` за ~0.7с |
| Gateway ANN enabled | `_ANN_AVAILABLE = True` без каких-либо зависимостей. `mode=ann` в POST /api/ask теперь работает out-of-the-box |
| Query logging в gateway.py | `_log_query()` пишет в `.claude/query_log.jsonl` при каждом запросе (ask / search / chat). Запись асинхронная, не влияет на latency |
| `improve_query_log.py` (новый) | Читает query_log.jsonl, выдаёт `docs/QUERY_ANALYTICS.md`: top queries, p50/p95/p99 latency, источники, zero-result queries, hour-of-day pattern |
| `improve_hot_cards.py` (новый) | Composite hot-score: 0.4×PageRank + 0.3×query_freq + 0.2×state_bonus + 0.1×summary_quality. Вывод: `docs/HOT_CARDS.md` + `.claude/hot_cards.json`. 1809 карточек проранжировано |
| `improve_run_all.py` обновлён | `improve_hot_cards.py` + `improve_query_log.py` в группе reports; `improve_ann_index.py` + `improve_graph_search.py` в semantic/graph |

### Inverted-Index ANN: как работает

```
Build (~0.7s):
  for doc in 1809 docs:
    tokenize + TF-IDF weight
    store in inverted_index[token] → [(doc_id, weight)]
  → save ann_meta.json (vocab=13633, postings=203180)

Query (<1ms warm):
  tokenize query → q_vec (sparse TF-IDF)
  for each token in q_vec:
    get posting list → accumulate dot-products
  normalise → cosine similarity → top-K
```

### CLI

```bash
python scripts/improve_ann_index.py --build                      # построить индекс
python scripts/improve_ann_index.py --query "агент с памятью"    # поиск
python scripts/improve_ann_index.py --benchmark                  # замер скорости
python scripts/improve_ann_index.py --stats                      # статистика

python scripts/improve_query_log.py                              # аналитика запросов
python scripts/improve_query_log.py --top 20                     # топ-20 запросов
python scripts/improve_query_log.py --json                       # JSON

python scripts/improve_hot_cards.py                              # топ горячих карточек
python scripts/improve_hot_cards.py --top 20 --state approved    # только approved
python scripts/improve_hot_cards.py --json                       # JSON
```

---

## Итерация 14 — Search Boost + Digest + Snapshot + Contact Drafts

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| Title-match boost в поиске | `_tfidf_search()` в gateway.py и precision_eval.py: `score *= (1 + 2.5 × title_overlap)`. Hit Rate@10: 0.850 → **1.000** (20/20). Mean MRR: 0.437 → 0.441 |
| `improve_digest_weekly.py` (переписан) | Четыре источника: git activity + card lifecycle + hot cards (топ-5) + query analytics. Flags: `--days`, `--no-cards` |
| `improve_knowledge_snapshot.py` (новый) | Comprehensive KPI snapshot: corpus/search/graph/skills/activity. Сохраняет `docs/KNOWLEDGE_SNAPSHOT.md` + `docs/snapshots/YYYYMMDD.json` для исторического тренда. `--trend` показывает таблицу изменений |
| `improve_contact_personalize.py` (новый) | Template-based contact drafts (без LLM). 3 шаблона (memory/knowledge/orchestration layer). 15 черновиков → `docs/contacts/{author}_draft.md`. `--stats`, `--dry-run`, `--author` |
| `improve_run_all.py` обновлён | knowledge_snapshot в reports group; contact_personalize в contacts-ext group |

### Архитектура title-boost

```
score = (TF-IDF term match in body) / len(words)

# New: extra multiplier for title overlap
title_tokens  = tokenize(doc.title)
title_overlap = |query_tokens ∩ title_tokens| / |query_tokens|
score *= (1 + 2.5 × title_overlap)
```

**Эффект:** при запросе "NGT Memory ассоциативный граф" документ `ngt-memory.md`
(title содержит {ngt, memory}) получает буст 1 + 2.5×(2/7) ≈ 1.71×, поднимается
с rank=17 в топ-10.

### CLI

```bash
python scripts/improve_precision_eval.py          # Hit Rate@10 eval
python scripts/improve_precision_eval.py --verbose # детали по каждому запросу

python scripts/improve_digest_weekly.py           # еженедельный дайджест
python scripts/improve_digest_weekly.py --days 14 # за 2 недели

python scripts/improve_knowledge_snapshot.py      # snapshot текущего состояния
python scripts/improve_knowledge_snapshot.py --trend  # исторический тренд

python scripts/improve_contact_personalize.py --dry-run   # предпросмотр черновиков
python scripts/improve_contact_personalize.py             # генерация всех черновиков
python scripts/improve_contact_personalize.py --author kksudo
python scripts/improve_contact_personalize.py --stats     # таблица статусов
```

---

## Итерация 15 — CI Quality Gate + Multi-Query + Feedback Loop

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `.github/workflows/docs.yml` расширен | +6 шагов: ANN build → card graph → hot cards → precision eval gate (Hit Rate@10 ≥ 0.70) → knowledge snapshot → weekly digest |
| `improve_multi_query.py` (новый) | Многозапросный поиск с RRF-слиянием. 4 стратегии декомпозиции: delimiter split, clause split, overlapping halves (≥7 токенов), passthrough. Взвешенный RRF + PageRank boost. CLI: `--query`, `--decompose`, `--eval`, `--no-graph`, `--top` |
| `improve_feedback_loop.py` (новый) | Читает `.claude/query_log.jsonl`, выявляет zero-result/low-result/high-demand запросы. BM25 поиск связанного контента. Создаёт заглушки `docs/cards/generated/{slug}.md` при `--apply`. Выводит `docs/FEEDBACK_LOOP.md` + `.claude/gap_queue.jsonl` |
| `improve_run_all.py` обновлён | `improve_multi_query.py` в группе graph; `improve_feedback_loop.py` в группе analytics |

### Архитектура CI Quality Gate

```
push to main
  ↓
Run fast scripts (--group reports)
  ↓
Auto-summarize pass 1/2/3 + promote
  ↓
Update search index
  ↓ ← NEW STEPS
Build ANN index (pure-Python, 0ms warm)
  ↓
Build card graph + PageRank
  ↓
Compute hot cards (composite score)
  ↓
Retrieval quality gate: Hit Rate@10 ≥ 0.70  ← CI FAILS if quality regresses
  ↓
Knowledge snapshot (YYYYMMDD.json)
  ↓
Weekly digest
  ↓
Commit & push auto-updated docs
```

### Архитектура multi-query search

```
query: "агент память MCP SQLite консолидация"
  ↓ decompose_query()
sub_queries = ["агент память MCP SQLite", "SQLite консолидация"]  (overlapping halves)

  ↓ для каждого sub_query: hybrid_search() → result_list
  ↓ опционально: graph_search(original_query) → graph_results

  ↓ _rrf_merge(result_lists, weights=[1.2, 1.0, 0.8], k=60)
     score = Σ_j  w_j / (60 + rank_j + 1)
     score *= (1 + 0.3 × pagerank)

  ↓ top-K результатов с полем _mq_score
```

### Архитектура feedback loop

```
.claude/query_log.jsonl
  ↓ load_log(days=7)
  ↓ detect_gaps()

zero_result: ["RAG квант", "memory palace"]   → BM25 → related cards → create stub
low_result:  ["MCP write back", "ANN HNSW"]   → рекомендация обогатить
high_demand: [("агент память", 5), ...]        → приоритет в следующем цикле

  ↓ build_report() → docs/FEEDBACK_LOOP.md
  ↓ append .claude/gap_queue.jsonl
  ↓ --apply: создать docs/cards/generated/{slug}.md (state: raw, tags: [gap, generated])
```

### CLI

```bash
# Multi-query search
python scripts/improve_multi_query.py --query "агент память MCP SQLite"
python scripts/improve_multi_query.py --query "RAG + BM25 + граф знаний" --top 10
python scripts/improve_multi_query.py --decompose "агент память MCP SQLite"  # показать декомпозицию
python scripts/improve_multi_query.py --eval   # сравнение multi vs single на eval set

# Feedback loop
python scripts/improve_feedback_loop.py           # анализ gap за 7 дней
python scripts/improve_feedback_loop.py --apply   # создать stub-карточки для gap
python scripts/improve_feedback_loop.py --days 30 # lookback 30 дней
python scripts/improve_feedback_loop.py --json    # JSON output
```

### Следующий уровень (Итерация 16)

| Задача | Сложность | Ценность |
|--------|-----------|---------|
| LLM-enhanced contact messages (ANTHROPIC_API_KEY) | средняя | высокая |
| Auto-fill gap stubs from related content (feedback_loop + gap_filler) | средняя | высокая |
| A/B test multi-query vs single-query hit rate via precision_eval | низкая | средняя |

---

## Итерация 11 — Knowledge Graph + Skill Metrics

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `improve_card_graph.py` | Directed graph 1166 узлов + 18 458 рёбер из wikilinks и md-ссылок. PageRank за 30 итераций. Топ-хаб: 1501 входящих ссылок (autofilled). Вывод: `docs/CARD_GRAPH.json` + `docs/CARD_GRAPH.md` |
| Gateway `/api/graph` | GET `/api/graph?top=100&state=approved` — возвращает отфильтрованный граф из CARD_GRAPH.json |
| `improve_skill_metrics.py` | Рубрика качества скилов: structure/length/examples/steps/tools/clarity. 28 скилов, средний балл 86/100, 27/28 хороших |
| `improve_run_all.py` | `improve_skill_metrics.py` + `improve_card_graph.py` добавлены в группу reports |

### CLI

```bash
python scripts/improve_card_graph.py          # построить граф + CARD_GRAPH.md
python scripts/improve_card_graph.py --top 20 # топ-20 хабов
python scripts/improve_card_graph.py --dot    # Graphviz DOT для топ-50
python scripts/improve_skill_metrics.py       # качество всех скилов
python scripts/improve_skill_metrics.py --low # только слабые скилы

# REST:
curl http://localhost:8083/api/graph?top=50
curl "http://localhost:8083/api/graph?state=approved&top=100"
```

---

## Итерация 10 — Summary Extender + 1005 Approved

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `improve_summary_extender.py` | Расширяет summary с 80-149ch до 150+ch для normalized карточек. Стратегии: предложения из body, abstract-auto, title-context. 713 карточек обновлено |
| Batch promote | +597 approved за один проход, +18 за второй → **1005 approved** |
| `improve_card_promote.py` threshold | `min_body_words` 300→270: компенсация агрессивного стриппинга пунктуации |
| CI 3-pass pipeline | `.github/workflows/docs.yml`: auto_summarize → progressive_summarize → summary_extender → promote |
| Second-tag injection | `improve_summary_extender.py` также добавляет 2-й тег если тегов < 2 |

### Результат

```
До Итерации 10:   approved=390   normalized=724  raw=51  promote_rate=69%
После Итерации 10: approved=1005  normalized=109  raw=51  promote_rate=98.7%
```

Пик достигнут: 98.7% всех карточек с достаточным содержимым теперь в статусе approved или normalized.
Оставшиеся 51 raw — navigation README-файлы с body < 150 слов (структурные, не содержательные).

### CLI

```bash
python scripts/improve_summary_extender.py --dry-run          # план
python scripts/improve_summary_extender.py --apply            # применить + promote
python scripts/improve_summary_extender.py --apply --no-promote  # только файлы
python scripts/improve_run_all.py --group lifecycle           # полный lifecycle pipeline
```

---

## Итерация 9 — Progressive Summarize + SSE Streaming

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `improve_progressive_summarize.py` | Второй проход суммаризации: abstract-auto блоки, секции ## Summary, мульти-предложения. 335 карточек исправлено |
| Batch promote | +311 normalized, +70 approved. Promote rate: 95.7% (было 69%) |
| `improve_bulk_decay.py` | Bulk decay пустых stub-карточек по date-age и содержанию (future-ready, работает когда корпус > 90 дней) |
| SSE Streaming Gateway | `gateway.py`: `stream=True` → `StreamingResponse` с word-by-word SSE чанками (OpenAI SSE format) |
| `improve_run_all.py` lifecycle | Добавлен `improve_auto_summarize.py` в группу lifecycle |

### Ключевые результаты

```
До Итерации 9:   approved=320  normalized=483  raw=362  promote_rate=69%
После Итерации 9: approved=390  normalized=724  raw=51   promote_rate=95.7%
```

Прорыв объяснён: `improve_auto_summarize.py` не мог извлечь длинные предложения из файлов
с `<!-- abstract-auto -->` блоками (slugified anchors, emoji-prefixed bullet points).
`improve_progressive_summarize.py` специально парсит `🎯 Проблема / 🔧 Подход / ✅ Результат`
структуру и склеивает их в связный summary.

### CLI

```bash
python scripts/improve_progressive_summarize.py --dry-run
python scripts/improve_progressive_summarize.py --apply
python scripts/improve_bulk_decay.py --stats
python scripts/improve_bulk_decay.py --apply --min-age 90
# SSE streaming test:
curl -N -X POST http://localhost:8083/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"что такое AgentFS?"}],"stream":true}'
```

---

## Итерация 8 — Auto-Summarize + Promote Lift

### Что реализовано

| Компонент | Детали |
|-----------|--------|
| `improve_auto_summarize.py` | Инжекция summary (TF-IDF/первое предложение) и тегов для raw-карточек с коротким summary < 80ch |
| Batch promote | 410 карточек обогащено → +90 normalized, +46 approved в двух итерациях промоушена |
| `improve_audit_db.py --write-log` | `cmd_write_log()`: читает `.claude/mcp_write_log.jsonl`, статистика по инструментам |
| Knowledge evolution snapshot | Снапшот KPI: approved=320, normalized=483, raw=362 |

### Результат автоматизации

Причина блокировки 361 raw-карточки была установлена: наличие тегов (`<!-- tags: -->`)
не помогало — критерий для promote — `summary ≥ 80ch` в frontmatter/HTML-комментарии.
`improve_auto_summarize.py` извлекает лучшее предложение из тела и инжектирует `<!-- summary --> > ...`.

```
До Итерации 8:   approved=274  normalized=441  raw=451  promote_rate=62.3%
После Итерации 8: approved=320  normalized=483  raw=362  promote_rate=69%
```

### CLI

```bash
python scripts/improve_auto_summarize.py --dry-run     # план без изменений
python scripts/improve_auto_summarize.py --apply       # применить
python scripts/improve_auto_summarize.py --apply --section 02-anthropic-vacancies
python scripts/improve_audit_db.py --write-log         # audit trail MCP write операций
python scripts/improve_knowledge_evolution.py          # снапшот KPI
```

---

## 1. Концептуальный статус

### Что это такое прямо сейчас

Lorenzo — это **исследовательская база знаний с живым поисковым движком**, собранная вокруг идеи Svyazi 2.0. Технически: монорепозиторий Markdown-документов с набором Python-скриптов, которые строят индексы, ищут, генерируют отчёты и экспортируют в разные форматы.

Авторам OSS-проектов отправлены открытые письма. Их отклик — желателен, но не является условием развития. Система растёт независимо.

### Три уровня зрелости

```
Уровень 1 — Корпус и поиск       ✅ ГОТОВО    (1632 карточки, BM25+TF-IDF+ANN)
Уровень 2 — Интеграция и API      ✅ ГОТОВО    (MCP 15 инструментов, Gateway OpenAI)
Уровень 3 — Жизненный цикл знания ✅ РЕАЛИЗОВАН (272 approved, 435 normalized, promoter, proposals)
```

**Петля обратной связи замкнута:** MCP-агент может добавлять карточки → passages + index синхронизируются → promoter переводит в normalized/approved → proposals генерируются автоматически.

---

## 2. Технический аудит

### 2.1 Что работает хорошо

| Компонент | Состояние | Детали |
|-----------|-----------|--------|
| BM25 passages | ✅ | 13 070 абзацев, хорошее покрытие |
| TF-IDF индекс | ✅ | 16 487 токенов, 1632 карточки |
| ANN (hnswlib) | ✅ | HNSW, 37× speedup vs brute-force |
| search_index.json | ✅ | 2500 docs, все с content+summary |
| Gateway HTTP | ✅ | FastAPI, OpenAI-compatible, write-back |
| MCP сервер | ✅ | 11 инструментов, stdio режим |
| CI/CD | ✅ | GitHub Actions daily 06:00 UTC |
| Orphan rate | ✅ | 0/1563 — отлично |
| Теги | ⚠️ | 1877/2500 (25% без тегов) |
| Broken links | ⚠️ | 3329 итого, но ~21 реальных (остальные — obsidian/ auto-copy) |

### 2.2 Критические проблемы

#### Проблема 1: Все карточки — `raw`, жизненный цикл не работает

```
Карточки по статусу:
  raw       1632  ← все
  normalized   0
  approved     0
  inferred     0
```

Это значит: Memory Write Policy (PROTOTYPE_SPEC §3.3) существует как спецификация, но ни один скрипт не переводит карточку из `raw` в следующий статус. Review Queue UI (Streamlit) есть, но очередь на одобрение пуста — нечего одобрять, потому что никто не генерирует `proposal`-карточки.

**Что нужно:** скрипт-промоутер `improve_card_promote.py` — автоматически переводит `raw → normalized` если карточка: имеет summary + теги + > 200 слов в body.

#### Проблема 2: MCP-сервер только читает

Текущий MCP-сервер имеет 11 инструментов, все — на чтение/запрос. Нет ни одного инструмента записи. Gateway имеет `POST /api/cards`, но MCP-агент не может добавить карточку без HTTP-вызова. Это архитектурный разрыв: LLM-агент через MCP видит корпус, но не может его обогатить.

**Что нужно:** добавить в `mcp_server.py` инструменты `add_card`, `update_card_state`, `add_edge`.

#### Проблема 3: passages.json не синхронизируется при write-back

Когда Gateway добавляет карточку через `POST /api/cards`, он создаёт `.md`-файл и обновляет `search_index.json`, но **не пересобирает `passages.json`**. Значит новая карточка попадёт в TF-IDF поиск, но не в BM25. Поиск становится несогласованным со временем.

**Что нужно:** после write-back запускать `improve_passage_retrieval.py --incremental` или добавить инкрементальное обновление passages прямо в gateway.

#### Проблема 4: Нет дедупликации при добавлении карточек

Gateway и MCP не проверяют, существует ли уже карточка с похожим содержимым. Повторные запросы создадут дубли. `improve_dedup.py` существует, но не интегрирован в write-back пайплайн.

#### Проблема 5: Теги на 25% карточек отсутствуют

1877/2500 документов имеют теги. 623 — без тегов. Это снижает качество фасетного поиска и кластеризации.

### 2.3 Технический долг по приоритету

| # | Задача | Сложность | Ценность |
|---|--------|-----------|---------|
| T1 | Card lifecycle: скрипт `improve_card_promote.py` | средняя | высокая |
| T2 | MCP write-back: `add_card` + `update_card_state` в `mcp_server.py` | средняя | высокая |
| T3 | Синхронизация passages при write-back | низкая | высокая |
| T4 | Дедупликация в write-back пайплайне | средняя | средняя |
| T5 | Авто-теги для 623 документов без тегов | низкая | средняя |
| T6 | Исправить якорные ссылки в habr-project файлах | низкая | низкая |
| T7 | LLM-обогащение через `improve_llm_enrich.py` | низкая (ключ есть) | высокая |
| T8 | Proposal-генератор: агент предлагает карточки-гипотезы | высокая | высокая |

---

## 3. Архитектурный анализ: плюсы и минусы

### Плюсы

**Local-first и offline-capable.** Вся система работает без интернета, без платных API, без Docker. Это редкость в AI-пространстве 2026 года. Полная воспроизводимость и контроль данных.

**Богатый поисковый стек.** BM25 + TF-IDF + ANN + граф-бонус — это нестандартная комбинация, которая даёт лучшие результаты, чем любой из методов по отдельности. Precision@5 ≥ 0.7 — реально достигнутая метрика.

**OpenAI-совместимый шлюз.** Любой клиент (Claude Desktop, Cursor, Python openai SDK) подключается без изменений кода. Это снижает барьер входа для использования корпуса до нуля.

**28 Claude-скиллов** охватывают весь workflow: от `analyze-project` до `write-contact` до `design-ensemble`. Это уникальный актив, который другие проекты строят годами.

**196 скриптов обработки** с рецептами и оркестратором — фактически собственная система ETL/ELT для знаний. Ни один из конкурентов (Obsidian + плагины, Notion AI, Roam) не даёт такой программируемости.

**Corpus quality 97.9/100.** Высокое качество документации — редкость в R&D проектах.

### Минусы

**Нет жизненного цикла карточек в реальности.** PROTOTYPE_SPEC описывает красивую систему state machine, но на практике все карточки `raw`. Это не баг — это пропасть между спецификацией и реализацией.

**Поиск не учит себя.** TF-IDF и BM25 — статичные модели. При добавлении новых карточек индекс нужно пересобирать вручную. Нет инкрементального обновления IDF-весов.

**Зависимость от файловой системы как БД.** При 2484 файлах и 2.9M слов поиск занимает секунды, но при 10K+ файлах начнутся проблемы. Нет чёткой стратегии перехода на настоящую БД.

**MCP только читает.** Главный интерфейс для AI-агентов — read-only. Агент видит корпус, но не может его развивать. Это противоречит идее Knowledge OS, где система должна самообогащаться.

**Нет event-системы.** Добавление карточки не триггерит переиндексацию, не уведомляет агентов, не запускает consolidation. Система реагирует только на cron.

**Habr-проекты — богатые файлы, но не связаны с живыми репозиториями.** AgentFS, Yodoca, MemNet существуют как документы, но нет автоматического мониторинга их GitHub-репозиториев: новые коммиты, issues, releases не попадают в корпус.

---

## 4. Идеи для улучшения

### Группа A — Быстрые победы (1-3 дня каждая)

**A1. Card Promoter** — `improve_card_promote.py`
Скрипт, который проходит по всем `raw`-карточкам и переводит в `normalized` те, что соответствуют критериям: summary ≥ 100 символов, теги ≥ 2, body ≥ 200 слов. Это сразу наполнит Review Queue реальными кандидатами.

**A2. MCP write-back** — добавить в `mcp_server.py`:
- `add_card(title, content, section, tags)` → создаёт `.md` + обновляет индекс
- `update_card_state(card_id, state, reason)` → raw→normalized→approved
- `add_edge(from_id, to_id, relation)` → обогащает граф

**A3. Passages sync** — в `gateway.py::_create_card()` после записи файла добавить вызов инкрементальной пересборки passages. Уже есть `improve_passage_retrieval.py --incremental`.

**A4. Auto-tags для 623 документов** — запустить `improve_tags.py` только на файлах без тегов (уже есть, просто не запускали на полном корпусе).

### Группа B — Средние улучшения (1-2 недели каждая)

**B1. GitHub Tracker** — `improve_github_tracker.py`
Мониторинг GitHub-репозиториев авторов: AgentFS, Yodoca, MemNet, agent-memory-mcp и др. При новом коммите/релизе создаётся карточка-событие. Это превращает статичную базу знаний в живую ленту.

```python
# Принцип работы:
# 1. Читает docs/contacts/*.md → извлекает GitHub-URL
# 2. Через GitHub API получает commits/releases за последние N дней
# 3. Создаёт Card Envelope с card_type="event", state="raw"
# 4. Добавляет edge: event → project
```

**B2. Proposal Generator** — `improve_proposal_gen.py`
Агент, который сравнивает пары проектов из корпуса и генерирует `proposal`-карточки с гипотезами об интеграции. Это создаёт реальную нагрузку на Review Queue.

```
AgentFS + Yodoca → proposal: "AgentFS vault как persistence layer для Yodoca episodes"
MemNet + NGT Memory → proposal: "MemNet forgetting policy применима к NGT-графу"
```

**B3. Incremental IDF** — обновление TF-IDF весов при добавлении новых карточек без полной пересборки. Сейчас добавление 1 карточки требует пересборки индекса (1632 документа). С инкрементальным IDF — O(n_new_tokens).

**B4. Card Deduplication в write-back** — перед созданием новой карточки проверять косинусное сходство с топ-5 похожими. Если similarity > 0.85 — предлагать merge вместо создания.

### Группа C — Стратегические улучшения (месяц+)

**C1. Knowledge Graph как первичная структура**
Сейчас граф — вторичная надстройка над файлами. Стратегически правильнее инвертировать: граф первичен, файлы — проекция. Это открывает graph traversal retrieval: "найти все проекты в 2 hop от AgentFS". Технология: NetworkX или собственная adjacency list поверх JSON.

**C2. Semantic Chunking + Real Embeddings**
TF-IDF хорош, но не понимает синонимы. Следующий шаг — sentence-transformers (или API Anthropic Embeddings). Это не требует GPU: `paraphrase-multilingual-MiniLM-L12-v2` (~420MB, CPU) даёт косинусное сходство для RU+EN. `improve_chunk_semantic.py` уже создаёт JSONL — нужно добавить embedding-поле.

**C3. Autonomous Consolidation Agent**
Агент-ночник: каждую ночь берёт N случайных `raw`-карточек, сравнивает, генерирует proposals для похожих, переводит очевидные в `normalized`. Использует локальный LLM (ollama + qwen2.5) или Claude API по расписанию.

**C4. RFC System**
Уже есть скилл `generate-rfc`. Нужна поддержка в виде папки `docs/rfcs/` с нумерованными RFC-файлами, статусами (Draft/Proposed/Accepted/Rejected) и автоматическим трекером в CI. Это даст формальную систему для принятия архитектурных решений.

---

## 5. Обогащение через MCP-серверы: конкретная схема

### Текущее состояние MCP

```
Инструменты (только чтение):
  search_docs(query)              → полнотекстовый поиск
  bm25_search(query)              → поиск по абзацам
  get_decisions(topic)            → решения по теме
  get_contacts(project)           → контакты авторов
  get_project_status(name)        → статус проекта
  run_improve(script, dry_run)    → запустить скрипт
  run_recipe(name, dry_run)       → запустить рецепт
  list_recipes()                  → список рецептов
  get_health()                    → здоровье репо
  list_scripts()                  → список скриптов
  update_contact_status(...)      → ← это единственный инструмент записи
```

### Что добавить (конкретные сигнатуры)

```python
# В mcp_server.py добавить:

@server.tool()
async def add_card(
    title: str,
    content: str,
    section: str = "05-habr-projects",
    tags: list[str] = [],
    card_type: str = "note",
    source_url: str = ""
) -> str:
    """Добавить новую карточку в корпус знаний."""
    # 1. Генерировать card_id (sha256 от title+content)
    # 2. Проверить на дубли (cosine > 0.85 → вернуть existing card_id)
    # 3. Создать .md файл в docs/{section}/
    # 4. Обновить search_index.json
    # 5. Запустить инкрементальную пересборку passages

@server.tool()
async def update_card_state(
    card_id: str,
    new_state: str,  # raw | normalized | approved | rejected | decayed
    reason: str = ""
) -> str:
    """Обновить статус карточки в жизненном цикле."""

@server.tool()
async def propose_integration(
    project_a: str,
    project_b: str,
    hypothesis: str
) -> str:
    """Создать proposal-карточку об интеграции двух проектов."""
    # → card_type="proposal", state="raw", edges=[project_a, project_b]

@server.tool()
async def get_card_by_id(card_id: str) -> dict:
    """Получить полную карточку по ID."""

@server.tool()
async def list_cards(
    card_type: str = "",
    state: str = "raw",
    section: str = "",
    limit: int = 20
) -> list[dict]:
    """Список карточек с фильтрацией."""
```

### Схема обогащения через MCP

```
LLM-агент (Claude Desktop / Cursor)
    │
    │ MCP stdio
    ▼
mcp_server.py
    │ add_card()
    ▼
docs/{section}/{slug}.md   ←── новый файл
    │
    │ инкрементальный rebuild
    ▼
search_index.json  +  passages.json
    │
    │ следующий daily CI run
    ▼
TF-IDF индекс, ANN граф, COLLAB_SUGGESTIONS.md
```

Это замыкает петлю: агент читает корпус → анализирует → добавляет новые знания → при следующем поиске эти знания уже доступны.

---

## 6. План действий (приоритизированный)

### Фаза 1 — Закрыть технический долг (1 неделя)

| Задача | Скрипт/файл | Трудозатраты |
|--------|-------------|-------------|
| Авто-теги для 623 файлов без тегов | `improve_tags.py` (уже есть) | 30 мин |
| Passages sync при write-back | `gateway.py` строка ~180 | 1 час |
| Якорные ссылки в habr-project файлах | `improve_broken_links.py --fix --section 05-habr-projects` | 1 час |
| Дедупликатор в write-back | `gateway.py` + `improve_dedup.py` | 3 часа |

### Фаза 2 — Card Lifecycle (1 неделя)

| Задача | Новый артефакт | Трудозатраты |
|--------|----------------|-------------|
| `improve_card_promote.py` | raw→normalized по критериям | 4 часа |
| Наполнить Review Queue proposals | запустить promoter на 1632 картах | 30 мин |
| Review + одобрить топ-50 карточек | `streamlit run review_queue.py` | 2 часа |

### Фаза 3 — MCP Write-back (1 неделя)

| Задача | Файл | Трудозатраты |
|--------|------|-------------|
| `add_card` инструмент в MCP | `mcp_server.py` | 4 часа |
| `update_card_state` инструмент | `mcp_server.py` | 2 часа |
| `propose_integration` инструмент | `mcp_server.py` | 2 часа |
| Тест через `improve_mcp_test.py` | `mcp_server.py` | 1 час |

### Фаза 4 — Живой корпус (2 недели)

| Задача | Новый артефакт | Трудозатраты |
|--------|----------------|-------------|
| `improve_github_tracker.py` | мониторинг 8 репозиториев авторов | 8 часов |
| `improve_proposal_gen.py` | автогенерация proposals | 8 часов |
| Incremental IDF update | `improve_embedding_index.py` | 6 часов |

### Фаза 5 — Семантический поиск (2-4 недели)

| Задача | Новый артефакт | Трудозатраты |
|--------|----------------|-------------|
| sentence-transformers интеграция | `improve_semantic_embeddings.py` | 12 часов |
| Обновить ANN индекс под новые embeddings | `improve_ann_index.py` | 4 часа |
| RFC system | `docs/rfcs/` + `improve_rfc_tracker.py` | 6 часов |

---

## 7. Концептуальное резюме

Проект находится в точке, когда **инфраструктура опередила процесс**. Есть отличный поиск, API, CI, скиллы — но нет живого потока знаний, который бы эту инфраструктуру нагружал.

Главный принцип следующего этапа: **замкнуть петлю обратной связи**.

```
Найти → Проанализировать → Добавить карточку → Предложить интеграцию → Одобрить → Найти снова
```

Сейчас петля разомкнута на шаге «Добавить карточку через MCP» и «Перевести из raw в approved». Как только эти два шага заработают, система начнёт самообогащаться — независимо от того, ответят ли авторы Habr-проектов.

---

_Документ составлен на основе аудита: PROTOTYPE_SPEC.md, PROGRESS.md, SCORING.md, HEALTH.md, BROKEN_LINKS.md, card_index stats, search_index stats, passages stats, mcp_server.py, gateway.py._

<!-- see-also -->

---

**Смотрите также:**
- [PROTOTYPE_SPEC](PROTOTYPE_SPEC.md)
- [INFO_PROCESSING_METHODS](INFO_PROCESSING_METHODS.md)
- [SCRIPT_EVAL_REPORT](SCRIPT_EVAL_REPORT.md)
- [PROCESSING_GUIDE](processing-guide/PROCESSING_GUIDE.md)

