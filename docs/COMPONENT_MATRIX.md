# Матрица компонентов Svyazi 2.0

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> - [Матрица возможностей](#матрица-возможностей)
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, AI Factory, Rufler, LiteParse, Yodoca

---

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Матрица возможностей](#матрица-возможностей)
- [Покрытие возможностей](#покрытие-возможностей)
- [Каталог компонентов](#каталог-компонентов)
- [Рекомендуемые ансамбли](#рекомендуемые-ансамбли)
- [Связанные документы](#связанные-документы)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, collaboration -->




<!-- toc-auto -->
## Contents

- [Матрица возможностей](#матрица-возможностей)
- [Покрытие возможностей](#покрытие-возможностей)
- [Каталог компонентов](#каталог-компонентов)
- [Рекомендуемые ансамбли](#рекомендуемые-ансамбли)


_Совместимость и возможности 14 компонентов экосистемы._

**Легенда:** ✅ Поддерживается · 🟡 Частично · ❌ Не поддерживается

## Матрица возможностей

| Компонент | Лицензия | Статус | Долгосро | Поиск/ин | MCP-совм | Граф зна | Безопасн | Оркестра | Веб-крау | Хранилищ | Документ | CRDT/syn |
|-----------|----------|--------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| **CardIndex** | 🟢 MIT | 🟢 stable | ✅ | ✅ | ✅ | 🟡 | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| **AgentFS** | 🟢 MIT | 🟢 stable | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ✅ | ✅ | 🟡 |
| **Yodoca** | 🟢 Apache 2.0 | 🔵 active | ✅ | ✅ | 🟡 | ❌ | 🟡 | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **NGT-memory** | 🟠 BSL 1.1 | 🔵 active | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **SENTINEL** | 🟢 MIT | 🔵 active | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Rufler** | ⚪ — | 🟡 experimental | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | 🟡 | ❌ |
| **knowledge-space** | 🟢 MIT | 🟢 stable | ✅ | ✅ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **Firecrawl** | 🟢 MIT | 🟢 stable | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Wikontic** | ⚪ — | ⚪ unknown | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Memnet** | ⚪ — | 🟡 experimental | ✅ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **agent-memory-mcp** | 🟢 MIT | 🟡 experimental | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **LiteParse** | ⚪ — | ⚪ unknown | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **AI Factory** | ⚪ — | ⚪ unknown | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **agent-pool** | ⚪ — | ⚪ unknown | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

## Покрытие возможностей

| Возможность | Полная поддержка | Частичная | Итого |
|-------------|-----------------|-----------|-------|
| Долгосрочная память | 6 | 1 | 7/14 |
| Поиск/индекс | 8 | 1 | 9/14 |
| MCP-совместим | 6 | 4 | 10/14 |
| Граф знаний | 2 | 2 | 4/14 |
| Безопасность/PII | 1 | 2 | 3/14 |
| Оркестрация | 3 | 0 | 3/14 |
| Веб-краулинг | 2 | 0 | 2/14 |
| Хранилище данных | 8 | 0 | 8/14 |
| Документированный API | 4 | 5 | 9/14 |
| CRDT/sync | 0 | 1 | 1/14 |

## Каталог компонентов

| Компонент | Лицензия | Статус | Репозиторий |
|-----------|----------|--------|-------------|
| **CardIndex** | 🟢 MIT | 🟢 stable | `kksudo/CardIndex` |
| **AgentFS** | 🟢 MIT | 🟢 stable | `kksudo/agentfs` |
| **Yodoca** | 🟢 Apache 2.0 | 🔵 active | `spbmolot/yodoca` |
| **NGT-memory** | 🟠 BSL 1.1 | 🔵 active | — |
| **SENTINEL** | 🟢 MIT | 🔵 active | — |
| **Rufler** | ⚪ — | 🟡 experimental | — |
| **knowledge-space** | 🟢 MIT | 🟢 stable | `kksudo/knowledge-space` |
| **Firecrawl** | 🟢 MIT | 🟢 stable | `mendableai/firecrawl` |
| **Wikontic** | ⚪ — | ⚪ unknown | — |
| **Memnet** | ⚪ — | 🟡 experimental | — |
| **agent-memory-mcp** | 🟢 MIT | 🟡 experimental | — |
| **LiteParse** | ⚪ — | ⚪ unknown | — |
| **AI Factory** | ⚪ — | ⚪ unknown | — |
| **agent-pool** | ⚪ — | ⚪ unknown | — |

## Рекомендуемые ансамбли

| Ансамбль | Компоненты | Ключевая функция |
|----------|-----------|-----------------|
| Knowledge OS | CardIndex + AgentFS + knowledge-space | Индекс знаний + AI FS |
| Memory Layer | Yodoca + NGT-memory + agent-memory-mcp | Долгосрочная память |
| Security Runtime | SENTINEL + AgentFS | PII-защита + MCP allowlist |
| Web Intelligence | Firecrawl + CardIndex + Yodoca | Краулинг → память |
| Agent Orchestra | Rufler + agent-pool + AI Factory | Оркестрация агентов |

<!-- related-auto -->
## Связанные документы

- [Нарратив проекта Lorenzo](NARRATIVE.md) _25%_
- [Приоритеты файлов](PRIORITIES.md) _25%_
- [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) _21%_
- [Карта плотности тем](DENSITY.md) _21%_
- [Граф связей проектов](GRAPH.md) _21%_
- [07 Mvp Planning](01-svyazi/07-mvp-planning.md) _17%_
- [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md) _17%_
- [Контактная стратегия и узкие вопросы для авторов](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) _17%_
## Связанные документы

- [07 Mvp Planning](01-svyazi/07-mvp-planning.md) _17%_
- [10 Second Order Ensembles](01-svyazi/10-second-order-ensembles.md) _17%_
- [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) _17%_
- [Новые ансамбли следующего шага](04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) _17%_
- [Сеть проектов и авторов](NETWORK.md) _17%_

<!-- see-also -->

---

**Смотрите также:**
- [ONBOARDING](ONBOARDING.md)
- [07-выводы](04-ai-collaborations/07-выводы.md)
- [PRIORITIES](PRIORITIES.md)
- [CONTACTS](CONTACTS.md)

<!-- backlinks-auto -->
## Упоминается в

- [Tech Radar — Svyazi 2.0](TECH_RADAR.md)
- [docs](README.md)
- [Все таблицы репозитория](TABLES.md)
- [Карта репозитория Lorenzo](SITEMAP.md)
- [Онбординг — Svyazi 2.0 / Lorenzo](ONBOARDING.md)
