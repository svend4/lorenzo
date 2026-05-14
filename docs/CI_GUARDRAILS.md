# CI Guardrails (защита от перерасхода minutes)

> Основано на инциденте [`docs/CI_COST_INCIDENT_2026-05-14.md`](CI_COST_INCIDENT_2026-05-14.md) (ветка `claude/current-dev-stage-dJtu0`). Этот документ закрепляет правила в `claude/current-dev-stage-iVIov`.

## 1. Обязательные требования к каждому `.github/workflows/*.yml`

```yaml
on:
  push:
    branches: [main, master]          # ← никаких wildcard "claude/**", "feature/**", "*"
    paths: [...]                       # ← конкретный список
  pull_request:
    branches: [main, master]
  workflow_dispatch:

concurrency:                           # ← ОБЯЗАТЕЛЬНО
  group: <workflow-id>-${{ github.ref }}
  cancel-in-progress: true

jobs:
  some-job:
    runs-on: ubuntu-latest
    timeout-minutes: 20                # ← ОБЯЗАТЕЛЬНО на каждом job
    steps:
      - name: Long step
        timeout-minutes: 15            # ← на шагах с pytest/network
```

## 2. Текущий статус workflows (после фикса 2026-05-14)

| Файл | Триггер | concurrency | timeout-minutes | Состояние |
|------|---------|-------------|-----------------|-----------|
| `test.yml` (v4) | `main`, `master`, PR, dispatch | ✅ `test-${{ github.ref }}` | 7 точек (6 jobs + pytest step) | ✅ |
| `docs.yml` | `main`, `master`, dispatch | ✅ `docs-update-${{ github.ref }}` | 25 мин | ✅ |
| `docs_check.yml` | PR (`docs/**`, `scripts/**`) | ✅ `docs-check-${{ github.ref }}` | 15 мин | ✅ |
| `benchmark.yml` | `main`, PR, dispatch | ✅ `benchmarks-${{ github.ref }}` | 30 мин | ✅ |
| `docs-portal.yml` | `main`, dispatch | ✅ `docs-portal-${{ github.ref }}` | 20/10 мин | ✅ |
| `publish-toolkit.yml` | tag `toolkit-v*`, dispatch | ✅ `publish-toolkit-${{ github.ref }}` | 5 jobs × 10–25 мин | ✅ |

## 3. Авто-коммиты

| Источник | Куда коммитит | `[skip ci]` |
|----------|----------------|-------------|
| `docs.yml` workflow (после `improve_run_all.py`) | `main`/`master` | ✅ есть |
| `.git/hooks/post-commit` (`improve_progress_sync.py`) | **не делает commit**, только модифицирует `docs/PROGRESS.md` | n/a |
| Ручные `chore: sync PROGRESS.md` от агента в feature-ветке | `claude/...` | n/a (workflow не триггерится на эту ветку) |

## 4. Чек-лист перед мерджем нового workflow

- [ ] В `on.push.branches` нет wildcard'ов (`claude/**`, `feature/**`, `*`)
- [ ] Есть `concurrency` с `cancel-in-progress: true`
- [ ] У каждого `job` есть `timeout-minutes` (15–30 мин)
- [ ] У pytest-step есть `--timeout=<60s>`
- [ ] `paths:` — конкретный список, без `**/*`

## 5. Запрещённые паттерны

```yaml
on:
  push:
    branches: ["claude/**"]      # ❌ feature-ветки активного агента
  push:
    branches: ["**"]             # ❌ любая ветка
  push:
    paths: ["**/*"]              # ❌ любой файл
```

## 6. Мониторинг

Раз в неделю проверять расход:

```bash
gh api -X GET /repos/svend4/lorenzo/actions/runs --paginate \
  | jq '[.workflow_runs[] | select(.created_at > "2026-05-01")] | length'
```

Или через UI: `Settings → Billing → Usage`.

Тревожные признаки:
- Расход растёт быстрее активности разработки.
- 5+ одновременных ранингов одного workflow.
- В billing один workflow >70% минут.
