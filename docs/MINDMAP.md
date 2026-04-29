# Майндмап репозитория Lorenzo

<!-- summary -->
> > 🎯 **Проблема:** Майндмап репозитория Lorenzo Contents - Структура разделов(структура-разделов) - Поток данных между проектами(поток-данных-между-проектами) - Легенда(легенда) Структура разделов По
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Майндмап репозитория Lorenzo Contents - Структура разделов(структура-разделов) - Поток данных между проектами(поток-данных-между-проектами) - Легенда(легенда) Структура разделов По
> 🏷️ **Ключевые слова:** `graph`, `glossary`, `entities`, `структура`, `разделов`, `поток`, `данных`, `между`
>


<!-- toc-auto -->
## Contents

- [Структура разделов](#структура-разделов)
- [Поток данных между проектами](#поток-данных-между-проектами)
- [Легенда](#легенда)


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

<!-- similar-docs -->

---

**Похожие документы:**
- [GLOSSARY](docs/GLOSSARY.md) (сходство 0.42)
- [GRAPH](docs/GRAPH.md) (сходство 0.18)
- [ENTITIES](docs/ENTITIES.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [GLOSSARY](docs/GLOSSARY.md)
- [GRAPH](docs/GRAPH.md)
- [NETWORK](docs/NETWORK.md)
- [ENTITIES](docs/ENTITIES.md)

