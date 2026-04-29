# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 16 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 18 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 38 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 17 |
| **local-first** | `local-first` | `localfirst` | 1 |
| **self-improvement** | `self-improvement` | `self-improve` | 142 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 15 |
| **Card Envelope** | `Card Envelope` | `Card-Envelope` | 13 |

**Всего несогласованных написаний: 266**


## Детали по файлам


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
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/READING_TIME.md`
- _...и ещё 13_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONTACTS.md`
- `docs/FAQ.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/DEPENDABOT.md`
- `docs/TABLES.md`
- _...и ещё 33_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/SPELLCHECK.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/SOURCE_MAP.md`
- _...и ещё 12_

### `localfirst` → должно быть `local-first`

- `docs/OUTLINE.md`

### `self-improve` → должно быть `self-improvement`

- `docs/CONTACTS.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/LLM_SUMMARIES.md`
- `docs/SPELLCHECK.md`
- `docs/NAMED_ENTITIES.md`
- _...и ещё 137_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/QA.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/CONCEPTS.md`
- _...и ещё 10_

### `Card-Envelope` → должно быть `Card Envelope`

- `docs/PARAGRAPH_QUALITY.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/READING_TIME.md`
- `docs/CONSISTENCY.md`
- _...и ещё 8_

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```

<!-- see-also -->

---

**Смотрите также:**
- [TAGS](docs/TAGS.md)
- [MISSING](docs/MISSING.md)
- [STATS](docs/STATS.md)
- [GLOSSARY](docs/GLOSSARY.md)

