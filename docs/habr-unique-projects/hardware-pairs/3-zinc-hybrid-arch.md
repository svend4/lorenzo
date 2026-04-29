# Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Yodoca, AutoResearch

---
<!-- tags: memory, orchestration, architecture, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 3. Кастомный inference engine на Zig/Vulkan (ZINC) × гибрид Attention+SSM+MoE

Родители: ZINC inference engine для Qwen3.5-35B-A3B на $500-карте AMD R9700 (habr.com/ru/articles/1020702/) и сама гибридная архитектура Qwen3.5: 4 слоя full attention + 36 слоёв SSM + MoE-роутер с 8+1 экспертами на слой. Биология: 39% времени уходит на MoE-маршрутизацию — ровно тот узел, в который Max уже целится своим MoME. Физика: Zig + Vulkan = переносимость, нет рантайм-зависимостей, один бинарник.

Дети:

ZINC-Q6 — порт MoME-роутера по Q6-гиперкубу как Vulkan-кернел внутри ZINC. Уже есть карта: 4 attention + 36 SSM + 8+1 эксперта на слой. Заменяешь стандартный routed-MoE на свой геометрический роутер, всё остальное остаётся. Это прямая дорожка от твоего pro2-репозитория к работающему локальному инференсу на доступном железе.

Hierarchical KV-cache как родной слой движка — иерархическая память (xMemory) перестаёт быть software-слоем поверх LLM и становится трёхуровневым paged KV-cache внутри inference engine: рабочий контекст в SRAM, эпизодический в VRAM, семантический в RAM. Управляется тем же MoME-роутером — какой уровень достать.

Autonomous Research Box — связка из ZINC + AutoResearch-loop Карпатого (habr.com/ru/articles/1026922/) + Sequential-протокол Дочкиной (habr.com/ru/articles/1017200/) + Yodoca-consolidator на одной R9700 за $500. Полный «ночной исследовательский отдел», который Карпатый описывает гипотетически, у тебя получается железно — за бюджет средней игровой видеокарты.

<!-- see-also -->

---

**Смотрите также:**
- [6-bonus-rram-memristor](docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md)
- [06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-](docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md)
- [3-crdt-self-hosted](docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md)
- [4-riscv-privacy](docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [3-crdt-self-hosted](docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md) (сходство 0.19)
- [4-riscv-privacy](docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md) (сходство 0.18)
- [6-bonus-rram-memristor](docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md) (сходство 0.17)

