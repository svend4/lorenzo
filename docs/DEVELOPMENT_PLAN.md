# Lorenzo — План развития: технический аудит и следующие шаги

_Дата: 2026-05-13 · Обновлено: 2026-05-13 · Ветка: claude/current-dev-stage-dJtu0_

---
<!-- tags: memory, rag, orchestration, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improve, collaboration -->

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

**Текущее распределение карточек:** 390 approved · 724 normalized · 51 raw · promote rate 95.7%

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

### Следующий уровень (Итерация 10)

| Задача | Сложность | Ценность |
|--------|-----------|---------|
| Neural embeddings (sentence-transformers) | низкая (pip install) | высокая |
| Auto-decay оставшихся 51 raw-стабов после даты > 90d | низкая | средняя |
| `improve_skill_metrics.py` — автоматические метрики по скилам | средняя | высокая |

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
