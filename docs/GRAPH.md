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
  Svyazi -- 120 --> Yodoca
  Svyazi -- 104 --> CardIndex
  Svyazi -- 85 --> AgentFS
  Svyazi -- 81 --> knowledge_space
  Svyazi -- 80 --> mclaude
  Svyazi -- 77 --> NGT_Memory
  CardIndex -- 77 --> Yodoca
  Svyazi -- 75 --> Rufler
  AgentFS -- 74 --> Yodoca
  CardIndex -- 73 --> AgentFS
  Svyazi -- 72 --> LiteParse
  Svyazi -- 70 --> AI_Factory
  AgentFS -- 70 --> knowledge_space
  knowledge_space -- 68 --> Yodoca
  mclaude -- 67 --> Yodoca
  Yodoca -- 66 --> NGT_Memory
  Svyazi -- 63 --> MemNet
  AgentFS -- 62 --> LiteParse
  mclaude -- 62 --> AI_Factory
  Rufler -- 62 --> Yodoca
  Svyazi -- 61 --> SENTINEL
  CardIndex -- 61 --> knowledge_space
  mclaude -- 60 --> Rufler
  LiteParse -- 60 --> Yodoca
  Yodoca -- 60 --> MemNet
  AgentFS -- 59 --> mclaude
  knowledge_space -- 59 --> mclaude
  CardIndex -- 58 --> LiteParse
  CardIndex -- 57 --> NGT_Memory
  knowledge_space -- 57 --> Rufler
  Svyazi -- 56 --> Auto_AI_Router
  AgentFS -- 56 --> Rufler
  AgentFS -- 56 --> SENTINEL
  AI_Factory -- 56 --> Yodoca
  mclaude -- 55 --> LiteParse
  CardIndex -- 54 --> mclaude
  CardIndex -- 54 --> Rufler
  AgentFS -- 54 --> AI_Factory
  AI_Factory -- 54 --> Rufler
  Svyazi -- 53 --> AutoResearch
  knowledge_space -- 52 --> LiteParse
  AgentFS -- 51 --> NGT_Memory
  knowledge_space -- 51 --> NGT_Memory
  Rufler -- 51 --> LiteParse
  CardIndex -- 50 --> AI_Factory
  CardIndex -- 50 --> SENTINEL
  AI_Factory -- 50 --> LiteParse
  Yodoca -- 50 --> SENTINEL
  mclaude -- 49 --> NGT_Memory
  AI_Factory -- 48 --> NGT_Memory
  LiteParse -- 48 --> Legal_RAG
  LiteParse -- 48 --> SENTINEL
  LiteLLM -- 48 --> Auto_AI_Router
  Svyazi -- 47 --> Legal_RAG
  Svyazi -- 47 --> Tool_Search
  Rufler -- 47 --> SENTINEL
  AI_Factory -- 46 --> SENTINEL
  SENTINEL -- 46 --> Auto_AI_Router
  CardIndex -- 45 --> Auto_AI_Router
  knowledge_space -- 45 --> AI_Factory
  Yodoca -- 45 --> AutoResearch
  Svyazi -- 44 --> LiteLLM
  LiteParse -- 44 --> NGT_Memory
  SENTINEL -- 44 --> Tool_Search
  Svyazi -- 43 --> Hybrid_RAG
  LiteParse -- 43 --> Auto_AI_Router
  Yodoca -- 43 --> Auto_AI_Router
  NGT_Memory -- 43 --> Auto_AI_Router
  Svyazi -- 42 --> Graph_RAG
  AgentFS -- 42 --> Auto_AI_Router
  knowledge_space -- 42 --> SENTINEL
  LiteParse -- 42 --> Hybrid_RAG
  Auto_AI_Router -- 42 --> Tool_Search
  knowledge_space -- 41 --> MemNet
  mclaude -- 41 --> SENTINEL
  LiteParse -- 41 --> Graph_RAG
  SENTINEL -- 41 --> LiteLLM
  LiteLLM -- 41 --> Tool_Search
  AgentFS -- 40 --> Tool_Search
  mclaude -- 40 --> AutoResearch
  AI_Factory -- 40 --> Auto_AI_Router
  Svyazi -- 39 --> Yjs
  AgentFS -- 39 --> Legal_RAG
  AgentFS -- 39 --> AutoResearch
  Rufler -- 39 --> AutoResearch
  Legal_RAG -- 39 --> Graph_RAG
  CardIndex -- 38 --> Legal_RAG
  CardIndex -- 38 --> Tool_Search
  AgentFS -- 38 --> Hybrid_RAG
  AI_Factory -- 38 --> AutoResearch
  Rufler -- 38 --> NGT_Memory
  LiteParse -- 38 --> LiteLLM
  LiteParse -- 38 --> Tool_Search
  NGT_Memory -- 38 --> SENTINEL
  Svyazi -- 37 --> Wikontic
  CardIndex -- 37 --> Hybrid_RAG
  CardIndex -- 37 --> AutoResearch
  AgentFS -- 37 --> LiteLLM
  Rufler -- 37 --> MemNet
  LiteParse -- 37 --> AutoResearch
  Legal_RAG -- 37 --> Hybrid_RAG
  Legal_RAG -- 37 --> Yodoca
  Hybrid_RAG -- 37 --> Yodoca
  Yodoca -- 37 --> Tool_Search
  CardIndex -- 36 --> MemNet
  CardIndex -- 36 --> LiteLLM
  knowledge_space -- 36 --> Auto_AI_Router
  mclaude -- 36 --> Auto_AI_Router
  AI_Factory -- 36 --> Legal_RAG
  Legal_RAG -- 36 --> SENTINEL
  Hybrid_RAG -- 36 --> Graph_RAG
  Yodoca -- 36 --> LiteLLM
  Yodoca -- 36 --> Wikontic
  AgentFS -- 35 --> Graph_RAG
  knowledge_space -- 35 --> AutoResearch
  mclaude -- 35 --> Legal_RAG
  mclaude -- 35 --> MemNet
  AI_Factory -- 35 --> Tool_Search
  Rufler -- 35 --> Auto_AI_Router
  Legal_RAG -- 35 --> NGT_Memory
  Legal_RAG -- 35 --> Auto_AI_Router
  Graph_RAG -- 35 --> SENTINEL
  CardIndex -- 34 --> Yjs
  knowledge_space -- 34 --> Legal_RAG
  AI_Factory -- 34 --> LiteLLM
  Hybrid_RAG -- 34 --> NGT_Memory
  Hybrid_RAG -- 34 --> SENTINEL
  NGT_Memory -- 34 --> LiteLLM
  NGT_Memory -- 34 --> AutoResearch
  Yjs -- 34 --> Automerge
  knowledge_space -- 33 --> Hybrid_RAG
  mclaude -- 33 --> Hybrid_RAG
  AI_Factory -- 33 --> Hybrid_RAG
  Rufler -- 33 --> Hybrid_RAG
  Rufler -- 33 --> Tool_Search
  LiteParse -- 33 --> MemNet
  Hybrid_RAG -- 33 --> Auto_AI_Router
  CardIndex -- 32 --> Graph_RAG
  AgentFS -- 32 --> MemNet
  Rufler -- 32 --> Legal_RAG
  NGT_Memory -- 32 --> MemNet
  Auto_AI_Router -- 32 --> AutoResearch
  mclaude -- 31 --> Graph_RAG
  mclaude -- 31 --> LiteLLM
  mclaude -- 31 --> Tool_Search
  Rufler -- 31 --> LiteLLM
  Graph_RAG -- 31 --> Yodoca
  NGT_Memory -- 31 --> Tool_Search
  NGT_Memory -- 31 --> Wikontic
  Svyazi -- 30 --> Automerge
  CardIndex -- 30 --> Wikontic
  knowledge_space -- 30 --> Graph_RAG
  knowledge_space -- 30 --> LiteLLM
  knowledge_space -- 30 --> Tool_Search
  AI_Factory -- 30 --> Graph_RAG
  Legal_RAG -- 30 --> LiteLLM
  Legal_RAG -- 30 --> Tool_Search
  Hybrid_RAG -- 30 --> LiteLLM
  Graph_RAG -- 30 --> NGT_Memory
  Graph_RAG -- 30 --> Auto_AI_Router
  AgentFS -- 29 --> Yjs
  Yodoca -- 29 --> Yjs
  knowledge_space -- 28 --> Yjs
  Rufler -- 28 --> Graph_RAG
  NGT_Memory -- 28 --> Yjs
  MemNet -- 28 --> AutoResearch
  MemNet -- 28 --> Wikontic
  LiteLLM -- 28 --> AutoResearch
  LiteParse -- 27 --> Yjs
  SENTINEL -- 27 --> AutoResearch
  AgentFS -- 26 --> Automerge
  knowledge_space -- 26 --> Wikontic
  AI_Factory -- 26 --> MemNet
  Rufler -- 26 --> Yjs
  Hybrid_RAG -- 26 --> Tool_Search
  Yodoca -- 26 --> Automerge
  MemNet -- 26 --> Auto_AI_Router
  AutoResearch -- 26 --> Yjs
  CardIndex -- 25 --> Automerge
  knowledge_space -- 25 --> Automerge
  mclaude -- 25 --> Yjs
  Rufler -- 25 --> Automerge
  Hybrid_RAG -- 25 --> AutoResearch
  Graph_RAG -- 25 --> LiteLLM
  MemNet -- 25 --> SENTINEL
  LiteParse -- 24 --> Automerge
  Graph_RAG -- 24 --> Tool_Search
  Auto_AI_Router -- 24 --> Yjs
  Tool_Search -- 24 --> AutoResearch
  AutoResearch -- 24 --> Automerge
  mclaude -- 23 --> Automerge
  NGT_Memory -- 23 --> Automerge
  AgentFS -- 22 --> Wikontic
  AI_Factory -- 22 --> Yjs
  Legal_RAG -- 22 --> MemNet
  Legal_RAG -- 22 --> AutoResearch
  MemNet -- 22 --> Yjs
  Hybrid_RAG -- 21 --> MemNet
  Graph_RAG -- 21 --> MemNet
  Graph_RAG -- 21 --> AutoResearch
  MemNet -- 21 --> LiteLLM
  AI_Factory -- 20 --> Automerge
  LiteParse -- 20 --> Wikontic
  Hybrid_RAG -- 20 --> Yjs
  SENTINEL -- 20 --> Yjs
  AutoResearch -- 20 --> Wikontic
  Hybrid_RAG -- 19 --> Automerge
  MemNet -- 19 --> Tool_Search
  MemNet -- 19 --> Automerge
  Auto_AI_Router -- 19 --> Automerge
  Svyazi -- 18 --> Firecrawl
  Rufler -- 18 --> Wikontic
  Legal_RAG -- 18 --> Yjs
  Graph_RAG -- 18 --> Yjs
  SENTINEL -- 18 --> Automerge
  knowledge_space -- 17 --> Firecrawl
  mclaude -- 17 --> Wikontic
  LiteLLM -- 17 --> Yjs
  LiteLLM -- 17 --> Automerge
  AgentFS -- 16 --> Firecrawl
  Legal_RAG -- 16 --> Automerge
  Graph_RAG -- 16 --> Automerge
  SENTINEL -- 16 --> Wikontic
  Wikontic -- 16 --> Yjs
  AI_Factory -- 15 --> Wikontic
  Rufler -- 15 --> Firecrawl
  Yodoca -- 15 --> Firecrawl
  SENTINEL -- 15 --> Firecrawl
  CardIndex -- 14 --> Firecrawl
  Hybrid_RAG -- 14 --> Wikontic
  Auto_AI_Router -- 14 --> Wikontic
  Tool_Search -- 14 --> Yjs
  Tool_Search -- 14 --> Automerge
  Wikontic -- 14 --> Automerge
  LiteParse -- 13 --> Firecrawl
  Graph_RAG -- 13 --> Wikontic
  Wikontic -- 12 --> Firecrawl
  mclaude -- 11 --> Firecrawl
  AI_Factory -- 11 --> Firecrawl
  Legal_RAG -- 11 --> Wikontic
  Hybrid_RAG -- 11 --> Firecrawl
  MemNet -- 11 --> Firecrawl
  LiteLLM -- 11 --> Wikontic
  Tool_Search -- 10 --> Wikontic
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
| **Svyazi** | **Yodoca** | 120 |
| **Svyazi** | **CardIndex** | 104 |
| **Svyazi** | **AgentFS** | 85 |
| **Svyazi** | **knowledge-space** | 81 |
| **Svyazi** | **mclaude** | 80 |
| **Svyazi** | **NGT Memory** | 77 |
| **CardIndex** | **Yodoca** | 77 |
| **Svyazi** | **Rufler** | 75 |
| **AgentFS** | **Yodoca** | 74 |
| **CardIndex** | **AgentFS** | 73 |
| **Svyazi** | **LiteParse** | 72 |
| **Svyazi** | **AI Factory** | 70 |
| **AgentFS** | **knowledge-space** | 70 |
| **knowledge-space** | **Yodoca** | 68 |
| **mclaude** | **Yodoca** | 67 |
| **Yodoca** | **NGT Memory** | 66 |
| **Svyazi** | **MemNet** | 63 |
| **AgentFS** | **LiteParse** | 62 |
| **mclaude** | **AI Factory** | 62 |
| **Rufler** | **Yodoca** | 62 |
| **Svyazi** | **SENTINEL** | 61 |
| **CardIndex** | **knowledge-space** | 61 |
| **mclaude** | **Rufler** | 60 |
| **LiteParse** | **Yodoca** | 60 |
| **Yodoca** | **MemNet** | 60 |

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
  Svyazi -> CardIndex [label="104"];
  Svyazi -> AgentFS [label="85"];
  Svyazi -> knowledge_space [label="81"];
  Svyazi -> mclaude [label="80"];
  Svyazi -> AI_Factory [label="70"];
  Svyazi -> Rufler [label="75"];
  Svyazi -> LiteParse [label="72"];
  Svyazi -> Legal_RAG [label="47"];
  Svyazi -> Hybrid_RAG [label="43"];
  Svyazi -> Graph_RAG [label="42"];
  Svyazi -> Yodoca [label="120"];
  Svyazi -> NGT_Memory [label="77"];
  Svyazi -> MemNet [label="63"];
  Svyazi -> SENTINEL [label="61"];
  Svyazi -> LiteLLM [label="44"];
  Svyazi -> Auto_AI_Router [label="56"];
  Svyazi -> Tool_Search [label="47"];
  Svyazi -> AutoResearch [label="53"];
  Svyazi -> Wikontic [label="37"];
  Svyazi -> Firecrawl [label="18"];
  Svyazi -> Yjs [label="39"];
  Svyazi -> Automerge [label="30"];
  CardIndex -> AgentFS [label="73"];
  CardIndex -> knowledge_space [label="61"];
  CardIndex -> mclaude [label="54"];
  CardIndex -> AI_Factory [label="50"];
  CardIndex -> Rufler [label="54"];
  CardIndex -> LiteParse [label="58"];
  CardIndex -> Legal_RAG [label="38"];
  CardIndex -> Hybrid_RAG [label="37"];
  CardIndex -> Graph_RAG [label="32"];
  CardIndex -> Yodoca [label="77"];
  CardIndex -> NGT_Memory [label="57"];
  CardIndex -> MemNet [label="36"];
  CardIndex -> SENTINEL [label="50"];
  CardIndex -> LiteLLM [label="36"];
  CardIndex -> Auto_AI_Router [label="45"];
  CardIndex -> Tool_Search [label="38"];
  CardIndex -> AutoResearch [label="37"];
  CardIndex -> Wikontic [label="30"];
  CardIndex -> Firecrawl [label="14"];
  CardIndex -> Yjs [label="34"];
  CardIndex -> Automerge [label="25"];
  AgentFS -> knowledge_space [label="70"];
  AgentFS -> mclaude [label="59"];
  AgentFS -> AI_Factory [label="54"];
  AgentFS -> Rufler [label="56"];
  AgentFS -> LiteParse [label="62"];
  AgentFS -> Legal_RAG [label="39"];
  AgentFS -> Hybrid_RAG [label="38"];
  AgentFS -> Graph_RAG [label="35"];
  AgentFS -> Yodoca [label="74"];
  AgentFS -> NGT_Memory [label="51"];
  AgentFS -> MemNet [label="32"];
  AgentFS -> SENTINEL [label="56"];
  AgentFS -> LiteLLM [label="37"];
  AgentFS -> Auto_AI_Router [label="42"];
  AgentFS -> Tool_Search [label="40"];
  AgentFS -> AutoResearch [label="39"];
  AgentFS -> Wikontic [label="22"];
  AgentFS -> Firecrawl [label="16"];
  AgentFS -> Yjs [label="29"];
  AgentFS -> Automerge [label="26"];
  knowledge_space -> mclaude [label="59"];
  knowledge_space -> AI_Factory [label="45"];
  knowledge_space -> Rufler [label="57"];
  knowledge_space -> LiteParse [label="52"];
  knowledge_space -> Legal_RAG [label="34"];
  knowledge_space -> Hybrid_RAG [label="33"];
  knowledge_space -> Graph_RAG [label="30"];
  knowledge_space -> Yodoca [label="68"];
  knowledge_space -> NGT_Memory [label="51"];
  knowledge_space -> MemNet [label="41"];
  knowledge_space -> SENTINEL [label="42"];
  knowledge_space -> LiteLLM [label="30"];
  knowledge_space -> Auto_AI_Router [label="36"];
  knowledge_space -> Tool_Search [label="30"];
  knowledge_space -> AutoResearch [label="35"];
  knowledge_space -> Wikontic [label="26"];
  knowledge_space -> Firecrawl [label="17"];
  knowledge_space -> Yjs [label="28"];
  knowledge_space -> Automerge [label="25"];
  mclaude -> AI_Factory [label="62"];
  mclaude -> Rufler [label="60"];
  mclaude -> LiteParse [label="55"];
  mclaude -> Legal_RAG [label="35"];
  mclaude -> Hybrid_RAG [label="33"];
  mclaude -> Graph_RAG [label="31"];
  mclaude -> Yodoca [label="67"];
  mclaude -> NGT_Memory [label="49"];
  mclaude -> MemNet [label="35"];
  mclaude -> SENTINEL [label="41"];
  mclaude -> LiteLLM [label="31"];
  mclaude -> Auto_AI_Router [label="36"];
  mclaude -> Tool_Search [label="31"];
  mclaude -> AutoResearch [label="40"];
  mclaude -> Wikontic [label="17"];
  mclaude -> Firecrawl [label="11"];
  mclaude -> Yjs [label="25"];
  mclaude -> Automerge [label="23"];
  AI_Factory -> Rufler [label="54"];
  AI_Factory -> LiteParse [label="50"];
  AI_Factory -> Legal_RAG [label="36"];
  AI_Factory -> Hybrid_RAG [label="33"];
  AI_Factory -> Graph_RAG [label="30"];
  AI_Factory -> Yodoca [label="56"];
  AI_Factory -> NGT_Memory [label="48"];
  AI_Factory -> MemNet [label="26"];
  AI_Factory -> SENTINEL [label="46"];
  AI_Factory -> LiteLLM [label="34"];
  AI_Factory -> Auto_AI_Router [label="40"];
  AI_Factory -> Tool_Search [label="35"];
  AI_Factory -> AutoResearch [label="38"];
  AI_Factory -> Wikontic [label="15"];
  AI_Factory -> Firecrawl [label="11"];
  AI_Factory -> Yjs [label="22"];
  AI_Factory -> Automerge [label="20"];
  Rufler -> LiteParse [label="51"];
  Rufler -> Legal_RAG [label="32"];
  Rufler -> Hybrid_RAG [label="33"];
  Rufler -> Graph_RAG [label="28"];
  Rufler -> Yodoca [label="62"];
  Rufler -> NGT_Memory [label="38"];
  Rufler -> MemNet [label="37"];
  Rufler -> SENTINEL [label="47"];
  Rufler -> LiteLLM [label="31"];
  Rufler -> Auto_AI_Router [label="35"];
  Rufler -> Tool_Search [label="33"];
  Rufler -> AutoResearch [label="39"];
  Rufler -> Wikontic [label="18"];
  Rufler -> Firecrawl [label="15"];
  Rufler -> Yjs [label="26"];
  Rufler -> Automerge [label="25"];
  LiteParse -> Legal_RAG [label="48"];
  LiteParse -> Hybrid_RAG [label="42"];
  LiteParse -> Graph_RAG [label="41"];
  LiteParse -> Yodoca [label="60"];
  LiteParse -> NGT_Memory [label="44"];
  LiteParse -> MemNet [label="33"];
  LiteParse -> SENTINEL [label="48"];
  LiteParse -> LiteLLM [label="38"];
  LiteParse -> Auto_AI_Router [label="43"];
  LiteParse -> Tool_Search [label="38"];
  LiteParse -> AutoResearch [label="37"];
  LiteParse -> Wikontic [label="20"];
  LiteParse -> Firecrawl [label="13"];
  LiteParse -> Yjs [label="27"];
  LiteParse -> Automerge [label="24"];
  Legal_RAG -> Hybrid_RAG [label="37"];
  Legal_RAG -> Graph_RAG [label="39"];
  Legal_RAG -> Yodoca [label="37"];
  Legal_RAG -> NGT_Memory [label="35"];
  Legal_RAG -> MemNet [label="22"];
  Legal_RAG -> SENTINEL [label="36"];
  Legal_RAG -> LiteLLM [label="30"];
  Legal_RAG -> Auto_AI_Router [label="35"];
  Legal_RAG -> Tool_Search [label="30"];
  Legal_RAG -> AutoResearch [label="22"];
  Legal_RAG -> Wikontic [label="11"];
  Legal_RAG -> Firecrawl [label="8"];
  Legal_RAG -> Yjs [label="18"];
  Legal_RAG -> Automerge [label="16"];
  Hybrid_RAG -> Graph_RAG [label="36"];
  Hybrid_RAG -> Yodoca [label="37"];
  Hybrid_RAG -> NGT_Memory [label="34"];
  Hybrid_RAG -> MemNet [label="21"];
  Hybrid_RAG -> SENTINEL [label="34"];
  Hybrid_RAG -> LiteLLM [label="30"];
  Hybrid_RAG -> Auto_AI_Router [label="33"];
  Hybrid_RAG -> Tool_Search [label="26"];
  Hybrid_RAG -> AutoResearch [label="25"];
  Hybrid_RAG -> Wikontic [label="14"];
  Hybrid_RAG -> Firecrawl [label="11"];
  Hybrid_RAG -> Yjs [label="20"];
  Hybrid_RAG -> Automerge [label="19"];
  Graph_RAG -> Yodoca [label="31"];
  Graph_RAG -> NGT_Memory [label="30"];
  Graph_RAG -> MemNet [label="21"];
  Graph_RAG -> SENTINEL [label="35"];
  Graph_RAG -> LiteLLM [label="25"];
  Graph_RAG -> Auto_AI_Router [label="30"];
  Graph_RAG -> Tool_Search [label="24"];
  Graph_RAG -> AutoResearch [label="21"];
  Graph_RAG -> Wikontic [label="13"];
  Graph_RAG -> Firecrawl [label="9"];
  Graph_RAG -> Yjs [label="18"];
  Graph_RAG -> Automerge [label="16"];
  Yodoca -> NGT_Memory [label="66"];
  Yodoca -> MemNet [label="60"];
  Yodoca -> SENTINEL [label="50"];
  Yodoca -> LiteLLM [label="36"];
  Yodoca -> Auto_AI_Router [label="43"];
  Yodoca -> Tool_Search [label="37"];
  Yodoca -> AutoResearch [label="45"];
  Yodoca -> Wikontic [label="36"];
  Yodoca -> Firecrawl [label="15"];
  Yodoca -> Yjs [label="29"];
  Yodoca -> Automerge [label="26"];
  NGT_Memory -> MemNet [label="32"];
  NGT_Memory -> SENTINEL [label="38"];
  NGT_Memory -> LiteLLM [label="34"];
  NGT_Memory -> Auto_AI_Router [label="43"];
  NGT_Memory -> Tool_Search [label="31"];
  NGT_Memory -> AutoResearch [label="34"];
  NGT_Memory -> Wikontic [label="31"];
  NGT_Memory -> Firecrawl [label="9"];
  NGT_Memory -> Yjs [label="28"];
  NGT_Memory -> Automerge [label="23"];
  MemNet -> SENTINEL [label="25"];
  MemNet -> LiteLLM [label="21"];
  MemNet -> Auto_AI_Router [label="26"];
  MemNet -> Tool_Search [label="19"];
  MemNet -> AutoResearch [label="28"];
  MemNet -> Wikontic [label="28"];
  MemNet -> Firecrawl [label="11"];
  MemNet -> Yjs [label="22"];
  MemNet -> Automerge [label="19"];
  SENTINEL -> LiteLLM [label="41"];
  SENTINEL -> Auto_AI_Router [label="46"];
  SENTINEL -> Tool_Search [label="44"];
  SENTINEL -> AutoResearch [label="27"];
  SENTINEL -> Wikontic [label="16"];
  SENTINEL -> Firecrawl [label="15"];
  SENTINEL -> Yjs [label="20"];
  SENTINEL -> Automerge [label="18"];
  LiteLLM -> Auto_AI_Router [label="48"];
  LiteLLM -> Tool_Search [label="41"];
  LiteLLM -> AutoResearch [label="28"];
  LiteLLM -> Wikontic [label="11"];
  LiteLLM -> Firecrawl [label="9"];
  LiteLLM -> Yjs [label="17"];
  LiteLLM -> Automerge [label="17"];
  Auto_AI_Router -> Tool_Search [label="42"];
  Auto_AI_Router -> AutoResearch [label="32"];
  Auto_AI_Router -> Wikontic [label="14"];
  Auto_AI_Router -> Firecrawl [label="9"];
  Auto_AI_Router -> Yjs [label="24"];
  Auto_AI_Router -> Automerge [label="19"];
  Tool_Search -> AutoResearch [label="24"];
  Tool_Search -> Wikontic [label="10"];
  Tool_Search -> Firecrawl [label="9"];
  Tool_Search -> Yjs [label="14"];
  Tool_Search -> Automerge [label="14"];
  AutoResearch -> Wikontic [label="20"];
  AutoResearch -> Firecrawl [label="9"];
  AutoResearch -> Yjs [label="26"];
  AutoResearch -> Automerge [label="24"];
  Wikontic -> Firecrawl [label="12"];
  Wikontic -> Yjs [label="16"];
  Wikontic -> Automerge [label="14"];
  Firecrawl -> Yjs [label="9"];
  Firecrawl -> Automerge [label="9"];
  Yjs -> Automerge [label="34"];
}
```

<!-- see-also -->

---

**Смотрите также:**
- [NETWORK](docs/NETWORK.md)
- [GLOSSARY](docs/GLOSSARY.md)
- [MINDMAP](docs/MINDMAP.md)
- [MISSING](docs/MISSING.md)

