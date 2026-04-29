# Сходство 1: Composite Skills паттерн уже встроен

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Чем Hermes похож на нашу архитектуру (InGit + Cowork + Nautilus)

Сходств больше, чем различий. Это надо признать честно.

Сходство 1: Composite Skills паттерн уже встроен

Hermes имеет buit-in skills system с 118 навыками в v0.10.0. Каждый навык — это специализированный инструмент. Skills Hub на agentskills.io позволяет community-shared skills.

Это очень похоже на то, что Document 7 описывает как Composite Skills Agent. Только Hermes уже реализовал концепцию, в то время как наши документы её только теоретизируют.

Но есть нюанс: skills в Hermes — это generally functional capabilities (web search, code execution, file operations, etc.), не профессиональные специализации в нашем смысле. То есть Hermes имеет «skill для поиска в интернете», но не «sub-agent для немецкого социального права». Профессиональная глубина skills в Hermes ограничена.
