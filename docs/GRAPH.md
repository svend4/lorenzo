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
  Svyazi -- 154 --> Yodoca
  Svyazi -- 153 --> AgentFS
  AgentFS -- 133 --> Yodoca
  Svyazi -- 125 --> CardIndex
  Svyazi -- 119 --> Rufler
  Svyazi -- 118 --> SENTINEL
  AgentFS -- 118 --> SENTINEL
  Svyazi -- 116 --> knowledge_space
  CardIndex -- 115 --> AgentFS
  AgentFS -- 114 --> Rufler
  Svyazi -- 114 --> NGT_Memory
  AgentFS -- 112 --> knowledge_space
  Svyazi -- 109 --> LiteParse
  Rufler -- 108 --> Yodoca
  CardIndex -- 105 --> Yodoca
  Rufler -- 105 --> SENTINEL
  Svyazi -- 105 --> Auto_AI_Router
  Svyazi -- 103 --> mclaude
  Yodoca -- 103 --> NGT_Memory
  Yodoca -- 102 --> SENTINEL
  SENTINEL -- 102 --> Auto_AI_Router
  knowledge_space -- 100 --> Yodoca
  AgentFS -- 100 --> LiteParse
  AgentFS -- 99 --> NGT_Memory
  AgentFS -- 97 --> Auto_AI_Router
  CardIndex -- 95 --> knowledge_space
  Svyazi -- 94 --> AI_Factory
  AgentFS -- 94 --> mclaude
  mclaude -- 93 --> Yodoca
  CardIndex -- 91 --> Rufler
  knowledge_space -- 91 --> LiteParse
  Rufler -- 91 --> LiteParse
  LiteParse -- 90 --> Yodoca
  knowledge_space -- 90 --> NGT_Memory
  mclaude -- 90 --> Rufler
  knowledge_space -- 89 --> Rufler
  mclaude -- 89 --> LiteParse
  AgentFS -- 88 --> AI_Factory
  AI_Factory -- 88 --> Yodoca
  LiteParse -- 88 --> SENTINEL
  CardIndex -- 87 --> SENTINEL
  Yodoca -- 87 --> Auto_AI_Router
  knowledge_space -- 86 --> SENTINEL
  CardIndex -- 86 --> AI_Factory
  CardIndex -- 86 --> LiteParse
  knowledge_space -- 85 --> mclaude
  Rufler -- 85 --> Auto_AI_Router
  CardIndex -- 84 --> mclaude
  mclaude -- 84 --> AI_Factory
  NGT_Memory -- 84 --> Auto_AI_Router
  CardIndex -- 83 --> NGT_Memory
  mclaude -- 83 --> NGT_Memory
  Rufler -- 83 --> NGT_Memory
  LiteParse -- 82 --> Auto_AI_Router
  Svyazi -- 81 --> Legal_RAG
  Svyazi -- 81 --> Graph_RAG
  NGT_Memory -- 81 --> SENTINEL
  Graph_RAG -- 80 --> SENTINEL
  mclaude -- 79 --> SENTINEL
  AI_Factory -- 78 --> Rufler
  AI_Factory -- 78 --> LiteParse
  Legal_RAG -- 78 --> SENTINEL
  Legal_RAG -- 78 --> Auto_AI_Router
  Graph_RAG -- 78 --> Auto_AI_Router
  knowledge_space -- 77 --> Auto_AI_Router
  Svyazi -- 76 --> MemNet
  AgentFS -- 76 --> Legal_RAG
  LiteParse -- 75 --> Legal_RAG
  AgentFS -- 74 --> Graph_RAG
  AI_Factory -- 74 --> NGT_Memory
  LiteParse -- 74 --> NGT_Memory
  mclaude -- 73 --> Auto_AI_Router
  Legal_RAG -- 73 --> Graph_RAG
  CardIndex -- 72 --> Auto_AI_Router
  knowledge_space -- 72 --> AI_Factory
  AI_Factory -- 71 --> SENTINEL
  Rufler -- 70 --> Legal_RAG
  Rufler -- 69 --> Graph_RAG
  Legal_RAG -- 67 --> Yodoca
  Yodoca -- 67 --> MemNet
  AgentFS -- 66 --> Tool_Search
  SENTINEL -- 66 --> Tool_Search
  LiteLLM -- 66 --> Auto_AI_Router
  LiteParse -- 66 --> Graph_RAG
  Graph_RAG -- 66 --> Yodoca
  Legal_RAG -- 65 --> NGT_Memory
  knowledge_space -- 64 --> Legal_RAG
  Svyazi -- 63 --> Tool_Search
  mclaude -- 63 --> Legal_RAG
  AI_Factory -- 63 --> Auto_AI_Router
  Graph_RAG -- 63 --> NGT_Memory
  SENTINEL -- 63 --> LiteLLM
  CardIndex -- 62 --> Tool_Search
  Svyazi -- 61 --> LiteLLM
  AgentFS -- 61 --> LiteLLM
  LiteParse -- 59 --> MemNet
  LiteLLM -- 59 --> Tool_Search
  Auto_AI_Router -- 59 --> Tool_Search
  CardIndex -- 59 --> LiteLLM
  AgentFS -- 59 --> MemNet
  Yodoca -- 58 --> Tool_Search
  LiteParse -- 58 --> LiteLLM
  knowledge_space -- 58 --> Graph_RAG
  LiteParse -- 57 --> Tool_Search
  Svyazi -- 57 --> AutoResearch
  CardIndex -- 57 --> Legal_RAG
  AI_Factory -- 57 --> LiteLLM
  Yodoca -- 56 --> Wikontic
  AI_Factory -- 56 --> Tool_Search
  mclaude -- 55 --> Graph_RAG
  Yodoca -- 55 --> LiteLLM
  Svyazi -- 54 --> Wikontic
  knowledge_space -- 54 --> MemNet
  MemNet -- 53 --> Auto_AI_Router
  Rufler -- 53 --> MemNet
  MemNet -- 53 --> SENTINEL
  CardIndex -- 52 --> Hybrid_RAG
  AgentFS -- 52 --> AutoResearch
  AI_Factory -- 52 --> AutoResearch
  Rufler -- 52 --> Tool_Search
  Yodoca -- 52 --> AutoResearch
  CardIndex -- 51 --> Graph_RAG
  mclaude -- 51 --> LiteLLM
  NGT_Memory -- 51 --> LiteLLM
  CardIndex -- 50 --> AutoResearch
  AgentFS -- 50 --> Hybrid_RAG
  knowledge_space -- 50 --> Tool_Search
  mclaude -- 50 --> Tool_Search
  LiteParse -- 50 --> Hybrid_RAG
  Svyazi -- 49 --> Hybrid_RAG
  knowledge_space -- 49 --> LiteLLM
  AI_Factory -- 49 --> Legal_RAG
  Rufler -- 49 --> LiteLLM
  LiteParse -- 49 --> AutoResearch
  CardIndex -- 48 --> MemNet
  mclaude -- 48 --> MemNet
  Rufler -- 48 --> AutoResearch
  Hybrid_RAG -- 48 --> Yodoca
  Legal_RAG -- 47 --> LiteLLM
  mclaude -- 46 --> AutoResearch
  AI_Factory -- 46 --> Hybrid_RAG
  Legal_RAG -- 46 --> Hybrid_RAG
  Hybrid_RAG -- 46 --> LiteLLM
  Hybrid_RAG -- 46 --> Auto_AI_Router
  NGT_Memory -- 46 --> MemNet
  NGT_Memory -- 46 --> Tool_Search
  Legal_RAG -- 45 --> MemNet
  mclaude -- 44 --> Hybrid_RAG
  Legal_RAG -- 44 --> Tool_Search
  Hybrid_RAG -- 44 --> NGT_Memory
  Hybrid_RAG -- 44 --> SENTINEL
  NGT_Memory -- 44 --> AutoResearch
  Graph_RAG -- 43 --> MemNet
  Auto_AI_Router -- 43 --> AutoResearch
  knowledge_space -- 42 --> Hybrid_RAG
  knowledge_space -- 42 --> AutoResearch
  Rufler -- 42 --> Hybrid_RAG
  AI_Factory -- 41 --> Graph_RAG
  Hybrid_RAG -- 41 --> Tool_Search
  Graph_RAG -- 41 --> LiteLLM
  SENTINEL -- 41 --> AutoResearch
  LiteLLM -- 41 --> AutoResearch
  CardIndex -- 40 --> Wikontic
  MemNet -- 40 --> Wikontic
  Svyazi -- 39 --> Yjs
  CardIndex -- 39 --> Yjs
  AI_Factory -- 39 --> MemNet
  Hybrid_RAG -- 39 --> Graph_RAG
  knowledge_space -- 38 --> Wikontic
  Graph_RAG -- 38 --> Tool_Search
  Yodoca -- 37 --> Yjs
  AgentFS -- 36 --> Wikontic
  Tool_Search -- 36 --> AutoResearch
  AgentFS -- 35 --> Yjs
  knowledge_space -- 35 --> Yjs
  LiteParse -- 35 --> Yjs
  NGT_Memory -- 35 --> Wikontic
  NGT_Memory -- 35 --> Yjs
  AI_Factory -- 33 --> Yjs
  Rufler -- 33 --> Yjs
  AutoResearch -- 33 --> Yjs
  Svyazi -- 32 --> Automerge
  CardIndex -- 32 --> Automerge
  Yodoca -- 32 --> Automerge
  NGT_Memory -- 32 --> Automerge
  Yjs -- 32 --> Automerge
  MemNet -- 31 --> LiteLLM
  mclaude -- 31 --> Yjs
  Hybrid_RAG -- 31 --> AutoResearch
  Auto_AI_Router -- 31 --> Yjs
  MemNet -- 30 --> Tool_Search
  AgentFS -- 30 --> Automerge
  knowledge_space -- 30 --> Automerge
  AI_Factory -- 30 --> Automerge
  Rufler -- 30 --> Wikontic
  Rufler -- 30 --> Automerge
  LiteParse -- 30 --> Wikontic
  LiteParse -- 30 --> Automerge
  AutoResearch -- 30 --> Automerge
  Hybrid_RAG -- 29 --> Yjs
  MemNet -- 29 --> AutoResearch
  SENTINEL -- 29 --> Yjs
  LiteLLM -- 29 --> Yjs
  Svyazi -- 28 --> Firecrawl
  CardIndex -- 28 --> Firecrawl
  Yodoca -- 28 --> Firecrawl
  mclaude -- 28 --> Automerge
  Hybrid_RAG -- 28 --> Automerge
  LiteLLM -- 28 --> Automerge
  Auto_AI_Router -- 28 --> Automerge
  Legal_RAG -- 27 --> AutoResearch
  Graph_RAG -- 27 --> AutoResearch
  SENTINEL -- 27 --> Wikontic
  AgentFS -- 26 --> Firecrawl
  Rufler -- 26 --> Firecrawl
  SENTINEL -- 26 --> Firecrawl
  Hybrid_RAG -- 26 --> MemNet
  SENTINEL -- 26 --> Automerge
  mclaude -- 25 --> Wikontic
  Legal_RAG -- 25 --> Yjs
  Graph_RAG -- 25 --> Yjs
  knowledge_space -- 24 --> Firecrawl
  AI_Factory -- 24 --> Wikontic
  Tool_Search -- 24 --> Yjs
  Tool_Search -- 24 --> Automerge
  MemNet -- 23 --> Yjs
  Legal_RAG -- 22 --> Automerge
  Graph_RAG -- 22 --> Automerge
  Auto_AI_Router -- 22 --> Wikontic
  Wikontic -- 22 --> Firecrawl
  Graph_RAG -- 21 --> Wikontic
  AI_Factory -- 20 --> Firecrawl
  LiteParse -- 20 --> Firecrawl
  MemNet -- 20 --> Firecrawl
  AutoResearch -- 20 --> Wikontic
  Legal_RAG -- 19 --> Wikontic
  MemNet -- 18 --> Automerge
  Tool_Search -- 18 --> Wikontic
  Hybrid_RAG -- 17 --> Wikontic
  LiteLLM -- 17 --> Wikontic
  Wikontic -- 17 --> Yjs
  mclaude -- 16 --> Firecrawl
  Hybrid_RAG -- 16 --> Firecrawl
  NGT_Memory -- 16 --> Firecrawl
  LiteLLM -- 16 --> Firecrawl
  Auto_AI_Router -- 16 --> Firecrawl
  Tool_Search -- 16 --> Firecrawl
  AutoResearch -- 16 --> Firecrawl
  Firecrawl -- 16 --> Yjs
  Firecrawl -- 16 --> Automerge
  Legal_RAG -- 14 --> Firecrawl
  Graph_RAG -- 14 --> Firecrawl
  Wikontic -- 14 --> Automerge
```

## Топ совместных упоминаний

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 154 |
| **Svyazi** | **AgentFS** | 153 |
| **AgentFS** | **Yodoca** | 133 |
| **Svyazi** | **CardIndex** | 125 |
| **Svyazi** | **Rufler** | 119 |
| **Svyazi** | **SENTINEL** | 118 |
| **AgentFS** | **SENTINEL** | 118 |
| **Svyazi** | **knowledge-space** | 116 |
| **CardIndex** | **AgentFS** | 115 |
| **AgentFS** | **Rufler** | 114 |
| **Svyazi** | **NGT Memory** | 114 |
| **AgentFS** | **knowledge-space** | 112 |
| **Svyazi** | **LiteParse** | 109 |
| **Rufler** | **Yodoca** | 108 |
| **CardIndex** | **Yodoca** | 105 |
| **Rufler** | **SENTINEL** | 105 |
| **Svyazi** | **Auto AI Router** | 105 |
| **Svyazi** | **mclaude** | 103 |
| **Yodoca** | **NGT Memory** | 103 |
| **Yodoca** | **SENTINEL** | 102 |
| **SENTINEL** | **Auto AI Router** | 102 |
| **knowledge-space** | **Yodoca** | 100 |
| **AgentFS** | **LiteParse** | 100 |
| **AgentFS** | **NGT Memory** | 99 |
| **AgentFS** | **Auto AI Router** | 97 |

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
  Svyazi -> Yodoca [label="154"];
  Svyazi -> Wikontic [label="54"];
  Yodoca -> Wikontic [label="56"];
  Svyazi -> CardIndex [label="125"];
  Svyazi -> AgentFS [label="153"];
  Svyazi -> SENTINEL [label="118"];
  Svyazi -> Tool_Search [label="63"];
  CardIndex -> AgentFS [label="115"];
  CardIndex -> Yodoca [label="105"];
  CardIndex -> SENTINEL [label="87"];
  CardIndex -> Tool_Search [label="62"];
  AgentFS -> Yodoca [label="133"];
  AgentFS -> SENTINEL [label="118"];
  AgentFS -> Tool_Search [label="66"];
  Yodoca -> SENTINEL [label="102"];
  Yodoca -> Tool_Search [label="58"];
  SENTINEL -> Tool_Search [label="66"];
  Svyazi -> knowledge_space [label="116"];
  Svyazi -> Rufler [label="119"];
  Svyazi -> Firecrawl [label="28"];
  CardIndex -> knowledge_space [label="95"];
  CardIndex -> Rufler [label="91"];
  CardIndex -> Firecrawl [label="28"];
  AgentFS -> knowledge_space [label="112"];
  AgentFS -> Rufler [label="114"];
  AgentFS -> Firecrawl [label="26"];
  knowledge_space -> Rufler [label="89"];
  knowledge_space -> Yodoca [label="100"];
  knowledge_space -> SENTINEL [label="86"];
  knowledge_space -> Firecrawl [label="24"];
  Rufler -> Yodoca [label="108"];
  Rufler -> SENTINEL [label="105"];
  Rufler -> Firecrawl [label="26"];
  Yodoca -> Firecrawl [label="28"];
  SENTINEL -> Firecrawl [label="26"];
  knowledge_space -> LiteParse [label="91"];
  LiteParse -> Yodoca [label="90"];
  Svyazi -> LiteParse [label="109"];
  Svyazi -> MemNet [label="76"];
  Svyazi -> LiteLLM [label="61"];
  Svyazi -> Auto_AI_Router [label="105"];
  LiteParse -> MemNet [label="59"];
  LiteParse -> LiteLLM [label="58"];
  LiteParse -> Auto_AI_Router [label="82"];
  LiteParse -> Tool_Search [label="57"];
  MemNet -> LiteLLM [label="31"];
  MemNet -> Auto_AI_Router [label="53"];
  MemNet -> Tool_Search [label="30"];
  LiteLLM -> Auto_AI_Router [label="66"];
  LiteLLM -> Tool_Search [label="59"];
  Auto_AI_Router -> Tool_Search [label="59"];
  Svyazi -> mclaude [label="103"];
  Svyazi -> AI_Factory [label="94"];
  Svyazi -> Legal_RAG [label="81"];
  Svyazi -> Hybrid_RAG [label="49"];
  Svyazi -> Graph_RAG [label="81"];
  Svyazi -> NGT_Memory [label="114"];
  Svyazi -> AutoResearch [label="57"];
  Svyazi -> Yjs [label="39"];
  Svyazi -> Automerge [label="32"];
  CardIndex -> mclaude [label="84"];
  CardIndex -> AI_Factory [label="86"];
  CardIndex -> LiteParse [label="86"];
  CardIndex -> Legal_RAG [label="57"];
  CardIndex -> Hybrid_RAG [label="52"];
  CardIndex -> Graph_RAG [label="51"];
  CardIndex -> NGT_Memory [label="83"];
  CardIndex -> MemNet [label="48"];
  CardIndex -> LiteLLM [label="59"];
  CardIndex -> Auto_AI_Router [label="72"];
  CardIndex -> AutoResearch [label="50"];
  CardIndex -> Wikontic [label="40"];
  CardIndex -> Yjs [label="39"];
  CardIndex -> Automerge [label="32"];
  AgentFS -> mclaude [label="94"];
  AgentFS -> AI_Factory [label="88"];
  AgentFS -> LiteParse [label="100"];
  AgentFS -> Legal_RAG [label="76"];
  AgentFS -> Hybrid_RAG [label="50"];
  AgentFS -> Graph_RAG [label="74"];
  AgentFS -> NGT_Memory [label="99"];
  AgentFS -> MemNet [label="59"];
  AgentFS -> LiteLLM [label="61"];
  AgentFS -> Auto_AI_Router [label="97"];
  AgentFS -> AutoResearch [label="52"];
  AgentFS -> Wikontic [label="36"];
  AgentFS -> Yjs [label="35"];
  AgentFS -> Automerge [label="30"];
  knowledge_space -> mclaude [label="85"];
  knowledge_space -> AI_Factory [label="72"];
  knowledge_space -> Legal_RAG [label="64"];
  knowledge_space -> Hybrid_RAG [label="42"];
  knowledge_space -> Graph_RAG [label="58"];
  knowledge_space -> NGT_Memory [label="90"];
  knowledge_space -> MemNet [label="54"];
  knowledge_space -> LiteLLM [label="49"];
  knowledge_space -> Auto_AI_Router [label="77"];
  knowledge_space -> Tool_Search [label="50"];
  knowledge_space -> AutoResearch [label="42"];
  knowledge_space -> Wikontic [label="38"];
  knowledge_space -> Yjs [label="35"];
  knowledge_space -> Automerge [label="30"];
  mclaude -> AI_Factory [label="84"];
  mclaude -> Rufler [label="90"];
  mclaude -> LiteParse [label="89"];
  mclaude -> Legal_RAG [label="63"];
  mclaude -> Hybrid_RAG [label="44"];
  mclaude -> Graph_RAG [label="55"];
  mclaude -> Yodoca [label="93"];
  mclaude -> NGT_Memory [label="83"];
  mclaude -> MemNet [label="48"];
  mclaude -> SENTINEL [label="79"];
  mclaude -> LiteLLM [label="51"];
  mclaude -> Auto_AI_Router [label="73"];
  mclaude -> Tool_Search [label="50"];
  mclaude -> AutoResearch [label="46"];
  mclaude -> Wikontic [label="25"];
  mclaude -> Firecrawl [label="16"];
  mclaude -> Yjs [label="31"];
  mclaude -> Automerge [label="28"];
  AI_Factory -> Rufler [label="78"];
  AI_Factory -> LiteParse [label="78"];
  AI_Factory -> Legal_RAG [label="49"];
  AI_Factory -> Hybrid_RAG [label="46"];
  AI_Factory -> Graph_RAG [label="41"];
  AI_Factory -> Yodoca [label="88"];
  AI_Factory -> NGT_Memory [label="74"];
  AI_Factory -> MemNet [label="39"];
  AI_Factory -> SENTINEL [label="71"];
  AI_Factory -> LiteLLM [label="57"];
  AI_Factory -> Auto_AI_Router [label="63"];
  AI_Factory -> Tool_Search [label="56"];
  AI_Factory -> AutoResearch [label="52"];
  AI_Factory -> Wikontic [label="24"];
  AI_Factory -> Firecrawl [label="20"];
  AI_Factory -> Yjs [label="33"];
  AI_Factory -> Automerge [label="30"];
  Rufler -> LiteParse [label="91"];
  Rufler -> Legal_RAG [label="70"];
  Rufler -> Hybrid_RAG [label="42"];
  Rufler -> Graph_RAG [label="69"];
  Rufler -> NGT_Memory [label="83"];
  Rufler -> MemNet [label="53"];
  Rufler -> LiteLLM [label="49"];
  Rufler -> Auto_AI_Router [label="85"];
  Rufler -> Tool_Search [label="52"];
  Rufler -> AutoResearch [label="48"];
  Rufler -> Wikontic [label="30"];
  Rufler -> Yjs [label="33"];
  Rufler -> Automerge [label="30"];
  LiteParse -> Legal_RAG [label="75"];
  LiteParse -> Hybrid_RAG [label="50"];
  LiteParse -> Graph_RAG [label="66"];
  LiteParse -> NGT_Memory [label="74"];
  LiteParse -> SENTINEL [label="88"];
  LiteParse -> AutoResearch [label="49"];
  LiteParse -> Wikontic [label="30"];
  LiteParse -> Firecrawl [label="20"];
  LiteParse -> Yjs [label="35"];
  LiteParse -> Automerge [label="30"];
  Legal_RAG -> Hybrid_RAG [label="46"];
  Legal_RAG -> Graph_RAG [label="73"];
  Legal_RAG -> Yodoca [label="67"];
  Legal_RAG -> NGT_Memory [label="65"];
  Legal_RAG -> MemNet [label="45"];
  Legal_RAG -> SENTINEL [label="78"];
  Legal_RAG -> LiteLLM [label="47"];
  Legal_RAG -> Auto_AI_Router [label="78"];
  Legal_RAG -> Tool_Search [label="44"];
  Legal_RAG -> AutoResearch [label="27"];
  Legal_RAG -> Wikontic [label="19"];
  Legal_RAG -> Firecrawl [label="14"];
  Legal_RAG -> Yjs [label="25"];
  Legal_RAG -> Automerge [label="22"];
  Hybrid_RAG -> Graph_RAG [label="39"];
  Hybrid_RAG -> Yodoca [label="48"];
  Hybrid_RAG -> NGT_Memory [label="44"];
  Hybrid_RAG -> MemNet [label="26"];
  Hybrid_RAG -> SENTINEL [label="44"];
  Hybrid_RAG -> LiteLLM [label="46"];
  Hybrid_RAG -> Auto_AI_Router [label="46"];
  Hybrid_RAG -> Tool_Search [label="41"];
  Hybrid_RAG -> AutoResearch [label="31"];
  Hybrid_RAG -> Wikontic [label="17"];
  Hybrid_RAG -> Firecrawl [label="16"];
  Hybrid_RAG -> Yjs [label="29"];
  Hybrid_RAG -> Automerge [label="28"];
  Graph_RAG -> Yodoca [label="66"];
  Graph_RAG -> NGT_Memory [label="63"];
  Graph_RAG -> MemNet [label="43"];
  Graph_RAG -> SENTINEL [label="80"];
  Graph_RAG -> LiteLLM [label="41"];
  Graph_RAG -> Auto_AI_Router [label="78"];
  Graph_RAG -> Tool_Search [label="38"];
  Graph_RAG -> AutoResearch [label="27"];
  Graph_RAG -> Wikontic [label="21"];
  Graph_RAG -> Firecrawl [label="14"];
  Graph_RAG -> Yjs [label="25"];
  Graph_RAG -> Automerge [label="22"];
  Yodoca -> NGT_Memory [label="103"];
  Yodoca -> MemNet [label="67"];
  Yodoca -> LiteLLM [label="55"];
  Yodoca -> Auto_AI_Router [label="87"];
  Yodoca -> AutoResearch [label="52"];
  Yodoca -> Yjs [label="37"];
  Yodoca -> Automerge [label="32"];
  NGT_Memory -> MemNet [label="46"];
  NGT_Memory -> SENTINEL [label="81"];
  NGT_Memory -> LiteLLM [label="51"];
  NGT_Memory -> Auto_AI_Router [label="84"];
  NGT_Memory -> Tool_Search [label="46"];
  NGT_Memory -> AutoResearch [label="44"];
  NGT_Memory -> Wikontic [label="35"];
  NGT_Memory -> Firecrawl [label="16"];
  NGT_Memory -> Yjs [label="35"];
  NGT_Memory -> Automerge [label="32"];
  MemNet -> SENTINEL [label="53"];
  MemNet -> AutoResearch [label="29"];
  MemNet -> Wikontic [label="40"];
  MemNet -> Firecrawl [label="20"];
  MemNet -> Yjs [label="23"];
  MemNet -> Automerge [label="18"];
  SENTINEL -> LiteLLM [label="63"];
  SENTINEL -> Auto_AI_Router [label="102"];
  SENTINEL -> AutoResearch [label="41"];
  SENTINEL -> Wikontic [label="27"];
  SENTINEL -> Yjs [label="29"];
  SENTINEL -> Automerge [label="26"];
  LiteLLM -> AutoResearch [label="41"];
  LiteLLM -> Wikontic [label="17"];
  LiteLLM -> Firecrawl [label="16"];
  LiteLLM -> Yjs [label="29"];
  LiteLLM -> Automerge [label="28"];
  Auto_AI_Router -> AutoResearch [label="43"];
  Auto_AI_Router -> Wikontic [label="22"];
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
