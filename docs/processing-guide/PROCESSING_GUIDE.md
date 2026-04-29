# Обработка больших массивов документов — Полное руководство

> Всё о том, как превратить неструктурированные документы (MHTML, Markdown, PDF) в управляемую, поисковую и обогащённую базу знаний.
> Основано на реальной практике: 9 исходных файлов → 483 структурированных документа в проекте Lorenzo.

---

## Содержание

1. [Обзор и таксономия](#часть-1-обзор-и-таксономия)
2. [Извлечение](#часть-2-извлечение)
3. [Чанкинг](#часть-3-чанкинг)
4. [Структурирование](#часть-4-структурирование)
5. [Анализ и NLP](#часть-5-анализ-и-nlp)
6. [Поиск](#часть-6-поиск)
7. [LLM-обогащение](#часть-7-llm-обогащение)
8. [Экспорт и интеграции](#часть-8-экспорт-и-интеграции)
9. [Автоматизация](#часть-9-автоматизация)
10. [Инновационные подходы](#часть-10-инновационные-подходы)

---


---

## Обработка больших массивов информации — Часть 1: Обзор и таксономия

> Руководство по всем доступным методам обработки разрозненных документов в проекте Lorenzo / Svyazi 2.0.

---

## Проблема

Когда у вас есть **большой разрозненный массив информации** — сохранённые сессии ChatGPT/Claude (MHTML), исследовательские отчёты, статьи с Хабра, технические документы — перед вами стоит задача:

1. **Извлечь** текст из разных форматов
2. **Разбить** на смысловые единицы
3. **Организовать** по темам и связям
4. **Обогатить** — найти то, что не видно напрямую
5. **Сделать доступным** — поиск, экспорт, навигация
6. **Автоматизировать** — чтобы работало без ручного труда

---

## Таксономия методов

Все доступные методы разбиты на **8 уровней** — от базовых до экспериментальных:

```
Уровень 0: ИСТОЧНИКИ        ← форматы: MD, MHTML, PDF, HTML, TXT
    ↓
Уровень 1: ИЗВЛЕЧЕНИЕ       ← парсинг, конвертация, нормализация
    ↓
Уровень 2: РАЗБИВКА         ← чанкинг, сегментация, дробление
    ↓
Уровень 3: СТРУКТУРИРОВАНИЕ ← теги, заголовки, шаблоны, связи
    ↓
Уровень 4: АНАЛИЗ           ← NLP, граф, противоречия, тональность
    ↓
Уровень 5: ПОИСК            ← BM25, фасеты, семантика, пассажи
    ↓
Уровень 6: LLM-ОБОГАЩЕНИЕ   ← резюме, вопросы, gaps, контакты
    ↓
Уровень 7: ЭКСПОРТ          ← Obsidian, Confluence, EPUB, RSS, RAG
    ↓
Уровень 8: АВТОМАТИЗАЦИЯ    ← оркестратор, watcher, CI/CD, MCP
```

---

## Что реализовано в Lorenzo

| Уровень | Скриптов | Статус |
|---------|---------|--------|
| 0 — Источники | `extract_mhtml.py`, `organize_docs.py` | ✅ |
| 1 — Извлечение | `part2_split_md.py` … `part8_collaborations.py` | ✅ |
| 2 — Разбивка | `improve_chunk_semantic.py`, `improve_text_segmenter.py` | ✅ |
| 3 — Структурирование | `improve_autofill.py`, `improve_auto_toc.py`, `improve_crosslink_all.py` | ✅ |
| 4 — Анализ | `improve_concept_graph.py`, `improve_contradiction_check.py`, `improve_textrank.py` | ✅ |
| 5 — Поиск | `improve_passage_retrieval.py`, `improve_faceted_search.py`, `improve_reading_list.py` | ✅ |
| 6 — LLM-обогащение | `improve_llm_*.py` × 5 | ✅ написаны, ждут API |
| 7 — Экспорт | `improve_obsidian.py`, `improve_epub.py`, `improve_confluence.py` | ✅ |
| 8 — Автоматизация | `improve_run_all.py`, `improve_watcher.py`, `mcp_server.py` | ✅ |

**Итого: 129 скриптов + 5 LLM + MCP-сервер + 4 Claude Skills + 6 шаблонов**

---

## Навигация по разделам

| Часть | Тема |
|-------|------|
| [02-extraction](02-extraction.md) | Извлечение: MHTML, PDF, HTML → Markdown |
| [03-chunking](03-chunking.md) | Разбивка: чанкинг, сегментация, слияние |
| [04-structuring](04-structuring.md) | Структурирование: теги, TOC, шаблоны, автозаполнение |
| [05-analysis](05-analysis.md) | Анализ: NLP, граф, NER, противоречия, тональность |
| [06-search](06-search.md) | Поиск: BM25, фасеты, пассажи, список чтения |
| [07-llm](07-llm.md) | LLM-обогащение: резюме, Q&A, gaps, контакты |
| [08-export](08-export.md) | Экспорт: форматы, RAG-пайплайн, интеграции |
| [09-automation](09-automation.md) | Автоматизация: оркестратор, watcher, CI/CD, MCP |
| [10-future](10-future.md) | Инновационные и ещё не придуманные подходы |

---

## Обработка больших массивов — Часть 2: Извлечение

> Как превратить сырые файлы (MHTML, PDF, HTML, TXT) в чистый Markdown.

---

## Проблема формата

Исходные файлы проекта Lorenzo — это **MHTML-архивы** (сохранённые страницы браузера из Claude.ai и ChatGPT). Внутри MHTML:
- Base64-закодированный HTML
- CSS, скрипты, изображения в одном файле
- Текст чата перемешан с UI-элементами
- Кодировка: quoted-printable или base64

Прямо читать нельзя — нужен парсер.

---

## Уровень 1: extract_mhtml.py

**Что делает:** MHTML → чистый Markdown

```bash
python scripts/extract_mhtml.py "Вакансии в Anthropic - Claude" output.md
```

**Алгоритм:**
1. Разбирает MIME-структуру файла (`email.message_from_bytes`)
2. Извлекает HTML-части (text/html)
3. Декодирует base64 / quoted-printable
4. BeautifulSoup: убирает `<script>`, `<style>`, навигацию
5. html2text или кастомный конвертер → Markdown
6. Постобработка: убирает дублированные переносы, артефакты UI

**Результат:**
```
7.6 МБ MHTML  →  ~165 000 слов чистого текста
```

---

## Уровень 2: organize_docs.py + part*.py

После извлечения текст **дробится по секциям** (часть 3).

Скрипты `part1_utils.py` … `part8_collaborations.py` — специализированные парсеры для каждого типа источника:

| Скрипт | Источник | Что делает |
|--------|---------|-----------|
| `part2_split_md.py` | Markdown | Делит по H2-заголовкам |
| `part3_mhtml.py` | MHTML (общий) | Базовое извлечение |
| `part4_svyazi.py` | deep-research-report | Парсит архитектурные секции |
| `part5_mhtml_engine.py` | MHTML (движок) | Расширенная очистка HTML |
| `part6_vacancies.py` | «Вакансии» | Кластеры вакансий Anthropic |
| `part7_tech_combinations.py` | «Комбинирование» | Синергии технологий |
| `part8_collaborations.py` | «Коллаборации» | Проекты и ансамбли |

---

## Поддерживаемые форматы

### Уже реализовано

| Формат | Инструмент | Примечание |
|--------|-----------|-----------|
| **MHTML** | `extract_mhtml.py` | Claude.ai, ChatGPT, любые браузеры |
| **Markdown** | `part2_split_md.py` | Нативный формат |
| **HTML** | `improve_export_html.py` | Обратный экспорт |

### Можно добавить (не реализовано)

| Формат | Библиотека | Сложность |
|--------|-----------|----------|
| **PDF** | `pdfplumber`, `PyMuPDF` | Средняя (таблицы сложно) |
| **DOCX/PPTX** | `python-docx`, `python-pptx` | Низкая |
| **Telegram-экспорт** | `json` (нативный формат) | Низкая |
| **Notion** | Notion API | Средняя |
| **Obsidian** | `markdown` (готово) | Готово |
| **Epub** | `ebooklib` | Средняя |
| **YouTube-субтитры** | `youtube-transcript-api` | Низкая |
| **Аудио/видео** | `whisper` (OpenAI) | Высокая |

---

## Качество извлечения

После парсинга MHTML «Вакансии» (7.6 МБ):

```
Исходный файл:    7 936 771 байт  (MHTML)
Чистый HTML:      ~4 200 000 байт
После html2text:  ~850 000 байт
Итоговый Markdown: ~610 000 слов  (в 357 файлах)
```

**Потери:** ~15% — UI-элементы, повторяющиеся кнопки «Copy», временны́е метки.
**Сохранено:** 100% текстового содержимого чата.

---

## Типичные проблемы и решения

| Проблема | Причина | Решение |
|---------|---------|---------|
| Артефакты `citeturnXXview0` | Claude.ai внутренние ссылки на источники | Постобработка regex |
| Дублированный текст | «Thinking» блоки + ответ | Фильтр по CSS-классам |
| Обрезанные заголовки | H2 > 60 символов → slug обрезается | `slugify` с полным текстом |
| Пустые файлы | Секции только с UI | Фильтр по минимуму слов |
| Кириллические имена файлов | Windows/Linux несовместимость | `pathlib` + UTF-8 |

---

## Следующий шаг после извлечения

После получения Markdown → **Часть 3: Разбивка на смысловые единицы**

---

## Обработка больших массивов — Часть 3: Разбивка и чанкинг

> Как правильно делить большой текст на смысловые части.

---

## Зачем делить?

Большой файл (50 000+ слов) — проблема для:
- **Поиска**: невозможно найти конкретный факт
- **LLM**: не влезает в контекстное окно
- **RAG**: слишком широкий чанк = шум в ответе
- **Навигации**: человек не читает монолит
- **Версионирования**: любое изменение — diff всего файла

---

## Стратегии разбивки

### Стратегия 1: По заголовкам (H2/H3) — реализовано

```python
# utils_chunker.py — chunk_by_headers()
```

**Как работает:**
- H1 = документ
- H2 = раздел → отдельный файл
- H3 = подраздел → чанк внутри файла

**Плюсы:** Сохраняет авторскую структуру, смысловые границы чёткие.
**Минусы:** Если автор плохо структурировал — секции неравномерные.

**Скрипт:** `part2_split_md.py`, `improve_text_segmenter.py`

```bash
python scripts/improve_text_segmenter.py --dry-run        # план
python scripts/improve_text_segmenter.py --apply --section 02-anthropic-vacancies
```

---

### Стратегия 2: Семантические чанки — реализовано

```python
# improve_chunk_semantic.py
```

**Как работает:**
1. H2/H3 = первичные границы
2. Если секция > 500 слов → дробить по абзацам
3. Если секция < 50 слов → объединить с соседней
4. Каждый чанк: `{file, section, text, word_count, tokens_est}`

**Вывод:** `docs/all_chunks.jsonl` — готово для RAG

```bash
python scripts/improve_chunk_semantic.py
python scripts/improve_chunk_semantic.py --section 05-habr-projects
```

**Пример чанка:**
```json
{
  "file": "docs/04-ai-collaborations/01-executive-summary.md",
  "section": "Executive summary",
  "text": "Если смотреть не на отдельные статьи...",
  "word_count": 312,
  "tokens_est": 520,
  "chunk_id": "04-ai-collaborations/01#executive-summary"
}
```

---

### Стратегия 3: Разбивка по абзацам (BM25-уровень) — реализовано

```python
# improve_passage_retrieval.py
```

**Как работает:** Каждый абзац (≥ 20 слов) — отдельная единица поиска.

**Зачем:** Для точного поиска — не «в каком файле», а «в каком абзаце».

```bash
python scripts/improve_passage_retrieval.py --index
python scripts/improve_passage_retrieval.py --query "ассоциативный граф памяти" --top 5
```

---

### Стратегия 4: Разбивка по теме (TF-IDF рубрикация) — реализовано

```python
# improve_reclassify.py
# improve_topic_model.py
```

**Как работает:** TF-IDF по словам → определяет к какому тематическому кластеру относится файл → перемещает если ошибочно классифицирован.

```bash
python scripts/improve_reclassify.py --section 02-anthropic-vacancies --dry-run
python scripts/improve_topic_model.py --topics 8
```

---

### Стратегия 5: Слияние коротких файлов по теме — реализовано

```python
# improve_merge_by_topic.py
# improve_merge_short.py
```

**Проблема:** После дробления появляются файлы по 50–100 слов — слишком мелко.

**Решение:**
- `merge_short`: объединяет файлы < 100 слов с соседними
- `merge_by_topic`: TF-IDF кластеризация → близкие файлы → один файл

```bash
python scripts/improve_merge_by_topic.py --section 02-anthropic-vacancies --dry-run
python scripts/improve_merge_short.py --min-words 150
```

---

### Стратегия 6: Разбивка по языку — реализовано

```python
# improve_language_split.py
```

**Проблема:** Файлы с MIX RU/EN — сложно индексировать, читать, переводить.

```bash
python scripts/improve_language_split.py                  # статистика
python scripts/improve_language_split.py --split          # разделить
```

---

## Параметры разбивки: что выбрать

| Задача | Стратегия | Размер чанка |
|--------|----------|-------------|
| RAG (LLM-поиск) | Семантический | 200–500 слов |
| Полнотекстовый поиск | По заголовкам | 500–2000 слов |
| Точный поиск фактов | По абзацам | 50–200 слов |
| Навигация человека | По заголовкам H2 | 300–1500 слов |
| Тематическое хранение | По теме (TF-IDF) | любой |

---

## Инструмент выбора стратегии: utils_chunker.py

```python
from scripts.utils_chunker import chunk_by_headers, estimate_tokens

chunks = chunk_by_headers(text, max_words=500, min_words=50)
for chunk in chunks:
    print(f"{chunk['section']}: {chunk['word_count']} слов, ~{estimate_tokens(chunk['text'])} токенов")
```

---

## Следующий шаг

После разбивки → **Часть 4: Структурирование (теги, TOC, шаблоны)**

---

## Обработка больших массивов — Часть 4: Структурирование

> Как превратить набор текстовых файлов в связанную, навигируемую базу знаний.

---

## Проблема неструктурированности

После извлечения и разбивки у вас есть N файлов с текстом. Но они:
- Не связаны ссылками между собой
- Не имеют единого формата метаданных
- Нет оглавлений
- Нет тегов для фильтрации
- Нет шаблонов — каждый файл уникален по структуре

---

## Инструмент 1: Автоматические метаданные — improve_autofill.py

**Что делает:** Читает шаблоны из `docs/templates/` и автоматически заполняет поля в каждом файле.

```bash
python scripts/improve_autofill.py --dry-run  # план без изменений
python scripts/improve_autofill.py            # применить
```

**Вставляет в каждый файл:**
```markdown
<!-- summary: краткое описание -->
<!-- tags: memory, rag, collaboration -->

## Статус
| Параметр | Значение |
|----------|---------|
| Упоминаний в репо | 13 |
| Слой | knowledge/filesystem |
| Контакт | [@kksudo](../../contacts/kksudo.md) |
```

---

## Инструмент 2: Оглавления — improve_auto_toc.py

**Что делает:** Добавляет `## Содержание` с якорными ссылками в каждый файл с 3+ заголовками.

```bash
python scripts/improve_auto_toc.py --apply --min-headings 3
```

**Результат:**
```markdown
## Содержание
- [Извлечение](#извлечение)
- [Разбивка](#разбивка)
  - [По заголовкам](#по-заголовкам)
  - [Семантическая](#семантическая)
- [Экспорт](#экспорт)
```

**Идемпотентно** — повторный запуск не дублирует TOC.

---

## Инструмент 3: Теги — improve_tags.py

**Что делает:** TF-IDF по тексту → предлагает теги → записывает в `<!-- tags: -->`.

```bash
python scripts/improve_tags.py
```

**Теги используются для:**
- Фасетного поиска (`improve_faceted_search.py --type projects`)
- Тематической карты (`improve_topic_model.py`)
- Obsidian-тегов (`improve_obsidian.py`)

---

## Инструмент 4: Перекрёстные ссылки — improve_crosslink_all.py

**Что делает:**
1. Сканирует все файлы, строит граф «кто на кого ссылается»
2. Инвертирует: добавляет блок «Упоминается в» в каждый файл
3. По ключевым словам добавляет «Связанные документы» (TF-IDF cosine)

```bash
python scripts/improve_crosslink_all.py --apply --keywords
```

**Результат:**
```markdown
## Упоминается в
- [Executive summary](../04-ai-collaborations/01-executive-summary.md)
- [MVP Planning](07-mvp-planning.md)

## Связанные документы
- [NGT Memory](../05-habr-projects/memory/ngt-memory.md) 71%
- [Yodoca](../05-habr-projects/memory/yodoca.md) 68%
```

---

## Инструмент 5: Шаблоны — docs/templates/

Шаблоны определяют **стандартную структуру** для каждого типа документа:

| Шаблон | Для чего | Поля |
|--------|---------|------|
| `project-component.md` | Документ проекта | название, лицензия, слой, контакт, статус |
| `contact-outreach.md` | Контактный файл | профиль, статус связи, черновик письма |
| `ensemble.md` | Ансамбль компонентов | участники, синергия, архитектура |
| `decision-record.md` | ADR (решение) | контекст, решение, последствия |
| `research-note.md` | Исследование | вопрос, находки, выводы |

```bash
python scripts/improve_templates.py  # создать/обновить шаблоны
```

---

## Инструмент 6: Автоабстракты — improve_abstract.py

**Что делает:** Без LLM строит абстракт из первых предложений каждого файла в формате «Проблема / Подход / Результат».

```bash
python scripts/improve_abstract.py --dry-run
python scripts/improve_abstract.py --apply --section 05-habr-projects
```

**Результат:**
```markdown
<!-- abstract-auto -->
> **Абстракт** (авто)
> 🎯 **Проблема:** У LLM нет долгосрочной памяти между сессиями
> 🔧 **Подход:** SQLite + FTS5 + асинхронные эмбеддинги
> ✅ **Результат:** hot path < 50 мс без LLM
```

---

## Инструмент 7: See-also и сноски

```bash
python scripts/improve_see_also.py       # блок «Смотрите также»
python scripts/improve_footnotes.py      # глоссарий-сноски
```

**Сноски** позволяют в тексте писать `[^agentfs]`, а в конце файла — расшифровку:
```markdown
[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT, kksudo)
```

---

## Итоговая структура файла после всех инструментов

```markdown
# Название проекта

<!-- summary: краткое описание -->
<!-- tags: memory, rag, local-first -->

<!-- abstract-auto -->
> 🎯 Проблема / 🔧 Подход / ✅ Результат

> [!IMPORTANT] Ключевой документ

## Статус
| Параметр | Значение |
...

## Содержание (TOC)
...

## Основной текст
...

[^термин]: Расшифровка

## Упоминается в
...

## Связанные документы
...

## Смотрите также
...
```

---

## Следующий шаг

После структурирования → **Часть 5: Анализ (NLP, граф, противоречия)**

---

## Обработка больших массивов — Часть 5: Анализ и NLP

> Что можно узнать о массиве документов без использования LLM.

---

## Что такое «анализ без LLM»

Все инструменты этого раздела работают **локально, без API, бесплатно** — на основе классических алгоритмов NLP: TF-IDF, BM25, TextRank, граф, регулярные выражения.

Они медленнее LLM в «понимании», но:
- Детерминированы (один вход = один выход)
- Масштабируются на миллионы документов
- Не требуют оплаты
- Можно запускать в CI/CD

---

## Группа 1: Извлечение сущностей

### improve_entities.py — индекс проектов и технологий

Строит `docs/ENTITIES.md` — таблицу «сущность → сколько раз упомянута → в каких файлах».

```bash
python scripts/improve_entities.py
```

Результат используется `improve_autofill.py` для автоматической расстановки статусов.

---

### improve_named_entity_index.py — NER без ML

Находит без ML-моделей:
- **Проекты:** CamelCase, имена с заглавной, известные OSS-имена
- **Люди:** @handle, «Андрей», «kksudo»
- **Технологии:** Python, SQLite, MCP, BM25
- **Даты:** 2024, Q1 2026, апрель 2026
- **URL:** github.com/…, habr.com/…

```bash
python scripts/improve_named_entity_index.py
python scripts/improve_named_entity_index.py --type projects --min-mentions 3
```

Вывод: `docs/NAMED_ENTITIES.md` + `docs/named_entities.json`

---

### improve_abbreviations.py — словарь аббревиатур

Находит аббревиатуры (2–5 заглавных букв) и их расшифровки в тексте.

```bash
python scripts/improve_abbreviations.py
# MHTML → "MIME HTML archive format"
# BM25  → "Best Match 25, алгоритм ранжирования"
# RAG   → "Retrieval-Augmented Generation"
```

---

## Группа 2: Граф знаний

### improve_concept_graph.py — граф концептов

Строит граф: какие концепты встречаются вместе в одних документах.

```bash
python scripts/improve_concept_graph.py
python scripts/improve_concept_graph.py --format dot  # Graphviz
python scripts/improve_concept_graph.py --top-concepts 50
```

Вывод: `docs/CONCEPT_GRAPH.md` + `docs/concept_graph.json`

**Применение:** Находит неочевидные связи — например, что «CRDT» и «AgentFS» часто упоминаются вместе, хотя нет прямых ссылок.

---

### improve_network.py — граф документов

Строит граф на уровне **файлов** (не концептов): кто на кого ссылается.

```bash
python scripts/improve_network.py
# Вывод: docs/network.dot (Graphviz), docs/NETWORK.md
```

---

### improve_cross_section.py — граф между секциями

Показывает, какие концепты «переходят» из одной секции в другую.

```bash
python scripts/improve_cross_section.py --top 30 --format dot
```

---

## Группа 3: Тематический анализ

### improve_topic_model.py — TF-IDF кластеризация

Без ML делит документы на тематические кластеры.

```bash
python scripts/improve_topic_model.py --topics 8
```

Пример кластеров:
```
Кластер 1 (87 файлов): agentfs, memory, cardindex, vault, filesystem
Кластер 2 (64 файла):  rag, retrieval, embedding, bm25, search
Кластер 3 (51 файл):   sentinel, security, mcp, allowlist, pii
```

---

### improve_clusters.py — похожие документы

TF-IDF cosine similarity → группы похожих файлов.

```bash
python scripts/improve_clusters.py
```

---

## Группа 4: Качество текста

### improve_textrank.py — автоматические резюме

**TextRank** (аналог PageRank для предложений):
1. Строит граф: предложения = вершины, сходство (Jaccard) = рёбра
2. PageRank = важность предложения
3. Топ-N = резюме

```bash
python scripts/improve_textrank.py                    # SUMMARIES.md
python scripts/improve_textrank.py --apply            # вставить в файлы
python scripts/improve_textrank.py --sentences 5      # 5 предложений
python scripts/improve_textrank.py --query "агент с памятью"
```

---

### improve_contradiction_check.py — противоречия

Ищет противоречивые утверждения между файлами.

```bash
python scripts/improve_contradiction_check.py
python scripts/improve_contradiction_check.py --min-confidence 0.6
```

Пример:
```
⚠️ Противоречие (0.72):
  docs/01-svyazi/03-component-catalog.md: "AgentFS поддерживает concurrent доступ"
  docs/01-svyazi/09-architectural-gaps.md: "AgentFS не поддерживает concurrent multi-agent доступ"
```

---

### improve_paragraph_quality.py — качество абзацев

```bash
python scripts/improve_paragraph_quality.py --verbose
```

Находит:
- **Дубли:** одинаковые абзацы в разных файлах (107 найдено)
- **Вода:** абзацы без конкретики («Это интересный подход»)
- **Обрывы:** незаконченные мысли

---

### improve_passive_voice.py — стиль

Находит пассивный залог, номинализации, канцеляризмы.

```bash
python scripts/improve_passive_voice.py
# "было принято решение" → "решили"
# "осуществляется обработка" → "обрабатывается"
```

---

### improve_vocabulary_richness.py — лексическое разнообразие

TTR (Type-Token Ratio), STTR (стандартизированный), hapax legomena (слова, встреченные 1 раз).

```bash
python scripts/improve_vocabulary_richness.py --section 01-svyazi
```

---

## Группа 5: Временной анализ

### improve_timeline_events.py — хронология

Извлекает даты и события из текстов → `docs/TIMELINE.md`.

```bash
python scripts/improve_timeline_events.py --from 2023 --to 2026
```

---

### improve_version_diff.py — семантический diff

Показывает не diff кода, а **что изменилось по смыслу** между коммитами.

```bash
python scripts/improve_version_diff.py --last 10
```

---

## Итог: что можно узнать без LLM

| Вопрос | Инструмент |
|--------|-----------|
| Какие проекты упоминаются чаще всего? | `improve_entities.py` |
| Какие концепты связаны между собой? | `improve_concept_graph.py` |
| Есть ли противоречия? | `improve_contradiction_check.py` |
| О чём каждый файл в 3 предложениях? | `improve_textrank.py` |
| На какие темы делится весь корпус? | `improve_topic_model.py` |
| Где дублируется информация? | `improve_paragraph_quality.py` |
| Что произошло когда? | `improve_timeline_events.py` |

---

## Следующий шаг

После анализа → **Часть 6: Поиск (BM25, фасеты, пассажи)**

---

## Обработка больших массивов — Часть 6: Поиск

> Как найти нужное в 1000+ документах: от простого grep до BM25 и фасетов.

---

## Уровни поиска (от простого к сложному)

```
Уровень 1: grep / find                  — быстро, грубо
Уровень 2: Поисковый индекс             — полнотекстовый, с preview
Уровень 3: BM25 (Okapi)                 — релевантность, не просто вхождение
Уровень 4: Поиск по абзацам (passage)  — точность на уровне абзаца
Уровень 5: Фасетный поиск              — поиск с фильтрами
Уровень 6: Список чтения по теме       — персонализированный маршрут
Уровень 7: Семантический (векторный)   — нужен embedding-модель
Уровень 8: LLM Q&A                     — вопрос → ответ с цитатами
```

---

## Уровень 2: Поисковый индекс — improve_search_index.py

**Строит:** `docs/search_index.json` — 1053 документа, 4.5 МБ

Каждая запись:
```json
{
  "file": "docs/05-habr-projects/memory/yodoca.md",
  "title": "Yodoca: консолидация и забывание",
  "content": "Yodoca — Научил ИИ-агента помнить важное...",
  "preview": "SQLite + FTS5, hot path < 50 мс...",
  "tags": ["memory", "sqlite", "collaboration"],
  "words": 847
}
```

```bash
python scripts/improve_search_index.py
python scripts/improve_index_update.py   # инкрементальное обновление
```

---

## Уровень 3: BM25 — improve_keyword_index.py

**BM25 (Best Match 25)** — стандарт информационного поиска. Лучше TF-IDF:
- Учитывает насыщенность документа (term saturation)
- Учитывает длину документа (document length normalization)
- Параметры: k1=1.5, b=0.75

```bash
python scripts/improve_keyword_index.py                    # построить индекс
python scripts/improve_keyword_index.py --query "агент память"  # поиск
```

**Инвертированный индекс + биграммы:**
```
"агент" → [{file: yodoca.md, score: 4.2}, {file: agentfs.md, score: 3.8}]
"агент память" → [{file: ngt-memory.md, score: 6.1}, ...]
```

---

## Уровень 4: Поиск по абзацам — improve_passage_retrieval.py

**Зачем:** Файл о Yodoca — 800 слов. BM25 найдёт файл. Но нужен **конкретный абзац** про «hot path».

```bash
python scripts/improve_passage_retrieval.py --index                    # построить
python scripts/improve_passage_retrieval.py --query "горячий путь SQLite" --top 5
```

**Результат:**
```
1. [0.847] docs/05-habr-projects/memory/yodoca.md §"hot path"
   "разделение на hot path (запись эпизодов в SQLite + FTS5 за <50 мс, без LLM) и
    slow path (асинхронные эмбеддинги)..."

2. [0.631] docs/04-ai-collaborations/04-приоритетные-ансамбли.md §"Память"
   "Yodoca обеспечивает горячий путь без LLM..."
```

**Применение в RAG:** Этот же `passages.json` можно подавать в LLM как контекст.

---

## Уровень 5: Фасетный поиск — improve_faceted_search.py

**Фасеты** — фильтры поверх полнотекстового поиска:

```bash
# Поиск по тексту в конкретной секции
python scripts/improve_faceted_search.py --query "граф памяти" --section 05-habr-projects

# Поиск файлов с конкретной сущностью
python scripts/improve_faceted_search.py --entity "AgentFS" --top 10

# Только файлы с проектами, изменённые после даты
python scripts/improve_faceted_search.py --type projects --after 2026-01-01

# Комбинация фасетов
python scripts/improve_faceted_search.py \
  --query "безопасность" \
  --entity "SENTINEL" \
  --section 04-ai-collaborations \
  --min-words 300
```

**Аналог:** Google Advanced Search, Elasticsearch с фильтрами.

---

## Уровень 6: Персонализированный список чтения — improve_reading_list.py

**Не просто поиск — маршрут изучения темы:**

```bash
python scripts/improve_reading_list.py --query "агент с памятью"
python scripts/improve_reading_list.py --query "RAG retrieval" --top 20
python scripts/improve_reading_list.py --query "Yodoca" --section 05-habr-projects
python scripts/improve_reading_list.py --format json  # machine-readable
```

**Алгоритм:**
1. BM25 по запросу → базовый score
2. Умножает на важность файла (из PRIORITIES.md)
3. Умножает на связность (количество входящих ссылок)
4. Оценивает время чтения (200 сл/мин RU, 250 EN)
5. Группирует по секциям для логического порядка

**Результат:**
```markdown
## Список чтения: "агент с памятью" (15 документов, ~45 мин)

### docs/05-habr-projects/memory/ (3 документа, ~12 мин)
1. yodoca.md — 847 слов, ~4 мин ⭐
2. ngt-memory.md — 1203 слова, ~6 мин
3. memnet.md — 412 слов, ~2 мин

### docs/04-ai-collaborations/ (4 документа, ~18 мин)
...
```

---

## Уровень 7: Похожие пассажи — improve_similar_passages.py

**Находит дублирующийся контент** между файлами — не точные копии, а **смыслово похожие** абзацы (TF-IDF cosine).

```bash
python scripts/improve_similar_passages.py
python scripts/improve_similar_passages.py --min-sim 0.7  # только очень похожие
```

**Применение:**
- Обнаружить, что одна идея описана в 5 разных местах
- Кандидаты для слияния в один канонический документ

---

## Уровень 8: Семантический поиск (не реализован, план)

**Векторный поиск** — embeddings + cosine similarity:

```python
# Нужно: sentence-transformers или API
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Индексация
embeddings = model.encode([chunk['text'] for chunk in chunks])
# → сохранить в FAISS / ChromaDB / SQLite-vec

# Поиск
query_vec = model.encode("как устроена долгосрочная память агента")
scores = cosine_similarity(query_vec, embeddings)
```

**Преимущество над BM25:** Находит семантически близкие тексты даже без общих слов.

**Почему не реализовано:** Требует ML-модель (200+ МБ) или платный API. BM25 даёт 80% качества при 0% стоимости.

---

## Сравнение методов поиска

| Метод | Точность | Скорость | Стоимость | Реализован |
|-------|---------|---------|----------|-----------|
| grep | низкая | мгновенно | 0 | ✅ |
| Полнотекстовый индекс | средняя | быстро | 0 | ✅ |
| BM25 | высокая | быстро | 0 | ✅ |
| Поиск по абзацам | очень высокая | быстро | 0 | ✅ |
| Фасетный | высокая + фильтры | быстро | 0 | ✅ |
| Семантический (векторный) | очень высокая | средне | модель | ❌ план |
| LLM Q&A | максимальная | медленно | $API | ✅ (ждёт ключа) |

---

## Следующий шаг

После поиска → **Часть 7: LLM-обогащение**

---

## Обработка больших массивов — Часть 7: LLM-обогащение

> Что может сделать языковая модель с документами, чего не может классический алгоритм.

---

## Граница классики и LLM

| Задача | Классика | LLM |
|--------|---------|-----|
| Найти все упоминания «AgentFS» | ✅ grep/BM25 | ✅ |
| Понять что AgentFS *делает* | ❌ | ✅ |
| Найти противоречия | 🟡 (ключевые слова) | ✅ (смысловые) |
| Написать резюме | 🟡 (TextRank) | ✅ (связный текст) |
| Предложить вопрос автору | ❌ | ✅ |
| Заполнить пробелы в документации | ❌ | ✅ |
| Перевести на другой язык | ❌ | ✅ |

---

## Архитектура: 5 LLM-скриптов

```
improve_llm_enrich.py    ← обогатить файл: добавить секции, углубить анализ
improve_llm_qa.py        ← Q&A по базе: вопрос → ответ с источниками
improve_llm_summary.py   ← каскадная суммаризация → DIGEST.md
improve_llm_gaps.py      ← найти пробелы: чего не хватает в документации
improve_llm_contact.py   ← персонализированные письма авторам
```

Все скрипты используют **claude-haiku-4-5** (дешёвый, быстрый) и **prompt caching**.

---

## improve_llm_enrich.py — обогащение файлов

**Что делает:** Читает файл, анализирует и дополняет недостающие секции.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...

python scripts/improve_llm_enrich.py --dry-run       # план + стоимость
python scripts/improve_llm_enrich.py --section 05-habr-projects  # ~$0.003
python scripts/improve_llm_enrich.py --file docs/05-habr-projects/memory/yodoca.md
python scripts/improve_llm_enrich.py --force          # перезаписать уже обогащённые
```

**Добавляет:**
- `## Технические детали` — если не было конкретики
- `## Место в архитектуре Svyazi` — как компонент встраивается
- `## Вопросы для автора` — что стоит уточнить
- `## Альтернативы` — похожие проекты и чем отличается

**Стоимость:**
```
21 файл × ~3000 токенов ≈ $0.011 всего
```

**Prompt caching:** Системный промпт кешируется → повторные запросы дешевле на 90%.

---

## improve_llm_qa.py — Q&A по базе знаний

**Что делает:** Вопрос на русском → поиск BM25 по `search_index.json` → ответ Claude с цитатами.

```bash
python scripts/improve_llm_qa.py --question "Что такое NGT Memory?"
python scripts/improve_llm_qa.py --question "Какая лицензия у Yodoca?"
python scripts/improve_llm_qa.py  # интерактивный режим
```

**Пример:**
```
Вопрос: Чем Yodoca отличается от NGT Memory?

Ответ: Yodoca (Apache 2.0) фокусируется на консолидации эпизодической
памяти через SQLite + FTS5, с явным механизмом "забывания" неважных событий.
NGT Memory (BSL 1.1) использует хеббовский ассоциативный граф: связи между
концептами усиливаются при совместных упоминаниях.

Источники:
- docs/05-habr-projects/memory/yodoca.md (score: 0.87)
- docs/05-habr-projects/memory/ngt-memory.md (score: 0.81)
```

**Кеш:** Повторные вопросы берутся из `docs/qa_cache.json` — бесплатно.

---

## improve_llm_summary.py — каскадная суммаризация

**Проблема:** Документ из 50 000 слов не влезает в контекст.

**Решение — Map-Reduce:**
1. **Map:** Каждая секция → краткое резюме (параллельно)
2. **Reduce:** Все резюме → итоговый дайджест

```bash
python scripts/improve_llm_summary.py --file docs/02-anthropic-vacancies/00-intro.md
python scripts/improve_llm_summary.py --section 01-svyazi
```

**utils_chunker.py** автоматически делит большие документы перед отправкой в API.

---

## improve_llm_gaps.py — пробелы в документации

**Что делает:** Анализирует всю базу знаний и находит:
- Темы, которые упоминаются, но не раскрыты
- Вопросы, которые остались без ответа
- Связи между проектами, которые не задокументированы

```bash
python scripts/improve_llm_gaps.py
# → docs/LLM_GAPS.md
```

---

## improve_llm_contact.py — персонализированные письма

**Что делает:** Читает `docs/contacts/<author>.md` + проектный файл → генерирует персонализированное первое сообщение.

```bash
python scripts/improve_llm_contact.py --author kksudo
python scripts/improve_llm_contact.py --all  # все 14 авторов
```

**Правила:**
- Конкретная ссылка на проект (URL из документа)
- Один конкретный технический вопрос
- Объяснение Svyazi в 1 предложении
- Максимум 5–7 предложений

---

## Стратегии работы с большими документами

### Стратегия 1: Sliding Window

```python
# utils_chunker.py
chunks = chunk_by_headers(text, max_words=2000)
for chunk in chunks:
    result = llm.complete(prompt + chunk['text'])
    results.append(result)
final = llm.complete(reduce_prompt + '\n'.join(results))
```

### Стратегия 2: Иерархическая суммаризация

```
Уровень 3: Абзац → 1 предложение
Уровень 2: Секция → 3 предложения  
Уровень 1: Документ → 1 абзац
Уровень 0: Раздел → 1 страница
```

### Стратегия 3: RAG (Retrieval-Augmented Generation)

```python
# Не передавать весь документ — только релевантные пассажи
query = "как работает hot path в Yodoca"
passages = bm25_search(query, passages_index, top_k=5)
context = '\n---\n'.join([p['text'] for p in passages])
answer = llm.complete(f"На основе контекста:\n{context}\n\nВопрос: {query}")
```

**Этот подход реализован в `improve_llm_qa.py`.**

---

## Оценка стоимости

| Операция | Модель | Стоимость |
|---------|-------|----------|
| Обогатить 1 файл (3K токенов) | claude-haiku-4-5 | ~$0.0005 |
| Обогатить 21 файл | claude-haiku-4-5 | ~$0.011 |
| Q&A 100 вопросов (с кешем) | claude-haiku-4-5 | ~$0.05 |
| Суммаризация 1 большого файла | claude-haiku-4-5 | ~$0.002 |
| 14 персонализированных писем | claude-haiku-4-5 | ~$0.003 |
| **Весь проект целиком** | claude-haiku-4-5 | **~$0.10** |

---

## Следующий шаг

После LLM-обогащения → **Часть 8: Экспорт и интеграции**

---

## Обработка больших массивов — Часть 8: Экспорт и интеграции

> Куда отправить обработанную базу знаний: форматы, платформы, пайплайны.

---

## Зачем экспортировать?

Markdown-база — это хорошо, но разные инструменты требуют разных форматов:
- **Obsidian** — vault с wikilinks и YAML frontmatter
- **Confluence** — корпоративная wiki (`.wiki` разметка)
- **EPUB** — книга для чтения офлайн
- **RSS/Atom** — фид изменений для подписчиков
- **JSONL** — для RAG-пайплайна (LlamaIndex, LangChain)
- **CSV** — для таблиц, Excel, Google Sheets
- **HTML** — для публикации на сайте

---

## Obsidian Vault — improve_obsidian.py

**Что делает:**
- Добавляет YAML frontmatter (теги, дата, тип документа)
- Конвертирует `[text](path/file.md)` → `[[wikilinks]]`
- Копирует в `docs/obsidian/` с сохранением структуры

```bash
python scripts/improve_obsidian.py
# → docs/obsidian/ (1053 файла готовы к открытию в Obsidian)
```

**Результат:** Открыть `docs/obsidian/` как vault в Obsidian → граф связей, поиск, теги.

---

## Confluence — improve_confluence.py

**Что делает:** Конвертирует Markdown → Confluence Wiki Markup (`.wiki`).

```bash
python scripts/improve_confluence.py
# → docs/confluence/**/*.wiki
```

Поддерживает: таблицы, заголовки, блоки кода, ссылки, callout-блоки → `{note}`, `{tip}`.

---

## EPUB — improve_epub.py

**Что делает:** Через `pandoc` собирает всю секцию в книгу.

```bash
python scripts/improve_epub.py --check           # проверить наличие pandoc
python scripts/improve_epub.py --section 01-svyazi
python scripts/improve_epub.py --section 05-habr-projects
```

**Требования:** `apt install pandoc`

---

## RSS/Atom — improve_rss.py

**Что делает:** Читает `git log` → генерирует RSS/Atom фид изменений.

```bash
python scripts/improve_rss.py
# → docs/feed.rss
# → docs/feed.atom
```

**Применение:** Подписчики могут следить за изменениями базы знаний через RSS-ридер.

---

## JSON/CSV — improve_export_json.py, improve_export_csv.py

```bash
python scripts/improve_export_json.py
# → docs/export_full.json  (528 документов, метаданные + текст)

python scripts/improve_export_csv.py
# → docs/export_full.csv  (для Excel, Google Sheets, pandas)
```

**Формат JSON:**
```json
[
  {
    "file": "docs/05-habr-projects/memory/yodoca.md",
    "title": "Yodoca: консолидация и забывание",
    "tags": ["memory", "sqlite"],
    "words": 847,
    "section": "05-habr-projects",
    "content": "Yodoca — Научил ИИ-агента..."
  }
]
```

---

## JSONL для RAG — improve_chunk_semantic.py

**Для LlamaIndex / LangChain / любого RAG-пайплайна:**

```bash
python scripts/improve_chunk_semantic.py
# → docs/all_chunks.jsonl  (семантические чанки, каждый 200-500 слов)
```

**Подключение к LlamaIndex:**
```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser

# Или напрямую из our chunks
import json
chunks = [json.loads(l) for l in open('docs/all_chunks.jsonl')]
```

---

## HTML — improve_export_html.py

```bash
python scripts/improve_export_html.py
# → docs/export_full.html  (статический сайт, можно открыть в браузере)
```

---

## Карта сайта — improve_sitemap.py

```bash
python scripts/improve_sitemap.py
# → docs/SITEMAP.md    (навигационная карта для людей)
# → docs/sitemap.xml   (для поисковых роботов)
```

---

## MCP-сервер — mcp_server.py

**Самая мощная интеграция:** Подключить базу знаний как MCP-инструменты к Claude Desktop.

```bash
python scripts/mcp_server.py  # stdio режим
```

**7 инструментов Claude получает:**

| Инструмент | Что делает |
|-----------|-----------|
| `search_docs` | BM25-поиск по базе |
| `get_doc` | Прочитать конкретный файл |
| `get_decisions` | Архитектурные решения |
| `get_contacts` | Авторы и статус связи |
| `get_project_status` | Статус конкретного проекта |
| `run_improve` | Запустить любой скрипт |
| `update_contact_status` | Обновить статус контакта |

**Конфигурация в Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "lorenzo": {
      "command": "python",
      "args": ["/home/user/lorenzo/scripts/mcp_server.py"]
    }
  }
}
```

---

## Сводная таблица экспортных форматов

| Формат | Инструмент | Назначение |
|--------|-----------|-----------|
| Obsidian vault | `improve_obsidian.py` | Личная база знаний |
| Confluence wiki | `improve_confluence.py` | Корпоративная wiki |
| EPUB | `improve_epub.py` | Офлайн-чтение |
| RSS/Atom | `improve_rss.py` | Подписка на изменения |
| JSON | `improve_export_json.py` | API, анализ данных |
| CSV | `improve_export_csv.py` | Excel, Google Sheets |
| HTML | `improve_export_html.py` | Статический сайт |
| JSONL (чанки) | `improve_chunk_semantic.py` | RAG-пайплайн |
| XML sitemap | `improve_sitemap.py` | SEO, навигация |
| MCP-сервер | `mcp_server.py` | Claude Desktop |

---

## Следующий шаг

После экспорта → **Часть 9: Автоматизация (оркестратор, watcher, CI/CD)**

---

## Обработка больших массивов — Часть 9: Автоматизация

> Как сделать так, чтобы всё работало само: оркестратор, watcher, CI/CD, MCP.

---

## Проблема ручного запуска

125 скриптов. Запускать вручную каждый раз — не вариант. Нужна система, которая:
1. **Знает порядок** — какой скрипт от чего зависит
2. **Пропускает ненужное** — если метрика уже хорошая
3. **Реагирует на изменения** — сама запускается когда файл изменился
4. **Работает в CI/CD** — на каждый push
5. **Отдаёт инструменты Claude** — через MCP

---

## Ступень 1: Оркестратор — improve_run_all.py

**Главный скрипт** — запускает все группы в правильном порядке.

```bash
# Запустить всё
python scripts/improve_run_all.py

# Только быстрые скрипты (< 5 сек каждый)
python scripts/improve_run_all.py --fast

# Умный режим: пропустить если метрика уже хорошая
python scripts/improve_run_all.py --smart

# Только конкретная группа
python scripts/improve_run_all.py --group quality
python scripts/improve_run_all.py --group deeptext
python scripts/improve_run_all.py --group meta

# Только изменённые файлы (git diff)
python scripts/improve_run_all.py --changed

# Параллельное выполнение групп
python scripts/improve_run_all.py --parallel 4

# Конкретный скрипт
python scripts/improve_run_all.py --only improve_metrics.py

# Отчёт о выполнении
python scripts/improve_run_all.py --report
```

**15 групп в порядке зависимостей:**
```
structure → index → analysis → extract → quality → graph → generate
    → reports → export → cicd → analytics → textwork → deeptext → meta → enrich
```

**SMART_CONDITIONS** — не запускать если уже хорошо:
```python
SMART_CONDITIONS = {
    "improve_metrics.py":     ("docs/METRICS.md", "Средний балл", 80),
    "improve_health.py":      ("docs/HEALTH.md",  "общий балл",   85),
    "improve_scoring.py":     ("docs/SCORING.md", "балл:",        90),
    "improve_broken_links.py":("docs/BROKEN_LINKS.md", "Найдено", 30),
    "improve_dedup.py":       ("docs/DUPLICATES.md", "Точных дублей", 0),
    "improve_spellcheck.py":  ("docs/SPELLCHECK.md", "проблем", 5),
}
```

---

## Ступень 2: Автономный Watcher — improve_watcher.py

**Следит за файлами и автоматически запускает нужные скрипты.**

```bash
python scripts/improve_watcher.py  # запустить (polling каждые 30 сек)
```

**Правила реакции:**
```python
RULES = [
    # Изменился docs-файл → обновить метрики и индекс
    Rule(pattern="docs/**/*.md",        scripts=["improve_metrics", "improve_search_index"]),
    # Новый contacts-файл → обновить приоритеты
    Rule(pattern="docs/contacts/*.md",  scripts=["improve_contact_priority", "improve_contacts"]),
    # Изменился скрипт → обновить карту зависимостей
    Rule(pattern="scripts/improve_*.py",scripts=["improve_dependency_map"]),
]
```

**Cooldown:** Каждый скрипт не чаще 1 раза в 60 секунд — защита от петель.

---

## Ступень 3: GitHub Actions CI/CD — .github/workflows/docs.yml

**Запускается при каждом push.**

```yaml
# .github/workflows/docs.yml (сгенерирован improve_ci_config.py)

on: [push]
jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt -q
      
      # Быстрые скрипты на PR
      - name: Run fast scripts
        if: github.event_name == 'pull_request'
        run: python scripts/improve_run_all.py --fast
        continue-on-error: true
      
      # Все скрипты на push в main
      - name: Run all scripts
        if: github.event_name == 'push'
        run: python scripts/improve_run_all.py --smart
        continue-on-error: true
      
      # Закоммитить обновлённые docs/
      - name: Commit updates
        run: |
          git config user.name "docs-bot"
          git add -A docs/
          git diff --staged --quiet || git commit -m "docs: auto-update [skip ci]"
          git push origin HEAD
```

```bash
python scripts/improve_ci_config.py  # сгенерировать/обновить workflow
```

---

## Ступень 4: Pre-commit хуки — .pre-commit-config.yaml

**Проверки перед каждым коммитом:**

```bash
python scripts/improve_pre_commit.py --install
# pre-commit install
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-broken-links
        name: Check broken links
        entry: python scripts/improve_broken_links.py
        language: python
      - id: validate-docs
        name: Validate docs structure
        entry: python scripts/improve_validate.py
        language: python
```

---

## Ступень 5: Dependabot — .github/dependabot.yml

**Мониторинг версий зависимостей и OSS-проектов:**

```bash
python scripts/improve_dependabot.py --generate-config
```

Отслеживает:
- `anthropic` SDK
- `beautifulsoup4`
- `mcp`
- Версии OSS-проектов (AgentFS, Yodoca) из GitHub releases

---

## Ступень 6: MCP-сервер — mcp_server.py (Claude Desktop)

**Самый высокий уровень автоматизации:** Claude сам решает когда запустить скрипт.

```python
# Claude может вызвать:
run_improve(script="improve_metrics", args=[])
search_docs(query="AgentFS concurrent access")
update_contact_status(author="kksudo", field="studied", value=True)
```

**Это означает:** Говорите Claude «обнови метрики» — он сам вызовет нужный скрипт через MCP.

---

## Ступень 7: Claude Skills (КОГДА запускать)

Skills в `.claude/skills/` — это инструкции для Claude **когда** использовать какой инструмент:

| Skill | Триггер | Действие |
|-------|---------|---------|
| `analyze-project.md` | «Расскажи про AgentFS» | Найти файл, прочитать ENTITIES/CONTACTS, синтезировать |
| `review-docs.md` | «Проверь документацию» | Запустить quality-группу, прочитать METRICS |
| `write-contact.md` | «Напиши автору kksudo» | Прочитать contacts/kksudo.md, сгенерировать письмо |
| `improve.md` | «Улучши файл X» | Запустить нужные скрипты, предложить правки |

---

## Полная цепочка автоматизации

```
Событие (push / изменение файла / запрос Claude)
    ↓
Триггер (CI/CD workflow / watcher polling / MCP вызов / Skill)
    ↓
Оркестратор (improve_run_all.py --smart --changed)
    ↓
Группа скриптов (quality / deeptext / meta / ...)
    ↓
Обновлённые docs/ + метрики
    ↓
Коммит + push (git add -A docs/ && git commit && git push)
    ↓
Уведомление (RSS фид / GitHub Pages / Obsidian sync)
```

---

## Следующий шаг

→ **Часть 10: Инновационные и ещё не придуманные подходы**

---

## Обработка больших массивов — Часть 10: Инновационные подходы

> Что можно сделать сегодня с новыми инструментами — и что ещё не придумано.

---

## Граница между «уже есть» и «ещё нет»

| Уровень | Статус | Пример |
|---------|--------|--------|
| grep, BM25, TF-IDF | ✅ реализовано | `improve_keyword_index.py` |
| Структурирование, TOC, теги | ✅ реализовано | `improve_auto_toc.py` |
| TextRank, граф концептов | ✅ реализовано | `improve_textrank.py` |
| LLM-обогащение (API) | ✅ реализовано | `improve_llm_enrich.py` |
| Векторный поиск | 🟡 план | sentence-transformers + FAISS |
| Мультиагентная обработка | 🟡 концепт | каждый агент = специалист |
| Автономный агент-документатор | 🔴 не реализовано | watcher + LLM + PR |
| Граф знаний с LLM-NER | 🔴 план | spaCy + Claude → Neo4j/Kuzu |
| Инкрементальное обучение | 🔴 концепт | база знаний обновляет модель |

---

## Уровень A: Векторный поиск (следующий шаг)

**Почему BM25 не всегда достаточно:**
```
Запрос: "как агент запоминает контекст разговора"
BM25 найдёт: файлы со словами "агент", "запоминает", "контекст"
Векторный найдёт: файлы о memory, episodic storage, session persistence — даже без этих слов
```

**Реализация:**

```python
# Шаг 1: Индексация (один раз)
from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # 200 МБ, CPU

chunks = [json.loads(l) for l in open('docs/all_chunks.jsonl')]
texts = [c['text'] for c in chunks]
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

# Сохранить индекс
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings.astype('float32'))
faiss.write_index(index, 'docs/vector_index.faiss')

# Шаг 2: Поиск
query = "как агент запоминает контекст"
query_vec = model.encode([query]).astype('float32')
scores, ids = index.search(query_vec, k=10)

for score, idx in zip(scores[0], ids[0]):
    print(f"[{score:.3f}] {chunks[idx]['file']} — {chunks[idx]['text'][:100]}")
```

**Гибридный поиск (BM25 + вектор):**
```python
# Reciprocal Rank Fusion — объединяет оба ранжирования
def rrf(bm25_results, vector_results, k=60):
    scores = {}
    for rank, (doc, _) in enumerate(bm25_results):
        scores[doc] = scores.get(doc, 0) + 1/(k + rank + 1)
    for rank, (doc, _) in enumerate(vector_results):
        scores[doc] = scores.get(doc, 0) + 1/(k + rank + 1)
    return sorted(scores.items(), key=lambda x: -x[1])
```

**Стоимость:**
- Модель: `paraphrase-multilingual-MiniLM-L12-v2` — бесплатно, CPU, ~200 МБ
- Индексация 1000 чанков: ~30 сек на CPU
- Поиск: < 10 мс

---

## Уровень B: Граф знаний с LLM-NER

**Концепция:** Не просто «кто упоминается», а «кто с кем связан и как».

```python
# Сейчас (regex NER):
entities = extract_by_regex(text)  # ["AgentFS", "kksudo", "SQLite"]

# Будущее (LLM NER):
response = claude.complete(f"""
Извлеки из текста:
1. Сущности: [тип: проект|человек|технология|концепт]
2. Отношения: (субъект) → [тип: использует|создан_автором|конкурент|зависит_от] → (объект)

Текст: {chunk}

Формат: JSON
""")
# → {"entities": [...], "relations": [{"from": "Yodoca", "type": "использует", "to": "SQLite"}]}
```

**Граф-база (без внешних сервисов):**
```python
# Kuzu — встраиваемая граф-БД (как SQLite, но для графов)
import kuzu

db = kuzu.Database('docs/knowledge_graph.kuzu')
conn = kuzu.Connection(db)

conn.execute("CREATE NODE TABLE Project(name STRING, PRIMARY KEY(name))")
conn.execute("CREATE REL TABLE USES(FROM Project TO Project)")

conn.execute("MERGE (p:Project {name: $name})", {"name": "Yodoca"})
conn.execute("MERGE (t:Project {name: $name})", {"name": "SQLite"})
conn.execute("MATCH (a:Project {name:'Yodoca'}),(b:Project {name:'SQLite'}) CREATE (a)-[:USES]->(b)")

# Запрос: что использует AgentFS?
result = conn.execute("MATCH (a:Project {name:'AgentFS'})-[:USES]->(b) RETURN b.name")
```

**Применение:**
- «Покажи все проекты, которые используют SQLite» — за 1 запрос
- «Найди путь между AgentFS и NGT Memory через общие зависимости»
- Визуализация в D3.js / Obsidian Graph

---

## Уровень C: Мультиагентная обработка

**Проблема:** Один LLM-агент обрабатывает документ последовательно. При 1000 файлах — это медленно и дорого.

**Решение:** Специализированные агенты работают параллельно.

```python
# Концепция pipeline с агентами
agents = {
    "extractor":    Agent(role="Извлекай факты и даты"),
    "summarizer":   Agent(role="Создавай краткие резюме"),
    "tagger":       Agent(role="Назначай теги и категории"),
    "linker":       Agent(role="Находи связи с другими документами"),
    "qa_generator": Agent(role="Генерируй вопросы-ответы"),
}

# Параллельная обработка батча файлов
async def process_batch(files: list[Path]):
    tasks = []
    for f in files:
        text = f.read_text()
        for agent in agents.values():
            tasks.append(agent.process(text))
    results = await asyncio.gather(*tasks)
    return merge_results(results)
```

**Claude Agent SDK:**
```python
# С Anthropic SDK — нативная поддержка агентных паттернов
import anthropic

client = anthropic.Anthropic()

def extract_facts(text):
    return client.messages.create(
        model="claude-haiku-4-5",
        system="Ты специалист по извлечению фактов. Только факты, без мнений.",
        messages=[{"role": "user", "content": text}]
    )

def find_contradictions(fact_a, fact_b):
    return client.messages.create(
        model="claude-haiku-4-5",
        system="Ты детектор противоречий. Отвечай YES/NO + объяснение.",
        messages=[{"role": "user", "content": f"Факт 1: {fact_a}\nФакт 2: {fact_b}"}]
    )
```

---

## Уровень D: Автономный агент-документатор

**Идея:** Агент постоянно следит за кодовой базой и сам поддерживает документацию актуальной.

```
git push → webhook → агент читает diff →
    анализирует изменения →
    обновляет docs/ →
    создаёт PR →
    ожидает апрув →
    мержит
```

**Пайплайн:**
```python
# 1. Триггер: изменился файл скрипта
changed_scripts = get_git_diff_files("scripts/")

# 2. Агент читает скрипт + текущую документацию
for script in changed_scripts:
    code = read_file(script)
    current_doc = read_file(f"docs/{script.stem}.md")
    
    # 3. LLM определяет что изменилось по смыслу
    delta = claude.complete(f"""
    Старая документация: {current_doc}
    Новый код: {code}
    
    Что изменилось в поведении? Обнови только изменившиеся секции.
    """)
    
    # 4. Обновляет документ
    write_file(f"docs/{script.stem}.md", apply_delta(current_doc, delta))

# 5. Создаёт PR
create_pr(title="docs: auto-update from code changes [bot]")
```

**Существующая инфраструктура в этом проекте:**
- `improve_watcher.py` — уже следит за файлами
- `mcp_server.py` → `run_improve()` — уже умеет запускать скрипты
- `.github/workflows/docs.yml` — уже запускает на push
- **Недостаёт:** LLM-агент, который читает diff и пишет документацию

---

## Уровень E: Инкрементальное обучение базы знаний

**Концепция:** База знаний не просто хранится — она «учится» при добавлении новых документов.

```python
# Проблема: добавили 100 новых файлов → весь индекс устарел
# Решение: инкрементальное обновление

class IncrementalKnowledgeBase:
    def __init__(self, index_path):
        self.index = load_faiss(index_path)
        self.metadata = load_json("docs/vector_metadata.json")
    
    def add_document(self, file_path):
        text = file_path.read_text()
        new_chunks = semantic_chunk(text)
        new_embeddings = encode(new_chunks)
        
        # Добавить новые чанки в индекс
        self.index.add(new_embeddings)
        self.metadata.extend([{"file": str(file_path), "chunk_id": i} 
                               for i in range(len(new_chunks))])
        
        # Пересчитать BM25 только для изменившихся файлов
        self.bm25.update(file_path, new_chunks)
        
        # Обновить граф концептов
        self.concept_graph.merge(extract_concepts(new_chunks))
    
    def remove_document(self, file_path):
        # Удалить из всех индексов по метаданным
        chunk_ids = [m['id'] for m in self.metadata if m['file'] == str(file_path)]
        self.index.remove_ids(chunk_ids)
```

---

## Уровень F: Темпоральное рассуждение

**Задача:** Не просто «что написано», а «что изменилось, когда и почему».

```python
# improve_temporal_reasoning.py (концепт)

def analyze_evolution(file_path: Path, commits: int = 20):
    """Анализирует эволюцию документа во времени."""
    history = git_log(file_path, n=commits)
    
    snapshots = []
    for commit in history:
        text = git_show(commit.hash, file_path)
        facts = extract_facts_llm(text)
        snapshots.append({"date": commit.date, "facts": facts, "hash": commit.hash})
    
    # Найти: какие факты появились, какие исчезли, какие противоречат
    timeline = diff_facts(snapshots)
    
    return {
        "appeared": timeline["new"],      # факты добавленные после X
        "disappeared": timeline["removed"], # факты убранные после Y
        "changed": timeline["modified"],   # факты изменившиеся
        "stable": timeline["unchanged"],   # факты не менявшиеся
    }
```

**Применение:**
- «Когда AgentFS перестал поддерживать concurrent доступ?»
- «Покажи как изменилась архитектура Svyazi за 6 месяцев»
- Автоматический changelog на основе семантики, а не кода

---

## Уровень G: Голосовой пайплайн (Speech-to-Knowledge)

```
Голосовое сообщение / подкаст
    ↓ Whisper (транскрипция, бесплатно локально)
    ↓ improve_segment_transcript.py (разбивка по темам)
    ↓ improve_llm_enrich.py (структурирование)
    ↓ docs/voice-notes/YYYY-MM-DD-{title}.md
    ↓ improve_search_index.py (добавить в индекс)
```

```python
# whisper_to_knowledge.py (концепт)
import whisper

model = whisper.load_model("base")  # 74 МБ, CPU
result = model.transcribe("meeting-2026-04-29.mp3", language="ru")

# Разбить по временным меткам на темы
segments = segment_by_topic(result['segments'])

for i, seg in enumerate(segments):
    write_doc(f"docs/voice-notes/{date}-topic-{i}.md", seg['text'])
```

---

## Уровень H: Синтез из нескольких репозиториев

**Задача:** Объединить знания из нескольких отдельных репозиториев в единую базу.

```python
# cross_repo_synthesizer.py (концепт)

REPOS = [
    "~/projects/agentfs-research",
    "~/projects/yodoca-notes", 
    "~/projects/lorenzo",
    "~/projects/sentinel-analysis",
]

def synthesize():
    all_chunks = []
    for repo in REPOS:
        chunks = load_chunks(repo + "/docs/all_chunks.jsonl")
        for c in chunks:
            c['source_repo'] = repo
        all_chunks.extend(chunks)
    
    # Единый индекс поверх всех репозиториев
    unified_index = build_bm25(all_chunks)
    unified_vectors = build_faiss(all_chunks)
    
    # Найти связи между репозиториями
    cross_refs = find_cross_repo_concepts(all_chunks)
    
    write_json("~/knowledge-os/unified_index.json", unified_index)
    write_json("~/knowledge-os/cross_refs.json", cross_refs)
```

---

## Уровень I: Не придуманные подходы

### Живой документ (Living Document)

Документ, который сам обновляется при появлении новых данных:

```markdown
<!-- @auto-update: query="AgentFS concurrent access", source="docs/", interval=daily -->
## Статус AgentFS

*Последнее обновление: 2026-04-29 (автоматически)*

AgentFS поддерживает concurrent read, но не concurrent write...
```

Скрипт находит все `<!-- @auto-update -->` директивы, выполняет запрос BM25/LLM и заменяет содержимое секции.

---

### Граф аргументов (Argument Graph)

Не просто «что сказано», а «почему так решили»:

```
Утверждение: "AgentFS не поддерживает concurrent write"
    ↑ Основание: "В коде найден GIL в _write_lock"
    ↑ Контр-аргумент: "В v0.3 добавили MVCC" (источник: commit abc123)
    ↑ Статус: ОТКРЫТЫЙ ВОПРОС (спросить kksudo)
```

Такой граф позволяет отследить «где мы приняли неверное решение на основе устаревших данных».

---

### Нейросеть на собственной базе (Domain-Specific Fine-tuning)

```python
# Использовать базу знаний как датасет для fine-tuning
# Тип: instruction-tuning

training_data = []
for qa in load_json("docs/qa_cache.json"):
    training_data.append({
        "instruction": qa['question'],
        "output": qa['answer'],
        "context": qa['sources'],
    })

# Fine-tune claude-haiku на этих данных →
# модель, которая знает проект лучше базовой
```

---

### Рефлексивный агент (Self-Improving Documentation)

```
Агент читает документ →
    Находит неясность →
    Формулирует вопрос →
    Ищет ответ в других документах →
    Если нашёл → дополняет документ →
    Если не нашёл → добавляет в docs/OPEN_QUESTIONS.md →
    Пересматривает логику своего поиска → улучшает алгоритм
```

Этот паттерн называется **ReAct** (Reasoning + Acting) — агент итеративно уточняет понимание.

---

## Дорожная карта реализации

| Фаза | Что делаем | Инструменты | Стоимость |
|------|-----------|-------------|---------|
| Сейчас | BM25 + TextRank + LLM API | всё в `scripts/` | ~$0.10 |
| Следующий шаг | Векторный поиск | sentence-transformers + FAISS | 0 |
| Через месяц | Граф знаний | Kuzu + claude-haiku | ~$1 |
| Через квартал | Мультиагентный пайплайн | Claude Agent SDK | ~$5/запуск |
| Через год | Автономный агент | MCP + GitHub API + LLM | ~$20/мес |

---

## Вывод

Текущая система (`scripts/improve_*.py`) реализует уровни 1–4 полностью и бесплатно.

Уровни 5–8 (векторный поиск, граф знаний, мультиагент, автономный агент) технически готовы к реализации — инфраструктура (`mcp_server.py`, `improve_watcher.py`, `all_chunks.jsonl`) уже есть. Нужно только:
1. Добавить `sentence-transformers` + FAISS (уровень A)
2. Добавить Kuzu + LLM-NER (уровень B-C)
3. Подключить к существующему `improve_watcher.py` (уровень D)

Остальные уровни (E-I) — это направления исследований, которые можно реализовать поверх существующей базы.

---

← **Часть 9: Автоматизация** | [Содержание](README.md)
