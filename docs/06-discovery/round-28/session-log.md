---
date: 2026-05-15
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 28 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Мультимодальные LLM — видят, слышат и понимают (Сбер AI) Хабр: https://habr.com/ru/companies/oleg-bunin/articles/914848/
 Файл:  
 Хабр: https://habr.com/ru/companies/oleg-bunin/articles/914848/
 Слой: orchestration / ingestion / analytics
 Уникальность: Production-интервью с руководителем ML Сбер: три модальност


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** Streaming/real-time AI, Multimodal Agent, LLM Evaluation, Federated AI  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Темы из R27 session-log:
1. **Streaming/real-time AI** — потоковая обработка с ML, feature stores, point-in-time correctness
2. **Multimodal Agent** — три модальности (текст + изображения + аудио) в production
3. **LLM Evaluation** — LLM-as-judge, self-preference bias, кросс-модельная оценка
4. **Federated AI** — федеративное обучение без передачи данных, edge устройства

## Найденные проекты

### 1. Volga — Rust stream processing engine для ML/AI
- **Файл:** `projects/volga-realtime-ml-stream-engine.md`
- **Хабр:** https://habr.com/ru/articles/1021290/
- **Слой:** orchestration / analytics / ingestion
- **Уникальность:** Rust-движок распределённой потоковой обработки, специально для ML feature computation. Apache Arrow + DataFusion. Три режима: streaming/batch/request. Point-in-time correct window aggregations — нет data leakage при обучении. Альтернатива Spark/Flink с ML-first API. State через SlateDB (LSM поверх S3).
- **Дата:** апрель 2025

### 2. Мультимодальные LLM — видят, слышат и понимают (Сбер AI)
- **Файл:** `projects/multimodal-llm-vision-audio-text.md`
- **Хабр:** https://habr.com/ru/companies/oleg-bunin/articles/914848/
- **Слой:** orchestration / ingestion / analytics
- **Уникальность:** Production-интервью с руководителем ML Сбер: три модальности в едином VLM. AGE-VLM alternating attention снижает галлюцинации на 23%. Реальные кейсы: документооборот (OCR→VLM), медицина (PACS+аудио+ЭМК), реклама (изображение+контекст страницы). Практика масштабирования на GPU.
- **Дата:** июнь 2025

### 3. LLM Judge — кросс-модельная оценка, $0.014/курс
- **Файл:** `projects/llm-judge-cross-model-evaluation.md`
- **Хабр:** https://habr.com/ru/articles/970744/
- **Слой:** orchestration / analytics
- **Уникальность:** Открытие: LLM статистически предпочитают outputs своего семейства (low-perplexity preference). Решение: кросс-модельная оценка. Двухстадийная валидация: Specification Check + Faithfulness Hallucination. Map-Reduce-Refine экономит 17 000× стоимость ($240 → $0.014 за курс).
- **Дата:** ноябрь 2025

### 4. Федеративное обучение на edge с памятью < 256 МБ (Eltex)
- **Файл:** `projects/federated-learning-edge-devices.md`
- **Хабр:** https://habr.com/ru/companies/oleg-bunin/articles/1009670/ (ч.1), 1009674 (ч.2)
- **Слой:** orchestration / memory
- **Уникальность:** Реальная платформа FL от инженера Eltex: Flower + TF Federated (цифровые двойники) + LiteRT. ~60% экономия памяти через gradient checkpointing, micro-batching, int8 QAT, layer freezing. Secure aggregation с дифференциальной приватностью. Данные не покидают устройство.
- **Дата:** апрель–май 2026

## Поиск аналогий в Lorenzo (collab_finder)

```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-28/projects/volga-realtime-ml-stream-engine.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-28/projects/multimodal-llm-vision-audio-text.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-28/projects/llm-judge-cross-model-evaluation.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-28/projects/federated-learning-edge-devices.md --top 4
```

Результаты → `docs/COLLAB_SUGGESTIONS.md`

Топ совпадений:
- Volga → Svyazi, Yodoca
- Multimodal → Svyazi
- LLM Judge → Svyazi, Yodoca
- Federated → Svyazi, Yodoca

## Кумулятивная карта (R01–R28)

| Раунд | Тема | Ключевые проекты |
|-------|------|-----------------|
| R01 | Memory + Knowledge | AgentFS, MemNet, NGT Memory, Yodoca, knowledge-space, mclaude |
| R02 | Voice, parsing, YAML | голосовые интерфейсы, парсинг, Rufler YAML |
| R03 | Code review, fine-tuned LLM | code review AI, специализированные LLM |
| R04 | Agent platform, MCP protocol | агентные платформы, MCP-протокол |
| R05 | Autonomous pipeline, Russian NLP | автономные пайплайны, RU NLP |
| R06 | Video AI, CLI agents, GitHub automation | видео AI, CLI агенты |
| R07 | Multi-agent arch, agent safety, MCP pipeline | мультиагентные системы |
| R08 | Codebase MCP, scientific ingestion, edu AI | инструменты разработчика |
| R09 | GraphRAG, decentralized AI, coding agent | GraphRAG, децентрализованный AI |
| R10 | Viral simulation, self-hosted stacks, Rust | self-hosted, производительность |
| R11 | Desktop agents, edge AI, voice embedded | edge AI, встроенные системы |
| R12 | Data analytics AI, audio gen, vector DBs | аналитика данных, векторные БД |
| R13 | Observability, ADD, self-healing tests, OCR | наблюдаемость, тесты, OCR |
| R14 | Context Engineering, DSPy, AI security, MarkItDown | контекст, безопасность |
| R15 | Code review AI, Text2SQL, fine-tuning, LLM security | код ревью, SQL, файнтюн |
| R16 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval | мониторинг LLM, ASR |
| R17 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | CoT, граф знаний, DBA |
| R18 | Agentic RAG, synthetic data, incident AI, RU embeddings | RAG, синтетика, FRIDA |
| R19 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference | мультимодальный RAG |
| R20 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | тесты, reasoning |
| R21 | Multi-agent case, A2A protocol, LLM privacy, RU classification | A2A, приватность |
| R22 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | legal tech, безопасность |
| R23 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | enterprise AI, безопасность |
| R24 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | производственные системы |
| R25 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование | отраслевые решения |
| R26 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт | BI/аналитика, финтех |
| R27 | LLM кибербезопасность, персональный AI, 5-фазный оркестратор, RAG тесты | безопасность, DevEx |
| R28 | Volga streaming ML, мультимодальный VLM, LLM Judge, federated edge | infrastructure, качество |

**Итого:** 116 проектов, 60+ авторов

## Темы для Round 29

1. **Code generation качество** — AI генерирует код, но насколько качественный: статический анализ сгенерированного кода, паттерны технического долга в AI-коде, security в сгенерированном коде
2. **LLM для баз данных** — AI-помощник DBA: автооптимизация запросов, обнаружение деградации производительности, NL2SQL второго поколения (самопроверяющийся)
3. **Агентные системы мониторинга** — AI наблюдает за AI: meta-monitoring, агент который следит за другими агентами, drift detection в продакшн
4. **Локализация и RU-специфика LLM** — особенности русского языка в LLM: морфология, ять-структуры, кириллические токены, RU-бенчмарки 2026

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
