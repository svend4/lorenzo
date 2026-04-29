---
title: "Согласованность терминов"
tags:
  - general
date: 2026-04-29
---

# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 4 |
| **knowledge-space** | `knowledge-space` | `knowledge space` | 23 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 3 |
| **CardIndex** | `CardIndex` | `card-index` | 3 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 24 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 68 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 22 |
| **local-first** | `local-first` | `localfirst` | 3 |
| **self-improvement** | `self-improvement` | `self-improve` | 225 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 7 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 19 |
| **Card Envelope** | `Card Envelope` | `Card-Envelope` | 15 |

**Всего несогласованных написаний: 416**


## Детали по файлам


### `knowledgespace` → должно быть `knowledge-space`

- `docs/EMPTY_SECTIONS.md`
- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`

### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/OUTLINE.md`
- `docs/CONCEPTS.md`
- `docs/SITEMAP.md`
- _...и ещё 18_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`

### `card-index` → должно быть `CardIndex`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/LANGUAGE_STATS.md`
- `docs/EMPTY_SECTIONS.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- _...и ещё 19_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/LANGUAGE_STATS.md`
- `docs/EMPTY_SECTIONS.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- _...и ещё 63_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/LANGUAGE_STATS.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- `docs/PARAGRAPH_QUALITY.md`
- _...и ещё 17_

### `localfirst` → должно быть `local-first`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/OUTLINE.md`

### `self-improve` → должно быть `self-improvement`

- `docs/PASSIVE_VOICE.md`
- `docs/READING_LIST.md`
- `docs/LANGUAGE_STATS.md`
- `docs/FOOTNOTES.md`
- `docs/EMPTY_SECTIONS.md`
- _...и ещё 220_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`
- `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- _...и ещё 2_

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/READING_LIST.md`
- `docs/LANGUAGE_STATS.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- _...и ещё 14_

### `Card-Envelope` → должно быть `Card Envelope`

- `docs/LANGUAGE_STATS.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- `docs/PARAGRAPH_QUALITY.md`
- _...и ещё 10_

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```
