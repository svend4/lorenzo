---
date: 2026-05-29
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 39 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Темы: LLM юридическая автоматизация v2, synthetic data generation, LLM персонализация v2, AI-assisted testing v2
Темы: LLM юридическая автоматизация v2, synthetic data generation, LLM персонализация v2, AI-assisted testing v2  
Статус: ✅ Завершён
Что искали
1.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** LLM юридическая автоматизация v2, synthetic data generation, LLM персонализация v2, AI-assisted testing v2  
**Статус:** ✅ Завершён

## Что искали

1. **LLM юридическая автоматизация v2** — генерация договоров, анализ рисков, compliance проверка
2. **Synthetic data generation** — дистилляция агентских трейсов, data augmentation без разметки
3. **LLM персонализация v2** — долгосрочные пользовательские профили, adaptive prompting, 5-слойная память
4. **AI-assisted testing v2** — LLM + мутационное тестирование, 6-gate pipeline

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R39-1 | Contract Risk Analysis: Schema Guided Reasoning | favioes | analytics/orchestration | [1005144](https://habr.com/ru/articles/1005144/) | — |
| R39-2 | Agent Trace Distillation: DevOps-LLM без разметки | makarsuperstar | analytics/orchestration | [1033434](https://habr.com/ru/articles/1033434/) | — |
| R39-3 | 5-Layer Memory: персонализация через pgvector | Svetafo | memory/orchestration | [1007940](https://habr.com/ru/articles/1007940/) | — |
| R39-4 | Agent Driven Testing: LLM + Stryker4s мутации | rurikovich | orchestration | [1010148](https://habr.com/ru/articles/1010148/) | — |

## Ключевые находки

### Contract Risk Analysis (favioes)
- Schema Guided Reasoning: CoT reasoning_effort=medium + типизированная JSON-схема → детерминированный вывод
- Preprocessing: восстановление визуальной нумерации из Word docx `numbering.xml` abstract numbering maps
- RapidFuzz fuzzy-matching для нечёткого поиска пунктов
- Стек: FastAPI + Celery + Redis + SQLAlchemy + xlsxwriter; 1000+ договоров/год

### Agent Trace Distillation (makarsuperstar)
- Учитель Gemma4:31b (avg_score 92.0) vs DeepSeek-Coder-v2 (72.7), Qwen3.6:27b — Gemma победила
- 8-метричный взвешенный валидатор (порог 84.8/100) фильтрует ~24% примеров
- Domain mismatch: Magicoder 38% on-topic vs GitHub трейсы 95% — acceptance rate не предсказывает on-topic
- Итог: 3899 валидных трейсов, oni:base-clean.v2 → 10/10 на боевых тестах без галлюцинаций

### 5-Layer Memory (Svetafo)
- Слои: сессионная → эпизодическая → семантическая → база знаний → синтезированные паттерны
- Memory Synthesizer: корреляция Спирмена (порог 0.65, p<0.05) для скрытых поведенческих паттернов
- Политики промоции между слоями с условиями (access_count, age_days, confidence)
- Стек: PostgreSQL 16 + pgvector, FastAPI, aiogram 3, n8n, Claude Haiku + GPT-4o-mini

### Agent Driven Testing / Stryker (rurikovich)
- 6-gate pipeline: компиляция → зелёные тесты → стабильность → мутации → smell → LLM ревью
- Дифференцированные пороги Stryker4s: pure functions 50%, business services 40%, I/O 30%
- Двухагентная архитектура: Writer Agent + Reviewer Agent (12-пунктный чеклист)
- 68 файлов сгенерировано, 86.8% принято; branch coverage +6%; экономия токенов 30–50%

## Collab Finder результаты

- **Contract Risk SGR** → Wikontic [0.400]
- **Agent Trace Distillation** → нет результатов (новая ниша)
- **5-Layer Memory** → Wikontic [0.459], Yodoca [0.435], agent-memory-mcp [0.417], NGT Memory [0.333]
- **Agent Testing Stryker** → agent-memory-mcp [0.417], NGT Memory [0.288], Rufler [0.246], mclaude [0.240]

## Запросы поиска

- `habr.com LLM юридический договор контракт автоматизация 2025`
- `habr.com синтетические данные LLM обучение генерация 2025`
- `habr.com LLM персонализация пользователь профиль 2025`
- `habr.com LLM тестирование тест-кейсы генерация 2025`

## Накопленная таблица раундов (R01–R39)

| Раунд | Проектов | Ключевая тема |
|-------|----------|---------------|
| R01 | 9 | Memory + Knowledge |
| R02 | 6 | Voice, parsing, YAML |
| R03 | 3 | Code review, fine-tuned LLM |
| R04 | 3 | Agent platform, MCP protocol |
| R05 | 3 | Autonomous pipeline, Russian NLP |
| R06 | 4 | Video AI, CLI agents, GitHub automation |
| R07 | 4 | Multi-agent arch, agent safety, MCP pipeline |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI |
| R09 | 4 | GraphRAG, decentralized AI, coding agent |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust |
| R11 | 4 | Desktop agents, edge AI, voice embedded |
| R12 | 4 | Data analytics AI, audio gen, vector DBs |
| R13 | 4 | Observability, ADD, self-healing tests, OCR |
| R14 | 4 | Context Engineering, DSPy, AI security, MarkItDown |
| R15 | 4 | Code review AI, Text2SQL, fine-tuning, LLM security |
| R16 | 4 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval |
| R17 | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA |
| R18 | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings |
| R19 | 4 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference |
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics |
| R21 | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification |
| R22 | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod |
| R23 | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection |
| R24 | 4 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек |
| R25 | 4 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование |
| R26 | 4 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт |
| R27 | 4 | LLM кибербезопасность, персональный AI с памятью, 5-фазный оркестратор, RAG тесты |
| R28 | 4 | Volga streaming ML, мультимодальный VLM Сбер, LLM Judge кросс-модельный, Federated edge |
| R29 | 4 | Comprehension debt, Text2SQL X5, AI мета-мониторинг, Кириллица в LLM |
| R30 | 4 | Coreness Flow composable, VLM vs IDP бенчмарк, синтетика граф-качество, HITL prod |
| R31 | 4 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic |
| R32 | 4 | Enterprise RAG (МТС), vLLM inference opt, FinPDF pipeline, Авито VLM |
| R33 | 4 | AI code agents v2, LLM data engineering, суверенный AI, red-teaming |
| R34 | 4 | LLM DevSecOps, Multimodal doc v2, LLM evaluation, Edge AI |
| R35 | 4 | LLM телеком, персонализация, AI образование v2, agent planning |
| R36 | 4 | LLM финансовый compliance, continuous adaptation, логистика AI, LLM для науки |
| R37 | 4 | LLM медиа, AI безопасность v2, LLM IoT/промышленность, LLM calibration |
| R38 | 4 | LLM медицина v2, multiagent coordination, LLM observability, RAG v3 |
| R39 | 4 | LLM юридическая авт. v2, synthetic data, персонализация v2, AI testing v2 |
| **Итого** | **160** | **39 раундов** |

## Темы для Round 40

1. **LLM для строительства и инфраструктуры** — анализ проектной документации, BIM, строительные нормы
2. **Structured output и function calling v2** — надёжный structured output, валидация, retry стратегии
3. **LLM для образования v3** — персонализированные учебные планы, адаптивное тестирование
4. **AI для кибербезопасности v2** — LLM для SIEM, threat hunting, автоматический анализ инцидентов


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```
