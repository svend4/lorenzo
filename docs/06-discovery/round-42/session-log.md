---
date: 2026-05-15
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 42 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Темы: LLM финтех v3, мультимодальные агенты v2, LLM DevOps/SRE v2, русскоязычные LLM v3
Темы: LLM финтех v3, мультимодальные агенты v2, LLM DevOps/SRE v2, русскоязычные LLM v3  
Статус: ✅ Завершён
Что искали
1.


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** LLM финтех v3, мультимодальные агенты v2, LLM DevOps/SRE v2, русскоязычные LLM v3  
**Статус:** ✅ Завершён

## Что искали

1. **LLM для финтех v3** — кредитный скоринг через LLM, объяснимые решения, регуляторные требования
2. **Мультимодальные агенты v2** — vision-language для промышленных задач, VLM + action, screenshot-based automation
3. **LLM DevOps/SRE v2** — автоматическое расследование инцидентов, runbook execution, RCA через LLM
4. **Русскоязычные LLM v3** — fine-tuning на русских корпусах, GigaChat/YandexGPT архитектурные детали, MERA-бенчмарки

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R42-1 | LLM против мошенников: контекстный AML/AF советник | daniilmaibe | analytics/orchestration | [908424](https://habr.com/ru/articles/908424/) | — |
| R42-2 | PhysicalAgent: 4-агентный VLA-pipeline для роботов | Artem_Lykov (MTS) | orchestration | [979682](https://habr.com/ru/companies/ru_mts/articles/979682/) | ArXiv 2509.13903 |
| R42-3 | SherlockOps: LLM-агент расследования алертов | asvata (Duops) | orchestration | [1022830](https://habr.com/ru/articles/1022830/) | [Duops/SherlockOps](https://github.com/Duops/SherlockOps) |
| R42-4 | T-Lite/T-Pro: открытые RU LLM с turbo-alignment | anatolii-potapov (T-Bank) | analytics | [865582](https://habr.com/ru/companies/tbank/articles/865582/) | [turbo-llm/turbo-alignment](https://github.com/turbo-llm/turbo-alignment) |

## Ключевые находки

### daniilmaibe: LLM как AML/AF советник
- LLM не заменяет правила и ML-скоринг, а работает третьим уровнем: генерирует natural-language объяснение подозрительной транзакции для аналитика
- Два режима: batch (еженедельные нарративы, ~$0.02/клиент на GPT-4-turbo) и hybrid (online second-stage при ML-score > threshold)
- Детальная cost model: $20K/неделю для 1M клиентов → оптимизация через smaller model (GPT-4o-mini: $0.002) или self-hosted (Qwen 7B: $0.0002)
- Паттерн: device_change + geo_anomaly + large_tx + нетипичный получатель → нарратив на русском языке за 2-3 мин вместо 15

### Artem_Lykov / MTS: PhysicalAgent VLA
- 4 агента: Perceive (VLM анализирует сцену) → Plan (video generation синтезирует гипотетическое видео) → Reason (VLM верифицирует физическую реалистичность) → Act (motion extraction → команды суставов → реальный робот)
- Ключевое: физический валидатор останавливает нереалистичные планы (телекинез, нарушение гравитации) → перегенерировать
- 80% успех к 3-4 итерации; zero task-specific training data; поддерживаются GPT-4o, Claude 3.5, Qwen-VL, Gemini Pro Flash
- ArXiv: 2509.13903; сравнение: RT-2 требует 130K траекторий, PhysicalAgent — 0

### SherlockOps (asvata, Duops)
- Go-бинарь (v1: n8n+MCP, v2: standalone); при алерте — автономный обход ~50 интеграций в фиксированном порядке
- Стоп-условия: нашёл "OOMKilled"/"CrashLoopBackOff" → остановиться; или max 5 tool calls → синтез RCA
- Claude с extended thinking mode выбран после тестирования (Gemini отклонён из-за сбоев MCP)
- Routing через X-Environment header: один агент → prod/staging/dev кластеры; результат → Slack/Telegram Markdown

### T-Bank: T-Lite 7B + T-Pro 32B
- 4-этапный pipeline на базе Qwen 2.5: Stage 1 (100B RU + 15% EN replay) → Stage 2 (40B instruction mix) → Stage 3 (1B SFT) → Stage 4 (1B DPO)
- Ключевое открытие: replay-based continual pretraining = -80-90% стоимости vs full pretraining, результаты сопоставимые
- MERA: T-Pro 0.629, T-Lite 0.552; ruGSM8K T-Pro 94.1%; Arena Hard Ru ELO T-Pro 90.17
- turbo-alignment (Apache 2.0): полный SFT→DPO toolkit; HuggingFace: t-tech

## Collab Finder результаты

- **AML LLM** → нет результатов (новая ниша)
- **PhysicalAgent** → нет результатов (новая ниша)
- **SherlockOps** → нет результатов (новая ниша)
- **T-Bank LLM** → нет результатов (новая ниша)

## Накопленная таблица раундов (R01–R42)

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
| **Итого** | **172** | **42 раунда** |

## Темы для Round 43

1. **LLM для медиа и контент-производства v2** — автоматическая генерация статей, fact-checking, SEO-оптимизация через LLM
2. **Retrieval-Augmented Generation v4** — long-context RAG, adaptive chunking, late interaction (ColBERT), production RAG evaluation
3. **LLM Reasoning v2** — chain-of-thought улучшения, Process Reward Models (PRM), математическое мышление, o1-style reasoning
4. **LLM для промышленности / Industry 4.0** — предиктивное обслуживание, цифровые двойники, LLM для SCADA/MES систем


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```
