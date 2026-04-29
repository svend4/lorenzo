# Lorenzo / Svyazi 2.0 — CLAUDE.md

Это репозиторий-монорепо для проекта **Svyazi 2.0** — экосистемы из 20+ OSS-компонентов
для AI-систем с памятью, оркестрацией агентов и безопасной обработкой данных.

## Структура репозитория

```
lorenzo/
├── docs/                          # вся документация (~460 файлов, 374K слов)
│   ├── 01-svyazi/                 # архитектура, компоненты, дорожная карта
│   ├── 02-anthropic-vacancies/    # анализ 436 вакансий Anthropic
│   ├── 03-technology-combinations/# 40+ комбинаций технологий
│   ├── 04-ai-collaborations/      # 5 ансамблей OSS-проектов
│   ├── 05-habr-projects/          # проекты с Хабра (память, граф, knowledge)
│   ├── autofilled/                # карточки, сгенерированные из шаблонов
│   ├── badges/                    # SVG-бейджи репо
│   └── templates/                 # шаблоны для новых документов
├── scripts/                       # 69 скриптов improve_*.py
│   ├── improve_run_all.py         # запустить все скрипты
│   ├── improve_llm_enrich.py      # LLM-обогащение stub-файлов (нужен API ключ)
│   ├── improve_llm_qa.py          # LLM-ответы на открытые вопросы
│   ├── improve_llm_gaps.py        # LLM-анализ семантических пробелов
│   ├── improve_autofill.py        # заполнение шаблонов данными
│   └── mcp_server.py              # MCP-сервер (search_docs, get_doc, run_script)
├── .claude/
│   ├── mcp.json                   # конфиг MCP-сервера для Claude Code
│   └── skills/                    # скиллы: analyze-project, write-contact, review-docs
└── CLAUDE.md                      # этот файл
```

## Ключевые документы

| Файл | Содержимое |
|------|-----------|
| `docs/SCORING.md` | Go/No-Go: **159/164 = 96% 🟢 GO** |
| `docs/01-svyazi/01-executive-summary.md` | краткое описание проекта |
| `docs/01-svyazi/07-mvp-planning.md` | MVP план, риски, оценки |
| `docs/01-svyazi/12-roadmap.md` | дорожная карта |
| `docs/CONTACTS.md` | контакты авторов OSS-компонентов |
| `docs/FAQ.md` | часто задаваемые вопросы (54 Q&A) |
| `docs/HEALTH.md` | здоровье репозитория |
| `docs/NETWORK.md` | граф связей компонентов |

## Скрипты — иерархия ступеней

### Ступень 1: Детерминированные скрипты (65 штук)
```bash
python scripts/improve_run_all.py            # все скрипты
python scripts/improve_run_all.py --fast     # без медленных
python scripts/improve_run_all.py --group analysis  # одна группа
```
Группы: `structure`, `index`, `analysis`, `extract`, `quality`, `graph`, `reports`, `export`, `enrich`

### Ступень 2: Шаблоны + автозаполнение
```bash
python scripts/improve_autofill.py           # заполняет шаблоны данными
# Шаблоны: docs/templates/component-card.md, research-note.md, ...
```

### Ступень 3: Claude API (требует ANTHROPIC_API_KEY)
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/improve_llm_enrich.py         # обогащает stub-файлы (<150 слов)
python scripts/improve_llm_qa.py             # отвечает на открытые вопросы
python scripts/improve_llm_gaps.py           # находит семантические пробелы
```
Модель: `claude-haiku-4-5`, ~$0.01–0.03 за файл.

### Ступень 4: Скиллы (.claude/skills/)
- `analyze-project` — алгоритм анализа любого компонента Svyazi
- `write-contact` — шаблон письма авторам OSS-проектов
- `review-docs` — воркфлоу проверки качества документации

### Ступень 5: MCP-сервер
```bash
python scripts/mcp_server.py                 # запуск сервера (stdio)
# Инструменты: search_docs, get_doc, run_script, get_stats
```
Конфиг: `.claude/mcp.json`

## Компоненты Svyazi 2.0

| Компонент | Роль | Лицензия |
|-----------|------|---------|
| CardIndex | индекс знаний, 785+ карточек | MIT |
| AgentFS | файловая система для AI | MIT |
| Yodoca | память с консолидацией | Apache 2.0 |
| NGT-memory | ассоциативный граф памяти | BSL 1.1 |
| SENTINEL | безопасность, allowlist MCP | MIT |
| Rufler | оркестратор агентов | — |
| knowledge-space | база знаний | MIT |
| Firecrawl | веб-краулер | MIT |

## Текущий статус

- **Документация:** ✅ 96% готовности (Go/No-Go)
- **Архитектура:** ✅ описана (integration contracts, ADR, security)
- **MVP-прототип:** ⬜ нужно реализовать Knowledge OS
- **Контакты с авторами:** ⬜ написать kksudo, spbmolot

## Полезные команды

```bash
# Обновить всю документацию
python scripts/improve_run_all.py

# Проверить качество
python scripts/improve_run_all.py --group quality

# Обновить статистику и отчёты
python scripts/improve_run_all.py --group reports

# Найти документ
grep -r "AgentFS" docs/ -l

# Посмотреть граф связей
cat docs/NETWORK.md
```
