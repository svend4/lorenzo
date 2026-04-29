# Синтез: хеббовский граф людей-навыков-идей

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, CardIndex, NGT Memory, Wikontic

---
<!-- tags: memory, knowledge, ingestion, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

Локальная система обнаружения коллабораций на хеббовском графе людей-навыков-идей.

Конкретно — кто что даёт:

— от Svyazi Чуяна: 6-слойная гибридная архитектура, CardIndex как single source of truth, Discovery-файл (накопление неизвестного), двухэтапный поиск, privacy by design; — от Wikontic Чепуровой: онтологический слой вместо ручного synonyms.yml — нормализация через автоматическую сверку с Wikidata, проверка триплетов на соответствие правилам онтологии; — от K2-18 Романова: формальная метрика качества структуры (Чуян пишет: «лучшее, что я пока придумал — показатель качества карточки» — у Романова это уже формализовано через образовательные метрики, оттуда можно адаптировать концепцию); — от NGT Memory: хеббовское усиление связей. Не просто «эти двое оба знают Go», а «эти двое в течение месяца независимо упомянули Wi-Fi и open-source-радиопланирование» — связь между ними укрепляется автоматически, и система предлагает их свести именно по этой ко-активации; — от Knowledge Graph Kit: MCP-обёртка, чтобы Claude / любая локальная LLM могла работать с базой как с инструментом, не зная про внутреннее устройство.

Получается система, где случай с Wi-Fi-инженером и питерским разработчиком — не баг и не везение, а основной режим работы. Такого пока нигде в публичном пространстве не видно — каждый из четырёх авторов закрывает свой кусок, но никто не собрал всё вместе.

Практический совет

<!-- see-also -->

---

**Смотрите также:**
- [02-related-projects](docs/habr-unique-projects/analogues/02-related-projects.md)
- [01-three-direct-analogues](docs/habr-unique-projects/analogues/01-three-direct-analogues.md)
- [02-related-projects-context](docs/ai-collaborations/candidates/02-related-projects-context.md)
- [01-three-key-candidates](docs/ai-collaborations/candidates/01-three-key-candidates.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [02-related-projects](docs/habr-unique-projects/analogues/02-related-projects.md) (сходство 0.50)
- [01-three-direct-analogues](docs/habr-unique-projects/analogues/01-three-direct-analogues.md) (сходство 0.18)
- [02-related-projects-context](docs/ai-collaborations/candidates/02-related-projects-context.md) (сходство 0.18)

