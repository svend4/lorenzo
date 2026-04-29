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
  Svyazi -- 100 --> CardIndex
  Svyazi -- 99 --> Yodoca
  Svyazi -- 82 --> AgentFS
  Svyazi -- 74 --> NGT_Memory
  AgentFS -- 72 --> Yodoca
  CardIndex -- 71 --> Yodoca
  Svyazi -- 69 --> knowledge_space
  CardIndex -- 69 --> AgentFS
  Svyazi -- 67 --> mclaude
  AgentFS -- 67 --> knowledge_space
  Svyazi -- 66 --> LiteParse
  Svyazi -- 64 --> AI_Factory
  Yodoca -- 64 --> NGT_Memory
  Svyazi -- 60 --> Rufler
  Svyazi -- 60 --> SENTINEL
  AgentFS -- 59 --> LiteParse
  mclaude -- 59 --> AI_Factory
  knowledge_space -- 58 --> Yodoca
  mclaude -- 58 --> Yodoca
  AgentFS -- 56 --> mclaude
  AgentFS -- 56 --> SENTINEL
  CardIndex -- 55 --> knowledge_space
  CardIndex -- 55 --> NGT_Memory
  LiteParse -- 55 --> Yodoca
  Svyazi -- 54 --> Auto_AI_Router
  CardIndex -- 54 --> LiteParse
  AgentFS -- 54 --> Rufler
  mclaude -- 54 --> Rufler
  knowledge_space -- 53 --> mclaude
  AI_Factory -- 53 --> Yodoca
  AgentFS -- 52 --> AI_Factory
  mclaude -- 52 --> LiteParse
  Rufler -- 52 --> Yodoca
  CardIndex -- 51 --> mclaude
  AI_Factory -- 51 --> Rufler
  CardIndex -- 50 --> Rufler
  AgentFS -- 50 --> NGT_Memory
  CardIndex -- 49 --> SENTINEL
  knowledge_space -- 49 --> LiteParse
  knowledge_space -- 49 --> NGT_Memory
  Yodoca -- 49 --> SENTINEL
  CardIndex -- 48 --> AI_Factory
  mclaude -- 48 --> NGT_Memory
  AI_Factory -- 48 --> LiteParse
  Rufler -- 48 --> LiteParse
  LiteLLM -- 48 --> Auto_AI_Router
  knowledge_space -- 47 --> Rufler
  LiteParse -- 47 --> SENTINEL
  Svyazi -- 46 --> MemNet
  Rufler -- 46 --> SENTINEL
  LiteParse -- 46 --> Legal_RAG
  SENTINEL -- 46 --> Auto_AI_Router
  Svyazi -- 45 --> Legal_RAG
  Svyazi -- 45 --> Tool_Search
  AI_Factory -- 45 --> NGT_Memory
  CardIndex -- 44 --> Auto_AI_Router
  AI_Factory -- 44 --> SENTINEL
  SENTINEL -- 44 --> Tool_Search
  Svyazi -- 43 --> AutoResearch
  knowledge_space -- 43 --> AI_Factory
  LiteParse -- 43 --> NGT_Memory
  Svyazi -- 42 --> LiteLLM
  AgentFS -- 42 --> Auto_AI_Router
  knowledge_space -- 42 --> SENTINEL
  LiteParse -- 42 --> Auto_AI_Router
  Yodoca -- 42 --> MemNet
  Yodoca -- 42 --> Auto_AI_Router
  NGT_Memory -- 42 --> Auto_AI_Router
  Auto_AI_Router -- 42 --> Tool_Search
  mclaude -- 41 --> SENTINEL
  SENTINEL -- 41 --> LiteLLM
  LiteLLM -- 41 --> Tool_Search
  Svyazi -- 40 --> Graph_RAG
  AgentFS -- 40 --> Tool_Search
  LiteParse -- 40 --> Graph_RAG
  Svyazi -- 39 --> Hybrid_RAG
  LiteParse -- 39 --> Hybrid_RAG
  Yodoca -- 39 --> AutoResearch
  CardIndex -- 38 --> Tool_Search
  AgentFS -- 38 --> Legal_RAG
  AI_Factory -- 38 --> Auto_AI_Router
  Legal_RAG -- 38 --> Graph_RAG
  NGT_Memory -- 38 --> SENTINEL
  AgentFS -- 37 --> LiteLLM
  Rufler -- 37 --> NGT_Memory
  LiteParse -- 37 --> LiteLLM
  LiteParse -- 37 --> Tool_Search
  CardIndex -- 36 --> Legal_RAG
  CardIndex -- 36 --> LiteLLM
  knowledge_space -- 36 --> Auto_AI_Router
  mclaude -- 36 --> Auto_AI_Router
  Legal_RAG -- 36 --> Yodoca
  Legal_RAG -- 36 --> SENTINEL
  Yodoca -- 36 --> Tool_Search
  Svyazi -- 35 --> Wikontic
  Svyazi -- 35 --> Yjs
  AgentFS -- 35 --> Hybrid_RAG
  mclaude -- 35 --> Legal_RAG
  AI_Factory -- 35 --> Tool_Search
  Legal_RAG -- 35 --> Auto_AI_Router
  Graph_RAG -- 35 --> SENTINEL
  Yodoca -- 35 --> LiteLLM
  CardIndex -- 34 --> Hybrid_RAG
  AgentFS -- 34 --> Graph_RAG
  AgentFS -- 34 --> AutoResearch
  mclaude -- 34 --> AutoResearch
  AI_Factory -- 34 --> Legal_RAG
  AI_Factory -- 34 --> LiteLLM
  AI_Factory -- 34 --> AutoResearch
  Rufler -- 34 --> Auto_AI_Router
  Legal_RAG -- 34 --> Hybrid_RAG
  Legal_RAG -- 34 --> NGT_Memory
  Hybrid_RAG -- 34 --> Yodoca
  knowledge_space -- 33 --> Legal_RAG
  Rufler -- 33 --> AutoResearch
  Hybrid_RAG -- 33 --> Graph_RAG
  Yodoca -- 33 --> Wikontic
  NGT_Memory -- 33 --> LiteLLM
  CardIndex -- 32 --> AutoResearch
  Rufler -- 32 --> Legal_RAG
  Rufler -- 32 --> Tool_Search
  LiteParse -- 32 --> AutoResearch
  Hybrid_RAG -- 32 --> SENTINEL
  mclaude -- 31 --> Hybrid_RAG
  mclaude -- 31 --> LiteLLM
  mclaude -- 31 --> Tool_Search
  AI_Factory -- 31 --> Hybrid_RAG
  Hybrid_RAG -- 31 --> NGT_Memory
  Hybrid_RAG -- 31 --> Auto_AI_Router
  NGT_Memory -- 31 --> AutoResearch
  NGT_Memory -- 31 --> Wikontic
  CardIndex -- 30 --> Graph_RAG
  CardIndex -- 30 --> Yjs
  knowledge_space -- 30 --> Hybrid_RAG
  knowledge_space -- 30 --> LiteLLM
  knowledge_space -- 30 --> Tool_Search
  mclaude -- 30 --> Graph_RAG
  Rufler -- 30 --> Hybrid_RAG
  Rufler -- 30 --> LiteLLM
  LiteParse -- 30 --> MemNet
  Legal_RAG -- 30 --> LiteLLM
  Legal_RAG -- 30 --> Tool_Search
  Hybrid_RAG -- 30 --> LiteLLM
  Graph_RAG -- 30 --> Yodoca
  Graph_RAG -- 30 --> Auto_AI_Router
  NGT_Memory -- 30 --> MemNet
  NGT_Memory -- 30 --> Tool_Search
  Yjs -- 30 --> Automerge
  CardIndex -- 29 --> MemNet
  AgentFS -- 29 --> MemNet
  knowledge_space -- 29 --> Graph_RAG
  knowledge_space -- 29 --> AutoResearch
  Graph_RAG -- 29 --> NGT_Memory
  Auto_AI_Router -- 29 --> AutoResearch
  knowledge_space -- 28 --> MemNet
  AI_Factory -- 28 --> Graph_RAG
  Rufler -- 28 --> Graph_RAG
  LiteLLM -- 27 --> AutoResearch
  Svyazi -- 26 --> Automerge
  CardIndex -- 26 --> Wikontic
  mclaude -- 26 --> MemNet
  Rufler -- 26 --> MemNet
  Hybrid_RAG -- 26 --> Tool_Search
  NGT_Memory -- 26 --> Yjs
  MemNet -- 26 --> Auto_AI_Router
  MemNet -- 26 --> Wikontic
  AgentFS -- 25 --> Yjs
  Graph_RAG -- 25 --> LiteLLM
  Yodoca -- 25 --> Yjs
  MemNet -- 25 --> SENTINEL
  SENTINEL -- 25 --> AutoResearch
  Graph_RAG -- 24 --> Tool_Search
  knowledge_space -- 23 --> Yjs
  AI_Factory -- 23 --> MemNet
  LiteParse -- 23 --> Yjs
  Tool_Search -- 23 --> AutoResearch
  AgentFS -- 22 --> Automerge
  knowledge_space -- 22 --> Wikontic
  Legal_RAG -- 22 --> MemNet
  Hybrid_RAG -- 22 --> AutoResearch
  Yodoca -- 22 --> Automerge
  MemNet -- 22 --> AutoResearch
  Auto_AI_Router -- 22 --> Yjs
  AutoResearch -- 22 --> Yjs
  CardIndex -- 21 --> Automerge
  mclaude -- 21 --> Yjs
  Rufler -- 21 --> Yjs
  Graph_RAG -- 21 --> MemNet
  NGT_Memory -- 21 --> Automerge
  MemNet -- 21 --> LiteLLM
  knowledge_space -- 20 --> Automerge
  AI_Factory -- 20 --> Yjs
  Rufler -- 20 --> Automerge
  LiteParse -- 20 --> Automerge
  AutoResearch -- 20 --> Automerge
  AgentFS -- 19 --> Wikontic
  mclaude -- 19 --> Automerge
  Legal_RAG -- 19 --> AutoResearch
  Hybrid_RAG -- 19 --> MemNet
  MemNet -- 19 --> Tool_Search
  Svyazi -- 18 --> Firecrawl
  AI_Factory -- 18 --> Automerge
  LiteParse -- 18 --> Wikontic
  Hybrid_RAG -- 18 --> Yjs
  Graph_RAG -- 18 --> AutoResearch
  SENTINEL -- 18 --> Yjs
  knowledge_space -- 17 --> Firecrawl
  Hybrid_RAG -- 17 --> Automerge
  MemNet -- 17 --> Yjs
  LiteLLM -- 17 --> Yjs
  LiteLLM -- 17 --> Automerge
  Auto_AI_Router -- 17 --> Automerge
  AgentFS -- 16 --> Firecrawl
  Rufler -- 16 --> Wikontic
  Legal_RAG -- 16 --> Yjs
  Graph_RAG -- 16 --> Yjs
  SENTINEL -- 16 --> Wikontic
  SENTINEL -- 16 --> Automerge
  AutoResearch -- 16 --> Wikontic
  mclaude -- 15 --> Wikontic
  Rufler -- 15 --> Firecrawl
  Yodoca -- 15 --> Firecrawl
  SENTINEL -- 15 --> Firecrawl
  CardIndex -- 14 --> Firecrawl
  Legal_RAG -- 14 --> Automerge
  Graph_RAG -- 14 --> Automerge
  MemNet -- 14 --> Automerge
  Auto_AI_Router -- 14 --> Wikontic
  Tool_Search -- 14 --> Yjs
  Tool_Search -- 14 --> Automerge
  AI_Factory -- 13 --> Wikontic
  LiteParse -- 13 --> Firecrawl
  Graph_RAG -- 13 --> Wikontic
  Hybrid_RAG -- 12 --> Wikontic
  Wikontic -- 12 --> Firecrawl
  Wikontic -- 12 --> Yjs
  mclaude -- 11 --> Firecrawl
  AI_Factory -- 11 --> Firecrawl
  Legal_RAG -- 11 --> Wikontic
  Hybrid_RAG -- 11 --> Firecrawl
  MemNet -- 11 --> Firecrawl
  LiteLLM -- 11 --> Wikontic
  Tool_Search -- 10 --> Wikontic
  Wikontic -- 10 --> Automerge
  Graph_RAG -- 9 --> Firecrawl
  NGT_Memory -- 9 --> Firecrawl
  LiteLLM -- 9 --> Firecrawl
  Auto_AI_Router -- 9 --> Firecrawl
  Tool_Search -- 9 --> Firecrawl
  AutoResearch -- 9 --> Firecrawl
  Firecrawl -- 9 --> Yjs
  Firecrawl -- 9 --> Automerge
  Legal_RAG -- 8 --> Firecrawl
```

## Топ совместных упоминаний

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **CardIndex** | 100 |
| **Svyazi** | **Yodoca** | 99 |
| **Svyazi** | **AgentFS** | 82 |
| **Svyazi** | **NGT Memory** | 74 |
| **AgentFS** | **Yodoca** | 72 |
| **CardIndex** | **Yodoca** | 71 |
| **Svyazi** | **knowledge-space** | 69 |
| **CardIndex** | **AgentFS** | 69 |
| **Svyazi** | **mclaude** | 67 |
| **AgentFS** | **knowledge-space** | 67 |
| **Svyazi** | **LiteParse** | 66 |
| **Svyazi** | **AI Factory** | 64 |
| **Yodoca** | **NGT Memory** | 64 |
| **Svyazi** | **Rufler** | 60 |
| **Svyazi** | **SENTINEL** | 60 |
| **AgentFS** | **LiteParse** | 59 |
| **mclaude** | **AI Factory** | 59 |
| **knowledge-space** | **Yodoca** | 58 |
| **mclaude** | **Yodoca** | 58 |
| **AgentFS** | **mclaude** | 56 |
| **AgentFS** | **SENTINEL** | 56 |
| **CardIndex** | **knowledge-space** | 55 |
| **CardIndex** | **NGT Memory** | 55 |
| **LiteParse** | **Yodoca** | 55 |
| **Svyazi** | **Auto AI Router** | 54 |

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
  Svyazi -> CardIndex [label="100"];
  Svyazi -> AgentFS [label="82"];
  Svyazi -> knowledge_space [label="69"];
  Svyazi -> mclaude [label="67"];
  Svyazi -> AI_Factory [label="64"];
  Svyazi -> Rufler [label="60"];
  Svyazi -> LiteParse [label="66"];
  Svyazi -> Legal_RAG [label="45"];
  Svyazi -> Hybrid_RAG [label="39"];
  Svyazi -> Graph_RAG [label="40"];
  Svyazi -> Yodoca [label="99"];
  Svyazi -> NGT_Memory [label="74"];
  Svyazi -> MemNet [label="46"];
  Svyazi -> SENTINEL [label="60"];
  Svyazi -> LiteLLM [label="42"];
  Svyazi -> Auto_AI_Router [label="54"];
  Svyazi -> Tool_Search [label="45"];
  Svyazi -> AutoResearch [label="43"];
  Svyazi -> Wikontic [label="35"];
  Svyazi -> Firecrawl [label="18"];
  Svyazi -> Yjs [label="35"];
  Svyazi -> Automerge [label="26"];
  CardIndex -> AgentFS [label="69"];
  CardIndex -> knowledge_space [label="55"];
  CardIndex -> mclaude [label="51"];
  CardIndex -> AI_Factory [label="48"];
  CardIndex -> Rufler [label="50"];
  CardIndex -> LiteParse [label="54"];
  CardIndex -> Legal_RAG [label="36"];
  CardIndex -> Hybrid_RAG [label="34"];
  CardIndex -> Graph_RAG [label="30"];
  CardIndex -> Yodoca [label="71"];
  CardIndex -> NGT_Memory [label="55"];
  CardIndex -> MemNet [label="29"];
  CardIndex -> SENTINEL [label="49"];
  CardIndex -> LiteLLM [label="36"];
  CardIndex -> Auto_AI_Router [label="44"];
  CardIndex -> Tool_Search [label="38"];
  CardIndex -> AutoResearch [label="32"];
  CardIndex -> Wikontic [label="26"];
  CardIndex -> Firecrawl [label="14"];
  CardIndex -> Yjs [label="30"];
  CardIndex -> Automerge [label="21"];
  AgentFS -> knowledge_space [label="67"];
  AgentFS -> mclaude [label="56"];
  AgentFS -> AI_Factory [label="52"];
  AgentFS -> Rufler [label="54"];
  AgentFS -> LiteParse [label="59"];
  AgentFS -> Legal_RAG [label="38"];
  AgentFS -> Hybrid_RAG [label="35"];
  AgentFS -> Graph_RAG [label="34"];
  AgentFS -> Yodoca [label="72"];
  AgentFS -> NGT_Memory [label="50"];
  AgentFS -> MemNet [label="29"];
  AgentFS -> SENTINEL [label="56"];
  AgentFS -> LiteLLM [label="37"];
  AgentFS -> Auto_AI_Router [label="42"];
  AgentFS -> Tool_Search [label="40"];
  AgentFS -> AutoResearch [label="34"];
  AgentFS -> Wikontic [label="19"];
  AgentFS -> Firecrawl [label="16"];
  AgentFS -> Yjs [label="25"];
  AgentFS -> Automerge [label="22"];
  knowledge_space -> mclaude [label="53"];
  knowledge_space -> AI_Factory [label="43"];
  knowledge_space -> Rufler [label="47"];
  knowledge_space -> LiteParse [label="49"];
  knowledge_space -> Legal_RAG [label="33"];
  knowledge_space -> Hybrid_RAG [label="30"];
  knowledge_space -> Graph_RAG [label="29"];
  knowledge_space -> Yodoca [label="58"];
  knowledge_space -> NGT_Memory [label="49"];
  knowledge_space -> MemNet [label="28"];
  knowledge_space -> SENTINEL [label="42"];
  knowledge_space -> LiteLLM [label="30"];
  knowledge_space -> Auto_AI_Router [label="36"];
  knowledge_space -> Tool_Search [label="30"];
  knowledge_space -> AutoResearch [label="29"];
  knowledge_space -> Wikontic [label="22"];
  knowledge_space -> Firecrawl [label="17"];
  knowledge_space -> Yjs [label="23"];
  knowledge_space -> Automerge [label="20"];
  mclaude -> AI_Factory [label="59"];
  mclaude -> Rufler [label="54"];
  mclaude -> LiteParse [label="52"];
  mclaude -> Legal_RAG [label="35"];
  mclaude -> Hybrid_RAG [label="31"];
  mclaude -> Graph_RAG [label="30"];
  mclaude -> Yodoca [label="58"];
  mclaude -> NGT_Memory [label="48"];
  mclaude -> MemNet [label="26"];
  mclaude -> SENTINEL [label="41"];
  mclaude -> LiteLLM [label="31"];
  mclaude -> Auto_AI_Router [label="36"];
  mclaude -> Tool_Search [label="31"];
  mclaude -> AutoResearch [label="34"];
  mclaude -> Wikontic [label="15"];
  mclaude -> Firecrawl [label="11"];
  mclaude -> Yjs [label="21"];
  mclaude -> Automerge [label="19"];
  AI_Factory -> Rufler [label="51"];
  AI_Factory -> LiteParse [label="48"];
  AI_Factory -> Legal_RAG [label="34"];
  AI_Factory -> Hybrid_RAG [label="31"];
  AI_Factory -> Graph_RAG [label="28"];
  AI_Factory -> Yodoca [label="53"];
  AI_Factory -> NGT_Memory [label="45"];
  AI_Factory -> MemNet [label="23"];
  AI_Factory -> SENTINEL [label="44"];
  AI_Factory -> LiteLLM [label="34"];
  AI_Factory -> Auto_AI_Router [label="38"];
  AI_Factory -> Tool_Search [label="35"];
  AI_Factory -> AutoResearch [label="34"];
  AI_Factory -> Wikontic [label="13"];
  AI_Factory -> Firecrawl [label="11"];
  AI_Factory -> Yjs [label="20"];
  AI_Factory -> Automerge [label="18"];
  Rufler -> LiteParse [label="48"];
  Rufler -> Legal_RAG [label="32"];
  Rufler -> Hybrid_RAG [label="30"];
  Rufler -> Graph_RAG [label="28"];
  Rufler -> Yodoca [label="52"];
  Rufler -> NGT_Memory [label="37"];
  Rufler -> MemNet [label="26"];
  Rufler -> SENTINEL [label="46"];
  Rufler -> LiteLLM [label="30"];
  Rufler -> Auto_AI_Router [label="34"];
  Rufler -> Tool_Search [label="32"];
  Rufler -> AutoResearch [label="33"];
  Rufler -> Wikontic [label="16"];
  Rufler -> Firecrawl [label="15"];
  Rufler -> Yjs [label="21"];
  Rufler -> Automerge [label="20"];
  LiteParse -> Legal_RAG [label="46"];
  LiteParse -> Hybrid_RAG [label="39"];
  LiteParse -> Graph_RAG [label="40"];
  LiteParse -> Yodoca [label="55"];
  LiteParse -> NGT_Memory [label="43"];
  LiteParse -> MemNet [label="30"];
  LiteParse -> SENTINEL [label="47"];
  LiteParse -> LiteLLM [label="37"];
  LiteParse -> Auto_AI_Router [label="42"];
  LiteParse -> Tool_Search [label="37"];
  LiteParse -> AutoResearch [label="32"];
  LiteParse -> Wikontic [label="18"];
  LiteParse -> Firecrawl [label="13"];
  LiteParse -> Yjs [label="23"];
  LiteParse -> Automerge [label="20"];
  Legal_RAG -> Hybrid_RAG [label="34"];
  Legal_RAG -> Graph_RAG [label="38"];
  Legal_RAG -> Yodoca [label="36"];
  Legal_RAG -> NGT_Memory [label="34"];
  Legal_RAG -> MemNet [label="22"];
  Legal_RAG -> SENTINEL [label="36"];
  Legal_RAG -> LiteLLM [label="30"];
  Legal_RAG -> Auto_AI_Router [label="35"];
  Legal_RAG -> Tool_Search [label="30"];
  Legal_RAG -> AutoResearch [label="19"];
  Legal_RAG -> Wikontic [label="11"];
  Legal_RAG -> Firecrawl [label="8"];
  Legal_RAG -> Yjs [label="16"];
  Legal_RAG -> Automerge [label="14"];
  Hybrid_RAG -> Graph_RAG [label="33"];
  Hybrid_RAG -> Yodoca [label="34"];
  Hybrid_RAG -> NGT_Memory [label="31"];
  Hybrid_RAG -> MemNet [label="19"];
  Hybrid_RAG -> SENTINEL [label="32"];
  Hybrid_RAG -> LiteLLM [label="30"];
  Hybrid_RAG -> Auto_AI_Router [label="31"];
  Hybrid_RAG -> Tool_Search [label="26"];
  Hybrid_RAG -> AutoResearch [label="22"];
  Hybrid_RAG -> Wikontic [label="12"];
  Hybrid_RAG -> Firecrawl [label="11"];
  Hybrid_RAG -> Yjs [label="18"];
  Hybrid_RAG -> Automerge [label="17"];
  Graph_RAG -> Yodoca [label="30"];
  Graph_RAG -> NGT_Memory [label="29"];
  Graph_RAG -> MemNet [label="21"];
  Graph_RAG -> SENTINEL [label="35"];
  Graph_RAG -> LiteLLM [label="25"];
  Graph_RAG -> Auto_AI_Router [label="30"];
  Graph_RAG -> Tool_Search [label="24"];
  Graph_RAG -> AutoResearch [label="18"];
  Graph_RAG -> Wikontic [label="13"];
  Graph_RAG -> Firecrawl [label="9"];
  Graph_RAG -> Yjs [label="16"];
  Graph_RAG -> Automerge [label="14"];
  Yodoca -> NGT_Memory [label="64"];
  Yodoca -> MemNet [label="42"];
  Yodoca -> SENTINEL [label="49"];
  Yodoca -> LiteLLM [label="35"];
  Yodoca -> Auto_AI_Router [label="42"];
  Yodoca -> Tool_Search [label="36"];
  Yodoca -> AutoResearch [label="39"];
  Yodoca -> Wikontic [label="33"];
  Yodoca -> Firecrawl [label="15"];
  Yodoca -> Yjs [label="25"];
  Yodoca -> Automerge [label="22"];
  NGT_Memory -> MemNet [label="30"];
  NGT_Memory -> SENTINEL [label="38"];
  NGT_Memory -> LiteLLM [label="33"];
  NGT_Memory -> Auto_AI_Router [label="42"];
  NGT_Memory -> Tool_Search [label="30"];
  NGT_Memory -> AutoResearch [label="31"];
  NGT_Memory -> Wikontic [label="31"];
  NGT_Memory -> Firecrawl [label="9"];
  NGT_Memory -> Yjs [label="26"];
  NGT_Memory -> Automerge [label="21"];
  MemNet -> SENTINEL [label="25"];
  MemNet -> LiteLLM [label="21"];
  MemNet -> Auto_AI_Router [label="26"];
  MemNet -> Tool_Search [label="19"];
  MemNet -> AutoResearch [label="22"];
  MemNet -> Wikontic [label="26"];
  MemNet -> Firecrawl [label="11"];
  MemNet -> Yjs [label="17"];
  MemNet -> Automerge [label="14"];
  SENTINEL -> LiteLLM [label="41"];
  SENTINEL -> Auto_AI_Router [label="46"];
  SENTINEL -> Tool_Search [label="44"];
  SENTINEL -> AutoResearch [label="25"];
  SENTINEL -> Wikontic [label="16"];
  SENTINEL -> Firecrawl [label="15"];
  SENTINEL -> Yjs [label="18"];
  SENTINEL -> Automerge [label="16"];
  LiteLLM -> Auto_AI_Router [label="48"];
  LiteLLM -> Tool_Search [label="41"];
  LiteLLM -> AutoResearch [label="27"];
  LiteLLM -> Wikontic [label="11"];
  LiteLLM -> Firecrawl [label="9"];
  LiteLLM -> Yjs [label="17"];
  LiteLLM -> Automerge [label="17"];
  Auto_AI_Router -> Tool_Search [label="42"];
  Auto_AI_Router -> AutoResearch [label="29"];
  Auto_AI_Router -> Wikontic [label="14"];
  Auto_AI_Router -> Firecrawl [label="9"];
  Auto_AI_Router -> Yjs [label="22"];
  Auto_AI_Router -> Automerge [label="17"];
  Tool_Search -> AutoResearch [label="23"];
  Tool_Search -> Wikontic [label="10"];
  Tool_Search -> Firecrawl [label="9"];
  Tool_Search -> Yjs [label="14"];
  Tool_Search -> Automerge [label="14"];
  AutoResearch -> Wikontic [label="16"];
  AutoResearch -> Firecrawl [label="9"];
  AutoResearch -> Yjs [label="22"];
  AutoResearch -> Automerge [label="20"];
  Wikontic -> Firecrawl [label="12"];
  Wikontic -> Yjs [label="12"];
  Wikontic -> Automerge [label="10"];
  Firecrawl -> Yjs [label="9"];
  Firecrawl -> Automerge [label="9"];
  Yjs -> Automerge [label="30"];
}
```

<!-- see-also -->

---

**Смотрите также:**
- [GLOSSARY](docs/GLOSSARY.md)
- [NETWORK](docs/NETWORK.md)
- [MINDMAP](docs/MINDMAP.md)
- [CONTACT_PRIORITY](docs/CONTACT_PRIORITY.md)

