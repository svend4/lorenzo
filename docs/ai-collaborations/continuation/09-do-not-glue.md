# Что пока не стоит склеивать в один релиз

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Auto AI Router, Tool Search, AutoResearch

---
<!-- tags: rag, security, self-improvement, collaboration -->




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

**Смотрите также:**
- [10-architecture-rfc](docs/ai-collaborations/continuation/10-architecture-rfc.md)
- [02-agentops-trace-envelope](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md)
- [05-roadmap-6-12-months](docs/ai-collaborations/continuation/05-roadmap-6-12-months.md)
- [03-a2a-vs-mcp-protocols](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)

