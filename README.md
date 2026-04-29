# Lorenzo — монорепозиторий

<!-- badges -->
![docs](docs/badges/docs.svg) ![words](docs/badges/words.svg) ![scripts](docs/badges/scripts.svg) ![health](docs/badges/health.svg) ![go/no-go](docs/badges/scoring.svg) ![license](docs/badges/license.svg) ![branch](docs/badges/branch.svg)

Монорепозиторий с двумя крупными активами:

1. **`docs/`** — исследовательская база по проекту **Svyazi 2.0** и смежным темам (1700+ файлов, ~1.7 млн слов, 22 проанализированных Habr-проекта, 14 контактов авторов).
2. **`docs-toolkit/`** — Python-пакет общего назначения: RAG / agent / workflow / eval / federation / observability framework для markdown-монорепозиториев. **53 спринта, 30+ модулей, 546 тестов.**

---

## Структура

```
lorenzo/
├── README.md                              # этот файл
├── CLAUDE.md                              # контекст для Claude Code
├── CHANGELOG.md                           # авто-changelog (improve_changelog_auto.py)
│
├── deep-research-report (1-4).md          # ОРИГИНАЛЫ — не изменены
├── Вакансии в Anthropic ...               # ОРИГИНАЛ MHTML — не изменён
├── Комбинирование технологий ...          # ОРИГИНАЛ MHTML — не изменён
├── Поиск коллабораций AI проектов         # ОРИГИНАЛ MHTML — не изменён
├── Поиск уникальных проектов на Хабре ... # ОРИГИНАЛ MHTML — не изменён
│
├── docs/                                  # тематически разделённые документы
│   ├── 01-svyazi/                         # Svyazi 2.0: архитектура, MVP (16 файлов)
│   ├── 02-anthropic-vacancies/            # 436 вакансий Anthropic, 12 кластеров (357 файлов)
│   ├── 03-technology-combinations/        # 40+ синергий технологий (7 файлов)
│   ├── 04-ai-collaborations/              # 5 ансамблей OSS-проектов (17 файлов)
│   ├── 05-habr-projects/                  # 22 Habr-проекта: memory/, knowledge/ (10+56 файлов)
│   ├── svyazi-2-0/                        # альтернативное представление Svyazi (59 файлов)
│   ├── nautilus/                          # NPP v1.1 RFC + 8 companion papers (255 файлов)
│   ├── lorenzo-agent/                     # системный промпт Lorenzo Catalyst Agent (62 файла)
│   ├── anthropic-vacancies/               # детальные кластеры + profile-mapping (111 файлов)
│   ├── technology-combinations/           # детальные комбинации
│   ├── ai-collaborations/                 # детальные коллаборации (30 файлов)
│   ├── habr-unique-projects/              # детальные Habr-проекты (56 файлов)
│   ├── contacts/                          # 14 контактов авторов
│   ├── obsidian/                          # экспорт в Obsidian формат (524 файла)
│   ├── glossary/                          # кросс-ссылочный словарь
│   ├── templates/                         # 23 шаблона документов
│   ├── ROADMAP/                           # ⭐ варианты развития (35 идей: simple → novel)
│   └── *.md                               # 100+ авто-генерируемых аналитических отчётов
│
├── docs-toolkit/                          # ⭐ Python-пакет (RAG/agent/workflow framework)
│   ├── docstoolkit/                       # 30+ модулей (см. ниже)
│   ├── tests/                             # 546 тестов
│   ├── README.md                          # обзор пакета + roadmap
│   └── pyproject.toml                     # PEP 621
│
├── scripts/                               # 96 batch-скриптов улучшения корпуса
│   ├── improve_*.py                       # обработка документов (12 групп)
│   ├── mcp_server.py                      # MCP-сервер для Claude Desktop
│   └── ...
│
└── .claude/skills/                        # 28 Claude-скиллов
```

---

## Что есть прямо сейчас (2026-04-29)

| Актив | Статус | Метрика |
|-------|--------|---------|
| Документная база | ✅ собрана | 1719 файлов, 1.68М слов |
| Анализ 22 Habr-проектов | ✅ завершён | 14 контактов готовы к отправке |
| docs-toolkit (Python framework) | ✅ 53 спринта | 546 тестов, MCP 30/30, шаблоны 23/23 |
| Скрипты обработки | ✅ зрелые | 96 скриптов в 12 группах |
| ROADMAP плана развития | ✅ описан | 35 идей × 4 уровня сложности |
| Контакты авторам | ⏳ не отправлены | требуется ручная отправка |
| LLM-обогащение (опц.) | ⏳ не запущено | `pip install anthropic` + `improve_llm_enrich.py` |
| Прототип Knowledge OS | ⏳ архитектура | Yodoca + AgentFS + CardIndex как старт |

**Прогресс MVP:** 45% (5/11 milestones). Подробнее: [`docs/PROGRESS.md`](docs/PROGRESS.md).

---

## Точки входа

### Если интересна исследовательская база
- **Что такое Lorenzo (агент)** → [docs/lorenzo-agent/README.md](docs/lorenzo-agent/README.md)
- **Svyazi 2.0** (главный проект) → [docs/01-svyazi/](docs/01-svyazi/) или [docs/svyazi-2-0/README.md](docs/svyazi-2-0/README.md)
- **Карьерные опции в Anthropic** → [docs/anthropic-vacancies/profile-mapping/README.md](docs/anthropic-vacancies/profile-mapping/README.md)
- **Архитектура Nautilus / DHLab** → [docs/nautilus/README.md](docs/nautilus/README.md)
- **Поиск компонента по имени** → [docs/glossary/components-by-name.md](docs/glossary/components-by-name.md)
- **Главный навигационный хаб** → [docs/INDEX.md](docs/INDEX.md)

### Если интересен `docs-toolkit` (Python framework)
- **Обзор пакета** → [docs-toolkit/README.md](docs-toolkit/README.md)
- **API reference** (25 модулей) → [docs-toolkit/API.md](docs-toolkit/API.md)
- **Возможности по слоям** → [docs/ROADMAP/00-CURRENT-STATE.md](docs/ROADMAP/00-CURRENT-STATE.md)
- **Что делать дальше** → [docs/ROADMAP/05-PRIORITIES.md](docs/ROADMAP/05-PRIORITIES.md)
- **Security policy** → [docs-toolkit/SECURITY.md](docs-toolkit/SECURITY.md)
- **Контекст для Claude Code** → [CLAUDE.md](CLAUDE.md)

### Если планируете развивать систему
- **Главный навигатор по идеям** → [docs/ROADMAP/README.md](docs/ROADMAP/README.md)
- **Простые улучшения** (1-3 спринта) → [docs/ROADMAP/01-SIMPLE.md](docs/ROADMAP/01-SIMPLE.md)
- **Mainstream RAG** (2-5 спринтов) → [docs/ROADMAP/02-MEDIUM.md](docs/ROADMAP/02-MEDIUM.md)
- **Frontier research** (4-8 спринтов) → [docs/ROADMAP/03-INNOVATIVE.md](docs/ROADMAP/03-INNOVATIVE.md)
- **Никем не сделанное** (6-12+ спринтов) → [docs/ROADMAP/04-NOVEL.md](docs/ROADMAP/04-NOVEL.md)

### Если нужны исходники
- [sources/README.md](sources/README.md) или сами `.md` / MHTML файлы в корне.

---

## docs-toolkit: возможности на сегодня

30+ модулей, реализованы за 53 спринта, покрыты 546 тестами:

| Слой | Модули | Возможности |
|------|--------|-------------|
| **Ingest** | `ingest/`, `frontmatter`, `lang/` | markdown / PDF / multi-modal загрузка, RU/EN детекция |
| **Retrieval** | `rag/`, `embeddings/`, `rag/adaptive` | keyword + BM25 + semantic + hybrid (RRF) + adaptive multi-hop |
| **Reasoning** | `agent/`, `agent/planner` | ReAct loop с tools, plan-and-execute, dependency-aware subtasks |
| **Orchestration** | `workflow/`, `router/`, `jobs/` | DAG-runner (sync+async), failover-chain, background queue |
| **Memory** | `conversation/`, `cache/` | Sessions с squash-summarize, TTL cache |
| **Eval** | `eval/`, `experiments/`, `feedback/` | Golden datasets P/R/F1, A/B tests, Wilson confidence |
| **Governance** | `auth/`, `budget/`, `prompts/` | RBAC scopes, per-scope budget guards, versioned prompts с A/B |
| **Observability** | `telemetry/`, `serve.py` | OTel traces, Prometheus metrics, SSE streaming |
| **Integration** | `federation/`, `events/`, `webhooks/` | NPP federation, pub-sub bus, HTTP delivery с HMAC+DLQ |
| **Time** | `timetravel/` | Git-based historical queries |

Подробный список модулей: [docs/ROADMAP/00-CURRENT-STATE.md](docs/ROADMAP/00-CURRENT-STATE.md#3-карта-модулей-docstoolkit).

---

## scripts/: 96 batch-скриптов в 12 группах

Запуск всех — `python scripts/improve_run_all.py [--smart|--fast|--group X|--changed|--parallel N]`

| Группа | Скриптов | Что делает |
|--------|---------:|------------|
| `quality` | ~6 | Орфография, читаемость, content gaps, link preview |
| `export` | ~5 | Obsidian, EPUB, RSS/Atom, Confluence, REPORT.md |
| `cicd` | ~4 | GitHub Issues, workflows, pre-commit, dependabot |
| `analytics` | ~6 | Citations, reading time, version diff, topic model |
| `textwork` | ~9 | Reclassify, merge by topic, outline, compare |
| `deeptext` | ~12 | TOC, abstracts, NER, timeline, BM25, chunks |
| `nlpplus` | ~10 | TextRank, heading audit, language split, faceted search |
| `content` | ~3 | Auto-linker, gap-filler, empty sections fill |
| `meta` | ~9 | Tech radar, onboarding, risk register, KPI |
| `llm` | ~4 | (платные) Enrich, summary, Q&A, contact |
| `reports` | ~10 | Health, metrics, scoring, badges |
| `infra` | ~18 | Run all, autofill, watch, benchmark, MCP |

Полный список с командами: [`CLAUDE.md`](CLAUDE.md).

---

## Принципы

1. **Ничего не удалено.** Все исходные документы в корне сохранены as-is.
2. **Разделено, а не сжато.** Содержимое больших отчётов перенесено в маленькие тематические файлы.
3. **Папки по темам, подпапки по подтемам.** Каждый раздел имеет свой `README.md`.
4. **Local-first, stdlib-first.** docs-toolkit работает offline, тяжёлые зависимости опциональны.
5. **Авто-обновление.** Большая часть документов в `docs/` авто-генерируется скриптами `improve_*.py`.
6. **Test-on-merge.** 546 тестов + integrity checks (mcp / templates) гарантируют корректность.

---

## Quick start

### Чтобы изучить корпус
```bash
# Главный индекс
cat docs/INDEX.md

# Состояние здоровья
cat docs/HEALTH.md

# Прогресс MVP
cat docs/PROGRESS.md
```

### Чтобы запустить docs-toolkit
```bash
cd docs-toolkit
pip install -e .

# Простой Q&A через RAG (offline echo answerer)
python -c "from docstoolkit.rag import ask; print(ask('что такое RAG?').answer)"

# Тесты
pytest tests/
```

### Чтобы перегенерировать аналитику корпуса
```bash
python scripts/improve_run_all.py --smart       # умные группы
python scripts/improve_run_all.py --group reports
```

### Чтобы развивать систему
1. Прочитайте [docs/ROADMAP/README.md](docs/ROADMAP/README.md)
2. Выберите путь (Quick value / Differentiation / Long-game) в [05-PRIORITIES.md](docs/ROADMAP/05-PRIORITIES.md)
3. Начинайте первый спринт.

---

## Связанные документы

- [`CLAUDE.md`](CLAUDE.md) — контекст проекта для Claude Code (читается каждой сессией)
- [`CHANGELOG.md`](CHANGELOG.md) — авто-генерируемый changelog
- [`docs-toolkit/CONTRIBUTING.md`](docs-toolkit/CONTRIBUTING.md) — как контрибьютить в пакет
- [`docs/INDEX.md`](docs/INDEX.md) — навигационный хаб по корпусу
- [`docs/HEALTH.md`](docs/HEALTH.md) — балл здоровья репо
- [`docs/TECH_RADAR.md`](docs/TECH_RADAR.md) — Tech Radar (ADOPT/TRIAL/ASSESS/HOLD)
- [`docs/SCORING.md`](docs/SCORING.md) — Go/No-Go скоринг (96% → GO)
- [`docs/RISK_REGISTER.md`](docs/RISK_REGISTER.md) — реестр рисков
- [`docs/COMPONENT_MATRIX.md`](docs/COMPONENT_MATRIX.md) — матрица 14 компонентов × 10 возможностей
