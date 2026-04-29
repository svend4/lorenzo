# Отчёт о дублировании

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **290**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/WORD_FREQ.md` vs `docs/obsidian/WORD_FREQ.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Слово | Частота | | |-------|---------|---| | **habr** | 71 | `███████████████` | | **memory** | 70 | `██████████████░` | | **llm** | 64 | `█████████████░░` | | **пара** | 63 | `█████████████░░` | |…

> | # | Слово | Частота | Визуализация | |---|-------|---------|-------------| | 1 | **anthropic** | 11,655 | `████████████████████` | | 2 | **vacancies** | 10,696 | `██████████████████░░` | | 3 | **про…

> | Слово | Частота | | |-------|---------|---| | **components** | 84 | `███████████████` | | **autofilled** | 81 | `██████████████░` | | **svyazi** | 51 | `█████████░░░░░░` | | **sgb** | 21 | `███░░░░░…

---

### 100% — `docs/SCHEDULE.md` vs `docs/obsidian/SCHEDULE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Срок | Веха | Статус | |------|------|--------| | **2024-Q4** | ✅ Исследование компонентов завершено | ✅ Выполнено | | **2024-Q4** | ✅ Архитектура Svyazi 2.0 задокументирована | ✅ Выполнено | | **20…

> ``` Фаза                    | Q4'24 | Q1'25 | Q2'25 | Q3'25 | Q4'25 | Q1'26 | Q2'26 | Q3'26 ------------------------|-------|-------|-------|-------|-------|-------|-------|------- Исследование       …

---

### 100% — `docs/ORPHANS.md` vs `docs/obsidian/ORPHANS.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> 1. Добавить ссылки на изолированные файлы из README.md соответствующего раздела 2. Проверить, не являются ли они дублями других файлов 3. Крупные изолированные файлы (>100 слов) — добавить в READING_O…

---

### 100% — `docs/CONSISTENCY.md` vs `docs/obsidian/CONSISTENCY.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - `docs/CONSISTENCY.md` - `docs/TABLES.md` - `docs/CONCEPTS.md` - `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` - `docs/02-anthropic-vacancies/365-развёрнутый…

> | Термин | Канонично | Вариант | Файлов | |--------|-----------|---------|--------| | **knowledge-space** | `knowledge-space` | `knowledge space` | 8 | | **knowledge-space** | `knowledge-space` | `kno…

---

### 100% — `docs/READING_TIME.md` vs `docs/obsidian/READING_TIME.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> - `docs/TABLES.md` — ~1ч 46мин, 24513 слов - `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` — ~1ч 31мин, 17180 слов - `docs/OUTLINE.md` — ~1ч 27мин, 20244 слов - `docs/PARAGRAP…

> | Файл | Время | Слов | Категория | |------|-------|------|-----------| | `docs/TABLES.md` | ~1ч 46мин | 24513 | 📕 Очень долго | | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md…

---

### 100% — `docs/DEPENDABOT.md` vs `docs/obsidian/DEPENDABOT.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в | |-------|------------|-----------------|--------|----------------| | `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` …

> | Проект | Репозиторий | Статус | |--------|------------|--------| | AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — | | NGT Memory | [https://github.com/spbmolot/…

---

### 100% — `docs/PARAGRAPH_QUALITY.md` vs `docs/obsidian/PARAGRAPH_QUALITY.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> - [Типы проблем](#типы-проблем) - [По файлам](#по-файлам)   - [`docs/CONCEPTS.md` (1443 проблем)](#docsconceptsmd-1443-проблем)   - [`docs/TABLES.md` (553 проблем)](#docstablesmd-553-проблем)   - [`do…

---

### 100% — `docs/SCORING.md` vs `docs/obsidian/SCORING.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Критерий | Статус | Вес | |----------|--------|-----| | Компоненты каталогизированы (20+) | ✅ | 10 | | Ансамбли определены (5+) | ✅ | 10 | | Архитектурные пробелы выявлены | ✅ | 8 | | Безопасность и…

> | Критерий | Статус | Вес | |----------|--------|-----| | Executive Summary существует | ✅ | 10 | | Архитектурные контракты описаны | ✅ | 10 | | MVP план задокументирован | ✅ | 10 | | Дорожная карта е…

> | Критерий | Статус | Вес | |----------|--------|-----| | Риски выявлены и задокументированы | ✅ | 8 | | Лицензии проверены | ✅ | 8 | | Сломанных ссылок < 30 | ❌ | 5 | |  ↳ _Слишком много сломанных сс…

---

### 100% — `docs/FAQ.md` vs `docs/obsidian/FAQ.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> A nautilus shell is a **spiral of nested chambers**, each larger than the last but built on the same geometry. This is *fractal scaling with preserved proportion*. Nautilus Protocol embodies the same …

> Если выберете первый или второй вариант, я могу написать в следующем сообщении. Если третий — то этот ответ остаётся как ваша заметка к шестому документу, и работа сессии завершена с шестью полноценны…

> Частично да. - Нижний треугольник — уже работает через MCP (каждый человек конфигурирует свои MCP servers для своих assistant'ов). - Верхний треугольник — частично через GitHub Issues/Linear/Asana с A…

---

### 100% — `docs/TECH_RADAR.md` vs `docs/obsidian/TECH_RADAR.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Технология / Компонент | Категория | Комментарий | |------------------------|-----------|------------| | **NGT-memory** | Компоненты | Ассоциативный граф памяти, BSL 1.1 | | **knowledge-space** | Ко…

> ``` ┌─────────────────────────┬─────────────────────────┐ │      🟢 ADOPT           │      🔵 TRIAL           │ │  • MCP Protocol          │  • Yodoca                │ │  • CardIndex             │  • SE…

> | Технология / Компонент | Категория | Комментарий | |------------------------|-----------|------------| | **MCP Protocol** | Инструменты | Стандарт интеграции AI-инструментов — Anthropic | | **CardIn…

---

### 100% — `docs/ALERTS.md` vs `docs/obsidian/ALERTS.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Тип | Количество | Назначение | |-----|------------|------------| | `[!NOTE]` | 0 | Нейтральная заметка | | `[!TIP]` | 42 | Практический совет | | `[!WARNING]` | 10 | Предупреждение о риске | | `[!I…

---

### 100% — `docs/VALIDATION.md` vs `docs/obsidian/VALIDATION.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Проверка | Статус | Проблем | |----------|--------|---------| | Разделы и README | ✅ | 0 | | Мета-файлы | ✅ | 0 | | Пустые/короткие файлы | ⚠️ | 6 | | Именование файлов | ✅ | 10 | | Заголовки H1 | ⚠…

> - ℹ️ Длинное кириллическое имя: `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` - ℹ️ Длинное кириллическое имя: `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-port…

> - 🔗 Сломана ссылка в `docs/01-svyazi/01-executive-summary.md`: `docs/04-ai-collaborations/01-executive-summary.md` - 🔗 Сломана ссылка в `docs/01-svyazi/01-executive-summary.md`: `docs/04-ai-collaborat…

---

### 100% — `docs/VERSION_DIFF.md` vs `docs/obsidian/VERSION_DIFF.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Файл | Δ слов | Добавленные темы | Удалённые темы | |------|--------|------------------|----------------| | `docs/TIMELINE.md` | -2390 | 2020 (2 упоминаний), 2021 (1 упоминаний), 2022 (5 упоминаний)…

> - `docs/PARAGRAPH_QUALITY.md` (+4796 слов) - `docs/CONTRADICTIONS.md` (+1693 слов) - `docs/NAMED_ENTITIES.md` (+1132 слов) - `docs/DEPENDENCY_MAP.md` (+601 слов) - `docs/INDEX.md` (+467 слов) - `docs/…

---

### 100% — `docs/ENTITIES.md` vs `docs/obsidian/ENTITIES.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Проект | Упоминаний | Файлов | |---------|------------|--------| | **Svyazi** | 2029 | 137 | | **Nautilus** | 1891 | 212 | | **Cowork** | 1487 | 127 | | **ingit** | 1478 | 121 | | **SGB** | 783 | 10…

> | Организация | Упоминаний | Файлов | |---------|------------|--------| | **Anthropic** | 12613 | 430 | | **Claude** | 1217 | 181 | | **GitHub** | 1068 | 139 | | **Habr** | 772 | 85 | | **Хабр** | 230…

> | Пара | Общих файлов | |------|-------------| | Cowork ↔ ingit | 108 | | Nautilus ↔ Cowork | 89 | | Nautilus ↔ ingit | 80 | | Svyazi ↔ NGT | 79 | | NGT ↔ Yodoca | 76 | | Nautilus ↔ SGB | 73 | | Svyaz…

---

### 100% — `docs/VOCABULARY.md` vs `docs/obsidian/VOCABULARY.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | STTR | TTR | Hapax% | Lex.Density | Токенов | |------|------|-----|--------|-------------|---------| | `ABBREVIATIONS.md` | 0.940 | 0.717 | 75% | 0.875 | 835 | | `HEALTH.md` | 0.909 | 0.909 |…

> - [Корпусная статистика](#корпусная-статистика) - [Топ файлов по богатству словаря (STTR)](#топ-файлов-по-богатству-словаря-sttr) - [Файлы с бедным словарём (требуют доработки)](#файлы-с-бедным-словар…

> | Метрика | Значение | |---------|----------| | Средний TTR | 0.434 | | Средний STTR (100-токенное окно) | 0.589 | | Lexical density | 0.835 | | Средняя длина слова | 6.58 | | Общая оценка | 🟠 Бедный …

---

### 100% — `docs/MISSING.md` vs `docs/obsidian/MISSING.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов | |--------|---------------|--------|------|---------|----------------| | ✅ | **Svyazi** | 139 | 147259 | ≥5ф/2000сл | `WORD_FREQ.md…

---

### 100% — `docs/COVERAGE.md` vs `docs/obsidian/COVERAGE.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks | |--------|--------|---------|------|-----|-----------|--------|-----------| | `01-svyazi` | 14 | 🟢 13/14 | 🟢 13/14 | 🟢 12/14…

> | Файл | Слов | Summary | Теги | TOC | CrossRefs | ## Статус | Backlinks | |------|------| ---|---|---|---|---|--- | | `docs/01-svyazi/00-intro-part2.md` | 5 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | | `docs/02-anthr…

> - ✅ `docs/04-ai-collaborations/00-intro.md` - ✅ `docs/04-ai-collaborations/01-executive-summary.md` - ✅ `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` - ✅ `docs/04-ai-collabora…

---

### 100% — `docs/SENTIMENT.md` vs `docs/obsidian/SENTIMENT.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Документ | Скептицизм‰ | Тон | |----------|------------|-----| | `PARAGRAPH_QUALITY` | 312.8 | 🔴 скептичный | | `198-8-риски-и-меры-противодействия` | 88.3 | 🔴 скептичный | | `177-8-risks-and-mitiga…

> | Документ | Оптимизм‰ | Тон | |----------|----------|-----| | `110-вопрос-fallback-ratio-как-крити` | 16.3 | 🟠 срочный | | `193-3-что-делает-агента-представите` | 16.0 | 🟢 оптимистичный | | `123-port…

> | Раздел | Оптимизм | Скептицизм | Срочность | Неопределённость | Тон | |--------|----------|------------|-----------|-----------------|-----| | **01-svyazi** | 2.3‰ | 7.1‰ | 4.9‰ | 0.5‰ | 🔴 скептичны…

---

### 100% — `docs/KPI_HISTORY.md` vs `docs/obsidian/KPI_HISTORY.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> | Метрика | Значение | Тренд | |---------|---------|-------| | Markdown документов | **529** | → | | Слов | **523,868** | → | | Скриптов | **125** | → | | Скоринг | **93%** | → | | Здоровье | **90/100…

---

### 100% — `docs/SEE_ALSO.md` vs `docs/obsidian/SEE_ALSO.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> - **01-executive-summary** → `03-component-catalog`, `04-ensembles-overview`, `07-mvp-planning` - **02-methodology** → `02-методика-и-рамка-отбора`, `01-executive-summary`, `07-выводы`, `08-что-это-пр…

---

### 100% — `docs/NAMED_ENTITIES.md` vs `docs/obsidian/NAMED_ENTITIES.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Сущность | Файлов | Тип | |----------|--------|-----| | `2026-04` | 79 | dates | | `2026-04-29` | 14 | dates | | `2026-04-19` | 11 | dates | | `апрель 2026` | 10 | dates | | `2026-04-26` | 9 | dates…

> - `docs/01-svyazi/02-methodology.md` - `docs/01-svyazi/03-component-catalog.md` - `docs/01-svyazi/04-ensembles-overview.md` - `docs/01-svyazi/06-security-privacy.md` - `docs/01-svyazi/09-architectural…

> - `docs/02-anthropic-vacancies/00-intro.md` - `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` - `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` …

---

### 100% — `docs/GRAPH.md` vs `docs/obsidian/GRAPH.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ```dot digraph lorenzo {   rankdir=LR;   node [shape=box];   subgraph cluster_ingestion {     label="INGESTION";     Svyazi [label="Svyazi"];     CardIndex [label="CardIndex"];     Firecrawl [label="F…

> | Проект A | Проект B | Файлов вместе | |----------|----------|---------------| | **Svyazi** | **Yodoca** | 74 | | **Svyazi** | **AgentFS** | 70 | | **AgentFS** | **Yodoca** | 64 | | **Svyazi** | **Ca…

> ```mermaid graph TD   subgraph ingestion[INGESTION]     Svyazi[Svyazi]     CardIndex[CardIndex]     Firecrawl[Firecrawl]   end   subgraph knowledge[KNOWLEDGE]     AgentFS[AgentFS]     knowledge-space[…

---

### 100% — `docs/COMPLEXITY.md` vs `docs/obsidian/COMPLEXITY.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Документ | Слов | Ср.длина пред. | Термин.плотность | Ур.заголовков | Балл | |----------|------|---------------|-----------------|--------------|------| | `342-что-такое-вариант-c-concept-doc` | 105…

> | Документ | Слов | Балл | |----------|------|------| | `03-portal-protocol-md` | 125 | 🟢 Простой | | `05-0-status-of-this-document` | 138 | 🟢 Простой | | `06-1-introduction` | 362 | 🟢 Простой | | `07…

---

### 100% — `docs/CITATION_INDEX.md` vs `docs/obsidian/CITATION_INDEX.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` - `docs/02-anthropic-vacancies/319-acknowledgments.md` - `docs/02-anthropic-vacancies/320-references.md` - `docs/02-anthropic-va…

> - `docs/02-anthropic-vacancies/00-intro.md` - `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` - `docs/02-anthropic-vacancies/67-о-проекте.md` - `docs/02-anthropic-vaca…

> - [Топ доменов](#топ-доменов) - [Наиболее цитируемые URL](#наиболее-цитируемые-url) - [Детали топ-10](#детали-топ-10)   - [`https://github.com/svend4/nautilus/issues`](#httpsgithubcomsvend4nautilusiss…

---

### 100% — `docs/METRICS.md` vs `docs/obsidian/METRICS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами | |--------|------|----------------|--------------|-------------|------------| | **01-svyazi** | 72 | 30.7 | 0.5 | 100% | 10…

> | Документ | Балл | Что отсутствует | |----------|------|----------------| | `ABBREVIATIONS` | 30 | summary, tags, TOC, callout | | `AUTHORS` | 30 | summary, tags, TOC, callout | | `BACKLINKS` | 30 | …

> | Документ | Балл | Слов | |----------|------|------| | `01-интегральный-анализ-профиля-svend4` | 100 | 19103 | | `02-общий-план-развития-nautilus-portal-p` | 100 | 3181 | | `109-3-принципы-консолидац…

---

### 100% — `docs/HEATMAP.md` vs `docs/obsidian/HEATMAP.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Тема | Лучший раздел | Плотность | |------|--------------|-----------| | **Память/Knowledge** | `01-svyazi` | 24.2‰ | | **Агент/Оркестр** | `03-technology-combinations` | 25.3‰ | | **Безопасность** …

> | Тема | svyazi | anthropic- | technology | ai-collabo | habr-proje | |------|------------|------------|------------|------------|------------| | **Память/Knowledge** | 24.2 | 3.2 | 15.7 | 16.5 | 21.3…

> ``` Тема                    | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr ------------------------|-----------|--------------|---------|-----------|-------- Память/Knowledge        | ██24…

---

### 100% — `docs/DIGEST_WEEKLY.md` vs `docs/obsidian/DIGEST_WEEKLY.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> ``` 898c42a feat: run all script groups, apply TOC/abstracts/crosslinks, rebuild search index 8e689b3 docs: auto-update via improve_run_all [skip ci] 69562b0 feat: add component matrix, KPI history tr…

---

### 100% — `docs/MINDMAP.md` vs `docs/obsidian/MINDMAP.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ```mermaid mindmap   root((Lorenzo Repository))     🧠 **Svyazi 2.0**       CardIndex       Evidence Envelope       Memory Write Policy       Ансамбли       MVP 12-18 дней       Безопасность     💼 **An…

> | Слой | Проекты | |------|---------| | Ingestion | Svyazi, CardIndex, Firecrawl | | Knowledge | AgentFS, knowledge-space | | Memory | Yodoca, NGT Memory, MemNet | | RAG | LiteParse, Legal RAG, Hybrid…

> ```mermaid flowchart LR   subgraph INGEST     Svyazi[Svyazi]     CardIndex[CardIndex]     Firecrawl[Firecrawl]   end   subgraph KNOWLEDGE     AgentFS[AgentFS]     knowledge-space[knowledge-space]   en…

---

### 100% — `docs/PRIORITIES.md` vs `docs/obsidian/PRIORITIES.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Файл | Score | |------|-------| | `docs/autofilled/components/.md` | 3.54 | | `docs/autofilled/components/spbmolot.md` | 3.54 | | `docs/autofilled/components/ingit.md` | 3.54 | | `docs/autofilled/co…

> | Файл | Score | |------|-------| | `docs/contacts/andrey-chuyan.md` | 13.65 | | `docs/contacts/anastasiyaw.md` | 11.54 | | `docs/contacts/kksudo.md` | 10.85 | | `docs/contacts/dmitriila.md` | 10.77 |…

> | Файл | Score | |------|-------| | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | 63.78 | | `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-fo…

---

### 100% — `docs/DENSITY.md` vs `docs/obsidian/DENSITY.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Тема | Основной раздел | % | |------|-----------------|---| | Svyazi | `root` | 70% | | CardIndex | `root` | 58% | | AgentFS | `root` | 54% | | Yodoca | `root` | 54% | | NGT-memory | `root` | 50% | …

> | Тема | Упоминаний | Визуализация | |------|------------|-------------| | **Вакансии** | 13065 | `███████████████` | | **Svyazi** | 2349 | `██░░░░░░░░░░░░░` | | **NGT-memory** | 1588 | `█░░░░░░░░░░░░…

> | Тема | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr | root | Итого | |------|-----------|--------------|---------|-----------|---------|------|-------| | **Svyazi** | 214 | 73 | 16 | 339…

---

_...и ещё 260 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- backlinks-auto -->
## Упоминается в

- [docs](README.md)
- [Все таблицы репозитория](TABLES.md)
- [Карта репозитория Lorenzo](SITEMAP.md)
- [Методика и рамка отбора](04-ai-collaborations/02-методика-и-рамка-отбора.md)
- [Методика и рамка отбора проектов](01-svyazi/02-methodology.md)

<!-- related-auto -->
## Связанные документы

- [Перекрёстные ссылки](CROSSREFS.md) _29%_
- [Приоритеты файлов](PRIORITIES.md) _25%_
- [Карта репозитория Lorenzo](SITEMAP.md) _25%_
- [Валидация структуры репозитория](VALIDATION.md) _25%_
- [Кластеры тематически близких файлов](CLUSTERS.md) _21%_
- [Инвертированный индекс ключевых слов](KEYWORD_INDEX.md) _21%_
- [AI-саммари разделов документации](LLM_SUMMARIES.md) _21%_
- [Время чтения документов](READING_TIME.md) _21%_
