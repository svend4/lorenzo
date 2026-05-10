# Граф связей проектов

<!-- toc-auto -->
## Содержание

- Основной раздел


<!-- summary -->
> Граф связей проектов — документ базы знаний репозитория Lorenzo.

<!-- tags: docs, reference, lorenzo -->

> [!NOTE]
> Документ содержит структурированную информацию из базы знаний репозитория Lorenzo.

<!-- alert-added -->


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
  Svyazi -- 276 --> Yodoca
  Svyazi -- 246 --> CardIndex
  Svyazi -- 215 --> AgentFS
  AgentFS -- 194 --> Yodoca
  Svyazi -- 187 --> knowledge_space
  Svyazi -- 185 --> mclaude
  CardIndex -- 180 --> Yodoca
  Svyazi -- 177 --> Rufler
  Svyazi -- 176 --> NGT_Memory
  Svyazi -- 175 --> MemNet
  AgentFS -- 174 --> knowledge_space
  CardIndex -- 173 --> AgentFS
  Svyazi -- 165 --> LiteParse
  Yodoca -- 162 --> NGT_Memory
  Yodoca -- 160 --> MemNet
  knowledge_space -- 159 --> Yodoca
  mclaude -- 157 --> Yodoca
  mclaude -- 149 --> Rufler
  Rufler -- 149 --> Yodoca
  AgentFS -- 147 --> mclaude
  AgentFS -- 145 --> LiteParse
  knowledge_space -- 145 --> mclaude
  Svyazi -- 143 --> AI_Factory
  AgentFS -- 141 --> Rufler
  knowledge_space -- 141 --> Rufler
  CardIndex -- 140 --> knowledge_space
  Svyazi -- 137 --> SENTINEL
  CardIndex -- 134 --> NGT_Memory
  LiteParse -- 134 --> Yodoca
  mclaude -- 131 --> AI_Factory
  CardIndex -- 130 --> LiteParse
  AgentFS -- 129 --> SENTINEL
  mclaude -- 129 --> LiteParse
  knowledge_space -- 125 --> LiteParse
  AgentFS -- 125 --> NGT_Memory
  CardIndex -- 124 --> mclaude
  CardIndex -- 124 --> Rufler
  Rufler -- 122 --> LiteParse
  AI_Factory -- 122 --> Yodoca
  AgentFS -- 119 --> AI_Factory
  Yodoca -- 117 --> SENTINEL
  Svyazi -- 116 --> AutoResearch
  knowledge_space -- 116 --> NGT_Memory
  Svyazi -- 115 --> Auto_AI_Router
  AI_Factory -- 115 --> Rufler
  CardIndex -- 111 --> SENTINEL
  CardIndex -- 111 --> AI_Factory
  CardIndex -- 110 --> MemNet
  mclaude -- 110 --> NGT_Memory
  AI_Factory -- 107 --> LiteParse
  knowledge_space -- 106 --> MemNet
  AgentFS -- 105 --> MemNet
  Rufler -- 103 --> MemNet
  AI_Factory -- 103 --> NGT_Memory
  Rufler -- 101 --> SENTINEL
  LiteParse -- 99 --> SENTINEL
  Yodoca -- 98 --> AutoResearch
  knowledge_space -- 98 --> AI_Factory
  LiteParse -- 97 --> Legal_RAG
  SENTINEL -- 97 --> Auto_AI_Router
  LiteLLM -- 96 --> Auto_AI_Router
  LiteParse -- 96 --> NGT_Memory
  Svyazi -- 95 --> Tool_Search
  Svyazi -- 95 --> Legal_RAG
  CardIndex -- 95 --> Auto_AI_Router
  AI_Factory -- 95 --> SENTINEL
  mclaude -- 94 --> MemNet
  SENTINEL -- 93 --> Tool_Search
  Svyazi -- 92 --> Wikontic
  NGT_Memory -- 92 --> MemNet
  knowledge_space -- 91 --> SENTINEL
  Yodoca -- 91 --> Auto_AI_Router
  Svyazi -- 90 --> Graph_RAG
  LiteParse -- 89 --> Auto_AI_Router
  mclaude -- 89 --> SENTINEL
  Rufler -- 88 --> AutoResearch
  LiteParse -- 88 --> MemNet
  Rufler -- 88 --> NGT_Memory
  Svyazi -- 87 --> LiteLLM
  AgentFS -- 87 --> Auto_AI_Router
  NGT_Memory -- 87 --> SENTINEL
  NGT_Memory -- 87 --> Auto_AI_Router
  Svyazi -- 86 --> Yjs
  Svyazi -- 86 --> Hybrid_RAG
  LiteParse -- 86 --> Hybrid_RAG
  Yodoca -- 85 --> Wikontic
  AgentFS -- 85 --> Tool_Search
  SENTINEL -- 85 --> LiteLLM
  AgentFS -- 84 --> AutoResearch
  mclaude -- 84 --> AutoResearch
  Auto_AI_Router -- 84 --> Tool_Search
  LiteParse -- 84 --> Graph_RAG
  LiteParse -- 83 --> AutoResearch
  Legal_RAG -- 83 --> Graph_RAG
  LiteLLM -- 82 --> Tool_Search
  CardIndex -- 81 --> Tool_Search
  AgentFS -- 81 --> Hybrid_RAG
  CardIndex -- 80 --> AutoResearch
  LiteParse -- 80 --> Tool_Search
  AgentFS -- 80 --> Legal_RAG
  Yodoca -- 79 --> Tool_Search
  CardIndex -- 79 --> Hybrid_RAG
  AI_Factory -- 79 --> Auto_AI_Router
  Yjs -- 78 --> Automerge
  LiteParse -- 78 --> LiteLLM
  CardIndex -- 78 --> Legal_RAG
  Legal_RAG -- 78 --> SENTINEL
  Hybrid_RAG -- 78 --> Yodoca
  AgentFS -- 77 --> LiteLLM
  knowledge_space -- 77 --> Auto_AI_Router
  Legal_RAG -- 77 --> Yodoca
  Graph_RAG -- 77 --> SENTINEL
  knowledge_space -- 76 --> AutoResearch
  Legal_RAG -- 76 --> Hybrid_RAG
  CardIndex -- 75 --> LiteLLM
  mclaude -- 75 --> Auto_AI_Router
  AI_Factory -- 75 --> AutoResearch
  Rufler -- 75 --> Auto_AI_Router
  Legal_RAG -- 75 --> NGT_Memory
  Yodoca -- 75 --> LiteLLM
  CardIndex -- 74 --> Yjs
  AgentFS -- 74 --> Graph_RAG
  mclaude -- 74 --> Legal_RAG
  Legal_RAG -- 74 --> Auto_AI_Router
  Hybrid_RAG -- 74 --> Graph_RAG
  AI_Factory -- 73 --> Legal_RAG
  AI_Factory -- 73 --> Tool_Search
  Hybrid_RAG -- 73 --> SENTINEL
  knowledge_space -- 72 --> Legal_RAG
  Hybrid_RAG -- 72 --> NGT_Memory
  knowledge_space -- 71 --> Hybrid_RAG
  Svyazi -- 70 --> Automerge
  CardIndex -- 69 --> Wikontic
  NGT_Memory -- 69 --> Wikontic
  MemNet -- 69 --> Wikontic
  MemNet -- 69 --> AutoResearch
  mclaude -- 69 --> Hybrid_RAG
  AI_Factory -- 69 --> LiteLLM
  Rufler -- 69 --> Hybrid_RAG
  Graph_RAG -- 69 --> Yodoca
  NGT_Memory -- 69 --> LiteLLM
  MemNet -- 69 --> SENTINEL
  knowledge_space -- 68 --> Wikontic
  mclaude -- 68 --> Graph_RAG
  AI_Factory -- 68 --> Hybrid_RAG
  Rufler -- 68 --> Legal_RAG
  AI_Factory -- 67 --> MemNet
  Rufler -- 67 --> Tool_Search
  Hybrid_RAG -- 67 --> Auto_AI_Router
  NGT_Memory -- 67 --> AutoResearch
  CardIndex -- 66 --> Graph_RAG
  knowledge_space -- 66 --> Graph_RAG
  Legal_RAG -- 66 --> Tool_Search
  AgentFS -- 65 --> Yjs
  knowledge_space -- 65 --> Yjs
  Yodoca -- 65 --> Yjs
  mclaude -- 65 --> Tool_Search
  Graph_RAG -- 65 --> NGT_Memory
  Graph_RAG -- 65 --> Auto_AI_Router
  NGT_Memory -- 65 --> Tool_Search
  Auto_AI_Router -- 64 --> AutoResearch
  Legal_RAG -- 64 --> LiteLLM
  knowledge_space -- 63 --> LiteLLM
  knowledge_space -- 63 --> Tool_Search
  mclaude -- 63 --> LiteLLM
  Rufler -- 63 --> LiteLLM
  Hybrid_RAG -- 63 --> LiteLLM
  AgentFS -- 62 --> Wikontic
  AI_Factory -- 62 --> Graph_RAG
  Rufler -- 62 --> Graph_RAG
  AgentFS -- 61 --> Automerge
  knowledge_space -- 61 --> Automerge
  Rufler -- 61 --> Yjs
  Yodoca -- 61 --> Automerge
  LiteParse -- 60 --> Yjs
  Rufler -- 59 --> Automerge
  CardIndex -- 58 --> Automerge
  LiteLLM -- 58 --> AutoResearch
  NGT_Memory -- 58 --> Yjs
  mclaude -- 57 --> Yjs
  AutoResearch -- 57 --> Yjs
  Hybrid_RAG -- 57 --> Tool_Search
  LiteParse -- 56 --> Automerge
  MemNet -- 56 --> Auto_AI_Router
  mclaude -- 55 --> Automerge
  AutoResearch -- 55 --> Automerge
  Legal_RAG -- 55 --> MemNet
  SENTINEL -- 55 --> AutoResearch
  Rufler -- 54 --> Wikontic
  MemNet -- 54 --> Yjs
  Graph_RAG -- 53 --> LiteLLM
  Graph_RAG -- 53 --> Tool_Search
  LiteParse -- 52 --> Wikontic
  Hybrid_RAG -- 52 --> MemNet
  Graph_RAG -- 51 --> MemNet
  mclaude -- 50 --> Wikontic
  Tool_Search -- 50 --> AutoResearch
  NGT_Memory -- 50 --> Automerge
  Hybrid_RAG -- 49 --> AutoResearch
  MemNet -- 48 --> Automerge
  MemNet -- 48 --> LiteLLM
  Auto_AI_Router -- 48 --> Yjs
  AutoResearch -- 45 --> Wikontic
  MemNet -- 44 --> Tool_Search
  AI_Factory -- 44 --> Yjs
  Legal_RAG -- 44 --> AutoResearch
  AI_Factory -- 42 --> Automerge
  Hybrid_RAG -- 41 --> Yjs
  Hybrid_RAG -- 41 --> Automerge
  Graph_RAG -- 41 --> AutoResearch
  SENTINEL -- 40 --> Yjs
  Auto_AI_Router -- 40 --> Automerge
  Svyazi -- 39 --> Firecrawl
  knowledge_space -- 39 --> Firecrawl
  Wikontic -- 38 --> Yjs
  SENTINEL -- 38 --> Automerge
  Legal_RAG -- 37 --> Yjs
  Wikontic -- 36 --> Automerge
  Graph_RAG -- 36 --> Yjs
  LiteLLM -- 36 --> Yjs
  LiteLLM -- 36 --> Automerge
  AgentFS -- 35 --> Firecrawl
  Legal_RAG -- 35 --> Automerge
  Graph_RAG -- 34 --> Automerge
  Rufler -- 33 --> Firecrawl
  Yodoca -- 33 --> Firecrawl
  SENTINEL -- 33 --> Wikontic
  CardIndex -- 31 --> Firecrawl
  SENTINEL -- 31 --> Firecrawl
  AI_Factory -- 31 --> Wikontic
  Hybrid_RAG -- 30 --> Wikontic
  Tool_Search -- 30 --> Yjs
  Tool_Search -- 30 --> Automerge
  LiteParse -- 27 --> Firecrawl
  MemNet -- 27 --> Firecrawl
  Auto_AI_Router -- 27 --> Wikontic
  mclaude -- 25 --> Firecrawl
  AI_Factory -- 25 --> Firecrawl
  Graph_RAG -- 25 --> Wikontic
  Wikontic -- 25 --> Firecrawl
  Legal_RAG -- 23 --> Wikontic
  Hybrid_RAG -- 23 --> Firecrawl
  LiteLLM -- 23 --> Wikontic
  NGT_Memory -- 21 --> Firecrawl
  Tool_Search -- 21 --> Wikontic
  Graph_RAG -- 19 --> Firecrawl
  LiteLLM -- 19 --> Firecrawl
  Auto_AI_Router -- 19 --> Firecrawl
  Tool_Search -- 19 --> Firecrawl
  AutoResearch -- 19 --> Firecrawl
  Firecrawl -- 19 --> Yjs
  Firecrawl -- 19 --> Automerge
  Legal_RAG -- 17 --> Firecrawl
```

## Топ совместных упоминаний

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 276 |
| **Svyazi** | **CardIndex** | 246 |
| **Svyazi** | **AgentFS** | 215 |
| **AgentFS** | **Yodoca** | 194 |
| **Svyazi** | **knowledge-space** | 187 |
| **Svyazi** | **mclaude** | 185 |
| **CardIndex** | **Yodoca** | 180 |
| **Svyazi** | **Rufler** | 177 |
| **Svyazi** | **NGT Memory** | 176 |
| **Svyazi** | **MemNet** | 175 |
| **AgentFS** | **knowledge-space** | 174 |
| **CardIndex** | **AgentFS** | 173 |
| **Svyazi** | **LiteParse** | 165 |
| **Yodoca** | **NGT Memory** | 162 |
| **Yodoca** | **MemNet** | 160 |
| **knowledge-space** | **Yodoca** | 159 |
| **mclaude** | **Yodoca** | 157 |
| **mclaude** | **Rufler** | 149 |
| **Rufler** | **Yodoca** | 149 |
| **AgentFS** | **mclaude** | 147 |
| **AgentFS** | **LiteParse** | 145 |
| **knowledge-space** | **mclaude** | 145 |
| **Svyazi** | **AI Factory** | 143 |
| **AgentFS** | **Rufler** | 141 |
| **knowledge-space** | **Rufler** | 141 |

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
  Svyazi -> CardIndex [label="246"];
  Svyazi -> mclaude [label="185"];
  Svyazi -> Yodoca [label="276"];
  Svyazi -> NGT_Memory [label="176"];
  Svyazi -> MemNet [label="175"];
  Svyazi -> Wikontic [label="92"];
  CardIndex -> mclaude [label="124"];
  CardIndex -> Yodoca [label="180"];
  CardIndex -> NGT_Memory [label="134"];
  CardIndex -> MemNet [label="110"];
  CardIndex -> Wikontic [label="69"];
  mclaude -> Yodoca [label="157"];
  mclaude -> NGT_Memory [label="110"];
  mclaude -> MemNet [label="94"];
  mclaude -> Wikontic [label="50"];
  Yodoca -> NGT_Memory [label="162"];
  Yodoca -> MemNet [label="160"];
  Yodoca -> Wikontic [label="85"];
  NGT_Memory -> MemNet [label="92"];
  NGT_Memory -> Wikontic [label="69"];
  MemNet -> Wikontic [label="69"];
  Svyazi -> AgentFS [label="215"];
  AgentFS -> Yodoca [label="194"];
  AgentFS -> Wikontic [label="62"];
  Svyazi -> SENTINEL [label="137"];
  Svyazi -> Tool_Search [label="95"];
  CardIndex -> AgentFS [label="173"];
  CardIndex -> SENTINEL [label="111"];
  CardIndex -> Tool_Search [label="81"];
  AgentFS -> SENTINEL [label="129"];
  AgentFS -> Tool_Search [label="85"];
  Yodoca -> SENTINEL [label="117"];
  Yodoca -> Tool_Search [label="79"];
  SENTINEL -> Tool_Search [label="93"];
  Svyazi -> knowledge_space [label="187"];
  Svyazi -> Rufler [label="177"];
  Svyazi -> LiteParse [label="165"];
  Svyazi -> AutoResearch [label="116"];
  Svyazi -> Yjs [label="86"];
  Svyazi -> Automerge [label="70"];
  CardIndex -> knowledge_space [label="140"];
  CardIndex -> Rufler [label="124"];
  CardIndex -> LiteParse [label="130"];
  CardIndex -> AutoResearch [label="80"];
  CardIndex -> Yjs [label="74"];
  CardIndex -> Automerge [label="58"];
  AgentFS -> knowledge_space [label="174"];
  AgentFS -> mclaude [label="147"];
  AgentFS -> Rufler [label="141"];
  AgentFS -> LiteParse [label="145"];
  AgentFS -> MemNet [label="105"];
  AgentFS -> AutoResearch [label="84"];
  AgentFS -> Yjs [label="65"];
  AgentFS -> Automerge [label="61"];
  knowledge_space -> mclaude [label="145"];
  knowledge_space -> Rufler [label="141"];
  knowledge_space -> LiteParse [label="125"];
  knowledge_space -> Yodoca [label="159"];
  knowledge_space -> MemNet [label="106"];
  knowledge_space -> AutoResearch [label="76"];
  knowledge_space -> Wikontic [label="68"];
  knowledge_space -> Yjs [label="65"];
  knowledge_space -> Automerge [label="61"];
  mclaude -> Rufler [label="149"];
  mclaude -> LiteParse [label="129"];
  mclaude -> AutoResearch [label="84"];
  mclaude -> Yjs [label="57"];
  mclaude -> Automerge [label="55"];
  Rufler -> LiteParse [label="122"];
  Rufler -> Yodoca [label="149"];
  Rufler -> MemNet [label="103"];
  Rufler -> AutoResearch [label="88"];
  Rufler -> Wikontic [label="54"];
  Rufler -> Yjs [label="61"];
  Rufler -> Automerge [label="59"];
  LiteParse -> Yodoca [label="134"];
  LiteParse -> MemNet [label="88"];
  LiteParse -> AutoResearch [label="83"];
  LiteParse -> Wikontic [label="52"];
  LiteParse -> Yjs [label="60"];
  LiteParse -> Automerge [label="56"];
  Yodoca -> AutoResearch [label="98"];
  Yodoca -> Yjs [label="65"];
  Yodoca -> Automerge [label="61"];
  MemNet -> AutoResearch [label="69"];
  MemNet -> Yjs [label="54"];
  MemNet -> Automerge [label="48"];
  AutoResearch -> Wikontic [label="45"];
  AutoResearch -> Yjs [label="57"];
  AutoResearch -> Automerge [label="55"];
  Wikontic -> Yjs [label="38"];
  Wikontic -> Automerge [label="36"];
  Yjs -> Automerge [label="78"];
  Svyazi -> Firecrawl [label="39"];
  CardIndex -> Firecrawl [label="31"];
  AgentFS -> Firecrawl [label="35"];
  knowledge_space -> SENTINEL [label="91"];
  knowledge_space -> Firecrawl [label="39"];
  Rufler -> SENTINEL [label="101"];
  Rufler -> Firecrawl [label="33"];
  Yodoca -> Firecrawl [label="33"];
  SENTINEL -> Firecrawl [label="31"];
  Svyazi -> LiteLLM [label="87"];
  Svyazi -> Auto_AI_Router [label="115"];
  LiteParse -> LiteLLM [label="78"];
  LiteParse -> Auto_AI_Router [label="89"];
  LiteParse -> Tool_Search [label="80"];
  MemNet -> LiteLLM [label="48"];
  MemNet -> Auto_AI_Router [label="56"];
  MemNet -> Tool_Search [label="44"];
  LiteLLM -> Auto_AI_Router [label="96"];
  LiteLLM -> Tool_Search [label="82"];
  LiteLLM -> AutoResearch [label="58"];
  Auto_AI_Router -> Tool_Search [label="84"];
  Auto_AI_Router -> AutoResearch [label="64"];
  Tool_Search -> AutoResearch [label="50"];
  Svyazi -> AI_Factory [label="143"];
  Svyazi -> Legal_RAG [label="95"];
  Svyazi -> Hybrid_RAG [label="86"];
  Svyazi -> Graph_RAG [label="90"];
  CardIndex -> AI_Factory [label="111"];
  CardIndex -> Legal_RAG [label="78"];
  CardIndex -> Hybrid_RAG [label="79"];
  CardIndex -> Graph_RAG [label="66"];
  CardIndex -> LiteLLM [label="75"];
  CardIndex -> Auto_AI_Router [label="95"];
  AgentFS -> AI_Factory [label="119"];
  AgentFS -> Legal_RAG [label="80"];
  AgentFS -> Hybrid_RAG [label="81"];
  AgentFS -> Graph_RAG [label="74"];
  AgentFS -> NGT_Memory [label="125"];
  AgentFS -> LiteLLM [label="77"];
  AgentFS -> Auto_AI_Router [label="87"];
  knowledge_space -> AI_Factory [label="98"];
  knowledge_space -> Legal_RAG [label="72"];
  knowledge_space -> Hybrid_RAG [label="71"];
  knowledge_space -> Graph_RAG [label="66"];
  knowledge_space -> NGT_Memory [label="116"];
  knowledge_space -> LiteLLM [label="63"];
  knowledge_space -> Auto_AI_Router [label="77"];
  knowledge_space -> Tool_Search [label="63"];
  mclaude -> AI_Factory [label="131"];
  mclaude -> Legal_RAG [label="74"];
  mclaude -> Hybrid_RAG [label="69"];
  mclaude -> Graph_RAG [label="68"];
  mclaude -> SENTINEL [label="89"];
  mclaude -> LiteLLM [label="63"];
  mclaude -> Auto_AI_Router [label="75"];
  mclaude -> Tool_Search [label="65"];
  mclaude -> Firecrawl [label="25"];
  AI_Factory -> Rufler [label="115"];
  AI_Factory -> LiteParse [label="107"];
  AI_Factory -> Legal_RAG [label="73"];
  AI_Factory -> Hybrid_RAG [label="68"];
  AI_Factory -> Graph_RAG [label="62"];
  AI_Factory -> Yodoca [label="122"];
  AI_Factory -> NGT_Memory [label="103"];
  AI_Factory -> MemNet [label="67"];
  AI_Factory -> SENTINEL [label="95"];
  AI_Factory -> LiteLLM [label="69"];
  AI_Factory -> Auto_AI_Router [label="79"];
  AI_Factory -> Tool_Search [label="73"];
  AI_Factory -> AutoResearch [label="75"];
  AI_Factory -> Wikontic [label="31"];
  AI_Factory -> Firecrawl [label="25"];
  AI_Factory -> Yjs [label="44"];
  AI_Factory -> Automerge [label="42"];
  Rufler -> Legal_RAG [label="68"];
  Rufler -> Hybrid_RAG [label="69"];
  Rufler -> Graph_RAG [label="62"];
  Rufler -> NGT_Memory [label="88"];
  Rufler -> LiteLLM [label="63"];
  Rufler -> Auto_AI_Router [label="75"];
  Rufler -> Tool_Search [label="67"];
  LiteParse -> Legal_RAG [label="97"];
  LiteParse -> Hybrid_RAG [label="86"];
  LiteParse -> Graph_RAG [label="84"];
  LiteParse -> NGT_Memory [label="96"];
  LiteParse -> SENTINEL [label="99"];
  LiteParse -> Firecrawl [label="27"];
  Legal_RAG -> Hybrid_RAG [label="76"];
  Legal_RAG -> Graph_RAG [label="83"];
  Legal_RAG -> Yodoca [label="77"];
  Legal_RAG -> NGT_Memory [label="75"];
  Legal_RAG -> MemNet [label="55"];
  Legal_RAG -> SENTINEL [label="78"];
  Legal_RAG -> LiteLLM [label="64"];
  Legal_RAG -> Auto_AI_Router [label="74"];
  Legal_RAG -> Tool_Search [label="66"];
  Legal_RAG -> AutoResearch [label="44"];
  Legal_RAG -> Wikontic [label="23"];
  Legal_RAG -> Firecrawl [label="17"];
  Legal_RAG -> Yjs [label="37"];
  Legal_RAG -> Automerge [label="35"];
  Hybrid_RAG -> Graph_RAG [label="74"];
  Hybrid_RAG -> Yodoca [label="78"];
  Hybrid_RAG -> NGT_Memory [label="72"];
  Hybrid_RAG -> MemNet [label="52"];
  Hybrid_RAG -> SENTINEL [label="73"];
  Hybrid_RAG -> LiteLLM [label="63"];
  Hybrid_RAG -> Auto_AI_Router [label="67"];
  Hybrid_RAG -> Tool_Search [label="57"];
  Hybrid_RAG -> AutoResearch [label="49"];
  Hybrid_RAG -> Wikontic [label="30"];
  Hybrid_RAG -> Firecrawl [label="23"];
  Hybrid_RAG -> Yjs [label="41"];
  Hybrid_RAG -> Automerge [label="41"];
  Graph_RAG -> Yodoca [label="69"];
  Graph_RAG -> NGT_Memory [label="65"];
  Graph_RAG -> MemNet [label="51"];
  Graph_RAG -> SENTINEL [label="77"];
  Graph_RAG -> LiteLLM [label="53"];
  Graph_RAG -> Auto_AI_Router [label="65"];
  Graph_RAG -> Tool_Search [label="53"];
  Graph_RAG -> AutoResearch [label="41"];
  Graph_RAG -> Wikontic [label="25"];
  Graph_RAG -> Firecrawl [label="19"];
  Graph_RAG -> Yjs [label="36"];
  Graph_RAG -> Automerge [label="34"];
  Yodoca -> LiteLLM [label="75"];
  Yodoca -> Auto_AI_Router [label="91"];
  NGT_Memory -> SENTINEL [label="87"];
  NGT_Memory -> LiteLLM [label="69"];
  NGT_Memory -> Auto_AI_Router [label="87"];
  NGT_Memory -> Tool_Search [label="65"];
  NGT_Memory -> AutoResearch [label="67"];
  NGT_Memory -> Firecrawl [label="21"];
  NGT_Memory -> Yjs [label="58"];
  NGT_Memory -> Automerge [label="50"];
  MemNet -> SENTINEL [label="69"];
  MemNet -> Firecrawl [label="27"];
  SENTINEL -> LiteLLM [label="85"];
  SENTINEL -> Auto_AI_Router [label="97"];
  SENTINEL -> AutoResearch [label="55"];
  SENTINEL -> Wikontic [label="33"];
  SENTINEL -> Yjs [label="40"];
  SENTINEL -> Automerge [label="38"];
  LiteLLM -> Wikontic [label="23"];
  LiteLLM -> Firecrawl [label="19"];
  LiteLLM -> Yjs [label="36"];
  LiteLLM -> Automerge [label="36"];
  Auto_AI_Router -> Wikontic [label="27"];
  Auto_AI_Router -> Firecrawl [label="19"];
  Auto_AI_Router -> Yjs [label="48"];
  Auto_AI_Router -> Automerge [label="40"];
  Tool_Search -> Wikontic [label="21"];
  Tool_Search -> Firecrawl [label="19"];
  Tool_Search -> Yjs [label="30"];
  Tool_Search -> Automerge [label="30"];
  AutoResearch -> Firecrawl [label="19"];
  Wikontic -> Firecrawl [label="25"];
  Firecrawl -> Yjs [label="19"];
  Firecrawl -> Automerge [label="19"];
}
```

<!-- see-also -->

---

**Смотрите также:**
- [NETWORK](NETWORK.md)
- [MINDMAP](MINDMAP.md)
- [GLOSSARY](GLOSSARY.md)
- [ENTITIES](ENTITIES.md)

