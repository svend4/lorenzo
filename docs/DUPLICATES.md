# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **991**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/STALENESS.md` vs `docs/obsidian/STALENESS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Файл | Слов | Проблемы | |------|------|---------| | `docs/MCP_DASHBOARD.md` | 21 | нет summary, нет тегов, короткий (21 слов) | | `docs/autofilled/README.md` | 66 | нет summary, нет тегов, короткий…

> | Файл | Слов | |------|------| | `docs/ai-collaborations/candidates/README.md` | 98 | | `docs/glossary/README.md` | 88 | | `docs/habr-unique-projects/analogues/README.md` | 91 | | `docs/habr-unique-p…

---

### 100% — `docs/BADGES.md` vs `docs/obsidian/BADGES.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> ## Markdown сниппеты для README ```markdown !tests !templates !skills !mcp_servers !manifests !scripts !health !validation ```

> - **tests** !tests - **templates** !templates - **skills** !skills - **mcp-servers** !mcp_servers - **manifests** !manifests - **scripts** !scripts - **health** !health - **validation** !validation

---

### 100% — `docs/GATEWAY.md` vs `docs/obsidian/GATEWAY.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ### С function calling ```python response = client.chat.completions.create(     model="lorenzo-gateway",     messages=[{"role": "user", "content": "найди проекты для памяти агента"}],     tools=[{    …

> **Как работает `add_card`:** 1. AI-агент (или пользователь) вызывает `POST /api/cards` или инструмент `add_card` 2. Gateway создаёт `.md` файл в `docs/<section>/` с правильным frontmatter 3. Сбрасывае…

> ### `POST /api/cards` Добавить карточку в корпус (обогащение базы знаний). ```bash curl -X POST http://localhost:8083/api/cards \      -H "Content-Type: application/json" \      -d '{        "title": …

---

### 100% — `docs/DECISIONS.md` vs `docs/obsidian/DECISIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2. > 🏷️ **Ключевые слова:** `svyazi`, `проект`, `cardindex`, `agentfs`, `добавляет`, `продолжение`, `rufler`, `memory` > > [!IMPORTAN…

> - **На Хабре пока не видно одного готового проекта, который уже собрал все слои в единое целое, но видно много авторов, каждый из которых почти идеально закрывает один слой будущей системы.** Поэтому …

> - submission в MCP Registry. У Anthropic есть официальный MCP Registry . После того как portal-mcp.py будет стабилен (пара недель testing), можно submit-ить Nautilus туда. Это даёт внешнюю discoverabi…

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

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо а…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `search` | Полнотекстовый поиск по корпусу | "найди про", "что есть о" | — | search_docs |…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/01-svyazi/00-intro-part2.md` — results, концептов, раздела, граф - `docs/01-svyazi/01-executive-summary.md` — синергии, линия, продолжение, вывод - `docs/01-svyazi/02-methodolog…

> **Документы:** - `docs/COVERAGE.md` — условные, обозначения, heatmap, отсутствует - `docs/DIGEST_WEEKLY.md` — digest, metrics, auto, preview - `docs/HEALTH.md` — балл, broken, links, validation - `doc…

> **Документы:** - `docs/02-anthropic-vacancies/06-1-introduction.md` — goals, introduction, merging, federation - `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` — informative, queryresult, …

---

### 100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Автор:** iximy - **Источник:** Хабр citeturn34view2 - **Лицензия:** неуточнено. citeturn34view2 - **Maturity:** практический implementation guide; публичный код в статье не акцентирован. citeturn3…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/svyazi-2-0/components/agent-memory-mcp.md` vs `docs/obsidian/svyazi-2-0/components/agent-memory-mcp.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

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

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

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

_...и ещё 961 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.
