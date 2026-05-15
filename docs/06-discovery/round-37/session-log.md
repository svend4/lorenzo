---
date: 2026-05-15
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 37 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Темы: LLM медиа, AI безопасность v2, LLM IoT/промышленность, LLM calibration/галлюцинации
Темы: LLM медиа, AI безопасность v2, LLM IoT/промышленность, LLM calibration/галлюцинации  
Статус: ✅ Завершён
Что искали
1.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Темы:** LLM медиа, AI безопасность v2, LLM IoT/промышленность, LLM calibration/галлюцинации  
**Статус:** ✅ Завершён

## Что искали

1. **LLM медиа и контент-генерация** — автоматизация рерайтинга, стилевая адаптация для СМИ
2. **Безопасность AI-систем v2** — on-premise LLM защита, атаки и детекция без облака
3. **LLM для IoT и промышленности** — управление физическими устройствами через LLM/MCP
4. **Оценка и calibration LLM** — детекция галлюцинаций мультимодальных моделей

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R37-1 | Rewrite Factory: стилевая декомпозиция | vaganovelena | orchestration/analytics | [1002228](https://habr.com/ru/articles/1002228/) | — |
| R37-2 | AISecurity: иммунная система для LLM | Dmitriila | orchestration/security | [996896](https://habr.com/ru/articles/996896/) | [DmitrL-dev/AISecurity](https://github.com/DmitrL-dev/AISecurity) |
| R37-3 | IoT-MCP: управление устройствами через LLM | — | orchestration | [953648](https://habr.com/ru/articles/953648/) | [poly-mcp/IoT-Edge-MCP-Server](https://github.com/poly-mcp/IoT-Edge-MCP-Server) |
| R37-4 | CV Guard: детекция галлюцинаций VLM | Bahama_Papa | analytics | [1007788](https://habr.com/ru/articles/1007788/) | — |

## Ключевые находки

### Rewrite Factory (vaganovelena)
- Декомпозиция редакционного голоса на 5 независимых компонентов: структура/тон/лексика/заголовки/эмоциональный регистр
- Осознанный отказ от RAG: семантика ищет по теме, не по стилю; chunking разрушает editorial voice
- Тег-based selection + Handlebars templating
- Производство: >90% экономии времени редактора, 60-70% принимаются без правок

### AISecurity / Иммунная система (Dmitriila)
- Трёхслойная архитектура: 36K строк C shield + 49 Rust super-engines (PyO3) + Micro-Model Swarm (<2000 параметров)
- F1=0.997 при <3ms на CPU, on-premise, данные не покидают сервер
- 87,056 реальных паттернов атак из jailbreak.chat, PromptHub, OWASP LLM Top 10
- Vs Lakera Guard: F1 0.997 vs 0.991, latency 2.8ms vs 67ms

### IoT-MCP (poly-mcp)
- Трёхуровневая архитектура: Local Host (LLM+MCP) / Datapool & Connection Server / IoT Devices
- JSON instruction protocol: command/duration/interval
- Datapool: UUID идемпотентность, буферизация при обрыве, параллельные команды
- IoT-MCP Bench: 114 базовых задач + 1,140 вариаций; Claude-3.5-Sonnet лучший (overall 0.87)

### CV Guard for LLM Hallucinations (Bahama_Papa)
- Трёхуровневый pipeline: LLM параллельно с CV → Guard V1 → Guard V2
- Guard V1: YOLO bounding boxes + Canny/Hough Transform (горизонт) + гистограмма (экспозиция) + Laplacian variance (резкость)
- Guard V2: паттерн-матчинг текстовых утверждений LLM к CV измерениям
- Результаты: ~70% детекция пространственных галлюцинаций, <100ms, $6-10/месяц

## Collab Finder результаты

- **Rewrite Factory** → Rufler [0.451], Yodoca [0.435], Wikontic [0.227]
- **AISecurity** → NGT Memory [0.400]
- **IoT-MCP** → Wikontic [0.400]
- **CV Guard** → нет результатов (новая ниша)

## Запросы поиска

- `habr.com LLM рерайтинг стиль СМИ автоматизация 2025`
- `habr.com LLM безопасность защита prompt injection on-premise 2025 Rust C`
- `habr.com IoT LLM управление устройствами MCP MQTT 2025`
- `habr.com LLM галлюцинации детекция верификация мультимодальный 2025`

## Накопленная таблица раундов (R01–R37)

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
| **Итого** | **152** | **37 раундов** |

## Темы для Round 38

1. **LLM для медицины v2** — клинические NLP задачи, медицинские агенты, анализ медкарт
2. **Multiagent coordination patterns** — протоколы координации, конфликт-резолюция, голосование агентов
3. **LLM observability и tracing** — production мониторинг LLM цепочек, distributed tracing, cost attribution
4. **Retrieval-Augmented Generation v3** — поздние интеграции, hybrid dense+sparse, adaptive chunking в prod


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```
