# operationalized/ — Lorenzo как «внуковая» комбинация

Анализ конкретной 6-узловой архитектуры pipeline, которая операционализирует концепт Lorenzo:

```
Habr Scout → Svyazi-like карточки → Collaboration Knowledge OS
   → Agent Team Kernel → Forensic RAG → Secure Agent Runtime
```

**Каждый из шести узлов — это существующий open-source проект**, не теоретический концепт. То есть Lorenzo как concept имеет almost ready-to-assemble building blocks.

| # | Файл | О чём |
|---|---|---|
| — | [`00-overview-grandchild-combination.md`](00-overview-grandchild-combination.md) | Обзор: что это за «внуковая» комбинация и как она ложится на Lorenzo |
| 1 | [`01-pluses-1-7.md`](01-pluses-1-7.md) | Плюсы 1–7: feasibility, self-reinforcing logic (flywheel), independent value, mission alignment, existing collaborators, pattern validation, Anastasia Бутова case |
| 2 | [`02-minuses-1-10.md`](02-minuses-1-10.md) | Минусы 1–10: integration сложность, component lifecycle risk, license compatibility, ambitious framing, competing platforms, Habr Scout limited scope, known limitations, complexity budget, real first project tension, tool vs impact |
| 3 | [`03-honest-opinion.md`](03-honest-opinion.md) | Что реально и что НЕ реально |
| 4 | [`04-recommendations.md`](04-recommendations.md) | Принять архитектуру как direction, не immediate plan |
| 5 | [`05-anchor-node-habr-scout.md`](05-anchor-node-habr-scout.md) | Habr Scout как anchor-узел для Phase 1 |
| 6 | [`06-conclusion-deserves-attention.md`](06-conclusion-deserves-attention.md) | Вывод |

## Маппинг узлов на проекты

| Узел pipeline | Проект |
|---|---|
| Habr Scout | Firecrawl + Playwright + Свяжи extraction |
| Svyazi-like карточки | Свяжи (Чуян) + knowledge-space (AnastasiyaW) |
| Collaboration Knowledge OS | AgentFS + Memory OS + knowledge-space |
| Agent Team Kernel | Rufler + agent-pool + mclaude (AnastasiyaW) |
| Forensic RAG | LiteParse + Hybrid RAG + Graph RAG |
| Secure Agent Runtime | SENTINEL + Shield + Claude permissions |

См. также:

- [`../README.md`](../README.md) — главный промпт Lorenzo.
- [`../../svyazi-2-0/ensembles/A-collaboration-os.md`](../../svyazi-2-0/ensembles/A-collaboration-os.md) — Collaboration OS из Svyazi 2.0.
- [`../../glossary/components-by-name.md`](../../glossary/components-by-name.md) — глоссарий упомянутых компонентов.
