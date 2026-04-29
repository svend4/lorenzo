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
  Svyazi -- 126 --> Yodoca
  Svyazi -- 122 --> CardIndex
  Svyazi -- 93 --> AgentFS
  Svyazi -- 91 --> MemNet
  Svyazi -- 88 --> knowledge_space
  Svyazi -- 84 --> NGT_Memory
  Svyazi -- 83 --> mclaude
  CardIndex -- 81 --> Yodoca
  Svyazi -- 79 --> Rufler
  AgentFS -- 78 --> Yodoca
  CardIndex -- 77 --> AgentFS
  Svyazi -- 75 --> AI_Factory
  Svyazi -- 75 --> LiteParse
  AgentFS -- 73 --> knowledge_space
  Yodoca -- 70 --> NGT_Memory
  knowledge_space -- 69 --> Yodoca
  mclaude -- 69 --> Yodoca
  Yodoca -- 68 --> MemNet
  Svyazi -- 65 --> SENTINEL
  Rufler -- 65 --> Yodoca
  CardIndex -- 64 --> knowledge_space
  mclaude -- 64 --> AI_Factory
  mclaude -- 63 --> Rufler
  Svyazi -- 62 --> Auto_AI_Router
  AgentFS -- 62 --> LiteParse
  AgentFS -- 61 --> mclaude
  knowledge_space -- 61 --> mclaude
  LiteParse -- 61 --> Yodoca
  CardIndex -- 60 --> NGT_Memory
  knowledge_space -- 60 --> Rufler
  AgentFS -- 59 --> Rufler
  AI_Factory -- 59 --> Yodoca
  CardIndex -- 58 --> LiteParse
  AgentFS -- 58 --> AI_Factory
  CardIndex -- 57 --> Rufler
  AI_Factory -- 57 --> Rufler
  CardIndex -- 56 --> mclaude
  AgentFS -- 56 --> SENTINEL
  mclaude -- 56 --> LiteParse
  CardIndex -- 54 --> AI_Factory
  AgentFS -- 54 --> NGT_Memory
  Svyazi -- 53 --> AutoResearch
  knowledge_space -- 53 --> NGT_Memory
  Rufler -- 53 --> LiteParse
  knowledge_space -- 52 --> LiteParse
  AI_Factory -- 51 --> LiteParse
  Yodoca -- 51 --> SENTINEL
  Svyazi -- 50 --> Tool_Search
  CardIndex -- 50 --> SENTINEL
  mclaude -- 50 --> NGT_Memory
  AI_Factory -- 50 --> NGT_Memory
  LiteLLM -- 50 --> Auto_AI_Router
  Svyazi -- 49 --> Legal_RAG
  knowledge_space -- 49 --> AI_Factory
  LiteParse -- 49 --> SENTINEL
  Svyazi -- 48 --> LiteLLM
  Rufler -- 48 --> SENTINEL
  LiteParse -- 48 --> Legal_RAG
  CardIndex -- 47 --> Auto_AI_Router
  knowledge_space -- 47 --> MemNet
  SENTINEL -- 47 --> Auto_AI_Router
  Svyazi -- 46 --> Hybrid_RAG
  Svyazi -- 46 --> Graph_RAG
  CardIndex -- 46 --> MemNet
  AI_Factory -- 46 --> SENTINEL
  LiteParse -- 45 --> NGT_Memory
  Yodoca -- 45 --> Auto_AI_Router
  Yodoca -- 45 --> AutoResearch
  SENTINEL -- 45 --> Tool_Search
  LiteParse -- 44 --> Auto_AI_Router
  AgentFS -- 43 --> Auto_AI_Router
  LiteParse -- 43 --> Hybrid_RAG
  NGT_Memory -- 43 --> Auto_AI_Router
  SENTINEL -- 43 --> LiteLLM
  Auto_AI_Router -- 43 --> Tool_Search
  knowledge_space -- 42 --> SENTINEL
  mclaude -- 42 --> SENTINEL
  Rufler -- 42 --> MemNet
  LiteParse -- 42 --> Graph_RAG
  LiteLLM -- 42 --> Tool_Search
  AI_Factory -- 41 --> Auto_AI_Router
  Svyazi -- 40 --> Wikontic
  AgentFS -- 40 --> Tool_Search
  Rufler -- 40 --> NGT_Memory
  Rufler -- 40 --> AutoResearch
  LiteParse -- 40 --> LiteLLM
  AgentFS -- 39 --> MemNet
  AgentFS -- 39 --> AutoResearch
  mclaude -- 39 --> MemNet
  mclaude -- 39 --> AutoResearch
  LiteParse -- 39 --> Tool_Search
  Legal_RAG -- 39 --> Graph_RAG
  NGT_Memory -- 39 --> SENTINEL
  Svyazi -- 38 --> Yjs
  CardIndex -- 38 --> Tool_Search
  AgentFS -- 38 --> Legal_RAG
  AgentFS -- 38 --> Hybrid_RAG
  AgentFS -- 38 --> LiteLLM
  AI_Factory -- 38 --> AutoResearch
  Legal_RAG -- 38 --> Hybrid_RAG
  Hybrid_RAG -- 38 --> Yodoca
  Yodoca -- 38 --> LiteLLM
  Yodoca -- 38 --> Tool_Search
  CardIndex -- 37 --> Legal_RAG
  CardIndex -- 37 --> Hybrid_RAG
  CardIndex -- 37 --> LiteLLM
  CardIndex -- 37 --> AutoResearch
  knowledge_space -- 37 --> Auto_AI_Router
  mclaude -- 37 --> Auto_AI_Router
  LiteParse -- 37 --> AutoResearch
  Legal_RAG -- 37 --> Yodoca
  Yodoca -- 37 --> Wikontic
  NGT_Memory -- 37 --> MemNet
  AI_Factory -- 36 --> Legal_RAG
  AI_Factory -- 36 --> LiteLLM
  AI_Factory -- 36 --> Tool_Search
  Rufler -- 36 --> Auto_AI_Router
  LiteParse -- 36 --> MemNet
  Legal_RAG -- 36 --> SENTINEL
  Hybrid_RAG -- 36 --> Graph_RAG
  Graph_RAG -- 36 --> SENTINEL
  AgentFS -- 35 --> Graph_RAG
  mclaude -- 35 --> Legal_RAG
  Rufler -- 35 --> Hybrid_RAG
  Legal_RAG -- 35 --> NGT_Memory
  Legal_RAG -- 35 --> Auto_AI_Router
  Hybrid_RAG -- 35 --> NGT_Memory
  Hybrid_RAG -- 35 --> SENTINEL
  NGT_Memory -- 35 --> LiteLLM
  knowledge_space -- 34 --> AutoResearch
  mclaude -- 34 --> Hybrid_RAG
  AI_Factory -- 34 --> Hybrid_RAG
  Rufler -- 34 --> Tool_Search
  Hybrid_RAG -- 34 --> Auto_AI_Router
  CardIndex -- 33 --> Yjs
  knowledge_space -- 33 --> Legal_RAG
  knowledge_space -- 33 --> Hybrid_RAG
  mclaude -- 33 --> LiteLLM
  Rufler -- 33 --> Legal_RAG
  Rufler -- 33 --> LiteLLM
  Hybrid_RAG -- 33 --> LiteLLM
  NGT_Memory -- 33 --> AutoResearch
  Yjs -- 33 --> Automerge
  CardIndex -- 32 --> Graph_RAG
  mclaude -- 32 --> Graph_RAG
  mclaude -- 32 --> Tool_Search
  Legal_RAG -- 32 --> LiteLLM
  Graph_RAG -- 32 --> Yodoca
  NGT_Memory -- 32 --> Wikontic
  knowledge_space -- 31 --> LiteLLM
  AI_Factory -- 31 --> MemNet
  Legal_RAG -- 31 --> Tool_Search
  Graph_RAG -- 31 --> NGT_Memory
  Graph_RAG -- 31 --> Auto_AI_Router
  NGT_Memory -- 31 --> Tool_Search
  Auto_AI_Router -- 31 --> AutoResearch
  CardIndex -- 30 --> Wikontic
  knowledge_space -- 30 --> Graph_RAG
  knowledge_space -- 30 --> Tool_Search
  AI_Factory -- 30 --> Graph_RAG
  MemNet -- 30 --> Auto_AI_Router
  MemNet -- 30 --> Wikontic
  Svyazi -- 29 --> Automerge
  Rufler -- 29 --> Graph_RAG
  MemNet -- 29 --> AutoResearch
  LiteLLM -- 29 --> AutoResearch
  AgentFS -- 28 --> Yjs
  Hybrid_RAG -- 28 --> Tool_Search
  Yodoca -- 28 --> Yjs
  MemNet -- 28 --> SENTINEL
  knowledge_space -- 27 --> Yjs
  Graph_RAG -- 27 --> LiteLLM
  NGT_Memory -- 27 --> Yjs
  SENTINEL -- 27 --> AutoResearch
  Rufler -- 26 --> Yjs
  LiteParse -- 26 --> Yjs
  AgentFS -- 25 --> Automerge
  knowledge_space -- 25 --> Wikontic
  Hybrid_RAG -- 25 --> AutoResearch
  Graph_RAG -- 25 --> MemNet
  Graph_RAG -- 25 --> Tool_Search
  Yodoca -- 25 --> Automerge
  AutoResearch -- 25 --> Yjs
  CardIndex -- 24 --> Automerge
  knowledge_space -- 24 --> Automerge
  mclaude -- 24 --> Yjs
  Rufler -- 24 --> Automerge
  Legal_RAG -- 24 --> MemNet
  MemNet -- 24 --> LiteLLM
  Tool_Search -- 24 --> AutoResearch
  LiteParse -- 23 --> Automerge
  Hybrid_RAG -- 23 --> MemNet
  MemNet -- 23 --> Yjs
  Auto_AI_Router -- 23 --> Yjs
  AutoResearch -- 23 --> Automerge
  AgentFS -- 22 --> Wikontic
  mclaude -- 22 --> Automerge
  Legal_RAG -- 22 --> AutoResearch
  NGT_Memory -- 22 --> Automerge
  AI_Factory -- 21 --> Yjs
  Graph_RAG -- 21 --> AutoResearch
  MemNet -- 20 --> Tool_Search
  Svyazi -- 19 --> Firecrawl
  AI_Factory -- 19 --> Automerge
  Rufler -- 19 --> Wikontic
  LiteParse -- 19 --> Wikontic
  Hybrid_RAG -- 19 --> Yjs
  MemNet -- 19 --> Automerge
  SENTINEL -- 19 --> Yjs
  AutoResearch -- 19 --> Wikontic
  knowledge_space -- 18 --> Firecrawl
  Hybrid_RAG -- 18 --> Automerge
  LiteLLM -- 18 --> Yjs
  Auto_AI_Router -- 18 --> Automerge
  AgentFS -- 17 --> Firecrawl
  Legal_RAG -- 17 --> Yjs
  Graph_RAG -- 17 --> Yjs
  SENTINEL -- 17 --> Automerge
  LiteLLM -- 17 --> Automerge
  mclaude -- 16 --> Wikontic
  AI_Factory -- 16 --> Wikontic
  Rufler -- 16 --> Firecrawl
  Yodoca -- 16 --> Firecrawl
  CardIndex -- 15 --> Firecrawl
  Legal_RAG -- 15 --> Automerge
  Graph_RAG -- 15 --> Automerge
  SENTINEL -- 15 --> Wikontic
  SENTINEL -- 15 --> Firecrawl
  Wikontic -- 15 --> Yjs
  Auto_AI_Router -- 14 --> Wikontic
  Tool_Search -- 14 --> Yjs
  Tool_Search -- 14 --> Automerge
  LiteParse -- 13 --> Firecrawl
  Hybrid_RAG -- 13 --> Wikontic
  MemNet -- 13 --> Firecrawl
  Wikontic -- 13 --> Automerge
  mclaude -- 12 --> Firecrawl
  AI_Factory -- 12 --> Firecrawl
  Graph_RAG -- 12 --> Wikontic
  LiteLLM -- 12 --> Wikontic
  Wikontic -- 12 --> Firecrawl
  Hybrid_RAG -- 11 --> Firecrawl
  Legal_RAG -- 10 --> Wikontic
  NGT_Memory -- 10 --> Firecrawl
  Tool_Search -- 10 --> Wikontic
  Graph_RAG -- 9 --> Firecrawl
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
| **Svyazi** | **Yodoca** | 126 |
| **Svyazi** | **CardIndex** | 122 |
| **Svyazi** | **AgentFS** | 93 |
| **Svyazi** | **MemNet** | 91 |
| **Svyazi** | **knowledge-space** | 88 |
| **Svyazi** | **NGT Memory** | 84 |
| **Svyazi** | **mclaude** | 83 |
| **CardIndex** | **Yodoca** | 81 |
| **Svyazi** | **Rufler** | 79 |
| **AgentFS** | **Yodoca** | 78 |
| **CardIndex** | **AgentFS** | 77 |
| **Svyazi** | **AI Factory** | 75 |
| **Svyazi** | **LiteParse** | 75 |
| **AgentFS** | **knowledge-space** | 73 |
| **Yodoca** | **NGT Memory** | 70 |
| **knowledge-space** | **Yodoca** | 69 |
| **mclaude** | **Yodoca** | 69 |
| **Yodoca** | **MemNet** | 68 |
| **Svyazi** | **SENTINEL** | 65 |
| **Rufler** | **Yodoca** | 65 |
| **CardIndex** | **knowledge-space** | 64 |
| **mclaude** | **AI Factory** | 64 |
| **mclaude** | **Rufler** | 63 |
| **Svyazi** | **Auto AI Router** | 62 |
| **AgentFS** | **LiteParse** | 62 |

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
  Svyazi -> CardIndex [label="122"];
  Svyazi -> AgentFS [label="93"];
  Svyazi -> knowledge_space [label="88"];
  Svyazi -> mclaude [label="83"];
  Svyazi -> AI_Factory [label="75"];
  Svyazi -> Rufler [label="79"];
  Svyazi -> LiteParse [label="75"];
  Svyazi -> Legal_RAG [label="49"];
  Svyazi -> Hybrid_RAG [label="46"];
  Svyazi -> Graph_RAG [label="46"];
  Svyazi -> Yodoca [label="126"];
  Svyazi -> NGT_Memory [label="84"];
  Svyazi -> MemNet [label="91"];
  Svyazi -> SENTINEL [label="65"];
  Svyazi -> LiteLLM [label="48"];
  Svyazi -> Auto_AI_Router [label="62"];
  Svyazi -> Tool_Search [label="50"];
  Svyazi -> AutoResearch [label="53"];
  Svyazi -> Wikontic [label="40"];
  Svyazi -> Firecrawl [label="19"];
  Svyazi -> Yjs [label="38"];
  Svyazi -> Automerge [label="29"];
  CardIndex -> AgentFS [label="77"];
  CardIndex -> knowledge_space [label="64"];
  CardIndex -> mclaude [label="56"];
  CardIndex -> AI_Factory [label="54"];
  CardIndex -> Rufler [label="57"];
  CardIndex -> LiteParse [label="58"];
  CardIndex -> Legal_RAG [label="37"];
  CardIndex -> Hybrid_RAG [label="37"];
  CardIndex -> Graph_RAG [label="32"];
  CardIndex -> Yodoca [label="81"];
  CardIndex -> NGT_Memory [label="60"];
  CardIndex -> MemNet [label="46"];
  CardIndex -> SENTINEL [label="50"];
  CardIndex -> LiteLLM [label="37"];
  CardIndex -> Auto_AI_Router [label="47"];
  CardIndex -> Tool_Search [label="38"];
  CardIndex -> AutoResearch [label="37"];
  CardIndex -> Wikontic [label="30"];
  CardIndex -> Firecrawl [label="15"];
  CardIndex -> Yjs [label="33"];
  CardIndex -> Automerge [label="24"];
  AgentFS -> knowledge_space [label="73"];
  AgentFS -> mclaude [label="61"];
  AgentFS -> AI_Factory [label="58"];
  AgentFS -> Rufler [label="59"];
  AgentFS -> LiteParse [label="62"];
  AgentFS -> Legal_RAG [label="38"];
  AgentFS -> Hybrid_RAG [label="38"];
  AgentFS -> Graph_RAG [label="35"];
  AgentFS -> Yodoca [label="78"];
  AgentFS -> NGT_Memory [label="54"];
  AgentFS -> MemNet [label="39"];
  AgentFS -> SENTINEL [label="56"];
  AgentFS -> LiteLLM [label="38"];
  AgentFS -> Auto_AI_Router [label="43"];
  AgentFS -> Tool_Search [label="40"];
  AgentFS -> AutoResearch [label="39"];
  AgentFS -> Wikontic [label="22"];
  AgentFS -> Firecrawl [label="17"];
  AgentFS -> Yjs [label="28"];
  AgentFS -> Automerge [label="25"];
  knowledge_space -> mclaude [label="61"];
  knowledge_space -> AI_Factory [label="49"];
  knowledge_space -> Rufler [label="60"];
  knowledge_space -> LiteParse [label="52"];
  knowledge_space -> Legal_RAG [label="33"];
  knowledge_space -> Hybrid_RAG [label="33"];
  knowledge_space -> Graph_RAG [label="30"];
  knowledge_space -> Yodoca [label="69"];
  knowledge_space -> NGT_Memory [label="53"];
  knowledge_space -> MemNet [label="47"];
  knowledge_space -> SENTINEL [label="42"];
  knowledge_space -> LiteLLM [label="31"];
  knowledge_space -> Auto_AI_Router [label="37"];
  knowledge_space -> Tool_Search [label="30"];
  knowledge_space -> AutoResearch [label="34"];
  knowledge_space -> Wikontic [label="25"];
  knowledge_space -> Firecrawl [label="18"];
  knowledge_space -> Yjs [label="27"];
  knowledge_space -> Automerge [label="24"];
  mclaude -> AI_Factory [label="64"];
  mclaude -> Rufler [label="63"];
  mclaude -> LiteParse [label="56"];
  mclaude -> Legal_RAG [label="35"];
  mclaude -> Hybrid_RAG [label="34"];
  mclaude -> Graph_RAG [label="32"];
  mclaude -> Yodoca [label="69"];
  mclaude -> NGT_Memory [label="50"];
  mclaude -> MemNet [label="39"];
  mclaude -> SENTINEL [label="42"];
  mclaude -> LiteLLM [label="33"];
  mclaude -> Auto_AI_Router [label="37"];
  mclaude -> Tool_Search [label="32"];
  mclaude -> AutoResearch [label="39"];
  mclaude -> Wikontic [label="16"];
  mclaude -> Firecrawl [label="12"];
  mclaude -> Yjs [label="24"];
  mclaude -> Automerge [label="22"];
  AI_Factory -> Rufler [label="57"];
  AI_Factory -> LiteParse [label="51"];
  AI_Factory -> Legal_RAG [label="36"];
  AI_Factory -> Hybrid_RAG [label="34"];
  AI_Factory -> Graph_RAG [label="30"];
  AI_Factory -> Yodoca [label="59"];
  AI_Factory -> NGT_Memory [label="50"];
  AI_Factory -> MemNet [label="31"];
  AI_Factory -> SENTINEL [label="46"];
  AI_Factory -> LiteLLM [label="36"];
  AI_Factory -> Auto_AI_Router [label="41"];
  AI_Factory -> Tool_Search [label="36"];
  AI_Factory -> AutoResearch [label="38"];
  AI_Factory -> Wikontic [label="16"];
  AI_Factory -> Firecrawl [label="12"];
  AI_Factory -> Yjs [label="21"];
  AI_Factory -> Automerge [label="19"];
  Rufler -> LiteParse [label="53"];
  Rufler -> Legal_RAG [label="33"];
  Rufler -> Hybrid_RAG [label="35"];
  Rufler -> Graph_RAG [label="29"];
  Rufler -> Yodoca [label="65"];
  Rufler -> NGT_Memory [label="40"];
  Rufler -> MemNet [label="42"];
  Rufler -> SENTINEL [label="48"];
  Rufler -> LiteLLM [label="33"];
  Rufler -> Auto_AI_Router [label="36"];
  Rufler -> Tool_Search [label="34"];
  Rufler -> AutoResearch [label="40"];
  Rufler -> Wikontic [label="19"];
  Rufler -> Firecrawl [label="16"];
  Rufler -> Yjs [label="26"];
  Rufler -> Automerge [label="24"];
  LiteParse -> Legal_RAG [label="48"];
  LiteParse -> Hybrid_RAG [label="43"];
  LiteParse -> Graph_RAG [label="42"];
  LiteParse -> Yodoca [label="61"];
  LiteParse -> NGT_Memory [label="45"];
  LiteParse -> MemNet [label="36"];
  LiteParse -> SENTINEL [label="49"];
  LiteParse -> LiteLLM [label="40"];
  LiteParse -> Auto_AI_Router [label="44"];
  LiteParse -> Tool_Search [label="39"];
  LiteParse -> AutoResearch [label="37"];
  LiteParse -> Wikontic [label="19"];
  LiteParse -> Firecrawl [label="13"];
  LiteParse -> Yjs [label="26"];
  LiteParse -> Automerge [label="23"];
  Legal_RAG -> Hybrid_RAG [label="38"];
  Legal_RAG -> Graph_RAG [label="39"];
  Legal_RAG -> Yodoca [label="37"];
  Legal_RAG -> NGT_Memory [label="35"];
  Legal_RAG -> MemNet [label="24"];
  Legal_RAG -> SENTINEL [label="36"];
  Legal_RAG -> LiteLLM [label="32"];
  Legal_RAG -> Auto_AI_Router [label="35"];
  Legal_RAG -> Tool_Search [label="31"];
  Legal_RAG -> AutoResearch [label="22"];
  Legal_RAG -> Wikontic [label="10"];
  Legal_RAG -> Firecrawl [label="8"];
  Legal_RAG -> Yjs [label="17"];
  Legal_RAG -> Automerge [label="15"];
  Hybrid_RAG -> Graph_RAG [label="36"];
  Hybrid_RAG -> Yodoca [label="38"];
  Hybrid_RAG -> NGT_Memory [label="35"];
  Hybrid_RAG -> MemNet [label="23"];
  Hybrid_RAG -> SENTINEL [label="35"];
  Hybrid_RAG -> LiteLLM [label="33"];
  Hybrid_RAG -> Auto_AI_Router [label="34"];
  Hybrid_RAG -> Tool_Search [label="28"];
  Hybrid_RAG -> AutoResearch [label="25"];
  Hybrid_RAG -> Wikontic [label="13"];
  Hybrid_RAG -> Firecrawl [label="11"];
  Hybrid_RAG -> Yjs [label="19"];
  Hybrid_RAG -> Automerge [label="18"];
  Graph_RAG -> Yodoca [label="32"];
  Graph_RAG -> NGT_Memory [label="31"];
  Graph_RAG -> MemNet [label="25"];
  Graph_RAG -> SENTINEL [label="36"];
  Graph_RAG -> LiteLLM [label="27"];
  Graph_RAG -> Auto_AI_Router [label="31"];
  Graph_RAG -> Tool_Search [label="25"];
  Graph_RAG -> AutoResearch [label="21"];
  Graph_RAG -> Wikontic [label="12"];
  Graph_RAG -> Firecrawl [label="9"];
  Graph_RAG -> Yjs [label="17"];
  Graph_RAG -> Automerge [label="15"];
  Yodoca -> NGT_Memory [label="70"];
  Yodoca -> MemNet [label="68"];
  Yodoca -> SENTINEL [label="51"];
  Yodoca -> LiteLLM [label="38"];
  Yodoca -> Auto_AI_Router [label="45"];
  Yodoca -> Tool_Search [label="38"];
  Yodoca -> AutoResearch [label="45"];
  Yodoca -> Wikontic [label="37"];
  Yodoca -> Firecrawl [label="16"];
  Yodoca -> Yjs [label="28"];
  Yodoca -> Automerge [label="25"];
  NGT_Memory -> MemNet [label="37"];
  NGT_Memory -> SENTINEL [label="39"];
  NGT_Memory -> LiteLLM [label="35"];
  NGT_Memory -> Auto_AI_Router [label="43"];
  NGT_Memory -> Tool_Search [label="31"];
  NGT_Memory -> AutoResearch [label="33"];
  NGT_Memory -> Wikontic [label="32"];
  NGT_Memory -> Firecrawl [label="10"];
  NGT_Memory -> Yjs [label="27"];
  NGT_Memory -> Automerge [label="22"];
  MemNet -> SENTINEL [label="28"];
  MemNet -> LiteLLM [label="24"];
  MemNet -> Auto_AI_Router [label="30"];
  MemNet -> Tool_Search [label="20"];
  MemNet -> AutoResearch [label="29"];
  MemNet -> Wikontic [label="30"];
  MemNet -> Firecrawl [label="13"];
  MemNet -> Yjs [label="23"];
  MemNet -> Automerge [label="19"];
  SENTINEL -> LiteLLM [label="43"];
  SENTINEL -> Auto_AI_Router [label="47"];
  SENTINEL -> Tool_Search [label="45"];
  SENTINEL -> AutoResearch [label="27"];
  SENTINEL -> Wikontic [label="15"];
  SENTINEL -> Firecrawl [label="15"];
  SENTINEL -> Yjs [label="19"];
  SENTINEL -> Automerge [label="17"];
  LiteLLM -> Auto_AI_Router [label="50"];
  LiteLLM -> Tool_Search [label="42"];
  LiteLLM -> AutoResearch [label="29"];
  LiteLLM -> Wikontic [label="12"];
  LiteLLM -> Firecrawl [label="9"];
  LiteLLM -> Yjs [label="18"];
  LiteLLM -> Automerge [label="17"];
  Auto_AI_Router -> Tool_Search [label="43"];
  Auto_AI_Router -> AutoResearch [label="31"];
  Auto_AI_Router -> Wikontic [label="14"];
  Auto_AI_Router -> Firecrawl [label="9"];
  Auto_AI_Router -> Yjs [label="23"];
  Auto_AI_Router -> Automerge [label="18"];
  Tool_Search -> AutoResearch [label="24"];
  Tool_Search -> Wikontic [label="10"];
  Tool_Search -> Firecrawl [label="9"];
  Tool_Search -> Yjs [label="14"];
  Tool_Search -> Automerge [label="14"];
  AutoResearch -> Wikontic [label="19"];
  AutoResearch -> Firecrawl [label="9"];
  AutoResearch -> Yjs [label="25"];
  AutoResearch -> Automerge [label="23"];
  Wikontic -> Firecrawl [label="12"];
  Wikontic -> Yjs [label="15"];
  Wikontic -> Automerge [label="13"];
  Firecrawl -> Yjs [label="9"];
  Firecrawl -> Automerge [label="9"];
  Yjs -> Automerge [label="33"];
}
```

<!-- see-also -->

---

**Смотрите также:**
- [GLOSSARY](docs/GLOSSARY.md)
- [NETWORK](docs/NETWORK.md)
- [MINDMAP](docs/MINDMAP.md)
- [ENTITIES](docs/ENTITIES.md)

