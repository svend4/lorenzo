# Четыре структурные причины, почему это не работает в текущих попытках

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ идеи AI-managed distributed virtual company как альтернативы найму одного человека з

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ идеи AI-managed distributed virtual company как альтернативы найму одного человека за высокую зарплату.

Почему это не работает в текущих попытках

Четыре структурные причины.

Первая — legal/compliance nightmare через границы. Пять фрилансеров в пяти странах получают деньги от компании — это пять юрисдикций, пять налоговых режимов, пять санкционных списков для проверки, пять версий IP-ownership, пять правил exit-clauses. Корпорация типа Anthropic не может просто так разослать $100K в Дрезден, Буэнос-Айрес, Лагос, Киев и Бангалор — её compliance-отдел затратит больше, чем стоит сам проект. Это главная причина, почему корпорации нанимают в штат, а не собирают команды фрилансеров: штатный сотрудник — одно юр.лицо, один контракт. Фриланс-команда — пять контрактов и пять точек отказа.

Вторая — trust/coordination problem между незнакомцами. Пять человек, которые не знают друг друга, будут тратить первые 2-3 месяца на выстраивание взаимопонимания и распределения ответственности. Это известный факт из research по distributed software teams (Herbsleb, Grinter, Olson) — temporal coordination cost между незнакомцами в среднем 25-40% времени проекта. AI-агент может помочь с матчингом, но не может заменить время, нужное людям, чтобы начать доверять друг другу в условиях высокой неопределённости задачи.

Третья — incentive misalignment под fixed prize pool. Если пять человек делят $500K, каждый из них рационально не хочет быть тем, кто делает 40% работы. Начинается free-riding или, наоборот, перенапряжение ответственных. Это проблема классических co-op contracts, хорошо изученная в experimental economics. Без сильной внешней модерации (как раз AI-агента с authority) распадается.

Четвёртая — ownership невнятная. Кому принадлежит результат? Если команда собрана ad hoc под миссию, кто владеет IP — AI-платформа, заказчик, сами фрилансеры? Сегодняшние legal frameworks не умеют отвечать на этот вопрос дёшево.

<!-- see-also -->

---

**Смотрите также:**
- [08-pluses-of-model](docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md)
- [07-current-implementations](docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md)
- [01-existing-landscape](docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md)
- [09-minuses-and-risks](docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md)

