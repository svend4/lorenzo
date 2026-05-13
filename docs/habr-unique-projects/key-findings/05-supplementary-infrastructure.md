---
state: normalized
---

# Источник данных и инфраструктурные кусочки

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, Yodoca, NGT Memory, MemNet, Wikontic

---
<!-- tags: memory, orchestration, ingestion, architecture, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

В прошлом ответе я предложил «Svyazi 2.0 на хеббовском графе». Теперь схема проявляется конкретнее — каждый блок занят конкретным проектом:

— Слой эпизодической памяти → паттерн Yodoca (SQLite + FTS5 + hot/slow path);
— Консолидатор знаний → отдельный приватный LLM-агент в духе Yodoca, не виден основному Оркестратору;
— Хеббовские/STDP-связи между сущностями → NGT Memory + MemNet (на двух уровнях: приложения и обучаемой архитектуры);
— Архитектурный паттерн «LLM = периферия» → PDA из бота для самопознания, event sourcing над всем;
— Онтология и нормализация → Wikontic (вместо ручного synonyms.yml);
— Метрика качества структуры → K2-18 Романова;
— Дерево контекста → ByteRover (доменные markdown-файлы вместо плоского профиля);
— Источник сырых данных → tg-chat-analyser (паттерны из чатов сообщества);
— MCP-интерфейс наружу → Knowledge Graph Kit (любой агент работает с базой через MCP);
— Distributed-протокол агентов для модерации inferred-значений → Sequential от Дочкиной (8–16 малых агентов лучше одного большого).

Самое любопытное: если опуститься на уровень глубже, твой собственный YiJing-Transformer с Q6 + MoME ложится под всё это как движок. MoME-эксперты в Q6-гиперкубе могут соответствовать ByteRover-доменам (legal-эксперт, networking-эксперт, технический эксперт), а LCI (Lyapunov Coherence Index, π≈3.14) даёт измеримую метрику когерентности связей в графе — то, чего Чуяну явно не хватает. Это уже не просто «совместить три проекта», а полная вертикаль от трансформерной геометрии до приложения для нетворкинга, в которой каждый слой имеет автора-партнёра на Хабре.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Источник данных и инфраструктурные"
```

## Смотрите также
- 06-[svyazi-2-0-block-map](06-svyazi-2-0-block-map.md)
- [04-dochkina-sequential](04-dochkina-sequential.md)
- [02-related-projects](../analogues/02-related-projects.md)
- 5-tinyml-[mcp-skills](../hardware-pairs/5-tinyml-mcp-skills.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [05-supplementary-infrastructure](../../obsidian/habr-unique-projects/key-findings/05-supplementary-infrastructure.md) (сходство 0.96)
- [06-svyazi-2-0-block-map](06-svyazi-2-0-block-map.md) (сходство 0.31)
- [06-svyazi-2-0-block-map](../../obsidian/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md) (сходство 0.30)

