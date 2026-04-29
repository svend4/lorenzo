# Агентные системы и роутинг

<!-- summary -->
> самоулучшения промпта". Добавляем durable state из агентской архитектуры:
**Проекты:** CardIndex, Auto AI Router

---
<!-- tags: knowledge, architecture, self-improvement, collaboration -->




самоулучшения промпта". Добавляем durable state из агентской архитектуры:
- Каждый извлечённый профиль = событие (event)
- Состояние = накопленный корпус + метрики качества
- Агент периодически запускает A/B-тестирование промптов
- Лучший промпт сохраняется как новое состояние
Результат: система сама улучшает свои промпты через накопленные данные, без ручного вмешательства.
1.2 Multi-domain профилирование с раздельным state У Свyazi один CardIndex для всех участников. При масштабе >1000 человек это становится узким местом. Durable state позволяет:
- Разделить граф на домены (legal / tech / business)
- Каждый домен = отдельный агентский поток с собственным состоянием
- Cross-domain запросы через event bus
Для Max'а: один домен = юридические дела, второй = AI/ML research, третий = Nautilus-коллаборации. Всё в одной системе, но изолированно.
---
#### Комбинация 2: Мультиагентный хаос-решение × Auto AI Router
Родители:
- "Мультиагентный хаос" (habr.com/ru/articles/1026856/) — статья 5 дней назад: как мы построили систему, которая действительно работает; Planner → Executor паттерн
- Auto AI Router на Go (habr.com/ru/articles/1027878/) — лёгкий прокси, OpenAI-формат, мегабайты RAM, старт <1с
Дети:
2.1 Иерархический

<!-- similar-docs -->

---

**Похожие документы:**
- [03-local-first](docs/03-technology-combinations/03-local-first.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [03-local-first](docs/03-technology-combinations/03-local-first.md)
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md)
- [WORD_FREQ](docs/WORD_FREQ.md)
- [04-sozialrecht-domain](docs/03-technology-combinations/04-sozialrecht-domain.md)

<!-- backlinks-auto -->
## Упоминается в

- [Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md)

<!-- related-auto -->
## Связанные документы

- [Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md) _29%_
- [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md) _21%_
- [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) _21%_
