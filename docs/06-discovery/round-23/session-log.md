---
date: 2026-05-15
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 23 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Durable State Architecture (1031440, май 2026) — Production-ready агент требует персистентного state: SessionContext (компактная техкарта, не полный транскрипт) + ApprovalQueue (Human-in-the-loop) + BackgroundJobs (async, пользователь не блокируется)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** LLM в HR-рекрутинге, Durable State агентов, RPA+AI Enterprise, Структурные инъекции

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| YooMoney: LLM-скрининг резюме — -70% труда HR, Gemma-3 on-premise | YooMoney | HR / orchestration / analytics | `projects/yoomoney-llm-hr-screening.md` |
| Правильная агентская архитектура 2026: Durable State + Approvals + Background Jobs | независимый разработчик | orchestration / memory | `projects/production-agent-durable-state.md` |
| RPA + AI-агенты в Enterprise (не вместо, а вместе) — RGS IT | RGS IT (Сергей) | orchestration / automation | `projects/rpa-llm-enterprise-rgs.md` |
| Структурные инъекции в LLM-агентов — Phantom Framework (Tsinghua/Ant Group) | Tsinghua + Ant Group | security / orchestration | `projects/structural-prompt-injection-phantom.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Durable State + A2A (R21) | agent interop | SessionContext синхронизируется между агентами: Discovery/Enricher/Monitor получают персистентный state | ⭐⭐⭐⭐⭐ |
| Phantom Injection + Jay Guard (R21) | privacy + security | Jay Guard анонимизирует данные ДО передачи агенту + Phantom-защита от structural injection = двойная безопасность | ⭐⭐⭐⭐⭐ |
| RPA+AI + n8n (R22) | automation | n8n визуальный оркестратор AI-агент → RPA-инструменты: существующие сценарии как tools | ⭐⭐⭐⭐ |
| HR Screening + LLM Router (R20) | cost optimization | Haiku для bulk-скрининга резюме, Sonnet только для финалистов → -85% стоимость | ⭐⭐⭐⭐ |
| Phantom + Durable State (R23) | safe agents | ApprovalQueue как Human-in-the-loop: агент не выполняет необратимые действия без подтверждения человека | ⭐⭐⭐⭐ |

## Главные находки раунда

**YooMoney HR Screening** (986874, январь 2026) — Gemma-3 on-premise в CRM-R: скрининг резюме на hard/soft skills, ранжирование по релевантности, evidence-based (только цитаты из текста). -70% ручного труда HRBP. Данные кандидатов не покидают контур (ФЗ-152). Паттерн: Document Relevance Analysis применимо к любым документам (не только HR). Для Lorenzo: оценка документов по критериям Svyazi.

**Durable State Architecture** (1031440, май 2026) — Production-ready агент требует персистентного state: SessionContext (компактная техкарта, не полный транскрипт) + ApprovalQueue (Human-in-the-loop) + BackgroundJobs (async, пользователь не блокируется). Ключевая проблема: stateless агент ломается при reconnect. Redis/Postgres хранят state вне агента. Для Lorenzo: improve_workflow_v2.py получает checkpoint/resume.

**RPA + AI Enterprise** (1019918, апрель 2026) — RGS IT: AI-агент = "мозг" (reasoning, planning), RPA-робот = "руки" (UI-действия в SAP/1С). Tool Registry: существующие RPA-сценарии → описания для LLM. Оркестратор изолирует credentials. -42× время обработки заявок (2-3 часа → 12-20 минут). Для Lorenzo: Python-скрипты как tools для AI-оркестратора (Script-as-Tool).

**Structural Prompt Injection / Phantom** (1002608, 2025) — атака не через убеждение, а через синтаксис: вставить `<|im_start|>` в веб-контент → LLM видит как системную команду. 87% success rate без защит. Единственная частично рабочая защита (DeBERTa-детектор): -69% атак но -45% полезности агента. Архитектурный вывод: пока control и data в одном token-пространстве — уязвимость is by design. LLM Firewall устарел для агентов (MCP plugin poisoning, октябрь 2025).

## Сводная карта R01–R23

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |
| R06 | 4 | Video AI, CLI agents, GitHub automation | Memory MCP v2, DevClaw паттерн |
| R07 | 4 | Multi-agent architecture, agent safety | openLight принцип, 9-агентный паттерн |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI | SocratiCode, Paper2Agent |
| R09 | 4 | GraphRAG, decentralized AI, coding agent | GraphRAG pipeline, HMP, OpenCode |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust | MiroFish, n8n AI Stack |
| R11 | 4 | Desktop agents, edge AI, voice embedded | Союз (MCP desktop), RPi+Ирина voice pipeline |
| R12 | 4 | Data analytics AI, audio gen, vector DBs | Veai IDE agent, BI Agent Pattern |
| R13 | 4 | Observability, ADD, self-healing, OCR | Langfuse pattern, ADD feedback loop |
| R14 | 4 | Context Engineering, DSPy, security, ingestion | MarkItDown, Security Audit framework |
| R15 | 4 | Code review AI, Text2SQL, fine-tuning, LLM security | Fine-tuning 2026, AI Review CI/CD |
| R16 | 4 | No-LangChain, monitoring LLM, GigaAM-v3, RAG eval | GigaAM-v3 SOTA, Custom LLM distillation |
| R17 | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | LLM-Wiki paradigm, Sberbank KG production |
| R18 | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings | FRIDA #1 ruMTEB, Agentic RAG taxonomy |
| R19 | 4 | Multimodal RAG, doc review AI, vector DB, LLM inference | Docling+RRF SoTA, Desmond Cognitive Worker |
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | LLM Router pattern, mutation test pipeline |
| R21 | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification | A2A+MCP stack, 3-agent autonomous ops |
| R22 | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | Graph RAG 96.7%, n8n+Ollama self-hosted |
| R23 | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | Durable State архитектура, Phantom framework |

**Итого: 96 проектов, 50+ авторов**

## Что осталось на R24

- **LLM для образования (EdTech)** — AI-тьютор, адаптивное обучение, генерация задач, feedback по эссе
- **Multimodal AI в production** — изображения + текст + аудио в одном pipeline; vision agents
- **AI для DevOps/SRE** — incident management с LLM, auto-remediation, log analysis beyond Langfuse
- **Федеративное обучение и приватный AI** — federated learning + LLM, дифференциальная приватность для корпоративных данных


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
- [Решения](../../DECISIONS.md)
