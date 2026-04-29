---
title: "11 Integration Contracts"
tags:
  - svyazi
date: 2026-04-29
---



<!-- toc -->
## Содержание

- [Интеграционный контракт, который стоит зафиксировать сразу](#интеграционный-контракт-который-стоит-зафиксировать-сразу)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---

<!-- summary -->
> Чтобы все эти ансамбли не рассыпались, полезно зафиксировать **минимальный интерфейсный контракт** между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели 
**Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], mclaude, AI Factory, LiteParse, Legal RAG[^rag], Hybrid RAG

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement -->



## Интеграционный контракт, который стоит зафиксировать сразу

Чтобы все эти ансамбли не рассыпались, полезно зафиксировать **минимальный интерфейсный контракт** между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели появятся три несовместимые сущности с названием “карточка”, два разных формата evidence и четыре несовместимых местоположения памяти.

Первый контракт — **Card Envelope**. У каждой карточки должен быть неизменяемый `card_id`, `card_type`, статус `raw | normalized | inferred | approved | rejected | decayed`, список source links, список relation edges, временные метки и хэш полезной нагрузки. Эта структура логически следует из CardIndex‑мышления Svyazi, immutable/event‑style практик AgentFS и Memory OS, а также из необходимости разводить truth и proposal в memory‑системах. Это не “идеальная онтология”, а минимальный договор, который позволяет системам вообще разговаривать между собой. citeturn41search0turn27view0turn39view3turn20view16

Второй контракт — **Evidence Envelope**. Любой retrieval‑ответ, match suggestion, profile enrichment или auto‑summary должен возвращать не только текст, но и `source_id`, `page`, `span`, `box`, `retrieval_method`, `confidence`, `supporting_nodes`. Для документов это page+box; для чатов и заметок — message/thread/time span; для голосовых эпизодов — timestamp window; для ассоциативных выводов — список triggered nodes и path explanation. Это прямой синтез из LiteParse/research-docs, Legal RAG, Hybrid RAG и Graph RAG. Без такого формата нельзя построить ни нормальную ручную модерацию, ни “объяснение рекомендации”. citeturn20view5turn20view6turn34view2turn34view3

Третий контракт — **Memory Write Policy**. Система должна различать хотя бы четыре режима записи: `episode` для сырых наблюдений, `fact` для подтверждённого знания, `proposal` для гипотез и `decay_event` для понижения значимости. Yodoca[^yodoca] уже мыслит память через consolidation + forgetting, NGT[^ngt] Memory — через ассоциативные связи и иерархическую консолидацию, agent-memory-mcp — через typed memory primitives, а Memory OS — через bi‑temporal и provenance‑heavy представление знаний. Из этих линий следует, что “записать что-то в память” никогда не должно быть одной неразличимой операцией. citeturn21view0turn22view4turn20view16turn39view3

Четвёртый контракт — **Skill and Tool Policy**. Каждый skill или MCP[^mcp]‑инструмент должен иметь класс доступа, класс среды, условия вызова и postcondition. Простейшее разбиение: `read`, `annotate`, `plan`, `mutate`, `publish`, `external_send`. Это дополняет Tool Search, который экономит контекст, но сам по себе не задаёт governance; LiteLLM и Auto AI Router, которые управляют провайдерами, но не правами; и SENTINEL[^sentinel], который контролирует угрозы, но выигрывает от того, что политика уже структурирована, а не размазана по промптам. citeturn39view1turn11search2turn39view0turn20view10

Ниже — упрощённая интеграционная спецификация, которую реально можно внедрить в MVP без чрезмерной формализации.

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope | `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope | `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy | `write_type`, `promotion_rule`, `review_required`, `decay_policy` | Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy | `tool_class`, `approval_mode`, `path_scope`, `network_scope`, `output_target` | Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record | `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | Не путать machine suggestion с accepted truth | mclaude, AI Factory, Sequential citeturn20view2turn20view3turn20view11 |

<!-- similar-docs -->

---

**Похожие документы:**
- [[11-интеграционный-контракт-который-стоит-зафиксироват]] (сходство 1.00)
- [[366-технический-stack-svyazi-2-0-foundation]] (сходство 0.19)
- [[09-архитектурные-зазоры-которые-важнее-новых-инструме]] (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [[11-интеграционный-контракт-который-стоит-зафиксироват]]
- [[366-технический-stack-svyazi-2-0-foundation]]
- [[09-architectural-gaps]]
- [[09-архитектурные-зазоры-которые-важнее-новых-инструме]]



<!-- footnotes-added -->

---

[^mcp]: Model Context Protocol — протокол для AI-инструментов

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^ngt]: OSS-проект: ассоциативный граф памяти (BSL 1.1)

[^sentinel]: OSS-проект: безопасность и allowlist для MCP

[^svyazi]: Главный проект: экосистема AI-компонентов

<!-- backlinks-auto -->
## Упоминается в

- [Svyazi[^svyazi] 2.0 — Архитектура и исследование](docs/01-svyazi/README.md)

<!-- related-auto -->
## Связанные документы

- [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксировать сразу]] _81%_
- [[09-architectural-gaps|09 Architectural Gaps]] _48%_
- [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструментов]] _48%_
- [[07-mvp-planning|07 Mvp Planning]] _33%_
- [[10-second-order-ensembles|10 Second Order Ensembles]] _33%_
- [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]] _33%_
- [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]] _33%_
- [[13-contacts|13 Contacts]] _29%_
