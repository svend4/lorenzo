# Отчёт об устаревших документах

<!-- toc-auto -->

> [!NOTE]
> Раздел `STALENESS` автоматически формируется из данных репозитория.

<!-- alert-added -->

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-11_
**Проекты:** Svyazi

---
<!-- tags: ingestion, anthropic, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-11_

Найдено проблем: **125** файлов

## Без метаданных (нет summary или тегов) — 100 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/autofilled/README.md` | 48 | нет summary, нет тегов, короткий (48 слов) |
| `docs/obsidian/QA.md` | 385 | нет summary, нет тегов |
| `docs/obsidian/SCORING.md` | 226 | нет summary |
| `docs/01-svyazi/QA.md` | 208 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 168 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 3042 | нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 314 | нет summary, нет тегов |
| `docs/COST.md` | 332 | нет summary, нет тегов |
| `docs/DIGEST.md` | 257 | нет summary, нет тегов |
| `docs/PROGRESS.md` | 219 | нет summary, нет тегов |
| `docs/QA.md` | 1999 | нет summary, нет тегов |
| `docs/READING_ORDER.md` | 4042 | нет summary, нет тегов |
| `docs/SCHEDULE.md` | 212 | нет summary, нет тегов |
| `docs/SCORING.md` | 198 | нет summary, нет тегов |
| `docs/SITEMAP.md` | 6630 | нет summary, нет тегов |
| `docs/STATS.md` | 355 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 25 файлов

| Файл | Слов |
|------|------|
| `docs/ALERTS.md` | 83 |
| `docs/MCP_DASHBOARD.md` | 97 |
| `docs/ai-collaborations/candidates/README.md` | 91 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` | 95 |
| `docs/habr-unique-projects/analogues/README.md` | 81 |
| `docs/habr-unique-projects/final-ensembles/README.md` | 92 |
| `docs/habr-unique-projects/software-pairs/README.md` | 97 |
| `docs/lorenzo-agent/naming/README.md` | 98 |
| `docs/meta-scripting/README.md` | 98 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/README.md` | 81 |
| `docs/nautilus/community-discussions/practical-observations/README.md` | 81 |
| `docs/nautilus/composite-skills-agents-companion-mentors/README.md` | 92 |
| `docs/nautilus/multi-tier-architecture/README.md` | 81 |
| `docs/nautilus/privacy-federation/README.md` | 99 |
| `docs/nautilus/supply-demand/README.md` | 81 |
| `docs/nautilus/transmission-box/README.md` | 81 |
| `docs/svyazi-2-0/limitations/README.md` | 85 |
| `docs/svyazi-2-0/outreach/README.md` | 88 |
| `docs/svyazi-2-0/overview/README.md` | 92 |
| `docs/svyazi-2-0/security/README.md` | 88 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```

<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [CONSISTENCY](CONSISTENCY.md)
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [SENTIMENT](SENTIMENT.md)
- [TABLES](TABLES.md)


<!-- see-also -->

---

**Смотрите также:**
- [TAGS](TAGS.md)
- [STATS](STATS.md)
- [COVERAGE](COVERAGE.md)
- [KNOWLEDGE_MAP](KNOWLEDGE_MAP.md)

