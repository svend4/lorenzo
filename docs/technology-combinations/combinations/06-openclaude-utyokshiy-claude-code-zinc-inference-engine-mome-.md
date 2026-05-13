---
state: approved
---

# Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория). Документ создан на основе исследования. Ссылки ведут на связанные материалы.
**Проекты:** AutoResearch

---
<!-- tags: self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 6 OpenClaude утёкший Claude"
```

## Смотрите также
- [02-knowledge-graphs](../../03-technology-combinations/02-knowledge-graphs.md)
- [02-multiagentnyy-khaos-reshenie-auto-ai-router](02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
- [3-zinc-hybrid-arch](../../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)
- 01-pravilnaya-agentskaya-arkhitektura-[svyazi-pattern](01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [01-08-summary](../synthesis-tables/01-08-summary.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ доступен для семантического поиска и навигации._ _Доступен поиск._

<!-- similar-docs -->

---

**Похожие документы:**
- [06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-](../../obsidian/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md) (сходство 0.94)
- [02-knowledge-graphs](../../obsidian/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.30)
- [02-knowledge-graphs](../../03-technology-combinations/02-knowledge-graphs.md) (сходство 0.30)

