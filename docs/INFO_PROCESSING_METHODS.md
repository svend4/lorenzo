# Методы обработки большого массива разрозненной информации

_База знаний Lorenzo — 1171 документ, 956K слов, 18 секций_

---

## Что такое «большой массив разрозненной информации»

В контексте Lorenzo это:
- Markdown-файлы разной длины (от 50 до 50 000 слов)
- Разные языки (RU/EN/MIX)
- Разные форматы внутри MD (таблицы, код, Q&A, нарративы, шаблоны)
- Разные источники (Habr, вакансии, собственные исследования, Obsidian-vault)
- Разные уровни качества (черновики → полноценные документы)
- Дублирование и противоречия внутри корпуса

---

## Карта всех уровней обработки

```
УРОВЕНЬ 0 — Сырые данные
  │  Markdown-файлы, MHTML-снимки, заметки, вакансии
  ▼
УРОВЕНЬ 1 — Структурирование и очистка
  │  TOC, заголовки, дедупликация, орфография, теги
  ▼
УРОВЕНЬ 2 — Извлечение (Extraction)
  │  Сущности, концепты, решения, задачи, цитаты, таблицы
  ▼
УРОВЕНЬ 3 — Индексирование (Indexing)
  │  Инвертированный индекс, BM25-корпус, TF-IDF векторы, чанки
  ▼
УРОВЕНЬ 4 — Анализ (Analysis)
  │  Кластеризация, граф концептов, противоречия, похожие тексты
  ▼
УРОВЕНЬ 5 — Поиск (Retrieval)
  │  BM25, фасеты, семантический поиск, RAG-пайплайн
  ▼
УРОВЕНЬ 6 — Обогащение (Enrichment)
  │  LLM-суммаризация, gap-filling, абстракты, связи
  ▼
УРОВЕНЬ 7 — Синтез (Synthesis)
  │  Отчёты, дайджесты, карты знаний, списки чтения
  ▼
УРОВЕНЬ 8 — Экспорт и действие
     EPUB, Obsidian, Confluence, GitHub Issues, RSS, письма авторам
```

---

## Классификация по подходу

| Подход | Описание | Примеры в Lorenzo |
|--------|----------|-------------------|
| **Детерминированный** | Regex, правила, счётчики | орфография, TOC, теги |
| **Статистический** | TF-IDF, BM25, косинус | поиск, кластеры, похожие |
| **Графовый** | PageRank, связи узлов | TextRank, concept_graph |
| **LLM-assisted** | Claude API | суммаризация, Q&A, письма |
| **Гибридный** | детерм. + статист. | faceted_search, gap_filler |
| **Инкрементальный** | только изменения | index_update, watch |
| **Агентный** | автономное решение | watcher, improve_run_all |
## Уровень 1 — Структурирование и очистка

### Цель
Привести разрозненные файлы к единому стандарту, пригодному для дальнейшей обработки.

### Скрипты

| Скрипт | Что делает | Идемпотентен |
|--------|-----------|--------------|
| `improve_auto_toc.py` | Добавляет TOC по заголовкам H2-H4 | ✅ маркер `<!-- toc-auto -->` |
| `improve_summaries.py` | Краткая аннотация в начало файла | ✅ маркер `<!-- summary -->` |
| `improve_abstract.py` | Структурированный абстракт (Проблема/Подход/Результат) | ✅ маркер `<!-- abstract-auto -->` |
| `improve_tags.py` | TF-IDF ключевые слова → YAML-теги | ✅ |
| `improve_autocorrect.py` | Исправляет написание терминов из CONSISTENCY.md | ✅ |
| `improve_spellcheck.py` | Орфография (словарь + pyspellchecker) | ✅ |
| `improve_merge_short.py` | Сливает файлы <200 слов с соседом | ⚠️ меняет файлы |
| `improve_text_segmenter.py` | Разбивает файлы >1500 слов на части | ⚠️ создаёт подпапки |
| `improve_readmes.py` | README для каждой папки | ✅ пропускает богатые |
| `improve_heading_audit.py` | Аудит иерархии H1→H2→H3 | только отчёт |
| `improve_language_split.py` | RU/EN/MIX классификация, опц. разделение | опц. `--split` |

### Ключевые паттерны

**Идемпотентные маркеры** — защита от двойной обработки:
```markdown
<!-- toc-auto -->        ← auto_toc.py не вставит TOC повторно
<!-- abstract-auto -->   ← abstract.py пропустит файл
<!-- summary -->         ← summaries.py пропустит файл
<!-- textrank-summary --> ← textrank.py пропустит файл
```

**Порядок обработки** (важно соблюдать):
```
1. merge_short → 2. auto_toc → 3. abstract → 4. tags → 5. autocorrect
```
Нарушение порядка: TOC до merge_short → TOC устареет после слияния файлов.

---

## Уровень 2 — Извлечение (Extraction)

### Цель
Вытащить структурированные данные из неструктурированного текста без LLM.

### Что извлекается

| Тип данных | Скрипт | Выход |
|-----------|--------|-------|
| Именованные сущности (люди, проекты, техн., org) | `improve_named_entity_index.py` | `named_entities.json` |
| Концепты и определения | `improve_concepts.py` | `CONCEPTS.md` |
| Аббревиатуры | `improve_abbreviations.py` | `ABBREVIATIONS.md` |
| Задачи и TODO | `improve_action_items.py` | `ACTION_ITEMS.md` |
| Архитектурные решения | `improve_decisions.py` | `DECISIONS.md` |
| Вопросы и гипотезы | `improve_question_extractor.py` | `QUESTIONS.md` |
| KPI и числовые метрики | `improve_kpi.py` | `KPI.md` |
| Таблицы | `improve_extract_tables.py` | `TABLES.md` |
| Блоки кода | `improve_extract_code.py` | `CODE_BLOCKS.md` |
| Даты и события | `improve_timeline_events.py` | `TIMELINE.md` |
| Внешние URL | `improve_citation_index.py` | `CITATION_INDEX.md` |
| Контакты (email, telegram) | `improve_contacts.py` | `CONTACTS.md` |

### Как работает NER без ML

`improve_named_entity_index.py` использует:
1. **Словари**: список известных проектов, имён, технологий
2. **Регулярные выражения**: паттерны дат, email, GitHub URL
3. **Контекстные правила**: заглавные слова рядом с «проект», «автор», «использует»
4. **Частотный фильтр**: `--min-mentions 3` отсеивает случайные совпадения

```python
ENTITY_PATTERNS = {
    "projects": r'\b(AgentFS|CardIndex|Yodoca|NGT Memory|...)\b',
    "people":   r'\b([А-Я][а-я]+\s[А-Я][а-я]+|@\w+)\b',
    "tech":     r'\b(RAG|MCP|LLM|BM25|TF-IDF|...)\b',
    "dates":    r'\b(202[3-9]-\d{2}|\d{1,2}\s(?:января|февраля|...))\b',
}
```

### Противоречия между утверждениями

`improve_contradiction_check.py` — инвертированный индекс (не O(n²)):
```
1. Парсим все утверждения → (тип, ключевые_слова, числовое_значение)
2. Инвертированный индекс: (тип, слово) → [список утверждений]
3. В каждом бакете: сравниваем числа (рост vs падение, +N% vs -N%)
4. MAX_BUCKET=50 — отсекаем шум от частых слов
5. MIN_NUM=3.0 — игнорируем номера списков (1., 2., 3.)
```
## Уровень 3 — Индексирование (Indexing)

### Цель
Построить структуры данных для быстрого поиска и анализа по всему корпусу.

### Типы индексов в Lorenzo

#### 3.1 Полнотекстовый поисковый индекс

`improve_search_index.py` → `docs/search_index.json`

```json
{
  "source": "docs/05-habr-projects/memory/yodoca.md",
  "title": "Yodoca — система памяти",
  "content": "полный текст до 3000 символов",
  "preview": "первые 500 символов",
  "words": 1247,
  "tags": ["memory", "agent", "yodoca"]
}
```

Особенности:
- Инкрементальное обновление (`improve_index_update.py`) — не пересчитывает неизменённые файлы
- Используется в `mcp_server.py` и `improve_llm_qa.py` как источник для RAG

#### 3.2 Инвертированный индекс слов

`improve_keyword_index.py` → `keyword_index.json`

```
слово → [{file, count, tf}, ...]
биграмма → [{file, count}, ...]
```

- Топ-2000 слов + топ-500 биграмм
- Используется в `improve_faceted_search.py`
- Поиск: O(1) по слову, без перебора файлов

#### 3.3 BM25-корпус абзацев

`improve_passage_retrieval.py --index` → `passages.json`

Формат одного абзаца:
```json
{
  "source": "docs/04-ai-collaborations/00-intro.md",
  "text": "первые 300 символов абзаца",
  "tokens": ["агент", "память", "rag", ...],
  "wc": 87
}
```

BM25-параметры: k1=1.5, b=0.75 (стандарт Okapi BM25)

#### 3.4 Семантические чанки для RAG

`improve_chunk_semantic.py` → `docs/chunks/*.jsonl`

Стратегия разбивки:
```
H1/H2/H3 заголовок → граница чанка
Целевой размер: 300-800 слов
Перекрытие: 50 слов (overlap)
ID чанка: MD5(source + heading + offset)
```

Формат JSONL (один чанк = одна строка):
```json
{"id": "a3f...", "source": "...", "section": "...", "text": "...", "words": 412}
```

Сейчас: 2063 чанка по 8 секциям (не охватывает nautilus/obsidian).

#### 3.5 Граф концептов

`improve_concept_graph.py` → `concept_graph.json` + `CONCEPT_GRAPH.md`

```json
{
  "nodes": [{"id": "agent", "files": 118, "category": "tech"}],
  "edges": [{"source": "agent", "target": "memory", "weight": 0.73}]
}
```

Используется в:
- `improve_knowledge_map.py` (топ концепты)
- `improve_cross_section.py` (кросс-секционный анализ)

---

## Уровень 4 — Анализ (Analysis)

### Цель
Найти скрытые паттерны, связи и проблемы внутри корпуса.

### 4.1 Кластеризация документов

`improve_clusters.py` — TF-IDF + косинусное расстояние:
```
1. TF-IDF вектор каждого файла
2. K-means (k=8) без sklearn: ручная реализация Lloyd's algorithm
3. Итерации до сходства центроидов < 0.001
```
Выход: `CLUSTERS.md` — тематические группы файлов

`improve_reclassify.py` — применяет кластеры для физического перемещения файлов по папкам (с `--apply`).

### 4.2 Поиск похожих текстов

Два уровня:
- `improve_similar.py` — похожие **файлы** (Jaccard similarity по bag-of-words)
- `improve_similar_passages.py` — похожие **абзацы** (TF-IDF cosine, порог 0.6)

Оба используют инвертированный индекс + MAX_BUCKET=100 для скорости (не O(n²)).

### 4.3 Тематическое моделирование

`improve_topic_model.py` — TF-IDF LDA без sklearn:
```
1. TF-IDF матрица всех файлов
2. SVD-разложение (ручная реализация power iteration)
3. 8-20 тематических кластеров
4. Метки: топ-5 слов кластера
```
Выход: `TOPIC_MODEL.md` — таблица: файл → тема → вес

### 4.4 Кросс-секционный анализ

`improve_cross_section.py` — новый скрипт:
```
1. TF-IDF вектор каждой СЕКЦИИ (агрегация по файлам)
2. Матрица косинусного сходства секций
3. Топ концепты присутствующие в ≥N секциях
4. Mermaid-граф с весами рёбер
```

Результат: Svyazi 2.0 ↔ AI-ансамбли = **0.944** (самая сильная связь)

### 4.5 Метрики качества документов

`improve_paragraph_quality.py`:
- Водяность (короткие предложения без смысла)
- Дублирование абзацев внутри файла
- Обрывочность (абзац <30 слов без контекста)

`improve_vocabulary_richness.py`:
- **TTR** = unique_tokens / total_tokens
- **STTR** = среднее TTR по окнам 100 токенов (стандартизованный)
- **Hapax ratio** = слова встречающиеся только 1 раз
- **Lexical density** = content_words / all_words

`improve_readability_v2.py` — Flesch-Kincaid адаптированный для RU:
```
FRE = 206.835 - 1.015*(слов/предложений) - 84.6*(слогов/слов)
```
## Уровень 5 — Поиск (Retrieval)

### Цель
Найти релевантные фрагменты по запросу пользователя без перебора всего корпуса.

### 5.1 Полнотекстовый поиск через инвертированный индекс

`improve_keyword_index.py --query "агент память"`

Алгоритм:
```
1. Токенизация запроса → список слов
2. Lookup каждого слова в keyword_index.json → бакеты файлов
3. Пересечение бакетов (AND) или объединение (OR)
4. Ранжирование по tf × idf
5. Вывод топ-N файлов с выдержками
```

Скорость: O(k × bucket) где k = слов в запросе, bucket ≈ 50-200 файлов.

### 5.2 BM25 на уровне абзацев

`improve_passage_retrieval.py --query "NGT Memory" --top 10`

Формула BM25:
```
score(q,d) = Σ idf(t) × tf(t,d)×(k1+1) / (tf(t,d) + k1×(1-b+b×|d|/avgdl))
```

Преимущество перед TF-IDF: учитывает длину абзаца (нормализует длинные тексты).

Выход: топ абзацев с указанием файла, позиции, и score BM25.

### 5.3 Фасетный поиск

`improve_faceted_search.py --query "RAG" --section 05-habr-projects --entity "AgentFS"`

Фасеты:
- `--query` — текстовый BM25-поиск
- `--entity` — фильтр по именованной сущности (из named_entities.json)
- `--type` — тип сущности: people / projects / tech / orgs
- `--section` — ограничение по разделу корпуса

Алгоритм:
```
1. BM25 по запросу → кандидаты
2. Пересечение с entity_filter (из named_entities.json)
3. Пересечение с section_filter (по пути файла)
4. Сортировка по score BM25
```

### 5.4 RAG-пайплайн

`improve_llm_qa.py --question "Что такое NGT Memory?"` реализует полный RAG:

```
1. RETRIEVE
   ├─ BM25 по passages.json → топ-5 абзацев
   ├─ TF-IDF по search_index.json → топ-3 документа
   └─ Объединение + дедупликация по source

2. AUGMENT
   └─ Формирование контекста: источник + текст + метаданные

3. GENERATE
   └─ Claude API: system(инструкция) + context(найденное) + user(вопрос)
```

Ключевой паттерн — `_doc_text()` объединяет `content` и `preview` из search_index.json.

### 5.5 Список чтения по теме

`improve_reading_list.py --query "агент с памятью" --top 15`

```
1. BM25-поиск по всем 486 документам
2. Оценка времени чтения (200 сл/мин RU, 250 EN)
3. Группировка по секциям
4. Форматы: md / text / json
```

---

## Уровень 6 — Обогащение (Enrichment)

### Цель
Улучшить качество документов с помощью LLM или автоматических методов.

### 6.1 LLM-суммаризация

`improve_llm_summary.py --file docs/05-habr-projects/memory/yodoca.md`

Каскадная суммаризация для больших файлов:
```
если файл > 4000 слов:
  1. Разбить на чанки по 3000 слов
  2. Суммаризировать каждый чанк
  3. Суммаризировать сводку из сумм
иначе:
  1. Суммаризировать напрямую
```

Стоимость: ~$0.003 за файл (claude-3-5-haiku).

### 6.2 LLM-обогащение проектов

`improve_llm_enrich.py --section 05-habr-projects`

Добавляет в каждый проектный файл:
- Анализ архитектурных решений
- Потенциальные синергии с другими проектами
- Открытые вопросы
- Оценку зрелости (1-10)

Dry-run перед запуском: `--dry-run` показывает план и стоимость (~$0.011 за 21 файл).

### 6.3 Генерация персонализированных сообщений

`improve_llm_contact.py --author kksudo`

```
1. Читает docs/contacts/kksudo.md (профиль + статус)
2. Читает проектный файл (AgentFS)
3. Генерирует сообщение с учётом:
   - Технических деталей проекта
   - Синергий с Svyazi 2.0
   - Тона (техн. коллаборация vs. деловое)
```

### 6.4 Автоматические абстракты (без LLM)

`improve_abstract.py --apply --section 05-habr-projects`

Структура абстракта:
```markdown
<!-- abstract-auto -->
**Проблема:** [первое предложение с ключевыми словами проблемы]
**Подход:** [предложение с методом/решением]
**Результат:** [предложение с числами/достижениями]
```

Алгоритм — TextRank + ключевые слова-триггеры:
- Проблема: "проблема", "задача", "вызов", "необходимо"
- Подход: "используется", "реализован", "основан на", "применяет"
- Результат: числа, %, "достигнуто", "показывает"

### 6.5 Заполнение пробелов (Gap Filler)

`improve_gap_filler.py --apply --mode cite --top 2`

```
1. Найти секции-заглушки (< 50 слов)
2. BM25-поиск по заголовку секции
3. Режим link: вставить ссылки на топ-N файлов
4. Режим cite: вставить первый абзац из топ-N файлов
```

Идемпотентность: маркер `<!-- gap-filled -->` защищает уже заполненные секции.
## Уровень 7 — Синтез (Synthesis)

### Цель
Собрать разрозненные данные в цельные артефакты: отчёты, карты, дайджесты.

### 7.1 Executive Summary

`improve_export_report.py --title "Svyazi — Brief"`

Агрегирует из уже существующих документов:
```
CONTACTS.md     → ключевые авторы и проекты
DECISIONS.md    → архитектурные решения
QUESTIONS.md    → открытые вопросы
METRICS.md      → метрики качества корпуса
READING_LIST.md → топ-N рекомендованных документов
```

Выход: `docs/REPORT.md` — единый документ для презентации.

### 7.2 Еженедельный автодайджест

`improve_digest_auto.py --days 7`

Алгоритм:
```
1. git log --since={7 дней} --name-only → список изменённых файлов
2. git diff {SHA}..HEAD → тексты изменений
3. Токенизация diff-текста → слова добавленные / удалённые
4. Новые концепты: слова ≥3 раз в добавленном, 0 раз в удалённом
5. Выход: DIGEST_AUTO.md (новые файлы, изменённые секции, новые концепты)
```

### 7.3 Карта знаний

`improve_knowledge_map.py`

Единый дашборд корпуса в `KNOWLEDGE_MAP.md`:
- Корпус: документов, слов, секций, RAG-чанков
- Метрики качества: здоровье репо, STTR, пустые секции, противоречия
- Таблица по секциям: файлов / слов / ср. слов/файл
- Топ концептов и сущностей
- Открытые вопросы (из QUESTIONS.md)
- Быстрые команды

### 7.4 Tech Radar

`improve_tech_radar.py`

Классифицирует 22 технологии по кольцам:
```
ADOPT  — проверено, рекомендуется (BM25, TF-IDF, TextRank)
TRIAL  — испытывается (MCP, RAG-pipeline, concept graph)
ASSESS — изучается (embeddings, vector DB)
HOLD   — не рекомендуется (sklearn зависимости)
```

Выход: `docs/TECH_RADAR.md` + таблица по категориям.

### 7.5 Матрица компонентов

`improve_component_matrix.py`

Матрица 14 компонентов × 10 возможностей (поиск, суммаризация, экспорт, ...):
- ✅ поддерживается
- ⚠️ частично
- ❌ не поддерживается

### 7.6 Граф концептов

`improve_concept_graph.py --format dot`

```
Узлы: концепты (agent, memory, RAG, ...)
Рёбра: совместное упоминание в одном документе
Веса: нормализованная частота совместного появления
```

Выходы:
- `concept_graph.json` — для Python-инструментов
- `CONCEPT_GRAPH.md` — Mermaid-граф для GitHub
- `concept_graph.dot` — для Graphviz (PDF/SVG)

---

## Уровень 8 — Экспорт и Действие

### Цель
Доставить результаты туда, где они нужны: другим системам, людям, платформам.

### 8.1 Obsidian Vault

`improve_obsidian.py`

Преобразует корпус для Obsidian:
- YAML frontmatter: `tags`, `created`, `modified`, `section`
- `[[wikilinks]]` вместо `[text](path.md)` — для граф-вью Obsidian
- Сохраняет оригиналы (работает на копии в `vault/`)

### 8.2 EPUB

`improve_epub.py --section 01-svyazi`

```
1. Собирает файлы секции по порядку (00-intro.md первый)
2. Pandoc: markdown → EPUB с оглавлением
3. Метаданные из frontmatter первого файла
```

Требует: `apt install pandoc`

### 8.3 RSS / Atom фид

`improve_rss.py`

```
git log --format="%H %ai %s" -- docs/ → список изменений
→ docs/feed.rss (RSS 2.0)
→ docs/feed.atom (Atom 1.0)
```

Используется в CI: подписчики получают уведомления об изменениях.

### 8.4 Confluence Wiki

`improve_confluence.py`

Конвертирует Markdown → Confluence Storage Format:
- Заголовки → `<h1>` ... `<h6>`
- Код-блоки → `<ac:structured-macro ac:name="code">`
- Таблицы → `<table>`

### 8.5 GitHub Issues

`improve_github_issues.py`

```
1. Читает CONTENT_GAPS.md, QUESTIONS.md, ACTION_ITEMS.md
2. Форматирует в списки задач с метками (label: gap / question / todo)
3. Опционально: создаёт через gh CLI (gh issue create)
```

### 8.6 CI/CD автоматизация

`.github/workflows/docs.yml` — безопасный вариант:
```yaml
jobs:
  update-docs:
    steps:
      - run: python scripts/improve_search_index.py
      - run: python scripts/improve_rss.py
      - run: python scripts/improve_health.py
      - run: |
          git add docs/search_index.json docs/feed.rss docs/feed.atom docs/HEALTH.md
          git diff --staged --quiet || git commit -m "docs: auto-update [skip ci]"
```

Принцип безопасности: `git add` только конкретные файлы, никогда `git add docs/`.
## Шаблоны и Скиллы

### Архитектурный принцип

```
Скрипт (КАК) → Шаблон (ЧТО) → Скилл (КОГДА) → Плагин (ГДЕ)
```

Каждая ступень оркестрирует предыдущую, не заменяя её.

### Шаблоны документов

`docs/templates/` — 6 шаблонов:

| Шаблон | Назначение |
|--------|-----------|
| `project.md` | Проектный файл: проблема/решение/архитектура/синергии |
| `contact.md` | Профиль автора: статус/проект/заметки |
| `decision.md` | ADR: контекст/решение/последствия |
| `reading-note.md` | Заметка о прочитанном |
| `weekly-review.md` | Еженедельный обзор |
| `experiment.md` | Эксперимент: гипотеза/метод/результат |

Шаблоны заполняются автоматически:
```bash
python scripts/improve_autofill.py  # создаёт docs/contacts/*.md из CONTACTS.md
```

### Claude Code Скиллы

`.claude/skills/` — 4 скилла (вызов через `/skill-name`):

**`/analyze-project`** — анализ проекта из docs/:
- Читает проектный файл
- Выявляет архитектурные решения
- Предлагает синергии с другими проектами в базе

**`/write-contact`** — помощь в написании первого сообщения:
- Анализирует профиль автора
- Учитывает технические детали проекта
- Адаптирует тон (академический / деловой / неформальный)

**`/review-docs`** — рецензия документа:
- Структурный анализ (заголовки, связность)
- Оценка полноты (нет ли пробелов)
- Конкретные правки

**`/improve`** — универсальный улучшатель:
- Применяется к любому элементу (файл, скрипт, конфиг)
- Предлагает план улучшений
- Реализует после подтверждения

---

## MCP-сервер

### Обзор

`scripts/mcp_server.py` — stdio-совместимый MCP-сервер с 7 инструментами.

Запуск для Claude Desktop:
```json
{
  "mcpServers": {
    "lorenzo": {
      "command": "python",
      "args": ["/path/to/scripts/mcp_server.py"]
    }
  }
}
```

### 7 инструментов MCP

| Инструмент | Описание |
|-----------|---------|
| `search_docs` | BM25-поиск по search_index.json |
| `get_document` | Полный текст документа по пути |
| `list_sections` | Список секций с количеством файлов |
| `get_entities` | Именованные сущности из named_entities.json |
| `get_concepts` | Граф концептов из concept_graph.json |
| `get_questions` | Открытые вопросы из QUESTIONS.md |
| `get_contacts` | Список авторов и статус из CONTACTS.md |

### Источники данных MCP

```
search_docs    → docs/search_index.json (content + preview)
get_entities   → named_entities.json
get_concepts   → concept_graph.json
get_questions  → docs/QUESTIONS.md
get_contacts   → docs/CONTACTS.md
```

Сервер работает без LLM — только локальные файлы и индексы.

---

## Оркестратор (improve_run_all.py)

### Группы скриптов

| Группа | Скриптов | Назначение |
|--------|----------|-----------|
| `reports` | 8 | Метрики, здоровье, scoring |
| `quality` | 4 | Орфография, читаемость, пробелы |
| `analytics` | 6 | Темы, цитирование, кросс-анализ |
| `export` | 5 | EPUB, Obsidian, RSS, Confluence |
| `cicd` | 4 | GitHub Issues, CI-конфиги |
| `textwork` | 8 | Рубрикация, слияние, сравнение |
| `deeptext` | 12 | TOC, NER, BM25, граф, чанки |
| `nlpplus` | 10 | TextRank, аудит, поиск, похожие |
| `content` | 4 | Применение изменений к файлам |
| `meta` | 9 | Tech radar, онбординг, риски |

### Режимы запуска

```bash
--smart      # пропускает скрипты с метрикой > порога (SMART_CONDITIONS)
--fast       # пропускает SLOW_SCRIPTS (>10 сек)
--parallel N # N параллельных воркеров (группы независимы)
--changed    # только группы для файлов, изменённых с последнего коммита
--group X    # только одна группа
```

### Инкрементальный режим

`improve_index_update.py` — обновляет search_index.json только для изменённых файлов:
```
1. git diff HEAD --name-only -- docs/ → список изменённых
2. Обновить только эти записи в search_index.json
3. Полная пересборка не нужна (экономия 80% времени)
```

`improve_watch.py` — polling-воркер:
```python
while True:
    изменённые = git_changed_since(last_check)
    if изменённые:
        run_scripts_for(изменённые)
    sleep(30)
```
## Инновационные и перспективные подходы

### Реализованные нестандартные решения

#### Ручная реализация алгоритмов без ML-библиотек

Весь Lorenzo работает без numpy, sklearn, torch:

| Алгоритм | Стандартный инструмент | В Lorenzo |
|---------|----------------------|---------|
| TF-IDF | sklearn.TfidfVectorizer | Ручной подсчёт через Counter |
| K-means | sklearn.KMeans | Lloyd's algorithm, ручная реализация |
| SVD | numpy.linalg.svd | Power iteration (ручная) |
| BM25 | rank_bm25 | Прямая формула Okapi |
| PageRank | networkx | Матричное умножение, ручная |
| Cosine sim | scipy.spatial | Dot product / норма вручную |

**Причина**: нулевые зависимости → работает везде, включая CI и edge-устройства.

#### Инвертированный индекс для O(1) поиска

Паттерн применяется везде где нужен поиск без O(n²):
```python
# Построение (однократно)
index = defaultdict(list)
for doc in corpus:
    for word in tokenize(doc):
        index[word].append(doc_id)

# Поиск (мгновенно)
candidates = set.intersection(*[set(index[w]) for w in query_words])
```

Используется в: keyword_index, contradiction_check, similar_passages, faceted_search.

#### Идемпотентные маркеры как протокол

Вместо базы данных состояния — маркеры прямо в файлах:
```markdown
<!-- abstract-auto -->   ← этот файл уже обработан improve_abstract.py
<!-- toc-auto -->        ← TOC актуален
<!-- textrank-summary --> ← резюме вставлено TextRank
```

Преимущество: файл сам несёт свою метаданные, независимо от БД или реестра.

---

### Направления, не реализованные (возможности)

#### Векторный поиск (embeddings)

Текущий Lorenzo: BM25 (лексический поиск) — работает только если слова совпадают.

**Следующий шаг**: embeddings через Anthropic API или локальная модель (e.g. nomic-embed):
```python
# Вместо BM25
embedding = anthropic.embeddings.create(text=query)
results = vector_db.search(embedding, top_k=10)
```

Даёт: семантический поиск ("агент с долгосрочной памятью" найдёт "persistent memory system").

#### Граф знаний (Knowledge Graph)

Текущий concept_graph.json — граф совместных упоминаний (co-occurrence).

**Следующий шаг**: граф с типизированными рёбрами:
```
AgentFS --реализует--> файловый слой
AgentFS --использует--> FUSE
AgentFS --совместим-с--> Yodoca
NGT Memory --альтернатива--> Yodoca
```

Позволяет: рассуждения типа "найди все реализации файлового слоя, совместимые с Yodoca".

#### Мультидокументная суммаризация

Текущий: суммаризация каждого файла по отдельности.

**Следующий шаг**: суммаризация кластера (например, всех файлов про memory):
```
1. Кластеризация → 8 тематических групп
2. BM25 → топ-5 документов каждой группы
3. LLM: "напиши синтез этих 5 документов в одном абзаце"
```

#### Автоматическое обнаружение пробелов через граф

Текущий `improve_content_gaps.py`: сравнивает упомянутые темы с существующими файлами.

**Следующий шаг**: анализ "дыр" в графе концептов:
```
Если концепт A → концепт B → концепт C
Но нет файла, связывающего A и C напрямую
→ Предложить написать "A через C"
```

#### Инкрементальный RAG с верификацией источников

**Forensic RAG** (упомянут в QUESTIONS.md):
```
Ответ = {
    "text": "Yodoca использует NGT Memory как бэкенд",
    "evidence": [
        {"source": "docs/memory/yodoca.md", "line": 47, "quote": "..."}
    ],
    "confidence": 0.87
}
```

Доказуемость: каждое утверждение привязано к конкретной строке источника.

#### Агентный цикл (Agentic Loop)

Текущий `improve_watch.py`: реактивный — запускается при изменении файлов.

**Следующий шаг**: проактивный агент:
```
1. Анализирует CONTENT_GAPS.md
2. Выбирает наивысший приоритет
3. Ищет BM25 по теме
4. Пишет черновик (LLM)
5. Ждёт подтверждения человека
6. Коммитит
7. Повторяет
```

#### Персонализированный дайджест

Текущий `improve_digest_auto.py`: единый дайджест для всех.

**Следующий шаг**: профиль читателя:
```python
profile = {
    "interests": ["memory", "agent", "RAG"],
    "read": ["yodoca.md", "agentfs.md"],
    "preferred_length": "short"
}
digest = personalized_digest(profile, recent_changes)
```

---

### Метрики для оценки эффективности

| Метрика | Инструмент | Значение |
|--------|-----------|---------|
| Покрытие индекса | search_index.json | 1162 из 1162 файлов |
| BM25-корпус | passages.json | ~8K абзацев |
| RAG-чанки | chunks/*.jsonl | 2063 (8 секций) |
| Словарное богатство | STTR | 0.636 |
| Здоровье репо | HEALTH.md | 77/100 |
| Противоречий найдено | CONTRADICTIONS.md | 9367 |
| Пустых секций | EMPTY_SECTIONS.md | 1632 |
| Уникальных концептов | concept_graph.json | ~500 узлов |
