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
  Svyazi -- 150 --> Yodoca
  Svyazi -- 142 --> AgentFS
  AgentFS -- 131 --> Yodoca
  Svyazi -- 119 --> CardIndex
  CardIndex -- 114 --> AgentFS
  Svyazi -- 112 --> SENTINEL
  AgentFS -- 112 --> SENTINEL
  Svyazi -- 112 --> Rufler
  Svyazi -- 111 --> NGT_Memory
  AgentFS -- 107 --> Rufler
  CardIndex -- 105 --> Yodoca
  Rufler -- 103 --> Yodoca
  Svyazi -- 103 --> LiteParse
  Svyazi -- 102 --> knowledge_space
  Yodoca -- 102 --> NGT_Memory
  AgentFS -- 100 --> knowledge_space
  Rufler -- 100 --> SENTINEL
  Yodoca -- 99 --> SENTINEL
  Svyazi -- 99 --> Auto_AI_Router
  SENTINEL -- 99 --> Auto_AI_Router
  AgentFS -- 98 --> NGT_Memory
  Svyazi -- 94 --> mclaude
  CardIndex -- 93 --> knowledge_space
  Svyazi -- 93 --> AI_Factory
  knowledge_space -- 92 --> Yodoca
  AgentFS -- 92 --> LiteParse
  AgentFS -- 90 --> Auto_AI_Router
  CardIndex -- 89 --> Rufler
  AgentFS -- 88 --> AI_Factory
  AI_Factory -- 88 --> Yodoca
  mclaude -- 87 --> Yodoca
  CardIndex -- 86 --> SENTINEL
  CardIndex -- 86 --> AI_Factory
  CardIndex -- 86 --> LiteParse
  AgentFS -- 85 --> mclaude
  Rufler -- 85 --> LiteParse
  LiteParse -- 85 --> Yodoca
  knowledge_space -- 84 --> LiteParse
  mclaude -- 84 --> AI_Factory
  mclaude -- 84 --> LiteParse
  CardIndex -- 83 --> mclaude
  LiteParse -- 83 --> SENTINEL
  Yodoca -- 83 --> Auto_AI_Router
  CardIndex -- 82 --> NGT_Memory
  knowledge_space -- 82 --> NGT_Memory
  mclaude -- 81 --> Rufler
  NGT_Memory -- 81 --> Auto_AI_Router
  Rufler -- 80 --> Auto_AI_Router
  knowledge_space -- 79 --> Rufler
  Rufler -- 79 --> NGT_Memory
  NGT_Memory -- 79 --> SENTINEL
  AI_Factory -- 78 --> LiteParse
  LiteParse -- 77 --> Auto_AI_Router
  Svyazi -- 77 --> Legal_RAG
  knowledge_space -- 77 --> mclaude
  mclaude -- 77 --> NGT_Memory
  AI_Factory -- 77 --> Rufler
  Graph_RAG -- 77 --> SENTINEL
  knowledge_space -- 76 --> SENTINEL
  Svyazi -- 76 --> Graph_RAG
  Legal_RAG -- 75 --> SENTINEL
  Legal_RAG -- 75 --> Auto_AI_Router
  Graph_RAG -- 75 --> Auto_AI_Router
  AI_Factory -- 74 --> NGT_Memory
  knowledge_space -- 72 --> AI_Factory
  AgentFS -- 71 --> Legal_RAG
  mclaude -- 71 --> SENTINEL
  AI_Factory -- 71 --> SENTINEL
  Legal_RAG -- 71 --> Graph_RAG
  CardIndex -- 70 --> Auto_AI_Router
  LiteParse -- 70 --> Legal_RAG
  LiteParse -- 69 --> NGT_Memory
  AgentFS -- 68 --> Graph_RAG
  SENTINEL -- 66 --> Tool_Search
  Svyazi -- 66 --> MemNet
  knowledge_space -- 66 --> Auto_AI_Router
  Rufler -- 66 --> Legal_RAG
  Legal_RAG -- 66 --> Yodoca
  AgentFS -- 65 --> Tool_Search
  LiteLLM -- 65 --> Auto_AI_Router
  mclaude -- 65 --> Auto_AI_Router
  Rufler -- 64 --> Graph_RAG
  AI_Factory -- 63 --> Auto_AI_Router
  Graph_RAG -- 63 --> Yodoca
  Legal_RAG -- 62 --> NGT_Memory
  SENTINEL -- 62 --> LiteLLM
  CardIndex -- 61 --> Tool_Search
  LiteParse -- 61 --> Graph_RAG
  Graph_RAG -- 61 --> NGT_Memory
  Yodoca -- 61 --> MemNet
  Svyazi -- 60 --> Tool_Search
  LiteLLM -- 59 --> Tool_Search
  Auto_AI_Router -- 59 --> Tool_Search
  AgentFS -- 59 --> LiteLLM
  Yodoca -- 58 --> Tool_Search
  Svyazi -- 58 --> LiteLLM
  LiteParse -- 57 --> LiteLLM
  LiteParse -- 57 --> Tool_Search
  Svyazi -- 57 --> AutoResearch
  CardIndex -- 57 --> Legal_RAG
  CardIndex -- 57 --> LiteLLM
  Yodoca -- 56 --> Wikontic
  AI_Factory -- 56 --> LiteLLM
  AI_Factory -- 56 --> Tool_Search
  knowledge_space -- 55 --> Legal_RAG
  mclaude -- 55 --> Legal_RAG
  Svyazi -- 54 --> Wikontic
  Yodoca -- 54 --> LiteLLM
  AgentFS -- 52 --> AutoResearch
  AI_Factory -- 52 --> AutoResearch
  Rufler -- 52 --> Tool_Search
  Yodoca -- 52 --> AutoResearch
  CardIndex -- 51 --> Hybrid_RAG
  LiteParse -- 50 --> MemNet
  CardIndex -- 50 --> Graph_RAG
  CardIndex -- 50 --> AutoResearch
  mclaude -- 50 --> LiteLLM
  mclaude -- 50 --> Tool_Search
  LiteParse -- 50 --> Hybrid_RAG
  NGT_Memory -- 50 --> LiteLLM
  AgentFS -- 49 --> Hybrid_RAG
  knowledge_space -- 49 --> Tool_Search
  AI_Factory -- 49 --> Legal_RAG
  LiteParse -- 49 --> AutoResearch
  AgentFS -- 48 --> MemNet
  knowledge_space -- 48 --> Graph_RAG
  Rufler -- 48 --> LiteLLM
  Hybrid_RAG -- 48 --> Yodoca
  Svyazi -- 47 --> Hybrid_RAG
  knowledge_space -- 47 --> LiteLLM
  mclaude -- 47 --> Graph_RAG
  Rufler -- 47 --> AutoResearch
  CardIndex -- 46 --> MemNet
  mclaude -- 46 --> AutoResearch
  AI_Factory -- 46 --> Hybrid_RAG
  Legal_RAG -- 46 --> Hybrid_RAG
  Legal_RAG -- 46 --> LiteLLM
  Hybrid_RAG -- 46 --> Auto_AI_Router
  NGT_Memory -- 46 --> Tool_Search
  Hybrid_RAG -- 45 --> LiteLLM
  knowledge_space -- 44 --> MemNet
  mclaude -- 44 --> Hybrid_RAG
  Legal_RAG -- 44 --> Tool_Search
  Hybrid_RAG -- 44 --> NGT_Memory
  Hybrid_RAG -- 44 --> SENTINEL
  NGT_Memory -- 44 --> AutoResearch
  Rufler -- 43 --> MemNet
  MemNet -- 43 --> SENTINEL
  Auto_AI_Router -- 43 --> AutoResearch
  MemNet -- 42 --> Auto_AI_Router
  knowledge_space -- 42 --> AutoResearch
  knowledge_space -- 41 --> Hybrid_RAG
  AI_Factory -- 41 --> Graph_RAG
  Rufler -- 41 --> Hybrid_RAG
  Hybrid_RAG -- 41 --> Tool_Search
  SENTINEL -- 41 --> AutoResearch
  CardIndex -- 40 --> Wikontic
  Graph_RAG -- 40 --> LiteLLM
  MemNet -- 40 --> Wikontic
  LiteLLM -- 40 --> AutoResearch
  Svyazi -- 39 --> Yjs
  CardIndex -- 39 --> Yjs
  mclaude -- 39 --> MemNet
  Hybrid_RAG -- 39 --> Graph_RAG
  AI_Factory -- 38 --> MemNet
  Graph_RAG -- 38 --> Tool_Search
  NGT_Memory -- 38 --> MemNet
  AgentFS -- 37 --> Wikontic
  knowledge_space -- 37 --> Wikontic
  Yodoca -- 37 --> Yjs
  Legal_RAG -- 36 --> MemNet
  Tool_Search -- 36 --> AutoResearch
  AgentFS -- 35 --> Yjs
  knowledge_space -- 35 --> Yjs
  LiteParse -- 35 --> Yjs
  Graph_RAG -- 35 --> MemNet
  NGT_Memory -- 35 --> Wikontic
  NGT_Memory -- 35 --> Yjs
  AI_Factory -- 33 --> Yjs
  AutoResearch -- 33 --> Yjs
  Svyazi -- 32 --> Automerge
  CardIndex -- 32 --> Automerge
  Rufler -- 32 --> Yjs
  Yodoca -- 32 --> Automerge
  NGT_Memory -- 32 --> Automerge
  Yjs -- 32 --> Automerge
  mclaude -- 31 --> Yjs
  Hybrid_RAG -- 31 --> AutoResearch
  Auto_AI_Router -- 31 --> Yjs
  AgentFS -- 30 --> Automerge
  knowledge_space -- 30 --> Automerge
  AI_Factory -- 30 --> Automerge
  Rufler -- 30 --> Automerge
  LiteParse -- 30 --> Wikontic
  LiteParse -- 30 --> Automerge
  AutoResearch -- 30 --> Automerge
  Svyazi -- 29 --> Firecrawl
  CardIndex -- 29 --> Firecrawl
  Yodoca -- 29 --> Firecrawl
  MemNet -- 29 --> LiteLLM
  MemNet -- 29 --> Tool_Search
  Rufler -- 29 --> Wikontic
  Hybrid_RAG -- 29 --> Yjs
  SENTINEL -- 29 --> Yjs
  mclaude -- 28 --> Automerge
  Hybrid_RAG -- 28 --> Automerge
  MemNet -- 28 --> AutoResearch
  LiteLLM -- 28 --> Yjs
  LiteLLM -- 28 --> Automerge
  Auto_AI_Router -- 28 --> Automerge
  AgentFS -- 27 --> Firecrawl
  Legal_RAG -- 27 --> AutoResearch
  Graph_RAG -- 27 --> AutoResearch
  SENTINEL -- 27 --> Wikontic
  Rufler -- 26 --> Firecrawl
  SENTINEL -- 26 --> Firecrawl
  Hybrid_RAG -- 26 --> MemNet
  SENTINEL -- 26 --> Automerge
  knowledge_space -- 25 --> Firecrawl
  mclaude -- 25 --> Wikontic
  Legal_RAG -- 25 --> Yjs
  Graph_RAG -- 25 --> Yjs
  AI_Factory -- 24 --> Wikontic
  Tool_Search -- 24 --> Yjs
  Tool_Search -- 24 --> Automerge
  MemNet -- 23 --> Yjs
  Legal_RAG -- 22 --> Automerge
  Graph_RAG -- 22 --> Automerge
  Wikontic -- 22 --> Firecrawl
  LiteParse -- 21 --> Firecrawl
  Graph_RAG -- 21 --> Wikontic
  MemNet -- 21 --> Firecrawl
  Auto_AI_Router -- 21 --> Wikontic
  AI_Factory -- 20 --> Firecrawl
  AutoResearch -- 20 --> Wikontic
  Legal_RAG -- 19 --> Wikontic
  MemNet -- 18 --> Automerge
  Tool_Search -- 18 --> Wikontic
  Hybrid_RAG -- 17 --> Wikontic
  NGT_Memory -- 17 --> Firecrawl
  Wikontic -- 17 --> Yjs
  mclaude -- 16 --> Firecrawl
  Hybrid_RAG -- 16 --> Firecrawl
  LiteLLM -- 16 --> Wikontic
  LiteLLM -- 16 --> Firecrawl
  Auto_AI_Router -- 16 --> Firecrawl
  Tool_Search -- 16 --> Firecrawl
  AutoResearch -- 16 --> Firecrawl
  Firecrawl -- 16 --> Yjs
  Firecrawl -- 16 --> Automerge
  Legal_RAG -- 15 --> Firecrawl
  Graph_RAG -- 14 --> Firecrawl
  Wikontic -- 14 --> Automerge
```

## Топ совместных упоминаний

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 150 |
| **Svyazi** | **AgentFS** | 142 |
| **AgentFS** | **Yodoca** | 131 |
| **Svyazi** | **CardIndex** | 119 |
| **CardIndex** | **AgentFS** | 114 |
| **Svyazi** | **SENTINEL** | 112 |
| **AgentFS** | **SENTINEL** | 112 |
| **Svyazi** | **Rufler** | 112 |
| **Svyazi** | **NGT Memory** | 111 |
| **AgentFS** | **Rufler** | 107 |
| **CardIndex** | **Yodoca** | 105 |
| **Rufler** | **Yodoca** | 103 |
| **Svyazi** | **LiteParse** | 103 |
| **Svyazi** | **knowledge-space** | 102 |
| **Yodoca** | **NGT Memory** | 102 |
| **AgentFS** | **knowledge-space** | 100 |
| **Rufler** | **SENTINEL** | 100 |
| **Yodoca** | **SENTINEL** | 99 |
| **Svyazi** | **Auto AI Router** | 99 |
| **SENTINEL** | **Auto AI Router** | 99 |
| **AgentFS** | **NGT Memory** | 98 |
| **Svyazi** | **mclaude** | 94 |
| **CardIndex** | **knowledge-space** | 93 |
| **Svyazi** | **AI Factory** | 93 |
| **knowledge-space** | **Yodoca** | 92 |

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
  Svyazi -> CardIndex [label="119"];
  Svyazi -> AgentFS [label="142"];
  Svyazi -> Yodoca [label="150"];
  Svyazi -> Wikontic [label="54"];
  CardIndex -> AgentFS [label="114"];
  CardIndex -> Yodoca [label="105"];
  CardIndex -> Wikontic [label="40"];
  AgentFS -> Yodoca [label="131"];
  AgentFS -> Wikontic [label="37"];
  Yodoca -> Wikontic [label="56"];
  Svyazi -> SENTINEL [label="112"];
  Svyazi -> Tool_Search [label="60"];
  CardIndex -> SENTINEL [label="86"];
  CardIndex -> Tool_Search [label="61"];
  AgentFS -> SENTINEL [label="112"];
  AgentFS -> Tool_Search [label="65"];
  Yodoca -> SENTINEL [label="99"];
  Yodoca -> Tool_Search [label="58"];
  SENTINEL -> Tool_Search [label="66"];
  Svyazi -> knowledge_space [label="102"];
  Svyazi -> Rufler [label="112"];
  Svyazi -> Firecrawl [label="29"];
  CardIndex -> knowledge_space [label="93"];
  CardIndex -> Rufler [label="89"];
  CardIndex -> Firecrawl [label="29"];
  AgentFS -> knowledge_space [label="100"];
  AgentFS -> Rufler [label="107"];
  AgentFS -> Firecrawl [label="27"];
  knowledge_space -> Rufler [label="79"];
  knowledge_space -> Yodoca [label="92"];
  knowledge_space -> SENTINEL [label="76"];
  knowledge_space -> Firecrawl [label="25"];
  Rufler -> Yodoca [label="103"];
  Rufler -> SENTINEL [label="100"];
  Rufler -> Firecrawl [label="26"];
  Yodoca -> Firecrawl [label="29"];
  SENTINEL -> Firecrawl [label="26"];
  Svyazi -> LiteParse [label="103"];
  Svyazi -> MemNet [label="66"];
  Svyazi -> LiteLLM [label="58"];
  Svyazi -> Auto_AI_Router [label="99"];
  LiteParse -> MemNet [label="50"];
  LiteParse -> LiteLLM [label="57"];
  LiteParse -> Auto_AI_Router [label="77"];
  LiteParse -> Tool_Search [label="57"];
  MemNet -> LiteLLM [label="29"];
  MemNet -> Auto_AI_Router [label="42"];
  MemNet -> Tool_Search [label="29"];
  LiteLLM -> Auto_AI_Router [label="65"];
  LiteLLM -> Tool_Search [label="59"];
  Auto_AI_Router -> Tool_Search [label="59"];
  Svyazi -> mclaude [label="94"];
  Svyazi -> AI_Factory [label="93"];
  Svyazi -> Legal_RAG [label="77"];
  Svyazi -> Hybrid_RAG [label="47"];
  Svyazi -> Graph_RAG [label="76"];
  Svyazi -> NGT_Memory [label="111"];
  Svyazi -> AutoResearch [label="57"];
  Svyazi -> Yjs [label="39"];
  Svyazi -> Automerge [label="32"];
  CardIndex -> mclaude [label="83"];
  CardIndex -> AI_Factory [label="86"];
  CardIndex -> LiteParse [label="86"];
  CardIndex -> Legal_RAG [label="57"];
  CardIndex -> Hybrid_RAG [label="51"];
  CardIndex -> Graph_RAG [label="50"];
  CardIndex -> NGT_Memory [label="82"];
  CardIndex -> MemNet [label="46"];
  CardIndex -> LiteLLM [label="57"];
  CardIndex -> Auto_AI_Router [label="70"];
  CardIndex -> AutoResearch [label="50"];
  CardIndex -> Yjs [label="39"];
  CardIndex -> Automerge [label="32"];
  AgentFS -> mclaude [label="85"];
  AgentFS -> AI_Factory [label="88"];
  AgentFS -> LiteParse [label="92"];
  AgentFS -> Legal_RAG [label="71"];
  AgentFS -> Hybrid_RAG [label="49"];
  AgentFS -> Graph_RAG [label="68"];
  AgentFS -> NGT_Memory [label="98"];
  AgentFS -> MemNet [label="48"];
  AgentFS -> LiteLLM [label="59"];
  AgentFS -> Auto_AI_Router [label="90"];
  AgentFS -> AutoResearch [label="52"];
  AgentFS -> Yjs [label="35"];
  AgentFS -> Automerge [label="30"];
  knowledge_space -> mclaude [label="77"];
  knowledge_space -> AI_Factory [label="72"];
  knowledge_space -> LiteParse [label="84"];
  knowledge_space -> Legal_RAG [label="55"];
  knowledge_space -> Hybrid_RAG [label="41"];
  knowledge_space -> Graph_RAG [label="48"];
  knowledge_space -> NGT_Memory [label="82"];
  knowledge_space -> MemNet [label="44"];
  knowledge_space -> LiteLLM [label="47"];
  knowledge_space -> Auto_AI_Router [label="66"];
  knowledge_space -> Tool_Search [label="49"];
  knowledge_space -> AutoResearch [label="42"];
  knowledge_space -> Wikontic [label="37"];
  knowledge_space -> Yjs [label="35"];
  knowledge_space -> Automerge [label="30"];
  mclaude -> AI_Factory [label="84"];
  mclaude -> Rufler [label="81"];
  mclaude -> LiteParse [label="84"];
  mclaude -> Legal_RAG [label="55"];
  mclaude -> Hybrid_RAG [label="44"];
  mclaude -> Graph_RAG [label="47"];
  mclaude -> Yodoca [label="87"];
  mclaude -> NGT_Memory [label="77"];
  mclaude -> MemNet [label="39"];
  mclaude -> SENTINEL [label="71"];
  mclaude -> LiteLLM [label="50"];
  mclaude -> Auto_AI_Router [label="65"];
  mclaude -> Tool_Search [label="50"];
  mclaude -> AutoResearch [label="46"];
  mclaude -> Wikontic [label="25"];
  mclaude -> Firecrawl [label="16"];
  mclaude -> Yjs [label="31"];
  mclaude -> Automerge [label="28"];
  AI_Factory -> Rufler [label="77"];
  AI_Factory -> LiteParse [label="78"];
  AI_Factory -> Legal_RAG [label="49"];
  AI_Factory -> Hybrid_RAG [label="46"];
  AI_Factory -> Graph_RAG [label="41"];
  AI_Factory -> Yodoca [label="88"];
  AI_Factory -> NGT_Memory [label="74"];
  AI_Factory -> MemNet [label="38"];
  AI_Factory -> SENTINEL [label="71"];
  AI_Factory -> LiteLLM [label="56"];
  AI_Factory -> Auto_AI_Router [label="63"];
  AI_Factory -> Tool_Search [label="56"];
  AI_Factory -> AutoResearch [label="52"];
  AI_Factory -> Wikontic [label="24"];
  AI_Factory -> Firecrawl [label="20"];
  AI_Factory -> Yjs [label="33"];
  AI_Factory -> Automerge [label="30"];
  Rufler -> LiteParse [label="85"];
  Rufler -> Legal_RAG [label="66"];
  Rufler -> Hybrid_RAG [label="41"];
  Rufler -> Graph_RAG [label="64"];
  Rufler -> NGT_Memory [label="79"];
  Rufler -> MemNet [label="43"];
  Rufler -> LiteLLM [label="48"];
  Rufler -> Auto_AI_Router [label="80"];
  Rufler -> Tool_Search [label="52"];
  Rufler -> AutoResearch [label="47"];
  Rufler -> Wikontic [label="29"];
  Rufler -> Yjs [label="32"];
  Rufler -> Automerge [label="30"];
  LiteParse -> Legal_RAG [label="70"];
  LiteParse -> Hybrid_RAG [label="50"];
  LiteParse -> Graph_RAG [label="61"];
  LiteParse -> Yodoca [label="85"];
  LiteParse -> NGT_Memory [label="69"];
  LiteParse -> SENTINEL [label="83"];
  LiteParse -> AutoResearch [label="49"];
  LiteParse -> Wikontic [label="30"];
  LiteParse -> Firecrawl [label="21"];
  LiteParse -> Yjs [label="35"];
  LiteParse -> Automerge [label="30"];
  Legal_RAG -> Hybrid_RAG [label="46"];
  Legal_RAG -> Graph_RAG [label="71"];
  Legal_RAG -> Yodoca [label="66"];
  Legal_RAG -> NGT_Memory [label="62"];
  Legal_RAG -> MemNet [label="36"];
  Legal_RAG -> SENTINEL [label="75"];
  Legal_RAG -> LiteLLM [label="46"];
  Legal_RAG -> Auto_AI_Router [label="75"];
  Legal_RAG -> Tool_Search [label="44"];
  Legal_RAG -> AutoResearch [label="27"];
  Legal_RAG -> Wikontic [label="19"];
  Legal_RAG -> Firecrawl [label="15"];
  Legal_RAG -> Yjs [label="25"];
  Legal_RAG -> Automerge [label="22"];
  Hybrid_RAG -> Graph_RAG [label="39"];
  Hybrid_RAG -> Yodoca [label="48"];
  Hybrid_RAG -> NGT_Memory [label="44"];
  Hybrid_RAG -> MemNet [label="26"];
  Hybrid_RAG -> SENTINEL [label="44"];
  Hybrid_RAG -> LiteLLM [label="45"];
  Hybrid_RAG -> Auto_AI_Router [label="46"];
  Hybrid_RAG -> Tool_Search [label="41"];
  Hybrid_RAG -> AutoResearch [label="31"];
  Hybrid_RAG -> Wikontic [label="17"];
  Hybrid_RAG -> Firecrawl [label="16"];
  Hybrid_RAG -> Yjs [label="29"];
  Hybrid_RAG -> Automerge [label="28"];
  Graph_RAG -> Yodoca [label="63"];
  Graph_RAG -> NGT_Memory [label="61"];
  Graph_RAG -> MemNet [label="35"];
  Graph_RAG -> SENTINEL [label="77"];
  Graph_RAG -> LiteLLM [label="40"];
  Graph_RAG -> Auto_AI_Router [label="75"];
  Graph_RAG -> Tool_Search [label="38"];
  Graph_RAG -> AutoResearch [label="27"];
  Graph_RAG -> Wikontic [label="21"];
  Graph_RAG -> Firecrawl [label="14"];
  Graph_RAG -> Yjs [label="25"];
  Graph_RAG -> Automerge [label="22"];
  Yodoca -> NGT_Memory [label="102"];
  Yodoca -> MemNet [label="61"];
  Yodoca -> LiteLLM [label="54"];
  Yodoca -> Auto_AI_Router [label="83"];
  Yodoca -> AutoResearch [label="52"];
  Yodoca -> Yjs [label="37"];
  Yodoca -> Automerge [label="32"];
  NGT_Memory -> MemNet [label="38"];
  NGT_Memory -> SENTINEL [label="79"];
  NGT_Memory -> LiteLLM [label="50"];
  NGT_Memory -> Auto_AI_Router [label="81"];
  NGT_Memory -> Tool_Search [label="46"];
  NGT_Memory -> AutoResearch [label="44"];
  NGT_Memory -> Wikontic [label="35"];
  NGT_Memory -> Firecrawl [label="17"];
  NGT_Memory -> Yjs [label="35"];
  NGT_Memory -> Automerge [label="32"];
  MemNet -> SENTINEL [label="43"];
  MemNet -> AutoResearch [label="28"];
  MemNet -> Wikontic [label="40"];
  MemNet -> Firecrawl [label="21"];
  MemNet -> Yjs [label="23"];
  MemNet -> Automerge [label="18"];
  SENTINEL -> LiteLLM [label="62"];
  SENTINEL -> Auto_AI_Router [label="99"];
  SENTINEL -> AutoResearch [label="41"];
  SENTINEL -> Wikontic [label="27"];
  SENTINEL -> Yjs [label="29"];
  SENTINEL -> Automerge [label="26"];
  LiteLLM -> AutoResearch [label="40"];
  LiteLLM -> Wikontic [label="16"];
  LiteLLM -> Firecrawl [label="16"];
  LiteLLM -> Yjs [label="28"];
  LiteLLM -> Automerge [label="28"];
  Auto_AI_Router -> AutoResearch [label="43"];
  Auto_AI_Router -> Wikontic [label="21"];
  Auto_AI_Router -> Firecrawl [label="16"];
  Auto_AI_Router -> Yjs [label="31"];
  Auto_AI_Router -> Automerge [label="28"];
  Tool_Search -> AutoResearch [label="36"];
  Tool_Search -> Wikontic [label="18"];
  Tool_Search -> Firecrawl [label="16"];
  Tool_Search -> Yjs [label="24"];
  Tool_Search -> Automerge [label="24"];
  AutoResearch -> Wikontic [label="20"];
  AutoResearch -> Firecrawl [label="16"];
  AutoResearch -> Yjs [label="33"];
  AutoResearch -> Automerge [label="30"];
  Wikontic -> Firecrawl [label="22"];
  Wikontic -> Yjs [label="17"];
  Wikontic -> Automerge [label="14"];
  Firecrawl -> Yjs [label="16"];
  Firecrawl -> Automerge [label="16"];
  Yjs -> Automerge [label="32"];
}
```

<!-- backlinks-auto -->
## Упоминается в

- [Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md)
- [docs](README.md)
- [Все таблицы репозитория](TABLES.md)
- [Карта репозитория Lorenzo](SITEMAP.md)

<!-- related-auto -->
## Связанные документы

- [Сеть проектов и авторов](NETWORK.md) _29%_
- [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md) _25%_
- [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) _25%_
- [Карта плотности тем](DENSITY.md) _25%_
- [Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md) _21%_
- [07 Mvp Planning](01-svyazi/07-mvp-planning.md) _21%_
- [Executive summary](04-ai-collaborations/01-executive-summary.md) _21%_
- [Контактная стратегия и узкие вопросы для авторов](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) _21%_
