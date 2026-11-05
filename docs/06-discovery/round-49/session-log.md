---
date: 2026-06-05
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 49 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> session-log — раздел документации проекта Lorenzo. Документ содержит описание рисков и ограничений.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Статус:** ✅ Завершён  
**Тема:** LLM финтех v2, Structured output v3, Self-hosted AI v2, LLM + базы данных v2

## Что искали

| Тема | Запрос | Результат |
|------|--------|-----------|
| LLM финтех v2 | RAG финансовый ассистент банк multi-hop гибридный поиск | Runoi — финансовый RAG 4-головый ретривер + ITERATIVE/DECOMPOSE стратегии |
| Structured output v3 | constrained decoding GBNF XGrammar формальные грамматики | Safreliy (PostgresPro) — GBNF + XGrammar + иерархия Хомского |
| Self-hosted AI v2 | on-premise LLM сервер hardware enterprise replicated tensor parallelism | Dmitrii-Chashchin (BVM) — 4× RTX 4090 водяное охлаждение, replicated vs TP |
| LLM + базы данных v2 | Text2SQL schema-agnostic SAP ERP итеративная разведка | gennadybanin — Text2SQL агент-сапёр для SAP ERP, 15%→85% точность |

## Найденные проекты

| Файл | Автор | Уникальность |
|------|-------|--------------|
| `runoi-finance-rag-four-head-hybrid-retriever.md` | Runoi | 4-головый ретривер (vector+BM25+граф+semantic), SeaAgent+DecompositionAgent, 9.66/10 LLM-judge, $0.98 за 500 запросов |
| `safreliy-gbnf-xgrammar-constrained-decoding.md` | Safreliy (PostgresPro) | GBNF через Хомского, XGrammar (99% CI-токены предвычислены), динамические грамматики, vLLM guided_grammar, 3 production кейса |
| `dmitrii-chashchin-self-hosted-4x4090-vllm-parallelism.md` | Dmitrii-Chashchin (BVM) | 4×RTX 4090 96GB суммарно, replicated 9.6× быстрее TP=4 на PCIe без NvLink; 18 564 t/s; водяное охлаждение 29-38°C |
| `gennadybanin-text2sql-sap-erp-schema-explorer.md` | gennadybanin (GunS82) | Schema-agnostic explorer: are_tables_present→explore_and_probe→execute; get_domain_texts добавил +31% точности; 15%→85% |

## Ключевые статьи Хабра

- https://habr.com/ru/articles/963482/ — Finance RAG 4-головый ретривер (ноябрь 2025)
- https://habr.com/ru/companies/postgrespro/articles/922260/ — GBNF + XGrammar constrained decoding (июнь 2025)
- https://habr.com/ru/articles/1032698/ — Self-hosted 4×RTX 4090 production кейс (май 2026)
- https://habr.com/ru/articles/954712/ — SAP ERP Text2SQL Schema Explorer (октябрь 2025)

## Итого по всем раундам

| Раунд | Проектов | Ключевая тема |
|-------|----------|---------------|
| R01 | 9 | Memory + Knowledge |
| R02 | 6 | Voice, parsing, YAML |
| R03 | 3 | Code review, fine-tuned LLM |
| R04 | 3 | Agent platform, MCP protocol |
| R05 | 3 | Autonomous pipeline, Russian NLP |
| R06 | 3 | Video AI, CLI agents, GitHub automation |
| R07 | 4 | Multi-agent arch, agent safety, MCP pipeline |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI |
| R09 | 4 | GraphRAG, decentralized AI, coding agent |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust |
| R11 | 4 | Desktop agents, edge AI, voice embedded |
| R12 | 4 | Data analytics AI, audio gen, vector DBs |
| R13 | 4 | Observability, ADD, self-healing tests, OCR |
| R14 | 4 | Context Engineering, DSPy, AI security, MarkItDown |
| R15 | 4 | Code review AI, Text2SQL, fine-tuning, LLM security |
| R16 | 4 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval |
| R17 | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA |
| R18 | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings |
| R19 | 4 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference |
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics |
| R21 | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification |
| R22 | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod |
| R23 | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection |
| R24 | 4 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек |
| R25 | 4 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование |
| R26 | 4 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт |
| R27 | 4 | LLM кибербезопасность, персональный AI с памятью, 5-фазный оркестратор, RAG тесты |
| R28 | 4 | Volga streaming ML, мультимодальный VLM Сбер, LLM Judge кросс-модельный, Federated edge |
| R29 | 4 | Comprehension debt, Text2SQL X5, AI мета-мониторинг, Кириллица в LLM |
| R30 | 4 | Coreness Flow composable, VLM vs IDP бенчмарк, синтетика граф-качество, HITL prod |
| R31 | 4 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic |
| R32 | 4 | Enterprise RAG (МТС), vLLM inference opt, FinPDF pipeline, Авито VLM |
| R33 | 4 | AI code agents v2, LLM data engineering, суверенный AI, red-teaming |
| R34 | 4 | LLM DevSecOps, Multimodal doc v2, LLM evaluation, Edge AI |
| R35 | 4 | LLM телеком, персонализация, AI образование v2, agent planning |
| R36 | 4 | LLM финансовый compliance, continuous adaptation, логистика AI, LLM для науки |
| R37 | 4 | LLM медиа, AI безопасность v2, LLM IoT/промышленность, LLM calibration |
| R38 | 4 | LLM медицина v2, multiagent coordination, LLM observability, RAG v3 |
| R39 | 4 | LLM юридическая авт. v2, synthetic data, персонализация v2, AI testing v2 |
| R40 | 4 | LLM строительство, structured output v2, образование v3, кибербезопасность v2 |
| R41 | 4 | Агро ML pipeline, SWE-MERA бенчмарк, Robovoice поддержка, Privacy LLM |
| R42 | 4 | AML LLM советник, PhysicalAgent VLA, SherlockOps SRE, T-Bank RU LLM |
| R43 | 4 | feeds.fun медиа, RAG чанкинг, LOCK-R reasoning, Kaspersky MLAD ICS |
| R44 | 4 | AI EMR ассистент, LoRA эмбеддинги, Yandex LLM eval, LangGraph агенты |
| R45 | 4 | MWS Vision Bench, MOEX DistilBERT, Avito Mistral RU, LLM Observability |
| R46 | 4 | Coordination Harness, Telecom Classifier, Code MCP, AQLM.rs браузер |
| R47 | 4 | LLM Judge образование, SENTINEL безопасность, MTS code review, Temporal KG |
| R48 | 4 | LLM медицина v3, Multimodal RAG v2, ML промышленность v2, Agent evaluation v2 |
| R49 | 4 | Finance RAG 4-head, GBNF constrained decoding, Self-hosted 4×4090, SAP Text2SQL |
| **Итого** | **200** | |

## Темы для Round 50

| Тема | Обоснование |
|------|-------------|
| LLM персонализация v3 | Новые подходы персонализации: user memory, preference learning, adaptive prompting |
| AI для контент-модерации | Автоматическая модерация: классификация токсичности, фейков, спама с LLM |
| LLM для научных вычислений | Символическое программирование + LLM, математические рассуждения, физические симуляции |
| Retrieval-Augmented Fine-Tuning (RAFT) | Сочетание fine-tuning + RAG: модель обучается работать с retrieved контекстом |


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
