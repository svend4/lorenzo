# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 3 |
| **knowledge-space** | `knowledge-space` | `knowledge space` | 16 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 22 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 40 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 19 |
| **local-first** | `local-first` | `localfirst` | 3 |
| **self-improvement** | `self-improvement` | `self-improve` | 156 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 18 |
| **Card Envelope** | `Card Envelope` | `Card-Envelope` | 15 |

**Всего несогласованных написаний: 298**


## Детали по файлам


### `knowledgespace` → должно быть `knowledge-space`

- `docs/EMPTY_SECTIONS.md`
- `docs/TABLES.md`
- `docs/CONSISTENCY.md`

### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/CONCEPTS.md`
- `docs/CONSISTENCY.md`
- `docs/OUTLINE.md`
- _...и ещё 11_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/QA.md`
- `docs/EMPTY_SECTIONS.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- _...и ещё 17_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONTACTS.md`
- `docs/FAQ.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/DEPENDABOT.md`
- `docs/EMPTY_SECTIONS.md`
- _...и ещё 35_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/SPELLCHECK.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- _...и ещё 14_

### `localfirst` → должно быть `local-first`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/OUTLINE.md`

### `self-improve` → должно быть `self-improvement`

- `docs/READING_LIST.md`
- `docs/CONTACTS.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/DIGEST_AUTO.md`
- `docs/LLM_SUMMARIES.md`
- _...и ещё 151_

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
- _...и ещё 13_

### `Card-Envelope` → должно быть `Card Envelope`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/LANGUAGE_STATS.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/VERSION_DIFF.md`
- _...и ещё 10_

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
- [LLM_SUMMARIES](docs/LLM_SUMMARIES.md)

