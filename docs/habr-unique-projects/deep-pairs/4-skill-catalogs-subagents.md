# Пара 4 — Скилл-каталоги × Subagent-оркестрация

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

---
<!-- tags: rag, orchestration, anthropic, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 4. Скилл-каталоги × Subagent-оркестрация

skills.sh (https://vc.ru/id744101/2789872) — каталог скиллов как «npm для агентов», установка одной командой, лидерборд по installs, поддержка Cursor/Codex/Cline. Субагенты в Cursor и Claude Code (https://habr.com/ru/articles/1006602/, habr.com/ru/articles/971620/) — отдельный экземпляр агента с собственным контекстным окном, получает задачу от оркестратора, выполняет автономно. Уровни: оркестратор / разработчик / ревьюер / рецензент. Anthropic Skills официально через CLAUDE.md.

Дети:

Каталог твоих 87+ skills как публичный пакет — выложить твой legal-domain-manager и multi-chat-orchestrator на skills.sh. Любой немецкий юрист с Claude Code или Cursor ставит одной командой и получает полный стек. Это монетизация без продукта: skill сам по себе бесплатный, но его наличие в каталоге = твоя видимость + обратная связь от пользователей + возможные коллаборации (точно та же модель, что у Чуяна с приглашением в комментарии).

Иерархия субагентов под legal — оркестратор (Opus 4.7) → аналитик дела (читает Bescheid, извлекает факты) → исследователь прецедентов (RAG по юридическому корпусу) → составитель (пишет Stellungnahme) → ревьюер (adversarial check) → форматтер (приводит к German court formatting). Каждый — со своим узким контекстом. Это твой multi-chat-orchestrator skill, но в одном Claude Code, не в нескольких чатах. 100k токенов контекста хватает на одно дело.

Self-aware MCP под legal (https://habr.com/ru/articles/1007122/) — расширенная версия: помимо OS/локации/времени даёт агенту знание про текущий Aktenzeichen, активные дедлайны (🔴≤3d/🟠≤7d/🟡≤14d), статус каждого дела. Агент не путает дела между собой и автоматически приоритизирует по красным дедлайнам.

<!-- see-also -->

---

**Смотрите также:**
- [6-tmux-village-openclaw](docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md)
- [1-workflow-llm-mcp](docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md)
- [8-self-aware-mcp-specs](docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md)
- [3-adversarial-multi-ide](docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md)

