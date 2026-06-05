---
date: 2026-05-13
tags: [rag, orchestration, knowledge, ingestion, self-improvement]
state: approved
---

# Ансамбль 6 — Continuous Eval Loop

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. ACD — Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для модели-испытуемого и автоматически выявляет тысяч
ACD — Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для модели-испытуемого и автоматически выявляет тысячи возможностей и ошибок, которые сложно обнаружить одной человеческой ко
**Проекты:** Svyazi, AI Factory

---
<!-- tags: orchestration, knowledge, ingestion, self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Ансамбль 6 Continuous Eval Loop"
```

## Смотрите также
- [8-budget-aware-intelligence-stack](8-budget-aware-intelligence-stack.md)
- [7-domain-agent-app-factory](7-domain-agent-app-factory.md)
- [1-agentic-knowledge-os](1-agentic-knowledge-os.md)
- [2-distributed-agent-workshop](2-distributed-agent-workshop.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [7-domain-agent-app-factory](7-domain-agent-app-factory.md)
- [8-budget-aware-intelligence-stack](8-budget-aware-intelligence-stack.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [6-continuous-eval-loop](../../obsidian/ai-collaborations/ensembles/6-continuous-eval-loop.md) (сходство 0.99)
- [8-budget-aware-intelligence-stack](8-budget-aware-intelligence-stack.md) (сходство 0.22)
- [8-budget-aware-intelligence-stack](../../obsidian/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md) (сходство 0.22)

