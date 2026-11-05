---
date: 2026-06-05
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Round 20 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Reasoning-LLM (Selectel, 892600, март 2025) — первый RU-разбор архитектуры thinking models: MLA, closed vs open thinking (o1 vs R1), дистилляция traces.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** LLM unit test generation (VK/OK), DeepSeek V3→V3.2, Reasoning-LLM архитектура (Selectel), LLM Compute Economics 2026

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Генерация юнит-тестов с LLM: пайплайн Одноклассников | VK / Одноклассники | orchestration / quality | `projects/llm-unit-test-generation-vk.md` |
| DeepSeek V3→V3.2 — технический обзор | независимый ML-исследователь | knowledge / orchestration | `projects/deepseek-v3-technical-overview.md` |
| Reasoning-LLM: архитектура думающих моделей | Selectel | orchestration / knowledge | `projects/reasoning-llm-architecture.md` |
| LLM Compute Economics 2026 — когда какую модель | независимый аналитик | orchestration / analytics | `projects/llm-compute-economics-2026.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| LLM Router (Economics + Reasoning + DeepSeek) | весь стек | 3-уровневый роутинг: Haiku(bulk) → Sonnet(standard) → Opus(complex) → local(offline) | ⭐⭐⭐⭐⭐ |
| Unit Tests + AI Review (R15) | CI/CD pipeline | авто-тест generation → mutation filter → авто-ревью = полный quality gate | ⭐⭐⭐⭐⭐ |
| DeepSeek /no_think + improve_llm_enrich | bulk обогащение | в 10-100× дешевле Claude при 85-90% качества для форматирования | ⭐⭐⭐⭐ |
| Reasoning + CoT Illusion (R17) | prompt strategy | R17 доказал: CoT вредит простым задачам → Reasoning только для сложных | ⭐⭐⭐⭐ |
| R1 Distillation + Synthetic Data (R18) | knowledge transfer | DeepSeek R1 traces → Distilabel → QLoRA fine-tune = reasoning в 7B | ⭐⭐⭐⭐ |

## Главные находки раунда

**LLM Unit Test Generation** (VK/Одноклассники, 921410, июнь 2025) — multi-level pipeline с мутационным тестированием как ключевым фильтром. Без мутационного теста LLM-тесты повышают coverage, но не качество. Реальные числа: +20% coverage, ~60% сгенерированных тестов отфильтровано как бесполезные. Прямое применение к Lorenzo: 159 скриптов без тестов → `improve_test_gen.py` + pytest-mutagen.

**DeepSeek V3.2** (973954, апрель 2026) — MIT-лицензия, технически на уровне GPT-5 по бенчмаркам, DSA (Sparse Attention) для длинного контекста. Ключевое: `/no_think` токен = быстрый ответ без reasoning overhead. OpenAI-совместимое API — прямая замена в Lorenzo за 10-20× меньше стоимости для bulk операций.

**Reasoning-LLM** (Selectel, 892600, март 2025) — первый RU-разбор архитектуры thinking models: MLA, closed vs open thinking (o1 vs R1), дистилляция traces. Практический фреймворк: reasoning оправдан если P(ошибка) × стоимость_ошибки > стоимость_reasoning. Для Lorenzo: только `improve_llm_qa.py` на сложных вопросах.

**LLM Compute Economics** (1024850, 2026) — «compute crunch»: reasoning inference в 10-50× тяжелее обычного. Матрица выбора 15+ сценариев: Haiku для форматирования ($0.25/M), DeepSeek для синтетики ($0.27/M), Opus только для критичных задач ($15-75/M). Паттерн LLM Router — экономия ~85% при правильном routing.

## Сводная карта R01–R20

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
| R19 | 4 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference | Docling+RRF SoTA, Desmond Cognitive Worker |
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | LLM Router pattern, mutation test pipeline |

**Итого: 84 проекта, 44+ авторов**

## Что осталось на R21

- **LLM для NLP-задач на русском** — NER, IE, классификация текста через LLM + fine-tuning, русские бенчмарки 2025-2026
- **AI для product analytics** — LLM-анализ пользовательского поведения, cohort analysis через SQL-агент
- **Multi-agent orchestration паттерны** — production кейсы: как координировать 5+ агентов без LangChain
- **Privacy-preserving AI** — federated learning, differential privacy для LLM, локальные модели для конфиденциальных данных


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
