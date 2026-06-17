---
date: 2026-06-05
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 52 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> habr.com/ru/companies/yandex/articles/800945/ ivan_zhirnov (Передовые Платежные Решения): Production-кейс: скриптовый бот → supervisor multi-agent LLM.
 ivan_zhirnov (Передовые Платежные Решения): Production-кейс: скриптовый бот → supervisor multi-agent LLM.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  
**Итого по всем раундам:** 212 проектов, 90+ авторов

## Темы поиска

1. **LLM квантование и прунинг для edge deployment** — GPTQ/AWQ, QLoRA, SmoothQuant, систематический обзор методов
2. **Conversational AI с handoff и эскалацией** — multi-agent chatbot, supervisor-pattern, детерминированная эскалация
3. **LLM для финансового аудита и бухгалтерии** — extraction из счетов-фактур, актов, договоров, ERP integration
4. **Машинное забывание (machine unlearning)** — TOFU/WMDP бенчмарки, gradient ascent, NPO + LoRA

## Найденные проекты

| # | Автор | Проект | Слой | Файл |
|---|-------|--------|------|------|
| 1 | re9ulus | Quantization Deep Dive: LLM.Int8/SmoothQuant/GPTQ/QLoRA | knowledge/ingestion | `projects/re9ulus-yandex-llm-quantization-deep-dive-gptq-qlora.md` |
| 2 | ivan_zhirnov | Multi-Agent Customer Support: 92% автоматизации | orchestration | `projects/ivan-zhirnov-multiagent-customer-support-92pct-automation.md` |
| 3 | Рег.облако+Raft | LLM Extraction бухгалтерских документов: F1=95.9% | ingestion/knowledge | `projects/runity-regcloud-llm-accounting-docs-qwen3-extraction.md` |
| 4 | MidavNibush | Machine Unlearning для LLM: TOFU/WMDP/NPO | orchestration/knowledge | `projects/midavnibush-machine-unlearning-llm-tofu-wmdp-openunlearning.md` |

## Ключевые находки раунда

- **re9ulus (Яндекс):** Систематическая таксономия 6 методов квантования LLM: outlier activation проблема → LLM.Int8 (смешанная точность), SmoothQuant (offline перенос), GPTQ (Hessian-оптимальный INT4, 3.25× на A100), SPQR (блочные outliers), QLoRA (NF4 + BF16 LoRA, 65B на 48GB). [habr.com/ru/companies/yandex/articles/800945/](https://habr.com/ru/companies/yandex/articles/800945/)

- **ivan_zhirnov (Передовые Платежные Решения):** Production-кейс: скриптовый бот → supervisor multi-agent LLM. 73K текстовых диалогов/месяц, 92%+ без эскалации. Ключевой урок: бизнес-логика (числа, комиссии) — в код, не в промпт. Детерминированный supervisor. FAISS+TF-IDF победил Chroma. [habr.com/ru/articles/976782/](https://habr.com/ru/articles/976782/)

- **Рег.облако + Raft:** 5-этапный асинхронный пайплайн extraction из 200+ бухгалтерских документов строительной отрасли. Qwen3-30B-A3B-Instruct (MoE, 3B активных параметров) победил dense 32B. F1=95.9% vs 63% baseline. Confidence threshold 0.70 для автоматического ERP import. [habr.com/ru/companies/runity/articles/987424/](https://habr.com/ru/companies/runity/articles/987424/)

- **MidavNibush (Вадим Шубин):** Machine Unlearning для LLM — удаление знаний из обученной модели. TOFU (20 вымышленных авторов) + WMDP (биооружие/кибероружие) бенчмарки. Gradient Ascent Forgetting + NPO (Negative Preference Optimization). OpenUnlearning с LoRA-расширением. MIA-тест для верификации забывания. [habr.com/ru/companies/oleg-bunin/articles/1014692/](https://habr.com/ru/companies/oleg-bunin/articles/1014692/)

## Темы для Round 53

1. **LLM для анализа кода и технического долга** — code smell detection, refactoring suggestions, tech debt quantification с AI
2. **Streaming LLM inference и long-context оптимизация** — KV-cache управление, prefill/decode оптимизация, speculative decoding
3. **LLM для HR и рекрутинга v2** — resume screening, interview simulation, candidate evaluation (новый угол: bias detection)
4. **Мультиагентные дебаты и consensus** — LLM debate frameworks, самокритика агентов, multi-perspective reasoning

## Накопленная таблица раундов (R01–R52)

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
| R40 | 4 | LLM строительство, structured output v2, образование v3, кибербезопасность v2 |
| R41 | 4 | Агро ML pipeline, SWE-MERA бенчмарк, Robovoice поддержка, Privacy LLM |
| R42 | 4 | AML LLM советник, PhysicalAgent VLA, SherlockOps SRE, T-Bank RU LLM |
| R43 | 4 | feeds.fun медиа, RAG чанкинг, LOCK-R reasoning, Kaspersky MLAD ICS |
| R44 | 4 | AI EMR ассистент, LoRA эмбеддинги, Yandex LLM eval, LangGraph агенты |
| R45 | 4 | MWS Vision Bench, MOEX DistilBERT, Avito Mistral RU, LLM Observability |
| R46 | 4 | Coordination Harness, Telecom Classifier, Code MCP, AQLM.rs браузер |
| R47 | 4 | LLM Judge образование, SENTINEL безопасность, MTS code review, Temporal KG |
| R48 | 4 | LLM медицина v3, Multimodal RAG v2, ML промышленность v2, Agent evaluation v2 |
| R49 | 4 | Finance RAG 4-head, GBNF constrained decoding, Self-hosted 4×4090, SAP Text2SQL |
| R50 | 4 | LLM персонализация v3, Qwen3Guard модерация, SR-Scientist, RAG embedder fine-tuning |
| R51 | 4 | Video RAG CLIP, Design by Contract, ЕГЭ репетитор, FREED++ drug discovery |
| R52 | 4 | LLM квантование GPTQ/QLoRA, Multi-agent customer support, Bухгалтерский extraction, Machine Unlearning |
| **Итого** | **212** | |


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```
