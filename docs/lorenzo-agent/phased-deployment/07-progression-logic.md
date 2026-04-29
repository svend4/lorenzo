# Логика прогрессии: conservative escalation

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — пятиуровневая phased deployment Lorenzo (от ручного режима к полноценному network).

---
<!-- tags: roadmap, anthropic -->




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

<!-- see-also -->

---

**Смотрите также:**
- [00-overview](docs/lorenzo-agent/phased-deployment/00-overview.md)
- [01-level-0-manual](docs/lorenzo-agent/phased-deployment/01-level-0-manual.md)
- [06-level-5-full-network](docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md)
- [03-level-2-basic-lite](docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md)

