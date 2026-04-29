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
  Svyazi -- 74 --> Yodoca
  Svyazi -- 70 --> AgentFS
  AgentFS -- 64 --> Yodoca
  Svyazi -- 60 --> CardIndex
  Svyazi -- 58 --> SENTINEL
  Svyazi -- 58 --> Rufler
  CardIndex -- 56 --> AgentFS
  AgentFS -- 56 --> SENTINEL
  Svyazi -- 55 --> NGT_Memory
  AgentFS -- 54 --> Rufler
  Svyazi -- 53 --> knowledge_space
  Svyazi -- 53 --> LiteParse
  Svyazi -- 53 --> Auto_AI_Router
  CardIndex -- 52 --> Yodoca
  Rufler -- 52 --> Yodoca
  SENTINEL -- 51 --> Auto_AI_Router
  Yodoca -- 50 --> SENTINEL
  Rufler -- 50 --> SENTINEL
  Yodoca -- 50 --> NGT_Memory
  Svyazi -- 49 --> mclaude
  Svyazi -- 49 --> AI_Factory
  AgentFS -- 48 --> knowledge_space
  AgentFS -- 48 --> NGT_Memory
  CardIndex -- 46 --> knowledge_space
  AgentFS -- 46 --> LiteParse
  CardIndex -- 45 --> Rufler
  AgentFS -- 45 --> AI_Factory
  AgentFS -- 45 --> Auto_AI_Router
  AI_Factory -- 45 --> Yodoca
  knowledge_space -- 44 --> Yodoca
  CardIndex -- 44 --> AI_Factory
  mclaude -- 44 --> AI_Factory
  mclaude -- 44 --> Yodoca
  CardIndex -- 43 --> SENTINEL
  CardIndex -- 43 --> LiteParse
  AgentFS -- 43 --> mclaude
  knowledge_space -- 43 --> LiteParse
  mclaude -- 43 --> LiteParse
  Rufler -- 43 --> LiteParse
  LiteParse -- 43 --> Yodoca
  LiteParse -- 43 --> SENTINEL
  CardIndex -- 42 --> mclaude
  mclaude -- 42 --> Rufler
  Yodoca -- 42 --> Auto_AI_Router
  knowledge_space -- 41 --> Rufler
  CardIndex -- 41 --> NGT_Memory
  Rufler -- 41 --> Auto_AI_Router
  NGT_Memory -- 41 --> Auto_AI_Router
  LiteParse -- 40 --> Auto_AI_Router
  Svyazi -- 40 --> Legal_RAG
  Svyazi -- 40 --> Graph_RAG
  knowledge_space -- 40 --> mclaude
  knowledge_space -- 40 --> NGT_Memory
  AI_Factory -- 40 --> Rufler
  AI_Factory -- 40 --> LiteParse
  Rufler -- 40 --> NGT_Memory
  Graph_RAG -- 40 --> SENTINEL
  NGT_Memory -- 40 --> SENTINEL
  knowledge_space -- 39 --> SENTINEL
  mclaude -- 39 --> NGT_Memory
  Legal_RAG -- 39 --> SENTINEL
  Legal_RAG -- 39 --> Auto_AI_Router
  Graph_RAG -- 39 --> Auto_AI_Router
  knowledge_space -- 38 --> AI_Factory
  AI_Factory -- 38 --> NGT_Memory
  Legal_RAG -- 37 --> Graph_RAG
  mclaude -- 36 --> SENTINEL
  AI_Factory -- 36 --> SENTINEL
  LiteParse -- 36 --> Legal_RAG
  Svyazi -- 35 --> MemNet
  CardIndex -- 35 --> Auto_AI_Router
  AgentFS -- 35 --> Legal_RAG
  knowledge_space -- 35 --> Auto_AI_Router
  LiteParse -- 35 --> NGT_Memory
  LiteLLM -- 34 --> Auto_AI_Router
  AgentFS -- 34 --> Graph_RAG
  mclaude -- 34 --> Auto_AI_Router
  SENTINEL -- 33 --> Tool_Search
  AI_Factory -- 33 --> Auto_AI_Router
  Rufler -- 33 --> Legal_RAG
  Legal_RAG -- 33 --> Yodoca
  Svyazi -- 32 --> Tool_Search
  AgentFS -- 32 --> Tool_Search
  Rufler -- 32 --> Graph_RAG
  LiteParse -- 32 --> Graph_RAG
  Graph_RAG -- 32 --> Yodoca
  Svyazi -- 31 --> LiteLLM
  LiteLLM -- 31 --> Tool_Search
  Auto_AI_Router -- 31 --> Tool_Search
  Legal_RAG -- 31 --> NGT_Memory
  Graph_RAG -- 31 --> NGT_Memory
  Yodoca -- 31 --> MemNet
  SENTINEL -- 31 --> LiteLLM
  CardIndex -- 30 --> Tool_Search
  Svyazi -- 30 --> AutoResearch
  Yodoca -- 29 --> Wikontic
  Yodoca -- 29 --> Tool_Search
  LiteParse -- 29 --> LiteLLM
  LiteParse -- 29 --> Tool_Search
  AgentFS -- 29 --> LiteLLM
  AI_Factory -- 29 --> LiteLLM
  AI_Factory -- 29 --> Tool_Search
  CardIndex -- 28 --> Legal_RAG
  CardIndex -- 28 --> LiteLLM
  knowledge_space -- 28 --> Legal_RAG
  mclaude -- 28 --> Legal_RAG
  Svyazi -- 27 --> Wikontic
  AgentFS -- 27 --> AutoResearch
  AI_Factory -- 27 --> AutoResearch
  Rufler -- 27 --> Tool_Search
  Yodoca -- 27 --> LiteLLM
  Yodoca -- 27 --> AutoResearch
  CardIndex -- 26 --> Hybrid_RAG
  CardIndex -- 26 --> AutoResearch
  mclaude -- 26 --> LiteLLM
  mclaude -- 26 --> Tool_Search
  LiteParse -- 26 --> Hybrid_RAG
  LiteParse -- 26 --> AutoResearch
  LiteParse -- 25 --> MemNet
  Svyazi -- 25 --> Hybrid_RAG
  CardIndex -- 25 --> Graph_RAG
  AgentFS -- 25 --> Hybrid_RAG
  knowledge_space -- 25 --> Graph_RAG
  knowledge_space -- 25 --> Tool_Search
  AI_Factory -- 25 --> Legal_RAG
  Rufler -- 25 --> LiteLLM
  Hybrid_RAG -- 25 --> Yodoca
  NGT_Memory -- 25 --> LiteLLM
  knowledge_space -- 24 --> LiteLLM
  mclaude -- 24 --> Graph_RAG
  mclaude -- 24 --> AutoResearch
  AI_Factory -- 24 --> Hybrid_RAG
  Rufler -- 24 --> AutoResearch
  Legal_RAG -- 24 --> Hybrid_RAG
  Hybrid_RAG -- 24 --> Auto_AI_Router
  MemNet -- 23 --> Auto_AI_Router
  AgentFS -- 23 --> MemNet
  knowledge_space -- 23 --> MemNet
  mclaude -- 23 --> Hybrid_RAG
  Legal_RAG -- 23 --> LiteLLM
  Hybrid_RAG -- 23 --> NGT_Memory
  Hybrid_RAG -- 23 --> SENTINEL
  Hybrid_RAG -- 23 --> LiteLLM
  NGT_Memory -- 23 --> Tool_Search
  NGT_Memory -- 23 --> AutoResearch
  CardIndex -- 22 --> MemNet
  knowledge_space -- 22 --> AutoResearch
  Rufler -- 22 --> MemNet
  Legal_RAG -- 22 --> Tool_Search
  MemNet -- 22 --> SENTINEL
  MemNet -- 22 --> Wikontic
  Auto_AI_Router -- 22 --> AutoResearch
  knowledge_space -- 21 --> Hybrid_RAG
  AI_Factory -- 21 --> Graph_RAG
  Rufler -- 21 --> Hybrid_RAG
  Hybrid_RAG -- 21 --> Tool_Search
  SENTINEL -- 21 --> AutoResearch
  Svyazi -- 20 --> Yjs
  CardIndex -- 20 --> Yjs
  mclaude -- 20 --> MemNet
  AI_Factory -- 20 --> MemNet
  Hybrid_RAG -- 20 --> Graph_RAG
  Graph_RAG -- 20 --> LiteLLM
  LiteLLM -- 20 --> AutoResearch
  CardIndex -- 19 --> Wikontic
  Graph_RAG -- 19 --> Tool_Search
  Yodoca -- 19 --> Yjs
  AgentFS -- 18 --> Wikontic
  AgentFS -- 18 --> Yjs
  knowledge_space -- 18 --> Wikontic
  knowledge_space -- 18 --> Yjs
  LiteParse -- 18 --> Yjs
  Legal_RAG -- 18 --> MemNet
  Graph_RAG -- 18 --> MemNet
  NGT_Memory -- 18 --> MemNet
  NGT_Memory -- 18 --> Yjs
  Tool_Search -- 18 --> AutoResearch
  AI_Factory -- 17 --> Yjs
  NGT_Memory -- 17 --> Wikontic
  AutoResearch -- 17 --> Yjs
  Svyazi -- 16 --> Automerge
  CardIndex -- 16 --> Automerge
  mclaude -- 16 --> Yjs
  Rufler -- 16 --> Yjs
  Hybrid_RAG -- 16 --> AutoResearch
  Yodoca -- 16 --> Automerge
  NGT_Memory -- 16 --> Automerge
  Auto_AI_Router -- 16 --> Yjs
  Yjs -- 16 --> Automerge
  MemNet -- 15 --> LiteLLM
  MemNet -- 15 --> Tool_Search
  AgentFS -- 15 --> Automerge
  knowledge_space -- 15 --> Automerge
  AI_Factory -- 15 --> Automerge
  Rufler -- 15 --> Automerge
  LiteParse -- 15 --> Wikontic
  LiteParse -- 15 --> Automerge
  Hybrid_RAG -- 15 --> Yjs
  MemNet -- 15 --> AutoResearch
  SENTINEL -- 15 --> Yjs
  AutoResearch -- 15 --> Automerge
  Svyazi -- 14 --> Firecrawl
  CardIndex -- 14 --> Firecrawl
  Yodoca -- 14 --> Firecrawl
  mclaude -- 14 --> Automerge
  Rufler -- 14 --> Wikontic
  Legal_RAG -- 14 --> AutoResearch
  Hybrid_RAG -- 14 --> Automerge
  Graph_RAG -- 14 --> AutoResearch
  SENTINEL -- 14 --> Wikontic
  LiteLLM -- 14 --> Yjs
  LiteLLM -- 14 --> Automerge
  Auto_AI_Router -- 14 --> Automerge
  AgentFS -- 13 --> Firecrawl
  Rufler -- 13 --> Firecrawl
  SENTINEL -- 13 --> Firecrawl
  Legal_RAG -- 13 --> Yjs
  Hybrid_RAG -- 13 --> MemNet
  Graph_RAG -- 13 --> Yjs
  SENTINEL -- 13 --> Automerge
  knowledge_space -- 12 --> Firecrawl
  mclaude -- 12 --> Wikontic
  AI_Factory -- 12 --> Wikontic
  MemNet -- 12 --> Yjs
  Tool_Search -- 12 --> Yjs
  Tool_Search -- 12 --> Automerge
  Legal_RAG -- 11 --> Automerge
  Graph_RAG -- 11 --> Wikontic
  Graph_RAG -- 11 --> Automerge
  Auto_AI_Router -- 11 --> Wikontic
  AutoResearch -- 11 --> Wikontic
  Wikontic -- 11 --> Firecrawl
  AI_Factory -- 10 --> Firecrawl
  LiteParse -- 10 --> Firecrawl
  MemNet -- 10 --> Firecrawl
  Legal_RAG -- 9 --> Wikontic
  MemNet -- 9 --> Automerge
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
  Legal_RAG -- 7 --> Firecrawl
  Graph_RAG -- 7 --> Firecrawl
  Wikontic -- 7 --> Automerge
```

## Топ совместных упоминаний

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 74 |
| **Svyazi** | **AgentFS** | 70 |
| **AgentFS** | **Yodoca** | 64 |
| **Svyazi** | **CardIndex** | 60 |
| **Svyazi** | **SENTINEL** | 58 |
| **Svyazi** | **Rufler** | 58 |
| **CardIndex** | **AgentFS** | 56 |
| **AgentFS** | **SENTINEL** | 56 |
| **Svyazi** | **NGT Memory** | 55 |
| **AgentFS** | **Rufler** | 54 |
| **Svyazi** | **knowledge-space** | 53 |
| **Svyazi** | **LiteParse** | 53 |
| **Svyazi** | **Auto AI Router** | 53 |
| **CardIndex** | **Yodoca** | 52 |
| **Rufler** | **Yodoca** | 52 |
| **SENTINEL** | **Auto AI Router** | 51 |
| **Yodoca** | **SENTINEL** | 50 |
| **Rufler** | **SENTINEL** | 50 |
| **Yodoca** | **NGT Memory** | 50 |
| **Svyazi** | **mclaude** | 49 |
| **Svyazi** | **AI Factory** | 49 |
| **AgentFS** | **knowledge-space** | 48 |
| **AgentFS** | **NGT Memory** | 48 |
| **CardIndex** | **knowledge-space** | 46 |
| **AgentFS** | **LiteParse** | 46 |

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
  Svyazi -> AgentFS [label="70"];
  Svyazi -> Yodoca [label="74"];
  Svyazi -> Wikontic [label="27"];
  AgentFS -> Yodoca [label="64"];
  AgentFS -> Wikontic [label="18"];
  Yodoca -> Wikontic [label="29"];
  Svyazi -> CardIndex [label="60"];
  Svyazi -> SENTINEL [label="58"];
  Svyazi -> Tool_Search [label="32"];
  CardIndex -> AgentFS [label="56"];
  CardIndex -> Yodoca [label="52"];
  CardIndex -> SENTINEL [label="43"];
  CardIndex -> Tool_Search [label="30"];
  AgentFS -> SENTINEL [label="56"];
  AgentFS -> Tool_Search [label="32"];
  Yodoca -> SENTINEL [label="50"];
  Yodoca -> Tool_Search [label="29"];
  SENTINEL -> Tool_Search [label="33"];
  Svyazi -> knowledge_space [label="53"];
  Svyazi -> Rufler [label="58"];
  Svyazi -> Firecrawl [label="14"];
  CardIndex -> knowledge_space [label="46"];
  CardIndex -> Rufler [label="45"];
  CardIndex -> Firecrawl [label="14"];
  AgentFS -> knowledge_space [label="48"];
  AgentFS -> Rufler [label="54"];
  AgentFS -> Firecrawl [label="13"];
  knowledge_space -> Rufler [label="41"];
  knowledge_space -> Yodoca [label="44"];
  knowledge_space -> SENTINEL [label="39"];
  knowledge_space -> Firecrawl [label="12"];
  Rufler -> Yodoca [label="52"];
  Rufler -> SENTINEL [label="50"];
  Rufler -> Firecrawl [label="13"];
  Yodoca -> Firecrawl [label="14"];
  SENTINEL -> Firecrawl [label="13"];
  Svyazi -> LiteParse [label="53"];
  Svyazi -> MemNet [label="35"];
  Svyazi -> LiteLLM [label="31"];
  Svyazi -> Auto_AI_Router [label="53"];
  LiteParse -> MemNet [label="25"];
  LiteParse -> LiteLLM [label="29"];
  LiteParse -> Auto_AI_Router [label="40"];
  LiteParse -> Tool_Search [label="29"];
  MemNet -> LiteLLM [label="15"];
  MemNet -> Auto_AI_Router [label="23"];
  MemNet -> Tool_Search [label="15"];
  LiteLLM -> Auto_AI_Router [label="34"];
  LiteLLM -> Tool_Search [label="31"];
  Auto_AI_Router -> Tool_Search [label="31"];
  Svyazi -> mclaude [label="49"];
  Svyazi -> AI_Factory [label="49"];
  Svyazi -> Legal_RAG [label="40"];
  Svyazi -> Hybrid_RAG [label="25"];
  Svyazi -> Graph_RAG [label="40"];
  Svyazi -> NGT_Memory [label="55"];
  Svyazi -> AutoResearch [label="30"];
  Svyazi -> Yjs [label="20"];
  Svyazi -> Automerge [label="16"];
  CardIndex -> mclaude [label="42"];
  CardIndex -> AI_Factory [label="44"];
  CardIndex -> LiteParse [label="43"];
  CardIndex -> Legal_RAG [label="28"];
  CardIndex -> Hybrid_RAG [label="26"];
  CardIndex -> Graph_RAG [label="25"];
  CardIndex -> NGT_Memory [label="41"];
  CardIndex -> MemNet [label="22"];
  CardIndex -> LiteLLM [label="28"];
  CardIndex -> Auto_AI_Router [label="35"];
  CardIndex -> AutoResearch [label="26"];
  CardIndex -> Wikontic [label="19"];
  CardIndex -> Yjs [label="20"];
  CardIndex -> Automerge [label="16"];
  AgentFS -> mclaude [label="43"];
  AgentFS -> AI_Factory [label="45"];
  AgentFS -> LiteParse [label="46"];
  AgentFS -> Legal_RAG [label="35"];
  AgentFS -> Hybrid_RAG [label="25"];
  AgentFS -> Graph_RAG [label="34"];
  AgentFS -> NGT_Memory [label="48"];
  AgentFS -> MemNet [label="23"];
  AgentFS -> LiteLLM [label="29"];
  AgentFS -> Auto_AI_Router [label="45"];
  AgentFS -> AutoResearch [label="27"];
  AgentFS -> Yjs [label="18"];
  AgentFS -> Automerge [label="15"];
  knowledge_space -> mclaude [label="40"];
  knowledge_space -> AI_Factory [label="38"];
  knowledge_space -> LiteParse [label="43"];
  knowledge_space -> Legal_RAG [label="28"];
  knowledge_space -> Hybrid_RAG [label="21"];
  knowledge_space -> Graph_RAG [label="25"];
  knowledge_space -> NGT_Memory [label="40"];
  knowledge_space -> MemNet [label="23"];
  knowledge_space -> LiteLLM [label="24"];
  knowledge_space -> Auto_AI_Router [label="35"];
  knowledge_space -> Tool_Search [label="25"];
  knowledge_space -> AutoResearch [label="22"];
  knowledge_space -> Wikontic [label="18"];
  knowledge_space -> Yjs [label="18"];
  knowledge_space -> Automerge [label="15"];
  mclaude -> AI_Factory [label="44"];
  mclaude -> Rufler [label="42"];
  mclaude -> LiteParse [label="43"];
  mclaude -> Legal_RAG [label="28"];
  mclaude -> Hybrid_RAG [label="23"];
  mclaude -> Graph_RAG [label="24"];
  mclaude -> Yodoca [label="44"];
  mclaude -> NGT_Memory [label="39"];
  mclaude -> MemNet [label="20"];
  mclaude -> SENTINEL [label="36"];
  mclaude -> LiteLLM [label="26"];
  mclaude -> Auto_AI_Router [label="34"];
  mclaude -> Tool_Search [label="26"];
  mclaude -> AutoResearch [label="24"];
  mclaude -> Wikontic [label="12"];
  mclaude -> Firecrawl [label="8"];
  mclaude -> Yjs [label="16"];
  mclaude -> Automerge [label="14"];
  AI_Factory -> Rufler [label="40"];
  AI_Factory -> LiteParse [label="40"];
  AI_Factory -> Legal_RAG [label="25"];
  AI_Factory -> Hybrid_RAG [label="24"];
  AI_Factory -> Graph_RAG [label="21"];
  AI_Factory -> Yodoca [label="45"];
  AI_Factory -> NGT_Memory [label="38"];
  AI_Factory -> MemNet [label="20"];
  AI_Factory -> SENTINEL [label="36"];
  AI_Factory -> LiteLLM [label="29"];
  AI_Factory -> Auto_AI_Router [label="33"];
  AI_Factory -> Tool_Search [label="29"];
  AI_Factory -> AutoResearch [label="27"];
  AI_Factory -> Wikontic [label="12"];
  AI_Factory -> Firecrawl [label="10"];
  AI_Factory -> Yjs [label="17"];
  AI_Factory -> Automerge [label="15"];
  Rufler -> LiteParse [label="43"];
  Rufler -> Legal_RAG [label="33"];
  Rufler -> Hybrid_RAG [label="21"];
  Rufler -> Graph_RAG [label="32"];
  Rufler -> NGT_Memory [label="40"];
  Rufler -> MemNet [label="22"];
  Rufler -> LiteLLM [label="25"];
  Rufler -> Auto_AI_Router [label="41"];
  Rufler -> Tool_Search [label="27"];
  Rufler -> AutoResearch [label="24"];
  Rufler -> Wikontic [label="14"];
  Rufler -> Yjs [label="16"];
  Rufler -> Automerge [label="15"];
  LiteParse -> Legal_RAG [label="36"];
  LiteParse -> Hybrid_RAG [label="26"];
  LiteParse -> Graph_RAG [label="32"];
  LiteParse -> Yodoca [label="43"];
  LiteParse -> NGT_Memory [label="35"];
  LiteParse -> SENTINEL [label="43"];
  LiteParse -> AutoResearch [label="26"];
  LiteParse -> Wikontic [label="15"];
  LiteParse -> Firecrawl [label="10"];
  LiteParse -> Yjs [label="18"];
  LiteParse -> Automerge [label="15"];
  Legal_RAG -> Hybrid_RAG [label="24"];
  Legal_RAG -> Graph_RAG [label="37"];
  Legal_RAG -> Yodoca [label="33"];
  Legal_RAG -> NGT_Memory [label="31"];
  Legal_RAG -> MemNet [label="18"];
  Legal_RAG -> SENTINEL [label="39"];
  Legal_RAG -> LiteLLM [label="23"];
  Legal_RAG -> Auto_AI_Router [label="39"];
  Legal_RAG -> Tool_Search [label="22"];
  Legal_RAG -> AutoResearch [label="14"];
  Legal_RAG -> Wikontic [label="9"];
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
  Graph_RAG -> Yodoca [label="32"];
  Graph_RAG -> NGT_Memory [label="31"];
  Graph_RAG -> MemNet [label="18"];
  Graph_RAG -> SENTINEL [label="40"];
  Graph_RAG -> LiteLLM [label="20"];
  Graph_RAG -> Auto_AI_Router [label="39"];
  Graph_RAG -> Tool_Search [label="19"];
  Graph_RAG -> AutoResearch [label="14"];
  Graph_RAG -> Wikontic [label="11"];
  Graph_RAG -> Firecrawl [label="7"];
  Graph_RAG -> Yjs [label="13"];
  Graph_RAG -> Automerge [label="11"];
  Yodoca -> NGT_Memory [label="50"];
  Yodoca -> MemNet [label="31"];
  Yodoca -> LiteLLM [label="27"];
  Yodoca -> Auto_AI_Router [label="42"];
  Yodoca -> AutoResearch [label="27"];
  Yodoca -> Yjs [label="19"];
  Yodoca -> Automerge [label="16"];
  NGT_Memory -> MemNet [label="18"];
  NGT_Memory -> SENTINEL [label="40"];
  NGT_Memory -> LiteLLM [label="25"];
  NGT_Memory -> Auto_AI_Router [label="41"];
  NGT_Memory -> Tool_Search [label="23"];
  NGT_Memory -> AutoResearch [label="23"];
  NGT_Memory -> Wikontic [label="17"];
  NGT_Memory -> Firecrawl [label="8"];
  NGT_Memory -> Yjs [label="18"];
  NGT_Memory -> Automerge [label="16"];
  MemNet -> SENTINEL [label="22"];
  MemNet -> AutoResearch [label="15"];
  MemNet -> Wikontic [label="22"];
  MemNet -> Firecrawl [label="10"];
  MemNet -> Yjs [label="12"];
  MemNet -> Automerge [label="9"];
  SENTINEL -> LiteLLM [label="31"];
  SENTINEL -> Auto_AI_Router [label="51"];
  SENTINEL -> AutoResearch [label="21"];
  SENTINEL -> Wikontic [label="14"];
  SENTINEL -> Yjs [label="15"];
  SENTINEL -> Automerge [label="13"];
  LiteLLM -> AutoResearch [label="20"];
  LiteLLM -> Wikontic [label="8"];
  LiteLLM -> Firecrawl [label="8"];
  LiteLLM -> Yjs [label="14"];
  LiteLLM -> Automerge [label="14"];
  Auto_AI_Router -> AutoResearch [label="22"];
  Auto_AI_Router -> Wikontic [label="11"];
  Auto_AI_Router -> Firecrawl [label="8"];
  Auto_AI_Router -> Yjs [label="16"];
  Auto_AI_Router -> Automerge [label="14"];
  Tool_Search -> AutoResearch [label="18"];
  Tool_Search -> Wikontic [label="9"];
  Tool_Search -> Firecrawl [label="8"];
  Tool_Search -> Yjs [label="12"];
  Tool_Search -> Automerge [label="12"];
  AutoResearch -> Wikontic [label="11"];
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
- [GLOSSARY](docs/GLOSSARY.md)
- [NETWORK](docs/NETWORK.md)
- [MINDMAP](docs/MINDMAP.md)
- [CONTACT_PRIORITY](docs/CONTACT_PRIORITY.md)

