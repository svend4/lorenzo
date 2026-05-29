---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Round 22 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Graph RAG 96.7% (1003064, 2025) — 5 техник из научных статей: HippoRAG PageRank, RAPTOR иерархия, Self-RAG IsRel, CRAG corrective, Microsoft GraphRAG communities.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** Claude+YandexGPT анализ договоров, LLM в AppSec (Solar Security), Self-hosted AI стек, Graph RAG 96.7%

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Claude + YandexGPT ensemble для договоров — 2.5× рисков | независимый разработчик | orchestration / analytics | `projects/claude-yandexgpt-contract-analysis.md` |
| LLM в AppSec — Solar Security: DerAI vs общие LLM | Solar Security | orchestration / quality | `projects/llm-appsec-solar-security.md` |
| Self-hosted AI стек: n8n + Ollama + Open WebUI + Docker | независимый разработчик | orchestration / memory | `projects/self-hosted-ai-stack-docker.md` |
| Graph RAG 96.7% — 5 техник + Neo4j + cascading fallback | независимый исследователь | knowledge / orchestration | `projects/graph-rag-96-percent-production.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Graph RAG Neo4j + FRIDA (R18) | knowledge stack | CONCEPT_GRAPH.md → Neo4j PhraseNode/PassageNode + FRIDA = 96%+ Q&A по Lorenzo | ⭐⭐⭐⭐⭐ |
| Self-hosted + Jay Guard (R21) | privacy stack | 100% локальный AI: LLM + анонимизация ПД = корпоративный compliance без облака | ⭐⭐⭐⭐⭐ |
| Contract Analysis + Docling (R19) | legal ingestion | PDF договор → Docling таблицы → Claude full-context → 2.5× больше рисков | ⭐⭐⭐⭐ |
| AppSec + AI Review (R15) + LLM Tests (R20) | quality gate | Semgrep SAST + DerAI triage + mutation tests = три слоя quality defense | ⭐⭐⭐⭐ |
| Self-hosted n8n + improve_workflow_v2 | automation | n8n визуальные пайплайны заменяют/дополняют improve_workflow_v2.py | ⭐⭐⭐⭐ |

## Главные находки раунда

**Contract Analysis** (992074, февраль 2026) — Claude vs YandexGPT на одном договоре: 2.5× больше рисков. Причина: 200K контекст = весь договор (vs чанки), юридическое рассуждение = применение ст. ГК РФ (1%/день = 365%/год → хищнические условия). Паттерн ensemble: YandexGPT (быстрый scan) → Claude только для договоров >1М рублей. Для Lorenzo: Document Risk Analysis паттерн.

**LLM in AppSec** (1031718, май 2026) — Solar Security: 20 приложений Java+Python, общие LLM (GPT-4o 67%, Claude 71%) против специализированной DerAI (89% точность). Вывод: общие LLM непригодны для SAST-сортировки — нужны специализированные, обученные на SAST-разметках. AI работает для triage, fix-patch, объяснений; не заменяет SAST. Vibe coding → security CI/CD layer необходим.

**Self-hosted AI stack** (973456, декабрь 2025) — n8n (400+ интеграций) + Ollama + Open WebUI + pgvector + Docker Compose. Бенчмарки декабрь 2025: qwen2.5:14b лучший баланс, qwen2.5:7b — скорость + RU. Coolify для управления деплоем. Self-hosted дешевле при >500K токенов/день + 100% контроль данных (ФЗ-152). n8n заменяет improve_workflow_v2.py для визуальной автоматизации.

**Graph RAG 96.7%** (1003064, 2025) — 5 техник из научных статей: HippoRAG PageRank, RAPTOR иерархия, Self-RAG IsRel, CRAG corrective, Microsoft GraphRAG communities. Neo4j: PhraseNode (entity+embedding+pagerank) + PassageNode (chunk+embedding). Cascading fallback: vector → cypher → hybrid → comprehensive → full_doc. 96.7% vs Microsoft GraphRAG 88% (+8.7%). Прямой апгрейд для Lorenzo CONCEPT_GRAPH.md → Neo4j.

## Сводная карта R01–R22

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

**Итого: 92 проекта, 48+ авторов**

## Что осталось на R23

- **LLM для HR и рекрутинга** — CV-анализ, сопоставление вакансий, bias detection
- **Conversational AI / диалоговые системы** — production chatbot архитектуры, state management, memory для долгих диалогов
- **AI для бизнес-процессов (BPA)** — RPA + LLM: автоматизация рутины (не только тексты, но и GUI automation)
- **Prompt injection защита** — атаки через внешние данные, защита production агентов, jailbreak-resistant архитектуры


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
