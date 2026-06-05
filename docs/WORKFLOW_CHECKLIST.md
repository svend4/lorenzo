# Workflow Checklist — пошаговая проверка CI

<!-- toc-auto -->

> [!NOTE]
> Раздел `WORKFLOW_CHECKLIST` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: workflow-checklist, docs -->


<!-- summary -->
> `WORKFLOW_CHECKLIST` — раздел документации проекта Lorenzo.


Чек-лист для ручной верификации всех 7 GitHub Actions workflow-файлов lorenzo
после инцидента 2026-05-14. Каждый workflow запускается отдельно, под контролем
оператора, без массового параллелизма.

> **Принцип:** workflows — это рецепты, тесты — работники. Этот гайд позволяет
> проверить, что каждый рецепт правильно командует своими работниками, не
> сжигая параллельные слоты впустую.

## Быстрая проверка локально (без CI)

```bash
# Симуляция всех workflows локально, без GitHub Actions:
python scripts/verify_all_workflows.py            # full
python scripts/verify_all_workflows.py --quick    # без pytest (быстро)
python scripts/verify_all_workflows.py --only test --json
```

## Автоматическое управление историей CI (без UI)

```bash
# 1. Получить токен (Personal Access Token, permission Actions: Read+Write):
#    https://github.com/settings/tokens?type=beta
export GITHUB_TOKEN=ghp_xxx

# 2. Посмотреть что бы удалилось (dry-run):
python scripts/cleanup_workflow_history.py

# 3. Удалить дубликаты + cancelled старше 7 дней:
python scripts/cleanup_workflow_history.py --apply

# 4. Запустить test.yml 3 раза подряд на main и замерить стабильность:
python scripts/rerun_workflows.py test.yml --count 3

# 5. Тестовый прогон enrich-docs в dry-mode:
python scripts/rerun_workflows.py enrich-docs.yml --count 1 --input dry_run=true
```

**Workflow для типичной очистки:**
1. `cleanup_workflow_history.py` (dry-run) → посмотреть план
2. `cleanup_workflow_history.py --apply` → удалить дубликаты
3. `rerun_workflows.py test.yml --count 3` → проверить стабильность
4. Если все 3 прогона ✅ → CI здоров, flake rate 0%

---

## Карта workflow'ов

| # | Файл | Триггер | Когда нужен | Время | Критичность |
|---|------|---------|-------------|-------|-------------|
| 1 | `test.yml` | push main, PR, manual | Каждый PR в main | ~10-15 мин | 🔴 высокая |
| 2 | `benchmark.yml` | push main, PR, manual | После изменений docs-toolkit | ~3-5 мин | 🟡 средняя |
| 3 | `docs.yml` | push main, manual | Регенерация docs/ | ~5 мин | 🟢 фоновая |
| 4 | `docs_check.yml` | PR | Валидация docs/ при PR | ~2 мин | 🟡 средняя |
| 5 | `docs-portal.yml` | push main, manual | Сборка HTML портала | ~3 мин | 🟢 фоновая |
| 6 | `publish-toolkit.yml` | tag, manual | Релиз в PyPI | ~5 мин | 🟢 редко |
| 7 | `enrich-docs.yml` | manual only | Обогащение docs/ ссылками | ~5 мин | 🟢 редко |

---

## Workflow #1 — test.yml (Test & Validate)

**Зачем:** прогон 4855 unit-тестов + проверка синтаксиса Python + smoke-тесты MCP.

### Ручной запуск

1. https://github.com/svend4/lorenzo/actions/workflows/test.yml
2. Кнопка **Run workflow** (справа сверху)
3. Branch: `main` → **Run workflow**

### Что должно произойти

6 jobs параллельно, каждый ≤ 20 мин:

| Job | Что делает | Ожидаемое время |
|-----|------------|----------------|
| `python-syntax` | `py_compile` 217 скриптов | ~30 сек |
| `unit-tests` | pytest tests/ (4855 тестов) | ~10 мин |
| `mcp-smoke` | smoke-тест MCP-сервера | ~1 мин |
| `validate-templates` | проверка docs/templates/ | ~1 мин |
| `validate-tasks` | проверка tasks/*.task.yaml | ~30 сек |
| `catalog-fresh` | регенерация catalogs, diff | ~2 мин |

### Что искать в логах

✅ **PASS** — каждый job отдельно зелёный:
```
=== 4855 passed in 400.15s (0:06:40) ===
```

❌ **FAIL варианты:**

| Сообщение | Что значит | Что делать |
|---|---|---|
| `FAILED tests/test_X.py::test_Y - AssertionError` | Тест сломался | Открыть тест, посмотреть assertion |
| `ImportError: cannot import name` | API изменился | Обновить тест или скрипт |
| `timeout` | Тест > 60 сек | Найти медленный тест, оптимизировать |
| `MCP smoke: connection refused` | MCP-сервер не стартовал | Проверить `scripts/mcp_server.py` |
| `Catalog out of date` | catalogs устарели | Локально `python scripts/improve_scripts_catalog.py`, закоммитить |

### Известные skip'ы

- `tests/test_ann_index.py::test_*_vocab_*` — Legacy HNSW API (skipped после PR этого исправления)
- `tests/test_ann_index.py::test_index_files_*` — требуют HNSW backend (skipped если hnswlib не установлен)

---

## Workflow #2 — benchmark.yml (Benchmarks)

**Зачем:** замер производительности docs-toolkit.

### Ручной запуск

1. https://github.com/svend4/lorenzo/actions/workflows/benchmark.yml
2. **Run workflow** → `main`

### Что должно произойти

Один job: запуск `docs-toolkit/bench/*.py` бенчмарков, сравнение с baseline.

### Что искать в логах

✅ **PASS** — все бенчмарки в пределах разумного:
```
benchmark_search:    47 ms (baseline 50 ms, -6%)
benchmark_index:    312 ms (baseline 300 ms, +4%)
```

❌ **FAIL варианты:**

| Сообщение | Что делать |
|---|---|
| `Regression: 50% slower` | Найти PR который замедлил, разобрать |
| `benchmark crashed` | Запустить локально: `python docs-toolkit/bench/*.py` |
| `out of memory` | На runner мало RAM (7GB) — оптимизировать алгоритм |

---

## Workflow #3 — docs.yml (docs-update)

**Зачем:** регенерация metrics, indexes, reports после push в main.

### Ручной запуск

1. https://github.com/svend4/lorenzo/actions/workflows/docs.yml
2. **Run workflow** → `main`

### Что должно произойти

Запускает 16 шагов:
- `improve_run_all.py --fast --group reports`
- `improve_auto_summarize.py --apply` (pass 1)
- `improve_progressive_summarize.py --apply --no-promote` (pass 2)
- `improve_summary_extender.py --apply --no-promote` (pass 3)
- `improve_card_promote.py --apply`
- `improve_proposal_gen.py --apply`
- `improve_rfc_tracker.py --update`
- `improve_knowledge_evolution.py`
- `improve_search_index.py`
- `improve_ann_index.py --build`
- `improve_card_graph.py`
- `improve_hot_cards.py`
- `improve_precision_eval.py --k 10` (quality gate)
- `improve_knowledge_snapshot.py`
- `improve_digest_weekly.py`
- `improve_rss.py`
- `git commit "docs: auto-update metrics [skip ci]" + push`

### Что искать в логах

✅ **PASS** — все шаги отрабатывают, в конце:
```
Retrieval quality gate: Hit Rate@10 = 0.85 (≥ 0.70 ✓)
[main XXXXXXX] docs: auto-update metrics [skip ci]
```

❌ **FAIL варианты:**

| Сообщение | Что делать |
|---|---|
| `Hit Rate@10 = 0.65 (< 0.70)` | Quality gate упал — проверить новые карточки в `docs/cards/raw/` |
| `Promote: 0 cards moved` | Lifecycle stuck — проверить `improve_card_promote.py --stats` |
| `git push: 403` | Нет write-permission — проверить `permissions: contents: write` |

---

## Workflow #4 — docs_check.yml (docs-check)

**Зачем:** валидация структуры docs/ при PR (markdown, links, frontmatter).

### Ручной запуск

Это PR-only workflow. Ручной запуск:
1. Открыть какой-то PR в main
2. https://github.com/svend4/lorenzo/actions/workflows/docs_check.yml
3. Если есть Run workflow — выбрать PR-branch

Или эквивалент локально:
```bash
python scripts/improve_validate.py
python scripts/improve_broken_links.py
```

### Что искать в логах

✅ **PASS** — структура валидна, ссылки рабочие.

❌ **Известная проблема (нужен фикс):**
```
OSError: [Errno 36] File name too long: '/path/...'
```
Это баг `improve_validate.py` — пытается создать файл с очень длинным именем
из текста markdown. См. `verify_all_workflows.py` отчёт.

---

## Workflow #5 — docs-portal.yml (Build docs portal)

**Зачем:** сборка `docs-toolkit/docs/` в статический HTML портал.

### Ручной запуск

1. https://github.com/svend4/lorenzo/actions/workflows/docs-portal.yml
2. **Run workflow** → `main`

### Что должно произойти

mkdocs или sphinx build → деплой на GitHub Pages (если настроено).

### Что искать

✅ Сборка успешна, артефакт загружен.

❌ Чаще всего падает на:
- Сломанная markdown-ссылка
- Несуществующий image-файл
- Конфликт версий mkdocs/themes

---

## Workflow #6 — publish-toolkit.yml (Publish docs-toolkit)

**Зачем:** публикация Python-пакета docs-toolkit в TestPyPI или PyPI.

### Ручной запуск

1. https://github.com/svend4/lorenzo/actions/workflows/publish-toolkit.yml
2. **Run workflow**:
   - target: `testpypi` (для проверки) или `pypi` (релиз)
   - branch: `main`

Или через тег:
```bash
git tag toolkit-v0.1.0
git push origin toolkit-v0.1.0  # автотриггер
```

### Что искать в логах

✅ **PASS** — пакет загружен, виден на PyPI.

❌ **FAIL варианты:**

| Сообщение | Что делать |
|---|---|
| `version X already exists on PyPI` | Поднять версию в `pyproject.toml` |
| `Invalid distribution` | Запустить `python -m build` локально |
| `Auth failed` | Проверить `PYPI_API_TOKEN` в Secrets |

---

## Workflow #7 — enrich-docs.yml (Auto-enrichment)

**Зачем:** добавление see-also секций, cross-ссылок, абстрактов в docs/.

### Ручной запуск

1. https://github.com/svend4/lorenzo/actions/workflows/enrich-docs.yml
2. **Run workflow**:
   - `dry_run`: `true` (предпросмотр без коммита) или `false` (применить)
   - branch: `main`

### Что должно произойти

6 enrichment-скриптов → safety gate → коммит `[skip ci]`.

### Что искать в логах

✅ **PASS** + `dry_run=false`:
```
✓ Safety check passed: +12500 / -200
[main XXXXXXX] docs: auto-enrich (see-also, crosslinks, ...) [skip ci]
```

✅ **PASS** + `dry_run=true`:
```
## Dry-run: would commit 245 files
## +12500 / -200 lines
```

❌ **Safety gate сработал** (защита):
```
::error::Enrichment removed more lines (1500) than added (300). Aborting.
```
Это **не баг workflow**, это **защита**. Что-то из enrichment-скриптов начало
стирать контент. Нужно расследование локально:
```bash
python scripts/improve_see_also.py        # запустить руками, посмотреть что меняется
git diff --stat
```

---

## После каждого запуска: что фиксировать

В Issue/PR-комментарии:
- ✅/❌ для каждого workflow
- Время выполнения (минуты)
- Скриншот failed-job если есть ошибки
- Ссылка на конкретный workflow run

Пример:
```markdown
## CI verification 2026-05-15

| Workflow | Status | Time | Notes |
|---|---|---|---|
| test.yml | ✅ | 11m | 4855 passed |
| benchmark.yml | ✅ | 3m | no regression |
| docs.yml | ❌ | 5m | Hit Rate@10 = 0.65 — see PR #28 |
| docs_check.yml | ⚠️ | 2m | OSError known issue, see Issue #X |
| docs-portal.yml | ✅ | 2m | |
| enrich-docs.yml | ✅ dry | 4m | +12500/-200, ready to commit |
```

---

## Аварийный план: что делать если всё красное

1. **Не паниковать** — 42,952 тестов проходят локально (audit 14 мая)
2. **Проверить локально** — `python scripts/verify_all_workflows.py`
3. **Если локально зелёно** — проблема в CI-среде:
   - Версия Python? (CI: 3.11)
   - pip cache? (попробовать без cache)
   - Permissions? (`contents: write` нужен)
4. **Если локально красно** — реальный баг, открыть Issue с traceback

---

## Связанные документы

- `docs/CI_COST_INCIDENT_2026-05-14.md` — постмортем инцидента 5441 мин
- `.github/workflows/*.yml` — сами файлы
- `scripts/verify_all_workflows.py` — локальный симулятор

## Смотрите также
- [Главная](README.md)
- [Метрики](METRICS.md)
- [Здоровье](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Сущности](ENTITIES.md)
- [Решения](DECISIONS.md)
