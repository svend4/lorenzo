# Round 44 — Session Log

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** LLM здравоохранение v3, Embeddings v2, LLM Evaluation v2, агентные фреймворки v2  
**Статус:** ✅ Завершён

## Что искали

1. **LLM для здравоохранения v3** — клинические решения, обработка медицинских записей, NLP для ЭМК (электронных медицинских карт)
2. **Embeddings v2** — fine-tuning эмбеддингов на домене, multi-vector embeddings, поздние взаимодействия (ColBERT), русскоязычные эмбеддинги
3. **LLM Evaluation v2** — автоматические оценщики (LLM-as-judge), составные метрики, alignment evaluation, production A/B тестирование LLM
4. **Агентные фреймворки v2** — производительность агентных систем, fault tolerance, state management, долгосрочные агентные задачи

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R44-1 | ИИ-ассистент врача: GigaAM ASR + Mistral NLP → авто-заполнение ЭМК | AI Talent Hub (Иоган, Мусаев, Кустов, Миллер) | orchestration/analytics | [915330](https://habr.com/ru/articles/915330/) | — |
| R44-2 | LoRA fine-tuning эмбеддингов на юридических документах с hard-negative mining | huraligne (Саприн Семён, PGK) | analytics | [913912](https://habr.com/ru/companies/pgk/articles/913912/) | — |
| R44-3 | Yandex: production pipeline оценки LLM — от бенчмарков до LLM-as-judge | ibarskaya (Яндекс) | analytics | [861084](https://habr.com/ru/companies/yandex/articles/861084/) | — |
| R44-4 | LangGraph: checkpoint, fault tolerance и state management для агентов | antipov_dmitry | orchestration | [956940](https://habr.com/ru/articles/956940/) | — |

## Ключевые находки

### AI Talent Hub: ИИ-ассистент врача
- End-to-end pipeline: GigaAM v2 (Сбер, RNNT) + Diart (онлайн диаризация) + Pyannote 3.1 + NVIDIA NeMo → разделение врач/пациент в реальном времени
- Mistral-based NLP: NER из медицинской речи → 8 полей ЭМК (жалобы, анамнез, диагноз МКБ-10, назначения)
- Синтетические данные: фармацевтические датасеты + LLM-симуляция диалогов → обход 152-ФЗ (нет реальных записей пациентов)
- Эвристика разделения спикеров: медтермины → врач, жалобы → пациент
- MVP-стадия: real-time задержка ещё оптимизируется, интеграции с ЕГИСЗ нет

### huraligne/PGK: LoRA эмбеддинги
- Base: deepvk/USER-bge-m3 (366M params); LoRA: r=16, alpha=32, target=[query, key, value, dense]
- 7.1M обучаемых параметров из 366M (1.94%) → дёшево + нет catastrophic forgetting
- Hard-negative mining: NVIDIA NV-Retriever алгоритм (threshold=0.97, n=3 per positive)
- ~2400 триплетов, A100, 2 часа, 40 эпох, batch=32, TripletLoss cosine margin=0.5
- Результаты: Recall@5 67.5%→79.4% (+11.9 pp), NDCG@5 0.525→0.612 (+16.6%)
- Единственная RU статья на Хабре с полным бенчмарком доменного LoRA fine-tuning эмбеддингов

### ibarskaya/Яндекс: LLM Evaluation pipeline
- Трёхуровневая воронка: статические бенчмарки → Chatbot Arena (ELO) → LLM-as-judge (GPT-4o)
- Ключевая находка: стилистическая предвзятость — длинные структурированные ответы побеждают в 67% Arena без роста качества
- Утечка бенчмарков: до 20% скора от memorization; решение — динамические датасеты
- LLM-as-judge bias: GPT-4o тоже предпочитает длинные ответы → нужны explicit rubrics + calibration на human labels
- Многоступенчатая аннотация: calibration (agreement >75%) → AI-assisted → expert review для спорных

### antipov_dmitry: LangGraph production patterns
- 15+ Python примеров: глубокое сравнение LangChain (stateless chains) vs LangGraph (stateful graph)
- 3 бэкенда чекпоинтинга: MemorySaver (RAM, dev) → SqliteSaver (локальный prod) → PostgresSaver (distributed, LangSmith)
- Fault tolerance: `.with_retry(stop_after_attempt=3, wait_exponential_jitter=True)` + `.with_fallbacks([backup_llm])`
- Time-travel: `get_state_history()` + откат к любому чекпоинту (агент принял неверное решение → undo)
- HITL: `interrupt_before/after` любого узла → человек одобряет/корректирует → агент продолжает
- LangSmith Deployment: managed горизонтальное масштабирование LangGraph в production

## Collab Finder результаты

- **AI EMR ассистент** → NGT Memory [0.40], Wikontic [0.30] (новая ниша)
- **LoRA эмбеддинги** → нет результатов (новая ниша)
- **Yandex LLM Evaluation** → нет результатов (новая ниша)
- **LangGraph checkpointing** → Rufler [0.41], mclaude [0.40], AgentFS [0.39]

## Накопленная таблица раундов (R01–R44)

| Раунд | Проектов | Ключевая тема |
|-------|----------|---------------|
| R01 | 9 | Memory + Knowledge |
| R02 | 6 | Voice, parsing, YAML |
| R03 | 3 | Code review, fine-tuned LLM |
| R04 | 3 | Agent platform, MCP protocol |
| R05 | 3 | Autonomous pipeline, Russian NLP |
| R06–R10 | 20 | Video AI, multi-agent, GraphRAG, Rust, simulation |
| R11–R15 | 20 | Desktop agents, analytics AI, observability, Text2SQL |
| R16–R20 | 20 | ASR, Knowledge Graph, synthetic data, reasoning |
| R21–R25 | 20 | A2A, legal NLP, HR AI, DevOps, визуальное тестирование |
| R26–R30 | 20 | Finam, AIOps, LLM кибербезопасность, VLM, HITL |
| R31–R35 | 20 | DBRM, Cognitive Memory, Enterprise RAG, red-teaming, Edge AI |
| R36–R37 | 8 | FinBench, Memento, Rewrite Factory, AISecurity, IoT-MCP |
| R38 | 4 | MAESTRO медицина, Sequential координация, LangFuse, Graph RAG |
| R39 | 4 | Contract SGR, Agent Distillation, 5-Layer Memory, Stryker Testing |
| R40 | 4 | LLM строительство, Structured Output, Академия, Kaspersky MCP |
| R41 | 4 | Агро ML pipeline, SWE-MERA бенчмарк, Robovoice поддержка, Privacy LLM |
| R42 | 4 | AML LLM советник, PhysicalAgent VLA, SherlockOps SRE, T-Bank RU LLM |
| R43 | 4 | feeds.fun медиа, RAG чанкинг, LOCK-R reasoning, Kaspersky MLAD ICS |
| R44 | 4 | AI EMR ассистент, LoRA эмбеддинги, Yandex LLM eval, LangGraph агенты |
| **Итого** | **180** | **44 раунда** |

## Темы для Round 45

1. **Multimodal AI v3** — обработка документов (PDF, таблицы, схемы), VLM для промышленности, мультимодальный RAG v2
2. **LLM для финансов v3** — кредитный скоринг, риск-менеджмент, регуляторный compliance, торговые стратегии
3. **Russian NLP v3** — специализированные русскоязычные модели, адаптация LLM к RU-домену, морфология и синтаксис
4. **AI Observability v2** — monitoring LLM в production, drift detection, cost optimization, SLA для AI-систем
