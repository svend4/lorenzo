# Ансамбль 8 — Budget-Aware Intelligence Stack

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, Tool Search

---
<!-- tags: rag, security, knowledge, ingestion, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

8. Budget-Aware Intelligence Stack: «не всё надо отдавать большой LLM»

Родители: SVM/TF-IDF + local models + RLM-Toolkit + MCP Tool Search + model routing.

Статья про SVM в 2026 году даёт важный анти-хайповый кубик: для персонализированных рекомендаций научных статей старый SVM/TF-IDF может быть быстрее, дешевле и интерпретируемее; гибрид SVM + LLM оценивается как production-вариант для высоких требований. Habr

RLM-Toolkit показывает другой масштаб: конфигурации для обработки 10M+ токенов, варианты Budget-First, Quality-First, Privacy-First и Speed-First, включая локальные модели, иерархическую память, трассировку, sandbox и контроль стоимости. Habr

MCP Tool Search в Claude Code показал сильную рационализацию: вместо загрузки всех MCP-серверов сразу система лениво подгружает нужные, что в примере снизило контекст MCP с десятков тысяч токенов до baseline и дало +76k свободных токенов. Habr

Что рождается при склейке:

Получается экономный интеллект-роутер.

Схема:

SVM/TF-IDF/BM25 → small local LLM → domain model → frontier LLM only if needed → trace/cost/eval

Дети этой связки:

Cheap-first Svyazi — сначала deterministic filter/SVM, потом локальная модель, и только спорные карточки идут в большую модель.

Legal Budget Router — простые запросы по делу обслуживает локальный RAG, сложные аргументы и финальный review идут в дорогую модель.

Research Compression Engine — 10M токенов литературы сжимается локально/дёшево, а большая модель подключается только к финальным гипотезам.

Главное новое свойство: качество сохраняется, стоимость падает. Большая модель становится не молотком для всего, а последним уровнем в иерархии.

<!-- see-also -->

---

**Смотрите также:**
- [02-agentops-trace-envelope](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md)
- [6-continuous-eval-loop](docs/ai-collaborations/ensembles/6-continuous-eval-loop.md)
- [5-agent-firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md)
- [7-domain-agent-app-factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [6-continuous-eval-loop](docs/ai-collaborations/ensembles/6-continuous-eval-loop.md) (сходство 0.17)
- [5-agent-firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md) (сходство 0.17)
- [02-agentops-trace-envelope](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md) (сходство 0.17)

