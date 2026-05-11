---
title: "Отчёт о дублировании"
tags:
  - duplicates
  - docs
  - general
date: 2026-05-11
---

# Отчёт о дублировании

<!-- toc -->
## Содержание

- [Похожие файлы (Jaccard ≥ 0.5)](#похожие-файлы-jaccard-05)
  - [100% — `docs/SENTINEL.md` vs `docs/obsidian/SENTINEL.md`](#100-docssentinelmd-vs-docsobsidiansentinelmd)
  - [100% — `docs/PRECISION_EVAL.md` vs `docs/obsidian/PRECISION_EVAL.md`](#100-docsprecision_evalmd-vs-docsobsidianprecision_evalmd)
  - [100% — `docs/BADGES.md` vs `docs/obsidian/BADGES.md`](#100-docsbadgesmd-vs-docsobsidianbadgesmd)
  - [100% — `docs/GATEWAY.md` vs `docs/obsidian/GATEWAY.md`](#100-docsgatewaymd-vs-docsobsidiangatewaymd)
  - [100% — `docs/DIGEST.md` vs `docs/obsidian/DIGEST.md`](#100-docsdigestmd-vs-docsobsidiandigestmd)
  - [100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`](#100-docssimilarmd-vs-docsobsidiansimilarmd)
  - [100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`](#100-docstopic_modelmd-vs-docsobsidiantopic_modelmd)
  - [100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`](#100-docssvyazi-2-0componentshybrid-ragmd-vs-docsobsidiansvyazi-2-0componentshybrid-ragmd)
  - [100% — `docs/svyazi-2-0/components/agent-memory-mcp.md` vs `docs/obsidian/svyazi-2-0/components/agent-memory-mcp.md`](#100-docssvyazi-2-0componentsagent-memory-mcpmd-vs-docsobsidiansvyazi-2-0componentsagent-memory-mcpmd)
  - [100% — `docs/svyazi-2-0/components/graph-rag.md` vs `docs/obsidian/svyazi-2-0/components/graph-rag.md`](#100-docssvyazi-2-0componentsgraph-ragmd-vs-docsobsidiansvyazi-2-0componentsgraph-ragmd)
  - [100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`](#100-docssvyazi-2-0componentsmclaudemd-vs-docsobsidiansvyazi-2-0componentsmclaudemd)
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
  - [100% — `docs/processing-guide/QA.md` vs `docs/anthropic-vacancies/QA.md`](#100-docsprocessing-guideqamd-vs-docsanthropic-vacanciesqamd)
  - [100% — `docs/03-technology-combinations/QA.md` vs `docs/02-anthropic-vacancies/QA.md`](#100-docs03-technology-combinationsqamd-vs-docs02-anthropic-vacanciesqamd)
  - [100% — `docs/03-technology-combinations/QA.md` vs `docs/01-svyazi/QA.md`](#100-docs03-technology-combinationsqamd-vs-docs01-svyaziqamd)
  - [100% — `docs/02-anthropic-vacancies/QA.md` vs `docs/01-svyazi/QA.md`](#100-docs02-anthropic-vacanciesqamd-vs-docs01-svyaziqamd)
  - [99% — `docs/DECISIONS.md` vs `docs/obsidian/DECISIONS.md`](#99-docsdecisionsmd-vs-docsobsidiandecisionsmd)
- [Смотрите также](#смотрите-также)

---


<!-- toc-auto -->

> [!NOTE]
> Раздел `DUPLICATES` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: duplicates, docs -->


<!-- summary -->
> `DUPLICATES` — раздел документации проекта Lorenzo.


Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **978**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/SENTINEL.md` vs `docs/obsidian/SENTINEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Итог - PII и секреты - Небезопасный код - Файлы credentials - Лицензионные риски - HTTP без TLS - Использование

> | Файл | Лицензия | Риск | |------|----------|------| | `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-` | BSL | Business Source License — не открытая, коммерческие ограниче | | `docs/ob…

> | Файл | Строка | Проблема | Фрагмент | |------|--------|----------|----------| | `scripts/gateway.py` | 655 | __import__() dynamic import | `t0      = __import__("time").time()` | | `scripts/gateway.…

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

> - **tests** !tests - **templates** !templates - **skills** !skills - **mcp-servers** !mcp_servers - **manifests** !manifests - **scripts** !scripts - **health** !health

> ## Markdown сниппеты для README ```markdown !tests !templates !skills !mcp_servers !manifests !scripts !health ```

---

### 100% — `docs/GATEWAY.md` vs `docs/obsidian/GATEWAY.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ### `POST /api/ask` Прямой RAG-запрос без OpenAI-совместимости. ```bash curl -X POST http://localhost:8083/api/ask \      -H "Content-Type: application/json" \      -d '{"query": "агент с памятью конс…

> **Полный цикл обогащения:** ``` Внешний источник (статья, разговор, результат анализа)     ↓ AI-агент анализирует и структурирует     ↓ POST /api/cards  →  docs/04-ai-collaborations/<slug>.md     ↓ py…

> | Аспект | Lorenzo Gateway | DAF-gateway | |--------|----------------|-------------| | Поиск | `hybrid_search()` — наш BM25+TF-IDF | `docstoolkit.rag` — внешняя библиотека | | Данные | `search_index.j…

---

### 100% — `docs/DIGEST.md` vs `docs/obsidian/DIGEST.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Дата | Hash | Описание | |------|------|---------| | 2026-05-11 | `a5b93b95` | chore: обновление CONCEPTS.md и ENTITIES.md | | 2026-05-11 | `56694311` | chore: обновление QUESTIONS.md | | 2026-05-11…

---

### 100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Сходство | Файл A | Файл B | |----------|--------|--------| | 1.000 | `svyazi.md` | `svend4.md` | | 1.000 | `svyazi.md` | `sgb.md` | | 1.000 | `svyazi.md` | `nautilus.md` | | 1.000 | `svend4.md` | `…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Тема 1: turn, cowork, view (2043 документов) - Тема 2: концептов, раздела, memory (141 документов) - Тема 4: acknowledgments, principal, type (128 документов) - Тема 6: informative, normative, porta…

> **Документы:** - `docs/01-svyazi/01-executive-summary.md` — синергии, продолжение, линия, вывод - `docs/01-svyazi/02-methodology.md` — отбора, шкала, зрелости, интеграционной - `docs/01-svyazi/03-comp…

> **Документы:** - `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` — фазу, открытые, ресурсов, вопросы - `docs/02-anthropic-vacancies/159-5-economic-model.md` — contributor, year, …

---

### 100% — `docs/svyazi-2-0/components/hybrid-rag.md` vs `docs/obsidian/svyazi-2-0/components/hybrid-rag.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

> - **Автор:** iximy - **Источник:** Хабр citeturn34view2 - **Лицензия:** неуточнено. citeturn34view2 - **Maturity:** практический implementation guide; публичный код в статье не акцентирован. citeturn3…

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

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

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** VladSpace / vpakspace - **Источник:** Хабр + GitHub citeturn34view3turn40search2 - **Лицензия:** неуточнено. citeturn34view3turn40search2 - **Maturity:** активный публичный repo / product…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/svyazi-2-0/components/mclaude.md` vs `docs/obsidian/svyazi-2-0/components/mclaude.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание - Ключевые компоненты и паттерны - Использование - Смотрите также - Кто ссылается на этот документ (3)

> - **Автор:** AnastasiyaW - **Источник:** Хабр + GitHub citeturn20view2turn37search0 - **Лицензия:** **MIT**. citeturn37search0 - **Maturity:** активный OSS. citeturn37search0 - **Релевантность к Svyaz…

> Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации…

---

### 100% — `docs/letters/vitalysemenov.md` vs `docs/obsidian/letters/vitalysemenov.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание того, как agent-memory-mcp + Memory OS закрывают memory-слой   в архитектуре Svyazi 2.0 (задокументировано детально) - Обсуждение, как `CardEnvelope` Svyazi соотносится с типами записей   a…

> Как gardener-loop решает конфликты bi-temporal фактов? Конкретно: если в `episodic` памяти есть запись «X произошло в момент T₁» (время события), добавленная в момент T₂ (время записи), а потом приход…

> Четыре типа записей (`episodic`, `semantic`, `procedural`, `working`) — это точная типизация, которой не хватает большинству memory-систем. В PROTOTYPE_SPEC Svyazi я использую похожее разделение: `fac…

---

### 100% — `docs/letters/antipozitive.md` vs `docs/obsidian/letters/antipozitive.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Я строю Svyazi 2.0 — локальную систему, которая связывает знания из разных источников через граф. Один из ключевых вопросов, с которым я работаю — как оценивать качество связей в таком графе, не прибе…

> В Svyazi 2.0 граф строится из карточек (факты, проекты, люди, эпизоды), и для каждой пары карточек нужно решить: есть между ними связь или это случайное совпадение терминов. При размере базы в 1600+ к…

> - Тестовый набор из реальных карточек Svyazi для проверки MemNet на   практическом случае (смешанные типы: факты, проекты, люди) - Обсуждение, как MemNet может стать слоем валидации связей поверх   BM…

---

### 100% — `docs/letters/nlaik.md` vs `docs/obsidian/letters/nlaik.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - Описание того, как LiteParse закрывает слой ingestion в Evidence Envelope   Svyazi 2.0 — уже задокументировано с примерами - Тестовый набор: 3-4 юридических/технических PDF на русском языке,   если …

> Я строю Svyazi 2.0 — локальную систему для работы со знаниями из документов. Ключевой компонент, который мне нужен — слой evidence: не просто найти нужный абзац, а показать, откуда взялся каждый факт,…

> Как LiteParse обрабатывает таблицы с объединёнными или перенесёнными ячейками? Это самый сложный случай в юридических и финансовых PDF, где данные в ячейке относятся к заголовку в предыдущей строке — …

---

### 100% — `docs/obsidian/processing-guide/06-search.md` vs `docs/processing-guide/06-search.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Алгоритм:** 1. BM25 по запросу → базовый score 2. Умножает на важность файла (из PRIORITIES.md) 3. Умножает на связность (количество входящих ссылок) 4. Оценивает время чтения (200 сл/мин RU, 250 EN…

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

> - Статус - Похожие документы - Использование - Смотрите также - Кто ссылается на этот документ (4)

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

### 100% — `docs/03-technology-combinations/QA.md` vs `docs/01-svyazi/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

### 100% — `docs/02-anthropic-vacancies/QA.md` vs `docs/01-svyazi/QA.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Кто ссылается на этот документ (6):** - README - OUTLINE - READABILITY - READING_TIME - SEARCH - TABLES

---

### 99% — `docs/DECISIONS.md` vs `docs/obsidian/DECISIONS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - как… > Я собираю Svyazi 2.0 — локальную community intelligence platform, которая строит граф знаний из текстов, документов и профилей людей. В слой памяти я рассматривал несколько подходов (Yodoca, …

> - читать перед погружением в детали. > Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти **три короткие итерации**, каждая из которых поднимает один новый класс св…

> - на файловое ядро Svyazi‑2.0. | | **mclaude** | AnastasiyaW | Хабр + GitHub citeturn20view2turn37search0 | Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом. | …

---

_...и ещё 948 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

## Смотрите также
- [[README|Главная]]
- [[METRICS|Метрики]]
- [[HEALTH|Здоровье]]
- [[GLOSSARY|Глоссарий]]
- [[ENTITIES|Сущности]]
- [[DECISIONS|Решения]]
