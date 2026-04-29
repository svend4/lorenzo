# Согласованность терминов

Анализ различных написаний одних и тех же терминов.

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **knowledge-space** | `knowledge-space` | `knowledge space` | 6 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 1 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 5 |
| **self-improvement** | `self-improvement` | `self-improve` | 48 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |

**Всего несогласованных написаний: 66**


## Детали по файлам


### `knowledge_space` → должно быть `knowledge-space`

- `docs/GRAPH.md`
- `docs/MINDMAP.md`

### `knowledge space` → должно быть `knowledge-space`

- `docs/MINDMAP.md`
- `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`
- `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md`
- _...и ещё 1_

### `AI-Factory` → должно быть `AI Factory`

- `docs/04-ai-collaborations/00-intro.md`

### `NGT-Memory` → должно быть `NGT Memory`

- `docs/SEARCH.md`
- `docs/PRIORITIES.md`
- `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
- `docs/05-habr-projects/memory/README.md`
- `docs/01-svyazi/03-component-catalog.md`

### `self-improve` → должно быть `self-improvement`

- `docs/TAGS.md`
- `docs/MISSING.md`
- `docs/MINDMAP.md`
- `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
- `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
- _...и ещё 43_

### `Svyazi-2.0` → должно быть `Svyazi 2.0`

- `docs/04-ai-collaborations/04-приоритетные-ансамбли.md`
- `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
- `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md`
- `docs/01-svyazi/04-ensembles-overview.md`

## Как исправить

```bash
# Пример: заменить все вхождения в docs/
find docs/ -name '*.md' -exec sed -i 's/old_term/new_term/g' {} +
```

<!-- similar-docs -->

---

**Похожие документы:**
- [PRIORITIES](docs/PRIORITIES.md) (сходство 0.24)
- [MISSING](docs/MISSING.md) (сходство 0.16)
- [TAGS](docs/TAGS.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [PRIORITIES](docs/PRIORITIES.md)
- [MISSING](docs/MISSING.md)
- [DENSITY](docs/DENSITY.md)
- [GLOSSARY](docs/GLOSSARY.md)

