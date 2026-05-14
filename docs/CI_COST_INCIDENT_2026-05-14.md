# Инцидент: перерасход GitHub Actions minutes (2026-05-14)

> **Статус:** разрешён · **Автор:** Claude Code session · **Коммит фикса:** [`9130eb51`](../../../commit/9130eb51) · **Probe:** [`8e82f348`](../../../commit/8e82f348) · **Re-probe после top-up бюджета:** см. историю коммитов ветки.
>
> **TL;DR:** воркфлоу `.github/workflows/test.yml` сжёг **5441 минуту за один день** (~$32.65) из-за триггера на push в любую ветку `claude/**`. GitHub Actions billing limit был исчерпан, тесты перестали запускаться до сброса 16 мая 01:00 UTC. Триггер изменён, добавлены `concurrency` и timeout-cap'ы.

---

## 1. Что произошло

С 10 по 14 мая 2026 года минуты GitHub Actions, потраченные на `test.yml` в репозитории `lorenzo`, росли по экспоненте:

| Дата       | Минут на test.yml | Стоимость   | Прирост за день |
|------------|-------------------|-------------|-----------------|
| 2026-05-10 | 102               | $0.61       | —               |
| 2026-05-11 | 328               | $1.97       | × 3.2           |
| 2026-05-12 | 242               | $1.45       | × 0.7           |
| 2026-05-13 | **1 698**         | **$10.19**  | × 7.0           |
| 2026-05-14 | **5 441**         | **$32.65**  | × 3.2           |
| **Σ**      | **7 811**         | **$46.87**  | —               |

Источник данных: `usageReport_1_d06e0a3f7cd5464b9994edf0e9ba1f72.csv` (GitHub Billing → Usage report).

На 14 мая в 18:xx UTC GitHub отключил запуски Actions: «You've hit your limit · resets May 16, 1am (UTC)». Это **заблокировало все CI-проверки**: `test.yml`, `docs.yml`, `docs_check.yml`, `benchmark.yml`. Ни push, ни PR не могли пройти валидацию.

## 2. Как это выглядело

Симптомы, по которым можно было заметить раньше:

1. **В UI GitHub Actions** на вкладке *Usage* — кривая `actions_linux` рвётся вверх с 13 мая.
2. **Время выполнения отдельных runs** растёт: средний run `test.yml` около 5-7 минут × 6 jobs = ~35 минут на push. При 100+ push'ах в день — около 3500 минут (попадает в порядок 5441).
3. **`Stop hook`-сообщения локально**: pre-commit пускал тяжёлые регенерации (`improve_run_all.py`), что плодило коммиты → каждый push снова запускал test.yml.
4. **Биллинг-email от GitHub** о приближении к лимиту (если подписан на уведомления).

## 3. Корневая причина

Файл `.github/workflows/test.yml` (v3) триггерил полный пайплайн **на каждый push в любую ветку `claude/**`**:

```yaml
on:
  push:
    branches: [main, master, "claude/**"]    # ← вот это
    paths:
      - "scripts/**.py"
      - "tests/**"
      …
```

При активной работе агента в ветке `claude/current-dev-stage-dJtu0` каждый commit (включая авто-коммиты регенерированной аналитики) триггерил **6 параллельных jobs**:

1. `python-syntax`
2. `unit-tests` (с `--timeout=120` на тест и **без `timeout-minutes`** на job → потолок 6 часов)
3. `mcp-smoke`
4. `validate-templates`
5. `validate-tasks`
6. `catalog-fresh` (тяжёлая регенерация SCRIPTS_CATALOG/TASKS_INDEX/REGISTRY)

Усугубляющие факторы:

- **Нет `concurrency`-группы** — старые ранинги не отменялись при новом push, копились параллельные запуски.
- **Нет `timeout-minutes` на job-level** — зависший тест мог тикать до 6-часового дефолта GitHub.
- **`Stop hook`-логика** провоцировала вторичные коммиты от агента (регенерация docs/), каждый из которых снова дёргал CI.

## 4. Что было сделано

Коммит [`9130eb51`](../../../commit/9130eb51), файл `.github/workflows/test.yml`:

```diff
-name: Test & Validate  # v3: fix textrank-runpy timeout + progress-sync tags
+name: Test & Validate  # v4: drop claude/** trigger + concurrency + lower test timeout

 on:
   push:
-    branches: [main, master, "claude/**"]
+    branches: [main, master]
     paths:
       - "scripts/**.py"
       - "tests/**"
       …
   pull_request:
     branches: [main, master]
   workflow_dispatch:

+concurrency:
+  group: test-${{ github.ref }}
+  cancel-in-progress: true

 jobs:
   python-syntax:
     runs-on: ubuntu-latest
+    timeout-minutes: 20
     …
   unit-tests:
     runs-on: ubuntu-latest
+    timeout-minutes: 20
     …
     - name: Run tests/
+      timeout-minutes: 15
-      run: pytest … --timeout=120 …
+      run: pytest … --timeout=60 …
```

Конкретно:

1. **Триггер `claude/**` удалён** — workflow запускается только на `main`/`master` и в PR.
2. **`concurrency` group** на `${{ github.ref }}` с `cancel-in-progress: true` — новый push отменит предыдущий ранинг по той же ветке.
3. **`timeout-minutes: 20` на каждый job** — потолок вместо 6-часового дефолта.
4. **`timeout-minutes: 15` на step `Run tests/`** + per-test `--timeout=60` — зависший тест убивается за минуту.

Ожидаемый эффект: бюджет минут на feature-ветке падает с тысяч в день до **нуля** (CI на feature-ветке не запускается вовсе); полный пайплайн прогоняется один раз при PR в `main`.

## 5. Инструкция: как делать в будущем

### 5.1. Правила для всех новых GitHub Actions workflow

**ОБЯЗАТЕЛЬНО** в каждом новом `.github/workflows/*.yml`:

```yaml
on:
  push:
    branches: [main, master]        # ← НИКОГДА не добавлять wildcard "claude/**", "feature/**", "*"
    paths: […]                       # ← всегда указывать paths, чтобы не тригериться на каждый коммит
  pull_request:
    branches: [main, master]
  workflow_dispatch:                  # ← оставить ручной запуск

concurrency:                          # ← ОБЯЗАТЕЛЬНО
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  some-job:
    runs-on: ubuntu-latest
    timeout-minutes: 20               # ← ОБЯЗАТЕЛЬНО на каждом job
    steps:
      - name: Long step
        timeout-minutes: 10           # ← желательно на step'ах, где есть pytest/network
        run: …
```

### 5.2. Чек-лист перед мерджем нового workflow

- [ ] В `on.push.branches` нет wildcard'ов (`claude/**`, `feature/**`, `*`)
- [ ] Есть секция `concurrency` с `cancel-in-progress: true`
- [ ] У каждого job есть `timeout-minutes` (рекомендуется 15-30 мин)
- [ ] У pytest-step есть `--timeout=<60s>` (плагин `pytest-timeout`)
- [ ] Если есть `paths:` — список конкретный, без `"**/*"` или `"**"`
- [ ] Тяжёлые job'ы (регенерация, neural-индексация) — отдельный workflow с `workflow_dispatch` или cron

### 5.3. Мониторинг

Раз в неделю проверять расход:

```bash
# Через gh CLI (если установлен):
gh api -X GET /repos/svend4/lorenzo/actions/runs --paginate \
  | jq '[.workflow_runs[] | select(.created_at > "2026-05-01")] | length'

# Или через UI:
# https://github.com/svend4/lorenzo/settings/billing → Usage
```

Признаки начинающейся утечки минут:
- Усреднённый расход растёт быстрее, чем активность разработки.
- В вкладке Actions висят 5+ одновременных ранингов одного workflow.
- В отчёте billing один workflow доминирует (>70% минут).

### 5.4. Что делать, если лимит уже исчерпан

1. **Не паниковать** — реальной поломки нет, ждать сброса до начала следующего расчётного периода (как правило, 1 число месяца UTC).
2. **Пока CI заблокирован** — прогонять тесты локально:
   ```bash
   python -m pytest tests/ --ignore=tests/test_ann_index.py -q --timeout=60
   python -m pytest docs-toolkit/tests/ -q
   ```
3. **Подготовить фикс** в feature-ветке (commit можно — push безопасен, CI не запустится из-за лимита).
4. **Сразу после сброса** — мерджить фикс в `main` под наблюдением, чтобы убедиться, что новый workflow не повторяет паттерн.

### 5.5. Запрещённые паттерны

❌ **Никогда не делать так:**

```yaml
on:
  push:                           # без branches: → триггер на любую ветку
    paths: ["**"]                 # триггер на любой файл
on:
  push:
    branches: ["**"]              # любая ветка
on:
  push:
    branches: ["feature/**"]      # feature-ветки активного агента/команды
```

✅ **Правильно:**

```yaml
on:
  push:
    branches: [main, master]      # только защищённые ветки
    paths: ["scripts/**.py", "tests/**", ".github/workflows/test.yml"]
  pull_request:
    branches: [main, master]
```

## 6. Тайм-лайн

| Время (UTC)         | Событие                                                           |
|---------------------|-------------------------------------------------------------------|
| 2026-05-10          | Первые запуски `test.yml` в claude/** ветке: 102 мин              |
| 2026-05-11..12      | Рост до 242-328 мин/день                                          |
| 2026-05-13          | Резкий скачок: 1698 мин (× 7)                                     |
| 2026-05-14          | Пик: 5441 мин ($32.65), GitHub блокирует Actions                  |
| 2026-05-14, ~18:00  | Инцидент обнаружен через usage report CSV                         |
| 2026-05-14, ~18:30  | Коммит [`9130eb51`](../../../commit/9130eb51) — фикс воркфлоу    |
| 2026-05-14          | Документация инцидента (этот файл)                                |
| **2026-05-16, 01:00** | **Сброс лимита GitHub Actions** — CI снова работает             |

## 7. Связанные файлы

- [`.github/workflows/test.yml`](../.github/workflows/test.yml) — исправленный workflow (v4)
- [`.github/workflows/docs.yml`](../.github/workflows/docs.yml) — auto-docs workflow (триггер только на main, OK)
- [`.github/workflows/benchmark.yml`](../.github/workflows/benchmark.yml) — benchmark workflow (проверить, что не триггерит на claude/**)
- [`.github/workflows/docs_check.yml`](../.github/workflows/docs_check.yml) — docs check workflow (проверить триггер)

## 8. Уроки

1. **Wildcard-триггеры — антипаттерн.** `claude/**`, `feature/**`, `dev/**` на push приводят к взрывному росту минут при активной работе на feature-ветках.
2. **`concurrency` — не optional.** Любой workflow, который может быть запущен несколько раз подряд, должен иметь `concurrency` группу с `cancel-in-progress`.
3. **`timeout-minutes` — не optional.** GitHub-дефолт 6 часов слишком велик для не-релизных job'ов.
4. **Авто-коммиты агента усиливают любую CI-утечку.** Если post-commit hook или скрипт делает дополнительные коммиты, каждый из них дёргает CI — нужно либо `[skip ci]` в commit message, либо отключать CI на feature-ветках совсем.
5. **Регулярный аудит billing.** Раз в неделю смотреть GitHub Billing → Usage; раз в месяц скачивать CSV usage report.
