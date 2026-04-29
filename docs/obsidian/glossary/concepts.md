---
title: "Ключевые понятия и паттерны"
tags:
  - glossary
date: 2026-04-29
---

# Ключевые понятия и паттерны

<!-- summary -->
> Не проекты, а концепции, которые повторяются в нескольких разделах.
**Проекты:** Svyazi, CardIndex, Legal RAG, Yodoca, NGT Memory, MemNet, Tool Search, AutoResearch

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, anthropic, self-improvement, collaboration -->




Не проекты, а концепции, которые повторяются в нескольких разделах.

| Понятие | Краткое определение | Где раскрыто |
|---|---|---|
| **CardIndex** | Source of truth: неизменяемая карточка как единица знания | [[card-envelope|Card Envelope]] · [[svyazi]] |
| **Card Envelope** | Стандарт схемы карточки: `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | [[card-envelope|Card Envelope]] · [[integration-spec|Integration spec]] |
| **Evidence Envelope** | Стандарт привязки вывода к источнику: `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | [[evidence-envelope|Evidence Envelope]] |
| **Memory Write Policy** | Различение `episode` / `fact` / `proposal` / `decay_event` при записи в память | [[memory-write-policy|Memory Write Policy]] |
| **Skill and Tool Policy** | Класс tool: `read` / `annotate` / `plan` / `mutate` / `publish` / `external_send` | [[skill-tool-policy|Skill and Tool Policy]] |
| **Review Record** | Артефакт человеческого решения: `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | [[review-record|Review Record]] |
| **Trace Envelope** | Расширение для AgentOps: trace_id, model_route, tools_used, token_cost, anomaly_flags | [[02-agentops-trace-envelope|AgentOps + Trace Envelope]] |
| **Hot path / Slow path** | Yodoca‑паттерн: эпизоды в SQLite за <50 мс vs асинхронные эмбеддинги ночью | [[yodoca|Yodoca карточка]] · [[01-yodoca|Habr key‑findings — Yodoca]] |
| **Ebbinghaus decay** | Контролируемое забывание редко используемых фактов | [[yodoca]] · [[memory-write-policy|Memory Write Policy]] |
| **Hebbian / STDP plasticity** | Усиление связи между концептами при ко‑активации | [[ngt-memory|NGT Memory]] · [[memnet]] · [[1-neuromorphic-ssm|Hardware pair 1]] |
| **Spreading activation / dream phase** | Самопроизвольная активация памяти без внешнего входа для поиска скрытых связей | [[memnet]] · [[02-memnet|Habr key‑findings — MemNet]] |
| **Discovery file** | Накопление неизвестного — то, что система не смогла классифицировать | [[svyazi]] · [[5-tinyml-mcp-skills|Sensor-driven life log]] |
| **«LLM как периферия»** | Архитектура, где LLM — не ядро, а узел; код отвечает за стабильность | [[03-pda-llm-as-periphery|PDA — LLM как периферия]] |
| **Sequential vs Coordinator** | Распределённая цепочка агентов, видящих результаты предшественников, выигрывает у центрального координатора на 44% | [[autoresearch-sequential|AutoResearch + Sequential]] · [[04-dochkina-sequential|Habr key‑findings — Dochkina]] |
| **Adversarial review** | Один агент пишет, другие критикуют; multi‑model | [[08-conductor-adversarial-review-auto-ai-router|Комбинация 8]] · [[3-adversarial-multi-ide|Adversarial × Multi-IDE]] |
| **Local‑first / privacy‑by‑design** | Данные принадлежат устройству пользователя, в облако только избранное | [[privacy]] · [[4-riscv-privacy|Hardware pair 4]] · [[G-federated-local-graph|Federated Local Graph]] |
| **Privacy by design** | Контакты — в отдельный raw‑слой; в карточки уходит только очищенный профиль | [[default-policy|Default policy]] |
| **Page-level grounding** | Единица доказательства — страница, не чанк | [[legal-rag|Legal RAG]] · [[3-forensic-rag|Forensic RAG (ai‑collab)]] |
| **Lazy MCP loading (Tool Search)** | Не грузить все MCP‑инструменты в контекст; падение overhead с 82k до 5.7k токенов | [[security-routing-plane|Security + routing plane]] |
| **Two parents → many children** | Метафора: hardware/software пара рождает несколько по‑разному ориентированных потомков | [[7-metaphor|Hardware metaphor]] · [[6-metaphor|Software metaphor]] |
| **Скромные родители → мощные дети** | Та же мысль с другой стороны: ни один проект сам по себе не революционен | [[01-08-summary|Synthesis 1‑8]] |
| **One‑man AI company** | Один человек ведёт 30–50 дел Sozialrecht параллельно с качеством офиса из 5 юристов | [[1-one-person-one-company|One person = one company]] |
| **Q6‑гиперкуб / MoME** | 64 гексаграммы как вершины Q6, MoME‑роутинг по геометрии | [[2-tsu-mome|Hardware pair 2 — TSU × MoME]] · [[3-zinc-hybrid-arch|Hardware pair 3]] · [[01-profile-five-layers|Profile five layers]] |
| **LCI (Lyapunov Coherence Index)** | Метрика энергетической когерентности системы | [[2-tsu-mome|Hardware pair 2]] · [[06-svyazi-2-0-block-map|Svyazi 2.0 block map]] |
| **Forward Deployed Engineer (FDE)** | Инженер, приходящий к клиенту с проблемой, строящий прототип на Claude в production | [[02-primary-fde|FDE primary match]] · [[01-fde-downgraded|FDE downgraded]] |
| **Beneficial Deployments** | Anthropic‑программа: применение Claude к общественно‑полезным задачам | [[03-secondary-beneficial-deployments|Secondary match]] · [[02-sales|Sales]] |

<!-- see-also -->

---

**Смотрите также:**
- [[components-by-name]]
- [[11-integration-contracts]]
- [[11-интеграционный-контракт-который-стоит-зафиксироват]]
- [[QA]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[components-by-name]] (сходство 0.19)
- [[11-integration-contracts]] (сходство 0.17)
- [[11-integration-contracts]] (сходство 0.17)

