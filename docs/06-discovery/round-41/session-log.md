# Round 41 — Session Log

**Дата:** май 2026  
**Темы:** LLM агропромышленность, code generation v3 (SWE-bench), клиентский сервис v2, privacy-preserving LLM  
**Статус:** ✅ Завершён

## Что искали

1. **LLM для агропромышленности** — точное земледелие, прогноз урожая, анализ почвенных данных
2. **LLM code generation v3** — unit-тестируемый код, архитектурные паттерны, SWE-bench production
3. **LLM для клиентского сервиса v2** — многоканальный CRM, escalation detection, sentiment-driven routing
4. **Privacy-preserving LLM** — federated fine-tuning, differential privacy, on-device inference без передачи данных

## Найденные проекты

| № | Проект | Автор | Слой | Хабр | GitHub |
|---|--------|-------|------|------|--------|
| R41-1 | Jet Infosystems: 8-этапный ML pipeline прогноза урожая | JetHabr | analytics/orchestration | [761984](https://habr.com/ru/companies/jetinfosystems/articles/761984/) | — |
| R41-2 | SWE-MERA: динамический анти-контаминационный бенчмарк | madrugado (ODS) | analytics | [948184](https://habr.com/ru/companies/ods/articles/948184/) | [MERA-Evaluation/repotest](https://github.com/MERA-Evaluation/repotest) |
| R41-3 | Robovoice: LLM+RAG омниканальная поддержка | mmikeles (SL Soft) | orchestration | [877914](https://habr.com/ru/companies/slsoft/articles/877914/) | — |
| R41-4 | Privacy-LLM: PII-Gateway + On-Device RAG + WebGPU | MaximML | orchestration/analytics | [988774](https://habr.com/ru/articles/988774/) | — |

## Ключевые находки

### Jet Infosystems: ML в полях (JetHabr)
- Единственная на Хабре статья с реальным production ML-пайплайном для растениеводства российского агрохолдинга
- 8 этапов: Sentinel-2 NDVI + метеоданные + экспертные отчёты → Airflow → ML-прогноз готовности урожая → расписание объездов
- Гибрид: классические агрономические формулы (CAT, ГТК) + ML-коррекция; сезонное переобучение на актуальных данных
- Честная документация проблем: облачность над полями, редкость метеостанций, ошибки ввода; Grafana + ручные override
- Примечание: статья 2023 года — более свежих агро-LLM статей на Хабре нет

### SWE-MERA (madrugado, ODS)
- Динамический бенчмарк против temporal contamination: ~250 новых GitHub issues ежемесячно из активных репозиториев
- Верификация: тесты берутся из реального merged PR (не написаны вручную), должны падать до патча агента
- Первый публичный результат: DeepSeek-R1 27.8% pass@1, Qwen2.5-Coder-32B 12.9%, Llama-3.3-70B 8.7% (528 задач)
- Агент-фреймворк: Aider; GitHub: MERA-Evaluation/repotest + SWE-MERA-submissions; ArXiv: 2507.11059

### Robovoice / SL Soft (mmikeles)
- Production омниканальный бот с двухагентной маршрутизацией: rule-based FSM (FAQ, статусы) vs LLM+RAG (сложные)
- Dagster ETL + LangChain + custom vector DB; интеграции: 1C, Bitrix24, Jira, Zendesk, Confluence, SharePoint
- Бенчмарк 5 LLM для RU: GPT-4o 96%/2.0с, GigaChat MAX 92%/1.2с, Gemma 2 9B 89%, LLaMA 3.1 70B 85%/0.8с, YandexGPT 4 83%
- Результаты: автоматизация 20%→90%, время обработки 10 мин→8-15 сек

### MaximML: Privacy-LLM (MaximML)
- 7 практических privacy-архитектур: Privacy-Gateway (NER-замена PII + аудит-лог), On-Device RAG (FAISS + локальный LLM), In-Browser inference (WebGPU/WebLLM, 1-3B квантизированные модели)
- Privacy-Gateway: regex + NER для структурированных PII → токены-заменители → облачный LLM → восстановление
- On-Device RAG: sentence-transformers + FAISS + Ollama — zero data egress
- Честное признание ограничений: NER false positives, context leakage при уникальных деталях

## Collab Finder результаты

- **Агро ML** → нет результатов (новая ниша)
- **SWE-MERA** → нет результатов (новая ниша)
- **Robovoice** → нет результатов (новая ниша)
- **Privacy LLM** → нет результатов (новая ниша)

## Накопленная таблица раундов (R01–R41)

| Раунд | Проектов | Ключевая тема |
|-------|----------|---------------|
| R01 | 9 | Memory + Knowledge |
| R02 | 6 | Voice, parsing, YAML |
| R03 | 3 | Code review, fine-tuned LLM |
| R04 | 3 | Agent platform, MCP protocol |
| R05 | 3 | Autonomous pipeline, Russian NLP |
| R06–R10 | 20 | Video AI, multi-agent, GraphRAG, Rust, simulation |
| R11–R15 | 20 | Desktop agents, analytics AI, observability, Text2SQL |
| R16–R20 | 20 | ASR, Knowledge Graph, synthetic data, reasoning |
| R21–R25 | 20 | A2A, legal NLP, HR AI, DevOps, визуальное тестирование |
| R26–R30 | 20 | Finam, AIOps, LLM кибербезопасность, VLM, HITL |
| R31–R35 | 20 | DBRM, Cognitive Memory, Enterprise RAG, red-teaming, Edge AI |
| R36–R37 | 8 | FinBench, Memento, Rewrite Factory, AISecurity, IoT-MCP |
| R38 | 4 | MAESTRO медицина, Sequential координация, LangFuse, Graph RAG |
| R39 | 4 | Contract SGR, Agent Distillation, 5-Layer Memory, Stryker Testing |
| R40 | 4 | LLM строительство, Structured Output, Академия, Kaspersky MCP |
| R41 | 4 | Агро ML pipeline, SWE-MERA бенчмарк, Robovoice поддержка, Privacy LLM |
| **Итого** | **168** | **41 раунд** |

## Темы для Round 42

1. **LLM для финтех v3** — кредитный скоринг через LLM, объяснимые решения, регуляторные требования
2. **Мультимодальные агенты v2** — vision-language для промышленных задач, VLM + action, screenshot-based automation
3. **LLM DevOps/SRE v2** — автоматическое расследование инцидентов, runbook execution, RCA через LLM
4. **Русскоязычные LLM v3** — fine-tuning на русских корпусах, GigaChat/YandexGPT архитектурные детали, MERA-бенчмарки
