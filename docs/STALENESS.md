# Отчёт об устаревших документах

<!-- toc-auto -->

> [!NOTE]
> Раздел `STALENESS` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-11_

---
<!-- tags: orchestration, anthropic, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-11_

Найдено проблем: **237** файлов

## Без метаданных (нет summary или тегов) — 232 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/ABBREVIATIONS.md` | 1368 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 9380 | нет summary, нет тегов |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 138 | нет summary, нет тегов |
| `docs/BACKLINKS.md` | 432 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 3639 | нет тегов |
| `docs/CLUSTERS.md` | 1669 | нет summary, нет тегов |
| `docs/CODE_BLOCKS.md` | 5044 | нет summary, нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/COMPLEXITY.md` | 343 | нет summary, нет тегов |
| `docs/CONCEPTS.md` | 16198 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 316 | нет summary, нет тегов |
| `docs/CONTENT_GAPS.md` | 674 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/CROSSREFS.md` | 502 | нет summary, нет тегов |
| `docs/DENSITY.md` | 336 | нет summary, нет тегов |
| `docs/DIGEST.md` | 198 | нет summary, нет тегов |
| `docs/ENTITIES.md` | 397 | нет summary, нет тегов |
| `docs/FOOTNOTES.md` | 204 | нет summary, нет тегов |
| `docs/GLOSSARY.md` | 158 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 5 файлов

| Файл | Слов |
|------|------|
| `docs/templates/contact-outreach.md` | 81 |
| `docs/templates/decision-record.md` | 53 |
| `docs/templates/ensemble.md` | 81 |
| `docs/templates/project-component.md` | 69 |
| `docs/templates/research-note.md` | 51 |

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
- [SPELLCHECK](SPELLCHECK.md)
- [TABLES](TABLES.md)

