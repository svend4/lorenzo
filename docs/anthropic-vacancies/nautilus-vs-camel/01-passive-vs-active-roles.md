# Пассивный vs активный: разделение ролей (библиотека vs research team)

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

Сначала разделение ролей: пассивный vs активный

Вы точно identifuei разницу:

Nautilus — это passive coordination layer. Он собирает information across repositories, federates queries через Portal Protocol, но не executes ничего. Это infrastructure для discovery and federation, не для action. Метафора: библиотека с card catalog. Catalog tells вам где что находится, но не reads books для вас.

CAMEL — это active execution framework. Когда вы создаёте ChatAgent или RolePlaying setup, agents actively выполняют tasks: search the web, write code, analyze documents, coordinate с друг другом. Метафора: research team. Team actually does work.

Это complementary, не competing functions.

<!-- see-also -->

---

**Смотрите также:**
- [00-question-camel-vs-nautilus](docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md)
- [08-difference-3-federation-missing](docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md)
- [17-appendix-b-change-log](docs/nautilus/npp-v1-0/17-appendix-b-change-log.md)
- [03-sgb-advocate-colleague-example](docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)

