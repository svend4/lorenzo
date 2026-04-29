# Lorenzo — CLAUDE.md

Контекст проекта для Claude Code. Читается автоматически при старте каждой сессии.

## Что это

Монорепозиторий исследований для **Svyazi 2.0** — локальной community intelligence platform.
Цель: собрать лучшие OSS-проекты с Хабра в единую архитектуру Knowledge OS.

## Структура

```
docs/
  01-svyazi/           — архитектура Svyazi 2.0 (16 файлов)
  02-anthropic-vacancies/ — анализ 436 вакансий Anthropic
  03-technology-combinations/ — 40+ синергий технологий
  04-ai-collaborations/ — 5 ансамблей OSS-проектов
  05-habr-projects/    — проекты с Хабра: memory/, knowledge/
  contacts/            — контактные файлы 14 авторов (generate автоматически)
  templates/           — шаблоны документов
  CONTACTS.md          — сводная таблица авторов и проектов
  ENTITIES.md          — упоминания проектов (22 проекта)
  DECISIONS.md         — ключевые архитектурные решения
  HEALTH.md            — балл здоровья репо (75/100)
  METRICS.md           — метрики качества документов (65.7/100)
  SCORING.md           — Go/No-Go (96% → GO)
  search_index.json    — поисковый индекс (483 документа, content+preview)
  CONTENT_GAPS.md      — темы без документа
  READING_TIME.md      — время чтения всех файлов
  TOPIC_MODEL.md       — тематические кластеры (TF-IDF)
  CITATION_INDEX.md    — индекс внешних URL
  VERSION_DIFF.md      — семантический diff последних коммитов
  GITHUB_ISSUES.md     — список задач для GitHub Issues
  DEPENDABOT.md        — статус зависимостей
  feed.rss / feed.atom — RSS/Atom фид изменений
  benchmark.json       — история замеров скриптов

scripts/
  improve_*.py           — 96 скриптов обработки документов (12 групп)
  utils_chunker.py       — утилиты чанкинга для больших текстов
  mcp_server.py          — MCP-сервер с 7 инструментами
  improve_run_all.py     — оркестратор (--smart, --fast, --group, --changed, --parallel)
  improve_autofill.py    — заполняет шаблоны из данных других скриптов
  improve_contact_status.py — CLI для обновления статуса контактов
  improve_llm_enrich.py  — Stage 3: LLM-обогащение проектных файлов
  improve_llm_summary.py — Stage 3: каскадная суммаризация → DIGEST.md
  improve_llm_qa.py      — Stage 3: Q&A по базе знаний (поиск + LLM)
  improve_llm_contact.py — Stage 3: персонализированные сообщения авторам
  improve_benchmark.py   — замер времени выполнения, история в benchmark.json
  improve_watch.py       — авто-запуск при изменении файлов (polling)

  # Quality/validation (группа quality)
  improve_spellcheck.py        — орфография (KNOWN_FIXES + pyspellchecker)
  improve_readability_v2.py    — индекс читаемости Флеш-Кинкейд для RU
  improve_content_gaps.py      — темы упомянутые, но без документа
  improve_link_preview.py      — статус внешних ссылок + title страниц

  # Export formats (группа export)
  improve_obsidian.py    — YAML frontmatter + [[wikilinks]] для Obsidian
  improve_epub.py        — EPUB через pandoc (apt install pandoc)
  improve_rss.py         — RSS/Atom фид из git log
  improve_confluence.py  — Confluence Wiki Markup

  # CI/CD (группа cicd)
  improve_github_issues.py — список задач → GitHub Issues (опц. gh CLI)
  improve_ci_config.py     — .github/workflows/docs.yml
  improve_pre_commit.py    — .pre-commit-config.yaml
  improve_dependabot.py    — мониторинг версий + .github/dependabot.yml

  # Analytics (группа analytics)
  improve_citation_index.py — индекс цитирования внешних URL
  improve_reading_time.py   — оценка времени чтения (200 сл/мин RU)
  improve_version_diff.py   — семантический diff между коммитами
  improve_topic_model.py    — TF-IDF кластеризация без ML-зависимостей

  # Работа с текстом (группа textwork)
  improve_reclassify.py      — TF-IDF рубрикация файлов по подпапкам
  improve_merge_by_topic.py  — слияние фрагментов одной темы в один файл
  improve_outline.py         — иерархический outline всей базы
  improve_compare_docs.py    — сравнение двух документов / batch по секции
  improve_subtopic_fill.py   — дополнение файлов-заглушек из базы знаний
  improve_crosslink_all.py   — обратные ссылки + related по ключевым словам
  improve_external_compare.py — сравнение с внешними URL/источниками
  improve_source_map.py      — карта происхождения текстов (git + frontmatter)
  improve_duplicate_across.py — поиск дублей между секциями/репозиториями

.claude/skills/
  analyze-project.md   — анализ проекта из docs/
  write-contact.md     — помощь в написании первого сообщения
  review-docs.md       — рецензия документа с правками
  improve.md           — универсальный навык улучшения любого элемента
```

## Ключевые проекты (из CONTACTS.md)

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| kksudo | AgentFS | knowledge/filesystem | 13 упоминаний |
| spbmolot | NGT Memory | memory | 12 упоминаний |
| VitalyOborin | Yodoca | memory | 7 упоминаний |
| AnastasiyaW | knowledge-space | knowledge | 11 упоминаний |
| andrey_chuyan | Svyazi | ingestion/CardIndex | 4 упоминания |

## Как работать

### Запустить все скрипты обработки
```bash
python scripts/improve_run_all.py --smart           # пропускает скрипты с хорошими метриками
python scripts/improve_run_all.py --fast            # пропускает медленные
python scripts/improve_run_all.py --group reports   # только отчёты
python scripts/improve_run_all.py --group quality   # проверка качества
python scripts/improve_run_all.py --group analytics # тематика + цитирование
python scripts/improve_run_all.py --group export    # экспорт форматов
python scripts/improve_run_all.py --group cicd      # CI/CD конфиги
python scripts/improve_run_all.py --group textwork  # работа с текстом
python scripts/improve_run_all.py --changed         # только группы для изменённых файлов
python scripts/improve_run_all.py --parallel 4      # параллельное выполнение групп
```

### Работа с контактами
```bash
python scripts/improve_contact_status.py --list              # сводная таблица
python scripts/improve_contact_status.py --author kksudo     # статус одного
python scripts/improve_contact_status.py --author kksudo --studied   # отметить
python scripts/improve_contact_status.py --author kksudo --messaged  # написали
python scripts/improve_contact_status.py --author kksudo --note "Ответил"
```

### LLM-обогащение (нужен ANTHROPIC_API_KEY)
```bash
pip install anthropic
python scripts/improve_llm_enrich.py --dry-run   # план и стоимость
python scripts/improve_llm_enrich.py --section 05-habr-projects  # ~$0.003
python scripts/improve_llm_qa.py --question "Что такое NGT Memory?"
python scripts/improve_llm_summary.py --file docs/05-habr-projects/memory/yodoca.md
```

### MCP-сервер (нужен pip install mcp)
```bash
python scripts/mcp_server.py   # stdio режим для Claude Desktop
```

### Заполнение шаблонов (бесплатно)
```bash
python scripts/improve_autofill.py --dry-run  # план
python scripts/improve_autofill.py            # создаёт docs/contacts/*.md
```

## Текущие приоритеты

1. **Написать авторам** — файлы готовы в `docs/contacts/`, нужно только отправить
2. **LLM-обогащение** — `improve_llm_enrich.py` обогатит 21 файл за ~$0.011
3. **Прототип** — начать с Yodoca + AgentFS + CardIndex (три слоя)

## Архитектурный принцип Svyazi 2.0

```
Скрипт (КАК) → Шаблон (ЧТО) → Скилл (КОГДА) → Плагин (ГДЕ)
```

Каждая ступень не заменяет предыдущую, а оркестрирует её.

### Новые инструменты качества
```bash
python scripts/improve_spellcheck.py              # орфография
python scripts/improve_spellcheck.py --fix        # авто-исправление
python scripts/improve_readability_v2.py          # читаемость (Flesch-Kincaid)
python scripts/improve_content_gaps.py --min-mentions 3  # пробелы в базе
python scripts/improve_link_preview.py            # статус ссылок (с кэшем)
```

### Экспорт
```bash
python scripts/improve_obsidian.py                # vault для Obsidian
python scripts/improve_epub.py --check            # проверить pandoc
python scripts/improve_epub.py --section 01-svyazi  # EPUB одной секции
python scripts/improve_rss.py                     # RSS + Atom фид
python scripts/improve_confluence.py              # Confluence Wiki
```

### Аналитика
```bash
python scripts/improve_topic_model.py --topics 8       # тематическое моделирование
python scripts/improve_citation_index.py               # индекс URL
python scripts/improve_reading_time.py                 # время чтения
python scripts/improve_version_diff.py --last 10       # diff за 10 коммитов
```

### Работа с текстом (рубрикация, слияние, анализ)
```bash
python scripts/improve_outline.py                          # оглавление всей базы
python scripts/improve_reclassify.py --section 02-anthropic-vacancies --dry-run
python scripts/improve_reclassify.py --section 02-anthropic-vacancies --apply
python scripts/improve_merge_by_topic.py --section 02-anthropic-vacancies --dry-run
python scripts/improve_merge_by_topic.py --section 02-anthropic-vacancies --apply
python scripts/improve_compare_docs.py --batch --section 05-habr-projects
python scripts/improve_compare_docs.py --a docs/file1.md --b docs/file2.md
python scripts/improve_subtopic_fill.py --apply --section 05-habr-projects
python scripts/improve_crosslink_all.py --apply --keywords
python scripts/improve_source_map.py --show-imported
python scripts/improve_duplicate_across.py --internal
python scripts/improve_external_compare.py --auto --section 05-habr-projects --limit 5
```

### CI/CD (одноразовая настройка)
```bash
python scripts/improve_ci_config.py               # .github/workflows/docs.yml
python scripts/improve_pre_commit.py --install    # pre-commit хуки
python scripts/improve_dependabot.py --generate-config  # dependabot.yml
python scripts/improve_github_issues.py           # список задач
```

## Важные предупреждения

- `search_index.json`: после запуска `improve_search_index.py` все записи имеют
  оба поля — `content` (полный текст 3000 симв.) и `preview` (500 симв.).
  Поиск в `improve_llm_qa.py` и `mcp_server.py` объединяет оба через `_doc_text()`.
- `improve_run_all.py --smart` пропускает только скрипты где метрика выше порога.
  Конфигурация в `SMART_CONDITIONS` — 6 скриптов с порогами 80-95%.
- LLM-скрипты (`improve_llm_*.py`) никогда не запускаются в `run_all` —
  только вручную. Требуют `ANTHROPIC_API_KEY`.
- post-commit хук в `.git/hooks/post-commit` автоматически обновляет PROGRESS.md
  после каждого коммита.
