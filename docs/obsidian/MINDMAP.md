---
title: "Майндмап репозитория Lorenzo"
tags:
  - general
date: 2026-05-10
---

# Майндмап репозитория Lorenzo

<!-- toc-auto -->
## Contents

- [Структура разделов](#структура-разделов)
- [Поток данных между проектами](#поток-данных-между-проектами)
- [Легенда](#легенда)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> knowledge-space[knowledge-space]
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




## Структура разделов

```mermaid
mindmap
  root((Lorenzo Repository))
    🧠 **Svyazi 2.0**
      CardIndex
      Evidence Envelope
      Memory Write Policy
      Ансамбли
      MVP 12-18 дней
      Безопасность
    💼 **Anthropic Vacancies**
      Research & ML
      GTM Sales
      Trust & Safety
      Inference Infra
      Product Eng
      Карьерный маппинг
    ⚙️ **Tech Combinations**
      Агентный роутинг
      Граф знаний
      Local-first
      Sozialrecht
      Бенчмарки
    🤝 **AI Collaborations**
      Knowledge OS
      Forensic RAG
      Agent Teams
      Security Runtime
      Web Intelligence
    📦 **Habr Projects**
      Yodoca
      NGT Memory
      MemNet
      knowledge-space
      AgentFS
      Wikontic
```

## Поток данных между проектами

```mermaid
flowchart LR
  subgraph INGEST
    Svyazi[Svyazi]
    CardIndex[CardIndex]
    Firecrawl[Firecrawl]
  end
  subgraph KNOWLEDGE
    AgentFS[AgentFS]
    knowledge-space[knowledge-space]
  end
  subgraph MEMORY
    Yodoca[Yodoca]
    NGT_Memory[NGT Memory]
    MemNet[MemNet]
  end
  subgraph RAG
    LiteParse[LiteParse]
    Legal_RAG[Legal RAG]
    Hybrid_RAG[Hybrid RAG]
  end
  subgraph ORCHESTRATION
    mclaude[mclaude]
    AI_Factory[AI Factory]
    Rufler[Rufler]
  end
  subgraph SECURITY
    LiteLLM[LiteLLM]
    SENTINEL[SENTINEL]
    Tool_Search[Tool Search]
  end
  Svyazi -->|ingest→index| CardIndex
  CardIndex -->|storage| AgentFS
  AgentFS -->|reference| knowledge-space
  Yodoca -->|consolidation| NGT_Memory
  NGT_Memory -->|recall→discovery| Svyazi
  LiteParse -->|evidence| Legal_RAG
  Legal_RAG -->|proof→card| CardIndex
  mclaude -->|coordination| AI_Factory
  AI_Factory -->|orchestration| Rufler
  Rufler -->|self-improvement| AutoResearch
  LiteLLM -->|gateway→guard| SENTINEL
  Tool_Search -->|lazy-load| LiteLLM
```

## Легенда

| Слой | Проекты |
|------|---------|
| Ingestion | Svyazi, CardIndex, Firecrawl |
| Knowledge | AgentFS, knowledge-space |
| Memory | Yodoca, NGT Memory, MemNet |
| RAG | LiteParse, Legal RAG, Hybrid RAG, Graph RAG |
| Orchestration | mclaude, AI Factory, Rufler, AutoResearch |
| Security | LiteLLM, SENTINEL, Tool Search, Auto AI Router |
| Sync | Yjs, Automerge |

<!-- see-also -->

---

## Смотрите также
- [[GLOSSARY]]
- [[CONTACT_PRIORITY]]
- [[GRAPH]]
- [[NETWORK]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

