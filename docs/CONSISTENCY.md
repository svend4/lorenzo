# Согласованность терминов

<!-- summary -->
> Анализ различных написаний одних и тех же терминов.
**Проекты:** Svyazi, knowledge-space, AI Factory, NGT Memory, Auto AI Router

---
<!-- tags: memory, rag, orchestration, knowledge, ingestion, local-first, architecture, anthropic, self-improve, collaboration -->




Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 15 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 3 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 4 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 18 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 39 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 15 |
| **local-first** | `local-first` | `localfirst` | 1 |
| **self-improvement** | `self-improvement` | `self-improve` | 148 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 18 |
| **Card Envelope** | `Card Envelope` | `Card-Envelope` | 11 |

**Всего несогласованных написаний: 276**


## Детали по файлам


### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/CONSISTENCY.md`
- `docs/OUTLINE.md`
- `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`
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

- `docs/READING_LIST.md`
- `docs/CONTACTS.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/LLM_SUMMARIES.md`
- `docs/SPELLCHECK.md`
- _...и ещё 143_

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

<!-- see-also -->

---

**Смотрите также:**
- [MISSING](docs/MISSING.md)
- [TAGS](docs/TAGS.md)
- [STATS](docs/STATS.md)
- [SPELLCHECK](docs/SPELLCHECK.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [CONSISTENCY](docs/obsidian/CONSISTENCY.md) (сходство 0.65)
- [TAGS](docs/TAGS.md) (сходство 0.24)
- [PRIORITIES](docs/obsidian/PRIORITIES.md) (сходство 0.20)

