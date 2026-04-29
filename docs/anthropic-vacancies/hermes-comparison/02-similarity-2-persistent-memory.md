# Сходство 2: Persistent memory — Layer B функциональность

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Сходство 2: Persistent memory — Layer B функциональность

Hermes имеет three-layer memory: FTS5 search, LLM summarization, Honcho user modeling. Это substantially решает многие из тех проблем, которые Document 2.3 идентифицировал как Layer B gap.

Cowork также имеет persistent memory, но Hermes идёт дальше — autonomous skill creation означает, что агент сам определяет, что worth remembering, без явного указания пользователя.
