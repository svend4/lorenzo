# Графы знаний и Legal AI

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> граф знаний (BSG B 8 SO 9/19 R → § 78 Abs. 6 SGB IX → Antragsteller)
**Проекты:** Yodoca, Auto AI Router, AutoResearch

---

<!-- toc -->
## Содержание

- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы)

---

<!-- tags: memory, rag, orchestration, knowledge, self-improvement, collaboration -->




граф знаний (BSG B 8 SO 9/19 R → § 78 Abs. 6 SGB IX → Antragsteller)
- Durable state: граф персистентен между запусками, растёт автоматически
- Query: вопросы типа "найди дела где § 78 + retroactive budget + BSG" идут через Graph-RAG, не через векторный поиск
Качество: находит многошаговые связи, которые обычный RAG пропускает.
4.2 Progressive knowledge refinement Первый проход — LLM парсит грубо, добавляет узлы в граф с confidence=low. Агент периодически переобрабатывает low-confidence узлы через более сильную модель, повышает точность. Граф становится точнее со временем без переобработки всего корпуса.
---
#### Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной
Родители:
- SourceCraft CLI (habr.com/ru/news/1026498/) — Яндекс, консольное приложение с ИИ-агентом, skills (сценарии), накопление знаний команды
- Claude Code — CLI с bash, MCP, subagents
- Sequential протокол (habr.com/ru/articles/1017200/) — 8-16 малых агентов, каждый видит результаты предшественников, 44% качества выше координатора
Дети:
5.1 Distributed code review без координатора Вместо одного агента-ревьюера — Sequential цепочка:
1. Agent-style — проверяет стиль и форматирование
2. Agent-logic — ищет логические баги
3. Agent-security — ищет уязвимости
4. Agent-performance — ищет узкие места
Каждый видит комментарии предыдущих, не дублирует. Все дешёвые модели (Haiku/DeepSeek), но вместе дают качество Opus.
5.2 Team knowledge graph через skills SourceCraft-skills + MCP-серверы + durable state:
- Каждый skill фиксирует паттерн решения
- Skills сохраняются в корпоративный граф знаний через MCP
- Новый разработчик получает автоматически релевантные skills для своей задачи
Для Max'а: legal skills (german-legal-deadline-calculator + court-document-analyzer) становятся частью командного графа, доступны всем через SourceCraft CLI.
---
#### Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер
Родители:
- OpenClaude (habr.com/ru/articles/1018234/) — форк Claude Code с OpenAI-совместимым провайдером, можно подключить любую модель
- ZINC (habr.com/ru/articles/1020702/) — кастомный inference на Zig/Vulkan для Qwen3.5-35B-A3B
- MoME-роутер — из твоего YiJing-Transformer/pro2, Q6-гиперкуб, LCI метрика
Дети:
6.1 OpenClaude + ZINC + Q6-роутер = локальный агент с геометрическим выбором экспертов OpenClaude даёт агентские инструменты (bash, file ops, MCP). ZINC даёт быстрый локальный инференс. Добавляем MoME:
- Qwen3.5-35B-A3B разбита на 8 экспертов по Q6-вершинам
- Роутер выбирает эксперта по задаче геометрически
- Всё локально, никаких API-ключей
- LCI контролирует когерентность агента
Применение: legal AI на собственном железе без отправки данных наружу. GDPR-compliant, RISC-V-ready.
6.2 AutoResearch loop с геометрическим роутингом AutoResearch Карпатого + Q6-роутер + ZINC:
- Ночью агент крутит эксперименты с промптами
- Роутер геометрически выбирает, какой эксперт подходит для данного типа задач
- Лучший промпт сохраняется, LCI отслеживает стабильность
- Утром — отчёт о том, какие эксперты сработали лучше на каких задачах
---
#### Комбинация 7: Crawl4AI × Docling × Yodoca consolidator
Родители:
- Crawl4AI (habr.com/ru/articles/875088/) — open-source веб-скрейпинг для LLM, оптимизация для обучения моделей
- Docling (от IBM Research) — структурированный DoclingDocument, таблицы/параграфы как объекты
- Yodoca (habr.com/ru/articles/1006622/) — агент-консолидатор, ночные cron-задачи, Ebbinghaus decay
Дети:
7.1 Self-consolidating legal corpus Crawl4AI собирает новые решения Sozialgericht и BSG с сайтов. Docling парсит в структуру. Yodoca-консолидатор ночью:
- Извлекает durable knowledge (прецеденты, применённые статьи, аргументы)
- Старые неиспользуемые дела затухают по Эббингаузу
- Часто используемые — укрепляются
Результат: корпус сам поддерживает актуальность, не нужно вручную чистить старые дела.
7.2 Wikipedia-style legal knowledge base Crawl4AI + Docling + Yodoca + LLM Wiki (Obsidian плагин):
- Каждое новое решение → markdown-страница в Obsidian vault
- Консолидатор извлекает wikilinks между делами
- Graph view показывает связи между прецедентами
- Поиск через гибридный RAG (векторный + BM25 + graph traversal)
---
#### Комбинация 8: Conductor × adversarial-review × Auto AI Router
Родители:
- Conductor (habr.com/ru/articles/1001478/) — $2.8M от YC, macOS-native, управление параллельными Claude Code агентами, клиенты Linear/Vercel/Notion/Stripe
- adversarial-review (habr.com/ru/articles/1019588/) — Claude Opus пишет план/код, Codex CLI ревьюит, цикл до APPROVED/REVISE
- Auto AI Router — Go-прокси, маршрутизация между моделями
Дети:
8.1 Multi-model adversarial pipeline Conductor запускает 3 параллельных потока:
- Writer (Claude Opus): пишет код
- Reviewer 1 (GPT-5.4): проверяет логику
- Reviewer 2 (DeepSeek-V3.2): проверяет

<!-- similar-docs -->

---

**Похожие документы:**
- [05-benchmarks](05-benchmarks.md) (сходство 0.14)
- [03-local-first](03-local-first.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [05-benchmarks](05-benchmarks.md)
- [03-local-first](03-local-first.md)
- [01-agent-routing](01-agent-routing.md)
- [04-приоритетные-ансамбли](../04-ai-collaborations/04-приоритетные-ансамбли.md)

<!-- backlinks-auto -->
## Упоминается в

- [Local-first и P2P стек](03-local-first.md)
- [MemNet: исследовательская память](../05-habr-projects/memory/memnet.md)
- [Агентные системы и роутинг](01-agent-routing.md)
- [Бенчмарки и производительность](05-benchmarks.md)
- [Введение](../04-ai-collaborations/00-intro.md)
- [Комбинирование технологий для новых свойств](README.md)
## Упоминается в

- [Комбинирование технологий для новых свойств](../README.md)

<!-- related-auto -->
## Связанные документы

- [Local-first и P2P стек](03-local-first.md) _33%_
- [MemNet: исследовательская память](../05-habr-projects/memory/memnet.md) _25%_
- [Бенчмарки и производительность](05-benchmarks.md) _21%_
- [Введение](../04-ai-collaborations/00-intro.md) _17%_
## Связанные документы

- [Local-first и P2P стек](03-local-first.md) _29%_
- [Бенчмарки и производительность](05-benchmarks.md) _21%_
- [Введение](../04-ai-collaborations/00-intro.md) _21%_
- [MemNet: исследовательская память](../05-habr-projects/memory/memnet.md) _21%_
- [Тепловая карта тем](../HEATMAP.md) _17%_
- [Приоритеты файлов](../PRIORITIES.md) _17%_
