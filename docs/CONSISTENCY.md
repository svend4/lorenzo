# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 8 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 3 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 3 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 5 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 17 |
| **self-improvement** | `self-improvement` | `self-improve` | 68 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 5 |

**Всего несогласованных написаний: 113**


## Детали по файлам


### `knowledge space` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- _...и ещё 3_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/04-ai-collaborations/QA.md`

### `knowledgespace` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/04-ai-collaborations/QA.md`
- `docs/05-habr-projects/QA.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/QA.md`
- `docs/04-ai-collaborations/00-intro.md`
- `docs/02-anthropic-vacancies/QA.md`

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/LANGUAGE_STATS.md`
- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/FAQ.md`
- _...и ещё 12_

### `self-improve` → должно быть `self-improvement`

- `docs/READING_LIST.md`
- `docs/LANGUAGE_STATS.md`
- `docs/FOOTNOTES.md`
- `docs/EMPTY_SECTIONS.md`
- `docs/CONSISTENCY.md`
- _...и ещё 63_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/QA.md`
- `docs/04-ai-collaborations/QA.md`
- `docs/03-technology-combinations/QA.md`
- `docs/02-anthropic-vacancies/QA.md`
- `docs/01-svyazi/QA.md`

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```
