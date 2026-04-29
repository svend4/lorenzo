# Комбинация 2: Мультиагентный хаос-решение × Auto AI Router

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Auto AI Router

---
<!-- tags: architecture, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

"Мультиагентный хаос" (habr.com/ru/articles/1026856/) — статья 5 дней назад: как мы построили систему, которая действительно работает; Planner → Executor паттерн

Auto AI Router на Go (habr.com/ru/articles/1027878/) — лёгкий прокси, OpenAI-формат, мегабайты RAM, старт <1с

Дети:

2.1 Иерархический роутинг агентов по сложности

Проблема мультиагентных систем — каждый агент вызывает дорогую модель. Router решает:

Простые запросы → локальная Qwen3:8B

Средние → облачная DeepSeek

Сложные архитектурные → Claude Opus

Роутер перед каждым агентом, не после

Экономия: 80% запросов идут на дешёвые модели, Opus только для Planner-агента.

2.2 Fault-tolerant агентский граф

Router даёт fallback из коробки. Если Opus недоступен → Sonnet → GPT-5.4 → локальная модель. Мультиагентная система перестаёт ломаться при отказе одного провайдера.

<!-- see-also -->

---

**Смотрите также:**
- [03-local-first](docs/03-technology-combinations/03-local-first.md)
- [01-agent-routing](docs/03-technology-combinations/01-agent-routing.md)
- [05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy](docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)
- [1-llm-gateway](docs/habr-unique-projects/deep-pairs/1-llm-gateway.md)

