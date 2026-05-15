# Round 40 — Session Log

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** LLM строительство/инфраструктура, structured output v2, LLM образование v3, AI кибербезопасность v2  
**Статус:** ✅ Завершён

## Что искали

1. **LLM для строительства и инфраструктуры** — BIM, строительные нормы, автоматическая проверка проектов
2. **Structured output и function calling v2** — надёжный JSON, три уровня: Instructor/BAML/Outlines
3. **LLM для образования v3** — production агент для вуза, гибридный поиск, SQL агент
4. **AI для кибербезопасности v2** — LLM + MCP + OpenSearch, codegen паттерн для анализа логов

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R40-1 | NSR Specification: LLM → BIM проверки из норм | nanocad (Нанософт) | analytics/orchestration | [947304](https://habr.com/ru/companies/nanosoft/articles/947304/) | — |
| R40-2 | Structured Output: Instructor + BAML + Outlines | slivka_83 | orchestration/analytics | [978534](https://habr.com/ru/articles/978534/) | [instructor](https://github.com/567-labs/instructor), [outlines](https://github.com/dottxt-ai/outlines) |
| R40-3 | Академия РАНХиГС: LangGraph + 25K запросов | SGERCEN | orchestration | [944500](https://habr.com/ru/articles/944500/) | — |
| R40-4 | Kaspersky: LLM + MCP + OpenSearch codegen | Ins4n3 | orchestration/analytics | [953780](https://habr.com/ru/companies/kaspersky/articles/953780/) | [ins4n333/aidemo](https://github.com/ins4n333/aidemo) |

## Ключевые находки

### NSR Specification (nanocad/Нанософт)
- Единственная российская система преобразования текстов СНиПов/СП в машиночитаемые BIM-правила
- LLM парсит каждый пункт нормы в триплет Subject→Object→Property → правило-чекер NSR
- Честная оценка: точность 50-60% (требует верификации), гибрид LLM + ручная проверка
- Форматы IFC/CDE, BIM-системы: CADLib/Larix/nanoCAD/BIMIT; мировые аналоги: buildingSMART IDS, Solibri

### Structured Output три уровня (slivka_83)
- Уровень 1: Instructor (retry + Pydantic ValidationError → LLM контекст) — application layer
- Уровень 2: BAML (soft parsing — trailing commas, одинарные кавычки, Markdown) — parsing layer
- Уровень 3: Outlines (logit masking — 100% гарантия, только self-hosted vLLM/Ollama) — sampling layer
- Adversarial тест (Mentalitet, 2026): ни один провайдер не поддерживает полный JSON Schema; client-side Pydantic валидация обязательна

### Академия РАНХиГС (SGERCEN)
- Production LangGraph StateGraph с 10+ узлами: модерация → цензура → FAQ → контекстуализация → маршрутизация → RAG/SQL/прямой ответ
- Гибридный поиск: multilingual-e5-base (768-dim) + BM25 + Milvus + RRF
- SQL-агент (LangChain + SQLAlchemy + PostgreSQL): ~100 программ × ~20 параметров
- 25K+ запросов от 10K+ пользователей за 2 месяца; Qwen3-32B-AWQ через vLLM на A6000

### Kaspersky LLM + MCP + OpenSearch (Ins4n3)
- 5-фаз: schema detection (1 лог) → codegen scroll script → local execution → codegen analysis → LLM synthesis
- Ключевой паттерн: LLM генерирует Python → Python работает вне LLM с полным объёмом данных (ГБ)
- Обходит деградацию контекста при >70-80% заполнении
- GitHub: 3 файла (opensearch.py, mcp.json, .roomodes с ролью PythonDeveloper)

## Collab Finder результаты

- **NSR BIM** → нет результатов (новая ниша для коллекции)
- **Structured Output** → нет результатов (новая ниша)
- **Академия РАНХиГС** → нет результатов (новая ниша)
- **Kaspersky MCP** → Wikontic [0.400]

## Накопленная таблица раундов (R01–R40)

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
| **Итого** | **164** | **40 раундов** |

## Темы для Round 41

1. **LLM для агропромышленности** — точное земледелие, прогноз урожая, анализ почвенных данных
2. **LLM code generation v3** — unit-тестируемый код, архитектурные паттерны, SWE-bench production
3. **LLM для клиентского сервиса v2** — многоканальный CRM, escalation detection, sentiment-driven routing
4. **Privacy-preserving LLM** — federated fine-tuning, differential privacy, on-device inference без передачи данных
