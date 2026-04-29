# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 8 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 2 |
| **CardIndex** | `CardIndex` | `card-index` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 4 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 25 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 1 |
| **self-improvement** | `self-improvement` | `self-improve` | 70 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 3 |

**Всего несогласованных написаний: 121**


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

### `knowledgespace` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/OUTLINE.md`

### `card-index` → должно быть `CardIndex`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/QA.md`
- `docs/04-ai-collaborations/00-intro.md`

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/FAQ.md`
- _...и ещё 20_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/OUTLINE.md`

### `self-improve` → должно быть `self-improvement`

- `docs/FOOTNOTES.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/CONTENT_GAPS.md`
- `docs/TABLES.md`
- _...и ещё 65_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/QA.md`

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```

<!-- see-also -->

---

**Смотрите также:**
- [MISSING](docs/MISSING.md)
- [PRIORITIES](docs/PRIORITIES.md)
- [STATS](docs/STATS.md)
- [SPELLCHECK](docs/SPELLCHECK.md)

