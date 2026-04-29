# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 8 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 4 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 18 |
| **self-improvement** | `self-improvement` | `self-improve` | 63 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 1 |

**Всего несогласованных написаний: 100**


## Детали по файлам


### `knowledge space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/CONSISTENCY.md`
- `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- _...и ещё 3_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/QA.md`
- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/04-ai-collaborations/00-intro.md`

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/FAQ.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/TABLES.md`
- `docs/SITEMAP.md`
- `docs/COMPONENT_MATRIX.md`
- _...и ещё 13_

### `self-improve` → должно быть `self-improvement`

- `docs/CONTACTS.md`
- `docs/PARAGRAPH_QUALITY.md`
- `docs/LLM_SUMMARIES.md`
- `docs/NAMED_ENTITIES.md`
- `docs/TABLES.md`
- _...и ещё 58_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/TABLES.md`
- `docs/CONSISTENCY.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`

### `Evidence-Envelope` → должно быть `Evidence Envelope`

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
- [SPELLCHECK](docs/SPELLCHECK.md)
- [STATS](docs/STATS.md)

