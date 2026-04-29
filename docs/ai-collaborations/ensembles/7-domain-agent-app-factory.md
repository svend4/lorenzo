# Ансамбль 7 — Domain Agent App Factory

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

---
<!-- tags: rag, local-first, architecture, anthropic, self-improvement, collaboration -->




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

**Смотрите также:**
- [1-agentic-knowledge-os](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md)
- [9-ambient-team-agent](docs/ai-collaborations/ensembles/9-ambient-team-agent.md)
- [6-continuous-eval-loop](docs/ai-collaborations/ensembles/6-continuous-eval-loop.md)
- [3-forensic-rag](docs/ai-collaborations/ensembles/3-forensic-rag.md)

