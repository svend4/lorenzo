# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 15 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 3 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 3 |
| **CardIndex** | `CardIndex` | `card-index` | 3 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 6 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 54 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 5 |
| **self-improvement** | `self-improvement` | `self-improve` | 145 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 7 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 4 |

**Всего несогласованных написаний: 291**


## Детали по файлам


### `knowledgespace` → должно быть `knowledge-space`

- `docs/EMPTY_SECTIONS.md`
- `docs/TABLES.md`
- `docs/CONSISTENCY.md`

### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/CONCEPTS.md`
- `docs/obsidian/CONSISTENCY.md`
- `docs/obsidian/CONCEPTS.md`
- _...и ещё 10_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/QA.md`
- `docs/EMPTY_SECTIONS.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- _...и ещё 16_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONTACTS.md`
- `docs/FAQ.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/DEPENDABOT.md`
- `docs/EMPTY_SECTIONS.md`
- _...и ещё 33_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/SPELLCHECK.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- _...и ещё 13_

### `localfirst` → должно быть `local-first`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/OUTLINE.md`

### `self-improve` → должно быть `self-improvement`

- `docs/FOOTNOTES.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/CONTENT_GAPS.md`
- `docs/TABLES.md`
- _...и ещё 140_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/READING_LIST.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/QA.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- _...и ещё 12_

### `Card-Envelope` → должно быть `Card Envelope`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/READING_TIME.md`
- _...и ещё 9_

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```
