# Различие 3: Federated knowledge architecture отсутствует

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Различие 3: Federated knowledge architecture отсутствует

Hermes — single-agent system per installation. Каждый пользователь имеет свой Hermes instance. Между instances нет federation.

Nautilus Portal Protocol specifically addresses federated queries across multiple repositories. Это совершенно другой architectural concern.

То есть для personal use Hermes сам по себе достаточен. Для federated knowledge work (multiple practitioners sharing patterns, OKWF guild structure), нужен Nautilus-like layer поверх Hermes.
