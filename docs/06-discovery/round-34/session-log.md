---
date: 2026-05-28
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 34 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> LLM для телеком и сети — анализ сетевого трафика через LLM, AI для сетевых операций (NetOps), автоматизация настройки оборудования
2.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** LLM DevSecOps, Multimodal doc processing v2, LLM evaluation/бенчмаркинг, Edge AI  
**Проектов найдено:** 4  
**Авторов:** 4 новых

## Найденные проекты

| # | Проект | Автор | Слой | Хабр |
|---|--------|-------|------|------|
| 1 | ai-review: локальный LLM в CI/CD | sound_right (Никита Филонов) | orchestration / cicd | 953598 |
| 2 | PDF pipeline: Marker + PaperMage + Unstructured | MaxRokatansky / OTUS | ingestion | 835930 |
| 3 | Multilingual MT-Bench (ru_mt_bench) | ruslandevlabs | analytics | 834158 |
| 4 | LLM на Raspberry Pi 5: Edge inference | Denbackyard / Cloud.ru | orchestration / edge | 964136 |

## Детали поиска

### Тема 1: LLM DevSecOps / Security Code Review
- **Запрос:** LLM code review безопасность CI/CD локальный
- **Выбранная статья:** https://habr.com/ru/articles/953598/ (октябрь 2025)
- **GitHub:** https://github.com/Nikita-Filonov/ai-review + https://github.com/Nikita-Filonov/test-ai-review
- **Уникальность:** Полностью локальный AI code review (Ollama в GitHub Actions runner), без передачи кода внешним API; benchmark 5 моделей (mistral/codellama/phi3/llama3/deepseek-coder); < 30 минут настройка
- **Другие кандидаты:** 1031718 (Solar Security DerAI, SAST fine-tuned), 1017858 (opensophy, DevSecOps pipeline с Claude)

### Тема 2: Multimodal Document Processing v2
- **Запрос:** PDF парсинг LayoutLMv3 Table Transformer мультимодальный
- **Выбранная статья:** https://habr.com/ru/companies/otus/articles/835930/ (август 2024)
- **GitHub:** marker (VikParuchuri), papermage (AllenAI), unstructured (Unstructured-IO)
- **Уникальность:** Практическое сравнение трёх pipeline с разными моделями: LayoutLMv3+Texify (Marker), Table Transformer DETR/PubTables-1M (Unstructured), YOLOX+IVILA (PaperMage); выводы по трейдоффам скорость/качество для разных типов документов
- **Другие кандидаты:** 1008610 (OCR → ADE, LayoutLM+LandingAI DPT, март 2026, нет standalone repo)

### Тема 3: LLM Evaluation и бенчмаркинг
- **Запрос:** MT-Bench русский язык LLM оценка бенчмарк
- **Выбранная статья:** https://habr.com/ru/articles/834158/ (август 2024)
- **GitHub:** https://github.com/Peter-Devine/multilingual_mt_bench
- **Уникальность:** Первая русскоязычная адаптация MT-Bench (80 вопросов, 8 категорий); LLM-as-judge pipeline (GPT-4 судья); drop-in совместимость с FastChat/LM-SYS; результаты для GigaChat/Saiga/YandexGPT vs GPT-4o/Claude
- **Другие кандидаты:** 970744 (LLM Judge кросс-модельный CLEV алгоритм, нет GitHub)

### Тема 4: Edge AI и мобильные LLM
- **Запрос:** LLM Raspberry Pi квантизация edge inference GGUF
- **Выбранная статья:** https://habr.com/ru/companies/cloud_ru/articles/964136/ (ноябрь 2025)
- **Уникальность:** Реальные TTFT/TPS замеры 5 моделей на Pi 5; сравнение GGUF квантизации q2/q4/q5/q8; гибридная архитектура Pi+Cloud (routing по сложности запроса); Open WebUI интеграция

## Cumulative Table R01–R34

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
| R34 | LLM DevSecOps, Multimodal doc v2, LLM evaluation, Edge AI | 4 |
| **Итого** | | **140** |

## Темы для Round 35

1. **LLM для телеком и сети** — анализ сетевого трафика через LLM, AI для сетевых операций (NetOps), автоматизация настройки оборудования
2. **Персонализация и рекомендательные системы с LLM** — LLM-powered рекомендации, user profiling через embeddings, cold-start problem
3. **AI для образования v2** — адаптивное обучение с LLM, автоматизированная генерация тестов, AI-тьютор с памятью студента
4. **Оркестрация и planning LLM агентов** — ReAct/CoT planning, tool use optimization, long-horizon task decomposition, agent debugging

## Новые авторы раунда

| Автор | Проект | Контакт |
|-------|--------|---------|
| sound_right (Никита Филонов) | ai-review | github.com/Nikita-Filonov |
| MaxRokatansky | PDF Pipeline comparison | otus.ru |
| ruslandevlabs | Multilingual MT-Bench | habr.com/ru/users/ruslandevlabs |
| Denbackyard | LLM on Raspberry Pi | cloud.ru |


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
