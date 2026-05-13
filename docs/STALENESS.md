# Отчёт об устаревших документах

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-13_
**Проекты:** Svyazi

---
<!-- tags: ingestion, local-first, anthropic, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-13_

Найдено проблем: **138** файлов

## Без метаданных (нет summary или тегов) — 104 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/QA.md` | 257 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 206 | нет summary, нет тегов |
| `docs/AUTHORS.md` | 132 | нет тегов |
| `docs/CHANGELOG.md` | 774 | нет summary, нет тегов |
| `docs/COMPLEXITY.md` | 384 | нет тегов |
| `docs/CONTACTS.md` | 316 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/CROSSREFS.md` | 522 | нет тегов |
| `docs/DIGEST.md` | 232 | нет summary, нет тегов |
| `docs/GLOSSARY.md` | 159 | нет тегов |
| `docs/LINKS.md` | 607 | нет тегов |
| `docs/MCP_DASHBOARD.md` | 21 | нет summary, нет тегов, короткий (21 слов) |
| `docs/PRIORITIES.md` | 1751 | нет тегов |
| `docs/PROGRESS.md` | 219 | нет summary, нет тегов |
| `docs/QA.md` | 2240 | нет summary, нет тегов |
| `docs/SCHEDULE.md` | 212 | нет summary, нет тегов |
| `docs/SCORING.md` | 211 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 34 файлов

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

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [TABLES](TABLES.md)
- [VERSION_DIFF](VERSION_DIFF.md)


<!-- see-also -->

---

**Смотрите также:**
- [COVERAGE](COVERAGE.md)
- [TAGS](TAGS.md)
- [STATS](STATS.md)
- [SPELLCHECK](SPELLCHECK.md)

