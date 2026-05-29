---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Round 09 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> HyperCortex Mesh Protocol — единственный за 9 раундов проект с децентрализованной архитектурой.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** GraphRAG производство, децентрализованный AI, открытый coding agent, PKM-системы

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Graph RAG Pipeline (96.7%) | неизвестен | knowledge graph / RAG / Neo4j | `projects/graphrag-production.md` |
| HyperCortex Mesh Protocol (HMP) | @kagvi13 | decentralized / P2P / cognitive mesh | `projects/hypercortex-hmp.md` |
| OpenCode | @anomalyco | coding agent / CLI / multi-provider | `projects/opencode.md` |
| Obsidian CTO PKM | неизвестен | PKM / knowledge / PARA | `projects/obsidian-cto-pkm.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| GraphRAG + improve_passage_retrieval | Lorenzo corpus | BM25 → Knowledge Graph retrieval (96.7% vs ~70%) | ⭐⭐⭐⭐⭐ |
| GraphRAG + Natasha (R05) | improve_named_entity_index | Natasha NER → Neo4j PhraseNode (русские сущности в графе) | ⭐⭐⭐⭐⭐ |
| OpenCode + SocratiCode (R08) | Lorenzo scripts | LSP + граф зависимостей = максимальное понимание кодовой базы | ⭐⭐⭐⭐ |
| HMP + TRAIL spec (R04) | Lorenzo MCP servers | TRAIL внутри узлов, HMP между узлами — полная иерархия | ⭐⭐⭐⭐ |
| PARA + improve_obsidian | Lorenzo vault | Lorenzo-карточки в PARA-структуре → Obsidian PKM из коробки | ⭐⭐⭐ |

## Главная находка раунда

**Graph RAG Pipeline** — конкретный производственный рецепт для следующего уровня поиска в Lorenzo.  
PhraseNode (Natasha NER → PageRank) + PassageNode (чанки) + Cypher traversal → 96.7%.  
Это **прямой апгрейд** `improve_passage_retrieval.py` + `improve_concept_graph.py`.

**HyperCortex Mesh Protocol** — единственный за 9 раундов проект с **децентрализованной** архитектурой.  
Противовес всем предыдущим паттернам (оркестратор → агенты). GitHub подтверждён.

**OpenCode** — 126k звёзд, мультипровайдерный, работает с локальными моделями.  
Важно для Svyazi как независимость от Claude Code subscription.

## Сводная карта R01–R09

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

**Итого: 40 проектов, 22+ авторов**

## Что осталось на R10

- Rust-based AI tools (производительность: rivet, lumni и подобные)
- AI для работы с видео/стриминга в реальном времени (не генерация, а анализ)
- Workflow-движки нового поколения (не YAML, а граф или код)
- Self-hosted RAG-стеки «под ключ» (one-command deploy)


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
