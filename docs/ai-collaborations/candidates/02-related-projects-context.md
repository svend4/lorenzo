# Смежные проекты в контексте

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi

---
<!-- tags: ingestion, architecture, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

«Программа поиска единомышленников ВКонтакте» (https://habr.com/ru/articles/495554/) — олдскульный аналог через анализ подписок, без LLM, но с той же концепцией matching по интересам. Полезна как контр-пример: показывает, чего не хватает без семантического слоя.

«Knowledge Graph Kit» Сэма Галлахера (Medium, не Хабр, но прямо в тему) — MCP-сервер с четырьмя типами узлов (Task/Note/Person/Project) и связями part_of/mentions/related_to, поверх SQLite + ChromaDB. По сути, минималистичный second brain, который любая LLM-агент может использовать через MCP. Это интерфейсный слой, которого Svyazi ещё не имеет.

«Анатомия ИИ-агента для подбора персонала» (https://habr.com/ru/companies/teamly/articles/1024062/) — про скоринг резюме, у которого есть обратная связь («кандидат прошёл/не прошёл»). Это закрывает дыру, на которую сам Чуян жалуется: «как сделать механизм обратной связи для самоулучшения промпта».

Что из этого может слипнуться в один уникальный проект
Если объединить эти подходы, получается одна штука, которой ещё ни у кого нет в open-source:

Локальная система обнаружения коллабораций на хеббовском графе людей-навыков-идей.

<!-- see-also -->

---

**Смотрите также:**
- [02-related-projects](docs/habr-unique-projects/analogues/02-related-projects.md)
- [01-three-key-candidates](docs/ai-collaborations/candidates/01-three-key-candidates.md)
- [03-synthesis-hebbian-collaboration-graph](docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md)
- [01-yodoca](docs/habr-unique-projects/key-findings/01-yodoca.md)

