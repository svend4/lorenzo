# Различие 1: Структурированная подложка отсутствует

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Различие 1: Структурированная подложка отсутствует

Hermes не imposes структуру на ваши файлы и проекты. Каждый пользователь хранит данные как ему удобно. Hermes adapts to whatever структура есть.

InGit specifically provides структуру (00_inbox через 90_exports, YAML metadata schemas). Это:

Делает кросс-проектное сравнение возможным

Стандартизирует team collaboration (когда станет доступным)

Обеспечивает predictable patterns для Hermes (или Cowork) к работе с

Делает migration между systems easier

То есть InGit + Hermes могло бы быть лучшей комбинацией, чем Hermes alone. Hermes как агентский слой, InGit как структурный слой. Точно так же, как InGit + Cowork.
