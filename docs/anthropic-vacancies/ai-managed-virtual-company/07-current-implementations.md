# Что существует сейчас в этом пространстве

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ идеи AI-managed distributed virtual company как альтернативы найму одного человека з

---
<!-- tags: orchestration, roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ идеи AI-managed distributed virtual company как альтернативы найму одного человека за высокую зарплату.

Что существует сейчас в этом пространстве

Разложу от самого простого к самому амбициозному.

Низкоуровневые frameworks. CrewAI, AutoGen (Microsoft Research), LangGraph — позволяют строить multi-agent pipelines, где один LLM играет роль менеджера, другие — роли исполнителей. Подходит для прототипа уровня 1-2. Работает. Не масштабируется за пределы демо.

Среднеуровневые попытки. MetaGPT (симулирует целую software company из AI-агентов — product manager, architect, engineer, QA), ChatDev (то же для софтверной разработки). Интересные артефакты, но все агенты — AI, людей нет. Ваша модель — противоположная: AI-агенты помощники живым людям, а не замена.

Ближе к вашей модели: AI-native staffing platforms. Mercor — AI собеседует и матчит фрилансеров. Braintrust — автоматизированный matching. Но они останавливаются на найме, не идут в оркестрацию проекта.

Ещё ближе: agents для pair-programming и code-review. Cursor's Background Agents, GitHub Copilot Workspace, Devin AI от Cognition, SWE-agent от Princeton. Это уже реальные персональные AI-супервайзеры для одиночных разработчиков. Но они не знают про команду — каждый работает изолированно со своим человеком.

То, чего пока нет в продукте. Именно то, что вы описали: иерархическая команда AI-агентов, координирующая живую distributed команду людей на протяжении всего проекта. Это white space в рынке. Исследования по этой теме (Stanford HAI, MIT CSAIL) идут, но продакшн-системы — ещё нет.

<!-- see-also -->

---

**Смотрите также:**
- [01-existing-landscape](docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md)
- [03-three-variants-A-B-C](docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md)
- [08-pluses-of-model](docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md)
- [10-three-entry-points](docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [01-existing-landscape](docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md) (сходство 0.20)
- [08-pluses-of-model](docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md) (сходство 0.16)
- [03-three-variants-A-B-C](docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md) (сходство 0.15)

