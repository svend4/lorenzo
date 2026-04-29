# 4. Nautilus Portal as Reference Substrate

<!-- summary -->
> The Double-Triangle Architecture requires a substrate capable of:

---

<!-- toc -->
## Содержание

- [4. Nautilus Portal as Reference Substrate](#4-nautilus-portal-as-reference-substrate)
  - [4.1. NPP Components Mapped to Double-Triangle Requirements](#41-npp-components-mapped-to-double-triangle-requirements)
  - [4.2. Required Extensions to NPP for Double-Triangle](#42-required-extensions-to-npp-for-double-triangle)
  - [4.3. Empirical Evidence from Nautilus Reference Implementation](#43-empirical-evidence-from-nautilus-reference-implementation)

---

<!-- tags: rag, knowledge, architecture, collaboration -->




## 4. Nautilus Portal as Reference Substrate

The Double-Triangle Architecture requires a substrate capable of:
- Representing diverse knowledge sources uniformly (for assistants 
  to query across Nodes)
- Providing distributed, persistent memory (for context continuity)
- Supporting multi-level consensus (for conflict resolution)
- Enabling federated queries (for Protocol 3 routing)

**Nautilus Portal Protocol (NPP) v1.1** was designed for knowledge 
federation but provides exactly these properties. We propose NPP 
as the **reference substrate** for Double-Triangle implementations.

### 4.1. NPP Components Mapped to Double-Triangle Requirements

**Adapters** (NPP) = interface between participants and shared 
space. In Double-Triangle, each assistant can read and write 
through the same adapter mechanism used by any participant, 
providing uniform cross-triangle access.

**PortalEntry structure** (NPP) = unified unit of knowledge. In 
Double-Triangle, this represents tasks, deliverables, context 
updates, and notifications uniformly, enabling a single mechanism 
for all inter-layer communication.

**Consensus model** (NPP) = conflict resolution between sources. 
In Double-Triangle, consensus operates at three levels (intra-Node 
between assistants, inter-Node, meta-level), all using the same 
mechanism with different scope.

**Q6 coordinate space** (NPP) = unified addressing for concepts. 
In Double-Triangle, Q6 addresses tasks and deliverables uniformly 
across domains, enabling cross-Node task similarity queries.

**Bridges** (NPP) = formal links between participants' domains. 
In Double-Triangle, bridges formalize responsibility boundaries 
between Nodes ("authentication is N_1's domain, authorization is 
N_2's, interface is: token format").

**Compatibility levels** (NPP) = graduated participation. In 
Double-Triangle, this allows Nodes to join teams with minimal 
setup (Level 0–1) and mature over time to full integration 
(Level 3).

**Federation over merging** (NPP principle) = preserve source 
autonomy. In Double-Triangle, this ensures Nodes remain 
functional without the meta-agent; M augments coordination but 
does not replace Node autonomy.

### 4.2. Required Extensions to NPP for Double-Triangle

While NPP v1.1 provides the substrate, three extensions are needed 
for full Double-Triangle support:

**Extension 1: Agent Registry.** NPP v1.1 registers repositories. 
Double-Triangle requires registering **agents** (AI assistants 
and meta-agents) as first-class participants. Agents have 
identities, capabilities, scope of authority, and audit trails.

**Extension 2: Task Protocol.** NPP v1.1 supports queries but not 
tasks. Double-Triangle requires formal task objects: task 
assignment, acceptance, completion, rejection, reassignment.

**Extension 3: Role Protocol.** NPP v1.1 has no concept of roles. 
Double-Triangle requires roles to be first-class: "this Node is 
responsible for X", "this assistant handles Y". Role assignments 
constrain Protocol 3 routing.

These extensions are additive — they do not break NPP v1.1 
compatibility. A Double-Triangle implementation is an NPP v1.1 
implementation plus these extensions.

### 4.3. Empirical Evidence from Nautilus Reference Implementation

The Nautilus reference implementation at `github.com/svend4/nautilus` 
provides empirical evidence that the substrate works in practice. 
As of 2026-04:

- 6,782 lines of Python, 13 adapters, 60 tests passing, 0 mypy 
  errors
- 7 knowledge repositories federated (info1, pro2, meta, data2, 
  data7, infosystems, ai_agents)
- 5 extended adapters enabling federation of external sources 
  (Obsidian vaults, arXiv papers, GitHub-topic repos, JSONL files, 
  self-declaring repos via AutoAdapter)
- Zero external dependencies (Python stdlib only)
- Full REST API, MCP wrapper, OpenAPI specification, Docker 
  deployment, CI/CD

This demonstrates that NPP can be implemented by a single 
developer in 4 months, providing a practical foundation for 
Double-Triangle deployments.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [158-4-proposed-infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md) (сходство 0.20)
- [139-2-the-double-triangle-architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) (сходство 0.17)
- [136-abstract](docs/02-anthropic-vacancies/136-abstract.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [158-4-proposed-infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md)
- [139-2-the-double-triangle-architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md)
- [136-abstract](docs/02-anthropic-vacancies/136-abstract.md)
- [68-about](docs/02-anthropic-vacancies/68-about.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) _29%_
- [5. Pattern Library as Bridge Between Triangles](docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md) _29%_
- [Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md) _29%_
- [Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md) _29%_
- [🇬🇧 About](docs/02-anthropic-vacancies/68-about.md) _29%_
- [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) _25%_
- [4. Proposed Infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md) _25%_
- [13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) _25%_
