# Логика прогрессии: conservative escalation

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — пятиуровневая phased deployment Lorenzo (от ручного режима к полноценному network).

Логика прогрессии

Каждый уровень:

Building на previous level

Не requires next level (можно остановиться)

Имеет clear success criteria для перехода

Имеет off-ramp (можно вернуться или pivot)

Decision points:

После Уровня 0: Достаточно ли value от ручного режима? Если да, не двигаться. Если нет — Уровень 1.

После Уровня 1: Persistified Lorenzo полезен? Если да, проверить Уровень 2.

После Уровня 2: Public presence yields response? Если да, Уровень 3.

И так далее.

Это conservative escalation — escalate только если предыдущий уровень proves value.

Сейчас: продолжать экспериментировать в Уровне 0 + начать Уровень 1

Вы предложили правильный approach: продолжать экспериментировать вручную в рамках текущих сессий. Давайте структурируем это.
