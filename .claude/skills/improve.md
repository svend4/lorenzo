# improve

Универсальный навык улучшения любого элемента Lorenzo: документа, контакта,
скрипта, раздела, или всей базы знаний целиком.

Когда использовать:
- «улучши файл X»
- «что не так с этим документом?»
- «как поднять метрику?»
- «база знаний устарела, обнови»
- «подготовь документ к отправке»
- «почему score 55, что делать?»
- любой запрос об улучшении чего-либо в проекте

---

## Auto-discovery скриптов

**Перед тем, как выбирать скрипт, прочитайте актуальный каталог:**

```
Read: docs/SCRIPTS_CATALOG.md
```

Или для машинного чтения:
```bash
cat docs/scripts_catalog.json | python -m json.tool | head -100
```

Каталог автогенерируется через `python scripts/improve_scripts_catalog.py`
из docstring каждого `improve_*.py`. Список скриптов в этом скилле ниже —
**может быть устаревшим**: каталог всегда актуальнее.

**Алгоритм выбора скрипта:**
1. Прочесть `docs/SCRIPTS_CATALOG.md`
2. Найти подходящие скрипты по группе и описанию
3. Если ничего не подошло — `grep -i "ключевое-слово" docs/SCRIPTS_CATALOG.md`
4. Если совсем ничего — задача за пределами текущего инструментария, нужен новый скрипт

**Группы скриптов:**
- `structure` — базовая структура (TOC, README, summaries, tags)
- `index` — индексы, поиск, бэклинки
- `analysis` — кластеры, дубли, частоты, приоритеты
- `extract` — action items, decisions, KPI, entities
- `quality` — валидация, broken links, орфография, читаемость
- `graph` — graph, mindmap, network, narrative
- `generate` — templates, autofill, footnotes, see-also
- `reports` — QA, contacts, changelog, health, report
- `export` — CSV, JSON, HTML, Obsidian, RSS, Confluence
- `cicd` — github issues, CI, pre-commit, dependabot
- `analytics` — citation index, reading time, version diff, topic model
- `textwork` — outline, reclassify, merge, compare, source map
- `deeptext` — TOC, abstract, paragraph quality, NER, BM25
- `nlpplus` — TextRank, headings, language split, passive, faceted search
- `content` — auto-linker, gap-filler (меняют файлы)

---

## Шаг 0 — Определить тип улучшения

Прочитать запрос и выбрать одну из веток:

| Что улучшать | Ветка |
|---|---|
| Конкретный `.md` файл | → **A: Один файл** |
| Раздел `docs/0X-*/` | → **B: Раздел** |
| Контактный файл `docs/contacts/*.md` | → **C: Контакт** |
| Все документы / «база знаний» | → **D: Полный прогон** |
| Скрипт `scripts/*.py` | → **E: Скрипт** |
| Метрика / балл качества | → **F: Метрика** |

---

## Ветка A — Один файл

### A1. Прочитать файл и диагностировать

```bash
# Читаем файл
Read: <path>

# Проверяем метрику этого файла
grep "<filename>" docs/METRICS.md
grep "<filename>" docs/HEALTH.md
grep "<filename>" docs/BROKEN_LINKS.md
grep "<filename>" docs/COMPLEXITY.md
```

### A2. Чеклист качества файла

Проверить вручную по прочитанному тексту:

- [ ] Есть `<!-- summary: ... -->` в первых 5 строках?
- [ ] Есть `<!-- tags: ... -->` ?
- [ ] Есть заголовок `#` первого уровня?
- [ ] Файл длиннее 100 слов?
- [ ] Есть конкретные факты или только абстрактные суждения?
- [ ] Есть ссылки на связанные документы (`<!-- see-also -->`)?
- [ ] Нет битых ссылок `[текст](путь)` ведущих в никуда?
- [ ] Есть `## Статус` блок (от improve_autofill)?

### A3. Алгоритмические улучшения (бесплатно, $0)

Запустить только нужные скрипты — не все подряд:

```bash
# Нет summary/тегов → запустить summaries
python scripts/improve_summaries.py

# Нет TOC (для файлов >500 слов)
python scripts/improve_toc.py

# Битые ссылки
python scripts/improve_broken_links.py

# Нет перекрёстных ссылок
python scripts/improve_crossrefs.py

# Орфография / согласованность терминов
python scripts/improve_autocorrect.py

# Нет блока Статус (контакт/проект)
python scripts/improve_autofill.py

# Низкая плотность ссылок
python scripts/improve_backlinks.py
```

После каждого скрипта — перечитать файл (`Read: <path>`) и проверить что изменилось.

### A4. Семантические улучшения (LLM, если алгоритм не помог)

Использовать когда файл технически корректен, но содержательно слабый:
— короткий (< 150 слов)
— нет конкретных фактов
— описание расплывчатое

```bash
# Dry-run: узнать стоимость
python scripts/improve_llm_enrich.py --dry-run --file <path>

# Реальный запуск (~$0.0001-0.001)
python scripts/improve_llm_enrich.py --file <path>

# Для длинных файлов (>3000 слов) — суммаризация
python scripts/improve_llm_summary.py --file <path>
```

Прочитать результат в `docs/enriched/<section>/<name>-enriched.md`.
Решить: использовать как есть или смёржить с исходником вручную.

### A5. Финальная проверка

```bash
python scripts/improve_metrics.py
grep "<filename>" docs/METRICS.md   # балл должен вырасти
```

Сравнить балл до и после. Сообщить пользователю что изменилось.

---

## Ветка B — Раздел (например, 05-habr-projects)

### B1. Диагностика раздела

```bash
grep "<section>" docs/METRICS.md       # балл раздела
grep "<section>" docs/CLUSTERS.md      # тематические кластеры
grep "<section>" docs/ORPHANS.md       # изолированные файлы
```

Прочитать результаты и найти слабые места.

### B2. Массовое улучшение по приоритету

```bash
# Приоритет 1: структура (быстро, бесплатно)
python scripts/improve_run_all.py --group structure --smart

# Приоритет 2: индексы
python scripts/improve_run_all.py --group index --smart

# Приоритет 3: качество
python scripts/improve_run_all.py --group quality --smart
```

`--smart` пропускает скрипты где балл уже выше порога.

### B3. LLM-обогащение раздела

Только если алгоритмических улучшений недостаточно:

```bash
python scripts/improve_llm_enrich.py --dry-run --section <section>
# Посмотреть стоимость → если приемлема:
python scripts/improve_llm_enrich.py --section <section>
```

### B4. Пересчитать метрики

```bash
python scripts/improve_metrics.py
python scripts/improve_health.py
python scripts/improve_progress_sync.py
```

Сообщить: балл до → балл после, что конкретно улучшилось.

---

## Ветка C — Контактный файл

### C1. Прочитать файл

```bash
Read: docs/contacts/<slug>.md
```

Проверить:
- Полный ли вопрос в `## Открытые вопросы`? (не обрезан ли)
- Правильно ли заполнен профиль?
- Какой текущий статус чеклиста?

### C2. Использовать навык write-contact

Если нужно улучшить черновик сообщения — вызвать навык:
```
→ Смотри .claude/skills/write-contact.md
```

### C3. Обновить статус после отправки

Если пользователь говорит «написал» / «ответили» — обновить `[x]` в файле:

```
Edit: docs/contacts/<slug>.md
Изменить:  - [ ] Написали первое сообщение
На:        - [x] Написали первое сообщение
```

Затем синхронизировать прогресс:
```bash
python scripts/improve_progress_sync.py
```

### C4. Обновить CONTACTS.md

Если изменились данные о проекте или авторе:
```bash
python scripts/improve_contacts.py
python scripts/improve_autofill.py
```

---

## Ветка D — Полный прогон базы знаний

Использовать когда много файлов изменилось или давно не запускались скрипты.

### D1. Быстрый прогон (5-10 минут, $0)

```bash
python scripts/improve_run_all.py --fast --smart
```

`--fast` пропускает медленные скрипты (clusters, similar, html-export).
`--smart` пропускает скрипты где метрика уже выше порога.

### D2. Полный прогон (20-40 минут, $0)

```bash
python scripts/improve_run_all.py --smart
```

### D3. Обновить прогресс после прогона

```bash
python scripts/improve_progress_sync.py
```

### D4. LLM-обогащение (нужен ANTHROPIC_API_KEY)

```bash
# Оценить стоимость
python scripts/improve_llm_enrich.py --dry-run

# Если стоимость приемлема:
python scripts/improve_llm_enrich.py --section 05-habr-projects

# Суммаризация для DIGEST.md
python scripts/improve_llm_summary.py --section 05-habr-projects
```

---

## Ветка E — Скрипт

### E1. Прочитать скрипт

```bash
Read: scripts/<script_name>.py
```

### E2. Запустить тест

```bash
python -m py_compile scripts/<script>.py  # синтаксис
python scripts/<script>.py --dry-run       # логика без изменений
```

### E3. Типичные улучшения скриптов Lorenzo

| Симптом | Улучшение |
|---|---|
| Падает на большом файле | Добавить `chunk_by_headers` из `utils_chunker.py` |
| Медленно на 400 файлах | Добавить в `SLOW_SCRIPTS` в `improve_run_all.py` |
| Дублирует данные из другого скрипта | Вынести в общую функцию или читать из уже готового .md |
| Нет `--dry-run` | Добавить флаг по образцу других скриптов |
| Не идемпотентен (каждый запуск добавляет дубли) | Добавить маркер-комментарий как `<!-- autofill-status -->` |
| Не учитывает `preview` поле в search_index.json | Заменить `doc.get("content","")` на `_doc_text(doc)` |

### E4. После правки — добавить в run_all

Если скрипт новый — добавить в нужную группу в `improve_run_all.py`:
```python
# scripts/improve_run_all.py, в нужный GROUPS[<group>]
"improve_<новый>.py",
```

---

## Ветка F — Метрика / балл качества

### F1. Прочитать текущие баллы

```bash
Read: docs/HEALTH.md      # 75/100 🟡
Read: docs/METRICS.md     # 65.7/100
Read: docs/SCORING.md     # 96% GO
```

### F2. Найти что именно снижает балл

Из `METRICS.md`:
- `% с summary` < 90% → запустить `improve_summaries.py`
- `% с тегами` < 80% → запустить `improve_tags.py`
- Раздел с низким баллом → → Ветка B для этого раздела

Из `HEALTH.md`:
- «Внутренние ссылки: X сломано» → запустить `improve_broken_links.py`, потом `improve_crossrefs.py`
- «Дублирование» → запустить `improve_dedup.py`

Из `SCORING.md`:
- Строки с ❌ → выяснить почему и устранить

### F3. Запустить целевые скрипты

```bash
# Только та группа что влияет на найденную метрику
python scripts/improve_run_all.py --group quality
python scripts/improve_run_all.py --group structure
```

### F4. Пересчитать и сравнить

```bash
python scripts/improve_metrics.py
python scripts/improve_health.py
python scripts/improve_scoring.py
python scripts/improve_progress_sync.py
```

Сообщить: было X → стало Y, что именно изменилось.

---

## Справка: какой скрипт что улучшает

| Скрипт | Что улучшает | Группа |
|---|---|---|
| `improve_summaries.py` | Добавляет `<!-- summary -->` | structure |
| `improve_tags.py` | Добавляет `<!-- tags -->` | structure |
| `improve_toc.py` | Оглавление для длинных файлов | structure |
| `improve_autocorrect.py` | Исправляет опечатки из CONSISTENCY.md | structure |
| `improve_autofill.py` | Заполняет шаблоны данными | — |
| `improve_crossrefs.py` | Перекрёстные ссылки между файлами | index |
| `improve_backlinks.py` | Индекс обратных ссылок | index |
| `improve_search_index.py` | Поисковый индекс | index |
| `improve_broken_links.py` | Находит и помечает битые ссылки | quality |
| `improve_metrics.py` | Пересчитывает баллы | quality |
| `improve_health.py` | Обновляет HEALTH.md | quality |
| `improve_dedup.py` | Находит дубли | analysis |
| `improve_similar.py` | Похожие документы | analysis |
| `improve_contacts.py` | Обновляет CONTACTS.md | reports |
| `improve_progress_sync.py` | Синхронизирует PROGRESS.md | — |
| `improve_llm_enrich.py` | LLM-описания проектов | llm |
| `improve_llm_summary.py` | LLM-суммаризация → DIGEST.md | llm |
| `improve_llm_qa.py` | Q&A по базе знаний | llm |

## Принцип: алгоритм раньше LLM

Сначала всегда пробовать алгоритмические скрипты ($0, мгновенно).
LLM подключать только если:
- Файл содержательно пустой (< 150 слов реального текста)
- Нужно написать новый текст, а не улучшить структуру
- Нужен смысловой вывод, а не паттерн

Стоимость LLM:
- haiku: ~$0.0001-0.001 на файл
- Весь 05-habr-projects: ~$0.003
- Все 460 документов: ~$0.30
