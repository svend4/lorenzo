---
title: "Отчёт о дублировании"
tags:
  - general
date: 2026-06-05
---

# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **935**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/CARD_GRAPH.md` vs `docs/obsidian/CARD_GRAPH.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | # | PageRank | In | Out | Путь | Теги | |---|----------|----|----|------|------| | 1 | 1.000 | 1501 | 5 | `docs/autofilled/README.md` · autofilled | collaboration | | 2 | 0.434 | 44 | 40 | `docs/aut…

> **rag** (507 карточек): `03-component-catalog`, `components-by-name`, `concepts` **anthropic** (443 карточек): `13-communications`, `00-question-habr-link`, `17-appendix-b-change-log` **architecture**…

---

### 100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> > **Примечание:** Hit Rate@K = доля запросов, где хотя бы 1 релевантный > документ попал в топ-K. Стандартный P@K с 1 документом/запрос ≤ 1/K, > поэтому Hit Rate — правильная метрика для этого набора …

> - **Метрика:** Hit Rate@10 — доля запросов с ≥1 релевантным документом в топ-10. - **Поиск:** `hybrid_search()` = 0.6×TF-IDF + 0.4×BM25 с фильтром шумовых документов. - **Фильтр шума:** исключаются me…

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.441 | — | — | | Avg Latency   | 1.251с | ≤ 5.0с…

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

> **Полный цикл обогащения:** ``` Внешний источник (статья, разговор, результат анализа)     ↓ AI-агент анализирует и структурирует     ↓ POST /api/cards  →  docs/04-ai-collaborations/<slug>.md     ↓ py…

> **Зачем:** любой AI-агент (Claude Desktop, Cursor, GPT-клиент, другой агент) может подключиться по OpenAI-протоколу и: - **читать** корпус через гибридный поиск (BM25 + TF-IDF) - **обогащать** его — д…

> - Содержание - Что это - Сравнение с DAF-gateway - Архитектура - Запуск - Эндпоинты   - `GET /api/health`   - `GET /api/status`   - `GET /api/benchmark`   - `POST /api/ask`   - `POST /api/search`   - …

---

### 100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks | |--------|--------|---------|------|-----|-----------|--------|-----------| | `01-svyazi` | 14 | 🟢 14/14 | 🟢 14/14 | 🟢 14/14…

> - ✅ `docs/04-ai-collaborations/00-intro.md` - ✅ `docs/04-ai-collaborations/01-executive-summary.md` - ✅ `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` - ✅ `docs/04-ai-collaborations/03-карт…

---

### 100% — `docs/DIGEST.md` vs `docs/obsidian/DIGEST.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Дата | Hash | Описание | |------|------|---------| | 2026-05-13 | `d655c2aa` | fix(docs-toolkit): suppress PytestCollectionWarning for TestResult dat | | 2026-05-13 | `7c934060` | fix: exclude catal…

---

### 100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - `02-why-document-exists.md` ↔ `01-missing-middle-layer.md` (1.000) - `svyazi.md` ↔ `svend4.md` (1.000) - `svyazi.md` ↔ `sgb.md` (1.000) - `svyazi.md` ↔ `nautilus.md` (1.000) - `svend4.md` ↔ `sgb.md`…

> | Сходство | Файл A | Файл B | |----------|--------|--------| | 1.000 | `02-why-document-exists.md` | `01-missing-middle-layer.md` | | 1.000 | `svyazi.md` | `svend4.md` | | 1.000 | `svyazi.md` | `sgb.…

---

### 100% — `docs/PROMOTE_LOG.md` vs `docs/obsidian/PROMOTE_LOG.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ### raw → normalized (311) - `docs/processing-guide/PROCESSING_GUIDE.md` - `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` - `docs/02-anthropic-vacancies/248-приложение-c-а…

> ### normalized → approved (46) - `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` - `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеив…

> ### normalized → approved (70) - `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` - `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` -…

---

### 100% — `docs/SKILL_METRICS.md` vs `docs/obsidian/SKILL_METRICS.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Скил | Score | Struct | Len | Examples | Steps | Tools | Clarity | Uses | Words | |------|-------|--------|-----|----------|-------|-------|---------|------|-------| | ✅ `review-docs` | **94** | 10 …

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

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `search` | Полнотекстовый поиск по корпусу | "найди про", "что есть о" | — | search_docs |…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо а…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/02-anthropic-vacancies/06-1-introduction.md` — goals, introduction, merging, federation - `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` — informative, queryresult, …

> - Тема 1: cowork, ingit, turn (2042 документов) - Тема 4: triangle, double, domain (123 документов) - Тема 2: memory, wikontic, yodoca (102 документов) - Тема 3: level, compatibility, bridges (83 доку…

> | Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 | |------|---------|---------|---------|---------|---------| | cowork, ingit, turn | cowork | ingit | appendix | turn | svyazi | | triangle, do…

---

### 100% — `docs/CONTRADICTIONS.md` vs `docs/obsidian/CONTRADICTIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **B:** `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` > YAML reviewstate: proposalid: "match20260429001" state: "pendingreview" requiredroles: - "evidencereviewer" - "privacyreviewer…

> **B:** `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` > 1) ^sentinel: OSS-проект: безопасность и allowlist для MCP ^svyazi: Главный проект: экосистема AI-компонен…

> **B:** `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md` > Фаза 2 — Расширение Областей (Годы 3-4) Деятельность: - Добавить области 2 (профессионалы на пенсии) и 8 (студен…

---

### 100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Источник: Хабр citeturn34view2 Проекты: Svyazi, Hybrid RAG Источник: Хабр citeturn34view2 > До…

> - **Автор:** iximy - **Источник:** Хабр citeturn34view2 - **Лицензия:** неуточнено. citeturn34view2 - **Maturity:** практический implementation guide; публичный код в статье не акцентирован. citeturn3…

---

### 100% — `docs/svyazi-2-0/components/agent-memory-mcp.md` vs `docs/obsidian/svyazi-2-0/components/agent-memory-mcp.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

---

### 100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Автор: VladSpace / vpakspace Проекты: Svyazi, Graph RAG Автор: VladSpace / vpakspace > Докумен…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Источник: Хабр + GitHub citeturn20view2turn37search0 Источник: Хабр + GitHub citeturn20view2tu…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

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

> Я строю Svyazi 2.0 — локальную knowledge-платформу для Claude. Ключевая задача — дать агенту постоянную типизированную память, которая не зависит от внешних сервисов и работает офлайн. Именно поэтому …

> - Описание того, как agent-memory-mcp + Memory OS закрывают memory-слой   в архитектуре Svyazi 2.0 (задокументировано детально) - Обсуждение, как `CardEnvelope` Svyazi соотносится с типами записей   a…

> Четыре типа записей (`episodic`, `semantic`, `procedural`, `working`) — это точная типизация, которой не хватает большинству memory-систем. В PROTOTYPE_SPEC Svyazi я использую похожее разделение: `fac…

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Тестовый набор из реальных карточек Svyazi для проверки MemNet на   практическом случае (смешанные типы: факты, проекты, люди) - Обсуждение, как MemNet может стать слоем валидации связей поверх   BM…

> <!-- summary --> > Открытое письмо автору MemNet — исследовательского проекта по ассоциативной памяти для LLM с формальными метриками качества связей. Документ содержит практические рекомендации и луч…

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

---

### 100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

> Как LiteParse обрабатывает таблицы с объединёнными или перенесёнными ячейками? Это самый сложный случай в юридических и финансовых PDF, где данные в ячейке относятся к заголовку в предыдущей строке — …

> Bounding boxes на страницах PDF — это принципиально другой уровень доверия к ответу агента. Когда источник цитаты — не «страница 3», а конкретный визуальный блок на странице, это меняет применимость с…

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Каждая запись: ```json {   "file": "docs/05-habr-projects/memory/yodoca.md",   "title": "Yodoca: консолидация и забывание",   "content": "Yodoca — Научил ИИ-агента помнить важное...",   "preview": "SQ…

> <!-- summary --> > Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь. Уровни поиска (от простого к сложному) Уровень 2: Поисковый индекс — improve_search_index.py У…

> ```bash python scripts/improve_reading_list.py --query "агент с памятью" python scripts/improve_reading_list.py --query "RAG retrieval" --top 20 python scripts/improve_reading_list.py --query "Yodoca"…

---

### 100% — `docs/obsidian/ai-collaborations/QA.md` vs `docs/ai-collaborations/QA.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > _Смотрите также: README · Глоссарий · Контакты_ Кто ссылается на этот документ (5): Документ содержит структурированную информацию из базы знаний репозитория Lorenzo.  -- Кто ссылае…

> - Содержание - Как реализован forensic RAG с доказуемостью? - Что такое Evidence Envelope и зачем он нужен? - Какие RAG-подходы сравниваются в документах? - Как работает AgentFS и что такое .agentos? …

> Документ индексирован в базе знаний репозитория Lorenzo. Навигация осуществляется через семантический поиск и граф концептов. Информация актуальна и регулярно обновляется скриптами обработки. Все данн…

---

### 100% — `docs/obsidian/contacts/QA.md` vs `docs/obsidian/meta-scripting/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

---

### 100% — `docs/obsidian/contacts/QA.md` vs `docs/obsidian/anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

---

### 100% — `docs/obsidian/05-habr-projects/02-collaboration-partners.md` vs `docs/05-habr-projects/02-collaboration-partners.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Авторы и контакты Статус Параметр Значение ------------------- Теги — Упоминаний в репо — Слой — Контакт — Статус связи не писали Обнов…

> - Статус - Похожие документы - Использование - Смотрите также - Кто ссылается на этот документ (4)

> Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Понял суть статьи. Андрей Чуян построил систем…

---

### 100% — `docs/obsidian/meta-scripting/QA.md` vs `docs/obsidian/anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

---

### 100% — `docs/obsidian/anthropic-vacancies/clusters/13-communications.md` vs `docs/obsidian/anthropic-vacancies/clusters/16-people.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/contacts/QA.md` vs `docs/meta-scripting/QA.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

---

### 100% — `docs/contacts/QA.md` vs `docs/anthropic-vacancies/QA.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

---

_...и ещё 905 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.
