# Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Svyazi, CardIndex

---
<!-- tags: knowledge, ingestion, architecture, self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

"Правильная агентская архитектура в 2026" (habr.com/ru/articles/1028290/) — durable state, event-driven ход/шаг/событие, персистентное состояние между запусками

Svyazi от Андрея Чуяна (habr.com/ru/articles/1027724/) — гибрид LLM + детерминированный код, 6-слойная архитектура для извлечения структурированных данных

Дети:

1.1 Агентская система с самообучающимися промптами

Svyazi уже умеет извлекать структуру из текста, но Чуян пишет: "Постоянно размышляю над механизмом обратной связи для самоулучшения промпта". Добавляем durable state из агентской архитектуры:

Каждый извлечённый профиль = событие (event)

Состояние = накопленный корпус + метрики качества

Агент периодически запускает A/B-тестирование промптов

Лучший промпт сохраняется как новое состояние

Результат: система сама улучшает свои промпты через накопленные данные, без ручного вмешательства.

1.2 Multi-domain профилирование с раздельным state

У Свyazi один CardIndex для всех участников. При масштабе >1000 человек это становится узким местом. Durable state позволяет:

Разделить граф на домены (legal / tech / business)

Каждый домен = отдельный агентский поток с собственным состоянием

Cross-domain запросы через event bus

Для Max'а: один домен = юридические дела, второй = AI/ML research, третий = Nautilus-коллаборации. Всё в одной системе, но изолированно.

<!-- see-also -->

---

**Смотрите также:**
- [01-agent-routing](../../03-technology-combinations/01-agent-routing.md)
- [04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura](04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)
- [03-crdt-local-first-svyazi-cardindex](03-crdt-local-first-svyazi-cardindex.md)
- [07-crawl4ai-docling-yodoca-consolidator](07-crawl4ai-docling-yodoca-consolidator.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [01-08-summary](../synthesis-tables/01-08-summary.md)

