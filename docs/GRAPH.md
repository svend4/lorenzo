# Граф связей проектов

Рёбра = совместные упоминания в одном файле (≥ 2 раз).

```mermaid
graph TD
  subgraph ingestion[INGESTION]
    Svyazi[Svyazi]
    CardIndex[CardIndex]
    Firecrawl[Firecrawl]
  end
  subgraph knowledge[KNOWLEDGE]
    AgentFS[AgentFS]
    knowledge_space[knowledge-space]
    Wikontic[Wikontic]
  end
  subgraph memory[MEMORY]
    Yodoca[Yodoca]
    NGT_Memory[NGT Memory]
    MemNet[MemNet]
  end
  subgraph rag[RAG]
    LiteParse[LiteParse]
    Legal_RAG[Legal RAG]
    Hybrid_RAG[Hybrid RAG]
    Graph_RAG[Graph RAG]
  end
  subgraph orchestration[ORCHESTRATION]
    mclaude[mclaude]
    AI_Factory[AI Factory]
    Rufler[Rufler]
    AutoResearch[AutoResearch]
  end
  subgraph security[SECURITY]
    SENTINEL[SENTINEL]
    LiteLLM[LiteLLM]
    Auto_AI_Router[Auto AI Router]
    Tool_Search[Tool Search]
  end
  subgraph sync[SYNC]
    Yjs[Yjs]
    Automerge[Automerge]
  end
  Svyazi -- 65 --> Yodoca
  Svyazi -- 63 --> CardIndex
  Svyazi -- 61 --> AgentFS
  CardIndex -- 56 --> AgentFS
  AgentFS -- 54 --> Yodoca
  CardIndex -- 52 --> Yodoca
  Svyazi -- 51 --> knowledge_space
  Svyazi -- 50 --> AI_Factory
  Svyazi -- 50 --> LiteParse
  Svyazi -- 47 --> mclaude
  Svyazi -- 47 --> Rufler
  Svyazi -- 47 --> NGT_Memory
  Svyazi -- 46 --> SENTINEL
  AgentFS -- 46 --> knowledge_space
  AgentFS -- 46 --> AI_Factory
  AI_Factory -- 46 --> Yodoca
  CardIndex -- 45 --> Rufler
  AgentFS -- 45 --> Rufler
  AgentFS -- 45 --> SENTINEL
  CardIndex -- 44 --> knowledge_space
  CardIndex -- 44 --> AI_Factory
  AgentFS -- 44 --> LiteParse
  mclaude -- 44 --> AI_Factory
  mclaude -- 44 --> Yodoca
  Rufler -- 44 --> Yodoca
  CardIndex -- 43 --> LiteParse
  LiteParse -- 43 --> Yodoca
  CardIndex -- 42 --> mclaude
  CardIndex -- 42 --> SENTINEL
  AgentFS -- 42 --> mclaude
  knowledge_space -- 42 --> Yodoca
  AI_Factory -- 41 --> LiteParse
  Yodoca -- 41 --> NGT_Memory
  Yodoca -- 41 --> SENTINEL
  mclaude -- 40 --> LiteParse
  AI_Factory -- 40 --> Rufler
  mclaude -- 39 --> Rufler
  Rufler -- 39 --> LiteParse
  Svyazi -- 38 --> Auto_AI_Router
  CardIndex -- 38 --> NGT_Memory
  knowledge_space -- 38 --> NGT_Memory
  AI_Factory -- 38 --> NGT_Memory
  Rufler -- 38 --> SENTINEL
  knowledge_space -- 37 --> AI_Factory
  knowledge_space -- 37 --> LiteParse
  mclaude -- 37 --> NGT_Memory
  AI_Factory -- 37 --> SENTINEL
  LiteParse -- 37 --> SENTINEL
  AgentFS -- 36 --> NGT_Memory
  knowledge_space -- 36 --> mclaude
  knowledge_space -- 36 --> Rufler
  SENTINEL -- 35 --> Auto_AI_Router
  knowledge_space -- 34 --> SENTINEL
  Svyazi -- 33 --> Tool_Search
  AgentFS -- 33 --> Auto_AI_Router
  mclaude -- 33 --> SENTINEL
  LiteParse -- 33 --> NGT_Memory
  LiteParse -- 33 --> Auto_AI_Router
  SENTINEL -- 33 --> Tool_Search
  LiteLLM -- 33 --> Auto_AI_Router
  Svyazi -- 32 --> Legal_RAG
  Svyazi -- 32 --> LiteLLM
  CardIndex -- 32 --> Auto_AI_Router
  AgentFS -- 32 --> Tool_Search
  Yodoca -- 32 --> Auto_AI_Router
  AI_Factory -- 31 --> Auto_AI_Router
  Rufler -- 31 --> NGT_Memory
  LiteParse -- 31 --> Legal_RAG
  SENTINEL -- 31 --> LiteLLM
  Svyazi -- 30 --> MemNet
  CardIndex -- 30 --> Tool_Search
  NGT_Memory -- 30 --> SENTINEL
  LiteLLM -- 30 --> Tool_Search
  Auto_AI_Router -- 30 --> Tool_Search
  Svyazi -- 29 --> AutoResearch
  AgentFS -- 29 --> LiteLLM
  mclaude -- 29 --> Auto_AI_Router
  LiteParse -- 29 --> LiteLLM
  LiteParse -- 29 --> Tool_Search
  Yodoca -- 29 --> Tool_Search
  NGT_Memory -- 29 --> Auto_AI_Router
  Svyazi -- 28 --> Graph_RAG
  CardIndex -- 28 --> LiteLLM
  AgentFS -- 28 --> Legal_RAG
  AI_Factory -- 28 --> LiteLLM
  AI_Factory -- 28 --> Tool_Search
  Svyazi -- 27 --> Hybrid_RAG
  CardIndex -- 27 --> Legal_RAG
  knowledge_space -- 27 --> Auto_AI_Router
  Rufler -- 27 --> Auto_AI_Router
  Legal_RAG -- 27 --> Yodoca
  Legal_RAG -- 27 --> SENTINEL
  Legal_RAG -- 27 --> Auto_AI_Router
  Yodoca -- 27 --> MemNet
  Yodoca -- 27 --> LiteLLM
  CardIndex -- 26 --> Hybrid_RAG
  AgentFS -- 26 --> AutoResearch
  mclaude -- 26 --> Legal_RAG
  AI_Factory -- 26 --> Legal_RAG
  AI_Factory -- 26 --> AutoResearch
  Rufler -- 26 --> Tool_Search
  LiteParse -- 26 --> Hybrid_RAG
  LiteParse -- 26 --> Graph_RAG
  Yodoca -- 26 --> AutoResearch
  CardIndex -- 25 --> AutoResearch
  AgentFS -- 25 --> Hybrid_RAG
  mclaude -- 25 --> LiteLLM
  mclaude -- 25 --> Tool_Search
  LiteParse -- 25 --> AutoResearch
  Legal_RAG -- 25 --> Graph_RAG
  Hybrid_RAG -- 25 --> Yodoca
  Graph_RAG -- 25 --> SENTINEL
  NGT_Memory -- 25 --> LiteLLM
  knowledge_space -- 24 --> Tool_Search
  AI_Factory -- 24 --> Hybrid_RAG
  Rufler -- 24 --> Legal_RAG
  Rufler -- 24 --> LiteLLM
  Legal_RAG -- 24 --> Hybrid_RAG
  Legal_RAG -- 24 --> NGT_Memory
  Hybrid_RAG -- 24 --> Auto_AI_Router
  Graph_RAG -- 24 --> Auto_AI_Router
  Yodoca -- 24 --> Wikontic
  Svyazi -- 23 --> Wikontic
  CardIndex -- 23 --> Graph_RAG
  AgentFS -- 23 --> Graph_RAG
  knowledge_space -- 23 --> Legal_RAG
  knowledge_space -- 23 --> LiteLLM
  mclaude -- 23 --> Hybrid_RAG
  mclaude -- 23 --> AutoResearch
  Rufler -- 23 --> AutoResearch
  Legal_RAG -- 23 --> LiteLLM
  Hybrid_RAG -- 23 --> NGT_Memory
  Hybrid_RAG -- 23 --> SENTINEL
  Hybrid_RAG -- 23 --> LiteLLM
  NGT_Memory -- 23 --> Tool_Search
  LiteParse -- 22 --> MemNet
  Legal_RAG -- 22 --> Tool_Search
  Graph_RAG -- 22 --> Yodoca
  NGT_Memory -- 22 --> AutoResearch
  Auto_AI_Router -- 22 --> AutoResearch
  CardIndex -- 21 --> MemNet
  AgentFS -- 21 --> MemNet
  knowledge_space -- 21 --> Hybrid_RAG
  knowledge_space -- 21 --> AutoResearch
  mclaude -- 21 --> Graph_RAG
  AI_Factory -- 21 --> Graph_RAG
  Rufler -- 21 --> Hybrid_RAG
  Hybrid_RAG -- 21 --> Tool_Search
  Graph_RAG -- 21 --> NGT_Memory
  SENTINEL -- 21 --> AutoResearch
  Svyazi -- 20 --> Yjs
  CardIndex -- 20 --> Yjs
  knowledge_space -- 20 --> Graph_RAG
  Hybrid_RAG -- 20 --> Graph_RAG
  Graph_RAG -- 20 --> LiteLLM
  MemNet -- 20 --> SENTINEL
  LiteLLM -- 20 --> AutoResearch
  knowledge_space -- 19 --> MemNet
  AI_Factory -- 19 --> MemNet
  Rufler -- 19 --> Graph_RAG
  Rufler -- 19 --> MemNet
  Graph_RAG -- 19 --> Tool_Search
  Yodoca -- 19 --> Yjs
  CardIndex -- 18 --> Wikontic
  AgentFS -- 18 --> Yjs
  knowledge_space -- 18 --> Yjs
  mclaude -- 18 --> MemNet
  LiteParse -- 18 --> Yjs
  NGT_Memory -- 18 --> MemNet
  NGT_Memory -- 18 --> Yjs
  MemNet -- 18 --> Auto_AI_Router
  MemNet -- 18 --> Wikontic
  Tool_Search -- 18 --> AutoResearch
  AI_Factory -- 17 --> Yjs
  AutoResearch -- 17 --> Yjs
  Svyazi -- 16 --> Automerge
  CardIndex -- 16 --> Automerge
  knowledge_space -- 16 --> Wikontic
  mclaude -- 16 --> Yjs
  Rufler -- 16 --> Yjs
  Hybrid_RAG -- 16 --> AutoResearch
  Yodoca -- 16 --> Automerge
  NGT_Memory -- 16 --> Wikontic
  NGT_Memory -- 16 --> Automerge
  Auto_AI_Router -- 16 --> Yjs
  Yjs -- 16 --> Automerge
  AgentFS -- 15 --> Automerge
  knowledge_space -- 15 --> Automerge
  AI_Factory -- 15 --> Automerge
  Rufler -- 15 --> Automerge
  LiteParse -- 15 --> Automerge
  Legal_RAG -- 15 --> MemNet
  Hybrid_RAG -- 15 --> Yjs
  Graph_RAG -- 15 --> MemNet
  SENTINEL -- 15 --> Yjs
  AutoResearch -- 15 --> Automerge
  Svyazi -- 14 --> Firecrawl
  CardIndex -- 14 --> Firecrawl
  AgentFS -- 14 --> Wikontic
  mclaude -- 14 --> Automerge
  Legal_RAG -- 14 --> AutoResearch
  Hybrid_RAG -- 14 --> Automerge
  Graph_RAG -- 14 --> AutoResearch
  Yodoca -- 14 --> Firecrawl
  MemNet -- 14 --> LiteLLM
  MemNet -- 14 --> Tool_Search
  LiteLLM -- 14 --> Yjs
  LiteLLM -- 14 --> Automerge
  Auto_AI_Router -- 14 --> Automerge
  AgentFS -- 13 --> Firecrawl
  Rufler -- 13 --> Firecrawl
  LiteParse -- 13 --> Wikontic
  Legal_RAG -- 13 --> Yjs
  Hybrid_RAG -- 13 --> MemNet
  Graph_RAG -- 13 --> Yjs
  MemNet -- 13 --> AutoResearch
  SENTINEL -- 13 --> Wikontic
  SENTINEL -- 13 --> Firecrawl
  SENTINEL -- 13 --> Automerge
  knowledge_space -- 12 --> Firecrawl
  AI_Factory -- 12 --> Wikontic
  Rufler -- 12 --> Wikontic
  MemNet -- 12 --> Yjs
  Tool_Search -- 12 --> Yjs
  Tool_Search -- 12 --> Automerge
  Legal_RAG -- 11 --> Automerge
  Graph_RAG -- 11 --> Automerge
  Wikontic -- 11 --> Firecrawl
  mclaude -- 10 --> Wikontic
  AI_Factory -- 10 --> Firecrawl
  LiteParse -- 10 --> Firecrawl
  MemNet -- 10 --> Firecrawl
  AutoResearch -- 10 --> Wikontic
  Graph_RAG -- 9 --> Wikontic
  MemNet -- 9 --> Automerge
  Auto_AI_Router -- 9 --> Wikontic
  Tool_Search -- 9 --> Wikontic
  Wikontic -- 9 --> Yjs
  mclaude -- 8 --> Firecrawl
  Hybrid_RAG -- 8 --> Wikontic
  Hybrid_RAG -- 8 --> Firecrawl
  NGT_Memory -- 8 --> Firecrawl
  LiteLLM -- 8 --> Wikontic
  LiteLLM -- 8 --> Firecrawl
  Auto_AI_Router -- 8 --> Firecrawl
  Tool_Search -- 8 --> Firecrawl
  AutoResearch -- 8 --> Firecrawl
  Firecrawl -- 8 --> Yjs
  Firecrawl -- 8 --> Automerge
  Legal_RAG -- 7 --> Wikontic
  Legal_RAG -- 7 --> Firecrawl
  Graph_RAG -- 7 --> Firecrawl
  Wikontic -- 7 --> Automerge
```

## Топ совместных упоминаний

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 65 |
| **Svyazi** | **CardIndex** | 63 |
| **Svyazi** | **AgentFS** | 61 |
| **CardIndex** | **AgentFS** | 56 |
| **AgentFS** | **Yodoca** | 54 |
| **CardIndex** | **Yodoca** | 52 |
| **Svyazi** | **knowledge-space** | 51 |
| **Svyazi** | **AI Factory** | 50 |
| **Svyazi** | **LiteParse** | 50 |
| **Svyazi** | **mclaude** | 47 |
| **Svyazi** | **Rufler** | 47 |
| **Svyazi** | **NGT Memory** | 47 |
| **Svyazi** | **SENTINEL** | 46 |
| **AgentFS** | **knowledge-space** | 46 |
| **AgentFS** | **AI Factory** | 46 |
| **AI Factory** | **Yodoca** | 46 |
| **CardIndex** | **Rufler** | 45 |
| **AgentFS** | **Rufler** | 45 |
| **AgentFS** | **SENTINEL** | 45 |
| **CardIndex** | **knowledge-space** | 44 |
| **CardIndex** | **AI Factory** | 44 |
| **AgentFS** | **LiteParse** | 44 |
| **mclaude** | **AI Factory** | 44 |
| **mclaude** | **Yodoca** | 44 |
| **Rufler** | **Yodoca** | 44 |

## DOT-формат (Graphviz)

```dot
digraph lorenzo {
  rankdir=LR;
  node [shape=box];
  subgraph cluster_ingestion {
    label="INGESTION";
    Svyazi [label="Svyazi"];
    CardIndex [label="CardIndex"];
    Firecrawl [label="Firecrawl"];
  }
  subgraph cluster_knowledge {
    label="KNOWLEDGE";
    AgentFS [label="AgentFS"];
    knowledge_space [label="knowledge-space"];
    Wikontic [label="Wikontic"];
  }
  subgraph cluster_memory {
    label="MEMORY";
    Yodoca [label="Yodoca"];
    NGT_Memory [label="NGT Memory"];
    MemNet [label="MemNet"];
  }
  subgraph cluster_rag {
    label="RAG";
    LiteParse [label="LiteParse"];
    Legal_RAG [label="Legal RAG"];
    Hybrid_RAG [label="Hybrid RAG"];
    Graph_RAG [label="Graph RAG"];
  }
  subgraph cluster_orchestration {
    label="ORCHESTRATION";
    mclaude [label="mclaude"];
    AI_Factory [label="AI Factory"];
    Rufler [label="Rufler"];
    AutoResearch [label="AutoResearch"];
  }
  subgraph cluster_security {
    label="SECURITY";
    SENTINEL [label="SENTINEL"];
    LiteLLM [label="LiteLLM"];
    Auto_AI_Router [label="Auto AI Router"];
    Tool_Search [label="Tool Search"];
  }
  subgraph cluster_sync {
    label="SYNC";
    Yjs [label="Yjs"];
    Automerge [label="Automerge"];
  }
  Svyazi -> CardIndex [label="63"];
  Svyazi -> AgentFS [label="61"];
  Svyazi -> knowledge_space [label="51"];
  Svyazi -> mclaude [label="47"];
  Svyazi -> AI_Factory [label="50"];
  Svyazi -> Rufler [label="47"];
  Svyazi -> LiteParse [label="50"];
  Svyazi -> Legal_RAG [label="32"];
  Svyazi -> Hybrid_RAG [label="27"];
  Svyazi -> Graph_RAG [label="28"];
  Svyazi -> Yodoca [label="65"];
  Svyazi -> NGT_Memory [label="47"];
  Svyazi -> MemNet [label="30"];
  Svyazi -> SENTINEL [label="46"];
  Svyazi -> LiteLLM [label="32"];
  Svyazi -> Auto_AI_Router [label="38"];
  Svyazi -> Tool_Search [label="33"];
  Svyazi -> AutoResearch [label="29"];
  Svyazi -> Wikontic [label="23"];
  Svyazi -> Firecrawl [label="14"];
  Svyazi -> Yjs [label="20"];
  Svyazi -> Automerge [label="16"];
  CardIndex -> AgentFS [label="56"];
  CardIndex -> knowledge_space [label="44"];
  CardIndex -> mclaude [label="42"];
  CardIndex -> AI_Factory [label="44"];
  CardIndex -> Rufler [label="45"];
  CardIndex -> LiteParse [label="43"];
  CardIndex -> Legal_RAG [label="27"];
  CardIndex -> Hybrid_RAG [label="26"];
  CardIndex -> Graph_RAG [label="23"];
  CardIndex -> Yodoca [label="52"];
  CardIndex -> NGT_Memory [label="38"];
  CardIndex -> MemNet [label="21"];
  CardIndex -> SENTINEL [label="42"];
  CardIndex -> LiteLLM [label="28"];
  CardIndex -> Auto_AI_Router [label="32"];
  CardIndex -> Tool_Search [label="30"];
  CardIndex -> AutoResearch [label="25"];
  CardIndex -> Wikontic [label="18"];
  CardIndex -> Firecrawl [label="14"];
  CardIndex -> Yjs [label="20"];
  CardIndex -> Automerge [label="16"];
  AgentFS -> knowledge_space [label="46"];
  AgentFS -> mclaude [label="42"];
  AgentFS -> AI_Factory [label="46"];
  AgentFS -> Rufler [label="45"];
  AgentFS -> LiteParse [label="44"];
  AgentFS -> Legal_RAG [label="28"];
  AgentFS -> Hybrid_RAG [label="25"];
  AgentFS -> Graph_RAG [label="23"];
  AgentFS -> Yodoca [label="54"];
  AgentFS -> NGT_Memory [label="36"];
  AgentFS -> MemNet [label="21"];
  AgentFS -> SENTINEL [label="45"];
  AgentFS -> LiteLLM [label="29"];
  AgentFS -> Auto_AI_Router [label="33"];
  AgentFS -> Tool_Search [label="32"];
  AgentFS -> AutoResearch [label="26"];
  AgentFS -> Wikontic [label="14"];
  AgentFS -> Firecrawl [label="13"];
  AgentFS -> Yjs [label="18"];
  AgentFS -> Automerge [label="15"];
  knowledge_space -> mclaude [label="36"];
  knowledge_space -> AI_Factory [label="37"];
  knowledge_space -> Rufler [label="36"];
  knowledge_space -> LiteParse [label="37"];
  knowledge_space -> Legal_RAG [label="23"];
  knowledge_space -> Hybrid_RAG [label="21"];
  knowledge_space -> Graph_RAG [label="20"];
  knowledge_space -> Yodoca [label="42"];
  knowledge_space -> NGT_Memory [label="38"];
  knowledge_space -> MemNet [label="19"];
  knowledge_space -> SENTINEL [label="34"];
  knowledge_space -> LiteLLM [label="23"];
  knowledge_space -> Auto_AI_Router [label="27"];
  knowledge_space -> Tool_Search [label="24"];
  knowledge_space -> AutoResearch [label="21"];
  knowledge_space -> Wikontic [label="16"];
  knowledge_space -> Firecrawl [label="12"];
  knowledge_space -> Yjs [label="18"];
  knowledge_space -> Automerge [label="15"];
  mclaude -> AI_Factory [label="44"];
  mclaude -> Rufler [label="39"];
  mclaude -> LiteParse [label="40"];
  mclaude -> Legal_RAG [label="26"];
  mclaude -> Hybrid_RAG [label="23"];
  mclaude -> Graph_RAG [label="21"];
  mclaude -> Yodoca [label="44"];
  mclaude -> NGT_Memory [label="37"];
  mclaude -> MemNet [label="18"];
  mclaude -> SENTINEL [label="33"];
  mclaude -> LiteLLM [label="25"];
  mclaude -> Auto_AI_Router [label="29"];
  mclaude -> Tool_Search [label="25"];
  mclaude -> AutoResearch [label="23"];
  mclaude -> Wikontic [label="10"];
  mclaude -> Firecrawl [label="8"];
  mclaude -> Yjs [label="16"];
  mclaude -> Automerge [label="14"];
  AI_Factory -> Rufler [label="40"];
  AI_Factory -> LiteParse [label="41"];
  AI_Factory -> Legal_RAG [label="26"];
  AI_Factory -> Hybrid_RAG [label="24"];
  AI_Factory -> Graph_RAG [label="21"];
  AI_Factory -> Yodoca [label="46"];
  AI_Factory -> NGT_Memory [label="38"];
  AI_Factory -> MemNet [label="19"];
  AI_Factory -> SENTINEL [label="37"];
  AI_Factory -> LiteLLM [label="28"];
  AI_Factory -> Auto_AI_Router [label="31"];
  AI_Factory -> Tool_Search [label="28"];
  AI_Factory -> AutoResearch [label="26"];
  AI_Factory -> Wikontic [label="12"];
  AI_Factory -> Firecrawl [label="10"];
  AI_Factory -> Yjs [label="17"];
  AI_Factory -> Automerge [label="15"];
  Rufler -> LiteParse [label="39"];
  Rufler -> Legal_RAG [label="24"];
  Rufler -> Hybrid_RAG [label="21"];
  Rufler -> Graph_RAG [label="19"];
  Rufler -> Yodoca [label="44"];
  Rufler -> NGT_Memory [label="31"];
  Rufler -> MemNet [label="19"];
  Rufler -> SENTINEL [label="38"];
  Rufler -> LiteLLM [label="24"];
  Rufler -> Auto_AI_Router [label="27"];
  Rufler -> Tool_Search [label="26"];
  Rufler -> AutoResearch [label="23"];
  Rufler -> Wikontic [label="12"];
  Rufler -> Firecrawl [label="13"];
  Rufler -> Yjs [label="16"];
  Rufler -> Automerge [label="15"];
  LiteParse -> Legal_RAG [label="31"];
  LiteParse -> Hybrid_RAG [label="26"];
  LiteParse -> Graph_RAG [label="26"];
  LiteParse -> Yodoca [label="43"];
  LiteParse -> NGT_Memory [label="33"];
  LiteParse -> MemNet [label="22"];
  LiteParse -> SENTINEL [label="37"];
  LiteParse -> LiteLLM [label="29"];
  LiteParse -> Auto_AI_Router [label="33"];
  LiteParse -> Tool_Search [label="29"];
  LiteParse -> AutoResearch [label="25"];
  LiteParse -> Wikontic [label="13"];
  LiteParse -> Firecrawl [label="10"];
  LiteParse -> Yjs [label="18"];
  LiteParse -> Automerge [label="15"];
  Legal_RAG -> Hybrid_RAG [label="24"];
  Legal_RAG -> Graph_RAG [label="25"];
  Legal_RAG -> Yodoca [label="27"];
  Legal_RAG -> NGT_Memory [label="24"];
  Legal_RAG -> MemNet [label="15"];
  Legal_RAG -> SENTINEL [label="27"];
  Legal_RAG -> LiteLLM [label="23"];
  Legal_RAG -> Auto_AI_Router [label="27"];
  Legal_RAG -> Tool_Search [label="22"];
  Legal_RAG -> AutoResearch [label="14"];
  Legal_RAG -> Wikontic [label="7"];
  Legal_RAG -> Firecrawl [label="7"];
  Legal_RAG -> Yjs [label="13"];
  Legal_RAG -> Automerge [label="11"];
  Hybrid_RAG -> Graph_RAG [label="20"];
  Hybrid_RAG -> Yodoca [label="25"];
  Hybrid_RAG -> NGT_Memory [label="23"];
  Hybrid_RAG -> MemNet [label="13"];
  Hybrid_RAG -> SENTINEL [label="23"];
  Hybrid_RAG -> LiteLLM [label="23"];
  Hybrid_RAG -> Auto_AI_Router [label="24"];
  Hybrid_RAG -> Tool_Search [label="21"];
  Hybrid_RAG -> AutoResearch [label="16"];
  Hybrid_RAG -> Wikontic [label="8"];
  Hybrid_RAG -> Firecrawl [label="8"];
  Hybrid_RAG -> Yjs [label="15"];
  Hybrid_RAG -> Automerge [label="14"];
  Graph_RAG -> Yodoca [label="22"];
  Graph_RAG -> NGT_Memory [label="21"];
  Graph_RAG -> MemNet [label="15"];
  Graph_RAG -> SENTINEL [label="25"];
  Graph_RAG -> LiteLLM [label="20"];
  Graph_RAG -> Auto_AI_Router [label="24"];
  Graph_RAG -> Tool_Search [label="19"];
  Graph_RAG -> AutoResearch [label="14"];
  Graph_RAG -> Wikontic [label="9"];
  Graph_RAG -> Firecrawl [label="7"];
  Graph_RAG -> Yjs [label="13"];
  Graph_RAG -> Automerge [label="11"];
  Yodoca -> NGT_Memory [label="41"];
  Yodoca -> MemNet [label="27"];
  Yodoca -> SENTINEL [label="41"];
  Yodoca -> LiteLLM [label="27"];
  Yodoca -> Auto_AI_Router [label="32"];
  Yodoca -> Tool_Search [label="29"];
  Yodoca -> AutoResearch [label="26"];
  Yodoca -> Wikontic [label="24"];
  Yodoca -> Firecrawl [label="14"];
  Yodoca -> Yjs [label="19"];
  Yodoca -> Automerge [label="16"];
  NGT_Memory -> MemNet [label="18"];
  NGT_Memory -> SENTINEL [label="30"];
  NGT_Memory -> LiteLLM [label="25"];
  NGT_Memory -> Auto_AI_Router [label="29"];
  NGT_Memory -> Tool_Search [label="23"];
  NGT_Memory -> AutoResearch [label="22"];
  NGT_Memory -> Wikontic [label="16"];
  NGT_Memory -> Firecrawl [label="8"];
  NGT_Memory -> Yjs [label="18"];
  NGT_Memory -> Automerge [label="16"];
  MemNet -> SENTINEL [label="20"];
  MemNet -> LiteLLM [label="14"];
  MemNet -> Auto_AI_Router [label="18"];
  MemNet -> Tool_Search [label="14"];
  MemNet -> AutoResearch [label="13"];
  MemNet -> Wikontic [label="18"];
  MemNet -> Firecrawl [label="10"];
  MemNet -> Yjs [label="12"];
  MemNet -> Automerge [label="9"];
  SENTINEL -> LiteLLM [label="31"];
  SENTINEL -> Auto_AI_Router [label="35"];
  SENTINEL -> Tool_Search [label="33"];
  SENTINEL -> AutoResearch [label="21"];
  SENTINEL -> Wikontic [label="13"];
  SENTINEL -> Firecrawl [label="13"];
  SENTINEL -> Yjs [label="15"];
  SENTINEL -> Automerge [label="13"];
  LiteLLM -> Auto_AI_Router [label="33"];
  LiteLLM -> Tool_Search [label="30"];
  LiteLLM -> AutoResearch [label="20"];
  LiteLLM -> Wikontic [label="8"];
  LiteLLM -> Firecrawl [label="8"];
  LiteLLM -> Yjs [label="14"];
  LiteLLM -> Automerge [label="14"];
  Auto_AI_Router -> Tool_Search [label="30"];
  Auto_AI_Router -> AutoResearch [label="22"];
  Auto_AI_Router -> Wikontic [label="9"];
  Auto_AI_Router -> Firecrawl [label="8"];
  Auto_AI_Router -> Yjs [label="16"];
  Auto_AI_Router -> Automerge [label="14"];
  Tool_Search -> AutoResearch [label="18"];
  Tool_Search -> Wikontic [label="9"];
  Tool_Search -> Firecrawl [label="8"];
  Tool_Search -> Yjs [label="12"];
  Tool_Search -> Automerge [label="12"];
  AutoResearch -> Wikontic [label="10"];
  AutoResearch -> Firecrawl [label="8"];
  AutoResearch -> Yjs [label="17"];
  AutoResearch -> Automerge [label="15"];
  Wikontic -> Firecrawl [label="11"];
  Wikontic -> Yjs [label="9"];
  Wikontic -> Automerge [label="7"];
  Firecrawl -> Yjs [label="8"];
  Firecrawl -> Automerge [label="8"];
  Yjs -> Automerge [label="16"];
}
```

<!-- see-also -->

---

**Смотрите также:**
- [NETWORK](docs/NETWORK.md)
- [GLOSSARY](docs/GLOSSARY.md)
- [MINDMAP](docs/MINDMAP.md)
- [MISSING](docs/MISSING.md)

