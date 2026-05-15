---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Round 17 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> CoT Illusion (1020016, апрель 2026) — экспериментальное опровержение: LLM игнорирует факты, CoT ухудшает фактические задачи.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** CoT Illusion (reasoning research), LLM-Wiki (второй мозг для агента), Sberbank Knowledge Graph, LLM as DBA (PostgresPro)

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| CoT Illusion Research | независимый исследователь | research / quality / orchestration | `projects/cot-illusion-research.md` |
| LLM-Wiki Second Brain | независимый разработчик | knowledge / memory / methodology | `projects/llm-wiki-second-brain.md` |
| Sberbank Knowledge Graph Search | Сбербанк | knowledge / search / graph | `projects/sberbank-knowledge-graph-search.md` |
| LLM as DBA (PostgresPro) | PostgresPro | analytics / orchestration / database | `projects/llm-as-dba-postgrespro.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| LLM-Wiki + Lorenzo architecture | весь стек | Lorenzo IS a LLM-Wiki: CLAUDE.md=AGENTS.md, improve_*.py=Ingest/Query/Lint | ⭐⭐⭐⭐⭐ |
| Sberbank KG + improve_concept_graph | Lorenzo graph | CONCEPT_GRAPH.md → Apache Jena Fuseki → SPARQL Knowledge Panel для Svyazi | ⭐⭐⭐⭐⭐ |
| CoT Illusion + DSPy (R14) | prompt optimization | DSPy тестирует CoT vs structured extraction → доказательная оптимизация промптов | ⭐⭐⭐⭐ |
| LLM DBA + Text2SQL (R15) | SQL agents | Schema Extractor (R17) + CoT+RAG (R15) = полный enterprise SQL-агент | ⭐⭐⭐⭐ |
| Sberbank KG + GraphRAG (R09) | knowledge systems | R09 pipeline + Apache Jena Fuseki = production Knowledge Graph стек | ⭐⭐⭐⭐ |

## Главные находки раунда

**LLM-Wiki** (1031970, май 2026) — смена парадигмы: «Obsidian = IDE, LLM = программист, wiki = кодовая база». AGENTS.md как universal interface работает в Claude Code, Codex, Cursor без изменений. GitHub vault с реализацией. **Lorenzo is a LLM-Wiki for Svyazi** — статья даёт язык и теоретическую рамку для того, что Lorenzo делает.

**CoT Illusion** (1020016, апрель 2026) — экспериментальное опровержение: LLM игнорирует факты, CoT ухудшает фактические задачи. Практический вывод: в `improve_llm_qa.py` и `improve_llm_enrich.py` заменить свободный CoT на structured extraction + citations. Комбинация с DSPy (R14) = доказательная оптимизация.

**Sberbank KG** (1029580, апрель 2026) — production Knowledge Panel через Apache Jena Fuseki (RDF) + Go API + LLM агент. 5-стадийный workflow. Гибридный поиск: граф + вектор. LightRAG как open-source альтернатива. Прямой путь от `improve_concept_graph.py` (Lorenzo) к SPARQL-поиску.

**LLM as DBA** (PostgresPro, 907614) — Schema Extractor Agent: 500+ таблиц → 3-4 релевантных (−85-90% токенов). Экосистема агентов: Schema, Query, Explain, Index, Vacuum. Дополняет Text2SQL X5Tech (R15): X5Tech = техники генерации SQL, PostgresPro = intelligent filtering схемы.

## Сводная карта R01–R17

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

**Итого: 72 проекта, 38+ авторов**

## Что осталось на R18

- **Agentic RAG** — агенты, управляющие процессом retrieval (не пассивный RAG, а active retrieval)
- **Синтетические данные для обучения** — генерация датасетов через LLM для fine-tuning
- **AI для DevOps / SRE** — автоматическое расследование инцидентов, runbook-агенты
- **Русскоязычные embedding-модели** — sentence transformers для русского языка, сравнение


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
