# Методология работы со скриптами

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Принципы: скрипты работают **по вызову**, под контролем человека или Claude.

---

<!-- toc -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Содержание

- [Основной принцип](#основной-принцип)
- [Три категории скриптов](#три-категории-скриптов)
  - [🟢 ЗЕЛЁНЫЕ — только чтение / stdout (~9 скриптов)](#зелёные-только-чтение-stdout-9-скриптов)
  - [🟡 ЖЁЛТЫЕ — пишут в выделенный файл-отчёт (~141 скрипт)](#жёлтые-пишут-в-выделенный-файл-отчёт-141-скрипт)
  - [🔴 КРАСНЫЕ — модифицируют входные файлы in-place (6 скриптов)](#красные-модифицируют-входные-файлы-in-place-6-скриптов)
- [Типичные рабочие сессии](#типичные-рабочие-сессии)
  - [Сессия: проверить состояние репо](#сессия-проверить-состояние-репо)
  - [Сессия: починить сломанные ссылки](#сессия-починить-сломанные-ссылки)
  - [Сессия: обновить поисковый индекс](#сессия-обновить-поисковый-индекс)
  - [Сессия: LLM-обогащение (нужен ANTHROPIC_API_KEY)](#сессия-llm-обогащение-нужен-anthropic_api_key)
  - [Сессия: полная переиндексация (раз в несколько недель)](#сессия-полная-переиндексация-раз-в-несколько-недель)
- [Что НЕ делать](#что-не-делать)
- Роль [GitHub Actions](#роль-github-actions)
- [Роль Claude / нейросети](#роль-claude-нейросети)

---

<!-- tags: rag, security, anthropic, self-improvement, collaboration -->




> Принципы: скрипты работают **по вызову**, под контролем человека или Claude.
> Никакой автоматики без явного решения.

---

## Основной принцип

```
Скрипт запускается только тогда, когда есть конкретная задача.
Результат проверяется до коммита.
Коммит делается вручную с осмысленным сообщением.
```

Бот (GitHub Actions) не делает автоматических коммитов.
Скрипты не запускаются по расписанию.
Watcher (`improve_watcher.py`) не активен в фоне.

---

## Три категории скриптов

Классификация определяется автоматически через `improve_self.py --audit`.
Алгоритм различает: пишет ли скрипт в те же файлы что читает (🔴),
в отдельный выходной файл (🟡), или не пишет вообще (🟢).

### 🟢 ЗЕЛЁНЫЕ — только чтение / stdout (~9 скриптов)

Не изменяют файлы совсем. Только считают и выводят в терминал.
Идемпотентны и безопасны в любой момент.

```bash
python scripts/improve_benchmark.py      # замер времени → stdout
python scripts/improve_faceted_search.py --query "..."  # поиск → stdout
python scripts/improve_reading_list.py --format text    # список → stdout
```

---

### 🟡 ЖЁЛТЫЕ — пишут в выделенный файл-отчёт (~141 скрипт)

**Это безопасные скрипты.** Каждый пишет только в ОДИН фиксированный
выходной файл (HEALTH.md, METRICS.md, search_index.json и т.д.).
Входные файлы docs/**/*.md они читают но не изменяют.
Перезапуск всегда заменяет только отчёт, не контент.

Примеры:
```bash
python scripts/improve_metrics.py        # → docs/METRICS.md
python scripts/improve_health.py         # → docs/HEALTH.md
python scripts/improve_search_index.py   # → docs/search_index.json
python scripts/improve_entities.py       # → docs/ENTITIES.md
python scripts/improve_stats.py          # → docs/STATS.md
python scripts/improve_topic_model.py    # → docs/TOPIC_MODEL.md
python scripts/improve_textrank.py       # → docs/SUMMARIES.md
python scripts/improve_citation_index.py # → docs/CITATION_INDEX.md
python scripts/improve_keyword_index.py  # → docs/keyword_index.json
```

> **Примечание об аудите:** ранняя версия алгоритма классификации ошибочно
> помечала ~130 из этих скриптов как «красные» (false positives) из-за
> слишком широкой эвристики (`write_text + rglob`). Алгоритм исправлен
> в `improve_self.py` — теперь он различает запись в loop-переменную (RED)
> vs запись в отдельный output-файл (YELLOW). Все 141 жёлтых скрипта
> проверены и подтверждены как безопасные.

Для скриптов с `--apply` (auto_toc, abstract, auto_linker и др.) —
сначала `--dry-run`:

```bash
python scripts/improve_auto_toc.py --dry-run
python scripts/improve_auto_toc.py --apply
python scripts/improve_auto_linker.py --dry-run
python scripts/improve_auto_linker.py --apply
python scripts/improve_gap_filler.py --dry-run
python scripts/improve_gap_filler.py --apply
```

**Рекомендация:** большинство жёлтых скриптов можно запускать свободно.

---

### 🔴 КРАСНЫЕ — модифицируют входные файлы in-place (6 скриптов)

Итерируют по docs/**/*.md и записывают изменения обратно в те же файлы.
Без свежих индексов могут затереть детальный контент заглушками.
Все 6 скриптов используют MARKER-паттерн для проверки «уже обработан».

```bash
python scripts/improve_alerts.py     # --dry-run добавлен ✓
python scripts/improve_footnotes.py  # --dry-run добавлен ✓
python scripts/improve_summaries.py  # ⚠ без dry-run — только при свежем индексе
python scripts/improve_backlinks.py  # ⚠ без dry-run — добавляет блоки backlinks
python scripts/improve_see_also.py   # ⚠ без dry-run — добавляет See Also секции
python scripts/improve_merge_short.py # ⚠ без dry-run — необратимо сливает файлы
```

**Правило:** запускать только если:
1. `docs/search_index.json` свежий (собран в этой сессии)
2. Есть конкретная причина (не «на всякий случай»)
3. Результат будет проверен через `git diff` до коммита

---

## Типичные рабочие сессии

### Сессия: проверить состояние репо

```bash
python scripts/improve_health.py
python scripts/improve_metrics.py
python scripts/improve_broken_links.py
# Прочитать docs/HEALTH.md и docs/BROKEN_LINKS.md
# Коммитить не обязательно
```

### Сессия: починить сломанные ссылки

```bash
python scripts/improve_broken_links.py          # посмотреть масштаб
python scripts/improve_broken_links.py --dry-run # предпросмотр исправлений
python scripts/improve_broken_links.py --fix     # применить
git diff docs/ | head -50                        # проверить результат
git add docs/ && git commit -m "fix: починить сломанные внутренние ссылки"
```

### Сессия: обновить поисковый индекс

```bash
python scripts/improve_search_index.py
python scripts/improve_passage_retrieval.py --index
python scripts/improve_keyword_index.py
git add docs/search_index.json docs/passages.json docs/keyword_index.json
git commit -m "chore: обновить поисковые индексы"
```

### Сессия: LLM-обогащение (нужен ANTHROPIC_API_KEY)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/improve_llm_enrich.py --dry-run    # план + стоимость
python scripts/improve_llm_enrich.py --section 05-habr-projects
# Проверить результат в docs/05-habr-projects/
git add docs/05-habr-projects/
git commit -m "feat: LLM-обогащение проектных файлов habr-projects"
```

### Сессия: полная переиндексация (раз в несколько недель)

```bash
# Порядок важен: индексы должны быть готовы до контентных скриптов
python scripts/improve_search_index.py       # 1. основной индекс
python scripts/improve_keyword_index.py      # 2. BM25 индекс
python scripts/improve_passage_retrieval.py --index  # 3. индекс абзацев
python scripts/improve_entities.py           # 4. сущности
python scripts/improve_textrank.py           # 5. резюме (зависит от индекса)
python scripts/improve_health.py             # 6. метрики
git add docs/search_index.json docs/passages.json docs/keyword_index.json \
        docs/ENTITIES.md docs/SUMMARIES.md docs/HEALTH.md
git commit -m "chore: полная переиндексация базы знаний"
```

---

## Что НЕ делать

```
❌ python scripts/improve_run_all.py              # запускает всё подряд без контроля
❌ python scripts/improve_run_all.py --group reports  # на CI-сервере без индексов
❌ git add -A && git commit                       # коммит без проверки что изменилось
❌ Запускать 🔴 скрипты без свежих индексов
❌ Запускать 🟡 скрипты без --dry-run сначала
```

---

## Роль GitHub Actions

| Workflow | Триггер | Что делает | Коммитит? |
|----------|---------|-----------|-----------|
| `docs.yml` | только вручную | запускает 4 скрипта, показывает результат | ❌ нет |
| `docs_check.yml` | при PR | проверяет качество, broken-links | ❌ нет |
| `docs-portal.yml` | push в main (только docs-toolkit/) | собирает статический сайт | ❌ нет |
| `benchmark.yml` | при изменении docs-toolkit | бенчмарки | ❌ нет |

**Итог: GitHub Actions больше ничего не коммитит в репозиторий автоматически.**

---

## Роль Claude / нейросети

Claude может:
- Запустить конкретный скрипт и объяснить результат
- Показать `--dry-run` и спросить подтверждение перед `--apply`
- Выбрать правильный порядок скриптов для задачи
- Объяснить почему что-то сломалось
- Предложить что запустить, но не делать это без согласования

Claude не должен:
- Запускать `improve_run_all.py` без явного запроса
- Делать коммиты без проверки результата
- Запускать 🔴 скрипты без предупреждения

---

_Документ обновляется вручную при изменении методологии._

<!-- see-also -->

---

**Смотрите также:**
- [05-synthesis](meta-scripting/05-synthesis.md)
- [02-architecture](meta-scripting/02-architecture.md)
- [03-catalog](meta-scripting/03-catalog.md)
- [09-automation](processing-guide/09-automation.md)

