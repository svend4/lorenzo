# ai-managed-virtual-company/ — анализ идеи разделить $500K на команду

В диалоге пользователь предложил радикальную модель: вместо найма одного «суперчеловека» за полмиллиона долларов в год, разделить эту сумму на 5–10 распределённых фрилансеров и собрать их вместе через AI-агента — «как группу супергероев, ангел-хранитель собирает их по всему миру». Claude развернул анализ.

| # | Раздел | Файл |
|---|---|---|
| — | Вопрос: разделить $500K на команду | [`00-question-rephrasing.md`](00-question-rephrasing.md) |
| 1 | Что уже существует (InnoCentive, Kaggle, Toptal, Fellows, DAOs) | [`01-existing-landscape.md`](01-existing-landscape.md) |
| 2 | Четыре структурные причины почему это не работает | [`02-four-structural-blockers.md`](02-four-structural-blockers.md) |
| 3 | Три варианта: A → B → C (AI-managed virtual company) | [`03-three-variants-A-B-C.md`](03-three-variants-A-B-C.md) |
| 4 | Что с этим делать | [`04-what-to-do.md`](04-what-to-do.md) |
| 5 | Сравнение с Terence Tao, Polymath Project | [`05-polymath-project-tao-comparison.md`](05-polymath-project-tao-comparison.md) |
| 6 | Двойственность «ангел-хранитель + строгий демон» | [`06-angel-vs-demon-duality.md`](06-angel-vs-demon-duality.md) |
| 7 | Что существует сейчас (MetaGPT, ChatDev, CrewAI, AutoGen) | [`07-current-implementations.md`](07-current-implementations.md) |
| 8 | Плюсы модели если её построить | [`08-pluses-of-model.md`](08-pluses-of-model.md) |
| 9 | Минусы и риски | [`09-minuses-and-risks.md`](09-minuses-and-risks.md) |
| 10 | Три точки входа разной амбиции | [`10-three-entry-points.md`](10-three-entry-points.md) |

## Главный вывод

Существуют три варианта реализуемости:

- **Вариант A** (слабый): AI-powered staffing agency — ускорение Toptal/Braintrust, ~20-30% efficiency gain.
- **Вариант B** (средний): AI-orchestrated research consortium с bounty prize — расширенная InnoCentive с многокомандным режимом.
- **Вариант C** (сильный, прорывной): **AI-managed distributed virtual company** — AI-агент управляет ad hoc-командой 6–12 месяцев. Это именно то, что описал пользователь, и это **ещё не построено в масштабе**. Ближайшие эксперименты: MetaGPT, ChatDev, CrewAI, AutoGen — но все имитируют роли, не управляют реальными людьми.

## Четыре структурных blocker'а

1. Legal/compliance nightmare через границы (5 юрисдикций → compliance-расходы выше проекта).
2. Trust/coordination problem между незнакомцами (25-40% времени проекта — Herbsleb/Grinter/Olson).
3. Incentive misalignment под fixed prize pool (free-riding в co-op contracts).
4. Ownership невнятная (legal frameworks не отвечают дёшево).
