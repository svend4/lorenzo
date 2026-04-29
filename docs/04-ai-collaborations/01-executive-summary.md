# Executive summary

> [!IMPORTANT]
> Главный документ проекта. Начните чтение отсюда.

<!-- alert-added -->

<!-- summary -->
> Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: ingestion и нормализация профи
**Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], mclaude, AI Factory, Rufler[^rufler], LiteParse, Legal RAG[^rag]

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, collaboration -->




## Executive summary

Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: ingestion и нормализация профилей из свободного текста, agent‑first knowledge base, файлосистемная память для агентов, ассоциативная и консолидируемая долговременная память, визуально проверяемый RAG, многоагентная оркестрация, безопасный MCP[^mcp]‑слой, локальный voice→vault вход и бюджетно‑осознанный роутинг моделей. Самостоятельно каждый блок выглядит либо как аккуратный pet‑project, либо как «узкая» инженерная находка. Но вместе они уже дают не “ещё один AI‑ассистент”, а операционную систему для обнаружения коллабораций, накопления доказуемого знания и полуавтономной работы агентов в локальном контуре. citeturn41search0turn33view3turn33view4turn21view0turn22view4turn20view5turn20view6turn20view11

Самая сильная линия синергии выглядит так. Основа — Svyazi‑подобный гибридный пайплайн: LLM[^llm] извлекает смысл, детерминированный код нормализует, а **CardIndex** фиксирует состояние карточки и версионирование. Поверх этого нужен agent‑readable слой знаний и единый source of truth для разных рантаймов — здесь хорошо ложатся knowledge‑space и AgentFS. Дальше память должна не просто хранить факты, а уметь усиливать слабые сигналы, консолидировать эпизоды и забывать шум — это зона Yodoca[^yodoca], NGT[^ngt] Memory, MemNet и более инженерных систем вроде agent-memory-mcp/Memory OS. Для многоагентной работы уже есть mclaude, AI Factory, AIF Handoff, Rufler и протокол Sequential; для forensic‑режима — research-docs/LiteParse, Legal RAG, Hybrid RAG и Graph RAG; для безопасного и дешёвого исполнения — Tool Search, LiteLLM, Auto AI Router, RLM-Toolkit и SENTINEL[^sentinel]. citeturn33view2turn27view0turn21view1turn22view3turn21view4turn20view16turn39view3turn20view2turn20view3turn20view4turn20view11turn20view5turn34view2turn34view3turn39view1turn39view0turn20view18turn20view10

Главный аналитический вывод: **на Хабре пока не видно одного готового проекта, который уже собрал все слои в единое целое, но видно много авторов, каждый из которых почти идеально закрывает один слой будущей системы.** Поэтому реальная ценность исследования — не в списке ссылок, а в правильной сборке ансамблей. Наиболее прагматичный путь — не строить большой новый монолит, а начать с минимального прототипа из пяти компонентов: Svyazi‑подобный import/normalize/CardIndex, AgentFS‑подобное файловое ядро, NGT կամ Yodoca‑подобная память, research-docs/LiteParse‑подобный evidence‑слой и LiteLLM/Auto AI Router+SENTINEL как исполнительный периметр. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn11search2turn39view0turn20view10

<!-- similar-docs -->

---

**Похожие документы:**
- [01-executive-summary](docs/01-svyazi/01-executive-summary.md) (сходство 0.68)
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.15)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [03-component-catalog](docs/01-svyazi/03-component-catalog.md)
- [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md)



<!-- footnotes-added -->

---

[^mcp]: Model Context Protocol — протокол для AI-инструментов

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^llm]: Large Language Model — большая языковая модель

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^ngt]: OSS-проект: ассоциативный граф памяти (BSL 1.1)

[^sentinel]: OSS-проект: безопасность и allowlist для MCP

[^rufler]: OSS-проект: оркестратор AI-агентов

[^svyazi]: Главный проект: экосистема AI-компонентов
