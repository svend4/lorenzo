# Round 46 — Session Log

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** Multi-agent coordination v2, LLM телеком v2, RAG для кода v2, Edge AI v2  
**Статус:** ✅ Завершён

## Что искали

1. **Multi-agent coordination v2** — протоколы взаимодействия между агентами, distributed reasoning, consensus механизмы, MAS (Multi-Agent Systems) в production
2. **LLM для телекома v2** — качество обслуживания с LLM, сетевое планирование, обработка тикетов, персонализация тарифов
3. **RAG для кода v2** — code search, documentation RAG, LLM code review с retrieval, codebase Q&A
4. **Edge AI v2** — квантизация для мобильных устройств, WebGPU inference, on-device персонализация, federated inference

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R46-1 | Глухой телефон для ИИ: физика LLM-графов и 4 метрики координации | aak204 | analytics/orchestration | [1019490](https://habr.com/ru/articles/1019490/) | [aak204/llm-coordination-harness](https://github.com/aak204/llm-coordination-harness) |
| R46-2 | Классификатор тикетов для телеком-поддержки на Qwen2.5-0.5B за $10/мес | ractangle | orchestration/analytics | [988916](https://habr.com/ru/articles/988916/) | — |
| R46-3 | MCP-сервер для кодовой базы: Tree-sitter + sqlite-vec + архитектурное зрение | EvgeniyRasyuk | orchestration/knowledge | [948002](https://habr.com/ru/articles/948002/) | — |
| R46-4 | AQLM.rs: 8B LLM в браузере через WebAssembly и 2-битную квантизацию | galqiwi (Yandex Research) | analytics | [864296](https://habr.com/ru/companies/yandex/articles/864296/) | [galqiwi/demo-aqlm-rs](https://github.com/galqiwi/demo-aqlm-rs) |

## Ключевые находки

### aak204: LLM Coordination Harness ("Глухой телефон")
- LLM Coordination Harness — измерительный фреймворк для мультиагентных LLM-систем
- 4 оригинальных метрики: F (Fidelity, сохранность фактов), ρ (Error Correlation, независимость ошибок), B (Propagation Balance, Gini коэффициент), C (Fan-in Pressure, насыщение контекста)
- Топологии: Star (flat) vs Balanced Tree с бюджетами 0/32/96 токенов на хоп
- 144 цикла, ~2000 API-вызовов; модели: Qwen 3.5 Plus + Gemini 3.1 Flash Lite через OpenRouter
- Парадокс: иерархическое дерево теряет ~25% фактов, но устойчивее к adversarial injection чем star
- Тот же автор что LOCK-R (R43) — второе оригинальное исследование

### ractangle: телеком-классификатор
- Qwen2.5-0.5B-Instruct fine-tuned на ~4000 синтетических телеком-примеров (Google Colab T4, 40 мин)
- GGUF Q4_K_M: 350 MB; FastAPI + llama-cpp-python на VPS 2vCPU/4GB RAM
- Структурированный вывод: intent + category + urgency + sentiment + routing_destination
- Intent accuracy 92%, category 89%, CPU inference 3-5 сек; total cost $10/месяц
- On-premise: данные клиентов не покидают инфраструктуру оператора (телеком compliance)
- Heuristic pre-filter для очевидных случаев (< 1мс) + LLM для неоднозначных

### EvgeniyRasyuk: Code MCP Server
- Трёхслойный retrieval: Tree-sitter AST parsing → sqlite-vec векторный поиск → local embeddings (all-MiniLM-L6-v2 через @xenova/transformers WASM)
- 4 агента: CollectorAgent → AnalysisAgent (call graphs, inheritance) → SemanticAgent (векторизация) → RefactoringAgent (дублирование)
- 13 MCP-инструментов: semantic_search, get_dependencies, get_dependents, trace_call_path, find_duplicates, get_complexity_hotspots
- 5.5x быстрее нативного Claude анализа (55.84с → <10с); 100+ файлов/сек; <100мс latency; ~65 MB RAM
- Отвечает на вопросы: "что сломается при изменении IUserService?" — impact analysis через граф зависимостей

### galqiwi/Yandex Research: AQLM.rs
- AQLM (Additive Quantization for Language Models): 2-битное аддитивное ВЕКТОРНОЕ квантование
- Llama 3.1 8B: 16 GB (bf16) → ~2.5 GB (AQLM 2-bit), 8x сжатие при ~3% потере качества
- Rust → WebAssembly: CPU inference в браузере без GPU; multi-thread через Web Workers + SharedArrayBuffer (~2x speedup)
- PV-Tuning (тот же автор, май 2024): донастройка кодовых книг после квантизации → компенсация ошибок
- GitHub: galqiwi/demo-aqlm-rs; живое демо на GitHub Pages
- Принципиально ≠ WebGPU/WebLLM (R41): здесь CPU+WASM; ≠ GGUF: аддитивное vs скалярное квантование

## Collab Finder результаты

- **Coordination Harness** → Rufler [0.41], mclaude [0.40], AgentFS [0.39], Wikontic [0.20]
- **Telecom Classifier** → NGT Memory [0.41], Yodoca [0.40], Wikontic [0.14]
- **Code MCP** → нет результатов (новая ниша)
- **AQLM.rs** → Wikontic [0.40]

## Накопленная таблица раундов (R01–R46)

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
| R45 | 4 | MWS Vision Bench, MOEX DistilBERT, Avito Mistral RU, LLM Observability |
| R46 | 4 | Coordination Harness, Telecom Classifier, Code MCP, AQLM.rs браузер |
| **Итого** | **188** | **46 раундов** |

## Темы для Round 47

1. **LLM для образования v3** — персонализированное обучение с LLM, автоматическая генерация заданий, адаптивные курсы, AI-тьютор
2. **Безопасность LLM v3** — защита от adversarial attacks, robustness testing, AI safety в production, prompt injection v2
3. **LLM для DevOps v2** — автоматизация CI/CD с LLM, log analysis, infrastructure-as-code generation, incident post-mortem
4. **Граф знаний v2** — KG construction with LLM, knowledge graph RAG v2, entity linking, dynamic knowledge graphs
