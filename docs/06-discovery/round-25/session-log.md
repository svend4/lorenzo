---
date: 2026-06-05
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Round 25 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Directum нормоконтроль (980140, декабрь 2025) — Open-source LLM на платформе Directum RX: проверка приказов/протоколов на стилистику + корпоративные стандарты через RAG регламентов.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** Юридический RAG, нормоконтроль LLM, AI-учёные, визуальное тестирование

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Law & Practice Ensemble RAG — законы + судебная практика с разными весами | OTUS | knowledge / orchestration | `projects/law-practice-ensemble-rag.md` |
| Directum: нормоконтроль на максималках — LLM проверяет корпоративные документы | Directum | orchestration / quality | `projects/directum-llm-normcontrol.md` |
| AI-учёные уже здесь: LLM меняют фундаментальную науку (AlphaFold 4, TxGemma) | независимый автор | knowledge / analytics | `projects/ai-scientists-llm-science.md` |
| Визуальное тестирование с AI: нейросеть vs pixel diff без ложных срабатываний | OTUS + Avito + T-Bank | quality / orchestration | `projects/visual-ai-testing-screenshots.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Legal RAG + Graph RAG (R22) | knowledge graph | Граф: статьи ГК → решения судов → комментарии → все связаны через Neo4j | ⭐⭐⭐⭐⭐ |
| Нормоконтроль + Contract Analysis (R22) | legal quality | Двухэтапный документ: нормоконтроль стиля → Claude анализирует риски | ⭐⭐⭐⭐⭐ |
| Science AI + Agentic RAG (R18) | research agent | Research Agent сам выбирает из 18 инструментов (PubMed, код, AlphaFold API) | ⭐⭐⭐⭐ |
| Visual Testing + LLM Tests (R20) | quality pipeline | Mutation тесты для кода + neural diff для UI = трёхслойная quality defense | ⭐⭐⭐⭐ |
| Legal RAG + FRIDA (R18) | RU legal embeddings | FRIDA русские embeddings для юридических текстов (терминология ГК РФ) | ⭐⭐⭐⭐ |

## Главные находки раунда

**Law & Practice Ensemble RAG** (946012, 2025) — Два индекса с разными весами: нормативные акты (0.6) + судебная практика (0.4). Ключевое: юридический ответ без практики = неполный (суды иногда трактуют иначе закона). Query routing: вопросы о нормах → law_heavy, о практике → practice_heavy. Метрики: с ensemble галлюцинации 4% (vs 15% только на законах), полнота 89%. Кейс: недвижимость (ГК РФ + Пленум ВС + арбитраж). Для Lorenzo: Docs+Decisions как Law+Practice.

**Directum нормоконтроль** (980140, декабрь 2025) — Open-source LLM на платформе Directum RX: проверка приказов/протоколов на стилистику + корпоративные стандарты через RAG регламентов. Multi-tenant: каждая организация имеет свой корпоративный RAG. Метрики: -80% нагрузки на нормоконтролёра, 25 сек vs 15 мин. Смежно: сравнение редакций договоров (990044). Для Lorenzo: structured document QA для discovery-файлов.

**AI-учёные** (938638 + 954612, 2025) — Систематический обзор LLM в науке: AlphaFold 4 (белки), TxGemma (лекарства), GNoME 2.2M материалов, AlphaProof (математика). Ключевая проблема: галлюцинации в науке = потерянные месяцы и миллионы рублей. Паттерны защиты: grounded generation, "не знаю" как валидный ответ, peer-review другой LLM. Research Agent: 18 инструментов (PubMed, код, AlphaFold API). Для Lorenzo: Knowledge Discovery Pipeline.

**Визуальное тестирование AI** (956492, 2025) — Проблема: только 20% команд используют screenshot-тесты из-за flakiness. Решение: displacement neural network (предсказывает dx/dy вместо boolean) + LLM описывает изменения человекочитаемо. T-Bank паттерн: semantic assertions через vision LLM вместо пиксельного сравнения. Для Lorenzo: visual QA над Mermaid/SVG артефактами.

## Сводная карта R01–R25

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |
| R06 | 4 | Video AI, CLI agents, GitHub automation | Memory MCP v2, DevClaw паттерн |
| R07 | 4 | Multi-agent architecture, agent safety | openLight принцип, 9-агентный паттерн |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI | SocratiCode, Paper2Agent |
| R09 | 4 | GraphRAG, decentralized AI, coding agent | GraphRAG pipeline, HMP, OpenCode |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust | MiroFish, n8n AI Stack |
| R11 | 4 | Desktop agents, edge AI, voice embedded | Союз (MCP desktop), RPi+Ирина voice pipeline |
| R12 | 4 | Data analytics AI, audio gen, vector DBs | Veai IDE agent, BI Agent Pattern |
| R13 | 4 | Observability, ADD, self-healing, OCR | Langfuse pattern, ADD feedback loop |
| R14 | 4 | Context Engineering, DSPy, security, ingestion | MarkItDown, Security Audit framework |
| R15 | 4 | Code review AI, Text2SQL, fine-tuning, LLM security | Fine-tuning 2026, AI Review CI/CD |
| R16 | 4 | No-LangChain, monitoring LLM, GigaAM-v3, RAG eval | GigaAM-v3 SOTA, Custom LLM distillation |
| R17 | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | LLM-Wiki paradigm, Sberbank KG production |
| R18 | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings | FRIDA #1 ruMTEB, Agentic RAG taxonomy |
| R19 | 4 | Multimodal RAG, doc review AI, vector DB, LLM inference | Docling+RRF SoTA, Desmond Cognitive Worker |
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | LLM Router pattern, mutation test pipeline |
| R21 | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification | A2A+MCP stack, 3-agent autonomous ops |
| R22 | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | Graph RAG 96.7%, n8n+Ollama self-hosted |
| R23 | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | Durable State архитектура, Phantom framework |
| R24 | 4 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | DevOps дистилляция 10/10, Sberbank -73% MTTR |
| R25 | 4 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование | Legal Ensemble RAG, Directum нормоконтроль |

**Итого: 104 проекта, 54+ авторов**

## Что осталось на R26

- **LLM для финансов и BI** — AI-аналитик финансовых отчётов, аномалии транзакций, генерация financial narrative
- **Кастомные embedding-модели** — domain-specific embeddings, contrastive learning, fine-tune для корпоративного поиска
- **AI для Supply Chain / Operations** — прогнозирование спроса, оптимизация маршрутов, warehouse AI
- **LLM как ядро продукта (B2B SaaS)** — примеры где AI = core value proposition, не feature; monetization patterns


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
- [Решения](../../DECISIONS.md)
