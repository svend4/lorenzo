# Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** AutoResearch

---
<!-- tags: self-improvement, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

OpenClaude (habr.com/ru/articles/1018234/) — форк Claude Code с OpenAI-совместимым провайдером, можно подключить любую модель

ZINC (habr.com/ru/articles/1020702/) — кастомный inference на Zig/Vulkan для Qwen3.5-35B-A3B

MoME-роутер — из твоего YiJing-Transformer/pro2, Q6-гиперкуб, LCI метрика

Дети:

6.1 OpenClaude + ZINC + Q6-роутер = локальный агент с геометрическим выбором экспертов

OpenClaude даёт агентские инструменты (bash, file ops, MCP). ZINC даёт быстрый локальный инференс. Добавляем MoME:

Qwen3.5-35B-A3B разбита на 8 экспертов по Q6-вершинам

Роутер выбирает эксперта по задаче геометрически

Всё локально, никаких API-ключей

LCI контролирует когерентность агента

Применение: legal AI на собственном железе без отправки данных наружу. GDPR-compliant, RISC-V-ready.

6.2 AutoResearch loop с геометрическим роутингом

AutoResearch Карпатого + Q6-роутер + ZINC:

Ночью агент крутит эксперименты с промптами

Роутер геометрически выбирает, какой эксперт подходит для данного типа задач

Лучший промпт сохраняется, LCI отслеживает стабильность

Утром — отчёт о том, какие эксперты сработали лучше на каких задачах

<!-- see-also -->

---

**Смотрите также:**
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md)
- [02-multiagentnyy-khaos-reshenie-auto-ai-router](docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
- [3-zinc-hybrid-arch](docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)
- [01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern](docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.29)
- [02-knowledge-graphs](docs/obsidian/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.28)
- [02-multiagentnyy-khaos-reshenie-auto-ai-router](docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md) (сходство 0.18)

