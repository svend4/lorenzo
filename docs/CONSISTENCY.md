# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 14 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 8 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 32 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 7 |
| **self-improvement** | `self-improvement` | `self-improve` | 140 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 8 |
| **Card Envelope** | `Card Envelope` | `Card-Envelope` | 6 |

**Всего несогласованных написаний: 221**


## Детали по файлам


### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/CONSISTENCY.md`
- `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- _...и ещё 9_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/QA.md`
- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/04-ai-collaborations/00-intro.md`
- `docs/glossary/components-by-name.md`
- _...и ещё 3_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONTACTS.md`
- `docs/FAQ.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/DEPENDABOT.md`
- `docs/TABLES.md`
- _...и ещё 27_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/OUTLINE.md`
- `docs/glossary/components-by-name.md`
- `docs/glossary/concepts.md`
- _...и ещё 2_

### `self-improve` → должно быть `self-improvement`

- `docs/CONTACTS.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/LLM_SUMMARIES.md`
- `docs/SPELLCHECK.md`
- `docs/NAMED_ENTITIES.md`
- _...и ещё 135_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/QA.md`
- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/CONSISTENCY.md`
- `docs/PRIORITIES.md`
- _...и ещё 3_

### `Card-Envelope` → должно быть `Card Envelope`

- `docs/TABLES.md`
- `docs/PRIORITIES.md`
- `docs/glossary/components-by-name.md`
- `docs/glossary/concepts.md`
- `docs/svyazi-2-0/architecture/README.md`
- _...и ещё 1_

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```

<!-- see-also -->

---

**Смотрите также:**
- [MISSING](docs/MISSING.md)
- [TAGS](docs/TAGS.md)
- [STATS](docs/STATS.md)
- [SPELLCHECK](docs/SPELLCHECK.md)

