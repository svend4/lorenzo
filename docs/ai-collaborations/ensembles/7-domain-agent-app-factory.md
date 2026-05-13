---
date: 2026-05-13
tags: [memory, rag, orchestration, local-first, architecture]
state: raw
---

# Ансамбль 7 — Domain Agent App Factory

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Habr
Статья про AI-ассистента юридической поддержки даёт бизнес-рамку: не «сделаем AI», а метрики — снижение нагрузки, время ответа, стоимость обращения, точность, hallucinations, user satisfaction; дальше выбираются RAG/GraphRAG, модель, deployment

---
<!-- tags: rag, local-first, architecture, anthropic, self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

7. Domain Agent App Factory: «из одного фитнес-тренера — фабрика вертикальных ассистентов»

Родители: Open-source AI Fitness Coach + Coreness + Legal Support AI Assistant + Moltbot/OpenClaw.

Фитнес-тренер на Хабре интересен не фитнесом, а архитектурой: multi-provider AI, 27 MCP-инструментов, Knowledge Graph упражнений на NetworkX/Neo4j, RAG-память на pgvector, PWA offline, Docker Compose и MIT-лицензия. Habr

Coreness — self-hosted платформа для развёртывания AI-ботов через YAML-конфиги: один сервер, много изолированных тенантов, свои LLM-модели, RAG из коробки, PostgreSQL с RLS и event-driven архитектура. Habr

Статья про AI-ассистента юридической поддержки даёт бизнес-рамку: не «сделаем AI», а метрики — снижение нагрузки, время ответа, стоимость обращения, точность, hallucinations, user satisfaction; дальше выбираются RAG/GraphRAG, модель, deployment и eval. Habr

Moltbot/OpenClaw добавляет автономного агента 24/7 с инструментами, браузером, почтой, API, фоном и 700+ skills; автор подчёркивает отличие от ChatGPT: агент не только отвечает, а выполняет действия. Habr

Что рождается при склейке:

Получается фабрика вертикальных агентных приложений.

Схема:

Coreness tenants/YAML → domain KG → domain MCP tools → RAG memory → PWA/Telegram → eval/business metrics

Дети этой связки:

Legal Coach — юридический ассистент с графом норм/документов, RAG-памятью, MCP-инструментами для дел, human escalation и business metrics.

Community Mentor — AI-наставник сообщества: знает участников, навыки, проекты, вакансии, события, предлагает связи и дорожные карты коллабораций.

BIM/Engineering Coach — тот же паттерн для инженерных стандартов, чертежей, спецификаций, документации, технической поддержки.

Главное новое свойство: вертикальный AI-продукт собирается не с нуля, а из повторяемого шаблона: KG + tools + RAG + tenant isolation + interface + eval.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Ансамбль 7 Domain Agent App Factory"
```

## Смотрите также
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [9-ambient-team-agent](9-ambient-team-agent.md)
- [6-continuous-eval-loop](6-continuous-eval-loop.md)
- [3-forensic-rag](3-forensic-rag.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (14):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [2-distributed-agent-workshop](2-distributed-agent-workshop.md)
- [3-forensic-rag](3-forensic-rag.md)
- _...ещё 6_


<!-- similar-docs -->

---

**Похожие документы:**
- [7-domain-agent-app-factory](../../obsidian/ai-collaborations/ensembles/7-domain-agent-app-factory.md) (сходство 0.99)
- [9-ambient-team-agent](9-ambient-team-agent.md) (сходство 0.24)
- [9-ambient-team-agent](../../obsidian/ai-collaborations/ensembles/9-ambient-team-agent.md) (сходство 0.24)

