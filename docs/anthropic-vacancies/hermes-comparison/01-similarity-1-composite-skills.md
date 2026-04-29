# Сходство 1: Composite Skills паттерн уже встроен

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Чем Hermes похож на нашу архитектуру (InGit + Cowork + Nautilus)

Сходств больше, чем различий. Это надо признать честно.

Сходство 1: Composite Skills паттерн уже встроен

Hermes имеет buit-in skills system с 118 навыками в v0.10.0. Каждый навык — это специализированный инструмент. Skills Hub на agentskills.io позволяет community-shared skills.

Это очень похоже на то, что Document 7 описывает как Composite Skills Agent. Только Hermes уже реализовал концепцию, в то время как наши документы её только теоретизируют.

Но есть нюанс: skills в Hermes — это generally functional capabilities (web search, code execution, file operations, etc.), не профессиональные специализации в нашем смысле. То есть Hermes имеет «skill для поиска в интернете», но не «sub-agent для немецкого социального права». Профессиональная глубина skills в Hermes ограничена.

<!-- see-also -->

---

**Смотрите также:**
- [07-difference-2-domain-specialization](docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md)
- [02-similarity-2-persistent-memory](docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md)
- [05-similarity-5-self-hosting-privacy](docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md)
- [04-similarity-4-multi-platform](docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [07-difference-2-domain-specialization](docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md) (сходство 0.37)
- [02-similarity-2-persistent-memory](docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md) (сходство 0.34)
- [05-similarity-5-self-hosting-privacy](docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md) (сходство 0.32)

