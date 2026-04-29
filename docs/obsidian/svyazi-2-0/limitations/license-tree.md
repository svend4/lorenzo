---
title: "Лицензионные развилки"
tags:
  - svyazi-2-0
date: 2026-04-29
---

# Лицензионные развилки

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Ограничения, лицензии и что пока лучше не склеивать».
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, LiteParse, Legal RAG, Hybrid RAG, Graph RAG

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement, collaboration -->




> Источник: `deep-research-report (3).md`, раздел «Ограничения, лицензии и что пока лучше не склеивать».

Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Svyazi как базовый паттерн остаётся авторским закрытым прототипом в просмотренных материалах, NGT Memory использует BSL 1.1 и прямо говорит о бесплатности для личных проектов, а по ряду других систем лицензия в просмотренных источниках либо не акцентирована, либо требует проверки уже на стороне репозитория и бизнес‑сценария. Это означает, что для коммерчески чувствительного стека ранний выбор memory‑слоя — не только инженерный, но и лицензионный. citeturn41search0turn22view5turn18search1turn15search3

## Развилки в коротком виде

| Слой | Permissive путь | BSL/закрытый путь | Замечание |
|---|---|---|---|
| Базовый ingest/CardIndex | свой пересборкой по описанию Svyazi | использовать только как референс архитектуры | код Svyazi в просмотренных источниках закрыт. |
| Долговременная память | Yodoca (Apache 2.0), agent-memory-mcp (TBD), MemNet (MIT) | NGT Memory (BSL 1.1, free for personal) | для коммерческого продукта проверять отдельно. |
| Knowledge layer | knowledge-space (MIT) | — | спокойно. |
| Файловое ядро | AgentFS (MIT) | — | спокойно. |
| Forensic RAG | LiteParse (Apache 2.0) | Hybrid RAG / Legal RAG / Graph RAG (TBD) | в основном статьи без явно заявленной OSS‑лицензии. |
| Routing/security | LiteLLM (MIT, кроме enterprise dirs), Auto AI Router (Apache 2.0) | SENTINEL (TBD) | смешанная картина. |
| Self-improvement | AutoResearch (TBD) | Sequential (research, без OSS) | использовать как pattern, не как dependency. |

<!-- see-also -->

---

**Смотрите также:**
- [[14-limitations]]
- [[executive-summary]]
- [[first-contacts]]
- [[risks]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[14-limitations]] (сходство 0.20)
- [[14-limitations]] (сходство 0.20)
- [[MINDMAP]] (сходство 0.19)

