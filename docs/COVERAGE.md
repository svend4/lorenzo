# Матрица покрытия документов

<!-- toc-auto -->
## Contents

- [Сводка по секциям](#сводка-по-секциям)
- [Файлы с низким покрытием (< 3 признаков) — 3 файлов](#файлы-с-низким-покрытием-3-признаков-3-файлов)
- [Полное покрытие — 1 файлов](#полное-покрытие-1-файлов)
- [Рекомендуемые действия](#рекомендуемые-действия)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> Условные обозначения: ✅ есть  ⬜ отсутствует
**Проекты:** Svyazi, MemNet

---
<!-- tags: memory, ingestion, anthropic, collaboration -->




_Обновлено: 2026-05-10_

Условные обозначения: ✅ есть  ⬜ отсутствует

## Сводка по секциям

| Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks |
|--------|--------|---------|------|-----|-----------|--------|-----------|
| `01-svyazi` | 14 | 🟢 13/14 | 🟢 13/14 | 🔴 3/14 | 🟢 12/14 | 🔴 0/14 | 🔴 6/14 |
| `02-anthropic-vacancies` | 355 | 🟢 354/355 | 🟢 353/355 | 🟡 212/355 | 🟢 354/355 | 🔴 0/355 | 🟢 324/355 |
| `03-technology-combinations` | 5 | 🟢 5/5 | 🟢 5/5 | 🟡 3/5 | 🟢 5/5 | 🔴 0/5 | 🟢 5/5 |
| `04-ai-collaborations` | 15 | 🟢 15/15 | 🟢 15/15 | 🔴 2/15 | 🟢 15/15 | 🟢 15/15 | 🟡 10/15 |
| `05-habr-projects` | 6 | 🟢 6/6 | 🟢 6/6 | 🔴 1/6 | 🟢 6/6 | 🟢 6/6 | 🟢 6/6 |

## Файлы с низким покрытием (< 3 признаков) — 3 файлов

| Файл | Слов | Summary | Теги | TOC | CrossRefs | ## Статус | Backlinks |
|------|------| ---|---|---|---|---|--- |
| `docs/01-svyazi/00-intro-part2.md` | 5 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 178 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |

## Полное покрытие — 1 файлов

- ✅ `docs/05-habr-projects/memory/memnet.md`

## Рекомендуемые действия

```bash
# Добавить summary и теги (быстро, $0)
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Добавить перекрёстные ссылки
python scripts/improve_crossrefs.py
python scripts/improve_backlinks.py

# Заполнить блок ## Статус в проектных файлах
python scripts/improve_autofill.py
```

<!-- see-also -->

---

**Смотрите также:**
- [TAGS](TAGS.md)
- [CONCEPT_GRAPH](CONCEPT_GRAPH.md)
- [28-appendix-a-minimal-working-example](02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)
- [LLM_SUMMARIES](LLM_SUMMARIES.md)

