# Письмо: AnastasiyaW / knowledge-space + mclaude

<!-- toc-auto -->

<!-- summary -->
> Открытое письмо автору knowledge-space и mclaude — карточной базы знаний и системы координации параллельных Claude-агентов.

<!-- tags: contacts, letters, knowledge-space, mclaude, orchestration, knowledge -->

> [!NOTE]
> Черновик письма. Не обязательно отправлять в точности — можно дать ссылку
> на этот документ как «я изучил ваш проект, вот что думаю».

---

**Кому:** AnastasiyaW
**Проекты:** [knowledge-space](../05-habr-projects/knowledge/knowledge-space.md), [mclaude](../05-habr-projects/knowledge/mclaude.md)
**Платформа:** GitHub / Habr
**Приоритет:** ★★★ (111 упоминаний в репо — наибольший охват)

---

## Письмо

Здравствуйте!

Я строю Svyazi 2.0 — локальный Knowledge OS, который собирает знания из документов
и связывает их с людьми, проектами и идеями. Изучая Habr-проекты по теме памяти
и организации знаний для агентов, я обнаружил, что два ваших проекта — knowledge-space
и mclaude — закрывают два принципиально разных уровня архитектуры, которые у меня
сейчас реализованы по отдельности и с трением между ними.

**Про knowledge-space:**

785+ карточек по AI/ML — это уже не просто база знаний, это бенчмарк для
карточной архитектуры. Меня интересует не содержание, а структура: как вы
разделяете reference cards (что-то есть) от operational cards (как что-то делать)?
В Svyazi я использую `CardEnvelope` с полем `type: fact|project|person|episode` —
но вопрос операциональных карточек (gotcha, benchmark, known-bad) пока не решён.

**Про mclaude:**

Механизм locks + handoffs + mailbox — это именно то, чего не хватает для работы
нескольких агентов над одним графом без конфликтов. Shared project memory в mclaude
семантически очень близка к CardStore в Svyazi — оба объекта хранят «общее знание
проекта», но с разными контрактами.

**Один вопрос, который меня останавливает:**

Держать operational benchmark/gotcha cards в одной базе с reference cards или
в отдельном слое? В knowledge-space, насколько я понял, всё в одном пространстве —
но как вы разграничиваете «что истинно» от «что сработало в этом контексте»?

**Что я готов предложить:**

- Детальное описание того, как knowledge-space + mclaude образуют связку
  «база знаний + координация» в Svyazi 2.0 (уже задокументировано)
- Обсуждение, как `CardEnvelope` из PROTOTYPE_SPEC соотносится с форматом
  карточек knowledge-space — возможно, контракт уже совместим
- Если интересно — показать, как mclaude-locks ложатся на
  `SkillPolicy(approval_mode)` в архитектуре Svyazi

---

_Черновик подготовлен: 2026-05-11_
_Связанный контакт: [contacts/anastasiyaw.md](../contacts/anastasiyaw.md)_


## Использование
```bash
# Запуск
python scripts/improve_anastasiyaw.py
```
