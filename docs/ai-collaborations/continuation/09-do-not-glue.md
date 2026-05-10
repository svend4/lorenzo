# Что пока не стоит склеивать в один релиз

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Auto AI Router, Tool Search, AutoResearch

---
<!-- tags: rag, security, self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

9. Что пока не стоит склеивать в один релиз

Есть пять соблазнов, которые лучше отложить.

Первый — сразу делать полный A2A‑mesh. A2A силён, но до стабилизации Card/Evidence/Memory contracts он добавит много распределённой сложности без гарантии качества. A2A нужен после того, как понятны роли агентов, типы задач и review states. A2A Protocol+1

Второй — сразу включать AutoResearch/self‑improvement. ACD и AutoResearch‑подобные подходы полезны только после появления метрик и regression set; иначе система будет “улучшать” то, что ещё не умеет измерять. ACD как направление показывает, что модели могут систематически генерировать задачи для выявления возможностей и слабостей, но именно это требует аккуратной функции качества. Habr

Третий — переносить inferred сразу в память как факт. Это главный путь к “структурным слухам”. Всё inferred должно жить как proposal до review.

Четвёртый — открывать внешние skills/MCP без quarantine. Prompt Worms и аудит OpenClaw показывают, что skill supply chain, persistent memory и external communications превращают агентную систему в поверхность заражения. Habr+1

Пятый — строить дорогой cloud‑first inference до бюджетного routing. Tool Search и Auto AI Router уже показывают, что сначала нужно срезать context overhead, ввести routing, sticky sessions, rate limits, failover и tracing; только потом масштабировать модели. Habr+1

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Что пока не стоит склеивать в один релиз"
```

## Смотрите также
- [10-architecture-rfc](10-architecture-rfc.md)
- [02-agentops-trace-envelope](02-agentops-trace-envelope.md)
- [05-roadmap-6-12-months](05-roadmap-6-12-months.md)
- 03-a2a-vs-[mcp-protocols](03-a2a-vs-mcp-protocols.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [10-architecture-rfc](10-architecture-rfc.md)
- [README](README.md)

