---
title: "Отчёт о дублировании"
tags:
  - general
date: 2026-05-13
---

# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **988**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/STALENESS.md` vs `docs/obsidian/STALENESS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Файл | Слов | |------|------| | `docs/ai-collaborations/candidates/README.md` | 98 | | `docs/glossary/README.md` | 88 | | `docs/habr-unique-projects/analogues/README.md` | 91 | | `docs/habr-unique-p…

> | Файл | Слов | Проблемы | |------|------|---------| | `docs/MCP_DASHBOARD.md` | 21 | нет summary, нет тегов, короткий (21 слов) | | `docs/autofilled/README.md` | 66 | нет summary, нет тегов, короткий…

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

> ### `GET /api/benchmark` Все 5 критериев успеха PROTOTYPE_SPEC §8 одним запросом. ```bash curl http://localhost:8083/api/benchmark ``` ```json {   "criteria": {     "latency_s":   {"value": 0.21, "thr…

> **Как работает `add_card`:** 1. AI-агент (или пользователь) вызывает `POST /api/cards` или инструмент `add_card` 2. Gateway создаёт `.md` файл в `docs/<section>/` с правильным frontmatter 3. Сбрасывае…

> ### Поиск коллаборации ```bash curl -X POST http://localhost:8083/v1/chat/completions \      -H "Content-Type: application/json" \      -d '{        "model": "lorenzo-gateway",        "messages": [{"r…

---

### 100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - ✅ `docs/04-ai-collaborations/00-intro.md` - ✅ `docs/04-ai-collaborations/01-executive-summary.md` - ✅ `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` - ✅ `docs/04-ai-collaborations/03-карт…

> | Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks | |--------|--------|---------|------|-----|-----------|--------|-----------| | `01-svyazi` | 14 | 🟢 14/14 | 🟢 14/14 | 🟢 14/14…

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

> | Проект | Файлов | Где упоминается | |--------|--------|-----------------| | **AI Factory** | 145 | `docs/01-svyazi/01-executive-summary.md`, `docs/01-svyazi/03-component-catalog.md`, `docs/01-svyazi…

> | Файл | Проектов | Список | |------|----------|--------| | `docs/TABLES.md` | 30 | Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory +24 | | `docs/obsidian/TABLES.md` | 30 | Svyazi, Ca…

---

### 100% — `docs/TASKS_INDEX.md` vs `docs/obsidian/TASKS_INDEX.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `compare` | Сравнение двух документов / разделов / подходов | "сравни", "в чём разница" | …

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо а…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 | |------|---------|---------|---------|---------|---------| | cowork, ingit, turn | cowork | ingit | appendix | turn | svyazi | | triangle, do…

> **Документы:** - `docs/05-habr-projects/01-synthesis.md` — wikontic, yodoca, memory, уникальные - `docs/05-habr-projects/02-collaboration-partners.md` — подобных, статус, wikontic, статьи - `docs/05-h…

> **Документы:** - `docs/02-anthropic-vacancies/06-1-introduction.md` — goals, introduction, merging, federation - `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` — informative, queryresult, …

---

### 100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** iximy - **Источник:** Хабр citeturn34view2 - **Лицензия:** неуточнено. citeturn34view2 - **Maturity:** практический implementation guide; публичный код в статье не акцентирован. citeturn3…

---

### 100% — `docs/svyazi-2-0/components/agent-memory-mcp.md` vs `docs/obsidian/svyazi-2-0/components/agent-memory-mcp.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

---

### 100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** AnastasiyaW - **Источник:** Хабр + GitHub citeturn20view2turn37search0 - **Лицензия:** **MIT**. citeturn37search0 - **Maturity:** активный OSS. citeturn37search0 - **Релевантность к Svyaz…

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

> Я строю Svyazi 2.0 — локальную knowledge-платформу для Claude. Ключевая задача — дать агенту постоянную типизированную память, которая не зависит от внешних сервисов и работает офлайн. Именно поэтому …

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Я строю Svyazi 2.0 — локальную систему, которая связывает знания из разных источников через граф. Один из ключевых вопросов, с которым я работаю — как оценивать качество связей в таком графе, не прибе…

> - Тестовый набор из реальных карточек Svyazi для проверки MemNet на   практическом случае (смешанные типы: факты, проекты, люди) - Обсуждение, как MemNet может стать слоем валидации связей поверх   BM…

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

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

### 100% — `docs/letters/QA.md` vs `docs/contacts/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

### 100% — `docs/letters/QA.md` vs `docs/meta-scripting/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

### 100% — `docs/letters/QA.md` vs `docs/anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

### 100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Как LiteParse обрабатывает таблицы с объединёнными или перенесёнными ячейками? Это самый сложный случай в юридических и финансовых PDF, где данные в ячейке относятся к заголовку в предыдущей строке — …

> Bounding boxes на страницах PDF — это принципиально другой уровень доверия к ответу агента. Когда источник цитаты — не «страница 3», а конкретный визуальный блок на странице, это меняет применимость с…

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

---

### 100% — `docs/04-ai-collaborations/QA.md` vs `docs/05-habr-projects/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

### 100% — `docs/04-ai-collaborations/QA.md` vs `docs/03-technology-combinations/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

### 100% — `docs/04-ai-collaborations/QA.md` vs `docs/02-anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

### 100% — `docs/04-ai-collaborations/QA.md` vs `docs/01-svyazi/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ```bash python scripts/improve_reading_list.py --query "агент с памятью" python scripts/improve_reading_list.py --query "RAG retrieval" --top 20 python scripts/improve_reading_list.py --query "Yodoca"…

> Каждая запись: ```json {   "file": "docs/05-habr-projects/memory/yodoca.md",   "title": "Yodoca: консолидация и забывание",   "content": "Yodoca — Научил ИИ-агента помнить важное...",   "preview": "SQ…

> - Уровни поиска (от простого к сложному) - Уровень 2: Поисковый индекс — improve_search_index.py - Уровень 3: BM25 — improve_keyword_index.py - Уровень 4: Поиск по абзацам — improve_passage_retrieval.…

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

_...и ещё 958 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [CONCEPTS](../CONCEPTS.md)
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

