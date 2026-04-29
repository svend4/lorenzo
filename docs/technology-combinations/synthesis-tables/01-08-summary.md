# Сводная таблица 1–8

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude`, секция 📊 «Сводная таблица синергии».
**Проекты:** Svyazi, CardIndex, Yodoca

---
<!-- tags: memory, rag, orchestration, knowledge, ingestion, local-first, architecture, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude`, секция 📊 «Сводная таблица синергии».

| Комбинация | Кубики | Уникальный результат | Экономия/ROI |
|---|---|---|---|
| [1](../combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md) | Агентская архитектура + Svyazi | Самообучающиеся промпты, multi‑domain профилирование | 70% времени на модерацию |
| [2](../combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md) | Мультиагенты + Router | Иерархический роутинг, fault tolerance | 80% бюджета на LLM |
| [3](../combinations/03-crdt-local-first-svyazi-cardindex.md) | CRDT + Svyazi | P2P граф сообщества, offline‑first discovery | Нулевые расходы на сервер |
| [4](../combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md) | LLM‑парсинг + Graph‑RAG + Агенты | Self‑building knowledge graph | 95% точность vs 60% обычного RAG |
| [5](../combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md) | SourceCraft + Claude Code + Sequential | Distributed code review, team knowledge graph | 44% выше качества vs координатор |
| [6](../combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md) | OpenClaude + ZINC + MoME | Локальный агент с Q6‑роутером | 100% privacy, $0/мес API |
| [7](../combinations/07-crawl4ai-docling-yodoca-consolidator.md) | Crawl4AI + Docling + Yodoca | Self‑consolidating legal corpus | Автоматическая актуализация |
| [8](../combinations/08-conductor-adversarial-review-auto-ai-router.md) | Conductor + adversarial + Router | Multi‑model adversarial, enterprise review | 3× ускорение ревью |

## 🎯 Главная находка: паттерн «скромные родители → мощные дети»

Ни один из этих проектов по отдельности не революционен:

- Svyazi — локальная система одного автора
- CRDT — академическая технология 2010‑х
- Yodoca — pet‑project с консолидацией
- Router — 200 строк Go‑кода

Но вместе они дают:

- P2P граф знаний с автообучением (Svyazi + CRDT + Yodoca + агенты)
- Distributed legal AI на домашнем железе (OpenClaude + ZINC + Q6 + Graph‑RAG)
- Enterprise multi‑model pipeline (Conductor + adversarial + Router + Sequential)

Каждая комбинация решает проблему, которую ни один SaaS не решает целиком, потому что SaaS‑провайдеры не комбинируют технологии через границы продуктов.

## Рекомендация

Для legal + AI/ML research стека прямо ложатся комбинации 1, 3, 4, 6, 7. Лучший первый проект — **Комбинация 4** (LLM‑парсинг + Graph‑RAG + Агенты) — закрывает сразу три боли: парсинг Bescheid, построение прецедентного графа, автоматическая актуализация корпуса. Все компоненты уже есть на Хабре с working code.

<!-- see-also -->

---

**Смотрите также:**
- [08-conductor-adversarial-review-auto-ai-router](docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md)
- [05-benchmarks](docs/03-technology-combinations/05-benchmarks.md)
- [01-legal-ai-stack](docs/technology-combinations/mega-stacks/01-legal-ai-stack.md)
- [15-19-extended](docs/technology-combinations/synthesis-tables/15-19-extended.md)

