# Lorenzo — монорепозиторий

<!-- badges -->
![docs](docs/badges/docs.svg) ![words](docs/badges/words.svg) ![scripts](docs/badges/scripts.svg) ![health](docs/badges/health.svg) ![go/no-go](docs/badges/scoring.svg) ![license](docs/badges/license.svg) ![branch](docs/badges/branch.svg)

Монорепозиторий с двумя крупными активами:

1. **`docs/`** — исследовательская база по проекту **Svyazi 2.0** и смежным темам (**2815 markdown-файлов**, ~2.9 млн слов, 22 проанализированных Habr-проекта, **32 контакт-файла** авторов).
2. **`docs-toolkit/`** — Python-пакет общего назначения: RAG / agent / workflow / eval / federation / observability framework для markdown-монорепозиториев. **220+ спринтов, 489 модулей, 546 тестовых файлов, версия 0.3.0** (Phases I–IX выполнены — см. [`docs-toolkit/DEVELOPMENT_STATUS.md`](docs-toolkit/DEVELOPMENT_STATUS.md)).

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
│   ├── docstoolkit/                       # 489 модулей (см. ниже)
│   ├── tests/                             # 546 тестовых файлов
│   ├── README.md                          # обзор пакета + roadmap
│   ├── DEVELOPMENT_STATUS.md              # детальный статус фаз I–IX
│   └── pyproject.toml                     # PEP 621, версия 0.3.0
│
├── scripts/                               # 187 batch-скриптов улучшения корпуса
│   ├── improve_*.py                       # обработка документов (24 группы)
│   ├── mcp_server.py                      # MCP-сервер для Claude Desktop
│   ├── gateway.py                         # OpenAI-compatible HTTP gateway (FastAPI)
│   └── ...
│
├── tests/                                 # 199 unit-тестов корневых скриптов
│
└── .claude/skills/                        # 28 Claude-скиллов
```

---

## Что есть прямо сейчас (2026-05-15)

| Актив | Статус | Метрика |
|-------|--------|---------|
| Документная база | ✅ собрана | **2815 markdown-файлов**, ~2.9 млн слов, **HEALTH 99/100**, **METRICS 97.9/100** |
| Анализ 22 Habr-проектов | ✅ завершён | **32 контакт-файла** в `docs/contacts/`, готовы к отправке |
| docs-toolkit (Python framework) | ✅ **220+ спринтов**, **v0.3.0** | **489 модулей**, **546 тестовых файлов**, roadmap 35/35 (Path A/B/C), Phases I–IX закрыты (18 выполнено, 3 отложено, 3 пропущено) |
| `ask()` composition matrix | ✅ | **17 ортогональных kwargs**, **6 named presets**, **18 standalone-хелперов** |
| Скрипты обработки | ✅ зрелые | **187 скриптов** в **24 группах** (`improve_run_all.py --group …`) |
| Тесты корневых скриптов | ✅ | **199 файлов** в `tests/` |
| Claude-скиллы | ✅ | **28 skills** в `.claude/skills/` |
| ROADMAP плана развития | ✅ описан | 35 идей × 4 уровня сложности |
| CI/CD | ✅ | `test.yml` (5 джоб: syntax/unit/MCP/templates/catalog), `docs.yml` (auto-PR с метриками), benchmark regression check |
| Прототип Knowledge OS | ✅ итерации 0–15 | RFC-система, lifecycle promote (1005 approved), 23 proposals, MCP 15 инструментов, OpenAI-compatible gateway |
| Контакты авторам | ⏳ не отправлены | требуется ручная отправка |
| LLM-обогащение (опц.) | ⏳ не запущено | `pip install anthropic` + `improve_llm_enrich.py` |

**Прогресс MVP:** **64% (7/11 milestones)** — Подробнее: [`docs/PROGRESS.md`](docs/PROGRESS.md).
**Go/No-Go:** **96 🟢** (см. [`docs/SCORING.md`](docs/SCORING.md))

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

**489 модулей**, реализованы за **220+ спринтов**, покрыты **546 тестовыми файлами** (десятки тысяч тест-кейсов). Полная карта: [`docs-toolkit/README.md`](docs-toolkit/README.md) + [`docs-toolkit/DEVELOPMENT_STATUS.md`](docs-toolkit/DEVELOPMENT_STATUS.md).

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
| **Reasoning advanced** | `self_rag/`, `debate/`, `got/`, `negotiation/`, `metabolism/`, `personality/`, `adversarial/`, `epistemic/`, `diffusion/`, `bandit/` | Self-RAG reflect loop, multi-agent debate, graph-of-thoughts, auction-broker, adversarial co-evolution |
| **Knowledge Graph** | `knowledge_graph/` | TripleStore (SQLite WAL), mini Query DSL `"py" uses ?x`, hash-join over patterns |
| **Privacy** | `federated_eval/`, `private_search/` | Gaussian DP + PrivacyAccountant, Bonawitz-style secure aggregation |
| **Composition** | `rag/presets`, `rag/advanced`, `rag/saved`, `rag/bulk_diff`, `rag/bandit_ask` | 17 ortho `ask()` kwargs + 6 named presets + 18 standalone-хелперов |
| **Deployment** | `Dockerfile`, `Dockerfile.bge`, `deploy/` | Docker images + docker-compose profiles + Helm chart |

Подробный список модулей: [docs/ROADMAP/00-CURRENT-STATE.md](docs/ROADMAP/00-CURRENT-STATE.md#3-карта-модулей-docstoolkit) + [docs-toolkit/PROFILES.md](docs-toolkit/PROFILES.md) (composition matrix) + [docs-toolkit/ARCHITECTURE.md](docs-toolkit/ARCHITECTURE.md) (5 ADRs).

---

## scripts/: 187 batch-скриптов в 24 группах

Запуск всех — `python scripts/improve_run_all.py [--smart|--fast|--group X|--changed|--parallel N]`

| Группа | Что делает |
|--------|------------|
| `quality` / `quality-extra` | Орфография, читаемость, content gaps, link preview, дубли, broken-links, retrieval Hit Rate@K |
| `export` / `export-extra` | Obsidian, EPUB, RSS/Atom, Confluence, REPORT.md, CSV/HTML/JSON, extract code/tables |
| `cicd` | GitHub Issues, workflows, pre-commit, dependabot |
| `analytics` | Citations, reading time, version diff, topic model, cross-section, digest-auto |
| `textwork` | Reclassify, merge by topic, outline, compare, subtopic-fill, crosslink, source-map |
| `deeptext` | TOC, abstracts, NER, timeline, BM25, semantic chunks, segmenter |
| `nlpplus` | TextRank, heading audit, language split, faceted search, similar passages, knowledge map |
| `content` / `content-gen` | Auto-linker, gap-filler, summaries, READMEs, TOC, Q&A, glossary, tags, badges, sitemap, mindmap |
| `meta` | Tech radar, onboarding, risk register, KPI snapshot, component matrix, dependency map |
| `analysis` | Decisions, concepts, KPI, action items, timeline, narrative, clusters, density, heatmap, sentiment |
| `links` | Backlinks, crossrefs, similar, graph, network, reading order |
| `llm` / `llm-extra` | (платные) Enrich, summary, Q&A, contact, semantic gap detection |
| `reports` | Health, metrics, scoring, entities, stats, orphans, missing, staleness, coverage, priorities, registry |
| `contacts-extra` | CONTACTS.md, contact priority, migrate to frontmatter |
| `templates` | Generate templates, init from template, migrate frontmatter |
| `index-meta` | Search index, scripts catalog, self-audit, SQLite audit log |
| `mcp-tools` | MCP dashboard, MCP smoke-tests |
| `workflow` | Pipeline runner v1/v2, task codegen, watcher, progress sync, changelog, digest |
| `lifecycle` | Card promote, proposals gen, RFC update, auto-summarize, progressive summarize |
| `semantic` | TF-IDF + sentence-transformers семантический индекс |
| `live` | GitHub author activity tracker (не в авто-запуске) |
| `infra` | Run all, autofill, watch, benchmark |

Полный список команд: [`CLAUDE.md`](CLAUDE.md) (читается Claude Code каждой сессией).

---

## Принципы

1. **Ничего не удалено.** Все исходные документы в корне сохранены as-is.
2. **Разделено, а не сжато.** Содержимое больших отчётов перенесено в маленькие тематические файлы.
3. **Папки по темам, подпапки по подтемам.** Каждый раздел имеет свой `README.md`.
4. **Local-first, stdlib-first.** docs-toolkit работает offline, тяжёлые зависимости опциональны.
5. **Авто-обновление.** Большая часть документов в `docs/` авто-генерируется скриптами `improve_*.py`; CI `docs.yml` открывает PR с обновлёнными метриками после push в main.
6. **Test-on-merge.** 546 тестовых файлов в `docs-toolkit/tests/` + 199 в `tests/` + integrity checks (MCP smoke / templates / catalog-fresh) — все 5 джоб в `.github/workflows/test.yml`.

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
- [`docs/CI_COST_INCIDENT_2026-05-14.md`](docs/CI_COST_INCIDENT_2026-05-14.md) — **постмортем перерасхода GitHub Actions minutes + инструкция по написанию воркфлоу** (обязательно к прочтению перед созданием нового `.github/workflows/*.yml`)
