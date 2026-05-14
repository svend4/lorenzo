# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **937**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/CARD_GRAPH.md` vs `docs/obsidian/CARD_GRAPH.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> **rag** (507 карточек): `03-component-catalog`, `components-by-name`, `concepts` **anthropic** (443 карточек): `13-communications`, `00-question-habr-link`, `17-appendix-b-change-log` **architecture**…

> | # | PageRank | In | Out | Путь | Теги | |---|----------|----|----|------|------| | 1 | 1.000 | 1501 | 5 | `docs/autofilled/README.md` · autofilled | collaboration | | 2 | 0.434 | 44 | 40 | `docs/aut…

---

### 100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.441 | — | — | | Avg Latency   | 1.251с | ≤ 5.0с…

> - **Метрика:** Hit Rate@10 — доля запросов с ≥1 релевантным документом в топ-10. - **Поиск:** `hybrid_search()` = 0.6×TF-IDF + 0.4×BM25 с фильтром шумовых документов. - **Фильтр шума:** исключаются me…

> | # | Запрос | Rank | Hit | |---|--------|------|-----| | 1 | Yodoca консолидация SQLite decay forgot memory | 1 | ✅ | | 2 | AgentFS файловая система агент vault kksudo | 3 | ✅ | | 3 | NGT Memory ассо…

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

> ``` ┌─────────────────────────────────────────────┐ │   Любой AI-клиент                           │ │   (Claude Desktop / Cursor / GPT / агент)   │ └─────────────────┬───────────────────────────┘     …

> ### Поиск коллаборации ```bash curl -X POST http://localhost:8083/v1/chat/completions \      -H "Content-Type: application/json" \      -d '{        "model": "lorenzo-gateway",        "messages": [{"r…

> ### `POST /api/cards` Добавить карточку в корпус (обогащение базы знаний). ```bash curl -X POST http://localhost:8083/api/cards \      -H "Content-Type: application/json" \      -d '{        "title": …

---

### 100% — `docs/DECISIONS.md` vs `docs/obsidian/DECISIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - переориентировать стратегию OKWF : начать с гильдийных Профессиональных Коллег, как первый продукт фонда. Использовать SGB-domain как pilot domain (используя ваш expertise). Если будете писать compa…

> - из memory-проектов, которые я изучил. **Что именно ценно:** Механизм decay в Yodoca отвечает на вопрос, который я не смог закрыть через другие подходы: как система сама решает, что устарело, а не жд…

> - отменить без явного `restore_event`. ### Идемпотентность Перед записью `episode` и `fact` выполняется проверка дубликата (cosine ≥ 0.85 по title+bod     _→ RFC-0002-memory-write-policy-для-svyazi-2-…

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

### 100% — `docs/PROMOTE_LOG.md` vs `docs/obsidian/PROMOTE_LOG.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ### normalized → approved (597) - `docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` - `docs/processing-guide/PROCESSING_GUIDE.md` - `docs/02-anthropic-vacancies/133-обратная-связь.md` -…

> ### normalized → approved (272) - `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` - `docs/04-ai-collaborations/00-intro.md` - `docs/02-anthropic-vacancies/342-что-такое-вариант-…

> ### raw → normalized (311) - `docs/processing-guide/PROCESSING_GUIDE.md` - `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` - `docs/02-anthropic-vacancies/248-приложение-c-а…

---

### 100% — `docs/SKILL_METRICS.md` vs `docs/obsidian/SKILL_METRICS.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Скил | Score | Struct | Len | Examples | Steps | Tools | Clarity | Uses | Words | |------|-------|--------|-----|----------|-------|-------|---------|------|-------| | ✅ `review-docs` | **94** | 10 …

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

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сей…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо а…

> | Task ID | Описание | Триггеры | Шаблон | MCP tool | |---------|----------|----------|--------|----------| | `compare` | Сравнение двух документов / разделов / подходов | "сравни", "в чём разница" | …

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` — passport, compatibility, minimal, curious - `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` — compatibility, level, re…

> **Документы:** - `docs/05-habr-projects/01-synthesis.md` — wikontic, yodoca, memory, уникальные - `docs/05-habr-projects/02-collaboration-partners.md` — подобных, статус, wikontic, статьи - `docs/05-h…

> | Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 | |------|---------|---------|---------|---------|---------| | cowork, ingit, turn | cowork | ingit | appendix | turn | svyazi | | triangle, do…

---

### 100% — `docs/CONTRADICTIONS.md` vs `docs/obsidian/CONTRADICTIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **B:** `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` > 1) ^sentinel: OSS-проект: безопасность и allowlist для MCP ^svyazi: Главный проект: экосистема AI-компонен…

> **B:** `docs/01-svyazi/04-ensembles-overview.md` > 1) ^sentinel: OSS-проект: безопасность и allowlist для MCP ^rufler: OSS-проект: оркестратор AI-агентов ^svyazi: Главный проект: экосистема AI-компоне…

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

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Автор: VitaliySemenov / moshael Проекты: Svyazi, agent-memory-mcp > Документ создан на основе …

> - **Автор:** VitaliySemenov / moshael - **Источник:** Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 - **Лицензия:** для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. cit…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

---

### 100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Автор: VladSpace / vpakspace Проекты: Svyazi, Graph RAG Автор: VladSpace / vpakspace > Докумен…

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > [!NOTE] > Документ создан на основе исследования. Ссылки ведут на связанные материалы. Источник: Хабр + GitHub citeturn20view2turn37search0 Источник: Хабр + GitHub citeturn20view2tu…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

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

> Как gardener-loop решает конфликты bi-temporal фактов? Конкретно: если в `episodic` памяти есть запись «X произошло в момент T₁» (время события), добавленная в момент T₂ (время записи), а потом приход…

> - Описание того, как agent-memory-mcp + Memory OS закрывают memory-слой   в архитектуре Svyazi 2.0 (задокументировано детально) - Обсуждение, как `CardEnvelope` Svyazi соотносится с типами записей   a…

> <!-- summary --> > Открытое письмо автору agent-memory-mcp — типизированного MCP-сервера памяти для AI-агентов с SQLite, четырьмя типами записей и Memory OS концепцией. Документ создан на основе иссле…

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > Открытое письмо автору MemNet — исследовательского проекта по ассоциативной памяти для LLM с формальными метриками качества связей. Документ содержит практические рекомендации и луч…

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

> - Тестовый набор из реальных карточек Svyazi для проверки MemNet на   практическом случае (смешанные типы: факты, проекты, люди) - Обсуждение, как MemNet может стать слоем валидации связей поверх   BM…

---

### 100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Bounding boxes на страницах PDF — это принципиально другой уровень доверия к ответу агента. Когда источник цитаты — не «страница 3», а конкретный визуальный блок на странице, это меняет применимость с…

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Результат:** ``` 1. [0.847] docs/05-habr-projects/memory/yodoca.md §"hot path"    "разделение на hot path (запись эпизодов в SQLite + FTS5 за <50 мс, без LLM) и     slow path (асинхронные эмбеддинги…

> **BM25 (Best Match 25)** — стандарт информационного поиска. Лучше TF-IDF: - Учитывает насыщенность документа (term saturation) - Учитывает длину документа (document length normalization) - Параметры: …

> | Метод | Точность | Скорость | Стоимость | Реализован | |-------|---------|---------|----------|-----------| | grep | низкая | мгновенно | 0 | ✅ | | Полнотекстовый индекс | средняя | быстро | 0 | ✅ |…

---

### 100% — `docs/obsidian/ai-collaborations/QA.md` vs `docs/ai-collaborations/QA.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория Lorenzo. Навигация осуществляется через семантический поиск и граф концептов. Информация актуальна и регулярно обновляется скриптами обработки. Все данн…

> <!-- summary --> > _Смотрите также: README · Глоссарий · Контакты_ Кто ссылается на этот документ (5): Документ содержит структурированную информацию из базы знаний репозитория Lorenzo.  -- Кто ссылае…

> - Содержание - Как реализован forensic RAG с доказуемостью? - Что такое Evidence Envelope и зачем он нужен? - Какие RAG-подходы сравниваются в документах? - Как работает AgentFS и что такое .agentos? …

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

> - Статус - Похожие документы - Использование - Смотрите также - Кто ссылается на этот документ (4)

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Авторы и контакты Статус Параметр Значение ------------------- Теги — Упоминаний в репо — Слой — Контакт — Статус связи не писали Обнов…

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

> <!-- summary --> > Раздел QA формируется автоматически из данных репозитория. Кто ссылается на этот документ (6):   Смотрите также  Главная  Метрики  Здоровье  Глоссарий  Сущности  -- Кто ссылается на…

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

_...и ещё 907 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.
