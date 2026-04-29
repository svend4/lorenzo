# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 16 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 3 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 3 |
| **CardIndex** | `CardIndex` | `card-index` | 3 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 6 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 54 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 5 |
| **self-improvement** | `self-improvement` | `self-improve` | 144 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 7 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 4 |

**Всего несогласованных написаний: 245**


## Детали по файлам


### `knowledge space` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/CONCEPTS.md`
- `docs/DUPLICATES.md`
- `docs/obsidian/CONSISTENCY.md`
- _...и ещё 11_

### `knowledge_space` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`

### `knowledgespace` → должно быть `knowledge-space`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`

### `card-index` → должно быть `CardIndex`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`

### `AI-Factory` → должно быть `AI Factory`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/QA.md`
- `docs/04-ai-collaborations/00-intro.md`
- `docs/obsidian/CONSISTENCY.md`
- _...и ещё 1_

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/TABLES.md`
- `docs/DEPENDABOT.md`
- `docs/PARAGRAPH_QUALITY.md`
- _...и ещё 49_

### `Auto-AI-Router` → должно быть `Auto AI Router`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/OUTLINE.md`
- `docs/obsidian/CONSISTENCY.md`
- `docs/obsidian/OUTLINE.md`

### `self-improve` → должно быть `self-improvement`

- `docs/FOOTNOTES.md`
- `docs/CONSISTENCY.md`
- `docs/READING_TIME.md`
- `docs/CONTENT_GAPS.md`
- `docs/TABLES.md`
- _...и ещё 139_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/obsidian/CONSISTENCY.md`
- `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- _...и ещё 2_

### `Evidence-Envelope` → должно быть `Evidence Envelope`

- `docs/CONSISTENCY.md`
- `docs/TABLES.md`
- `docs/QA.md`
- `docs/obsidian/CONSISTENCY.md`

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```

<!-- backlinks-auto -->
## Упоминается в

- [docs](README.md)
- [Все таблицы репозитория](TABLES.md)
- [Карта репозитория Lorenzo](SITEMAP.md)

<!-- related-auto -->
## Связанные документы

- [Приоритеты файлов](PRIORITIES.md) _25%_
- [Перекрёстные ссылки](CROSSREFS.md) _21%_
- [Граф связей проектов](GRAPH.md) _21%_
- [Нарратив проекта Lorenzo](NARRATIVE.md) _21%_
- [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md) _17%_
- [Матрица компонентов Svyazi 2.0](COMPONENT_MATRIX.md) _17%_
