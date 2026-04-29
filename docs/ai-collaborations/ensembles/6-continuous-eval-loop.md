# Ансамбль 6 — Continuous Eval Loop

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, AI Factory

---
<!-- tags: orchestration, knowledge, ingestion, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

6. Continuous Eval Loop: «самоулучшение не на вере, а на метриках»

Родители: Langfuse/LLM observability + human-eval legal bench + AI Factory self-learning patches + ACD.

В статье по Langfuse автор пишет, что LLM-сервисы трудно интерпретировать: для бизнеса они выглядят как black box, для инженеров — как плохо воспроизводимые состояния. Langfuse выбран из-за self-hosting, контроля данных, управления промптами, cost tracking, версионирования и глубокого трейсинга цепочек/агентов/workflow. Habr

Большой гайд по LLM Observability покрывает Langfuse, Phoenix, OpenLIT, Langtrace, LangWatch и Lunary как инструменты для трейсинга LLM и AI-агентов. Habr

Юридический human-eval bench даёт редкий доменный пример: практикующий юрист организовала слепое сравнение пяти нейросетевых сервисов с 11 коллегами-оценщиками в области, где часто нет одного единственно правильного ответа. Habr

AI Factory добавляет механизм самообучения: /aif-fix создаёт патч с описанием ошибки, причины и исправления, а /aif-evolve анализирует накопленные патчи, находит повторяющиеся проблемы и обновляет skills под проект. Habr

ACD — Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для модели-испытуемого и автоматически выявляет тысячи возможностей и ошибок, которые сложно обнаружить одной человеческой команде. Habr

Что рождается при склейке:

Получается continuous evaluation and improvement loop для агентов.

Схема:

agent traces → Langfuse/Phoenix → human/LLM eval → error patches → skill evolution → regression benchmark → redeploy

Дети этой связки:

Prompt CI/CD — промпты, skills и workflows тестируются как код: с версиями, регрессиями, метриками, rollback.

Legal Quality Bench — каждое новое правило, шаблон или legal skill прогоняется на наборе эталонных дел и оценивается человеком/LLM-судьёй.

Svyazi Self-Improver — карточки с низким качеством extraction превращаются в тест-кейсы; система сама предлагает, какой prompt/нормализатор улучшить.

Главное новое свойство: самоулучшение становится инженерным процессом, а не «давайте поправим промпт на глаз».

<!-- see-also -->

---

**Смотрите также:**
- [8-budget-aware-intelligence-stack](docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md)
- [7-domain-agent-app-factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md)
- [1-agentic-knowledge-os](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md)
- [2-distributed-agent-workshop](docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [8-budget-aware-intelligence-stack](docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md) (сходство 0.17)
- [7-domain-agent-app-factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md) (сходство 0.16)
- [1-agentic-knowledge-os](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md) (сходство 0.15)

