# Пара 2 — Термодинамические TSU × MoE/MoME-роутинг

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** MemNet

---
<!-- tags: memory, knowledge, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 2. Термодинамические TSU (Extropic, Normal Computing) × MoE/MoME-роутинг

Родители: вероятностные процессоры на p-битах с тепловым шумом как примитивом (Extropic XTR-0 и грядущий Z1, библиотека thrml — habr.com/ru/companies/ruvds/articles/980152/, habr.com/ru/articles/800033/; Normal Computing — habr.com/ru/news/789164/) и MoE/MoME-роутинг с softmax-выбором экспертов. Биология: и то и другое — вероятностное взвешенное сэмплирование. Физика: матричное умножение ускоряется максимум в ~4× (закон Амдала), а probabilistic sampling — нативная операция TSU и до 10 000× энергоэффективнее.

Дети:

Probabilistic MoME router — гейт MoE / MoME перестаёт быть softmax-слоем на GPU и становится thermodynamic sampling по экспертам. Для твоего Q6-гиперкуба это особенно красиво: вершины Q6 = энергетические минимумы EBM, и роутер сам сваливается в нужную через тепловую релаксацию. LCI (Lyapunov Coherence Index) тогда — буквально измеряемая энергетическая когерентность системы, не метафора.

Thermodynamic confidence layer — для legal-AI: вместо тройки verified/claimed/inferred (которая у Чуяна ставится post-hoc детерминированным кодом) — энергетическая модель убеждений, физически реализованная p-битами. Каждый факт в карточке участника несёт распределение, а не метку. Для Sozialgericht-документов это, кстати, гораздо честнее, чем категорические inferred.

Dream-engine для discovery — у MemNet («Memory Is All You Need») были «фазы сновидений» — self-attention над слотами без внешнего входа, чтобы найти скрытые связи. На TSU это становится буквальной диффузионной моделью на p-битах в режиме ночного отжига. Discovery-механизм Чуяна (накопление неизвестного → ручная модерация) превращается в физический процесс.

<!-- see-also -->

---

**Смотрите также:**
- [02-memnet](docs/habr-unique-projects/key-findings/02-memnet.md)
- [3-zinc-hybrid-arch](docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)
- [5-tinyml-mcp-skills](docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md)
- [6-bonus-rram-memristor](docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md)

