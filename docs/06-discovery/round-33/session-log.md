---
date: 2026-06-05
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 33 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> LLM evaluation и бенчмаркинг — OpenEvals, MT-Bench адаптации для RU, автоматический harness, judge calibration
4.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** AI code agents v2, LLM data engineering, суверенный AI, red-teaming  
**Проектов найдено:** 4  
**Авторов:** 4 новых

## Найденные проекты

| # | Проект | Автор | Слой | Хабр |
|---|--------|-------|------|------|
| 1 | Cursor Multi-Agent Orchestrator | rdudov | orchestration | 971620 |
| 2 | Just AI LLM Data Quality Pipeline | Арина Макунина / Just AI | orchestration / analytics | 1011428 |
| 3 | YADRO Sovereign LLM Inference Cluster | jet-47 / YADRO | orchestration | 930304 |
| 4 | LLAMATOR Red Teaming LLM (Russian) | nizamovtimur / ITMO | analytics / orchestration | 851640 |

## Детали поиска

### Тема 1: AI Code Agents v2 (Cursor Multi-Agent)
- **Запрос:** мультиагентная разработка cursor субагенты оркестратор
- **Статья:** https://habr.com/ru/articles/971620/ (ноябрь 2025)
- **GitHub:** https://github.com/rdudov/agents
- **Уникальность:** Практическая оркестрация без нативной поддержки мультиагентов в Cursor: 5 ролей (analyst/architect/planner/developer/reviewer) через cursor-agent CLI; маршрутизация Opus 4.5 → Composer-1; top-down skeleton-first стратегия

### Тема 2: LLM Data Engineering / Data Quality
- **Запрос:** LLM data quality автоматизация правил диагностика инцидентов
- **Статья:** https://habr.com/ru/companies/just_ai/articles/1011428/ (апрель 2026)
- **Уникальность:** Трёхуровневая архитектура DQ+LLM без прямого доступа к БД; "verifiable artifacts only" принцип; Zero-Shot генерация YAML-правил + автодиагностика инцидентов; Caila gateway; Claude Sonnet 4

### Тема 3: Суверенный AI / On-Premise LLM Inference
- **Запрос:** суверенный LLM инференс кластер on-premise vLLM
- **Статья:** https://habr.com/ru/companies/yadro/articles/930304/ (июль 2025)
- **Уникальность:** Честный production-отчёт от российского производителя: RTX 4090 + H100, три итерации стека (Triton → vLLM+LiteLLM → vLLM Production Stack), T-pro-it-1.0 vs глобальные модели, FP8 + tensor parallelism

### Тема 4: Red Teaming LLM (Russian)
- **Запрос:** red teaming LLM уязвимости prompt injection русский язык
- **Статья:** https://habr.com/ru/articles/851640/ (октябрь 2024)
- **GitHub:** https://github.com/RomiconEZ/LLaMator
- **Уникальность:** Единственный open-source red-teaming фреймворк с явной поддержкой русскоязычных LLM и RAG-систем; двухагентная архитектура (attacker + judge); 16 категорий атак включая кириллические obfuscation техники; Excel audit reports для ФСТЭК

## Cumulative Table R01–R33

| Раунд | Тема | Проектов |
|-------|------|----------|
| R01 | Memory + Knowledge | 9 |
| R02 | Voice, parsing, YAML | 6 |
| R03 | Code review, fine-tuned LLM | 3 |
| R04 | Agent platform, MCP protocol | 3 |
| R05 | Autonomous pipeline, Russian NLP | 3 |
| R06 | Video AI, CLI agents, GitHub automation | 4 |
| R07 | Multi-agent arch, agent safety, MCP pipeline | 4 |
| R08 | Codebase MCP, scientific ingestion, edu AI | 4 |
| R09 | GraphRAG, decentralized AI, coding agent | 4 |
| R10 | Viral simulation, self-hosted stacks, Rust | 4 |
| R11 | Desktop agents, edge AI, voice embedded | 4 |
| R12 | Data analytics AI, audio gen, vector DBs | 4 |
| R13 | Observability, ADD, self-healing tests, OCR | 4 |
| R14 | Context Engineering, DSPy, AI security, MarkItDown | 4 |
| R15 | Code review AI, Text2SQL, fine-tuning, LLM security | 4 |
| R16 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval | 4 |
| R17 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | 4 |
| R18 | Agentic RAG, synthetic data, incident AI, RU embeddings | 4 |
| R19 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference | 4 |
| R20 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | 4 |
| R21 | Multi-agent case, A2A protocol, LLM privacy, RU classification | 4 |
| R22 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | 4 |
| R23 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | 4 |
| R24 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | 4 |
| R25 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование | 4 |
| R26 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт | 4 |
| R27 | LLM кибербезопасность, персональный AI с памятью, 5-фазный оркестратор, RAG тесты | 4 |
| R28 | Volga streaming ML, мультимодальный VLM Сбер, LLM Judge кросс-модельный, Federated edge | 4 |
| R29 | Comprehension debt, Text2SQL X5, AI мета-мониторинг, Кириллица в LLM | 4 |
| R30 | Coreness Flow composable, VLM vs IDP бенчмарк, синтетика граф-качество, HITL prod | 4 |
| R31 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic | 4 |
| R32 | Enterprise RAG (МТС), vLLM inference opt, FinPDF pipeline, Авито VLM | 4 |
| R33 | AI code agents v2, LLM data engineering, суверенный AI, red-teaming | 4 |
| **Итого** | | **136** |

## Темы для Round 34

1. **LLM агенты для DevSecOps** — автоматический code review безопасности, SAST интеграция с LLM, уязвимости в IaC
2. **Multimodal document processing v2** — таблицы + формулы + чарты из PDF, LayoutLM для русских корп. документов
3. **LLM evaluation и бенчмаркинг** — OpenEvals, MT-Bench адаптации для RU, автоматический harness, judge calibration
4. **Edge AI и мобильные LLM** — TFLite/ONNX Runtime для мобильных, квантизация для Raspberry Pi, federated fine-tuning

## Новые авторы раунда

| Автор | Проект | Контакт |
|-------|--------|---------|
| rdudov | Cursor Multi-Agent | github.com/rdudov |
| Арина Макунина / Just AI | LLM Data Quality | just-ai.com |
| jet-47 / YADRO | Sovereign Inference | habr.com/companies/yadro |
| nizamovtimur | LLAMATOR | github.com/RomiconEZ |


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
