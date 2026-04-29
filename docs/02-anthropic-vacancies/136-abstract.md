# Abstract

<!-- summary -->
> We introduce the **Double-Triangle Architecture** for human-AI

---



## Abstract

We introduce the **Double-Triangle Architecture** for human-AI 
collaboration in distributed knowledge work. The central thesis: 
each human participant in modern AI-assisted workflows 
simultaneously occupies two roles — as **conductor** of personal 
AI assistants (lower triangle, directed downward from human to 
assistants), and as **performer** coordinated by higher-level 
meta-agents (upper triangle, directed upward from human toward 
team-level coordination). These two triangles superimpose to form 
a six-pointed star topology, which we argue is the correct 
architectural primitive for the next generation of AI-managed 
knowledge work.

Existing systems implement only one triangle: personal assistants 
(Cursor, Copilot, ChatGPT) operate in the lower triangle only; 
multi-agent frameworks (CrewAI, MetaGPT, AutoGen) operate in the 
upper triangle only and typically replace humans rather than 
augment them. Neither paradigm captures the full structure of how 
humans will actually work alongside AI over the next decade.

We present three contributions:

1. **Formal specification** of the Double-Triangle Architecture, 
   including three inter-layer protocols and six architectural 
   invariants
2. **Reference implementation** via **Nautilus Portal Protocol** 
   (NPP v1.1), which provides the federated knowledge substrate 
   required to support the architecture
3. **Deployment paths** for four concrete domains: humanities 
   (legal/medical/social), project management, open-source 
   development, and generic knowledge work

We also present empirical evidence from a 4-month single-person 
AI-assisted deployment producing 6,782 lines of production code 
across 13 adapters, a formal protocol specification, REST API, 
SDK, Docker containerization, and 60 passing tests — suggesting 
that **single-person operations can achieve team-level output** 
when the Double-Triangle substrate is properly instantiated.

We conclude with open questions on governance, consent, economics, 
and burnout dynamics, and invite research collaboration on these 
unsolved issues.

---
