---
title: "Отчёт о дублировании"
tags:
  - general
date: 2026-05-13
---

# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **998**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/LANGUAGE_STATS.md` vs `docs/obsidian/LANGUAGE_STATS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | Язык | Ожидалось | RU% | EN% | |------|------|-----------|-----|-----| | `173-4-ten-domains-of-application.md` | EN | RU | 2% | 98% | | `217-6-risks-specific-to-this-category.md` | EN | RU | …

> | Файл | RU% | EN% | |------|-----|-----| | `181-12-closing.md` | 20% | 80% | | `45-passports-pro2-md.md` | 20% | 80% | | `211-table-of-contents.md` | 20% | 80% | | `325-аннотация.md` | 80% | 20% | | …

> | Секция | RU | EN | MIX | |--------|----|----|-----| | `01-svyazi` | 0 | 0 | 16 | | `02-anthropic-vacancies` | 52 | 122 | 183 | | `03-technology-combinations` | 0 | 0 | 7 | | `04-ai-collaborations` |…

---

### 100% — `docs/CONSISTENCY.md` vs `docs/obsidian/CONSISTENCY.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Термин | Канонично | Вариант | Файлов | |--------|-----------|---------|--------| | **knowledge-space** | `knowledge-space` | `knowledgespace` | 7 | | **knowledge-space** | `knowledge-space` | `know…

> - `docs/CONSISTENCY.md` - `docs/obsidian/CONSISTENCY.md` - `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` - `docs/obsidian/02-anthropic-vacancies/365-развёрнутый…

---

### 100% — `docs/STALENESS.md` vs `docs/obsidian/STALENESS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Файл | Слов | Проблемы | |------|------|---------| | `docs/MCP_DASHBOARD.md` | 21 | нет summary, нет тегов, короткий (21 слов) | | `docs/autofilled/README.md` | 66 | нет summary, нет тегов, короткий…

> | Файл | Слов | |------|------| | `docs/ai-collaborations/candidates/README.md` | 98 | | `docs/glossary/README.md` | 88 | | `docs/habr-unique-projects/analogues/README.md` | 91 | | `docs/habr-unique-p…

---

### 100% — `docs/KPI.md` vs `docs/obsidian/KPI.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Значение | Контекст | Источник | |----------|----------|---------| | **34** | g — 68 ролей - Sales — 150 ролей (самый большой кластер, ≈34% всего найма) - Fin | `00-intro` | | **90** | Посадить тако…

> | Значение | Контекст | Источник | |----------|----------|---------| | **429** | ициальных данных Anthropic Статья даёт только общие цифры (≈429 вакансий, вилка  | `00-intro` | | **10** | овую повестк…

> | Значение | Контекст | Источник | |----------|----------|---------| | **0.1.5** | **MIT**. citeturn33view4turn27view0 \| Рабочий прототип, версия 0.1.5; “рабо | `03-component-catalog` | | **4.5**…

---

### 100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@5 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.589 | — | — | | Avg Latency   | 1.385с | ≤ 5.0с …

> > **Примечание:** Hit Rate@K = доля запросов, где хотя бы 1 релевантный > документ попал в топ-K. Стандартный P@K с 1 документом/запрос ≤ 1/K, > поэтому Hit Rate — правильная метрика для этого набора …

> - **Метрика:** Hit Rate@5 — доля запросов с ≥1 релевантным документом в топ-5. - **Поиск:** `hybrid_search()` = 0.6×TF-IDF + 0.4×BM25 с фильтром шумовых документов. - **Фильтр шума:** исключаются meta…

---

### 100% — `docs/BADGES.md` vs `docs/obsidian/BADGES.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> ## Markdown сниппеты для README ```markdown !tests !templates !skills !mcp_servers !manifests !scripts !health !validation ```

> - **tests** !tests - **templates** !templates - **skills** !skills - **mcp-servers** !mcp_servers - **manifests** !manifests - **scripts** !scripts - **health** !health - **validation** !validation

---

### 100% — `docs/BACKLINKS.md` vs `docs/obsidian/BACKLINKS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Раздел | Входящих | Исходящих | |--------|----------|-----------| | **.claude** | 28 | 0 | | **01-svyazi** | 383 | 183 | | **02-anthropic-vacancies** | 7110 | 4972 | | **03-technology-combinations**…

> | Документ | Входящих ссылок | Ссылающиеся файлы | |----------|----------------|-------------------| | `READABILITY` | 736 | `00-intro-part2.md`, `02-methodology.md`, `06-security-privacy.md`, `QA.md`…

---

### 100% — `docs/VALIDATION.md` vs `docs/obsidian/VALIDATION.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> - **agent-spec** — Спецификация AI-агента: тип, принципал, скилы, tools, память, decision boundary - **contact-outreach** — Контактный файл автора OSS-проекта: профиль, статус связи, первое сообщение …

---

### 100% — `docs/GATEWAY.md` vs `docs/obsidian/GATEWAY.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ### `POST /api/search` Лёгкий поиск — только список результатов, без LLM-синтеза и контекста. Подходит для автодополнения и быстрого UI. ```bash curl -X POST http://localhost:8083/api/search \      -H…

> ``` ┌─────────────────────────────────────────────┐ │   Любой AI-клиент                           │ │   (Claude Desktop / Cursor / GPT / агент)   │ └─────────────────┬───────────────────────────┘     …

> - Что это - Сравнение с DAF-gateway - Архитектура - Запуск - Эндпоинты (`/api/health`, `/api/status`, `/api/benchmark`, `/api/ask`, `/api/search`, `/api/collabs`, `/api/cards`, `/v1/chat/completions`)…

---

### 100% — `docs/CLUSTERS.md` vs `docs/obsidian/CLUSTERS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` — _276-the-two-layer-stack-as-it-exists_ - `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` — _277-what-s-missing-lay…

> - `docs/02-anthropic-vacancies/13-angle-perspective.md` — _13-angle-perspective_ - `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` — _134-the-double-triangle-architecture-md_ …

> - `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` — _216-5-the-economics-of-profession-wide-replication_ - `docs/02-anthropic-vacancies/217-6-risks-specific-to-this…

---

### 100% — `docs/DECISIONS.md` vs `docs/obsidian/DECISIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - identifies potential collaborator/contributor. Андрей — fullstack-разработчик, основатель сообщества, активный в russian-language tech community. Если OKWF будет recruiting первых contributors, имен…

> - **Svyazi‑2.0 нужно начинать не с “самой умной модели”, а с самой строгой структуры переходов между слоями**. Сильная модель без карточного статуса, Evidence Envelope и review protocol быстро превращ…

> - переименовать папку в что-то более описательное , если она действительно реализует routing ( hexagram_routing/ ) или orchestrator ( experiment_orchestrator/ ). «[nautilus](../05-habr-projects/memory…

---

### 100% — `docs/KEYWORD_INDEX.md` vs `docs/obsidian/KEYWORD_INDEX.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Слово | Файлов | Всего упоминаний | |-------|--------|-----------------| | `документ` | 1243 | 5402 | | `кто` | 1236 | 2541 | | `ссылается` | 1235 | 2270 | | `документы` | 1157 | 4053 | | `также` | …

> | Биграмм | Файлов | Всего | |---------|--------|-------| | `смотрите также` | 718 | 3878 | | `reading time` | 698 | 1467 | | `использование смотрите` | 606 | 1390 | | `вакансии anthropic` | 594 | 119…

---

### 100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks | |--------|--------|---------|------|-----|-----------|--------|-----------| | `01-svyazi` | 14 | 🟢 14/14 | 🟢 14/14 | 🟢 14/14…

> - ✅ `docs/04-ai-collaborations/00-intro.md` - ✅ `docs/04-ai-collaborations/01-executive-summary.md` - ✅ `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` - ✅ `docs/04-ai-collaborations/03-карт…

---

### 100% — `docs/KPI_HISTORY.md` vs `docs/obsidian/KPI_HISTORY.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Метрика | Значение | Тренд | |---------|---------|-------| | Markdown документов | **2500** | ↑ +3 | | Слов | **2,878,363** | ↓ -54453 | | Скриптов | **167** | ↑ +1 | | Скоринг | **96%** | → = | | З…

> | Дата | Docs | Слов | Скриптов | Скоринг | Здоровье | |------|------|------|----------|---------|---------| | 2026-05-13 | 2500 | 2,878,363 | 167 | 96% | 99/100 | | 2026-05-12 | 2497 | 2,932,816 | 16…

---

### 100% — `docs/DIGEST.md` vs `docs/obsidian/DIGEST.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Дата | Hash | Описание | |------|------|---------| | 2026-05-13 | `d655c2aa` | fix(docs-toolkit): suppress PytestCollectionWarning for TestResult dat | | 2026-05-13 | `7c934060` | fix: exclude catal…

---

### 100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Сходство | Файл A | Файл B | |----------|--------|--------| | 1.000 | `02-why-document-exists.md` | `01-missing-middle-layer.md` | | 1.000 | `svyazi.md` | `svend4.md` | | 1.000 | `svyazi.md` | `sgb.…

> - `02-why-document-exists.md` ↔ `01-missing-middle-layer.md` (1.000) - `svyazi.md` ↔ `svend4.md` (1.000) - `svyazi.md` ↔ `sgb.md` (1.000) - `svyazi.md` ↔ `nautilus.md` (1.000) - `svend4.md` ↔ `sgb.md`…

---

### 100% — `docs/CROSSREFS.md` vs `docs/obsidian/CROSSREFS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Файл | Проектов | Список | |------|----------|--------| | `docs/TABLES.md` | 30 | Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory +24 | | `docs/obsidian/TABLES.md` | 30 | Svyazi, Ca…

> | Проект | Файлов | Где упоминается | |--------|--------|-----------------| | **AI Factory** | 145 | `docs/01-svyazi/01-executive-summary.md`, `docs/01-svyazi/03-component-catalog.md`, `docs/01-svyazi…

---

### 100% — `docs/TASKS_INDEX.md` vs `docs/obsidian/TASKS_INDEX.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `compare` | Сравнение двух документов / разделов / подходов | "сравни", "в чём разница" | …

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `search` | Полнотекстовый поиск по корпусу | "найди про", "что есть о" | — | search_docs |…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

---

### 100% — `docs/CONCEPT_GRAPH.md` vs `docs/obsidian/CONCEPT_GRAPH.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Концепт | Файлов | Связей | Категория | |---------|--------|--------|-----------| | `документ` | 956 | 13283 | other | | `сходство` | 723 | 11179 | other | | `смотрите` | 692 | 11073 | other | | `та…

> ```mermaid graph TD     документ["документ\n(956)"]     сходство["сходство\n(723)"]     смотрите["смотрите\n(692)"]     также["также\n(687)"]     anthropic["anthropic\n(633)"]     использование["испол…

---

### 100% — `docs/COMPARE.md` vs `docs/obsidian/COMPARE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (19240 слов) - `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (3329 слов) - `docs/02-anthropi…

> | Файл | Было | Стало | Δ | |------|------|-------|---| | `DIGEST_AUTO.md` | 506 | 428 | -78 | | `CONCEPT_GRAPH.md` | 646 | 691 | +45 | | `COMPARE.md` | 477 | 521 | +44 | | `CONSISTENCY.md` | 697 | 65…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` — passport, compatibility, minimal, curious - `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` — compatibility, level, re…

> **Документы:** - `docs/02-anthropic-vacancies/12-content-overview.md` — content, overview, angle, perspective - `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` — triangle, dou…

> - Тема 1: cowork, ingit, turn (2042 документов) - Тема 4: triangle, double, domain (123 документов) - Тема 2: memory, wikontic, yodoca (102 документов) - Тема 3: level, compatibility, bridges (83 доку…

---

### 100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - **Автор:** iximy - **Источник:** Хабр citeturn34view2 - **Лицензия:** неуточнено. citeturn34view2 - **Maturity:** практический implementation guide; публичный код в статье не акцентирован. citeturn3…

---

### 100% — `docs/svyazi-2-0/components/agent-memory-mcp.md` vs `docs/obsidian/svyazi-2-0/components/agent-memory-mcp.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

---

### 100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Автор:** AnastasiyaW - **Источник:** Хабр + GitHub citeturn20view2turn37search0 - **Лицензия:** **MIT**. citeturn37search0 - **Maturity:** активный OSS. citeturn37search0 - **Релевантность к Svyaz…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/badges/README.md` vs `docs/obsidian/badges/README.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> !docs — `docs.svg` !words — `words.svg` !scripts — `scripts.svg` !health — `health.svg` !go/no-go — `scoring.svg` !license — `license.svg` !branch — `branch.svg`

---

### 100% — `docs/letters/vitalysemenov.md` vs `docs/obsidian/letters/vitalysemenov.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Я строю Svyazi 2.0 — локальную knowledge-платформу для Claude. Ключевая задача — дать агенту постоянную типизированную память, которая не зависит от внешних сервисов и работает офлайн. Именно поэтому …

> - Описание того, как agent-memory-mcp + Memory OS закрывают memory-слой   в архитектуре Svyazi 2.0 (задокументировано детально) - Обсуждение, как `CardEnvelope` Svyazi соотносится с типами записей   a…

> Четыре типа записей (`episodic`, `semantic`, `procedural`, `working`) — это точная типизация, которой не хватает большинству memory-систем. В PROTOTYPE_SPEC Svyazi я использую похожее разделение: `fac…

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

> - Тестовый набор из реальных карточек Svyazi для проверки MemNet на   практическом случае (смешанные типы: факты, проекты, люди) - Обсуждение, как MemNet может стать слоем валидации связей поверх   BM…

> Я строю Svyazi 2.0 — локальную систему, которая связывает знания из разных источников через граф. Один из ключевых вопросов, с которым я работаю — как оценивать качество связей в таком графе, не прибе…

---

### 100% — `docs/letters/QA.md` vs `docs/lorenzo-agent/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

### 100% — `docs/letters/QA.md` vs `docs/processing-guide/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

_...и ещё 968 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.
