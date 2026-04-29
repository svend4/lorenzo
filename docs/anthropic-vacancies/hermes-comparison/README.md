# hermes-comparison/ — сравнение собственной архитектуры с Hermes Agent

Hermes Agent — open-source автономный AI-агент от **Nous Research**, MIT лицензия, 95 600+ stars на GitHub к апрелю 2026. Самый быстрорастущий AI agent framework 2026 года.

Claude провёл честное и подробное сравнение Hermes с архитектурой DHLab (InGit + Cowork + Nautilus), и переоценил приоритеты на основе того, что Hermes уже покрывает.

| # | Раздел | Файл |
|---|---|---|
| — | Что такое Hermes Agent | [`00-question-what-is-hermes.md`](00-question-what-is-hermes.md) |
| 1 | Сходство 1: Composite Skills паттерн уже встроен | [`01-similarity-1-composite-skills.md`](01-similarity-1-composite-skills.md) |
| 2 | Сходство 2: Persistent memory — Layer B | [`02-similarity-2-persistent-memory.md`](02-similarity-2-persistent-memory.md) |
| 3 | Сходство 3: MCP support | [`03-similarity-3-mcp-support.md`](03-similarity-3-mcp-support.md) |
| 4 | Сходство 4: Multi-platform reach | [`04-similarity-4-multi-platform.md`](04-similarity-4-multi-platform.md) |
| 5 | Сходство 5: Self-hosting и privacy | [`05-similarity-5-self-hosting-privacy.md`](05-similarity-5-self-hosting-privacy.md) |
| 6 | Различие 1: Структурированная подложка отсутствует | [`06-difference-1-structured-substrate-missing.md`](06-difference-1-structured-substrate-missing.md) |
| 7 | Различие 2: Domain-specific specialization | [`07-difference-2-domain-specialization.md`](07-difference-2-domain-specialization.md) |
| 8 | Различие 3: Federated knowledge architecture | [`08-difference-3-federation-missing.md`](08-difference-3-federation-missing.md) |
| 9 | Различие 4: Institutional vision | [`09-difference-4-institutional-vision.md`](09-difference-4-institutional-vision.md) |
| 10 | Различие 5: Дрифт между tool capability и mission | [`10-difference-5-tool-vs-mission-drift.md`](10-difference-5-tool-vs-mission-drift.md) |
| 11 | Плюсы Hermes | [`11-pluses-of-hermes.md`](11-pluses-of-hermes.md) |
| 12 | Минусы Hermes | [`12-minuses-of-hermes.md`](12-minuses-of-hermes.md) |
| 13 | **Переприоритизация: что Hermes покрывает / не покрывает / synergy** | [`13-reprioritization.md`](13-reprioritization.md) |

## Ключевая мысль (раздел 13)

> Stop trying to build the agent layer. Hermes и Cowork (и multiple others coming) covered это. Focus на what's still missing: domain expertise, institutional architecture, federation.

### Низкий приоритет (Hermes/Cowork покрывает)
- Persistent memory infrastructure
- Multi-platform reach
- Skill creation framework
- Agent orchestration
- Computer use capability

### Высокий приоритет (Hermes/Cowork НЕ покрывает)
- SGB-specific MCP servers (Composite Skills sub-agents)
- Pattern Library architecture (Nautilus в Document 1)
- OKWF institutional design (Document 4)
- Representative Agent-specific governance (Document 5)
- Cross-practitioner federation (Portal Protocol)
- Audit infrastructure для regulated domains
