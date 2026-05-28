---
date: 2026-05-28
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 43 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Темы: LLM для медиа v2, RAG v4 production, LLM Reasoning v2, LLM промышленность / Industry 4.0
Темы: LLM для медиа v2, RAG v4 production, LLM Reasoning v2, LLM промышленность / Industry 4.0  
Статус: ✅ Завершён
Что искали
1.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** LLM для медиа v2, RAG v4 production, LLM Reasoning v2, LLM промышленность / Industry 4.0  
**Статус:** ✅ Завершён

## Что искали

1. **LLM для медиа и контент-производства v2** — автоматическая генерация статей, fact-checking, SEO-оптимизация через LLM
2. **Retrieval-Augmented Generation v4** — long-context RAG, adaptive chunking, late interaction (ColBERT), production RAG evaluation
3. **LLM Reasoning v2** — chain-of-thought улучшения, Process Reward Models (PRM), математическое мышление, o1-style reasoning
4. **LLM для промышленности / Industry 4.0** — предиктивное обслуживание, цифровые двойники, LLM для SCADA/MES систем

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R43-1 | feeds.fun: LLM-автотегирование новостей с прозрачным ранжированием | Tiendil | analytics | [891308](https://habr.com/ru/articles/891308/) | [Tiendil/feeds.fun](https://github.com/Tiendil/feeds.fun) |
| R43-2 | RAG: 10 стратегий чанкинга + RAGAS CI/CD | Tianno (Oleg Bunin) | orchestration/analytics | [967102](https://habr.com/ru/companies/oleg-bunin/articles/967102/) | — |
| R43-3 | LOCK-R: CoT-парадокс и blind judge для LLM-рассуждений | aak204 | analytics | [1020016](https://habr.com/ru/articles/1020016/) | [aak204/LOCK-R](https://github.com/aak204/LOCK-R) |
| R43-4 | Kaspersky MLAD: цифровой двойник ICS + LLM как компрессор | Friflex_dev | analytics/orchestration | [1014940](https://habr.com/ru/amp/publications/1014940/) | — |

## Ключевые находки

### Tiendil: feeds.fun
- Open-source (Python/FastAPI/PostgreSQL/Vue.js) новостной агрегатор: LLM тегирует RSS-статьи → пользовательские сценарии фильтруют → прозрачный числовой скор
- Два уровня дедупликации URL (exact + canonical), прокси для bot-blocking, тест-корпус с mandatory/desired/forbidden assertions для CI
- Поддержка OpenAI и Gemini; стоимость: ~$0.00015/статья (gpt-4o-mini) → ~$4.5/месяц на 1000 статей/день
- 90% экономия времени по самооценке: 1000 статей → 50-100 релевантных

### Tianno: 10 стратегий чанкинга
- Системная классификация: fixed-size → sentence → semantic clustering → recursive/hierarchical → LDA topic-based → modality-aware → agentic auto-selection → hybrid
- Hybrid (regex структуры + LDA тематика + semantic проверка) — победитель benchmark (RAGAS Faithfulness 0.91 vs 0.74 у fixed-size)
- RAGAS evaluation на 100 QA-парах трёх уровней сложности в Weaviate+Qwen/Llama/Gemma; интеграция в CI/CD как quality gate

### aak204: LOCK-R / CoT-парадокс
- Детективный бенчмарк LOCK-R с байесовскими метриками (Bayesian Regret, Asymmetry Kc) вместо accuracy
- Ключевое открытие: CoT-парадокс — Chain-of-Thought удваивает байесовскую ошибку при верификации (рационализация гипотезы), но улучшает исследование
- Решение: Blind Judge архитектура — Thinking Explorer (CoT=ON) + Blind Judge (CoT=OFF, видит только факты) → regret 1.47→0.09 (16x)
- Подтверждено на Qwen3.5-9B и GPT-5.4; production кейс: debugging Payment API 40%→100% accuracy

### Friflex_dev: Kaspersky MLAD
- Цифровой двойник АСУ ТП в Dymola+MATLAB Simulink: физические модели (теплообмен, гидродинамика, химкинетика) → синтетические ПЛК-данные → обучение детектора аномалий без реальных атак
- Обнаруживает: целевые кибератаки (подмена сигналов) + человеческие ошибки (открытый вентиль) + оборудованные сбои
- LLM как компрессор: дообученный LLM = 4000x сжатие бинарных сенсорных данных (vs 10-15x gzip/bzip2); dual-use: высокая perplexity = аномалия

## Collab Finder результаты

- **feeds.fun** → нет результатов (новая ниша)
- **RAG чанкинг** → нет результатов (новая ниша)
- **LOCK-R** → нет результатов (новая ниша)
- **Kaspersky MLAD** → нет результатов (новая ниша)

## Накопленная таблица раундов (R01–R43)

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
| **Итого** | **176** | **43 раунда** |

## Темы для Round 44

1. **LLM для здравоохранения v3** — клинические решения, обработка медицинских записей, NLP для ЭМК (электронных медицинских карт)
2. **Embeddings v2** — fine-tuning эмбеддингов на домене, multi-vector embeddings, поздние взаимодействия (ColBERT), русскоязычные эмбеддинги
3. **LLM Evaluation v2** — автоматические оценщики (LLM-as-judge), составные метрики, alignment evaluation, production A/B тестирование LLM
4. **Агентные фреймворки v2** — производительность агентных систем, fault tolerance, state management, долгосрочные агентные задачи


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```
