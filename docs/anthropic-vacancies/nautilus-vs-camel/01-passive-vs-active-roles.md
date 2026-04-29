# Пассивный vs активный: разделение ролей (библиотека vs research team)

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

Сначала разделение ролей: пассивный vs активный

Вы точно identifuei разницу:

Nautilus — это passive coordination layer. Он собирает information across repositories, federates queries через Portal Protocol, но не executes ничего. Это infrastructure для discovery and federation, не для action. Метафора: библиотека с card catalog. Catalog tells вам где что находится, но не reads books для вас.

CAMEL — это active execution framework. Когда вы создаёте ChatAgent или RolePlaying setup, agents actively выполняют tasks: search the web, write code, analyze documents, coordinate с друг другом. Метафора: research team. Team actually does work.

Это complementary, не competing functions.
