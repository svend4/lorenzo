# Local-first и P2P стек

<!-- summary -->
> - Сложные архитектурные → Claude Opus
**Проекты:** Svyazi, CardIndex, Yjs

---
<!-- tags: rag, knowledge, ingestion, local-first, architecture, collaboration -->




локальная Qwen3:8B
- Средние → облачная DeepSeek
- Сложные архитектурные → Claude Opus
- Роутер перед каждым агентом, не после
Экономия: 80% запросов идут на дешёвые модели, Opus только для Planner-агента.
2.2 Fault-tolerant агентский граф Router даёт fallback из коробки. Если Opus недоступен → Sonnet → GPT-5.4 → локальная модель. Мультиагентная система перестаёт ломаться при отказе одного провайдера.
---
#### Комбинация 3: CRDT local-first × Svyazi CardIndex
Родители:
- CRDT / RON / Yjs (habr.com/ru/articles/534510/, habr.com/ru/articles/946722/) — conflict-free replicated data types, p2p синхронизация
- Svyazi CardIndex — YAML-структура профилей с хешами для дедупликации
Дети:
3.1 P2P-граф сообщества без центрального сервера Сейчас Svyazi — single-user система. С CRDT:
- Каждый участник ведёт локальный CardIndex
- Изменения синхронизируются p2p через Yjs
- Конфликты (два человека обновили профиль одного участника) мержатся автоматически
- Никакого центрального сервера — privacy by design
Для legal-community Max'а: каждый юрист в сообществе ведёт свой локальный граф дел и участников, но всё синхронизируется peer-to-peer. Данные не покидают машины участников.
3.2 Offline-first discovery Discovery-файл Svyazi (накопление неизвестного) синхронизируется через CRDT между устройствами:
- Ноутбук нашёл новую сущность → добавил в discovery
- Телефон оффлайн 2 дня
- При подключении автоматически получает обновления
- Модерация тоже распределённая
---
#### Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура
Родители:
- Парсинг с LLM (habr.com/ru/articles/892954/) — Structured Outputs, Pydantic, автоматическое извлечение структуры
- Graph-RAG (habr.com/ru/articles/871700/) — Microsoft Research, графы знаний вместо плоского RAG
- Durable state агенты (habr.com/ru/articles/1028290/)
Дети:
4.1 Self-building legal knowledge graph Агент читает новые решения Sozialgericht:
- Парсер LLM: извлекает сущности (судья, § закона, истец, ответчик, решение)
- Graph builder: строит

<!-- similar-docs -->

---

**Похожие документы:**
- [01-agent-routing](docs/03-technology-combinations/01-agent-routing.md) (сходство 0.12)
- [05-benchmarks](docs/03-technology-combinations/05-benchmarks.md) (сходство 0.11)
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [01-agent-routing](docs/03-technology-combinations/01-agent-routing.md)
- [05-benchmarks](docs/03-technology-combinations/05-benchmarks.md)
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md)
- [WORD_FREQ](docs/WORD_FREQ.md)

<!-- backlinks-auto -->
## Упоминается в

- [Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md)

<!-- related-auto -->
## Связанные документы

- [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) _33%_
- [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md) _29%_
- [Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md) _25%_
- [Приоритеты файлов](docs/PRIORITIES.md) _25%_
- [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md) _21%_
- [Глоссарий проектов](docs/GLOSSARY.md) _17%_
- [Тепловая карта тем](docs/HEATMAP.md) _17%_
- [Карта репозитория Lorenzo](docs/SITEMAP.md) _17%_
