# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **973**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/SENTINEL.md` vs `docs/obsidian/SENTINEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | Строка | Проблема | Фрагмент | |------|--------|----------|----------| | `scripts/gateway.py` | 655 | __import__() dynamic import | `t0      = __import__("time").time()` | | `scripts/gateway.…

> - `http://localhost:8000```````` в `docs/SENTINEL.md` - `http://localhost:8000````````` в `docs/SENTINEL.md` - `http://localhost:8080```````` в `docs/SENTINEL.md` - `http://localhost:8080````````` в `…

> | Категория | Найдено | |-----------|---------| | PII / секреты в docs | 0 | | Небезопасные паттерны в коде | 3 | | Credential-файлы | 0 | | HTTP (не HTTPS) ссылок | 445 | | Лицензионных рисков | 4 | …

---

### 100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> > **Примечание:** Hit Rate@K = доля запросов, где хотя бы 1 релевантный > документ попал в топ-K. Стандартный P@K с 1 документом/запрос ≤ 1/K, > поэтому Hit Rate — правильная метрика для этого набора …

> | # | Запрос | Rank | Hit | |---|--------|------|-----| | 1 | Yodoca консолидация SQLite decay forgot memory | 4 | ✅ | | 2 | AgentFS файловая система агент vault kksudo | 2 | ✅ | | 3 | NGT Memory ассо…

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.603 | — | — | | Avg Latency   | 1.106с | ≤ 5.0с…

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

> ### Простой поиск ```bash curl -X POST http://localhost:8083/v1/chat/completions \      -H "Content-Type: application/json" \      -d '{        "model": "lorenzo-gateway",        "messages": [{"role":…

---

### 100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - ✅ `docs/04-ai-collaborations/00-intro.md` - ✅ `docs/04-ai-collaborations/01-executive-summary.md` - ✅ `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` - ✅ `docs/04-ai-collaborations/03-карт…

> | Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks | |--------|--------|---------|------|-----|-----------|--------|-----------| | `01-svyazi` | 14 | 🟢 14/14 | 🟢 14/14 | 🟢 14/14…

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

> | Файл | Проектов | Список | |------|----------|--------| | `docs/TABLES.md` | 30 | Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory +24 | | `docs/obsidian/TABLES.md` | 30 | Svyazi, Ca…

> | Проект | Файлов | Где упоминается | |--------|--------|-----------------| | **AI Factory** | 147 | `docs/01-svyazi/01-executive-summary.md`, `docs/01-svyazi/03-component-catalog.md`, `docs/01-svyazi…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/COVERAGE.md` — условные, обозначения, heatmap, отсутствует - `docs/DIGEST_WEEKLY.md` — digest, metrics, auto, preview - `docs/HEALTH.md` — балл, broken, links, validation - `doc…

> - Тема 1: cowork, ingit, turn (2042 документов) - Тема 4: triangle, double, domain (123 документов) - Тема 2: memory, wikontic, yodoca (102 документов) - Тема 3: level, compatibility, bridges (83 доку…

> | Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 | |------|---------|---------|---------|---------|---------| | cowork, ingit, turn | cowork | ingit | appendix | turn | svyazi | | triangle, do…

---

### 100% — `docs/CONTRADICTIONS.md` vs `docs/obsidian/CONTRADICTIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **A:** `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` > YAML reviewstate: proposalid: "match20260429001" state: "pendingreview" requiredroles: - "evidencereviewer…

> **A:** `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` > md) --- ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Model — большая языковая модель ^cardin…

> **B:** `docs/01-svyazi/04-ensembles-overview.md` > 1) ^sentinel: OSS-проект: безопасность и allowlist для MCP ^rufler: OSS-проект: оркестратор AI-агентов ^svyazi: Главный проект: экосистема AI-компоне…

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

> - Описание того, как agent-memory-mcp + Memory OS закрывают memory-слой   в архитектуре Svyazi 2.0 (задокументировано детально) - Обсуждение, как `CardEnvelope` Svyazi соотносится с типами записей   a…

> Четыре типа записей (`episodic`, `semantic`, `procedural`, `working`) — это точная типизация, которой не хватает большинству memory-систем. В PROTOTYPE_SPEC Svyazi я использую похожее разделение: `fac…

> Как gardener-loop решает конфликты bi-temporal фактов? Конкретно: если в `episodic` памяти есть запись «X произошло в момент T₁» (время события), добавленная в момент T₂ (время записи), а потом приход…

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

> Bounding boxes на страницах PDF — это принципиально другой уровень доверия к ответу агента. Когда источник цитаты — не «страница 3», а конкретный визуальный блок на странице, это меняет применимость с…

> Как LiteParse обрабатывает таблицы с объединёнными или перенесёнными ячейками? Это самый сложный случай в юридических и финансовых PDF, где данные в ячейке относятся к заголовку в предыдущей строке — …

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Каждая запись: ```json {   "file": "docs/05-habr-projects/memory/yodoca.md",   "title": "Yodoca: консолидация и забывание",   "content": "Yodoca — Научил ИИ-агента помнить важное...",   "preview": "SQ…

> | Метод | Точность | Скорость | Стоимость | Реализован | |-------|---------|---------|----------|-----------| | grep | низкая | мгновенно | 0 | ✅ | | Полнотекстовый индекс | средняя | быстро | 0 | ✅ |…

> ``` Уровень 1: grep / find                  — быстро, грубо Уровень 2: Поисковый индекс             — полнотекстовый, с preview Уровень 3: BM25 (Okapi)                 — релевантность, не просто вхожд…

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

> Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Понял суть статьи. Андрей Чуян построил систем…

> <!-- summary --> > автора статьи выше подобных авторов подобных разработчиков или ещё может быть или может быть даже несколько проектов которые вместе можно совместить и которые дойдут вместе один уни…

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Авторы и контакты Статус Параметр Значение ------------------- Теги — Упоминаний в репо — Слой — Контакт — Статус связи не писали Обнов…

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

### 100% — `docs/processing-guide/QA.md` vs `docs/anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES - README

---

### 100% — `docs/03-technology-combinations/QA.md` vs `docs/02-anthropic-vacancies/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

_...и ещё 943 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.
