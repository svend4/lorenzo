---
date: 2026-05-29
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 45 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Multi-agent coordination v2 — протоколы взаимодействия между агентами, distributed reasoning, consensus механизмы, MAS (Multi-Agent Systems) в production
2.


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** Multimodal AI v3, LLM финансы v3, Russian NLP v3, AI Observability v2  
**Статус:** ✅ Завершён

## Что искали

1. **Multimodal AI v3** — обработка документов (PDF, таблицы, схемы), VLM для промышленности, мультимодальный RAG v2
2. **LLM для финансов v3** — кредитный скоринг, риск-менеджмент, регуляторный compliance, торговые стратегии
3. **Russian NLP v3** — специализированные русскоязычные модели, адаптация LLM к RU-домену, морфология и синтаксис
4. **AI Observability v2** — monitoring LLM в production, drift detection, cost optimization, SLA для AI-систем

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R45-1 | MWS Vision Bench: первый RU бенчмарк для бизнес-OCR с VLM | eCaesar (MTS AI) | analytics | [953292](https://habr.com/ru/companies/mts_ai/articles/953292/) | есть (HuggingFace) |
| R45-2 | DistilBERT для торговых сигналов на MOEX | empenoso (Михаил Шардин) | analytics | [955612](https://habr.com/ru/articles/955612/) | [empenoso/llm-stock-market-predictor](https://github.com/empenoso/llm-stock-market-predictor) |
| R45-3 | Авито: Mistral-7B русскоязычный — новый токенизатор + continual pretraining | Anastasiya_Rysmyatova (Авито) | analytics | [852958](https://habr.com/ru/companies/avito/articles/852958/) | — |
| R45-4 | LLM Observability & AI Agent Tracing: semantic span typing и 6 инструментов | antipov_dmitry | orchestration/analytics | [972480](https://habr.com/ru/articles/972480/) | — |

## Ключевые находки

### MTS AI / eCaesar: MWS Vision Bench
- Первый структурированный русскоязычный бенчмарк для бизнес-OCR с VLM: 800 изображений, 2580 QA-пар
- 5 типов задач с разными метриками: full-page OCR (CER), image-to-markdown (TEDS), text grounding (IoU), KIE (F1 на JSON), VQA
- Документы: сканы, схемы, таблицы, чертежи, рукопись, смешанные
- Лидерборд: Gemini-2.5-Pro (0.682) > Flash (0.644) > GPT-4.1-mini (0.643) > Claude-4.5-Sonnet (0.639)
- Ключевые выводы: grounding < IoU 0.25 для большинства моделей (кроме Anthropic); летние 2025 модели — регресс vision при росте LM; vision encoder завис на ~500M параметров
- Публичный датасет на HuggingFace + закрытый test set

### empenoso: MOEX DistilBERT
- DistilBERT fine-tuned на OHLCV → текст → binary classification (цена вырастет/упадёт)
- Паттерн: числа → текстовые описания ("цена растёт сильно, объём выше среднего") → LLM
- Walk-forward валидация: 252 дня обучения, 21 день теста, сдвиг 21 день
- 227+ тикеров MOEX; AUC-ROC средний ~0.53; лучшие: AFLT (0.72), RTSB (0.70), PIKK (0.70)
- Честный вывод: эффективный рынок делает задачу сложной; умеренная предиктивная сила на отдельных эмитентах
- Open-source GitHub: Docker + публичные данные MOEX → воспроизводимо

### Авито / Anastasiya_Rysmyatova: Mistral-7B русификация
- Новый SentencePiece токенизатор для русского: chars/token 2.1 → 3.3 (+57%, 1.5x быстрее инференс)
- Инициализация embeddings: новые токены через усреднение embeddings подтокенов старого токенизатора
- CPT: 1.1 TB дедуплицированных RU текстов, 72× A100 80GB, ~15 дней/эпоха, Megatron-LM + DeepSpeed
- Двухступенчатое обучение: Stage 1 (100GB, embeddings заморожены) → Stage 2 (1TB, полное разморажение)
- 10% английских данных: предотвращение catastrophic forgetting EN знаний
- SFT на задачах Авито: модерация, поиск, генерация описаний, извлечение параметров
- LoRA не решает проблему токенизатора — нужен полный CPT

### antipov_dmitry: LLM Observability
- Semantic Span Typing — новая парадигма: `llm.reasoning`, `agent.planning`, `agent.observation`, `agent.memory`, `workflow.state_transition`
- Таксономия production-багов: ~40% — галлюцинация параметров инструментов; context drift; RAG cascade failure; "кроличья нора"
- 6 open-source платформ: Langfuse (PostgreSQL, prod), Phoenix (SQLite, отладка), OpenLIT (GPU+DCGM), Langtrace (JS native), LangWatch (guardrails), Lunary (fast start)
- Post-mortem > real-time для LLM-агентов: баги проявляются в последовательности решений
- DAG-с-циклами: реальный граф обхода агента ≠ дерево (нужна специальная визуализация)
- OpenTelemetry OTLP → vendor-neutral backend

## Collab Finder результаты

- **MWS Vision Bench** → нет результатов (новая ниша)
- **MOEX DistilBERT** → нет результатов (новая ниша)
- **Avito Mistral-7B** → нет результатов (новая ниша)
- **LLM Observability** → agent-memory-mcp [0.42], NGT Memory [0.29], knowledge-space [0.24]

## Накопленная таблица раундов (R01–R45)

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
| **Итого** | **184** | **45 раундов** |

## Темы для Round 46

1. **Multi-agent coordination v2** — протоколы взаимодействия между агентами, distributed reasoning, consensus механизмы, MAS (Multi-Agent Systems) в production
2. **LLM для телекома v2** — качество обслуживания с LLM, сетевое планирование, обработка тикетов, персонализация тарифов
3. **RAG для кода v2** — code search, documentation RAG, LLM code review с retrieval, codebase Q&A
4. **Edge AI v2** — квантизация для мобильных устройств, WebGPU inference, on-device персонализация, federated inference


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```
