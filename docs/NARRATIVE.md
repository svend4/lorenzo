# Нарратив проекта Lorenzo

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Глава 1: Исходная точка — Svyazi 2.0](#глава-1-исходная-точка-svyazi-20)
- [Глава 2: Экосистема проектов](#глава-2-экосистема-проектов)
- [Глава 3: Ансамбли — синергия компонентов](#глава-3-ансамбли-синергия-компонентов)
- [Глава 4: MVP — что строим первым](#глава-4-mvp-что-строим-первым)
- [Глава 5: Архитектурные пробелы](#глава-5-архитектурные-пробелы)
- [Глава 6: Контракты интеграции](#глава-6-контракты-интеграции)
- [Глава 7: Дорожная карта](#глава-7-дорожная-карта)
- [Глава 8: Команда и контакты](#глава-8-команда-и-контакты)
- [Глава 9: AI-коллаборации](#глава-9-ai-коллаборации)
- [Глава 10: Yodoca — память](#глава-10-yodoca-память)
- [Глава 11: NGT — граф памяти](#глава-11-ngt-граф-памяти)
- [Общая картина](#общая-картина)

---


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Нарратив проекта Lorenzo Contents - Глава 1: Исходная точка — Svyazi 2.0(глава-1-исходная-точка-svyazi-20) - Глава 2: Экосистема проектов(глава-2-экосистема-проектов) - Глава 3: Ан
> 🔧 **Подход:** Что у н Проекты: Svyazi, Yodoca --- Yodoca — «Научил ИИ-агента помнить важное и забывать лишнее в SQLite» URL Это не просто аналог, это архитектурное… → Читать полностью(docs/05-ha
> ✅ **Результат:** Svyazi хорошо закрывает ingest и нормализацию; AgentFS даёт .agentos и compile‑to‑runtime политику Проекты: Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler
> 🏷️ **Ключевые слова:** `глава`, `svyazi`, `memory`, `knowledge`, `summary`, `ingestion`, `проекты`, `читать`
>


<!-- toc-auto -->
## Contents

- [Глава 1: Исходная точка — Svyazi 2.0](#глава-1-исходная-точка-[svyazi](../docs/01-svyazi/00-intro-part2.md)-20)
- [Глава 2: Экосистема проектов](#глава-2-экосистема-проектов)
- [Глава 3: Ансамбли — синергия компонентов](#глава-3-ансамбли-синергия-компонентов)
- [Глава 4: MVP — что строим первым](#глава-4-mvp-что-строим-первым)
- [Глава 5: Архитектурные пробелы](#глава-5-архитектурные-пробелы)
- [Глава 6: Контракты интеграции](#глава-6-контракты-интеграции)
- [Глава 7: Дорожная карта](#глава-7-дорожная-карта)
- [Глава 8: Команда и контакты](#глава-8-команда-и-контакты)
- [Глава 9: AI-коллаборации](#глава-9-ai-коллаборации)
- [Глава 10: Yodoca — память](#глава-10-[yodoca](../docs/01-svyazi/01-executive-summary.md)-память)
- [Глава 11: NGT — граф памяти](#глава-11-[ngt](../docs/01-svyazi/01-executive-summary.md)-граф-памяти)
- [Общая картина](#общая-картина)


> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

_Связный рассказ о том, как складывается проект — от первых идей до конкретных планов._

---


## Глава 1: Исходная точка — Svyazi 2.0

> <!-- summary --> > Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: ingestion и нормализация профи **Проекты:** Svyazi, CardIndex, AgentFS, mclaude, AI Factory, Rufler, LiteParse, Legal RAG --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement,…

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/01-executive-summary.md)_

---


## Глава 2: Экосистема проектов

> <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration --> | Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые компоненты и паттерны | Лицензия | Maturity / статус | Релевантность к Svyazi‑2.0 | |---|---|---|---|---|---|---|---| | **Svyazi** | Андрей Чуян | Хабр citeturn41search0 | Гибридная система извлечения структурированных профилей…

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/03-component-catalog.md)_

---


## Глава 3: Ансамбли — синергия компонентов

> <!-- summary --> > Ниже — не все теоретически возможные комбинации, а **пять ансамблей с максимальным приростом свойств при минимальном интеграционном риске**. **Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, self-improvement, collaboration --> Ниже — не все теоретически возможные комбинации, а **пять ансамблей с максимальным приростом свойств…

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/04-ensembles-overview.md)_

---


## Глава 4: MVP — что строим первым

> <!-- summary --> > Наиболее рациональный прототип — **не собирать всё сразу**, а доказать одну центральную способность: *система находит и объясняет кандидатные коллаборации по свободным описаниям, документам и речевым **Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement, collaboration --> Наиболее рациональный прототип — **не собирать всё…

- **🛠️ MVP:** — **12–18 инженерных дней** для одного сильного разработчика или пары “backend + agent/operator”
- **🛠️ MVP:** и проверить один сценарий: **обнаружение и объяснение полезных коллабораций**

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/07-mvp-planning.md)_

---


## Глава 5: Архитектурные пробелы

> <!-- summary --> > После первичного обзора видно, что дефицит уже не в наличии компонентов, а в **стыках между ними**. Svyazi хорошо закрывает ingest и нормализацию; AgentFS даёт `.agentos` и compile‑to‑runtime политику **Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement --> После первичного обзора видно, что…

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/09-architectural-gaps.md)_

---


## Глава 6: Контракты интеграции

> <!-- summary --> > Чтобы все эти ансамбли не рассыпались, полезно зафиксировать **минимальный интерфейсный контракт** между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели **Проекты:** Svyazi, CardIndex, AgentFS, mclaude, AI Factory, LiteParse, Legal RAG, Hybrid RAG --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement --> Чтобы все эти…

- **🛠️ MVP:** без чрезмерной формализации
- **🛠️ MVP:** | На какие идеи опирается |

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/11-integration-contracts.md)_

---


## Глава 7: Дорожная карта

> <!-- summary --> > Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти **три короткие итерации**, каждая из которых поднимает один новый класс свойств. Первая итерация должна закрепить **Проекты:** Svyazi, mclaude, AI Factory, Yodoca, NGT Memory --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement --> Если идти дальше после…

- **🚀 Старт:** должна закрепить контракт и доказуемость
- **🎯 Цель:** | Минимум, который должен заработать | Оценка усилий | Главный риск |

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/12-roadmap.md)_

---


## Глава 8: Команда и контакты

> <!-- summary --> > С практической точки зрения следующие письма или комментарии лучше строить не вокруг общей фразы “давайте сделаем Svyazi‑2.0”, а вокруг **одного конкретного шва**, который автор уже хорошо понимает. У **Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Yodoca, NGT Memory --- <!-- tags: memory, rag, orchestration, knowledge, ingestion, architecture, self-improvement, collaboration --> С практической точки зрения следующие…

_[→ Читать полностью](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/13-contacts.md)_

---


## Глава 9: AI-коллаборации

> <!-- summary --> > https://habr.com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект по разработке программного обеспечени **Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, AI Factory, Rufler, LiteParse, Legal RAG --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration --> **[Запрос]** " Du hast…

- **🤝 Контакт:** ему в комменты с тегами на Чепурову и Романова (и со ссылкой на NGT Memory), описав идею объединения, может оказаться буквально тем самым «карточкой к
- **🎯 Цель:** «как мерить качество извлечённой структуры», над которой Чуян ещё думает
- **🎯 Цель:** проходит через планирование, реализацию, ревью, security review и уведомление в Telegram; AI Factory сканирует проект, определяет стек, ставит skills, настраивает MCP-серверы, создаёт

_[→ Читать полностью](docs/04-ai-collaborations/00-intro.md)_

---


## Глава 10: Yodoca — память

> <!-- summary --> > Yodoca — «Научил ИИ-агента помнить важное и забывать лишнее в SQLite» https://habr.com/ru/articles/1006622/ Это не просто аналог, это архитектурное продолжение Svyazi на уровне agentic memory. Что у н **Проекты:** Svyazi, Yodoca --- <!-- tags: memory, ingestion, architecture, collaboration --> Yodoca — «Научил ИИ-агента помнить важное и забывать лишнее в SQLite» https://habr.com/ru/articles/1006622/ Это не просто аналог, это архитектурное…

_[→ Читать полностью](docs/05-habr-projects/memory/yodoca.md)_

---


## Глава 11: NGT — граф памяти

> <!-- summary --> > ассоциативные связи в персистентной памяти LLM **Проекты:** Svyazi, NGT Memory --- <!-- tags: memory, ingestion, collaboration --> ассоциативные связи в персистентной памяти LLM Выявляя ассоциативные связи в персистентной памяти LLM Соберу ещё один пласт — авторские проекты с ярко выраженной идеей "обнаружения связей" между людьми/идеями через LLM. Excavated analogous projects and synthesized unified collaboration-discovery system Excavated…

- **🎯 Цель:** «как мерить качество извлечённой структуры», над которой Чуян ещё думает

_[→ Читать полностью](docs/05-habr-projects/memory/ngt-memory.md)_

---


## Общая картина

Lorenzo — это не один проект, а **экосистема взаимосвязанных компонентов**:

1. **Svyazi 2.0** — ядро, объединяющее 20+ OSS-проектов
2. **Ансамбли** — синергетические сборки для конкретных задач
3. **MVP** — минимально жизнеспособный прототип за 12-18 месяцев
4. **Команда** — распределённые авторы на Хабре и [GitHub](../docs/01-svyazi/03-component-catalog.md)
5. **Следующий шаг** — контакт с авторами ключевых компонентов

_Полная дорожная карта: [docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/12-roadmap.md](docs/01-svyazi/12-roadmap.md)_


<!-- see-also -->

---

**Смотрите также:**
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
- [07-mvp-planning](docs/01-[svyazi](../docs/01-svyazi/00-intro-part2.md)/07-mvp-planning.md)
- [01-executive-summary](docs/04-ai-collaborations/01-executive-summary.md)
- [13-контактная-стратегия-и-узкие-вопросы-для-авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [SIMILAR_PASSAGES](docs/SIMILAR_PASSAGES.md) (сходство 0.26)
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.20)
- [13-контактная-стратегия-и-узкие-вопросы-для-авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) (сходство 0.19)

