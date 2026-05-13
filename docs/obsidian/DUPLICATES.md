---
title: "Отчёт о дублировании"
tags:
  - general
date: 2026-05-13
---

# Отчёт о дублировании

<!-- toc -->
## Содержание

- [Похожие файлы (Jaccard ≥ 0.5)](#похожие-файлы-jaccard-05)
  - [100% — `docs/SENTINEL.md` vs `docs/obsidian/SENTINEL.md`](#100-docssentinelmd-vs-docsobsidiansentinelmd)
  - [100% — `docs/CONSISTENCY.md` vs `docs/obsidian/CONSISTENCY.md`](#100-docsconsistencymd-vs-docsobsidianconsistencymd)
  - [100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`](#100-docsprecision_evalmd-vs-docsobsidianprecision_evalmd)
  - [100% — `docs/BADGES.md` vs `docs/obsidian/BADGES.md`](#100-docsbadgesmd-vs-docsobsidianbadgesmd)
  - [100% — `docs/GATEWAY.md` vs `docs/obsidian/GATEWAY.md`](#100-docsgatewaymd-vs-docsobsidiangatewaymd)
  - [100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`](#100-docscoveragemd-vs-docsobsidiancoveragemd)
  - [100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`](#100-docssimilarmd-vs-docsobsidiansimilarmd)
  - [100% — `docs/CROSSREFS.md` vs `docs/obsidian/CROSSREFS.md`](#100-docscrossrefsmd-vs-docsobsidiancrossrefsmd)
  - [100% — `docs/TASKS_INDEX.md` vs `docs/obsidian/TASKS_INDEX.md`](#100-docstasks_indexmd-vs-docsobsidiantasks_indexmd)
  - [100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`](#100-docstopic_modelmd-vs-docsobsidiantopic_modelmd)
  - [100% — `docs/CONTRADICTIONS.md` vs `docs/obsidian/CONTRADICTIONS.md`](#100-docscontradictionsmd-vs-docsobsidiancontradictionsmd)
  - [100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`](#100-docssvyazi-2-0componentshybrid-ragmd-vs-docsobsidiansvyazi-2-0componentshybrid-ragmd)
  - [100% — `docs/svyazi-2-0/components/agent-memory-mcp.md` vs `docs/obsidian/svyazi-2-0/components/agent-memory-mcp.md`](#100-docssvyazi-2-0componentsagent-memory-mcpmd-vs-docsobsidiansvyazi-2-0componentsagent-memory-mcpmd)
  - [100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`](#100-docssvyazi-2-0componentsgraph-ragmd-vs-docsobsidiansvyazi-2-0componentsgraph-ragmd)
  - [100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`](#100-docssvyazi-2-0componentsmclaudemd-vs-docsobsidiansvyazi-2-0componentsmclaudemd)
  - [100% — `docs/badges/README.md` vs `docs/obsidian/badges/README.md`](#100-docsbadgesreadmemd-vs-docsobsidianbadgesreadmemd)
  - [100% — `docs/letters/vitalysemenov.md` vs `docs/obsidian/letters/vitalysemenov.md`](#100-docslettersvitalysemenovmd-vs-docsobsidianlettersvitalysemenovmd)
  - [100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`](#100-docslettersantipozitivemd-vs-docsobsidianlettersantipozitivemd)
  - [100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`](#100-docslettersnlaikmd-vs-docsobsidianlettersnlaikmd)
  - [100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`](#100-docsobsidianprocessing-guide06-searchmd-vs-docsprocessing-guide06-searchmd)
  - [100% — `docs/obsidian/templates/retrospective.md` vs `docs/obsidian/templates/meeting-notes.md`](#100-docsobsidiantemplatesretrospectivemd-vs-docsobsidiantemplatesmeeting-notesmd)
  - [100% — `docs/obsidian/templates/faq-entry.md` vs `docs/obsidian/nautilus/review-methodology/15-appendix-c-history.md`](#100-docsobsidiantemplatesfaq-entrymd-vs-docsobsidiannautilusreview-methodology15-appendix-c-historymd)
  - [100% — `docs/obsidian/templates/faq-entry.md` vs `docs/obsidian/02-anthropic-vacancies/120-главные-технические-риски.md`](#100-docsobsidiantemplatesfaq-entrymd-vs-docsobsidian02-anthropic-vacancies120-главные-технические-рискиmd)
  - [100% — `docs/obsidian/templates/weekly-digest.md` vs `docs/obsidian/nautilus/review-methodology/00-tldr.md`](#100-docsobsidiantemplatesweekly-digestmd-vs-docsobsidiannautilusreview-methodology00-tldrmd)
  - [100% — `docs/obsidian/ai-collaborations/QA.md` vs `docs/ai-collaborations/QA.md`](#100-docsobsidianai-collaborationsqamd-vs-docsai-collaborationsqamd)
  - [100% — `docs/obsidian/05-habr-projects/02-collaboration-partners.md` vs `docs/05-habr-projects/02-collaboration-partners.md`](#100-docsobsidian05-habr-projects02-collaboration-partnersmd-vs-docs05-habr-projects02-collaboration-partnersmd)
  - [100% — `docs/obsidian/nautilus/review-methodology/15-appendix-c-history.md` vs `docs/obsidian/02-anthropic-vacancies/120-главные-технические-риски.md`](#100-docsobsidiannautilusreview-methodology15-appendix-c-historymd-vs-docsobsidian02-anthropic-vacancies120-главные-технические-рискиmd)
  - [100% — `docs/obsidian/anthropic-vacancies/clusters/13-communications.md` vs `docs/obsidian/anthropic-vacancies/clusters/16-people.md`](#100-docsobsidiananthropic-vacanciesclusters13-communicationsmd-vs-docsobsidiananthropic-vacanciesclusters16-peoplemd)
  - [100% — `docs/lorenzo-agent/QA.md` vs `docs/processing-guide/QA.md`](#100-docslorenzo-agentqamd-vs-docsprocessing-guideqamd)
  - [100% — `docs/lorenzo-agent/QA.md` vs `docs/anthropic-vacancies/QA.md`](#100-docslorenzo-agentqamd-vs-docsanthropic-vacanciesqamd)

---


Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **975**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/SENTINEL.md` vs `docs/obsidian/SENTINEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | Лицензия | Риск | |------|----------|------| | `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-` | BSL | Business Source License — не открытая, коммерческие ограниче | | `docs/ob…

> - Итог - PII и секреты - Небезопасный код - Файлы credentials - Лицензионные риски - HTTP без TLS - Использование

> - `http://localhost:8000```````` в `docs/SENTINEL.md` - `http://localhost:8000````````` в `docs/SENTINEL.md` - `http://localhost:8080```````` в `docs/SENTINEL.md` - `http://localhost:8080````````` в `…

---

### 100% — `docs/CONSISTENCY.md` vs `docs/obsidian/CONSISTENCY.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Термин | Канонично | Вариант | Файлов | |--------|-----------|---------|--------| | **knowledge-space** | `knowledge-space` | `knowledgespace` | 6 | | **knowledge-space** | `knowledge-space` | `know…

> - `docs/CONSISTENCY.md` - `docs/obsidian/CONSISTENCY.md` - `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` - `docs/obsidian/02-anthropic-vacancies/365-развёрнутый…

---

### 100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.603 | — | — | | Avg Latency   | 1.106с | ≤ 5.0с…

> | # | Запрос | Rank | Hit | |---|--------|------|-----| | 1 | Yodoca консолидация SQLite decay forgot memory | 4 | ✅ | | 2 | AgentFS файловая система агент vault kksudo | 2 | ✅ | | 3 | NGT Memory ассо…

> > **Примечание:** Hit Rate@K = доля запросов, где хотя бы 1 релевантный > документ попал в топ-K. Стандартный P@K с 1 документом/запрос ≤ 1/K, > поэтому Hit Rate — правильная метрика для этого набора …

---

### 100% — `docs/BADGES.md` vs `docs/obsidian/BADGES.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - **tests** !tests - **templates** !templates - **skills** !skills - **mcp-servers** !mcp_servers - **manifests** !manifests - **scripts** !scripts - **health** !health - **validation** !validation

> ## Markdown сниппеты для README ```markdown !tests !templates !skills !mcp_servers !manifests !scripts !health !validation ```

---

### 100% — `docs/GATEWAY.md` vs `docs/obsidian/GATEWAY.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Что это - Сравнение с DAF-gateway - Архитектура - Запуск - Эндпоинты (`/api/health`, `/api/status`, `/api/benchmark`, `/api/ask`, `/api/search`, `/api/collabs`, `/api/cards`, `/v1/chat/completions`)…

> ### Claude Desktop Добавить в `claude_desktop_config.json`: ```json {   "mcpServers": {     "lorenzo": {       "command": "python",       "args": ["/path/to/scripts/mcp_server.py"]     }   } } ``` > Д…

> | Инструмент | Описание | Параметры | |-----------|---------|----------| | `search` | Гибридный поиск по корпусу | `query`, `top_k` | | `get_card` | Прочитать документ по пути | `path` | | `add_card` …

---

### 100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks | |--------|--------|---------|------|-----|-----------|--------|-----------| | `01-svyazi` | 14 | 🟢 14/14 | 🟢 14/14 | 🟢 14/14…

> - ✅ `docs/04-ai-collaborations/00-intro.md` - ✅ `docs/04-ai-collaborations/01-executive-summary.md` - ✅ `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` - ✅ `docs/04-ai-collaborations/03-карт…

---

### 100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - `02-why-document-exists.md` ↔ `01-missing-middle-layer.md` (1.000) - `svyazi.md` ↔ `svend4.md` (1.000) - `svyazi.md` ↔ `sgb.md` (1.000) - `svyazi.md` ↔ `nautilus.md` (1.000) - `svend4.md` ↔ `sgb.md`…

> | Сходство | Файл A | Файл B | |----------|--------|--------| | 1.000 | `02-why-document-exists.md` | `01-missing-middle-layer.md` | | 1.000 | `svyazi.md` | `svend4.md` | | 1.000 | `svyazi.md` | `sgb.…

---

### 100% — `docs/CROSSREFS.md` vs `docs/obsidian/CROSSREFS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Проект | Файлов | Где упоминается | |--------|--------|-----------------| | **AI Factory** | 147 | `docs/01-svyazi/01-executive-summary.md`, `docs/01-svyazi/03-component-catalog.md`, `docs/01-svyazi…

> | Файл | Проектов | Список | |------|----------|--------| | `docs/TABLES.md` | 30 | Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory +24 | | `docs/obsidian/TABLES.md` | 30 | Svyazi, Ca…

---

### 100% — `docs/TASKS_INDEX.md` vs `docs/obsidian/TASKS_INDEX.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо а…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `search` | Полнотекстовый поиск по корпусу | "найди про", "что есть о" | — | search_docs |…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` — passport, compatibility, minimal, curious - `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` — compatibility, level, re…

> **Документы:** - `docs/05-habr-projects/01-synthesis.md` — wikontic, yodoca, memory, уникальные - `docs/05-habr-projects/02-collaboration-partners.md` — подобных, статус, wikontic, статьи - `docs/05-h…

> **Документы:** - `docs/COVERAGE.md` — условные, обозначения, heatmap, отсутствует - `docs/DIGEST_WEEKLY.md` — digest, metrics, auto, preview - `docs/HEALTH.md` — балл, broken, links, validation - `doc…

---

### 100% — `docs/CONTRADICTIONS.md` vs `docs/obsidian/CONTRADICTIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **A:** `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` > YAML reviewstate: proposalid: "match20260429001" state: "pendingreview" requiredroles: - "evidencereviewer…

> **B:** `docs/01-svyazi/04-ensembles-overview.md` > 1) ^sentinel: OSS-проект: безопасность и allowlist для MCP ^rufler: OSS-проект: оркестратор AI-агентов ^svyazi: Главный проект: экосистема AI-компоне…

> **A:** `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` > Контекст Автор этой статьи непосредственно вовлечён в немецкое социальное право через текущие разбирательства в …

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

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

---

### 100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

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

> Как gardener-loop решает конфликты bi-temporal фактов? Конкретно: если в `episodic` памяти есть запись «X произошло в момент T₁» (время события), добавленная в момент T₂ (время записи), а потом приход…

> - Описание того, как agent-memory-mcp + Memory OS закрывают memory-слой   в архитектуре Svyazi 2.0 (задокументировано детально) - Обсуждение, как `CardEnvelope` Svyazi соотносится с типами записей   a…

> Четыре типа записей (`episodic`, `semantic`, `procedural`, `working`) — это точная типизация, которой не хватает большинству memory-систем. В PROTOTYPE_SPEC Svyazi я использую похожее разделение: `fac…

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

> Я строю Svyazi 2.0 — локальную систему, которая связывает знания из разных источников через граф. Один из ключевых вопросов, с которым я работаю — как оценивать качество связей в таком графе, не прибе…

> - Тестовый набор из реальных карточек Svyazi для проверки MemNet на   практическом случае (смешанные типы: факты, проекты, люди) - Обсуждение, как MemNet может стать слоем валидации связей поверх   BM…

---

### 100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

> Bounding boxes на страницах PDF — это принципиально другой уровень доверия к ответу агента. Когда источник цитаты — не «страница 3», а конкретный визуальный блок на странице, это меняет применимость с…

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Метод | Точность | Скорость | Стоимость | Реализован | |-------|---------|---------|----------|-----------| | grep | низкая | мгновенно | 0 | ✅ | | Полнотекстовый индекс | средняя | быстро | 0 | ✅ |…

> ``` Уровень 1: grep / find                  — быстро, грубо Уровень 2: Поисковый индекс             — полнотекстовый, с preview Уровень 3: BM25 (Okapi)                 — релевантность, не просто вхожд…

> **BM25 (Best Match 25)** — стандарт информационного поиска. Лучше TF-IDF: - Учитывает насыщенность документа (term saturation) - Учитывает длину документа (document length normalization) - Параметры: …

---

### 100% — `docs/obsidian/templates/retrospective.md` vs `docs/obsidian/templates/meeting-notes.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/obsidian/templates/faq-entry.md` vs `docs/obsidian/nautilus/review-methodology/15-appendix-c-history.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/obsidian/templates/faq-entry.md` vs `docs/obsidian/02-anthropic-vacancies/120-главные-технические-риски.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/obsidian/templates/weekly-digest.md` vs `docs/obsidian/nautilus/review-methodology/00-tldr.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/obsidian/ai-collaborations/QA.md` vs `docs/ai-collaborations/QA.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - Содержание - Как реализован forensic RAG с доказуемостью? - Что такое Evidence Envelope и зачем он нужен? - Какие RAG-подходы сравниваются в документах? - Как работает AgentFS и что такое .agentos? …

> Документ индексирован в базе знаний репозитория Lorenzo. Навигация осуществляется через семантический поиск и граф концептов. Информация актуальна и регулярно обновляется скриптами обработки. Все данн…

---

### 100% — `docs/obsidian/05-habr-projects/02-collaboration-partners.md` vs `docs/05-habr-projects/02-collaboration-partners.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > автора статьи выше подобных авторов подобных разработчиков или ещё может быть или может быть даже несколько проектов которые вместе можно совместить и которые дойдут вместе один уни…

> - Статус - Похожие документы - Использование - Смотрите также - Кто ссылается на этот документ (4)

> Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Понял суть статьи. Андрей Чуян построил систем…

---

### 100% — `docs/obsidian/nautilus/review-methodology/15-appendix-c-history.md` vs `docs/obsidian/02-anthropic-vacancies/120-главные-технические-риски.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/obsidian/anthropic-vacancies/clusters/13-communications.md` vs `docs/obsidian/anthropic-vacancies/clusters/16-people.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/lorenzo-agent/QA.md` vs `docs/processing-guide/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

### 100% — `docs/lorenzo-agent/QA.md` vs `docs/anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

_...и ещё 945 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- backlinks -->

---

**Кто ссылается на этот документ (18):**
- [[02-methodology]]
- [[197-7-управление-и-надзор]]
- [[02-методика-и-рамка-отбора]]
- [[CONCEPTS]]
- [[EMPTY_SECTIONS]]
- [[LLM_SUMMARIES]]
- [[OUTLINE]]
- [[PRECISION_EVAL]]
- _...ещё 10_

