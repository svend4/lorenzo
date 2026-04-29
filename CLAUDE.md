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
  search_index.json    — поисковый индекс (460 документов)

scripts/
  improve_*.py           — 71 скрипт обработки документов
  utils_chunker.py       — утилиты чанкинга для больших текстов
  mcp_server.py          — MCP-сервер с 7 инструментами
  improve_run_all.py     — оркестратор (--smart, --fast, --group, --changed)
  improve_autofill.py    — заполняет шаблоны из данных других скриптов
  improve_contact_status.py — CLI для обновления статуса контактов
  improve_llm_enrich.py  — Stage 3: LLM-обогащение проектных файлов
  improve_llm_summary.py — Stage 3: каскадная суммаризация → DIGEST.md
  improve_llm_qa.py      — Stage 3: Q&A по базе знаний (поиск + LLM)

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
python scripts/improve_run_all.py --smart       # пропускает скрипты с хорошими метриками
python scripts/improve_run_all.py --fast        # пропускает медленные
python scripts/improve_run_all.py --group reports  # только отчёты
python scripts/improve_run_all.py --changed     # только группы для изменённых файлов
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
