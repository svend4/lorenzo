---
title: "Отчёт о дублировании"
tags:
  - general
date: 2026-05-12
---

# Отчёт о дублировании

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **974**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/SENTINEL.md` vs `docs/obsidian/SENTINEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | Строка | Проблема | Фрагмент | |------|--------|----------|----------| | `scripts/gateway.py` | 655 | __import__() dynamic import | `t0      = __import__("time").time()` | | `scripts/gateway.…

> - `http://localhost:8000```````` в `docs/SENTINEL.md` - `http://localhost:8000````````` в `docs/SENTINEL.md` - `http://localhost:8080```````` в `docs/SENTINEL.md` - `http://localhost:8080````````` в `…

> - Итог - PII и секреты - Небезопасный код - Файлы credentials - Лицензионные риски - HTTP без TLS - Использование

---

### 100% — `docs/CONSISTENCY.md` vs `docs/obsidian/CONSISTENCY.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - `docs/CONSISTENCY.md` - `docs/obsidian/CONSISTENCY.md` - `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` - `docs/obsidian/02-anthropic-vacancies/365-развёрнутый…

> | Термин | Канонично | Вариант | Файлов | |--------|-----------|---------|--------| | **knowledge-space** | `knowledge-space` | `knowledgespace` | 6 | | **knowledge-space** | `knowledge-space` | `know…

---

### 100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | # | Запрос | Rank | Hit | |---|--------|------|-----| | 1 | Yodoca консолидация SQLite decay forgot memory | 4 | ✅ | | 2 | AgentFS файловая система агент vault kksudo | 2 | ✅ | | 3 | NGT Memory ассо…

> | Метрика | Значение | Порог | Статус | |---------|---------|-------|--------| | Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS | | Mean MRR      | 0.603 | — | — | | Avg Latency   | 1.106с | ≤ 5.0с…

> - **Метрика:** Hit Rate@10 — доля запросов с ≥1 релевантным документом в топ-10. - **Поиск:** `hybrid_search()` = 0.6×TF-IDF + 0.4×BM25 с фильтром шумовых документов. - **Фильтр шума:** исключаются me…

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

> | Аспект | Lorenzo Gateway | DAF-gateway | |--------|----------------|-------------| | Поиск | `hybrid_search()` — наш BM25+TF-IDF | `docstoolkit.rag` — внешняя библиотека | | Данные | `search_index.j…

> ### `GET /api/benchmark` Все 5 критериев успеха PROTOTYPE_SPEC §8 одним запросом. ```bash curl http://localhost:8083/api/benchmark ``` ```json {   "criteria": {     "latency_s":   {"value": 0.21, "thr…

> ### Поиск коллаборации ```bash curl -X POST http://localhost:8083/v1/chat/completions \      -H "Content-Type: application/json" \      -d '{        "model": "lorenzo-gateway",        "messages": [{"r…

---

### 100% — `docs/CLUSTERS.md` vs `docs/obsidian/CLUSTERS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` — _150-appendix-c-version-history_ - `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` — _161-7-phased-rollout-plan_ - `docs/…

> - `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` — _343-lorenzo-catalyst-agent-глубокая-проработка-специфи_ - `docs/02-anthropic-vacancies/364-final-note-ты-ex…

> - `docs/02-anthropic-vacancies/03-portal-protocol-md.md` — _03-portal-protocol-md_ - `docs/02-anthropic-vacancies/04-abstract.md` — _04-abstract_ - `docs/02-anthropic-vacancies/05-0-status-of-this-doc…

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

> | Сходство | Файл A | Файл B | |----------|--------|--------| | 1.000 | `02-why-document-exists.md` | `01-missing-middle-layer.md` | | 1.000 | `svyazi.md` | `svend4.md` | | 1.000 | `svyazi.md` | `sgb.…

> - `02-why-document-exists.md` ↔ `01-missing-middle-layer.md` (1.000) - `svyazi.md` ↔ `svend4.md` (1.000) - `svyazi.md` ↔ `sgb.md` (1.000) - `svyazi.md` ↔ `nautilus.md` (1.000) - `svend4.md` ↔ `sgb.md`…

---

### 100% — `docs/CROSSREFS.md` vs `docs/obsidian/CROSSREFS.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Проект | Файлов | Где упоминается | |--------|--------|-----------------| | **AI Factory** | 147 | `docs/01-svyazi/01-executive-summary.md`, `docs/01-svyazi/03-component-catalog.md`, `docs/01-svyazi…

> | Файл | Проектов | Список | |------|----------|--------| | `docs/TABLES.md` | 30 | Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory +24 | | `docs/obsidian/TABLES.md` | 30 | Svyazi, Ca…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Тема 1: cowork, ingit, turn (2042 документов) - Тема 4: triangle, double, domain (123 документов) - Тема 2: memory, wikontic, yodoca (102 документов) - Тема 3: level, compatibility, bridges (83 доку…

> **Документы:** - `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` — passport, compatibility, minimal, curious - `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` — compatibility, level, re…

> **Документы:** - `docs/COVERAGE.md` — условные, обозначения, heatmap, отсутствует - `docs/DIGEST_WEEKLY.md` — digest, metrics, auto, preview - `docs/HEALTH.md` — балл, broken, links, validation - `doc…

---

### 100% — `docs/CONTRADICTIONS.md` vs `docs/obsidian/CONTRADICTIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **B:** `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` > md) --- ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Model — большая языковая модель ^cardin…

> **A:** `docs/01-svyazi/11-integration-contracts.md` > 1) ^sentinel: OSS-проект: безопасность и allowlist для MCP ^svyazi: Главный проект: экосистема AI-компонентов --- Кто ссылается на этот документ (…

> **B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` > knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референс…

---

### 100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** iximy - **Источник:** Хабр citeturn34view2 - **Лицензия:** неуточнено. citeturn34view2 - **Maturity:** практический implementation guide; публичный код в статье не акцентирован. citeturn3…

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

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** AnastasiyaW - **Источник:** Хабр + GitHub citeturn20view2turn37search0 - **Лицензия:** **MIT**. citeturn37search0 - **Maturity:** активный OSS. citeturn37search0 - **Релевантность к Svyaz…

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

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

> Bounding boxes на страницах PDF — это принципиально другой уровень доверия к ответу агента. Когда источник цитаты — не «страница 3», а конкретный визуальный блок на странице, это меняет применимость с…

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Алгоритм:** 1. BM25 по запросу → базовый score 2. Умножает на важность файла (из PRIORITIES.md) 3. Умножает на связность (количество входящих ссылок) 4. Оценивает время чтения (200 сл/мин RU, 250 EN…

> ```bash python scripts/improve_reading_list.py --query "агент с памятью" python scripts/improve_reading_list.py --query "RAG retrieval" --top 20 python scripts/improve_reading_list.py --query "Yodoca"…

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

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Авторы и контакты Статус Параметр Значение ------------------- Теги — Упоминаний в репо — Слой — Контакт — Статус связи не писали Обнов…

> - Статус - Похожие документы - Использование - Смотрите также - Кто ссылается на этот документ (4)

> <!-- summary --> > автора статьи выше подобных авторов подобных разработчиков или ещё может быть или может быть даже несколько проектов которые вместе можно совместить и которые дойдут вместе один уни…

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

_...и ещё 944 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

