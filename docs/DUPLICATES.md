# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **938**

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

> | # | Запрос | Rank | Hit | |---|--------|------|-----| | 1 | Yodoca консолидация SQLite decay forgot memory | 1 | ✅ | | 2 | AgentFS файловая система агент vault kksudo | 3 | ✅ | | 3 | NGT Memory ассо…

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.441 | — | — | | Avg Latency   | 1.251с | ≤ 5.0с…

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

> ### Простой поиск ```bash curl -X POST http://localhost:8083/v1/chat/completions \      -H "Content-Type: application/json" \      -d '{        "model": "lorenzo-gateway",        "messages": [{"role":…

> - Что это - Сравнение с DAF-gateway - Архитектура - Запуск - Эндпоинты (`/api/health`, `/api/status`, `/api/benchmark`, `/api/ask`, `/api/search`, `/api/collabs`, `/api/cards`, `/v1/chat/completions`)…

> ### Обогащение корпуса через chat ```bash # Инструмент add_card создаёт .md файл в docs/ и сбрасывает кэш индекса curl -X POST http://localhost:8083/v1/chat/completions \      -H "Content-Type: applic…

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

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `compare` | Сравнение двух документов / разделов / подходов | "сравни", "в чём разница" | …

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `search` | Полнотекстовый поиск по корпусу | "найди про", "что есть о" | — | search_docs |…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` — passport, compatibility, minimal, curious - `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` — compatibility, level, re…

> **Документы:** - `docs/01-svyazi/00-intro-part2.md` — results, концептов, раздела, граф - `docs/01-svyazi/01-executive-summary.md` — синергии, линия, продолжение, вывод - `docs/01-svyazi/02-methodolog…

> - Тема 1: cowork, ingit, turn (2042 документов) - Тема 4: triangle, double, domain (123 документов) - Тема 2: memory, wikontic, yodoca (102 документов) - Тема 3: level, compatibility, bridges (83 доку…

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

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

---

### 100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Автор: VladSpace / vpakspace Проекты: Svyazi, Graph RAG Автор: VladSpace / vpakspace > Докумен…

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Источник: Хабр + GitHub citeturn20view2turn37search0 Источник: Хабр + GitHub citeturn20view2tu…

> - **Автор:** AnastasiyaW - **Источник:** Хабр + GitHub citeturn20view2turn37search0 - **Лицензия:** **MIT**. citeturn37search0 - **Maturity:** активный OSS. citeturn37search0 - **Релевантность к Svyaz…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

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

> Как gardener-loop решает конфликты bi-temporal фактов? Конкретно: если в `episodic` памяти есть запись «X произошло в момент T₁» (время события), добавленная в момент T₂ (время записи), а потом приход…

> <!-- summary --> > Открытое письмо автору agent-memory-mcp — типизированного MCP-сервера памяти для AI-агентов с SQLite, четырьмя типами записей и Memory OS концепцией. Документ создан на основе иссле…

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Я строю Svyazi 2.0 — локальную систему, которая связывает знания из разных источников через граф. Один из ключевых вопросов, с которым я работаю — как оценивать качество связей в таком графе, не прибе…

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

> <!-- summary --> > Открытое письмо автору MemNet — исследовательского проекта по ассоциативной памяти для LLM с формальными метриками качества связей. Документ содержит практические рекомендации и луч…

---

### 100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

> Как LiteParse обрабатывает таблицы с объединёнными или перенесёнными ячейками? Это самый сложный случай в юридических и финансовых PDF, где данные в ячейке относятся к заголовку в предыдущей строке — …

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Метод | Точность | Скорость | Стоимость | Реализован | |-------|---------|---------|----------|-----------| | grep | низкая | мгновенно | 0 | ✅ | | Полнотекстовый индекс | средняя | быстро | 0 | ✅ |…

> ``` Уровень 1: grep / find                  — быстро, грубо Уровень 2: Поисковый индекс             — полнотекстовый, с preview Уровень 3: BM25 (Okapi)                 — релевантность, не просто вхожд…

> ```bash python scripts/improve_reading_list.py --query "агент с памятью" python scripts/improve_reading_list.py --query "RAG retrieval" --top 20 python scripts/improve_reading_list.py --query "Yodoca"…

---

### 100% — `docs/obsidian/ai-collaborations/QA.md` vs `docs/ai-collaborations/QA.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Содержание - Как реализован forensic RAG с доказуемостью? - Что такое Evidence Envelope и зачем он нужен? - Какие RAG-подходы сравниваются в документах? - Как работает AgentFS и что такое .agentos? …

> Документ индексирован в базе знаний репозитория Lorenzo. Навигация осуществляется через семантический поиск и граф концептов. Информация актуальна и регулярно обновляется скриптами обработки. Все данн…

> <!-- summary --> > _Смотрите также: README · Глоссарий · Контакты_ Кто ссылается на этот документ (5): Документ содержит структурированную информацию из базы знаний репозитория Lorenzo.  -- Кто ссылае…

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

> <!-- summary --> > автора статьи выше подобных авторов подобных разработчиков или ещё может быть или может быть даже несколько проектов которые вместе можно совместить и которые дойдут вместе один уни…

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Авторы и контакты Статус Параметр Значение ------------------- Теги — Упоминаний в репо — Слой — Контакт — Статус связи не писали Обнов…

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

### 100% — `docs/meta-scripting/QA.md` vs `docs/anthropic-vacancies/QA.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

---

### 99% — `docs/PRIORITIES.md` vs `docs/obsidian/PRIORITIES.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | Score | |------|-------| | `docs/obsidian/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md` | 4.71 | | `docs/nautilus/community-discussions/habr-article-1-reaction…

> | Файл | Score | |------|-------| | `docs/obsidian/meta-scripting/05-synthesis.md` | 2.02 | | `docs/meta-scripting/05-synthesis.md` | 2.02 | | `docs/obsidian/meta-scripting/02-architecture.md` | 0.31 …

> | Файл | Score | |------|-------| | `docs/obsidian/nautilus/privacy-federation/03-what-this-gives-technically.md` | 1.22 | | `docs/nautilus/privacy-federation/03-what-this-gives-technically.md` | 0.81…

---

_...и ещё 908 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- see-also -->

---

**Смотрите также:**
- [TOPIC_MODEL](TOPIC_MODEL.md)
- [VERSION_DIFF](VERSION_DIFF.md)
- [antipozitive](letters/antipozitive.md)
- [WORD_FREQ](WORD_FREQ.md)

