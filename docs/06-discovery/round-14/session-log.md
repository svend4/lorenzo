---
date: 2026-05-29
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 14 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> OSS: CLAUDE.md + 12 MCP + skills | ⭐⭐⭐⭐ | MarkItDown + OCR Guide (R13) | Qwen3 VL | MarkItDown (структура) + VLM (сложные элементы) = полный doc ingestion pipeline | ⭐⭐⭐⭐ |
 MarkItDown + OCR Guide (R13) | Qwen3 VL | MarkItDown (структура) + VLM (сложные элементы) = полный doc ingestion pipeline | ⭐⭐⭐⭐ |
Главные находки раунда
Context Engineering (1028260) — манифест 2026 года: в


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** Context Engineering, DSPy (алгоритмическая оптимизация промптов), безопасность AI-агентов, MarkItDown (универсальный doc→Markdown конвертер)

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Context Engineering | независимый исследователь | orchestration / methodology / 2026 | `projects/context-engineering.md` |
| DSPy | Stanford NLP (Omar Khattab) | optimization / prompting / quality | `projects/dspy-prompt-optimizer.md` |
| AI Agent Security Audit | Дмитрий Лабинцев + bgauryy | security / governance / quality | `projects/ai-agent-security-audit.md` |
| MarkItDown | Microsoft OSS | ingestion / document-AI / preprocessing | `projects/markitdown.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| MarkItDown + improve_chunk_semantic | Lorenzo ingestion | PDF/DOCX/PPTX → Markdown → chunks → corpus = внешние статьи в Lorenzo | ⭐⭐⭐⭐⭐ |
| Security Audit + openLight (R07) | openLight принцип | openLight = практическое воплощение 5-фазного аудита: только whitelist tools | ⭐⭐⭐⭐⭐ |
| DSPy + improve_llm_enrich | Stage 3 LLM | Автооптимизация промптов обогащения карточек: больше качества, те же токены | ⭐⭐⭐⭐ |
| Context Engineering + Lorenzo | весь стек | Lorenzo — лучший пример Context Engineering в рус. OSS: CLAUDE.md + 12 MCP + skills | ⭐⭐⭐⭐ |
| MarkItDown + OCR Guide (R13) | Qwen3 VL | MarkItDown (структура) + VLM (сложные элементы) = полный doc ingestion pipeline | ⭐⭐⭐⭐ |

## Главные находки раунда

**Context Engineering** (1028260) — манифест 2026 года: ваш промпт = 0.03% контекста. CLAUDE.md, MCP, memory, skills — вот настоящий контекст агента. Lorenzo — живой пример Context Engineering. Статья даёт теоретическую рамку для архитектуры Svyazi 2.0.

**DSPy** (github.com/stanfordnlp/dspy, MIT, 22k+ stars) — Stanford фреймворк: промпт = параметр, который компилятор оптимизирует автоматически. MIPROv2 и BootstrapFewShot выбирают лучшие инструкции и few-shot примеры. Применимо к `improve_llm_enrich.py` + `improve_llm_qa.py`.

**AI Agent Security Audit** (989764, github.com/doneyli/ai-agent-security-audit) — первый code-verified аудит открытого агента: 18 уязвимостей, 26% из 31k skills содержат уязвимость. 5-фазный фреймворк применим к 12 MCP-серверам Lorenzo. openLight (R07) закрывает ключевую уязвимость — eval() без sandbox.

**MarkItDown** (github.com/microsoft/markitdown, MIT, 91k stars) — де-факто стандарт doc→Markdown конвертации. PDF, DOCX, PPTX, XLSX, изображения → структурированный Markdown. Прямое применение: ingestion внешних Хабр-статей в Lorenzo corpus без ручного копирования.

## Сводная карта R01–R14

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

**Итого: 60 проектов, 32+ авторов**

## Что осталось на R15

- **AI для работы с таблицами и SQL** — Text-to-SQL агенты, pandas-agent, SQL-code gen (не архитектурный паттерн как в R12 BI, а конкретные open-source реализации)
- **Streaming и real-time агенты** — агенты с потоковой обработкой данных (Kafka + LLM, stream reasoning)
- **AI code review 2.0** — глубокий анализ кода (не просто ревью, а понимание архитектурных паттернов)
- **Персонализированные LLM** — fine-tuning на личных данных, приватное дообучение


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
