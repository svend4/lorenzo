# Методология работы со скриптами

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

### 🟢 ЗЕЛЁНЫЕ — только читают и считают (безопасно запускать в любое время)

Не изменяют файлы в `docs/`. Генерируют отчёты в stdout или перезаписывают
только свой выходной файл. Идемпотентны — повторный запуск даёт тот же результат.

```bash
python scripts/improve_metrics.py        # → docs/METRICS.md
python scripts/improve_health.py         # → docs/HEALTH.md
python scripts/improve_search_index.py   # → docs/search_index.json
python scripts/improve_entities.py       # → docs/ENTITIES.md
python scripts/improve_broken_links.py   # → docs/BROKEN_LINKS.md (без --fix)
python scripts/improve_stats.py          # → docs/STATS.md
python scripts/improve_topic_model.py    # → docs/TOPIC_MODEL.md
python scripts/improve_textrank.py       # → docs/SUMMARIES.md
python scripts/improve_citation_index.py # → docs/CITATION_INDEX.md
python scripts/improve_reading_time.py   # → docs/READING_TIME.md
python scripts/improve_keyword_index.py  # → docs/keyword_index.json
python scripts/improve_passage_retrieval.py --index  # → docs/passages.json
```

**Рекомендация:** запускать после каждой рабочей сессии для актуализации метрик.

---

### 🟡 ЖЁЛТЫЕ — изменяют файлы в docs/ (сначала --dry-run)

Добавляют или изменяют контент в документах. Перед запуском обязательно
посмотреть что изменится через `--dry-run`. Коммитить результат только после
визуальной проверки.

```bash
# Правило: сначала dry-run, потом apply
python scripts/improve_auto_toc.py --dry-run
python scripts/improve_auto_toc.py --apply          # только после проверки

python scripts/improve_abstract.py --dry-run
python scripts/improve_abstract.py --apply

python scripts/improve_broken_links.py --dry-run
python scripts/improve_broken_links.py --fix

python scripts/improve_auto_linker.py --dry-run
python scripts/improve_auto_linker.py --apply

python scripts/improve_gap_filler.py --dry-run
python scripts/improve_gap_filler.py --apply

python scripts/improve_crosslink_all.py --dry-run
python scripts/improve_crosslink_all.py --apply
```

**Рекомендация:** запускать точечно по необходимости, не группами.

---

### 🔴 КРАСНЫЕ — перезаписывают секции целиком (только по явной задаче)

Заменяют существующий контент. Требуют наличия предварительно собранных
индексов (`search_index.json`, `passages.json`). На чистом окружении без
индексов могут затереть детальный контент пустыми заглушками.

```bash
python scripts/improve_summaries.py      # перезаписывает ## Summary секции
python scripts/improve_readmes.py        # перезаписывает README файлы разделов
python scripts/improve_qa.py             # перезаписывает QA секции
python scripts/improve_crosslink_all.py  # перезаписывает backlinks во всех файлах
```

**Правило:** запускать только если:
1. `docs/search_index.json` свежий (собран в этой сессии)
2. Есть конкретная причина (не «на всякий случай»)
3. Результат будет проверен до коммита

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
