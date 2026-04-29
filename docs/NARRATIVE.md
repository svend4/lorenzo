# Нарратив проекта Lorenzo

_Связный рассказ о том, как складывается проект — от первых идей до конкретных планов._

---


## Глава 1: Исходная точка — Svyazi 2.0

> > [!IMPORTANT] > Главный документ проекта. Начните чтение отсюда. <!-- alert-added --> <!-- summary --> > Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: ingestion и нормализация профи **Проекты:** Svyazi, CardIndex[^cardindex], AgentFS[^agentfs], mclaude, AI Factory, Rufler[^rufler], LiteParse, Legal RAG[^rag] ---…

_[→ Читать полностью](docs/01-svyazi/01-executive-summary.md)_

---


## Глава 2: Экосистема проектов

> <!-- summary --> > <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration --> **Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration --> | Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые…

_[→ Читать полностью](docs/01-svyazi/03-component-catalog.md)_

---


## Глава 3: Ансамбли — синергия компонентов

> <!-- summary --> > Ниже — не все теоретически возможные комбинации, а **пять ансамблей с максимальным приростом свойств при минимальном интеграционном риске**. **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], knowledge-space[^knowledge-space], mclaude, AI Factory, Rufler[^rufler], LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, self-improvement, collaboration --> Ниже — не все теоретически возможные комбинации, а **пять ансамблей с максимальным приростом свойств…

_[→ Читать полностью](docs/01-svyazi/04-ensembles-overview.md)_

---


## Глава 4: MVP — что строим первым

> <!-- summary --> > Наиболее рациональный прототип — **не собирать всё сразу**, а доказать одну центральную способность: *система находит и объясняет кандидатные коллаборации по свободным описаниям, документам и речевым **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], knowledge-space[^knowledge-space], mclaude, AI Factory, Rufler[^rufler], LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement, collaboration --> Наиболее рациональный прототип — **не собирать всё…

- **🛠️ MVP:** — **12–18 инженерных дней** для одного сильного разработчика или пары “backend + agent/operator”
- **🛠️ MVP:** и проверить один сценарий: **обнаружение и объяснение полезных коллабораций**

_[→ Читать полностью](docs/01-svyazi/07-mvp-planning.md)_

---


## Глава 5: Архитектурные пробелы

> <!-- summary --> > После первичного обзора видно, что дефицит уже не в наличии компонентов, а в **стыках между ними**. Svyazi[^svyazi] хорошо закрывает ingest и нормализацию; AgentFS[^agentfs] даёт `.agentos` и compile‑to‑runtime политику **Проекты:** Svyazi, CardIndex[^cardindex], AgentFS, knowledge-space[^knowledge-space], mclaude, AI Factory, Rufler[^rufler], LiteParse --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement --> После первичного обзора видно, что…

_[→ Читать полностью](docs/01-svyazi/09-architectural-gaps.md)_

---


## Глава 6: Контракты интеграции

> <!-- summary --> > Чтобы все эти ансамбли не рассыпались, полезно зафиксировать **минимальный интерфейсный контракт** между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], mclaude, AI Factory, LiteParse, Legal RAG[^rag], Hybrid RAG --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement --> Чтобы все эти…

- **🛠️ MVP:** без чрезмерной формализации
- **🛠️ MVP:** | На какие идеи опирается |

_[→ Читать полностью](docs/01-svyazi/11-integration-contracts.md)_

---


## Глава 7: Дорожная карта

> <!-- summary --> > Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти **три короткие итерации**, каждая из которых поднимает один новый класс свойств. Первая итерация должна закрепить **Проекты:** Svyazi[^svyazi], mclaude, AI Factory, Yodoca[^yodoca], NGT[^ngt] Memory --- <!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement --> Если идти дальше после…

- **🚀 Старт:** должна закрепить контракт и доказуемость
- **🎯 Цель:** | Минимум, который должен заработать | Оценка усилий | Главный риск |

_[→ Читать полностью](docs/01-svyazi/12-roadmap.md)_

---


## Глава 8: Команда и контакты

> <!-- summary --> > С практической точки зрения следующие письма или комментарии лучше строить не вокруг общей фразы “давайте сделаем Svyazi[^svyazi]‑2.0”, а вокруг **одного конкретного шва**, который автор уже хорошо понимает. У **Проекты:** Svyazi, CardIndex[^cardindex], AgentFS[^agentfs], knowledge-space[^knowledge-space], mclaude, AI Factory, Yodoca[^yodoca], NGT[^ngt] Memory --- <!-- tags: memory, rag, orchestration, knowledge, ingestion, architecture, self-improvement, collaboration --> С практической точки зрения следующие…

_[→ Читать полностью](docs/01-svyazi/13-contacts.md)_

---


## Глава 9: AI-коллаборации

> <!-- autofill-status --> | Параметр | Значение | |----------|---------| | Теги | — | | Упоминаний в репо | — | | Слой | — | | Контакт | — | | Статус связи | не писали | _Обновлено: 2026-04-29_ > [!TIP] > Этот документ описывает MVP-подход. Начните с него для быстрого прототипа. <!-- alert-added --> <!-- summary --> >…

- **🤝 Контакт:** ему в комменты с тегами на Чепурову и Романова (и со ссылкой на NGT Memory), описав идею объединения, может оказаться буквально тем самым «карточкой к
- **🎯 Цель:** «как мерить качество извлечённой структуры», над которой Чуян ещё думает
- **🎯 Цель:** проходит через планирование, реализацию, ревью, security review и уведомление в Telegram; AI Factory сканирует проект, определяет стек, ставит skills, настраивает MCP-серверы, создаёт

_[→ Читать полностью](docs/04-ai-collaborations/00-intro.md)_

---


## Глава 10: Yodoca — память

> > [!IMPORTANT] > Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь. <!-- alert-added --> <!-- autofill-status --> | Параметр | Значение | |----------|---------| | Теги | — | | Упоминаний в репо | 229 | | Слой | memory | | Контакт | [@VitalyOborin](docs/contacts/vitalyoborin.md) | | Статус связи | не писали | _Обновлено: 2026-04-29_ <!-- summary --> >…

_[→ Читать полностью](docs/05-habr-projects/memory/yodoca.md)_

---


## Глава 11: NGT — граф памяти

> <!-- autofill-status --> | Параметр | Значение | |----------|---------| | Теги | — | | Упоминаний в репо | 260 | | Слой | memory | | Контакт | [@spbmolot](docs/contacts/spbmolot.md) | | Статус связи | не писали | _Обновлено: 2026-04-29_ <!-- summary --> > ассоциативные связи в персистентной памяти LLM[^llm] **Проекты:** Svyazi[^svyazi], NGT Memory --- <!-- tags: memory, ingestion, collaboration…

- **🎯 Цель:** «как мерить качество извлечённой структуры», над которой Чуян ещё думает

_[→ Читать полностью](docs/05-habr-projects/memory/ngt-memory.md)_

---


## Общая картина

Lorenzo — это не один проект, а **экосистема взаимосвязанных компонентов**:

1. **Svyazi 2.0** — ядро, объединяющее 20+ OSS-проектов
2. **Ансамбли** — синергетические сборки для конкретных задач
3. **MVP** — минимально жизнеспособный прототип за 12-18 месяцев
4. **Команда** — распределённые авторы на Хабре и GitHub
5. **Следующий шаг** — контакт с авторами ключевых компонентов

_Полная дорожная карта: [docs/01-svyazi/12-roadmap.md](docs/01-svyazi/12-roadmap.md)_


<!-- see-also -->

---

**Смотрите также:**
- [01-executive-summary](docs/04-ai-collaborations/01-executive-summary.md)
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
- [mvp-plan](docs/svyazi-2-0/prototype/mvp-plan.md)
- [13-контактная-стратегия-и-узкие-вопросы-для-авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md)

