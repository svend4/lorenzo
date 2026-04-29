# Майндмап репозитория Lorenzo

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
    knowledge_space[knowledge space]
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
  AgentFS -->|reference| knowledge_space
  Yodoca -->|consolidation| NGT_Memory
  NGT_Memory -->|recall→discovery| Svyazi
  LiteParse -->|evidence| Legal_RAG
  Legal_RAG -->|proof→card| CardIndex
  mclaude -->|coordination| AI_Factory
  AI_Factory -->|orchestration| Rufler
  Rufler -->|self-improve| AutoResearch
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

<!-- backlinks-auto -->
## Упоминается в

- [docs](README.md)
- [Все таблицы репозитория](TABLES.md)
- [Домен: немецкое социальное право](03-technology-combinations/04-sozialrecht-domain.md)
- [Карта репозитория Lorenzo](SITEMAP.md)

<!-- related-auto -->
## Связанные документы

- [Нарратив проекта Lorenzo](NARRATIVE.md) _21%_
- [13 Contacts](01-svyazi/13-contacts.md) _17%_
- [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) _17%_
- [Контактная стратегия и узкие вопросы для авторов](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) _17%_
- [Матрица компонентов Svyazi 2.0](COMPONENT_MATRIX.md) _17%_
- [Граф связей проектов](GRAPH.md) _17%_
- [Сеть проектов и авторов](NETWORK.md) _17%_
- [Приоритеты файлов](PRIORITIES.md) _17%_
