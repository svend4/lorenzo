# Отчёт об устаревших документах

<!-- toc-auto -->

> [!NOTE]
> Раздел `STALENESS` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: staleness, docs -->


<!-- summary -->
> `STALENESS` — раздел документации проекта Lorenzo.


_Порог: 30 дней. Обновлено: 2026-05-13_

Найдено проблем: **135** файлов

## Без метаданных (нет summary или тегов) — 94 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/MCP_DASHBOARD.md` | 21 | нет summary, нет тегов, короткий (21 слов) |
| `docs/autofilled/README.md` | 66 | нет summary, нет тегов, короткий (66 слов) |
| `docs/autofilled/components/README.md` | 96 | нет summary, нет тегов, короткий (96 слов) |
| `docs/badges/README.md` | 69 | нет summary, нет тегов, короткий (69 слов) |
| `docs/01-svyazi/QA.md` | 257 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 206 | нет summary, нет тегов |
| `docs/ABBREVIATIONS.md` | 1306 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 8984 | нет summary, нет тегов |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 129 | нет тегов |
| `docs/BACKLINKS.md` | 423 | нет тегов |
| `docs/CHANGELOG.md` | 821 | нет summary, нет тегов |
| `docs/CODE_BLOCKS.md` | 5051 | нет summary, нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/COMPLEXITY.md` | 350 | нет тегов |
| `docs/CONCEPTS.md` | 16170 | нет summary, нет тегов |
| `docs/CONSISTENCY.md` | 525 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 41 файлов

| Файл | Слов |
|------|------|
| `docs/ai-collaborations/candidates/README.md` | 98 |
| `docs/glossary/README.md` | 88 |
| `docs/habr-unique-projects/analogues/README.md` | 91 |
| `docs/habr-unique-projects/final-ensembles/README.md` | 99 |
| `docs/lorenzo-agent/scenarios/README.md` | 88 |
| `docs/nautilus/community-discussions/agent-changes-reality/README.md` | 98 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/README.md` | 88 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/README.md` | 91 |
| `docs/nautilus/community-discussions/practical-observations/README.md` | 91 |
| `docs/nautilus/community-discussions/voiceless-contributors/README.md` | 88 |
| `docs/nautilus/composite-skills-agents-companion-mentors/README.md` | 99 |
| `docs/nautilus/innovation-transitions/README.md` | 95 |
| `docs/nautilus/multi-tier-architecture/README.md` | 91 |
| `docs/nautilus/supply-demand/README.md` | 91 |
| `docs/nautilus/transmission-box/README.md` | 91 |
| `docs/svyazi-2-0/limitations/README.md` | 95 |
| `docs/svyazi-2-0/outreach/README.md` | 98 |
| `docs/svyazi-2-0/prototype/README.md` | 88 |
| `docs/svyazi-2-0/security/README.md` | 98 |
| `docs/technology-combinations/research-reports/README.md` | 91 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```

## Смотрите также
- [Главная](README.md)
- [Метрики](METRICS.md)
- [Здоровье](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Сущности](ENTITIES.md)

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [TABLES](TABLES.md)

