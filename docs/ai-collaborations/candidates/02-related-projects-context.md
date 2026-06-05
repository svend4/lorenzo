---
date: 2026-05-13
tags: [memory, rag, orchestration, ingestion, architecture]
state: approved
---

# Смежные проекты в контексте

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. Что из этого может слипнуться в один уникальный проект Если объединить эти подходы, получается одна штука, которой ещё ни у кого нет в open-source:
Если объединить эти подходы, получается одна штука, которой ещё ни у кого нет в open-source:
Локальная система обнаружения коллабораций на хеббовском графе людей-навыков-идей.
**Проекты:** Svyazi

---
<!-- tags: ingestion, architecture, self-improvement, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

«Программа поиска единомышленников ВКонтакте» (https://habr.com/ru/articles/495554/) — олдскульный аналог через анализ подписок, без LLM, но с той же концепцией matching по интересам. Полезна как контр-пример: показывает, чего не хватает без семантического слоя.

«Knowledge Graph Kit» Сэма Галлахера (Medium, не Хабр, но прямо в тему) — MCP-сервер с четырьмя типами узлов (Task/Note/Person/Project) и связями part_of/mentions/related_to, поверх SQLite + ChromaDB. По сути, минималистичный second brain, который любая LLM-агент может использовать через MCP. Это интерфейсный слой, которого Svyazi ещё не имеет.

«Анатомия ИИ-агента для подбора персонала» (https://habr.com/ru/companies/teamly/articles/1024062/) — про скоринг резюме, у которого есть обратная связь («кандидат прошёл/не прошёл»). Это закрывает дыру, на которую сам Чуян жалуется: «как сделать механизм обратной связи для самоулучшения промпта».

Что из этого может слипнуться в один уникальный проект
Если объединить эти подходы, получается одна штука, которой ещё ни у кого нет в open-source:

Локальная система обнаружения коллабораций на хеббовском графе людей-навыков-идей.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Смежные проекты в контексте"
```

## Смотрите также
- [02-related-projects](../../habr-unique-projects/analogues/02-related-projects.md)
- [01-three-key-candidates](01-three-key-candidates.md)
- [03-synthesis-hebbian-collaboration-graph](03-synthesis-hebbian-collaboration-graph.md)
- [01-yodoca](../../habr-unique-projects/key-findings/01-yodoca.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [01-three-key-candidates](01-three-key-candidates.md)
- [03-synthesis-hebbian-collaboration-graph](03-synthesis-hebbian-collaboration-graph.md)
- [README](README.md)
- _...ещё 2_


<!-- similar-docs -->

---

**Похожие документы:**
- [02-related-projects-context](../../obsidian/ai-collaborations/candidates/02-related-projects-context.md) (сходство 0.96)
- [02-related-projects](../../obsidian/habr-unique-projects/analogues/02-related-projects.md) (сходство 0.58)
- [02-related-projects](../../habr-unique-projects/analogues/02-related-projects.md) (сходство 0.57)

