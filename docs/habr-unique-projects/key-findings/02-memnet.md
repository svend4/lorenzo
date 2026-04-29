# MemNet — нейроархитектурный двойник «магии» Svyazi

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, NGT Memory, MemNet

---
<!-- tags: memory, ingestion, architecture, roadmap, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Нейроархитектурный двойник «магии» Svyazi

MemNet — «Memory Is All You Need»
https://habr.com/ru/articles/983684/
Здесь автор делает то же самое, что NGT Memory из прошлого ответа, но на уровне обучаемой архитектуры, а не приложения. Память — дифференцируемый граф со слотами-векторами и матрицей смежности; связи обновляются по STDP (spike-timing-dependent plasticity, нейробиологический родственник Хебба); есть spreading activation для ассоциативного recall; и — самое интересное — периодические фазы «сновидений», когда self-attention идёт по слотам памяти без внешнего входа, и именно тогда «обнаруживаются скрытые связи и абстрагируются представления». Это и есть формализация того, что у Чуяна получилось эмпирически с Wi-Fi-инженером — только на уровне трансформера.

Для тебя, с твоим YiJing-Transformer + MoME + Q6, это особенно близко: STDP-граф над слотами + dream-фаза по сути решают ту же задачу, что MoME-роутинг по гиперкубу — выбор релевантных «экспертов» при запросе.

Философский родственник: «LLM как периферия»

AI-бот для самопознания

<!-- see-also -->

---

**Смотрите также:**
- [2-tsu-mome](docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md)
- [01-yodoca](docs/habr-unique-projects/key-findings/01-yodoca.md)
- [05-supplementary-infrastructure](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md)
- [03-pda-llm-as-periphery](docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md)

