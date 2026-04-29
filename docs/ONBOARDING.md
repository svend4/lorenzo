# Онбординг — Svyazi 2.0 / Lorenzo

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> _Руководство для новых участников проекта._
**Проекты:** Svyazi, CardIndex, AgentFS, Rufler, Yodoca, SENTINEL, Firecrawl

---
<!-- tags: memory, orchestration, security, knowledge, ingestion, architecture, roadmap, anthropic, collaboration -->




_Руководство для новых участников проекта._

## Что это такое?

**Svyazi 2.0** — экосистема из 20+ взаимосвязанных OSS-проектов для построения AI-систем с долгосрочной памятью, оркестрацией агентов и безопасной обработкой данных.

Статус готовности: **96% 🟢 GO** (документация и архитектура).

## Первые 30 минут

```bash
# 1. Клонировать репозиторий
git clone <repo-url> && cd lorenzo

# 2. Прочитать Executive Summary
cat docs/01-svyazi/01-executive-summary.md

# 3. Посмотреть статус проекта
cat docs/SCORING.md

# 4. Прочитать FAQ
cat docs/FAQ.md

# 5. Запустить скрипты (генерация/обновление docs)
pip install beautifulsoup4 lxml
python scripts/improve_run_all.py --fast
```

## Структура документации

_Всего: 407 файлов, 306,267 слов_

| Раздел | Тема | Файлов | Слов |
|--------|------|--------|------|
| [`docs/01-svyazi/`](docs/01-svyazi/README.md) | Архитектура Svyazi 2.0 | 16 | 10,166 |
| [`docs/02-anthropic-vacancies/`](docs/02-anthropic-vacancies/README.md) | Вакансии Anthropic | 357 | 260,851 |
| [`docs/03-technology-combinations/`](docs/03-technology-combinations/README.md) | Комбинации технологий | 7 | 2,433 |
| [`docs/04-ai-collaborations/`](docs/04-ai-collaborations/README.md) | AI-коллаборации | 17 | 24,521 |
| [`docs/05-habr-projects/`](docs/05-habr-projects/README.md) | Хабр-проекты | 10 | 8,296 |

## Ключевые документы

| Документ | Зачем читать |
|----------|-------------|
| `docs/01-svyazi/01-executive-summary.md` | Общий обзор проекта — начни здесь |
| `docs/01-svyazi/07-mvp-planning.md` | MVP план, риски, оценки времени |
| `docs/01-svyazi/12-roadmap.md` | Дорожная карта по кварталам |
| `docs/01-svyazi/11-integration-contracts.md` | API-контракты между компонентами |
| `docs/CONTACTS.md` | Авторы компонентов и шаблоны писем |
| `docs/FAQ.md` | 54 вопроса и ответа |
| `docs/TECH_RADAR.md` | Что использовать, что избегать |
| `CLAUDE.md` | Гид по репо для Claude Code |

## Скрипты автоматизации

В репо 75 скриптов `improve_*.py` для автоматического обновления документации.

```bash
# Все скрипты быстро
python scripts/improve_run_all.py --fast

# Конкретная группа
python scripts/improve_run_all.py --group analysis
# Группы: structure, index, analysis, extract, quality, graph, reports, export

# LLM-обогащение (нужен API ключ)
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/improve_run_all.py --group enrich

# Автономный вотчер (следит за изменениями)
python scripts/improve_watcher.py
```

## Архитектура компонентов

| Компонент | Роль | Лицензия | Автор |
|-----------|------|---------|-------|
| **CardIndex** | Индекс знаний (785+ карточек) | MIT | kksudo |
| **AgentFS** | Файловая система для AI | MIT | kksudo |
| **Yodoca** | Память с консолидацией | Apache 2.0 | spbmolot |
| **NGT-memory** | Ассоциативный граф памяти | BSL 1.1 | — |
| **SENTINEL** | Безопасность, allowlist MCP | MIT | — |
| **Rufler** | Оркестратор агентов | — | — |
| **Firecrawl** | Веб-краулер для AI | MIT | — |

## Как внести вклад

1. **Документация:** редактируй файлы в `docs/`, запусти `improve_run_all.py`
2. **Скрипты:** добавь `scripts/improve_*.py`, добавь в группу в `improve_run_all.py`
3. **Контакты:** авторы компонентов в `docs/CONTACTS.md`, шаблон в `docs/templates/contact-outreach.md`
4. **Архитектура:** новые ADR в `docs/01-svyazi/` по шаблону `docs/templates/adr-template.md`

## Контакты

- Контакты авторов компонентов: `docs/CONTACTS.md`
- Шаблон письма для коллаборации: `docs/templates/contact-outreach.md`
- Автор репозитория: `svend4` (GitHub)

---

_Этот документ генерируется скриптом `improve_onboarding.py`._
_Для AI-ассистента: читай `CLAUDE.md` для понимания структуры репо._


<!-- see-also -->

---

**Смотрите также:**
- [INDEX](docs/INDEX.md)
- [PRIORITIES](docs/PRIORITIES.md)
- [PROGRESS](docs/PROGRESS.md)
- [TECH_RADAR](docs/TECH_RADAR.md)

