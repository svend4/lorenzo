# Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** LiteLLM, Auto AI Router

---
<!-- tags: security, architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 1. LLM-gateway × Self-hosted фронт + локальный inference

Auto AI Router на Go (https://habr.com/ru/articles/1027878/, статья от 25 апреля) — лёгкий прокси, OpenAI-формат, десятки мегабайт RAM, старт <1 с. Автор открыто говорит: не заменяет LiteLLM, а закрывает узкую нишу высокопроизводительного маршрутизатора. LiteLLM (BerriAI) — 100+ провайдеров, виртуальные ключи, бюджеты, fallback. Open WebUI / LibreChat — фронт. Ollama — локальный backend. По отдельности каждое решает один кусок головоломки.

Дети:

Иерархия моделей по сложности на одной машине — паттерн из комментариев (https://habr.com/ru/articles/1024884/comments/): LibreChat → LiteLLM → Ollama локально + fallback на дешёвый облачный (DeepSeek/Gemini Flash) → topовый только для архитектурных задач. На RTX 5090 дома — все рутинные запросы бесплатно, сложные дешевле в 10×, тесты гонишь локально. Бюджетирование автоматическое.

Auto AI Router как sidecar — крутится рядом с Open WebUI, балансирует ключи Anthropic+OpenAI+Vertex+локальные, прячет это под единый OpenAI endpoint. Любой клиент (Cursor, Codex, Claude Code, чат пользователя) видит один URL, не зная что под ним. Особенно ценно для Max'а: отвязка от любых блокировок, жёсткая RPM-защита от случайного выжигания лимитов.

Слой qwen-classifier перед роутером — твой legal-domain-manager уже умеет классифицировать тип запроса (Bescheid? Klage? Stellungnahme?). Поставив маленький классификатор перед LiteLLM, ты получаешь content-aware routing: «это юридический вопрос → Opus», «это рутинный шаблон → Qwen3:8B локально». Сэкономит 80% бюджета без потери качества.

<!-- see-also -->

---

**Смотрите также:**
- [02-multiagentnyy-khaos-reshenie-auto-ai-router](../../technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
- [6-tmux-village-openclaw](6-tmux-village-openclaw.md)
- [4-skill-catalogs-subagents](4-skill-catalogs-subagents.md)
- [1-one-person-one-company](../final-ensembles/1-one-person-one-company.md)

