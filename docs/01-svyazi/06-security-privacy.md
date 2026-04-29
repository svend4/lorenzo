
<!-- summary -->
> Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а **с самого начала считать skills, MCP servers, импорты документов и memory writes потенциально недоверенными**. Это не паранойя,
**Проекты:** Svyazi, AgentFS, AI Factory, agent-memory-mcp, SENTINEL, LiteLLM, Auto AI Router, Tool Search

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, self-improvement, collaboration -->



## Безопасность, приватность и бюджетный роутинг

Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а **с самого начала считать skills, MCP servers, импорты документов и memory writes потенциально недоверенными**. Это не паранойя, а прямой вывод из материалов про Prompt Worms, катастрофы автономных агентов и практик защиты AI Factory/SENTINEL. Дополнительный важный сигнал: сами reference MCP servers указываются как образовательные примеры, а не production‑готовые решения — значит, прод‑политики доступа и аудит нужно строить отдельно. citeturn34view4turn34view5turn29search6turn20view10turn15search10

**Что стоит зафиксировать как default policy**

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске | `agent-memory-mcp` демонстрирует хороший паттерн Path Guard/allowlist против traversal и выхода за пределы проекта. citeturn20view16 |
| PII separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal | `inferred` и weak signals не писать сразу в «истину», а ставить в pending review | И Svyazi, и более тяжёлые memory‑системы сходятся на нужде в review‑контуре. citeturn41search0turn36search0 |
| Runtime firewall | Между агентом и mutating tools держать специализированный защитный слой | Именно для этого и нужен SENTINEL‑подобный слой, а не только “умный промпт”. citeturn20view10 |

С точки зрения приватности лучший режим для первых версий — **local-first by default, cloud by exception**. Голос, стенограммы, первичные профили, внутренние документы и memory‑база должны оставаться локально; в облако есть смысл отправлять только самые сложные этапы, где действительно нужен дорогой reasoning. Такой подход уже поддерживают и локальные voice‑пайплайны, и AgentFS/knowledge‑workspace‑подходы, и budget/privacy‑режимы RLM‑Toolkit. citeturn21view10turn35search0turn27view0turn20view18

**Практичный бюджетный роутинг моделей**

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |

Эта схема опирается сразу на несколько наблюдений из найденных источников. Во‑первых, Memory OS показывает, что на extraction высокий reasoning не всегда полезен и может ломать schema discipline. Во‑вторых, Tool Search снижает context tax ещё до начала работы. В‑третьих, Auto AI Router и LiteLLM позволяют скрыть провайдерную сложность за единым API, а RLM‑Toolkit прямо формализует budget‑first / privacy‑first конфигурации. citeturn39view3turn39view1turn39view0turn11search2turn20view18

Практически это означает следующее. Если нужен **самый дешёвый** режим — запускать extraction, indexing и basic memory на локальной модели, а в облако отправлять только ambiguous ranking и финальное объяснение. Если нужен **самый приватный** режим — использовать локальные модели и gateway только как внутренний abstraction layer. Если нужен **самый качественный** режим — оставить локально retrieval и memory, а премиум‑модель включать только на объяснение, конфликт‑resolution и сложные relation‑queries. При таком подходе дорогая модель перестаёт быть “двигателем всего” и становится “дорогим, но редким specialist step”. citeturn20view18turn39view0turn11search2

<!-- similar-docs -->

---

**Похожие документы:**
- [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) (сходство 1.00)
- [05-план-прототипа-и-возможные-контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) (сходство 0.13)
- [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) (сходство 0.13)

