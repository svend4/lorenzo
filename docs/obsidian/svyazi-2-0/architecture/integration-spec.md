---
title: "Интеграционная спецификация (минимум для MVP)"
tags:
  - memory
  - rag
  - orchestration
  - security
  - knowledge
  - ingestion
  - architecture
  - roadmap
  - svyazi-2-0
date: 2026-04-29
---

# Интеграционная спецификация (минимум для MVP)

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`.
**Проекты:** Svyazi, AgentFS, mclaude, AI Factory, LiteParse, Legal RAG, Graph RAG, Yodoca

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap -->




> Источник: `deep-research-report (3).md`.

Чтобы все ансамбли не рассыпались, полезно зафиксировать **минимальный интерфейсный контракт** между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели появятся три несовместимые сущности с названием «карточка», два разных формата evidence и четыре несовместимых местоположения памяти.

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope | `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope | `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy | `write_type`, `promotion_rule`, `review_required`, `decay_policy` | Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy | `tool_class`, `approval_mode`, `path_scope`, `network_scope`, `output_target` | Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record | `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | Не путать machine suggestion с accepted truth | mclaude, AI Factory, Sequential citeturn20view2turn20view3turn20view11 |

Подробности — в отдельных файлах:

- [[card-envelope|`card-envelope.md`]]
- [[evidence-envelope|`evidence-envelope.md`]]
- [[memory-write-policy|`memory-write-policy.md`]]
- [[skill-tool-policy|`skill-tool-policy.md`]]
- [[review-record|`review-record.md`]]

<!-- see-also -->

---

**Смотрите также:**
- [[11-интеграционный-контракт-который-стоит-зафиксироват]]
- [[11-integration-contracts]]
- [[review-record]]
- [[QA]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[11-интеграционный-контракт-который-стоит-зафиксироват]] (сходство 0.39)
- [[11-integration-contracts]] (сходство 0.37)
- [[11-интеграционный-контракт-который-стоит-зафиксироват]] (сходство 0.37)

