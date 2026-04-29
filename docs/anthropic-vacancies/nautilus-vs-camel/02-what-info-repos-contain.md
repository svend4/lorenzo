# Что у нас есть в трёх info repositories (info1/info7/info40)

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

Что у нас есть в трёх info repositories

Из info1, info7, info40, agent-related concepts включают:

Из info7:

7 Professional Agents (Medical, Investment, Career, Legal, Social, Healthcare, Financial) — concepts, не working code

Leonardo AI с RL + RAG + Meta-Learning + Consciousness Layer — architectural concept

5-level meta-agent hierarchy — coordination pattern

Five orchestration strategies (Sequential, Parallel, Pipeline, Hierarchical, Collaborative) — decision framework

Corpus Callosum pattern (RAG ↔ Knowledge Graph bidirectional) — integration approach

Из info40:

Marketplace concept для agents (commercial/volunteer/hybrid) — economic model

5 detailed use cases (academic research, startup MVP, content marketing, medical research, legal due diligence) — applied scenarios

Three-layer microservices architecture (Gateway, Registry/Marketplace/Orchestrator, Workers) — deployment structure

PostgreSQL schema concepts (9 tables) — data model

Из info1 (inferred):

Earlier formulations что evolved в info7 и info40

Большинство этого — conceptual frameworks, не реализованный code.

Возможно ли построить эти на CAMEL? Прямой ответ

Да, возможно, и я думаю это правильное направление. CAMEL действительно подходит для этого лучше, чем Hermes или Cowork. Дайте мне объяснить почему.

Почему CAMEL особенно хорошо подходит

1. Multi-agent first. CAMEL specifically designed для систем из multiple agents, что точно соответствует info7's multi-agent vision (Professional Agents) и info40's marketplace (multiple specialized agents).

2. Workforce pattern уже реализован. Workforce coordinates specialized agents для complex tasks. Это directly maps к info7's «5-level meta-agent hierarchy» concept. Не нужно строить это с нуля; CAMEL provides infrastructure.

3. Role-Playing pattern для multi-agent collaboration. Когда info7 описывает 7 Professional Agents working together, CAMEL's Role-Playing setup natively supports это.

4. Apache 2.0 license. Дружественное для commercial use, что важно если info40's marketplace concept будет implemented commercially.

5. Mature framework. 3 года разработки, 209 contributors, established patterns. Vs Hermes (2 месяца) или своё с нуля (years).

6. Python-based. Большинство ML/AI ecosystem in Python. Easy integration с RAG libraries, knowledge graphs, LLM providers.

7. Designed for research and experimentation. info1/info7/info40 conceptual exploration легче переводится в CAMEL framework, который designed для exactly such exploration.

Почему не Hermes для этой задачи

Hermes лучше для personal productivity scenario (single user, persistent agent через messaging platforms). Но:

Single-agent focus limits multi-agent coordination

Skills system designed for general capabilities, не для Professional Agent specialization

Marketplace concept не natural fit

Workforce-style coordination требует много custom development

Почему не Cowork

Cowork is excellent для end-user experience, но:

Vendor lock-in to Anthropic

No native multi-agent coordination

Building marketplace/orchestration on top required custom work outside Cowork

Apache 2.0 / MIT preferred для open-source academic work

Конкретно: как может выглядеть синтез CAMEL + info insights

Дайте мне показать conceptual architecture который could implement insights из info repositories using CAMEL infrastructure:

Layer 1: CAMEL как execution substrate

CAMEL provides:

ChatAgent base class для individual agents

Workforce для coordination

Role-Playing для collaboration

Memory storage abstractions

Tool integration framework

MCP support

Это уже работает. Не нужно строить.

Layer 2: Info insights as adaptation layer

Над CAMEL можно adapt:

Из info7 — Professional Agent specialization pattern:
Each of info7's «7 Professional Agents» становится CAMEL ChatAgent с specialized system prompt и domain-specific tools.

python

# Conceptual sketch, не tested code:
from camel.agents import ChatAgent

legal_agent = ChatAgent(
system_message="You are a German social law specialist...",
tools=[sgb_lookup_tool, court_database_tool, ...]
)

medical_agent = ChatAgent(
system_message="You are a medical assessment specialist...",
tools=[icd10_tool, medical_literature_tool, ...]
)

# Etc.

CAMEL handles all infrastructure. Specializations — это just configurations.

Из info7 — 5-level hierarchy:
CAMEL's Workforce can be nested. Top-level workforce coordinates department workforces, which coordinate team workforces, which coordinate individual agents. Это natural fit даже если CAMEL не explicitly designed для 5 levels.

Из info7 — Five orchestration strategies:
В CAMEL вы choose between:

Sequential: passing messages between ChatAgents в order

Parallel: spawning multiple agents simultaneously

Pipeline: streaming data через chains

Hierarchical: Workforce delegating до sub-Workforces

Collaborative: Role-Playing между agents

CAMEL provides primitives для всех этих patterns.

Из info40 — Marketplace concept:
This requires building на top of CAMEL. CAMEL doesn't natively provide marketplace, но agents created в CAMEL могут быть registered в external marketplace system. info40's PostgreSQL schema concepts could service в качестве blueprint.

Из info40 — Use cases scenarios:
Каждый из 5 use cases (academic research, startup MVP, etc.) можно implement как CAMEL example. Например, Legal M&A Due Diligence — это natural fit для Workforce of specialized agents.

Из info7 — Corpus Callosum pattern:
CAMEL has separate Memory и RAG modules. info7's bidirectional sync pattern can be implemented as adaptation layer between CAMEL's memory storage и external knowledge graph.

Layer 3: Nautilus как federation/coordination

Здесь Nautilus (ваш existing project) plays its role. Multiple CAMEL-based deployments could federate через Nautilus Portal Protocol:

Practitioner A's deployment (Legal Advocate Colleague на CAMEL)

Practitioner B's deployment (Medical Diagnosis Assistant на CAMEL)

Practitioner C's deployment (Education Counselor на CAMEL)

Nautilus federates queries across them. Each remains independent CAMEL instance, но they can share patterns, knowledge, configurations через Nautilus Portal Protocol.

Связка: посредник между ними

Ваш вопрос о «какой посредник» — это критично.

Я вижу несколько possibilities:

Посредник Variant 1: MCP Protocol

MCP может service в качестве universal mediator.

CAMEL agents использует tools через MCP. Specialized capabilities packaged as MCP servers:

mcp-sgb-knowledge — German social law knowledge

mcp-medical-icd10 — medical coding

mcp-legal-precedents — case law database

CAMEL ChatAgent consumes any MCP server. Same MCP servers могут also быть consumed by Hermes, Cowork, Claude Code, и другими MCP-compliant systems.

This means: build domain expertise once как MCP servers, deploy across multiple agent platforms.

Посредник Variant 2: Nautilus Portal Protocol

Nautilus Portal Protocol as federation layer.

Каждый CAMEL deployment exposes Portal Protocol endpoints. Other CAMEL deployments (или Hermes, или Cowork) могут query patterns, knowledge, configurations через Portal Protocol.

Nautilus does passive federation — это правильный role. CAMEL deployments do active execution. Combination.

Посредник Variant 3: Marketplace (info40 inspired)

Marketplace as discovery mediator.

Practitioners deploy CAMEL-based services. Service registry (info40 architecture) lets others discover what's available. Practitioners outside specific deployment can use available agents.

Это extension of Nautilus Portal Protocol — adds commercial/volunteer/hybrid economy dimension.

Recommended combination

Optimal posredник setup:

MCP для interoperability across agent platforms

Nautilus Portal Protocol для federation knowledge

Marketplace layer (inspired by info40) для discovery and economy

Каждый посредник handles different concern. Together они enable rich ecosystem.
