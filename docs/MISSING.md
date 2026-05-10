# Карта пробелов знаний

<!-- toc-auto -->
## Содержание

- Основной раздел


<!-- summary -->
> Карта пробелов знаний — документ базы знаний репозитория Lorenzo.

<!-- tags: docs, reference, lorenzo -->


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

Анализ покрытия ключевых тем и проектов в docs/.

| Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов |
|--------|---------------|--------|------|---------|----------------|
| ✅ | **Svyazi** | 621 | 752299 | ≥5ф/2000сл | `COLLAB_SUGGESTIONS.md`, `WORD_FREQ.md` |
| ✅ | **local-first** | 368 | 485482 | ≥2ф/300сл | `LANGUAGE_STATS.md`, `FOOTNOTES.md` |
| ✅ | **self-improvement** | 333 | 30607 | ≥1ф/100сл | `COLLAB_SUGGESTIONS.md`, `PASSIVE_VOICE.md` |
| ✅ | **Yodoca** | 324 | 571054 | ≥2ф/300сл | `COLLAB_SUGGESTIONS.md`, `WORD_FREQ.md` |
| ✅ | **CardIndex** | 298 | 532372 | ≥3ф/500сл | `COLLAB_SUGGESTIONS.md`, `SCHEDULE.md` |
| ✅ | **AgentFS** | 250 | 480303 | ≥3ф/500сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **knowledge-space** | 229 | 497863 | ≥3ф/500сл | `LANGUAGE_STATS.md`, `FOOTNOTES.md` |
| ✅ | **NGT Memory** | 210 | 146777 | ≥2ф/300сл | `COLLAB_SUGGESTIONS.md`, `GLOSSARY.md` |
| ✅ | **mclaude** | 201 | 420895 | ≥2ф/200сл | `COLLAB_SUGGESTIONS.md`, `LANGUAGE_STATS.md` |
| ✅ | **Rufler** | 190 | 430100 | ≥2ф/200сл | `LANGUAGE_STATS.md`, `FOOTNOTES.md` |
| ✅ | **LiteParse** | 178 | 418264 | ≥2ф/300сл | `LANGUAGE_STATS.md`, `BROKEN_LINKS.md` |
| ✅ | **SENTINEL** | 153 | 133270 | ≥2ф/200сл | `SCHEDULE.md`, `FOOTNOTES.md` |
| ✅ | **AI Factory** | 153 | 132705 | ≥2ф/200сл | `GLOSSARY.md`, `CONSISTENCY.md` |
| ✅ | **CRDT** | 137 | 415260 | ≥1ф/100сл | `LANGUAGE_STATS.md`, `FOOTNOTES.md` |
| ✅ | **AutoResearch** | 133 | 386930 | ≥1ф/100сл | `PASSIVE_VOICE.md`, `LANGUAGE_STATS.md` |
| ✅ | **Evidence Envelope** | 101 | 50583 | ≥2ф/200сл | `EMPTY_SECTIONS.md`, `CONSISTENCY.md` |
| ✅ | **Sozialrecht** | 87 | 421613 | ≥1ф/200сл | `LANGUAGE_STATS.md`, `EMPTY_SECTIONS.md` |
| ✅ | **Card Envelope** | 76 | 45237 | ≥2ф/200сл | `CONSISTENCY.md`, `PROTOTYPE_SPEC.md` |
| ✅ | **privacy by design** | 46 | 35626 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **Memory Write Policy** | 45 | 41111 | ≥2ф/200сл | `QUESTIONS.md`, `PROTOTYPE_SPEC.md` |
| ✅ | **Review Record** | 44 | 34462 | ≥1ф/100сл | `EMPTY_SECTIONS.md`, `PROTOTYPE_SPEC.md` |
| ✅ | **бюджетный роутинг** | 40 | 64901 | ≥2ф/300сл | `EMPTY_SECTIONS.md`, `RISK_REGISTER.md` |
| ✅ | **Skill Policy** | 29 | 9593 | ≥1ф/100сл | `TABLES.md`, `SUMMARIES.md` |
| ✅ | **лицензия BSL** | 6 | 3930 | ≥1ф/50сл | `RISK_REGISTER.md`, `TABLES.md` |
| ✅ | **voice ingestion** | 4 | 2280 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |

## Итог

- ✅ Хорошо раскрыто: **25**
- ⚠️ Слабо раскрыто: **0**
- ❌ Отсутствует: **0**

## Рекомендации

Темы со статусом ❌ или ⚠️ нужно дополнить отдельными документами.

<!-- see-also -->

---

**Смотрите также:**
- [CONSISTENCY](CONSISTENCY.md)
- [QA](svyazi-2-0/QA.md)
- [TAGS](TAGS.md)
- [CONTACT_PRIORITY](CONTACT_PRIORITY.md)



## Использование

```bash
python scripts/improve_run_all.py --group reports
```

```bash
python scripts/improve_semantic_search.py --query "MISSING"
```
