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

**Всего несогласованных написаний: 276**


## Детали по файлам


### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/obsidian/CONSISTENCY.md`
- `docs/obsidian/CONCEPTS.md`
- _...и ещё 10_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/04-ai-collaborations/QA.md`

### `knowledgespace` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/04-ai-collaborations/QA.md`
- `docs/05-habr-projects/QA.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/QA.md`
- `docs/TABLES.md`
- `docs/READING_TIME.md`
- `docs/CONSISTENCY.md`
- _...и ещё 13_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONTACTS.md`
- `docs/FAQ.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/DEPENDABOT.md`
- `docs/LANGUAGE_STATS.md`
- _...и ещё 34_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/SPELLCHECK.md`
- `docs/TABLES.md`
- `docs/SOURCE_MAP.md`
- `docs/READING_TIME.md`
- _...и ещё 10_

### `localfirst` → должно быть `local-first`

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

- `docs/PARAGRAPH_QUALITY.md`
- `docs/QA.md`
- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/READING_TIME.md`
- _...и ещё 13_

### `Card-Envelope` → должно быть `Card Envelope`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/TABLES.md`
- `docs/READING_TIME.md`
- `docs/OUTLINE.md`
- `docs/READABILITY.md`
- _...и ещё 6_

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```
